---
id: TASK-395
title: De-chain the BSIP engine — continuous assessment over prescriptive caps/NOVA-lookups (give the algorithm freedom; NOVA = workstream 1; inversion-invariant guardrail enables it)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-24
depends_on: [TASK-409]
blocks: []
category_id: null
activation_eval: "RETURNED + orchestrator-VERIFIED 2026-07-01. Eval artifacts _rescore_staging/_dechain_activation_eval_20260701/ (headline counts re-checked vs aggregate json: 845 scored; Stage0-alone 0 affected byte-clean; Stage0+D4 224 affected all-downward -8..-2, 7 grade movers, 0 large movers >15, 0 inversions; Chokita 26.1>Petit 21.4 UNRESOLVED; baseline reproduces 10/12, NOT granola+hard_cheeses). Verdict: SPLIT activation — GO 10 (5 unconditional + 5 conditional on copy re-audit) / NO-GO 2 (granola, hard_cheeses baselines don't reproduce). Chokita/Petit inversion (the motivating case) needs Stage 2 NOVA-replacement, not this stage. AWAITING OWNER go/no-go (tripwire-1). No flag flipped, no deploy."
summary: >
  Owner directive 2026-06-24: give the scoring engine more freedom to assess products continuously; remove as many hard 'chains' (caps, rigid NOVA-class lookups, binary red-label caps) as possible, keeping only genuine safety vetoes + an outcome-level dominance guardrail. Originated from the verified Petit-Beurre/Chokita NOVA inversion (P396 debate: Nutrition+RedTeam+C3). Touches published scores across all 12 categories => D6/D7 + conformance + drift + re-audit; owner-gated deploy.
---

# TASK-395 — De-chain the BSIP engine — continuous assessment over prescriptive caps/NOVA-lookups

## UPDATE (2026-07-01 reconciliation): TASK-409 dependency SATISFIED — now blocked on the owner-gated activation go/no-go
TASK-409's clean re-derive/provenance reconciliation LANDED on origin (repro commit series + merged
PRs #30–#32; local == origin 0/0) and is registered CLOSED. The resume trigger's precondition ("409
clean re-derive landed") is therefore met. What remains BLOCKED is *activation itself*, which is a
score-moving, owner-gated go/no-go across all 12 categories (tripwire-1) — NOT an orchestrator move.
Next forward step when the owner opens activation: re-run the de-chain shadow against the now-committed
clean baseline, then D6/D7 + conformance + drift + re-audit. (Caveat: closure of 409 rests on committed/
merged-PR evidence, not a fresh end-to-end round-trip gate run — recommend that confirming pass as the
first activation step.)

## State (2026-06-26): BLOCKED on TASK-409 — parked one step behind the clean baseline (owner-endorsed sequencing)

**Build phase done + shadow-validated.** The de-chain mechanism (continuous processing
signal + NOVA subordination = `BARI_DECHAIN_V1`; ingredient-confidence gate = `BARI_INGCONF_V1`)
is built behind feature flags, **default OFF, byte-identical when off** (verified 0/53
mismatches, multiple runs). Shadow re-shadow on cleaned data complete (Phase A/B/C report:
`03_operations/bsip2/proto_v0/.../_shadow_v4/PHASE_ABC_REPORT.md`): 0 large movers >15 on
reproducing categories, 0 ingconf invariant violations; RT-1/RT-2 resolved, RT-5 traced to
the TASK-407 lexicon gap (nutrition lane), macro-inference retired.

**Why BLOCKED, not IN_PROGRESS:** the only forward move is *activation*, which is a
score-moving owner-gated go/no-go. TASK-409 is concurrently re-deriving the **whole corpus on
the cleaned data** (a separate score movement). Activating de-chain on top of that would land
two score-moving programs at once and destroy per-change attribution — the exact thing the
traceability work exists to protect. So de-chain waits until TASK-409's clean re-derive becomes
the new published baseline; THEN evaluate de-chain activation against the clean baseline, one
cleanly-attributable move at a time.

**Resume trigger:** TASK-409 clean re-derive landed + accepted as the new baseline → re-run the
de-chain shadow against the clean baseline, then D6/D7 + conformance + drift + re-audit for an
activation go/no-go (owner-gated).

