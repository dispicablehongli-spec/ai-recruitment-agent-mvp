import pytest

from backend.agent.graph import initial_state
from backend.agent.nodes.pdf_parse import pdf_parse_node


@pytest.mark.asyncio
async def test_pdf_parse_node_sets_text():
    state = initial_state(b"%PDF-1.4\nhello world")
    await pdf_parse_node(state)
    assert state["resume_text"]
