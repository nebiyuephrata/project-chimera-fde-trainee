# Chimera Runtime Skills – Interfaces (Spec-First)

This document defines **schema-level contracts** for initial runtime skills, as required by:

- `.cursor/rules.md` §3 & §10 – strict separation between Developer MCP tools and Runtime Agent Skills, and mandatory use of Pydantic / JSON Schema.  
- `specs/functional.md` – Agent-Level and Governance stories (trends, content generation, posting, persona & safety).  
- `specs/technical.md` – JSON-style task payloads and strong typing.

> Implementation code MUST NOT be added here yet. This file is **interfaces + acceptance criteria only**.

---

## 1. `trend_fetch` Skill

**Functional spec reference**:  
- `specs/functional.md` – Agent-Level: "Fetch real-time trends via MCP Resources so I can create relevant content" (relevance ≥ 0.75).  
- Swarm-Level: Planner consumes these trends to build DAG tasks.

### 1.1 Input Schema (JSON Schema style)

```json
{
  "$id": "skills/trend_fetch/input",
  "type": "object",
  "required": ["query", "locale", "time_window_minutes"],
  "properties": {
    "query": {
      "type": "string",
      "description": "High-level topic or keyword to search trends for (e.g., 'AI agents', 'Ethereum')."
    },
    "locale": {
      "type": "string",
      "description": "BCP-47 locale or region code (e.g., 'en-US', 'global')."
    },
    "time_window_minutes": {
      "type": "integer",
      "minimum": 5,
      "maximum": 1440,
      "description": "Lookback window for trends, in minutes."
    },
    "platform_hints": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Optional list of platform hints (e.g., ['twitter', 'tiktok'])."
    }
  },
  "additionalProperties": false
}
```

### 1.2 Output Schema

```json
{
  "$id": "skills/trend_fetch/output",
  "type": "object",
  "required": ["trends", "query", "generated_at"],
  "properties": {
    "query": { "type": "string" },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    },
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "relevance", "source_uri"],
        "properties": {
          "title": { "type": "string" },
          "summary": { "type": "string" },
          "relevance": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Relevance score; >= 0.75 is required by the spec."
          },
          "source_uri": {
            "type": "string",
            "description": "Typically an MCP resource handle, e.g. 'mcp://news/top/123'."
          }
        },
        "additionalProperties": false
      },
      "minItems": 0
    }
  },
  "additionalProperties": false
}
```

### 1.3 Acceptance Criteria

- Trends with `relevance < 0.75` MUST NOT be returned to the Planner (spec-enforced filter).  
- All `source_uri` values MUST be resolvable via MCP Resources, not raw HTTP-only links.  
- Empty result sets are allowed but must still conform to the output schema.

---

## 2. `generate_content` Skill

**Functional spec reference**:  
- `specs/functional.md` – Agent-Level: "Generate multimodal content (text, image, video) via MCP Tools" with persona consistency lock (character_reference_id / LoRA).  
- Governance section: Brand Owner persona consistency.

### 2.1 Input Schema

```json
{
  "$id": "skills/generate_content/input",
  "type": "object",
  "required": ["goal_description", "persona_id", "target_platforms"],
  "properties": {
    "goal_description": {
      "type": "string",
      "description": "High-level campaign or post goal, often derived from Planner tasks."
    },
    "persona_id": {
      "type": "string",
      "description": "Identifier mapping to SOUL.md and persona embedding."
    },
    "target_platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["twitter", "instagram", "tiktok", "threads", "youtube"]
      },
      "minItems": 1
    },
    "trend_ids": {
      "type": "array",
      "items": { "type": "string" },
      "description": "IDs or URIs of trends from trend_fetch."
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_length_tokens": { "type": "integer", "minimum": 32, "maximum": 4096 },
        "no_sensitive_topics": { "type": "boolean" }
      }
    }
  },
  "additionalProperties": false
}
```

### 2.2 Output Schema

```json
{
  "$id": "skills/generate_content/output",
  "type": "object",
  "required": ["persona_id", "candidates"],
  "properties": {
    "persona_id": { "type": "string" },
    "candidates": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "modality", "body", "safety_flags"],
        "properties": {
          "id": { "type": "string" },
          "modality": {
            "type": "string",
            "enum": ["text", "image", "video"]
          },
          "body": {
            "type": "string",
            "description": "For non-text modalities, a prompt or descriptor."
          },
          "safety_flags": {
            "type": "object",
            "properties": {
              "requires_hitl": { "type": "boolean" },
              "policy_violations": {
                "type": "array",
                "items": { "type": "string" }
              }
            }
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

### 2.3 Acceptance Criteria

- At least one candidate MUST be produced per call (`minItems: 1`).  
- If any safety or policy issues are detected, `safety_flags.requires_hitl` MUST be `true`.  
- Persona mismatch (detected downstream) should be traceable via `persona_id` and candidate `id`.

---

## 3. `post_content` Skill

**Functional spec reference**:  
- `specs/functional.md` – Agent-Level: "Publish content & reply to engagement via MCP Tools" with platform-agnostic design and dry-run capability.  
- Governance & Compliance: HITL and budget controls before posting.

### 3.1 Input Schema

```json
{
  "$id": "skills/post_content/input",
  "type": "object",
  "required": ["content_id", "platform", "dry_run"],
  "properties": {
    "content_id": {
      "type": "string",
      "description": "Identifier of a candidate from generate_content."
    },
    "platform": {
      "type": "string",
      "enum": ["twitter", "instagram", "tiktok", "threads", "youtube"]
    },
    "dry_run": {
      "type": "boolean",
      "description": "If true, simulate posting and return a mock receipt."
    },
    "scheduled_for": {
      "type": "string",
      "format": "date-time",
      "description": "Optional scheduling time; immediate if omitted."
    },
    "judge_approval_id": {
      "type": "string",
      "description": "Reference to a Judge verdict that approved this content."
    }
  },
  "additionalProperties": false
}
```

### 3.2 Output Schema

```json
{
  "$id": "skills/post_content/output",
  "type": "object",
  "required": ["content_id", "platform", "dry_run", "status"],
  "properties": {
    "content_id": { "type": "string" },
    "platform": { "type": "string" },
    "dry_run": { "type": "boolean" },
    "status": {
      "type": "string",
      "enum": ["scheduled", "posted", "simulated", "failed"]
    },
    "provider_post_id": {
      "type": "string",
      "description": "Provider-specific identifier (e.g., tweet ID). May be absent in dry_run."
    },
    "error": {
      "type": "string",
      "description": "Optional error detail when status = 'failed'."
    }
  },
  "additionalProperties": false
}
```

### 3.3 Acceptance Criteria

- When `dry_run` is `true`, `status` MUST be `"simulated"` and no real post is created.  
- When `status` is `"posted"` or `"scheduled"`, `provider_post_id` MUST be present.  
- Posts without a valid `judge_approval_id` MUST NOT be executed in production (checked upstream by Judge/HITL logic).

