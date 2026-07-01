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

## Remaining W2 work (rebuild restored the Phase-1 floor; these complete the workstream)
1. **Nutrition adjudicates the 13 disagreements** (`needs_nutrition_review`): engine_divergence vs seed_defect vs policy_ambiguous. Findings-only, never auto-fix (tripwire-1).
2. **Scale seed 30 → ~150** so it becomes a PROTECTIVE gate (C3 ruling: methodology-validation at 30, protective at 100–200).
3. **Make shadow_gate merge-BLOCKING** at the right threshold once scaled (industry: ~30 cases/PR <5min, block on regression).
4. **`content_regression.py`** — rubric LLM-judge scoring milk/brined/cereals goldens for voice+structure drift (the content arm; net-new).
