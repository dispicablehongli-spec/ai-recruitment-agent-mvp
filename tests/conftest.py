import asyncio
import os

import pytest


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def has_openai_key():
    return bool(os.getenv('OPENAI_API_KEY'))
