import pytest

from backend.agent.nodes.error_node import error_node
from backend.agent.nodes.final_rejection import final_rejection_node
from backend.agent.nodes.success import success_node


@pytest.mark.asyncio
async def test_terminal_nodes_results():
    success_state = {"status": "", "final_result": None}
    reject_state = {"status": "", "final_result": None, "failure_type": None}
    error_state = {"status": "", "final_result": None, "errors": []}

    await success_node(success_state)
    await final_rejection_node(reject_state)
    await error_node(error_state, RuntimeError("x"))

    assert success_state["final_result"] == "success"
    assert reject_state["final_result"] == "rejected"
    assert error_state["final_result"] == "error"
