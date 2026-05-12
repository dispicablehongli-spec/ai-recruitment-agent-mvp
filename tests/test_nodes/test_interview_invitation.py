import pytest

from backend.agent.nodes.interview_invitation import interview_invitation_node


@pytest.mark.asyncio
async def test_invitation_logs_link():
    state = {"logs": [], "status": "", "force_invite_error": False}
    await interview_invitation_node(state)
    assert "invite link:" in state["logs"][0]
