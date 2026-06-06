# Legacy-Page Score Freshness Audit — HEAD vs Published Engine Drift

**Task:** TASK-178
**Date:** 2026-06-04
**Author:** QA Agent (bari-qa-audit)
**Type:** Read-only audit. No score moved, no page reshipped, no engine edited.
**Verdict:** RETURNED — re-baseline required before any legacy page is rebuilt.

---

## 0. Most dangerous finding first

**BREAD is the worst-affected legacy category, not milk.** Re-running the published
`bread_retail_003` corpus under the current engine HEAD reproduces only **165/256
(64%)** of published scores, with **83 grade-affecting drifts, all upward (+~8.2)**,
including multiple **C→B grade flips on the live shelf**. Of the **24 breads that
actually render on the live page, 18 sit on a HEAD trace that drifted ≥2pt upward**
(typically +6 to +8.5). A naive full rebuild would silently push almost the entire
bread shelf up ~6–8 points and compress it toward the A-ceiling.

By contrast the milk slice that triggered this task (13/20) is the *least* severe of
the three, and its frozen invariant is intact.

The drift is **systematic and upward** in every legacy category, and its dominant
cause **predates the git repo** (git init = 2026-06-01; all three freezes are older),
so it is **not recoverable or diff-able from version control** — see §4.

---

## 1. Scope

| Category | Published run (freeze) | Freeze date | In scope | Why |
|---|---|---|---|---|
| Milk & alternatives | `run_004_recalibrated` | 2026-05-18 | **YES** | Live page renders these; 13/20 measured by TASK-169C |
| Bread | `bread_retail_003` (`real_bread_retail_003_v1`) | 2026-05-25 | **YES** | Live page renders calibrated derivatives of these |
| Snack bars | `proto_v0/outputs` (sealed) | 2026-05-17 | **YES** | Live page derives from this corpus; ceiling invariant lives here |
| Cheese | recal (TASK-142/149 line) | 2026-06-02 | **OUT** | Already on the post-recal engine; rebuilt after constants folded in |
| Hummus | recal (TASK-150) | 2026-06-02 | **OUT** | Same — re-scored and shipped on current engine |
| Yogurt | `run_169D` recal | 2026-06-03 | **OUT** | Shipped on HEAD engine yesterday; reproduces by construction |
| Maadanim | recal (TASK-149 line) | 2026-06-02 | **OUT** | Re-scored on current engine |

**Reasoning for OUT:** cheese/hummus/yogurt/maadanim were all (re)generated on the
*current* engine after the v2 recal constants became the unconditional baseline (§4),
so HEAD reproduces them by construction. They are not exposed to the pre-recal→HEAD
drift this audit measures. They should still be re-confirmed if/when the next engine
change lands, but they are not part of *this* re-baseline.

---

## 2. Per-category reproduction rate + drift counts

| Category | Published scored | Reproduced exactly | Repro rate | Grade-affecting | Cosmetic (<2pt, same grade) | Drift direction |
|---|---|---|---|---|---|---|
| **Milk** | 20 | 13 | **65%** | **3** (1 grade-flip, 2 ≥2pt same-grade) | 4 | mixed (−3.6 to +1.8) |
| **Bread** | 256 | 165 | **64%** | **83** (all ≥2pt; many C→B flips) | 8 | uniformly **upward** (~+8.2) |
| **Snack bars** | 53 | 5 | **9%** | **29** (D→C, E→D, C→B flips) | 19 | uniformly **upward** (+2 to +14) |

Method: each category re-run through the **current HEAD pipeline** against the *same*
frozen input corpus that produced the published trace, comparing
`final_score_estimate`/`final_score` and grade. Snack figures independently
reproduced and they exactly match the numbers TASK-169E already recorded
(`head_vs_published_proto_v0_2026_05_17 = 5/53`).

### 2a. Grade-affecting milk deltas (full)

