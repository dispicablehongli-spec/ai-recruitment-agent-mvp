from copy import deepcopy
from uuid import uuid4

from backend.agent.edges import next_after_match, next_after_required_fields
from backend.agent.nodes.error_node import error_node
from backend.agent.nodes.final_rejection import final_rejection_node
from backend.agent.nodes.interview_invitation import interview_invitation_node
from backend.agent.nodes.job_selection import job_selection_node
from backend.agent.nodes.match_jobs import match_jobs_node
from backend.agent.nodes.pdf_parse import pdf_parse_node
from backend.agent.nodes.reupload_request import resume_reupload_request_node
from backend.agent.nodes.resume_extract import resume_extract_node
from backend.agent.nodes.resume_required_fields_check import resume_required_fields_check_node
from backend.agent.nodes.resume_reupload import resume_reupload_node
from backend.agent.nodes.success import success_node
from backend.services.job_service import get_all_jobs


def initial_state(pdf_bytes: bytes, use_demo_jobs: bool = False, use_real_llm: bool = False) -> dict:
    return {
        "application_id": str(uuid4()),
        "pdf_bytes": pdf_bytes,
        "resume_text": "",
        "parsed_resume": {},
        "all_jobs": get_all_jobs(use_demo_jobs),
        "all_match_results": [],
        "qualified_jobs": [],
        "selected_job_id": None,
        "resume_required_fields_complete": False,
        "missing_required_resume_fields": [],
        "resume_quality_warnings": [],
        "reupload_suggestions": [],
        "resume_reupload_count": 0,
        "max_resume_reupload_count": 2,
        "total_upload_count": 1,
        "max_total_upload_count": 5,
        "status": "created",
        "status_message": "",
        "logs": [],
        "errors": [],
        "final_result": None,
        "failure_type": None,
        "final_failure_reason": None,
        "user_cancelled": False,
        "use_real_llm": use_real_llm,
    }


async def run_until_interrupt_or_end(state: dict) -> dict:
    state = deepcopy(state)
    try:
        if state.get("final_result"):
            return state

        if state.get("status") == "required_resume_fields_missing_waiting_reupload":
            return state
        if state.get("status") == "waiting_job_selection" and not state.get("selected_job_id"):
            return state

        # Resume after job selection: skip re-parsing (pdf_bytes was cleared at storage time)
        if state.get("status") == "waiting_job_selection" and state.get("selected_job_id"):
            await interview_invitation_node(state)
            await success_node(state)
            return state

        await pdf_parse_node(state)
        if state.get("final_result"):
            return state
        await resume_extract_node(state)
        await resume_required_fields_check_node(state)
        branch = next_after_required_fields(state)
        if branch == "reupload_request":
            await resume_reupload_request_node(state)
            return state

        await match_jobs_node(state)
        if next_after_match(state) == "final_rejection":
            state["failure_type"] = "MATCH_FAILED"
            await final_rejection_node(state)
            return state

        await job_selection_node(state)
        if state["status"] == "waiting_job_selection":
            return state

        await interview_invitation_node(state)
        await success_node(state)
        return state
    except Exception as err:
        return await error_node(state, err)


async def apply_reupload(state: dict, pdf_bytes: bytes) -> dict:
    state = deepcopy(state)
    state["pdf_bytes"] = pdf_bytes
    await resume_reupload_node(state)
    if state["resume_reupload_count"] > state["max_resume_reupload_count"]:
        state["failure_type"] = "RESUME_REQUIRED_FIELDS_MISSING"
        return await final_rejection_node(state)
    return await run_until_interrupt_or_end(state)


async def apply_cancel(state: dict) -> dict:
    state = deepcopy(state)
    state["user_cancelled"] = True
    state["failure_type"] = "USER_CANCELLED"
    return await final_rejection_node(state)


async def apply_job_selection(state: dict, job_id: str) -> dict:
    state = deepcopy(state)
    state["selected_job_id"] = job_id
    return await run_until_interrupt_or_end(state)
