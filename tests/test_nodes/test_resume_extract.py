import pytest

from backend.agent.graph import initial_state
from backend.agent.nodes.resume_extract import resume_extract_node


@pytest.mark.asyncio
async def test_resume_extract_mock_fields():
    state = initial_state(b"%PDF-1.4\npython fastapi")
    state["resume_text"] = "python fastapi"
    await resume_extract_node(state)
    assert state["parsed_resume"]["name"] is not None
