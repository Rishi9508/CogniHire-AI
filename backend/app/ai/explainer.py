"""Explanation generator for ranking results.

Produces human-readable natural language summaries explaining
why a candidate was ranked at a particular position, including
score breakdowns, matched/missing skills, and actionable insights.
"""

from typing import Dict, List


class Explainer:
    """Generate natural language explanations for ranking results."""

    @staticmethod
    def generate_explanation(
        candidate_name: str,
        rank: int,
        total_candidates: int,
        semantic_score: float,
        skill_score: float,
        experience_score: float,
        overall_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
    ) -> str:
        """Generate a natural language explanation for a candidate's ranking.

        Args:
            candidate_name: Name of the candidate.
            rank: Candidate's rank (1-indexed).
            total_candidates: Total number of candidates ranked.
            semantic_score: Cosine similarity score.
            skill_score: Skill overlap score.
            experience_score: Experience match score.
            overall_score: Weighted overall score.
            matched_skills: Skills that matched.
            missing_skills: Skills that are missing.

        Returns:
            Multi-sentence explanation string.
        """
        parts: List[str] = []

        # Rank summary
        parts.append(
            f"{candidate_name} is ranked #{rank} out of {total_candidates} "
            f"candidate{'s' if total_candidates != 1 else ''} with an overall "
            f"match score of {overall_score:.0%}."
        )

        # Semantic analysis
        if semantic_score >= 0.7:
            parts.append(
                f"The resume shows strong semantic alignment with the job description "
                f"(semantic similarity: {semantic_score:.0%})."
            )
        elif semantic_score >= 0.4:
            parts.append(
                f"The resume has moderate semantic alignment with the job description "
                f"(semantic similarity: {semantic_score:.0%})."
            )
        else:
            parts.append(
                f"The resume has limited semantic alignment with the job description "
                f"(semantic similarity: {semantic_score:.0%})."
            )

        # Skills analysis
        if matched_skills:
            skills_str = ", ".join(matched_skills[:10])
            parts.append(
                f"Matched {len(matched_skills)} required skill{'s' if len(matched_skills) != 1 else ''}: "
                f"{skills_str}."
            )
        else:
            parts.append("No direct skill matches were found with the required skills.")

        if missing_skills:
            missing_str = ", ".join(missing_skills[:10])
            parts.append(
                f"Missing {len(missing_skills)} required skill{'s' if len(missing_skills) != 1 else ''}: "
                f"{missing_str}."
            )

        # Experience analysis
        if experience_score >= 1.0:
            parts.append("Experience level is an exact match for this role.")
        elif experience_score >= 0.5:
            parts.append("Experience level is close to the job requirements.")
        else:
            parts.append(
                "Experience level does not closely match the job requirements."
            )

        # Recommendation
        if overall_score >= 0.75:
            parts.append("Strong recommendation: this candidate is a very good fit.")
        elif overall_score >= 0.50:
            parts.append(
                "Moderate recommendation: this candidate is worth considering."
            )
        elif overall_score >= 0.30:
            parts.append(
                "Weak recommendation: this candidate partially matches the requirements."
            )
        else:
            parts.append(
                "Not recommended: this candidate does not match the requirements well."
            )

        return " ".join(parts)

    @staticmethod
    def generate_score_breakdown(
        semantic_score: float,
        skill_score: float,
        experience_score: float,
        overall_score: float,
    ) -> Dict:
        """Generate a structured score breakdown.

        Returns:
            Dict with formatted score components and weights.
        """
        return {
            "semantic": {
                "score": round(semantic_score, 4),
                "weight": 0.60,
                "weighted_contribution": round(0.60 * semantic_score, 4),
                "label": "Resume-JD Semantic Similarity",
            },
            "skill": {
                "score": round(skill_score, 4),
                "weight": 0.30,
                "weighted_contribution": round(0.30 * skill_score, 4),
                "label": "Skill Match Coverage",
            },
            "experience": {
                "score": round(experience_score, 4),
                "weight": 0.10,
                "weighted_contribution": round(0.10 * experience_score, 4),
                "label": "Experience Level Match",
            },
            "overall": {
                "score": round(overall_score, 4),
                "label": "Overall Match Score",
            },
        }
