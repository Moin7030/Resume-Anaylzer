# from utils import extract_contact_info

# # text=open('resume.txt').read()
# # print(extract_contact_info(text))

# # test.py (temporary file)
# from utils import parse_resume_sections

# text = open("resume.txt").read()
# print(parse_resume_sections(text))


# text = open("resume.txt").read()
# print(parse_resume_sections(text))
# print(extract_contact_info(text))

from llm import get_embedding_model
from utils import compute_similarity, semantic_skill_match

model = get_embedding_model()

# ── Test 1 — Check raw similarity scores first
print("=== Raw Similarity Scores ===")
print("TensorFlow vs Deep Learning:", compute_similarity("TensorFlow", "Deep Learning", model))
print("Python vs Data Analysis:", compute_similarity("Python", "Data Analysis", model))
print("SQL vs Java:", compute_similarity("SQL", "Java", model))

print()

# ── Test 2 — Check all combinations
print("=== All Combinations ===")
candidate_skills = ["TensorFlow", "Python", "SQL"]
required_skills  = ["Deep Learning", "Data Analysis", "Java"]

for req in required_skills:
    for cand in candidate_skills:
        score = compute_similarity(cand, req, model)
        print(f"{cand} vs {req}: {round(score, 3)}")
    print()

print()

# ── Test 3 — Run semantic match with lower threshold
print("=== Semantic Match (threshold=0.3) ===")
result = semantic_skill_match(
    candidate_skills=candidate_skills,
    required_skills=required_skills,
    model=model,
    threshold=0.3    # ← lower threshold to see if anything matches
)
print(result)