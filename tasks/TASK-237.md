---
id: TASK-237
title: "Salty-snacks: REMOVE Open Food Facts — re-source nutrition + ingredients from real Yochananof/Shufersal product-page panels, re-score"
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-228, TASK-231, TASK-234]
blocks: [TASK-232]
roadmap_impact: true
work_type: data-resource-replacement
owner_signoff: "Owner directive 2026-06-10: OFF is not an acceptable nutrition source. Re-source salty-snacks from real retailer panels (scope: salty-snacks only, now). Re-scoring on real data is authorized."
---

# TASK-237 — Remove OFF from salty-snacks; re-source real retailer nutrition

## Why (owner directive)

The salty-snacks v4 corpus took its **nutrition panels from Open Food Facts** (`_meta` provenance:
"Panel: Open Food Facts by real EAN"; BSIP0 = `01_bsip0_off_panels.py`). OFF was the root cause of
EVERY data defect this session: the trans-fat "<1g ÷ serving" artifacts that zeroed products, the
English ingredient text, 3 chips with impossible kcal (128–145/100g, dropped), fabricated 38g
fiber, missing sodium, garbled strings. OFF is crowdsourced/unverified and is **not acceptable** as
the nutrition source for a data-integrity product. Identity + image are already real (Yochananof
catalog, real EAN); only the NUTRITION + INGREDIENTS were OFF.

## Scope (salty-snacks only, now)

Re-source the nutrition panel AND ingredient list for the 38 salty-snacks products from the **real
retailer product pages** — the same way the frozen-vegetables scrape pulled real panels from
Shufersal product pages. **Yochananof is primary** (the corpus identity is already Yochananof; its
product pages carry real Hebrew nutrition + ingredients — reuse `03_operations/bsip0/scrape/
yohananof/03_scrape_yohananof.py` + `parser.py`, and the category scrapers
`02_products/hard_cheeses/scrape_cheeses_yohananof.py` / `juices/scrape_juices_yohananof.py`).
Shufersal product pages (`03_operations/bsip0/scrape/shufersal_frozen_vegetables/02_scrape_shufersal_v2.py`)
are the fallback for any product Yochananof lacks.

- For each of the 38 products: open its real retailer product page (by EAN / Yochananof product
  URL), scrape the real nutrition panel (energy, protein, fat, sat-fat, **trans**, carbs, sugar,
  fiber, sodium) and the real Hebrew ingredient list.
- **Replace** the OFF-sourced BSIP1 nutrition with the retailer-panel values. **Delete OFF from the
  salty pipeline** — no OFF fallback anywhere. Mark `panel_source: retailer_product_page` in provenance.
- For any product whose retailer page genuinely lacks nutrition or ingredients: mark it honestly
  (panel-only / partial per the existing confidence-label convention "חסרים נתוני רכיבים") or drop it
  — **never** fall back to OFF.
- The trans-declaration artifact handling and the manual `data_corrections` from TASK-231/234 are
  moot once real panels replace OFF — but if a real retailer panel shows a genuine "<1g" trans
  declaration, handle it via the engine's existing `threshold_declaration` convention, not a hack.
- Re-run BSIP2 on the real panels (UNCHANGED engine — this is a data re-source, not a scoring
  change). Scores WILL move (real data); that is expected and authorized.

## Preserve (do not regress)

All the copy/quality work already shipped: leakage-clean consumer strings (is_clean gate), no
recommendation language, reworded confidence labels, brand normalization, sodium metric bar, the
confidence-label↔ingredient consistency gate, real images (host api.yochananof.co.il, HTTP 200).

## Acceptance criteria
- [ ] 0 products sourced from OFF; `panel_source = retailer_product_page` for all; OFF code path removed from the salty build
- [ ] Real nutrition + real Hebrew ingredients per product (or honest panel-only/drop; never OFF)
- [ ] Re-scored on the unchanged engine; grade distribution reported (OFF-era vs real-panel)
- [ ] All gates pass: is_clean on every consumer string, confidence↔ingredient consistency, imageUrl 200, tsc + build clean
- [ ] Ingredient coverage reported (how many now have real Hebrew ingredients vs panel-only)

## Return block
Report: shelf size, how many products got real retailer panels vs panel-only vs dropped, the
nutrition+ingredient source per product, grade distribution OFF-era→real, and confirmation OFF is
fully removed from the salty pipeline. Do NOT mark CLOSED — RETURN for orchestrator verification + re-QA.
