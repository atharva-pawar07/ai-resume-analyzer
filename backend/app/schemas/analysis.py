
from pydantic import BaseModel
from datetime import datetime


class ResumeAnalysisResult(BaseModel):
    target_role: str
    detected_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    skill_match_percentage: float


class ResumeAnalysisResponse(BaseModel):
    message: str
    resume_id: int
    candidate_name: str
    analysis: ResumeAnalysisResult


class AnalysisHistoryResponse(BaseModel):
    id: int
    resume_id: int
    target_role: str
    detected_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    skill_match_percentage: float
    created_at: datetime

class SkillRecommendation(BaseModel):
    skill: str
    reason: str
    suggestion: str
    project: str


class ResumeImprovementResponse(BaseModel):
    resume_id: int
    analysis_id: int
    target_role: str
    missing_skills: list[str]
    recommendations: list[SkillRecommendation]