---
id: TASK-133B
title: F2 - protein-bar matrix discount + collagen marker in Protein Quality dimension
owner: nutrition-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-01
blocker: "waiting on TASK-133A (named-additive/fragmentation taxonomy)"
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
