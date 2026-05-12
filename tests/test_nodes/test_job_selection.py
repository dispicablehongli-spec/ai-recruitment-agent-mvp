import pytest

from backend.agent.nodes.job_selection import job_selection_node


@pytest.mark.asyncio
async def test_job_selection_valid():
    state = {
        "selected_job_id": "a",
        "qualified_jobs": [{"id": "a"}],
        "status": "waiting_job_selection",
    }
    await job_selection_node(state)

