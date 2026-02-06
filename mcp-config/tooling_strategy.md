# Tooling Strategy – Developer MCP Tools vs Runtime Agent Skills

This document encodes the separation of concerns required by `.cursor/rules.md`:

- **Rule 3**: Developer MCP tools (git-mcp, filesystem-mcp, code-review-mcp) are ONLY for development workflow.  
- **Rule 3**: Runtime Agent Skills (e.g., trend_fetch, generate_image, post_content, wallet_balance) are ONLY for Chimera agents via MCP.  
- **Rule 5 & 10**: All interfaces must use Pydantic / JSON Schema and remain spec-driven.

The stories in `specs/functional.md` (Agent-Level, Swarm-Level, Operator & Governance sections) define *what* the system must do.  
This file defines *how we wire tools* to meet those stories without crossing Dev/Runtime boundaries.

## 1. Developer MCP Tools (for Ephrata’s workflow only)

Developer tools exist to help you, the human FDE, work on this repository safely and traceably.  
They MUST NOT be used by runtime Chimera agents.

- **git-mcp**  
  - **Purpose**: Inspect branches, diffs, commit history, and PR metadata.  
  - **Specs reference**: Supports traceability and CI requirements implied by `specs/_meta.md` (Core Constraints: traceability, CI must pass).  
  - **Example usage**: "List changed files since main" to scope a code review.

- **filesystem-mcp**  
  - **Purpose**: Read and navigate project files (`specs/`, `docs/`, `src/`, `tests/`) without direct shell access.  
  - **Specs reference**: Enforces the Prime Directive in `.cursor/rules.md` §1–2 by always consulting specs before edits.  
  - **Example usage**: "Show specs/functional.md before implementing a new test."

- **code-review-mcp**  
  - **Purpose**: Run static analysis on diffs, suggest improvements, and check alignment with SRS (FastRender Swarm, HITL, budget rules).  
  - **Specs reference**: Validates that implementations honor `specs/functional.md` Swarm, Operator, and Governance stories.  
  - **Example usage**: "Review changes to planner service for adherence to HITL rules."

- **test-runner-mcp** (or pytest-mcp)  
  - **Purpose**: Trigger `pytest` runs, surface failing tests, and map failures back to specs.  
  - **Specs reference**: Implements `.cursor/rules.md` §2 (TDD) and ensures TDD tests (e.g., `tests/unit/test_task_schema.py`) remain the source of truth for acceptance.  
  - **Example usage**: "Run unit tests for task schema and skill interfaces."

**Rules for Developer MCP tools**
- NEVER embed production credentials or wallets.  
- NEVER call external social/commerce APIs on behalf of Chimera agents.  
- MAY read/write local files in this repo as part of development, under Git control.

## 2. Runtime Agent Skills (for Chimera agents only)

Runtime skills are the **only way** Chimera agents interact with the outside world via MCP.  
They implement the functional stories in `specs/functional.md` "Agent-Level Stories" and the governance constraints.

Each skill:
- Exposes **strictly typed interfaces** (Pydantic / JSON Schema).  
- Enforces **HITL, budget, and safety** constraints indirectly by feeding data to Planner/Worker/Judge.  
- Is versioned and documented in `skills/` with inputs, outputs, and failure modes.

### 2.1 `trend_fetch` (Runtime Skill)

- **Purpose**: Fetch real-time trends and signals from external sources (news, social feeds, etc.) via MCP Resources.  
- **Specs reference**:
  - `specs/functional.md` – Agent-Level: "Fetch real-time trends via MCP Resources so I can create relevant content" with relevance score ≥ 0.75.  
  - Swarm-Level: Planner uses these signals to build DAG tasks.
- **High-level behavior**:
  - Input: topic, locale, time window, optional platform hints.  
  - Output: normalized list of trend objects with relevance scores and source URIs (often `mcp://...` handles).

### 2.2 `generate_content` (Runtime Skill)

- **Purpose**: Generate multimodal content (text, image, video) for an agent persona, ready for review/posting.  
- **Specs reference**:
  - `specs/functional.md` – Agent-Level: "Generate multimodal content via MCP Tools" with persona consistency lock (character_reference_id or LoRA).  
  - Governance stories: Brand Owner persona enforcement.
- **High-level behavior**:
  - Input: goal_description, target platforms, persona constraints (from SOUL.md), and optional trend IDs.  
  - Output: one or more candidate content payloads with metadata (length, modality, safety flags).

### 2.3 `post_content` (Runtime Skill)

- **Purpose**: Publish content or replies to supported platforms via MCP Tools, respecting dry-run and HITL decisions.  
- **Specs reference**:
  - `specs/functional.md` – Agent-Level: "Publish content & reply to engagement via MCP Tools" with platform-agnostic design and dry-run capability.  
  - Governance & Compliance: Judge/HITL must approve risky content before posting.
- **High-level behavior**:
  - Input: approved content payload, target platform(s), scheduling options, dry_run flag.  
  - Output: posting receipts (IDs, timestamps) or simulated receipts in dry-run mode.

## 3. Schema Discipline (Pydantic / JSON Schema)

Per `.cursor/rules.md` §10 and `specs/technical.md`:

- **All skill interfaces** (inputs and outputs) MUST be defined using:
  - Pydantic models in code (preferred), and/or  
  - Equivalent JSON Schema documents in `skills/README.md` for documentation.
- **No loosely typed dicts** may cross the boundary between Orchestrator/Planner/Worker/Judge and skills.  
- **Tests first**: For each new skill, add a failing unit test (e.g., under `tests/unit/test_skill_interfaces.py`) that encodes:
  - Required fields (e.g., `query` for `trend_fetch`).  
  - Enum-like constraints (e.g., supported platforms).  
  - Basic invariants (e.g., non-empty arrays for required resources).

Runtime agents may only call these skills through MCP servers that honor these strict schemas.  
Developer MCP tools MUST NOT bypass these schemas or directly mutate production state.

