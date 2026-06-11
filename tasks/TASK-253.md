---
id: TASK-253
title: "Project Shadow1 — shadow scoring: every engine change auto-backtests against the registered scored corpus"
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
  the REGISTERED scored corpus (~700 products, 12 corpora, per-category shipped
  flag configs) — NOT yet the full historical corpus: bread/butter/salty-snacks
  need bespoke loaders (deferred, registry-listed) — and emits a per-product
  diff report with attribution —
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

## Merge gates (owner, 2026-06-11) — all three addressed in-branch

Owner directive: PR merges as **Shadow1 foundation**, not as "complete full-corpus
backtesting." Required fixes, disposition:

1. **Corpus-scope wording** — DONE: all claims renamed from "full historical corpus" to
   "registered scored corpus" (task title/summary, README + scope-honesty section,
   harness docstring, registry purpose, and a scope line stamped into every generated
   report). The "full corpus" claim is earned only when the registry's deferred list
   is empty.
2. **Yogurt trim/fermentation coupling** — DOCUMENTED: `BARI_RECAL_P0_YOGURT_TRIM` gates
   both the apex A-ceiling AND the R7 v1.1 Path-B +8 eligibility (bio-naturel
   7290102395231: trim off → loses +8 → 80.8/A → 72.8/B). Recorded in the registry
   yogurt note + README "Known engine couplings". **Splitting the flags is an engine
   change owned by Nutrition** (Shadow observes, never modifies) — open follow-up below.
3. **CI vs stable baseline** — DEFINED + IMPLEMENTED: two baseline tiers. CURRENT =
   gitignored local scratch (determinism checks, what-ifs). APPROVED = the only
   committed baseline (`baselines/approved/`, gitignore exception), rotated solely via
   `promote` (which refuses an engine-hash mismatch with HEAD) in a reviewed commit
   after a ship. CI contract: `diff --approved` on any engine-file-touching PR — HEAD
   vs the last blessed engine, **never a self-captured baseline**; exit 2 hard-blocks,
   exit 1 requires Nutrition sign-off on the report, exit 0 passes. Full law in
   README §"CI integration & baseline policy". No baseline is promoted in this PR —
   the first promotion happens at the next blessed engine state.

## Phase 1 Return Block (2026-06-11)

**Status proposal:** RETURNED — Phase 1 (registry + harness + baseline + proofs) delivered.

- **DoD 1 — registry:** `03_operations/shadow/shadow_registry_v1.json` — 12 active corpora
  (2 frozen / 6 published / 4 candidate), per-category shipped flags seeded from the
  authoritative batch runners (`batch_run_yogurt_006.py`, `batch_run_cereals_008.py`,
  `batch_run_maadanim_001.py`, `batch_run_cheese_004.py`, `batch_run_hummus_003.py`,
  `batch_run_hard_cheeses_001.py`, `run_snackbars_007_headpin.py`), snack-bars
  no-A invariant, 5 deferred corpora with reasons.
- **DoD 2 — harness:** `03_operations/bsip2/proto_v0/src/shadow_backtest.py`
  (baseline/diff/status; stdlib-only). Baseline captured:
  `baseline_20260611T165545Z`, engine `cd65ab5ef646b8b4`, **704 products / 12 corpora,
  0 scoring errors** (engine state: task-244 working tree, git `02e647f2` + dirty
  `score_engine.py`).
- **DoD 3 — determinism proof PASS:** `runs/shadow_20260611T165604Z` — verdict CLEAN,
  704/704 identical, exit 0.
- **DoD 4 — sensitivity proof PASS:** `runs/shadow_20260611T165734Z`
  (`--set BARI_RECAL_P0_YOGURT_TRIM=off`) — movement confined to yogurt (3) +
  yogurt_yohananof (1), all 4 attributed (trim ceiling removal: apex products
  89.9/A → 90.1–95.6/S at stage `weighted_dims`; bio-naturel 80.8/A → 72.8/B via
  `ferm_bonus` mechanism change — the +8/trim interaction, surfaced by Shadow, worth a
  Nutrition look). Frozen rows untouched; exit 1.
- **DoD 5 — frozen-impact table** rendered in every `shadow_report.md`; exit codes
  0/1/2 verified live (0 in determinism run, 1 in what-if run).
- **Commit/PR:** branch `project-shadow1` (off master, via worktree — main tree
  untouched), commit `f2db5928`, pushed to origin. PR creation:
  https://github.com/Argento17/Barint/pull/new/project-shadow1 (gh CLI unavailable;
  API call not permitted this session — one click to open).
- **Open for Phase 2:** bespoke loaders (bread_retail_003, butter, salty_snacks),
  published-anchor cross-check (baseline vs live frontend JSONs), CI hook so every
  engine-touching PR runs `diff` automatically (converges with Spine/TASK-252 runner).
