import pytest

from backend.llm.client import LLMClient, LLMRetryExhaustedError


@pytest.mark.asyncio
async def test_retry_exhausted(monkeypatch):
    client = LLMClient()

    async def fail_chat(_: str) -> str:
        raise TimeoutError("boom")

    monkeypatch.setattr(client, "_chat", fail_chat)
    with pytest.raises(LLMRetryExhaustedError):
        await client.chat_json("x")
