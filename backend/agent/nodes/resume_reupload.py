async def resume_reupload_node(state: dict) -> dict:
    state["resume_reupload_count"] += 1
    state["total_upload_count"] += 1
    state["status"] = "resume_reuploading"
    return state
