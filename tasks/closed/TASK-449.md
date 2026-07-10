---
id: TASK-449
title: 17 dimension-Pareto inversions on brined_cheeses (golden page): worse-on-every-dimension cheeses outrank better ones via post-dimension penalty layer (NOT red-label-cap; de-anchor 0 effect, measured)
owner: nutrition-agent
status: CLOSED
close_reason: >
  LIVE via PR #38 (merge 4b21fbfa). Orchestrator-verified full chain: engine+router commits
  code-reviewed; P461 joint-flag rebuild w/ Step-A 36/36 reproduction; two-gate (Content
  1c0f0223/dbba8afc + Adversarial QA 48c04507 w/ independent engine re-run) + targeted
  re-verify GO (e82d3c54); bake sha-identical, build exit 0; production fetch confirms new
  shelf order serving. Flagship dimension-Pareto inversion RESOLVED; 24 moves/14 flips
  downward-only; sweep preserved 3/3. Residuals routed: 2 pre-existing sub-2pt inversions
  (nutrition standing), FAQ generator decimal defect (data), stale adapter prose (TASK-460),
  flag-default-flip PR (owner tripwire-1).
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  v2 guardrail (dimension-based Pareto) surfaced 17 real inversions on brined incl. sheep feta 71.6 > salty cow 48413 66.3 (worse on all 10 dims). Cause = post-dimension penalties (sodium/sat-fat) overriding dimension ordering; likely double-counts sodium (regulatory_quality dim + separate penalty). Measured: BARI_REDLABEL_V1=on does NOT change it. Nutrition/Product D6/D7 review.
---

# TASK-449 — 17 dimension-Pareto inversions on brined_cheeses (golden page): worse-on-every-dimension cheeses outrank better ones via post-dimension penalty layer (NOT red-label-cap; de-anchor 0 effect, measured)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## DISPATCHED (2026-07-02, unattended 3AM orchestrate)
P449 → Nutrition Agent (native Sonnet), **FINDINGS-ONLY** diagnosis, run in background. Boundary: no score/engine/JSON/config edit — report only to `tasks/reports/TASK-449_brined_inversion_diagnosis_2026-07-02.md`. Objective: confirm/refute the **sodium double-count** hypothesis (regulatory_quality dimension + separate post-dimension penalty) behind the 17 dimension-Pareto inversions on the golden brined page; trace the flagship pair (sheep feta 71.6 vs cow 48413 66.3); recommend the single best fix with blast-radius words. Any resulting fix = **tripwire #1 (published scores on the golden page) → owner-gated**; this dispatch only produces the recommendation. Awaiting return → orchestrator verify → surface to owner.

## RETURN 1 → CHANGES_REQUESTED (2026-07-02, orchestrator-verified)
P449 returned a report (sha 42aa169b…). **Structural finding VALID + code-confirmed:** sodium double-count is PARTIAL-TRUE — expressed in BOTH the `regulatory_quality` dimension (score_engine.py:2108-2119, 5% weight) AND the `SODIUM_GENERAL_BANDS` post-dimension guardrail (constants.py:257-263). Boundary respected (no engine/JSON edits; git-clean on the 3 engine files). **But the flagship causal trace FAILED verification:** agent claimed bc-028 sheep feta (930mg) → −8 (700-899 band) vs bc-037 cow (1065mg) → −12, a "4-point differential = main driver." Verified against artifacts: bands are `[(900,None,12),(700,899,8),…]` and frontend JSON shows bc-028=930mg / bc-037=1065mg → **both ≥900 → both −12; differential = 0, not 4.** The stated mechanism is a band-misassignment error, and the proposed fix (remove the guardrail for brined) would NOT resolve the flagship inversion (both lose −12, gap persists). Root cause: agent's own `not_done` admits it never ran the engine (analytical derivation). **Re-dispatched once** (SendMessage to same agent): run the ACTUAL BSIP2 engine trace on the real brined corpus, find the true driver of 71.6>66.3, re-derive the fix. Keep the valid structural finding. Any fix remains tripwire #1 / owner-gated.

