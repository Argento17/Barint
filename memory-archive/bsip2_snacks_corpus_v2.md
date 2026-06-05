---
name: bsip2_snacks_corpus_v2
description: "Snacks CE corpus v2 — 18-product corpus, E-01/02/03 improvements applied 2026-05-30, updated scores in both frontend files"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Snacks comparison page (`/hashvaot/snacks`) is now product-live with 18 CE-approved products. Build date: 2026-05-29.

**Why:** Prior corpus had 14 displayable products from a 48-scored BSIP2 run. Two removed for quality (snk-008 near-duplicate, snk-014 unverifiable), six added for editorial coverage.

**How to apply:** Any future snacks corpus changes follow same editorial selection criteria: ≥7pt gap between near-duplicates, traceable to BSIP2 run data, no children's products (Section 2.8 rule).

## Corpus Summary

- Scraped: 53 | Scored: 48 | Displayed: 18
- Score range: 17–70 | Only B grade: snk-001 (70)
- E-grade products: snk-006 (17), snk-007 (29), snk-013 (17), snk-020 (33)
- Source run: yochananof_snack_retail_v1
- RC-01 recalibration applied 2026-05-30: snk-015 score 55→63 (SC-2 natural sugar relief); now 2nd place (was 4th)
- E-01/02/03 improvements applied 2026-05-30 (see section below); 9 products updated

## E-01/02/03 Scientific Improvements (2026-05-30)

Three scoring improvements implemented in `constants.py`, `signal_extractor.py`, `score_engine.py`:

**E-01 Sweetener Tier Classification**: Replaced flat `SWEETENER_CAP=70 / penalty=15` with 3-tier system. Tier A (stevia/monkfruit/thaumatin) cap=75/penalty=8; Tier B (sugar alcohols) cap=73/penalty=10; Tier C (synthetic) cap=70/penalty=15. Worst tier present dominates.

**E-02 Fermentation Quality Signal**: +5 bonus to `whole_food_integrity` when `has_fermentation=True`. No products in snacks corpus triggered this (fermentation is bread-relevant).

**E-03 Fortification Discount**: 0.80 multiplier on `nutrient_density` raw score when `has_fortification=True` (explicit "מועשר"/"מחוזק" language OR ≥2 distinct synthetic vitamins). Triggered on several fitness/cereal-style bars.

Score changes in corpus (old→new, both files updated):

| Product | Old | New | Driver |
|---|---|---|---|
| snk-002 | 56 | 57 | stale sync |
| snk-004 | 58 | 59 | stale sync |
| snk-007 | 29 | 28 | E-03 fortification discount |
| snk-010 | 45 | 46 | stale sync |
| snk-011 | 43 | 44 | stale sync |
| snk-013 | 13 | 17 | stale sync |
| snk-018 | 46 | 44 | stale sync |
| snk-019 | 41 | 40 | stale sync |
| snk-020 | 32 | 33 | stale sync |

snk-013 `key_observation_he` updated: removed "הציון הנמוך ביותר בקטגוריה:" prefix (now ties snk-006 at 17).
No grade changes — all products remain in same letter tier.

## RC-01 Recalibration (2026-05-30)

Natural whole-fruit sugar relief implemented in `score_engine.py`. For SC-2 products (NOVA1-2, no added sugar, whole fruit primary):
- `SNACK_BAR_RED_SUGAR_LABEL`: 55 → 63
- `ISRAELI_RED_LABEL_1_SUGAR`: 55 → 63
- `HIGH_SUGAR_25G_PLUS`: 60 → 68

Only product affected in current corpus: snk-015 (47.6g sugar, all from dates, 4 ingredients).

## Files

| File | Role |
|---|---|
| `src/data/comparisons/snacks_frontend_v2.json` | BariProductVM corpus (canonical) |
| `src/lib/comparisons/snack-page-data.ts` | Filter metadata, cluster data, stats |
| `src/lib/comparisons/snack-types.ts` | SnackFilterId, SnackClusterId types |
| `src/lib/comparisons/snacks-shelf-filters.ts` | Shelf lens derivation |
| `src/lib/blog/snack-analysis-content.ts` | Methodology lines |
| `src/lib/comparisons/snacks-comparison-page-data.ts` | Page assembly, prologue |
| `src/components/snack/snack-shelf-stat-bar.tsx` | Stat bar UI |

## Filter System (v2)

4 shelf lens options (NOVA-free):
- "date-based" → תמרים/טבעי (5 products)
- "oat-cereal" → שיבולת שועל ודגנים (7 products)
- "wellness" → מיצוב בריאות (10 products)
- "grade-e" → ציון E (4 products)

Removed: nova2/nova3/nova4/whole-base/multi-sweeteners/additives-5-plus/protein/fitness filter IDs.

## Expansion Schema

All 18 products have: positiveSignals, limitingFactors (new), bottomLine, comparisonContext.
Nutrition fields remain null (BSIP2 data gap — requires ingredient scrape).

## NOVA Cleanup

NOVA terminology removed from: insightLine, key_observation_he, explainability_tags, legend, glossary, filters, stat bar.
Retained in engine/blog route only (filter-panel.tsx, snack-product-detail.ts, map-section.tsx).

## CE Handoff

`C:\Bari\02_products\snack_bars\reports\snacks_ce_handoff_v2.md`

[[governance_maturity_v1]]
[[bsip2_snack_bars_001]]
