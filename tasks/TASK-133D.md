---
id: TASK-133D
title: F4 - BHA named-additive penalty (differentiate BHT); verify FDA GRAS status first
owner: nutrition-agent
status: RETURNED
priority: LOW
created_at: 2026-06-01
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

## Implementation status — 2026-06-01 (structural build COMPLETE; gate PASSED)

Report: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md).

- **GATE PASSED (WebSearch 2026-06-01):** FDA launched a **post-market reassessment of BHA
  (E320) on 2026-02-10** (RFI closed 2026-04-13; **no final GRAS rule has landed** as of
  2026-06); NTP lists BHA as "reasonably anticipated to be a human carcinogen." **BHT (E321)
  is not yet under reassessment** (FDA reassesses it only after BHA). → **GO** for a small
  named BHA penalty; BHT explicitly differentiated; no regulatory-tracking subsystem needed
  (static penalty correct while no rule has landed).
- **Built:** taxonomy resolves BHA→E320 (`is_named_concern`) and BHT→E321 (`is_named_concern=False`);
  `tax_bha_present` / `tax_bht_present` emitted; `BHA_NAMED_PENALTY` (−5 placeholder) applied in
  `_identity_additive_deltas()`, distinct from the generic antioxidant-category count. BHT excluded.
- **Validated:** synthetic BHA product → −5 applied; synthetic BHT product → unchanged. No
  BHA-containing products in the current real corpora (penalty is dormant until one appears).
## Return block — 2026-06-01 (proposed RETURNED → Controller to record CLOSED)

DEC-004 **DECIDED** (BHA −5 ratified). FDA gate PASSED (BHA under active reassessment since
2026-02-10, no final rule landed; BHT not yet under reassessment → differentiated). BHA named
penalty applied, BHT excluded, no regulatory-tracking subsystem. No BHA products in current real
corpora → penalty dormant (zero live impact). Specs synced (`processing_analysis.md`, `ui_language.md`).
Awaiting Central Controller to record CLOSED.
