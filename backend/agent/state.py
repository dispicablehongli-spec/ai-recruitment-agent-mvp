from __future__ import annotations

from typing import TypedDict

from backend.llm.schemas import MatchResult


class GraphState(TypedDict):
    application_id: str
    pdf_bytes: bytes
    resume_text: str
    parsed_resume: dict
    all_jobs: list[dict]
    all_match_results: list[MatchResult]
    qualified_jobs: list[dict]
    selected_job_id: str | None
    resume_required_fields_complete: bool
    missing_required_resume_fields: list[str]
    resume_quality_warnings: list[str]
    reupload_suggestions: list[str]
    resume_reupload_count: int
    max_resume_reupload_count: int
    total_upload_count: int
    max_total_upload_count: int
    status: str
    status_message: str
    logs: list[str]
    errors: list[str]
    final_result: str | None
    failure_type: str | None
    final_failure_reason: str | None
    user_cancelled: bool
