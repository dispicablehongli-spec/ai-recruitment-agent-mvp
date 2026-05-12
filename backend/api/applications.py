from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from backend.agent.graph import (
    apply_cancel,
    apply_job_selection,
    apply_reupload,
    initial_state,
    run_until_interrupt_or_end,
)
from backend.api.sse import push_event, subscribe_events
from backend.services.storage import (
    create_application_record,
    get_application,
    init_db,
    update_application,
)

router = APIRouter()


async def _startup() -> None:
    await init_db()


def _application_payload(state: dict[str, Any]) -> dict[str, Any]:
    payload = dict(state)
    payload["pdf_bytes"] = ""
    payload["all_match_results"] = [
        item.model_dump() if hasattr(item, "model_dump") else item for item in payload.get("all_match_results", [])
    ]
    return payload


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, str]:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only pdf is supported")
    pdf_bytes = await file.read()
    state = initial_state(pdf_bytes)
    await create_application_record(state["application_id"], _application_payload(state), "created")
    state = await run_until_interrupt_or_end(state)
    await update_application(
        state["application_id"],
        _application_payload(state),
        state["status"],
        state.get("final_result"),
        state.get("failure_type"),
    )
    await push_event(state["application_id"], {"status": state["status"], "message": "state updated"})
    return {"application_id": state["application_id"], "status": state["status"]}


@router.get("/{application_id}")
async def get_snapshot(application_id: str) -> dict[str, Any]:
    app = await get_application(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="application not found")
    return app


@router.get("/{application_id}/events")
async def events(application_id: str) -> StreamingResponse:
    return StreamingResponse(subscribe_events(application_id), media_type="text/event-stream")


@router.post("/{application_id}/select-job")
async def select_job(application_id: str, payload: dict[str, str]) -> dict[str, Any]:
    app = await get_application(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="application not found")
    state = await apply_job_selection(app["payload"], payload["job_id"])
    await update_application(application_id, _application_payload(state), state["status"], state.get("final_result"), state.get("failure_type"))
    await push_event(application_id, {"status": state["status"], "message": "job selected"})
    return {"status": state["status"], "final_result": state.get("final_result")}


@router.post("/{application_id}/reupload")
async def reupload_resume(application_id: str, file: UploadFile = File(...)) -> dict[str, Any]:
    app = await get_application(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="application not found")
    if app["status"] != "required_resume_fields_missing_waiting_reupload":
        raise HTTPException(status_code=409, detail="state does not allow reupload")
    state = await apply_reupload(app["payload"], await file.read())
    await update_application(application_id, _application_payload(state), state["status"], state.get("final_result"), state.get("failure_type"))
    await push_event(application_id, {"status": state["status"], "message": "resume reuploaded"})
    return {
        "status": state["status"],
        "resume_reupload_count": state["resume_reupload_count"],
        "max_resume_reupload_count": state["max_resume_reupload_count"],
    }


@router.post("/{application_id}/cancel")
async def cancel(application_id: str) -> dict[str, Any]:
    app = await get_application(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="application not found")
    if app["status"] != "required_resume_fields_missing_waiting_reupload":
        raise HTTPException(status_code=409, detail="state does not allow cancel")
    state = await apply_cancel(app["payload"])
    await update_application(application_id, _application_payload(state), state["status"], state.get("final_result"), state.get("failure_type"))
    await push_event(application_id, {"status": "user_cancelled_terminated", "message": "user cancelled"})
    return {"application_id": application_id, "status": "user_cancelled_terminated", "failure_type": "USER_CANCELLED"}


@router.get("/{application_id}/result")
async def get_result(application_id: str) -> dict[str, Any]:
    app = await get_application(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="application not found")
    return {
        "application_id": application_id,
        "final_result": app["final_result"],
        "failure_type": app["failure_type"],
        "status": app["status"],
    }
