"""Rankings API router — compute and retrieve candidate rankings."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.ranking import RankingResponse, RankingListResponse


router = APIRouter(prefix="/api/rankings", tags=["Rankings"])


@router.post("/compute/{job_id}", response_model=RankingListResponse, status_code=201)
async def compute_rankings(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Compute (or recompute) rankings for all candidates against a job.

    This runs the full AI pipeline:
    1. Loads job embedding and required skills
    2. Loads all candidate embeddings and skills
    3. Computes hybrid semantic + skill + experience scores
    4. Generates natural language explanations
    5. Stores results (replaces any previous rankings for this job)
    """
    ranking_service = request.app.state.ranking_service
    job_service = request.app.state.job_service

    # Verify job exists
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        await ranking_service.compute_rankings(session, job_id)
        enriched_rankings = await ranking_service.get_rankings(session, job_id)

        # Convert to response format
        ranking_responses = [
            RankingResponse(**r) for r in enriched_rankings
        ]

        return RankingListResponse(
            job_id=job_id,
            job_title=job.title,
            rankings=ranking_responses,
            total=len(ranking_responses),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compute rankings: {str(e)}",
        )


@router.get("/{job_id}", response_model=RankingListResponse)
async def get_rankings(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get cached rankings for a job.

    Returns previously computed rankings sorted by rank.
    If no rankings exist, returns an empty list.
    """
    ranking_service = request.app.state.ranking_service
    job_service = request.app.state.job_service

    # Verify job exists
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    rankings = await ranking_service.get_rankings(session, job_id)

    ranking_responses = [
        RankingResponse(**r) for r in rankings
    ]

    return RankingListResponse(
        job_id=job_id,
        job_title=job.title,
        rankings=ranking_responses,
        total=len(ranking_responses),
    )
