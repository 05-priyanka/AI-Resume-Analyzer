import re


SKILL_LIST = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "javascript",
    "react",
    "angular",
    "node.js",
    "django",
    "flask",
    "git",
    "github",
    "linux",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "data visualization",
    "artificial intelligence",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "rest api",
    "api",
    "data structures",
    "algorithms",
    "object oriented programming",
    "operating systems",
    "dbms",
    "computer networks"
]


SKILL_DISPLAY_NAMES = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "c": "C",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "react": "React",
    "angular": "Angular",
    "node.js": "Node.js",
    "django": "Django",
    "flask": "Flask",
    "git": "Git",
    "github": "GitHub",
    "linux": "Linux",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "scikit-learn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "data visualization": "Data Visualization",
    "artificial intelligence": "Artificial Intelligence",
    "excel": "Excel",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "aws": "AWS",
    "azure": "Azure",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "rest api": "REST API",
    "api": "API",
    "data structures": "Data Structures",
    "algorithms": "Algorithms",
    "object oriented programming": "Object Oriented Programming",
    "operating systems": "Operating Systems",
    "dbms": "DBMS",
    "computer networks": "Computer Networks"
}


SKILL_ALIASES = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machinelearning": "machine learning",
    "ai": "artificial intelligence",
    "artificial-intelligence": "artificial intelligence",
    "rest": "rest api",
    "restful api": "rest api",
    "restful": "rest api",
    "postgres": "sql",
    "data structure": "data structures",
    "algorithm": "algorithms",
    "dsa": "data structures",
    "nodejs": "node.js",
    "git hub": "github"
}


def normalize_text(text):

    if not text:
        return ""

    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text


def normalize_for_matching(text):

    if not text:
        return ""

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("\xa0", " ")

    text = re.sub(
        r"[/|,;:(){}\[\]]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def skill_present(text, skill):

    text = normalize_for_matching(text)

    skill = skill.lower()

    if skill == "c++":

        return bool(
            re.search(
                r"(?<!\w)c\+\+(?!\w)",
                text
            )
        )

    if skill == "c":

        return bool(
            re.search(
                r"(?<!\w)c(?!\w)",
                text
            )
        )

    if skill == "node.js":

        return bool(
            re.search(
                r"(?<!\w)node\.?js(?!\w)",
                text
            )
        )

    if skill == "rest api":

        return bool(
            re.search(
                r"\brest\s*(?:ful\s*)?api\b",
                text
            )
        )

    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text
        )
    )


def extract_skills(resume_text):

    if not resume_text:
        return []

    text = normalize_for_matching(
        resume_text
    )

    detected_skills = []

    for skill in SKILL_LIST:

        if skill_present(
            text,
            skill
        ):

            display_name = SKILL_DISPLAY_NAMES.get(
                skill,
                skill.title()
            )

            detected_skills.append(
                display_name
            )

    return sorted(
        set(detected_skills),
        key=str.lower
    )


def detect_section(text, section):

    if not text:
        return False

    text = normalize_text(text)

    lines = text.splitlines()

    if section == "Professional Summary":

        cleaned_text = text.lower()

        cleaned_text = re.sub(
            r"[^a-z\s]",
            " ",
            cleaned_text
        )

        cleaned_text = re.sub(
            r"\s+",
            " ",
            cleaned_text
        )

        summary_words = [
            "professional summary",
            "professional profile",
            "summary",
            "objective",
            "profile"
        ]

        for word in summary_words:

            if word in cleaned_text:
                return True

        return False


    if section == "Technical Skills":

        patterns = [
            r"^\s*technical\s+skills?\s*:?\s*$",
            r"^\s*skills?\s*:?\s*$",
            r"^\s*programming\s+skills?\s*:?\s*$",
            r"^\s*technical\s+expertise\s*:?\s*$"
        ]

        return any(
            re.fullmatch(
                pattern,
                line.strip().lower()
            )
            for line in lines
            for pattern in patterns
        )


    if section == "Education":

        patterns = [
            r"^\s*education\s*:?\s*$",
            r"^\s*academic\s+background\s*:?\s*$",
            r"^\s*educational\s+qualification\s*:?\s*$"
        ]

        return any(
            re.fullmatch(
                pattern,
                line.strip().lower()
            )
            for line in lines
            for pattern in patterns
        )


    if section == "Projects":

        patterns = [
            r"^\s*projects?\s*:?\s*$",
            r"^\s*personal\s+projects?\s*:?\s*$",
            r"^\s*academic\s+projects?\s*:?\s*$",
            r"^\s*project\s+experience\s*:?\s*$"
        ]

        return any(
            re.fullmatch(
                pattern,
                line.strip().lower()
            )
            for line in lines
            for pattern in patterns
        )


    if section == "Experience":

        patterns = [
            r"^\s*experience\s*:?\s*$",
            r"^\s*work\s+experience\s*:?\s*$",
            r"^\s*professional\s+experience\s*:?\s*$",
            r"^\s*internship\s+experience\s*:?\s*$",
            r"^\s*work\s+history\s*:?\s*$"
        ]

        return any(
            re.fullmatch(
                pattern,
                line.strip().lower()
            )
            for line in lines
            for pattern in patterns
        )


    if section == "Certifications":

        patterns = [
            r"^\s*certifications?\s*:?\s*$",
            r"^\s*professional\s+certifications?\s*:?\s*$",
            r"^\s*certificates?\s*:?\s*$"
        ]

        return any(
            re.fullmatch(
                pattern,
                line.strip().lower()
            )
            for line in lines
            for pattern in patterns
        )


    if section == "Contact Information":

        contact_patterns = [
            r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
            r"\b(?:linkedin\.com|github\.com)\b",
            r"\b(?:phone|mobile|contact)\b",
            r"\b\d{10}\b"
        ]

        return any(
            re.search(
                pattern,
                text,
                re.IGNORECASE
            )
            for pattern in contact_patterns
        )

    return False


