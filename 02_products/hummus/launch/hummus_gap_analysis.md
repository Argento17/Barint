# Hummus Category — Gap Analysis

**Task:** TASK-058  
**Owner:** Frontend Agent  
**Date:** 2026-05-31  
**Input:** hummus_status_audit.md  
**Scope:** Items required to make `/hashvaot/hummus` production-ready

---

## Gap Summary

| Gap ID | Item | Owner | Effort | Hard dependency |
|---|---|---|---|---|
| GAP-01 | Resolve HUM-001 fat data (decision required) | Product Agent | — | None — decision gates GAP-02 |
| GAP-02 | Build frontend dataset JSON (`hummus_frontend_v1.json`) | Data Agent | M | GAP-01 decision |
| GAP-03 | Copy frontend JSON to website repo | Data Agent | XS | GAP-02 |
| GAP-04 | Create category definition file (`hummus.ts`) | Frontend Agent | S | GAP-03 |
| GAP-05 | Update category registry (`index.ts`, `types.ts`) | Frontend Agent | XS | GAP-04 |
| GAP-06 | Create route page (`/hashvaot/hummus/page.tsx`) | Frontend Agent | S | GAP-05 |
| GAP-07 | Create comparison page component | Frontend Agent | M | GAP-06 |
| GAP-08 | Write Hebrew category copy (hero, prologue, methodology) | Content Agent | S | GAP-02 (needs data for accuracy) |
| GAP-09 | Write product insight lines (69 products) | Content Agent | L | GAP-08 |
| GAP-10 | QA audit — frontend page | QA Agent | S | GAP-07, GAP-09 |
| GAP-11 | Product Agent go-live approval | Product Agent | — | GAP-10 PASS |

**Effort key:** XS = < 1 hour, S = 1–4 hours, M = 4–16 hours, L = 16–40 hours

---

## Gap Details

---

### GAP-01 — Fat Data Resolution (Decision)

**What is missing:** A Product Agent decision on how to handle the 59/69 BSIP1 records with corrupted `fat_g` values before the frontend dataset is built.

**Why it matters:** The frontend dataset is built from BSIP1 + BSIP2 data. If corrupted fat values are passed through to the frontend JSON, the nutrition panel will display wrong fat figures (0.5g instead of 5–12g) for 86% of products. This is a consumer-facing data quality problem.

**Options:**

| Option | Description | Effort | Risk |
|---|---|---|---|
| A — Re-scrape | Manually verify and correct `fat_g` for 59 products from product packaging or retailer detail pages | L (16–40h for Data Agent) | Delays launch by 1–2 weeks |
| B — Suppress fat display | Exclude `fat_g` from the nutrition panel in the frontend dataset for hummus; document in MethodologyFooter | XS (config in build script) | Nutrition panel less informative; acceptable |
| C — Flag with caveat | Show fat values with a data quality label ("ערך חלקי") where `fat_g < 1.0` and product contains tahini | S (Frontend Agent adds caveat logic) | Adds UI complexity; transparent |
| D — Launch with known issue | Accept fat values as-is, document in internal issue register only | None | Consumer-facing bad data; not recommended |

**Recommended:** Option B — Suppress fat display for hummus v1. The BSIP2 scoring used `allowed_with_warning` which means the scores are valid; only the display field is incorrect. Suppressing is the cleanest consumer-facing outcome and does not delay the launch. Document in MethodologyFooter.

**Owner:** Product Agent (decision), Data Agent (implementation if B or C)  
**Effort:** Decision only — downstream effort is XS (Option B) to S (Option C)  
**Dependency:** None — gates GAP-02

---

### GAP-02 — Build Frontend Dataset JSON

**What is missing:** `hummus_frontend_v1.json` — the frontend-formatted dataset matching `BariCategoryPageVM` schema.

**Source data:** `C:\Bari\03_operations\bsip2\sprint1\outputs\production_hummus.json` (BSIP2 output) + BSIP1 canonical records from `C:\Bari\02_products\hummus\canonical_bsip1\`.

**What the build script must produce:**
```
BariCategoryPageVM
  ├── hero: { tagline, productCount, scoredCount, topProduct }
  ├── prologue: { sentences: string[] }      ← provided by Content Agent (GAP-08)
  ├── products: BariProductVM[]              ← 69 products from run_hummus_002
  │     ├── id, name, imageUrl
  │     ├── score, grade
  │     ├── insightLine                      ← provided by Content Agent (GAP-09)
  │     ├── confidence: "verified"|"partial"|"insufficient"
  │     └── expansion: BariExpansionVM
  │           ├── nutrition (fat_g suppressed if Option B selected)
  │           ├── ingredients
  │           ├── confidenceLabel (Hebrew pre-rendered)
  │           ├── servingNote: "ל-100 גרם"
  │           ├── positiveSignals
  │           ├── limitingFactors
  │           └── bottomLine
  ├── filters: BariFilterVM[]
  └── methodology: BariMethodologyVM        ← provided by Content Agent (GAP-08)
