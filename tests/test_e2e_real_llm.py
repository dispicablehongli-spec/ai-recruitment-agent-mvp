import pytest


@pytest.mark.skip(reason="requires real OpenAI key and fixtures")
def test_e2e_real_llm_placeholder():
    assert True
