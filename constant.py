
import re

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


section_pattern={
    "education":
   r"^(education|academic background|qualification|qualifications|education & training)",

   "experience":
   r"^(experience|work experience|employment history|professional experience)$",

   "skills":
   r"^(projects|personal projects|academic project)$",

   "certifications":
   r"^(certifications|certificates|licenses)$"

}
