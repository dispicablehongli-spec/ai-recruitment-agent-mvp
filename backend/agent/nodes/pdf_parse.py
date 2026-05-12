from backend.services.pdf_service import parse_pdf_bytes


async def pdf_parse_node(state: dict) -> dict:
    if state["total_upload_count"] > state["max_total_upload_count"]:
        state["status"] = "upload_limit_exceeded"
        state["failure_type"] = "RESUME_REQUIRED_FIELDS_MISSING"
        state["final_failure_reason"] = "upload limit exceeded"
        state["final_result"] = "rejected"
        return state

    state["status"] = "parsing_document"
    state["resume_text"] = parse_pdf_bytes(state["pdf_bytes"])
    state["status"] = "parse_success"
    return state
