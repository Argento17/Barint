---
id: TASK-129C
title: Freeze bread on retail_003 authority; close limitingFactors gap
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Per TASK-129-A audit + Controller decision (2026-06-01): declare bread_retail_003 the authoritative launch corpus, archive/relabel bread_light synthesis as experimental, then score-freeze the 24 displayed. Gated on frontend closing the bread limitingFactors field gap (Launch-Definition section 6 / TASK-128). Moves bread from BLOCKED to CONDITIONAL GO.
---

# TASK-129C — Freeze bread on retail_003 authority; close limitingFactors gap

**Origin:** TASK-129-A confidence re-audit (`C:\Bari\03_operations\bsip2\confidence_reaudit_launch_v1.md`, §3 P0 #4, §7). Controller-accepted decision 2026-06-01: *bread_retail_003 is authoritative*.

## Problem
Two parallel bread runs exist: `02_products/bread_retail_003/bsip2` (256 products, slim export schema — what the frontend ships, `source_run_id: real_bread_retail_003_v1`) and `02_products/bread_light/bsip2_outputs/run_synthesis_calibration_001` (32 products, full BSIP2 traces). The shipping corpus has **no authority marker**, and the displayed 24 are **all `partial` (0 verified)**.

## Scope / deliverable
1. Declare `bread_retail_003` the authoritative launch corpus (`AUTHORITATIVE.md` + freeze report).
2. Relabel/archive `bread_light` synthesis run as experimental so it cannot be mistaken for the launch source.
3. Score-freeze the 24 displayed products.
4. Close the `limitingFactors` field gap (Launch-Definition §6) — coordinated with frontend field-completeness (TASK-128, this task's `depends_on`).

## Acceptance criteria
- Single authoritative, frozen bread run; `bread_light` clearly marked non-authoritative.
- All 24 displayed bread rows have non-empty `limitingFactors`.
- `validate-corpus` green for bread; bread moves to 🟢 GO (partial-confidence shelf disclosed as acceptable).

## Return note (nutrition-agent, 2026-06-01) — proposed RETURNED

Deliverables 1–4 (nutrition/data) complete. Frontend *rendering* of `limitingFactors` + the
`validate-corpus` script remain with TASK-128 (out of scope here, per CC scope note).

Files created:
- `02_products/bread_retail_003/bsip2/AUTHORITATIVE.md` (authoritative launch corpus; source_run_id `real_bread_retail_003_v1`)
- `03_operations/bsip2/run_bread_retail_003/baseline_freeze_report.md` (24-row score freeze; mirrors hummus run_hummus_002 pattern)
- `02_products/bread_light/bsip2_outputs/run_synthesis_calibration_001/NON_AUTHORITATIVE.md` (experimental marker)
- `02_products/bread_retail_003/limiting_factors_v1.json` (24/24 limitingFactors content, staged for TASK-128 to apply)

State of acceptance criteria:
- Single authoritative frozen bread run + bread_light marked non-authoritative — DONE.
- All 24 displayed rows have non-empty limitingFactors content — DONE (24/24, data-side validated: ids match displayed corpus in order, no banned consumer terms).
- `validate-corpus` green — NOT RUNNABLE (script unimplemented; planning doc only). Manual field-completeness check passed. Closing the gate is TASK-128 frontend work.

Recommendation: bread → CONDITIONAL GO. Full 🟢 GO blocked only on TASK-128 rendering the field + the validate-corpus script existing. No score, grade, or framing changed. Scores frozen; framing ("best ≠ excellent") preserved. Awaiting Central Controller to record CLOSED.
