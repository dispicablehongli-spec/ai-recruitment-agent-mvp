import os

import pytest

from backend.llm.client import get_llm_client


@pytest.mark.asyncio
async def test_llm_client_smoke(has_openai_key):
    if not has_openai_key or os.getenv("RUN_REAL_LLM_TESTS") != "1":
        pytest.skip("real llm test is disabled")
    data = await get_llm_client().chat_json('Return {"ok": true}')
    assert data.get("ok") is True
