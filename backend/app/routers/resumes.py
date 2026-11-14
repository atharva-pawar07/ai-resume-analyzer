
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.models.resume import Resume
from backend.app.schemas.resume import ResumeCreate, ResumeResponse

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"]
)


# CREATE RESUME
@router.post(
    "/",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_resume(
    resume_data: ResumeCreate,
    db: AsyncSession = Depends(get_db)
):
    new_resume = Resume(**resume_data.model_dump())

    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    return new_resume


# GET ALL RESUMES
@router.get("/", response_model=list[ResumeResponse])
async def get_resumes(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Resume))

    resumes = result.scalars().all()

    return resumes


# GET SINGLE RESUME
@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id)
    )

    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return resume


# UPDATE RESUME
@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    resume_data: ResumeCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id)
    )

    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    for key, value in resume_data.model_dump().items():
        setattr(resume, key, value)

    await db.commit()
    await db.refresh(resume)

    return resume


# DELETE RESUME
@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id)
    )

    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    await db.delete(resume)
    await db.commit()

    return {
        "message": "Resume deleted successfully"
    }
