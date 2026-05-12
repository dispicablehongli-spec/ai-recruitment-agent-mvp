REQUIRED_FIELDS = [
    "name",
    "date_of_birth",
    "gender",
    "email",
    "phone",
    "experiences",
    "skills",
    "education",
]


async def resume_required_fields_check_node(state: dict) -> dict:
    state["status"] = "validating_required_resume_fields"
    missing: list[str] = []
    for key in REQUIRED_FIELDS:
        value = state["parsed_resume"].get(key)
        if value is None or value == "" or value == []:
            missing.append(key)
    state["missing_required_resume_fields"] = missing
    state["resume_required_fields_complete"] = len(missing) == 0
    state["reupload_suggestions"] = [f"please provide {name}" for name in missing]
    return state
