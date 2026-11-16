import pytest
from datetime import datetime, timedelta, timezone
import jwt

from backend.app.core.security import SECRET_KEY, ALGORITHM


# -------------------- HELPER FUNCTIONS --------------------

async def register_and_login(client, email="test@example.com", full_name="Test User"):
    register = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": "TestPassword123"
        }
    )
    assert register.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "TestPassword123"
        }
    )
    assert login.status_code == 200

    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def create_resume(client, headers, **overrides):
    data = {
        "name": "Atharva Pawar",
        "email": "atharva@example.com",
        "phone": "9876543210",
        "target_role": "Python Developer",
        "skills": ["Python", "FastAPI"],
        "experience_years": 0
    }
    data.update(overrides)

    response = await client.post(
        "/api/v1/resumes/",
        headers=headers,
        json=data
    )
    assert response.status_code == 201
    return response.json()


async def create_job(client, headers, **overrides):
    data = {
        "title": "Junior Python Developer",
        "company_name": "Test Company",
        "description": (
            "We need a Python developer with FastAPI, SQL, PostgreSQL, "
            "Git and JavaScript experience for backend application development."
        )
    }
    data.update(overrides)

    response = await client.post(
        "/api/v1/jobs/",
        headers=headers,
        json=data
    )
    assert response.status_code == 201
    return response.json()


# -------------------- ROOT AND HEALTH --------------------

@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to AI Resume Analyzer API"
    assert response.json()["status"] == "running"


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["application"] == "AI Resume Analyzer"


# -------------------- AUTHENTICATION --------------------

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 201
    assert response.json()["full_name"] == "Test User"
    assert response.json()["email"] == "testuser@example.com"
    assert "id" in response.json()
    assert "hashed_password" not in response.json()


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "full_name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "TestPassword123"
    }

    first = await client.post("/api/v1/auth/register", json=payload)
    second = await client.post("/api/v1/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


@pytest.mark.asyncio
async def test_login_user(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Login User",
            "email": "login@example.com",
            "password": "TestPassword123"
        }
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Invalid Login",
            "email": "invalidlogin@example.com",
            "password": "CorrectPassword123"
        }
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalidlogin@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_get_current_user(client):
    headers = await register_and_login(
        client, "profile@example.com", "Profile User"
    )

    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["full_name"] == "Profile User"
    assert response.json()["email"] == "profile@example.com"


