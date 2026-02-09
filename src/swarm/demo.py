"""Minimal FastRender Swarm demo: planner -> worker -> judge."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from threading import Event, Thread
from typing import Literal

import redis
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


def worker(client: redis.Redis, task_queue: str, results_queue: str) -> TaskPayload | None:
    """Pop a task, call mocked MCP, push result to results queue."""
    raw_task = client.lpop(task_queue)
    if raw_task is None:
        return None
    task = TaskPayload.model_validate_json(raw_task)
    task.status = "in_progress"

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
        client.rpush(task_queue, task.model_dump_json())
        return None

    trend = response["data"]
    result = (
        f"Task {task.task_id} ({task.task_type}) -> "
        f"{task.context.goal_description}. Trend: {trend}"
    )
    task.status = "review"
    client.rpush(results_queue, json.dumps({"task": task.model_dump(), "result": result}))
    return task


def judge(result: str) -> dict[str, object]:
    """Score the result and decide approval."""
    confidence = 0.8 if "Trend:" in result else 0.4
    approved = confidence >= 0.7
    reason = "Meets minimum confidence threshold" if approved else "Low confidence"
    return {"approved": approved, "reason": reason, "confidence": confidence}


def load_hitl_queue(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_hitl_queue(path: Path, queue: list[dict[str, object]]) -> None:
    path.write_text(json.dumps(queue, indent=2), encoding="utf-8")


def enqueue_hitl(path: Path, payload: dict[str, object]) -> None:
    queue = load_hitl_queue(path)
    queue.append(payload)
    save_hitl_queue(path, queue)


def hitl_moderator(path: Path, result_box: dict[str, str], done: Event) -> None:
    queue = load_hitl_queue(path)
    if not queue:
        result_box["decision"] = "approve"
        done.set()
        return
    item = queue.pop(0)
    decision = "approve" if item.get("confidence", 0) >= 0.6 else "reject"
    save_hitl_queue(path, queue)
    result_box["decision"] = decision
    done.set()


def main() -> None:
    goal = "Create a short campaign update about creator trends."
    tasks = planner(goal)
    redis_url = "redis://localhost:6379/0"
    client = redis.Redis.from_url(redis_url, decode_responses=True)
    task_queue = "swarm:tasks"
    results_queue = "swarm:results"
    judged_queue = "swarm:judged"

    for task in tasks:
        client.rpush(task_queue, task.model_dump_json())

    pending = worker(client, task_queue, results_queue)
    if pending is None:
        print("No task processed (empty queue or MCP error).")
        return

    raw_result = client.lpop(results_queue)
    if raw_result is None:
        print("No results to judge.")
        return
    result_item = json.loads(raw_result)
    result = result_item["result"]
    verdict = judge(result)
    pending.status = "complete" if verdict["approved"] else "review"
    hitl_path = Path("hitl_queue.json")
    decision = None
    if verdict["confidence"] < 0.7:
        enqueue_hitl(
            hitl_path,
            {"task_id": pending.task_id, "result": result, "confidence": verdict["confidence"]},
        )
        decision_box: dict[str, str] = {}
        done = Event()
        Thread(target=hitl_moderator, args=(hitl_path, decision_box, done), daemon=True).start()
        if done.wait(timeout=0.2):
            decision = decision_box.get("decision")
            pending.status = "complete" if decision == "approve" else "review"

    client.rpush(
        judged_queue,
        json.dumps({"task_id": pending.task_id, "status": pending.status, "verdict": verdict}),
    )

    output = {
        "goal": goal,
        "task": pending.model_dump(),
        "result": result,
        "verdict": verdict,
        "hitl_decision": decision or "pending",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
