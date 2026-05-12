async def final_rejection_node(state: dict) -> dict:
    state["final_result"] = "rejected"
    if not state.get("failure_type"):
        state["failure_type"] = "MATCH_FAILED"
    state["status"] = "match_failed_terminated"
    return state
