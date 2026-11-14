
from fastapi import FastAPI

from backend.app.routers import health, resumes, auth


app = FastAPI(
    title="AI Resume Analyzer",
    description="An AI-powered resume analysis and job matching platform",
    version="1.0.0"
)


# Register API routers
app.include_router(health.router)
app.include_router(resumes.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer!",
        "status": "Backend is running successfully"
    }
