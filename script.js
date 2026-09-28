// MERA FUTURE - FINAL FRONTEND JAVASCRIPT

const API_BASE_URL = "http://127.0.0.1:8000";

let selectedStudentId = null;


//    HELPER FUNCTIONS

function setText(selector, value) {

    document.querySelectorAll(selector).forEach(element => {

        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            element.innerText = "-";
        } else {
            element.innerText = value;
        }

    });

}


function safeNumber(value, fallback = 0) {

    const number = Number(value);

    return Number.isFinite(number)
        ? number
        : fallback;

}


function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


function studentURL(endpoint) {

    if (!selectedStudentId) {
        return `${API_BASE_URL}/${endpoint}`;
    }

    return `${API_BASE_URL}/${endpoint}?student_id=${encodeURIComponent(selectedStudentId)}`;

}


function updateProgress(selector, value) {

    const element =
        document.querySelector(selector);

    if (!element) {
        return;
    }

    const percentage =
        Math.min(
            Math.max(
                safeNumber(value),
                0
            ),
            100
        );

    element.style.width =
        `${percentage}%`;

}


//    STUDENT SELECTOR

function setupStudentSelector() {

    const selector =
        document.getElementById("student-selector");

    if (!selector) {

        console.error(
            "Student selector not found!"
        );

        return;

    }


    selector.addEventListener(
        "change",
        async function () {

            selectedStudentId =
                this.value;

            if (!selectedStudentId) {
                return;
            }

            console.log(
                "Selected Student ID:",
                selectedStudentId
            );

            await loadAllStudentData();

        }
    );

}


//    SECTION NAVIGATION

