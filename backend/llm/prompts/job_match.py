def build_job_match_prompt(parsed_resume: dict, job: dict) -> str:
    return f"""
You are a recruiter assistant. Score resume for the job.
Return strict JSON:
job_id, match_score, is_information_complete, missing_dimensions, skill_score, experience_score, industry_score, education_score, strengths, risks, missing_skills, reasoning.
Scores are integers [0, 100].
Job:
{job}
Resume:
{parsed_resume}
""".strip()
