# BSIP2 Regression Check Report

**Run date:** 2026-06-05 16:39 UTC
**Corpus version:** v1
**Classifier:** structural_classifier_v1
**Overall status:** WARN

| Status | Count |
|--------|-------|
| PASS   | 11     |
| WARN   | 1     |
| FAIL   | 0     |
| SKIP   | 0     |
| TOTAL  | 12    |

---

## Results by Entry

### ✓ `anchor_whole_milk_tnuva` — PASS

**Plain whole dairy milk — single ingredient, 3.4% fat, no additives**  
Type: real_product | Score: 85 | NOVA: 1 | Structural class: **A** (expected: A)
Expected score band: 70–100
Class weights: `A=0.83  |  B=0.17  |  C=0.00  |  D=0.00  |  E=0.00  |  F=0.00`

### ✓ `anchor_oat_drink_oatly` — PASS

**Oatly oat drink — oat base with gums and emulsifiers, industrially homogenized**  
Type: real_product | Score: 50.7 | NOVA: 3 | Structural class: **D** (expected: D)
Expected score band: 35–65
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.06  |  B=0.20  |  C=0.31  |  D=0.35  |  E=0.08  |  F=0.00`

### ⚠ `anchor_soy_drink` — WARN

**Soy drink — soy protein base with regulators/emulsifiers**  
Type: real_product | Score: 67.0 | NOVA: 2 | Structural class: **B** (expected: C)
Expected score band: 52–78
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.29  |  B=0.49  |  C=0.22  |  D=0.00  |  E=0.00  |  F=0.00`

**Issues:** WARN: structural_class=B (expected C, but acceptable as secondary)

### ✓ `anchor_protein_drink_go_milk` — PASS

**Go Milk high-protein drink — added whey/isolate, fortified**  
Type: real_product | Score: 41.4 | NOVA: 4 | Structural class: **E** (expected: E)
Expected score band: 25–55
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.03  |  B=0.04  |  C=0.02  |  D=0.12  |  E=0.43  |  F=0.35`

### ✓ `anchor_almond_drink_alpro` — PASS

**Alpro almond drink — almond base with gums, stabilizers, vitamins**  
Type: real_product | Score: 45.3 | NOVA: 4 | Structural class: **D** (expected: D)
Expected score band: 30–58
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.05  |  B=0.05  |  C=0.02  |  D=0.32  |  E=0.24  |  F=0.32`

### ✓ `anchor_rice_drink_vitariz` — PASS

**Vitariz rice drink — rice base with vitamins, minimal structure**  
Type: real_product | Score: 49.4 | NOVA: 2 | Structural class: **B** (expected: B)
Expected score band: 35–65
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.26  |  B=0.48  |  C=0.24  |  D=0.02  |  E=0.00  |  F=0.00`

### ✓ `concept_plain_yogurt_clean` — PASS

**Plain fermented yogurt — milk + live cultures, no additives**  
Type: signal_bundle | Score: None | NOVA: 2 | Structural class: **B** (expected: B)
Expected score band: 78–100
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.26  |  B=0.45  |  C=0.20  |  D=0.00  |  E=0.08  |  F=0.00`

### ✓ `concept_rolled_oats_pure` — PASS

**Pure rolled oats — single grain, mechanically flattened, no additives**  
Type: signal_bundle | Score: None | NOVA: 2 | Structural class: **B** (expected: B)
Expected score band: 88–100
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.30  |  B=0.43  |  C=0.19  |  D=0.00  |  E=0.08  |  F=0.00`

### ✓ `concept_date_nut_bar_clean` — PASS

**Clean date-nut bar — dates + nuts, no additives, no added sugar**  
Type: signal_bundle | Score: None | NOVA: 2 | Structural class: **B** (expected: B)
Expected score band: 72–95
Class weights: `A=0.24  |  B=0.45  |  C=0.22  |  D=0.02  |  E=0.08  |  F=0.00`

### ✓ `concept_protein_bar_with_isolates` — PASS

**Protein bar with isolates — whey isolate, additives, sweeteners, fortification**  
Type: signal_bundle | Score: None | NOVA: 4 | Structural class: **E** (expected: E)
Expected score band: 25–60
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.00  |  B=0.00  |  C=0.00  |  D=0.21  |  E=0.50  |  F=0.28`

### ✓ `concept_sweetened_puffed_cereal` — PASS

**Sweetened puffed cereal (Nesquik-type) — extruded, sugar-coated, NOVA4**  
Type: signal_bundle | Score: None | NOVA: 4 | Structural class: **F** (expected: F)
Expected score band: 20–50
⚠ Between-worlds product (strong secondary structural class)
Class weights: `A=0.00  |  B=0.00  |  C=0.03  |  D=0.29  |  E=0.23  |  F=0.45`

### ✓ `concept_plain_whole_nuts` — PASS

**Plain whole nuts — single ingredient, no processing**  
Type: signal_bundle | Score: None | NOVA: 1 | Structural class: **A** (expected: A)
Expected score band: 85–100
Class weights: `A=0.75  |  B=0.15  |  C=0.00  |  D=0.00  |  E=0.10  |  F=0.00`


---

## Between-Worlds Products (Ontology Tension Zones)

These products express two structural classes strongly. They are valuable calibration anchors.

- `anchor_oat_drink_oatly` (D): weights = {'A': 0.057, 'B': 0.199, 'C': 0.306, 'D': 0.355, 'E': 0.083, 'F': 0.0}
- `anchor_soy_drink` (B): weights = {'A': 0.286, 'B': 0.494, 'C': 0.22, 'D': 0.0, 'E': 0.0, 'F': 0.0}
- `anchor_protein_drink_go_milk` (E): weights = {'A': 0.033, 'B': 0.045, 'C': 0.021, 'D': 0.116, 'E': 0.434, 'F': 0.351}
- `anchor_almond_drink_alpro` (D): weights = {'A': 0.051, 'B': 0.051, 'C': 0.019, 'D': 0.319, 'E': 0.241, 'F': 0.319}
- `anchor_rice_drink_vitariz` (B): weights = {'A': 0.257, 'B': 0.485, 'C': 0.24, 'D': 0.018, 'E': 0.0, 'F': 0.0}
- `concept_plain_yogurt_clean` (B): weights = {'A': 0.262, 'B': 0.454, 'C': 0.202, 'D': 0.0, 'E': 0.082, 'F': 0.0}
- `concept_rolled_oats_pure` (B): weights = {'A': 0.301, 'B': 0.426, 'C': 0.191, 'D': 0.0, 'E': 0.082, 'F': 0.0}
- `concept_protein_bar_with_isolates` (E): weights = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.211, 'E': 0.504, 'F': 0.285}
- `concept_sweetened_puffed_cereal` (F): weights = {'A': 0.0, 'B': 0.0, 'C': 0.03, 'D': 0.287, 'E': 0.234, 'F': 0.449}