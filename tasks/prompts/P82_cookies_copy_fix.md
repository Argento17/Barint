# P82 — Cookies copy fix: C3 review #1 findings (route: C1 / Content)

**Task:** TASK-275. **Lane:** C1 Content Agent (Hebrew editorial + factual re-grounding — judgment, only C1
can do this). Fix the copy errors C3 review #1 caught. Scores LOCKED = run_cookies_003.

## Fix in `02_products/cookies_coffee/cookies_coffee_copy_v1.json` (edit in place)
The full C3 finding list is in `tasks/returns/P81_return.md` — read it. The governing rule for the CRITICAL +
most HIGH items:

**GROUND EVERY THRESHOLD CLAIM IN THE PRODUCT'S ACTUAL FIRED RED LABELS** (from its run_cookies_003 trace —
look for `ISRAELI_RED_LABEL_1_SUGAR` and `ISRAELI_RED_LABEL_1_SAT_FAT` in the trace; only state a threshold
"crossed" if that label actually fired):
1. **CRITICAL — false "two thresholds/limiters":** several verdicts claim sugar AND sat-fat both crossed
   when the trace fired ONLY sugar (sat-fat < 5g). Named by C3: Gatenio פתי בר וניל (sat-fat ~3.4g) +
   שוקולד (~3.6g), Osem עוגיות שוקולד זהבה (~3.5g). Correct ALL such verdicts to state only the label that
   actually fired. Check all ~24 verdicts that say "שני הסף"/"שני מגבילים" against their trace.
2. **HIGH — sugar threshold is 17.5g, not 17g:** don't call 17.1–17.3g "crosses the threshold". Products at
   17.3g (e.g. עוגיות השושנים) are BELOW — describe as "near the threshold", not "crossing". Fix the
   methodologyLines + categoryCaveat text that says "מעל 17 גרם" → use 17.5g or "סביב סף התווית".
3. **HIGH — sat-fat crossing is >5g:** a product at exactly 5.0g (e.g. גנדולה אורגני שוקולד) does NOT cross;
   trace red_labels confirms sugar-only. Don't claim sat-fat crossing there.
4. **HIGH — "no additives"/"ללא תוספים" on truncated ingredient lists:** for products whose trace
   ingredient list is incomplete/truncated (e.g. barcodes 7290119041107, 7290119043149 show a cut-off list),
   do NOT claim "ללא תוספים"/"היעדר תוספים". State only what is verified; if the list is partial, say so or
   omit the absence claim. (This is the brined "clean-claim" error — never assert absence from a partial list.)
5. **MED:** (a) agave (אגבה) is added sugar — mention it neutrally as a sweetener, never as a quality/natural
   point; (b) `מעבוד` → `עיבוד` everywhere; (c) `מאותה מותג` → `מאותו מותג`; (d) replace the hollow line
   "הפרטים קובעים כאן" with a concrete product point or remove it.

## Guards
- Keep all CORRECT verdicts unchanged; touch only what C3 flagged + any other verdict whose threshold claim
  doesn't match its trace red_labels. Preserve the honest least-bad / C-ceiling framing.
- No fabrication, no invented numbers, OFF ban. Brand stays in every title. ≤1 em-dash/sentence. No internal
  tokens. Re-run hebrew_readability on changed strings.
- Do NOT change scores/grades (copy only).

## Return
Return contract: task=P82, proposed_status=RETURNED, artifact (copy_v1.json + sha256), counts (verdicts
changed, "two-threshold" claims corrected, 17→17.5 fixes, no-additives claims removed/qualified, MED fixes),
a per-product list of the threshold-claim corrections (barcode + before/after), not_done, self_check.
Propose RETURNED — do NOT close. Orchestrator re-verifies corrected claims vs trace red_labels + re-merges.
