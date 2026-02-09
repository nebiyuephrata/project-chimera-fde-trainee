"""Minimal FastRender Swarm demo: planner -> worker -> judge."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TaskContext(BaseModel):
    goal_description: str
    persona_constraints: list[str] = Field(default_factory=list)
    required_resources: list[str] = Field(default_factory=list)


class TaskPayload(BaseModel):
    task_id: str
    task_type: Literal["generate_content", "reply_comment", "execute_transaction"]
    priority: Literal["high", "medium", "low"]
    context: TaskContext
    assigned_worker_id: str
    created_at: str
    status: Literal["pending", "in_progress", "review", "complete"]


def planner(goal: str) -> list[TaskPayload]:
    """Decompose a natural language goal into a task list."""
    now = datetime.utcnow().isoformat()
    base_context = TaskContext(
        goal_description=goal,
        persona_constraints=["brand_safe", "informative"],
        required_resources=["mcp://memory/recent"],
    )
    tasks = [
        TaskPayload(
            task_id=str(uuid.uuid4()),
            task_type="generate_content",
            priority="high",
            context=base_context,
            assigned_worker_id="worker-1",
            created_at=now,
            status="pending",
        ),
        TaskPayload(
            task_id=str(uuid.uuid4()),
            task_type="reply_comment",
            priority="medium",
            context=base_context,
            assigned_worker_id="worker-1",
            created_at=now,
            status="pending",
        ),
    ]
    return tasks


MCP_REGISTRY: dict[str, dict[str, object]] = {
    "trend_fetch": {"status": 200, "data": "AI creator tools are rising this week."},
    "generate_image": {"status": 200, "data": "image://placeholder.png"},
}


def mcp_call(payload: dict[str, object]) -> dict[str, object]:
    """Mock MCP call via registry lookup."""
    skill = payload.get("skill")
    response = MCP_REGISTRY.get(str(skill), {"status": 404, "data": "Not found"})
    return {"status": response["status"], "data": response["data"], "skill": skill}


def worker(task: TaskPayload, queue: list[TaskPayload]) -> str | None:
    """Execute a task using mocked MCP."""
    payload = {
        "skill": "trend_fetch",
        "input": task.context.model_dump(),
        "task_id": task.task_id,
    }
    print("MCP payload:", json.dumps(payload, indent=2))
    response = mcp_call(payload)
    print("MCP response:", json.dumps(response, indent=2))

    if response["status"] == 500:
        task.status = "pending"
        queue.append(task)
        return None

    trend = response["data"]
    return (
        f"Task {task.task_id} ({task.task_type}) -> "
        f"{task.context.goal_description}. Trend: {trend}"
    )


def judge(result: str) -> dict[str, object]:
    """Score the result and decide approval."""
    confidence = 0.8 if "Trend:" in result else 0.4
    approved = confidence >= 0.7
    reason = "Meets minimum confidence threshold" if approved else "Low confidence"
    return {"approved": approved, "reason": reason, "confidence": confidence}


def main() -> None:
    goal = "Create a short campaign update about creator trends."
    tasks = planner(goal)

    task_store: dict[str, TaskPayload] = {task.task_id: task for task in tasks}
    result_store: dict[str, str] = {}

    queue = [task for task in task_store.values() if task.status == "pending"]
    pending = queue.pop(0)
    pending.status = "in_progress"

    result = worker(pending, queue)
    if result is None:
        print("Task re-queued due to MCP error.")
        return
    result_store[pending.task_id] = result
    pending.status = "review"

    verdict = judge(result)
    pending.status = "complete" if verdict["approved"] else "review"

    output = {
        "goal": goal,
        "task": pending.model_dump(),
        "result": result,
        "verdict": verdict,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
