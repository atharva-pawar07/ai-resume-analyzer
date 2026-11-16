
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
]


# --------------------------------------------------
# 2. JOB ROLE REQUIREMENTS
# --------------------------------------------------

ROLE_SKILLS = {
    "python developer": [
        "Python",
        "SQL",
        "Git",
        "Django",
        "FastAPI",
    ],

    "backend developer": [
        "Python",
        "FastAPI",
        "SQL",
        "PostgreSQL",
        "Git",
        "Docker",
    ],

    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "TypeScript",
        "Git",
    ],

    "full stack developer": [
        "Python",
        "FastAPI",
        "React",
        "JavaScript",
        "PostgreSQL",
        "HTML",
        "CSS",
        "Git",
    ],

    "full stack ai developer": [
        "Python",
        "FastAPI",
        "React",
        "JavaScript",
        "PostgreSQL",
        "SQL",
        "Machine Learning",
        "Artificial Intelligence",
        "Git",
    ],
}


# --------------------------------------------------
# 3. EXTRACT SKILLS FROM RESUME
# --------------------------------------------------

def extract_skills(resume_text: str) -> list[str]:
    """
    Identify known technical skills in resume text.
    """

    detected_skills = []

    text = resume_text.lower()

    for skill in SKILL_KEYWORDS:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            detected_skills.append(skill)

    return detected_skills


# --------------------------------------------------
# 4. GET REQUIRED SKILLS FOR JOB ROLE
# --------------------------------------------------

def get_required_skills(target_role: str) -> list[str]:
    """
    Return reference skills for the requested job role.
    """

    normalized_role = target_role.strip().lower()

    return ROLE_SKILLS.get(normalized_role, [])


# --------------------------------------------------
# 5. COMPARE DETECTED AND REQUIRED SKILLS
# --------------------------------------------------

def compare_skills(
    detected_skills: list[str],
    required_skills: list[str]
) -> dict:
    """
    Compare resume skills with job role requirements.
    """

    detected_set = {
        skill.lower()
        for skill in detected_skills
    }

    matched_skills = [
        skill
        for skill in required_skills
        if skill.lower() in detected_set
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in detected_set
    ]

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


# --------------------------------------------------
# 6. CALCULATE SKILL MATCH PERCENTAGE
# --------------------------------------------------

def calculate_skill_match(
    matched_skills: list[str],
    required_skills: list[str]
) -> float:
    """
    Calculate the percentage of required skills found
    in the resume.
    """

    if not required_skills:
        return 0.0

    percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(percentage, 2)


# --------------------------------------------------
# 7. COMPLETE RESUME ANALYSIS
# --------------------------------------------------

def analyze_resume(
    resume_text: str,
    target_role: str
) -> dict:
    """
    Analyze resume text against a target job role.
    """

    # Get role requirements
    required_skills = get_required_skills(target_role)

    # Handle unsupported job roles
    if not required_skills:
        return {
            "target_role": target_role,
            "error": "Unsupported job role",
            "message": (
                "We don't have skill requirements "
                "for this role yet."
            ),
        }

    # Extract skills from resume
    detected_skills = extract_skills(resume_text)

    # Compare detected and required skills
    skill_comparison = compare_skills(
        detected_skills,
        required_skills
    )

    matched_skills = skill_comparison["matched_skills"]
    missing_skills = skill_comparison["missing_skills"]

    # Calculate skill match percentage
    skill_match_percentage = calculate_skill_match(
        matched_skills,
        required_skills
    )

    # Return analysis report
    return {
        "target_role": target_role,
        "detected_skills": detected_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage,
    }
