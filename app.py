import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq

from utils import(extract_skills,analyzer_skill_gap,calculate_match_score,
                  analyze_resume,build_candidate_profile,extract_contact_info)
from dotenv import load_dotenv
load_dotenv()
from llm import get_llm

# ✅ Step 3 — check API key first
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Groq API key not found")
    st.stop()

# ✅ Step 4 — create LLM once, after key is confirmed
llm = get_llm()

st.title("Resume Analyzer")

# Resume upload & Text extraction
uploaded_file=st.file_uploader(
    "upload resume",
    type=['pdf']
)

if uploaded_file is not None:

    st.success(f"uploaded:{uploaded_file.name}")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.pdf' 
    ) as temp_file:
        
        temp_file.write(uploaded_file.read())

        temp_path=temp_file.name

    loader=PyPDFLoader(temp_path)    

    documents=loader.load()

    resume_text=""

    for doc in documents:
        resume_text=resume_text+doc.page_content + "\n"

    st.subheader("Extracted resume text")

    st.text_area(
        "resume content",
        resume_text,
        height=400
    )

    os.remove(temp_path)

    # skills

    st.subheader("Detected skills")
        
    skills=extract_skills(resume_text)


    for skill in skills:
        st.write("✅", skill)

        # job description
    
    st.subheader("Job Description")

    job_description=st.text_area(
        "Paste job Description Here",
        height=250
    )  

    jd_skills=extract_skills(job_description)
    st.write("Resume Skills:", skills)
    st.write("JD Skills:", jd_skills)

    st.subheader("Required Skills")

    for jd_skill in jd_skills:
        st.write("📌", jd_skill)


    # analyzer_skill_gap

    matched_skills,missing_skills=analyzer_skill_gap(skills,jd_skills)

    st.subheader("matched skills")

    for matched_skill in matched_skills:
        st.success(matched_skill)

    for missing_skill in missing_skills:
        st.error(missing_skill)


    # calcualte_match_Score

    score=calculate_match_score(
        matched_skills,
        jd_skills
    )

    st.subheader("Match Score")
    st.metric(
        "Resume Match %",
        f"{score}%"
    )

    # AI Resume Review
     
    analysis=analyze_resume(llm,resume_text,job_description)

    st.subheader("AI Resume Review")
    st.write(analysis)


# After resume_text is ready
    candidate=build_candidate_profile(resume_text)
    contact_info=candidate
    st.subheader("Contact Information")

    if contact_info['email']:
        st.write('Email:',contact_info['email'])
    else:
        st.warning("Email not found")

    if contact_info['phone']:
        st.write("Phone:",contact_info['phone'])
    else:
        st.warning("Phone not found")

    if contact_info['github']:
        st.write("Github:",contact_info['github'])
    else:
        st.write("Github not found")

    if contact_info['linkedin']:
        st.write('linkedin',contact_info['linkedin'])

    else:
        st.warning('linkedin not found')                            

    # Build candidate profile — ONE call does everything
candidate = build_candidate_profile(resume_text)

# ── Contact Information ──────────────────────────
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

# ── Education Details (NEW in Day 12) ───────────
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

# ── Experience Details (NEW in Day 12) ──────────
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

# ── Project Details (NEW in Day 12) ─────────────
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

# ── Skills ───────────────────────────────────────
st.subheader("🛠️ Detected Skills")
for skill in candidate["skills"]:
    st.write("✅", skill)    