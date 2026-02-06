
# Architecture Strategy – Project Chimera

## Chosen Agent Pattern
FastRender Hierarchical Swarm (Planner → Worker → Judge)

Why:
- Parallelism & throughput: Workers stateless/ephemeral → horizontal scale
- Error recovery & quality: Judge validates every output, implements OCC
- Dynamic re-planning: Planner reacts to failures/news/budget changes
- Superior to sequential chain (single choke point) or flat swarm (no governance)

## Human-in-the-Loop Placement
At Judge level (Review Queue)
- Confidence >0.90: Auto-approve
- 0.70–0.90: Async HITL
- <0.70: Reject & re-plan
- Mandatory HITL on sensitive topics regardless of score

## Database Choice & Rationale
Hybrid (Weaviate + PostgreSQL + Redis)
- Weaviate: semantic memory, vector search for RAG, trend detection, persona embeddings
- PostgreSQL: ACID transactional data (campaigns, logs, wallet states, P&L)
- Redis: queues (task/review), short-term/episodic cache, high-velocity access

Why this combo:
- High-velocity video metadata (captions, embeddings, engagement) needs semantic indexing (Weaviate) + fast caching (Redis)
- Financial agency (AgentKit wallets) requires strong consistency (PostgreSQL)
- Avoids single-DB trade-offs: pure relational lacks semantic search, pure vector lacks ACID

## High-Level Diagram
```mermaid
flowchart TD
    O[Orchestrator] -->|HITL Escalation| J[Judge]
    P[Planner] -->|DAG Tasks| TQ[Redis Task Queue]
    TQ --> WP[Worker Pool<br>(Stateless, Parallel)]
    WP --> RQ[Redis Review Queue]
    RQ --> J
    J -->|Approve| MCP[MCP Servers<br>(Twitter, Weaviate, Coinbase...)]
    J -->|Reject/Re-plan| P
    G[(Global State<br>Weaviate + PostgreSQL)] <--> P
    G <--> J
    G <--> WP
    style O fill:#ffcc99,stroke:#333
    style G fill:#99ccff,stroke:#333
    style MCP fill:#ccffcc,stroke:#333
```
