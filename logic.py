# MERA FUTURE - BACKEND LOGIC
import os
import re
import sqlite3
import pandas as pd

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(
    BASE_DIR,
    "Database",
    "career_platform.db"
)

STUDENT_CSV = os.path.join(
    BASE_DIR,
    "student.csv"
)

COURSES_CSV = os.path.join(
    BASE_DIR,
    "student_online_courses.csv"
)

INTERNSHIPS_CSV = os.path.join(
    BASE_DIR,
    "student_internships.csv"
)

# DATABASE
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_students():
    conn = get_connection()

    try:
        df = pd.read_sql(
            "SELECT * FROM students ORDER BY student_id ASC",
            conn
        )
    finally:
        conn.close()

    return df


def get_next_student_id():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT MAX(student_id) FROM students"
        )

        result = cursor.fetchone()

    finally:
        conn.close()

    if result is None or result[0] is None:
        return 1

    return int(result[0]) + 1


# TEXT HELPERS
def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def normalize_text(value):
    value = clean_text(value).lower()

    value = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except:
        return default


# CAREER RECOMMENDATION
def recommend_career(student):

    skills = normalize_text(
        student.get("known_skills", "")
    )

    preferred_domain = normalize_text(
        student.get("preferred_domain", "")
    )

    career_goal = normalize_text(
        student.get("career_goal", "")
    )

    coding_level = normalize_text(
        student.get("coding_level", "")
    )

    technical = safe_float(
        student.get("technical_score", 0)
    )

    aptitude = safe_float(
        student.get("aptitude_score", 0)
    )

    problem_solving = safe_float(
        student.get("problem_solving_score", 0)
    )

    communication = safe_float(
        student.get("communication_score", 0)
    )

    careers = {
        "AI / ML Engineer": 0,
        "Data Analyst": 0,
        "Web Developer": 0,
        "Software Developer": 0,
        "Cybersecurity Analyst": 0,
        "Cloud Engineer": 0
    }

    # Skills
    if "python" in skills:
        careers["AI / ML Engineer"] += 3
        careers["Data Analyst"] += 2
        careers["Software Developer"] += 1

    if "machine learning" in skills:
        careers["AI / ML Engineer"] += 5

    if "numpy" in skills:
        careers["AI / ML Engineer"] += 2

    if "pandas" in skills:
        careers["AI / ML Engineer"] += 2
        careers["Data Analyst"] += 3

    if "sql" in skills:
        careers["Data Analyst"] += 4

    if "excel" in skills:
        careers["Data Analyst"] += 3

    if "html" in skills:
        careers["Web Developer"] += 3

    if "css" in skills:
        careers["Web Developer"] += 3

    if "javascript" in skills:
        careers["Web Developer"] += 4

    if "java" in skills:
        careers["Software Developer"] += 3

    if "oop" in skills:
        careers["Software Developer"] += 3

    if "networking" in skills:
        careers["Cybersecurity Analyst"] += 3

    if "linux" in skills:
        careers["Cybersecurity Analyst"] += 3

    if "security" in skills:
        careers["Cybersecurity Analyst"] += 4

    if "aws" in skills:
        careers["Cloud Engineer"] += 4

    if "azure" in skills:
        careers["Cloud Engineer"] += 4

    if "docker" in skills:
        careers["Cloud Engineer"] += 3

    # Preferred domain
    domain_map = {
        "ai": "AI / ML Engineer",
        "artificial intelligence": "AI / ML Engineer",
        "machine learning": "AI / ML Engineer",
        "ml": "AI / ML Engineer",
        "data": "Data Analyst",
        "data analysis": "Data Analyst",
        "web": "Web Developer",
        "web development": "Web Developer",
        "software": "Software Developer",
        "software development": "Software Developer",
        "cybersecurity": "Cybersecurity Analyst",
        "cyber security": "Cybersecurity Analyst",
        "cloud": "Cloud Engineer"
    }

    for key, career in domain_map.items():

        if key in preferred_domain:
            careers[career] += 5

        if key in career_goal:
            careers[career] += 5

    # Coding
    if coding_level in ["advanced", "high"]:
        careers["AI / ML Engineer"] += 2
        careers["Software Developer"] += 2
        careers["Web Developer"] += 2

    elif coding_level in ["intermediate", "medium"]:
        careers["Data Analyst"] += 2
        careers["Web Developer"] += 2
        careers["Software Developer"] += 2

    # Scores
    if technical >= 80:
        careers["AI / ML Engineer"] += 2
        careers["Software Developer"] += 2
        careers["Cloud Engineer"] += 2

    if aptitude >= 80:
        careers["Data Analyst"] += 2
        careers["AI / ML Engineer"] += 2

    if problem_solving >= 80:
        careers["AI / ML Engineer"] += 2
        careers["Software Developer"] += 2
        careers["Cybersecurity Analyst"] += 2

    if communication >= 80:
        careers["Data Analyst"] += 1
        careers["Web Developer"] += 1

    best_career = max(
        careers,
        key=careers.get
    )

    return best_career, careers


