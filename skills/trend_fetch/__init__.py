"""
Runtime skill: trend_fetch

Spec references:
- skills/README.md §1 `trend_fetch` – input/output JSON Schemas and acceptance criteria
- specs/functional.md – Agent-level story: "Fetch real-time trends via MCP Resources..."
- specs/technical.md – general requirement to use Pydantic / JSON Schema for interfaces

This module provides a Pydantic-first interface for the `trend_fetch` skill and a
mock implementation that returns hardcoded trends. It is intentionally MCP-agnostic
for now; real MCP calls will be wired in later.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class TrendFetchInput(BaseModel):
    """
    Pydantic mirror of the `skills/trend_fetch/input` JSON Schema from skills/README.md.

    Required fields (see skills/README.md lines 21–40):
    - query: string
    - locale: string (BCP-47 or region code, e.g., "en-US", "global")
    - time_window_minutes: integer in [5, 1440]
    Optional:
    - platform_hints: list of strings (e.g., ["twitter", "tiktok"])
    """

    query: str = Field(..., description="High-level topic to search trends for.")
    locale: str = Field(..., description="BCP-47 locale or region code, e.g. 'en-US'.")
    time_window_minutes: int = Field(
        ...,
        ge=5,
        le=1440,
        description="Lookback window for trends in minutes.",
    )
    platform_hints: Optional[List[str]] = Field(
        default=None,
        description="Optional list of platform hints, e.g. ['twitter', 'tiktok'].",
    )


class TrendItem(BaseModel):
    """
    Single trend item, as defined in the `skills/trend_fetch/output` schema
    (skills/README.md lines 54–86).

    - title: string
    - summary: string
    - relevance: float in [0.0, 1.0]; spec requires >= 0.75 for returned items
    - source_uri: string, typically an MCP resource handle (e.g. 'mcp://news/top/123')
    """

    title: str
    summary: str
    relevance: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score; >= 0.75 will be enforced by callers per spec.",
    )
    source_uri: str = Field(
        ...,
        description="MCP resource handle, e.g. 'mcp://news/top/123'.",
    )


class TrendFetchOutput(BaseModel):
    """
    Pydantic mirror of `skills/trend_fetch/output` (skills/README.md lines 54–88).

    Required fields:
    - query: echo of the input query
    - generated_at: ISO 8601 timestamp
    - trends: list[TrendItem]
    """

    query: str
    generated_at: datetime
    trends: List[TrendItem]


def trend_fetch(input: TrendFetchInput) -> TrendFetchOutput:
    """
    Placeholder implementation of the `trend_fetch` runtime skill.

    For now this function:
    - DOES NOT call any real MCP server or external API.
    - Returns a hardcoded list of trend items that conform to the output schema.
    - Uses relevance scores >= 0.75 to respect the spec's acceptance criteria
      (skills/README.md §1.3).

    This structure is suitable for unit tests and for later replacement with a
    real MCP-backed implementation.
    """

    now = datetime.now(timezone.utc)

    # Hardcoded, spec-conforming mock trends.
    mock_trends: List[TrendItem] = [
        TrendItem(
            title="AI agents orchestrating social campaigns",
            summary="Discussion around autonomous agents coordinating brand campaigns.",
            relevance=0.9,
            source_uri="mcp://news/top/ai-agents-1",
        ),
        TrendItem(
            title="On-chain influencer economies",
            summary="Emerging patterns of creators using crypto-native revenue models.",
            relevance=0.82,
            source_uri="mcp://news/top/onchain-creators-2",
        ),
    ]

    return TrendFetchOutput(
        query=input.query,
        generated_at=now,
        trends=mock_trends,
    )