function showSection(
    sectionId,
    clickedButton = null
) {

    document
        .querySelectorAll(".content-section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


    const targetSection =
        document.getElementById(sectionId);

    if (targetSection) {

        targetSection.classList.add(
            "active-section"
        );

    }


    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove(
                "active"
            );

        });


    if (clickedButton) {

        clickedButton.classList.add(
            "active"
        );

    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


//    LOAD STUDENT LIST

async function loadStudentList() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/students`
            );


        if (!response.ok) {

            throw new Error(
                "Student List API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Student List:",
            data
        );


        const selector =
            document.getElementById(
                "student-selector"
            );


        if (!selector) {

            console.error(
                "Student selector not found!"
            );

            return;

        }


        selector.innerHTML =
            '<option value="">Select Student</option>';


        const students =
            Array.isArray(data.students)
                ? data.students
                : [];


        students.forEach(student => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                student.student_id;


            option.textContent =
                student.name;


            selector.appendChild(
                option
            );

        });


        console.log(
            "Students loaded:",
            students.length
        );


        /*
         * Automatically select first student
         * so dashboard is not empty.
         */

        if (students.length > 0 && !
        selectedStudentId) {
            selectedStudentId =
                students[0].student_id;

    selector.value =
        selectedStudentId;

    console.log(
        "Auto selected Student ID:",
        selectedStudentId
    );
}


    } catch (error) {

        console.error(
            "Student List API Error:",
            error
        );

    }

}


//    LOAD ALL DATA FOR SELECTED STUDENT

async function loadAllStudentData() {

    if (!selectedStudentId) {

        console.warn(
            "No student selected"
        );

        return;

    }


    console.log(
        "Loading complete dashboard for student:",
        selectedStudentId
    );


    /*
     * Run all APIs for SAME selected student.
     */

    await loadStudentData();
    await loadCareerData();
    await loadSkillsData();
    await loadCoursesData();
    await loadInternshipsData();
    await loadResumeData();
    await loadReadinessData();
    await loadInterviewQuestion();


    console.log(
        "Complete dashboard loaded for student:",
        selectedStudentId
    );

}


//    LOAD SELECTED STUDENT PROFILE

async function loadStudentData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("student")
            );


        if (!response.ok) {

            throw new Error(
                "Student API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Student Data:",
            data
        );


        if (!data || !data.name){
            return;
        }


        //    BASIC PROFILE

        setText(
            ".profile-name",
            data.name
        );
        console.log("Name Set To:",data.name);


        setText(
            ".profile-stream",
            data.stream
        );


        setText(
            ".profile-degree",
            data.stream
                ? data.stream.toUpperCase()
                : "BCA"
        );


        setText(
            ".semester-value",
            data.semester
        );


        setText(
            ".cgpa-value",
            safeNumber(
                data.cgpa
            ).toFixed(1)
        );


        const projects =
            safeNumber(
                data.projects_completed ??
                data.projects
            );


        setText(
            ".projects-value",
            projects
        );


        const internshipMonths =
            safeNumber(
                data.internship_months
            );


        setText(
            ".internship-value",
            `${internshipMonths} months`
        );


        //    CAREER / PERSONAL DATA

        setText(
            ".career-goal",
            data.career_goal
        );


        setText(
            ".preferred-domain",
            data.preferred_domain
        );


        setText(
            ".coding-level",
            data.coding_level
        );


        //    SCORES

        const technical =
            safeNumber(
                data.technical_score
            );


        const resume =
            safeNumber(
                data.resume_score
            );


        const readiness =
            safeNumber(
                data.readiness_score ??
                data.readiness
            );


        setText(
            ".technical-value",
            `${technical}%`
        );


        setText(
            ".resume-value",
            resume.toFixed(1)
        );


        setText(
            ".readiness-score",
            `${readiness}%`
        );


        //    PROGRESS BARS

        updateProgress(
            ".technical-progress",
            technical
        );


        updateProgress(
            ".resume-progress",
            resume
        );


        updateProgress(
            ".projects-progress",
            projects * 10
        );


        updateProgress(
            ".internship-progress",
            internshipMonths * 10
        );


        //    CURRENT SKILLS

        updateCurrentSkills(
            data.known_skills ??
            data.skills
        );


    } catch (error) {

        console.error(
            "Student API Error:",
            error
        );

    }

}


//    CAREER RECOMMENDATION

async function loadCareerData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("career")
            );


        if (!response.ok) {

            throw new Error(
                "Career API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Career Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const career =
            data.career ||
            data.recommended_career ||
            "-";


        setText(
            ".recommended-career",
            career
        );


        setText(
            ".profile-career",
            career
        );


        /*
         * Preferred domain and career goal
         * come from student profile.
         */

        if (data.preferred_domain !== undefined) {

            setText(
                ".preferred-domain",
                data.preferred_domain
            );

        }


        if (data.career_goal !== undefined) {

            setText(
                ".career-goal",
                data.career_goal
            );

        }


    } catch (error) {

        console.error(
            "Career API Error:",
            error
        );

    }

}


//    SKILLS / SKILL GAP

async function loadSkillsData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("skills")
            );


        if (!response.ok) {

            throw new Error(
                "Skills API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Skills Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const currentSkills =
            Array.isArray(
                data.current_skills
            )
                ? data.current_skills
                : [];


        const missingSkills =
            Array.isArray(
                data.missing_skills
            )
                ? data.missing_skills
                : [];


        /*
         * Backend currently sends:
         * current_skills
         * missing_skills
         *
         * If required_skills is unavailable,
         * combine current + missing.
         */

        let requiredSkills =
            Array.isArray(
                data.required_skills
            )
                ? data.required_skills
                : [];


        if (
            requiredSkills.length === 0
        ) {

            requiredSkills = [
                ...currentSkills,
                ...missingSkills
            ];

        }


        setText(
            ".current-skills-count",
            currentSkills.length
        );


        setText(
            ".missing-skills-count",
            missingSkills.length
        );


        const skillsList =
            document.getElementById(
                "skills-list"
            );


        if (!skillsList) {
            return;
        }


        if (
            requiredSkills.length === 0
        ) {

            skillsList.innerHTML = `
                <div class="skill-item">
                    <div class="skill-name">
                        No skill information available
                    </div>
                </div>
            `;

            return;

        }


        skillsList.innerHTML =
            requiredSkills
                .map(skill => {

                    const skillName =
                        String(skill);


                    const isMissing =
                        missingSkills.some(
                            missing =>
                                String(missing)
                                    .toLowerCase()
                                    .trim() ===
                                skillName
                                    .toLowerCase()
                                    .trim()
                        );


                    return `
                        <div class="skill-item">

                            <div class="skill-name">
                                ${escapeHTML(skillName)}
                            </div>

                            <div class="skill-status ${
                                isMissing
                                    ? "learning"
                                    : "available"
                            }">

                                ${
                                    isMissing
                                        ? "Required"
                                        : "Available"
                                }

                            </div>

                        </div>
                    `;

                })
                .join("");


    } catch (error) {

        console.error(
            "Skills API Error:",
            error
        );

    }

}


//    COURSES

async function loadCoursesData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("courses")
            );


        if (!response.ok) {

            throw new Error(
                "Courses API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Courses Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const courses =
            Array.isArray(
                data.courses
            )
                ? data.courses
                : [];


        const coursesList =
            document.getElementById(
                "courses-list"
            );


        if (!coursesList) {
            return;
        }


        if (courses.length === 0) {

            coursesList.innerHTML = `
                <div class="course-card">

                    <div class="course-icon">
                        📚
                    </div>

                    <h3>
                        No matching courses
                    </h3>

                    <p>
                        No course recommendations
                        are currently available.
                    </p>

                </div>
            `;

            return;

        }


        coursesList.innerHTML =
            courses
                .map(course => {

                    const title =
                        course.course_name ||
                        course.name ||
                        "Recommended Course";


                    const description =
                        course.description ||
                        course.course_description ||
                        "Recommended course for your career profile.";


                    const platform =
                        course.platform ||
                        course.provider ||
                        "Online Course";


                    return `
                        <div class="course-card">

                            <div class="course-icon">
                                📚
                            </div>

                            <span class="course-type">
                                ${escapeHTML(platform)}
                            </span>

                            <h3>
                                ${escapeHTML(title)}
                            </h3>

                            <p>
                                ${escapeHTML(description)}
                            </p>

                            <button
                                class="secondary-btn"
                                onclick="showCourseMessage()">

                                View Course

                            </button>

                        </div>
                    `;

                })
                .join("");


    } catch (error) {

        console.error(
            "Courses API Error:",
            error
        );

    }

}


//    INTERNSHIPS

async function loadInternshipsData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("internships")
            );


        if (!response.ok) {

            throw new Error(
                "Internships API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Internships Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const internships =
            Array.isArray(
                data.internships
            )
                ? data.internships
                : [];


        const internshipsList =
            document.getElementById(
                "internships-list"
            );


        if (!internshipsList) {
            return;
        }


        if (internships.length === 0) {

            internshipsList.innerHTML = `
                <div class="internship-card">

                    <div class="company-icon">
                        💼
                    </div>

                    <h3>
                        No matching internships
                    </h3>

                    <p>
                        No eligible internship
                        opportunities are currently available.
                    </p>

                </div>
            `;

            return;

        }


        internshipsList.innerHTML =
            internships
                .map(internship => {

                    const title =
                        internship.internship_name ||
                        internship.name ||
                        internship.title ||
                        "Internship Opportunity";


                    const description =
                        internship.description ||
                        internship.internship_description ||
                        "Internship opportunity matched with your profile.";


                    const company =
                        internship.company ||
                        internship.organization ||
                        "Company";


                    return `
                        <div class="internship-card">

                            <div class="internship-top">

                                <div class="company-icon">
                                    🏢
                                </div>

                                <span class="internship-badge">
                                    Matched
                                </span>

                            </div>

                            <h3>
                                ${escapeHTML(title)}
                            </h3>

                            <p>
                                ${escapeHTML(description)}
                            </p>

                            <div class="internship-details">

                                <span>
                                    🏢 ${escapeHTML(company)}
                                </span>

                                <span>
                                    🎓 Eligible
                                </span>

                            </div>

                            <button
                                class="secondary-btn"
                                onclick="showInternshipMessage()">

                                View Opportunity

                            </button>

                        </div>
                    `;

                })
                .join("");


    } catch (error) {

        console.error(
            "Internships API Error:",
            error
        );

    }

}


//    RESUME

async function loadResumeData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("resume")
            );


        if (!response.ok) {

            throw new Error(
                "Resume API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Resume Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const score =
            safeNumber(
                data.resume_score
            );


        setText(
            ".resume-value",
            score.toFixed(1)
        );


        updateProgress(
            ".resume-progress",
            score
        );


        const suggestions =
            Array.isArray(
                data.suggestions
            )
                ? data.suggestions
                : [];


        const suggestionsList =
            document.getElementById(
                "resume-suggestions"
            );


        if (!suggestionsList) {
            return;
        }


        if (suggestions.length === 0) {

            suggestionsList.innerHTML = `
                <div class="suggestion">

                    <span>✓</span>

                    <p>
                        Your resume profile looks good.
                    </p>

                </div>
            `;

            return;

        }


        suggestionsList.innerHTML =
            suggestions
                .map(suggestion => {

                    return `
                        <div class="suggestion">

                            <span>✓</span>

                            <p>
                                ${escapeHTML(suggestion)}
                            </p>

                        </div>
                    `;

                })
                .join("");


    } catch (error) {

        console.error(
            "Resume API Error:",
            error
        );

    }

}


//    READINESS

async function loadReadinessData() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("readiness")
            );


        if (!response.ok) {

            throw new Error(
                "Readiness API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Readiness Data:",
            data
        );


        if (data.status !== "success") {
            return;
        }


        const readiness =
            safeNumber(
                data.readiness_score ??
                data.readiness
            );


        setText(
            ".readiness-score",
            `${readiness}%`
        );
        const mlReadiness =
    safeNumber(
        data.ml_readiness_prediction
    );

setText(
    ".ml-readiness-value",
    `${mlReadiness.toFixed(1)}%`
);


        const technical =
            safeNumber(
                data.technical_score
            );


        setText(
            ".technical-value",
            `${technical}%`
        );


        const projects =
            safeNumber(
                data.projects_completed ??
                data.projects
            );


        setText(
            ".projects-value",
            projects
        );


        const internship =
            safeNumber(
                data.internship_months
            );


        setText(
            ".internship-value",
            `${internship} months`
        );


        updateProgress(
            ".technical-progress",
            technical
        );


        updateProgress(
            ".projects-progress",
            projects * 10
        );


        updateProgress(
            ".internship-progress",
            internship * 10
        );


    } catch (error) {

        console.error(
            "Readiness API Error:",
            error
        );

    }

}


//    MOCK INTERVIEW

async function loadInterviewQuestion() {

    if (!selectedStudentId) {
        return;
    }


    try {

        const response =
            await fetch(
                studentURL("interview")
            );


        if (!response.ok) {

            throw new Error(
                "Interview API Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Interview Data:",
            data
        );


        const questionElement =
            document.getElementById(
                "interview-question"
            );


        if (!questionElement) {
            return;
        }


        let question = null;


        /*
         * Backend currently returns:
         *
         * questions: [...]
         *
         * So take first question.
         */

        if (
            Array.isArray(data.questions) &&
            data.questions.length > 0
        ) {

            question =
                data.questions[0];

        }


        if (
            !question &&
            data.question
        ) {

            question =
                data.question;

        }


        questionElement.innerText =
            question ||
            "Tell me about yourself and your technical skills.";


    } catch (error) {

        console.error(
            "Interview API Error:",
            error
        );


        const questionElement =
            document.getElementById(
                "interview-question"
            );


        if (questionElement) {

            questionElement.innerText =
                "Tell me about yourself and your technical skills.";

        }

    }

}


//    SUBMIT INTERVIEW

async function submitInterview() {

    const answerElement =
        document.getElementById(
            "interview-answer"
        );


    const resultElement =
        document.getElementById(
            "interview-result"
        );


    if (
        !answerElement ||
        !resultElement
    ) {

        return;

    }


    const answer =
        answerElement.value.trim();


    if (!answer) {

        resultElement.style.display =
            "block";


        resultElement.style.background =
            "#fef2f2";


        resultElement.style.color =
            "#991b1b";


        resultElement.innerText =
            "Please enter your answer first.";


        return;

    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/interview/evaluate`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        answer: answer,

                        student_id:
                            Number(
                                selectedStudentId
                            )

                    })

                }
            );


        if (!response.ok) {

            throw new Error(
                "Interview Evaluation Error"
            );

        }


        const data =
            await response.json();


        console.log(
            "Interview Evaluation:",
            data
        );


        resultElement.style.display =
            "block";


        resultElement.style.background =
            "#f0fdf4";


        resultElement.style.color =
            "#166534";


        resultElement.innerText =
            data.feedback ||
            data.message ||
            "Answer evaluated successfully.";


    } catch (error) {

        console.error(
            "Interview Evaluation Error:",
            error
        );


        resultElement.style.display =
            "block";


        resultElement.style.background =
            "#fef2f2";


        resultElement.style.color =
            "#991b1b";


        resultElement.innerText =
            "Unable to evaluate answer. Please check the API.";

    }

}


