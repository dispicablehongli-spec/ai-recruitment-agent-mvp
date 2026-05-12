from backend.agent.graph import initial_state


def test_state_defaults():
    state = initial_state(b"fake", use_demo_jobs=True)
    assert state["resume_reupload_count"] == 0
    assert state["max_resume_reupload_count"] == 2
    assert state["total_upload_count"] == 1
    assert state["max_total_upload_count"] == 5
    assert state["user_cancelled"] is False
