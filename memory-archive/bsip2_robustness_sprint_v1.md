---
name: bsip2-robustness-sprint-v1
description: "BSIP2 Robustness & Uncertainty Sprint v1 — corpus, results, new modules, report locations"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Sprint completed 2026-05-25. Stress-tested BSIP2 against 50 synthetic "noisy reality" products.

**Why:** BSIP2 ontology sophistication was advancing faster than operational robustness. Sprint validates the pipeline survives messy real-world food data before API/public launch.

**How to apply:** When touching scoring, routing, or confidence logic, re-run `run_robustness_sprint.py` to validate regressions against the noisy corpus. Add new corner cases to `create_robustness_corpus.py` as new product types are added.

## New modules created

- `interpretation_confidence.py` — 5-band confidence system (very_high/high/moderate/low/insufficient_context) with router stability input and Hebrew narrative generation
- `failure_taxonomy.py` — 10-category failure classification (OCR_DEGRADATION, SEMANTIC_AMBIGUITY, CATEGORY_LEAKAGE, MISSINGNESS, RETAILER_INCONSISTENCY, ONTOLOGY_GAP, WEAK_SUPPRESSION, CONFIDENCE_OVERSTATEMENT, INGREDIENT_TRUNCATION, HYBRID_CONFLICT)
- `graceful_degradation.py` — 4-level degradation (FULL/CAUTIOUS/UNCERTAINTY/INSUFFICIENT) with score range and grade provisional flags
- `create_robustness_corpus.py` — 50-product corpus generator (Groups A–H)
- `run_robustness_sprint.py` — main runner generating all 8 reports

## Corpus: robustness_corpus_001.json

Location: `C:\Bari\03_operations\bsip2\proto_v0\src\robustness_corpus_001.json`

50 products, 8 groups:
- A (5): Clean baselines — all route correctly
- B (8): Missing/partial nutrition — B5 (all-null nutrition) → INSUFFICIENT
- C (8): Missing/corrupted ingredients — C6/C7 OCR severe → degraded
- D (8): Routing instability — borderline categories
- E (8): Claim vs reality — marketing gap detection
- F (5): Missing identity fields — empty name, null barcode
- G (4): Data consistency failures — impossible nutrition values
- H (4): Hybrid/edge cases — protein powder, cheese bread

## Sprint results

- **50/50 products**: 0 pipeline errors
- **Routing accuracy**: 42/50 (84%)
- **Degradation breakdown**: FULL=36 (72%), CAUTIOUS=9 (18%), UNCERTAINTY=3 (6%), INSUFFICIENT=2 (4%)
- **Total failure instances**: 71 across 50 products (avg 1.4/product)

### Key routing failures found

| ID | Expected | Got | Reason |
|:---|:---------|:----|:-------|
| C7 | snack_bar_granola | whole_food_fat | Severe OCR destroys all snack signals; nut tokens dominate |
| D3 | snack_bar_granola | cracker | Hard anchor 'קרקר' overrides sweet cracker signals (anchor wins correctly) |
| D4 | snack_bar_granola | cereal | 'שיבולת שועל' + 'עוגיות ביסקוויט' → cereal wins over snack |
| F3 | cereal | snack_bar_granola | Vague name, no hard anchor; grain signals route to snack |
| G3 | snack_bar_granola | dairy_protein | Protein powder → mig (whey) triggers dairy routing |
| G4 | snack_bar_granola | dairy_protein | Same issue; no protein_powder category defined |
| H1 | snack_bar_granola | cereal | 'גרנולה לבוקר' hard anchor correctly fires; expectation was wrong |

### Confidence band behavior validated
- OCR-corrupted products correctly drop to moderate/low bands
- Impossible data (sugar > carbs) correctly triggers UNCERTAINTY degradation
- All-null nutrition correctly reaches INSUFFICIENT
- Clean products with full data reach very_high or high

## Reports generated (8)

Location: `C:\Bari\03_operations\reports\robustness\`

- `robustness_validation_001.md` — Full summary table + overall metrics
- `uncertainty_behavior_001.md` — Band distribution + confidence drop analysis
- `noisy_corpus_failures_001.md` — Failure taxonomy breakdown per product
- `routing_under_noise_001.md` — Router stability expected vs actual
- `missingness_resilience_001.md` — Missing field impact analysis
- `confidence_distribution_001.md` — Band distribution + ceiling applications
- `ambiguity_patterns_001.md` — Hybrid/instability product behavior
- `retailer_noise_examples_001.md` — Concrete worst-case case studies

## Open gaps identified by sprint

1. **ONTOLOGY_GAP: protein powder** — G3/G4 route to dairy_protein because whey triggers dairy signals. A dedicated `protein_supplement` category or anchor needed.
2. **OCR_DEGRADATION: C7** — Severe symbol noise destroys all snack signals; nut tokens from ingredient list contaminate to WFF. May need character-class sanitization before signal extraction.
3. **D3 anchor tension** — 'קרקר' hard anchor overrides sweet-cracker context; hybrid detection should widen to include `cracker+dessert` pair.
4. **Grade ceiling map** — moderate band caps grade at B; some high-quality bread products (C1=80.8) get capped. May need per-category ceiling relaxation for bakery.

[[bsip2_bread_light_sprint]]
[[bsip2_synthesis_calibration_v1]]
