"""Ranking ORM model."""

from sqlalchemy import Column, Text, Float, Integer, DateTime, ForeignKey
from datetime import datetime, timezone

from app.core.database import Base


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Text, primary_key=True)
    job_id = Column(Text, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Text, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    semantic_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)
    matched_skills = Column(Text, nullable=True)  # JSON string list
    missing_skills = Column(Text, nullable=True)  # JSON string list
    explanation = Column(Text, nullable=True)
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
