"""Pydantic schemas for Candidate API request/response DTOs."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CandidateResponse(BaseModel):
    """Response DTO for a single candidate."""
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    resume_path: Optional[str] = None
    skills: List[str] = []
    experience: List[str] = []
    education: List[str] = []
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CandidateListResponse(BaseModel):
    """Response DTO for listing candidates."""
    candidates: List[CandidateResponse]
    total: int
