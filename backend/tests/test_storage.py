import asyncio
import os
import pytest

from backend.services.storage import (
    create_application,
    get_application,
    init_db,
    set_final,
    update_status,
)


@pytest.fixture(autouse=True)
def use_tmp_db(tmp_path, monkeypatch):
    """Redirect the database to a temp directory for each test."""
    from backend import config as cfg

    original = cfg.get_settings.cache_clear  # type: ignore[attr-defined]
    cfg.get_settings.cache_clear()

    # Patch data_dir on the cached settings instance after clearing cache
    settings = cfg.get_settings()
    monkeypatch.setattr(settings, "data_dir", tmp_path)

    yield

    cfg.get_settings.cache_clear()


def run(coro):  # tiny helper so tests stay readable
    return asyncio.get_event_loop().run_until_complete(coro)


def test_create_and_get():
    run(init_db())
    app_id = run(create_application())
    record = run(get_application(app_id))
    assert record is not None
    assert record["id"] == app_id
    assert record["status"] == "pending"


def test_update_status():
    run(init_db())
    app_id = run(create_application())
    run(update_status(app_id, "processing"))
    record = run(get_application(app_id))
    assert record["status"] == "processing"


def test_set_final_success():
    run(init_db())
    app_id = run(create_application())
    run(set_final(app_id, "success"))
    record = run(get_application(app_id))
    assert record["final_result"] == "success"
    assert record["status"] == "done"
    assert record["failure_type"] is None


def test_set_final_with_failure_type():
    run(init_db())
    app_id = run(create_application())
    run(set_final(app_id, "rejected", failure_type="MATCH_FAILED"))
    record = run(get_application(app_id))
    assert record["final_result"] == "rejected"
    assert record["failure_type"] == "MATCH_FAILED"
