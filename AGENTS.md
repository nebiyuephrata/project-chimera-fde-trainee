## Project Chimera – Agent Governance Stub

This document is a **governance template** for Chimera agents.  
It is intentionally kept as a stub; all sections below are placeholders that
must be refined and ratified before production use.

References (SRS):
- **§1.2 BoardKit Pattern** – multi-role decision-making and escalation model.
- **§5.2 Ethical Framework** – non-negotiable safety, compliance, and brand rules.

---

### Ethical Boundaries

- **Placeholder**: Define disallowed content categories (e.g., hate, harassment,
  disallowed financial advice) and escalation rules.
- **Placeholder**: Map confidence thresholds and HITL requirements to risk levels,
  aligning with SRS §5.2 (Ethical Framework).
- **Placeholder**: Specify mandatory disclosure rules for AI-generated content and
  when agents must self-identify as AI.

---

### Brand Voice Guidelines

- **Placeholder**: Describe tone, style, and persona constraints derived from
  each agent's `SOUL.md`.
- **Placeholder**: List examples of on-brand vs. off-brand outputs for future
  calibration.
- **Placeholder**: Define how Judges should evaluate persona alignment and when
  to flag drift for review (ties into SRS §1.2 BoardKit Pattern).

---

### Operational Rules

- **Placeholder**: Encode the FastRender Swarm roles (Planner → Worker → Judge)
  and their decision rights for campaigns.
- **Placeholder**: Define limits for tool usage, budget thresholds, and when to
  route decisions to the "Board" (BoardKit pattern, SRS §1.2).
- **Placeholder**: Specify logging, auditing, and traceability requirements for
  all agent actions.

---

### Update Process (GitOps via SOUL.md)

- **Placeholder**: All governance and persona changes must be proposed via git
  (pull request) updates to `SOUL.md` and this `AGENTS.md`.
- **Placeholder**: Describe the review process (e.g., which human roles must
  approve changes) following SRS §1.2 (BoardKit pattern).
- **Placeholder**: Require that any change to ethical or operational rules be
  linked to an SRS update (especially §5.2 Ethical Framework) and recorded in
  release notes.

