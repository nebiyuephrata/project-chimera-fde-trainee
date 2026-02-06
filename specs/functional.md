# Functional Spec

## User stories (draft)

### As an operator, I can submit a goal for the system
**Acceptance criteria**
- Given a goal string, the planner produces a task graph (or linear plan) in a structured schema.
- The orchestrator persists the plan and emits work items for workers.

### As a reviewer, I can evaluate outputs
**Acceptance criteria**
- Judge produces a verdict with confidence score and rationale.
- Outputs that fail constraints are either rejected or revised.

