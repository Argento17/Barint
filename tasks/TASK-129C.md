---
id: TASK-129C
title: Freeze bread on retail_003 authority; close limitingFactors gap
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-01
depends_on: [TASK-128]
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
