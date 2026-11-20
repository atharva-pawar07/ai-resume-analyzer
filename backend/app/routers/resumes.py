
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
from backend.app.models.analysis import Analysis

from backend.app.schemas.resume import (
    ResumeCreate,
    ResumeResponse
)

from backend.app.schemas.analysis import (
    ResumeAnalysisResponse,
    AnalysisHistoryResponse
)
from backend.app.ai.gemini_service import (
    generate_ai_resume_analysis,
    GeminiNotConfiguredError,
    GeminiAnalysisError
)

from backend.app.services.pdf_service import extract_text_from_pdf
from backend.app.ai.resume_analyzer import analyze_resume

from backend.app.ai.recommendation_engine import generate_recommendations

from backend.app.schemas.analysis import ResumeImprovementResponse


router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"]
)

MAX_FILE_SIZE = 5 * 1024 * 1024


# 1. Create Resume
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


# 2. Get All Resumes
@router.get("/", response_model=list[ResumeResponse])
async def get_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Resume).where(
            Resume.user_id == current_user.id
        )
    )

    return result.scalars().all()


# 3. Get Resume By ID
@router.get("/{resume_id}", response_model=ResumeResponse)
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


# 4. Update Resume
@router.put("/{resume_id}", response_model=ResumeResponse)
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


# 5. Delete Resume
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


# 6. Upload Resume PDF
@router.post("/{resume_id}/upload-pdf")
async def upload_resume_pdf(
    resume_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
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

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

        pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

        if not pdf_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )

        if len(pdf_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="PDF file must be smaller than 5 MB"
            )

        if not pdf_bytes.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PDF file"
            )

        extracted_text = extract_text_from_pdf(pdf_bytes)

        resume.resume_text = extracted_text

        await db.commit()
        await db.refresh(resume)

        return {
            "message": "Resume PDF uploaded successfully",
            "resume_id": resume.id,
            "extracted_text": extracted_text
        }

    finally:
        await file.close()


# 7. Analyze Resume
@router.post(
    "/{resume_id}/analyze",
    response_model=ResumeAnalysisResponse
)
async def analyze_resume_endpoint(
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

    if not resume.resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a PDF resume first"
        )

    analysis_result = analyze_resume(
        resume.resume_text,
        resume.target_role
    )

    if "error" in analysis_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=analysis_result["message"]
        )

    new_analysis = Analysis(
        resume_id=resume.id,
        target_role=analysis_result["target_role"],
        detected_skills=analysis_result["detected_skills"],
        required_skills=analysis_result["required_skills"],
        matched_skills=analysis_result["matched_skills"],
        missing_skills=analysis_result["missing_skills"],
        skill_match_percentage=analysis_result["skill_match_percentage"]
    )

    db.add(new_analysis)
    await db.commit()
    await db.refresh(new_analysis)

    return {
        "message": "Resume analyzed successfully",
        "resume_id": resume.id,
        "candidate_name": resume.name,
        "analysis": analysis_result
    }


# 8. Get Analysis History
@router.get(
    "/{resume_id}/analyses",
    response_model=list[AnalysisHistoryResponse]
)
async def get_analysis_history(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify resume ownership
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

    # Retrieve analysis reports
    result = await db.execute(
        select(Analysis)
        .where(Analysis.resume_id == resume_id)
        .order_by(
    Analysis.created_at.desc(),
    Analysis.id.desc()
)
    )

    analyses = result.scalars().all()

    return analyses


# 9. Get Specific Analysis Report
@router.get(
    "/{resume_id}/analyses/{analysis_id}",
    response_model=AnalysisHistoryResponse
)
async def get_analysis_report(
    resume_id: int,
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Analysis)
        .join(Resume, Analysis.resume_id == Resume.id)
        .where(
            Analysis.id == analysis_id,
            Analysis.resume_id == resume_id,
            Resume.user_id == current_user.id
        )
    )

    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis report not found"
        )

    return analysis

# Get Resume Improvement Suggestions
@router.get(
    "/{resume_id}/analyses/{analysis_id}/recommendations",
    response_model=ResumeImprovementResponse
)
async def get_resume_recommendations(
    resume_id: int,
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find analysis belonging to the current user's resume
    result = await db.execute(
        select(Analysis)
        .join(Resume, Analysis.resume_id == Resume.id)
        .where(
            Analysis.id == analysis_id,
            Analysis.resume_id == resume_id,
            Resume.user_id == current_user.id
        )
    )

    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis report not found"
        )

    # Generate recommendations from missing skills
    recommendations = generate_recommendations(
    analysis.missing_skills,
    analysis.target_role
)

    return {
        "resume_id": resume_id,
        "analysis_id": analysis_id,
        "target_role": analysis.target_role,
        "missing_skills": analysis.missing_skills,
        "recommendations": recommendations
    }
# 10. Gemini AI Resume Analysis
@router.post("/{resume_id}/ai-analysis")
async def ai_resume_analysis(
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

    if not resume.resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a PDF resume first"
        )

    try:
        ai_result = generate_ai_resume_analysis(
            resume.resume_text,
            resume.target_role
        )

        return {
            "message": "AI resume analysis completed",
            "resume_id": resume.id,
            "candidate_name": resume.name,
            "target_role": resume.target_role,
            "ai_analysis": ai_result
        }

    except GeminiNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc)
        )

    except GeminiAnalysisError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc)
        )
