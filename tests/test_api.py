from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app


@pytest.mark.asyncio
async def test_basic_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        health = await client.get("/health")
        assert health.status_code == 200
        jobs = await client.get("/jobs")
        assert jobs.status_code == 200
        assert len(jobs.json()) >= 1


@pytest.mark.asyncio
async def test_upload_and_result():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        files = {"file": ("resume.pdf", BytesIO(b"%PDF-1.4\npython fastapi sql"), "application/pdf")}
        response = await client.post("/applications/upload", files=files)
        assert response.status_code == 200
        app_id = response.json()["application_id"]
        snapshot = await client.get(f"/applications/{app_id}")
        assert snapshot.status_code == 200
