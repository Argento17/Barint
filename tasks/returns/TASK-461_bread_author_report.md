# TASK-461 Phase-2 #7 — BREAD copy overhaul: author report

**Author lane:** Content Agent (C1 native, this session). **Status proposed:** RETURNED (DRAFT until Adversarial QA).
**Artifact:** `bread_copy_overhaul.json` (scratchpad), sha256 `67cddb3c81b0b6f7e80d3c40ff06049e6b8fda23b55fb2401d0dbbd2cd07a56c`
**Target file:** `bari-web/src/data/comparisons/bread_frontend_v4.json`

## 1. Isolation proof (zero git writes)

- Baseline obtained read-only: `git show origin/master:bari-web/src/data/comparisons/bread_frontend_v4.json` → scratchpad `bread_origin.json`.
- Blob sha (git ls-tree origin/master): **`b2fb0fd484503ea89b0241acfee32a1843579e37`**; baseline sha256 `0d2516b287b7b2b09fb89060bb34d0403d8dda1e542e8f551f3a27dc051ae508` (86,241 bytes).
- Nothing under `C:\Bari` touched; all work in scratchpad (`survey*.py`, `build_copy.py`, `verify_copy.py`, artifact, this report). Git ops used: `ls-tree`, `show` only.
- **Field isolation (script `verify_copy.py` §1):** `_meta` identical; changed-field census = `{insightLine: 23, rowVerdict: 23}`; non-copy-field changes: **NONE (23/23 clean)**; key-sets identical per product (rowVerdict key coverage was 23/23 in production — no keys added, hummus lesson applied).
- **Byte preservation:** source serialization exactly reproduced (`json.dumps(..., ensure_ascii=False, indent=2)`, no trailing newline, roundtrip byte-equal), so the output differs from origin only inside the two copy strings.

## 2. Metrics (all script-derived, `verify_copy.py`)

| Metric | Old (origin/master) | New |
|---|---|---|
| em/en dashes in copy fields | 47 | **0** |
| Trailing "ציון X." grade-recitation line on rowVerdict | 23/23 | **0** (grade renders on the card) |
| Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/ציון/נקודות…) | present (ציון ×23) | **0** |
| Opening 3-word duplicates, insightLine | 10/23 stamped (43.5%: "100% קמח חיטה" ×3, "קמח חיטה לבן" ×3, ×2 ×2) | **0 (23/23 unique)** |
| Opening 3-word duplicates, rowVerdict | 20/23 stamped ("קלוריות בינוניות, חלבון" ×12, +3 +3 +2 variants) | **0 (23/23 unique)** |
| Cross-field opening uniqueness | — | **46/46 unique** |
| 5-gram census (R3, no editorial phrase >2×) | — | **max repetition = 1; zero 5-grams above 1** |
| Panel grams/mg carriers (budget ≤4/23) | ~20/23 recite panel numbers | **4/23** (r1, r7, r8, r20 — each a verified shelf extreme) |
| Purchase-verb drift (R4) | — | **0** |
| "X ולא Y" antithesis patterns | present | **0** |

## 3. Rank-check table (superlatives — 63/63 PASS, script-derived)

Panel-number carriers and headline superlatives; full 63-check list in `verify_copy.py` output.

