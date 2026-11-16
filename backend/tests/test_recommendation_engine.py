from backend.app.ai.recommendation_engine import generate_recommendations


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