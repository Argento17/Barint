---
id: TASK-171H
title: Dossier expansion - widen engine to ~15 tractable actives
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Build ~10 new Evidence Dossiers (tractable single-actives from the coverage-ranked list; DEFER multivitamin+probiotics to the hard-category gate) per methodology v1.3 — incl. the structure_function_umbrella claim-map each. Nutrition+Research, from literature/dsld/pubchem/NIH-ODS/EFSA. All candidate/should_affect_score_now:false; cite all; NEEDS-ENV-VERIFY flags. Measure per-dossier build cost. Target: 5->~15 actives, ~40-55% shelf coverage.
---

# TASK-171H — Dossier expansion to 15 actives

## CLOSED 2026-06-03 — 10 new dossiers, engine now covers 15 actives
**Built (10):** vitamin C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vitamin E, CoQ10.
Dropped **collagen** (contested claim+peptide-spec, difficulty > ~1.5% coverage); built vit E + CoQ10 instead
(probe different failure modes — antioxidant-halo-failed-RCT + clinical-vs-consumer conflation). **Deferred to
hard-gate (notes, not dossiers): multivitamin, probiotics, B-complex** (all need blend/CFU machinery).
**Iron** built with necessity = reader-context-only (Invariant 1, never scored).

**Close-gate verified:** `load_all()` = **16 dossiers** load clean (uncited-umbrella guard still hard-fails);
**golden corpus 17/17** (engine + MVP dossiers untouched, only files added + loader map extended); biotin
umbrella confirmed (all-cosmetic refusals → cap-1 E). Registry `SUPP-EV-007…016` + deferral notes added.

**Standouts:** every `structure_function_umbrella` populated with **13 cited refusals**; **biotin refuses all 4
cosmetic phrases → cap-1 fires (E)** = resolution is a *floor, not a loophole*; **B12 'nerve' MAPS Strong where
magnesium 'nerve' was null** = per-active boundary correct. Coverage ~15–25% → **~40–55%**.

**Maintenance estimate VALIDATED:** measured ~**30–33 h/yr at 15 actives** (inside the 24–40 band; widen set is
settled-vitamin/mineral-heavy so contested fraction came in lower than projected).

## Carried-forward / flagged
- ⚠️ **Citation integrity (material):** first-pass authoring had **~15 mismatched PMIDs** (right topic, wrong id);
  agent caught + corrected all via live `literature` title-check; **zero known-wrong remain.** Recommends a standing
  **"PMID title-check" step in the §5.1 sweep** — the loader hard-fails an *uncited* map but cannot catch a *mis*-cited one. **A real maintenance-integrity signal for the dossier model.**
- `NEEDS-ENV-VERIFY` on every primary UL/safety number (vit C 2000, zinc 40/25, iron 45, calcium 2500, folic 1000mcg, vit E 1000mg/400IU, biotin assay-interference).
- **Per-number Product D7 gate** applies if/when zinc's discrepant UL (NIH 40/EFSA 25) or iron's toxicity-veto touch a published score (none ship now).
- Contested watch: CoQ10 statin-myopathy (Weak, semi-annual sweep, may re-classify); vit E high-dose harm thresholds.

# TASK-171H — Dossier expansion - widen engine to ~15 tractable actives

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
