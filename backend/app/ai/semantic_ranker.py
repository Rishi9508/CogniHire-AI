"""Semantic ranker implementing the hybrid scoring formula.

Scoring formula:
    overall = 0.60 * semantic_score + 0.30 * skill_score + 0.10 * experience_score

Where:
    - semantic_score: cosine similarity between JD and resume embeddings
    - skill_score: |matched_skills| / max(|required_skills|, 1)
    - experience_score: 1.0 (exact), 0.5 (adjacent), 0.0 (mismatch)
"""

from typing import Dict, List, Set, Tuple

import numpy as np

from app.ai.embeddings import EmbeddingEngine
from app.ai.ner import NERExtractor


# Scoring weights
WEIGHT_SEMANTIC = 0.60
WEIGHT_SKILL = 0.30
WEIGHT_EXPERIENCE = 0.10


class SemanticRanker:
    """Rank candidates against a job using hybrid semantic + skill scoring."""

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        ner_extractor: NERExtractor,
    ) -> None:
        self.embedding_engine = embedding_engine
        self.ner_extractor = ner_extractor

    def compute_skill_overlap(
        self,
        required_skills: List[str],
        candidate_skills: List[str],
    ) -> Tuple[List[str], List[str], float]:
        """Compute skill overlap between job requirements and candidate skills.

        Args:
            required_skills: Skills required by the job.
            candidate_skills: Skills the candidate has.

        Returns:
            Tuple of (matched_skills, missing_skills, skill_score).
        """
        required_set: Set[str] = {s.lower() for s in required_skills}
        candidate_set: Set[str] = {s.lower() for s in candidate_skills}

        matched_lower = required_set & candidate_set
        missing_lower = required_set - candidate_set

        # Map back to original casing from required_skills
        req_map = {s.lower(): s for s in required_skills}
        matched = sorted([req_map[m] for m in matched_lower])
        missing = sorted([req_map[m] for m in missing_lower])

        denominator = max(len(required_skills), 1)
        skill_score = len(matched) / denominator

        return matched, missing, min(skill_score, 1.0)

    def rank_candidate(
        self,
        job_embedding: np.ndarray,
        candidate_embedding: np.ndarray,
        required_skills: List[str],
        candidate_skills: List[str],
        job_experience_level: str,
        candidate_experience_level: str,
    ) -> Dict:
        """Score a single candidate against a job.

        Returns:
            Dict with semantic_score, skill_score, experience_score,
            overall_score, matched_skills, missing_skills.
        """
        # 1. Semantic similarity
        semantic_score = self.embedding_engine.cosine_similarity(
            job_embedding, candidate_embedding
        )

        # 2. Skill overlap
        matched_skills, missing_skills, skill_score = self.compute_skill_overlap(
            required_skills, candidate_skills
        )

        # 3. Experience match
        experience_score = NERExtractor.compute_experience_score(
            job_experience_level, candidate_experience_level
        )

        # 4. Weighted overall score
        overall_score = (
            WEIGHT_SEMANTIC * semantic_score
            + WEIGHT_SKILL * skill_score
            + WEIGHT_EXPERIENCE * experience_score
        )

        return {
            "semantic_score": round(semantic_score, 4),
            "skill_score": round(skill_score, 4),
            "experience_score": round(experience_score, 4),
            "overall_score": round(overall_score, 4),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }

    def rank_candidates(
        self,
        job_embedding: np.ndarray,
        required_skills: List[str],
        job_experience_level: str,
        candidates: List[Dict],
    ) -> List[Dict]:
        """Rank multiple candidates against a job.

        Args:
            job_embedding: The job's embedding vector.
            required_skills: Skills required by the job.
            job_experience_level: Experience level of the job.
            candidates: List of dicts with 'id', 'embedding', 'skills',
                        'experience_level' keys.

        Returns:
            List of ranking dicts sorted by overall_score (descending),
            each augmented with 'candidate_id' and 'rank'.
        """
        results: List[Dict] = []

        for candidate in candidates:
            candidate_embedding = candidate["embedding"]
            candidate_skills = candidate.get("skills", [])
            candidate_exp = candidate.get("experience_level", "unknown")

            ranking = self.rank_candidate(
                job_embedding=job_embedding,
                candidate_embedding=candidate_embedding,
                required_skills=required_skills,
                candidate_skills=candidate_skills,
                job_experience_level=job_experience_level,
                candidate_experience_level=candidate_exp,
            )
            ranking["candidate_id"] = candidate["id"]
            results.append(ranking)

        # Sort by overall score descending
        results.sort(key=lambda x: x["overall_score"], reverse=True)

        # Assign ranks (1-indexed)
        for i, r in enumerate(results):
            r["rank"] = i + 1

        return results
