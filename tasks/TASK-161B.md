---
id: TASK-161B
title: Regenerate +/- reason signals (cheese, yogurts, bread) from BSIP2 explanation engine
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — verified in src/data/comparisons/: cheese 51 rows (42 +pos / 44 -lim), yogurts 11 (10/4), bread 24 (24/19); every row renders >=1 of +/-; real named values (e.g. 'חלבון גבוה לקטגוריה — 9 גרם ל-100 גרם'). Generated deterministically from BSIP2 traces (run_cheese_003 / run_yogurt_004) via build_cheese_signals.py / build_yogurts_signals.py / build-bread-frontend-v2.mjs; scores id-matched unchanged (0 mismatches); 0 of 9 engine-v2 banned phrases. Products legitimately lacking one signal omitted, not invented. Two issues escalated separately (NOT defects of this task): (a) bread grade drift shufersal_3268429 A-vs-B (pre-existing, frozen-invariant — Product/Nutrition call); (b) some pre-existing bread positiveSignals read as false strengths ('בסיס קמח מזוקק','שמרים תעשייתיים') — Content cleanup -> TASK-161E."
depends_on: []
blocks: []
category_id: null
summary: >
  cheese/yogurts frontend JSON have 0 positiveSignals+limitingFactors; bread has 0 limitingFactors. Regenerate expansion.positiveSignals[]/limitingFactors[] deterministically from the explanation engine (same source hummus/maadanim use). No fabrication; rebuild frontend JSON. Snacks metric value if Nutrition picks one.
---

# TASK-161B — Regenerate +/- reason signals (cheese, yogurts, bread) from BSIP2 explanation engine

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