| Claim in copy | Verification | Result |
|---|---|---|
| r1 שיא חלבון (27.5 גרם), שיא סיבים, נתרן נמוך מכולם | max protein/fiber, min sodium over 23 | PASS |
| r1 "פחות ממחצית הנתרן של כל לחם אחר" | 126×2 = 252 < 288 (next lowest) | PASS |
| r7 "500 מ"ג נתרן, הגבוה במדף כולו" | shelf max (next: 434) | PASS |
| r7 "החלבון הנמוך בקטגוריה" | 5.2 = shelf min | PASS |
| r8 "יותר מ-14 גרם סיבים, השיא של לחמי החיטה והשיפון" | 14.2 = max among grain-flour breads (r1 seed-flour 18.5 and r17 gluten/flax 17.4 excluded; both are non-grain-flour constructions, stated as such in their own copy) | PASS |
| r20 "נעצרת מתחת ל-4 גרם סיבים" | 3.9 | PASS |
| r15 "הסיבים הנמוכים ביותר שנמדדו בקטגוריה" | 2.9 = min of reported; hedged with "שנמדדו" because r23 fiber is null | PASS |
| r16 "ארבע חמישיות מהקמח שיפון מלא" | parse: "80% ממשקל הקמחים" | PASS (truth fix, §5) |
| r18 "מהקלוריות הגבוהות במדף" | 266 = max, but 266/263/259 cluster → soft form, no superlative | PASS |
| r22 "ערכת המתחלבים הגדולה במדף: שלושה" | 3 emulsifiers (E481+E472e+E471) = shelf max | PASS |
| r23 "הנתרן מטפס כמעט לראש הקטגוריה" | 434 = 2nd of 23 | PASS |
| Ties presented as ties | r3–r4 (0.4), r4–r5 (1.1), r8/r9/r10 (0.1/0.0), r16–r17 (0.1), r18/r19/r20 (exact 69.0), r21→trio (1.0) — all narrated as shared standings, differentiated by composition only | PASS |

## 4. Family map (rule once, differentiate by real deltas)

- **אחיד pair (r11 kal 82.0/A ↔ r14 75.2/B):** same dark-flour base; r11 adds whole wheat + whole rye + fiber (10.4g vs 3.0g). Ruled in r11's RV ("שיעור בקריאת רשימות"), mirrored in r14; gap 6.8 = real, narrated as real.
- **Pita pair (r13 79.2 ↔ r15 75.0):** same white-pita archetype; real deltas only: sugar position in list (3rd vs 2nd), cysteine vs emulsifier; 4.2 gap = real.
- **Sourdough construction twins (r4 89.3 ↔ r5 88.2):** identical rye-sourdough sub-recipe (whole rye flour + water); 1.1 apart → narrated as one tier ("במרחק שאין טעם להכריע לפיו"); differentiated by flour mix (90% whole vs 40% white).
- **The 83-knot (r8 83.1 / r9 83.0 / r10 83.0):** narrated once as a trio of near-identical standings; each block claims only its own composition edge (r8 fiber+low sodium; r9 protein; r10 all-whole+inulin, powder sourdough).
- **The 69.0 trio (r18 / r19 / r20):** exact score tie, three unrelated products; each RV names the tie and its own distinct reason (indulgence bake / salty spelt sourdough / honest half-whole).

## 5. Live truth defect found and fixed (r16, לחם מחמצת שיפון+אגוזים)

Production insightLine + rowVerdict claim **"קמח לבן הוא הרכיב הדומיננטי" / "ארבעים אחוז קמח חיטה לבן הוא הרכיב הגדול"**. The parsed label in the same artifact says: `קמח שיפון מלא (36% ממשקל הלחם, 80% ממשקל הקמחים)` — whole rye is the dominant flour by a wide margin; white wheat is the ~20% remainder. The "40%" figure appears nowhere in the parse. New copy is written to the parse (four-fifths whole rye; the catch = sugar, soy oil, improver kit, 2% sourdough, top-3 kcal). `expansion.comparisonContext` carries the same stale "קמח חיטה לבן (40%)" claim — **outside the 2-field scope**, routed as a sibling/expansion-pass note (same pattern as choctab M3).

## 6. Before/after ×4 (incl. the worst template stamp)

**(a) r14 לחם אחיד פרוס — the worst stamp specimen.** The old RV opening "קלוריות בינוניות, חלבון" is shared verbatim by **12 of 23 products**; r14 also opens its IL with "קמח חיטה כהה" like r11.
- OLD RV: "קלוריות בינוניות, חלבון וסיבים נמוכים. קמח חיטה כהה כרכיב יחיד, ללא קמח מלא בכלל. שני מייצבים. הציון מושפע מהיעדר דגן מלא.\nציון B."
- NEW RV: "הגרסה הבסיסית של לחם האחיד, במרחק גדול מהגרסה ה'קל' המשודרגת. שם הוסיפו קמחים מלאים וסיבים; כאן הבסיס הכהה נשאר לבד, והסיבים נמוכים כמו בפיתה לבנה. אחד המתחלבים ברשימה עודנו שנוי במחלוקת."

