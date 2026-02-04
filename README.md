# Project Chimera – Forward Deployed Engineer (FDE) Trainee Assessment

**Repository for the 10 Academy / Tenacious FDE Trainee Challenge**  
**Date:** February 2026  
**Trainee:** Ephrata Nebiyu

## Overview

This repository contains my submission for the **Project Chimera: The Agentic Infrastructure Challenge**.

Project Chimera is an autonomous influencer network — a system that creates and operates persistent, goal-directed AI influencers capable of researching trends, generating multimodal content (text, images, video), engaging audiences across social platforms, and even managing economic transactions via non-custodial wallets (Coinbase AgentKit).

My role as **Forward Deployed Engineer (FDE) Trainee** is to act as the **Lead Architect and Governor** — not to rapidly prototype, but to build a **robust, spec-driven, traceable, and agent-ready engineering environment** that a swarm of AI agents could later use to implement features with minimal human intervention.

## Core Principles Demonstrated

- **Spec-Driven Development (SDD)** — All implementation follows ratified specifications (specs/ directory)
- **Traceability** — Connected to Tenx MCP Sense throughout development
- **Agentic Orchestration** — Hierarchical FastRender Swarm (Planner → Worker → Judge)
- **Governance & Safety** — Human-in-the-Loop (HITL), confidence scoring, budget controls, OCC
- **Infrastructure as Code** — Dockerized environment, Makefile, CI/CD pipeline, failing TDD tests
- **Tool Separation** — Developer MCP tools vs runtime Agent Skills

## Repository Structure
project-chimera-fde-trainee/
├── README.md                  # Project overview, your role, submission links, how to run/setup
├── docs/                      # Research & decisions (Day 1 focus)
│   ├── research-summary.md    # Key insights from readings (a16z, OpenClaw/MoltBook, SRS Qs)
│   └── architecture_strategy.md # Agent pattern, HITL placement, DB choice, why + Mermaid diagram
├── specs/                     # Empty for now — populate Day 2 with GitHub Spec Kit files
│   ├── _meta.md               # (stub: high-level vision/constraints placeholder)
│   ├── functional.md          # (stub: placeholder user stories)
│   └── technical.md           # (stub: placeholder API/DB notes)
├── infra/                     # Setup & containerization (start Day 1–2)
│   ├── Dockerfile             # (stub or basic Python base image)
│   ├── Makefile               # (stub: targets like setup, test)
│   └── setup.sh               # (optional: uv/pyproject.toml init script)
├── mcp-config/                # MCP & skills (notes Day 1, full Day 2)
│   └── tooling_strategy.md    # Dev MCP servers vs runtime skills separation
├── skills/                    # Skill contracts (Day 2+)
│   └── README.md              # Placeholder: "Skills interfaces to be defined here"
├── tests/                     # TDD failing tests (Day 3)
│   └── (empty for now)
├── .github/workflows/         # CI/CD (Day 3)
│   └── main.yml               # (stub: basic test runner placeholder)
├── .cursor/                   # or CLAUDE.md — IDE agent rules
│   └── rules.md               # (stub: Prime Directive, context)
├── pyproject.toml             # or requirements.txt — Python env (uv recommended)
└── .gitignore                 # Standard Python + secrets ignore

## Current Status (Day 1 - Feb 04, 2026)
- Repo initialized
- Research summary & architecture strategy drafted (see docs/)
- MCP Sense connected (log/screenshot in docs/ if needed)
- Next: Specs population & tooling strategy
