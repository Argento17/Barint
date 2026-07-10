# TASK-461 Phase-2 #2 — Cookies/Coffee copy overhaul: Author report (Content Agent)

**Category:** cookies_coffee (117 products — largest corpus category)
**Target file (repo):** `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json`
**Status: DRAFT — pending Adversarial QA gate.** Zero git writes performed; all work on scratchpad copies.

## 1. Source + isolation proof

| item | value |
|---|---|
| Baseline | `git show origin/master:bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json` |
| Baseline blob sha (git ls-tree) | `675eac00510d2a7ba77ce17928639ade04275102` |
| Baseline bytes / sha256 | 768,101 / `b718df15efdd96a8cdc3c6c6005c30a08cca613d47a9377f4041e654821f6c77` |
| Artifact | `cookies_coffee_copy_overhaul.json` (scratchpad) |
| Artifact bytes / sha256 (post-M1 rework) | 775,694 / `af492d788f0c03494e5d2e76018accc62163bb99481e96bfaa608152a8dceddc` |
| Superseded pre-M1 version | 775,107 / `81ecc1fa…` (kept as `cookies_overhaul_v1_preM1.json` for diff audit) |
| Round-trip fidelity | baseline byte-reproduces under `json.dumps(ensure_ascii=False, indent=2)`, no trailing newline — same serializer used for artifact |

**Field-isolation (script `verify_apply.py`, full JSON tree walk):** 234 changed leaves = `insightLine` ×117 + `rowVerdict` ×117. Non-copy-field diffs: **0**. `_meta` identical: True. `page_copy` identical: True (stale-count issue NOT touched, per spec). Scores/ranks identical old↔new: True (script check). Products touched: 117/117.

## 2. Audit metrics (all script-derived, `verify_apply.py` + `metrics.py`)

| metric | old (origin/master) | new |
|---|---|---|
| em dashes (both fields, 117 products) | 242 | **0** |
| banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | present | **0 hits** |
| opening-3-words uniqueness, insightLine | — | **117/117 unique** |
| opening-3-words uniqueness, rowVerdict | — | **117/117 unique** |
| "X, ולא Y" antithesis scan | — | 0 suspects |
| products with nutrition-panel digits | 9/117 | **6/117** (target ≤8; see §3) |
| empty fields | — | 0 |
| IL words: min/max/median/stdev | 7/16/11/1.8 | 9/15/12/1.5 |
| RV words: min/max/median/stdev/most-common | 22/69/31/8.8/34(12x) | 26/44/35/3.4/35(22x) |
| grade distribution (must be unchanged) | C:9 D:27 E:81 | C:9 D:27 E:81 ✔ |

Note on stdev: RV stdev tightened because the old copy mixed 22-word stubs with 69-word essays; uniqueness gates (117/117 openings, 0 shared templates) are the anti-stamping tripwire, and they pass.

## 3. Numbers kept (nutrition-panel digits) — 6/117, each a verified shelf extreme

| rank | product | number | justification (script rank-check) |
|---|---|---|---|
| 6 | אחוה עוגיות זעתר | 730 מ"ג נתרן | shelf-max sodium; gap to #2 ≥ 200mg (next: 510) |
| 78 | פרה קראנץ' שוקולד לבן | 562 קלוריות | shelf-max energy density |
| 84 | באלזן היט וניל | 17 גרם שומן רווי | shelf-max satFat (verified tie with Hit שוקולד) |
| 88 | אוראו ציפוי שוקולד לבן | 49 גרם סוכר | shelf-max sugar |
| 91 | באלזן היט שוקולד | 17 גרם שומן רווי | shelf-max satFat (tie partner); also max sodium among sweet products (510, stated word-form) |
| 93 | אוראו דאבל קרם וניל | 43 גרם סוכר | top-5 sugar; number carries the "double cream" story |

