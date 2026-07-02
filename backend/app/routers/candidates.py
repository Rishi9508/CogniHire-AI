"""Candidates API router — upload resumes and manage candidates."""

import json
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.candidate import CandidateResponse, CandidateListResponse


router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _candidate_to_response(candidate) -> CandidateResponse:
    """Convert a Candidate ORM instance to a CandidateResponse schema."""
    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        resume_path=candidate.resume_path,
        skills=json.loads(candidate.skills) if candidate.skills else [],
        experience=json.loads(candidate.experience) if candidate.experience else [],
        education=json.loads(candidate.education) if candidate.education else [],
        created_at=candidate.created_at,
    )


def _validate_file(file: UploadFile) -> None:
    """Validate uploaded file extension."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a filename")

    # Check extension
    filename_lower = file.filename.lower()
    if not any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )


@router.post("/upload", response_model=List[CandidateResponse], status_code=201)
async def upload_resumes(
    request: Request,
    files: List[UploadFile] = File(..., description="Resume files (PDF or DOCX)"),
    session: AsyncSession = Depends(get_session),
):
    """Upload one or more resume files.

    Each file is parsed, skills are extracted, and an embedding is generated.
    Supports PDF and DOCX formats.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    candidate_service = request.app.state.candidate_service
    results: List[CandidateResponse] = []
    errors: List[str] = []

    for file in files:
        try:
            _validate_file(file)

            # Read file content
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                errors.append(f"{file.filename}: File too large (max 10MB)")
                continue

            if len(content) == 0:
                errors.append(f"{file.filename}: File is empty")
                continue

            # Process the resume
            candidate = await candidate_service.upload_resume(
                session, file.filename, content
            )
            results.append(_candidate_to_response(candidate))

        except HTTPException:
            raise
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    if not results and errors:
        raise HTTPException(
            status_code=400,
            detail=f"All uploads failed: {'; '.join(errors)}",
        )

    return results


@router.get("", response_model=CandidateListResponse)
async def list_candidates(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """List all candidates, newest first."""
    candidate_service = request.app.state.candidate_service
    candidates = await candidate_service.list_candidates(session)
    return CandidateListResponse(
        candidates=[_candidate_to_response(c) for c in candidates],
        total=len(candidates),
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get a single candidate by ID."""
    candidate_service = request.app.state.candidate_service
    candidate = await candidate_service.get_candidate(session, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return _candidate_to_response(candidate)


@router.delete("/{candidate_id}", status_code=200)
async def delete_candidate(
    candidate_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Delete a candidate by ID. Also removes the uploaded resume file."""
    candidate_service = request.app.state.candidate_service
    deleted = await candidate_service.delete_candidate(session, candidate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully", "id": candidate_id}
