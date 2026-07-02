"""Candidate ORM model."""

from sqlalchemy import Column, Text, LargeBinary, DateTime
from datetime import datetime, timezone

from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    resume_path = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)  # JSON string list
    experience = Column(Text, nullable=True)  # JSON string list
    education = Column(Text, nullable=True)  # JSON string list
    embedding = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
