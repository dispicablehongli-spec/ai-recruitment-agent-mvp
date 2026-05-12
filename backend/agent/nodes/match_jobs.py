import asyncio

from backend.llm.client import get_llm_client
from backend.llm.prompts.job_match import build_job_match_prompt
from backend.llm.schemas import MatchResult


def _score_resume_for_job(parsed_resume: dict, job: dict) -> MatchResult:
    skills = {s.lower() for s in parsed_resume.get("skills", [])}
    job_skills = {s.lower() for s in job.get("skills", [])}
    overlap = len(skills & job_skills)
    total = max(len(job_skills), 1)
    skill_score = int((overlap / total) * 100)
    experience_score = 80
    industry_score = 70
    education_score = 75
    match_score = round(skill_score * 0.35 + experience_score * 0.30 + industry_score * 0.20 + education_score * 0.15)
    return MatchResult(
        job_id=job["id"],
        match_score=match_score,
        is_information_complete=True,
        missing_dimensions=[],
        skill_score=skill_score,
        experience_score=experience_score,
        industry_score=industry_score,
        education_score=education_score,
        strengths=["skill overlap" if overlap else "general profile"],
        risks=[] if overlap else ["missing job specific skills"],
        missing_skills=list(job_skills - skills),
        reasoning="deterministic mock scoring",
    )


async def _real_match(parsed_resume: dict, job: dict) -> MatchResult:
    prompt = build_job_match_prompt(parsed_resume, job)
    data = await get_llm_client().chat_json(prompt)
    return MatchResult.model_validate(data)


async def match_jobs_node(state: dict) -> dict:
    state["status"] = "matching_jobs"
    jobs = state["all_jobs"]
    if state.get("use_real_llm"):
        semaphore = asyncio.Semaphore(5)

        async def run(job: dict) -> MatchResult:
            async with semaphore:
                return await _real_match(state["parsed_resume"], job)

        results = await asyncio.gather(*(run(job) for job in jobs))
    else:
        results = [_score_resume_for_job(state["parsed_resume"], job) for job in jobs]

    state["all_match_results"] = results
    qualified_ids = {result.job_id for result in results if result.match_score >= 75}
    state["qualified_jobs"] = [job for job in jobs if job["id"] in qualified_ids]
    return state
