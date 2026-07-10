# TASK-461 — Author Report (Content Agent, authoring phase)

**Deliverable:** `brined_v2_copy_overhaul.json` (same directory as this report) — full brined-cheeses
frontend artifact, identical to the origin/master production copy except `insightLine` and
`rowVerdict` re-authored on all 36 products.

**Status: DRAFT.** Awaiting Adversarial QA gate sign-off. This report is self-verification, not approval.

- Baseline: `brined_origin.json`, verified JSON-equal to
  `git show origin/master:bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (freshness
  check in `digest.py` output: `fresh = True`). Baseline sha256 `583db15028fb2fc5c0df0e1c4d4ead2fa81c4bd48ce2522db443ef960ea8c339`.
- Final artifact sha256: `9ba7fc112fd43230aff032fe2aed986ecc117a755eaab6197c89a43f5886fe62`.
- Zero git writes; only read-only `git show` used. No file inside `C:\Bari` touched.
- Serializer proven byte-identical (`json.dumps(ensure_ascii=False, indent=2)` round-trips the
  production file exactly, asserted in `author.py` before any mutation).

---

## (a) Proof of isolation — field-level diff (verbatim `audit.py` output)

```
=== FIELD-LEVEL ISOLATION DIFF ===
_meta identical: True
product count: base=36 new=36
products where changed fields == [insightLine, rowVerdict] exactly: 36/36
violations: []
id order identical: True
_hash_no_rank all identical: True
all non-copy product content byte-identical (stripped dump): True
```

Scores, grades, ranks, nutrition, ingredients, additives, signals, confidence fields, imageUrls,
`_meta`, `_hash_no_rank`: all byte-identical to origin/master. Score distribution therefore unchanged:
n=36, min 47.1, max 82.7, median 66.15, stdev 8.22, grades A:3 B:18 C:13 D:2,
most common score 63.6 (3 products). (Derived by `facts.py` from the artifact.)

## (b) Audit metrics on the NEW copy (verbatim `audit.py` output)

```
OLD: em-dash total=74   NEW: em-dash total=0 (en-dash=0, horiz-bar=0)
banned-vocab hits (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/נקודות): 0   (old copy: 44)
antithesis (", לא " / " ולא ") hits: 0
'שלושה רכיבים': old 19/36 -> new 1/36   (single deliberate use, bc-016, as shelf context)
'נתרן':          old 27/36 -> new 2/36
'מ"ג':           old 24/36 -> new 2/36
opening-3-words uniqueness: insightLine 36/36 unique, rowVerdict 36/36 unique
products containing any digit: 8/36 (old: 36/36)
products reciting nutrition-panel numbers (mg/g): 4/36
rowVerdict length: min 127 / max 220 / avg 166 chars; insightLine: min 60 / max 94 / avg 72
```

### Justification for every number kept

| Product | Number(s) | Why the number IS the story |
|---|---|---|
| bc-002 | 1,550 מ"ג | Max sodium of the entire 5% group (2nd-highest on shelf). The fired driver and the verdict's whole point. |
| bc-007 | 21 גרם | Unique protein max of the 5% group. Defining stat of the product. |
| bc-036 | 1,628 מ"ג | Shelf-max sodium. The single fact that explains a 2-ingredient cheese landing at C. |
| bc-017 | 24% / 14 גרם | Preserved dry-matter-fat clarification: label panel says 14 g while the name says 24%. The contrast requires both numbers. |
| bc-013 | 13% | Fat-tier from the product name (context for "a full-fat cheese in the A range"). |
| bc-011, bc-030, bc-037 | 5% / 16% | Fat-tier group labels from product names; no panel values recited. |
| bc-037 | "עשרים גרם" (spelled out) | Rare-tier protein finding: only 7/36 products reach 20 g. |
| bc-027 | "עשרים אחוז" (spelled out) | Name fact; every pure-sheep feta on the shelf is 20% fat (verified). |
| bc-047 | "חצי אחוז" | Sum of label percentages (שום 0.3% + עשבי תיבול 0.2%) proving the seasoning is token. |
| bc-043 | "ל-D" | Grade letter, displayed on the card anyway. |

Missing-data honesty retained (varied phrasing, once each) for the 3 products with null sugar:
bc-031, bc-037, bc-048.

### Preserved-truth notes
- Twin Tzfatit case (bc-004/bc-005): identity fact kept and sharpened (ingredients + nutrition +
  score verified equal).
- bc-006 vs bc-012: identical nutrition, 1.8-pt score gap presented as a non-difference
  (sub-2-pt noise rule). Same for bc-027 vs bc-028 (0.1) and bc-039 vs bc-041 (0.0).
  bc-024's 1.2–1.3-pt gaps to sibling sheep fetas: no ranking claim made, only the factual
  sodium difference (1,500 vs 930/1,100).
- Oil-dipped feta (bc-048): "different product" insight preserved, voice rewritten.
- **Production-copy error fixed:** old bc-035 copy claimed "על התווית: 14 גרם שומן" (dry-matter
  clarification copied from bc-017), but bc-035's own panel fat is 24.0 g. New copy drops the
  false claim and grounds bc-035 in its real story (added cream, richest bulgarit on the shelf).
  Old bc-035's "מלח (27%)" label oddity was dropped rather than repeated without explanation.

## (c) Superlative / relative-claim rank-check table

All checks computed by `facts.py` against the full 36-product corpus (output: `facts.txt`).

| Product | Claim in new copy | Corpus verification |
|---|---|---|
| bc-004 | "הכי פחות מלוחה במדף" / "הכבישה העדינה ביותר במדף" | sodium 600 = shelf min (tied only with bc-005, its byte-identical twin) |
| bc-004/005 | "המקום הראשון" | rank 1 (shared), grade A |
| bc-005 | "הרשימה, לוח התזונה והציון זהים לחלוטין" | nutrition equal=True, ingredients equal=True, 82.7=82.7 |
| bc-013 | "היחידה במדף שמצהירה על תרבית לקטית" | ingredient scan "תרבית": [bc-013] only |
| bc-013 | "אחת משלוש בלבד שמוותרות על חומר משמר" | no-משמר scan: bc-013, bc-038, bc-036 = exactly 3 |
| bc-013 | "המליחות מהנמוכות כאן" | 720 = 3rd-lowest of 36 |
| bc-001 | "פטת העיזים הטובה במדף" / "מעל כל שאר גבינות העיזים" | goat set (5): 76.1 > next 73.2; gap 2.9 > 2-pt noise floor |
| bc-003 | "חלבון גבוה יחסית לגרסאות הרזות" | 16 g = 4th of 14 in the fat==5 group |
| bc-031 | "החלבון מהגבוהים בין הרזות" | 18.5 g = 3rd of 14 in fat==5 |
| bc-002 | "שיא המלח של קבוצת ה-5%" | 1,550 = max of fat==5 (and 2nd of 36) |
| bc-002 | "חלבון שכמעט מוביל את קבוצת הרזות" | 20.5 = 2nd of 14, 0.5 behind leader |
| bc-007 | "אלופת החלבון של קבוצת ה-5%" | 21 g = unique max of fat==5 |
| bc-007 | "כבישה מלוחה מהמקובל" | 1,300 > shelf median 1,000 |
| bc-008 | "קרובה לראש רשימת העיזים" | 2nd of 5 goat products |
| bc-009 | "ייצור מזורז" | E575 d4 explanation: "סימן לייצור מהיר" (artifact text) |
| bc-010 | "היחידה במדף שמכניסה חמאה לרשימה" | ingredient scan "חמאה": [bc-010] only |
| bc-010 | "בחצי התחתון של קבוצת הרזות" | 10th of 14 in fat==5 by score |
| bc-006/032 | "פחות חלבון מרוב המדף/השכנות" | 10 g; 29/36 products have more |
| bc-012 | "הפרש הציון קטן מכדי להטות קנייה" | 1.8 pts < 2-pt noise floor; nutrition equal=True |
| bc-029 | "מלח מהעדינים במדף" | 770 = 4th-lowest of 36 |
| bc-029 | "המדורגת הגבוהה ביותר בין הפטות השמנות" | fat>=16 fetas: 68.8 top, gap 2.2 to next |
| bc-011 | "כבישה מלוחה יותר" (vs siblings) | 1,200 vs 1,010 (bc-006/bc-012) |
| bc-014 | "הכבישה המלוחה מהמקובל" | 1,300 > median 1,000 |
| bc-037 | "מעט גבינות כאן נוגעות בעשרים גרם חלבון" | protein>=20: 7/36 |
| bc-037 | "חלבון שמוביל את כל קבוצת ה-16%" | 20 g = max of fat==16 (9 products) |
| bc-015 | "מליחות שגרתית" | 950 ≈ median 1,000 |
| bc-038 | "החלומי המוביל במדף" | halloumi set (4): 65.7 vs next 63.6; gap 2.1 > 2 |
| bc-038 | "בלי חומר משמר" | ingredient scan: no משמר in list |
| bc-016/043/047 | stabilizers rare on shelf | E406/E410 present only in these 3 of 36 |
| bc-025 | "מליחות ממוצעת" | 1,000 = shelf median exactly |
| bc-027 | "מליחות מעט מעל השכנות" | 1,100 vs median 1,000 |
| bc-027 | sheep feta = 20% fat as category constant | all 3 pure-sheep fetas: fat 20.0 |
| bc-028 | "הפרש אפסי בציון" (vs bc-027) | 0.1 pts |
| bc-018 | "החלבון הכי גבוה בין גבינות העיזים" | 17 g = goat max (5 products) |
| bc-018 | "המלח הכי כבד ביניהן" | 1,400 = goat max |
| bc-018/017 | "מהמלוחות בקטגוריה/במדף" | 1,400 = tied 4th-highest of 36 |
| bc-036 | "המלוחה במדף כולו" | 1,628 = shelf max |
| bc-036 | "אין רשימה נקייה יותר מחלב ומלח" | 2 top-level ingredients = unique shortest list |
| bc-036 | "הקלוריות בחלק הגבוה" | 257 kcal = 8th of 36 (top quartile) |
| bc-039 | "שיא החלבון של המדף" | 24 g = unique shelf max |
| bc-039 | "החלומי הכבד ביותר בו" | fat 28 = halloumi max (28>24,24,23) |
| bc-039 | "צפיפות קלורית מהגבוהות בו" | 356 kcal = top-2 (356 vs 355 treated as tie; no "highest" claim) |
| bc-041 | "פחות שומן ופחות קלוריות... הציון יוצא זהה" | 24<28 fat, 310<356 kcal, 63.6=63.6 |
| bc-024 | "המלוחה בין הכבשים" | 1,500 = max of sheep fetas (1,100 / 930 next) |
| bc-017 | 24% = dry-matter reading, panel 14 g | panel fat 14.0 vs name "24%"; hedged "ככל הנראה" (preserved from prod copy) |
| bc-030 | "בחלק התחתון של קבוצת ה-16%" | 6th of 9 by score |
| bc-035 | "הבולגרית העשירה ביותר במדף" | fat 24 = max of 18 bulgarit products (next 16) |
| bc-035 | "מכפילה ויותר את הקלוריות" (vs lean Tzfatit) | 274/117 = 2.34x |
| bc-035 | "אזור התחתון של הבולגריות" | 3rd-lowest bulgarit score |
| bc-044 | "היחיד במדף עם... ניטראטים" | E252 scan: [bc-044] only |
| bc-044 | "מתחת לאחיו" | 57.7 vs 63.6/63.6/65.7; gap 5.9 > 2 |
| bc-048 | "המוצר השמן ביותר במדף" | fat 31 = shelf max (next 28) |
| bc-048 | "חלבון מהנמוכים בו" | 8 g = 3rd-lowest |
| bc-048 | "המלח דווקא מרוסן" | 800 = 5th-lowest sodium |
| bc-043 | "כמחצית מהמקובל במדף" (protein) | 7.3 vs shelf median 14.0 |
| bc-043 | "מהדלות בקטגוריה" | 2nd-lowest protein |
| bc-043 | "אחת משתי הגבינות היחידות שיורדות ל-D" | D grades: exactly [bc-043, bc-047] |
| bc-047 | "הרשימה הארוכה במדף" | 9 top-level items = unique max (next 6) |
| bc-047 | "החלבון הנמוך במדף כולו" | 7.0 = shelf min |
| bc-047 | "סוגרת את הדירוג" | rank 36/36 |
| bc-047 | "חצי אחוז בסך הכל" | label: שום 0.3% + עשבי תיבול 0.2% |

Noise-floor discipline: every claim of similarity/difference between specific products was checked
against the 2-pt rule (bc-006/bc-012: 1.8 = "no difference"; bc-027/bc-028: 0.1 = "identical bottom
line"; bc-039/bc-041: 0.0 = "same score"; bc-024 vs siblings: 1.2/1.3 = no rank claim made;
bc-001 vs bc-008: 2.9, bc-038 vs next halloumi: 2.1, bc-044 vs siblings: 5.9 = rank claims allowed).

## (d) Before / after — 5 representative products

### bc-004 — גבינה צפתית 5% (top A, rank 1)
**Before (insight):** הנתרן הנמוך ביותר בין כל גבינות ה-A — ורק שלושה רכיבים.
**Before (verdict):** צפתית 5% מחלבות גד. הנתרן (600 מ"ג) נמוך משמעותית מחציון המדף — ולכן הגבינה הזו נמלטת מחיסרון פער הנתרן. עם זאת, 600 מ"ג מחייב חיסרון בסיסי מינימלי, כפי שכל גבינה בטווח הזה מקבלת. שלושה רכיבים, עיבוד מינימלי.
**After (insight):** הגבינה הכי פחות מלוחה במדף, וזה בדיוק מה שמרים אותה למקום הראשון.
**After (verdict):** צפתית קלאסית שעושה הכל נכון: חלב, מלח וחומר משמר יחיד, שומן נמוך, והכבישה העדינה ביותר במדף. בקטגוריה שנמדדת על המלח שלה, הגבינה שמרסנת אותו לוקחת את המקום הראשון.

### bc-025 — בולגרית מסורתית 16% שופרסל (mid B, rank 21)
**Before (insight):** בולגרית 16% פשוטה: שלושה רכיבים, רשימה נקייה, נתרן ליד החציון.
**Before (verdict):** בולגרית מסורתית 16%. שלושה רכיבים, חומר משמר בודד, כ-14 גרם חלבון. הנתרן (1,000 מ"ג) בדיוק על החציון ולא מוסיף חיסרון מעבר לבסיס. ה-B נובע מ-16% שומן.
**After (insight):** הבולגרית השמנה של שופרסל נשארת בתלם: רשימה בסיסית, מליחות ממוצעת, בלי דרמות.
**After (verdict):** גרסה ישרה של בולגרית שמנה: חלב, מלח וחומר משמר, בלי אף תוספת מעבר. הדירוג משקף כמעט אך ורק את בחירת השומן, ומי ששלם איתה מקבל גבינה מסודרת בהחלט.

### bc-005 — גבינה צפתית מעודנת 5% (the identical-twin case, rank 1)
**Before (insight):** גרסת 'מעודנת' — ציון וטביעת אצבע תזונתית זהים לחלוטין לגרסה הסטנדרטית.
**Before (verdict):** צפתית מעודנת 5% מחלבות גד. כל נתון — שומן, חלבון, נתרן, רשימת רכיבים — זהה לגרסה הסטנדרטית של אותה מחלבה. בארי לא מצאה הבדל מהותי בין השתיים.
**After (insight):** אותה גבינה בדיוק עם המילה 'מעודנת' על האריזה: זהה לצפתית הרגילה של גד בכל נתון.
**After (verdict):** מי שמתלבט בין שתי הצפתיות של גד יכול להירגע: הרשימה, לוח התזונה והציון זהים לחלוטין. ההבדל היחיד שמצאנו כתוב על האריזה, ובתוך המקרר זו אותה גבינה.

### bc-036 — גבינת טמרה מלוחה בקר 17% (C, rank 25)
**Before (insight):** שני רכיבים בלבד — אבל הנתרן הגבוה ביותר במדף, 628 מ"ג מעל החציון.
**Before (verdict):** גבינת טמרה מלוחה — שני רכיבים בלבד: חלב ומלח. אין כלום מיותר. ובכל זאת C. הסיבה: 1,628 מ"ג נתרן — הגבוה ביותר במדף, 628 מ"ג מעל חציון המדף. הכבישה הממושכת מקבלת חיסרון כפול: בסיסי ופער. גם שומן של 17% ו-257 קק"ל מוסיפים.
**After (insight):** הפשטות הכי קיצונית במדף פוגשת כאן את המליחות הכי קיצונית בו, והמלח מכריע.
**After (verdict):** אין רשימה נקייה יותר מחלב ומלח, ובכל זאת הגבינה יושבת עמוק בטבלה: הכבישה שלה היא המלוחה במדף כולו, 1,628 מ"ג נתרן, והקלוריות גם הן בחלק הגבוה. תזכורת טובה לכך שגם כבישה מסורתית לגמרי יכולה להגזים במלח.

### bc-047 — בולגרית שום+עשבי תיבול 16% (worst D, rank 36)
**Before (insight):** 10 רכיבים, מדד עיבוד גבוה, תקרת עיבוד — הציון הנמוך ביותר בין הבולגריות.
**Before (verdict):** בולגרית מתובלת של משק צוריאל: 10 רכיבים כולל מייצבים, מי מלח, סיבים תזונתיים, שום ועשבים. מדד עיבוד גבוה — ועוצר בתקרה. 7 גרם חלבון בלבד. עיבוד גבוה, מייצבים ו-7 גרם חלבון הם הגורמים.
**After (insight):** הרשימה הארוכה במדף פוגשת את החלבון הנמוך בו, והשילוב סוגר את הטבלה.
**After (verdict):** התיבול עצמו סמלי, חצי אחוז בסך הכל של שום ועשבים, ומסביבו הרשימה העמוסה בקטגוריה: מייצבים, רכיבי חלב וסיבים מוספים. עם החלבון הנמוך במדף כולו זו הגבינה שסוגרת את הדירוג, והמרחק שלה מפשטות הצמרת הוא כל הסיפור של הקטגוריה.

---

## Handover notes (for the git-owning lane, after QA sign-off)
- Target file: `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (replace whole file
  with `brined_v2_copy_overhaul.json`; the artifact already carries origin/master's exact bytes for
  everything except the 72 copy fields).
- Commit-time baseline for run_gates `--baseline`: origin/master copy, sha256
  `583db15028fb2fc5c0df0e1c4d4ead2fa81c4bd48ce2522db443ef960ea8c339`.
- The main working tree's copy of this file is stale (993 lines behind production); do not diff
  against it.
- Re-run `audit.py` (this directory) after any further edit; it re-proves isolation + all metrics.
