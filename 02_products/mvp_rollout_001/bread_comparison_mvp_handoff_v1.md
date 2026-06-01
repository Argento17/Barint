# Bread Comparison — MVP Handoff v1
**Date:** 2026-05-30
**Route:** `/hashvaot/bread`
**Status:** 🟡 LIVE but old format — needs component swap + rescore

---

## A. Category Status

| Dimension | Status |
|---|---|
| Data | ✓ 24 products in `src/data/comparisons/bread_frontend_v2.json` |
| Scoring | 🟡 BSIP2-derived; recalibration + re-run needed |
| Explanations | ✓ All 24 products have BariExpansionVM fields |
| Images | ✓ Shufersal Cloudinary URLs |
| Component | ✗ `BreadComparisonPage` → old `ComparisonShelfPage` format |
| Route | ✓ `/hashvaot/bread` (active, old format) |
| MVP readiness | 🟡 Needs component swap + rescore |

---

## B. Data Structure

**File:** `src/data/comparisons/bread_frontend_v2.json`  
**Schema:** BariProductVM (canonical) with `_website_cluster` internal field  
**Loaded via:** `src/lib/comparisons/bread-comparison-page-data.ts`  
**Products:** 24

**Score distribution (current):**
- A (≥80): 2 products (scores 82: "לחם טחינה פרוס", "קרקר כוסמין מלא")
- B (65–79): 19 products (scores 66–80)
- C (50–64): 3 products (scores 59, 60, 61)

**Grade inconsistency to fix:**
- "לחם ירוק מקמח מלא": `score: 80, grade: "B"` — incorrect. Score 80 ≥ 80 = grade A.
- "לחם שיפון מלא מסטמכר": `score: 76, grade: "B"` — correct.
- Audit all products: verify `grade = score_to_grade(score)` for each.

