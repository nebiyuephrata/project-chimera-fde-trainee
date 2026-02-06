# Technical Specifications – Schemas, Contracts & Interfaces

## Database Schema (Hybrid)
- Weaviate: vector index for semantic memory, persona embeddings, trend alerts
- PostgreSQL: transactional tables (campaigns, logs, wallet states, user accounts)
- Redis: task_queue, review_queue, short-term/episodic cache

## Agent Task Payload (JSON – Planner → Worker)
```json
{
  "task_id": "uuid-v4",
  "task_type": "generate_content | reply_comment | execute_transaction",
  "priority": "high | medium | low",
  "context": {
    "goal_description": "string",
    "persona_constraints": ["string"],
    "required_resources": ["mcp://twitter/mentions/123", "mcp://memory/recent"]
  },
  "assigned_worker_id": "string",
  "created_at": "timestamp",
  "status": "pending | in_progress | review | complete"
}
```
