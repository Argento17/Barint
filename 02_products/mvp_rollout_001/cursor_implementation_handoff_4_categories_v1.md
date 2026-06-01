# Cursor Implementation Handoff — 4 Categories MVP v1
**Date:** 2026-05-30
**For:** Cursor AI
**Scope:** Milk, Snacks, Bread, Yogurts — 70% MVP rollout

Read this fully before starting. Every step is a concrete action. Do not write planning documents. Do not ask questions. Execute in sequence.

---

## CHECKPOINT 0 — Environment

Working repo: `C:\Users\HP\bari`  
BSIP2 engine: `C:\Bari\03_operations\bsip2\proto_v0\src\`  
Primary language: TypeScript (Next.js App Router)  
Data format: BariProductVM (see `src/lib/view-models/index.ts`)

---

## PART 1 — SCORING RECALIBRATION

**Do this before any frontend work.**

### Step 1.1 — Update BSIP2 constants

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\constants.py`

**Change 1:** Raise NOVA3 processing cap from 82 to 87.
```python
# In PROCESSING_CAPS list:
# Find:
("NOVA_PROXY_3_PROCESSED", "nova==3", 82),
# Replace with:
("NOVA_PROXY_3_PROCESSED", "nova==3", 87),
```

**Change 2:** Add yogurt calorie density table.
```python
# In CALORIE_DENSITY_TABLES dict, add entry:
"yogurt": [(60,95),(100,88),(140,78),(180,65),(250,50),(1e9,30)],
```

### Step 1.2 — Update BSIP2 score engine

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`

**Change 1:** Raise fiber nutrient density ceiling.
```python
# In score_nutrient_density():
# Find:
fs = min(85, max(0, (fiber / 12) * 85))
# Replace with:
fs = min(95, max(0, (fiber / 12) * 95))
```

**Change 2:** Add fermentation post-score bonus.
```python
# In score_product(), after computing weighted dimension sum and before
# calling _apply_guardrail_caps() (or equivalent final score step):
# Add:
has_fermentation = l3.get("has_fermentation", False)
nova_level_for_bonus = l1.get("nova_level", 4) or l3.get("nova_level", 4)
if has_fermentation and nova_level_for_bonus <= 3:
    pre_guardrail_score = min(100, pre_guardrail_score + 6)
    # Add to trace:
    notes.append("fermentation_bonus: +6 (direct, pre-guardrail)")
