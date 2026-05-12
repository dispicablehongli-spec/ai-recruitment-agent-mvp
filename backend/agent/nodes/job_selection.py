async def job_selection_node(state: dict) -> dict:
    selected = state.get("selected_job_id")
    if not selected:
        state["status"] = "waiting_job_selection"
        return state
    qualified_ids = {job["id"] for job in state["qualified_jobs"]}
    if selected not in qualified_ids:
        raise ValueError("selected job is not in qualified jobs")
    return state
