---
name: bsip1-enrichment-v1
description: "BSIP1 semantic enrichment sprint — ingredient_enricher.py, fields added, coverage numbers, known limitations"
metadata: 
  node_type: memory
  type: project
  originSessionId: e98ff19c-3c0d-4e26-8e96-38583f14e9c8
---

BSIP1 enrichment v1 completed 2026-05-19. 171 products enriched across 5 runs (run_001/snack_bars, run_cereals_001, run_yogurt_001, run_milk_001, run_milk_002).

**Why:** ingredients_raw and semantic extraction were missing, blocking BSIP2 from reasoning about additive systems, fiber laundering, protein engineering, NOVA evidence, and matrix integrity.

**Files created:**
- `C:\Bari\03_operations\bsip1\core\ingredient_enricher.py` — extraction engine
- `C:\Bari\03_operations\bsip1\core\enrich_runner.py` — batch runner (enriches all runs, generates report)
- `C:\Bari\03_operations\bsip1\core\test_enricher.py` — 64-check test suite (all passing)
- `C:\Bari\03_operations\bsip1\reports\enrichment_validation_001.md` — coverage report

**New fields added to every BSIP1 record:**
- `ingredients_raw` — raw string from BSIP0 or fallback to ingredients_text_he
- `ingredients_raw_provenance` — source, bsip0_status, missing flag
- `ingredient_order` — ordered list [{position, text, percentage_declared, has_subgroup}]
- `extracted_additives` — [{term, category, position}] for emulsifiers, stabilizers, preservatives, colors, raising agents, humectants, glazing agents, etc.
- `extracted_flavors` — [{term, category}] including flavor_descriptor ("בטעם") for routing suppression
- `extracted_sweeteners` — [{term, category, position}] sugars, syrups, polyols, intense sweeteners
- `extracted_protein_markers` — [{term, category, position}] whey, casein, soy isolate, pea protein, etc.
- `extracted_matrix_markers` — [{term, category}] flour, starch, puffed, flakes, maltodextrin
- `extracted_fermentation_markers` — [{term, category}] cultures, yeast, sourdough
- `extracted_roasting_markers` — [{term, category}] roasted, baked, toasted
- `enrichment_summary` — convenience counts + boolean flags (has_live_cultures, has_flavor_descriptor, has_prebiotic_fiber, has_protein_isolate_or_concentrate)
- `enrichment_version` — "bsip1_enrichment_v1"
- `enrichment_warnings` — list of issues encountered

**Coverage summary:**
- Raw ingredient text: 167/171 (97%)
- From BSIP0 scrape: 44/171 (25%) — only Yohananof snack_bars have BSIP0 source
- BSIP1 text fallback: 123/171 (71%)
- Missing completely: 4/171 (2%) — 4 snack bars with no ingredient text in any source
- Products with additives: 87/171 (50%)
- Products with sweeteners: 108/171 (63%)
- Products with fermentation markers: 45/171 (26%)
- Products with protein markers: 38/171 (22%)

**Known limitations:**
- Nested sub-ingredient position attributed to parent item position
- Homonym terms (e.g., "קרמל") may be color or flavor — BSIP2 must add context logic
- Only Yohananof indexed in BSIP0; other retailers use text fallback
- E-number dash variants (E-322 vs E322) both covered but other formatting variants may miss
- "has_protein_isolate_or_concentrate" is 0/171 — no Israeli product explicitly uses "מרוכז"/"בידוד" labels yet

**How to apply:** When BSIP2 needs additive/sweetener/protein/matrix signals, read from enriched BSIP1 JSONs. The `enrichment_summary` flags are convenience shortcuts. Run `enrich_runner.py` again after any new BSIP1 run to keep all records current.

**Next sprint per user:** Matrix Integrity implementation → Router v2 hardening → regression reruns.
