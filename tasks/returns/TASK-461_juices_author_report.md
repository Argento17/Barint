# TASK-461 Phase-2 #6 — JUICES copy overhaul: author report (Content Agent)

**Artifact:** `juices_copy_overhaul.json` (scratchpad)
sha256 `84b030f5b02aac6ead9b3657117b16716f1378878d25dae716f4747eaa6e4b29`
**Status: DRAFT until Adversarial QA sign-off** (two-gate hard rule).

## 1. Isolation proof (zero git writes)

- Baseline = **origin/master** via read-only `git show origin/master:bari-web/src/data/comparisons/juices_frontend_v3.json` → scratchpad `juices_origin.json` (sha256 `1dd4cfda9ff8073e89bdb6b2f90b4a238c55eccfd5de596dba8bcd24813c5bbe`).
- Blob sha recorded via `git ls-tree origin/master`: **`95c42010dd40a3bada829e0e6efcd88c6d802f09`**.
- Nothing under `C:\Bari` touched; all work in scratchpad; git used read-only (`ls-tree`, `show`) only.
- Serialization fidelity proven before editing: `json.dumps(load(origin), ensure_ascii=False, indent=2)` reproduces the origin file **byte-exact** (asserted in `author_juices.py`), so the output is byte-identical everywhere outside the copy fields.
- Flattened-path diff origin→new: **34 changed paths, all matching `products[i].(insightLine|rowVerdict)`; 0 outside the copy surface**. Key-sets identical (no keys added — all 17 products already carry `rowVerdict`, unlike hummus). `score`/`grade`/`rank`/`_hash_no_rank`/`_meta`/`expansion` byte-identical.

## 2. Metrics (script-derived, `verify_juices.py`)

| Metric | Old | New |
|---|---|---|
| Em dashes (both fields, 17 products) | 38 | **0** |
| En dashes | 0 | **0** |
| Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות) | present (audit) | **0** |
| Literal score values in copy | 2 (jc-024 rowVerdict: "(35.4)", "(35.3)") | **0** |
| R4 purchase-verb hits (כדאי/שווה + לקנות/לבחור/לרכוש) | — | **0** |
| Opening uniqueness (first 3 words, all 34 strings) | template-stamped (94.1% recitation per audit) | **34/34 unique** |
| Products with panel grams/mg in copy | ~all (recitation) | **4/17** (budget ≤4) |
| Products with kcal in copy | — | **1/17** (jc-005, justified below) |
| Max 5-gram repetition (R3 census) | — | **2** (nothing >2×) |
| Empty fields | — | **0** |

**Panel-number justifications (4/17 grams + 1 kcal):**
1. **jc-006** 12.6 g — shelf-max stated sugar (verified extreme): the pomegranate honesty story.
2. **jc-017** 11.4 g — the "מיץ חמוציות" carries more sugar per 100ml than a squeezed orange, most of it added (label-vs-reality; artifact limitingFactors: "רוב הסוכר הוא מהסוכר הלבן המוסף").
3. **jc-019** 1.2 g — shelf-min stated sugar (verified extreme), and the point is it's sweetener work.
4. **jc-026** 9.5 g — the composition contrast that IS the story: under 10% fruit yet among the sweetest of the sweetened drinks, from white sugar.
5. **jc-005** "54 הקלוריות" (kcal, not grams) — sugar is missing from its label; per the artifact itself the score basis is the disclosed kcal, so the kcal is the honest anchor (R2).

**5-gram census detail:** only two 5-grams appear exactly 2× — both inside the deliberate R2 partial-panel clause "נתון הסוכר לא הופיע על האריזה" used consistently on the two products whose labels omit sugar (jc-005, jc-011). Everything else ≤1.

**R2 (partial-panel) policy applied:** all 17 products are `confidence: partial` and the chip already discloses; copy narrates missing data **only where material** — the two products with no sugar value at all (jc-005, jc-011), with one consistent clause.

## 3. Superlative rank-check table (16/16 PASS, script vs full 17-product corpus)

