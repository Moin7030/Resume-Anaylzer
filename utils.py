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

