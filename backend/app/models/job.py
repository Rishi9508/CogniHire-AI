"""Job ORM model."""

from sqlalchemy import Column, Text, LargeBinary, DateTime
from datetime import datetime, timezone

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=True)  # JSON string list
    preferred_skills = Column(Text, nullable=True)  # JSON string list
    experience_level = Column(Text, nullable=True)
    embedding = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
