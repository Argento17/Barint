# Bari Comparison View Model Specification v1

## What This Document Is

The deterministic interface between BSIP backend outputs and the Bari frontend UI.

Not a scoring document. Not a design document. Not a philosophy document.

A contract. The backend produces; the frontend renders.

---

## The Boundary Rule

The UI layer must never contain:

- Ontology concepts (NOVA, archetype labels, routing clusters)
- Scoring logic (dimension weights, caps, penalties, synthesis layers)
- Confidence computation (trust scores, observation counts)
- Framework vocabulary (bread-light, milk-orbit, snack decomposition)
- BSIP stage awareness (BSIP0, BSIP1, BSIP2, pipeline identifiers)

**The VM boundary is where all interpretation terminates.**

After this boundary: rendering only.

---

## Canonical TypeScript Interfaces

Source of truth: `src/lib/view-models/index.ts`

```typescript
export type BariGrade = "A" | "B" | "C" | "D" | "E";
export type BariConfidence = "verified" | "partial" | "insufficient";

export interface BariNutritionVM {
  energyKcal: number | null;
  protein: number | null;
  sugar: number | null;
  fat: number | null;
  fiber: number | null;
  sodium: number | null;
}

export interface BariExpansionVM {
  nutrition: BariNutritionVM | null;
  ingredients: string | null;
  confidenceLabel: string;   // pre-rendered Hebrew, e.g. "נתונים מלאים"
  servingNote: string;       // e.g. "ל-100 גרם"
}

export interface BariProductVM {
  id: string;
  name: string;
  imageUrl: string | null;
  score: number | null;
  grade: BariGrade | null;
  insightLine: string;       // "" = no insight slot rendered
  confidence: BariConfidence;
  expansion: BariExpansionVM;
}

export interface BariFilterVM {
  id: string;        // opaque to UI
  label: string;     // pre-rendered Hebrew
  count: number;
  isActive: boolean;
}

export interface BariHeroVM {
  categoryNameHe: string;
  tagline: string;
  productCount: number;
  scoredCount: number;
  averageScore: number | null;
  topProduct: { name: string; score: number; grade: BariGrade } | null;
}

export interface BariPrologueVM {
  sentences: string[];   // 2–3 pre-authored sentences
}

export interface BariMethodologyVM {
  text: string;
  sourceNote: string | null;
  lastUpdated: string | null;
}

export interface BariCategoryPageVM {
  hero: BariHeroVM;
  prologue: BariPrologueVM;
  products: BariProductVM[];
  filters: BariFilterVM[];
  methodology: BariMethodologyVM;
}
```

---

## Product Rendering Rules

| Field | Rule |
|-------|------|
| `name` | Render as-is. Never truncate in expansion. line-clamp-2 in row only. |
| `imageUrl = null` | 56×56 placeholder: background `#EDEEED`, `rounded-md`. No icon, no label. |
| `score = null` | Chip renders "—" in `#9A9FA6`, chip background `#EEEEEA`. |
| `score` present | Display as integer (backend already rounded). No decimal, no suffix. |
| `grade = null` | Grade slot hidden. |
| `insightLine = ""` | Insight slot not rendered. Row min-height still maintained via token. |
| `insightLine` present | Render verbatim. line-clamp-1. Never rewrite, never abbreviate, never enrich. |
| `expansion` | Always passed. Null content fields are handled per field rules below. |

---

## Confidence → UI Mapping

| State | Chip bg | Score visible | Grade visible | Expansion |
|-------|---------|--------------|--------------|-----------|
| `verified` | grade tint via `gradePalette[grade]` (Gen 1.1) | yes | yes | full content |
| `partial` | grade tint via `gradePalette[grade]` (Gen 1.1) | yes | yes | available data only |
| `insufficient` | `#EEEEEA` (no grade → neutral null state) | no | no | confidence label + close only |

Score chip border: grade accent via `gradePalette[grade]` for verified/partial; `rgba(17,19,24,0.07)` for insufficient.

**Color encodes grade, never confidence.** As of the Gen 1.1 directive (2026-06-03) the chip is color-coded by grade (one hue family per grade A→E, tinted bg + accent border/number). Confidence still introduces no second color axis: the `verified` and `partial` chips for the same grade are visually identical; confidence differences are structural only (which content the expansion shows). The `insufficient` state has no grade and so renders the neutral null chip.

---

## Nutrition VM Rendering Rules

- All values are per 100g or 100ml. Backend normalizes. UI never normalizes.
- `null` field → hide cell entirely. Do not show "—".
- `0` is a valid value. Display it.
- Display order is fixed: energyKcal → protein → sugar → fat → fiber → sodium.
- Labels and units are UI constants (not from the VM). The VM carries numbers only.

