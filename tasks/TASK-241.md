---
id: TASK-241
title: "Salty-snacks: rescue the 12 basis-error drops from Shufersal real per-100g panels, re-score, re-add"
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-237]
blocks: [TASK-232]
roadmap_impact: true
work_type: data-resource-replacement
owner_signoff: "Owner 2026-06-10: rescue the 12 dropped products from Shufersal rather than accept a 25-product shelf. OFF removal stays LOCAL to salty-snacks (global ban TASK-238 retracted)."
---

# TASK-241 — Rescue the 12 basis-error drops from Shufersal

## Why
TASK-237 re-sourced salty-snacks from real Yochananof panels and dropped 38→25. 12 of those drops
were **per-serving panels mislabeled as per-100g** on their Yochananof pages (kcal 47–132/100g,
unrecoverable there). Owner wants them rescued from Shufersal rather than accept the 34% cut.

## Scope (salty-snacks local; OFF stays removed)
- Read the drop manifest `02_products/salty_snacks/reports/salty_snacks_retailer_drops.json`
  (+ `_meta.dropped_products`). Take the 12 **basis-error** SKUs only (NOT the genuine no-panel
  Calbee import `8851016002685` — leave dropped).
- For each, scrape the REAL per-100g nutrition panel + real Hebrew ingredients from the **Shufersal**
  product page. Shufersal EAN-search returns 0 → use **name-based search** like
  `03_operations/bsip0/scrape/shufersal_frozen_vegetables/02_scrape_shufersal_v2.py`; match by
  name+brand against the manifest, confirm identity.
- **Verify the Shufersal panel is genuinely per-100g** (Atwater check vs stated kcal; reject the
  per-serving artifact). Any product that still can't yield a clean per-100g panel → stays dropped
  (honest). **NO OFF fallback** — OFF stays removed from the salty pipeline.
- Identity/image stay from the existing Yochananof catalog entry (already real); only PANEL +
  INGREDIENTS come from Shufersal for these 12. Mark `panel_source = shufersal_product_page`.
- Re-add to BSIP1, re-score on the UNCHANGED engine, regenerate the corpus.

## Preserve (all TASK-237 gates)
`off_removed=true`; is_clean on every consumer string; confidence↔ingredient consistency; real
images HTTP 200; leakage-clean copy + brand normalization + sodium bar; tsc+build clean.

## Acceptance criteria
- [ ] Each of the 12 recovered with a VERIFIED per-100g Shufersal panel + Hebrew ingredients, or honestly left dropped (report which + why)
- [ ] 0 OFF; no per-serving-mislabeled panel shipped
- [ ] Re-scored on unchanged engine; final shelf size + grade distribution reported
- [ ] All gates pass (is_clean, confidence↔ingredient, images 200, tsc+build)

## Return block
How many of the 12 recovered vs left dropped (+why), final shelf size, grade distribution, panel
source per recovered product, gate confirmation. Do NOT close — RETURN for orchestrator verification.
Hero copy + re-QA are handled by orchestrator AFTER this settles the final shelf.
