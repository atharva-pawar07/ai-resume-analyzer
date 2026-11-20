
# --------------------------------------------------
# 1. SKILL LEARNING DATABASE
# --------------------------------------------------

SKILL_RECOMMENDATIONS = {
    "Python": {
        "priority": "High",
        "duration": "2 weeks",
        "reason": "Python is essential for backend development and AI applications.",
        "topics": [
            "Python fundamentals and data types",
            "Functions and modules",
            "Object-oriented programming",
            "File handling and exception handling",
            "Virtual environments and packages"
        ],
        "suggestion": "Practice Python fundamentals and solve programming problems.",
        "project": "Build a Python-based job application tracker."
    },

    "FastAPI": {
        "priority": "High",
        "duration": "2 weeks",
        "reason": "FastAPI is useful for building modern Python backend services.",
        "topics": [
            "Routes and HTTP methods",
            "Path and query parameters",
            "Pydantic validation",
            "Dependency injection",
            "Authentication and database integration"
        ],
        "suggestion": "Build REST APIs and connect them to PostgreSQL.",
        "project": "Build a REST API with JWT authentication and PostgreSQL."
    },

    "React": {
        "priority": "High",
        "duration": "3 weeks",
        "reason": "React is important for building interactive frontend applications.",
        "topics": [
            "Components and JSX",
            "Props and state",
            "Events and forms",
            "useEffect and other hooks",
            "API integration and routing"
        ],
        "suggestion": "Practice components, state management, hooks, and API integration.",
        "project": "Build a React dashboard connected to a FastAPI backend."
    },

    "JavaScript": {
        "priority": "High",
        "duration": "2 weeks",
        "reason": "JavaScript powers interactive web applications and React development.",
        "topics": [
            "Variables and data types",
            "Functions and array methods",
            "Objects and destructuring",
            "Promises and async/await",
            "Fetch API and error handling"
        ],
        "suggestion": "Practice modern JavaScript and asynchronous programming.",
        "project": "Build an interactive job search dashboard."
    },

    "PostgreSQL": {
        "priority": "High",
        "duration": "2 weeks",
        "reason": "PostgreSQL is useful for managing application data and relationships.",
        "topics": [
            "Tables and data types",
            "Primary and foreign keys",
            "JOIN operations",
            "Indexes and constraints",
            "Transactions"
        ],
        "suggestion": "Practice SQL queries and database relationships.",
        "project": "Build a database-backed job application tracker."
    },

    "SQL": {
        "priority": "High",
        "duration": "2 weeks",
        "reason": "SQL is essential for retrieving and managing relational data.",
        "topics": [
            "SELECT and filtering",
            "INSERT, UPDATE, and DELETE",
            "JOIN operations",
            "GROUP BY and aggregate functions",
            "Subqueries"
        ],
        "suggestion": "Solve practical SQL exercises using sample databases.",
        "project": "Create an employee management database."
    },

    "Git": {
        "priority": "Medium",
        "duration": "1 week",
        "reason": "Git helps developers track changes and collaborate on projects.",
        "topics": [
            "Repositories and commits",
            "Branches",
            "Merging",
            "Resolving conflicts",
            "Pull requests"
        ],
        "suggestion": "Practice Git through regular project commits.",
        "project": "Manage a project using feature branches on GitHub."
    },

    "Machine Learning": {
        "priority": "High",
        "duration": "4 weeks",
        "reason": "Machine Learning helps applications identify patterns and make predictions.",
        "topics": [
            "Supervised and unsupervised learning",
            "Data preprocessing",
            "Feature engineering",
            "Model training",
            "Model evaluation"
        ],
        "suggestion": "Learn NumPy, Pandas, and scikit-learn before building models.",
        "project": "Build a basic job recommendation model."
    },

    "Artificial Intelligence": {
        "priority": "High",
        "duration": "3 weeks",
        "reason": "AI fundamentals help developers build intelligent applications.",
        "topics": [
            "AI fundamentals",
            "Machine Learning basics",
            "Large Language Models",
            "Embeddings and vector search",
            "Retrieval-Augmented Generation"
        ],
        "suggestion": "Study AI concepts and experiment with retrieval-based applications.",
        "project": "Build an AI-powered career assistant."
    },

    "HTML": {
        "priority": "Medium",
        "duration": "1 week",
        "reason": "HTML provides the structure of web applications.",
        "topics": [
            "Semantic HTML",
            "Forms and inputs",
            "Tables and lists",
            "Accessibility basics"
        ],
        "suggestion": "Practice building accessible web page structures.",
        "project": "Build a structured portfolio website."
    },

    "CSS": {
        "priority": "Medium",
        "duration": "1 week",
        "reason": "CSS is needed to create responsive and usable interfaces.",
        "topics": [
            "Selectors and box model",
            "Flexbox",
            "CSS Grid",
            "Responsive design",
            "Media queries"
        ],
        "suggestion": "Practice responsive layouts and reusable styling.",
        "project": "Build a responsive career dashboard."
    },

    "Docker": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "Docker helps package applications and their dependencies.",
        "topics": [
            "Images and containers",
            "Dockerfiles",
            "Ports and volumes",
            "Environment variables",
            "Docker Compose"
        ],
        "suggestion": "Containerize a small backend application.",
        "project": "Run a FastAPI and PostgreSQL application using Docker Compose."
    },

    "Django": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "Django is a Python framework for building web applications.",
        "topics": [
            "Models and ORM",
            "Views and URLs",
            "Templates",
            "Forms",
            "Authentication"
        ],
        "suggestion": "Learn Django's request-response flow and ORM.",
        "project": "Build a job application management website."
    },

    "Node.js": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "Node.js enables server-side JavaScript development.",
        "topics": [
            "Node.js fundamentals",
            "Modules",
            "Asynchronous programming",
            "HTTP servers",
            "API development"
        ],
        "suggestion": "Understand the Node.js runtime and asynchronous operations.",
        "project": "Build a simple REST API."
    },

    "TypeScript": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "TypeScript adds static type checking to JavaScript applications.",
        "topics": [
            "Basic types",
            "Interfaces and type aliases",
            "Functions and generics",
            "Type narrowing",
            "React with TypeScript"
        ],
        "suggestion": "Convert a small JavaScript application to TypeScript.",
        "project": "Build a typed React job dashboard."
    },

    "AWS": {
        "priority": "Medium",
        "duration": "3 weeks",
        "reason": "AWS provides cloud infrastructure for deploying applications.",
        "topics": [
            "Cloud fundamentals",
            "IAM basics",
            "Compute services",
            "Storage services",
            "Application deployment"
        ],
        "suggestion": "Understand cloud fundamentals and deploy a small application.",
        "project": "Deploy a FastAPI application to a cloud environment."
    },

    "Linux": {
        "priority": "Medium",
        "duration": "1 week",
        "reason": "Linux skills are useful for development and deployment environments.",
        "topics": [
            "File system navigation",
            "File permissions",
            "Shell commands",
            "Processes",
            "Environment variables"
        ],
        "suggestion": "Practice common Linux commands in a development environment.",
        "project": "Create a shell script to automate project setup."
    },

    "Deep Learning": {
        "priority": "High",
        "duration": "4 weeks",
        "reason": "Deep Learning supports advanced AI applications and neural network development.",
        "topics": [
            "Neural network fundamentals",
            "Activation functions",
            "Backpropagation",
            "Convolutional neural networks",
            "Model evaluation"
        ],
        "suggestion": "Study neural networks and experiment with small datasets.",
        "project": "Build an image classification model."
    },

    "NumPy": {
        "priority": "Medium",
        "duration": "1 week",
        "reason": "NumPy provides efficient numerical computing tools for Python.",
        "topics": [
            "Arrays",
            "Array indexing",
            "Array operations",
            "Broadcasting",
            "Linear algebra basics"
        ],
        "suggestion": "Practice numerical operations using Python arrays.",
        "project": "Build a small numerical data analysis tool."
    },

    "Pandas": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "Pandas is useful for cleaning, processing, and analyzing datasets.",
        "topics": [
            "Series and DataFrames",
            "Reading CSV files",
            "Filtering and sorting",
            "Handling missing data",
            "Grouping and aggregation"
        ],
        "suggestion": "Practice data cleaning and analysis with real datasets.",
        "project": "Build a job market data analysis dashboard."
    },

    "TensorFlow": {
        "priority": "Medium",
        "duration": "3 weeks",
        "reason": "TensorFlow is a framework for developing and training machine learning models.",
        "topics": [
            "Tensors",
            "Keras basics",
            "Building neural networks",
            "Model training",
            "Model evaluation"
        ],
        "suggestion": "Start with small neural network experiments.",
        "project": "Build a simple classification model."
    },

    "PyTorch": {
        "priority": "Medium",
        "duration": "3 weeks",
        "reason": "PyTorch is widely used for deep learning and AI research.",
        "topics": [
            "Tensors",
            "Autograd",
            "Neural network modules",
            "Training loops",
            "Model evaluation"
        ],
        "suggestion": "Practice building and training small neural networks.",
        "project": "Build a basic text classification model."
    },

    "Scikit-learn": {
        "priority": "Medium",
        "duration": "2 weeks",
        "reason": "Scikit-learn provides practical tools for traditional machine learning.",
        "topics": [
            "Data preprocessing",
            "Train-test split",
            "Classification",
            "Regression",
            "Model evaluation"
        ],
        "suggestion": "Train and evaluate models using structured datasets.",
        "project": "Build a job recommendation prototype."
    }
}


