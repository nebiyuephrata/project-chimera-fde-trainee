# Technical Spec

## Task schema (draft)

### `Task`
- `id`: string
- `title`: string
- `description`: string
- `status`: one of `pending | in_progress | done | failed`
- `inputs`: object
- `outputs`: object

## Interfaces (draft)
- `planner.plan(goal) -> Plan`
- `worker.execute(task) -> Result`
- `judge.evaluate(result) -> Verdict`