def calculate_resume_score(resume_text):

    if not resume_text:
        return 0, {}

    sections = {
        "Professional Summary": False,
        "Technical Skills": False,
        "Education": False,
        "Projects": False,
        "Experience": False,
        "Certifications": False,
        "Contact Information": False
    }

    for section in sections:

        sections[section] = detect_section(
            resume_text,
            section
        )

    skills = extract_skills(
        resume_text
    )

    text = normalize_for_matching(
        resume_text
    )

    word_count = len(
        text.split()
    )

    score = 0

    if sections["Professional Summary"]:
        score += 15

    if sections["Technical Skills"]:
        score += 15

    if sections["Education"]:
        score += 15

    if sections["Projects"]:
        score += 15

    if sections["Certifications"]:
        score += 10

    if sections["Contact Information"]:
        score += 10

    if sections["Experience"]:
        score += 5

    if len(skills) >= 10:
        score += 10

    elif len(skills) >= 7:
        score += 8

    elif len(skills) >= 5:
        score += 6

    elif len(skills) >= 3:
        score += 4

    elif len(skills) > 0:
        score += 2

    if word_count >= 400:
        score += 5

    elif word_count >= 300:
        score += 4

    elif word_count >= 200:
        score += 3

    elif word_count >= 100:
        score += 2

    elif word_count > 0:
        score += 1

    score = min(
        score,
        100
    )

    return score, sections


def canonical_skill(skill):

    skill = skill.lower().strip()

    return SKILL_ALIASES.get(
        skill,
        skill
    )


def get_matching_skills(text):

    detected = extract_skills(
        text
    )

    canonical = set()

    for skill in detected:

        canonical.add(
            canonical_skill(
                skill
            )
        )

    if "rest api" in canonical:
        canonical.add("api")

    if (
        "sql" in canonical
        or "mysql" in canonical
        or "postgresql" in canonical
    ):
        canonical.add("sql")

    return canonical


def match_job_description(
    resume_text,
    job_description
):

    if not resume_text or not job_description:
        return 0, [], []

    resume_skills = get_matching_skills(
        resume_text
    )

    job_skills = get_matching_skills(
        job_description
    )

    if not job_skills:
        return 0, [], []

    matched_skills = (
        resume_skills.intersection(
            job_skills
        )
    )

    missing_skills = (
        job_skills.difference(
            resume_skills
        )
    )

    if "rest api" in matched_skills:
        matched_skills.discard("api")

    if "rest api" in missing_skills:
        missing_skills.discard("api")

    match_score = round(
        (
            len(matched_skills)
            / len(job_skills)
        ) * 100
    )

    matched = sorted(
        [
            SKILL_DISPLAY_NAMES.get(
                skill,
                skill.title()
            )
            for skill in matched_skills
        ]
    )

    missing = sorted(
        [
            SKILL_DISPLAY_NAMES.get(
                skill,
                skill.title()
            )
            for skill in missing_skills
        ]
    )

    return (
        match_score,
        matched,
        missing
    )


