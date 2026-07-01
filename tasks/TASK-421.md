---
id: TASK-421
title: W2: Golden regression suite — scale gold set 30->150, merge-blocking CI gate, + content/voice regression
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-420]
blocks: []
category_id: null
summary: >
  Scale gold_set_seed_v0.json 30->~150 (Nutrition adjudicates); wire shadow_gate.yml to block merge/promote on regression past threshold, <5min. Add content_regression.py: rubric LLM-judge scoring milk/brined/cereals goldens for voice+structure drift. Score-neutral (gold_check changes no published score).
---

# TASK-421 — W2: Golden regression suite

## Blocker RESOLVED — gold set REBUILT (was lost in the port/reset) ✅ verified 2026-07-01
The original gold-set files were built in worktrees, never committed, and lost when the worktrees
were removed. Rebuilt from the surviving spec (`03_operations/shadow/goldset/phase0_nutrition_grounding.md`
+ recovered P237–P242 prompts). Data Agent rebuilt 4 files + CI step under `03_operations/shadow/goldset/`:
- `gold_set_schema.json` (sha 33505071) — 13-rule contract incl. independence firewall + OFF-ban on rubric basis.
- `gold_set_seed_v0.json` (sha 0c8513e3) — 30 entries (10 good/10 poor/10 adversarial), blind-authored,
  0 engine-score leak, 0 OFF basis, grade cutoffs exact (S≥90/A80/B65/C50/D35/E0).
- `validate_goldset.py` (sha bc6b3450) — schema validator, exit 0 on the 30-seed.
- `gold_check.py` (sha 95eff6b8) — accuracy harness importing score_corpus from shadow_backtest (no dup path).
- `shadow_gate.yml` — gold_check CI step (exit 2 = ::warning:: non-blocking, per P238/P240; protective only after scaling).

**Orchestrator-verified independently:** validate_goldset exit 0; gold_check exit 2 (deterministic findings,
not a crash); **reproduces 5 published baseline scores EXACTLY** (milk 85.0/A, 33.5/E, 46.2/D, 49.7/D; yogurt 80.8/A);
verdicts PASS:10 ADVISORY:3 FAIL:13 UNVERIFIABLE:4, grade+score agreement 13/26 (50%); **no tracked
engine/score/config file modified (tripwire-1 clean)**; the lone "OFF" grep hit is the seed's own ban-declaration
note, not a data dependency (0 real OFF). 4 UNVERIFIABLE = corpus dirs absent in this checkout (findings, not failures).

## W2 completion status (2026-07-01)
1. **Nutrition adjudication — ✅ DONE + applied.** `adjudication_v0.md`: 13 → 7 engine_divergence (accept) / 6 seed_defect / 0 ambiguous. Found the seed was systematically low on brined cheeses (3 interacting flags un-pre-computed). Applied the 6 corrected bands to the seed (G-007/G-010 clamped to C's cutoff for R5). gold_check now PASS:16 FAIL:7 (was 10/13), agreement 50%→73%. The 7 remaining FAILs are the accepted divergences.
2. **Merge-BLOCKING protective gate — ✅ DONE.** Added `gold_check --baseline / --write-baseline`: blocks (exit 1) ONLY on a REGRESSION (an accepted PASS/ADVISORY entry newly FAILing), never on standing accepted divergences. Captured `accepted_baseline_v0.json`; `shadow_gate.yml` flipped to `--baseline` mode. Verified: real baseline → exit 0; simulated PASS→FAIL → exit 1 BLOCK naming the entry.
3. **content_regression.py — ✅ DONE + shipped** (content arm; freezes milk/brined/cereals golden copy, flags drift via pluggable judge).
4. **Scale seed 30 → ~150 — ⏳ RE-DISPATCHED.** First dispatch failed silently (ran 29min, persisted 0 entries). The protective-gate MECHANISM is live at 30; scaling is coverage expansion. Re-dispatched with incremental-write instructions. On return: re-run `--write-baseline` to re-capture the accepted baseline at ~150.

**Net: the protective gold-set gate is FUNCTIONAL and merge-blocking today at 30 entries; scaling to 150 (in flight) widens coverage.**
