import json
from pathlib import Path
from typing import Any

from backend.config import get_settings


def _load(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_all_jobs(use_demo: bool = False) -> list[dict[str, Any]]:
    settings = get_settings()
    filename = "jobs.demo.json" if use_demo else "jobs.json"
    return _load(settings.data_dir / filename)
