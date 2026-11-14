
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="user"
    )
