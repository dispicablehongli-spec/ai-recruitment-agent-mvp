import os
import pytest


def test_llm_chat_returns_ok_json() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key.startswith("your-") or os.getenv("RUN_REAL_LLM_TESTS") != "1":
        pytest.skip("real llm test disabled")

    from backend.llm.client import chat

    result = chat('Return the JSON {"ok": true}', response_format={"type": "json_object"})
    assert "ok" in result, f"Expected 'ok' in response, got: {result}"
