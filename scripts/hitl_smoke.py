"""Smoke test for HITL API + WebSocket."""

from __future__ import annotations

import asyncio
import json

import requests
import websockets


API_BASE = "http://localhost:8000"
WS_URL = "ws://localhost:8000/hitl"


def seed_and_update() -> None:
    tasks = requests.get(f"{API_BASE}/hitl/tasks", timeout=5).json()["tasks"]
    task_id = tasks[0]["task_id"]
    requests.post(f"{API_BASE}/hitl/{task_id}/approve", timeout=5)


async def listen_ws() -> None:
    async with websockets.connect(WS_URL) as ws:
        for _ in range(3):
            msg = await ws.recv()
            print("WS:", msg)


def main() -> None:
    seed_and_update()
    asyncio.run(listen_ws())


if __name__ == "__main__":
    main()
