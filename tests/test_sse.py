import pytest

from backend.api.sse import event_queues, push_event


@pytest.mark.asyncio
async def test_push_event_creates_queue():
    await push_event("abc", {"status": "x"})
    assert "abc" in event_queues
