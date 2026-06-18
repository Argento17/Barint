---
id: TASK-306
title: Hummus tighten to prepared-dips-only — exclude canned/raw chickpeas + empty-ingredient products, re-run, re-gate
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  C1-GROK (P161) + orchestrator-verified. Tightened hummus to prepared-dips-only: 6 more exclusions (208428 + 7290018359686
  canned whole chickpeas whose 'ingredients' were marketing/recipe copy; 7296073733317/733348/1990261/3643714 empty-ingredient)
  → 12 total excluded, 57 kept. VERIFIED: 57 products, 0 grade-A, 0 empty-ingredient remaining, all 12 excluded absent, top-3 all
  tahini/oil-bearing dips (new #1 = 7296073725404 B/70.6 cooked-chickpeas+raw-tahini 31%), G8 PASS, C10 Δ0, OFF=0, score==trace OK.
  Owner 'prepared dips only' ruling satisfied. Only 2 products need fresh copy (7290106577480 C→E, 7290106577572 C→D vs live).
  Hummus now joins the clean deploy set.
depends_on: [TASK-304]
blocks: []
category_id: null
summary: >
  Owner ruling: hummus shelf = prepared dips only. Beyond the 6 raw-chickpea bags already excluded, ALSO exclude (a) products whose ingredients are only chickpeas/water/salt with NO tahini/oil/seasoning (canned/cooked whole chickpeas, not a dip) and (b) products with empty/unknown ingredient data. KEEP prepared spreads (tahini/שמן/oil/garlic/lemon/seasoning present). Add exclusions to configs/hummus_shelfrel_002.json, re-run --shelf, re-gate (G8/C10/OFF/score==trace). Report new dips-only set + its grade dist + the changed/new products needing copy.
---

# TASK-306 — Hummus tighten to prepared-dips-only — exclude canned/raw chickpeas + empty-ingredient products, re-run, re-gate

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
