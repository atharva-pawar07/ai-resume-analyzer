
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user

from backend.app.models.resume import Resume
from backend.app.models.user import User

from backend.app.schemas.resume import (
    ResumeCreate,
    ResumeResponse
)

from backend.app.services.pdf_service import extract_text_from_pdf


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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_resume = Resume(
        **resume_data.model_dump(),
        user_id=current_user.id
    )

    db.add(new_resume)

    await db.commit()
    await db.refresh(new_resume)

    return new_resume


# GET ALL RESUMES BELONGING TO CURRENT USER
@router.get(
    "/",
    response_model=list[ResumeResponse]
)
async def get_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Resume).where(
            Resume.user_id == current_user.id
        )
    )

    resumes = result.scalars().all()

    return resumes


# GET SINGLE RESUME BELONGING TO CURRENT USER
@router.get(
    "/{resume_id}",
    response_model=ResumeResponse
)
async def get_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
    )

    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return resume


# UPDATE RESUME BELONGING TO CURRENT USER
@router.put(
    "/{resume_id}",
    response_model=ResumeResponse
)
async def update_resume(
    resume_id: int,
    resume_data: ResumeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
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


# DELETE RESUME BELONGING TO CURRENT USER
@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
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


# UPLOAD PDF RESUME
@router.post("/{resume_id}/upload-pdf")
async def upload_resume_pdf(
    resume_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check resume ownership
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
    )

    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Check PDF content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    # Maximum file size: 5 MB
    MAX_FILE_SIZE = 5 * 1024 * 1024

    # Read at most 5 MB + 1 byte
    pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

    # Check empty file
    if not pdf_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    # Check file size
    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="PDF file size must not exceed 5 MB"
        )

    # Verify actual PDF signature
    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PDF file"
        )

    # Extract text
    extracted_text = extract_text_from_pdf(pdf_bytes)

    # Save extracted text
    resume.resume_text = extracted_text

    await db.commit()
    await db.refresh(resume)

    # Close uploaded file
    await file.close()

    return {
        "message": "PDF uploaded and text extracted successfully",
        "resume_id": resume.id,
        "extracted_text": extracted_text
    }
