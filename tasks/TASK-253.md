---
id: TASK-253
title: "Project Shadow1 — shadow scoring: every engine change auto-backtests against the full historical corpus"
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner mandate 2026-06-11 ("full mandate to start Project Shadow1"). Tech-leap
  program from comparison_chain_tech_leaps_v1 (leap 3, "Data Trust" tier):
  quant-fund-style backtest for the scoring engine. Any engine diff re-scores
  every registered historical corpus (~700 products, 12 corpora, per-category
  shipped flag configs) and emits a per-product diff report with attribution —
  which dimension/stage/mechanism moved which score, by how much — plus an
  always-generated frozen-impact table that replaces "did this touch a frozen
  category?" as a manual check. NON-GOALS: no score changes, no methodology
  changes, no engine changes — Shadow observes the engine; it never modifies it
  or any published artifact. Read-only against all corpora.
---

# TASK-253 — Project Shadow1

## Mandate

Owner, 2026-06-11: *"full mandate to start Project Shadow1."*
Source concept: `01_framework/operations/comparison_chain_tech_leaps_v1.html` — leap 3
(Shadow Scoring), "Data Trust" tier. Kills: "did this touch a frozen category?" as a
manual check — it becomes a generated table on every change. Nutrition signs off on a
complete impact picture instead of a 12-product sample.

## Design (v1)

- **Registry** (`03_operations/shadow/shadow_registry_v1.json`): every scored corpus —
  BSIP1 source dir, corpus class (`frozen` / `published` / `candidate`), the category's
  shipped engine-flag config (seeded from the authoritative batch runners), invariant
  checks, and a deferred list (bespoke-loader corpora) with reasons.
- **Harness** (`03_operations/bsip2/proto_v0/src/shadow_backtest.py`):
  - `baseline` — score all registered corpora under their recorded flag configs at the
    current engine; persist a per-product snapshot (score, grade, dimension scores,
    pipeline-stage scores, applied caps/penalties/floors/bonuses) keyed by engine hash
    + git rev.
  - `diff` — re-score at HEAD under the **baseline's** flags (apples-to-apples), diff
    every product, and attribute each move: per-dimension deltas, the pipeline stage
    where the move entered (weighted dims → cap → penalty → floors → final), and
    changed mechanisms (fermentation bonus, binding cap, penalties, floors, NOVA,
    confidence ceiling). `--set FLAG=VAL` enables what-if runs.
  - **Frozen-impact table generated on every diff**; any movement in a frozen corpus or
    invariant violation (e.g. snack bars: no product at A or above) → exit code 2.
    Movement elsewhere → exit 1. Clean → exit 0. CI-ready.
- Generated state (`baselines/`, `runs/`) is gitignored; registry + code are the law.

## Corpus coverage (active, v1)

milk (frozen, 20) · snack_bars (frozen, 53) · yogurt run_006 (88) · yogurt_yohananof (8)
· cereals_008 (63) · cereals_multiretailer (37) · maadanim (200) · cheese_003 (59) ·
cheese_yohananof (5) · hummus canonical (69) · juices (65) · hard_cheeses (37) —
**~704 products / 12 corpora**, exceeding the ~400 in the leap spec.
Deferred (bespoke loaders, registry-listed with reasons): bread_retail_003, butter,
salty_snacks, bread_light synthesis; frozen_vegetables is score-free by design (TASK-235).

## Guards

- Shadow is **read-only** over corpora and published artifacts — it scores in memory and
  writes only under `03_operations/shadow/`.
- Shadow never sets `BARI_*` flags globally for other processes; flags are set per scoring
  pass and every known flag is pinned explicitly (no env leakage between corpora).
- A baseline is only comparable to a diff run under identical per-corpus flags; the harness
  enforces this by always replaying the baseline's recorded flags.
- Zero new Python dependencies (stdlib only).

## DoD

1. Registry exists with all active + deferred corpora, classes, flags, invariants.
2. Harness runs `baseline` and `diff` end-to-end over all active corpora.
3. Determinism proof: `diff` immediately after `baseline` reports **zero** movement.
4. Sensitivity proof: a flag what-if (`--set`) produces movement **with attribution**
   confined to the expected category, frozen table stays clean.
5. Frozen-impact table present in every diff report; exit codes wired (0/1/2).
