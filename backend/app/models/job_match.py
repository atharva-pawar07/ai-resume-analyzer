
from datetime import datetime

from sqlalchemy import (
    Integer,
    Float,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    detected_skills: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    required_skills: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    matched_skills: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    missing_skills: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    skill_match_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    text_similarity_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
