# P167 / TASK-317 — Spine step 2: affected-set resolver (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Build a new module; read-only over shadow/registry/configs. NO engine/scoring/page/bari-web edits. No commit, no deploy. Propose RETURNED.

## Goal
Turn a scoring-flag what-if into a clean "what's affected" manifest the spine orchestrator (step 4) will consume:
> given `BARI_X=on` → which categories MOVE, by how much, is any FROZEN corpus touched, and which `rescore_all` shelves must re-run.

Shadow already produces the data. Don't re-implement scoring — wrap Shadow's output.

## Inputs / contracts (verified)
- `03_operations/bsip2/proto_v0/src/shadow_backtest.py diff --set FLAG=VAL` writes `runs/shadow_<ts>/shadow_report.json`.
- `shadow_report.json` top keys: `flag_overrides, verdict, exit_code, engine_changed, corpora[...]`. Each corpus entry:
  `{name?, class, flags, n, moved, grade_changes, added_pids, removed_pids, invariant_violations, moves[]}`
  (note: confirm whether the corpus name is a key or in the entry — sample at `03_operations/shadow/runs/shadow_20260615T155350Z/shadow_report.json`).
- `03_operations/shadow/shadow_registry_v1.json` → `corpora[]` with `{name, class, source, flags, baseline_run}`.
- The rescore_all shelves / config keys: filenames in `03_operations/page_generator/configs/*.json` (cereals, granola, juices, brined_cheeses, cakes, cookies_coffee, hummus_shelfrel_002, snacks, hard_cheeses).

## Build `03_operations/page_generator/affected_set.py`
CLI:
```
python affected_set.py --set BARI_X=on [--set BARI_Y=off ...] [--report <path to existing shadow_report.json>] [--out affected_set.json]
```
- If `--report` is given, parse it; otherwise invoke `shadow_backtest.py diff --set ...` (cwd = its dir) and read the report it writes (capture the path from its stdout `written:` line or the newest runs/ dir).
- A corpus is **affected** if `moved>0` OR `grade_changes` non-empty/>0 OR `added_pids` OR `removed_pids` OR `invariant_violations`.
- Build a `corpus name → config/shelf key` map (registry/config names mostly align; handle the known alias hummus→hummus_shelfrel_002 and cakes↔cakes_hard_cookies; derive the rest by matching registry corpus name to a config category). If a moved corpus has no config (e.g. a deferred/bespoke one), list it under `affected_no_config` with a reason — don't silently drop it.
- Emit `affected_set.json`:
  ```
  {
    "flag_overrides": {...}, "shadow_verdict": "...", "shadow_exit_code": N, "frozen_touched": bool,
    "affected": [{"corpus": "...", "class": "...", "n": N, "moved": N, "grade_changes": N, "max_abs_move": X.X, "shelf": "<config key or null>"}],
    "affected_shelves": ["cereals", ...],          // the rescore_all --shelf args to re-run
    "frozen_breaches": ["milk", ...],              // frozen corpora that moved (BLOCK)
    "affected_no_config": [{"corpus":"...","reason":"..."}]
  }
  ```
- Also print a short human summary. Exit non-zero (mirror shadow: 2 if frozen_touched/invariant, 1 if non-frozen movement, 0 if none) so it's CI/orchestrator-usable.

## Verify
- Run against the sample report `03_operations/shadow/runs/shadow_20260615T155350Z/shadow_report.json` (`--report`) and show the affected_set.json + summary + exit code.
- If feasible/fast, also do one real `--set` what-if end-to-end and show it resolves (note runtime). If too slow, the `--report` path proof is sufficient — say so.
- Sanity: frozen corpus (milk) moving → frozen_touched=true + exit 2.

## Return (do NOT close — propose RETURNED)
The module + a sample affected_set.json + the exit-code behavior. Files changed (path+action+sha256). End with the TASK-317 return-contract JSON (`01_framework/operations/return_contract_v1.md`): task, proposed_status, artifacts[], counts{} (with commands), commands_run[], not_done[], self_check. Boundaries: new module only (+ no edits to shadow/engine/configs/pages); OFF-ban absolute.
