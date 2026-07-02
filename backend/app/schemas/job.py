"""Pydantic schemas for Job API request/response DTOs."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class JobCreate(BaseModel):
    """Request body for creating a job."""
    title: str = Field(..., min_length=1, max_length=500, description="Job title")
    description: str = Field(..., min_length=10, description="Full job description text")


class JobResponse(BaseModel):
    """Response DTO for a single job."""
    id: str
    title: str
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_level: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    """Response DTO for listing jobs."""
    jobs: List[JobResponse]
    total: int
