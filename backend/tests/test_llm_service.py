
from backend.app.ai.llm_service import generate_career_guidance


def test_local_llm_generates_career_guidance():
    resume = """
    Python Developer Fresher.
    Skills: Python, SQL, HTML, CSS, JavaScript.
    Project: AI Resume Analyzer using Python and FastAPI.
    """

    job_description = """
    Junior Full Stack AI Developer.
    Requirements: Python, FastAPI, React, PostgreSQL,
    machine learning and REST APIs.
    """

    retrieved_documents = [
        {
            "title": "Full Stack AI Developer Roadmap",
            "category": "career_roadmap",
            "content": (
                "Full Stack AI Developers use React, "
                "Python, FastAPI, PostgreSQL, machine learning "
                "and retrieval augmented generation."
            ),
        },
        {
            "title": "FastAPI Backend Development",
            "category": "technical_skill",
            "content": (
                "FastAPI is used to build Python REST APIs "
                "with request validation and database integration."
            ),
        },
    ]

    result = generate_career_guidance(
        resume_text=resume,
        job_description=job_description,
        retrieved_documents=retrieved_documents,
    )

    assert isinstance(result, dict)
    assert isinstance(result["overall_assessment"], str)
    assert isinstance(result["matched_evidence"], list)
    assert isinstance(result["skill_gaps"], list)
    assert isinstance(result["recommendations"], list)
    assert isinstance(result["learning_plan"], list)
    assert isinstance(result["limitations"], list)

    print("\nAI GENERATED CAREER GUIDANCE:")
    print(result)


def test_empty_resume_is_rejected():
    try:
        generate_career_guidance(
            resume_text="",
            job_description="Python Developer",
            retrieved_documents=[{"title": "Python", "content": "Python"}],
        )
        assert False, "Expected ValueError"
    except ValueError:
        pass
