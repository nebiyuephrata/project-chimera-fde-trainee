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
- Route sensitive tasks to the Judge with HITL required so we stay compliant  
  - Acceptance: Tasks tagged as politics/health/finance/legal are always queued for human review

As a Worker Agent, I need to:
- Execute single atomic task using MCP Tools so I remain focused & scalable  
  - Acceptance: Stateless, no peer communication, result pushed to ReviewQueue
- Emit structured telemetry (latency, tool calls, tokens, errors) so the Orchestrator can optimize the swarm  
  - Acceptance: Each task result includes timing + tool usage summary

As a Judge Agent, I need to:
- Validate output confidence, persona alignment & safety so quality is maintained  
  - Acceptance: >0.90 auto-approve, 0.70–0.90 async HITL, <0.70 reject/re-plan
- Enforce budget and risk policies for AgentKit transactions so agents cannot overspend  
  - Acceptance: Any transaction exceeding campaign_budget or risk_threshold is rejected and escalated
- Maintain an auditable review log so operators can trace why decisions were made  
  - Acceptance: Each verdict stores rationale, confidence, and references to reviewed resources

## Operator & Orchestrator Stories
As an Operator, I need to:
- Create and manage multi-step campaigns (goals, budget, time window, target platforms)  
  - Acceptance: Campaigns can be created via a single API call or UI flow and are persisted in PostgreSQL
- Inspect what each agent is doing in near real time so I can build trust  
  - Acceptance: For any campaign, I can view a timeline of tasks, outputs, and Judge decisions
- Pause or kill a campaign instantly if something goes wrong  
  - Acceptance: Orchestrator stops scheduling new tasks and cancels queued work within a bounded time (e.g., 30s)

As the Orchestrator, I need to:
- Assign tasks to Workers based on priority and capacity so SLAs are met  
  - Acceptance: High-priority tasks are always dequeued before low-priority ones
- Backoff or shed load when external MCP servers are degraded so the system remains stable  
  - Acceptance: Exponential backoff and circuit-breaking on repeated MCP failures
- Surface health metrics (queue depth, error rates, budget usage) to operators  
  - Acceptance: Metrics are exposed via a standard interface (logs/metrics endpoint) for dashboards

## Governance, Safety & Compliance Stories
As a Compliance Officer, I need to:
- Ensure agents self-disclose as AI when asked or when required by platform policy  
  - Acceptance: Responses to direct questions like "Are you AI?" always include a clear disclosure
- Enforce content policies (no hate, harassment, disallowed financial advice)  
  - Acceptance: Violating content is blocked by the Judge and never published

As a Brand Owner, I need to:
- Lock each agent to a well-defined persona (SOUL.md) so tone and values stay consistent  
  - Acceptance: Outputs that drift from persona constraints are flagged and require HITL approval

As a Finance / CFO role, I need to:
- Set per-campaign and per-agent spending limits so influencer activity stays within budget  
  - Acceptance: Any action that would exceed the remaining budget is rejected with a clear reason
- Review a ledger of all on-chain and off-chain economic actions initiated by agents  
  - Acceptance: Each transaction record includes who/what initiated it, rationale, and Judge verdict
