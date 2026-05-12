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

    # Safe name extraction: work entirely on lower-cased text to avoid IndexError
    name = "Demo Candidate"
    if "name:" in lower:
        parts = lower.split("name:", 1)
        if len(parts) > 1:
            name = parts[1].splitlines()[0].strip().title() or "Demo Candidate"

    # Detect email: if the text already contains an @-address, use it; otherwise treat as missing
    import re as _re
    email_match = _re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else None

    # Detect "graphic/design/art" profile → simulate a non-tech match-failed scenario
    is_non_tech = any(kw in lower for kw in ["graphic design", "illustrat", "figma", "procreate", "adobe illustrator"])
    effective_skills = ["painting"] if is_non_tech else (skills if skills else ["python", "fastapi"])

    return {
        "name": name,
        "date_of_birth": "1998-01",
        "gender": "male",
        "email": email,
        "phone": "18800000000",
        "experiences": ["Built backend systems"],
        "skills": effective_skills,
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
