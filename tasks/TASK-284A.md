---
id: TASK-284A
title: Data verification pass: PHVO partial-vs-generic split + milk seed-oil anomaly + exact seed_pen 10to5 blast radius
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-15
completed_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Unblocks EV-097 and firms EV-096. (1) Recover ingredient text from BSIP1 source for the 70 has_phvo products (trace text empty); classify each as partial (מוקשה חלקית/partially hydrogenated) vs generic (שומן מוקשה/שומנים מוקשים/שומן צמחי מוקשה/מרגרינה); exact split counts. (2) Confirm the 3 milk has_seed_oil=True products — real (flavored/plant) or extraction artifact. (3) Compute EXACT seed_pen 10to5 grade-boundary crossings across the 719 confirmed-path products (agent only estimated ~10-14). Verification + counts ONLY; no score moves.
---

# TASK-284A — Data verification pass: PHVO partial-vs-generic split + milk seed-oil anomaly + exact seed_pen 10to5 blast radius

## Results (2026-06-15)

### D1: PHVO split — 0 partial / 49 generic (49 unique barcodes, 70 traces)
All 70 has_phvo traces recovered ingredient text from BSIP1 source files. Zero contain `מוקשה חלקית` or `partially hydrogenated`. All 49 unique barcodes trigger on generic markers only (מרגרינה dominant, plus שומן מוקשה/שומן צמחי מוקשה). Two confirmed-חלקית barcodes from the earlier BSIP0 raw scan (7290101114116, 7290101114109, cheese_spreads) are NOT in the has_phvo=True scored corpus. EV-097 two-tier proposal confirmed: all 49 currently-scored PHVO products would move from ceiling 40 to ceiling 55.

### D2: Milk seed-oil — 8 unique barcodes (not 3), all REAL
All are plant-based alternatives (oat/rice drinks — Alpro, Isola Bio, Oatly-style products). Seed oil (canola, sunflower) is genuine ingredient confirmed in BSIP1 files. Not extraction artifacts. None in frozen dairy milk corpus (run_005_headpin). No data correction needed.

### D3: Exact blast radius — 5 grade crossers (not ~10-14)
719 traces on confirmed seed_pen=10 path (matches Nutrition Agent count). Reducing seed_pen 10→5 (+0.4 final delta): exactly 5 unique barcode+category pairs cross a grade boundary (2 E→D, 3 D→C). All 5 in published but non-frozen categories (breakfast_cereals x3, cakes_hard_cookies x1, salty_snacks x1). 0 frozen crossers.

## Artifacts
- `tasks/TASK-284A-verification-report.md` — full report with ingredient snippets and barcode tables
- `tasks/_temp_verify_284a_v2.py` — reproducible verification script

## close_reason (orchestrator, 2026-06-15)
CLOSED — DoD met (3 verified counts) + orchestrator spot-verified: report file present; מרגרינה
confirmed dominant in cakes/cookies BSIP1 source (57 files); `מוקשה חלקית` independently confirmed = 0.
Two Nutrition-Agent estimates corrected (seed_pen crossers ~10–14 → **5**; milk seed-oil 3 → **8**, all
benign plant-based, 0 frozen). **Open item handed to parent TASK-284:** EV-097's split is confirmed,
but "49 move ceiling 40→55" is a CEILING-parameter change — its actual grade impact is uncomputed
(only binds where pre-ceiling fat_quality >40, e.g. lower-sat margarine products). The Shadow re-score
must quantify EV-097's grade blast radius alongside EV-096's confirmed 5.