```

Note: Variable names (`pre_guardrail_score`, `notes`) may differ — adapt to match existing code structure. The behavior must be: +6 added to total score BEFORE guardrail caps, capped at 100, only for has_fermentation=True AND nova≤3.

### Step 1.3 — Re-run BSIP2 on Snacks

Run the snacks batch scorer against the existing corpus.

Update `src/data/comparisons/snacks_frontend_v2.json`:
- Replace all `score` values with new rounded-integer outputs
- Replace all `grade` values using: S≥90, A≥80, B≥65, C≥50, D≥35, E<35
- Update any `bottomLine` or `insightLine` text that contains a quoted old score number (grep: `/[0-9]+\/(A|B|C|D|E)/`)
- Update `comparisonContext` fields where they state relative score differences
- Re-sort `products` array by score descending
- Update `_meta.generated` to current date

### Step 1.4 — Re-run BSIP2 on Bread

Run the bread batch scorer against the existing corpus.

Update `src/data/comparisons/bread_frontend_v2.json`:
- Same update rules as Step 1.3
- **Special fix:** "לחם ירוק מקמח מלא" currently has `"score": 80, "grade": "B"` — this is incorrect. Score ≥80 = grade A. Fix the grade field.
- Audit ALL products: verify each `grade` field matches `score_to_grade(score)` using the thresholds above
- Re-sort by score descending
- Update `_meta.generated`

---

## PART 2 — BREAD: COMPONENT SWAP

The bread route currently uses `ComparisonShelfPage` (old format). Replace it with the milk/snacks pattern.

### Step 2.1 — Create BreadComparisonDesktopPage

**Source to copy from:** `src/components/comparisons/snacks-comparison-desktop-page.tsx`

**New file:** `src/components/comparisons/bread-comparison-desktop-page.tsx`

**Required changes from snacks template:**

1. Change import from snacks filters to bread filters:
```typescript
// Remove:
import {
  filterSnacksProducts,
  SNACKS_SHELF_LENS_OPTIONS,
  type SnacksShelfFilterId,
} from "@/lib/comparisons/snacks-shelf-filters";
// Add:
import {
  filterBreadProducts,
  BREAD_SHELF_LENS_OPTIONS,
  type BreadShelfFilterId,
} from "@/lib/comparisons/bread-shelf-filters";
```

2. Change state type:
```typescript
// Remove:
const [activeFilters, setActiveFilters] = useState<SnacksShelfFilterId[]>([]);
// Add:
const [activeFilters, setActiveFilters] = useState<BreadShelfFilterId[]>([]);
```

3. Change filter function call:
```typescript
// Remove:
filterSnacksProducts(products, activeFilters)
// Add:
filterBreadProducts(products, activeFilters)
```

4. Change options reference:
```typescript
// Remove:
SNACKS_SHELF_LENS_OPTIONS.map(...)
// Add:
BREAD_SHELF_LENS_OPTIONS.map(...)
```

5. Change component export name:
```typescript
export interface BreadComparisonDesktopPageProps { ... }
export function BreadComparisonDesktopPage({ ... }) { ... }
```

6. All other markup, styles, expansion panel, methodology section: **identical to snacks** — do not change.

7. Remove the `segment` display if snacks template shows it (bread products do not have a `segment` field).

### Step 2.2 — Verify bread-comparison-page-data.ts exports

**File:** `src/lib/comparisons/bread-comparison-page-data.ts`

Confirm these are exported (they should already exist):
- `breadProducts: BariProductVM[]`
- `breadHero: { eyebrow: string; title: string }`
- `breadMetadataLine: string`
- `breadPrologueSentences: readonly string[]`
- `breadMethodologyLines: readonly string[]`
- `breadComparisonMetadata: Metadata`

If any are missing, add them following the `snacks-comparison-page-data.ts` pattern.

**Hero content:**
```typescript
export const breadHero = {
  eyebrow: "מנוע השוואה · לחמים",
  title: "לחם: מה שכתוב על האריזה לא תמיד מה שבפנים",
};
```

**Metadata line:**
```typescript
export const breadMetadataLine = `${breadProducts.length} מוצרים נבדקו · מדגם שופרסל · ממוין לפי ציון Bari`;
```

**Prologue:**
```typescript
export const breadPrologueSentences = [
  "לחם נראה כמו קטגוריה פשוטה: קמח, מים, מחמצת. אבל המדף מספר סיפור יותר מורכב.",
  "חלק מהמוצרים שמציגים 'מחמצת' בשם משתמשים בשמרים תעשייתיים ברכיבים. חלק אחר מסתמכים על כותרת 'מלא' כדי להציג רכיבים מעורבים.",
  "ההשוואה מתבססת על מה שאפשר לבדוק: ערכי חלבון, סיבים, נתרן, ותסיסה מאומתת ברשימת הרכיבים — לא על המיתוג.",
] as const;
```

**Methodology lines:**
```typescript
export const breadMethodologyLines = [
  "ניתוח לחמים מבוסס על נתונים מגלויות שופרסל — מדגם מדף, לא סקר שוק מלא.",
  "לכל מוצר נבחנו הרכב הרכיבים, ערכי חלבון וסיבים, רמת עיבוד ותסיסה מאומתת ברכיבים.",
  "ציון הלחם אינו מבוסס על קלוריות בלבד — הוא משקלל מבנה, מקור הדגן, ורמת ההנדסה במוצר.",
  "ההשוואה נועדה לעזור בהשוואה בין מוצרים, ולא מהווה המלצה תזונתית אישית.",
] as const;
```

### Step 2.3 — Update bread route

**File:** `src/app/hashvaot/bread/page.tsx`

Replace entirely:
```typescript
import type { Metadata } from "next";

import { BreadComparisonDesktopPage } from "@/components/comparisons/bread-comparison-desktop-page";
import {
  breadComparisonMetadata,
  breadHero,
  breadMetadataLine,
  breadMethodologyLines,
  breadPrologueSentences,
  breadProducts,
} from "@/lib/comparisons/bread-comparison-page-data";

export const metadata: Metadata = breadComparisonMetadata;

