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
          'education':extract_education_details(section.get('education',"")),
          'experience':extract_experience_details(section.get('experience','')),
          'project':extract_project_details(section.get('projects','')),
          'skills':SKILLS,
          'certification':section.get('certification','')


    }
    
    return candidate

Degree_keyword=[
       "b.tech", "btech", "b.e", "be",
    "m.tech", "mtech", "bca", "mca",
    "b.sc", "m.sc", "mba", "phd"
]

role_keywords=[
     "intern", "developer", "engineer", "analyst", "manager", "researcher"
]

def extract_year(text):
     pattern=r"\b(19|20)\d{2}\b"
     return re.findall(r"\b(?:19|20)\d{2}\b",text)

def extract_degree(text):
    text_lower=text.lower()
    found=[]
    for degree in Degree_keyword:
        pattern =r'\b'+re.escape(degree)+'r\b'
        if re.search(pattern,text_lower):
            found.append(degree)
    return found

def extract_university(text):
    pattern=r"([A-Z][A-Za-z&,\s]*?(University|Institute|College))"
    match=re.search(pattern,text)
    return match.group().strip() if match else None


def extract_company(text):
    pattern=r"([A-Z][A-Za-z&]*\s?){1,3}(Pvt\.?\s?Ltd\.?|Technologies|Solutions|Systems|Inc\.?|LLP)"
    match=re.search(pattern,text)
    return match.group().strip() if match else None

def extract_role(text):
    text_lower=text.lower()
    for role in role_keywords:
        if role in text_lower:
            return role
    return None

def extract_education_details(education_text):
    return{
        "Degree":extract_degree(education_text),
        "university":extract_university(education_text),
        "Graduation_year":extract_year(education_text)
    }    

def extract_experience_details(experience_text):
    return{
        "Company":extract_company(experience_text),
        "University":extract_university(experience_text),
        "Graduation_year":extract_year(experience_text)
    }

def extract_experience_details(experience_text):
    return{
        "Company":extract_company(experience_text),
        "Role":extract_role(experience_text),
        "Duration":extract_year(experience_text)
    } 

def extract_project_details(projects_text):
    lines=[line.strip() for line in projects_text.split("\n") if line.strip()]
    return{
        "title":lines[0] if lines else None,
        "Description":"".join(lines[1:]) if len(lines)>1 else "",
        "Technologies":extract_skills(projects_text)
    }

     
          


        


