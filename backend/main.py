
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.auth import router as auth_router
from backend.app.routers.resumes import router as resumes_router
from backend.app.routers.health import router as health_router
from backend.app.routers.jobs import router as jobs_router
from backend.app.routers.job_matches import router as job_matches_router


app = FastAPI(
    title="AI Resume Analyzer",
    description="An API for resume management, job matching, and AI-powered career analysis.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(job_matches_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "status": "running"
    }
