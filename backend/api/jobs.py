from fastapi import APIRouter

from backend.services.job_service import get_all_jobs

router = APIRouter()


@router.get("")
async def list_jobs() -> list[dict]:
    return get_all_jobs()
