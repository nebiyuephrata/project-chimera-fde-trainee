"""
TDD stubs for Runtime Skill interfaces.

Specs referenced:
- `.cursor/rules.md` §3 & §10: Runtime Agent Skills must use Pydantic / JSON Schema interfaces.
- `specs/functional.md` Agent-Level stories:
  - Trend fetching, content generation, and posting.
- `specs/technical.md`: Strongly typed JSON payloads.

This file intentionally contains a **failing** test for the `trend_fetch` input
schema: the model defined here is incomplete and does not yet enforce the
required `query` field. Future work should move these schemas into a proper
`skills/` module and make this test pass.
"""

from __future__ import annotations

from typing import List, Optional

import pytest
from pydantic import BaseModel, ValidationError


class TrendFetchInput(BaseModel):
    """
    INCOMPLETE schema for the `trend_fetch` skill input.

    According to `skills/README.md` and the functional spec, the input
    MUST contain:
    - query: string
    - locale: string
    - time_window_minutes: int

    For TDD purposes, this model is intentionally missing the `query` field,
    so the test below will FAIL until the schema is brought in line with the
    documented contract.
    """

    # NOTE: `query` is intentionally omitted here.
    locale: str
    time_window_minutes: int
    platform_hints: Optional[List[str]] = None


def test_trend_fetch_requires_query_field() -> None:
    """
    From `skills/README.md` (skills/trend_fetch/input):
    - `query` is a required field.

    This test encodes that contract by expecting a ValidationError when
    `query` is missing from the payload. Right now it FAILS because the
    TrendFetchInput model does not declare `query` at all, so instantiating
    it without `query` does not raise.
    """

    with pytest.raises(ValidationError):
        TrendFetchInput(
            locale="en-US",
            time_window_minutes=60,
            platform_hints=["twitter"],
        )

