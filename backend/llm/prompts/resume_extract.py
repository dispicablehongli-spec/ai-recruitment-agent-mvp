def build_resume_extract_prompt(resume_text: str) -> str:
    return f"""
You are a resume parser. Return strict JSON with fields:
name, date_of_birth, gender, email, phone, experiences, skills, education, certifications, years_of_experience, industry_tags.
If unknown use null or [].

Resume text:
{resume_text}
""".strip()