**(b) r16 — truth fix.**
- OLD IL: "שיפון מלא עם מחמצת שיפון (2%) ואגוזי מלך (3%) — שילוב מעניין; אבל קמח לבן הוא הרכיב הדומיננטי." (false vs parse)
- NEW IL: "ארבע חמישיות מהקמח כאן הן שיפון מלא, ובכל זאת זו כיכר של החצי התחתון: סוכר, שמן סויה וערכת משפרי אפייה שלמה מלווים אותה."

**(c) r1 לחם טחינה (shelf top, S).**
- OLD IL: "חלבון וסיבים ברמות שנדירות במדף הלחמים — הטחינה וקמחי הזרעים (פשתן, שומשום, אפונה, שקדים) בונים כאן פרופיל שלא קיים בשאר הקטגוריה."
- NEW IL: "טחינה וקמחי זרעים במקום קמח חיטה בונים כאן את הפרופיל החזק בקטגוריה: שיא החלבון, שיא הסיבים, והנתרן הנמוך מכולם."

**(d) r20 אנג'ל חצי מלא (name-honesty story).**
- OLD RV: "קלוריות בינוניות, חלבון סביר, סיבים נמוכים יחסית. חמישים אחוז קמח חיטה מלא וחמישים אחוז קמח לבן — השם מממש בדיוק. שלושה חומרי עזר ותוספת סיבים ישירה ברכיבים.\nציון B."
- NEW RV: "חמישים חמישים בין מלא ללבן, כהצהרת האריזה, והתוצאה נעצרת מתחת ל-4 גרם סיבים גם אחרי תוספת סיבים ייעודית. רביעיית חומרי עזר משלימה תמונה של לחם תעשייתי מסודר. ההבטחה מתקיימת במדויק; היא פשוט הבטחה צנועה."
(Note: the OLD line said "שלושה חומרי עזר"; d4 lists four — E282, E202, E481, E300. New copy says רביעייה, script-checked.)

Additional soft truth fixes baked in: r2 old "רשימה שאפשר לספור על יד אחת" (parse has 12 entries) dropped; r7 old "חמישה רכיבים" followed by a six-item list replaced with a count-free formulation; r21 old IL "ארבעים אחוז חיטה מלאה" (parse: 28% of loaf weight / 76% of flours) replaced with the flour-fraction truth.

## 7. Data flags (routed to Data lane, no copy leans on them)

1. **fat = 0.25 identical across 16/23 products** — looks imputed/floored; flagrantly implausible for r1 (tahini-based) and r22 (25.4% seeds). No fat claim anywhere in new copy.
2. **r11 d4_additives under-extraction:** parse contains "חומרים משמרים: קלציום פרופינט ופוסטיום סורבט" (typos) but d4 lists only E481/E330/E300. Copy references preservatives from the ingredients field, not d4 counts.
3. **r16 expansion.comparisonContext contradicts expansion.ingredients** (white 40% vs whole-rye 80% of flours) — stale copy surface outside scope, needs the expansion pass.
4. **r23 ingredients field carries retail-site disclaimer text** ("אין להסתמך על הפירוט המופיע באתר…") — parse tail pollution.
5. Minor parse corruption tokens: r1 "חומ ר משמר"/"אגומות", r6 "n0מכיל", r2 ".n מאפיינים" — cosmetic, none load-bearing.

## 8. House rules compliance

- **R1 provenance adjectives:** none used (no origin claims; מסטמכר named as brand only).
- **R2 partial-scan narration:** 22/23 products are `partial/low_extraction`; confidence chip discloses; copy narrates confidence nowhere (consistent within category).
- **R3 5-gram self-census:** max repetition 1 (§2).
- **R4 purchase verbs:** 0; who-it-suits framings are descriptive only.
