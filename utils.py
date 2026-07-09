SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "nlp",
    "docker",
    "git",
    "github",
    "aws",
    "azure",
    "flask",
    "streamlit",
    "pandas",
    "numpy",
    "scikit-learn"
]
# extract skills
def extract_skills(text):

    text=text.lower()
    found_skills=[]

    for skills in SKILLS:
        if skills in text:
            found_skills.append(skills)

    return found_skills        

# analyze skill gap
def analyzer_skill_gap(
            candidate_skills,
            required_skills
    ):
        candidate_skills=set(candidate_skills)
        required_skills=set(required_skills)

        matched_skills=candidate_skills.intersection(
            required_skills
    )
        missing_skills=required_skills.difference(
        candidate_skills)

        return (
        list(matched_skills),
        list(missing_skills)
    )    

# calculate match score

def calculate_match_score(
        matched_skills,
        required_skills
):
    if len(required_skills)==0:
        return 0
    
    score=(
        len(matched_skills)/len(required_skills))*100
    
    return round(score,2)

# LLM function

from langchain_core.prompts import PromptTemplate
from prompts import ANALYSIS_PROMPT

def analyze_resume(llm,resume_text,job_description):
    prompt=PromptTemplate.from_template(
        ANALYSIS_PROMPT
    )

    chain=prompt| llm

    try:

        response=chain.invoke({
            "resume":resume_text,
            "job_description":job_description
        })

        return response.content
    except Exception as e:
         return f"LLM error:{str(e)}"



import re

SECTION_HEADERS = {

    "education": [
        "education",
        "academic background",
        "qualification"
    ],

    "experience": [
        "experience",
        "work experience",
        "employment"
    ],

    "projects": [
        "projects",
        "project"
    ],

    "skills": [
        "skills",
        "technical skills"
    ],

    "certifications": [
        "certifications",
        "certificates"
    ]

}

def parse_resume_sections(resume_text):

    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "certifications": "",
        "others": ""
    }

    

    lines=resume_text.split("\n")

    current_section='others'

    for line in lines:
        clean_line=line.strip().lower()
        match_section=None

        for section_name,keywords in SECTION_HEADERS.items():
            for keyword in keywords:
                pattern=r"^\s*"+re.escape(keyword)+r"\s*:?\s*$"
                if re.match(pattern,clean_line):
                     
                    match_section=section_name
                    break
            if match_section:
                     break
                
                

        if match_section:
                 current_section=match_section
                 continue
            
        sections[current_section]+=line+'\n'
             

    return sections     



def extract_email(text):
     pattern=r"[a-zA-Z0._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
     match=re.search(pattern,text)
     return match.group() if match else None


def extract_phone(text):
     pattern=r"(\+91[\-\s]?[6-9]\d{9})"
     match=re.search(pattern,text)
     return match.group() if match else None

def extract_github(text):
     pattern=r"(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_-]+"
     match=re.search(pattern,text)
     return match.group() if match else None

def extract_linkedin(text):
     pattern=r"(https?:\/\/)?(www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+"
     match=re.search(pattern,text)
     return match.group() if match else None


def extract_contact_info(text):
     return {
          "email":extract_email(text),
          "phone":extract_phone(text),
          "github":extract_github(text),
          "linkedin":extract_linkedin(text)
     }


def build_candidate_profile(resume_text):
    section=parse_resume_sections(resume_text)
    contact=extract_contact_info(resume_text)
    SKILLS=extract_skills(resume_text)

    candidate={
          "name":None,
          "email":contact.get('email'),
          'phone':contact.get('phone'),
          'github':contact.get('github'),
          'linkedin':contact.get('linkedin'),
          'education':section.get('education',""),
          'experience':section.get('experience',''),
          'project':section.get('projects',''),
          'skills':SKILLS,
          'certification':section.get('certification','')


    }
    
    return candidate

