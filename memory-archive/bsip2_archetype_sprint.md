---
name: bsip2-archetype-sprint
description: "Structural Class Stability + Regression Framework sprint (2026-05-20) — deliverables, key findings, known gaps. NOTE: originally called 'archetype' but renamed to 'structural class' to avoid collision with BSIP2 v3 archetype term."
metadata: 
  node_type: memory
  type: project
  originSessionId: 88339fa2-f552-455b-8eed-95c12c9cad01
---

Sprint completed 2026-05-20. Structural class infrastructure is live across all 4 categories (163 products).

## Terminology Note

"Archetype" is a reserved term in BSIP2 v3 — it means the scoring interpretation context (cereal_system, dairy_liquid, snack_bar, yogurt_system, beverage, whole_food_fat). The A-F behavioral classes were renamed to "structural class" to avoid conceptual debt.

## Deliverables

**New engine module:**
- `src/structural_classifier.py` (MODULE_VERSION = structural_classifier_v1)
  - 6 structural classes: A (Intact Whole Food), B (Lightly Transformed Traditional), C (Mechanically Fragmented), D (Industrially Reconstructed), E (Engineered Wellness System), F (Structurally Void System)
  - Soft assignment: primary + secondary with confidence weights
  - Reads: nova_proxy, dimension_scores (additive_quality, whole_food_integrity, protein_quality), L1/L3 signals
  - Key E vs F discriminator: protein_quality >= 35 → E boost; sweetener + low_pq → F boost
  - Return fields: primary, primary_label, primary_confidence, secondary, secondary_label, secondary_confidence, class_weights, is_between_worlds, classification_notes, classifier_version

**Golden Corpus:**
- `01_framework/bsip2_framework/validation/golden_corpus/golden_corpus_manifest.json`
- 12 entries: 6 real products (milk run_004), 6 signal bundles
- Corpus fields: `expected_structural_class`, `structural_class_rationale`
- Regression result: 11 PASS, 1 WARN (soy drink legitimately between B-C)

**Regression runner:**
- `src/run_regression_check.py` → `03_operations/reports/regression/regression_check_001.md`

**Structural class coherence report:**
- `src/generate_structural_report.py` → `03_operations/reports/structural_class_report_001.md`

**All 4 batch runners** integrated: `trace["structural_class"] = classify_structural_class(trace)` after assemble_trace.

## Key Findings from First Run (163 products)

| Structural Class | Count | Score Range | Mean |
|-----------------|-------|-------------|------|
| A (Intact) | 22 | 60–90.7 | 84.1 |
| B (Traditional) | 19 | 49.4–81.1 | 62.9 |
| C (Fragmented) | **0** | — | — |
| D (Industrial) | 71 | 24.9–75.8 | 55.8 |
| E (Wellness) | 24 | 13.4–64.1 | 37.5 |
| F (Void) | 27 | 15.6–61.5 | 34.6 |

## Known Gaps

1. **Structural class C is empty** — No products classified as Mechanically Fragmented. Corpus lacks nut butters, stone-ground products, compressed whole-food bars. Expected to populate when bread/crackers category is added.

2. **Vitariz rice drink classified as B** — NOVA proxy doesn't detect rice enzymatic hydrolysis, so rice drink = NOVA 2 = structural class B. True structural classification should be D. Corpus entry documents this as a sentinel for future NOVA proxy fix.

3. **High between-worlds rate** — 111/163 products show meaningful secondary structural classes. Normal for food products on spectrums; may indicate some boundary tightening needed.

**Why:** Ontology is becoming the moat. Need stability infrastructure before adding bread/crackers category.

**How to apply:** Run `run_regression_check.py` after every engine change. Run `generate_structural_report.py` after any batch re-run. Monitor structural class C population when bread is added.
