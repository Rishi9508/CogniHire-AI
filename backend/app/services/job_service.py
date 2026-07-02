"""Job service — business logic for creating, reading, and deleting jobs."""

import json
import uuid
from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.ai.embeddings import EmbeddingEngine
from app.ai.ner import NERExtractor


class JobService:
    """Service layer for Job operations."""

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        ner_extractor: NERExtractor,
    ) -> None:
        self.embedding_engine = embedding_engine
        self.ner_extractor = ner_extractor

    async def create_job(
        self,
        session: AsyncSession,
        title: str,
        description: str,
    ) -> Job:
        """Create a new job from title and description text.

        Automatically extracts skills, experience level, and generates
        the embedding vector.
        """
        # Extract skills and experience level using NER
        ner_results = self.ner_extractor.extract_all(description)
        required_skills = ner_results["skills"]
        experience_level = ner_results["experience_level"]

        # Also extract skills from the title and merge
        title_skills = self.ner_extractor.extract_skills(title)
        all_skills = sorted(set(required_skills + title_skills))

        # Generate embedding from the full job description
        embedding = self.embedding_engine.encode(f"{title}\n{description}")
        embedding_bytes = EmbeddingEngine.to_bytes(embedding)

        job = Job(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            required_skills=json.dumps(all_skills),
            preferred_skills=json.dumps([]),
            experience_level=experience_level,
            embedding=embedding_bytes,
        )

        session.add(job)
        await session.flush()
        return job

    async def get_job(
        self,
        session: AsyncSession,
        job_id: str,
    ) -> Optional[Job]:
        """Retrieve a single job by ID."""
        result = await session.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()

    async def list_jobs(self, session: AsyncSession) -> List[Job]:
        """Retrieve all jobs ordered by creation date (newest first)."""
        result = await session.execute(
            select(Job).order_by(Job.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete_job(
        self,
        session: AsyncSession,
        job_id: str,
    ) -> bool:
        """Delete a job by ID. Returns True if deleted, False if not found."""
        result = await session.execute(delete(Job).where(Job.id == job_id))
        return result.rowcount > 0
