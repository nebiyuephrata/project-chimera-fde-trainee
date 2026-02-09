from __future__ import annotations

import os

from fastapi.testclient import TestClient

os.environ["HITL_USE_MEMORY"] = "1"

from src.api.hitl_api import app  # noqa: E402


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_tasks() -> None:
    response = client.get("/hitl/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 1


def test_update_task() -> None:
    tasks = client.get("/hitl/tasks").json()["tasks"]
    task_id = tasks[0]["task_id"]
    response = client.post(f"/hitl/{task_id}/approve")
    assert response.status_code == 200
    assert response.json()["task"]["status"] == "approved"
