from __future__ import annotations

from skills.generate_content import GenerateContentInput, generate_content


def test_generate_content_returns_candidate() -> None:
    payload = GenerateContentInput(
        goal_description="Draft a short update",
        persona_id="persona-1",
        target_platforms=["twitter"],
    )
    output = generate_content(payload)
    assert output.candidates, "Expected at least one candidate"
