"""Minimal Orchestrator Campaign API (spec-first, TDD slice).

Spec quotes implemented:
- specs/functional.md: "Campaigns can be created via a single API call ... and are persisted in PostgreSQL"
- specs/functional.md: "Pause or kill a campaign instantly if something goes wrong"
"""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.core.campaign_store import CampaignRecord, build_campaign_store


Platform = Literal["twitter", "instagram", "threads", "tiktok", "youtube"]


class CampaignCreateRequest(BaseModel):
    name: str = Field(..., min_length=3)
    goal: str = Field(..., min_length=8)
    budget: float = Field(..., gt=0)
    time_window_hours: int = Field(..., ge=1)
    target_platforms: list[Platform] = Field(..., min_length=1)


class CampaignResponse(BaseModel):
    id: str
    name: str
    goal: str
    budget: float
    time_window_hours: int
    target_platforms: list[str]
    status: Literal["active", "paused", "killed"]
    created_at: str
    updated_at: str


class CampaignListResponse(BaseModel):
    campaigns: list[CampaignResponse]


app = FastAPI(title="Chimera Orchestrator API")

_store = None
_store_key: tuple[str, str] | None = None


def _current_store_key() -> tuple[str, str]:
    from os import getenv

    backend = getenv("CHIMERA_CAMPAIGN_DB_BACKEND", "postgres").lower()
    locator = (
        getenv("POSTGRES_URL", "")
        if backend == "postgres"
        else getenv("CHIMERA_CAMPAIGN_SQLITE_PATH", "/tmp/chimera_campaigns.db")
    )
    return backend, locator


def _get_store():
    global _store
    global _store_key
    key = _current_store_key()
    if _store is None or key != _store_key:
        _store = build_campaign_store()
        _store_key = key
    return _store


def _to_response(record: CampaignRecord) -> CampaignResponse:
    return CampaignResponse(
        id=record.id,
        name=record.name,
        goal=record.goal,
        budget=record.budget,
        time_window_hours=record.time_window_hours,
        target_platforms=record.target_platforms,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@app.post("/campaigns", response_model=CampaignResponse, status_code=201)
def create_campaign(payload: CampaignCreateRequest) -> CampaignResponse:
    record = _get_store().create_campaign(
        name=payload.name,
        goal=payload.goal,
        budget=payload.budget,
        time_window_hours=payload.time_window_hours,
        target_platforms=payload.target_platforms,
    )
    return _to_response(record)


@app.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: str) -> CampaignResponse:
    record = _get_store().get_campaign(campaign_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return _to_response(record)


@app.get("/campaigns", response_model=CampaignListResponse)
def list_campaigns() -> CampaignListResponse:
    records = _get_store().list_campaigns()
    return CampaignListResponse(campaigns=[_to_response(record) for record in records])


@app.post("/campaigns/{campaign_id}/pause", response_model=CampaignResponse)
def pause_campaign(campaign_id: str) -> CampaignResponse:
    store = _get_store()
    existing = store.get_campaign(campaign_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if existing.status == "killed":
        raise HTTPException(status_code=409, detail="Killed campaigns cannot be paused")
    updated = store.update_status(campaign_id, "paused")
    if updated is None:
        raise HTTPException(status_code=500, detail="Failed to pause campaign")
    return _to_response(updated)


@app.post("/campaigns/{campaign_id}/kill", response_model=CampaignResponse)
def kill_campaign(campaign_id: str) -> CampaignResponse:
    updated = _get_store().update_status(campaign_id, "killed")
    if updated is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return _to_response(updated)
