from fastapi import FastAPI

from backend.api.applications import router as applications_router
from backend.api.jobs import router as jobs_router

app = FastAPI(title="AI Recruitment Agent MVP")
app.include_router(applications_router, prefix="/applications", tags=["applications"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
