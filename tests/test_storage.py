from uuid import uuid4

import pytest

from backend.services.storage import create_application_record, get_application, init_db, update_application


@pytest.mark.asyncio
async def test_storage_crud():
    await init_db()
    app_id = str(uuid4())
    payload = {"application_id": app_id, "status": "created"}
    await create_application_record(app_id, payload, "created")
    data = await get_application(app_id)
    assert data is not None
    assert data["status"] == "created"

    payload["status"] = "updated"
    await update_application(app_id, payload, "updated")
    data = await get_application(app_id)
    assert data["status"] == "updated"
