import os
from pathlib import Path
import pytest
from backend.agent.graph import initial_state, run_until_interrupt_or_end
from backend.services.pdf_service import PdfParseError, parse_pdf_bytes

FIXTURES = Path(__file__).parent.parent / "demo-fixtures" / "resumes"


def test_pdf_parse_demo_success():
    pdf = FIXTURES / "resume_success.pdf"
    if not pdf.exists():
        pytest.skip("fixture not found")
    text = parse_pdf_bytes(pdf.read_bytes())
    assert len(text) > 10


def test_pdf_parse_damaged():
    # Empty bytes produce no text after fallback decode → PdfParseError
    with pytest.raises(PdfParseError):
        parse_pdf_bytes(b"")


@pytest.mark.asyncio
async def test_e2e_real_pdf_happy():
    pdf = FIXTURES / "resume_success.pdf"
    if not pdf.exists():
        pytest.skip("fixture not found")
    state = initial_state(pdf.read_bytes())
    state = await run_until_interrupt_or_end(state)
    assert state["status"] in ("waiting_job_selection", "required_resume_fields_missing_waiting_reupload")


@pytest.mark.asyncio
async def test_e2e_real_pdf_match_failed():
    pdf = FIXTURES / "resume_match_failed.pdf"
    if not pdf.exists():
        pytest.skip("fixture not found")
    state = initial_state(pdf.read_bytes())
    state = await run_until_interrupt_or_end(state)
    assert state["final_result"] == "rejected"
    assert state["failure_type"] == "MATCH_FAILED"
