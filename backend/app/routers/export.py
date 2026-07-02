"""Export API router — download rankings as CSV."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.export_service import ExportService


router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/{job_id}")
async def export_rankings_csv(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Export rankings for a job as a CSV file download.

    Returns a CSV file with columns:
    Rank, Candidate Name, Email, Overall Score, Semantic Score,
    Skill Score, Matched Skills, Missing Skills, Explanation.
    """
    job_service = request.app.state.job_service
    ranking_service = request.app.state.ranking_service

    # Verify job exists
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get rankings
    rankings = await ranking_service.get_rankings(session, job_id)
    if not rankings:
        raise HTTPException(
            status_code=404,
            detail="No rankings found for this job. Compute rankings first.",
        )

    # Generate CSV bytes
    csv_bytes = ExportService.generate_csv_bytes(job.title, rankings)

    # Create safe filename
    safe_title = "".join(
        c if c.isalnum() or c in (" ", "-", "_") else "_"
        for c in job.title
    ).strip().replace(" ", "_")
    filename = f"rankings_{safe_title}.csv"

    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
