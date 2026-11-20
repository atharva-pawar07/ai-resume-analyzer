
CAREER_KNOWLEDGE_BASE = [
    {
        "id": "full_stack_ai_roadmap",
        "category": "career_roadmap",
        "title": "Full Stack AI Developer Roadmap",
        "content": """
        A Full Stack AI Developer builds complete web applications
        integrated with artificial intelligence.

        Frontend: HTML, CSS, JavaScript, React, components, props,
        state management, hooks, forms, API integration and routing.

        Backend: Python, FastAPI, REST APIs, Pydantic, authentication,
        middleware, asynchronous programming and API testing.

        Database: PostgreSQL, SQL, relationships, joins, indexes,
        SQLAlchemy, SQLModel and Alembic migrations.

        AI and Machine Learning: Python, NumPy, Pandas, Scikit-learn,
        supervised learning, unsupervised learning, NLP and model evaluation.

        Generative AI: Large Language Models, prompt engineering,
        embeddings, vector databases, semantic search, RAG and AI agents.

        Recommended learning order:
        Python fundamentals, SQL, FastAPI, PostgreSQL, React,
        machine learning fundamentals, NLP, embeddings, RAG and agents.
        """
    },
    {
        "id": "react_development",
        "category": "technical_skill",
        "title": "React Frontend Development",
        "content": """
        React is a JavaScript library for building user interfaces.

        Important concepts include components, JSX, props, state,
        event handling, conditional rendering, lists, forms,
        useState, useEffect, useContext, useRef and custom hooks.

        Developers should understand React Router, API integration
        using fetch or Axios, authentication flows, form validation,
        reusable components and frontend application architecture.

        A practical project should connect a React frontend to a
        Python FastAPI backend and display API responses.
        """
    },
    {
        "id": "python_development",
        "category": "technical_skill",
        "title": "Python Development",
        "content": """
        Python is widely used in backend development, automation,
        data science, machine learning and artificial intelligence.

        Important fundamentals include variables, data types,
        conditions, loops, functions, lists, dictionaries, sets,
        tuples, comprehensions, exceptions, modules and packages.

        Advanced concepts include object-oriented programming,
        decorators, generators, context managers, type hints,
        asynchronous programming and virtual environments.

        Python developers should write modular code, handle errors,
        test functions and understand package management.
        """
    },
    {
        "id": "fastapi_development",
        "category": "technical_skill",
        "title": "FastAPI Backend Development",
        "content": """
        FastAPI is a Python framework for building APIs.

        Important topics include path parameters, query parameters,
        request bodies, Pydantic models, response models,
        HTTP methods, status codes and exception handling.

        Intermediate topics include dependency injection,
        middleware, CORS, authentication, JWT, file uploads,
        background tasks and asynchronous endpoints.

        Database integration includes PostgreSQL, SQLAlchemy,
        SQLModel, database sessions and Alembic migrations.

        FastAPI can also expose machine learning models and
        retrieval augmented generation services through APIs.
        """
    },
    {
        "id": "postgresql",
        "category": "technical_skill",
        "title": "PostgreSQL Database Development",
        "content": """
        PostgreSQL is a relational database management system.

        Important topics include tables, primary keys, foreign keys,
        constraints, data types, CRUD operations, joins, subqueries,
        aggregate functions, indexes and transactions.

        Advanced topics include normalization, query optimization,
        database migrations and relational data modelling.

        Full Stack AI applications may store users, resumes,
        extracted skills, job descriptions, job matches,
        recommendations and analysis history in PostgreSQL.
        """
    },
    {
        "id": "machine_learning",
        "category": "ai_concept",
        "title": "Machine Learning Fundamentals",
        "content": """
        Machine learning enables systems to learn patterns from data.

        Supervised learning uses labelled data for classification
        and regression. Unsupervised learning discovers patterns
        in unlabelled data, including clustering.

        Important concepts include features, labels, preprocessing,
        training data, testing data, overfitting, underfitting,
        cross-validation and model evaluation.

        Python libraries include NumPy, Pandas and Scikit-learn.

        Developers should understand model selection, evaluation
        metrics and limitations before deploying models.
        """
    },
    {
        "id": "natural_language_processing",
        "category": "ai_concept",
        "title": "Natural Language Processing",
        "content": """
        Natural Language Processing enables computers to process
        and analyse human language.

        Important concepts include text normalization, tokenization,
        stop-word removal, stemming, lemmatization, text classification,
        named entity recognition and information extraction.

        NLP applications include resume parsing, job description
        analysis, skill extraction, document classification and
        text similarity.

        TF-IDF is a statistical text representation technique.
        It is not the same as pretrained semantic embeddings.
        """
    },
    {
        "id": "embeddings",
        "category": "ai_concept",
        "title": "Text Embeddings and Semantic Search",
        "content": """
        Text embeddings convert text into numerical vectors
        representing semantic information.

        Similar meanings can have nearby vector representations
        even when they use different words.

        Sentence Transformers provides pretrained models
        for generating sentence and paragraph embeddings.

        Semantic retrieval compares query embeddings with
        document embeddings using cosine similarity or
        other vector similarity measures.

        Embeddings can power semantic resume matching,
        job search, knowledge retrieval and RAG applications.

        TF-IDF and embeddings are different techniques:
        TF-IDF is based on word statistics, while pretrained
        embeddings represent learned semantic relationships.
        """
    },
    {
        "id": "large_language_models",
        "category": "ai_concept",
        "title": "Large Language Models",
        "content": """
        Large Language Models generate and understand text
        using patterns learned during training.

        Applications include summarization, question answering,
        explanation, classification and personalized guidance.

        Important concepts include tokens, context windows,
        inference, prompts, structured output and hallucinations.

        An LLM can use retrieved documents as context to generate
        answers grounded in an application's knowledge base.

        Generated output should be validated and checked against
        available evidence.
        """
    },
    {
        "id": "rag",
        "category": "ai_concept",
        "title": "Retrieval Augmented Generation",
        "content": """
        Retrieval Augmented Generation combines information
        retrieval with large language model generation.

        A typical RAG pipeline contains document ingestion,
        document cleaning, chunking, embedding generation,
        vector indexing, query embedding, similarity retrieval,
        context construction and answer generation.

        First, documents are converted into embeddings.
        Next, a user's question is converted into an embedding.
        The system retrieves relevant document chunks.
        Retrieved information is included in the LLM prompt.
        The LLM generates an answer using the supplied context.

        RAG is useful for knowledge-grounded question answering,
        personalized career advice, skill-gap analysis,
        resume guidance and job requirement explanations.

        Retrieval quality and answer faithfulness should be evaluated.
        """
    },
    {
        "id": "ai_agents",
        "category": "ai_concept",
        "title": "AI Agents",
        "content": """
        AI agents are systems that use an AI model to decide
        and execute actions toward a goal.

        An agent may use tools such as APIs, databases,
        search systems, calculators and retrieval systems.

        Career assistant examples include finding relevant jobs,
        analysing skill gaps, retrieving learning resources
        and preparing personalized learning plans.

        Reliable agents need tool validation, permissions,
        error handling, observability and safeguards.
        """
    },
    {
        "id": "full_stack_ai_jobs",
        "category": "job_role",
        "title": "Full Stack AI Developer Job Requirements",
        "content": """
        Full Stack AI Developer roles combine web development
        and artificial intelligence.

        Frontend requirements may include JavaScript, React,
        HTML, CSS, API integration and responsive interfaces.

        Backend requirements may include Python, FastAPI,
        REST APIs, authentication and database integration.

        Database requirements may include PostgreSQL and SQL.

        AI requirements may include machine learning,
        NLP, LLMs, prompt engineering, embeddings,
        vector search and retrieval augmented generation.

        Additional requirements vary by employer and seniority.
        Some positions require Docker, cloud deployment,
        testing, Git and software engineering fundamentals.

        A fresher should check actual experience requirements
        rather than assuming every role is entry-level.
        """
    },
    {
        "id": "fresher_job_readiness",
        "category": "career_guidance",
        "title": "Fresher Software Developer Job Readiness",
        "content": """
        Freshers should demonstrate programming fundamentals,
        problem solving, database knowledge, API development,
        Git usage and practical project experience.

        A strong portfolio project should have working features,
        understandable architecture, meaningful documentation,
        tests and a demonstrable user interface.

        Candidates should be able to explain their own code,
        technical decisions, trade-offs and limitations.

        Skills currently demonstrated should be separated from
        technologies that are only planned or being studied.

        Job recommendations should consider experience,
        required skills, eligibility and role expectations.
        """
    },
    {
        "id": "resume_job_matching",
        "category": "career_guidance",
        "title": "Resume and Job Matching",
        "content": """
        Resume and job matching compares a candidate's profile
        with the requirements of a job description.

        Relevant information includes technical skills,
        project experience, education, work experience
        and job eligibility requirements.

        A matching system can identify matched skills,
        missing skills, relevant project evidence and
        experience gaps.

        Skill matching, lexical similarity and semantic similarity
        measure different aspects of relevance.

        A match score is not the probability of being hired.
        Recommendations should explain why a job is relevant
        and which requirements the candidate still lacks.
        """
    }
]


def get_all_documents() -> list[dict]:
    return CAREER_KNOWLEDGE_BASE


def get_document_by_id(document_id: str) -> dict | None:
    return next(
        (doc for doc in CAREER_KNOWLEDGE_BASE if doc["id"] == document_id),
        None
    )


def get_documents_by_category(category: str) -> list[dict]:
    return [
        doc for doc in CAREER_KNOWLEDGE_BASE
        if doc["category"].lower() == category.lower()
    ]
