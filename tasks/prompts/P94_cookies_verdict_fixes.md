# P94 — Cookies: 3 verdict factual fixes (C3 #2) (route: C1 / Content)

**Task:** TASK-275. **Lane:** C1 Content. Fix 3 factually-wrong rowVerdicts caught by C3 review #2
(orchestrator-verified true against run_cookies_004). Edit `02_products/cookies_coffee/cookies_coffee_copy_v1.json`.
Ground numbers in the trace/ingredients; touch ONLY these 3 entries.

1. **`7290119041350` (עוגיות קוואקר ללת"ס — VOILA).** Current verdict: "...הסרת תוספת הסוכר לא שינתה את הרכב".
   DATA: sugar = **23.2g**, ingredients include `סוכר` + `אבקת סוכר`. The "ללא תוספת סוכר"/"sugar-free" premise
   is contradicted by the data. Rewrite: do NOT validate sugar removal — state the scanned nutrition still
   shows high sugar (23 גרם) + high sat-fat, i.e. the "no-added-sugar" name conflicts with the label data.
2. **`7290017962108` (עוגיות וניל פקאן — דני וגלית).** Current verdict: "הפקאן הוא מקור שומן בלתי רווי".
   DATA: ingredients = שקדים (almonds), קמח אורז מלא, סוכר קנים, רסק תפוחים, שמן קנולה… — **NO pecan (פקאן)**.
   Remove the pecan causal claim (fabrication — the name says pecan, the parsed ingredients don't). Keep:
   high total fat, sat-fat below threshold (~4g), sugar 17.7g crosses the threshold. Real fat sources =
   almonds + canola.
3. **`7290119040803` (עוגיות קינמון מסוכרות — לה פזואלוס).** Current verdict: "...וסוכר של 23 גרם".
   DATA: sugar = **20.0g**, not 23. Change to "20 גרם" (or "כ-20 גרם"). Sat-fat (9.5g) + sugar both cross —
   that part is fine.

## Guards
Touch ONLY these 3 rowVerdicts/insightLines. No fabrication, ground in run_004. OFF ban. Brand in titles.
≤1 em-dash/sentence. No internal tokens. Re-run hebrew_readability on the 3 changed strings. No score changes.

## Return
Return contract: task=P94, proposed_status=RETURNED, artifact (copy_v1.json +sha256), counts (verdicts fixed=3,
per-product before/after fragment, readability clean), not_done, self_check. Propose RETURNED — do NOT close.
Orchestrator verifies the 3 fixes vs data + re-merges.
