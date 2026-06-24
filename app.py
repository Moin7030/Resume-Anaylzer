import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from utils import extract_skills



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
