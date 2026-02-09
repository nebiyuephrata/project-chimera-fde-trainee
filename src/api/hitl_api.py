"""Minimal HITL API with REST + WebSocket (in-memory)."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class HitlTask(BaseModel):
    task_id: str
    snippet: str
    confidence: float
    reason: str
    timestamp: str
    status: Literal["pending", "approved", "rejected", "editing"] = "pending"


class HitlUpdate(BaseModel):
    status: Literal["approved", "rejected", "editing"]
    editor_note: str | None = None


app = FastAPI(title="Chimera HITL API")

_tasks: Dict[str, HitlTask] = {}
_task_order: List[str] = []
_connections: List[WebSocket] = []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _seed_tasks() -> None:
    if _tasks:
        return
    seed = [
        HitlTask(
            task_id="task-api-1",
            snippet="Generated summary for creator campaign launch.",
            confidence=0.62,
            reason="Low confidence: factual accuracy",
            timestamp=_now_iso(),
        ),
        HitlTask(
            task_id="task-api-2",
            snippet="Reply to brand partner comment pending tone check.",
            confidence=0.73,
            reason="Borderline tone alignment",
            timestamp=_now_iso(),
        ),
    ]
    for task in seed:
        _tasks[task.task_id] = task
        _task_order.append(task.task_id)


async def _broadcast(message: dict[str, Any]) -> None:
    if not _connections:
        return
    data = message | {"timestamp": _now_iso()}
    for ws in list(_connections):
        try:
            await ws.send_json(data)
        except Exception:
            _connections.remove(ws)


@app.get("/hitl/tasks")
def get_hitl_tasks() -> dict[str, list[HitlTask]]:
    _seed_tasks()
    tasks = [_tasks[task_id] for task_id in _task_order]
    return {"tasks": tasks}


@app.post("/hitl/{task_id}/{action}")
async def update_task(task_id: str, action: str, payload: HitlUpdate | None = None) -> dict[str, HitlTask]:
    _seed_tasks()
    task = _tasks.get(task_id)
    if task is None:
        return {
            "task": HitlTask(
                task_id=task_id,
                snippet="Unknown task",
                confidence=0.0,
                reason="Not found",
                timestamp=_now_iso(),
                status="rejected",
            )
        }

    if action not in {"approve", "reject", "edit"}:
        return {"task": task}

    status_map = {"approve": "approved", "reject": "rejected", "edit": "editing"}
    task.status = status_map[action]
    _tasks[task_id] = task
    await _broadcast({"type": "task.update", "payload": task.model_dump()})
    return {"task": task}


@app.websocket("/hitl")
async def hitl_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    _connections.append(websocket)
    _seed_tasks()
    for task_id in _task_order:
        await websocket.send_json({"type": "task.new", "payload": _tasks[task_id].model_dump()})
        await asyncio.sleep(0.5)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        _connections.remove(websocket)
