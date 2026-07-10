# TASK-461 Phase-2 #3 — Chocolate Tablets copy overhaul (author report)

**Lane:** Content Agent (this chat, no subagents spawned). **Status: DRAFT until Adversarial QA.**
**Scope:** `bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json`, insightLine + rowVerdict only, 35/35 products.

## 1. Isolation proof (zero git writes)

| item | value |
|---|---|
| Baseline source | `git show origin/master:bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json` (read-only) |
| Baseline blob sha (git ls-tree) | `45c962fe990ca21be87320b3f65cbc4982803869` |
| Baseline sha256 | `34191fe5aace025c90002e2a89fbf84f5c342aba948646b4f393073bc8d7214f` |
| Final artifact | scratchpad `choctab_copy_overhaul.json` |
| Final sha256 | `e7cd57b6f2e28ef8d3d2b81398c30c437e8009a23a14f0ee08ca87c6f6efddfd` |
| Serialization | `json.dumps(..., ensure_ascii=False, indent=2)`, no trailing newline — proven byte-identical on origin roundtrip |
| Field isolation | **35/35 products changed in exactly {insightLine, rowVerdict}**; `_meta`, score, grade, rank, nutrition, d4_additives, expansion, `_hash_no_rank` all identical (JSON-level per-key diff, `choctab_apply_audit.py`) |
| Git | `git status --porcelain` on target file: empty; HEAD unchanged (`1f90d8c1`); no add/commit/branch/stash/checkout run |

## 2. Metrics (script-derived, `choctab_audit.txt`)

