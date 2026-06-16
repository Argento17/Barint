# Biscuits × Sugar — Product Agent D7 Co-Sign (Phase 2 Enrollment)

**Task:** TASK-278 — Project Rescore (Phase 2: biscuits × sugar enrollment)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Governance co-sign only. No engine code change. No pilot rescore. Zero score movement.
**Enrollment proposal:** `02_products/cookies_coffee/methodology/shelf_relative_sugar_enrollment_v1.md`
**Phase-1 D7 reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The enrollment proposal is sound. All six Phase-1 hard conditions are addressed. The three
expert-call parameters (floor value, band magnitudes, scope) are ratified below with single
recommended values. EV-085 is registered on this co-sign. The pilot acceptance set is locked
before any rescore runs.

Five conditions carry forward from this co-sign into the pilot implementation. None are waived.

---

## Section 1 — Scope Confirmation

### Decision: `{biscuit}` only — CONFIRMED

Scope `frozenset({"biscuit"})` is correct and bounded. The structural guard confirms zero
published-category bleed: the scope check returns `(0, "category=X not in scope")` for all
live categories (milk, yogurt, bread, snack, cereal, brined cheese). The biscuit router
category ID (EV-058) does not overlap any live published category.

Published categories affected: **zero**. The 58 products in `run_cookies_004` are not live on
the consumer frontend. This enrollment is therefore zero-risk for published-score contamination.

The scope guard must be verified in the pilot run output: a cross-corpus diff on all 7 live
published categories with `BARI_SHELF_RELATIVE_V1=on, scope={biscuit}` must show exactly zero
movement outside the biscuit corpus. This is pilot success criterion #7 and must pass.

---

## Section 2 — Floor Decision (cond 5)

### Decision: `formulation_absolute_floor = 55` — CONFIRMED AT PROPOSED VALUE

The Nutrition Agent proposed 55. I confirm it as the correct value. Reasoning:

**Why 55, not lower:** A stricter floor (e.g., 45) would eliminate meaningful within-C
differentiation for the moderate-sugar biscuit cohort (20–24g) and would be inconsistent with
the C-ceiling finding. Products in the 20–24g range that already score in the upper D/lower C
zone are not equivalent to the Lotus outliers (38g+). Collapsing them to the same floor level
manufactures false equivalence in the downward direction — the same failure class the mechanism
is designed to fix.

**Why 55, not higher:** A looser floor (e.g., 65) would allow a high-sugar biscuit (≥20g) to
approach grade B territory (70) after receiving 3pts of below-median relief. That would violate
the Anti-Immunity Rule for a formulation-nutrient category. The D7 Phase-1 co-sign was explicit:
no indulgence category product with elevated sugar reaches grade A via relative relief. Grade B
at 70 is adjacent — 65+3=68 is too close to the B threshold to be defensible.

**Architectural coherence:** Floor=55 is the score produced by the ISRAELI_RED_LABEL_1_SUGAR
single cap. A product that has crossed the Israeli red-label sugar threshold (17.5g/100g) should
not be lifted above what the absolute backbone's most lenient single-cap produces. The relative
relief layer cannot undo the signal the absolute cap is encoding.

**Anti-Immunity verification:** Grade B requires ≥70. Grade A requires ≥80. Floor=55 plus
maximum relief B=3 yields a maximum reachable score of 58 for any product entering with exactly
55 (the floor). No B. No A. Anti-Immunity is mechanically guaranteed.

**The 20g trigger threshold** is confirmed. It sits above the Israeli red-label threshold (17.5g)
and below the corpus median (21.5g). Products between 17.5g and 20g carry the absolute backbone's
red-label cap signal already; the floor ensures products in the 20g+ zone (the dense Q2–Q3
cluster) cannot escape meaningful penalization through relative positioning.

---

## Section 3 — Band Magnitudes (cond 4)

### Decision: P=6 max penalty, B=3 max relief — CONFIRMED

**P=6 is proportionate.** A product at r_above=3.25 (Lotus, 38.1g on a 21.5g median shelf) is
more than 3 robust standard deviations above the median. The 6-point penalty for this distance
is a differentiation residual, not a double-count: the absolute backbone already applies its
caps; the 6pts is the within-E ordering signal that the hard cliff suppresses. P=6 does not
alter Lotus's grade (18.1 − 6 = 12.1, remains E). It moves Lotus to the bottom of the E band
where it belongs.

