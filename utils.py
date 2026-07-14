import re
from langchain_core.prompts import PromptTemplate
from prompts import ANALYSIS_PROMPT
from sentence_transformers import util as st_util

# ── Constants ───────────────────────────────────
SKILLS = [
    "python", "java", "c++", "sql",
    "tensorflow", "pytorch", "machine learning",
    "deep learning", "nlp", "docker",
    "git", "github", "aws", "azure",
    "flask", "streamlit", "pandas",
    "numpy", "scikit-learn"
]

SECTION_HEADERS = {
    "education": ["education", "academic background", "qualification"],
    "experience": ["experience", "work experience", "employment"],
    "projects": ["projects", "project"],
    "skills": ["skills", "technical skills"],
    "certifications": ["certifications", "certificates"]
}

DEGREE_KEYWORDS = [
    "b.tech", "btech", "b.e", "be",
    "m.tech", "mtech", "bca", "mca",
    "b.sc", "m.sc", "mba", "phd"
]

ROLE_KEYWORDS = [
    "intern", "developer", "engineer",
    "analyst", "manager", "researcher"
]

# ── Skills ──────────────────────────────────────
def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    return found_skills

# ── Skill Gap ────────────────────────────────────
def analyzer_skill_gap(candidate_skills, required_skills):
    candidate_skills = set(candidate_skills)
    required_skills = set(required_skills)
    matched_skills = candidate_skills.intersection(required_skills)
    missing_skills = required_skills.difference(candidate_skills)
    return (list(matched_skills), list(missing_skills))

# ── Match Score ──────────────────────────────────
def calculate_match_score(matched_skills, required_skills):
    if len(required_skills) == 0:
        return 0
    score = (len(matched_skills) / len(required_skills)) * 100
    return round(score, 2)

# ── LLM Analysis ─────────────────────────────────
def analyze_resume(llm, resume_text, job_description):
    prompt = PromptTemplate.from_template(ANALYSIS_PROMPT)
    chain = prompt | llm
    try:
        response = chain.invoke({
            "resume": resume_text,
            "job_description": job_description
        })
        return response.content
    except Exception as e:
        return f"LLM error: {str(e)}"

# ── Section Parser ───────────────────────────────
def parse_resume_sections(resume_text):
    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "certifications": "",
        "others": ""
    }
    lines = resume_text.split("\n")
    current_section = "others"

    for line in lines:
        clean_line = line.strip().lower()
        matched_section = None

        for section_name, keywords in SECTION_HEADERS.items():
            for keyword in keywords:
                pattern = r"^\s*" + re.escape(keyword) + r"\s*:?\s*$"
                if re.match(pattern, clean_line):
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            current_section = matched_section
            continue

        sections[current_section] += line + "\n"

    return sections

# ── Contact Extraction ───────────────────────────
def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_phone(text):
    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_github(text):
    pattern = r"(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_-]+"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_linkedin(text):
    pattern = r"(https?:\/\/)?(www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_contact_info(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "github": extract_github(text),
        "linkedin": extract_linkedin(text)
    }

# ── Day 12 Functions ─────────────────────────────
def extract_year(text):
    return re.findall(r"\b(?:19|20)\d{2}\b", text)

def extract_degree(text):
    text_lower = text.lower()
    found = []
    for degree in DEGREE_KEYWORDS:
        pattern = r"\b" + re.escape(degree) + r"\b"
        if re.search(pattern, text_lower):
            found.append(degree)
    return found

def extract_university(text):
    pattern = r"([A-Z][A-Za-z&,\s]*?(University|Institute|College))"
    match = re.search(pattern, text)
    return match.group().strip() if match else None

def extract_company(text):
    pattern = r"([A-Z][A-Za-z&]*\s?){1,3}(Pvt\.?\s?Ltd\.?|Technologies|Solutions|Systems|Inc\.?|LLP)"
    match = re.search(pattern, text)
    return match.group().strip() if match else None

def extract_role(text):
    text_lower = text.lower()
    for role in ROLE_KEYWORDS:
        if role in text_lower:
            return role
    return None

# ✅ All lowercase keys
def extract_education_details(education_text):
    return {
        "degree": extract_degree(education_text),
        "university": extract_university(education_text),
        "graduation_year": extract_year(education_text)
    }

# ✅ No duplicate, correct lowercase keys
def extract_experience_details(experience_text):
    return {
        "company": extract_company(experience_text),
        "role": extract_role(experience_text),
        "duration": extract_year(experience_text)
    }

def extract_project_details(projects_text):
    lines = [line.strip() for line in projects_text.split("\n") if line.strip()]
    return {
        "title": lines[0] if lines else None,
        "description": " ".join(lines[1:]) if len(lines) > 1 else "",
        "technologies": extract_skills(projects_text)
    }


          
# day 13--Embedding work-----

def get_embedding(text,model):
    return model.encode(text,convert_to_tensor=True)

def compute_similarity(text1,text2,model):
    embedding1=get_embedding(text1,model)
    embedding2=get_embedding(text2,model)
    similarity_score=st_util.cos_sim(embedding1,embedding2)
    return float(similarity_score[0][0])

        
# day 14-----Semantic skills



def semantic_skill_match(candidate_skills,required_skills,model,threshold=0.5):
    matched=[]
    missing=[]

    for req_skill in required_skills:
        best_score=0
        best_match=None

        for cand_skill in candidate_skills:
            score=compute_similarity(cand_skill,req_skill,model)
            if score>best_score:
                best_score=score
                best_match=cand_skill

        if best_score>=threshold:
            matched.append({
                "required":req_skill,
                "matched_with":best_match,
                'score':round(best_score,2)
            })
        else:
            missing.append(req_skill)
    return{
    'matched':matched,
    'missing':missing
}                            

# ✅ Moved to bottom, all correct key names
def build_candidate_profile(resume_text):
    sections = parse_resume_sections(resume_text)
    contact = extract_contact_info(resume_text)
    skills = extract_skills(resume_text)

    candidate = {
        "name": None,
        "email": contact.get("email"),
        "phone": contact.get("phone"),
        "github": contact.get("github"),
        "linkedin": contact.get("linkedin"),
        "education": extract_education_details(sections.get("education", "")),
        "experience": extract_experience_details(sections.get("experience", "")),
        "projects": extract_project_details(sections.get("projects", "")),
        "skills": skills,
        "certifications": sections.get("certifications", "")
    }

    return candidate
