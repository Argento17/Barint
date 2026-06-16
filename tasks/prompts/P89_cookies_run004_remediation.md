# P89 — Data remediation → run_cookies_004 (route: C1 / Data)

**Task:** TASK-275. **Lane:** C1 Data. Execute the P88 Nutrition ruling + RT-6 additives fix → run_cookies_004.
Ruling: `02_products/cookies_coffee/methodology/cookies_coffee_redteam_scope_ruling_v1.md`. Red-team report:
`reports/red_team_cookies_page_v1.md`.

## Do
1. **Drop 2 → OUT_OF_SCOPE** in `factory_run_001/corpus_filter.json` (retain data, don't delete):
   - `ck-7290106656727` (עוגיות חיוכים — Elite children's character cookie, §1.3).
   - `ck-7290119043149` (לה פזואלוס butter — 1-ingredient truncated parse, NOVA-2 artifact, missing_data_discard_rule).
2. **Re-route `ck-80083764` (עוגיות דגנים שיבולת שועל — oat) to `biscuit`** — Nutrition §1.4 (oat/whole-grain IN).
   It currently routes to snack_bar_granola because P75b's `עוגיות` anchor excludes `דגנים`. Refine the router
   **TARGETED**: allow named-`עוגיות` OAT biscuits (`שיבולת שועל`) to reach `biscuit`, while granola/cereal stay
   excluded. **HARD GATE (Product C2 / tripwire-1):** re-run engine_invariants (342 6/6) + the bleed-sim across
   ALL live corpora — must stay **0 hits**, AND no live published score moves. **If the targeted re-route
   re-admits ANY granola/cereal/live product (bleed > 0) → DO NOT ship it; instead drop ck-80083764 to
   OUT_OF_SCOPE too (corpus 58) and report that.** The safety proof decides.
3. **RT-6 additives re-parse** — 4 products show E-codes in displayed ingredients but empty `d4_additives`:
   VOILA flower (E200 sorbic acid + E160a), 3 VOILA/לה פזואלוס oat products (E500/E450). Re-parse their
   ingredient text → populate `d4_additives` with the real E-codes (name + number). Scan all remaining
   products for the same parse gap.
4. **Re-score → run_cookies_004** on the final corpus (59, or 58 if the re-route fails the bleed gate). Same
   flag config as run_003 (RECAL_P0 off, all brined/grad/shelf off).

## Report (the gating numbers)
- Final corpus count; new grade distribution; **the empirical MAX score+grade** (does anything reach B? — this
  unfreezes the RT-7 ceiling claim for Content); the re-routed oat product's new score/grade/category (expect
  ~biscuit, ~61/C, snack-bar caps gone); bleed-sim result (MUST be 0); engine_invariants (342); OFF 0;
  d4_additives now populated for the 4 RT-6 products (list them).

## Guards
OFF ban absolute. No fabrication. Frozen invariants untouchable — bleed-sim + live-score diff are the
tripwire-1 gate; STOP/fallback-to-drop on any movement. Don't delete dropped products' data.

## Return
Return contract: task=P89, proposed_status=RETURNED, artifacts (corpus_filter.json + router_v2.py if changed +
run_cookies_004 run_record + bleed report, all +sha256), counts (corpus_final, dist, max score/grade, oat
product new score+category, bleed_hits=0, invariants, off=0, additives_fixed=N), commands_run (exit codes),
not_done, self_check. Propose RETURNED — do NOT close. Orchestrator re-runs invariants + bleed + verifies dist.