| Product | Name (he) | Pub | HEAD | Δ | Verdict |
|---|---|---|---|---|---|
| `bsip1_5411188300328` | אלפרו שוקו משקה סויה | 38.1/D | **34.5/E** | −3.6 | **GRADE FLIP D→E** |
| `bsip1_7290107932134` | חלב בבקבוק 1% מועשר — מהדרין | 60.2/C | 56.6/C | −3.6 | ≥2pt, same grade |
| `bsip1_7290114313285` | מולר פרוטאין משקה בננה | 49.6/D | 46.5/D | −3.1 | ≥2pt, same grade |

Cosmetic (<2pt) milk: `5411188112709` (+1.8), `7290014760141` (+1.8),
`7290110324773` (−1.0), `7290119385560` (−0.3).

### 2b. FROZEN INVARIANT CHECK — milk top holds

| Product | Name | Pub | HEAD | Status |
|---|---|---|---|---|
| `bsip1_7290000051352` | חלב מלא בטעם של פעם 3.4% | 85/A | 85/A | **HELD** |
| `bsip1_7290019790259` | חלב טבעי 4% | 85/A | 85/A | **HELD** |
| `bsip1_7290102392094` | חלב עיזים | 85/A | 85/A | **HELD** |

CLAUDE.md invariant "milk top = 85/A (whole/4%/goat), no reversion" is **NOT
threatened** by HEAD. The 7 milk drifts are all mid/lower shelf.

### 2c. Bread — rendered-page slice (for TASK-169F)

Of the 24 breads on `bread_frontend_v2.json`, drift on their backing HEAD trace:

| page_id | page score | trace pub | trace HEAD | Δ | flag |
|---|---|---|---|---|---|
| shufersal_2079996 | 73 | 73.4 | 79.6 | +6.2 | DRIFT |
| shufersal_497044 | 72 | 72.2 | 80.7 | +8.5 | DRIFT |
| shufersal_7290016967074 | 72 | 72.0 | 72.0 | 0.0 | — |
| shufersal_7290018500460 | 67 | 66.9 | 72.0 | +5.1 | DRIFT |
| shufersal_3268429 | 80 | 79.8 | 82.0 | +2.2 | DRIFT |
| shufersal_481203 | 77 | 76.9 | 82.0 | +5.1 | DRIFT |
| shufersal_3054183 | 76 | 75.7 | 82.0 | +6.3 | DRIFT |
| shufersal_2079927 | 75 | 75.3 | 81.5 | +6.2 | DRIFT |
| shufersal_3268252 | 75 | 75.2 | 82.0 | +6.8 | DRIFT |
| shufersal_574370 | 75 | 74.8 | 82.0 | +7.2 | DRIFT |
| shufersal_481197 | 76 | 75.9 | 82.0 | +6.1 | DRIFT |
| shufersal_4685027 | 70 | 70.3 | 72.0 | +1.7 | — |
| shufersal_2079217 | 61 | 60.7 | 67.4 | +6.7 | DRIFT |
| shufersal_2079477 | 67 | 67.1 | 74.1 | +7.0 | DRIFT |
| shufersal_7290016245325 | 82 | 82.0 | 82.0 | 0.0 | — |
| shufersal_7290018500316 | 68 | 67.9 | 76.1 | +8.2 | DRIFT |
| shufersal_6451507 | 66 | 66.1 | 69.0 | +2.9 | DRIFT |
| shufersal_6451484 | 60 | 60.5 | 68.8 | +8.3 | DRIFT |
| shufersal_2079033 | 74 | 73.6 | 80.2 | +6.6 | DRIFT |
| shufersal_96086000966 | 82 | 81.5 | 81.5 | 0.0 | — |
| shufersal_96086000577 | 78 | 77.7 | 77.7 | 0.0 | — |
| shufersal_7296073134459 | 72 | 72.2 | 72.2 | 0.0 | — |
| shufersal_7296073134442 | 71 | 71.4 | 71.4 | 0.0 | — |
| shufersal_8434165658523 | 59 | 59.2 | 67.4 | +8.2 | DRIFT |

**18 of 24 rendered breads drift ≥2pt upward.** The 6 that match are the verified
A-tops (tahini bread 82, crackers) or floor/capped items. Note: the live page renders
*lechem-calibration-patched, rounded* scores (downstream of the trace), so the page
value tracks `trace pub`, not `trace HEAD` — the +6/+8 gap is exactly what a rebuild
would inject.

