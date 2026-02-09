"""Mock WebSocket server for HITL queue updates."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

import websockets


TASKS = [
    {
        "task_id": "task-ws-1",
        "snippet": "Drafted post on creator economy trends.",
        "confidence": 0.61,
        "reason": "Low confidence: factual accuracy",
        "timestamp": "",
        "status": "pending",
    },
    {
        "task_id": "task-ws-2",
        "snippet": "Reply to brand partner comment.",
        "confidence": 0.73,
        "reason": "Tone alignment check",
        "timestamp": "",
        "status": "pending",
    },
    {
        "task_id": "task-ws-3",
        "snippet": "Summary of sponsor pricing changes.",
        "confidence": 0.58,
        "reason": "Requires legal review",
        "timestamp": "",
        "status": "pending",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def handle_connection(websocket: Any) -> None:
    for task in TASKS:
        task = {**task, "timestamp": now_iso()}
        message = {"type": "task.new", "payload": task}
        await websocket.send(json.dumps(message))
        await asyncio.sleep(3)


async def main() -> None:
    async with websockets.serve(handle_connection, "0.0.0.0", 8000, ping_interval=20):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
