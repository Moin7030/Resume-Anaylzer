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

def extract_skills(text):

    text=text.lower()
    found_skills=[]

    for skills in SKILLS:
        if skills in text:
            found_skills.append(skills)

    return found_skills        