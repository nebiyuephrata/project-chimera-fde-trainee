# ADR-001: Agent Pattern Selection

## Status: Accepted

## Context
Need high parallelism, error recovery, governance for autonomous influencers.

## Decision
Chose FastRender Hierarchical Swarm (Planner -> Worker -> Judge) over sequential chain or flat swarm.

## Rationale
- Parallelism (stateless Workers)
- Quality gating (Judge + OCC)
- Dynamic re-planning (SRS section 3.1)

## Alternatives Considered
- Sequential chain: too linear, single choke point
- Flat swarm: no governance

## Consequences
Higher throughput, better safety, more complex debugging.
