"""Minimal HITL API with REST + WebSocket (Redis-backed, in-memory fallback)."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Literal, Optional

import redis
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
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


@dataclass
class InMemoryStore:
    tasks: Dict[str, HitlTask] = field(default_factory=dict)
    order: List[str] = field(default_factory=list)

    def seed(self, seed: Iterable[HitlTask]) -> None:
        if self.tasks:
            return
        for task in seed:
            self.tasks[task.task_id] = task
            self.order.append(task.task_id)

    def list_tasks(self) -> list[HitlTask]:
        return [self.tasks[task_id] for task_id in self.order]

    def get_task(self, task_id: str) -> Optional[HitlTask]:
        return self.tasks.get(task_id)

    def update_status(self, task_id: str, status: str) -> Optional[HitlTask]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = status
        self.tasks[task_id] = task
        return task


@dataclass
class RedisStore:
    client: redis.Redis
    list_key: str = "hitl:tasks"
    task_prefix: str = "hitl:task:"

    def seed(self, seed: Iterable[HitlTask]) -> None:
        if self.client.llen(self.list_key) > 0:
            return
        for task in seed:
            self.client.rpush(self.list_key, task.task_id)
            self.client.set(self.task_prefix + task.task_id, task.model_dump_json())

    def list_tasks(self) -> list[HitlTask]:
        task_ids = self.client.lrange(self.list_key, 0, -1)
        tasks: list[HitlTask] = []
        for task_id in task_ids:
            raw = self.client.get(self.task_prefix + task_id)
            if raw:
                tasks.append(HitlTask.model_validate_json(raw))
        return tasks

    def get_task(self, task_id: str) -> Optional[HitlTask]:
        raw = self.client.get(self.task_prefix + task_id)
        if not raw:
            return None
        return HitlTask.model_validate_json(raw)

    def update_status(self, task_id: str, status: str) -> Optional[HitlTask]:
        task = self.get_task(task_id)
        if not task:
            return None
        task.status = status
        self.client.set(self.task_prefix + task_id, task.model_dump_json())
        if status in {"approved", "rejected"}:
            self.client.lrem(self.list_key, 0, task_id)
        elif status == "editing":
            self.client.lrem(self.list_key, 0, task_id)
            self.client.rpush(self.list_key, task_id)
        return task


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _seed_tasks() -> list[HitlTask]:
    return [
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


def _build_store() -> InMemoryStore | RedisStore:
    if os.getenv("HITL_USE_MEMORY", "").lower() in {"1", "true", "yes"}:
        return InMemoryStore()
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(redis_url, decode_responses=True)
    return RedisStore(client=client)


def _ensure_seed(store: InMemoryStore | RedisStore) -> None:
    store.seed(_seed_tasks())


app = FastAPI(title="Chimera HITL API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)

_connections: List[WebSocket] = []
_store = _build_store()


async def _broadcast(message: dict[str, Any]) -> None:
    if not _connections:
        return
    data = message | {"timestamp": _now_iso()}
    for ws in list(_connections):
        try:
            await ws.send_json(data)
        except Exception:
            _connections.remove(ws)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hitl/tasks")
def get_hitl_tasks() -> dict[str, list[HitlTask]]:
    _ensure_seed(_store)
    tasks = _store.list_tasks()
    return {"tasks": tasks}


@app.post("/hitl/{task_id}/{action}")
async def update_task(task_id: str, action: str, _payload: HitlUpdate | None = None) -> dict[str, HitlTask]:
    _ensure_seed(_store)
    task = _store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if action not in {"approve", "reject", "edit"}:
        raise HTTPException(status_code=400, detail="Invalid action")

    status_map = {"approve": "approved", "reject": "rejected", "edit": "editing"}
    updated = _store.update_status(task_id, status_map[action])
    if updated is None:
        raise HTTPException(status_code=500, detail="Failed to update task")
    await _broadcast({"type": "task.update", "payload": updated.model_dump()})
    return {"task": updated}


@app.websocket("/hitl")
async def hitl_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    _connections.append(websocket)
    _ensure_seed(_store)
    for task in _store.list_tasks():
        await websocket.send_json({"type": "task.new", "payload": task.model_dump()})
        await asyncio.sleep(0.5)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        _connections.remove(websocket)
