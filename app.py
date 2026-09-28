import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Mera Future",
    page_icon="",
    layout="wide")

# 2. LOAD DATASET.
df = pd.read_csv("student.csv")
courses_df = pd.read_csv("student_online_courses.csv")
courses_df.columns = (
    courses_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
interships_df = pd.read_csv("student_internships.csv")

# 3. TITLE
st.title("🎓 Mera Future")

st.write(
    "AI-based student profile analysis and career path recommendation system")

# 4. STUDENT SELECTION
st.sidebar.header("👤 Student Selection")
student_name = st.sidebar.selectbox("Select Student",df["name"].dropna().unique())
student = df[df["name"] == student_name].iloc[0]


# STUDENT PROFILE
st.header("📋 Student Profile")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Student ID", student["student_id"])

with col2:
    st.metric("Academic Year", student["academic_year"])

with col3:
    st.metric("Semester", student["semester"])

with col4:
    st.metric("CGPA", student["cgpa"])


# ACADEMIC & PERSONAL INFORMATION
st.subheader("🎓 Academic Information")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Name:**", student["name"])
    st.write("**Date of Birth:**", student["dob"])

with col2:
    st.write("**Stream:**", student["stream"])
    st.write("**CGPA:**", student["cgpa"])

with col3:
    st.write("**Career Goal:**", student["career_goal"])
    st.write("**Preferred Domain:**", student["preferred_domain"])


# SKILLS
st.subheader("💻 Skills & Experience")
col1, col2 = st.columns(2)

with col1:
    st.write("**Known Skills:**")
    st.info(str(student["known_skills"]))

    st.write("**Coding Level:**")
    st.info(str(student["coding_level"]))

    st.write("**Soft Skills:**")
    st.info(str(student["soft_skills"]))

with col2:
    st.write("**Certifications:**")
    st.info(str(student["certification"]))

    st.write("**Projects Completed:**")
    st.info(str(student["projects_completed"]))

    st.write("**Internship:**")
    st.info(f"{student['internship_months']} months")


# PERFORMANCE SCORES
st.subheader("📊 Student Performance")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Communication",student["communication_score"])

with col2:
    st.metric( "Technical",student["technical_score"])

with col3:
    st.metric("Aptitude",student["aptitude_score"])

with col4:
    st.metric("Problem Solving",student["problem_solving_score"])

with col5:
    st.metric("Resume",student["resume_score"])


# CAREER RECOMMENDATION FUNCTION
def recommend_career(student):

    scores = {
        "AI / ML Engineer": 0,
        "Data Analyst": 0,
        "Web Developer": 0,
        "Software Developer": 0,
        "Cybersecurity Analyst": 0,
        "Cloud Engineer": 0
        }

    skills = str(student["known_skills"]).lower()
    domain = str(student["preferred_domain"]).lower()
    goal = str(student["career_goal"]).lower()
    coding = str(student["coding_level"]).lower()

    technical = float(student["technical_score"])
    aptitude = float(student["aptitude_score"])
    problem_solving = float(student["problem_solving_score"])
    communication = float(student["communication_score"])

    # AI / ML
    if any(word in skills for word in [
        "python", "machine learning", "ml",
        "numpy", "pandas", "tensorflow",
        "pytorch", "artificial intelligence", "ai"]):
        scores["AI / ML Engineer"] += 30

    if "ai" in domain or "machine learning" in domain:
        scores["AI / ML Engineer"] += 30

    if "ai" in goal or "machine learning" in goal:
        scores["AI / ML Engineer"] += 30

    scores["AI / ML Engineer"] += (
        technical * 0.05 +
        aptitude * 0.05 +
        problem_solving * 0.05)


    # DATA ANALYST
    if any(word in skills for word in [
        "python", "sql", "pandas","excel", "statistics", "data analysis"]):
        scores["Data Analyst"] += 30

    if "data" in domain:
        scores["Data Analyst"] += 30

    if "data" in goal:
        scores["Data Analyst"] += 30

    scores["Data Analyst"] += (
        aptitude * 0.08 +
        technical * 0.04)


    # WEB DEVELOPER
    if any(word in skills for word in [
        "html", "css", "javascript","react", "node", "web", "php"]):
        scores["Web Developer"] += 40

    if "web" in domain:
        scores["Web Developer"] += 30

    if "web" in goal:
        scores["Web Developer"] += 30

    scores["Web Developer"] += technical * 0.05


    # SOFTWARE DEVELOPER
    if any(word in skills for word in [
        "java", "c++", "c#", "python",".net", "software development"]):
        scores["Software Developer"] += 30

    if "software" in domain:
        scores["Software Developer"] += 30

    if "software" in goal:
        scores["Software Developer"] += 30

    scores["Software Developer"] += (
        technical * 0.05 +
        problem_solving * 0.05 )


    # CYBERSECURITY
    if any(word in skills for word in ["cybersecurity", "cyber security","networking", "ethical hacking","security", "linux"]):
        scores["Cybersecurity Analyst"] += 40

    if "cyber" in domain or "security" in domain:
        scores["Cybersecurity Analyst"] += 30

    if "cyber" in goal or "security" in goal:
        scores["Cybersecurity Analyst"] += 30

    scores["Cybersecurity Analyst"] += (
        technical * 0.05 +
        problem_solving * 0.05 )


    # CLOUD
    if any(word in skills for word in [
        "aws", "azure", "cloud", "docker", "devops" ]):
        scores["Cloud Engineer"] += 40

    if "cloud" in domain or "devops" in domain:
        scores["Cloud Engineer"] += 30

    if "cloud" in goal or "devops" in goal:
        scores["Cloud Engineer"] += 30

    scores["Cloud Engineer"] += technical * 0.05


    # CODING LEVEL BONUS
    if "advanced" in coding:
        for career in scores:
            scores[career] += 5

    elif "intermediate" in coding:
        for career in scores:
            scores[career] += 3


    # COMMUNICATION BONUS
    if communication >= 80:
        scores["Data Analyst"] += 3
        scores["Web Developer"] += 3
        scores["Software Developer"] += 3


    # Highest score
    recommended_career = max(
        scores,
        key=scores.get )

    return recommended_career, scores


# CAREER RECOMMENDATION
st.header("🤖 AI Career Recommendation")
career, career_scores = recommend_career(student)
st.success(f"Recommended Career Path: {career}")

# SKILL GAP ANALYSIS
st.header("⚠️ Skill Gap Analysis")

# Student ke current skills
known_skills = str(student["known_skills"])

# Student ke missing skills
skill_gap = str(student["skill_gap"])

st.subheader("💻 Current Skills")

for skill in known_skills.split(";"):
    skill = skill.strip()

    if skill:
        st.success("✓ " + skill)


st.subheader("📚 Skills to Improve")

if skill_gap.lower() != "nan" and skill_gap.strip():

    missing_skills = skill_gap.split(";")

    for skill in missing_skills:
        skill = skill.strip()

        if skill:
            st.warning("⚠️ " + skill)

else:
    st.info("No skill gap information available.")

# CAREER MATCH SCORES
st.subheader("📈 Career Match Analysis")
career_df = pd.DataFrame(
    {
        "Career": list(career_scores.keys()),
        "Match Score": list(career_scores.values())
    }
)

career_df = career_df.sort_values(
    by="Match Score",ascending=False)

st.dataframe(
    career_df,
    use_container_width=True,
    hide_index=True)

# ONLINE COURSE RECOMMENDATION
st.header("🎓 Recommended Online Courses & Certifications")

student_career = str(student["career_goal"]).lower()
student_domain = str(student["preferred_domain"]).lower()
student_skills = str(student["known_skills"]).lower()

recommended_courses = courses_df[
    courses_df["career_path"].astype(str).str.lower().apply(
        lambda x: student_career in x or student_domain in x)]

if len(recommended_courses) > 0:

    st.write("Courses matching your career goal/domain:")

    st.dataframe(
        recommended_courses[
            ["course_name","provider", "skill","level","duration_hours","certificate_available", "course_url"
            ]
        ].head(5),
        use_container_width=True,
        hide_index=True )

else:
    st.info("No matching courses found.")

# INTERNSHIP MATCHING
st.header("💼 Recommended Internship Opportunities")
student_career = str(student["career_goal"]).lower()
student_domain = str(student["preferred_domain"]).lower()
student_skills = str(student["known_skills"]).lower()

# Career path ke according internships filter
recommended_internships = interships_df[
    interships_df["career_path"].astype(str).str.lower().apply(
        lambda x: student_career in x or student_domain in x)]

# Student ke CGPA ke according eligible internships
recommended_internships = recommended_internships[
    pd.to_numeric(
        recommended_internships["eligibility_cgpa"],
        errors="coerce"
    ).fillna(0) <= float(student["cgpa"])]

if len(recommended_internships) > 0:
    st.write("Internships matching your career and eligibility:")

    st.dataframe(
        recommended_internships[
            [ "company","internship_role","career_path","duration_months","stipend_inr","work_mode","eligibility_cgpa","location", "application_url"
            ]
        ].head(5),
        use_container_width=True,
        hide_index=True)

else:
    st.info("No matching internship opportunities found.")

# READINESS SCORE
st.subheader("🚀 Career Readiness")
readiness = float(student["readiness_score"])
st.metric(
    "Career Readiness Score",
    f"{readiness}%")

st.progress(
    min(max(readiness / 100, 0), 1))

# EMPLOYMENT STATUS
st.subheader("💼 Employment Status")
st.write(
    student["employment_status"])