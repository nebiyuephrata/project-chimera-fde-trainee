"""
Runtime skill: post_content

Spec references:
- skills/README.md §3 `post_content` – input/output JSON Schemas and acceptance criteria
- specs/functional.md – Agent-level story: "Publish content & reply to engagement via MCP Tools"
- specs/technical.md – Pydantic / JSON Schema for all interfaces

Placeholder implementation: returns mock status. No real MCP call yet.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class PostContentInput(BaseModel):
    """
    Pydantic mirror of skills/post_content/input (skills/README.md §3.1).

    Required: content_id, platform, dry_run.
    Optional: scheduled_for, judge_approval_id.
    """

    content_id: str = Field(..., description="Identifier of a candidate from generate_content.")
    platform: Literal["twitter", "instagram", "tiktok", "threads", "youtube"] = Field(
        ...,
        description="Target platform.",
    )
    dry_run: bool = Field(
        ...,
        description="If true, simulate posting and return a mock receipt.",
    )
    scheduled_for: Optional[datetime] = Field(
        default=None,
        description="Optional scheduling time; immediate if omitted.",
    )
    judge_approval_id: Optional[str] = Field(
        default=None,
        description="Reference to a Judge verdict that approved this content.",
    )


class PostContentOutput(BaseModel):
    """
    Pydantic mirror of skills/post_content/output (skills/README.md §3.2).

    Required: content_id, platform, dry_run, status.
    Optional: provider_post_id, error.
    """

    content_id: str
    platform: str
    dry_run: bool
    status: Literal["scheduled", "posted", "simulated", "failed"]
    provider_post_id: Optional[str] = None
    error: Optional[str] = None


def post_content(input: PostContentInput) -> PostContentOutput:
    """
    Placeholder implementation of the post_content runtime skill.

    Returns mock status. No real MCP call yet.
    Per spec §3.3: when dry_run is true, status MUST be "simulated".
    """

    status: Literal["scheduled", "posted", "simulated", "failed"] = (
        "simulated" if input.dry_run else "posted"
    )
    provider_post_id = None if input.dry_run else "mock-provider-id-123"

    return PostContentOutput(
        content_id=input.content_id,
        platform=input.platform,
        dry_run=input.dry_run,
        status=status,
        provider_post_id=provider_post_id,
    )
