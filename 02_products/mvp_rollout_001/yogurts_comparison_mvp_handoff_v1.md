# Yogurts Comparison — MVP Handoff v1
**Date:** 2026-05-30
**Route:** `/hashvaot/yogurts` (does not exist)
**Status:** 🔴 NOT READY — create data, build component, register route

---

## A. Category Status

| Dimension | Status |
|---|---|
| Data | ✗ No file exists |
| Scoring | ✗ No BSIP2 run |
| Explanations | ✗ None written |
| Images | ✗ Need Yochananof/Shufersal URLs |
| Component | ✗ No component |
| Route | ✗ No route |
| MVP readiness | 🔴 Blocked — create data first |

---

## B. MVP Approach

**Recommended path: Manual corpus creation**  
Create `src/data/comparisons/yogurts_frontend_v1.json` with manually-calibrated scores using the BSIP2 scoring framework. No BSIP2 re-run required for MVP — scores derive from known product attributes and R-01/R-02/R-04/R-05 calibration logic.

**Why manual is acceptable for MVP:**
- Yogurt is a well-understood category with predictable scoring patterns
- Most significant quality differentiators are visible on label (plain vs. flavored, protein level, additive count)
- Post-MVP can replace with full BSIP2-derived scores
- The מעדנים run already scored several yogurt-adjacent products (יופלה GO: 69/B, confirming model behavior)

---

## C. Required Data File

**Target:** `src/data/comparisons/yogurts_frontend_v1.json`  
**Schema:** BariProductVM (identical to snacks and bread)

### Proposed Corpus (14 products)

Score targets are calibrated using R-01/R-02/R-04/R-05. They represent final post-recalibration values.

