"""Pydantic schemas for Ranking API response DTOs."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RankingResponse(BaseModel):
    """Response DTO for a single ranking entry."""
    id: str
    job_id: str
    candidate_id: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    semantic_score: float
    skill_score: float
    overall_score: float
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    explanation: Optional[str] = None
    rank: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RankingListResponse(BaseModel):
    """Response DTO for listing rankings for a job."""
    job_id: str
    job_title: Optional[str] = None
    rankings: List[RankingResponse]
    total: int
