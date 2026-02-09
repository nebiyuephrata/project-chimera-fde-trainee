"""
Runtime skill: generate_content

Spec references:
- skills/README.md §2 `generate_content` – input/output JSON Schemas and acceptance criteria
- specs/functional.md – Agent-level story: "Generate multimodal content via MCP Tools"
- specs/technical.md – Pydantic / JSON Schema for all interfaces

Placeholder implementation: returns mock candidates. No real MCP call yet.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class GenerateContentConstraints(BaseModel):
    """Optional constraints block from skills/README.md §2.1."""

    max_length_tokens: Optional[int] = Field(None, ge=32, le=4096)
    no_sensitive_topics: Optional[bool] = None


class GenerateContentInput(BaseModel):
    """
    Pydantic mirror of skills/generate_content/input (skills/README.md §2.1).

    Required: goal_description, persona_id, target_platforms.
    Optional: trend_ids, constraints.
    """

    goal_description: str = Field(..., description="High-level campaign or post goal.")
    persona_id: str = Field(..., description="Identifier mapping to SOUL.md and persona embedding.")
    target_platforms: List[Literal["twitter", "instagram", "tiktok", "threads", "youtube"]] = Field(
        ...,
        min_length=1,
        description="Target platforms for the content.",
    )
    trend_ids: Optional[List[str]] = Field(
        default=None,
        description="IDs or URIs of trends from trend_fetch.",
    )
    constraints: Optional[GenerateContentConstraints] = None


class SafetyFlags(BaseModel):
    """Safety flags per skills/README.md §2.2 candidate schema."""

    requires_hitl: bool = False
    policy_violations: List[str] = Field(default_factory=list)


class ContentCandidate(BaseModel):
    """Single candidate from generate_content output (skills/README.md §2.2)."""

    id: str
    modality: Literal["text", "image", "video"]
    body: str
    safety_flags: SafetyFlags = Field(default_factory=SafetyFlags)


class GenerateContentOutput(BaseModel):
    """
    Pydantic mirror of skills/generate_content/output (skills/README.md §2.2).

    Required: persona_id, candidates (minItems: 1).
    """

    persona_id: str
    candidates: List[ContentCandidate] = Field(..., min_length=1)


def generate_content(input: GenerateContentInput) -> GenerateContentOutput:
    """
    Placeholder implementation of the generate_content runtime skill.

    Returns mock candidates. No real MCP call yet.
    Per spec §2.3: at least one candidate MUST be produced per call.
    """

    return GenerateContentOutput(
        persona_id=input.persona_id,
        candidates=[
            ContentCandidate(
                id="mock-candidate-1",
                modality="text",
                body="Mock post body aligned with persona.",
                safety_flags=SafetyFlags(requires_hitl=False, policy_violations=[]),
            ),
        ],
    )
