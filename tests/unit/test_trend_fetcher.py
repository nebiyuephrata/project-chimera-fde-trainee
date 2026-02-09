"""
Tests for the `trend_fetch` runtime skill.

Specs referenced:
- `skills/README.md` §1 `trend_fetch` – input/output JSON Schemas and acceptance criteria.
- `specs/functional.md` – Agent-level story: "Fetch real-time trends via MCP Resources..."
- `specs/technical.md` – Pydantic / JSON Schema for all interfaces.

Purpose:
- Assert that the trend data structure matches the API contract.
- This test is written **TDD-first** and is expected to FAIL initially
  as the implementation is still evolving.
"""

from __future__ import annotations

from typing import Iterable

from skills.trend_fetch import TrendFetchInput, TrendFetchOutput, TrendItem, trend_fetch


def _all_items(iterable: Iterable[TrendItem]) -> list[TrendItem]:
    return list(iterable)


def test_trend_fetcher_output_matches_contract_and_minimum_count() -> None:
    """
    Contract checks derived from `skills/README.md`:

    Input (skills/trend_fetch/input):
    - required: ["query", "locale", "time_window_minutes"]

    Output (skills/trend_fetch/output):
    - required: ["trends", "query", "generated_at"]
    - trends[*].required: ["title", "relevance", "source_uri"]
    - relevance: number in [0.0, 1.0], with spec note that >= 0.75 is required.

    This test asserts:
    - The call returns a TrendFetchOutput.
    - At least **three** TrendItem objects are returned (stronger acceptance
      criterion for the Planner than the base spec).
    - All trends have relevance in [0.0, 1.0] and >= 0.75.
    - All source_uri values look like MCP handles (start with "mcp://").

    NOTE: The current stub implementation only returns two trends, so this test
    is expected to FAIL until the implementation is extended to satisfy the
    stronger contract.
    """

    input_payload = TrendFetchInput(
        query="AI agents",
        locale="en-US",
        time_window_minutes=60,
        platform_hints=["twitter"],
    )

    result = trend_fetch(input_payload)

    # Basic type and echo checks
    assert isinstance(result, TrendFetchOutput)
    assert result.query == input_payload.query

    trends = _all_items(result.trends)

    # Stronger contract: Planner expects a richer set of trends (>= 3).
    assert len(trends) >= 3

    for t in trends:
        assert isinstance(t, TrendItem)
        assert isinstance(t.title, str) and t.title
        assert isinstance(t.summary, str) and t.summary
        assert 0.0 <= t.relevance <= 1.0
        # Spec note from skills/README.md §1.3: planner should only see >= 0.75.
        assert t.relevance >= 0.75
        # Spec note: source_uri should be an MCP resource handle, not raw HTTP.
        assert t.source_uri.startswith("mcp://")
