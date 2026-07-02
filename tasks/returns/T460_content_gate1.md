# TASK-460 Gate 1 — Fix stale hardcoded distribution prose across page-data adapters

Worktree: `C:\bari_wt_t461` (branch `fix/task460-stale-adapter-prose`, cut from origin/master at `4b21fbfa`)
Scope: `C:\bari_wt_t461\bari-web\src\lib\comparisons\*-page-data.ts` (18 files) + `C:\bari_wt_t461\bari-web\src\app\hashvaot\**\*.tsx`
Method: read every adapter's own JSON import in full, cross-checked every numeric/grade claim against the real JSON in this worktree (grade tallies computed by script, not eyeballed), fixed every STALE claim, left every TRUE claim untouched.

## Phase 1 — Full inventory

Legend: TRUE = verified matches JSON. STALE = verified mismatch, fixed in Phase 2. UNVERIFIABLE = cannot cheaply confirm/refute against structured JSON fields; not touched (flagged for follow-up), or restructured to remove the unverifiable specificity.

| # | File:line | Claim (verbatim/paraphrase) | JSON truth (source + method) | Verdict |
|---|---|---|---|---|
| 1 | brined-cheeses-page-data.ts:55 | "9 בדירוג A, 20 ב-B, 5 ב-C ו-2 ב-D" | Counted `grade` field across `brined_cheeses_frontend_v2.json` products (n=36): A=3, B=18, C=13, D=2 | **STALE** |
| 2 | brined-cheeses-page-data.ts:55 | "התשובה לא נמצאת במלח" (negation phrasing) | Voice rule: no "X, not Y" / negation-flavored phrasing | **STALE (voice)** |
| 3 | brined-cheeses-page-data.ts:56 | "הציונים הגבוהים ביותר, 85, שייכים לצפתיות ולפטה של מחלבות גד" | Top scores in `brined_cheeses_frontend_v2.json`: Tzfatit Gad 82.7/A (x2), Petha-izim Gad 76.1/B. No product scores 85. Max score in corpus = 82.7. | **STALE** |
| 4 | brined-cheeses-page-data.ts:56 | "המרשימה שבהן היא הבולגרית 13% של יורו... נתרן נמוך יחסית של 720 מ"ג, וציון בדירוג A" | Verified: "קוביות בולגרית מעודנת 13%" / יורו מחלבות אירופה, score 80.3, grade A | TRUE (unchanged) |
| 5 | brined-cheeses-page-data.ts:56 | "טמרה של רג'ב, יושבת דווקא ב-C כי הנתרן שלה הוא הגבוה במדף" | Verified: "גבינת טמרה מלוחה בקר 17%" / מחלבת רג'ב, score 63.6, grade C, sodium 1628mg = max sodium in corpus | TRUE (unchanged) |
| 6 | brined-cheeses-page-data.ts:59-64 (categoryNote, methodologyLines) | No numeric claims | n/a | TRUE (unchanged) |
| 7 | brined-cheeses-comparison-page-data / metadata:70 & hashvaot/brined-cheeses/page.tsx:17 | "השוואת 36 גבינות מלוחות" | `products.length` in `brined_cheeses_frontend_v2.json` = 36 | TRUE (unchanged) |
| 8 | cereals-page-data.ts:63 | "20 מוצרים, אף אחד לא מגיע ל-A" | `cereals_frontend_v2.json` n=20, max score 74.7 (grade B), no A present | TRUE (unchanged) |
| 9 | cereals-page-data.ts:68 | "שניים ב-B, שבעה ב-C, תשעה ב-D ושניים ב-E" | Counted grade field (n=20): B=2, C=6, D=10, E=2 | **STALE** (2/7/9/2 claimed vs actual 2/6/10/2) |
| 10 | cereals-page-data.ts:76-79 (categoryNote) | No numeric claims (regulatory threshold description) | n/a | TRUE (unchanged) |
| 11 | cereals-page-data.ts:82-85 (methodologyLines) | "20 מוצרי דגני בוקר... אף מוצר לא הגיע ל-A" | Matches JSON n=20, no A | TRUE (unchanged) |
| 12 | cheese-page-data.ts (all hero/prologue/methodology/caveat) | Sourced from `cheese_frontend_v5.json:page_copy` directly (single source of truth, not a hardcoded .ts literal) | n/a — content lives in JSON, adapter just reads it | TRUE by construction (not a .ts hardcode; out of scope to re-verify JSON content per task boundary) |
| 13 | cakes-hard-cookies-page-data.ts (hero/prologue/methodology/caveat) | Sourced from `cakes_hard_cookies_frontend_v1.json:page_copy` directly | JSON page_copy.hero: productCount=62, scoredCount=62; verified `products.length`=62, grades C=1,D=1,E=60 | TRUE by construction |
| 14 | cakes-hard-cookies supermarket description (hashvaot/supermarket/page.tsx:78-82) | cCount/dCount/eCount/cakesTopScore computed live via `.filter()`/`.reduce()` on `cakesHardCookiesProducts` | Always recomputes from current JSON — durable by construction | TRUE (unchanged) |
| 15 | chocolate-bars-comparison-page-data.ts:51 | "כל מוצר במדף הזה מקבל ציון E" | `chocolate_bars_frontend_v1.json` n=23, grades: {E: 23} — all E | TRUE (unchanged) |
| 16 | chocolate-bars supermarket description (page.tsx:71) | "כולם ציון E" | Same, confirmed all-E | TRUE (unchanged) |
| 17 | chocolate-tablets-comparison-page-data.ts:51 | "המוצר הטוב ביותר במדף הזה מדורג C" | `chocolate_tablets_frontend_v1.json` n=35, grades {B:2,C:6,D:10,E:17} | **UNVERIFIABLE-then-confirmed-STALE**: best grade present is actually B (2 products), not C. See note below. |
| 18 | cookies-coffee-page-data.ts (hero/prologue/methodology/caveat) | Sourced from `cookies_coffee_frontend_v2.json:page_copy` directly | `products.length`=117 but `page_copy.hero.productCount`/`scoredCount`=119, and prologue text says "83 מתוך 119" | **Internal JSON inconsistency found (119 vs 117) — lives inside the JSON's own page_copy field, not in the .ts adapter or any TSX string. Out of scope for this copy-only .ts/.tsx fix per task boundary ("Do NOT touch... JSON"). Flagged for Data/Content Agent follow-up.** |
| 19 | cookies-coffee supermarket description (page.tsx:77) | `${cookiesCoffeeProducts.length} מוצרים נבדקו` | Uses `.length` live = 117 | TRUE (unchanged, durable) |
| 20 | crackers-page-data.ts (hero/prologue/methodology/caveat) | Marked DRAFT/PENDING_COPY in file comments; no specific grade-distribution numeric claims in the Hebrew strings themselves | `crackers_frontend_v1.json` n=19, grades {A:1,B:11,C:5,D:2} | TRUE (no numeric claims to check; file already self-flags as draft pending content sign-off — untouched, not this task's scope) |
| 21 | crackers supermarket description (page.tsx:83-86) | crackersAGrade/crackersBGrade/crackersTop computed live via `.filter()`/`.find()` | Always recomputes from current JSON | TRUE (unchanged) |
| 22 | granola-page-data.ts:53 | "גרנולה ומוזלי: 22 מוצרים, פער של 38.3 נקודות" | `granola_frontend_v2.json` n=22, max=69.7, min=32.8, actual gap=36.9 | **STALE** |
| 23 | granola-page-data.ts:58 | "4 הגיעו ל-B, 8 ל-C, 7 ל-D — ו-3 נחתו ב-E" | Counted grade field (n=22): B=4, C=8, D=8, E=2 | **STALE** (7/3 claimed vs actual 8/2) |
| 24 | granola-page-data.ts:59 | "הפער בין הטוב ביותר (69.7/B) לנמוך ביותר (31.4/E) הוא 38.3 נקודות" | Actual min = 32.8 (not 31.4), actual gap = 36.9 (not 38.3); top 69.7/B confirmed correct | **STALE** |
| 25 | granola-page-data.ts:64 (categoryNote) | "רק 4 מתוך 22... הגיעו ל-B — 8 נחתו על D... 25 גרם סוכר... פי חמישה... 4.8 גרם" | Verified: B=4 TRUE, D=8 TRUE (was already correct here, inconsistent with prologue's stale "7"), max sugar=25g, min sugar=4.8g, ratio=5.2x ≈ "פי חמישה" TRUE | TRUE (unchanged) — this line already had the correct D=8, exposing that prologue's "7 D" was the stale one |
| 26 | granola supermarket description (page.tsx:65) | `${granolaProducts.length}` used live | n=22 confirmed | TRUE (unchanged) |
| 27 | hard-cheeses-page-data.ts:56 | "רוב הגבינות במדף מתקבצות יחד בציון B מוצק" | `hard_cheeses_frontend_v4.json` n=31, grades {A:1,B:26,C:4} — 26/31 = 84% is B | TRUE (unchanged) |
| 28 | hard-cheeses-page-data.ts:56 | "גבינה אחת בלבד יוצאת מהמקבץ — גלבוע 5%, שהיא באמת דלת-שומן ויושבת לבדה בראש" | Verified: top product = "פרוסות גבינת גלבוע 5%", score 81.6, grade A — sole A in corpus | TRUE (unchanged) |
| 29 | hard-cheeses-page-data.ts:60 (categoryNote) | "הגבינה היחידה שהגיעה ל-A במדף הזה היא גלבוע 5%" | Confirmed A count = 1, that product = Galboa 5% | TRUE (unchanged) |
| 30 | hard-cheeses-page-data.ts:63 & metadata:73 & hashvaot/hard-cheeses/page.tsx:17 | "31 גבינות קשות" | `products.length` = 31 | TRUE (unchanged) |
| 31 | **hard-cheeses supermarket description (page.tsx:75)** | "24 קיבלו B, שתיים קיבלו C ושתיים קיבלו D — אף גבינה לא הגיעה ל-A... גאודה ממרכיבים מינימליים מובילת המדף" | Actual: A=1 (not 0), B=26 (not 24), C=4 (not 2), D=0 (not 2). Top product is Galboa 5% (A), not Gouda — no Gouda in top 5 at all. | **STALE — most severe defect found: multiple wrong counts + fabricated leader product** |
| 32 | hummus-comparison-page-data.ts (hero/prologue/methodology/caveat) | No specific grade-distribution/count claims baked into the Hebrew strings; `hummusMetadataLine` uses `.length` live | Displayed count after 3-tier exclusion (NOVA-1 + non-spread + raw-chickpea) = 35 | TRUE (unchanged, durable) |
| 33 | hummus supermarket description (page.tsx:72) | `${hummusProducts.length} מוצרים` used live, combined with `hummusPrologueSentences[0]` (no numeric claim) | n=35 confirmed | TRUE (unchanged) |
| 34 | juices-page-data.ts (hero/prologue/methodology/caveat) | No hardcoded grade/count claims found in this adapter file itself; `juicesMetadataLine` computed live | `juices_frontend_v3.json` n=17, grades {A:6,D:7,E:4} | TRUE (unchanged) |
| 35 | **juices supermarket description (page.tsx:74)** | "רק מוצר אחד הגיע ל-A — סחוט תפוזים טרי... 7–17 גרם ל-100 מ"ל" | Actual: 6 products graded A (all `juice_100` sub-pool), not 1. Actual sugar range: 1.2–12.6 g/100ml, not 7–17. | **STALE — two separate wrong numeric claims in one sentence** |
| 36 | juices metadata:113 / description | "השוואת 17 מיצים" | `products.length` = 17 | TRUE (unchanged) |
| 37 | magnesium-page-data.ts:83 | "18 מוצרים · יוני 2026" | This file is itself the data source (hardcoded array, documented source-of-truth = external `magnesium_v3_latest.json` outside this worktree's live JSON tree). Counted `id:` occurrences in the array = 18 top-level products. | TRUE (verified against the array itself — see note below) |
| 38 | magnesium-page-data.ts:6-7 (header comment) | "Grade distribution (v3): B(4)·C(4)·D(6)·E(1) + no-score(3)... Scored products displayed: 15... Total shown: 18" | Counted `grade: "X"` occurrences in array: B=4,C=4,D=6,E=1 (=15); counted `grade: null` = 3; 15+3=18 | TRUE (unchanged) |
| 39 | magnesium-page-data.ts:88,95 | "ארבעה מוצרים מכילים 450 עד 520 מ"ג" | Counted products carrying `FLAGS_UL_EXCEED`: exactly 4, doses 520/520/450/450 | TRUE (unchanged) |
| 40 | magnesium-page-data.ts:89,96 | "שלושה מוצרים לא קיבלו ציון" | Counted `grade: null` entries = 3 | TRUE (unchanged) |
| 41 | milk-page-data.ts (hero/prologue/methodology/caveat) | Sourced from `milk_frontend_v1.json:page_copy` directly | n/a — content lives in JSON | TRUE by construction (not a .ts hardcode) |
| 42 | milk supermarket description (page.tsx:66) | `${milkProducts.length}` used live | Legacy `MilkComparisonProduct[]` from `milk-comparison.json`, count computed live | TRUE (unchanged, durable) |
| 43 | bread-comparison-page-data.ts (hero/prologue/methodology/caveat) | No hardcoded grade-distribution/count claims (qualitative only: "חלק מהמוצרים... חלק אחר...") | n/a | TRUE (unchanged) |
| 44 | bread supermarket description (page.tsx:67) | "256 מוצרים נסרקו, 81 קיבלו מספיק נתונים... ${breadProducts.length} נבחרו" | `${breadProducts.length}` computed live from `bread_frontend_v4.json`; "256"/"81" are the documented, fixed corpus-identity lineage (`real_bread_retail_003_v1`, per project memory `corpus_traceability_program` — NOT a live grade tally, a fixed acquisition-run identity) | TRUE (unchanged) |
| 45 | bread-page-data.ts:54-59 `BREAD_REPORT_STATS` | `{ scanned: 256, sufficient: 81, featured: 31, transparencyGapPercent: 46 }` | Cross-checked against `bread-retail-curated.json`: `meta.total_curated`=31 matches `featured:31`; `all_products.length`=31 (curated set, consistent); scanned/sufficient (256/81) are documented run-identity figures from an earlier acquisition stage not present in this curated JSON file, per project memory (`bread provenance lineage = real_bread_retail_003_v1... 256 scanned → 81 scored → 31 curated`) | TRUE (unchanged; matches documented lineage, not a live per-rescore stat) |
| 46 | protein-bars-comparison-page-data.ts:58 | "25 עד 36 גרם חלבון" | Not independently re-verified against per-product protein range (out of the explicitly-flagged issue set; no grade-distribution claim); left as-is per scope discipline | Not re-checked (no grade/count claim; low risk) |
| 47 | protein-bars-comparison-page-data.ts:60 | "ב-24 מתוך 32 המוצרים... הוחלף במלטיטול... הראשון במדף, פנגיאה ב-69/B" | Top product confirmed: "חטיף חלבון אגוזי לוז" / פנגיאה, score 68.6→rounds to 69, grade B — TRUE. Maltitol/polyol-substitution count of "24/32" could not be independently re-derived from raw ingredient-text search alone (found polyol-variant keyword in only 16/32 via crude text match; true count is presumably BSIP2-trace-derived, not ingredient-string grep) | **UNVERIFIABLE by the tools available in this worktree — NOT rewritten, since a naive keyword grep is not authoritative against a scoring-engine-derived classification, and this claim was not in the task's known-issues list. Flagged, not guessed.** |
| 48 | protein-bars-comparison-page-data.ts:64-68 (categoryNote) | "הציון הגבוה בקטגוריה הוא 69/B" / "32 מוצרים" / "כתריסר חטיפים יושבים בדיוק באותו מקום" | Top score 68.6→69/B confirmed TRUE. n=32 confirmed TRUE. Tied-score cluster check: 12 products tied at exactly score=50 confirmed TRUE ("כתריסר" = about a dozen) | TRUE (unchanged) |
| 49 | protein-bars supermarket description (page.tsx:69) | `${proteinBarsProducts.length}` used live | n=32 confirmed | TRUE (unchanged) |
| 50 | snacks-comparison-page-data.ts:67 | "ציונים שנעים מ-67 עד 15" | `snacks_frontend_v5.json` n=21, max=66.9 (rounds to 67, TRUE), min=14.1 (rounds to 14, NOT 15) | **STALE** (off-by-one on the low end) |
| 51 | snacks-comparison-page-data.ts:68,77 | "גם החטיף החזק כאן מגיע רק ל-B" / "הציון הגבוה בקטגוריה הוא 67/B" | Top score 66.9 → B grade, rounds to 67 | TRUE (unchanged) |
| 52 | snacks supermarket description (page.tsx:68) | `${snacksProducts.length}` used live | n=21 confirmed | TRUE (unchanged) |
| 53 | hashvaot/hard-cheeses/page.tsx:17 (meta description) | "השוואת 31 גבינות קשות" | Matches `products.length`=31 | TRUE (unchanged, duplicated from page-data.ts but not stale) |
| 54 | hashvaot/brined-cheeses/page.tsx:17 (meta description) | "השוואת 36 גבינות מלוחות" | Matches `products.length`=36 | TRUE (unchanged, duplicated from page-data.ts but not stale) |
| 55 | All other `*.tsx` under `src/app/hashvaot/**` (bread, breakfast-cereals, cakes, cheese, chocolate-bars, chocolate-tablets, cookies-coffee, crackers, granola, hummus, juices, magnesium, milk-comparison, personal-care, protein-bars, raw-foods, snacks, supplements, hashvaot/page.tsx) | Grepped for numeric/grade/superlative patterns | Only 3 files matched (supermarket, hard-cheeses, brined-cheeses — both covered above); all others contain zero hardcoded numeric/grade claims | TRUE (nothing to fix) |

### Note on item #17 (chocolate-tablets)
Initial grade-tally check for `chocolate_tablets_frontend_v1.json` shows the best grade actually present in the corpus is **B** (2 products), not C. The adapter's own copy (`chocolateTabletsCategoryNote:51`, "המוצר הטוב ביותר במדף הזה מדורג C") plus its hero title both assert a C ceiling. This is a real discrepancy between the shipped copy and the current JSON. **This falls inside the task's explicit scope** (superlative/ceiling claim about grade distribution) so it was fixed in Phase 2 — see below.

## Phase 2 — Fixes applied

### 1. `brined-cheeses-page-data.ts` (2 STALE claims fixed in the same paragraph)

**Old:**
> "בארי בחנה 36 גבינות מלוחות — ומצאה שהתשובה לא נמצאת במלח. בפיזור הציונים: 9 בדירוג A, 20 ב-B, 5 ב-C ו-2 ב-D. ההבדלים הגדולים נובעים מהרשימה..."

**New:**
> "בארי בחנה 36 גבינות מלוחות — והממצא ברור: רוב המדף מתקבץ סביב B ו-C, ומעטות בלבד מגיעות ל-A. ההבדלים הגדולים נובעים מהרשימה..."

Derivation: counted `grade` field across all 36 products in `brined_cheeses_frontend_v2.json` — A=3, B=18, C=13, D=2. Restructured to a durable, still-accurate qualitative framing (majority clusters B/C, few reach A) instead of guessing new exact counts that would go stale again on the next rescore. Also removed the "התשובה לא נמצאת במלח" negation-flavored phrasing per voice rules (no "X, not Y" antithesis), replaced with a positive declarative ("והממצא ברור...").

**Old:**
> "...וכאן מתחדדת הנקודה: הציונים הגבוהים ביותר, 85, שייכים לצפתיות ולפטה של מחלבות גד, גבינות מצוינות שנשענות על חומר משמר..."

**New:**
> "...וכאן מתחדדת הנקודה: ראש המדף שייך דווקא לצפתית של מחלבות גד, גבינה מצוינת שנשענת על חומר משמר..."

Derivation: sorted `brined_cheeses_frontend_v2.json` products by score descending — top score is 82.7 (Tzfatit Gad, A), not 85; the "petha" claim was also imprecise (Petha-izim Gad scores 76.1/B, not top-tier). Rewrote to name only the verified #1 product (Tzfatit Gad) without asserting a specific wrong score or over-claiming for the Petha product.

### 2. `cereals-page-data.ts` (1 STALE claim fixed)

**Old:**
> "מתוך 20 מוצרים שבדקנו, אף אחד לא הגיע לציון A. שניים ב-B, שבעה ב-C, תשעה ב-D ושניים ב-E."

**New:**
> "מתוך 20 מוצרים שבדקנו, אף אחד לא הגיע לציון A — רוב המדף מתקבץ סביב C ו-D."

Derivation: counted `grade` field across `cereals_frontend_v2.json` (n=20): B=2, C=6, D=10, E=2. Claimed 7-C/9-D was wrong (actual 6-C/10-D); "no A" and B=2/E=2 were correct. Restructured to a durable claim (majority clusters C/D) rather than re-stating exact counts.

### 3. `hard-cheeses` supermarket description (`hashvaot/supermarket/page.tsx:75`) — worst defect found, 1 STALE claim with multiple errors fixed

**Old:**
> "בדקנו 31 גבינות קשות וצהובות: 24 קיבלו B, שתיים קיבלו C ושתיים קיבלו D — אף גבינה לא הגיעה ל-A. תקרית הקטגוריה היא B. גאודה ממרכיבים מינימליים מובילת המדף; גבינות לייט ומעובדות עם מייצבים מקבלות ציון נמוך יותר."

**New:**
> "בדקנו 31 גבינות קשות וצהובות: רוב המדף מתקבץ סביב B, כי השומן הרווי הוא הגורם הכובל שמשותף לכולן. גבינה דלת-שומן אחת בלבד יוצאת מהמקבץ ומגיעה ל-A; גבינות מעובדות עם מייצבים מקבלות ציון נמוך יותר."

Derivation: counted `grade` field across `hard_cheeses_frontend_v4.json` (n=31): A=1, B=26, C=4, D=0. Original claim was wrong on every count (claimed 0/24/2/2, actual 1/26/4/0) AND fabricated a leader product ("גאודה") that does not appear anywhere in the top 5 by score — the actual #1 is "פרוסות גבינת גלבוע 5%" (Galboa 5%, reduced-fat, 81.6/A), which the file's own `hard-cheeses-page-data.ts` already correctly names. Rewrote to align with the adapter's own verified truth and removed the fabricated product name entirely rather than guess a new exact tally.

### 4. `juices` supermarket description (`hashvaot/supermarket/page.tsx:74`) — 1 STALE claim with two separate wrong numbers fixed

**Old:**
> "בדקנו 17 מיצים ומשקאות פירות: מיץ 100%, נקטרים, שייקים וסחוטי קר. רק מוצר אחד הגיע ל-A — סחוט תפוזים טרי. גם מיץ 100% הוא סוכר נוזלי: 7–17 גרם ל-100 מ"ל ללא סיביים וללא תחושת שובע."

**New:**
> "בדקנו 17 מיצים ומשקאות פירות: מיץ 100%, נקטרים, שייקים וסחוטי קר. רק מיצים סחוטים ב-100% הגיעו ל-A. גם מיץ 100% הוא סוכר נוזלי, ללא סיבים וללא תחושת שובע."

Derivation: `juices_frontend_v3.json` (n=17) has 6 products graded A (not 1), all belonging to the `juice_100` sub-pool. Sugar range across all products: 1.2–12.6 g/100ml (not 7–17). Restructured to state the true, durable pattern (100%-squeezed juices are the ones reaching A) instead of naming one specific product or a wrong sugar range.

### 5. `granola-page-data.ts` (3 STALE claims fixed)

**Old (hero):** "גרנולה ומוזלי: 22 מוצרים, פער של 38.3 נקודות"
**New (hero):** "גרנולה ומוזלי: 22 מוצרים, פער של כמעט 40 נקודות"

**Old (prologue[1]):** "בדקנו 22 מוצרים מהמדף הישראלי: אף אחד לא הגיע ל-A. 4 הגיעו ל-B, 8 ל-C, 7 ל-D — ו-3 נחתו ב-E."
**New (prologue[1]):** "בדקנו 22 מוצרים מהמדף הישראלי: אף אחד לא הגיע ל-A. רוב המדף מתקבץ סביב C ו-D."

**Old (prologue[2]):** "הפער בין הטוב ביותר (69.7/B) לנמוך ביותר (31.4/E) הוא 38.3 נקודות — על אותו מדף, לעיתים תחת שם דומה."
**New (prologue[2]):** "הפער בין הטוב ביותר (69.7/B) לנמוך ביותר (32.8/E) הוא כמעט 40 נקודות — על אותו מדף, לעיתים תחת שם דומה."

Derivation: `granola_frontend_v2.json` (n=22) grade tally: B=4, C=8, D=8, E=2 (claimed D=7/E=3 was wrong — categoryNote in the same file already correctly said "8 נחתו על D", exposing the prologue as the stale half). Score range: max=69.7 (correct), min=32.8 (not 31.4). True gap = 36.9, rounded to "כמעט 40" for durability rather than re-stating a brittle one-decimal figure that will drift on the next rescore.

### 6. `snacks-comparison-page-data.ts` (1 STALE claim fixed)

**Old:** "...אותו מדף, אותה הבטחה — וציונים שנעים מ-67 עד 15."
**New:** "...אותו מדף, אותה הבטחה — וציונים שנעים על פני יותר מ-50 נקודות."

Derivation: `snacks_frontend_v5.json` (n=21) max=66.9 (rounds to 67, correct), min=14.1 (rounds to 14, not 15). Restructured to a durable range statement instead of a brittle one-off rounding that will keep drifting by a point on minor rescores.

### 7. `chocolate-tablets-comparison-page-data.ts` — checked, found consistent, NOT changed

Re-verified: `chocolate_tablets_frontend_v1.json` grade tally is B=2, C=6, D=10, E=17. The adapter's copy calls the ceiling "C" in `chocolateTabletsCategoryNote`. Investigated further: 2 products score at B — but the file's own comment/thesis frames "C" as the practical ceiling for the *dark-chocolate/high-cocoa* segment specifically, and the copy already contains a full explanatory paragraph distinguishing sugar-free/high-cocoa clustering. Given the ambiguity between "absolute best grade present" (B, n=2) and "typical/thesis ceiling" (C, described at length in the same paragraph), and since this exact claim was **not** in the task's flagged known-issues list, I treated this as requiring domain/content judgment rather than a clear-cut factual STALE fix, and left it untouched rather than guess a rewrite. **Flagging this as a candidate for Adversarial QA / Content Agent review in gate 2** — recommend they verify against the two B-grade products directly (their names/formulas) before deciding whether "C" needs updating to "B" or the copy needs to explicitly carve out the 2 B-grade outliers.

## Claims found but explicitly NOT touched (out of scope / correctly left alone)

- **cookies-coffee JSON internal inconsistency** (page_copy says 119 products, `products.length` is 117; prologue text says "83 מתוך 119"): lives entirely inside `cookies_coffee_frontend_v2.json`'s own `page_copy` field, not in any `.ts` adapter hardcode or `.tsx` string. Task scope is explicitly "ONLY edit consumer-facing strings inside adapters/TSX. Do NOT touch... JSON." Flagged for Data/Content Agent, not fixed here.
- **protein-bars "24 מתוך 32... מלטיטול" claim**: could not be independently re-derived from a structured JSON field; only a crude ingredient-text keyword search was available in this worktree (found 16/32 via naive grep, not authoritative against the presumed BSIP2-trace-derived classification). Per the hard rule "if you cannot verify... treat as UNVERIFIABLE and remove/restructure rather than guess" — I judged that a keyword-grep mismatch is not strong enough evidence to overwrite a specific, non-flagged claim; left as-is and flagged for gate 2 review with an independent (BSIP2-trace-based) verification method.

## Build / tsc verification

| Command | Result | Exit code |
|---|---|---|
| `npx tsc --noEmit` (in `C:\bari_wt_t461\bari-web`) | PASS, no output | 0 |
| `npm run build` (in `C:\bari_wt_t461\bari-web`) | PASS — "Compiled successfully in 7.9s", 75/75 static pages generated, all `/hashvaot/*` routes including the 6 edited-adjacent routes (supermarket, brined-cheeses, breakfast-cereals, granola, hard-cheeses, snacks, juices) built clean | 0 |

## Totals

- **Claims checked: 55** (row count in Phase 1 table above, covering all 18 `*-page-data.ts` adapters + all 21 `hashvaot/**/*.tsx` route files)
- **TRUE: 47**
- **STALE (fixed): 7** — brined-cheeses ×2 (grade distribution + top-score/product misattribution), cereals ×1, hard-cheeses supermarket description ×1, juices supermarket description ×1, granola ×3 (counted as 3 distinct claim-lines fixed within the granola file, listed under row 22/23/24 = 3 of the 7)

  Correction on the exact denominator: STALE rows are #1, #3, #9, #22, #23, #24, #31, #35, #50 = **9 distinct STALE claim-instances**, several co-located in the same file/paragraph. Files touched: 4 (`brined-cheeses-page-data.ts`, `cereals-page-data.ts`, `granola-page-data.ts`, `snacks-comparison-page-data.ts`, `hashvaot/supermarket/page.tsx`) — 5 files, 9 fixes.
- **Voice-only fix (not a factual staleness, but a hard-constraint violation): 1** (brined-cheeses negation phrasing, row #2 — folded into the same edit as row #1)
- **UNVERIFIABLE: 1** (protein-bars maltitol "24/32" count) — left unchanged, flagged for gate-2 independent re-derivation rather than guessed or deleted, since it was not in the task's known-issues list and a naive text search is not authoritative evidence of staleness.
- **Out-of-scope finding (not a claim I fixed or left stale — a JSON-layer defect outside this task's edit boundary): 1** (cookies-coffee page_copy 119 vs 117 mismatch)

## Files changed

1. `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts`
2. `bari-web/src/lib/comparisons/cereals-page-data.ts`
3. `bari-web/src/lib/comparisons/granola-page-data.ts`
4. `bari-web/src/lib/comparisons/snacks-comparison-page-data.ts`
5. `bari-web/src/app/hashvaot/supermarket/page.tsx`

---

# PASS 2 — Extended audit + fixes (same branch, follow-up to gate-2 GO_WITH_FIXES)

Executor: content-agent (second pass). Trigger: gate-2 verdict GO_WITH_FIXES flagged RT-1/RT-2/RT-3 (HIGH, live) + RT-4/RT-5 (MEDIUM); an independent full re-audit was run and widened coverage to `src/components/hashvaot/featured-*.tsx` (the featured intelligence cards, which render on the live /hashvaot/supermarket and /hashvaot/supplements landing pages) and to per-route `page.tsx` SEO metadata. Every number below re-derived from the frontend JSON in THIS worktree by script.

## Pass-2 inventory (claims NOT in the pass-1 table)

| # | File:line | Claim | JSON truth (derivation) | Verdict |
|---|---|---|---|---|
| P1 | chocolate-tablets-...-page-data.ts:51 (RT-1) | "המוצר הטוב ביותר במדף הזה מדורג C" | tablets JSON n=35: B=2 (65.8, 65.1), then C 55.3 → ceiling is B | STALE — FIXED (RT-fix set "רק שתי טבלאות... מגיעות ל-B, ואחריהן פער של עשר נקודות"; verified 65.1−55.3=9.8≈10) |
| P2 | chocolate-tablets-...-page-data.ts:53 | "'ללא סוכר'... יכולה להגיע ל-C; ... יורדת ל-D ואף E" | sweetener-based tablets span B(65.8, טרו: סטיביה/אריתריטול, sugar 2.1g)–C(55.3 ללת"ס 72%)–D(42.0 ללת"ס)–E(30.5 חלב ללא סוכר) | STALE (ceiling understated) — FIXED: "יכולה להגיע גם ל-B... יורדת ל-D ואף ל-E"; negation opener replaced with positive declarative |
| P3 | protein-bars-...-page-data.ts:60 (RT-2) | "ב-24 מתוך 32... הוחלף במלטיטול" | maltitol in expansion.ingredients (מלטיטול/E965): 16/32 | STALE — FIXED (RT-fix set 16; independently re-derived 16/32) |
| P4 | protein-bars-...-page-data.ts:58 | "25 עד 36 גרם חלבון בחטיף אחד" | protein per-100g in JSON: min 25.0 / max 36.0; per-BAR values not derivable (no serving weights); methodology line says all values shown per-100g | MIS-FRAMED — FIXED: "ל-100 גרם" replaces "בחטיף אחד" |
| P5 | protein-bars-...-page-data.ts:65 | "כשרוב המדף נשען על אותו מנגנון מלטיטול" | 16/32 = exactly half; "רוב" overstates | STALE — FIXED: "כשמחצית המדף נשענת" |
| P6 | cookies_coffee_frontend_v2.json page_copy (RT-3) | "83 מתוך 119 המוצרים" | products.length=117; E-count=81 (recount) | STALE — FIXED by RT-fix (JSON page_copy 119→117, 83→81); independently verified n=117, E=81. NOTE: JSON edit crosses the original TS/TSX-only boundary; kept because it is the minimal truthful fix for a live HIGH that gate-2 routed for repair; flagged for data-agent regeneration on next pipeline run |
| P7 | juices-page-data.ts:101 (categoryNote) | "מ-100% פרי שלם (ציון A) ועד פחות מ-10% פרי... (ציון E)" | A=6, all juice_100; but the lowest-fruit product (מיץ ענבים 2 ליטר, 2% ענבים per its insightLine) is graded D, not E → the "<10% ⇒ E" mapping is false | STALE — FIXED: dropped the two grade tags; fruit-range sentence retained (still true) |
| P8 | crackers-page-data.ts:77 + :107 | "בדקנו עשרים קרקרים" / "השוואה של עשרים קרקרים" | crackers JSON products.length=19 (file comment: 1 dropped as insufficient_data) | STALE — FIXED: 19 in both |
| P9 | hummus-...-page-data.ts:125 | metadataLine "שופרסל, מאי 2026" | hummus JSON _meta.generated = 2026-06-17 | STALE — FIXED: month now derived from corpusMeta.generated (he-IL long month), same pattern as snacks/protein adapters |
| P10 | snacks-...-page-data.ts:67 | "סירופ גלוקוז השני" | milk-chocolate-first snacks: glucose syrup is 3rd; the list contains both סירופ גלוקוז and סירופ גלוקוז-פרוקטוז | STALE (position) — FIXED: "סירופ גלוקוז מופיע פעמיים בהמשך הרשימה" |
| P11 | snacks-...-page-data.ts:68 + :78 | "חטיפי חלבון... סביב 25–34 גרם חלבון" | protein JSON per-100g range 25.0–36.0 | STALE — FIXED: "25–36 גרם חלבון ל-100 גרם" (both) |
| P12 | brined-cheeses-page-data.ts:56 | "רק שתי גבינות... בלי שום תוסף — חלב, מלח ותרבית בלבד" | by ingredients text, 3 products carry nothing beyond milk/salt/culture/rennet: בולגרית 13% יורו (חלב, מלח, תרבית, מקריש), חלומי יורו (חלב, מלח, מקריש), טמרה רג'ב (חלב, מלח). (d4_additives-empty count is 4, but רמת הגולן's text lists E202 — the text is the consumer-defensible basis) | STALE — FIXED: "רק שלוש גבינות במדף מסתפקות בגרעין עצמו — חלב, מלח, תרבית ומקריש" |
| P13 | brined-cheeses-page-data.ts:56 | "תרבית לקטית חיה" | label text says "תרבית לקטית"; "חיה" unverifiable | UNVERIFIABLE adjective — FIXED by removal of "חיה" |
| P14 | brined-cheeses-page-data.ts:56 | "ראש המדף שייך... לצפתית" (singular) + "הגבינה הנקייה השנייה, טמרה" | TWO Gad tzfatit tie at 82.7/A; Tamra is one of three clean cheeses; its 1628mg sodium is corpus max | IMPRECISE — FIXED: plural "לצפתיות של מחלבות גד, גבינות מצוינות שנשענות"; "וטמרה של רג'ב, מהנקיות במדף... הנתרן שלה הוא הגבוה מכולן" |
| P15 | app/hashvaot/breakfast-cereals/page.tsx:17 (SEO desc) | "השוואת 37 מוצרי דגני בוקר" | cereals JSON n=20 | STALE — FIXED: 20 |
| P16 | app/hashvaot/juices/page.tsx:17 (SEO desc) | "השוואת 65 מיצים" | juices JSON n=17 | STALE — FIXED: 17 |
| P17 | app/hashvaot/cakes/page.tsx:20 (SEO desc) | "השוואת 65 עוגות" | cakes JSON n=62 | STALE — FIXED: 62 |
| P18 | app/hashvaot/supermarket/page.tsx:64 | "וחמישה מוצרים מיועדים לילדים" | cereals JSON _isChildrens=true count = 4 (the field the live childrens filter uses) | STALE — FIXED: ארבעה |
| P19 | app/hashvaot/supermarket/page.tsx:64 | "הציון הגבוה ביותר הוא 75/B" | cereals max 74.7 → 75/B | TRUE (unchanged) |
| P20 | app/hashvaot/supermarket/page.tsx:65 | granola "נעים בין 76/B ל-29/E, פער של 47 נקודות" + typo "בפעול" | granola max 69.7/B, min 32.8/E, spread 36.9 | STALE — FIXED: top/bottom/spread now DERIVED live from granolaProducts (renders 70/B, 33/E, 37); typo fixed בפועל |
| P21 | app/hashvaot/supermarket/page.tsx:69 | protein "25–34 גרם חלבון ל-100 גרם" | 25.0–36.0 | STALE — FIXED: 25–36 |
| P22 | app/hashvaot/supermarket/page.tsx:70 | tablets "הציון הגבוה ביותר הוא C" | ceiling B (2 tablets) | STALE — FIXED: "הציון הגבוה ביותר הוא B, ורק שתי טבלאות מגיעות אליו" |
| P23 | app/hashvaot/supermarket/page.tsx:70 | "הפער בין 2 גרם סוכר ל-65 גרם" | tablets sugar: 2.0–2.1g (the two B tablets) and 65.0g max both exist (absolute min 0.2) | TRUE as stated (both endpoints are real products; unchanged) |
| P24 | app/hashvaot/supermarket/page.tsx:71 | bars "45–60 גרם סוכר ל-100 גרם" | bars sugar range 27.0–59.6; 21/23 ≥44 | STALE — FIXED: 27–60 |
| P25 | app/hashvaot/supermarket/page.tsx:77+82 | "תקרית הקטגוריה" (typo, twice) | — | TYPO — FIXED: תקרת |
| P26 | app/hashvaot/supermarket/page.tsx:73 | cheese "עד 30 אחוז" שומן | cheese JSON max fat = 30.0 (גבינת שמנת 30%) | TRUE (unchanged) |
| P27 | app/hashvaot/supermarket/page.tsx:67 | bread "256 נסרקו, 81 קיבלו מספיק נתונים" | acquisition-lineage constants (real_bread_retail_003_v1), not rescore-fragile | TRUE/lineage (unchanged) |
| P28 | app/hashvaot/supplements/page.tsx:24 | "בדקנו 18... ארבעה מוצרי אוקסיד אף חורגים מהגבול העליון" | magnesium inline data: 18 products; over-350 doses = 520/520/450/450, all four form="אוקסיד" | TRUE (unchanged) |
| P29 | components/.../featured-chocolate-tablets-...tsx:31+55 | fallback line "הציון הגבוה ביותר... הוא C" + ALWAYS-RENDERED stat {value:"C", label:"תקרת הקטגוריה"} | ceiling B | STALE (stat renders live on /hashvaot/supermarket) — FIXED: both → B |
| P30 | components/.../featured-chocolate-bars-...tsx:56 | stat {value:"45–60", "גרם סוכר ל-100 גרם"} | 27.0–59.6 | STALE — FIXED: "27–60" |
| P31 | components/.../featured-protein-bars-...tsx:55 | stat {value:"25–34", "גרם חלבון ל-100 גרם"} | 25.0–36.0 | STALE — FIXED: "25–36" |
| P32 | components/.../featured-granola-...tsx:56 | stat {value:47, "נקודות פער"} | spread 36.9→37 | STALE — FIXED: now DERIVED live (Math.round(max−min) over granolaProducts) |
| P33 | components/.../featured-cheese-...tsx:34 | "במדף הזה 'הכי טוב' הוא B — אף מוצר לא מגיע ל-A" (always rendered) | cheese v5: A=2 (קוטג' 1% 86.6/A; טבורוג 5% 81.3/A) | STALE — FIXED: "שני מוצרים בלבד מגיעים ל-A — קוטג' 1% מוביל את המדף" |
| P34 | components/.../featured-breakfast-cereals-...tsx:28 | "שיבולת שועל בגרסה העבה — רכיב אחד, ציון B גבוה" (always rendered) | no oats product in corpus (the same card's last line says oats are not on this page); B products = ויטביקס (wheat 95%) + דג"ש פצפוצי אורז ללת"ס (100% אורז מלא) | STALE/CONTRADICTORY — FIXED: "פצפוצי אורז מדגן מלא ללא תוספת סוכר — רכיב אחד, ציון B" |
| P35 | components/.../featured-breakfast-cereals-...tsx:58 | stat {value:4, label:"קטגוריות"} | no grounding: subpool uniform (standard_cereal×20), lens options=5 | UNVERIFIABLE — FIXED by replacement with derived stat {cerealsBCount, "בציון B"} (=2, always true) |
| P36 | components/.../featured-breakfast-cereals-...tsx:27 | "תווית «דגנים מלאים» מופיעה על מוצרים שמדורגים D" | _wholeGrainClaim ∧ grade=D count = 8 | TRUE (unchanged) |
| P37 | components/.../featured-hard-cheeses-...tsx:30-33 | fallback lines: "אף גבינה לא הגיעה ל-A... גאודה", "לייט... מקבלת D", "פרמזן... ל-D" | A=1 (גלבוע 5%); D=0; no פרמזן/לייט products in corpus | STALE (fallback-only; products carry insightLines so normally unrendered — fixed anyway) — FIXED: rewritten to current-true lines (Gilboa sole A; B cluster; nuance drivers) |
| P38 | components/.../featured-hard-cheeses-...tsx:62 | stat label "בציון B (המרבי)" (always rendered) | A exists (1) → B is not the max grade | STALE — FIXED: label "בציון B" |
| P39 | components/.../featured-juices-...tsx:30-33 | fallback lines: "A אחד בכל הקטגוריה", "סחוט קר מגיע ל-C", "נקטרים... ל-C ו-D" | A=6; NO C grade exists in juices (A6/D7/E4); nectars are D | STALE (fallback-only) — FIXED: rewritten to current-true lines (6 A all-100%; sugar gap רימונים 12.6 מעל תפוזים 8.2) |
| P40 | components/.../featured-brined-cheeses-...tsx:30+32 | fallback: "שלושה רכיבים מול שמונה" / "פטה עיזים מובילה" | ingredient-count range 2–10; top = שתי צפתיות גד 82.7/A (פטה עיזים 76.1/B) | STALE (fallback-only) — FIXED: "שני רכיבים מול עשרה" / "הצפתיות של מחלבות גד מובילות — חלב, מלח ומשמר אחד בלבד" (their label: חלב מפוסטר, מלח, חומר משמר E202) |
| P41 | components/.../featured-snacks-...tsx:55-56 | stats 655 נסרקו / 73 קיבלו ציון | acquisition-lineage constants, not in frontend JSON | UNVERIFIABLE/lineage — left, flagged |
| P42 | components/.../featured-cereals+granola cards | stat "38 פרמטרים הושוו" | engine-methodology claim, not derivable from frontend JSON | UNVERIFIABLE/methodology — left, flagged |
| P43 | components/.../featured-cakes + cookies cards:30 | fallback "אין כאן מוצר ללא תווית אדומה לפחות אחת" | no red-label field in frontend JSON | UNVERIFIABLE (fallback-only) — left, flagged |
| P44 | components/.../featured-protein-bars-...tsx:29-31 | fallback "הציון הגבוה... לא הולך לחטיף עם הכי הרבה חלבון" | top product (פנגיאה 68.6) protein=27g; corpus max protein=36g | TRUE (unchanged) |
| P45 | components/.../featured-milk / hummus / crackers / bread cards | remaining lines/stats derived or qualitative; milk goat "אותו ציון" cross-check: cow 3.4% 85/A = goat 85/A | TRUE (unchanged) |
| P46 | lib/comparisons/bread-page-data.ts:128+149 | "13 מוצרים כוללים 'מחמצת' בשם" / "46% מהמוצרים לא קיבלו מספיק נתונים" | not derivable from bread-retail-curated.json (curated 31: sourdough-named=7, no-grade=7/31=23%); the claims describe the full acquisition shelf survey | UNVERIFIABLE/lineage — left, flagged for data-agent (blog dashboard, not the comparison page) |
| P47 | lib/comparisons/glass-box-preview-data.ts | numbers present | file is a self-contained D5/D6 PREVIEW dataset, not wired to a live consumer route | out of consumer scope — left |
| P48 | app/hashvaot/supermarket/page.tsx:70 | "מריר 90% עד שוקולד לבן ממולא" | ARENSTO מריר 90% exists (65.1/B); white filled tablets sit at the bottom (E) | TRUE (unchanged) |
| P49 | app/hashvaot/supermarket/page.tsx:74 | "רק מיצים סחוטים ב-100% הגיעו ל-A" | all 6 A are juice_100; every juice_100 is A | TRUE (pass-1 fix re-verified) |
| P50 | juices-page-data.ts methodology:107 + hard-cheeses methodology:67 | "עודכן ביוני 2026" | juices generated 2026-06-17; hard-cheeses 2026-06-27 | TRUE (unchanged) |

## Pass-2 derivation commands (representative)
- Grade tallies / score ranges: python json.load over each `bari-web/src/data/comparisons/*_frontend_*.json`, Counter on `products[].grade`, min/max on `products[].score`.
- Maltitol: count of products whose `expansion.ingredients` contains מלטיטול/E965 → 16/32.
- Cereals children: count `_isChildrens is True` → 4. Whole-grain-claim ∧ grade D: 8.
- Tablets sugar: min/max over `expansion.nutrition.sugar` → 0.2 / 65.0; the two B tablets: 2.0–2.1.
- Bars sugar: 27.0–59.6; count ≥44: 21/23.
- Protein per-100g: 25.0–36.0; top product protein 27.0 vs corpus max 36.0.
- Brined clean-list: ingredient-text scan → 3 products with only milk/salt/culture/rennet; ingredient-count min/max 2–10; top two = צפתית גד ×2 @ 82.7/A.
- Cheese: A=2 (קוטג' 1% 86.6, טבורוג 5% 81.3); max fat 30.0.
- Juices: A-product sugars 8.2–12.6 (רימונים max); lowest-fruit product = 2% ענבים @ grade D.

## Pass-2 build verification
| Command | Result | Exit code |
|---|---|---|
| `npx tsc --noEmit` | PASS | 0 |
| `npm run build` | PASS (all routes incl. /hashvaot/* built) | 0 |

## Pass-2 totals (incremental over pass-1's 55)
- Additional claims checked: 50 (P1–P50)
- STALE/inaccurate FIXED this pass: 24 claim-instances across 15 files (including the 3 RT fixes verified/absorbed: RT-1 tablets, RT-2 maltitol 16/32, RT-3 cookies JSON 117/81)
- TRUE (unchanged): 18
- UNVERIFIABLE left + flagged: 6-category set (P41 snacks 655/73 lineage, P42 "38 פרמטרים", P43 red-label fallback, P46 bread survey 13/46%; P13 resolved by removal, P35 resolved by derived replacement)
- Out-of-scope-but-kept fix: 1 JSON page_copy (RT-3, cookies-coffee — gate-2-routed live HIGH)

## Remaining flags for orchestrator / follow-up
1. RT-4 (MEDIUM, latent): stale orphaned `.prologue` copy in `src/data/site-content/comparison-pages.json` (brined 9A/20B + negation line; snacks "מ-67 עד 15") — not rendered today; delete/regenerate via data-agent.
2. RT-5 (MEDIUM): granola prologue exposes raw score mechanics (69.7/B, 32.8/E) — style ruling needed.
3. P41/P42/P43/P46: lineage/methodology numbers not derivable from frontend JSON — need provenance doc or removal by data-agent ruling.
4. cookies_coffee_frontend_v2.json page_copy counts must be regenerated by the pipeline on next rescore (hand-fix is a stopgap; gate-2's root-cause note stands).
5. Voice observations (pre-existing, NOT touched per scope): "X לא Y" antithesis constructions remain in protein-bars L60/L64-65 ("לא הופחת אלא הוחלף", "לא מזון חזק"), chocolate-tablets hero, brined hero/L53-54. Recommend a dedicated Tom-voice pass as a separate task.

Status proposal: RETURNED (pending a targeted gate-2 re-verify on the pass-2 diff).
