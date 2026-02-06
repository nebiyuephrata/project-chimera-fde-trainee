# Functional Specifications – User Stories & Acceptance Criteria

## Agent-Level Stories
As a Chimera Agent, I need to:
- Fetch real-time trends via MCP Resources so I can create relevant content
  - Acceptance: Trends filtered by relevance score ≥ 0.75, passed to Planner
- Generate multimodal content (text, image, video) via MCP Tools so I can publish engaging posts
  - Acceptance: All generation includes persona consistency lock (character_reference_id or LoRA)
- Publish content & reply to engagement via MCP Tools so I can grow audience
  - Acceptance: Platform-agnostic (twitter, instagram, threads), dry-run capability
- Check wallet balance & execute micro-transactions via AgentKit so I can manage economic agency
  - Acceptance: Balance check before any cost-incurring task, budget enforced by CFO Judge
- Self-disclose AI nature when directly asked so I remain compliant
  - Acceptance: Honesty Directive overrides persona constraints

## Swarm-Level Stories
As a Planner Agent, I need to:
- Decompose campaign goals into DAG tasks so Workers can execute in parallel
  - Acceptance: Dynamic re-planning on failure/news event
- Monitor GlobalState & budget so I can adjust priorities
  - Acceptance: Blocks cost-incurring tasks if balance low

As a Worker Agent, I need to:
- Execute single atomic task using MCP Tools so I remain focused & scalable
  - Acceptance: Stateless, no peer communication, result pushed to ReviewQueue

As a Judge Agent, I need to:
- Validate output confidence, persona alignment & safety so quality is maintained
  - Acceptance: >0.90 auto-approve, 0.70–0.90 async HITL, <0.70 reject/re-plan
  - Mandatory HITL on sensitive topics (politics, health, finance, legal)
