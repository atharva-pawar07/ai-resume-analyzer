from datetime import datetime

from pydantic import BaseModel


class JobMatchCreate(BaseModel):
    resume_id: int
    job_id: int


class JobMatchResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    detected_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    skill_match_percentage: float
    created_at: datetime