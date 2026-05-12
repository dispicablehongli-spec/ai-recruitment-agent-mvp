import pytest

from backend.agent.graph import initial_state
from backend.agent.nodes.match_jobs import match_jobs_node


@pytest.mark.asyncio
async def test_happy():
    state = initial_state(b"%PDF")
    state["parsed_resume"] = {
        "skills": ["python", "fastapi", "sql"],
    }
    await match_jobs_node(state)
    assert len(state["qualified_jobs"]) >= 1
