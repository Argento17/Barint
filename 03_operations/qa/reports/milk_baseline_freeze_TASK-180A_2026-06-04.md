# QA Freeze Record — Milk Frozen Baseline (`run_005_headpin`)

**Task:** TASK-180A
**Date:** 2026-06-04
**Author:** QA Agent (bari-qa-audit)
**Decision right:** D9 (QA Baseline Freeze — I/A/M, sole authority) · supports D8 (score propagation post-implementation)
**Type:** Baseline freeze. No frontend / milk-comparison JSON touched. No engine edit. No data deleted.

---

## VERDICT: FREEZE — PASS

`run_005_headpin` is frozen as the **authoritative milk-and-alternatives BSIP2 baseline**, superseding
`run_004_recalibrated`. The run is internally consistent (20/20), the frozen 85/A invariant is verified
HELD, and all 3 grade-affecting moves are owner-signed. No hard fail. Cleared to freeze.

---

## 1. Pinned engine baseline (verified)

| Item | Value | Verified |
|---|---|---|
| Tag | `engine-baseline-2026-06-04` (annotated) | `git tag --list` returns it |
| Tag → commit | `f075d9e077cba3db6e50f3b85eff23a9af352992` | `git rev-list -n 1` matches run_record |
| run_record `engine_baseline_commit` | `f075d9e077cba3db6e50f3b85eff23a9af352992` | matches tag |
| BSIP1 source corpus | `C:\Bari\03_operations\bsip1\run_milk_002\output` | same corpus that produced run_004 (delta = engine state, not corpus) |

## 2. Owner-signed grade-affecting moves (the 3 that gate the freeze)

All three signed off by the owner on 2026-06-04 under TASK-180A. All downward (re-baseline tightens, does not inflate).

| # | Product ID | Name (he) | run_004 | run_005 | Δ | Class | Signed |
|---|---|---|---|---|---|---|---|
| 1 | `bsip1_5411188300328` | אלפרו שוקו משקה סויה | 38.1/D | **34.5/E** | −3.6 | **GRADE FLIP D→E** | YES |
| 2 | `bsip1_7290107932134` | חלב בבקבוק 1% מועשר — מהדרין | 60.2/C | 56.6/C | −3.6 | ≥2pt same-grade | YES |
| 3 | `bsip1_7290114313285` | מולר פרוטאין משקה בננה 25g | 49.6/D | 46.5/D | −3.1 | ≥2pt same-grade | YES |

Hard rule (cannot freeze over an unsigned grade move): **satisfied** — 0 unsigned grade-affecting moves.

## 3. Frozen-invariant verification — milk top 85/A (whole / 4% / goat)

Verified independently against each per-product `bsip2_trace.json` (`final_score_estimate` / `grade_estimate`),
not only the run_record summary block.

| Product ID | Item | Expected | Trace (run_005) | Status |
|---|---|---|---|---|
| `bsip1_7290000051352` | חלב מלא בטעם של פעם 3.4% (whole) | 85/A | 85/A | **HELD** |
| `bsip1_7290019790259` | חלב טבעי 4% (natural 4%) | 85/A | 85/A | **HELD** |
| `bsip1_7290102392094` | חלב עיזים (goat) | 85/A | 85/A | **HELD** |

All three HELD exactly. No frozen-top move. Top of shelf remains **85/A**.

## 4. Reproduction stats (vs published run_004_recalibrated)

| Metric | Value |
|---|---|
| Published scored | 20 |
| Reproduced exactly (\|Δ\|<0.05, same grade) | **13 / 20 (65%)** |
| Grade-affecting (flip OR \|Δ\|≥2pt) | 3 (all owner-signed) |
| — grade flips | 1 (D→E) |
| — ≥2pt same-grade | 2 |
| Cosmetic (<2pt, same grade) | 4 |
| Missing on head | 0 |

## 5. Internal consistency check (the freeze gate)

Method: read all 20 per-product `bsip2_trace.json`; extract `final_score_estimate` / `grade_estimate`;
test for null/NaN; cross-check each against the `run_record.json` `delta_table` head value.

| Check | Result |
|---|---|
| Product trace files present | 20 / 20 (one `bsip2_trace.json` each) |
| Missing scores | 0 |
| Null / NaN scores | 0 |
| Trace score == run_record head_score (all 20) | PASS (max abs delta < 0.05) |
| Trace grade == run_record head_grade (all 20) | PASS |
| run_record `head_scored_count` | 20 (matches) |
| delta_table rows | 20 (matches) |

**No missing, no NaN, no trace/record mismatch. Run is internally consistent.**

## 6. Marker actions (run_004 not deleted)

- **Wrote** `run_005_headpin/AUTHORITATIVE.md` — declares run_005 the frozen authoritative milk baseline.
- **Wrote** `run_004_recalibrated/SUPERSEDED.md` — retires run_004's authoritative status. run_004 had **no**
  `AUTHORITATIVE.md` file to delete (it was authoritative only via the CLAUDE.md invariant convention);
  the SUPERSEDED marker records the retirement explicitly.
- **No data deleted or overwritten** in run_004 — all its traces, run_record, and reports preserved as history.

## 7. CLAUDE.md frozen-invariant update (proposed — applied by orchestrator)

Current line:
> Milk scores = `run_004_recalibrated`. Top = 85/A (whole/4%/goat dairy). No reversion.

Proposed replacement:
> Milk scores = `run_005_headpin` (frozen 2026-06-04, TASK-180A, engine tag `engine-baseline-2026-06-04` / `f075d9e`; supersedes `run_004_recalibrated`, retained as history). Top = 85/A (whole 3.4% / natural 4% / goat dairy). No reversion.

## 8. Hard-rule / constraint compliance

- No frontend / milk-comparison JSON touched (Frontend regenerates next from `run_005_headpin`).
- `run_004_recalibrated` not deleted or overwritten; only authoritative status retired.
- No freeze over an unsigned grade move — all 3 owner-signed.
- No invented expected values — every figure read from traces, run_record, or git.
- Frozen invariant named and independently verified HELD.

## Artifacts

- This freeze record: `C:\Bari\03_operations\qa\reports\milk_baseline_freeze_TASK-180A_2026-06-04.md`
- Authoritative marker: `C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin\AUTHORITATIVE.md`
- Superseded marker: `C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\SUPERSEDED.md`
- Frozen run: `C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin\` (20 traces + run_record.json)
- Data Agent pre-sign-off memo: `C:\Bari\03_operations\qa\reports\milk_rebaseline_TASK-180A_2026-06-04.md`
- Audit basis: `C:\Bari\03_operations\qa\reports\legacy_score_drift_audit_TASK-178_2026-06-04.md`
- Pinned engine tag: `engine-baseline-2026-06-04` → `f075d9e077cba3db6e50f3b85eff23a9af352992`