# --------------------------------------------------
# 2. ROLE-SPECIFIC PRIORITIES
# --------------------------------------------------

ROLE_PRIORITY = {
    "full stack ai developer": {
        "high": [
            "Python",
            "FastAPI",
            "React",
            "JavaScript",
            "PostgreSQL",
            "SQL",
            "Artificial Intelligence",
            "Machine Learning"
        ],
        "medium": [
            "HTML",
            "CSS",
            "Git",
            "Docker",
            "NumPy",
            "Pandas",
            "Scikit-learn"
        ]
    },

    "full stack developer": {
        "high": [
            "Python",
            "FastAPI",
            "React",
            "JavaScript",
            "PostgreSQL",
            "SQL"
        ],
        "medium": [
            "HTML",
            "CSS",
            "Git",
            "Docker",
            "TypeScript"
        ]
    },

    "backend developer": {
        "high": [
            "Python",
            "FastAPI",
            "SQL",
            "PostgreSQL"
        ],
        "medium": [
            "Git",
            "Docker",
            "Linux",
            "AWS"
        ]
    },

    "python backend developer": {
        "high": [
            "Python",
            "FastAPI",
            "SQL",
            "PostgreSQL"
        ],
        "medium": [
            "Git",
            "Docker",
            "Linux"
        ]
    },

    "python developer": {
        "high": [
            "Python",
            "SQL",
            "FastAPI"
        ],
        "medium": [
            "Django",
            "Git",
            "PostgreSQL"
        ]
    },

    "frontend developer": {
        "high": [
            "HTML",
            "CSS",
            "JavaScript",
            "React"
        ],
        "medium": [
            "TypeScript",
            "Git"
        ]
    },

    "react developer": {
        "high": [
            "HTML",
            "CSS",
            "JavaScript",
            "React"
        ],
        "medium": [
            "TypeScript",
            "Git"
        ]
    },

    "ai developer": {
        "high": [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "FastAPI"
        ],
        "medium": [
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "SQL",
            "Git"
        ]
    },

    "machine learning engineer": {
        "high": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NumPy",
            "Pandas",
            "Scikit-learn"
        ],
        "medium": [
            "TensorFlow",
            "PyTorch",
            "SQL",
            "Git"
        ]
    },

    "data analyst": {
        "high": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy"
        ],
        "medium": [
            "Scikit-learn",
            "Git"
        ]
    },

    "software developer": {
        "high": [
            "Python",
            "Java",
            "JavaScript",
            "SQL"
        ],
        "medium": [
            "Git",
            "Docker"
        ]
    },

    "java developer": {
        "high": [
            "Java",
            "SQL"
        ],
        "medium": [
            "Git",
            "Docker"
        ]
    },

    "devops engineer": {
        "high": [
            "Linux",
            "Docker",
            "AWS",
            "Git"
        ],
        "medium": [
            "Python"
        ]
    }
}


