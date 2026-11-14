
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from backend.app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    target_role: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    skills: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list
    )

    experience_years: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0
    )

    # Foreign key connecting resume to its owner
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationship with User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="resumes"
    )
