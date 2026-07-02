"""Candidate service — business logic for uploading, parsing, and managing candidates."""

import json
import os
import uuid
from pathlib import Path
from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.ai.embeddings import EmbeddingEngine
from app.ai.resume_parser import ResumeParser
from app.ai.ner import NERExtractor
from app.core.config import settings


class CandidateService:
    """Service layer for Candidate operations."""

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        ner_extractor: NERExtractor,
    ) -> None:
        self.embedding_engine = embedding_engine
        self.ner_extractor = ner_extractor
        self.parser = ResumeParser()

    async def upload_resume(
        self,
        session: AsyncSession,
        filename: str,
        file_content: bytes,
    ) -> Candidate:
        """Upload, parse, and process a single resume file.

        Steps:
            1. Save file to uploads/
            2. Extract text from PDF/DOCX
            3. Parse structured data (name, email, phone, experience, education)
            4. Extract skills via NER
            5. Generate embedding
            6. Store in database
        """
        # 1. Save file to disk
        candidate_id = str(uuid.uuid4())
        safe_filename = f"{candidate_id}_{filename}"
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / safe_filename

        with open(file_path, "wb") as f:
            f.write(file_content)

        try:
            # 2 & 3. Parse resume
            parsed = self.parser.parse(str(file_path))

            # 4. Extract skills
            skills = self.ner_extractor.extract_skills(parsed["raw_text"])

            # Infer experience level for later use in ranking
            exp_level = self.ner_extractor.extract_experience_level(parsed["raw_text"])

            # 5. Generate embedding
            embedding = self.embedding_engine.encode(parsed["raw_text"])
            embedding_bytes = EmbeddingEngine.to_bytes(embedding)

            # 6. Create candidate record
            candidate = Candidate(
                id=candidate_id,
                name=parsed.get("name", "Unknown Candidate"),
                email=parsed.get("email"),
                phone=parsed.get("phone"),
                resume_path=str(file_path),
                raw_text=parsed["raw_text"],
                skills=json.dumps(skills),
                experience=json.dumps(parsed.get("experience", [])),
                education=json.dumps(parsed.get("education", [])),
                embedding=embedding_bytes,
            )

            session.add(candidate)
            await session.flush()
            return candidate

        except Exception:
            # Clean up file if processing fails
            if file_path.exists():
                os.remove(file_path)
            raise

    async def get_candidate(
        self,
        session: AsyncSession,
        candidate_id: str,
    ) -> Optional[Candidate]:
        """Retrieve a single candidate by ID."""
        result = await session.execute(
            select(Candidate).where(Candidate.id == candidate_id)
        )
        return result.scalar_one_or_none()

    async def list_candidates(self, session: AsyncSession) -> List[Candidate]:
        """Retrieve all candidates ordered by creation date (newest first)."""
        result = await session.execute(
            select(Candidate).order_by(Candidate.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete_candidate(
        self,
        session: AsyncSession,
        candidate_id: str,
    ) -> bool:
        """Delete a candidate by ID. Also removes the uploaded resume file.

        Returns True if deleted, False if not found.
        """
        # First, get the candidate to find the resume path
        candidate = await self.get_candidate(session, candidate_id)
        if not candidate:
            return False

        # Delete the file if it exists
        if candidate.resume_path:
            resume_path = Path(candidate.resume_path)
            if resume_path.exists():
                os.remove(resume_path)

        # Delete from database
        await session.execute(
            delete(Candidate).where(Candidate.id == candidate_id)
        )
        return True
