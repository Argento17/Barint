# Project Shadow1 — Shadow Scoring (TASK-253)

Tech leap 3 (`01_framework/operations/comparison_chain_tech_leaps_v1.html`, "Data Trust"):
**every engine change auto-backtests against the registered scored corpus.** Any engine
diff re-scores ~700 products across 12 registered corpora under each category's shipped
flag config and emits a per-product diff report with attribution — which dimension /
pipeline stage / mechanism moved which score, by how much. The frozen-impact table is
generated on every diff; "did this touch a frozen category?" is no longer a manual check.

**Scope honesty (Shadow1 foundation):** this is NOT yet the full historical corpus.
bread_retail_003, butter, and salty_snacks require bespoke loaders and are registry-listed
as deferred with reasons; the "full corpus" claim is earned only when the deferred list is
empty. Until then, every report speaks for the registered corpora only.

## Layout

- `shadow_registry_v1.json` — the law: every scored corpus, its class
  (`frozen` / `published` / `candidate`), its shipped engine-flag config (seeded from the
  authoritative batch runners), invariant checks, and the deferred list (bespoke-loader
  corpora) with reasons.
- Harness: `03_operations/bsip2/proto_v0/src/shadow_backtest.py` (lives with the engine
  modules it imports).
- `runs/` and `baselines/*` — generated state, gitignored — **except**
  `baselines/approved/`, which is committed: it holds the APPROVED baseline that CI
  diffs against (see "CI integration & baseline policy").

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

## CI integration & baseline policy (stable baseline, never self-comparison)

Two baseline tiers with different jobs:

| Tier | Where | Lifecycle | Use |
|---|---|---|---|
| CURRENT | `baselines/` (gitignored) | recaptured freely, local scratch | determinism check, local engine work, what-ifs |
| APPROVED | `baselines/approved/` (**committed**) | rotated only by `promote` + a reviewed commit | the only baseline CI may use |

A CI run that captures a baseline and diffs at the same HEAD proves nothing — it compares
the engine with itself. The CI contract is therefore:

1. **Trigger:** any PR whose diff touches one of the 9 engine files (the `ENGINE_FILES`
   set in `shadow_backtest.py`).
2. **Run:** `python shadow_backtest.py diff --approved` — HEAD code vs the committed
   APPROVED baseline (the last blessed engine state). Refuses to run if none is promoted.
3. **Gate:** exit 2 (frozen touched / invariant violated) → hard block, no override in CI.
   Exit 1 (movement) → block until Nutrition signs off on the attached `shadow_report.md`
   (the complete impact picture). Exit 0 → pass.
4. **Rotation:** after the engine change ships, run `baseline` then `promote` at the
   blessed engine state and commit `baselines/approved/` in the shipping PR — baseline
   rotation is itself a reviewed change, never automatic. `promote` refuses a baseline
   whose engine hash differs from HEAD, so a stale capture can't be blessed by accident.

The actual CI wiring (workflow file) is Phase 2 and converges with the Spine runner
(TASK-252); the contract above is the law it must implement.

## Known engine couplings (documented, not fixed here)

- **Yogurt trim ↔ fermentation Path B** (Shadow finding, 2026-06-11, run
  `shadow_20260611T165734Z`): `BARI_RECAL_P0_YOGURT_TRIM` does not only cap the yogurt
  apex at 89.9/A — with it OFF, the R7 v1.1 Path-B +8 fermentation bonus is also lost
  (bio-naturel 7290102395231: 80.8/A → 72.8/B). Interpreting a trim what-if as "cap only"
  is therefore wrong. Splitting the two behaviors into independent flags is an engine
  change owned by Nutrition (tracked in TASK-253 follow-ups); Shadow documents the
  coupling and will verify the split when it lands.

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