```json
[
  {
    "id": "yog-001",
    "name": "יוגורט מלא 3% תנובה",
    "score": 88, "grade": "A",
    "confidence": "partial",
    "insightLine": "חלב, תרבית — 2 מרכיבים בלבד. הבסיס הפשוט ביותר ביוגורט ישראלי",
    "_cluster": "plain"
  },
  {
    "id": "yog-002",
    "name": "יוגורט ביו 1.5% תנובה",
    "score": 87, "grade": "A",
    "confidence": "partial",
    "insightLine": "תרביות פרוביוטיות מאומתות. בסיס פשוט, תסיסה נוספת — מה שביו אמור להיות",
    "_cluster": "plain"
  },
  {
    "id": "yog-003",
    "name": "יוגורט 0% שומן",
    "score": 82, "grade": "A",
    "confidence": "partial",
    "insightLine": "ללא שומן, ללא תוספים. חלבון טוב ל-100 גרם",
    "_cluster": "plain"
  },
  {
    "id": "yog-004",
    "name": "יוגורט יווני 5% שטראוס",
    "score": 85, "grade": "A",
    "confidence": "partial",
    "insightLine": "מסוי כפול: 2× חלבון יחסית ליוגורט רגיל. מתאים לשימוש כתחליף גבינה",
    "_cluster": "greek"
  },
  {
    "id": "yog-005",
    "name": "יוגורט יווני 0% שטראוס",
    "score": 80, "grade": "A",
    "confidence": "partial",
    "insightLine": "גרסת 0% עם פרופיל חלבון גבוה. הפשרה בין שומן לחלבון",
    "_cluster": "greek"
  },
  {
    "id": "yog-006",
    "name": "אקטיביה טבעית דנונה",
    "score": 78, "grade": "B",
    "confidence": "partial",
    "insightLine": "תרביות ביו מאומתות. מעט עמילן מוסף — עדיין קרוב לבסיס",
    "_cluster": "plain"
  },
  {
    "id": "yog-007",
    "name": "יופלה בטעמי פירות",
    "score": 62, "grade": "C",
    "confidence": "partial",
    "insightLine": "5 מרכיבים + טעמי פירות: סוכר מוסף + חומרי טעם וריח — ציון ממוצע",
    "_cluster": "flavored"
  },
  {
    "id": "yog-008",
    "name": "אקטיביה טעמים דנונה",
    "score": 65, "grade": "B",
    "confidence": "partial",
    "insightLine": "אקטיביה עם טעמי פירות. יותר מרכיבים, סוכר מוסף, אבל תרביות ביו",
    "_cluster": "flavored"
  },
  {
    "id": "yog-009",
    "name": "יוגורט קוקוס טבעי (ללא גלוטן)",
    "score": 68, "grade": "B",
    "confidence": "partial",
    "insightLine": "תחליף ללא-חלב. קוקוס + תרבית — תוספים מייצבים, אבל בסיס סביר",
    "_cluster": "dairy-free"
  },
  {
    "id": "yog-010",
    "name": "יוגורט סויה טבעי",
    "score": 72, "grade": "B",
    "confidence": "partial",
    "insightLine": "חלבון סויה + תרבית. ללא סוכר מוסף. מייצבים מינימליים",
    "_cluster": "dairy-free"
  },
  {
    "id": "yog-011",
    "name": "יוגורט שתיה בניחוח וניל",
    "score": 55, "grade": "C",
    "confidence": "partial",
    "insightLine": "יוגורט שתיה = תוספי סמיכות + סוכר מוסף + טעמים. ציון ממוצע",
    "_cluster": "flavored"
  },
  {
    "id": "yog-012",
    "name": "יופלה GO פירות יער",
    "score": 69, "grade": "B",
    "confidence": "partial",
    "insightLine": "פרוטאין גבוה יחסית ל-100 גרם, אבל חומרי מתיקות ורמת עיבוד גבוהה",
    "_cluster": "high-protein"
  },
  {
    "id": "yog-013",
    "name": "מילקי יוגורט קרם-שוקולד",
    "score": 38, "grade": "D",
    "confidence": "partial",
    "insightLine": "מעדן עם שכבת שוקולד: 4 מקורות סוכר, ממתיקים, חומרי ייצוב. מוצר הנאה",
    "_cluster": "flavored"
  },
  {
    "id": "yog-014",
    "name": "יוגורט 0% ממותק ממתיק",
    "score": 51, "grade": "C",
    "confidence": "partial",
    "insightLine": "0% שומן + ממתיק מלאכותי. פשרה: קלוריות נמוכות, ממתיק סינטטי",
    "_cluster": "flavored"
  }
]
```

**Image sources:** Use Yochananof API pattern:
```
https://api.yochananof.co.il/media/catalog/product/cache/[hash]/[barcode]_s1_[date].jpg
```

For MVP, use Shufersal Cloudinary as backup (confirmed working for bread category).

---

## D. Scoring Logic (Manual Calibration Rules)

The following rules translate scoring framework to manual scores:

**Rule 1 — Plain dairy NOVA1:**  
Base score = 85. Apply +3 for fermentation (bio cultures count). Apply R-04 dairy sugar relief.
→ Plain yogurt: 83–90

**Rule 2 — Greek/strained NOVA2:**  
Base = 80. High protein bonus acknowledged but not a separate dimension.
→ Greek yogurt: 80–87

**Rule 3 — Flavored dairy NOVA3 with added sugar:**  
Base = 65. Apply sugar penalty: if red label sugar → -10. If additives ≥3 → -8.
→ Flavored yogurt: 55–70

**Rule 4 — High-protein functional NOVA3:**  
Base = 65. Protein acknowledged. Sweetener tier applies.
→ Protein yogurts: 60–72

**Rule 5 — Non-dairy NOVA2–3:**  
Base = 70. Deduct for each stabilizer/emulsifier category beyond 2.
→ Non-dairy plain: 65–78; non-dairy flavored: 52–65

**Rule 6 — Dessert-style (מעדן-like) NOVA4:**  
Base = 40. Cap at 50.
→ Dessert yogurts: 35–50

---

## E. Expansion Content Template

For each product, write:

**positiveSignals (1–3 items):**
- Specific, observable. "תרבית פרוביוטית מאומתת ברכיבים"
- Protein level if >6g/100g. "9.5g חלבון ל-100 גרם"
- Minimal ingredient count if ≤4. "2 מרכיבים בלבד"

**limitingFactors (0–2 items):**
- Sugar sources: "סוכר מוסף ברשימת הרכיבים" (if present)
- Additives: "2+ מייצבים/מסמיכים" (if present)
- Sweetener if present: "ממתיק [שם ספציפי] — טעם מתוק ללא סוכר"

**bottomLine (required):**
Format: `[score]/[grade]: [1-sentence honest description]`
Example: `88/A: הבסיס הפשוט ביותר — חלב ותרבית בלבד. המוצר שממנו כדאי לצאת כשמשווים`

**comparisonContext (recommended):**
Position within the corpus. Example: `הציון הגבוה ביותר בקטגוריה — 26 נקודות מעל יופלה GO (62/C). ההבדל: 2 מרכיבים מול 8+`

---

## F. Filters

**Filter IDs and labels:**

```typescript
export const YOGURTS_SHELF_LENS_OPTIONS = [
  { id: "plain", label: "טבעי/נטורל" },
  { id: "greek", label: "יווני/מסוי" },
  { id: "dairy-free", label: "ללא חלב" },
  { id: "high-protein", label: "עתיר חלבון" },
  { id: "flavored", label: "בטעמים" },
];
```

Filter logic: use `_cluster` internal field in JSON (strip before rendering, same pattern as snacks).

---

## G. Methodology Disclosure

```
ניתוח יוגורטים מבוסס על לייבלים של מוצרים נבחרים מהמדף הישראלי.
לכל מוצר נבחנו הרכב הרכיבים, רמת חלבון, תוספי מייצבים, סוכר מוסף ורמת עיבוד.
ציון יוגורט טבעי מבוסס גבוה יותר ממוצר בטעמים — לא בגלל שמות, אלא בגלל מה שכתוב ברשימת הרכיבים.
הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.
```

---

## H. Hero & Prologue Content

**Eyebrow:** `מנוע השוואה · יוגורטים`  
**Title:** `יוגורט: לא כל "טבעי" נוצר שווה`  
**Metadata line:** `[N] מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`

**Prologue sentences:**
1. "יוגורט נראה כמו מזון פשוט — חלב ותרבית. אבל המדף מציג ספקטרום רחב: ממוצרים עם 2 מרכיבים בלבד ועד מוצרים עם 8+ רכיבים, סוכר וממתיקים."
2. "ציון Bari ליוגורטים מבדיל בין יוגורט טבעי לא מתוק, יוגורט מועשר בתרביות, ומוצרי 'יוגורט' שמוצרי הנאה הם שמם הנאמן יותר."
3. "הנתון הבודד שהכי מדבר: רשימת הרכיבים. כמה מרכיבים, מה בהם — ומה לא."

---

## I. Files to Create

| File | Action | Notes |
|---|---|---|
| `src/data/comparisons/yogurts_frontend_v1.json` | CREATE | 14 products, BariProductVM + `_cluster` |
| `src/lib/comparisons/yogurts-shelf-filters.ts` | CREATE | YOGURTS_SHELF_LENS_OPTIONS, filterYogutsProducts |
| `src/lib/comparisons/yogurts-comparison-page-data.ts` | CREATE | Load corpus, export yogurtsProducts, hero, prologue, methodology |
| `src/components/comparisons/yogurts-comparison-desktop-page.tsx` | CREATE | Copy SnacksComparisonDesktopPage pattern |
| `src/app/hashvaot/yogurts/page.tsx` | CREATE | Route entry point |

---

## J. Launch Readiness

**Status: 🔴 NOT READY**

**Blocked on:** data file creation + expansion content writing + component build.

**Estimated effort:** 2 days total.
- Day 1: Create corpus JSON with 14 products + expansion content
- Day 2: Build component + filters + route + QA

**Can launch at MVP with manual scores.** Post-MVP: replace with BSIP2-derived scores from a proper scraping run.