### 2d. Snack — ceiling invariant check

| Product | Pub (sealed proto_v0) | HEAD | Note |
|---|---|---|---|
| `bsip1_7290011498870` (= snk-001, date bar) | 65/C | **70/B** | Live page already shows 70/B (editorial recal, not the sealed trace) |
| `bsip1_8423207210287` | 55.5/C | **69.5/B** | Second product now crowding the B-ceiling under HEAD |

Invariant "no snack bar reaches A; snk-001 70/B is the ceiling" is **NOT threatened**
(max HEAD value ≈ 70/B). But HEAD produces a **second 69.5/B** product that did not
exist at 55.5/C in the sealed set — a rebuild would no longer present snk-001 as a
lone ceiling. Flag for editorial, not a hard invariant break.

---

## 3. Delta classification summary

| | Grade-affecting | Cosmetic (<2pt, same grade) | Exact match |
|---|---|---|---|
| Milk | 3 | 4 | 13 |
| Bread | 83 | 8 | 165 |
| Snack | 29 | 19 | 5 |

"Grade-affecting" = grade flip **or** |Δ| ≥ 2pt (a ≥2pt move on the live page is a
visible, defensibility-relevant change even without a grade flip).

---

## 4. Engine-change root cause

**Primary cause (pre-git, not diffable): the v2 grade recalibration became the
unconditional engine baseline AFTER the snack (05-17) and around the milk (05-18)
freezes, and BEFORE the bread (05-25) re-run was itself frozen against an
intermediate state.** The recal constants are live and **unflagged** in HEAD
`constants.py`:

```
NOVA_PROCESSING_SCORES = {1:95, 2:85, 3:65, 4:35}   # NOVA3 60→65 etc.
NOVA_WFI_SCORES        = {1:100,2:85, 3:60, 4:30}
GRADE_THRESHOLDS       = S≥90 A≥80 B≥65 C≥50 D≥35 E
NOVA1_SINGLE_FLOOR     = 85   (was 75)
WHOLE_FOOD_FAT_FLOOR   = 70   (was 65)
CONFIDENCE_LOW_CEILING = 75   (was 70)
```

These are exactly the deltas the `batch_run_milk_004.py` header documents as the
"v2 grade recalibration." They apply to **every** category on rebuild. Milk
`run_004` was generated *with* them (so 13/20 still reproduce; the 7 misses are
later micro-edits — see secondary). Bread_003 and snack_001 traces were produced by
engine states that **did not have the full recal folded in**, so re-running them
under HEAD inherits the NOVA-score lift + floor/cap lift and drifts uniformly
**upward** (+6 to +8 bread, +2 to +14 snack). The drift is in the **base scoring
layer** (verified: HEAD `score_result.final_score_estimate` for a sample bread =
82.0 vs published base 75.7, *before* the synthesis fiber/gss nudge), not the
synthesis/calibration layers.

- **Not version-controlled:** git was initialized `7c02daf` on **2026-06-01**, after
  all three freezes. `score_synthesis.py` and the recal-bearing `constants.py` state
  at freeze time are **not in git history**, so the dominant drift cannot be bisected
  to a commit. This is itself a finding: the legacy freezes have no reproducible
  engine pin.

**Secondary cause (git-visible, small): BSIP2 0.4.0** (`8dac1d4`, 2026-06-01,
TASK-133 F1/F2/F4 — protein-matrix discount, additive identity, BHA penalty). Its
own validation reported "464 products → 4 changed, 0 grade-flips; live pages
unaffected," and its constant additions are mostly **0-magnitude placeholders**.
This explains a small number of the **milk** 7-product misses (additive-identity /
EV-series effects) but **does not** explain the systematic bread/snack upward shift.

**Net:** the dangerous drift is the **unflagged v2 recal baseline applied to
pre-recal frozen corpora**, compounded by the absence of a git-pinned engine state
at freeze time.

---

## 5. Re-baseline plan

