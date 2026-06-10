---
id: TASK-241
title: "Salty-snacks: rescue the 12 basis-error drops from Shufersal real per-100g panels, re-score, re-add"
owner: data-agent
status: RETURNED
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

## RETURN (data-agent, 2026-06-10) — RETURNED for orchestrator verification
Recovered **4 of 12** basis-error drops from Shufersal; **8 left honestly dropped**. Final shelf
**29** (was 25). Grades A1/B5/C11/D4/E8, median 56.2. Engine UNCHANGED (data re-source only).

Recovered (panel_source=shufersal_product_page, identity gtin13==barcode, verified per-100g):
- 7290111564291 פריכיות דקות עם קינואה — kcal 390, 67/B
- 9322969000022 פריכיות תירס עם סויה וזרעי פשתן — kcal 391, 74/B
- 7290106574953 בייגלה שטוחים שומשום — kcal 436, 57/C (confidence "partial": Shufersal panel omits fiber — honest)
- 7290112968807 פיטנס קרקר דק סלק — kcal 458, 61/C

Left dropped (no Shufersal page with gtin13 == full barcode; only same-line-different-flavor or
different-barcode collisions — refused to ship a name-only guessed panel): 7290000060071,
7290111564277, 7702024074625, 7290122782615, 7290000070919, 7290000076133, 7290106573314,
7290112965684. (Calbee 8851016002685 no_panel stays dropped, out of scope by design.)

Gates: off_removed=true, is_clean PASS (29/29), confidence↔ingredient PASS, images HTTP 200 (4/4),
brand-norm + sodium-bar PASS, tsc PASS, next build PASS, engine/D4 unchanged.
Run record: 02_products/salty_snacks/reports/run_record_salty_snacks_rescue_task241.json
Hero NOT touched (orchestrator's, per brief).
