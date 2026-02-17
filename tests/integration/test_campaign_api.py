from __future__ import annotations

import os
from pathlib import Path

from fastapi.testclient import TestClient


# Spec quotes implemented by this test module:
# - specs/functional.md: "Campaigns can be created via a single API call ... and are persisted in PostgreSQL"
# - specs/functional.md: "Create and manage multi-step campaigns ..."
# - specs/functional.md: "Pause or kill a campaign instantly if something goes wrong"


def _build_client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "campaigns.db"
    os.environ["CHIMERA_CAMPAIGN_DB_BACKEND"] = "sqlite"
    os.environ["CHIMERA_CAMPAIGN_SQLITE_PATH"] = str(db_path)

    from src.api.orchestrator_api import app

    return TestClient(app)


def test_create_campaign_single_api_call_persists_record(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    payload = {
        "name": "Launch Creator Sprint",
        "goal": "Ship a 7-day cross-platform creator campaign.",
        "budget": 250.0,
        "time_window_hours": 72,
        "target_platforms": ["twitter", "instagram", "threads"],
    }

    create_response = client.post("/campaigns", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()

    fetch_response = client.get(f"/campaigns/{created['id']}")
    assert fetch_response.status_code == 200
    fetched = fetch_response.json()

    assert fetched["id"] == created["id"]
    assert fetched["name"] == payload["name"]
    assert fetched["goal"] == payload["goal"]
    assert fetched["budget"] == payload["budget"]
    assert fetched["status"] == "active"


def test_pause_then_kill_campaign_updates_status(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    create_response = client.post(
        "/campaigns",
        json={
            "name": "Crisis Hold",
            "goal": "Pause or stop campaign if policy risk appears.",
            "budget": 120.0,
            "time_window_hours": 24,
            "target_platforms": ["twitter"],
        },
    )
    campaign_id = create_response.json()["id"]

    pause_response = client.post(f"/campaigns/{campaign_id}/pause")
    assert pause_response.status_code == 200
    assert pause_response.json()["status"] == "paused"

    kill_response = client.post(f"/campaigns/{campaign_id}/kill")
    assert kill_response.status_code == 200
    assert kill_response.json()["status"] == "killed"


def test_get_unknown_campaign_returns_404(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/campaigns/not-a-real-id")
    assert response.status_code == 404


def test_list_campaigns_returns_created_campaigns(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    client.post(
        "/campaigns",
        json={
            "name": "Campaign A",
            "goal": "Run creator growth test A.",
            "budget": 50.0,
            "time_window_hours": 12,
            "target_platforms": ["twitter"],
        },
    )
    client.post(
        "/campaigns",
        json={
            "name": "Campaign B",
            "goal": "Run creator growth test B.",
            "budget": 80.0,
            "time_window_hours": 24,
            "target_platforms": ["instagram"],
        },
    )

    response = client.get("/campaigns")
    assert response.status_code == 200
    data = response.json()
    assert "campaigns" in data
    assert len(data["campaigns"]) == 2
    names = {item["name"] for item in data["campaigns"]}
    assert names == {"Campaign A", "Campaign B"}
