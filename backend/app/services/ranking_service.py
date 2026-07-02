"""Ranking service — orchestrates the full AI ranking pipeline."""

import json
import uuid
from typing import Dict, List, Optional

import numpy as np
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.candidate import Candidate
from app.models.ranking import Ranking
from app.ai.embeddings import EmbeddingEngine
from app.ai.ner import NERExtractor
from app.ai.semantic_ranker import SemanticRanker
from app.ai.explainer import Explainer


class RankingService:
    """Service layer for computing and retrieving candidate rankings."""

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        ner_extractor: NERExtractor,
    ) -> None:
        self.embedding_engine = embedding_engine
        self.ner_extractor = ner_extractor
        self.ranker = SemanticRanker(embedding_engine, ner_extractor)
        self.explainer = Explainer()

    async def compute_rankings(
        self,
        session: AsyncSession,
        job_id: str,
    ) -> List[Ranking]:
        """Compute and store rankings for all candidates against a job.

        Steps:
            1. Load the job and all candidates
            2. Delete any existing rankings for this job
            3. Run the semantic ranker on all candidates
            4. Generate explanations for each ranking
            5. Store rankings in the database
        """
        # 1. Load job
        job_result = await session.execute(select(Job).where(Job.id == job_id))
        job = job_result.scalar_one_or_none()
        if not job:
            raise ValueError(f"Job not found: {job_id}")

        # Load all candidates
        candidates_result = await session.execute(select(Candidate))
        candidates = list(candidates_result.scalars().all())

        if not candidates:
            raise ValueError("No candidates found to rank")

        # 2. Delete existing rankings for this job
        await session.execute(delete(Ranking).where(Ranking.job_id == job_id))

        # Prepare job data
        job_embedding = EmbeddingEngine.from_bytes(job.embedding)
        required_skills = json.loads(job.required_skills) if job.required_skills else []
        job_experience_level = job.experience_level or "unknown"

        # Prepare candidate data
        candidate_data: List[Dict] = []
        candidate_map: Dict[str, Candidate] = {}

        for c in candidates:
            if not c.embedding:
                continue

            c_embedding = EmbeddingEngine.from_bytes(c.embedding)
            c_skills = json.loads(c.skills) if c.skills else []
            c_exp = self.ner_extractor.extract_experience_level(
                c.raw_text or ""
            )

            candidate_data.append({
                "id": c.id,
                "embedding": c_embedding,
                "skills": c_skills,
                "experience_level": c_exp,
            })
            candidate_map[c.id] = c

        if not candidate_data:
            raise ValueError("No candidates with valid embeddings found")

        # 3. Run the ranker
        ranking_results = self.ranker.rank_candidates(
            job_embedding=job_embedding,
            required_skills=required_skills,
            job_experience_level=job_experience_level,
            candidates=candidate_data,
        )

        # 4 & 5. Generate explanations and store
        ranking_objects: List[Ranking] = []
        total_candidates = len(ranking_results)

        for result in ranking_results:
            candidate = candidate_map[result["candidate_id"]]

            explanation = self.explainer.generate_explanation(
                candidate_name=candidate.name,
                rank=result["rank"],
                total_candidates=total_candidates,
                semantic_score=result["semantic_score"],
                skill_score=result["skill_score"],
                experience_score=result["experience_score"],
                overall_score=result["overall_score"],
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
            )

            ranking = Ranking(
                id=str(uuid.uuid4()),
                job_id=job_id,
                candidate_id=result["candidate_id"],
                semantic_score=result["semantic_score"],
                skill_score=result["skill_score"],
                overall_score=result["overall_score"],
                matched_skills=json.dumps(result["matched_skills"]),
                missing_skills=json.dumps(result["missing_skills"]),
                explanation=explanation,
                rank=result["rank"],
            )

            session.add(ranking)
            ranking_objects.append(ranking)

        await session.flush()
        return ranking_objects

    async def get_rankings(
        self,
        session: AsyncSession,
        job_id: str,
    ) -> List[Dict]:
        """Retrieve cached rankings for a job, enriched with candidate info.

        Returns list of dicts with ranking data + candidate_name and candidate_email.
        """
        result = await session.execute(
            select(Ranking)
            .where(Ranking.job_id == job_id)
            .order_by(Ranking.rank)
        )
        rankings = list(result.scalars().all())

        enriched: List[Dict] = []
        for r in rankings:
            # Look up candidate info
            c_result = await session.execute(
                select(Candidate).where(Candidate.id == r.candidate_id)
            )
            candidate = c_result.scalar_one_or_none()

            enriched.append({
                "id": r.id,
                "job_id": r.job_id,
                "candidate_id": r.candidate_id,
                "candidate_name": candidate.name if candidate else "Unknown",
                "candidate_email": candidate.email if candidate else None,
                "semantic_score": r.semantic_score,
                "skill_score": r.skill_score,
                "overall_score": r.overall_score,
                "matched_skills": json.loads(r.matched_skills) if r.matched_skills else [],
                "missing_skills": json.loads(r.missing_skills) if r.missing_skills else [],
                "explanation": r.explanation,
                "rank": r.rank,
                "created_at": r.created_at,
            })

        return enriched
