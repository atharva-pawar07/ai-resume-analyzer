
from pydantic import BaseModel, Field, EmailStr


class ResumeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    target_role: str
    skills: list[str] = Field(default_factory=list)
    experience_years: float = Field(default=0, ge=0)


class ResumeResponse(ResumeCreate):
    id: int
