"""
High-level interface tests for runtime skills in `skills/`.

Specs referenced:
- `.cursor/rules.md` §3 & §10 – Runtime Agent Skills must use Pydantic / JSON Schema.
- `skills/README.md` – contracts for `trend_fetch`, `generate_content`, `post_content`.
- `specs/functional.md` – Agent-level stories for trends, content generation, posting.

Purpose:
- Assert that skills modules expose the expected call signatures and Pydantic
  models as per the spec.
- These tests are deliberately **TDD-failing** for skills that are not yet
  implemented (e.g., generate_content, post_content).
"""

from __future__ import annotations

import inspect

from skills import trend_fetch as trend_fetch_skill


def test_trend_fetch_skill_signature_uses_pydantic_models() -> None:
    """
    From `skills/README.md` §1 (`trend_fetch` Skill):
    - Input: skills/trend_fetch/input
    - Output: skills/trend_fetch/output

    This test asserts that:
    - `trend_fetch` is callable.
    - It takes a single positional parameter (the input model).
    - It has a return annotation corresponding to the output model.
    """

    fn = getattr(trend_fetch_skill, "trend_fetch", None)
    assert callable(fn), "trend_fetch skill function must be defined"

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    # Expect exactly one input parameter besides `self`/`cls` (plain function).
    assert len(params) == 1

    # Check that type hints are present; exact type matching can be tightened later.
    assert params[0].annotation is not inspect._empty
    assert sig.return_annotation is not inspect._empty


def test_generate_content_skill_module_and_interface_exist() -> None:
    """
    From `skills/README.md` §2 (`generate_content` Skill):
    - Requires Pydantic input/output models and a callable `generate_content`.

    This test is intentionally written to FAIL until the `skills/generate_content`
    module is created with the correct interface.
    """

    # Importing this module will currently FAIL because it does not exist yet.
    import skills.generate_content as generate_content_skill  # type: ignore[import]  # noqa: F401

    assert hasattr(
        generate_content_skill, "generate_content"
    ), "generate_content() must be defined on skills.generate_content"


def test_post_content_skill_module_and_interface_exist() -> None:
    """
    From `skills/README.md` §3 (`post_content` Skill):
    - Requires Pydantic input/output models and a callable `post_content`.

    This test is intentionally written to FAIL until the `skills/post_content`
    module is created with the correct interface.
    """

    import skills.post_content as post_content_skill  # type: ignore[import]  # noqa: F401

    assert hasattr(
        post_content_skill, "post_content"
    ), "post_content() must be defined on skills.post_content"