export default function BreadComparisonRoute() {
  return (
    <BreadComparisonDesktopPage
      products={breadProducts}
      metadataLine={breadMetadataLine}
      hero={breadHero}
      prologueSentences={breadPrologueSentences}
      methodologyLines={breadMethodologyLines}
    />
  );
}
```

---

## PART 3 — YOGURTS: FULL BUILD

### Step 3.1 — Create yogurts data file

**File:** `src/data/comparisons/yogurts_frontend_v1.json`

Use the corpus defined in `yogurts_comparison_mvp_handoff_v1.md` (14 products).

Schema exactly matches `snacks_frontend_v2.json`. Required fields per product:
- `id` (yog-001 through yog-014)
- `name` (Hebrew product name)
- `imageUrl` (Yochananof or Shufersal CDN — use null if not found)
- `score` (integer, from manual calibration table)
- `grade` (derived from score using standard thresholds)
- `insightLine` (Hebrew, ≤15 words, product-specific)
- `confidence`: `"partial"` for all (manual scoring)
- `expansion`: object with:
  - `nutrition`: null (not available for MVP)
  - `ingredients`: null or partial string if known
  - `confidenceLabel`: `"נתונים חלקיים"`
  - `servingNote`: `"ל-100 גרם"`
  - `positiveSignals`: 1–3 Hebrew strings
  - `limitingFactors`: 0–2 Hebrew strings
  - `bottomLine`: required
  - `comparisonContext`: recommended
- `_cluster`: internal field, one of: `"plain"`, `"greek"`, `"dairy-free"`, `"high-protein"`, `"flavored"`

Include `_meta` block at top:
```json
{
  "_meta": {
    "generated": "2026-05-30T00:00:00Z",
    "category": "yogurts",
    "product_count": 14,
    "scored_count": 14,
    "schema": "BariProductVM[]",
    "version": "v1-manual",
    "expansion": "manual_calibration_v1",
    "source_run_id": "manual_yogurts_v1",
    "scope_note": "ניתוח ידני — לא ריצת BSIP2 מלאה. ציונים מבוססים על לוגיקת מנוע BSIP2 עם ידע מוצרי ידני",
    "production_pass": "Manual scoring pass 2026-05-30 per bari_scoring_recalibration_v1 + R-01/R-02/R-04/R-05"
  },
  "products": [ ... ]
}
```

### Step 3.2 — Create yogurts shelf filters

**New file:** `src/lib/comparisons/yogurts-shelf-filters.ts`

```typescript
import type { BariProductVM } from "@/lib/view-models";

export type YogurtsShelfFilterId = "plain" | "greek" | "dairy-free" | "high-protein" | "flavored";

export const YOGURTS_SHELF_LENS_OPTIONS: Array<{ id: YogurtsShelfFilterId; label: string }> = [
  { id: "plain", label: "טבעי/נטורל" },
  { id: "greek", label: "יווני/מסוי" },
  { id: "dairy-free", label: "ללא חלב" },
  { id: "high-protein", label: "עתיר חלבון" },
  { id: "flavored", label: "בטעמים" },
];

type YogutsCorpusProduct = BariProductVM & { _cluster?: string };

const clusterMap = new Map<string, YogurtsShelfFilterId>();
// Map is populated at load time from the JSON _cluster fields
// (same pattern as bread-shelf-filters.ts using curated JSON)

export function filterYogurtsProducts(
  products: BariProductVM[],
  activeFilters: YogurtsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) => {
    const internal = (product as YogutsCorpusProduct)._cluster;
    return internal != null && activeFilters.includes(internal as YogurtsShelfFilterId);
  });
}
```

Note: The `_cluster` field is stripped before rendering. Keep it on the internal product type only.

### Step 3.3 — Create yogurts page data

**New file:** `src/lib/comparisons/yogurts-comparison-page-data.ts`

Follow `snacks-comparison-page-data.ts` exactly, substituting:
- Import from `@/data/comparisons/yogurts_frontend_v1.json`
- Internal type: `YogutsCorpusProduct = BariProductVM & { _cluster?: string }`
- Strip function: strips `_cluster` (not `_internal_cluster`)
- Hero, prologue, methodology: use yogurt content from handoff doc

```typescript
export const yogurtsHero = {
  eyebrow: "מנוע השוואה · יוגורטים",
  title: "יוגורט: לא כל 'טבעי' נוצר שווה",
};

export const yogurtsMetadataLine = `${yogurtsProducts.length} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`;

export const yogurtsPrologueSentences = [
  "יוגורט נראה כמו מזון פשוט — חלב ותרבית. אבל המדף מציג ספקטרום רחב: ממוצרים עם 2 מרכיבים בלבד ועד מוצרים עם 8+ רכיבים, סוכר וממתיקים.",
  "ציון Bari ליוגורטים מבדיל בין יוגורט טבעי לא מתוק, יוגורט מועשר בתרביות, ומוצרי 'יוגורט' שמוצרי הנאה הם שמם הנאמן יותר.",
  "הנתון הבודד שהכי מדבר: רשימת הרכיבים. כמה מרכיבים, מה בהם — ומה לא.",
] as const;

export const yogurtsMethodologyLines = [
  "ניתוח יוגורטים מבוסס על לייבלים של מוצרים נבחרים מהמדף הישראלי.",
  "לכל מוצר נבחנו הרכב הרכיבים, רמת חלבון, תוספי מייצבים, סוכר מוסף ורמת עיבוד.",
  "ציון יוגורט טבעי מבוסס גבוה יותר ממוצר בטעמים — לא בגלל שמות, אלא בגלל מה שכתוב ברשימת הרכיבים.",
  "הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.",
] as const;
```

### Step 3.4 — Create YogurtsComparisonDesktopPage

**New file:** `src/components/comparisons/yogurts-comparison-desktop-page.tsx`

Copy `snacks-comparison-desktop-page.tsx` and substitute:
- Import `YOGURTS_SHELF_LENS_OPTIONS`, `filterYogurtsProducts`, `YogurtsShelfFilterId`
- Change state type to `YogurtsShelfFilterId[]`
- Change export name to `YogurtsComparisonDesktopPage`
- All rendering logic identical

### Step 3.5 — Create yogurts route

**New file:** `src/app/hashvaot/yogurts/page.tsx`

```typescript
import type { Metadata } from "next";

