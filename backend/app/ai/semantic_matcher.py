
import re
import numpy as np

from backend.app.ai.rag_retriever import embedding_model


def clean_text(text: str) -> str:
    """Normalize text before semantic comparison."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_chunks(text: str) -> list[str]:
    """
    Split text into meaningful sentence groups.
    This helps avoid embedding an entire long resume
    or job description as one truncated input.
    """
    text = text.replace("\r\n", "\n")

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 4
    ]

    if not sentences and text.strip():
        return [text.strip()]

    chunks = []

    for index in range(0, len(sentences), 3):
        chunk = " ".join(sentences[index:index + 3])
        chunks.append(chunk)

    return chunks


def calculate_similarity(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculate semantic similarity using pretrained
    Sentence Transformer embeddings and cosine similarity.

    This score measures textual semantic relevance.
    It is not a hiring probability or verified skill-match score.
    """

    if (
        not isinstance(resume_text, str)
        or not isinstance(job_description, str)
        or not resume_text.strip()
        or not job_description.strip()
    ):
        return 0.0

    resume_chunks = split_into_chunks(clean_text(resume_text))
    job_chunks = split_into_chunks(clean_text(job_description))

    if not resume_chunks or not job_chunks:
        return 0.0

    resume_embeddings = embedding_model.encode(
        resume_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    job_embeddings = embedding_model.encode(
        job_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    similarity_matrix = np.dot(
        job_embeddings,
        resume_embeddings.T
    )

    # Find the strongest resume evidence for each job chunk.
    best_matches = np.max(similarity_matrix, axis=1)

    # Average relevance across job-description chunks.
    semantic_score = np.mean(best_matches)

    # Convert cosine similarity into a percentage-like score.
    return round(
        float(np.clip(semantic_score, 0.0, 1.0)) * 100,
        2
    )
