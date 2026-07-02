"""Jobs API router — CRUD endpoints for job descriptions."""

import json

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.job import JobCreate, JobResponse, JobListResponse


router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


def _job_to_response(job) -> JobResponse:
    """Convert a Job ORM instance to a JobResponse schema."""
    return JobResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        required_skills=json.loads(job.required_skills) if job.required_skills else [],
        preferred_skills=json.loads(job.preferred_skills) if job.preferred_skills else [],
        experience_level=job.experience_level,
        created_at=job.created_at,
    )


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(
    body: JobCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Create a new job posting.

    Automatically extracts required skills, experience level,
    and generates a semantic embedding from the description.
    """
    job_service = request.app.state.job_service
    try:
        job = await job_service.create_job(session, body.title, body.description)
        return _job_to_response(job)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("", response_model=JobListResponse)
async def list_jobs(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """List all jobs, newest first."""
    job_service = request.app.state.job_service
    jobs = await job_service.list_jobs(session)
    return JobListResponse(
        jobs=[_job_to_response(j) for j in jobs],
        total=len(jobs),
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get a single job by ID."""
    job_service = request.app.state.job_service
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_to_response(job)


@router.delete("/{job_id}", status_code=200)
async def delete_job(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Delete a job by ID."""
    job_service = request.app.state.job_service
    deleted = await job_service.delete_job(session, job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully", "id": job_id}
