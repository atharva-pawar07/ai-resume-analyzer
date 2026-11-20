
import json
import logging
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"


class LLMServiceError(Exception):
    """Raised when local LLM generation fails."""


def generate_career_guidance(
    resume_text: str,
    job_description: str,
    retrieved_documents: list[dict],
) -> dict:
    """
    Generate career guidance using retrieved knowledge
    and the local Qwen language model.
    """

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not retrieved_documents:
        raise ValueError("Retrieved knowledge documents are required.")

    # Prepare retrieved knowledge for the LLM.
    knowledge_context = "\n\n".join(
        f"""
        Source: {document.get('title', 'Unknown')}
        Category: {document.get('category', 'Unknown')}
        Content: {document.get('content', '')}
        """
        for document in retrieved_documents
    )

    prompt = f"""
    You are an AI career guidance assistant.

    Your task is to analyse a candidate's resume against
    a specific job description.

    Use the supplied career knowledge as supporting context.

    IMPORTANT RULES:
    1. Base candidate-specific claims on the supplied resume.
    2. Base job requirements on the supplied job description.
    3. Do not invent skills, experience, qualifications or achievements.
    4. Do not claim the candidate has a skill unless the resume supports it.
    5. Distinguish missing evidence from confirmed lack of a skill.
    6. Do not invent job listings, companies or application links.
    7. Do not treat a matching score as hiring probability.
    8. If information is insufficient, explicitly say so.
    9. Use the retrieved knowledge to explain relevant concepts
       and suggest learning steps.
    10. Return valid JSON only.

    CANDIDATE RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    RETRIEVED CAREER KNOWLEDGE:
    {knowledge_context}

    Return JSON using exactly this structure:

    {{
        "overall_assessment": "Detailed assessment",
        "matched_evidence": [
            {{
                "skill": "Skill name",
                "evidence": "Evidence from the resume"
            }}
        ],
        "skill_gaps": [
            {{
                "skill": "Skill name",
                "reason": "Why it matters for this job"
            }}
        ],
        "recommendations": [
            "Actionable recommendation"
        ],
        "learning_plan": [
            {{
                "topic": "Topic to learn",
                "reason": "Why it is relevant"
            }}
        ],
        "limitations": [
            "Information that could not be verified"
        ]
    }}
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful, evidence-based career "
                    "assistant. Never invent candidate information. "
                    "Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "num_ctx": 4096,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        generated_text = response_data["message"]["content"]
        result = json.loads(generated_text)

        required_fields = [
            "overall_assessment",
            "matched_evidence",
            "skill_gaps",
            "recommendations",
            "learning_plan",
            "limitations",
        ]

        if not isinstance(result, dict):
            raise ValueError("LLM response must be a JSON object.")

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing response field: {field}")

        return result

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        logger.exception("Ollama HTTP error: %s", details)
        raise LLMServiceError(
            f"Ollama returned HTTP {error.code}."
        ) from error

    except urllib.error.URLError as error:
        logger.exception("Could not connect to Ollama.")
        raise LLMServiceError(
            "Cannot connect to Ollama. Make sure it is running."
        ) from error

    except (KeyError, json.JSONDecodeError, ValueError) as error:
        logger.exception("Invalid LLM response.")
        raise LLMServiceError(
            f"Invalid response from local LLM: {error}"
        ) from error

    except TimeoutError as error:
        logger.exception("Ollama request timed out.")
        raise LLMServiceError(
            "Local LLM generation timed out."
        ) from error
