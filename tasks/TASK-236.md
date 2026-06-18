---
id: TASK-236
title: "Engine: absence-as-zero — a missing nutrient field is scored as 0 (cross-category)"
owner: nutrition
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-10
completed_at: null
depends_on: []
blocks: []
related: [TASK-235, TASK-189]
category_id: null
roadmap_impact: false
work_type: defect
deferred: true
blocker: >
  Cross-category scoring-philosophy change. Treating a missing nutrient field as a true
  zero alters how nutrient_density (and likely other dimensions) score every product whose
  label omits a field — i.e. it can move PUBLISHED scores. Requires a Nutrition+Product D7
  decision on the absence-vs-zero rule + EV-### evidence before any engine change. Deferred,
  not yet scheduled.
---

# TASK-236 — Engine: a missing nutrient field is scored as `0` (absence ≠ zero)

## Status
**BLOCKED / deferred** — logged for later per owner (2026-06-10). **Do NOT solve inside TASK-235.**

## The defect
The engine treats a nutrient field that is *absent* from a label as a literal `0` rather than
"not characterized." Confirmed in frozen vegetables: crushed garlic's `nutrient_density` computed
`fiber=0g → 0.0` (dimension note: `protein=6.0g→30.0, fiber=0g→0.0, weighted 65/35=19.5`) — but
garlic genuinely contains fiber; the label simply omitted it. The gap was scored as a deficiency.

## Why it matters
- Understates every product whose label omits fiber (or any benefit nutrient) — systematically and silently.
- Same class as the granola sodium scoring gap (**TASK-189**): a data condition the engine mishandles.
- It is a **methodology change that can move published scores**, so it is governed (D7), not a quick patch.

## Scope when picked up
- Decide the absence-vs-zero rule (impute from authoritative generic? mark "not characterized" and
  re-weight? suppress the field from the dimension?) — Nutrition owns; Product co-signs (D7).
- Identify all dimensions/penalties that read nutrient fields and currently coerce null→0.
- EV-### evidence registry entries for any imputation thresholds.
- Re-verify affected published scores across categories before shipping.

## Provenance
Surfaced 2026-06-10 during TASK-235 (frozen-vegetables v2) diagnosis. Frozen v2 itself sidesteps this
by removing the score for that category; the engine fix remains owed for the categories that keep scoring.
