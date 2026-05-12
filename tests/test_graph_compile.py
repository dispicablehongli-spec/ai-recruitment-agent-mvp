from backend.agent.graph import initial_state


def test_graph_compile_placeholder():
    state = initial_state(b"%PDF")
    assert "application_id" in state
