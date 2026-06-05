---
name: bsip2-matrix-integrity-v1
description: "BSIP2 Matrix Integrity Engine — v1 baseline + v2 calibration sprint outcomes, algorithm design, file locations, validation numbers"
metadata: 
  node_type: memory
  type: project
  originSessionId: 88339fa2-f552-455b-8eed-95c12c9cad01
---

Matrix Integrity Engine v2 (calibration sprint) completed 2026-05-20.
V1 implemented same day and archived immediately for comparison.

**Files:**
- `C:\Bari\03_operations\bsip2\proto_v0\src\matrix_integrity.py` — v2 engine (current)
- `C:\Bari\03_operations\bsip2\proto_v0\src\matrix_integrity_v1_archive.py` — v1 kept for comparison
- `C:\Bari\03_operations\bsip2\proto_v0\src\run_matrix_validation.py` — v1 validation runner
- `C:\Bari\03_operations\bsip2\proto_v0\src\run_matrix_validation_v2.py` — v2 comparison runner
- `C:\Bari\03_operations\bsip2\reports\matrix_integrity_validation_001.md` — v1 baseline report
- `C:\Bari\03_operations\bsip2\reports\matrix_integrity_calibration_v2.md` — v1 vs v2 comparison

**MODULE_VERSION:** `matrix_integrity_v2`

---

## v2 Algorithm Design (7-component model)

Unchanged from v1:
1. **Matrix degradation** (0–55 pts pull via ×0.55): position-weighted degradation from `extracted_matrix_markers`. Same scores as v1.
2. **Structural void penalty** (+22 pos1, +12 pos2): refined syrup/sugar in primary position.
3. **Fermentation credit** (0–0.40 factor): reduces degradation. live_cultures → 0.40 cap.

New in v2:
4. **Supplemental mechanical scan**: Scans `ingredient_order` texts directly for Hebrew patterns not in MATRIX_TERMS. Produces virtual signals merged into degradation. Patterns: שיבולת שועל=6, פתיתי=10, גרנולה=16, מוזלי=8, פופקורן=52. Suppressed at positions where a matrix_marker already fired.
5. **Assembly complexity drag** (0–12 flat penalty): step function by ingredient count (n≤2→0, n≤4→1, n≤6→2.5, n≤9→4.5, n≤12→6.5, n≤15→8.5, n>15→up to 11) + diversity bonus. Breaks the 100 ceiling for assembled whole-food products.
6. **Engineering intensity** (0–30 pts via ×0.30): same composite formula. Fortification now context-aware: `basic_restoration` (≤10 pts) vs `wellness_engineering` (up to 28 pts, fires when isolates+prebiotic_fiber+sweetener stacking co-occur). wellness_engineering not yet seen in current 4 categories.
7. **HP reconstruction** (0–15 pts via ×0.15): same base triads. v2 additions: position weighting (early sweetener+flavor → ×1.1-1.2), dense additive amplification (≥4 types → ×1.15), matrix weakness amplification (degradation≥50+HP≥40 → ×1.12), false-positive suppression (single flavor on clean matrix → ×0.5).

**Score formula:**
`score = 100 − adjusted_degradation×0.55 − engineering_intensity×0.30 − hp_score×0.15 − assembly_drag`

**New trace fields in v2:**
- `supplemental_signals`, `supplemental_provenance` — soft transform scan results
- `assembly_drag` — flat drag applied
- `fortification_type` — "none" / "basic_restoration" / "partial_compensation" / "wellness_engineering"
- `transformation_type` — "minimal_transformation" / "traditional_transformation" / "mechanical_degradation" / "industrial_restructuring" / "reconstruction_compensation"
- `provenance` — dict with `degradation_signals`, `engineering_signals`, `compensation_signals`, `protective_signals`, `assembly_drag_note` as human-readable string lists

---

## Calibration Results (v1 → v2, 163 products)

**Score compression reduced:**
- Products at 100: 51 → 24 (−27)
- Products at ≥95: 71 → 51 (−20)

**Distribution shift:**
- 90-100 (minimal): 89 → 75 (−14)
- 75-89 (low): 22 → 29 (+7)
- 40-57 (high): 14 → 29 (+15)

**Per-category averages (v1 → v2):**
- snack_bars: 70.6 → 61.5 (−9.0 avg, max still 100)
- cereals: 85.7 → 80.0 (−5.7 avg)
- yogurt: 96.6 → 94.8 (−1.9 avg, plain yogurts still 100)
- milk: 96.8 → 93.4 (−3.3 avg, oat drinks now ~94)

**Gradient realism:**
- Rolled oats (שיבולת שועל): 100 → 96.7 ✓ (target 94-97)
- Overnight oat base with seeds: 100 → 96.1 ✓
- Muesli bircher base: 100 → 94.7 ✓ (target 88-94)
- Granola with honey+nuts: 100 → 94.4 ✓ (target 78-88)
- Date/nut bar (2-4 ingredients): 100 → 99.0 ✓

**Traditional foods correctly protected:**
- Plain yogurt (1.5%, 3%, Greek, goat): still 100
- Laban drinkable 3%: still 100
- Soy yogurt natural: still 100
- Simple flavored yogurt: 100 → 98.6 (drag 1.4 only)

**HP amplification on ultra-processed bars:**
- Diet crispy bars (glucose syrup + sweetener + flavor + emulsifier): HP 45→64, 75→100
- Fitness grain snacks with early sweeteners: HP 85→100

**Fortification nuance:** All current products = basic_restoration. wellness_engineering prepared but awaiting protein shake / sports bar categories.

**Only one product gained score (expected rare):**
- יוגורט שיבולת שועל +0.9: HP false-positive suppression fired, previously over-penalized for simple flavor.

---

## Position Weight Function (unchanged)
1.0 / 0.82 / 0.68 / 0.55 / 0.44 / 0.35 / 0.28 / 0.22 / 0.17 / 0.13 / decaying to 0.08

## Output Fields (unchanged interface)
- `matrix_integrity_score` (0–100)
- `reconstruction_depth` (0–5)
- `structural_degradation_level` (minimal/low/moderate/high/severe/extreme)
- `engineering_intensity` (0–100)
- `compensation_signals` (list, now includes fortif_type suffix)
- `dominant_matrix_signals` (list, soft signals tagged [soft])
- `integrity_summary` (string, now includes assembly drag + transform type)
- `matrix_integrity_trace` (dict, expanded)

## Known Limitations (updated)
- Supplemental scan vocabulary is Hebrew-only and limited (6 patterns). Needs expansion for bread/cracker sprint.
- "wellness_engineering" fortification untested on real products — awaits sports bar category.
- Assembly drag is flat step function; no position sensitivity.
- Extrusion/expansion still invisible (hidden process limitation).
- Fermentation credit is categorical, not quantitative.

## Next Steps
- Bread/crackers will be the stress-test category: flour semantics + sourdough ambiguity + seed laundering + fiber enrichment + artisanal halos.
- Before bread: Router v2 hardening.
- Feed `matrix_integrity_score` + `transformation_type` into BSIP2 L1 as structural signals.
