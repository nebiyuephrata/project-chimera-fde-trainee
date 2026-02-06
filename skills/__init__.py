"""
Runtime skills package for Project Chimera.

Spec references:
- `.cursor/rules.md` §3 & §10 – strict separation between Developer MCP tools and
  Runtime Agent Skills, and mandatory Pydantic / JSON Schema interfaces.
- `skills/README.md` – contracts for trend_fetch, generate_content, post_content.

This package exposes skill modules under `skills.*` so that tests and the
runtime can import them as regular Python packages.
"""

from __future__ import annotations

# Public re-exports for convenience (optional, may expand as skills are added).
from . import trend_fetch  # noqa: F401