# --------------------------------------------------
# 3. ROLE NORMALIZATION
# --------------------------------------------------

ROLE_ALIASES = {
    "fullstack developer": "full stack developer",
    "full-stack developer": "full stack developer",
    "fullstack ai developer": "full stack ai developer",
    "full-stack ai developer": "full stack ai developer",
    "ai engineer": "ai developer",
    "ml engineer": "machine learning engineer",
    "frontend engineer": "frontend developer",
    "backend engineer": "backend developer",
    "software engineer": "software developer"
}


def normalize_role(target_role: str) -> str:
    normalized = " ".join(target_role.strip().lower().split())
    return ROLE_ALIASES.get(normalized, normalized)


# --------------------------------------------------
# 4. DETERMINE ROLE-SPECIFIC PRIORITY
# --------------------------------------------------

def get_skill_priority(
    skill: str,
    target_role: str
) -> str:

    normalized_role = normalize_role(target_role)
    role_config = ROLE_PRIORITY.get(normalized_role)

    if not role_config:
        return SKILL_RECOMMENDATIONS.get(
            skill, {}
        ).get("priority", "Medium")

    if skill in role_config["high"]:
        return "High"

    if skill in role_config["medium"]:
        return "Medium"

    return "Low"


# --------------------------------------------------
# 5. GENERATE PERSONALIZED RECOMMENDATIONS
# --------------------------------------------------

def generate_recommendations(
    missing_skills: list[str],
    target_role: str = ""
) -> list[dict]:

    recommendations = []

    for skill in missing_skills:

        recommendation = SKILL_RECOMMENDATIONS.get(skill)

        if not recommendation:
            continue

        personalized_recommendation = {
            "skill": skill,
            **recommendation,
            "priority": get_skill_priority(
                skill,
                target_role
            )
        }

        recommendations.append(
            personalized_recommendation
        )

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item["priority"], 3
        )
    )

    return recommendations
