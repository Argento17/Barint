# TASK-461 Phase-2 #9 — GRANOLA copy overhaul: Content-author return (DRAFT until Adversarial QA)

Author lane: C1 native content (this agent). Scope: insightLine + rowVerdict ONLY, all 22 products of
`bari-web/src/data/comparisons/granola_frontend_v2.json`. Register per owner-accepted pilot + house rules R1–R4.

## 1. Isolation proof (zero git writes; nothing under C:\Bari touched)

- Baseline obtained read-only: `git show origin/master:bari-web/src/data/comparisons/granola_frontend_v2.json`
  → scratchpad `granola_origin.json`. **Blob sha (git ls-tree): `60539d49b9a5f817f21e6e8b0c33360732a94061`.**
  File sha256 `ac543531ea543ceccbabbfa60e09f5ae07395e5a2a3c7ab8aedf8d0c6475fd23` (89,672 bytes). NEVER the local tree.
- Only git commands run: `ls-tree`, `show` (read-only). No add/commit/branch/checkout/stash/worktree/push.
- All outputs in scratchpad. Hebrew authored via `.py` files + `python -X utf8` (no shell-inline Hebrew).
- Round-trip proof: `json.dumps(origin, ensure_ascii=False, indent=2)` reproduces the origin file byte-for-byte
  (asserted in `granola_author.py`), so the swap is byte-safe outside the two copy fields.
- **Field isolation (script-derived, `granola_verify.py` §1): 44 changed leaves = exactly
  `products[i].insightLine` ×22 + `products[i].rowVerdict` ×22; out-of-scope diffs: 0.**
  `_meta` byte-identical; `score`/`grade`/`rank`/`_hash_no_rank`/`expansion`/`d4_additives` identical for 22/22.
- rowVerdict key coverage checked FIRST (hummus lesson): 22/22 products carry both keys in production; 0 keys added.

## 2. Deliverable

- **Artifact: `granola_copy_overhaul.json`** (scratchpad, 89,909 bytes)
  sha256 `f322a871829915c35929d64d9e616cc5c166a16e76d5dc807fc6a25819a815c2`
- Score immobility (Rule 5): grade_dist **B:4 C:8 D:8 E:2**, min 32.8 / max 69.7 / median 52.3 /
  stdev 12.789 / most_common_score 61.0 (×2) — **identical before and after; score vectors byte-equal.**

## 3. Copy metrics (all script-derived, `granola_verify.py`)

