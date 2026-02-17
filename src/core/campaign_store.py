"""Campaign persistence for Orchestrator APIs.

Spec quotes implemented:
- specs/functional.md: "Campaigns can be created via a single API call ... and are persisted in PostgreSQL"
- specs/functional.md: "Pause or kill a campaign instantly if something goes wrong"
"""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4


CampaignStatus = Literal["active", "paused", "killed"]


@dataclass
class CampaignRecord:
    id: str
    name: str
    goal: str
    budget: float
    time_window_hours: int
    target_platforms: list[str]
    status: CampaignStatus
    created_at: str
    updated_at: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_record(raw: dict[str, object]) -> CampaignRecord:
    return CampaignRecord(
        id=str(raw["id"]),
        name=str(raw["name"]),
        goal=str(raw["goal"]),
        budget=float(raw["budget"]),
        time_window_hours=int(raw["time_window_hours"]),
        target_platforms=list(json.loads(str(raw["target_platforms"]))),
        status=str(raw["status"]),  # type: ignore[assignment]
        created_at=str(raw["created_at"]),
        updated_at=str(raw["updated_at"]),
    )


class SQLiteCampaignStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS campaigns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    budget REAL NOT NULL,
                    time_window_hours INTEGER NOT NULL,
                    target_platforms TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def create_campaign(
        self,
        *,
        name: str,
        goal: str,
        budget: float,
        time_window_hours: int,
        target_platforms: list[str],
    ) -> CampaignRecord:
        campaign_id = str(uuid4())
        now = _now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO campaigns (
                    id, name, goal, budget, time_window_hours, target_platforms,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    campaign_id,
                    name,
                    goal,
                    budget,
                    time_window_hours,
                    json.dumps(target_platforms),
                    "active",
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        return _normalize_record(dict(row))

    def get_campaign(self, campaign_id: str) -> Optional[CampaignRecord]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        if row is None:
            return None
        return _normalize_record(dict(row))

    def list_campaigns(self) -> list[CampaignRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM campaigns ORDER BY created_at DESC"
            ).fetchall()
        return [_normalize_record(dict(row)) for row in rows]

    def update_status(self, campaign_id: str, status: CampaignStatus) -> Optional[CampaignRecord]:
        now = _now_iso()
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
            if row is None:
                return None
            conn.execute(
                "UPDATE campaigns SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, campaign_id),
            )
            updated = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        return _normalize_record(dict(updated))


class PostgresCampaignStore:
    def __init__(self, dsn: str) -> None:
        try:
            import psycopg
        except Exception as exc:  # pragma: no cover - exercised only in postgres runtime
            raise RuntimeError(
                "PostgreSQL backend requires psycopg. Install with `pip install psycopg[binary]`."
            ) from exc
        self._psycopg = psycopg
        self.dsn = dsn
        self._ensure_schema()

    def _connect(self):
        return self._psycopg.connect(self.dsn)

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS campaigns (
                        id UUID PRIMARY KEY,
                        name TEXT NOT NULL,
                        goal TEXT NOT NULL,
                        budget NUMERIC(20, 6) NOT NULL,
                        time_window_hours INTEGER NOT NULL,
                        target_platforms JSONB NOT NULL,
                        status TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL,
                        updated_at TIMESTAMPTZ NOT NULL
                    )
                    """
                )

    def create_campaign(
        self,
        *,
        name: str,
        goal: str,
        budget: float,
        time_window_hours: int,
        target_platforms: list[str],
    ) -> CampaignRecord:
        campaign_id = str(uuid4())
        now = _now_iso()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO campaigns (
                        id, name, goal, budget, time_window_hours, target_platforms,
                        status, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s)
                    """,
                    (
                        campaign_id,
                        name,
                        goal,
                        budget,
                        time_window_hours,
                        json.dumps(target_platforms),
                        "active",
                        now,
                        now,
                    ),
                )
                cur.execute(
                    """
                    SELECT id::text, name, goal, budget::float8, time_window_hours,
                           target_platforms::text, status, created_at::text, updated_at::text
                    FROM campaigns WHERE id = %s
                    """,
                    (campaign_id,),
                )
                row = cur.fetchone()
                columns = [d[0] for d in cur.description]
        return _normalize_record(dict(zip(columns, row)))

    def get_campaign(self, campaign_id: str) -> Optional[CampaignRecord]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id::text, name, goal, budget::float8, time_window_hours,
                           target_platforms::text, status, created_at::text, updated_at::text
                    FROM campaigns WHERE id = %s
                    """,
                    (campaign_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                columns = [d[0] for d in cur.description]
        return _normalize_record(dict(zip(columns, row)))

    def list_campaigns(self) -> list[CampaignRecord]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id::text, name, goal, budget::float8, time_window_hours,
                           target_platforms::text, status, created_at::text, updated_at::text
                    FROM campaigns
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
                columns = [d[0] for d in cur.description]
        return [_normalize_record(dict(zip(columns, row))) for row in rows]

    def update_status(self, campaign_id: str, status: CampaignStatus) -> Optional[CampaignRecord]:
        now = _now_iso()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE campaigns SET status = %s, updated_at = %s WHERE id = %s",
                    (status, now, campaign_id),
                )
                if cur.rowcount == 0:
                    return None
                cur.execute(
                    """
                    SELECT id::text, name, goal, budget::float8, time_window_hours,
                           target_platforms::text, status, created_at::text, updated_at::text
                    FROM campaigns WHERE id = %s
                    """,
                    (campaign_id,),
                )
                row = cur.fetchone()
                columns = [d[0] for d in cur.description]
        return _normalize_record(dict(zip(columns, row)))


def build_campaign_store() -> SQLiteCampaignStore | PostgresCampaignStore:
    backend = os.getenv("CHIMERA_CAMPAIGN_DB_BACKEND", "postgres").lower()
    if backend == "postgres":
        dsn = os.getenv(
            "POSTGRES_URL",
            "postgresql://chimera:chimera@localhost:5432/chimera",
        )
        return PostgresCampaignStore(dsn=dsn)
    db_path = os.getenv("CHIMERA_CAMPAIGN_SQLITE_PATH", "/tmp/chimera_campaigns.db")
    return SQLiteCampaignStore(db_path=db_path)