def generate_resume_feedback(
    resume_text,
    section_scores=None,
    skills=None
):

    if section_scores is None:

        _, section_scores = calculate_resume_score(
            resume_text
        )

    if skills is None:

        skills = extract_skills(
            resume_text
        )

    strengths = []
    improvements = []
    recommendations = []


    if section_scores.get(
        "Professional Summary",
        False
    ):

        strengths.append(
            "Professional Summary section is present"
        )


    if section_scores.get(
        "Technical Skills",
        False
    ):

        strengths.append(
            "Technical Skills section is present"
        )


    if section_scores.get(
        "Education",
        False
    ):

        strengths.append(
            "Education details are included"
        )


    if section_scores.get(
        "Projects",
        False
    ):

        strengths.append(
            "Projects section is included"
        )


    if section_scores.get(
        "Experience",
        False
    ):

        strengths.append(
            "Experience information is included"
        )


    if section_scores.get(
        "Certifications",
        False
    ):

        strengths.append(
            "Certifications are included"
        )


    if section_scores.get(
        "Contact Information",
        False
    ):

        strengths.append(
            "Contact information is available"
        )


    if len(skills) >= 5:

        strengths.append(
            "Good technical skill coverage"
        )

    elif len(skills) > 0:

        improvements.append(
            "Consider adding more relevant technical skills"
        )

    else:

        improvements.append(
            "No technical skills were detected"
        )


    if not section_scores.get(
        "Professional Summary",
        False
    ):

        improvements.append(
            "Consider adding a Professional Summary section"
        )


    if not section_scores.get(
        "Projects",
        False
    ):

        improvements.append(
            "Consider adding projects that demonstrate your skills"
        )


    if not section_scores.get(
        "Certifications",
        False
    ):

        improvements.append(
            "Consider adding relevant certifications"
        )


    if not section_scores.get(
        "Experience",
        False
    ):

        improvements.append(
            "Internship or work experience can strengthen "
            "your resume, but it is optional for students."
        )


    skills_lower = {
        skill.lower()
        for skill in skills
    }


    if (
        "machine learning" not in skills_lower
        and "artificial intelligence" not in skills_lower
    ):

        recommendations.append(
            "Consider adding Machine Learning skills or "
            "projects if relevant to your Data Science career goals."
        )


    if (
        "sql" not in skills_lower
        and "mysql" not in skills_lower
        and "postgresql" not in skills_lower
    ):

        recommendations.append(
            "Consider strengthening your SQL and database skills."
        )


    if (
        "data structures" not in skills_lower
        and "algorithms" not in skills_lower
    ):

        recommendations.append(
            "Consider strengthening your Data Structures and Algorithms skills."
        )


    if (
        "git" not in skills_lower
        and "github" not in skills_lower
    ):

        recommendations.append(
            "Consider adding Git and GitHub experience."
        )


    if not section_scores.get(
        "Experience",
        False
    ):

        recommendations.append(
            "Build practical experience through internships, "
            "academic projects, freelance work, or open-source contributions."
        )


    return (
        strengths,
        improvements,
        recommendations
    )


def generate_job_suggestions(missing_skills):

    suggestions = []


    suggestion_map = {

        "Algorithms":
            "Strengthen your Algorithms knowledge by adding "
            "projects involving sorting, searching, graphs, "
            "dynamic programming, or problem solving.",

        "Data Structures":
            "Add practical Data Structures projects or "
            "demonstrate knowledge of arrays, linked lists, "
            "trees, graphs, stacks, and queues.",

        "Machine Learning":
            "Consider adding a Machine Learning project such "
            "as prediction, classification, recommendation, "
            "or sentiment analysis.",

        "SQL":
            "Add SQL-based projects demonstrating joins, "
            "subqueries, aggregation, normalization, and "
            "database design.",

        "REST API":
            "Build or add a project that consumes or creates "
            "REST APIs using Python, Flask, Django, Node.js, "
            "or another backend framework.",

        "API":
            "Demonstrate API development or integration in "
            "one of your projects.",

        "Git":
            "Showcase Git usage through a GitHub project "
            "with commits, branches, and version control.",

        "GitHub":
            "Add relevant GitHub projects and keep your "
            "repositories organized with clear README files.",

        "React":
            "Consider adding a React-based project to "
            "demonstrate frontend development skills.",

        "Python":
            "Add a Python project demonstrating practical "
            "problem-solving or data processing.",

        "Data Analysis":
            "Add a data analysis project using Pandas, "
            "NumPy, Matplotlib, or similar tools."
    }


    for skill in missing_skills:

        if skill in suggestion_map:

            suggestions.append(
                suggestion_map[skill]
            )

        else:

            suggestions.append(
                f"Consider learning or demonstrating "
                f"{skill} through a relevant project."
            )


    return suggestions