## RETURN 2 → ✅ VERIFIED (2026-07-02, orchestrator, against run_brined_005 traces + engine code)
Report sha 33ca04af… matches; boundary respected (score_engine.py/constants.py git-clean, 0 edits). **Real driver confirmed = R7 v1.1 Path B fermentation bonus +8** (`FERMENTATION_DIRECT_BONUS`=8 constants.py:122; feta name marker "פטה" in `CULTURED_CHEESE_NAME_MARKERS_HE` constants.py:831; Path B `cultured_cheese_name` route score_engine.py:3850-3863 fires for dairy_protein/default + name-marker + nova≤3). **Decisive trace proof:** cow 48413 is better-or-equal on ALL 10 dimensions (satiety 100 vs 71.2, fat_quality 27.5 vs 16.3, protein/nutrient higher, rest equal) yet its weighted_dimension_score 78.32 < feta's 83.61 → only an additive bonus to the feta explains it; both then take the SAME −12 sodium guardrail (differential 0, per my RETURN-1 catch). Final 71.61 vs 66.32. **Sodium double-count real but non-causal** (both −12). Nutrition D6 diagnosis COMPLETE + verified.
- **Fix (Nutrition D6 initial ruling):** restrict Path B name-marker fermentation bonus to NON-brined_food contexts (all brined are fermented by definition → the name-marker bonus doesn't differentiate within brined, only rewards marker words → systematic inversions). = published-score change on the GOLDEN page → **tripwire #1**.

## DISPATCHED — Product D7 co-sign (2026-07-02, findings-only)
P449D7 → Product Agent (native Sonnet), background. Co-sign verdict on the proposed fix (defect-or-defensible position, CO-SIGN/CONDITIONS/REJECT, blast-radius words, sequencing). No score/code/JSON edits. Completes the D6/D7 package the task calls for → then **owner go/no-go (tripwire #1)**. Awaiting return → orchestrator verify → surface complete package to owner.

## D7 RETURN → ✅ VERIFIED + PACKAGE COMPLETE → PARKED FOR OWNER (tripwire #1)
Product D7 = **CO-SIGN, Option A** (restrict Path B `is_cultured_cheese` to `context_flag != "brined_food"`). Orchestrator-verified: report now sha 0cd49116 (D7 section appended at report line 286, "## Product D7 Co-sign", verdict CO-SIGN Option A); boundary respected (score_engine.py/constants.py git-clean, 0 code edits); supporting claim spot-checked TRUE — `context_flag == "brined_food"` is already a first-class engine concept (score_engine.py:2405 EV-053, :2660 sodium_weight 0.7), so Option A is architecturally consistent (not a new mechanism). Product judged it a **clear defect** (name marker = cheese type, not fermentation quality above baseline; brined fermentation is table-stakes per constants.py:824-828 Path B purpose) — not the TASK-419 "inversion can be correct" exception.
- **D6 (Nutrition) + D7 (Product) both signed. Diagnosis + fix recommendation complete and verified.**
- **Product's co-sign CONDITIONS (implementation prerequisites, owner-gated):** (1) close the trace-serialization gap — engine must emit `fermentation_bonus_applied`/`_note` to trace JSON (bonus was proven arithmetically, not read from a field); (2) full cross-corpus baseline diff before any golden-page deploy (Rule 8 / EV-052 precedent); (3) brined grade-distribution artifact (min/max/median/stdev/histogram) with the return. Affected-product count within brined = **needs a Data Agent trace census** (not computed).
- **Blast radius (interpreted):** downward-only within brined_food; products with a `CULTURED_CHEESE_NAME_MARKERS_HE` name token (feta/bulgarian/mozzarella/כבושה/מיושנת) lose up to +8; some grade-boundary crossings likely; **zero cross-category leakage** (scoped to context_flag brined_food).
- **STATUS: IN_PROGRESS, parked. WALL = owner go/no-go (tripwire #1, published scores on the GOLDEN page).** Nothing implemented/deployed. On owner GO → supervised path: Data census + implement Option A behind a sub-flag → cross-corpus diff → both page gates → owner push.

## OWNER GO (2026-07-02) → IMPLEMENTATION DISPATCHED
Owner approved the launch-readiness report in full ("I approve all", `tasks/reports/launch_readiness_and_strategy_investigation_2026-07-02.md` P0-3 names this fix explicitly) → tripwire #1 go/no-go = **GO**. Deploy itself remains owner-gated (tripwire #2, PR click).
- **P459 → C1-GROK dispatched (2026-07-02):** implement Option A behind sub-flag `BARI_FERMENT_MARKER_BRINED_FIX_V1` in worktree `C:\bari_wt_t449` off origin/master, with Product's 3 co-sign conditions (trace serialization of the bonus, Rule-8 cross-corpus diff, grade-distribution artifact) + marker census. Bundled in same dispatch as separate commit: router_v2 "מלא" collision fix with a mandatory zero-movement cross-corpus proof (any movement → BLOCKED, back to D6).
- Pipeline after return: orchestrator verify → Content pass on any copy citing changed numbers/ranks → Adversarial QA gate → owner PR.

## IMPLEMENTATION VERIFIED (2026-07-02, orchestrator) → TWO-GATE STAGE
P459 (Grok) + P460 contract rework + surgical table regen: **C0 validate_return PASS exit 0** (orchestrator re-ran independently, --root C:\bari_wt_t449, PowerShell). Verified: commits 1a25819b (Option A: flag-gated suppression exactly on the co-signed condition + fermentation_bonus_applied/note trace emission) + 6616f78a (router "חלב" 0.70→0.85, cross-corpus zero-movement) — code reviewed directly by orchestrator; candidate `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` sha-pinned, corpus-pinned 36/36 vs live, 24 score-moves/16 grade-moves downward-only, OFF spot-proof 2/2 matches live, G4/G5/G6/G7/G8 PASS (G1/G3 pre-existing live debt, G2 WARN golden posture). ON dist: n=36 min 46.0 max 82.7 median 65.05 stdev 8.34 most_common 62(x6).
- **⚠️ For QA:** grade-mover count discrepancy between Grok return 1 (19) and contract (16) — QA must count independently from the artifact.
- **Gate 1 dispatched:** Content flip-copy (Sonnet) on the candidate. Gate 2 next: Adversarial QA (Opus, independent). Then owner PR (tripwire #2).

## CLOSED (2026-07-02) — LIVE via PR #38 (merge 4b21fbfa)
Full chain verified: engine 1a25819b + router 6616f78a (D6/D7 co-signed, owner GO); P461 joint-flag rebuild (Step-A repro 36/36); Content gate-1 re-pass 1c0f0223; Adversarial QA 48c04507 GO_WITH_FIXES (flagship Pareto inversion RESOLVED — QA re-ran the engine independently: OFF-OFF reproduces live 36/36, ON-ON reproduces candidate 36/36); RT-1/2/3 fixed dbba8afc; targeted re-verify GO e82d3c54; bake 9a2cc15f (sha-identical, build 0). Owner merged PR #38; production verified via live fetch: new shelf order serving (top = צפתית 82.7/A; former 84.1 leader correctly B). Public impact: 24 score moves / 14 grade flips, downward-only, sweep 3/3 preserved.
- **Residuals routed:** (1) 2 pre-existing sub-2pt same-grade Pareto inversions (sodium-surcharge double-count) → nutrition-agent standing item; (2) FAQ generator decimal-leakage defect → data-agent; (3) stale hardcoded distribution prose in page-data adapters discovered during post-deploy verification (pre-existing, multi-category) → **TASK-460 (CRITICAL, dispatched)**; (4) brined rescore recipe now requires TWO flags ON — default-flip engine PR pending owner (tripwire #1).
