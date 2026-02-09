"""Database configuration helpers (local/dev)."""

from __future__ import annotations

import os


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


POSTGRES_URL = get_env("POSTGRES_URL", "postgresql://chimera:chimera@localhost:5432/chimera")
REDIS_URL = get_env("REDIS_URL", "redis://localhost:6379/0")
WEAVIATE_URL = get_env("WEAVIATE_URL", "http://localhost:8080")
