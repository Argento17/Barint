---
id: TASK-133D
title: F4 - BHA named-additive penalty (differentiate BHT); verify FDA GRAS status first
owner: nutrition-agent
status: BLOCKED
priority: LOW
created_at: 2026-06-01
blocker: "waiting on TASK-133A (named-additive taxonomy)"
depends_on: [TASK-133A]
blocks: []
category_id: null
summary: >
  WATCH (Low). Cheap piggyback once the named-additive lookup exists: add BHA (E320) as a small named penalty in the existing additive/processing dimension; explicitly differentiate BHT (NOT under reassessment). Do NOT build regulatory-status tracking. Verify current FDA GRAS/reassessment outcome first - Apr-2026 comment window has closed and the spring-2026 GRAS rule may have landed.
---

# TASK-133D — F4 - BHA named-additive penalty (differentiate BHT); verify FDA GRAS status first

## Plan of record — Phase D (F4, do last / verify first)

Roadmap: [TASK-133_implementation_roadmap.md](../research/TASK-133_implementation_roadmap.md) §Phase D.

- **Gate:** WebSearch the current FDA BHA / GRAS-rule outcome **before coding** — the Apr-2026 comment
  window closed and the spring-2026 rule may have landed. Go/no-go on the result.
- **Code:** BHA (E320) small named penalty in the additive/processing dimension via the taxonomy;
  **BHT explicitly excluded**. No regulatory-tracking subsystem.
- **DoD:** BHA-containing snack/oil/cereal products flagged; BHT products unchanged. Size: S.
- **Calibration sign-off:** [DEC-004](../decisions/decisions.json) gates the penalty size.
