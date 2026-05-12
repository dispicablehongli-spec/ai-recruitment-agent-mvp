from backend.llm.client import get_llm_client
from backend.llm.prompts.resume_extract import build_resume_extract_prompt
from backend.llm.schemas import ResumeSchema


def _mock_resume(text: str) -> dict:
    lower = text.lower()
    skills = []
    for item in ["python", "fastapi", "sql", "asyncio", "react", "typescript"]:
        if item in lower:
            skills.append(item)
    if not skills and "match_failed" not in lower:
        skills = ["python", "fastapi"]
    return {
        "name": "Demo Candidate" if "name:" not in lower else text.split("name:")[1].splitlines()[0].strip(),
        "date_of_birth": "1998-01",
        "gender": "male",
        "email": None if "missing_email" in lower else "demo@example.com",
        "phone": "18800000000",
        "experiences": ["Built backend systems"],
        "skills": skills if "match_failed" not in lower else ["painting"],
        "education": ["Demo University, Bachelor"],
        "certifications": [],
        "years_of_experience": 3,
        "industry_tags": ["software"],
    }


async def resume_extract_node(state: dict) -> dict:
    state["status"] = "parsing_document"
    if state.get("use_real_llm"):
        prompt = build_resume_extract_prompt(state["resume_text"])
        data = await get_llm_client().chat_json(prompt)
    else:
        data = _mock_resume(state["resume_text"])
    state["parsed_resume"] = ResumeSchema.model_validate(data).model_dump()
    return state
