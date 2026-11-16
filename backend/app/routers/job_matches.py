
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user

from backend.app.models.resume import Resume
from backend.app.models.job import Job
from backend.app.models.job_match import JobMatch
from backend.app.models.user import User

from backend.app.schemas.job_match import (
    JobMatchCreate,
    JobMatchResponse
)

from backend.app.ai.resume_analyzer import (
    extract_skills,
    compare_skills,
    calculate_skill_match
)


router = APIRouter(
    prefix="/api/v1/job-matches",
    tags=["Job Matching"]
)


# 1. Compare Resume with Job Description
@router.post(
    "/",
    response_model=JobMatchResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_job_match(
    match_data: JobMatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find resume belonging to current user
    resume_result = await db.execute(
        select(Resume).where(
            Resume.id == match_data.resume_id,
            Resume.user_id == current_user.id
        )
    )

    resume = resume_result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Check whether resume has extracted text
    if not resume.resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload a PDF resume before matching"
        )

    # Find job belonging to current user
    job_result = await db.execute(
        select(Job).where(
            Job.id == match_data.job_id,
            Job.user_id == current_user.id
        )
    )

    job = job_result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    # Detect skills from resume and job description
    detected_skills = extract_skills(resume.resume_text)
    required_skills = extract_skills(job.description)

    if not required_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No supported skills found in the job description"
        )

    # Compare skills
    comparison = compare_skills(
        detected_skills,
        required_skills
    )

    matched_skills = comparison["matched_skills"]
    missing_skills = comparison["missing_skills"]

    # Calculate match percentage
    match_percentage = calculate_skill_match(
        matched_skills,
        required_skills
    )

    # Save matching result
    new_match = JobMatch(
        resume_id=resume.id,
        job_id=job.id,
        user_id=current_user.id,
        detected_skills=detected_skills,
        required_skills=required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        skill_match_percentage=match_percentage
    )

    db.add(new_match)
    await db.commit()
    await db.refresh(new_match)

    return new_match


# 2. Get All Job Matching Reports
@router.get(
    "/",
    response_model=list[JobMatchResponse]
)
async def get_job_matches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(JobMatch)
        .where(JobMatch.user_id == current_user.id)
        .order_by(
            JobMatch.created_at.desc(),
            JobMatch.id.desc()
        )
    )

    return result.scalars().all()


# 3. Get Specific Job Matching Report
@router.get(
    "/{match_id}",
    response_model=JobMatchResponse
)
async def get_job_match(
    match_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(JobMatch).where(
            JobMatch.id == match_id,
            JobMatch.user_id == current_user.id
        )
    )

    match = result.scalar_one_or_none()

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job matching report not found"
        )

    return match