| Claim in copy | Check | Result |
|---|---|---|
| jc-006 "המתיקות הטבעית הגבוהה ביותר שנמדדה" | max stated sugar 12.6; next 11.4 | PASS |
| jc-006 "עובר כל תפוז סחוט" | 12.6 > 8.2/8.6/8.7 | PASS |
| jc-019 "הנמוך בסקירה" (sugar) | min stated 1.2 (missing-label products are 100% juice at 44–54 kcal, physically higher) | PASS |
| jc-019 "מדורגת מתחת לגרסה הרגילה" | 39.9 vs 49.1, gap 9.2 ≥ 2 | PASS |
| jc-017 "מוביל את כל המשקאות הממותקים… בפער ניכר" | top non-A; gap to next = 9.2 ≥ 2 | PASS |
| jc-018 "נגיעת הפרי הקטנה ביותר בסקירה כולה" (2%) | min fruit share; next lowest 9.1% | PASS |
| jc-023 "רשימת התוספים הארוכה ביותר בסקירה" | d4_additives 8; sole max (next 5) | PASS |
| jc-021 "נתח גדול יותר מכל פרי בודד במשקאות הממותקים" | peach puree 31.5% > mango 25% > cranberry 25% > apple 14% | PASS |
| jc-024 "פחות פרי מאשר באפרסק ובתות-בננה" | 25% < 40% = 40% | PASS |
| jc-026 "בין המתוקים שבמשקאות הממותקים" | 9.5 = 2nd of non-A stated (plural claim, no sole-max) | PASS |
| jc-027 "חותם את הטבלה" | positional rank 17 (displayed fact; grouped, no sole-worst quality claim) | PASS |
| jc-003 "הסחוט היחיד… שנוקב בזן" | only cultivar-named product (ולנסיה) across 17 names | PASS (name scan) |
| jc-011 "פרי ההדר היחיד שאינו תפוז בין הסחוטים" | A group = 3 oranges + 2 pomegranates (not citrus) + clementine | PASS |

