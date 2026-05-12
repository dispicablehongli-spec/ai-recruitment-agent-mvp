import asyncio
import json
from collections.abc import AsyncGenerator

event_queues: dict[str, asyncio.Queue] = {}


async def push_event(application_id: str, event: dict) -> None:
    queue = event_queues.setdefault(application_id, asyncio.Queue())
    await queue.put(event)


async def subscribe_events(application_id: str) -> AsyncGenerator[str, None]:
    queue = event_queues.setdefault(application_id, asyncio.Queue())
    try:
        while True:
            event = await queue.get()
            yield f"event: status_update\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"
    finally:
        if queue.empty():
            event_queues.pop(application_id, None)
