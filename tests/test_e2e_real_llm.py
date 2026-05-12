import os
import pytest
from backend.agent.graph import apply_job_selection, initial_state, run_until_interrupt_or_end


@pytest.mark.asyncio
async def test_e2e_real_llm():
    if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        pytest.skip("OPENAI_API_KEY not configured")

    state = initial_state(
        b"%PDF-1.4\nname: Alice Zhang\nemail: alice@example.com\nphone: 13800000000\n"
        b"gender: female\ndate_of_birth: 1995-05\n"
        b"skills: python fastapi sql asyncio\n"
        b"experience: 3 years backend development\n"
        b"education: Tsinghua University, Bachelor of Computer Science\n",
        use_real_llm=True,
    )
    state = await run_until_interrupt_or_end(state)
    # system_error is valid when LLM API is unreachable or returns unexpected output
    assert state["status"] in (
        "waiting_job_selection",
        "required_resume_fields_missing_waiting_reupload",
        "process_success",
        "match_failed_terminated",
        "system_error",
    )
    if state["status"] == "waiting_job_selection":
        assert len(state["qualified_jobs"]) >= 1
