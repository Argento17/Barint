---
id: TASK-129B
title: Reconcile yogurts to a frozen machine run, then score-freeze
owner: nutrition-agent
status: IN_PROGRESS
priority: CRITICAL
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Per TASK-129-A audit + Controller decision (2026-06-01): retire the v1-mvp-manual hand-tuned yogurt scores as source of truth. Regenerate from run_yogurt_001, diff vs the 13 displayed scores, resolve each delta, freeze the reconciled corpus. Unblocks yogurts frontend NO-GO (launch gate).
---

# TASK-129B — Reconcile yogurts to a frozen machine run, then score-freeze

**Origin:** TASK-129-A confidence re-audit (`C:\Bari\03_operations\bsip2\confidence_reaudit_launch_v1.md`, §3 P0 #2, §7). Controller-accepted decision 2026-06-01: *reconcile to machine run*.

## Problem
The shipping yogurts shelf (`src/data/comparisons/yogurts_frontend_v1.json`, `version: v1-mvp-manual`) displays 13 **hand-tuned** scores ("ציונים מכווננים ידנית"). They are not reproducible from any frozen BSIP2 run, so the category **cannot be score-frozen** and is **NO-GO** for launch. A machine run (`02_products/yogurt_system/bsip2_outputs/run_yogurt_001`, 45 products) exists but is not what the frontend ships.

## Scope / deliverable
1. Regenerate yogurts from `run_yogurt_001` (or a fresh `run_yogurt_002` if the corpus needs refresh) for the 13 displayed products.
2. Diff machine output vs the 13 manual scores; for every delta, either accept the machine score or record a justified, rule-based calibration (no free-hand tuning).
3. Re-confirm display data-sufficiency labels (all currently `partial`) against the §5 gate.
4. Mark the chosen run authoritative (`AUTHORITATIVE.md` + freeze report, mirror the hummus pattern) and update the frontend corpus to cite `source_run_id`.

## Acceptance criteria
- Every displayed yogurt score traces to a frozen, reproducible run; 0 hand-tuned values remain.
- Freeze marker present; frontend `_meta.source_run_id` + `authoritative: true` set.
- Yogurts moves from 🔴 NO-GO to 🟢 GO in the launch board.
