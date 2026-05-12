async def resume_reupload_request_node(state: dict) -> dict:
    state["status"] = "required_resume_fields_missing_waiting_reupload"
    return state
