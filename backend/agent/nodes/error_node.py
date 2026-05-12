async def error_node(state: dict, err: Exception) -> dict:
    state["final_result"] = "error"
    state["status"] = "system_error"
    state["errors"].append(str(err))
    return state