| metric | OLD (origin/master) | NEW |
|---|---|---|
| em/en dashes (both fields, 35 products) | **80** | **0** |
| banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | ≥1 (e.g. ct-036 "פרמטרים") | **0** |
| products carrying panel grams/mg | 7/35 | **4/35**, each a verified shelf extreme: ct-002 (25 גרם fiber, shelf-max), ct-008 (0.2 גרם sugar, shelf-min), ct-031 (65 גרם sugar, shelf-max), ct-032 (357 מ"ג sodium, shelf-max) |
| opening uniqueness (first 3 words) | not enforced | **insightLine 35/35 unique; rowVerdict 35/35 unique** |
| health-halo terms (בריא/בריאות/מזין) | 0 | **0** |
| insightLine words | — | min 10 / max 15 / median 13 / mean 13.3 / stdev 1.1 |
| rowVerdict words | — | min 28 / max 47 / median 37 / mean 37.5 / stdev 4.6 |

Shelf distribution (unchanged, fresh TASK-455 scores): grades B:2 C:6 D:10 E:17; scores min 12.8 / max 65.8 / median 35.1 / stdev 14.60.

## 3. Framing guardrails honored (TASK-455 / EV-REDLABEL-013)

- **No health-halo on dark:** the two B tablets are framed as the shelf's least-problematic indulgence, explicitly still candy: ct-002 "ראש הדירוג הזה מסמן את הפינוק המחושב ביותר, וזה כל מה שהוא מסמן"; ct-001 "גם היא פינוק להנאה מדודה, ושום דבר מעבר". Zero "בריא" anywhere.
- **#1/#2 sole-leader hedge preserved:** gap is 0.7 pts (sub-2 = tie). Both framed as co-leaders ("אחת משתי הטבלות שחולקות את ראש הדירוג" / "השותפה השנייה בצמרת"); neither claims sole leadership.
- **Indulgence stance (cookies precedent):** copy helps pick a better tablet; E-grade milk/filled/white products ruled factually and proportionately, no moralizing (e.g. ct-031 "מי שאוהב לבן אוהב בדיוק את זה").

## 4. Superlative rank-check table (all vs full 35, from artifact `nutrition_per_100g`)

| claim in copy | product | check (top of ranking) | verdict |
|---|---|---|---|
| "הסוכר הנמוך במדף כולו" 0.2g | ct-008 | 0.2 < ct-034 0.3 < ct-038 0.7 | TRUE |
| "הטבלה המתוקה ביותר במדף" 65g | ct-031 | 65 > 60 (ct-030, ct-032) | TRUE |
| "מהטבלות המתוקות במדף כולו" | ct-030 | 60 = tied 2nd | TRUE |
| "שיא המדף ובפער עצום" נתרן 357mg | ct-032 | 357 vs next 215 | TRUE |
| "הנתרן... המקום השני בקטגוריה" | ct-025 | 215 = 2nd | TRUE |
| "שורת הנתרן, מהגבוהות במדף" | ct-024 | 124 = 3rd | TRUE |
| "שורת הסיבים עד 25 גרם, הגבוה במדף" | ct-002 | 25 > ct-016 22 (11 products undeclared — claim is over declared values, consistent with shelf convention) | TRUE |
| "עשירת החלבון של המדף" | ct-012 | 12.5 > ct-001 11.0 (all 35 declared) | TRUE |
| "הטבלה השמנה ביותר במדף" | ct-003 | fat 55 > ct-001 53 | TRUE |
| "מהטבלות השמנות והצפופות במדף" | ct-001 | fat 2nd (53), kcal 2nd (607) | TRUE |
| "השומן הרווי הנמוך במדף/בקטגוריה" | ct-019 | 11 < ct-018 13 | TRUE |
| "צפוף קלורית יותר מה-90% של אותו בית" + "מהצפופות קלורית במדף" | ct-017 | 610 kcal = shelf max; Lindt 90% = 592 | TRUE |
| "היחידה במדף שממתיקה בסוכר דמררה" | ct-012 | "דמררה" in 1/35 ingredient lists | TRUE |
| "שלושה ממתיקים" + "יותר תוספי מזון מכל מריר אחר במדף" | ct-016 | 3 distinct sweeteners (erythritol/maltitol/sucralose); d4=3 vs next dark d4=2 | TRUE |
| "הרשימה הארוכה במדף כולו" | ct-010 | 14 top-level ingredient items vs next 12 (ct-026) | TRUE |
| "אבקת שומן קוקוס... שכמעט לא רואים בקטגוריה" | ct-026 | "קוקוס" in 1/35 lists | TRUE |
| "סוגרת את הדירוג" / "המקום האחרון בדירוג" | ct-033 | rank 35, gap to 34th = 2.3 pts (>2, not a tie) | TRUE |
| ingredient-order claims (סוכר ראשון: ct-018/020/023/024/028/029/030/033; ממתיק ראשון: ct-008/011/022) | — | each verified against `expansion.ingredients` string order | TRUE |

Component percentages used (label-derived, not panel): cocoa % (many), מרציפן 44%, שקדים 38%-of-marzipan context, אגוזי לוז 34%/16%/8%-implied ("מעטים"), פיסטוק 10% ("עשירית"), נוגט 56% ("יותר ממחצית"), דבש 3% (no number used), קקאו 28% ("מתחת לשלושים אחוז"), 47% ("מתחת לחצי").

## 5. Family map (ruled once, differentiated by real deltas)

| family | members (rank) | ruling | differentiators used |
|---|---|---|---|
| טרו no-added-sugar | ct-002 (1), ct-010 (9) | engineering route: sweeteners+inulin replace sugar | dark co-leader vs milk version with the shelf's longest ingredient list |
| ARENSTO darks | ct-001 (2), ct-015 (8), ct-039 (16) | one clean short formula, a cocoa ladder | 90/81/75: sugar's role grows as cocoa falls; ct-001 carries the concentration story |
| טוסו no-added-sugar | ct-034 (4), ct-008 (5), ct-011 (10) | maltitol route | ct-034 = single sweetener + cocoa-first list; ct-008/ct-011 = maltitol ahead of cocoa (real list-order delta inside the family) |
| לינדט dark ladder | ct-003 (7), ct-012 (13), ct-007 (6), ct-017 (19), ct-035 (21) | each rung has its own mechanism | 90% = 3 cocoa forms, fattest; 85% = demerara + protein max; 78% = milk-fat trick; 70% mild = sweetened gateway, kcal max; 70% classic = the honest benchmark |
| לינדט flavored | ct-023 (25), ct-024 (26), ct-018 (18), ct-020 (20) | sweet base wearing a 'מריר' label | mint/salt = literal twins (only delta: sea salt → sodium); hazelnut = nuts are the asset; pistachio = caramelized sugar-on-sugar |
| צ'וקטה | ct-009 (11), ct-036 (22), ct-021 (23) | private-label mirror of the big brands | 85% honest clone; 70% = Lindt-70 twin (brand/price call); 60% = definition floor, PGPR enters |
| טובלרון | ct-027 (29), ct-030 (31) | nougat identity (honey+almonds) in two shells | dark 50% vs milk 28%; milk = double sweetening |
| מילקה | ct-029 (32), ct-031 (33) | milk-candy structure | "extra cocoa" name vs sugar-first list; white = zero cocoa solids + sugar max |
| שוקולד פרה | ct-016 (15), ct-025 (28), ct-028 (30), ct-033 (35) | one brand, four different candies | no-sugar engineering max; biscuit brings oils+sodium 2nd; nuts 16% on sweet base; white closes the ranking |
| singles | ct-038, ct-013, ct-014, ct-019, ct-022, ct-026, ct-032 | each ruled on its own fired driver | — |

## 6. Before/after ×5

**ct-002 (rank 1, B) insightLine**
- OLD: `52% קקאו ללא תוספת סוכר, עם 2.1 גרם סוכר בלבד ל-100 גרם — מהמובילים במדף הזה.`
- NEW: `צמרת המדף נלקחת כאן בהנדסה: אריתריטול, סטיביה וסיבי אינולין תופסים את המקום של הסוכר.`
- (kills em dash + panel recitation; opinion up front; engineering finding leads)

**ct-016 (rank 15, D) rowVerdict**
- OLD: `55% קקאו עם שלושה ממתיקים (אריתריתול, מלטיטול, סוכרלוז) ושני מתחלבים (לציטין ו-PGPR): נוסחה מורכבת שמשקפת מאמץ להגיע לטעם ספציפי. הסיבים הגבוהים מגיעים מסיבי תירס ואינולין, לא מהקקאו. תקין מבחינת סוכר; מוטל בספק מבחינת נוסחה.`
- NEW: `שוקולד פרה פותרת את משוואת האפס-סוכר בכוח: אריתריטול, מלטיטול וסוכרלוז יחד, PGPR לצד הלציטין, ואינולין וסיבי תירס שממלאים את שורת הסיבים. התוצאה באמת דלת סוכר, והמחיר הוא יותר תוספי מזון מכל מריר אחר במדף. מי שסופר רכיבים כמו שהוא סופר סוכר ידפדף הלאה.`
- (drops "לא מהקקאו" antithesis; superlative now script-verified vs all darks)

**ct-017 (rank 19, E) insightLine**
- OLD: `לינדט 70% 'מילד' — הגרסה שנועדה להיות נגישה, והסוכר כאן מאשר בדיוק את זה.`
- NEW: `ה'מילד' מרכך את המרירות בעזרת סוכר, ויוצא צפוף קלורית יותר מה-90% של אותו בית.`
- (new verified insight: the mild 70% is the shelf's most caloric tablet, denser than the 90%)

**ct-036 (rank 22, E) rowVerdict**
- OLD: `הנוסחה דומה ללינדט 70%: ... בכל שאר הפרמטרים מדובר בהפרש של מחיר ומותג.`
- NEW: `מי שמשווה אותה ללינדט 70% ימצא הבדלים קטנים מכדי להכריע: אותה קבוצת רכיבים, מתיקות דומה, אותה שורה תחתונה של ממתק קקאו. הבחירה כאן היא עניין של מותג, מחיר וזמינות, והמדף מרוויח מזה שיש לקלאסיקה תחרות.`
- (kills the "פרמטרים" engine-vocab leak — the one live Tier-4 leak on this page; drops the unfounded fiber-vs-undeclared comparison the old copy implied)

**ct-020 (rank 20, E) rowVerdict**
- OLD: `כשהמרכיב הראשון הוא סוכר, הפיסטוק הוא המילוי והשוקולד הוא הציפוי. הפיסטוקים אמיתיים ומקורמלים. ה'אקסלנס' מתייחס לחוויה — ציון E אומר את שאר הסיפור.`
- NEW: `עשירית מהטבלה פיסטוק, וסביבו מנגנון של ממתק: סוכר בראש הרשימה, קרמול על האגוז, שומן חלב לרכות. החוויה מפנקת באמת; ה'אקסלנס' שעל האריזה מתאר את הטעם, והלוח מתאר ממתק.`
- (em dash gone; grade-letter crutch replaced with the mechanism)

## 7. Flags for other lanes (NOT touched by this pass — outside the two-field scope)

1. **STALE EXPANSION COPY vs fresh grades (Content follow-up, this page):** `expansion.comparisonContext` of ct-002 and ct-001 still says "וגם הוא רק C" / "עדיין C" while both products are now grade **B** (post TASK-455 flips). Same stale-C language pattern appears in several C/D-band expansion blocks. insightLine/rowVerdict are now consistent with fresh grades; the expansion layer needs its own pass.
2. **Corrupted ingredient parses (Data lane):** ct-001 "רבקת קקאו שמן" (garbled token), ct-016 "ממתי קים", ct-002 nested-paren corruption "סטיביה (ממתיקים(אריתריתול...". Copy avoids leaning on any corrupted token (no ingredient-count claims where the parse is garbled).
3. **ct-019 sodium = 0.0** on a marzipan product — plausible but worth a Data-lane eyeball (label may say "<5mg").

## 8. Deliverables

- `choctab_copy_overhaul.json` (scratchpad) — final artifact, sha256 `e7cd57b6f2e28ef8d3d2b81398c30c437e8009a23a14f0ee08ca87c6f6efddfd`
- `choctab_copy.py` — the 70 authored strings (source of truth for the apply)
- `choctab_apply_audit.py` + `choctab_audit.txt` — apply + full audit output
- `choctab_final_readout.txt` — human-readable all-35 readout for QA
- this report


## 9. Post-QA fix pass (GO_WITH_FIXES, 2 surgical fixes — this section appended after Adversarial QA)

Pre-fix artifact preserved: `choctab_overhaul_v1_preQA.json`, sha256 `e7cd57b6f2e28ef8d3d2b81398c30c437e8009a23a14f0ee08ca87c6f6efddfd`.

**Fix 1 — ct-024 (QA MEDIUM: literal-identity over-claim vs ct-023).** Panel rows differ ±1 on satFat/carbs/sugar/fiber/protein; only sodium is material (13 → 124 mg). Twin insight kept, wording now literally true; score comparison stays tie-framed (gap 0.4).
- IL OLD: `תאומה מלאה של גרסת המנטה, עד שקמצוץ מלח הים מחליף את השמן ומעלה את הנתרן.`
- IL NEW: `האחות המלוחה של גרסת המנטה: אותו ממתק כמעט שורה בשורה, ורק הנתרן באמת זז.`
- RV OLD: `ההבדל היחיד מהמנטה הוא מלח ים בשיעור זעיר, וההשלכה היחידה שלו יושבת בשורת הנתרן, מהגבוהות במדף בגלל התוספת הזו. כל השאר זהה: סוכר ראשון, קקאו מתחת לחצי, ביצוע מוקפד של ממתק. הבחירה בין השתיים היא טעם אישי נטו.`
- RV NEW: `ההבדל הממשי היחיד מגרסת המנטה הוא ההחלפה של שמן המנטה בקמצוץ מלח ים, שמזניק את שורת הנתרן אל הגבוהות במדף; בשאר הלוח ההפרשים בין השתיים קטנים מכדי להטריד מישהו. גם כאן הסוכר ראשון והקקאו מתחת לחצי, ביצוע מוקפד של ממתק. הבחירה בין השתיים היא טעם אישי נטו.`

**Fix 2 — ct-030 (QA MEDIUM: buy-verb recommendation drift).** Imperative purchase phrasing removed; iconic-candy framing kept.
- RV OLD (ending): `...זהו ממתק איקוני עם צורה שאין לאף אחד אחר, וכדאי לקנות אותו בתור בדיוק זה.`
- RV NEW (ending): `...זהו ממתק איקוני עם צורה שאין לאף אחד אחר, וההגדרה הזו אומרת עליו הכל.`

**Verification after fixes (`choctab_apply_audit.py` re-run + census):**
- Surgical-diff vs preQA: changed = ct-024 {insightLine, rowVerdict}, ct-030 {rowVerdict}; **0 other products, 0 other fields**.
- Isolation vs origin/master: 35/35 clean; score/grade/rank/_hash_no_rank identical.
- Em dashes 0; banned vocab 0; health-halo 0; openings 70/70 unique; panel numbers 4/35 (unchanged set).
- Buy-verb census: 0 hits (כדאי לקנות / קנו / תקנו / שווה לקנות) across 35 products.
- 5-gram census: 1 shared 5-gram — `עיסת קקאו סוכר חמאת קקאו` (ct-013, ct-035): both literal ingredient-list quotes of products whose labels genuinely open with the same three ingredients. Factual recitation, not template drift; left as-is.
- Observation surfaced (no action, out of fix scope): ct-027 contains descriptive `הצורה והטעם הם הסיבה לקנות` and ct-023 `יקבל בדיוק את מה שקנה` — descriptive of buyer intent, not instructions; QA passed both. Flagged for the gate's awareness only.

**Final artifact:** `choctab_copy_overhaul.json`, sha256 `c03cc84fccd91b8ac8d5e7aecfb55eb6dad2c2d3e57568cf7ac91144172d1236`. Fix 3 (stale expansion "רק C") untouched per instruction — expansion layer routed elsewhere.