**Cluster map (from `_website_cluster`):**
- `everyday` — 6 products (standard white/mixed breads)
- `fermentation` — 6 products (sourdough and standard yeast comparison)
- `strong` — 7 products (whole grain, high fiber)
- `wellness_ambig` — 3 products (claims don't fully match composition)
- `crackers` — 4 products

**Known data gaps:**
- `energyKcal`, `sugar`, `fat` are null on all products (partial scrape)
- `protein` and `fiber` present on most products ✓
- `sodium` present on most products ✓
- Ingredients present on ~8 of 24 products (from bread-retail-003 run)
- Nulls acceptable for MVP

---

## C. Required Component Work

**The bread route currently uses:**
```tsx
// app/hashvaot/bread/page.tsx
import { BreadComparisonPage } from "@/components/comparisons/bread-comparison-page";
// BreadComparisonPage wraps ComparisonShelfPage (OLD format)
```

**Required:** Create `BreadComparisonDesktopPage` following the exact `SnacksComparisonDesktopPage` pattern.

**Reference:** `src/components/comparisons/snacks-comparison-desktop-page.tsx`

**Differences from snacks:**
1. Filters: use `BREAD_SHELF_LENS_OPTIONS` and `filterBreadProducts` (both already exist in `bread-shelf-filters.ts`)
2. Hero eyebrow/title: bread-specific Hebrew
3. Prologue sentences: bread-specific
4. The expansion panel structure is identical (BariExpansionVM)
5. No segment field in bread products (snacks had `segment`, bread does not)

**Files to create:**
- `src/components/comparisons/bread-comparison-desktop-page.tsx`

**Files to update:**
- `src/app/hashvaot/bread/page.tsx` — swap import and component
- `src/lib/comparisons/bread-comparison-page-data.ts` — ensure it exports `breadHero`, `breadMetadataLine`, `breadPrologueSentences`, `breadMethodologyLines`, `breadProducts` (check existing exports are complete)

---

## D. Scoring Guidance (Post-Recalibration)

Apply R-01, R-02, R-03, then re-run BSIP2 on bread corpus.

**Expected grade changes after recalibration:**

| Product | Current | Expected | Driver |
|---|---|---|---|
| לחם מחמצת קמח מלא | 77/B | 83/A | R-02 fermentation +6 |
| לחם שיפון קל | 75/B | 81/A | R-02 fermentation +6 |
| לחם מחמצת גרעינים | 76/B | 82/A | R-02 fermentation +6 |
| לחם שיפון מלא מסטמכר | 76/B | 79–82/B–A | R-03 fiber gain |
| קרקר כוסמין מלא ושומשום | 82/A | 84–86/A | R-01 cap relief + R-03 |
| קרקר כוסמין אורגני | 78/B | 81–83/A | R-01 cap relief + R-03 |
| לחם ירוק מקמח מלא | 80/A* | 82–84/A | R-03 fiber + fix grade |
| לחם דגנים מלא | 75/B | 77–79/B | R-03 fiber gain |
| לחם אחיד פרוס קל | 73/B | 73–74/B | No fermentation, low fiber gain |
| לחם כוסמין לבן | 68/B | 69/B | Small R-03 gain |

*Grade inconsistency — should already be A.

**Products that should NOT change significantly:**
- Low-C products (59–61): "לחם מחמצת אגוזים צימוקים", "קרם קרקר", "לחם מחמצת שיפון+אגוזים"
- These are correctly positioned — weak on composition or data

**After recalibration, expected distribution:**
- A (≥80): ~8 products (was 2)
- B (65–79): ~13 products (was 19)
- C (50–64): ~3 products (was 3)

---

## E. Explanation Guidance

Bread explanations are in BariExpansionVM format. Current quality is adequate for MVP.

**What explanations must say:**
- Whether fermentation is verified in ingredients vs. just in the name
- Fiber level with specific gram value
- Grain type (whole wheat, rye, spelt, etc.)
- Honest caveat when ingredient data is limited ("נתונים חלקיים — הניתוח מבוסס על ערכים תזונתיים זמינים")

**Bread-specific insight patterns:**
- "מחמצת ברכיבים, לא רק בשם" — high value signal
- "מחמצת בשם, שמרים ברכיבים" — important contradiction to surface
- Fiber source disclosure: "הסיבים כאן מגיעים מ[טחינה/שומשום/עם]" when not from grain

**Phrases to avoid:**
- "NOVA", "NOVA3"
- "עיבוד מינימלי" without evidence
- "ממד", "BSIP", "גורם הגנה"

**Post-rescore updates needed:**
- `insightLine` fields with score references → update to new scores
- `bottomLine` fields with explicit scores → update
- Sort order → re-sort by new score

---

## F. Methodology Disclosure

Use these lines:

```
ניתוח לחמים מבוסס על נתונים מגלויות שופרסל — מדגם מדף, לא סקר שוק מלא.
לכל מוצר נבחנו הרכב הרכיבים, ערכי חלבון וסיבים, רמת עיבוד ותסיסה מאומתת ברכיבים.
ציון הלחם אינו מבוסס על קלוריות בלבד — הוא משקלל מבנה, מקור הדגן, ורמת ההנדסה במוצר.
ההשוואה נועדה לעזור בהשוואה בין מוצרים, ולא מהווה המלצה תזונתית אישית.
```

Add scope note: "מדגם מדף שופרסל בלבד"

---

## G. Hero & Prologue Content

**Eyebrow:** `מנוע השוואה · לחמים`  
**Title:** `לחם: מה שכתוב על האריזה לא תמיד מה שבפנים`  
**Metadata line:** `[N] מוצרים נבדקו · מדגם שופרסל · ממוין לפי ציון Bari`

**Prologue sentences (3):**
1. "לחם נראה כמו קטגוריה פשוטה: קמח, מים, מחמצת. אבל המדף מספר סיפור יותר מורכב."
2. "חלק מהמוצרים שמציגים 'מחמצת' בשם משתמשים בשמרים תעשייתיים ברכיבים. חלק אחר מסתמכים על כותרת 'מלא' כדי להציג רכיבים מעורבים."
3. "ההשוואה מתבססת על מה שאפשר לבדוק: ערכי חלבון, סיבים, נתרן, ותסיסה מאומתת ברשימת הרכיבים — לא על המיתוג."

---

## H. Launch Readiness

**Status: 🟡 Needs component swap + rescore**

**Tasks:**
1. Create `bread-comparison-desktop-page.tsx` (copy snacks pattern, swap filters)
2. Update `bread/page.tsx` to use new component
3. Apply R-01/R-02/R-03 in BSIP2 engine
4. Re-run BSIP2 on bread corpus
5. Update `bread_frontend_v2.json` (scores, grades, text references)
6. Fix grade inconsistency ("לחם ירוק": 80 must be A)
7. QA: verify filters work, expansion opens, mobile preserved

Estimated time: 4–6 hours.