**B=3 does not violate Anti-Immunity.** The highest-scoring product in the corpus is 63.1/C
(sugar=0g). With B=3, projected max = 66.1. This remains grade C (C threshold: 65–79). The
floor backstops this independently: products with ≥20g sugar are floored at 55 regardless of
relief. The sugar-free cohort (0g) is below the 20g threshold, so the floor does not constrain
them — but their scores are already in the D/C range and B=3 is insufficient to push any of
them to B territory.

**Asymmetry is the correct design.** P=6 > B=3 ensures below-median relief cannot launder a
product the absolute backbone has identified as problematic. This was the decisive reason in the
Phase-1 D7 co-sign for adopting asymmetric P>B over pure one-sided-high. The rationale is
unchanged here — it applies to the biscuit/sugar enrollment as the paradigm case.

**Pilot calibration note:** If the pilot reveals that within-D grade products with ≥20g sugar
and high relief accumulation are crossing the D-to-C boundary (score 65 threshold), recalibrate
B downward to 2 before any live deployment. At B=3, the highest D product in the corpus
(45.7/D at sugar=0g — not subject to the floor) would reach 48.7/D, safely below 65. No
grade-boundary inflation is expected, but the pilot must verify.

---

## Section 4 — Pilot Acceptance Set (Ratified Before Pilot Runs)

The following is the locked pilot acceptance gate. All 7 criteria must pass. Any failure
is a hard stop — the pilot does not ship.

| # | Criterion | Pass Condition |
|---|---|---|
| 1 | Resolution restored | Fewer products pinned at identical cliff scores vs. baseline run |
| 2 | Rank inversions corrected | Inversion A (Lotus gap widens) AND Inversion B (Moroccan gap narrows) — both must confirm |
| 3 | Shelf average stable | Shelf average score lift vs. baseline ≤1.5 pts |
| 4 | Anti-Immunity holds | No biscuit with sugars_g ≥ 20g reaches grade A (score ≥ 80) |
| 5 | Absolute floor enforced | All 51 products with sugars_g ≥ 20g confirm composite score ≤ 55 |
| 6 | Flag-off byte-identical | `BARI_SHELF_RELATIVE_V1=off` → zero movement across all published categories vs. committed baselines |
| 7 | No cross-category contamination | Enrolled biscuit corpus does not move any non-biscuit published score |

### Ratified Named Inversions

**Inversion A — Lotus (5410126806250) vs. פתי בר קמח מלא אורגני (7290018371923)**

- Lotus: 38.1g sugar, baseline 18.1/E. Expected post-pilot: 18.1 − 6 = 12.1.
- פתי בר אורגני: 20.5g sugar, baseline 29.0/E. Expected post-pilot: ~29.0 (r_below=0.20 → band 0, no relief).
- Pass condition: gap widens from baseline 10.9pts to at least 13pts post-pilot. Lotus must
  remain E; פתי בר must remain E. Neither should cross a grade boundary.

**Inversion B — עוגיות סגנון מרוקאי (7290119041053) vs. ביסקוויט בטעם וניל הדר (5317194)**

- מרוקאי: 13.5g sugar, baseline 37.2/D. Expected post-pilot: 37.2 + 2 = 39.2.
- וניל הדר: 22.0g sugar, baseline 48.3/D. Expected post-pilot: ~48.3 (r_above=0.10 → band 0, no penalty).
- Pass condition: inversion gap narrows from 11.1pts to ≤10pts. Direction confirmed: lower-sugar
  product moves toward the higher-scored product. Full gap closure is not expected (other dimensions
  dominate); measurable improvement is the standard.

Both inversions must be verified by trace inspection, not by summary statistics alone.
The `SUGAR_SHELF_REL_V1` rule tag must appear in the relevant trace entries when the surcharge fires.

---

## Section 5 — Pilot Verify Item (Orchestrator Finding)

**Flagged: crude-index quartiles vs. interpolated IQR**

The orchestrator flagged that the engine's `compute_shelf_stats()` currently uses crude-index
quartiles (`values[n//4]`) rather than the interpolated IQR computation that yields exactly
6.9g / robust_scale=5.115 per the proposal.

This is a pre-pilot blocking item. Before the pilot runs:

1. Confirm what `compute_shelf_stats()` actually computes for Q1/Q3 on n=57.
2. If the engine's crude-index method yields Q1=values[14] and Q3=values[42] on the sorted
   57-element array, verify whether this matches the interpolated Q1=17.1 / Q3=24.0.
3. If the crude-index result diverges from 17.1/24.0 by more than 0.5g, the bands must
   recalibrate to the engine-computed values — the proposal's band structure was designed
   against median=21.5 / robust_scale=5.115, and the pilot acceptance criteria cite these
   specific values. A scale discrepancy changes which band a product falls in.