| Metric | Baseline | New |
|---|---|---|
| Em dashes in copy fields | 52 (per-product dist {1:4, 2:9, 3:6, 4:3}) | **0** (dist {0:22}); en dashes 0 |
| Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/NOVA) | present in category style | **0** |
| R4 purchase-verb drift (כדאי/שווה + לקנות/לבחור/לרכוש) | — | **0** |
| Score literals (decimals not %, "נקודות") | — | **0** (single decimal hit = 4.8 גרם sugar, a panel fact, not a score) |
| Opening 3-words uniqueness | template-repetitive | **44/44 unique** (both fields) |
| 5-gram census (R3) | — | **max repetition = 1** (limit ≤2) |
| Panel grams/mg/kcal products | 77.3% recitation | **2/22** (both justified shelf extremes, see §4) |
| Grade-letter mentions | pervasive | 2 (#5 "ובכל זאת C" = the clean-list paradox; #21 "שתי ה-E" = bottom-pair standing) |
| "בסקירה" stamps | — | 0 |

Panel-number justification (≤4/22 allowed, used 2):
- **7290106773714 (מיקס קראנץ' מלוח):** 504 קק"ל = shelf max (next 451); 4.8 גרם סוכר = shelf min (next 8.0); 394 מ"ג נתרן = shelf max (next 195). Triple verified extreme; the product IS the number story. Sodium stated as displayed fact; the C is attributed to energy density (per the artifact's comparisonContext), never to a sodium penalty (TASK-189 gap respected).
- **7290011668587 (עשירה):** 25 גרם סוכר = shelf max (next 21.0) and the driver of the EV-105/TASK-385 flag.

## 4. Superlative rank-check table (script vs all 22, `granola_verify.py` §6)

| Claim in copy | Value | Next | Verdict |
|---|---|---|---|
| #19 "המתוקה בקטגוריה" | sugar 25.0 | 21.0 | TRUE, unique max |
| #5 "הסוכר הנמוך במדף" | 4.8 | 8.0 | TRUE, unique min |
| #5 "שיא הקלוריות של הקטגוריה" | 504 | 451 | TRUE, unique max |
| #5 sodium 394 מ"ג (stated fact) | 394 | 195 | TRUE, unique max |
| #4 "סיבים בראש המדף/הטבלה" | 14.7 | 14.5 | TRUE exact max (0.2 margin noted) |
| #19 "הסיבים הנמוכים בקטגוריה" | 5.7 | 6.0 | TRUE, unique min |
| #6+#9 "שיא החלבון... מתחלק בין שתי אחיות" | 23.7/23.6 | 20.7 | TRUE pair, 0.1 apart → ruled as shared |
| #16 "החלבון מהנמוכים בקטגוריה" | 8.7 | 8.9 | TRUE min, hedged (cluster 8.7–9.0) |
| #8 "הסיבים מהנמוכים במדף" | 6.3 | 4th-lowest | TRUE hedged |
| #11 "הסוכר הגבוה במשפחת שקד תבור" | 15.6 | family: 9.9/9.5/4.8 | TRUE family max |
| #1 "צמרת המדף מתחלקת בין שתיים" / #2 "צמודה לראש המדף" | 69.7 vs 69.3 | gap 0.4 | sub-2pt → shared-top framing |
| #21+#22 shared bottom | 33.4 vs 32.8 | gap 0.6 | sub-2pt → tie framing (fixes live sole-lowest claim) |
| #15 "עד לציון זהה" (Fitness twins) | 41.0 = 41.0 | third sister 40.9 | TRUE exact tie |

Sweetener-count and share claims: **15/15 sweetener checks + 15/15 share-claim checks PASS** against the parsed
ingredient strings (verify §7–§8), incl. #9=3 sources, #15=4, #16=4, #17=5-in-base, #19=3, #20/#22=3-in-base,
quinoa 2.9%, honey 2.1%, pecan 3% last, nuts 4.5% after raisins, base 89%/83%.

## 5. Family map (rule once, differentiate by real deltas)

| Family | Members (rank) | Ruling | Differentiators used |
|---|---|---|---|
| דני וגלית | #1, #3 | clean-list top pair | #1 chicory-boosted fiber + apple-concentrate sweetening; #3 monk-fruit choice vs maple-8% central sweetener |
| תלמה (protein series) | #2, #6, #9 | protein is engineered (soy concentrate/isolate), ruled at #2; #6+#9 share protein max | #2 chocolate+B-standing; #6 cranberries carry sugar+veg oil, 15 ingredients; #9 nuts 9% + THREE sweeteners |
| שקד תבור | #4, #5, #7, #11 | brand pattern = real nuts/chicory + syrup sweetening | #4 fiber max/calorie near-max; #5 cleanest list triple-extreme; #7 chicory 10% behind fiber; #11 three syrups, family sugar max |
| שקוף שזה טבעי | #8, #10, #12, #13 | name promises transparency/nature, list is engineered | #8 pea-protein engineering; #10 superfood-vs-average gap; #12 brown sugar 2nd; #13 no-added-sugar vs maltitol+double veg fat |
| פיטנס | #14, #15, #16 | industrial skeleton ruled at #14 (real whole grain + 3–4 sugar sources + sunflower oil) | #14 chocolate; #15 quinoa 2.9% gimmick, 4 sources, exact-tie twin; #16 honey 2.1% = smallest of 4 sweeteners, shelf-low protein |
| גרין | #17, #18, #21 | two processed layers (granola + cereal-bar bits), each with palm oil + caramel color | #17 nuts 4.5%; #18 near-copy, pecan 3% last; #21 + candied/preserved fruit layer → E |
| שוק קולינרי | #20, #22 | one industrial base = 89%/83% of product | #20 nuts-name vs 4.5%; #22 candied-fruit layer, shared shelf bottom |

## 6. Live truth defects found & fixed (in the two owned fields)

1. **#19 (7290011668587) grade contradiction:** production copy says "מסבירים את ה-E" while the artifact's
   score fields say **38.0 / D**. New copy uses NO grade letter for this product (standing framed via the
   verified sugar max). Root cause routed as data flag (see §7.1) — this is the "known queued defect" class.
2. **#9 (7290112497994) sweetener undercount:** live "שני ממתיקים (סירופ גלוקוז וסוכר)" — parse contains
   THREE top-level added-sugar sources (סירופ גלוקוז, סילאן, סוכר). Fixed to three.
3. **#19 sweetener undercount:** live "שני מקורות סוכר מוסף: סוכר ואיזוגלוקוז" — parse also contains
   סילאן תמרים. Fixed to three.
4. **#22 (1343845) tie-discipline breach:** live "הנמוכה ביותר בקטגוריה" at 0.6pt below #21 (sub-2pt = tie).
   Reframed as shared bottom; #21 reframed symmetrically ("אחת משתי גרנולות ה-E").
5. **#21 over-claim trimmed:** live copy implies ALL fruits candied+preserved; parse shows raisins plain and
   banana candied without sulfite. New copy: "רוב הפירות" + names the four candied ones only.

## 7. Flags routed onward (NOT fixed here — outside 2-field scope)

1. **DATA/ORCHESTRATOR — #19 three-way inconsistency:** `_meta.generated_from` states the TASK-385/EV-105 refresh
   applied (7290011668587 D→E, 38.0→33.0, run `run_granola_task385_25g`), but the product's score fields still
   read 38.0/D (rank 19), while its expansion copy (comparisonContext + consumerExplanation, untouched) still
   says E. Either the refresh never landed in the score fields or _meta overstates. Expansion staleness =
   pre-existing baseline defect (choctab M3 class) → sibling note + future expansion pass.
2. **DATA — #3 (7290017962023) name-vs-parse gap:** name contains "תמר", scanned ingredient list contains no
   date ingredient (has אוכמניות 5%). Possible parse drop or name-integrity issue. Kept OUT of consumer copy
   (negative-absence claims on OCR-noisy parses are not defensible).
3. **DATA — #5 (7290106773714) artifact-internal tension:** positiveSignals claims "ללא סוכר מוסף" while the
   parse lists סילאן טבעי (date syrup). New copy avoids asserting "ללא סוכר מוסף"; states silan as the only
   sweetening + shelf-min sugar fact.
4. **DATA (cosmetic OCR):** "אוכ מניות" (#1), "סירופגלוקוז" (#20), "(דגלים" for דקלים (#21 sub-list), "בנננה"
   (#21). No copy leans on corrupted tokens.
5. **OFF check:** 3 regex hits, ALL inside `_meta`'s TASK-238 removal-provenance note (P35 sweep documentation
   of products REMOVED for OFF sourcing). No OFF dependency in any displayed field → no CRITICAL.

## 8. Before/after ×4

**#19 עשירה (grade-contradiction + undercount fix)**
- Before (IL): "הממותקת ביותר במדף — שני מקורות סוכר מוסף ברשימה: סוכר ואיזוגלוקוז. חומר משמר שמופיע עם הפירות היבשים." (RV ends "...מסבירים את ה-E" — vs grade field D)
- After (IL): "המתוקה בקטגוריה, עם 25 גרם סוכר ל-100 גרם שמגיעים משלושה כיוונים: סוכר, איזוגלוקוז וסילאן תמרים."
- After (RV): "עשירה זה תיאור מדויק בעיקר לגבי הסוכר: שלושה ממתיקים מוספים, פירות יבשים שמגיעים עם חומר משמר גופריתי, והסיבים הנמוכים בקטגוריה. האננס, הפפאיה והצימוקים אמיתיים ונדיבים, וכל מה שסביבם ממותק ומשומר."

**#9 פרוטאין+אגוזים (sweetener count fix)**
- Before (RV): "הבסיס טוב — שיבולת שועל מלאה 51%, אגוזים 9% ... והרשימה הארוכה עם שני ממתיקים (סירופ גלוקוז וסוכר) מונעת ממנה לטפס ל-B."
- After (IL): "חולקת עם אחותה את שיא החלבון של הקטגוריה, ומלווה אותו בשלושה ממתיקים נפרדים: סירופ גלוקוז, סילאן וסוכר."
- After (RV): "תשעה אחוזי אגוזים, קשיו, שקדים, פקאן וקוקוס, מייחדים אותה בתוך סדרת החלבון של תלמה. הבסיס נשאר שיבולת שועל מלאה מעל מחצית, החלבון מגיע מתוספת סויה, ושלושת מקורות הסוכר ברשימה מסבירים למה היא מביטה במובילות מלמטה."

**#5 מיקס קראנץ' מלוח (the character product; sodium-as-fact, C-via-density)**
- Before (IL): "רשימת רכיבים נקייה מהמדף — שיבולת שועל, שלושה סוגי אגוזים, זרעי חמנייה ודלעת, טחינה, סילאן, ללא סוכר מוסף. הסוכר הנמוך מטעה: ... וזה חלק גדול מהסיבה שהיא נשארת ב-C ולא מטפסת גבוה יותר."
- After (IL): "מהרשימות הנקיות בקטגוריה, עם סילאן כהמתקה יחידה, ובכל זאת C: אגוזים, זרעים וטחינה מרכזים כאן 504 קלוריות ל-100 גרם."
- After (RV): "הסוכר הנמוך במדף, 4.8 גרם בלבד, נמצא דווקא בגרנולה הזאת, לצד שלושה סוגי אגוזים, טחינה וזרעים, בלי שמן מוסף ובלי תוספים. הצפיפות היא הצד השני של אותה רשימה: שיא הקלוריות של הקטגוריה, והמלח שבשם מביא איתו 394 מ\"ג נתרן. מי שסופר קלוריות ימצא כאן הרבה מהן בכל כף."

**#22 עם פירות (tie discipline)**
- Before (IL): "שמן דקלים, סירופ גלוקוז וסוכר חום בגרנולת הבסיס — ו-17% פירות שכולם מסוכרים בנפרד עם חומרי שימור. הנמוכה ביותר בקטגוריה."
- After (IL): "תחתית המדף מתחלקת בין שתי גרנולות פירות, וזו אחת מהן: בסיס עם שמן דקל ושלושה ממתיקים, ופירות שכמעט כולם מסוכרים מראש."
- After (RV): "שכבת הבסיס, 83% מהמוצר, נושאת שמן דקל, סוכר חום, סירופ גלוקוז ודבש, ומעליה פירות שכמעט כולם הגיעו מסוכרים או משומרים: פפאיה, אננס, בננה, חמוציות ותפוח. ההרכב הזה, שכבה אחרי שכבה, הוא שמסביר את מיקומה למטה."

## 9. Category-context compliance

- **TASK-189 sodium gap respected:** sodium appears once (shelf-max fact on #5); the C is attributed to energy
  density per the artifact's own comparisonContext; no sodium drama invented anywhere else (e.g., #19's 195mg not mentioned).
- **Health-image-vs-label** is the shelf's editorial spine: every name-promise (אגוזים 4.5%, פקאן 3%, קינואה 2.9%, דבש 2.1%, סופרפוד, פיטנס, תמר, ללא תוספת סוכר) is exposed factually, never moralized.
- **R1:** the only provenance adjective is "מייפל קנדי" — verbatim from the parse ("סירופ מייפל קנדי (8%)").
- **R2:** all 22 products are `verified`/`sufficient` ("מבוסס על נתונים מלאים") → zero partial-scan narration, consistent shelf-wide.

## 10. POST-QA SURGICAL FIX — M2 (orchestrator-dispatched, 2026-07-02)

QA verdict on v1: **GO_WITH_FIXES (0 CRITICAL / 0 HIGH / 3 MEDIUM)**. M1 (2 grade letters) accepted as-is
per orchestrator ruling (matches pilot register); M3 routed. M2 = this fix.

- **Scope: exactly ONE field — #14 (7613035635845) `insightLine`.** Nothing else touched
  (tree-walk vs pre-fix artifact: 1 changed leaf, `$.products[13].insightLine`; asserted in `granola_fix_m2.py`).
- **Finding (R1):** "הצהרת 95% דגנים מלאים אמיתית" endorsed a figure that exists only as a package
  declaration (artifact positiveSignals: "95% דגנים מלאים לפי ההצהרה"), not in the parse.
- **Old IL:** "הצהרת 95% דגנים מלאים אמיתית, ומסביבה שלושה מקורות סוכר מוסף, שמן חמניות ועוד סוכר בתוך השוקולד עצמו."
- **New IL:** "על האריזה מוצהרים 95% דגנים מלאים, וברשימה עצמה מקיפים אותם שלושה מקורות סוכר מוסף, שמן חמניות ועוד סוכר בתוך השוקולד."
  (declaration attributed to the package; insight — genuine whole-grain base ringed by 3 sugar sources + oil — retained; no new numbers.)
- **rowVerdict check (QA-requested):** "דגן מלא אמיתי בבסיס" IS parse-corroborated — whole-grain
  ingredients lead the scanned list: פתיתי שיבולת שועל מלאה (42.8%) at index 0, קמח חיטה מלא (14.1%)
  second, before the first sugar (script-verified index order 0 < 45 < 80). **rowVerdict unchanged.**
- **Full suite re-run on the fixed artifact — all constraints hold:** isolation vs origin 44/44 copy-leaves
  (out-of-scope 0), em/en dashes 0, banned vocab 0, R4 0, openings 44/44 unique (new opening "על האריזה מוצהרים"
  collides with nothing), max 5-gram = 1, panel-number products 2/22, all 15+15 parse checks PASS,
  grade letters still exactly the 2 accepted under M1.
- **Artifact continuity:** pre-fix preserved as `granola_overhaul_v1_preQA.json`
  (sha256 `f322a871829915c35929d64d9e616cc5c166a16e76d5dc807fc6a25819a815c2` = the exact QA-gated version);
  fixed deliverable `granola_copy_overhaul.json`
  sha256 **`1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5`**.

## QA hotspot suggestions (for the adversarial lane)

#19 no-letter framing vs the D/E mess; #5 "בלי שמן מוסף ובלי תוספים" (parse has no oil, d4 empty) and the
silan-only-sweetener claim; the three shared-max/tie rulings (#6/#9 protein, #1/#2 top, #21/#22 bottom);
#13 "שומן צמחי כפול"; #18 "סוגר את הרשימה" (pecan literally last); #17 "חמישה מקורות סוכר" base-scoped.
