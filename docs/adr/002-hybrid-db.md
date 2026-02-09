# ADR-002: Hybrid Data Storage

## Status: Accepted

## Context
The system needs durable transactional data, fast queues, and semantic memory for agent context. A single database does not meet all performance and retrieval requirements.

## Decision
Adopt a hybrid storage strategy:
- PostgreSQL for transactional records (campaigns, accounts, wallet states, audit logs).
- Weaviate for vector search over memory, trends, and embeddings.
- Redis for short-term caching and work queues (task_queue, review_queue).

## Rationale
- Fit-for-purpose data stores reduce complexity in query patterns.
- Vector search requires dedicated indexing and retrieval performance.
- Queues and ephemeral state benefit from in-memory speed.

## Alternatives Considered
- Single relational database: weak for vector search and high-volume queues.
- Full document database: insufficient transactional guarantees.

## Consequences
More operational complexity, but improved performance and clarity of responsibilities.