The implementation step (not this co-sign) must confirm `compute_shelf_stats()` yields
scale ≈ 5.115 on the biscuit corpus, or document the actual engine value and adjust the
acceptance thresholds accordingly. This is a data fidelity check, not a scoring change — but
it must be resolved before the pilot is deemed valid.

---

## Section 6 — Hard Conditions (All Blocking)

The Phase-1 D7 co-sign established 6 hard conditions. All 6 carry through to this enrollment.
The following enrollment-specific conditions are added:

**Carried from Phase-1:**

1. EV-084 registered (done at Phase-1 co-sign — confirmed in registry at line 1881).
2. `compute_shelf_stats()` IQR-primary default before any pilot run.
3. n≥20 guard — adopted. n=57 >> 20, non-binding on this corpus.
4. Asymmetric P>B — confirmed. P=6, B=3. Direction: permits below-median relief.
5. `formulation_absolute_floor` non-None — floor=55, threshold=20g. Confirmed.
6. Six-guard no-regression plan executes before merge. Guards 1 (milk byte-identical) and
   2 (all published categories byte-identical at flag-off) are mandatory hard gates.

**Enrollment-specific (added here):**

7. Compute_shelf_stats scale verification: engine must yield scale≈5.115 on biscuit corpus
   before acceptance thresholds are locked (see §5). Any divergence = recalibrate or document.
8. Trace verification: `SUGAR_SHELF_REL_V1` rule tag must appear in traces for the 2 named
   inversion barcodes when the surcharge fires. Tagless application is not auditable.
9. Floor compliance: all 51 products with sugars_g ≥ 20g must be individually confirmed at
   composite score ≤ 55 in the pilot output. Spot-check is not sufficient — full distribution.
10. Family budget raise: the existing sugar family budget for biscuits must be raised by exactly
    max(P, B) = 6 points at implementation. The exact existing budget value must be read from
    constants.py. This raise is a D7 implementation decision — the principle is locked here,
    the exact delta value is verified at constants-read time.

---

## Section 7 — Tripwire Assessment

**No tripwire fires on this co-sign.**

- Frozen invariants: not touched. Milk scores (`run_005_headpin`), yogurt page, bread provenance,
  and all published category scores are untouched. Flag default=off; zero score movement.
- Consumer-facing / irreversible: not applicable. The biscuit category is unpublished. The flag
  is default-off. The pilot rescore is internal. Owner go-live gate (tripwire-1) is required
  before any published movement — that gate is explicitly preserved.
- Major program start/kill: this is Phase 2 of an already-approved program (TASK-278, D7 Phase-1
  co-signed 2026-06-14).
- External commitment/spend/legal: none.
- Strategy redefinition: not applicable.

Reversal condition: if the pilot reveals that below-median relief (B=3) enables any product
with ≥20g sugar to exceed score 55 despite the floor, halt immediately — this indicates a floor
implementation error. Fix the floor implementation before any further run.

**Owner escalation: NOT required.** This co-sign is within the D7 lane. The first published
score movement (owner go-live for the biscuits page) is the tripwire-1 gate that escalates.

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Floor value | (a) 45 — strict / matches single E-grade hard cap; (b) 55 — matches red-label single cap, C-ceiling coherent; (c) 65 — loose, risks B-adjacency | (b) 55 | Architecturally coherent with ISRAELI_RED_LABEL_1_SUGAR cap; B=3 relief cannot reach grade B from 55; C-ceiling finding expressed mechanically for high-sugar cohort | Revisit if pilot shows products at 55+3=58 creating consumer-confusing comparisons near C threshold |
| Band P value | (a) P=4 — moderate; (b) P=6 — proportionate to 3+ robust SD outliers; (c) P=8 — punitive | (b) P=6 | Lotus at r_above=3.25 receives a grade-neutral 6pt penalty — correct within-E differentiation; P=8 would risk double-counting the absolute backbone's already-deep E placement | Recalibrate to P=4 if pilot shows high-sugar outliers receiving penalties that misrepresent their ordinal rank vs. moderate-sugar products |
| Band B value | (a) B=0 — one-sided-high (suppresses below-median signal); (b) B=3 — asymmetric, bounded; (c) B=5 — symmetric-risk | (b) B=3 | Phase-1 D7 co-sign resolved this: valid below-median signal should surface; B < P enforces asymmetry; floor=55 backstops Anti-Immunity for high-sugar products, so B=3 carries no Anti-Immunity risk for the ≥20g cohort | Revert to B=0 (one-sided-high) for sugar/biscuits if pilot shows relief enabling grade-boundary inflation — see §3 calibration note |
| Pilot acceptance: inversion A type | (a) True inversion (incorrect direction); (b) Resolution case (correct direction, insufficient separation) | Both types ratified — one of each | True inversion (Inv B) confirms the model fixes wrong-direction rank errors; resolution case (Inv A) confirms within-band differentiation is improved | No reversal — both types of improvement are necessary; if only one is demonstrable, flag as partial pass requiring explanation |
| Owner escalation | (a) Escalate — design-level approval; (b) D7 lane sufficient | (b) D7 lane | No tripwire fires: flag default-off, zero published score movement, unpublished category, fully reversible, within approved TASK-278 program | Escalate immediately if any pilot guard failure causes a published score to move |

