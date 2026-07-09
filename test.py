from utils import extract_contact_info

# text=open('resume.txt').read()
# print(extract_contact_info(text))

# test.py (temporary file)
from utils import parse_resume_sections

text = open("resume.txt").read()
print(parse_resume_sections(text))


text = open("resume.txt").read()
print(parse_resume_sections(text))
print(extract_contact_info(text))