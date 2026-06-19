---
id: TASK-350
title: SIE red-team CRITICAL remediation (RT-1 elemental veto bug, RT-2 D3 claim translation, RT-3 infant dosing)
owner: nutrition-agent
status: CLOSED
priority: HIGH
closed_at: 2026-06-19
final_close_reason: >
  ALL red-team CRITICALs CLOSED + independently re-confirmed. Decider red-team on v7
  (red_team_sie_v7.md) = ZERO open CRITICAL: RT-1/RT-3 (v6), RT6-C1 iron double-conversion +
  RT6-C2 D3 traceability (v7) all verified CLOSED. Root fix = explicit per-mineral label_basis
  (iron=elemental→no convert, verified vs MOH reg; mag/zinc=compound→convert) + claim_translation_
  provenance in trace. Orchestrator independently verified: 3 iron products back to S/91.2, magnesium
  conversion intact (oxide 520→B not re-vetoed), golden 17/17 (SAFE-FAIL still vetoes), 0 false-veto,
  0 false-safe, qa 5/5, v7 dist S11/A9/B16/C4/D15/E23 (78 scored), food scoring byte-identical.
  3 residual HIGH (NOT critical, routed to follow-up TASK-351): H2 zinc picolinate label_basis
  (2 products B should be S — conservative under-score), H3 mag carbonate dossier gap (1 product
  C should be D), H1 latent iron worst-case guard (0 current products). Closing the CRITICAL-
  remediation scope; go-live decision + D7 co-sign are separate owner calls.
reopened_at: 2026-06-19
reopen_reason: >
  Re-red-team of v6 (red_team_sie_v6.md) found 2 NEW CRITICALs — go-live gate FAILED, so the
  prior CLOSE was premature (orchestrator self-correction). RT6-C1 (orchestrator-VERIFIED): the
  RT-1 iron alias fix caused a double-conversion — Israeli iron labels state ELEMENTAL iron, but
  the engine now treats the stated mg as COMPOUND bisglycinate and converts down (30mg × 0.274 =
  8.22mg → false fairy_dust). 3 iron products collapsed v3 S/91.2 → v6: 7290118814061 (SupHerb
  Iron 9-months, PREGNANCY iron) D/49, 783495578741 (Category5) D/49, 7290012056741 (Tink) A/81.5.
  A pregnancy iron supplement graded D = harmful false verdict. RT6-C2: RT-2 only partially closed
  — 3 of 7 D3 S-grades still rest on an unauditable English pre-translation in the trace. v7 fix
  needed: represent each dose's BASIS (elemental vs compound) so the engine converts only compound
  labels (root fix, stops the whack-a-mole), + close the D3 traceability gap. RT-1/RT-3 confirmed
  CLOSED by the re-red-team. (Superseded close_reason below.)
prior_close_reason: >
  All 3 red-team CRITICALs remediated across 3 passes, each pass orchestrator-verified against
  artifacts (and each caught a real defect the prior pass missed/introduced — the loop working):
  RT-1 false vetoes (9 Mg pass-1 + zinc pass-2 + Hadas-Mag false-safe pass-3) → v6 has 0 veto_safety
  in scored AND 0 false-safe (independent worst-case scan: only Hadas Mag form=None worstcase>UL →
  correctly unscoreable_incomplete; other 4 ambiguous minerals worstcase<=UL → neutral-scored). RT-2
  (4 D3 S→A) + RT-3 (3 infant→unscoreable_pediatric) verified in pass-1. v6 dist S8/A10/B16/C4/D17/E23
  = 78 scored (re-run confirmed); golden 17/17 with SAFE-FAIL-d3-50k still vetoing (elemental fix did
  not disable real safety); qa_audit 5/5 (re-run exit 0); food SCORING byte-identical (score_engine sha
  unchanged). SUPP-EV-022/023/024 registered. NOTE: 4 unrelated bari-web frontend files (juices/snacks)
  are dirty in the shared tree from concurrent NON-supplement work — not touched by this task.
  GATE REMAINING before go-live: re-red-team v6 to zero-CRITICAL + Product D7 co-sign (separate steps).
created_at: 2026-06-19
depends_on: [TASK-277]
blocks: []
category_id: null
summary: >
  Fix the 3 red-team CRITICALs on the SIE v3 corpus: RT-1 magnesium/iron elemental-conversion key mismatch (10 Mg+1 zinc false safety vetoes), RT-2 hidden human D3 claim translation inflating S-grades, RT-3 infant products scored vs adult doses. Re-score to v4, re-run golden+QA, before/after delta. EDPG; no published score moves; re-red-team after.
---

# TASK-350 — SIE red-team CRITICAL remediation (RT-1 elemental veto bug, RT-2 D3 claim translation, RT-3 infant dosing)

## Orchestrator verification — 2026-06-19 → CHANGES_REQUESTED

First-pass return (Nutrition, v4) VERIFIED-GOOD on most scope: golden re-run 17/17 (SAFE-FAIL-d3-50k
still vetoes, FORM-FAIL-mg-oxide still form-penalized — elemental fix did not disable real safety;
fixtures.py edit legitimate, R3 dose rebased to stay in its honesty-cap band); RT-1 magnesium = 9/9
false vetoes resolved + 1 genuine retained (Hadas 600mg no-form); RT-2 = 4 D3 S→A; RT-3 = 3 infant →
unscoreable_pediatric; v4 dist S8/A10/B16/C4/D17/E24 (79 scored) confirmed from JSON; food invariants
byte-identical (git diff = supplement tree only).

