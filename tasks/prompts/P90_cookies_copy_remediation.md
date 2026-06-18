# P90 — Cookies copy remediation: red-team RT-1/3/7/8 + corpus 58 (route: C1 / Content)

**Task:** TASK-275. **Lane:** C1 Content. Fix the copy for the FINAL 58-product corpus (run_cookies_004).
Targeted edits only — the other 56 per-product verdicts were already corrected (P82) and carry verbatim.

## Edit `02_products/cookies_coffee/cookies_coffee_copy_v1.json`
1. **Align to 58:** REMOVE the entries for the 3 dropped products (now OUT_OF_SCOPE): `7290106656727`
   (חיוכים), `7290119043149` (truncated butter), `80083764` (oat). 58 product entries remain.
2. **RT-1 — fix the false prologue claim** (currently "...לכל אחד מהם...שחצות לפחות אחד מסף התווית האדומה" —
   FALSE: 6 products cross neither). Use the VERIFIED counts for the 58: **24 חוצים את שני הספים, 28 חוצים סף
   אחד, 6 אינם חוצים אף סף**; **7 הגיעו ל-C**. Rewrite the prologue + caveat so every number is accurate and
   no "each/all" overclaim remains. Update "61 מוצרים" → "58 מוצרים" everywhere.
3. **RT-3 — sugar threshold is 17.5g, not 17g.** Anywhere the shell says "מעל 17 גרם" use 17.5g (or "שבע
   עשרה וחצי גרם"). Sat-fat threshold = "מעל 5 גרם".
4. **RT-7 — the C-ceiling claim is now CONFIRMED accurate** (run_004 max = 63.1/C, nothing reached B). Keep
   "ציון C הוא תקרת הקטגוריה" — it is true. Do not over-state it as a permanent law (it's this shelf's result).
5. **RT-8 — peanut disclosure** on the 2 peanut verdicts (`7290013453631`, `7290123330488`, both E, protein
   ~15g): state honestly that the protein comes from peanuts (natural, not fortification) AND that the high
   protein does NOT make them a healthier choice — they score E because sugar+saturated-fat dominate. Don't
   imply "healthy".

## Guards
- Touch ONLY the prologue/methodology/caveat (pageShell) + the 2 peanut verdicts + the 3 removals. Leave the
  other 56 verdicts unchanged. Ground every number in run_cookies_004. No fabrication. OFF ban. Brand in
  titles. ≤1 em-dash/sentence. No internal tokens. Re-run hebrew_readability on changed strings.
- Do NOT change scores/grades.

## Return
Return contract: task=P90, proposed_status=RETURNED, artifact (copy_v1.json +sha256), counts (entries=58,
prologue counts corrected, 17→17.5 fixes, C-ceiling kept-as-true, peanut disclosures=2, 3 entries removed,
readability clean), not_done, self_check. Propose RETURNED — do NOT close. Orchestrator verifies counts vs
run_004 + re-merges into the JSON + syncs page-data.ts shell.
