from uuid import uuid4


async def interview_invitation_node(state: dict) -> dict:
    if state.get("force_invite_error"):
        raise RuntimeError("forced invitation error")
    invite_url = f"https://recruit.example.com/invite/{uuid4()}"
    state["logs"].append(f"invite link: {invite_url}")
    state["status"] = "interview_invited"
    return state