```

**Build script:** Adapt `build_frontend_dataset.py` for hummus category. Key adaptations needed:
- Category ID: `"hummus"`
- Source data path: `02_products/hummus/`
- Fat suppression: Apply Option B logic if Product Agent selects it
- Filter dimensions: Confirm which 3 filter dimensions are valid for hummus (e.g., score tier, product type, additive presence)

**Owner:** Data Agent  
**Effort:** M (4–8 hours — script adaptation + run + validation of output schema)  
**Dependency:** GAP-01 (decision on fat handling must precede build)

---

### GAP-03 — Copy Frontend JSON to Website Repo

**What is missing:** The file `hummus_frontend_v1.json` in `C:\bari\bari-web\src\data\comparisons\`.

**Action:**
```powershell
Copy-Item "C:\Bari\03_operations\...\hummus_frontend_v1.json" `
          "C:\bari\bari-web\src\data\comparisons\hummus_frontend_v1.json"
```

**Owner:** Data Agent  
**Effort:** XS (< 5 minutes, but requires GAP-02 complete)  
**Dependency:** GAP-02

---

### GAP-04 — Create Category Definition File (`hummus.ts`)

**What is missing:** `C:\bari\bari-web\src\lib\comparisons\registry\categories\hummus.ts`

**Template:** Model on `maadanim.ts` (most recently built Gen 1 category). Must implement `ComparisonCategoryDefinition`:

```typescript
import type { ComparisonCategoryDefinition } from '../types'
import hummusData from '../../data/comparisons/hummus_frontend_v1.json'

export const hummusCategoryDefinition: ComparisonCategoryDefinition = {
  id: 'hummus',
  routePath: '/hashvaot/hummus',
  metadata: {
    title: 'השוואת חומוס — 2026 | ברי',
    description: '...',  // from Content Agent GAP-08
  },
  getPageData: () => { ... },
  getCorpusPayload: () => { ... },
}
```

**Owner:** Frontend Agent  
**Effort:** S (2–3 hours — template adaptation, type compliance, JSON import wiring)  
**Dependency:** GAP-03 (JSON must exist before import can be validated)

---

### GAP-05 — Update Category Registry

**What is missing:** Two edits to existing files in `C:\bari\bari-web\src\lib\comparisons\registry\`:

**`types.ts`** — Add `"hummus"` to the union type:
```typescript
// Before:
export type ComparisonCategoryId = "maadanim" | "bread" | "snacks" | "yogurts"

// After:
export type ComparisonCategoryId = "maadanim" | "bread" | "snacks" | "yogurts" | "hummus"
```

**`index.ts`** — Add import and registration:
```typescript
import { hummusCategoryDefinition } from './categories/hummus'
// ... add to registry map
```

**Owner:** Frontend Agent  
**Effort:** XS (15–30 minutes)  
**Dependency:** GAP-04 (definition file must exist before import)

---

### GAP-06 — Create Route Page

**What is missing:** `C:\bari\bari-web\src\app\hashvaot\hummus\page.tsx`

This is the Next.js App Router page file. Template from `src/app/hashvaot/maadanim/page.tsx` or equivalent. It calls `getComparisonCategory('hummus')` and renders the comparison page component.

```typescript
import { getComparisonCategory } from '@/lib/comparisons/registry'
import { HummusComparisonPage } from '@/components/comparisons/hummus-comparison-page'

