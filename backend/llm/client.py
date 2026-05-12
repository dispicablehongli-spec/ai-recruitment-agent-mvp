from __future__ import annotations

import asyncio
import json
from functools import lru_cache
from typing import Any

from openai import AsyncOpenAI, OpenAI

from backend.config import get_settings


class LLMRetryExhaustedError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _get_sync_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)


@lru_cache(maxsize=1)
def _get_async_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)


def chat(prompt: str, response_format: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    client = _get_sync_client()
    kwargs: dict[str, Any] = {"model": settings.openai_model, "messages": [{"role": "user", "content": prompt}]}
    if response_format is not None:
        kwargs["response_format"] = response_format
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


class LLMClient:
    def __init__(self) -> None:
        self._client = None
        self._model = get_settings().openai_model

    async def _chat(self, prompt: str) -> str:
        if self._client is None:
            self._client = _get_async_client()
        response = await self._client.responses.create(model=self._model, input=prompt)
        return response.output_text

    async def chat_json(self, prompt: str) -> dict[str, Any]:
        net_retry = 3
        json_retry = 1
        waits = [1, 2, 4]
        net_attempt = 0
        while True:
            try:
                text = await self._chat(prompt)
                try:
                    return json.loads(text)
                except Exception as exc:
                    if json_retry <= 0:
                        raise LLMRetryExhaustedError("json validation failed") from exc
                    json_retry -= 1
                    return json.loads(await self._chat(prompt))
            except LLMRetryExhaustedError:
                raise
            except Exception as exc:
                if net_attempt >= net_retry:
                    raise LLMRetryExhaustedError("network retries exhausted") from exc
                await asyncio.sleep(waits[net_attempt])
                net_attempt += 1


_CLIENT: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = LLMClient()
    return _CLIENT
