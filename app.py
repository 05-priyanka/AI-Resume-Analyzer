import streamlit as st

from resume_parser import extract_text_from_pdf

from utils import (
    extract_skills,
    calculate_resume_score,
    match_job_description,
    generate_resume_feedback,
    generate_job_suggestions
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #9aa0a6;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .score-box {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(
            135deg,
            #123d2b,
            #176b48
        );
        text-align: center;
        margin: 15px 0 25px 0;
    }

    .score-number {
        font-size: 48px;
        font-weight: 700;
        color: white;
    }

    .score-label {
        font-size: 16px;
        color: #d8f3e5;
    }

    .skill-box {
        padding: 10px 15px;
        border-radius: 10px;
        background-color: #1f2937;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume, identify strengths, find improvements '
    'and check your match with a job description.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# NAME
# --------------------------------------------------

name = st.text_input(
    "Enter your name:",
    placeholder="Enter your name"
)


if name.strip():

    st.success(f"Welcome, {name}! 👋")

    choice = st.radio(
        "Do you want to analyze your resume?",
        ["Yes", "No"],
        horizontal=True
    )


    # --------------------------------------------------
    # NO
    # --------------------------------------------------

    if choice == "No":

        st.info(
            "No problem! You can analyze your resume "
            "whenever you are ready."
        )


    # --------------------------------------------------
    # YES
    # --------------------------------------------------

    else:

        st.success(
            "Great! Let's analyze your resume. 🚀"
        )

        uploaded_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            help="Upload your resume in PDF format."
        )


        if uploaded_file is not None:

            # ------------------------------------------
            # EXTRACT TEXT
            # ------------------------------------------

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            st.success(
                "Resume uploaded successfully! 🎉"
            )


            # ------------------------------------------
            # RESUME SCORE
            # ------------------------------------------

            score, section_scores = (
                calculate_resume_score(
                    resume_text
                )
            )


            st.markdown(
                '<div class="section-title">'
                '📊 Resume Score'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="score-box">
                    <div class="score-label">
                        Overall Resume Score
                    </div>
                    <div class="score-number">
                        {score}/100
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(score / 100)


            # ------------------------------------------
            # RESUME SECTIONS
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '📋 Resume Sections'
                '</div>',
                unsafe_allow_html=True
            )

            section_columns = st.columns(2)

            for index, (section, found) in enumerate(
                section_scores.items()
            ):

                with section_columns[index % 2]:

                    if section == "Experience" and not found:

                        st.info(
                            "ℹ️ Experience "
                            "(Optional for students)"
                        )

                    elif found:

                        st.success(
                            f"✅ {section}"
                        )

                    else:

                        st.error(
                            f"❌ {section}"
                        )


            # ------------------------------------------
            # SKILLS
            # ------------------------------------------

            skills = extract_skills(
                resume_text
            )

            st.markdown(
                '<div class="section-title">'
                '🛠️ Skills Detected'
                '</div>',
                unsafe_allow_html=True
            )

            if skills:

                st.markdown(
                    f"""
                    <div class="skill-box">
                        {" • ".join(skills)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "No technical skills detected."
                )


            # ------------------------------------------
            # FEEDBACK
            # ------------------------------------------

            strengths, improvements, recommendations = (
                generate_resume_feedback(
                    resume_text,
                    section_scores,
                    skills
                )
            )


            # ------------------------------------------
            # STRENGTHS
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '💪 Resume Strengths'
                '</div>',
                unsafe_allow_html=True
            )

            if strengths:

                for strength in strengths:

                    st.success(
                        f"✓ {strength}"
                    )

            else:

                st.info(
                    "No specific strengths detected."
                )


            # ------------------------------------------
            # IMPROVEMENTS
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '🔧 Areas to Improve'
                '</div>',
                unsafe_allow_html=True
            )

            if improvements:

                for improvement in improvements:

                    st.warning(
                        f"⚠️ {improvement}"
                    )

            else:

                st.success(
                    "Your resume has good coverage "
                    "of the major sections!"
                )


            # ------------------------------------------
            # RECOMMENDATIONS
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '💡 Recommendations'
                '</div>',
                unsafe_allow_html=True
            )

            if recommendations:

                for recommendation in recommendations:

                    st.info(
                        f"💡 {recommendation}"
                    )

            else:

                st.success(
                    "No major recommendations "
                    "at this time."
                )


            # ------------------------------------------
            # JOB DESCRIPTION
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '💼 Job Description Matching'
                '</div>',
                unsafe_allow_html=True
            )

            st.write(
                "Paste a job description below to see "
                "how well your resume matches the role."
            )

            job_description = st.text_area(
                "Paste the job description here:",
                height=220,
                placeholder=(
                    "Example:\n"
                    "Python programming knowledge...\n"
                    "SQL and databases...\n"
                    "Data Structures and Algorithms..."
                )
            )


            # ------------------------------------------
            # DEFAULT JOB RESULTS
            # ------------------------------------------

            match_score = None
            matched_skills = []
            missing_skills = []
            suggestions = []


            # ------------------------------------------
            # JOB MATCHING
            # ------------------------------------------

            if job_description.strip():

                (
                    match_score,
                    matched_skills,
                    missing_skills
                ) = match_job_description(
                    resume_text,
                    job_description
                )


                st.markdown(
                    '<div class="section-title">'
                    '🎯 Job Match Score'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.metric(
                    "Match Score",
                    f"{match_score}%"
                )

                st.progress(
                    match_score / 100
                )


                # --------------------------------------
                # MATCHING SKILLS
                # --------------------------------------

                st.markdown(
                    "### ✅ Matching Skills"
                )

                if matched_skills:

                    st.success(
                        ", ".join(matched_skills)
                    )

                else:

                    st.info(
                        "No matching skills detected."
                    )


                # --------------------------------------
                # MISSING SKILLS
                # --------------------------------------

                st.markdown(
                    "### ❌ Missing Skills"
                )

                if missing_skills:

                    st.warning(
                        ", ".join(missing_skills)
                    )

                else:

                    st.success(
                        "No major missing skills detected!"
                    )


                # --------------------------------------
                # JOB SUGGESTIONS
                # --------------------------------------

                st.markdown(
                    "### 🎯 Job-Specific Suggestions"
                )

                if missing_skills:

                    suggestions = (
                        generate_job_suggestions(
                            missing_skills
                        )
                    )

                    for suggestion in suggestions:

                        st.warning(
                            suggestion
                        )

                else:

                    st.success(
                        "Your resume matches the "
                        "required skills well!"
                    )


            # ------------------------------------------
            # EXTRACTED TEXT
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '📄 Extracted Resume Text'
                '</div>',
                unsafe_allow_html=True
            )

            with st.expander(
                "View extracted resume content"
            ):

                st.text_area(
                    "Resume content:",
                    resume_text,
                    height=500
                )


            # ------------------------------------------
            # DOWNLOAD REPORT
            # ------------------------------------------

            report = f"""
AI RESUME ANALYZER
==================

Candidate Name:
{name}

RESUME SCORE
------------
Overall Score: {score}/100


RESUME SECTIONS
---------------

"""

            for section, found in section_scores.items():

                if section == "Experience" and not found:

                    report += (
                        f"{section}: "
                        "Optional for students\n"
                    )

                elif found:

                    report += (
                        f"{section}: Present\n"
                    )

                else:

                    report += (
                        f"{section}: Missing\n"
                    )


            report += """

SKILLS DETECTED
---------------

"""

            if skills:

                report += ", ".join(skills)

            else:

                report += "No technical skills detected."


            report += """



RESUME STRENGTHS
----------------

"""

            if strengths:

                for strength in strengths:

                    report += (
                        f"- {strength}\n"
                    )

            else:

                report += (
                    "No specific strengths detected.\n"
                )


            report += """

AREAS TO IMPROVE
----------------

"""

            if improvements:

                for improvement in improvements:

                    report += (
                        f"- {improvement}\n"
                    )

            else:

                report += (
                    "No major improvements identified.\n"
                )


            report += """

RECOMMENDATIONS
---------------

"""

            if recommendations:

                for recommendation in recommendations:

                    report += (
                        f"- {recommendation}\n"
                    )

            else:

                report += (
                    "No major recommendations.\n"
                )


            # ------------------------------------------
            # JOB MATCH REPORT
            # ------------------------------------------

            if job_description.strip():

                report += f"""

JOB DESCRIPTION MATCHING
------------------------

Job Match Score: {match_score}%


MATCHING SKILLS
---------------

"""

                if matched_skills:

                    report += (
                        ", ".join(matched_skills)
                    )

                else:

                    report += (
                        "No matching skills detected."
                    )


                report += """



MISSING SKILLS
--------------

"""

                if missing_skills:

                    report += (
                        ", ".join(missing_skills)
                    )

                else:

                    report += (
                        "No major missing skills."
                    )


                report += """



JOB-SPECIFIC SUGGESTIONS
------------------------

"""

                if suggestions:

                    for suggestion in suggestions:

                        report += (
                            f"- {suggestion}\n"
                        )

                else:

                    report += (
                        "No additional suggestions.\n"
                    )


            report += """



EXTRACTED RESUME TEXT
---------------------

"""

            report += resume_text


            # ------------------------------------------
            # DOWNLOAD BUTTON
            # ------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '📥 Download Analysis Report'
                '</div>',
                unsafe_allow_html=True
            )

            st.write(
                "Save your complete resume analysis "
                "as a text report."
            )

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )


else:

    st.info(
        "Please enter your name to continue."
    )