**Tie discipline (sub-2pt = ties; enforced, script-checked):**
- A group is a **six-way tie at 85** — every A verdict frames shared leadership; zero intra-group ranking (orange sugar spread 8.2–8.7 = 0.5 g treated as "קטנים מכדי להכריע").
- Spring nectar trio 37.4/36.9/35.4 — adjacent gaps 0.5/1.5 < 2 → tie language only ("בהפרשים שברמת הרעש", "עד כדי תיקו", "במרחק קטן"). Differentiation by composition only.
- jc-018 vs jc-020 (39.8/38.1, gap 1.7) → "בהפרש קטן מכדי להכריע".
- jc-025 vs jc-026 (33.4/33.3) and jc-027 vs jc-023 (28.5/30.3, gap 1.8) → grouped bottom framing, **no sole-worst claim** (the old copy's "הנמוך ביותר בסקירה" on jc-027 was a 1.8-pt claim; replaced with positional "חותם את הטבלה" + "קבוצה תחתונה צפופה").

## 4. Family map (rule once, differentiate by real deltas)

| Family | Members | Rule stated once | Real differentiators used |
|---|---|---|---|
| Squeezed oranges | jc-003, jc-001, jc-002 | "אותו מוצר משלושה מותגים" (jc-001) | jc-003 = only declared cultivar (Valencia); jc-002 = ingredient string identical word-for-word to jc-001 (verified: both exactly "מיץ תפוזים"); choice = shelf/price |
| Pomegranate pair | jc-006, jc-005 | pomegranate = naturally sweetest/densest | jc-006 carries the 12.6 number (stated); jc-005 = missing sugar label → R2 clause + kcal anchor |
| Clementine | jc-011 | — | only non-orange citrus among the squeezed |
| Ocean Spray pair | jc-017, jc-019 | 25% fruit is the ceiling of both | regular = shortest list on the shelf but real added sugar; diet = sweetener swap that ranks *below* the regular (9.2 pts) |
| Grape drinks | jc-018, jc-020, jc-026 | grape look is engineering (caramel color) | 2% vs 17% (mostly apple: 12/5) vs 9.1% (sugar 2nd in list); sulphite phrasing varied per product |
| Spring nectar trio | jc-021, jc-022, jc-024 | nectar = fruit in sugar water, ties | peach: biggest single-fruit share (31.5%); strawberry-banana: headline fruit = 3%, after the sugar; mango: least fruit but cleanest list (6 items, no colors/preservatives) |
| Lemonana pair | jc-025, jc-027 | bottom-group framing | Tapuzina: main fruit is pear (7.2% vs 3.1% lemon); Prigat: "סחוט" name vs water+sugar-first list (6% lemon) |

## 5. Live truth defects found in production copy (fixed by this re-authoring)

1. **jc-021 (peach) rowVerdict claims "הנמוך בציון מבין שלושת נקטרי ספרינג"** — stale after the TASK-442/395 de-anchor re-flow: current scores make peach the **highest** of the trio (37.4 vs 36.9/35.4). Removed; replaced with tie framing.
2. **jc-024 (mango) rowVerdict claims "האמצעי בציון (35.4) — מעל נקטר האפרסק (35.3)"** — doubly false: mango is now the lowest of the trio, and peach is 37.4 (35.3 no longer exists on the shelf). Also leaked **two literal score values** into consumer copy (same defect class as the hard_cheeses "67 נקודות"). Removed.
3. **jc-023 old copy self-contradicts on ingredient count** — insightLine said "תשעה עשר רכיבים", rowVerdict said "שמונה עשר רכיבים". The parsed ingredient string is truncated ("*עשוי"), so neither count is verifiable. New copy makes no total-count claim; it counts only verifiable sub-claims (2 sugars, 4 stabilizers — both explicit in the parsed list).

## 6. Data flags → Data Agent (no copy leans on these)

- **jc-019** parsed list ends "ממתקים - סוכרלוז, אססולאם קי" — corrupted tail (likely "אצסולפאם K"). d4_additives carries only E440+E955. Copy names only פרוקטוז/סוכרלוז/פקטין (all clean fields).
- **jc-025** parsed list truncated mid-word: "צבע מאכל (כלור" — copy says only "צבע מאכל" (safe under truncation).
- **jc-023** parsed list truncated at "*עשוי" (and contains a Passover-variant stabilizer clause) — total-ingredient-count claims avoided.
- **Stale expansion copy (OUTSIDE 2-field scope, pre-existing):** `expansion.comparisonContext` of jc-021 still says "הנמוך בציון… (35.3)" and jc-024 "האמצעי בציון (35.4)" — same stale-ordering defect class as §5, living in a field this task must not touch. **Route as sibling/handover note for a later expansion pass** (precedent: choctab M3).

## 7. Before/after ×4

**jc-024 (מנגו) rowVerdict — stale scores + score-literal leak, killed:**
- OLD: "25% מחית מנגו מרוכזת — כלומר רוב הפחית אינו פרי. הפחית מציגה מנגו; הרשימה מגלה שהמים באים ראשון. מבין שלושת נקטרי ספרינג בסקירה, נקטר המנגו הוא האמצעי בציון (35.4) — מעל נקטר האפרסק (35.3) ומתחת לנקטר תות-בננה (36.9)."
- NEW: "סוגר את שלישיית הנקטרים במרחק קטן מהשניים האחרים. יש בו פחות פרי מאשר באפרסק ובתות-בננה, אבל הרשימה מהפשוטות במדף הממותק, שישה רכיבים בסך הכל. נקטר בסיסי שעושה בדיוק מה שכתוב עליו: מנגו מרוכז, מים וסוכר."

**jc-025 (תפוזינה לימונענע) insightLine — wrong-angle framing replaced with the real find:**
- OLD: "משקה בטעם תפוז — 10% רכז הוא אגסים ולימון, והתפוז עצמו נעדר מהרשימה." (the product is a lemon-mint drink, so "orange missing" fights a strawman)
- NEW: "האגס הוא הפרי המרכזי בלימונענע הזה, יותר מכפליים מהלימון שעל השם." (7.2% pear vs 3.1% lemon, from the parsed list)

**jc-020 (ג'אמפ ענבים) insightLine — recitation replaced with the composition story the old copy missed:**
- OLD: "17% פרי בלבד — והשאר נשען על צבע קרמל ומשמר מקבוצת הסולפיטים."
- NEW: "משקה הענבים של ג'אמפ מחזיק יותר תפוח מענבים: 12% מול 5%."

**jc-001 (פרימור תפוזים) rowVerdict — em dashes and shaky 0.5g superlative out; honest tie ruling in:**
- OLD: "המיץ הפשוט ביותר שאפשר למצוא: תפוזים סחוטים, ללא ריכוז, בלי כלום נוסף. כל הסוכר בכוס הגיע מהפרי עצמו. עם 8.2 גרם ל-100 מ"ל זהו גם הנמוך ביותר בסוכר מבין מיצי התפוזים הסחוטים — אם בתוך קבוצת ה-A אתם רוצים למזער את הסוכר, זה התפוז לקחת."
- NEW: "אחד מששת השווים בפסגת הסקירה. תפוז בלבד, בלי ריכוז ובלי שום תוספת, וכל הסוכר בכוס הגיע מהפרי. שלושת התפוזים הסחוטים כאן הם למעשה אותו מוצר משלושה מותגים, וההבדלים התזונתיים ביניהם קטנים מכדי להכריע."

## 8. Category honesty note (owner spec)

Sugar-in-liquid tension handled without moralizing and without health-halo: every A verdict carries the free-sugar truth in its own words (e.g. jc-003: "סוכר חופשי בנוזל, בלי הסיבים של הפרי השלם"); no "בריא"/"קל"/"ללא חשש" framing anywhere; jc-019's "no added sugar" is explicitly framed as sweetener work that leaves the fruit share unchanged.

## 9. QA hotspot suggestions (for the Adversarial QA lane)

1. The two fixed stale-trio claims (§5) — re-derive trio ordering independently.
2. jc-011 "פרי ההדר היחיד שאינו תפוז בין הסחוטים" — citrus-scope check (grapefruit appears only in fruit drinks).
3. jc-020 "12% מול 5%" and jc-025 "7.2% אגס / 3.1% לימון" — parse-derived percentages.
4. jc-023 "ארבעה מייצבים" + "שני סוגי סוכר" vs its truncated parsed list.
5. Tie-language sweep: confirm no residual ordering claim inside any sub-2pt cluster.
6. jc-005/jc-011 R2 clause consistency (deliberate 2× repetition).

---

## 10. POST-QA FIX PASS (GO_WITH_FIXES: 0 CRITICAL / 2 HIGH / 3 MEDIUM — 3 fixes applied)

**Artifact versions:** pre-QA preserved as `juices_overhaul_v1_preQA.json` (sha256 `84b030f5b02aac6ead9b3657117b16716f1378878d25dae716f4747eaa6e4b29`, byte-identical to the gated v1). Final post-fix artifact `juices_copy_overhaul.json` sha256 **`9ba0dbcab35dc36774c6116f90befee85eb23c5002a64c4af5a66fba0ccc3ad9`**. Diff continuity: v1→v2 delta = exactly the 3 fixes below.

### Fix 1 — RT-1 HIGH (jc-018 insightLine): false absolute superlative rescoped
QA was right: "נגיעת הפרי הקטנה ביותר בסקירה כולה" was FALSE as an absolute-component claim — jc-025 carries a 1.6% grapefruit component (רכיבי אשכוליות 1.6%), smaller than jc-018's 2% grapes. Census re-derived from scratch (`fruit_census.py`): every % literal verified present in the parsed ingredient strings; min TOTAL fruit share = jc-018 2.0% (next: 9.1%); min SINGLE component = jc-025 1.6%. New copy is explicitly **total-scoped** ("כל הפרי שבבקבוק"), which is bulletproof against both readings.
- OLD: "כמות הענבים כאן, 2%, היא נגיעת הפרי הקטנה ביותר בסקירה כולה."
- NEW: "שני אחוזי ענבים הם כל הפרי שבבקבוק, פחות מכל מוצר אחר בסקירה."

### Fix 2 — RT-3 (jc-017 rowVerdict): non-derivable added-sugar split replaced
"ורובו מהסוכר המוסף" asserted an added-vs-fruit sugar split that no artifact field measures (the limitingFactor text making the same claim is itself generated copy, per QA ruling). Replaced with a parse-derivable fact: in the ingredient list (מים, מיץ חמוציות 25%, סוכר) the sugar sits immediately after the cranberries.
- OLD (sentence 3): "ובכל זאת יש בכוס 11.4 גרם סוכר ל-100 מ"ל, יותר מאשר בתפוז סחוט, ורובו מהסוכר המוסף."
- NEW (sentence 3): "ובכל זאת יש בכוס 11.4 גרם סוכר ל-100 מ"ל, יותר מאשר בתפוז סחוט, כשהסוכר ברשימה מגיע מיד אחרי החמוציות."

### Fix 3 — RT-2, ORCHESTRATOR-AUTHORIZED SCOPE EXCEPTION (jc-021 + jc-024 `expansion.comparisonContext` ONLY)
The two expansion texts leaked raw score literals ("35.3"/"35.4") and asserted the pre-de-anchor trio ordering; after the rowVerdict fix the same card would contradict itself on screen. Minimal edit: only the stale opening claim replaced; **the remainder of each text is byte-preserved** (verified: `new_opening + old_tail == new_text`). No other expansion field on any product touched. New openings: no em dashes, no engine vocab, no new numbers (the retained "(25%)" in jc-024 is a pre-existing number in the preserved clause).
- jc-021 OLD opening: "הנמוך בציון מבין שלושת נקטרי ספרינג בסקירה (35.3)." → NEW: "קרוב בציון לשני נקטרי ספרינג האחרים, וההפרשים בין השלושה קטנים." (tie framing; gaps 0.5/1.5)
- jc-024 OLD opening: "האמצעי בציון מבין שלושת נקטרי ספרינג בסקירה (35.4), ועם אחוז הפרי הנמוך ביניהם (25%)." → NEW: "אחרון בשלישיית נקטרי ספרינג בסקירה, במרחק קטן, ועם אחוז הפרי הנמוך ביניהם (25%)." (aligned with current scores: mango 35.4 is lowest of the trio; "במרחק קטן" keeps tie honesty)

### Post-fix verification (full suite re-run, `verify_juices.py` updated isolation spec)
- Isolation: **36 changed leaves = 34 copy fields + exactly `products[10].expansion.comparisonContext` (jc-021) + `products[12].expansion.comparisonContext` (jc-024); 0 outside the authorized surface**; key-sets identical; scores/grades/ranks/_hash_no_rank identical.
- Em dashes 0 | en dashes 0 | banned vocab 0 | score literals in copy 0 | R4 hits 0.
- Openings still 34/34 unique (jc-018's new opening "שני אחוזי ענבים" collides with nothing).
- Panel grams still 4/17 (same four products); kcal 1/17 (jc-005).
- 5-gram census: max repetition still 2 (only the deliberate R2 clause); nothing >2×.
- Rank-check table: **29/29 PASS**, including the new Fix-1 scope checks (total vs component), Fix-2 derivability check, and the four Fix-3 comparisonContext checks per product (literal removal, no-em-dash, tail byte-preservation, clean opening).
- Rule-5 distributions unchanged: grades A6/D7/E4; scores min 28.5 / max 85 / median 39.8 / stdev 24.26 / most-common 85 (×6). rowVerdict length dist now min 187 / max 230 / median 207 / stdev 12.3.
