---
name: project-bsip2-run003
description: "BSIP2 milk_and_alternatives run_003 — fixes applied, scores, and report locations"
metadata: 
  node_type: memory
  type: project
  originSessionId: e98ff19c-3c0d-4e26-8e96-38583f14e9c8
---

Run_003 executed 2026-05-18. Applied two targeted fixes to BSIP2 proto_v0.

**Fix 1 — Beverage liquid gate expansion (category_classifier.py):**
Added three fallback signals to the beverage gate (runs unconditionally now):
- Fallback A (+0.85 boost): `nutrition_basis_claimed` contains "ליטר" or 'מ"ל'
- Fallback B (+0.75 boost): brand field matches `KNOWN_PLANT_MILK_BRANDS` set
- Fallback C (+0.60 boost): plant-milk base term in name + no solid-food exclusion

**Fix 2 — SE gate beverage threshold (constants.py):**
`SE_BEVERAGE_KCAL` lowered from 20.0 → 10.0 to exempt plain plant milks (15 kcal) from catastrophic SE collapse. Diet beverages near 0 kcal still trigger SE.

**Score changes (run_002 → run_003):**
- אלפרו שקדים ללא סוכר (5411188112709): 38.1 E (whole_food_fat) → 43.4 D (beverage) ✓
- אלפרו שיבולת שועל ללא סוכר (5411188124689): 51.4 D (cereal) → 49.1 D (beverage) ✓
- All other 18 products: unchanged ✓ (zero regressions)

**Final hierarchy (run_003):**
- B: 4 dairy milks (75, 75, 75, 73.2)
- C: Plain soy drink 66.1; enriched dairy 58.3; basic soy no-added-sugar 56.2
- D: Almond drink 50.8; oat drinks 49.1–46.6; rice drinks 48.5/47.2; Alpro barista 46.8; Alpro almond 43.4
- E: Go Milk protein 39.5; Alpro soy chocolate 36.2

**Output locations:**
- Run traces: `02_products\milk_and_alternatives\intelligence_bsip2\run_003\products\`
- Run summary: `02_products\milk_and_alternatives\intelligence_bsip2\run_003\reports\run_003_batch_summary.md`
- Presentation reports: `02_products\milk_and_alternatives\reports\run_003_final\`
  - executive_summary.md, full_comparison_report.md, comparison_tables.md
  - website_candidates.md, architectural_outcomes.md, visual_catalog.md
- Visuals (8 PNGs): `02_products\milk_and_alternatives\reports\run_003_final\visuals\`
- Batch runner: `03_operations\bsip2\proto_v0\src\batch_run_milk_003.py`
- Report generator: `03_operations\bsip2\proto_v0\src\generate_run_003_reports.py`

**Why:** SE_BEVERAGE_KCAL=10 was the cleaner fix vs sweetener-based exemption; Alpro almond has "חומרי טעם וריח" which fires flavor_enhancer detection, so sweetener-based exemption wouldn't have helped.

**Remaining issues:** NOVA 4 for "חומרי טעם וריח" (generic flavoring — may be natural); kcal_plausible range penalizes low-kcal beverages (15 kcal < 20 floor triggers confidence deduction). Both deferred.

**How to apply:** Reference these scores and category assignments for any future category comparisons or blog content.
