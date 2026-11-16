from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user

from backend.app.models.job import Job
from backend.app.models.user import User

from backend.app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse
)


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)


# 1. Create Job Description
@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_job(
    job_data: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_job = Job(
        title=job_data.title,
        company_name=job_data.company_name,
        description=job_data.description,
        user_id=current_user.id
    )

    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    return new_job


# 2. Get All Job Descriptions
@router.get(
    "/",
    response_model=list[JobResponse]
)
async def get_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Job)
        .where(Job.user_id == current_user.id)
        .order_by(Job.id.desc())
    )

    return result.scalars().all()


# 3. Get Single Job Description
@router.get(
    "/{job_id}",
    response_model=JobResponse
)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == current_user.id
        )
    )

    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    return job


# 4. Update Job Description
@router.put(
    "/{job_id}",
    response_model=JobResponse
)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == current_user.id
        )
    )

    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    job.title = job_data.title
    job.company_name = job_data.company_name
    job.description = job_data.description

    await db.commit()
    await db.refresh(job)

    return job


# 5. Delete Job Description
@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == current_user.id
        )
    )

    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    await db.delete(job)
    await db.commit()

    return None