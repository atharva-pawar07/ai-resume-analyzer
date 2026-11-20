
from backend.app.ai.rag_retriever import retrieve_relevant_documents


def test_semantic_retrieval():
    results = retrieve_relevant_documents(
        "I want to build a React frontend with a Python API and database",
        top_k=3
    )

    assert len(results) == 3
    assert all("title" in result for result in results)
    assert all("similarity_score" in result for result in results)


def test_empty_query():
    assert retrieve_relevant_documents("") == []


def test_invalid_top_k():
    assert retrieve_relevant_documents("Python development", top_k=0) == []
