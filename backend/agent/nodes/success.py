async def success_node(state: dict) -> dict:
    state["final_result"] = "success"
    state["status"] = "process_success"
    return state
