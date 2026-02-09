"""
TDD stubs for Runtime Skill interfaces.

Specs referenced:
- `.cursor/rules.md` §3 & §10: Runtime Agent Skills must use Pydantic / JSON Schema interfaces.
- `specs/functional.md` Agent-Level stories:
  - Trend fetching, content generation, and posting.
- `specs/technical.md`: Strongly typed JSON payloads.

Uses the canonical TrendFetchInput from skills.trend_fetch, which enforces
the required `query` field per skills/README.md §1.1.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from skills.trend_fetch import TrendFetchInput


def test_trend_fetch_requires_query_field() -> None:
    """
    From `skills/README.md` (skills/trend_fetch/input):
    - `query` is a required field.

    This test encodes that contract by expecting a ValidationError when
    `query` is missing from the payload. Uses the canonical TrendFetchInput
    from skills.trend_fetch, which enforces this requirement.
    """

    with pytest.raises(ValidationError):
        TrendFetchInput(
            locale="en-US",
            time_window_minutes=60,
            platform_hints=["twitter"],
        )

