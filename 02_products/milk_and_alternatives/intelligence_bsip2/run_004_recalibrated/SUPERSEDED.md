# SUPERSEDED — Authoritative status retired

**`run_004_recalibrated` is NO LONGER the authoritative milk baseline.**

| Field | Value |
|---|---|
| Superseded by | `run_005_headpin` |
| Retired by | QA Agent |
| Retire date | 2026-06-04 |
| Task | TASK-180A |

## What changed
- `run_005_headpin` rescored the same milk corpus on the pinned engine tag
  `engine-baseline-2026-06-04` (commit `f075d9e077cba3db6e50f3b85eff23a9af352992`)
  and is now the frozen, authoritative milk baseline.
- Reproduction vs this run: 13/20 exact; 3 grade-affecting moves (owner-signed 2026-06-04),
  4 cosmetic. Frozen top trio (whole 3.4% / natural 4% / goat) held at 85/A.

## What this marker does and does NOT do
- **Does:** retire this run's authoritative status. Future page regeneration must read `run_005_headpin`.
- **Does NOT:** delete or modify any data in this directory. All `run_004_recalibrated` traces,
  `run_record`, and reports are preserved as history.

## References
- New authoritative marker: `..\run_005_headpin\AUTHORITATIVE.md`
- QA freeze record: `C:\Bari\03_operations\qa\reports\milk_baseline_freeze_TASK-180A_2026-06-04.md`
