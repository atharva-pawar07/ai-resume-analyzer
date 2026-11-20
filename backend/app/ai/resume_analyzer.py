
import re


# --------------------------------------------------
# 1. SKILL KEYWORDS
# --------------------------------------------------

SKILL_KEYWORDS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C++",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "SQLite",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "REST API",
    "Bootstrap",
    "Tailwind CSS",
    "Express.js",
    "Next.js",
    "Redis",
    "Linux",
]


# --------------------------------------------------
# 2. JOB ROLE REQUIREMENTS
# --------------------------------------------------

ROLE_SKILLS = {
    "python developer": [
        "Python", "SQL", "Git", "Django", "FastAPI",
    ],

    "backend developer": [
        "Python", "FastAPI", "SQL", "PostgreSQL", "Git", "Docker",
    ],

    "python backend developer": [
        "Python", "FastAPI", "SQL", "PostgreSQL", "Git",
    ],

    "frontend developer": [
        "HTML", "CSS", "JavaScript", "React", "TypeScript", "Git",
    ],

    "react developer": [
        "HTML", "CSS", "JavaScript", "React", "Git",
    ],

    "full stack developer": [
        "Python", "FastAPI", "React", "JavaScript",
        "PostgreSQL", "HTML", "CSS", "Git",
    ],

    "full stack ai developer": [
        "Python", "FastAPI", "React", "JavaScript",
        "PostgreSQL", "SQL", "Machine Learning",
        "Artificial Intelligence", "Git",
    ],

    "ai developer": [
        "Python", "Machine Learning", "Artificial Intelligence",
        "SQL", "Git", "FastAPI",
    ],

    "machine learning engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "Pandas", "NumPy",
    ],

    "data analyst": [
        "Python", "SQL", "Pandas", "NumPy", "Excel",
    ],

    "software developer": [
        "Python", "Java", "JavaScript", "SQL", "Git",
    ],

    "java developer": [
        "Java", "SQL", "Git", "Docker",
    ],

    "devops engineer": [
        "Python", "Linux", "Docker", "AWS", "Git",
    ],
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
    "software engineer": "software developer",
}


def normalize_role(target_role: str) -> str:
    normalized = re.sub(r"\s+", " ", target_role.strip().lower())
    return ROLE_ALIASES.get(normalized, normalized)


# --------------------------------------------------
# 4. EXTRACT SKILLS FROM RESUME
# --------------------------------------------------


def extract_skills(resume_text: str) -> list[str]:
    detected_skills = []
    text = resume_text.lower()

    for skill in SKILL_KEYWORDS:
        if skill == "REST API":
            pattern = r"(?<!\w)rest\s+apis?(?!\w)"
        else:
            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

        if re.search(pattern, text):
            detected_skills.append(skill)

    return detected_skills


def get_required_skills(target_role: str) -> list[str]:
    normalized_role = normalize_role(target_role)
    return ROLE_SKILLS.get(normalized_role, [])


# --------------------------------------------------
# 6. COMPARE DETECTED AND REQUIRED SKILLS
# --------------------------------------------------

def compare_skills(
    detected_skills: list[str],
    required_skills: list[str]
) -> dict:

    detected_set = {
        skill.lower()
        for skill in detected_skills
    }

    matched_skills = [
        skill for skill in required_skills
        if skill.lower() in detected_set
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in detected_set
    ]

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


# --------------------------------------------------
# 7. CALCULATE SKILL MATCH PERCENTAGE
# --------------------------------------------------

def calculate_skill_match(
    matched_skills: list[str],
    required_skills: list[str]
) -> float:

    if not required_skills:
        return 0.0

    percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(percentage, 2)


# --------------------------------------------------
# 8. COMPLETE RESUME ANALYSIS
# --------------------------------------------------

def analyze_resume(
    resume_text: str,
    target_role: str
) -> dict:

    required_skills = get_required_skills(target_role)

    if not required_skills:
        return {
            "target_role": target_role,
            "error": "Unsupported job role",
            "message": (
                "We don't have skill requirements "
                "for this role yet."
            ),
        }

    detected_skills = extract_skills(resume_text)

    skill_comparison = compare_skills(
        detected_skills,
        required_skills
    )

    matched_skills = skill_comparison["matched_skills"]
    missing_skills = skill_comparison["missing_skills"]

    skill_match_percentage = calculate_skill_match(
        matched_skills,
        required_skills
    )

    return {
        "target_role": target_role,
        "detected_skills": detected_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage,
    }
