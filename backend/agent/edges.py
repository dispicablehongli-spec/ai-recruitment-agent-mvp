def next_after_required_fields(state: dict) -> str:
    if state["resume_required_fields_complete"]:
        return "match_jobs"
    return "reupload_request"


def next_after_match(state: dict) -> str:
    if state["qualified_jobs"]:
        return "job_selection"
    return "final_rejection"