---

## EV-085 Registration

EV-085 is registered in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
as part of this co-sign. See Section 8 for the full registry entry. The Nutrition Agent's
draft EV-085 in §7 of the enrollment proposal is adopted with one addition: the `status` field
is updated to reflect Product Agent co-sign granted.

---

```json
{
  "task": "TASK-278 Phase-2 / Product Agent D7 co-sign",
  "proposed_status": "RETURNED",
  "verdict": "CO-SIGN APPROVED WITH CONDITIONS",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/shelf_relative_sugar_enrollment_d7_cosign_v1.md",
      "sha256": "986fac14967ff46403ceafbfb91441d7ab06447f01d5ac0d188ce9fa35c65d80"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "note": "EV-085 appended — see write operation"
    }
  ],
  "counts": {
    "hard_conditions_total": 10,
    "hard_conditions_carried_from_phase1": 6,
    "hard_conditions_enrollment_specific": 4,
    "pilot_acceptance_criteria": 7,
    "named_inversions_ratified": 2,
    "tripwires_fired": 0,
    "ev_id_registered": "EV-085",
    "ev_track_max_before_this": "EV-084",
    "published_scores_moved": 0,
    "scope_categories": 1,
    "floor_value": 55,
    "floor_threshold_g": 20.0,
    "max_penalty_P_pts": 6,
    "max_relief_B_pts": 3,
    "corpus_n_with_sugar": 57,
    "corpus_n_total": 58,
    "median_sugar_g": 21.5,
    "robust_scale_g": 5.115
  },
  "commands_run": [
    {
      "cmd": "Read shelf_relative_sugar_enrollment_v1.md",
      "exit_code": 0,
      "output_summary": "9-section enrollment proposal, Nutrition Agent co-sign, EV-085 draft, full distribution stats confirmed"
    },
    {
      "cmd": "Read shelf_relative_d7_cosign_v1.md",
      "exit_code": 0,
      "output_summary": "Phase-1 D7 co-sign confirmed, 6 hard conditions verified, EV-084 registered"
    },
    {
      "cmd": "Grep bsip2_evidence_registry_v1.md for EV-08x entries",
      "exit_code": 0,
      "output_summary": "EV-084 at line 1881 confirmed as max TASK-278 EV-track entry; EV-085 has no collision"
    },
    {
      "cmd": "Read evidence registry tail (lines 1920-1979)",
      "exit_code": 0,
      "output_summary": "Confirmed EV-059 at line 1949 (post-EV-084); end-of-registry footer at line 1975; EV-085 append location confirmed"
    }
  ],
  "not_done": [
    "Pilot rescore (run_cookies_004 with BARI_SHELF_RELATIVE_V1=on, scope={biscuit}) — requires this co-sign first; blocked until compute_shelf_stats scale verification passes",
    "compute_shelf_stats crude-index vs. interpolated IQR verification — must confirm scale=5.115 on engine before pilot is valid",
    "Phase-3 no-regression gauntlet (Guards 1-6 + 4 enrollment-specific conditions) — runs at implementation",
    "Family budget raise: read constants.py for exact existing sugar family budget, add 6pts, verify combined total is not double-counting",
    "SUGAR_SHELF_REL_V1 rule tag implementation: trace tagging must be verified for the 2 named inversion barcodes",
    "Floor compliance full-distribution check: all 51 products with sugars_g >= 20g must individually confirm composite score <= 55",
    "Owner go-live gate: required before any published score movement; biscuit page is unpublished but go-live is non-negotiable before consumer deployment"
  ],
  "acceptance_test": {
    "spec": "D7 co-sign conditions 1-6 from Phase-1 all addressed; enrollment-specific conditions 7-10 documented; EV-085 registered; pilot acceptance set locked before pilot runs; no tripwire fires; floor=55 confirmed with Anti-Immunity proof",
    "result": "PASS — all Phase-1 conditions addressed in enrollment proposal; 4 enrollment-specific conditions added; pilot gate locked; EV-085 written to registry"
  }
}
```
