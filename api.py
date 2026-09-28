from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle

# Load trained ML readiness model
with open("readiness_model.pkl", "rb") as f:
    readiness_model = pickle.load(f)

from .logic import (
    get_connection,
    load_students,
    get_next_student_id,
    recommend_career,
    calculate_skill_gap,
    calculate_resume_score,
    calculate_readiness,
    find_courses,
    find_internships,
    get_interview_questions,
    evaluate_interview_answer,
    clean_records
)


# FASTAPI APP
app = FastAPI(
    title="Mera Future API",
    description="AI-Powered Career Readiness & Employability Platform",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PYDANTIC MODELS
class StudentCreate(BaseModel):
    name: str
    dob: Optional[str] = ""
    stream: Optional[str] = ""
    semester: Optional[int] = 0

    cgpa: float = 0

    technical_score: float = 0
    aptitude_score: float = 0
    problem_solving_score: float = 0
    communication_score: float = 0

    known_skills: Optional[str] = ""
    certification: Optional[str] = ""

    projects_completed: int = 0
    internship_months: int = 0
    github_projects: int = 0

    coding_level: Optional[str] = ""
    preferred_domain: Optional[str] = ""
    career_goal: Optional[str] = ""
    soft_skills: Optional[str] = ""


class InterviewAnswer(BaseModel):
    career: str
    question_index: int
    answer: str


# CURRENT STUDENT
def get_current_student(student_id=None):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        if student_id is None:
            cursor.execute(
                """
                SELECT *
                FROM students
                ORDER BY student_id DESC
                LIMIT 1
                """
            )
        else:
            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE student_id = ?
                """,
                (student_id,)
            )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        columns = [
            description[0]
            for description in cursor.description
        ]

        student = dict(zip(columns, row))

        return student

    finally:
        conn.close()


# HOME
@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Mera Future API is running"
    }


# GET ALL STUDENTS
# IMPORTANT FOR STUDENT DROPDOWN
@app.get("/students")
def get_all_students():

    df = load_students()

    return {
        "status": "success",
        "students": clean_records(df)
    }


# GET SELECTED STUDENT
@app.get("/student")
def get_student(student_id: Optional[int] = None):

    return get_current_student(student_id)


# REGISTER STUDENT
@app.post("/register")
def register_student(student: StudentCreate):

    conn = get_connection()

    try:

        student_id = get_next_student_id()

        student_data = student.model_dump()

        # TEMP STUDENT FOR CALCULATIONS
        temp_student = {
            "student_id": student_id,
            "academic_year": "",
            "name": student_data["name"],
            "dob": student_data["dob"],
            "stream": student_data["stream"],
            "semester": student_data["semester"],
            "cgpa": student_data["cgpa"],
            "known_skills": student_data["known_skills"],
            "certification": student_data["certification"],
            "projects_completed": student_data["projects_completed"],
            "internship_months": student_data["internship_months"],
            "communication_score": student_data["communication_score"],
            "technical_score": student_data["technical_score"],
            "aptitude_score": student_data["aptitude_score"],
            "problem_solving_score": student_data["problem_solving_score"],
            "github_projects": student_data["github_projects"],
            "coding_level": student_data["coding_level"],
            "preferred_domain": student_data["preferred_domain"],
            "career_goal": student_data["career_goal"],
            "soft_skills": student_data["soft_skills"]
        }

        # CALCULATIONS
        career, _ = recommend_career(temp_student)

        skill_gap = calculate_skill_gap(
            temp_student,
            career
        )

        resume_score, _ = calculate_resume_score(
            temp_student
        )

        readiness_score = calculate_readiness(
            temp_student
        )

        # INSERT
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO students (
                student_id,
                academic_year,
                name,
                dob,
                stream,
                semester,
                cgpa,
                known_skills,
                certification,
                projects_completed,
                internship_months,
                communication_score,
                technical_score,
                aptitude_score,
                problem_solving_score,
                resume_score,
                github_projects,
                coding_level,
                preferred_domain,
                career_goal,
                soft_skills,
                readiness_score,
                skill_gap,
                employment_status
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?
            )
            """,
            (
                student_id,
                "",
                student_data["name"],
                student_data["dob"],
                student_data["stream"],
                student_data["semester"],
                student_data["cgpa"],
                student_data["known_skills"],
                student_data["certification"],
                student_data["projects_completed"],
                student_data["internship_months"],
                student_data["communication_score"],
                student_data["technical_score"],
                student_data["aptitude_score"],
                student_data["problem_solving_score"],
                resume_score,
                student_data["github_projects"],
                student_data["coding_level"],
                student_data["preferred_domain"],
                student_data["career_goal"],
                student_data["soft_skills"],
                readiness_score,
                ", ".join(skill_gap),
                "Student"
            )
        )

        conn.commit()

        return {
            "status": "success",
            "message": "Student registered successfully",
            "student_id": student_id,
            "career": career,
            "skill_gap": skill_gap,
            "resume_score": resume_score,
            "readiness_score": readiness_score
        }

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        conn.close()


