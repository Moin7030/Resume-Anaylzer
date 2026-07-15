import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from llm import get_llm,get_embedding_model

# ✅ Bug fixed — clean single import, no duplicates
from utils import (
    extract_skills,
    analyzer_skill_gap,
    calculate_match_score,
    analyze_resume,
    build_candidate_profile,
    compute_similarity,
    semantic_skill_match,
    match_project_to_job
)


load_dotenv()

# ✅ Check API key first
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Groq API key not found")
    st.stop()

# ✅ Create LLM once
llm = get_llm()

st.title("Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume", type=['pdf'])

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    resume_text = ""
    for doc in documents:
        resume_text = resume_text + doc.page_content + "\n"

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=400)
    os.remove(temp_path)

    # ✅ Bug 9 fixed — called only ONCE
    candidate = build_candidate_profile(resume_text)

    # ── Contact Information ───────────────────────
    st.subheader("📋 Contact Information")

    if candidate["email"]:
        st.write("📧 Email:", candidate["email"])
    else:
        st.warning("⚠️ Email not found")

    if candidate["phone"]:
        st.write("📱 Phone:", candidate["phone"])
    else:
        st.warning("⚠️ Phone not found")

    if candidate["github"]:
        st.write("💻 GitHub:", candidate["github"])
    else:
        st.warning("⚠️ GitHub not found")

    if candidate["linkedin"]:
        st.write("🔗 LinkedIn:", candidate["linkedin"])
    else:
        st.warning("⚠️ LinkedIn not found")

    # ── Education Details ─────────────────────────
    st.subheader("🎓 Education Details")
    education = candidate["education"]

    if education["degree"]:
        st.write("📜 Degree:", ", ".join(education["degree"]))
    else:
        st.warning("⚠️ Degree not found")

    if education["university"]:
        st.write("🏫 University:", education["university"])
    else:
        st.warning("⚠️ University not found")

    if education["graduation_year"]:
        st.write("📅 Graduation Year:", ", ".join(education["graduation_year"]))
    else:
        st.warning("⚠️ Graduation year not found")

    # ── Experience Details ────────────────────────
    st.subheader("💼 Experience Details")
    experience = candidate["experience"]

    if experience["company"]:
        st.write("🏢 Company:", experience["company"])
    else:
        st.warning("⚠️ Company not found")

    if experience["role"]:
        st.write("👔 Role:", experience["role"])
    else:
        st.warning("⚠️ Role not found")

    if experience["duration"]:
        st.write("📅 Duration:", " - ".join(experience["duration"]))
    else:
        st.warning("⚠️ Duration not found")

    # ── Project Details ───────────────────────────
    st.subheader("📁 Project Details")
    projects = candidate["projects"]

    if projects["title"]:
        st.write("📌 Title:", projects["title"])
    else:
        st.warning("⚠️ Project title not found")

    if projects["description"]:
        st.write("📝 Description:", projects["description"])
    else:
        st.warning("⚠️ Description not found")

    if projects["technologies"]:
        st.write("🛠️ Technologies:", ", ".join(projects["technologies"]))
    else:
        st.warning("⚠️ Technologies not found")

    # ── Skills ────────────────────────────────────
    st.subheader("🛠️ Detected Skills")
    skills = candidate["skills"]
    for skill in skills:
        st.write("✅", skill)

    # ── Job Description ───────────────────────────
    st.subheader("Job Description")
    job_description = st.text_area("Paste Job Description Here", height=250)

    jd_skills = extract_skills(job_description)

    st.subheader("Required Skills")
    for jd_skill in jd_skills:
        st.write("📌", jd_skill)

    # ── Skill Gap ─────────────────────────────────
    matched_skills, missing_skills = analyzer_skill_gap(skills, jd_skills)

    st.subheader("✅ Matched Skills")
    for matched_skill in matched_skills:
        st.success(matched_skill)

    st.subheader("❌ Missing Skills")
    for missing_skill in missing_skills:
        st.error(missing_skill)

    # ── Match Score ───────────────────────────────
    score = calculate_match_score(matched_skills, jd_skills)
    st.subheader("Match Score")
    st.metric("Resume Match %", f"{score}%")

    # ── AI Resume Review ──────────────────────────
    analysis = analyze_resume(llm, resume_text, job_description)
    st.subheader("🤖 AI Resume Review")
    st.write(analysis)

    result=semantic_skill_match(
        candidate_skills=candidate['skills'],
        required_skills=jd_skills,
        model=get_embedding_model(),
        threshold=0.5
    )

    st.write("Matched Skills:",result['matched'])
    st.write("Missing Skills:",result['missing'])

   # ── Project Relevance ─────────────────────────
    st.subheader("📁 Project Relevance")

    project_match = match_projects_to_job(
        project_details=candidate["projects"],
        job_description=job_description,
        model=embedding_model
    )

    if project_match["project_title"]:
        st.write("📌 Project:", project_match["project_title"])
        st.write("🎯 Relevance Score:", project_match["relevance_score"])

        if project_match["relevance_score"] >= 0.6:
            st.success("✅ Project highly relevant to this job!")
        elif project_match["relevance_score"] >= 0.4:
            st.warning("⚠️ Project somewhat relevant to this job")
        else:
            st.error("❌ Project has low relevance to this job")
    else:
        st.warning("⚠️ No project found in resume")