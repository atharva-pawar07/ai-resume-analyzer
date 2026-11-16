
from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, func

from backend.app.core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False
    )

    target_role: Mapped[str] = mapped_column(
        String(150),
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

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
    )
    
    resume = relationship(
        "Resume",
        back_populates="analyses"
    )