@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Invalid Email",
            "email": "not-an-email",
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Short Password",
            "email": "short@example.com",
            "password": "12345"
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_unregistered_email(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_with_expired_token(client):
    token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


# -------------------- RESUME CRUD --------------------

@pytest.mark.asyncio
async def test_create_resume(client):
    headers = await register_and_login(
        client, "resumetest@example.com", "Resume Test User"
    )

    resume = await create_resume(
        client,
        headers,
        target_role="Full Stack AI Developer",
        skills=["Python", "FastAPI", "React", "SQL"]
    )

    assert resume["target_role"] == "Full Stack AI Developer"
    assert resume["skills"] == ["Python", "FastAPI", "React", "SQL"]
    assert "id" in resume


@pytest.mark.asyncio
async def test_create_resume_without_token(client):
    response = await client.post(
        "/api/v1/resumes/",
        json={
            "name": "Unauthorized User",
            "email": "unauthorized@example.com",
            "target_role": "Python Developer",
            "skills": ["Python"],
            "experience_years": 0
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_resumes(client):
    headers = await register_and_login(
        client, "resumelist@example.com", "Resume List User"
    )

    await create_resume(client, headers, target_role="Python Developer")
    await create_resume(client, headers, target_role="Backend Developer")

    response = await client.get("/api/v1/resumes/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_users_cannot_access_other_users_resumes(client):
    owner_headers = await register_and_login(
        client, "owner@example.com", "Resume Owner"
    )
    resume = await create_resume(client, owner_headers)

    other_headers = await register_and_login(
        client, "otheruser@example.com", "Other User"
    )

    response = await client.get(
        f"/api/v1/resumes/{resume['id']}",
        headers=other_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_resume_by_id(client):
    headers = await register_and_login(
        client, "getresume@example.com", "Get Resume User"
    )
    resume = await create_resume(client, headers)

    response = await client.get(
        f"/api/v1/resumes/{resume['id']}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == resume["id"]


@pytest.mark.asyncio
async def test_get_nonexistent_resume(client):
    headers = await register_and_login(
        client, "missingresume@example.com", "Missing Resume User"
    )

    response = await client.get(
        "/api/v1/resumes/99999",
        headers=headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_resume(client):
    headers = await register_and_login(
        client, "updateresume@example.com", "Update Resume User"
    )
    resume = await create_resume(client, headers)

    response = await client.put(
        f"/api/v1/resumes/{resume['id']}",
        headers=headers,
        json={
            "name": "Atharva Pawar",
            "email": "atharva@example.com",
            "phone": "9876543210",
            "target_role": "Full Stack AI Developer",
            "skills": ["Python", "FastAPI", "React", "SQL"],
            "experience_years": 1
        }
    )

    assert response.status_code == 200
    assert response.json()["target_role"] == "Full Stack AI Developer"


@pytest.mark.asyncio
async def test_update_nonexistent_resume(client):
    headers = await register_and_login(
        client, "updatemissing@example.com", "Update Missing User"
    )

    response = await client.put(
        "/api/v1/resumes/99999",
        headers=headers,
        json={
            "name": "Atharva Pawar",
            "email": "atharva@example.com",
            "target_role": "Python Developer",
            "skills": ["Python"],
            "experience_years": 0
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_resume(client):
    headers = await register_and_login(
        client, "deleteresume@example.com", "Delete Resume User"
    )
    resume = await create_resume(client, headers)

    response = await client.delete(
        f"/api/v1/resumes/{resume['id']}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Resume deleted successfully"


@pytest.mark.asyncio
async def test_delete_other_users_resume(client):
    owner_headers = await register_and_login(
        client, "deleteowner@example.com", "Delete Owner"
    )
    resume = await create_resume(client, owner_headers)

    other_headers = await register_and_login(
        client, "deleteother@example.com", "Other User"
    )

    response = await client.delete(
        f"/api/v1/resumes/{resume['id']}",
        headers=other_headers
    )

    assert response.status_code == 404


# -------------------- PDF AND ANALYSIS --------------------

@pytest.mark.asyncio
async def test_upload_resume_rejects_non_pdf_content_type(client):
    headers = await register_and_login(
        client, "wrongtype@example.com", "Wrong Type User"
    )
    resume = await create_resume(client, headers)

    response = await client.post(
        f"/api/v1/resumes/{resume['id']}/upload-pdf",
        headers=headers,
        files={"file": ("resume.txt", b"not a pdf", "text/plain")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"


@pytest.mark.asyncio
async def test_upload_resume_rejects_invalid_pdf_signature(client):
    headers = await register_and_login(
        client, "invalidpdf@example.com", "Invalid PDF User"
    )
    resume = await create_resume(client, headers)

    response = await client.post(
        f"/api/v1/resumes/{resume['id']}/upload-pdf",
        headers=headers,
        files={"file": ("resume.pdf", b"not a real pdf", "application/pdf")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF file"


@pytest.mark.asyncio
async def test_analyze_resume_without_uploaded_pdf(client):
    headers = await register_and_login(
        client, "analyzenopdf@example.com", "Analyze No PDF User"
    )
    resume = await create_resume(client, headers)

    response = await client.post(
        f"/api/v1/resumes/{resume['id']}/analyze",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PDF resume first"


# -------------------- JOB API --------------------

@pytest.mark.asyncio
async def test_create_job(client):
    headers = await register_and_login(
        client, "createjob@example.com", "Create Job User"
    )
    job = await create_job(client, headers)

    assert job["title"] == "Junior Python Developer"
    assert job["company_name"] == "Test Company"
    assert "FastAPI" in job["description"]


@pytest.mark.asyncio
async def test_get_all_jobs(client):
    headers = await register_and_login(
        client, "listjobs@example.com", "List Jobs User"
    )

    await create_job(client, headers, title="Python Developer")
    await create_job(client, headers, title="Backend Developer")

    response = await client.get("/api/v1/jobs/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_nonexistent_job(client):
    headers = await register_and_login(
        client, "missingjob@example.com", "Missing Job User"
    )

    response = await client.get(
        "/api/v1/jobs/99999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job description not found"


# -------------------- JOB MATCHING --------------------

@pytest.mark.asyncio
async def test_job_match_requires_uploaded_resume_pdf(client):
    headers = await register_and_login(
        client, "matchnopdf@example.com", "Match No PDF User"
    )
    resume = await create_resume(client, headers)
    job = await create_job(client, headers)

    response = await client.post(
        "/api/v1/job-matches/",
        headers=headers,
        json={
            "resume_id": resume["id"],
            "job_id": job["id"]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Upload a PDF resume before matching"