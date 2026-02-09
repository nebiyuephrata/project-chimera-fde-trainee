from __future__ import annotations

from skills.post_content import PostContentInput, post_content


def test_post_content_dry_run_is_simulated() -> None:
    payload = PostContentInput(
        content_id="candidate-1",
        platform="twitter",
        dry_run=True,
    )
    output = post_content(payload)
    assert output.status == "simulated"