# CAREER
@app.get("/career")
def get_career(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    career, scores = recommend_career(student)

    return {
        "status": "success",
        "career": career,
        "scores": scores
    }


# SKILL GAP
@app.get("/skills")
def get_skills(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    career, _ = recommend_career(student)

    skill_gap = calculate_skill_gap(
        student,
        career
    )

    known_skills = student.get(
        "known_skills",
        ""
    )

    if not known_skills:
        current_skills = []
    else:
        current_skills = [
            skill.strip()
            for skill in str(known_skills).split(",")
            if skill.strip()
        ]

    return {
        "status": "success",
        "career": career,
        "current_skills": current_skills,
        "missing_skills": skill_gap
    }


# COURSES
@app.get("/courses")
def get_courses(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    career, _ = recommend_career(student)

    try:
        courses_df = __import__("pandas").read_csv(
            "student_online_courses.csv"
        )

        courses = find_courses(
            courses_df,
            student,
            career
        )

        return {
            "status": "success",
            "career": career,
            "courses": clean_records(courses)
        }

    except FileNotFoundError:

        return {
            "status": "success",
            "career": career,
            "courses": []
        }


# INTERNSHIPS
@app.get("/internships")
def get_internships(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    career, _ = recommend_career(student)

    try:
        internships_df = __import__("pandas").read_csv(
            "student_internships.csv"
        )

        internships = find_internships(
            internships_df,
            student,
            career
        )

        return {
            "status": "success",
            "career": career,
            "internships": clean_records(internships)
        }

    except FileNotFoundError:

        return {
            "status": "success",
            "career": career,
            "internships": []
        }


# RESUME
@app.get("/resume")
def get_resume(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    resume_score, suggestions = calculate_resume_score(
        student
    )

    return {
        "status": "success",
        "resume_score": resume_score,
        "suggestions": suggestions
    }


# READINESS
@app.get("/readiness")
def get_readiness(student_id: Optional[int] = None):

    student = get_current_student(student_id)

    # Existing readiness score
    readiness_score = calculate_readiness(student)

    # Scikit-learn ML prediction
    ml_prediction = readiness_model.predict([[
        float(student.get("cgpa", 0)),
        float(student.get("technical_score", 0)),
        float(student.get("projects_completed", 0)),
        float(student.get("github_projects", 0)),
        float(student.get("internship_months", 0))
    ]])[0]

    # Keep prediction between 0 and 100
    ml_prediction = round(
        max(0, min(100, ml_prediction)), 1
    )

    return {
        "status": "success",

        # Existing score
        "readiness_score": readiness_score,

        # New Scikit-learn prediction
        "ml_readiness_prediction": ml_prediction,

        "technical_score": student.get(
            "technical_score", 0
        ),
        "aptitude_score": student.get(
            "aptitude_score", 0
        ),
        "problem_solving_score": student.get(
            "problem_solving_score", 0
        ),
        "communication_score": student.get(
            "communication_score", 0
        ),
        "projects_completed": student.get(
            "projects_completed", 0
        ),
        "internship_months": student.get(
            "internship_months", 0
        ),
        "github_projects": student.get(
            "github_projects", 0
        )
    }


# MOCK INTERVIEW
@app.get("/interview")
def get_interview(
    student_id: Optional[int] = None
):

    student = get_current_student(student_id)

    career, _ = recommend_career(student)

    questions = get_interview_questions(
        career
    )

    return {
        "status": "success",
        "career": career,
        "questions": questions
    }


# EVALUATE INTERVIEW ANSWER
@app.post("/interview/evaluate")
def evaluate_answer(
    answer: InterviewAnswer
):

    result = evaluate_interview_answer(
        answer.career,
        answer.question_index,
        answer.answer
    )

    return {
        "status": "success",
        "result": result
    }