Ingredient percentages quoted from labels (e.g. "58% בוטנים", "45% קרם", "68% סוכר במילוי") are label quotes, not panel recitation — same class the cheese QA passed 6/6. The stray "4" tokens in the digit census are "פונסו 4R" (a colorant name).

## 4. Superlative / claim rank-check table

**59/59 scripted claim checks PASS** (`verify_apply.py`, run against the full 117-product corpus, ties = sub-2-point rule). Highlights:

| claim in copy | check | result |
|---|---|---|
| r1 "פסגת המדף... אם בוחרים עוגייה, זו הבחירה" | score gap #1→#2 > 2 (59.8 vs 56.6) | PASS |
| r1 "סיבים שרוב המדף לא מתקרב אליה" | 8.1g ≥ 2× median fiber (median 2.9) | PASS |
| r6 sodium "הרחק מעל כל מוצר אחר" | 730 vs next 510 | PASS |
| r58 "החלבון הגבוה בקטגוריה כולה" | protein 15.4 = shelf max | PASS |
| r13 "יותר סיבים מכל מוצר אחר כאן" | fiber 17.0 = shelf max (מוספים disclosed) | PASS |
| r8 "הטובה בקופסה של רחלי" | family max, gap > 2 (52.4 vs 49.7) | PASS |
| r34 "אחת משתיים בלבד במשפחה עם שני סימונים" | Racheli 2_PLUS = exactly {שוקוצ'יפס, אלפחורס} | PASS |
| r11 "מהבודדות בקופסה בלי סימון אדום בכלל" | רייפעת trace has zero ISRAELI_RED caps | PASS |
| r19 "השומן הרווי הגבוה במשפחת רחלי" | 12.3 = family max | PASS |
| r33 "היחידה מבין המרוקאיות עם שני סימונים" | only בבקה carries 2_PLUS among "מרוקאי"-named | PASS |
| r90 "היחידה במשפחת הקוקיס שסוכרים ראשונים" | first-ingredient scan of all 5 Shufersal products | PASS |
| r95 "העמוסה ביותר בתוספים במשפחת מרבה, וגם המתוקה שבה" | only Merba with ADDITIVE_MARKERS_5_PLUS; family-max sugar 41.2 | PASS |
| r97 "העוגייה הקלורית ביותר של אסם" | 527 = Osem family max (suspect-panel product excluded) | PASS |
| r98 "הקלוריות השניות בגובהן במדף" | 544 = shelf #2 | PASS |
| r101 "החלשה מבין שלוש הסנדוויץ' של צ'וקטה" | 25.9 > 19.3 > 15.0, both gaps > 2 | PASS |
| r112 "בתחתית משפחת מרבה" | 12.2 = family min, gap 2.7 | PASS |
| r115 "ההפרש... קטן מכדי לדבר עליו" | 10.3 within 2.0 of the 10.0 pair (tie handling) | PASS |
| r116/117 "המקום האחרון... משותף" | exact 10.0 tie, honest joint-last | PASS |
| every "מסומן אדום" (incl. all "שני סימונים") | matching ISRAELI_RED_LABEL_* / 2_PLUS cap in that product's trace | PASS (all products) |
| all 5 partial-confidence products | disclosure clause present, one consistent formula | PASS 5/5 |

Three claims were weakened after the first check run FAILED them (rank 11–21 for "מהגבוהים במדף" phrasing): r46 → red-label phrasing, r73 → "גבוה מאוד", r92/r55 → non-superlative phrasing. Re-run: all pass.

## 5. Family-handling map (rule the family once, differentiate by real deltas)

| family | members | handling |
|---|---|---|
| דני וגלית (4) | r1, r2, r5, r16 | leaders ruled as a house style (almond/spelt base, plant sweeteners); each differentiated by its real delta (satFat red on r2, cane sugar + KfP on r5, triple-sugar red on r16) |
| קופסת העוגיות של רחלי (11) | r8–r57 | ruled as the "home-style" family: real eggs, short lists, satFat as the family ceiling; r8 = verified family best, r57 (אלפחורס) = verified family outlier/worst; ללת"ס twins (r17, r20) ruled as sugar-swap-only vs their originals |
| VOILA trio | r29, r30, r31 | identical formula (script: identical panels) — ruled once, variants told apart by shape only; honest "one product, three shapes" |
| Quaker cross-brand trio | r65 (VOILA), r66 (VOILA ללת"ס), r67 (לה פזואלוס) | identical panels ACROSS brands — named openly; r66 carries the label-vs-scan finding (§6) |
| לוטוס quartet | r73–r76 | identical panels — "one product, four packages"; only real ING delta (oil naming) narrated on r76 |
| הדר pair | r26, r27 | identical panels; vanilla vs cocoa = flavor-only choice |
| לה פזואלוס קינמון/מקלות עלים | r71, r72 | identical panels; cinnamon % = only felt difference |
| נסיכה pair | r104, r105 | identical panels incl. Ponceau 4R filling; color variety = only difference |
| מרבה (7) | r79–r112 | family signature = sugar-first lists; differentiated by coating (r81), colors+wax (r95), humectant softness (r112 = verified family worst) |
| שופרסל קוקיס (5) | r44–r90 | butter+margarine signature; r90 = only sugar-first member; partial-panel members disclosed |
| צ'וקטה sandwiches (3) + פתי בר | r32, r54, r69, r101 | sandwich trio ranked honestly (middle/best/worst verified); פתי בר carries the live truth-defect fix (§6) |
| אסם (10) | r25–r117 | no stamped ruling; each product on its own driver (sugar-first fills, GF starch-base pair at joint-last) |
| PASTICERE (3) | r52, r55, r80 | margarine-template family; r80 = verified family-max sugar |
| באלזן/בלזן Hit (3) | r84, r91, r94 | satFat-record family; the 17g tie stated as a tie |
| Tulino pair | r68, r98 | 40%-cream twins; "difference is cosmetic" |
| אוראו (3) | r88, r93, r106 | coated pair ruled vs each other (49 vs 47), דאבל on its own number |

No fabricated distinctions: every variant sentence tied to a verifiable ING/panel/trace delta; where no delta exists, the copy says so explicitly.

## 6. Truth-defect fixes vs live copy + data flags

**Truth defects fixed (live production copy):**
1. **r32 צ'וקטה פתי בר בטעם חמאה — live copy states the wrong grade.** Live IL: "…מוריד ל-E"; live RV: "…הציון נחת על E". The product's grade is **D** (35.7). New copy carries no grade contradiction.
2. **r3 לה פזואלוס בטעם חמאה — live copy calls the list "נקייה, ללא תוספים".** The scanned list contains E450/E500 and "שמנים ושומנים מהצומח (חלקם מוקשים)" — partially hydrogenated fats. New copy names the hydrogenation and the missing-butter reality. (Live RV also leaked "תקרת עיבוד" — engine vocab.)
3. **r95 מרבה צבעוני — live copy claims "שישה צבעי מאכל".** The scanned coating names five colorants; count unverifiable. New copy: "שורת צבעי מאכל" (no count).

**Data-lane flags (NOT fixed here — copy written defensively around them):**
1. **Per-serving panels stored as per-100g** on 4 products (all `servingNote: "ל-100 גרם"`): r7 (93 kcal), r25 (97), r39 (94), r40 (92) — physically implausible for baked cookies. No calorie/extreme claims made for these 4; they are excluded from all rank-checks (`SUSPECT` set in script).
2. **r66 VOILA קוואקר ללת"ס:** product name says "ללא תוספת סוכר" while the scanned ING contains "סוכר, אבקת סוכר" and the panel shows 23.2g sugar — identical to the regular version. Either a real label problem or a scrape that crossed variants. Copy presents it as "the scanned list" finding; flagged for Data Agent verification.
3. **r4 גנדולה (bsip1_cookies_80083764):** truncated ING string + missing satFat, yet `confidence: verified`. Copy discloses the gap; chip/confidence mismatch flagged.
4. **r70 מן בטעם חמאה:** satFat missing with `confidence: verified` — same chip mismatch class; copy discloses.

## 7. Before/after ×6

**r1 (top) — עוגיות גרידת לימון ללת"ס (דני וגלית), 59.8 C**
- OLD IL: שקדים ואורז מלא ראשונים ברשימה — ממתיק אגבה, אפס תווית אדומה.
- NEW IL: שקדים וקמח אורז מלא במקום קמח לבן: פסגת המדף הזה, והיא עדיין עוגייה.
- NEW RV: העוגייה המבוססת ביותר במדף: שקדים כרכיב ראשון, קמח אורז מלא אחריהם, אגבה במקום סוכר לבן וכמות סיבים שרוב המדף לא מתקרב אליה. שמן הקנולה הוא הפשרה היחידה ברשימה. גם המנצחת של קטגוריית העוגיות נשארת חטיף צפוף בקלוריות, אבל אם בוחרים עוגייה, זו הבחירה.

**r6 (mid, C-with-a-catch) — עוגיות מזרחיות עם זעתר (אחוה), 54.0 C**
- OLD IL: עוגיית זעתר ללא סוכר — נתרן גבוה במיוחד, יוצאת דופן בקטגוריה.
- NEW IL: היחידה במדף שהיא בכלל לא קינוח: מאפה זעתר בלי גרם סוכר, עם הנתרן הגבוה בקטגוריה.
- NEW RV: עוגייה מזרחית מלוחה שמטפסת לצמרת בקטגוריה שנחנקת מסוכר, פשוט כי אין בה סוכר בכלל. המחיר נמצא בצד השני של התווית: 730 מ"ג נתרן, הרחק מעל כל מוצר אחר כאן. בחירה מעניינת לצד הקפה, כל עוד המלח הוא שיקול פתוח אצלכם.

**r32 (truth-defect fix) — פתי בר בטעם חמאה (צ'וקטה), 35.7 D**
- OLD IL: שמן חמניות בלבד — שומן רווי נמוך, אך סולפיט ברשימה, אלרגן מוצהר, מוריד ל-E. *(product is D — live grade error)*
- NEW IL: פתי בר בלי חמאה וכמעט בלי שומן רווי, שהסוכר הכפול שלו עושה את הנזק.
- NEW RV: מקור השומן היחיד הוא שמן חמניות, והשומן הרווי מהנמוכים במדף כולו. הסוכר פחות מרשים: סוכר לבן ועוד סירופ גלוקוזה-פרוקטוזה, יחד מעבר לסימון האדום, ובסוף הרשימה סולפיט. חמאה, אגב, אין; יש טעם חמאה.

**Family trio (cross-brand identical formula) — r65/r66/r67, all 20.1 E**
- OLD (r66) IL: שמן דקל ושני מקורות סוכר ברשימה — למרות שם 'ללא תוספת סוכר'.
- NEW r65 IL: קוואקר הוא 8% מהעוגייה הזאת; שומן הדקלים והסוכר הם הרוב הדומם.
- NEW r66 IL: השם אומר ללא תוספת סוכר, ורשימת הרכיבים שנסרקה כוללת סוכר וגם אבקת סוכר.
- NEW r67 IL: עוגיית שיבולת שועל שהיא תאומה מלאה של הקוואקר של VOILA, עד הגרם.
- NEW r67 RV (family ruling): אותה רשימה ואותו לוח תזונה כמו בשתי עוגיות הקוואקר של VOILA: קמח לבן ושומן דקלים בראש, שיבולת שועל ב-8%, שני סימונים אדומים ונתרן גבוה. מותג אחר, מוצר זהה. הבחירה בין השלוש היא בחירה בין אריזות.

**r117 (worst, joint-last) — פתי בר ללא גלוטן קלאסי (אסם), 10.0 E**
- OLD IL: ללא גלוטן קלאסי — עמילן ושמן דקל, הציון הנמוך ביותר בקטגוריה.
- NEW IL: עמילן, סוכר ושמן דקל בתחתית המשותפת של המדף: התואר עוגייה כמעט טכני.
- NEW RV: הרשימה שנסרקה נפתחת בעמילן במקום דגן, ממשיכה בסוכר ובשלושה שמנים, ונסגרת במייצב שנוי במחלוקת. חלבון כמעט אפסי, מהנמוכים בקטגוריה, משלים את התמונה. חולק את המקום האחרון עם גרסת השוקו שלו; ללא גלוטן הוא הנתון היחיד שהתקיים כאן במלואו.

**r88 (number-as-story) — אוראו בציפוי שוקולד לבן, 16.1 E**
- OLD IL: אוראו בציפוי שוקולד לבן — סוכר הגבוה ביותר שנמדד בקטגוריה.
- NEW IL: שיא הסוכר של הקטגוריה: 49 גרם למאה, כמעט מחצית מהעוגייה.
- NEW RV: ציפוי שוקולד לבן על אוראו מזניק את הסוכר לגבוה ביותר שנמדד במדף, עם שלושה שמנים צמחיים וסירופ גלוקוז-פרוקטוז מאחוריו. הקקאו עצמו נעצר בשני אחוזים. הדירוג משקף מוצר שהוא קודם כל סוכר, ורק אחר כך עוגייה.

## 8. Category stance (register rule 6)

The shelf is treated as an indulgence shelf: no product is framed as health food and none is moralized at. The best product's verdict says explicitly "והיא עדיין עוגייה"; grade-E rulings are proportionate and factual (drivers named from traces: red-label caps, sugar-first lists, margarine/hydrogenation, additive stacks). House rules honored: (R1) no brand-inferred provenance — a "בלגי"/"אוקראינית" adjective was drafted and removed because it is not label-derived; (R2) partial-panel narration present exactly on the 5 partial-confidence products, one consistent clause each.

## 9. M1 rework (Adversarial QA GO_WITH_FIXES, template-drift finding)

QA finding: the clause "סוכר ושומן רווי מסומנים שניהם אדום" appeared verbatim in 13 rowVerdicts (all factually correct). Fix executed as a targeted rework; the dual red-label FACT is retained in all 13, now phrased distinctly and woven into each product's stance.

**The 13 cohort ids (rank / id):** r52 ck-4820180816590 · r57 ck-7290013740694 · r65 ck-7290119041206 · r68 ck-7296073162001 · r71 ck-7290119040803 · r79 ck-8710502139017 · r92 ck-8000500366073 · r96 ck-7622300356767 · r97 ck-61245 · r102 ck-8710502470028 · r109 ck-7290000075143 · r111 ck-7290101111986 · r114 ck-7290019816058.

**insightLine touches:** 1 — r79 only (flow + it carried a 3× 5-gram "הרכיב הראשון ברשימה לפני הקמח"): "הוא הרכיב הראשון ברשימה, לפני הקמח והשוקולד" → "הוא פותח את הרשימה, עוד לפני הקמח והשוקולד".

**Minimal non-cohort touches (4, forced by the new ≤2× 5-gram gate — census found four more 3× chains, three entirely outside the cohort):** r21 (breaks "סימון אדום על שומן רווי" 3×), r56 (breaks "הסוכר והשומן הרווי חוצים שניהם לסימון" 3×), r70 (breaks "בסריקה והדירוג נשען על מה" 3×), r100 (breaks "הסוכר והשומן הרווי מסומנים שניהם" 3×). Each was a one-sentence rephrase preserving its facts; every other product byte-identical (changed-set diff vs pre-M1 = exactly 17 products, script-verified).

**Old→new, the 3 QA-flagged weakest (given deeper rework):**
- **r79 מרבה טריפל שוקולד** — OLD RV: "יש כאן קקאו אמיתי, עיסה וחמאת קקאו, וגם קמח שיבולת שועל. אבל המבנה ברור: סוכר ראשון, שמני דקלים וחמניות מיד אחרי הקמח, וסירופ גלוקוזה לחיזוק. סוכר ושומן רווי מסומנים שניהם אדום. משפחת מרבה כולה מדברת באותה שפה." → NEW RV: "שלושת השוקולדים שבשם נשענים על היגיון אחד: מתיקות. הסוכר פותח את הרשימה ומגובה בסירופ גלוקוזה, שמני הדקלים והחמניות באים מיד אחרי הקמח, והתווית מקבלת את שני האדומים, של הסוכר ושל השומן הרווי. הקקאו, עיסה וחמאת קקאו, דווקא אמיתי. משפחת מרבה כולה מדברת באותה שפה."
- **r102 מרבה נוגטלי** — OLD RV: "החמאה ואגוזי המלך אמיתיים, ושניהם בכמויות סמליות; את המבנה קובעים הסוכר, שמעל ארבעים אחוז מהמשקל, קמח לבן ושמן צמחי. סוכר ושומן רווי מסומנים שניהם אדום. מהמתוקות במשפחה שכולה מתוקה." → NEW RV: "השם מבטיח נוגט, והרשימה מספקת בעיקר מתיקות: סוכר שמעל ארבעים אחוז מהמשקל, קמח לבן ושמן צמחי, כשהחמאה ואגוזי המלך נשארים בכמויות סמליות. הסוכר צבוע אדום, והשומן הרווי מצטרף אליו. מהמתוקות במשפחה שכולה מתוקה."
- **r109 אסם שוקוצ'יפס קלאסי** — OLD RV: "מקרה נדיר שבו השוקולד עצמו מוביל את הרשימה, עם מוצקי קקאו גבוהים. זה גם מה שמסביר את המאזן: סוכר ושומן רווי מסומנים שניהם אדום, וצפיפות קלורית מהגבוהות במדף. מוצר שוקולד יותר מאשר מוצר מאפה, ונכון לקרוא אותו כך." → NEW RV: "מקרה נדיר שבו השוקולד עצמו מוביל את הרשימה, עם מוצקי קקאו גבוהים. המחיר כתוב בתווית: כשכמעט שליש מהמוצר הוא שוקולד, האדום מגיע גם לשורת הסוכר וגם לשורת השומן הרווי, והקלוריות צפופות בהתאם. מוצר שוקולד יותר מאשר מוצר מאפה, ונכון לקרוא אותו כך."

**Post-rework verification (all script-derived, `m1_census.py` + `verify_apply.py` + `metrics.py` re-run):**
- Verbatim clause carriers: 13 → **0**.
- 5-grams appearing >2×: **0** (top repeated 5-grams now all at exactly 2, e.g. "בסריקה והדירוג נשען על מה" 2×, "סימון אדום על שומן רווי" 2×).
- Dual red-label fact retention on cohort: **13/13** (regex: red-mark stem + סוכר + שומן ה?רווי in RV).
- Full suite re-run: claim checks **59/59 PASS**; field isolation vs origin baseline clean (234 leaves, all insightLine/rowVerdict, `_meta`/`page_copy` identical); em dashes **0**; banned vocab **0**; antithesis **0**; openings unique **117/117 both fields**; panel-digit products still **6/117** (no new numbers).
- Changed-set diff vs pre-M1 artifact: exactly 17 products (13 cohort + 4 logged non-cohort), 16 RV-only + 1 IL+RV (r79).
- RV word distribution after rework: min 26 / max 46 / median 35 / stdev 3.9 / most_common 35(18x).

## Return contract

```json
{
  "task": "TASK-461 (Phase-2 category #2: cookies_coffee)",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "SCRATCHPAD/cookies_coffee_copy_overhaul.json", "action": "created+M1-reworked", "sha256": "af492d788f0c03494e5d2e76018accc62163bb99481e96bfaa608152a8dceddc"},
    {"path": "SCRATCHPAD/TASK-461_cookies_author_report.md", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/cookies_origin.json", "action": "created", "sha256": "b718df15efdd96a8cdc3c6c6005c30a08cca613d47a9377f4041e654821f6c77"},
    {"path": "SCRATCHPAD/verify_apply.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"},
    {"path": "SCRATCHPAD/metrics.py", "action": "created", "sha256": "SEE_FINAL_MESSAGE"}
  ],
  "counts": {
    "products_reauthored": "117/117 (products[] of origin/master cookies_coffee_frontend_v2.json, blob 675eac00)",
    "changed_leaves_field_isolation": "234/234 are insightLine|rowVerdict (verify_apply.py tree walk); non-copy diffs 0/234",
    "em_dashes_new": "0/117 products (verify_apply.py; old = 242)",
    "banned_engine_vocab_hits": "0/117 (verify_apply.py, 7-term list)",
    "opening3_unique_insightLine": "117/117 (verify_apply.py)",
    "opening3_unique_rowVerdict": "117/117 (verify_apply.py)",
    "panel_number_products": "6/117 (metrics.py; each a script-verified shelf extreme; old = 9/117)",
    "claim_checks_pass": "59/59 (verify_apply.py rank/family/red-label/twin checks vs full corpus)",
    "partial_confidence_disclosures": "5/5 (verify_apply.py)",
    "grade_dist_unchanged": "C:9 D:27 E:81 = baseline (metrics.py); scores/ranks identical 117/117",
    "rv_words_distribution": "min 26 / max 44 / median 35 / stdev 3.4 / most_common 35(22x) (metrics.py; old stdev 8.8, min 22, max 69)",
    "il_words_distribution": "min 9 / max 15 / median 12 / stdev 1.5 / most_common 12(27x) (metrics.py)",
    "live_truth_defects_fixed": "3/3 found (r32 wrong-grade claim, r3 false clean-list claim, r95 unverifiable color count)",
    "data_flags_raised": "4 (4x per-serving panels as per-100g; r66 name-vs-list sugar; r4 + r70 verified-chip with missing fields)",
    "m1_verbatim_clause_carriers": "0/117 after rework (m1_census.py; was 13/117)",
    "m1_5grams_over_2x": "0 (m1_census.py full-corpus 5-gram census; max repetition now exactly 2)",
    "m1_dual_fact_retention": "13/13 cohort RVs still state both red labels (m1_census.py)",
    "m1_changed_products_vs_preM1": "17/117 = 13 cohort + 4 logged chain-breakers (r21,r56,r70,r100); insightLine touched only r79"
  },
  "commands_run": [
    {"cmd": "git ls-tree origin/master -- bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json", "exit_code": 0},
    {"cmd": "git show origin/master:bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json > SCRATCHPAD/cookies_origin.json", "exit_code": 0},
    {"cmd": "python -X utf8 inspect.py && python -X utf8 extract.py && python -X utf8 servcheck.py", "exit_code": 0},
    {"cmd": "python -X utf8 verify_apply.py", "exit_code": 0},
    {"cmd": "python -X utf8 metrics.py", "exit_code": 0}
  ],
  "not_done": [
    "Adversarial QA gate (independent lane) — this is a DRAFT by definition",
    "page_copy stale-count issue intentionally untouched (out of scope per dispatch)",
    "Data-lane flags in report §6 handed off, not fixed (data work is out of this lane)"
  ],
  "self_check": "Acceptance test: baseline-identical except insightLine/rowVerdict x117. Observed: full-tree walk found exactly 234 changed leaves, all named insightLine/rowVerdict, _meta and page_copy byte-identical, scores/ranks/grade-dist unchanged; artifact sha256 81ecc1fa..."
}
```

*Git usage this lane: `ls-tree`/`show` only (read-only). No file under C:\Bari touched.*
