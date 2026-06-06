# SIE Phase-2 Calibration — proto_v0 (v1)

**Task:** TASK-171C · **Date:** 2026-06-03 · **Owner:** Data Agent
**Spec:** `01_framework/supplement_framework/methodology_v1.md` v1.2 (D7 co-signed)
**Status:** CALIBRATION-PENDING — every number below is candidate; nothing ships;
no published score; Nutrition D8 implementation-verify required.

## What this is

The candidate weights/thresholds in `src/constants.py` tuned until all 14 golden
fixtures land in their expected grade band **and** carry the correct binding
constraint (esp. the inverted-E pair). Calibration was kept **minimal and
principled** — I did not chase numbers; I started from the spec's candidate values
(§3.1 weights, §2.x bands, §3.2 ceilings) and only set within-band representative
values + the two seams the spec leaves to the implementer.

## Candidate values as built (all `# CALIBRATION-PENDING`)

| Constant | Value | Source / basis |
|---|---|---|
| Dimension weights | Ev 0.30 / Dose 0.25 / Form 0.20 / Honesty 0.15 / Safety 0.10 | §3.1 candidate table, verbatim |
| Grade bands | S90 / A80 / B65 / C50 / D35 / E0 | §4 + D7 ruling 1 (start aligned with BSIP2) |
| Evidence sub-score | band midpoints: Strong 92.5 / Moderate 72 / Weak 47 / Insufficient 17 | §2.1 bands; midpoint = neutral representative |
| Dose in-range | 92 | §2.2 "85–100" band, upper-mid |
| Dose sub-therapeutic | 50→84 graded by proximity in [0.5·min, min) | §2.2 "50–84 graded by proximity" |
| Dose fairy-dust | 20 | §2.2 "0–34" band |
| Dose over-studied | 72 | §2.2 "60–84, no bonus" |
| `FAIRY_DUST_FRACTION` | 0.5 | §2.2 candidate, verbatim |
| Form preferred/acceptable/poor-as-premium/poor-honest | 92 / 72 / 22 / 45 | §2.3 bands, representative |
| Honesty debits | claim-substance 35 · misleading-true 20 · filler 12 · pixie 20 | §2.4 severity ordering |
| Honesty hidden-blend sub-score | 25 | floors the sub-score so the trace reads honestly (cap does the grade work) |
| Cap 1 insufficient-evidence ceiling | 34 | §3.2 #1 candidate (= E ceiling) |
| Cap 2 fairy-dust ceiling | 49 | §3.2 #2 "~D-band" (= D ceiling, 35–49) |
| Cap 3 honesty core / secondary | 49 / 64 | §3.2 #3 + D7 ruling 2 (core→D, secondary→C) |
| Cap 5 form-evidence coupling ceiling | 49 | §3.2 #5 (form-honesty band, D ceiling) |
| Veto 4 safety floor | 20 | §3.2 #4 "~E-band", mirrors BSIP2 trans-fat veto floor 20 |
| Safety neutral blend value | 70 | see "Seam B" below |

## Seams the spec left to the implementer (documented, principled)

**Seam A — Evidence sub-score representative value.** §2.1 gives bands, not points.
I used the **band midpoint** (Strong→92.5, Weak→47, …). Midpoint is the neutral
choice; it makes a Strong-claim, perfectly-delivered product land S and a Weak-claim
otherwise-excellent product land B (see FLAG-1). Any non-midpoint choice would be an
unjustified thumb on the scale and should carry its own SUPP-EV.

**Seam B — how Safety enters the blend.** §2.5 is explicit that Safety is a veto/cap
that "does not lift the score" and "absence of harm isn't a virtue." A `neutral`
Safety therefore must not *reward* a product. I enter `neutral` at a **modest fixed
70** (below the typical good-dimension value of ~92) so it neither rewards nor
penalizes a clean product, and the veto is enforced **separately as a hard floor**
(not via the blend). This is the one genuinely arbitrary number in the build —
**flagged as needing a future SUPP-EV justification** (FLAG-3). It does not affect any
fixture's grade band (the safety-relevant fixtures are veto-floored, not blend-bound).

## What I tuned and why (minimal set)

1. **Honesty hidden-blend sub-score → 25 (not a smooth debit).** §2.4 makes a hidden
   blend a *cap* on the whole product; I additionally floor the Honesty *sub-score* so
   the trace signature reads `Honesty LOW`, matching the §13 intent. Concern-
   coordination (§3.2 #6): when the blend is hidden, the other Honesty debits are
   **not** also charged (no triple-counting of one deception).
2. **Safety comparison on the elemental/active basis.** §2.5 requires the UL check use
   the **same basis as the dossier** (elemental, daily, adult). The scorer now routes
   the Safety daily-dose through the same normalizer as Dose (elemental conversion +
   per-serving→per-day) before comparing to the UL. Without this, a magnesium label's
   raw *compound* mass was compared to an *elemental* UL → spurious veto. This is a
   correctness fix, not a tuning knob.
3. **No weight changes.** The §3.1 candidate weights were left exactly as the spec
   gives them; all fixtures resolve correctly on those weights.

## FLAGS for Nutrition D8 (do not silently deviate — §ConstraintsHard)

- **FLAG-1 — Weak evidence has no cap; an otherwise-excellent Weak-claim product
  lands B.** The omega-3 "brain & mood" FAIL anchor (Weak tier) scores **77.5 / B**
  because Weak (47) only enters the 30%-weighted blend — there is no §3.2 cap for Weak
  (only Insufficient caps). It is correctly a *relative* FAIL vs the Strong-claim PASS
  anchor (same molecule: S vs B). **Question for Nutrition:** is "B / sound but
  compromised" the right ceiling for a Weak-evidence claim, or should Weak carry a
  B-ceiling (or C-ceiling) cap so a thin-evidence product can't reach A/B on delivery
  alone? The spec does not specify one; I did **not** invent one. Flagged for D8.

- **FLAG-2 — Magnesium dossier internal tension: `min_effective` (300 mg elemental)
  exceeds the governing UL (250 mg elemental supplemental).** An *adequately-dosed*
  magnesium supplement structurally **breaches the supplemental UL** — the effective
  dose sits above the safety ceiling. This is a real property of the co-signed dossier
  (EFSA 250 governs the veto; effective dose 300–400), not an engine bug. The engine
  behaves correctly (vetoes a 300 mg elemental Mg SKU), but the **dossier is internally
  in tension** and a real Israeli Mg SKU dosed to work would be safety-vetoed. The Form
  fixtures dose to ~245 mg elemental (just under UL) to exercise the Form axis without
  confounding it. **Escalated to Nutrition** (per Hard Rule: enrichment producing an
  unexpected distribution) — likely resolutions: (a) the UL is a *supplemental* GI-
  tolerance line and a 250–400 mg band should be a **Safety NOTE, not a hard veto**
  (graded reading, hinted in the dossier's `ul_governing_decision`); or (b) confirm the
  effective-dose vs UL numbers on the next sweep. **Not resolved here — Nutrition D8.**

- **FLAG-3 — Safety-neutral blend value (70) is genuinely arbitrary.** See Seam B.
  Needs a SUPP-EV justification before it can move a published score. Currently affects
  no fixture grade.

## Calibration outcome

14 / 14 fixtures land in their expected grade band AND carry the expected binding
constraint, including the decisive inverted-E pair. No weight or band threshold from
the spec was changed; the two implementer seams are documented above; three substantive
questions are flagged for Nutrition D8 rather than silently resolved.