UI label constants:
```
energyKcal  → 'קק"ל'   unit: ""
protein     → "חלבון"   unit: "ג'"
sugar       → "סוכרים"  unit: "ג'"
fat         → "שומן"    unit: "ג'"
fiber       → "סיבים"   unit: "ג'"
sodium      → "נתרן"    unit: 'מ"ג'
```

---

## Expansion Section Rules

The expansion renders: nutrition grid → ingredient list → confidence row.

Any section with null data is hidden entirely. The section order is fixed; it never reorders based on available data.

**Ingredient list:**
- Render verbatim. Never summarize.
- Clip at 4 lines. Show "הצג הכל" to expand.
- Once expanded, no re-collapse.
- `null` → section hidden.

**Confidence row (bottom of expansion):**
- Left: `confidenceLabel` from VM. Never computed by UI.
- Right: "סגור" button. Triggers row collapse.

**`insufficient` products:**
- Expansion still animates open.
- Content: confidence label row only. No nutrition, no ingredients.
- This is intentional — the user learns why the score is missing.

---

## Filter VM Rules

- `id` is opaque. UI never branches on its string value.
- `label` is the display string. UI renders as-is.
- `count` is pre-computed. UI never counts products against filters.
- `isActive` drives the visual selection state.
- First filter in the array is always "all". UI may assume this structurally.

---

## Hero VM Rules

- `averageScore`: null if fewer than 3 scored products. UI must handle null gracefully (hide the average line).
- `topProduct`: null if no product scores ≥ 60. UI hides the accent element.
- `tagline`: 1 pre-authored sentence. Renders below category name. Never dynamic.

---

## Product Ordering

Products arrive pre-ordered. UI never sorts.

Order: scored products descending by score → unscored (`insufficient`) appended last.

---

## Methodology VM Rules

Entire content is pre-authored. UI renders verbatim. No dynamic computation, no conditional phrasing.

`text` is max 4 sentences. `sourceNote` and `lastUpdated` are optional metadata lines rendered below the main text.

---

## Missing-Data Decision Table

| What is null/missing | What the UI renders |
|---------------------|---------------------|
| `imageUrl` | 56×56 `#EDEEED` placeholder |
| `score` | Chip "—", background `#EEEEEA` |
| `grade` | No grade letter rendered |
| `insightLine = ""` | No insight slot (row height unchanged) |
| `expansion.nutrition` | Nutrition grid hidden |
| `expansion.ingredients` | Ingredient section hidden |
| All expansion content null | Confidence label + close only |
| `hero.averageScore` | Average line hidden |
| `hero.topProduct` | Top product accent hidden |
| `methodology.sourceNote` | Source line hidden |
| `methodology.lastUpdated` | Update line hidden |

---

## Backend → VM Transformation Notes

These field mappings apply when transforming BSIP output into the VM. This work belongs to the backend/data layer, not the UI.

| BSIP field | VM field | Note |
|------------|----------|------|
| `confidence_level: "full"` | `confidence: "verified"` | Language boundary |
| `name_he` | `name` | Language specificity removed — all text is Hebrew |
| `image_url` | `imageUrl` | camelCase |
| `insight_line` | `insightLine` | camelCase |
| `ingredients_he` | `expansion.ingredients` | Moved into expansion |
| `nutrition` (root) | `expansion.nutrition` | Moved into expansion, fields renamed |
| `energy_kcal` | `energyKcal` | camelCase, inside BariNutritionVM |
| `protein_g` | `protein` | Unit suffix removed (unit is UI concern) |
| `sugar_g` | `sugar` | Unit suffix removed |
| `fat_g` | `fat` | Unit suffix removed |
| `fiber_g` | `fiber` | Unit suffix removed |
| `sodium_mg` | `sodium` | Unit suffix removed |
| `confidence_level` (any) | `expansion.confidenceLabel` | Backend renders Hebrew string |

**The transformation layer must add:**
- `expansion.servingNote` — e.g. `"ל-100 גרם"` based on product category
- `hero.averageScore` — computed from scored products, null if < 3
- `hero.topProduct` — best scored product, null if best score < 60
- `filters` — computed from the full product list
- `prologue.sentences` — editorial, authored per category
- `methodology.*` — authored per category

---

## Import Discipline

Correct:
```typescript
import type { BariProductVM, BariCategoryPageVM } from "@/lib/view-models";
```

Incorrect — must never appear in UI components:
```typescript
import type { ComparisonProduct } from "@/lib/comparisons/comparison-product";
import type { BariGrade } from "@/lib/comparisons/comparison-product";
```

UI components import from `@/lib/view-models` only.

`@/lib/comparisons/` is backend/transformation territory.

---

## Version

v1 — established 2026-05-28.

Amend this document only when the rendering contract changes. Score changes, editorial changes, and category expansions do not require amendment.