DEFECT (why not CLOSED): RT-1 remediation INCOMPLETE — the red-team flagged "10 Mg **+ 1 zinc**" false
vetoes; the zinc (7290018365359 Tink Zinc Picolinate "50 מג") is STILL E/20 veto_safety. It is
name_derived, form=None, 50mg from the name (elemental-vs-compound ambiguous); zinc picolinate 50mg
compound = ~10.5mg elemental (< 40mg UL) → false safety warning. Zinc dossier never got the RT-1
alias fix. Follow-up dispatched (agent aa49cfaa…): fix zinc.yaml aliases + a form=None ruling
(never assert a safety veto on an ambiguous name-derived mineral dose) + sweep ALL surviving
veto_safety to prove each is a genuine overdose; re-score → v5; golden 17/17; qa PASS.

Next after fix verified: re-red-team to zero-CRITICAL → owner go-live call.

---

## Third-pass return — Nutrition Agent, 2026-06-19 (TASK-350 third pass)

**CHANGES_REQUESTED defect addressed:** SUPP-EV-023 (v5) introduced a false-safe. The
`ambiguous_basis_no_form` guard returned `safety=neutral` (full score path) for ALL form=None minerals,
including cases where worst-case elemental (amount × max_fraction) exceeds the UL. Hadas Full-Mag
600mg (7290001943700) scored B/71.6 — asserting a clean grade when 600 × 0.603 (oxide, max Mg
fraction) = 361.8mg > 350mg UL. A genuinely indeterminate product is not safe to score B.

### Rule implemented (SUPP-EV-024)

In `score_safety()`, after detecting `elemental_by_form non-empty AND active.form is None`:
1. Compute `worst_case = amount × max(elemental_by_form.values())`
2. If `worst_case ≤ UL` → `SAFETY_NEUTRAL` (reason: `ambiguous_basis_no_form`). Cannot exceed UL
   under any form — SUPP-EV-023 behavior preserved.
3. If `worst_case > UL` → `SAFETY_UNSCOREABLE` (reason: `mineral_form_undeterminable_dose_may_exceed_ul`).
   Runner intercepts after `score_label()` → routes to `unscoreable_incomplete`.

New constant `SAFETY_UNSCOREABLE = "unscoreable"` in `constants.py`. `_weighted_blend()` guarded
against the sentinel. Runner intercept added in `run_full.py` after `score_label()` return.

### Ambiguous-basis worst-case table (all 5 form=None minerals from v5)

| Barcode | Active | Amount (mg) | Max fraction | Worst-case elemental (mg) | UL (mg) | Resolution |
|---|---|---|---|---|---|---|
| 0033984010642 (Solgar Zinc 22mg) | zinc | 22.0 | 0.803 | 17.67 | 40 | neutral-scored |
| 7290001943700 (Hadas Full-Mag 600mg) | magnesium | 600.0 | 0.603 | 361.80 | 350 | **unscoreable_incomplete** |
| 7290016417197 (Acosup Iron 15mg) | iron | 15.0 | 0.368 | 5.52 | 45 | neutral-scored |
| 7290016417227 (Acosup Zinc 20mg) | zinc | 20.0 | 0.803 | 16.06 | 40 | neutral-scored |
| 7290015765985 (Sideral Iron 30mg) | iron | 30.0 | 0.368 | 11.04 | 45 | neutral-scored |

Only Hadas Mag flips to unscoreable. 4 others remain neutral-scored (correct).

### Hadas Mag before → after
- v5 (false-safe): B/71.6, safety=neutral, reason=ambiguous_basis_no_form
- v6 (corrected): unscoreable_incomplete, reason=mineral_form_undeterminable_dose_may_exceed_ul

### Grade distribution delta v5 → v6
| Grade | v5 | v6 | Delta |
|---|---|---|---|
| S | 8 | 8 | 0 |
| A | 10 | 10 | 0 |
| B | 17 | 16 | −1 |
| C | 4 | 4 | 0 |
| D | 17 | 17 | 0 |
| E | 23 | 23 | 0 |
| scored | 79 | 78 | −1 |
| unscoreable_incomplete | 25 | 26 | +1 |

### Zero veto_safety AND zero false-safe confirmed
- `veto_safety` in v6 scored products: **0** (verified by scan)
- `ambiguous_basis_no_form` neutrals in v6: **4** (all with worst-case ≤ UL)
- `SAFETY_UNSCOREABLE` routed to unscoreable_incomplete: **1** (Hadas Mag 600mg only)

### Golden validation: 17/17 PASS
`run_golden_validation.py` exit 0. SAFE-FAIL-d3-50k: non-mineral dossier, known form "D3
(cholecalciferol)" → guard does not engage → veto_safety fires correctly (preserved).
Low-dose ambiguous minerals: 4 pass neutral-scored (RT-1 fix not regressed).

### QA audit: 5/5 PASS
All checks PASS on `_corpus_run_full_v6.json`:
- TRACEABILITY: 78 scored SKUs, 0 missing dose, 0 missing source_url
- OFF BAN: 204 files scanned, 0 references
- NO FABRICATION: 0 omega3+name_derived scored
- DISTRIBUTION: S=8/A=10/B=16/C=4/D=17/E=23 computed = header = reported
- UNSCOREABLE: scored=78/incomplete=26/premarket=11/pediatric=3/total=118

### Food invariants: byte-identical
Food BSIP2 `score_engine.py` sha256: `42d3c150e84738a477a1dcc2fa5ce3fdcb0854dd2d0356ede18df7596e337518` (unchanged).
No food category files touched. Supplement engine is a sibling tree.