# REQUIRED SKILLS
def get_required_skills(career):

    skills = {

        "AI / ML Engineer": [
            "Python",
            "NumPy",
            "Pandas",
            "Machine Learning",
            "Scikit-learn",
            "Statistics"
        ],

        "Data Analyst": [
            "SQL",
            "Excel",
            "Python",
            "Statistics",
            "Pandas",
            "Power BI"
        ],

        "Web Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ],

        "Software Developer": [
            "Python",
            "Java",
            "OOP",
            "Data Structures",
            "Algorithms",
            "Git"
        ],

        "Cybersecurity Analyst": [
            "Networking",
            "Linux",
            "Security",
            "Ethical Hacking"
        ],

        "Cloud Engineer": [
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes",
            "DevOps"
        ]
    }

    return skills.get(
        career,
        []
    )


# SKILL GAP
def calculate_skill_gap(student, career):

    known_skills = normalize_text(
        student.get("known_skills", "")
    )

    required_skills = get_required_skills(
        career
    )

    current_skills = []
    missing_skills = []

    for skill in required_skills:

        if normalize_text(skill) in known_skills:
            current_skills.append(skill)
        else:
            missing_skills.append(skill)

    return missing_skills


# RESUME SCORE
def calculate_resume_score(student):

    skills = clean_text(
        student.get("known_skills", "")
    )

    certification = clean_text(
        student.get("certification", "")
    )

    projects = safe_int(
        student.get("projects_completed", 0)
    )

    internship = safe_int(
        student.get("internship_months", 0)
    )

    cgpa = safe_float(
        student.get("cgpa", 0)
    )

    skill_list = [
        x.strip()
        for x in re.split(
            r"[,;]",
            skills
        )
        if x.strip()
    ]

    skill_score = min(
        len(skill_list) * 5,
        25
    )

    if certification.lower() in [
        "",
        "none",
        "nan"
    ]:
        certification_score = 5
    else:
        certification_score = 20

    project_score = min(
        projects * 6,
        25
    )

    internship_score = min(
        internship * 4,
        20
    )

    academic_score = min(
        cgpa * 1.2,
        10
    )

    total = (
        skill_score
        + certification_score
        + project_score
        + internship_score
        + academic_score
    )

    suggestions = []

    if len(skill_list) < 4:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if projects < 2:
        suggestions.append(
            "Add more practical projects."
        )

    if internship < 3:
        suggestions.append(
            "Add internship experience."
        )

    if certification.lower() in [
        "",
        "none",
        "nan"
    ]:
        suggestions.append(
            "Add relevant certifications."
        )

    return round(total, 1), suggestions


# READINESS
def calculate_readiness(student):

    cgpa = safe_float(
        student.get("cgpa", 0)
    )

    technical = safe_float(
        student.get("technical_score", 0)
    )

    aptitude = safe_float(
        student.get("aptitude_score", 0)
    )

    problem = safe_float(
        student.get("problem_solving_score", 0)
    )

    communication = safe_float(
        student.get("communication_score", 0)
    )

    projects = safe_int(
        student.get("projects_completed", 0)
    )

    internship = safe_int(
        student.get("internship_months", 0)
    )

    github = safe_int(
        student.get("github_projects", 0)
    )

    certification = clean_text(
        student.get("certification", "")
    )

    score = (
        (cgpa / 10) * 20
        + technical * 0.15
        + aptitude * 0.10
        + problem * 0.15
        + communication * 0.10
        + min(projects * 2, 10)
        + min(internship * 2, 10)
        + min(github, 5)
    )

    if certification.lower() not in [
        "",
        "none",
        "nan"
    ]:
        score += 5

    return round(
        min(max(score, 0), 100),
        1
    )


