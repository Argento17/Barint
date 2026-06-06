# AUTHORITATIVE — Milk Frozen Baseline

**This run (`run_005_headpin`) is the authoritative, frozen milk-and-alternatives BSIP2 baseline.**

| Field | Value |
|---|---|
| Run ID | `run_005_headpin` |
| Task | TASK-180A |
| Frozen by | QA Agent |
| Freeze date | 2026-06-04 |
| Engine baseline tag | `engine-baseline-2026-06-04` (annotated) |
| Engine baseline commit | `f075d9e077cba3db6e50f3b85eff23a9af352992` |
| BSIP1 source corpus | `C:\Bari\03_operations\bsip1\run_milk_002\output` |
| Products scored | 20 / 20 (no missing, no NaN/null) |
| Reproduction vs run_004 | 13/20 exact (65%); 3 grade-affecting (owner-signed), 4 cosmetic |
| Frozen top trio | 85/A — whole 3.4% / natural 4% / goat — **HELD** |

## Status
- **Supersedes:** `run_004_recalibrated` as the milk frozen baseline (see that run's `SUPERSEDED.md`).
- **Owner sign-off:** All 3 grade-affecting moves signed off by the owner on 2026-06-04 under TASK-180A,
  including the Alpro Choco soy flip `bsip1_5411188300328` 38.1/D → 34.5/E.
- The milk comparison page is to be regenerated **from this run**.

## ⚠️ Live-page score override above this baseline (do NOT silently revert on rebuild)
- **Rice drink `8000215204219` (= page key `8000215204219`): live page shows 52.3/C, NOT this run's 49.4/D.**
  This is a **deliberate owner-approved manual override** shipped under TASK-169C (commit `191b658`,
  "ship rice drink D->C"; frontend 52.3 = recal raw 55.31 − builder ~3.0 calibration). The owner
  re-confirmed it on 2026-06-04 (TASK-180A): **the override WINS over the frozen-engine value.**
- **Any future milk rebuild MUST re-apply rice = 52.3/C** (or whatever the owner has most recently
  signed) on top of this run, rather than overwriting it with the engine's 49.4/D. Re-confirm with the
  owner before changing rice. This run scores rice 49.4/D for engine-consistency; the page is the
  override layer. See [[milk_rebaseline_run005_task180a]].

## QA freeze record
`C:\Bari\03_operations\qa\reports\milk_baseline_freeze_TASK-180A_2026-06-04.md`

## Hard rules honored
- Frozen invariant (milk top 85/A) independently verified HELD against per-product traces.
- No frontend / milk-comparison JSON touched by this freeze.
- `run_004_recalibrated` data left intact (history); only its authoritative status retired.
- No freeze over an unsigned grade move — all 3 moves owner-signed.

Do not hand-edit per-product traces or `run_record.json` in this run. Re-baselining requires a new run + a new QA freeze.
