from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

import aiosqlite

from backend.config import get_settings

_DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id          TEXT PRIMARY KEY,
    status      TEXT NOT NULL DEFAULT 'pending',
    final_result TEXT,
    failure_type TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""


def _db_path() -> Path:
    return get_settings().data_dir / "applications.db"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def init_db() -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.executescript(_DB_SCHEMA)
        await db.commit()


async def create_application() -> str:
    app_id = str(uuid.uuid4())
    now = _now()
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "INSERT INTO applications (id, status, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (app_id, "pending", now, now),
        )
        await db.commit()
    return app_id


async def create_application_record(application_id: str, payload: dict[str, Any], status: str) -> None:
    now = _now()
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "INSERT OR REPLACE INTO applications (id, status, final_result, failure_type, created_at, updated_at) VALUES (?, ?, NULL, NULL, ?, ?)",
            (application_id, status, now, now),
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS application_payloads (id TEXT PRIMARY KEY, payload_json TEXT NOT NULL)"
        )
        await db.execute(
            "INSERT OR REPLACE INTO application_payloads (id, payload_json) VALUES (?, ?)",
            (application_id, json.dumps(payload, ensure_ascii=False)),
        )
        await db.commit()


async def get_application(app_id: str) -> dict[str, Any] | None:
    async with aiosqlite.connect(_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            result = dict(row)
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS application_payloads (id TEXT PRIMARY KEY, payload_json TEXT NOT NULL)"
        )
        async with db.execute("SELECT payload_json FROM application_payloads WHERE id = ?", (app_id,)) as cursor:
            payload_row = await cursor.fetchone()
            payload = json.loads(payload_row[0]) if payload_row else {}
    return {
        "id": result["id"],
        "application_id": result["id"],
        "status": result["status"],
        "final_result": result["final_result"],
        "failure_type": result["failure_type"],
        "payload": payload,
    }


async def update_status(app_id: str, status: str) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "UPDATE applications SET status = ?, updated_at = ? WHERE id = ?",
            (status, _now(), app_id),
        )
        await db.commit()


async def set_final(
    app_id: str,
    final_result: str,
    failure_type: str | None = None,
) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "UPDATE applications SET final_result = ?, failure_type = ?, status = 'done', updated_at = ? WHERE id = ?",
            (final_result, failure_type, _now(), app_id),
        )
        await db.commit()


async def update_application(
    application_id: str,
    payload: dict[str, Any],
    status: str,
    final_result: str | None = None,
    failure_type: str | None = None,
) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "UPDATE applications SET status = ?, final_result = ?, failure_type = ?, updated_at = ? WHERE id = ?",
            (status, final_result, failure_type, _now(), application_id),
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS application_payloads (id TEXT PRIMARY KEY, payload_json TEXT NOT NULL)"
        )
        await db.execute(
            "INSERT OR REPLACE INTO application_payloads (id, payload_json) VALUES (?, ?)",
            (application_id, json.dumps(payload, ensure_ascii=False)),
        )
        await db.commit()