import { YogurtsComparisonDesktopPage } from "@/components/comparisons/yogurts-comparison-desktop-page";
import {
  yogurtsHero,
  yogurtsMetadataLine,
  yogurtsMethodologyLines,
  yogurtsPrologueSentences,
  yogurtsProducts,
} from "@/lib/comparisons/yogurts-comparison-page-data";

export const metadata: Metadata = {
  title: "השוואת יוגורטים | Bari",
  description: "השוואת יוגורטים ותחליפי יוגורט — ציון Bari, חלבון, תרביות, סוכר מוסף. מידע, לא המלצה.",
};

export default function YogurtsComparisonRoute() {
  return (
    <YogurtsComparisonDesktopPage
      products={yogurtsProducts}
      metadataLine={yogurtsMetadataLine}
      hero={yogurtsHero}
      prologueSentences={yogurtsPrologueSentences}
      methodologyLines={yogurtsMethodologyLines}
    />
  );
}
```

---

## PART 4 — QA CHECKLIST

Run after all parts complete.

### All four categories

- [ ] `npm run build` passes with no errors
- [ ] `npm run lint` passes

### Per category at `/hashvaot/[route]`

**Milk** (`/hashvaot/milk-comparison`):
- [ ] 18 products visible
- [ ] Scores displayed
- [ ] Filters functional
- [ ] Expansion panel opens
- [ ] RTL correct

**Snacks** (`/hashvaot/snacks`):
- [ ] 18 products visible, re-sorted by new scores
- [ ] Filters functional (date-based, oat-cereal, wellness, grade-e)
- [ ] No score references in text that don't match JSON scores
- [ ] snk-001 still rank 1

**Bread** (`/hashvaot/bread`):
- [ ] 24 products visible
- [ ] New component active (NOT ComparisonShelfPage)
- [ ] Filters functional (everyday, מחמצת, מלא ודגנים, לחמי בריאות, קרקרים)
- [ ] "לחם ירוק מקמח מלא" shows grade A (not B)
- [ ] Sourdough breads promoted to A range (e.g., "לחם מחמצת קמח מלא")

**Yogurts** (`/hashvaot/yogurts`):
- [ ] Route loads at `/hashvaot/yogurts`
- [ ] 14 products visible
- [ ] Filters functional (5 options)
- [ ] Plain yogurt (yog-001) at rank 1 with score 88/A
- [ ] Dessert yogurt (yog-013) at bottom, score 38/D
- [ ] Mobile layout works

### Content sanity

- [ ] No "NOVA" text visible in any shelf-facing field
- [ ] No "ממד" / "BSIP" / "גורם הגנה" in any expansion
- [ ] No "חזק/בינוני/חלש" grade labels
- [ ] All `insightLine` fields are product-specific (≥1 specific detail)
- [ ] All `bottomLine` fields contain a score reference in format `[score]/[grade]:`

---

## PART 5 — DO NOT TOUCH

- `src/data/milk-comparison.json` — do not modify
- `src/components/comparisons/milk-comparison-page.tsx` — do not modify
- `src/app/hashvaot/milk-comparison/page.tsx` — do not modify
- `src/app/hashvaot/maadanim/page.tsx` — do not modify
- Any file under `src/app/hashvaot/maadanim/` — do not modify
- Score mechanics, guardrail logic beyond R-01/R-02/R-03 — do not modify
- Grade thresholds — do not modify

---

## EXECUTION ORDER SUMMARY

1. `constants.py`: R-01 cap + R-05 yogurt table
2. `score_engine.py`: R-03 fiber ceiling + R-02 fermentation bonus
3. Re-run BSIP2 snacks → update `snacks_frontend_v2.json`
4. Re-run BSIP2 bread → update `bread_frontend_v2.json`
5. Create `bread-comparison-desktop-page.tsx`
6. Update `bread-comparison-page-data.ts` exports
7. Update `bread/page.tsx`
8. Create `yogurts_frontend_v1.json`
9. Create `yogurts-shelf-filters.ts`
10. Create `yogurts-comparison-page-data.ts`
11. Create `yogurts-comparison-desktop-page.tsx`
12. Create `yogurts/page.tsx`
13. `npm run build`
14. QA checklist
