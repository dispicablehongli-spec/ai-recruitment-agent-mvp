from backend.agent.graph import initial_state


def test_checkpointer_placeholder():
    state = initial_state(b"%PDF")
    assert state["max_total_upload_count"] == 5
