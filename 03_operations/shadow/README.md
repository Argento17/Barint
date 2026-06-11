# Project Shadow1 — Shadow Scoring (TASK-253)

Tech leap 3 (`01_framework/operations/comparison_chain_tech_leaps_v1.html`, "Data Trust"):
**every engine change auto-backtests against the full historical corpus.** Any engine diff
re-scores ~700 products across 12 registered corpora under each category's shipped flag
config and emits a per-product diff report with attribution — which dimension / pipeline
stage / mechanism moved which score, by how much. The frozen-impact table is generated on
every diff; "did this touch a frozen category?" is no longer a manual check.

## Layout

- `shadow_registry_v1.json` — the law: every scored corpus, its class
  (`frozen` / `published` / `candidate`), its shipped engine-flag config (seeded from the
  authoritative batch runners), invariant checks, and the deferred list (bespoke-loader
  corpora) with reasons.
- Harness: `03_operations/bsip2/proto_v0/src/shadow_backtest.py` (lives with the engine
  modules it imports).
- `baselines/`, `runs/` — **generated state, gitignored.** Regenerate with one command.

## Usage

```
cd C:\Bari\03_operations\bsip2\proto_v0\src

python shadow_backtest.py baseline            # snapshot all corpora at current engine
python shadow_backtest.py status              # baseline vs HEAD engine hash
python shadow_backtest.py diff                # re-score at HEAD, diff vs baseline
python shadow_backtest.py diff --set BARI_X=on --note "what-if"   # flag what-if
```

`diff` exit codes (CI-ready): `0` clean · `1` movement in non-frozen corpora ·
`2` frozen corpus touched or invariant violated.

## Workflow for any engine change

1. Before touching the engine: `baseline` (or confirm `status` says UNCHANGED vs the
   stored baseline).
2. Make the engine change.
3. `diff` — read `runs/shadow_<ts>/shadow_report.md`: frozen table first, then the movers
   with attribution. Nutrition signs off on this complete impact picture, not a
   12-product sample.
4. After the change is approved + shipped, capture a fresh `baseline` so the next diff
   measures from the new law.

## Semantics that keep it honest

- Baseline and diff always score a corpus under **identical flags** (diff replays the
  baseline's recorded flags), so movement = engine-code behavior change, never a flag
  artifact. `--set` overrides are explicitly labeled what-ifs in the report.
- Every known `BARI_*` flag is pinned explicitly per scoring pass — no environment
  leakage between corpora.
- Read-only over corpora and published artifacts; an engine crash on a product is
  reported as a finding, not an abort.
- Engine identity = sha256 over the 9 engine source files (same set as the 169D/headpin
  run records) + git rev + dirty-engine-file list in every artifact.
