# P88 — Nutrition ruling: red-team scope/routing findings (route: C1 / Nutrition)

**Task:** TASK-275. **Lane:** C1 Nutrition. Rule on the scope/routing findings from the Stage-9 red-team
(`02_products/cookies_coffee/reports/red_team_cookies_page_v1.md`). Scores = run_cookies_003. Ground every
call in the methodology (`cookies_coffee_scoring_interpretation_v1.md` §1.3 + `_routing_ruling_v1.md`) + the trace.

## Decide (each: IN / OUT / re-route, with reason)
1. **RT-2 — grain product `ck-80083764` (עוגיות דגנים עם שיבולת שועל — גנדולה).** Trace: `category=snack_bar_granola`
   (the `דגנים` signal beat the `עוגיות` biscuit anchor); sugar 17.0 (<17.5, doesn't cross), scored 55/C under
   SNACK-BAR caps, not biscuit caps. Is this a coffee biscuit (→ re-route to biscuit + re-score) or a grain
   snack (→ OUT of this page)? Orchestrator recommendation: **OUT** (it's lens-inconsistent — scored as a
   snack bar, doesn't belong on the biscuit shelf). Rule + reason.
2. **RT-4 — `ck-7290106656727` (עוגיות חיוכים שוקולד — עלית).** §1.3 explicitly excludes **children's
   character cookies**. "חיוכים" (smileys) is Elite's character children's cookie. Score 15.4/E. Orchestrator
   recommendation: **OUT** (matches §1.3; corpus filter missed it). Rule + reason.
3. **RT-5 — `ck-7290119043149` (לה פזואלוס butter cookie).** Trace parsed only 1 ingredient → NOVA=2 (looks
   minimally processed) but the real label has hydrogenated fats + artificial flavorings. Is this a genuine
   one-shot data miss → **TRANSPARENCY_NULL / discard** (missing_data_discard_rule), or recoverable? It must
   NOT display as low-NOVA/"minimal processing" on a partial parse. Rule.
4. **RT-7 — grade ceiling.** After any OUT/re-route above, does C remain the honest ceiling, or does the
   routing-ruling's "B achievable for clean digestives" now hold? State the expected ceiling for the FINAL corpus.
5. **RT-8 — peanut cookies (protein ~15g, IN via the §1.3 natural-not-fortified exception).** Keep IN, but the
   copy must DISCLOSE the high-protein/peanut nature honestly (not imply "healthy"). Confirm keep-with-disclosure.

## Output
`02_products/cookies_coffee/methodology/cookies_coffee_redteam_scope_ruling_v1.md` — per-finding ruling +
the FINAL corpus count (61 minus any drops) + expected ceiling. This gates the Data re-score + Content fixes.

## Guards
No engine edits, no fabrication, OFF ban. If you drop products, they move to OUT_OF_SCOPE (don't delete data).
Frozen invariants untouched. Return contract: task=P88, proposed_status=RETURNED, artifact+sha256, the
per-finding rulings, final corpus count, not_done, self_check. Propose RETURNED — do NOT close.
