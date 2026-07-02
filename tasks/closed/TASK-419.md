---
id: TASK-419
title: De-chain Stage 2 — continuous NOVA-lookup replacement (the workstream that actually resolves the Chokita/Petit-Beurre inversion)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
closed_at: 2026-07-01
depends_on: [TASK-418]
blocks: []
category_id: null
summary: >
  Owner 2026-07-01: hold activation, BUILD Stage 2. Stage 0+D4 (ready) does NOT resolve the motivating inversion (Chokita 26.1 > Petit-Beurre 21.4 unchanged) — that needs replacing the rigid NOVA-class lookup with a continuous, label-derivable processing assessment (D6 Workstream 1, flagged 'not yet label-derivable'). Deliver: feasibility + design for continuous NOVA-subordination from label evidence, behind a flag, byte-identical off, inversion-invariant guardrail (formalize BARI-INVERSION-TEST-001 as a machine test), then shadow. Score-moving => D6/D7 + owner-gated activation later.
---

# TASK-419 — De-chain Stage 2 — continuous NOVA-lookup replacement (the workstream that actually resolves the Chokita/Petit-Beurre inversion)

## Update 2026-07-01 (orchestrator) — feasibility/design stage DELIVERED (P258, C3); dependency status
**P258 (C3 / gpt-5.5) returned the feasibility + design study** — orchestrator-reviewed, on-DoD:
- **Verdict: PARTIALLY-FEASIBLE.** A true academic "continuous NOVA" is NOT label-derivable (extrusion,
  fractionation depth, factory intent are invisible); a defensible **continuous label-observable
  processing-burden** signal IS, with NOVA demoted to a non-authoritative historical proxy.
- **Recommended: Design 1 — Refined Matrix Degradation Score** (continuous burden from refined
  starch/sugar/fat tokens + whole-food-complexity credit; additives contribute but do NOT duplicate D4;
  nutrition as corroboration). Resolves Petit-Beurre>Chokita by removing the "plain+additive-light ⇒ high
  processing quality" free pass. Designs 2/3 kept as corroboration, not primary.
- **Inversion guardrail:** formalize `BARI-INVERSION-TEST-001` as a permanent machine-executable dominance
  invariant (fixture pairs), not a one-off assertion.
Consult only — C3 never closes. Design ACCEPTED as the Stage-2 direction.

**Dependency (TASK-418):** the reproducible baseline this task must shadow against now EXISTS (TASK-429 pinned
it; landed 0a303e34). The 418 pollution-refresh is owner-gated but does not block the Stage-2 BUILD, which
shadows byte-identical-off against the pinned baseline.

**Next stage (BUILD, not yet dispatched):** implement Design 1 behind a flag (byte-identical OFF), encode
`BARI-INVERSION-TEST-001` as a machine test, run the OFF/ON shadow vs the pinned baseline. Score-neutral while
OFF + shadow = analysis; **activation is score-moving → D6/D7 + owner-gated (tripwire #1).** Sequenced AFTER the
owner rules on the 418 refresh (the ruling may reshape the baseline the shadow measures against).

## Update 2026-07-01 (orchestrator) — P277 Stage-2 BUILT + orchestrator-VERIFIED; BLOCKED on a reweight decision
Worktree `C:/bari_p277` (branch `p277/stage2-continuous-proc`). All DoD *deliverables* met; the task GOAL
(resolve the inversion) is NOT achieved by Design 1 alone — needs a scoring-weight decision (tripwire).
- **Byte-identical-OFF (hard safety) ✅ VERIFIED independently:** flag `BARI_PROC_CONTINUOUS_V1` defaults off in
  both engine files; HC canonical harness = 31/31 drift 0; cross-engine diff master-vs-p277(off) = **0 delta on
  snacks(51)+chocolate_tablets(123)** (+ agent's full 16-shelf rescore_all = 0). Reversible, score-neutral off.
- **`BARI-INVERSION-TEST-001` machine test ✅ built** (`src/test_bari_inversion_001.py`, real pair 74184 פתי בר
  vs 61245 שוקוציפס). **FAILS both OFF (21.4>15.6) and ON (20.9>15.4)** — reported honestly.
- **Design 1 implemented** (signal_extractor + score_engine, NOVA demoted to proxy behind the flag). It penalizes
  the plain cookie's processing correctly (processing_quality 35→32) but at 15% dimension weight can't flip the
  pair — the chocolate cookie has a genuinely worse sugar/fat panel. Agent REFUSED to curve-fit a ~37pt swing
  for one pair (correct per "don't manufacture differentiation" [[butter_clustering_honest_finding]]).
- **OFF/ON shadow (16 shelves):** flag ON moves 700/1119 scores, 51/1119 grade moves (direction-sane on spot
  check). This is what activation WOULD do; NOT activated.

**WALL — owner + Nutrition decision (tripwire #1):** resolving the inversion requires either (a) accepting the
current ranking as correct (plain-refined-with-better-panel legitimately outranks chocolate-with-worse-panel —
possibly NOT a real defect), (b) raising the processing dimension weight as philosophy (moves ALL published
scores = tripwire), or (c) revising the design. The safe machinery is in place to evaluate any choice in shadow.

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Update 2026-07-01 (orchestrator) — RULED (P279, Nutrition) + orchestrator-VERIFIED → CLOSED
**Ruling: the Petit-Beurre>Chokita ordering is NOT a defect — it is correct.** Verified on the real label
records: chocolate cookie 61245 is worse on every macro axis vs plain 74184 — 527/460 kcal, 34/22g sugar,
28.2/14g fat, and decisively **11.9/4.0g sat-fat** (61245 crosses the >5.0 red-label line → 2 red labels vs 1).
The engine correctly credits 61245's complexity (processing 44>35, additive 48>30, combined weight 0.25) but
that can't and shouldn't overcome its worse macro dimensions (weight 0.40). So 21.4>15.6 is the right ordinal
call (both grade E). No feasible processing reweight flips it without blunting legitimate sugar/fat/red-label
sensitivity = curve-fitting one pair (rejected, per [[butter_clustering_honest_finding]]).
**Resolution:** no scoring change; no activation. Stage-2 machinery (flag `BARI_PROC_CONTINUOUS_V1`, Design 1,
byte-identical OFF — verified) preserved as a DORMANT validated scaffold on branch `p277/stage2-continuous-proc`
(commit f449d8cb, NOT on master); its future activation is a separate D6/D7 decision on its own merits, not an
inversion fix. `BARI-INVERSION-TEST-001` as written encodes a false invariant (whole-food markers overriding a
worse macro panel) → flag for retire/reframe with a genuinely comparable fixture. CLOSED.
