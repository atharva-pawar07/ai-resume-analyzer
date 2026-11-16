SKILL_RECOMMENDATIONS = {
    "Python": {
        "reason": "Python is a core programming language for backend and AI development.",
        "suggestion": "Practice Python fundamentals, OOP, file handling, and problem-solving.",
        "project": "Build a Python-based task management application."
    },
    "FastAPI": {
        "reason": "FastAPI is useful for building modern Python REST APIs.",
        "suggestion": "Learn routing, Pydantic validation, dependency injection, and authentication.",
        "project": "Build a REST API with JWT authentication and PostgreSQL."
    },
    "React": {
        "reason": "React is widely used for building interactive frontend applications.",
        "suggestion": "Practice components, props, state, hooks, and API integration.",
        "project": "Build a React dashboard connected to your FastAPI backend."
    },
    "PostgreSQL": {
        "reason": "PostgreSQL is important for storing and managing application data.",
        "suggestion": "Practice joins, indexes, relationships, constraints, and SQL queries.",
        "project": "Build a database-backed job application tracker."
    },
    "SQL": {
        "reason": "SQL is essential for retrieving and managing relational data.",
        "suggestion": "Practice SELECT, JOIN, GROUP BY, subqueries, and aggregate functions.",
        "project": "Create a database for an employee management system."
    },
    "Git": {
        "reason": "Git helps developers track changes and collaborate on code.",
        "suggestion": "Practice commits, branches, merging, pull requests, and conflict resolution.",
        "project": "Manage a project using Git branches and GitHub."
    },
    "Machine Learning": {
        "reason": "Machine Learning helps applications learn patterns from data.",
        "suggestion": "Study NumPy, Pandas, scikit-learn, model training, and evaluation.",
        "project": "Build a basic job recommendation model."
    },
    "Artificial Intelligence": {
        "reason": "AI knowledge is useful for building intelligent applications.",
        "suggestion": "Learn AI fundamentals, LLMs, embeddings, and retrieval-augmented generation.",
        "project": "Build an AI-powered career assistant."
    },
    "JavaScript": {
        "reason": "JavaScript powers interactive web applications.",
        "suggestion": "Practice ES6+, asynchronous JavaScript, promises, and Fetch API.",
        "project": "Build an interactive job search dashboard."
    }
}


def generate_recommendations(missing_skills: list[str]) -> list[dict]:
    recommendations = []

    for skill in missing_skills:
        recommendation = SKILL_RECOMMENDATIONS.get(skill)

        if recommendation:
            recommendations.append({
                "skill": skill,
                **recommendation
            })

    return recommendations