**Note:** the traceability/prevention handoff that consumed this chat (snacks/hard_cheeses
bindings + harness fix) is a SEPARATE, now-CLOSED workstream — released to TASK-409
(commit c38bc6fad; reply `tasks/handoffs/dechain_STEP1_reply_to_orchestrator_2026-06-26.md`).
It is not TASK-395 itself.


## OWNER GO — red-label DE-ANCHOR activation (2026-07-01, "go with your recommendation")
Owner directive: "drift away almost completely from the red-label things." Confirmed (Nutrition + orchestrator) that this = ACTIVATE BARI_REDLABEL_V1 / this de-chain program (continuous severity replaces binary red-label caps). Owner GO on staged rollout, zero-change categories first; each grade-moving stage returns for owner go-live.

**Verified activation shape (aggregate_activation_eval, orchestrator-checked):** Stage-0 alone 0-affected byte-clean; Stage-0+D4 224/845 affected (-8..-2, median -2), 7 grade movers, 0 large movers >15, 0 new inversions. De-anchor is NOT uniformly downward (BabyBel D->C up; undisclosed-sat-fat products down = correct signature). TASK-442 tighter-thresholds PARKED behind this (would churn opposite direction). Track B copy honesty fix ships independently.

**Rollout (Nutrition-recommended, owner-approved):** Stage 0 (0-change) -> Stages 3-4 (graduated sugar) -> Stage 5 (BARI_REDLABEL_V1 cross-category, SEPARATE D7) -> Stage 6 (S-8 cap) -> Stage 8 (fat cap F-1, last, owner-gated). Per stage: zero-flip cats first.

**TWO PREREQUISITES (in flight, must clear before grade-moving stages):**
1. **Correct inversion guardrail** — the existing inversion_invariant.py FALSE-POSITIVES (fires 6 on brined; its 4-signal panel omits sodium/protein which drive cheese scores). Nutrition dispatched to design a correct dominance predicate (likely dimension_scores-based) + machine test. NOT landing the broken gate.
2. **Track B MoH copy honesty fix** — dispatched (correct false MoH threshold attributions; de-emphasize red-label framing).

**DEPENDENCY:** baseline reproduction — activation_eval shows flag-OFF does NOT reproduce committed published baseline on the shelves (PRE-EXISTING-DRIFT, 114/453 mismatch) = the corpus-traceability problem. Valid measurement is flag ON-vs-OFF on identical corpus, but DEPLOYING de-anchored scores to live needs the baseline resolved (which corpus is truth). Ties to TASK-409/corpus_traceability. NO-GO categories: granola + hard_cheeses (baselines don't reproduce).

**CAVEAT:** de-anchor does NOT resolve the Chokita/Petit-Beurre NOVA inversion (separate chain = Stage 2 NOVA-replacement).
**Status: activation AUTHORIZED, staged; Stage 0 clearable now; grade-moving stages gated on the 2 prerequisites + baseline resolution.**


## PREREQUISITE UPDATE (2026-07-01) — inversion guardrail MET; de-anchor↔inversion measured
**Guardrail prerequisite CLEARED:** correct guardrail built + landed (inversion_invariant_v2.py, commit 412dbdce) — dimension-based Pareto over the engine's own 10 dimension_scores. Old panel gate was BOTH false-positive (6 on brined) AND false-negative (missed 17 real). Not wired blocking (would block live brined; Product/D7 call).
**MEASURED (honest, hypothesis refuted):** de-anchor (BARI_REDLABEL_V1=on) does NOT change brined scores (0/0) and does NOT reduce brined's 17 v2-inversions. So the brined inversions are a SEPARATE post-dimension-penalty issue (over-penalizing salty cheeses; likely sodium double-count), NOT red-label-cap-induced -> TASK-449 (Nutrition/Product). De-anchor and these inversions are orthogonal on brined.
**Implication for de-anchor:** proceeds on its own merits (moves scores in OTHER categories per eval; brined 0-change). v2 guardrail is now the de-anchor SAFETY METRIC: each de-anchor stage must not INCREASE v2-inversions in the categories it moves.
