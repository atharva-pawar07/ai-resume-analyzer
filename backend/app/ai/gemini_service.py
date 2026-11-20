
import json
import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")


class GeminiNotConfiguredError(Exception):
    pass


class GeminiAnalysisError(Exception):
    pass


def generate_ai_resume_analysis(
    resume_text: str,
    target_role: str
) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiNotConfiguredError(
            "Gemini API key is not configured."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a strict, evidence-based technical recruiter.

Evaluate the candidate's resume against the target role.

TARGET ROLE:
{target_role}

RESUME CONTENT:
<resume>
{resume_text[:30000]}
</resume>

EVALUATION RULES:

1. Use only information explicitly supported by the resume.
2. Never invent experience, projects, technologies,
   qualifications, certifications, achievements, or dates.
3. Do not assume the candidate knows any technology unless
   the resume provides evidence.
4. Distinguish listed skills from skills demonstrated in projects.
5. Say "not demonstrated in the resume" when evidence is absent.
6. Do not invent resume errors or timeline discrepancies.
7. Evaluate fairly for the candidate's experience level.
8. Make suggestions specific to the target role.
9. Do not claim AI, LLM, RAG, or agent experience unless demonstrated.
10. Recommend practical projects that address evidence gaps.

Return ONLY valid JSON with exactly this structure:

{{
    "overall_assessment": "Evidence-based assessment of the candidate.",
    "strengths": [
        "Strength supported by resume evidence"
    ],
    "missing_skills": [
        "Relevant skill not demonstrated in the resume"
    ],
    "improvement_suggestions": [
        "Specific and practical resume improvement"
    ],
    "recommended_projects": [
        "Project idea relevant to the target role"
    ],
    "summary": "Honest final assessment and next steps."
}}

Return valid JSON only.
Do not use Markdown code fences.
Do not add text outside the JSON.
"""

    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            break

        except Exception as exc:
            error_code = getattr(exc, "code", None)

            logger.exception(
                "Gemini API request failed: %s",
                str(exc)
            )

            if error_code in (503, 429) and attempt < 2:
                wait_seconds = 5 * (attempt + 1)

                logger.warning(
                    "Gemini temporarily unavailable. "
                    "Retrying in %s seconds.",
                    wait_seconds
                )

                time.sleep(wait_seconds)
                continue

            raise GeminiAnalysisError(
                f"Gemini request failed: "
                f"{type(exc).__name__}: {str(exc)}"
            ) from exc

    if response is None or not response.text:
        raise GeminiAnalysisError(
            "Gemini returned an empty response."
        )

    try:
        result = json.loads(response.text)

        required_fields = [
            "overall_assessment",
            "strengths",
            "missing_skills",
            "improvement_suggestions",
            "recommended_projects",
            "summary"
        ]

        if not isinstance(result, dict):
            raise ValueError("Response must be a JSON object.")

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing field: {field}")

        for field in required_fields[1:5]:
            if not isinstance(result[field], list):
                raise ValueError(f"{field} must be a list.")

            if not all(
                isinstance(item, str) for item in result[field]
            ):
                raise ValueError(
                    f"{field} must contain only strings."
                )

        for field in ["overall_assessment", "summary"]:
            if not isinstance(result[field], str):
                raise ValueError(f"{field} must be a string.")

        return result

    except (json.JSONDecodeError, ValueError) as exc:
        logger.exception(
            "Invalid Gemini response: %s",
            str(exc)
        )

        raise GeminiAnalysisError(
            f"Gemini returned invalid analysis: {str(exc)}"
        ) from exc