//    CURRENT SKILLS

function updateCurrentSkills(skills) {

    if (
        skills === null ||
        skills === undefined
    ) {

        setText(
            ".current-skills-count",
            0
        );

        return;

    }


    /*
     * If backend sends array.
     */

    if (Array.isArray(skills)) {

        setText(
            ".current-skills-count",
            skills.length
        );

        return;

    }


    /*
     * If backend sends string.
     */

    const skillText =
        String(skills).trim();


    if (
        !skillText ||
        skillText.toLowerCase() === "none"
    ) {

        setText(
            ".current-skills-count",
            0
        );

        return;

    }


    const skillArray =
        skillText
            .split(/[;,]/)
            .map(
                skill => skill.trim()
            )
            .filter(Boolean);


    setText(
        ".current-skills-count",
        skillArray.length
    );

}


//    MESSAGES

function showCourseMessage() {

    alert(
        "Course details will be available soon."
    );

}


function showInternshipMessage() {

    alert(
        "Internship opportunity details will be available soon."
    );

}


//    INITIALIZE

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        console.log(
            "Mera Future frontend started"
        );


        /*
         * 1. Load all students
         */

        await loadStudentList();


        /*
         * 2. Activate dropdown
         */

        setupStudentSelector();


        /*
         * 3. Load first selected student
         */

        if (selectedStudentId) {

            await loadAllStudentData();

        }


        console.log(
            "All frontend data loaded"
        );

    }
);

