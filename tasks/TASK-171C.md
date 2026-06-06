---
id: TASK-171C
title: Phase 2 - SIE engine prototype + golden-corpus validation
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Build the supplement scoring engine (5-dim scorer + caps/vetoes + dose short-circuit + binding-constraint attribution + structured trace) per methodology_v1.md v1.2, in 03_operations/supplement_engine/proto_v0/src/. Build golden corpus (per-dimension anchors + 3 attribution archetypes) and validation runner; calibrate candidate weights/thresholds until each fixture lands in its expected grade AND the binding constraint is correctly attributed (esp. the inverted-E pair). Reads in-house dossiers/labels only (EDPG). All numbers candidate/calibration-pending; nothing ships. Nutrition D8-verifies.
---

# TASK-171C — Phase 2 - SIE engine prototype + golden-corpus validation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Deliverable (2026-06-03, Data Agent) — proposing RETURNED

Built the SIE engine prototype + golden corpus + validation harness per
`methodology_v1.md` v1.2; calibrated until all fixtures pass grade + attribution.
All numbers CALIBRATION-PENDING; nothing shipped; no published score; separate tree
(no BSIP2 imports/shared constants — firewall held). Pending **Nutrition D8**
implementation-verification.

**Files built** (`03_operations/supplement_engine/proto_v0/`):
- `src/constants.py` — 5-dim weights, grade bands, all §3.2 caps/floors/veto thresholds, every value `# CALIBRATION-PENDING`
- `src/dossier_loader.py` — loads + validates the 5 in-house dossiers (EDPG firewall)
- `src/supplement_label.py` — in-house label model (BSIP0-S analogue)
- `src/score_engine.py` — 5 dimension scorers, dose short-circuit (§2.2), §3 blend over applicable dims, §3.2 caps/veto most-restrictive-wins, §12 binding-constraint identification
- `src/trace_writer.py` — §12.2 structured trace (Dose N/A explicit, one binding_constraint, SUPP-EV refs, no consumer prose)
- `golden_corpus/fixtures.py` — 11 §6 anchors + 3 §13 archetypes
- `run_golden_validation.py` — scores all, asserts grade + binding + inverted-E test
- `reports/phase2_calibration_v1.md`, `reports/phase2_validation_v1.md`
- `golden_corpus/traces/*.json` — 14 emitted traces

**Result:** 14/14 fixtures pass grade band AND binding constraint. Inverted-E pair
(no-evidence `cap_1` vs dangerous `veto_safety`) never confused — PASSED.

**Flagged for Nutrition D8** (not silently deviated): FLAG-1 Weak evidence has no
cap (otherwise-excellent Weak product lands B); FLAG-2 magnesium dossier tension
(`min_effective` 300 > governing UL 250 elemental — adequately-dosed Mg breaches the
UL); FLAG-3 safety-neutral blend value (70) genuinely arbitrary, needs SUPP-EV.

## Nutrition D8 verification (2026-06-03, nutrition-agent)
**D8 VERDICT: implementation MATCHES the v1.2 spec — no deviations.** Independently ran the
validation (14/14) and inspected code against §2.1–2.5/§3/§12: dose short-circuit (Insufficient→Dose
N/A, dropped from denominator not 0), binding-constraint = dominant-limiting-dimension fallback (not
lowest raw sub-score), most-restrictive-wins — all confirmed in code, not just in passing. Inverted-E
pair distinct. Confirmed the Data Agent's correctness fix (Safety compares UL on the same elemental+
per-day basis — prior raw-compound-vs-elemental compare was a real bug).
**Flag rulings:** FLAG-1 → no cap, B is correct (Weak = one-axis compromise per §4; no rule change, no
D7). FLAG-2 → graded-Safety revision (hard veto → NIH/IOM 350; EFSA 250 reversible-GI → Safety NOTE);
edited `score_engine.py`/`constants.py`/`trace_writer.py`/`magnesium.yaml`; re-validated 14/14 green.
FLAG-3 → principled direction recorded, deferred to SUPP-EV-006 (no fixture impact). FLAG-1/FLAG-3 are
carried-forward calibration items, not close blockers.

## Product D7 co-sign — FLAG-2 (2026-06-03, product-agent)
**CO-SIGNED** as a **standing meta-rule** (not Mg-only): hard Safety veto reserved for toxicity/harm
ceilings; reversible self-limiting tolerance thresholds (GI/osmotic) → graded Safety NOTE band.
Supersedes the prior "most-conservative-tolerance governs the veto" ruling. Guardrail: reversible-vs-
toxicity classification is a dossier-level, Nutrition-owned, cited judgement — engine never infers it.
Recorded in methodology §2.5 + §11 (item 11) + SUPP-EV-002. Candidate / no score-movement / no launch.

## CLOSED 2026-06-03 — orchestrator close-readiness gate
Independently re-ran `run_golden_validation.py`: **14/14 PASS**, inverted-E test PASSED (no-evidence
`cap_1_insufficient_evidence` vs dangerous `veto_safety` — different binding constraints, inverted
signatures). Artifacts verified on disk (full src tree, 14 traces, calibration+validation reports,
SUPP-EV registry). Separate tree confirmed (no BSIP2 imports/shared constants; food invariants
untouched). D8-VERIFIED + FLAG-2 D7 CO-SIGNED. All numbers candidate/calibration-pending; nothing
ships. `cc_reviewed: true`.

## Carried-forward (not blockers)
- FLAG-3 → SUPP-EV-006 (safety-neutral blend value; possible "exclude neutral Safety from blend" — would need D7).
- Primary UL/safety numbers remain `NEEDS-ENV-VERIFY` (EFSA/NIH/FDA sheets) before any value moves a published score.

## Next
Phase 3 (TASK-171D, not opened) — Israeli supplement corpus (BSIP0-S scrape: Super-Pharm / iHerb-IL /
brand sites) + QA freeze. The one remaining data gap; engine is proven, so this is now de-risked.
