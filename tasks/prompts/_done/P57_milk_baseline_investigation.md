# P57 / Diagnose: committed engine can't reproduce frozen milk 85/A (route: C1-GEMINI)

Read-only DIAGNOSIS. The frozen milk invariant (top = whole 3.4% / natural 4% / goat = 85/A,
run_005_headpin) is NOT reproduced by the current committed engine — it returns 64-65/C-B, 0/20
exact, "85/A BROKEN". This is PRE-EXISTING (not caused by the current uncommitted P56 work — proven by
stash test). Find the ROOT CAUSE. Do NOT fix, do NOT modify scores/engine. Report only. Propose RETURNED.

## Established facts (don't re-litigate)
- `python 03_operations/bsip2/proto_v0/src/batch_run_milk_005_headpin.py` → 0/20 reproduced, milk top
  85/A → 64.3/64.7/65.2. With `BARI_RECAL_P0=on` → 1/20, still broken. The harness sets NO flags.
- The whole-milk drop is ~−20pts and fat-driven (not sodium) — see the delta_table in
  `02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/run_record.json`.
- LEAD: that run_record cites `engine_baseline_commit: fce7975...`, but CLAUDE.md / the frozen-invariant
  record cite the milk freeze at engine tag `engine-baseline-2026-06-04 / f075d9e`. Possible
  baseline-commit MISMATCH (harness compares vs the wrong engine state) vs a real regression.

## Investigate
1. **Baseline provenance:** what engine commit/flag-set produced the PUBLISHED milk 85/A scores?
   Check the published milk traces' provenance + CLAUDE.md frozen invariant (`run_005_headpin`,
   `engine-baseline-2026-06-04`, `f075d9e`). Reconcile `fce7975` vs `f075d9e` — are they the same
   baseline, two commits, or is the harness pointed at the wrong one?
2. **Git archaeology:** `git log --oneline -- 03_operations/bsip2/proto_v0/src/score_engine.py
   03_operations/bsip2/proto_v0/src/constants.py` since the freeze date (2026-06-04). Which commit(s)
   changed milk-relevant scoring (fat_quality, satFat red-label, calorie_density, processing)? The
   recent "frozen vegetables: engine ECS-v1 baseline" commit is a suspect.
3. **Flag dependency:** what flag set did the milk freeze require (BARI_RECAL_P0 canonical-on for dairy,
   BARI_REDLABEL_V1 bundle, others)? Does the harness `batch_run_milk_005_headpin.py` set them? Test a
   few flag combinations and report which (if any) restores 85/A.
4. **Classify the root cause:** (A) HARNESS/BASELINE-TAG issue (harness compares vs wrong commit or
   doesn't set the canonical flags → low severity, fixable in the harness), or (B) REAL ENGINE
   REGRESSION (a committed change moved milk and wasn't flag-gated → serious frozen-invariant violation).

## Guards
- Read-only. Do NOT modify score_engine.py, constants.py, any run_record, or any published score.
- Do NOT run the uncommitted P56 work into this; you're diagnosing the COMMITTED engine.
- OFF ban absolute.

## Return (machine-readable contract)
- Reconciliation of fce7975 vs f075d9e. - The suspect commit(s) with the diff that moved milk. - The
  flag set that does/doesn't restore 85/A (with the command + result). - CLASSIFICATION: harness vs real
  regression, with evidence. - Recommended next step (do not execute it).
- End with the JSON return contract (`01_framework/operations/return_contract_v1.md`). Propose RETURNED.
