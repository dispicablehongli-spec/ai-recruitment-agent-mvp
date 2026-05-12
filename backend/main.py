from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.applications import _startup, router as applications_router
from backend.api.jobs import router as jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _startup()
    yield


app = FastAPI(title="AI Recruitment Agent MVP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications_router, prefix="/applications", tags=["applications"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