export default async function HummusPage() {
  const category = getComparisonCategory('hummus')
  const data = await category.getPageData()
  return <HummusComparisonPage data={data} />
}
```

**Owner:** Frontend Agent  
**Effort:** S (1–2 hours — template with no novel logic)  
**Dependency:** GAP-05 (registry must include hummus before route can resolve the category)

---

### GAP-07 — Create Comparison Page Component

**What is missing:** `C:\bari\bari-web\src\components\comparisons\hummus-comparison-page.tsx`

This is the Gen 1 canonical comparison page component. It uses the shared component tree (`CategoryHero`, `CategoryPrologue`, `ProductTable`, `MethodologyFooter`) — no custom Gen 0 components.

**Architecture (Gen 1 frozen pattern):**
```
[1] CategoryHero      — hero.tagline, hero.productCount
[2] CategoryPrologue  — prologue.sentences[]
[3] ProductTable      — products[], filters[]
[4] MethodologyFooter — methodology text
```

Desktop: renders `BariComparisonDesktopPage` at `lg:` breakpoint.  
Mobile: renders `ComparisonShelfPage` (full-width single column).  

**Owner:** Frontend Agent  
**Effort:** M (4–8 hours — Gen 1 component scaffold, RTL validation, mobile layout review)  
**Dependency:** GAP-06 (route must exist to test the component end-to-end)

**Note:** This is the reference implementation for future categories. It must be built strictly to Gen 1 patterns — no Gen 0 components, no framework vocabulary in rendered text, no sheet/modal expansion, no score chip color variation.

---

### GAP-08 — Hebrew Category Copy

**What is missing:** Consumer-facing Hebrew text for three slots:

| Slot | Field | Constraint |
|---|---|---|
| `<title>` + `<meta description>` | metadata in `hummus.ts` | Title ≤60 chars, description ≤155 chars |
| CategoryHero | `hero.tagline` | Single sentence, max 280px mobile, no statistics |
| CategoryPrologue | `prologue.sentences[]` | 2–3 sentences, consumer vocabulary, no framework terms |
| MethodologyFooter | `methodology.text` | 2–4 sentences, 12px display, explains the comparison without BSIP vocabulary |

**Example target:**

- Meta title: `השוואת חומוס — 2026 | ברי`
- Meta description: `בדקנו 69 מוצרי חומוס ישראלים לפי הרכב הרכיבים. גלה מה מסתתר מאחורי הסיר.` (97 chars)
- Hero tagline: `בדקנו 69 מוצרי חומוס ישראלים — ולא כולם מה שהם נראים`
- Prologue: Context on the Israeli hummus market, what makes structural quality in hummus (chickpea-first, tahini presence, additive load), how many products reviewed.
- Methodology: What the score reflects (ingredient structure, processing level) without BSIP, NOVA, cap, floor vocabulary.

**Owner:** Content Agent  
**Effort:** S (2–4 hours — Hebrew writing + leakage check)  
**Dependency:** GAP-02 must be started (Content Agent needs product names and distribution for accurate prologue claims)

---

### GAP-09 — Product Insight Lines (69 products)

**What is missing:** `insightLine` field for all 69 products in the frontend dataset.

The insight line is a brief Hebrew phrase below the product name in the comparison table. It describes the product, not the scoring mechanism. It must not use framework vocabulary.

Examples:
- `חומוס עם פחמימות נמוכות ורכיבים פשוטים`
- `מטבוחה עשירה בעגבניות, ללא חומרים משמרים`
- `חומוס קל עם ממתיקים מלאכותיים — בדוק את הרשימה`

**Volume:** 69 insight lines. This is the highest-effort content task.

**Owner:** Content Agent  
**Effort:** L (16–24 hours — 69 individual lines, each requiring review of BSIP2 trace for accuracy)  
**Dependency:** GAP-02 (frontend dataset must exist with scores/signals for accuracy) + Nutrition Agent accuracy review

---

### GAP-10 — QA Audit

**What is missing:** QA Agent review of the live hummus comparison page before go-live approval.

**Scope of QA audit:**
- All 69 product rows render correctly (name, score chip, insight line)
- Expansion sections render (nutrition, ingredients, signals)
- Filters work (at minimum: "הכל", score tier)
- Mobile layout: row height ≤ 80px collapsed, image 48px, RTL correct
- Desktop layout: two-column renders at `lg:` breakpoint
- No Gen 0 patterns in rendered output (no grade color chips, no sheet expansion)
- No framework vocabulary in any rendered text
- Meta title and description present and correct in `<head>`
- `hreflang="he"` present
- `dir="rtl"` present
- Structured data (`ItemList`) present if implemented

**Owner:** QA Agent  
**Effort:** S (2–4 hours)  
**Dependency:** GAP-07 + GAP-09 (page and all content must be complete before QA)

---

### GAP-11 — Product Agent Go-Live Approval

**What is missing:** Product Agent final approval to make `/hashvaot/hummus` publicly accessible.

**Inputs required:**
- QA Agent PASS verdict (GAP-10)
- Content Agent copy approval from Nutrition Agent (accuracy) and Product Agent (positioning)
- Data Agent confirmation that run_hummus_002 is the authoritative source for the live dataset

**Owner:** Product Agent  
**Effort:** Decision (no implementation)  
**Dependency:** GAP-10 PASS

---

## Dependency Graph

```
GAP-01 (Decision: fat data)
    ↓
GAP-02 (Build frontend JSON)  ←──────────────── GAP-08 starts in parallel
    ↓
GAP-03 (Copy JSON to website repo)
    ↓
GAP-04 (Create hummus.ts)
    ↓
GAP-05 (Update registry)
    ↓
GAP-06 (Create route page)
    ↓
GAP-07 (Create comparison component)
    ↓                ↑
GAP-09 (Insight lines) ←── depends on GAP-02 (data), feeds into GAP-10
    ↓
GAP-10 (QA audit)
    ↓
GAP-11 (Go-live approval)
```

GAP-08 (category copy) can start as soon as GAP-02 is underway — the prologue needs product counts, which are known (69).

---

## Effort Total

| Owner | Gaps | Total effort |
|---|---|---|
| Product Agent | GAP-01, GAP-11 | Decisions only |
| Data Agent | GAP-02, GAP-03 | M + XS = ~8–16 hours |
| Frontend Agent | GAP-04, GAP-05, GAP-06, GAP-07 | S + XS + S + M = ~8–14 hours |
| Content Agent | GAP-08, GAP-09 | S + L = ~18–28 hours |
| QA Agent | GAP-10 | S = ~2–4 hours |
| Nutrition Agent | Review GAP-09 | S = ~2–3 hours |
| **Total** | **11 gaps** | **~38–65 hours** |

The bottleneck is GAP-09 (69 insight lines). This is the longest single task and gates QA. Content Agent should begin drafting insight lines as soon as BSIP2 traces from run_hummus_002 are accessible.
