---
id: TASK-496
title: Persist BARI_REDLABEL_CONTINUOUS_V1 flag into category configs (traceability robustness) — HARD score-neutrality gate
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "MERGED LIVE PR #78 (squash). BARI_REDLABEL_CONTINUOUS_V1 persisted into cheese/cakes/chocolate_bars/chocolate_tablets configs (flag line only) + rescore_all.py isolation guard (MANAGED_BARI_VARS + MILK_CANONICAL_FLAGS). SCORE-NEUTRAL PROVEN: isolated single-shelf rescore from config (no env) = 167/167 products byte-identical score+grade vs origin/master frontend, max|Δ|=0.0, grade dists identical. Verified diff = 4 configs + harness only, 0 engine/frontend/score. bread+hard_cheeses correctly excluded. Orchestrator-merged (internal, no tripwire — 0 published-score change). FINDING logged → TASK-500 (pre-existing multi-shelf reload cross-contamination, not TASK-496-caused)."
depends_on: []
blocks: []
category_id: null
summary: >
  cheese/cakes/chocolate-bars/chocolate-tablets live scores were produced with BARI_REDLABEL_CONTINUOUS_V1=on
  supplied as an ENV OVERRIDE at scoring time — the flag is NOT persisted in the committed category configs,
  so the shadow gate / rescore harness cannot reproduce those categories without someone manually setting the
  env var. Persist the flag into the committed configs so reproduction is automatic from config alone
  ("systematic not artisanal" / traceability). THIS IS A REPRODUCIBILITY FIX, NOT A SCORING CHANGE — it MUST
  produce byte-identical scores. HARD GATE: if persisting the flag moves ANY published score, STOP and return
  as a finding (that would be tripwire-1 / owner). Do NOT ship a score change.
---

# TASK-496 — persist BARI_REDLABEL_CONTINUOUS_V1 into configs (score-neutral robustness)

## Investigation-first (understand before changing)
1. Find where the scoring engine READS BARI_REDLABEL_CONTINUOUS_V1 (env vs config precedence). Grep shows it
   passed as a config-dict key (alongside BARI_REDLABEL_V1) in rescore scripts + read from env by the engine.
   Determine the exact read path + how a category config supplies feature-flags to the engine.
2. Identify which live categories depend on it = cheese (v5), cakes, chocolate-bars, chocolate-tablets (per
   red-team reports + evidence registry). Confirm the exact set.
3. Determine the SAFEST persistence approach: add the flag = on to those categories' committed configs
   (page_generator/configs/*.json or wherever the engine reads per-category flags) such that the engine
   reads it from config when env is absent, WITHOUT changing behavior when env IS set (production).

## HARD score-neutrality gate (the whole point)
- After persisting: rescore each affected category through the spine (use the `rescore` skill) with the flag
  coming from CONFIG and NO env override, and diff against the committed live baseline (the current
  origin/master frontend scores). REQUIREMENT: **0 score / 0 grade / 0 rank movement, every product, every
  category.** Emit the self-verifying movement table (should be all-zero).
- If ANY movement appears → the flag-in-config is NOT equivalent to the env override → **STOP, do NOT ship,
  return as a FINDING** (this means env and config diverge — an owner/Nutrition matter, tripwire-1). Do not
  attempt to "make scores match" by editing scores.

## Guards
- Base off origin/master (not local HEAD — F1 divergence). Isolated worktree. OFF ban irrelevant (no data).
- Do NOT edit any frontend JSON score/grade/rank. Only the config flag + (if needed) the engine's config-read
  path. Internal/traceability → if fully score-neutral, orchestrator may merge after verifying the zero-diff.
- This is scoring-adjacent: the neutrality proof IS the safety. No neutrality proof → no ship.

## Return: 5-part + the all-zero movement table (or the finding if not neutral) + Return Contract JSON.
Propose RETURNED. Do not write CLOSED.