Goal: let each legacy page be regenerated **without silently moving published
scores**, by deliberately rescoring on HEAD and getting per-invariant owner sign-off
on the intended moves.

**Step 0 — Pin HEAD.** Tag the current engine commit as `engine-baseline-2026-06-04`
so every legacy rescore from here is git-reproducible (closes the pre-git gap). No
code change, tag only.

**Step 1 — Milk re-baseline (lowest risk).**
1. Rescore the 20-product milk corpus on HEAD → `run_005_headpin` (new dir, do not
   overwrite `run_004_recalibrated`).
2. Owner reviews the 1 grade-flip (Alpro Choco soy 38.1/D→34.5/E) + 2 ≥2pt moves.
3. **Invariant sign-off:** confirm 85/A top trio unchanged (already verified HELD).
4. On owner accept → Frontend regenerates `milk-comparison.json` from `run_005`.

**Step 2 — Snack re-baseline (ceiling-sensitive).**
1. Rescore the 53-product snack corpus on HEAD → new pinned run.
2. **Invariant sign-off (Nutrition + Product):** confirm no bar reaches A (max HEAD
   ≈70/B); decide editorial handling of the **second 69.5/B** product now crowding
   the snk-001 ceiling. This is a presentation decision, not an invariant break.
3. Reconcile snk-XXX editorial corpus → HEAD trace values (the live page is on an
   editorial recal layer, not raw traces — that crosswalk must be re-pinned).
4. On accept → Frontend regenerates `snacks_frontend_v2.json`.

**Step 3 — Bread re-baseline (highest risk, coordinate with TASK-169F).**
1. **Do NOT rebuild bread independently.** TASK-169F is concurrently re-modelling
   bread R3/R5 for the recal. Hand 169F the §2c slice so it can subtract
   pre-existing drift (the +6/+8 base-layer lift) from recal-*intended* moves.
2. Rescore on HEAD → pinned run; expect ~18 rendered breads to move up +6/+8 and
   several C→B flips.
3. **Invariant sign-off (Product):** bread provenance stays
   `real_bread_retail_003_v1`; confirm the A-ceiling still withholds macro-only A's
   (tahini bread 82/A and crackers already reproduce — A-tops are stable); review the
   shelf-compression risk (most of the shelf rising into B narrows discrimination).
4. Decide whether the lechem-calibration-patch downstream layer is retained,
   re-tuned, or retired against the new base.
5. On accept → Frontend regenerates `bread_frontend_v2.json`.

**Step 4 — Freeze.** QA re-runs reproduction (must be 100% against the new pinned
runs by construction), then freezes each new baseline. QA cannot freeze over any
unresolved grade-flip the owner has not signed off.

**Sequencing:** Step 0 first; then Steps 1/2 in parallel; Step 3 gated on 169F.
Nothing ships from this audit — every step above is a *future* tracked rescore with
its own owner gate.

---

## 6. Hard-rule / constraint compliance

- Read-only: no published run dir, engine source, or live JSON was modified. The two
  repro harnesses (`03_operations/qa/repro_audit_178.py`, `repro_bread_178.py`) write
  nothing to product/score dirs — they print only.
- Every delta comes from an actual HEAD re-run vs the published trace (no invented
  values). Snack figures cross-checked against the independently-produced TASK-169E
  record (5/53 match).
- Frozen invariants named and checked: milk top **HELD**; snack no-A **HELD** (ceiling
  crowding flagged, not broken); bread provenance/A-ceiling **HELD**.
- Cross-link: §2c bread slice is structured for TASK-169F consumption; milk slice
  (§2a/2b) and its 13/20 measurement flagged per task.

---

## Artifacts

- This report: `C:\Bari\03_operations\qa\reports\legacy_score_drift_audit_TASK-178_2026-06-04.md`
- Milk/snack repro harness: `C:\Bari\03_operations\qa\repro_audit_178.py`
- Bread repro harness: `C:\Bari\03_operations\qa\repro_bread_178.py`
- Snack drift source-of-truth: `C:\Bari\02_products\snack_bars\bsip2_outputs\run_snackbars_006_recal_p0\run_record.json`
