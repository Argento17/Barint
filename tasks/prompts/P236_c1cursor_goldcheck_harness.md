(route: C1-CURSOR)

# P236 — Gold Set Phase 1: build the `gold_check.py` accuracy harness (TASK-349)

Spec-complete build. Read `tasks/TASK-349.md` and `03_operations/shadow/goldset/phase0_nutrition_grounding.md`
first. The Gold Set is an ACCURACY gate, sibling to Shadow1 (`03_operations/bsip2/proto_v0/src/shadow_backtest.py`).
Shadow checks whether a score CHANGED; this checks whether a score is RIGHT vs reviewed expectations.

## Repo / paths
- Repo root: `C:\Bari` (you are in an isolated checkout — work only in these paths).
- BUILD THIS FILE ONLY: `03_operations/shadow/goldset/gold_check.py` (stdlib only, no new deps).
- Reuse, do not duplicate, the scoring path from `shadow_backtest.py`: import and reuse its
  `score_corpus(source, flags, shelf_rel)`, `lookup_shelf_rel`, `resolve_sources`, `engine_hash`,
  `load_registry`, `corpus_configs` helpers (same dir-relative import trick it uses). Do NOT re-implement scoring.
- INPUT it consumes at runtime: `03_operations/shadow/goldset/gold_set_seed_v0.json` (built in parallel by
  another lane — assume the SHARED CONTRACT below; if the file is absent, exit 3 with a clear message).

## SHARED GOLD CONTRACT (identical across P236/P237/P238 — build to this exactly)
Top level: `{ "schema_version": "v0", "source_baseline": "<id>", "note": "...", "entries": [ <entry>... ] }`
Entry:
```
{
  "id": "G-001", "pid": "bsip1_...", "corpus": "milk", "tier": "good|poor|ambiguous",
  "scoring_flags": { ... },                 // exact per-corpus flag config (apples-to-apples)
  "expected": {
    "grade_band": ["B","C"],                // inclusive list of acceptable grades (S/A/B/C/D/E)
    "score_range": [50, 64],                // inclusive numeric range
    "dimensions": { "fat_quality": "low", "nutrient_density": "high" }  // 0-4 dims, direction labels
  },
  "rubric": [ {"criterion":"...","rationale":"...","basis":"USDA FDC|BSIP0 panel|direct product scrape","citation":"..."} ],
  "provenance": { "authored_by":"...", "authored_blind": true, "reviewed_by":"...", "agreement":"yes|no|pending" }
}
```
- The gold entry NEVER stores the engine's actual score/grade — the whole point is independence. Fetch
  the engine output at runtime and compare against `expected`.
- Dimension direction cut-points (0–100 dim scores): **low ≤ 45, medium 46–69, high ≥ 70.** Treat a dim
  within ±5 of a boundary as BORDERLINE (advisory, not fail).

## Objective — the harness must
1. Load the seed. For each entry, score that product at HEAD under `entry.scoring_flags` via the reused
   shadow scoring path (pin shelf_rel like shadow does for shelf-relative corpora). Get actual
   score / grade / dimension_scores.
2. Per entry, evaluate three checks: grade ∈ grade_band; score ∈ score_range; each expected dimension
   direction satisfied (per cut-points). Verdict: **PASS** (all satisfied), **ADVISORY** (only borderline
   misses — score within ±3 of range or a dim borderline), **FAIL** (grade outside band, or score clearly
   outside range, or a dim direction clearly violated).
3. Aggregate: agreement % = PASS / total; full verdict distribution; a **findings list** of every FAIL
   (pid, expected vs actual, which check failed) — these are FINDINGS routed to Nutrition, NOT fixes.
4. Exit codes: **0** = all PASS · **1** = advisories only (no FAIL) · **2** = ≥1 FAIL · **3** = harness
   error (missing seed/source). Print a summary; write `goldset/runs/<ts>/gold_report.{json,md}`.
5. CLI: `python gold_check.py [--seed PATH] [--gold-id G-001 ...]`. stdlib only.

## Boundaries / guards
- READ-ONLY over the engine and all corpora and published scores. You score IN MEMORY only. Never write
  to score_engine/constants/configs/page-JSON; never run a rescore that mutates state; never run git.
- OFF ban (absolute): no Open Food Facts anywhere.
- A gold disagreement is a FINDING, never an engine change. The harness MUST NOT modify the engine to pass.
- Determinism: two runs at the same HEAD must produce identical verdicts.

## Return format
Path + sha of gold_check.py, the CLI help, and a dry-run note (if the seed exists, paste the summary +
exit code; if not, show the exit-3 message). End with the return contract. Do not close — propose RETURNED.

```json
{
  "task": "P236", "proposed_status": "RETURNED",
  "artifacts": [{"path": "03_operations/shadow/goldset/gold_check.py", "action": "created", "sha256": "<hash>"}],
  "counts": {"lines": "<n>", "exit_codes_implemented": "4/4 (0/1/2/3)"},
  "commands_run": [{"cmd": "python 03_operations/shadow/goldset/gold_check.py --help", "exit_code": 0}],
  "not_done": [], "self_check": "reused shadow score_corpus (no duplicate scoring path); determinism: <observed>"
}
```