# COURSES
def find_courses(courses_df, student, career):

    if courses_df is None or courses_df.empty:
        return []

    result = courses_df.copy()

    search_text = " ".join([
        normalize_text(career),
        normalize_text(
            student.get("preferred_domain", "")
        ),
        normalize_text(
            student.get("career_goal", "")
        )
    ])

    matched = []

    for _, row in result.iterrows():

        row_text = " ".join(
            normalize_text(value)
            for value in row.astype(str).tolist()
        )

        if (
            career.lower() in row_text
            or any(
                word in row_text
                for word in search_text.split()
                if len(word) > 2
            )
        ):
            matched.append(
                row.to_dict()
            )

    return matched


# INTERNSHIPS
def find_internships(
    internships_df,
    student,
    career
):

    if (
        internships_df is None
        or internships_df.empty
    ):
        return []

    cgpa = safe_float(
        student.get("cgpa", 0)
    )

    search_text = " ".join([
        normalize_text(career),
        normalize_text(
            student.get("preferred_domain", "")
        ),
        normalize_text(
            student.get("career_goal", "")
        )
    ])

    matched = []

    for _, row in internships_df.iterrows():

        row_text = " ".join(
            normalize_text(value)
            for value in row.astype(str).tolist()
        )

        career_match = any(
            word in row_text
            for word in search_text.split()
            if len(word) > 2
        )

        if not career_match:
            continue

        if "eligibility_cgpa" in row.index:

            required_cgpa = safe_float(
                row["eligibility_cgpa"]
            )

            if required_cgpa > cgpa:
                continue

        matched.append(
            row.to_dict()
        )

    return matched


# MOCK INTERVIEW
def get_interview_questions(career):

    questions = {

        "AI / ML Engineer": [
            "What is Machine Learning?",
            "Explain supervised and unsupervised learning.",
            "What is overfitting?"
        ],

        "Data Analyst": [
            "What is data analysis?",
            "What is the difference between SQL and Excel?",
            "What is data visualization?"
        ],

        "Web Developer": [
            "What is HTML?",
            "What is CSS?",
            "What is JavaScript?"
        ],

        "Software Developer": [
            "What is OOP?",
            "What is inheritance?",
            "What is a data structure?"
        ],

        "Cybersecurity Analyst": [
            "What is cybersecurity?",
            "What is phishing?",
            "What is a firewall?"
        ],

        "Cloud Engineer": [
            "What is cloud computing?",
            "What is AWS?",
            "What is virtualization?"
        ]
    }

    return questions.get(
        career,
        [
            "Tell me about yourself.",
            "What are your technical skills?",
            "What are your career goals?"
        ]
    )


def evaluate_interview_answer(
    career,
    question_index,
    answer
):

    answer = clean_text(answer)

    if not answer:
        return {
            "score": 0,
            "feedback": "Please provide an answer."
        }

    length = len(answer.split())

    if length < 5:
        score = 40
        feedback = (
            "Your answer is very short. "
            "Try explaining your answer with an example."
        )

    elif length < 15:
        score = 65
        feedback = (
            "Good start. Add more technical details "
            "and a practical example."
        )

    else:
        score = 85
        feedback = (
            "Good answer. Try to keep it structured "
            "and include practical examples."
        )

    return {
        "score": score,
        "feedback": feedback
    }


# LOAD CSV DATA
def load_courses():

    try:
        return pd.read_csv(
            COURSES_CSV
        )
    except:
        return pd.DataFrame()


def load_internships():

    try:
        return pd.read_csv(
            INTERNSHIPS_CSV
        )
    except:
        return pd.DataFrame()


# CLEAN API RECORDS
def clean_records(df):

    if df is None:
        return []

    if isinstance(df, pd.DataFrame):
        records = df.to_dict(
            orient="records"
        )
    else:
        records = df

    cleaned = []

    for record in records:

        item = {}

        for key, value in record.items():

            if pd.isna(value):
                item[key] = None
            else:
                item[key] = value

        cleaned.append(item)

    return cleaned