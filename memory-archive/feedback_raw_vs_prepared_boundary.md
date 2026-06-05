---
name: feedback_raw_vs_prepared_boundary
description: "Category-boundary test for hummus/spreads — prepared vs raw is decided by tahini+sodium+energy, NEVER protein or the word \"סלט\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d712d892-9d66-49e2-833b-3e97e740d2bc
---

When deciding whether a product belongs on a *prepared spread* comparison shelf (hummus etc.),
do NOT exclude something for high protein or for being named "סלט" (salad). A thick tahini-based
chickpea salad is still hummus and stays.

**Why:** On TASK-137A I proposed excluding `סלט חומוס` (80/A) on a protein-only read (18.2 g) —
wrong. The Product Owner corrected it twice: "DO NOT EXCLUDE HUMUS SPREADS/SALAD", then "chickpeas
are in every hummus — make sure it's not RAW CHICKPEAS in the list." The real defect was two
raw/dry chickpea items (`bsip1_1990261`, `bsip1_3643714`, "חומוס" 73/B) mis-tagged `hummus_spread`.

**How to apply:** The boundary test is *prepared vs raw*, decided by:
- **Tahini** present → prepared (keep). Absent → suspect raw.
- **Sodium** 300–480 mg/100g → prepared (salted). ~0–15 mg → raw/dry (unsalted).
- **Energy** 250–290 kcal/100g → prepared (water/oil diluted). 360–390 kcal → dry legume.
- **Protein is NOT a boundary signal** (a thick salad legitimately reaches ~18 g).

Raw chickpeas = same exclusion class as the existing `EXCLUDED_NOVA1_IDS` (TASK-069). Mechanism:
`EXCLUDED_RAW_CHICKPEA_IDS` in `hummus-comparison-page-data.ts`. Counts auto-derive from the
displayed set. Carry this discriminator to every category boundary call (see [[bari_comparison_governance_v1]],
[[bari_usecase_guardrails_v2]]). Part of [[project_hummus_137]].
