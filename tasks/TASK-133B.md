---
id: TASK-133B
title: F2 - protein-bar matrix discount + collagen marker in Protein Quality dimension
owner: nutrition-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-01
depends_on: [TASK-133A]
blocks: []
category_id: null
summary: >
  ADOPT (High). Discount the Protein Quality dimension contribution for bar-format + protein_isolate/reconstructed-source products (empirical DIAAS 47-81% of label; use as a conservative band, not per-product). Add collagen marker + extra discount (incomplete AA profile, lowest matrix DIAAS). Coordinate via PROCESSING_LOAD family to avoid double-count with NOVA-4/additive caps. Closes the documented protein-isolate-bar gaming hole.
---

# TASK-133B — F2 - protein-bar matrix discount + collagen marker in Protein Quality dimension

## Plan of record — Phase B (F2, highest value)

Roadmap: [TASK-133_implementation_roadmap.md](../research/TASK-133_implementation_roadmap.md) §Phase B.

- **Code:** add `collagen` marker; wire `matrix_integrity.py` output into the **Protein Quality
  dimension** as a discount; collagen sub-penalty; discount curve in `constants.py`.
- **Key design call:** discount the protein-**quality** contribution only (leave protein mass feeding
  satiety / nutrient density). **Coordinate via the PROCESSING_LOAD family** so it does not double-count
  with the degradation penalty `matrix_integrity.py` already applies to reconstructed products.
- **Validation:** `batch_run_snack_bars_001.py` + matrix case studies — isolate bar drops; hummus /
  Greek yogurt / whey-isolate-in-context unchanged (golden suite §"Protein pudding", §"Whey isolate").
- **DoD:** golden qualitative behavior preserved; isolate bar moves in intended direction; no unintended
  swings on dairy_protein corpus. Size: M.
- **Calibration sign-off:** [DEC-004](../decisions/decisions.json) gates magnitude (discount curve) and scope.

## Implementation status — 2026-06-01 (structural build COMPLETE)

Report: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md).

- **Built:** `collagen` + `RECONSTRUCTED_PROTEIN_MARKERS_HE` detection in `signal_extractor.py`
  (emits `protein_matrix_form`, `has_collagen`); `PROTEIN_QUALITY_MATRIX_DISCOUNT` +
  `PROTEIN_MATRIX_DISCOUNT_BAR_CATEGORIES` in `constants.py` (placeholder ×0.80 reconstructed /
  ×0.55 collagen, DEC-004-gated); `score_protein_quality(nn, l3, category)` applies the
  **quality-only** discount (DEC-004 G2). Protein mass still feeds satiety/nutrient-density.
- **Gaming resistance (Req 3/5):** trigger is **primary-position gated (top 3)** — a trace
  garnish (0.6% soy crisp, 1.5% collagen on a milk base) does not discount the dominant protein.
  Milk powder excluded (not a fraction).
- **Double-count:** F2 is the **sole owner** of the reconstructed-protein penalty in the live
  path; `matrix_integrity.py` degradation is not composited in (no double-count today).
- **Validated:** golden 11 PASS / 1 (pre-existing) WARN / 0 FAIL, no golden score changed.
  Cross-corpora (464 products): **4 changed, 0 grade-flips**; yogurt/milk/bread/hummus = 0
  (in-context whey + frozen milk preserved); clean isolate bar pq 80.8 → 64.6.
## Return block — 2026-06-01 (proposed RETURNED → Controller to record CLOSED)

DEC-004 **DECIDED** (magnitudes ratified: reconstructed ×0.80, collagen ×0.55, quality-only).
Phase E complete: version `0.4.0`; specs synced; **frontend rescore verified as a no-op — F2
changes 0 displayed products on every live page** (the one affected corpus product is not
displayed). DoD met: golden behavior preserved (11 PASS/1 pre-existing WARN/0 FAIL, no golden
score changed); isolate bar moves down (clean isolate pq 80.8→64.6); no dairy_protein swings
(yogurt/milk = 0). Report: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md).
Awaiting Central Controller to record CLOSED.
