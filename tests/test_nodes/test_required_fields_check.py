import pytest

from backend.agent.nodes.resume_required_fields_check import resume_required_fields_check_node


@pytest.mark.asyncio
async def test_required_fields_missing_email():
    state = {
        "parsed_resume": {
            "name": "a",
            "date_of_birth": "1999",
            "gender": "male",
            "email": None,
            "phone": "1",
            "experiences": ["x"],
            "skills": ["python"],
            "education": ["u"],
        },
        "status": "",
    }
    await resume_required_fields_check_node(state)
    assert state["resume_required_fields_complete"] is False
    assert "email" in state["missing_required_resume_fields"]
