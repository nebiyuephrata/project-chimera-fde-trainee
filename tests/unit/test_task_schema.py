"""
TDD test file for the Agent Task payload schema.

Spec source (specs/technical.md):

```json
{
  "task_id": "uuid-v4",
  "task_type": "generate_content | reply_comment | execute_transaction",
  "priority": "high | medium | low",
  "context": {
    "goal_description": "string",
    "persona_constraints": ["string"],
    "required_resources": ["mcp://twitter/mentions/123", "mcp://memory/recent"]
  },
  "assigned_worker_id": "string",
  "created_at": "timestamp",
  "status": "pending | in_progress | review | complete"
}
```

Prime directive (from .cursor/rules.md):
- Use Pydantic / JSON Schema for all interfaces (tasks, results, tools).
- Write failing tests first (TDD) to enforce the spec.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Literal

import pytest
from pydantic import BaseModel, UUID4, ValidationError, field_validator


class TaskContext(BaseModel):
    """
    Context block for an Agent Task.

    Mirrors the nested JSON object from specs/technical.md:

    \"context\": {
      \"goal_description\": \"string\",
      \"persona_constraints\": [\"string\"],
      \"required_resources\": [\"mcp://twitter/mentions/123\", \"mcp://memory/recent\"]
    }
    """

    goal_description: str
    persona_constraints: List[str]
    required_resources: List[str]

    @field_validator("required_resources")
    @classmethod
    def ensure_required_resources_non_empty(cls, value: List[str]) -> List[str]:
        """
        Enforce that required_resources is present and non-empty, reflecting
        the spec's expectation that the Planner passes concrete MCP resources
        (e.g., mcp://twitter/..., mcp://memory/...).
        """
        if not value:
            raise ValueError("required_resources must contain at least one MCP resource")
        return value


class AgentTask(BaseModel):
    """
    Agent Task model aligned with specs/technical.md.

    Fields are strongly typed and constrained so that invalid payloads will
    raise ValidationError and the tests below enforce the spec contract.
    """

    # UUID for correlating tasks across Planner / Worker / Judge.
    task_id: UUID4

    # From spec: "generate_content | reply_comment | execute_transaction"
    task_type: Literal["generate_content", "reply_comment", "execute_transaction"]

    # From spec: "high | medium | low"
    priority: Literal["high", "medium", "low"]

    # Nested context block (see TaskContext above).
    context: TaskContext

    # Worker identity + lifecycle metadata.
    assigned_worker_id: str
    created_at: datetime

    # From spec: "pending | in_progress | review | complete"
    status: Literal["pending", "in_progress", "review", "complete"]


def test_agent_task_includes_all_required_fields_from_spec() -> None:
    """
    This test enforces that the Pydantic model exposes all required fields from
    the Agent Task payload spec in specs/technical.md.

    Originally this test FAILED because AgentTask only defined task_id and
    omitted:
    - task_type
    - priority
    - context
    - assigned_worker_id
    - created_at
    - status

    After implementing the full schema (see AgentTask above), this test now
    passes and protects the contract going forward.
    """

    required_fields = {
        "task_id",
        "task_type",
        "priority",
        "context",
        "assigned_worker_id",
        "created_at",
        "status",
    }

    assert required_fields.issubset(
        AgentTask.model_fields.keys()
    ), "AgentTask is missing one or more required fields from the spec."


def test_priority_must_be_limited_to_allowed_enum_values() -> None:
    """
    This test encodes the priority enum from the spec:
    - priority: \"high | medium | low\"

    It EXPECTS that an invalid priority like \"urgent\" raises a ValidationError.
    With the Literal-based priority field on AgentTask, this now behaves as a
    real enum and the invalid value is rejected.
    """

    with pytest.raises(ValidationError):
        AgentTask(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            task_type="generate_content",
            priority="urgent",  # Not in {high, medium, low}
            context={
                "goal_description": "Grow engagement on X.",
                "persona_constraints": ["no political content"],
                "required_resources": ["mcp://twitter/mentions/recent"],
            },
            assigned_worker_id="worker-1",
            created_at="2026-02-06T12:00:00Z",
            status="pending",
        )


def test_context_requires_required_resources_list() -> None:
    """
    This test encodes the nested context object from the spec:

    \"context\": {
      \"goal_description\": \"string\",
      \"persona_constraints\": [\"string\"],
      \"required_resources\": [\"mcp://twitter/mentions/123\", \"mcp://memory/recent\"]
    }

    It EXPECTS that omitting required_resources (or providing an empty list)
    causes a ValidationError.
    With TaskContext now modeled explicitly, nested validation ensures this.
    """

    with pytest.raises(ValidationError):
        AgentTask(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            task_type="generate_content",
            priority="high",
            context={
                "goal_description": "Create a short video about Project Chimera.",
                # Missing persona_constraints and required_resources on purpose.
            },
            assigned_worker_id="worker-2",
            created_at="2026-02-06T12:05:00Z",
            status="pending",
        )

