# 📄 AI Resume Analyzer

An interactive web application that analyzes resumes and provides useful feedback to help students and job seekers improve their resumes and check their suitability for a particular job.

## 🚀 Features

- 👤 Personalized welcome using the user's name
- 📄 Upload resume in PDF format
- 📊 Calculate an overall resume score
- ✅ Check important resume sections
- 🛠️ Detect technical skills from the resume
- 💪 Identify resume strengths
- ⚠️ Find areas that can be improved
- 💡 Provide personalized resume recommendations
- 🎯 Match a resume with a given job description
- 📈 Calculate job match score
- ✅ Display matching skills
- ❌ Display missing skills
- 🎯 Generate job-specific suggestions
- 📑 Display extracted resume text
- 📥 Download a complete resume analysis report

## 🛠️ Technologies Used

- Python
- Streamlit
- PyPDF2
- Regular Expressions (re)

## 📁 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── resume_parser.py
├── utils.py
├── requirements.txt
└── README.md

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/05-priyanka/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

### 2. Install the required libraries

```bash
pip install -r requirements.txt

### 3. Run the application

```bash
python -m streamlit run app.py

## 💡 Usage

1. Open the application in your browser.
2. Enter your name.
3. Upload your resume in PDF format.
4. Enter a job description.
5. Click the analyze button.
6. Review your resume score, matching skills, missing skills, and recommendations.
7. Download the complete analysis report.