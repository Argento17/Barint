---
id: TASK-273
title: Brined golden-page intro rewrite + inviting comparison table (Content+Design, Nutrition-consulted)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
closed_at: 2026-06-13
close_reason: >
  Content's prose (story opening, methodology, count-agnostic frame) was strong and kept, but its brand call-outs were sourced from v1 → 2 wrong brands + a false 'minimalism' framing on preservative-containing products (it even documented the preservative in its own metadata yet wrote against it). Per owner's minimal-resource directive, orchestrator corrected the copy INLINE against verified frontend_v2 facts instead of another Content round-trip: filled {{N}}=36 / {{DIST}}=9A/20B/5C/2D, fixed brands (גד→יורו, dropped המושבה mis-attribution), replaced the fabricated clean-exemplar with the true 2-clean story (יורו bulgarit 13% 80/A + רג'ב tamra 65/C; top-85 gad cheeses lean on a preservative → 'clean != top score'). Re-ran offline gate: is_clean=True, em-dash<=1/sentence, no internal tokens, no placeholders. Draft: 02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json. Expressive-Hebrew-API enhancement tracked separately in TASK-274; render/charts in TASK-268.
depends_on: [TASK-272]
blocks: []
category_id: null
summary: >
  Owner 2026-06-13: intro not readable; keep first 2 story sentences, add expressive Hebrew sentiment (standing per-page rule), more creative, good words for some brands, plus an inviting comparison-table design. Count-agnostic until Data settles corpus.
---

# TASK-273 — Brined golden-page intro rewrite + inviting comparison table (Content+Design, Nutrition-consulted)

## Deliverable (Content draft v1, 2026-06-13)
Draft at `02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json`. Prose (prologue 1-3, methodology 1-3) is strong, readable, em-dash/leakage gates pass, "capped at 75" removed, count-agnostic `{{N}}`/`{{DIST}}` placeholders.

## CHANGES_REQUESTED — orchestrator verification 2026-06-13 (facts checked vs brined_cheeses_frontend_v2.json)
Content sourced brand facts from **v1**; against authoritative **v2** the brand call-outs are wrong:
- `7290108509106` — Content says "מחלבות גד", v2 brand = **"יורו מחלבות אירופה"** (720mg ✓, score 80/A). WRONG BRAND.
- `554457` — Content says "מחלבת המושבה", v2 brand = **"מחלבות גד"** (600mg lowest-in-A ✓ tied w/ 554532, score 85/A). WRONG BRAND.
- `7290019635826` gad goat feta — framed as clean low-sodium exemplar + "highest score on shelf"; v2 = 85/A but **3-way tie** at 85 (554457, 554532) and sodium **950mg** (mid-shelf, NOT low). Misleading.
- "שתי גבינות בלבד ללא שום תוסף" — verify the "2" against final corpus (16 products carry no d4_additives entries; "2" must be the ≤3-natural-ingredient definition — confirm or correct).

## Re-dispatch plan (bundled — do NOT re-dispatch standalone)
Held for ONE consolidated correction AFTER **TASK-272** finalizes the corpus (removals change `{{N}}`/`{{DIST}}` and could shift superlatives). Then: re-ground every brand call-out + superlative against FINAL v2, fill placeholders, confirm "2 clean". Pending owner clarification on the "Hebrew expressive-sentiment API fixture" (Content has no such API configured; used internal phrase library).
