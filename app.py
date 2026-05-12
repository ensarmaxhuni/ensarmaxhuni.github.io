import os
import re
from io import BytesIO

import streamlit as st
from pypdf import PdfReader

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


SKILL_KEYWORDS = [
    "python", "sql", "excel", "power bi", "tableau", "machine learning",
    "deep learning", "generative ai", "llm", "langchain", "rag", "openai",
    "azure", "aws", "google cloud", "data analysis", "pandas", "numpy",
    "statistics", "dashboard", "api", "automation", "project management",
    "business intelligence", "finance", "marketing", "operations", "leadership"
]

ACTION_VERBS = [
    "built", "created", "developed", "analyzed", "managed", "led", "automated",
    "improved", "optimized", "designed", "implemented", "reduced", "increased",
    "delivered", "launched", "forecasted", "reported", "coordinated"
]


def extract_pdf_text(uploaded_file) -> str:
    """Extract text from a PDF upload."""
    pdf_bytes = uploaded_file.read()
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()


def extract_txt_text(uploaded_file) -> str:
    """Extract text from a TXT upload."""
    return uploaded_file.read().decode("utf-8", errors="ignore")


def basic_resume_analysis(resume_text: str, job_description: str = "") -> dict:
    """Rule-based resume analysis that works without an API key."""
    text = resume_text.lower()
    jd_text = job_description.lower()

    found_skills = sorted({skill for skill in SKILL_KEYWORDS if skill in text})
    jd_skills = sorted({skill for skill in SKILL_KEYWORDS if skill in jd_text})
    missing_skills = [skill for skill in jd_skills if skill not in found_skills]

    action_verb_count = sum(len(re.findall(rf"\b{verb}\b", text)) for verb in ACTION_VERBS)
    numbers_count = len(re.findall(r"\b\d+[%$]?|[%$]\d+", resume_text))

    sections = {
        "experience": bool(re.search(r"experience|employment|work history", text)),
        "education": "education" in text,
        "skills": "skills" in text,
        "projects": "project" in text,
        "certifications": bool(re.search(r"certification|certificate|certified", text)),
    }

    score = 40
    score += min(len(found_skills) * 3, 25)
    score += min(action_verb_count * 2, 15)
    score += min(numbers_count * 2, 10)
    score += sum(2 for present in sections.values() if present)
    if job_description and jd_skills:
        match_rate = (len(jd_skills) - len(missing_skills)) / len(jd_skills)
        score = int((score * 0.65) + (match_rate * 100 * 0.35))
    score = max(0, min(score, 100))

    recommendations = []
    if numbers_count < 5:
        recommendations.append("Add more measurable results, such as percentages, dollar amounts, time saved, or process improvements.")
    if action_verb_count < 8:
        recommendations.append("Start more bullet points with strong action verbs like built, analyzed, automated, improved, or led.")
    if not sections["projects"]:
        recommendations.append("Add a Projects section, especially AI, analytics, automation, or dashboard projects.")
    if not sections["certifications"]:
        recommendations.append("Add relevant certifications such as AI, data analytics, cloud AI, Power BI, or Python.")
    if missing_skills:
        recommendations.append("Add relevant job-description keywords where truthful: " + ", ".join(missing_skills[:8]) + ".")

    return {
        "ats_score": score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "sections": sections,
        "recommendations": recommendations,
        "numbers_count": numbers_count,
        "action_verb_count": action_verb_count,
    }


def ai_resume_analysis(resume_text: str, job_description: str = "") -> str:
    """Use OpenAI when an API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return ""

    client = OpenAI(api_key=api_key)
    prompt = f"""
You are an expert resume coach and ATS analyst.
Analyze the resume below for an entry-level AI, data analyst, AI business analyst, or AI operations role.

Return:
1. Overall score from 0-100
2. Strongest parts
3. Weakest parts
4. Missing AI/data keywords
5. ATS improvements
6. 5 rewritten bullet examples
7. Best target roles

Resume:
{resume_text[:12000]}

Job description, if provided:
{job_description[:6000]}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""


st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get an ATS-style score, keyword match, and improvement suggestions.")

with st.sidebar:
    st.header("How to use")
    st.write("1. Upload a PDF or TXT resume")
    st.write("2. Paste a job description if you have one")
    st.write("3. Click Analyze")
    st.info("Optional: add OPENAI_API_KEY in your environment for deeper AI feedback.")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])
job_description = st.text_area("Paste job description here (optional)", height=180)

if st.button("Analyze Resume", type="primary"):
    if not uploaded_file:
        st.warning("Please upload a resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            if uploaded_file.name.lower().endswith(".pdf"):
                resume_text = extract_pdf_text(uploaded_file)
            else:
                resume_text = extract_txt_text(uploaded_file)

            if not resume_text:
                st.error("Could not extract text from the resume. Try uploading a TXT version.")
                st.stop()

            results = basic_resume_analysis(resume_text, job_description)
            ai_feedback = ai_resume_analysis(resume_text, job_description)

        col1, col2, col3 = st.columns(3)
        col1.metric("ATS-Style Score", f"{results['ats_score']}/100")
        col2.metric("Skills Found", len(results["found_skills"]))
        col3.metric("Quantified Results", results["numbers_count"])

        st.subheader("Detected Skills")
        if results["found_skills"]:
            st.write(", ".join(results["found_skills"]))
        else:
            st.write("No major AI/data/business keywords detected yet.")

        if job_description:
            st.subheader("Missing Keywords From Job Description")
            if results["missing_skills"]:
                st.write(", ".join(results["missing_skills"]))
            else:
                st.success("Good keyword match based on the current keyword list.")

        st.subheader("Resume Sections Check")
        for section, present in results["sections"].items():
            st.write(f"{'✅' if present else '❌'} {section.title()}")

        st.subheader("Recommended Improvements")
        if results["recommendations"]:
            for item in results["recommendations"]:
                st.write(f"- {item}")
        else:
            st.success("Your resume has a solid structure. Keep improving keyword alignment and measurable results.")

        if ai_feedback:
            st.subheader("AI-Powered Detailed Feedback")
            st.markdown(ai_feedback)
        else:
            st.caption("Add an OPENAI_API_KEY to unlock deeper AI-written feedback.")

        with st.expander("Preview extracted resume text"):
            st.text(resume_text[:5000])
