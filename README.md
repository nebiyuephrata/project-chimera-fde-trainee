# Project Chimera – FDE Trainee Submission

Spec-driven architecture for Autonomous AI Influencers using MCP, FastRender Swarm, Agentic Commerce (Coinbase AgentKit), and TDD governance.

**Trainee:** Ephrata Nebiyu  
**Assessment:** 10 Academy / Tenacious FDE Trainee Challenge  
**Date:** February 2026

## Overview
Robust, traceable engineering environment for autonomous influencers — perception (MCP), reasoning (Swarm), content generation, engagement, economic agency.

Role: Lead Architect & Governor (spec-first, no vibe coding).

## Core Principles
- Spec-Driven Development (SDD)
- Traceability via Tenx MCP Sense
- Hierarchical FastRender Swarm (Planner → Worker → Judge)
- HITL, confidence scoring, budget controls, OCC
- Dockerized, Makefile, CI/CD, failing TDD tests

## Structure
project-chimera-fde-trainee/
├── .cursor/                      # Cursor IDE rules & context (critical for spec enforcement)
│   └── rules.md
├── .github/                      # CI/CD & workflows
│   └── workflows/
│       └── ci.yml                # Lint, test, spec-check on push
├── docs/                         # Research, decisions, diagrams (Day 1–2)
│   ├── research-summary.md
│   ├── architecture_strategy.md
│   └── diagrams/                 # Mermaid exports or draw.io files (optional)
├── infra/                        # Infrastructure as Code (Docker, Makefile, Helm later)
│   ├── Dockerfile
│   ├── Makefile
│   ├── docker-compose.yml        # Local dev (Redis, Weaviate, MCP servers)
│   └── k8s/                      # Future Kubernetes manifests (stub for now)
├── mcp-config/                   # MCP-specific configs & servers
│   ├── tooling_strategy.md       # Dev vs Runtime separation
│   └── servers/                  # Custom MCP server stubs (e.g., news_server.py)
├── scripts/                      # Utility scripts (setup, bootstrap, validate-specs)
│   └── bootstrap.sh              # One-click env setup
├── skills/                       # Runtime Agent Skills (interfaces & impl)
│   ├── README.md
│   ├── trend_fetch/
│   ├── generate_content/
│   └── post_content/
├── specs/                        # Source of truth — GitHub Spec Kit style
│   ├── _meta.md                  # Vision, constraints, glossary
│   ├── functional.md             # User stories & acceptance criteria
│   ├── technical.md              # Schemas, DB ERD, API contracts
│   ├── openclaw_integration.md   # Optional agent social network plan
│   └── soul.md                   # Example agent persona (one per agent type)
├── src/                          # Core application code (services)
│   ├── __init__.py
│   ├── planner/                  # Planner service
│   ├── worker/                   # Worker pool
│   ├── judge/                    # Judge & governance
│   ├── orchestrator/             # Central control plane
│   ├── core/                     # Shared utils, schemas, MCP client
│   └── commerce/                 # Agentic Commerce logic (Coinbase AgentKit)
├── tests/                        # TDD failing tests first
│   ├── unit/
│   ├── integration/
│   └── test_task_schema.py       # Example failing test stub
├── .env.example                  # Env vars template (no secrets)
├── .gitignore
├── pyproject.toml                # uv / Poetry / modern Python config
├── README.md                     # Your current one (updated below)
└── requirements-dev.txt          # Optional if not using pyproject.toml.

## Current Status (Day 2 – Feb 06, 2026)
- specs/ bootstrapped (_meta, functional, technical)
- .cursor/rules.md enforcing spec-first behavior
- Next: Populate skills/, tooling_strategy.md, initial failing tests

## Setup
```bash
make setup          # Install deps (uv sync)
make test           # Run failing tests (TDD)
make spec-check     # Validate code vs specs (custom script later)
```