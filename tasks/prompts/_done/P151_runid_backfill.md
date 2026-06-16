# P151 / Backfill _meta.run_id on frontend JSONs missing it (TASK-291) (route: C2)

## ⚠️ REWORK — ROUND 2 (orchestrator, 2026-06-16). Round 1 used the WRONG matching rule.
Round 1 matched run_id by **barcode-presence** — that assigned runs that merely CONTAIN the barcodes,
not the run that PRODUCED the page's scores. Orchestrator verification:
- ✅ `cereals_frontend_v2.json = run_cereals_008` — CORRECT (scores match). **KEEP, do not touch.**
- ✅ `granola_frontend_v1.json = run_cereals_008` — CORRECT (scores match, rounding). **KEEP, do not touch.**
- ❌ `snacks_frontend_v2.json = run_snack_bars_001` — WRONG (page 60 vs trace 56.7; page 57 vs 68.0). **FIX.**
- ❌ `yogurts_frontend_v3.json = run_yogurt_006` — WRONG (page 87 vs trace 92.6). **FIX.**

**Corrected matching rule (use SCORE-PROVENANCE, not barcode-presence):** a run_id is correct ONLY if that
run's `bsip2_trace.json` `final_score_estimate` REPRODUCES the page's `score` (within rounding, |Δ|<0.6)
for a sample of ≥3 of the page's products. For `snacks_frontend_v2.json` and `yogurts_frontend_v3.json`:
search candidate runs and assign run_id ONLY to the run whose traces reproduce the page scores ≥80% of
products. If NO run reproduces them → **REVERT** (remove the run_id you added in round 1; leave it absent)
and report "no score-matching run found — ambiguous." NEVER assign a run that doesn't reproduce the scores.
Re-confirm cereals_v2 + granola_v1 are unchanged. Then the original task below still applies.

---


## Repo / context
- Repo root: `C:\Bari`. Read first: `C:\Bari\tasks\TASK-291.md`.
- Spine datastore: `03_operations/spine/spine.db` — rebuild with `python 03_operations/spine/ingest.py`.
  Tables: `live_state`, `scores(run_id, product_key, ...)`, `lineage(child_path, parent_path)`, `artifacts`.
- The exact set of files to fix = `SELECT data_file FROM live_state WHERE run_id IS NULL` (≈7 files, e.g.
  cereals_frontend_v2.json, cheese_frontend_v3.json, granola_frontend_v1.json, hummus_frontend_v5.json,
  snacks_frontend_v2.json, yogurts_frontend_v3.json). Use the query — do not assume the list.

## Objective (mechanical, unambiguous-only)
For each such file:
1. Find the authoritative source BSIP2 run for the page's products by querying `spine.db` — match the page's
   product barcodes/ids to `scores`/`lineage`, find the dominant `run_id`.
2. If ≥80% of the page's products trace to ONE run_id → set `_meta.run_id` to that run in the JSON
   (minimal edit, preserve all other fields + formatting).
3. If ambiguous (no single run ≥80%, or no match) → DO NOT guess. Leave the file unchanged and list it in
   your return as "ambiguous — needs orchestrator decision" with the run distribution you found.

## Boundaries / guards
- OFF ban (TASK-238): touch only `_meta.run_id`; never add/alter data from OFF or any source.
- Change ONLY `_meta.run_id`. Do NOT touch scores, grades, products, copy, or other `_meta` fields. No
  engine, no other files.
- Do NOT commit, push, or close. Propose RETURNED.

## Return format
- Per file: the run_id set (or "ambiguous" + run distribution).
- Confirm only `_meta.run_id` changed per file (e.g. `git diff` shows only that line).
- End with the machine-readable return contract (status RETURNED).
