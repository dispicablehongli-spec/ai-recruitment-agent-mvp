import pytest

from backend.agent.graph import (
    apply_cancel,
    apply_job_selection,
    apply_reupload,
    initial_state,
    run_until_interrupt_or_end,
)


@pytest.mark.asyncio
async def test_happy_path():
    state = initial_state(b"%PDF-1.4\nname:demo\npython fastapi sql")
    state = await run_until_interrupt_or_end(state)
    assert state["status"] == "waiting_job_selection"
    assert state["qualified_jobs"]
    state = await apply_job_selection(state, state["qualified_jobs"][0]["id"])
    assert state["final_result"] == "success"


@pytest.mark.asyncio
async def test_match_failed():
    state = initial_state(b"%PDF-1.4\nmatch_failed")
    state = await run_until_interrupt_or_end(state)
    assert state["final_result"] == "rejected"
    assert state["failure_type"] == "MATCH_FAILED"


@pytest.mark.asyncio
async def test_user_cancel():
    state = initial_state(b"%PDF-1.4\nmissing_email")
    state = await run_until_interrupt_or_end(state)
    assert state["status"] == "required_resume_fields_missing_waiting_reupload"
    state = await apply_cancel(state)
    assert state["failure_type"] == "USER_CANCELLED"


@pytest.mark.asyncio
async def test_reupload_success():
    state = initial_state(b"%PDF-1.4\nmissing_email")
    state = await run_until_interrupt_or_end(state)
    assert state["status"] == "required_resume_fields_missing_waiting_reupload"
    state = await apply_reupload(state, b"%PDF-1.4\npython fastapi sql")
    assert state["status"] == "waiting_job_selection"
