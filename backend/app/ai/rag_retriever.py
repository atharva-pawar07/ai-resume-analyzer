
import numpy as np
from sentence_transformers import SentenceTransformer

from backend.app.ai.career_knowledge_base import get_all_documents


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load the pretrained embedding model.
embedding_model = SentenceTransformer(MODEL_NAME)

# Load career knowledge documents.
documents = get_all_documents()

# Combine title and content for better retrieval.
document_texts = [
    f"{document['title']}\n{document['content']}"
    for document in documents
]

# Generate and normalize document embeddings.
document_embeddings = embedding_model.encode(
    document_texts,
    convert_to_numpy=True,
    normalize_embeddings=True
)


def retrieve_relevant_documents(
    query: str,
    top_k: int = 4
) -> list[dict]:
    """
    Retrieve knowledge documents using semantic embeddings.
    """

    if not query or not query.strip():
        return []

    if top_k < 1:
        return []

    if not documents:
        return []

    # Convert the user's query into an embedding.
    query_embedding = embedding_model.encode(
        query.strip(),
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Cosine similarity because vectors are normalized.
    scores = np.dot(document_embeddings, query_embedding)

    # Rank documents by similarity.
    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        document = documents[int(index)]

        results.append({
            "id": document["id"],
            "category": document["category"],
            "title": document["title"],
            "content": document["content"],
            "similarity_score": round(float(scores[index]), 4)
        })

    return results
