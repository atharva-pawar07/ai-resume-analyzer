from backend.app.ai.recommendation_engine import generate_recommendations
from backend.app.ai.resume_analyzer import extract_skills


def test_generate_recommendations():
    missing_skills = ["SQL", "Git"]

    result = generate_recommendations(missing_skills)

    assert len(result) == 2
    assert result[0]["skill"] == "SQL"
    assert result[1]["skill"] == "Git"


def test_generate_recommendations_with_no_missing_skills():
    result = generate_recommendations([])

    assert result == []


def test_generate_recommendations_with_unsupported_skill():
    result = generate_recommendations(["Unknown Technology"])

    assert result == []

def test_extract_skills():
    resume_text = """
    I have experience with Python, FastAPI, React and PostgreSQL.
    """

    result = extract_skills(resume_text)

    assert "Python" in result
    assert "FastAPI" in result
    assert "React" in result
    assert "PostgreSQL" in result


def test_extract_skills_is_case_insensitive():
    resume_text = "I know python, FASTAPI, and react."

    result = extract_skills(resume_text)

    assert "Python" in result
    assert "FastAPI" in result
    assert "React" in result

def test_extract_skills_does_not_match_partial_words():
    resume_text = "I worked with PythonDeveloper and JavaScriptFramework."

    result = extract_skills(resume_text)

    assert "Python" not in result
    assert "JavaScript" not in result