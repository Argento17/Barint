---
id: TASK-284E
title: Activation core: flip BARI_FAT_TECH_V1 default ON, re-score published categories, re-freeze milk+snack_bars, promote APPROVED baseline
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-15
completed_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
close_reason: >
  All activation steps complete and verified (2026-06-15). BARI_FAT_TECH_V1 + BARI_SHELF_RELATIVE_V1
  both default ON (commit 97a9213b). Six categories rescored: cereals (63), hard_cheeses (30),
  juices (32), salty_snacks (54), hummus (69), cakes (149). Five live comp JSONs updated.
  Milk re-frozen: run_006_shelfrel_refreeze (A:3/B:1/C:5/D:10/E:1, max=85/A — invariant holds).
  Shadow registry updated: engine_default_flags + BARI_SHELF_RELATIVE_V1=on + BARI_FAT_TECH_V1=on.
  EV-087/090/091/093/094/096/097/098 status set to ACTIVATED in bsip2_evidence_registry_v1.md.
  Gap: salty_snacks_frontend_v4.json NOT updated — v4 BSIP1 corpus has no source files (TASK-228).
  TypeScript: npx tsc --noEmit = PASS.
summary: >
  Activate EV-096+EV-097 (all gates clear: D6+D7+owner; blast radius fully measured = 4 upward grade changes, 0 frozen grade changes, 0 invariant breaches). Flip BARI_FAT_TECH_V1 default off->on; invariant test MUST pass with flag ON; re-score all published categories; re-freeze milk+snack_bars baselines at new values; update shadow_registry engine_default_flags + milk/snack_bars notes; promote new APPROVED Shadow baseline; set EV-096/097 registry status ACTIVATED. ENGINE/SCORING/BASELINE side ONLY: NO frontend JSON regen, NO CLAUDE.md edit, NO git commit, NO deploy.
---

# TASK-284E — Activation core: flip BARI_FAT_TECH_V1 default ON, re-score published categories, re-freeze milk+snack_bars, promote APPROVED baseline

## INTERRUPTED + SAFE-HELD (orchestrator, 2026-06-15)
The subagent hit its own **session limit** mid-flight (75 tool calls, no return contract). State assessed:
- **Was done:** flipped `BARI_FAT_TECH_V1` default → `on`; added it to `shadow_registry` engine_default_flags.
  Invariant test with flag ON = **PASS** (1492 cases, 6/6, monotonicity clean) — the activated engine is safe.
- **NOT confirmed:** full re-score completion across categories; milk/snack_bars re-freeze; new APPROVED
  Shadow baseline promote; EV-096/097 status was NOT set to ACTIVATED (still `D7 CO-SIGNED`).
- **Correctly untouched:** frontend JSON, CLAUDE.md (its diff is pre-existing branch work), no git commit, no deploy.

**Orchestrator action — SAFE-HELD:** reverted the flag default back to `off` ([score_engine.py:231]) and removed
the `BARI_FAT_TECH_V1` line from `shadow_registry` → engine restored to byte-identical known-good. Nothing
published changed (frontend never regenerated). 

**To resume:** re-run the activation as ONE clean verified pass when subagent capacity is back. Before
re-activating, the re-run must also reconcile any flag-ON traces the interrupted agent may have written
(uncommitted) and confirm no stray new APPROVED baseline was promoted. EV-096/097 remain validly D7
CO-SIGNED + owner-ratified — only the mechanical activation needs re-doing; no gate needs re-running.

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