// ADD STUDENT MODAL

document.addEventListener("DOMContentLoaded", () => {

    const addStudentBtn = document.getElementById("add-student-btn");
    const addStudentModal = document.getElementById("add-student-modal");
    const closeModalBtn = document.getElementById("close-modal-btn");

    if (addStudentBtn && addStudentModal) {

        addStudentBtn.addEventListener("click", () => {
            addStudentModal.style.display = "flex";
        });

    }

    if (closeModalBtn && addStudentModal) {

        closeModalBtn.addEventListener("click", () => {
            addStudentModal.style.display = "none";
        });

    }

});

// REGISTER NEW STUDENT

const addStudentForm = document.getElementById("add-student-form");

if (addStudentForm) {
    addStudentForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const studentData = {
            name: document.getElementById("student-name").value.trim(),
            dob: document.getElementById("student-dob").value,
            stream: document.getElementById("student-stream").value.trim(),
            semester: Number(document.getElementById("student-semester").value),
            cgpa: Number(document.getElementById("student-cgpa").value),

            known_skills: document.getElementById("student-skills").value.trim(),
            certification: document.getElementById("student-certification").value.trim(),

            projects_completed: Number(
                document.getElementById("student-projects").value
            ),

            internship_months: Number(
                document.getElementById("student-internship").value
            ),

            coding_level: document.getElementById("student-coding").value,

            preferred_domain:
                document.getElementById("student-domain").value.trim(),

            career_goal:
                document.getElementById("student-career-goal").value.trim(),

            technical_score:
                Number(document.getElementById("student-technical").value),

            aptitude_score:
                Number(document.getElementById("student-aptitude").value),

            problem_solving_score:
                Number(document.getElementById("student-problem").value),

            communication_score:
                Number(document.getElementById("student-communication").value)
        };

        try {

            const response = await fetch(`${API_BASE_URL}/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(studentData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "Registration failed");
            }

            alert("✅ Student successfully registered!");
            document.getElementById("add-student-modal").style.display="none";



            // Reload student list
            // Reload student list
await loadStudentList();

// Select newly registered student
selectedStudentId = String(result.student_id);

const studentSelector =
    document.getElementById("student-selector");

if (studentSelector) {
    studentSelector.value = selectedStudentId;
}

// Load newly registered student's complete dashboard
await loadAllStudentData();
        } catch (error) {
            console.error("Registration Error:", error);
            alert("❌ Student registration failed: " + error.message);
        }
    });
}