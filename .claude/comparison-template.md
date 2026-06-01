# Bari Comparison Template â€” Implementation Guide

**Authority document:** `C:\Bari\01_framework\frontend\comparison_template_v1.md`  
**Build sequence:** `C:\Bari\01_framework\frontend\component_build_sequence_v1.md`  
**Handoff protocol:** `C:\Bari\01_framework\frontend\cursor_handoff_protocol_v1.md`  
**Last verified:** 2026-05-30

This document is the implementation reference for adding a new category comparison page.

---

## Bari Repository Map â€” TWO SEPARATE LOCATIONS

Implementation in this guide spans **both** repos. Know which is which.

| Repo | Path | Role in a category build |
|------|------|--------------------------|
| **Website repo** | `C:\bari-web` | Where you build the page: components, routes, registry, the consumed frontend JSON, lint, build |
| **Product / data workspace** | `C:\Bari` | Where the data comes from: BSIP2 scoring, `build_frontend_dataset.py`, the source JSON before it is copied over |

- Page/component/route/registry implementation, lint, build â†’ **`C:\bari-web`**.
- BSIP2 scoring run + JSON generation â†’ **`C:\Bari\03_operations\`**, output then copied to `C:\bari-web\src\data\comparisons\`.
- **Never assume `C:\Bari` is the website repo.** Before implementing the page, **confirm the working directory is `C:\bari-web`**.

---

## Canonical Page Structure

Every comparison page has exactly 4 sections. No additions.

```
[1] CategoryHero        src/components/shared/category-hero.tsx
[2] CategoryPrologue    src/components/shared/category-prologue.tsx
[3] ProductTable        src/components/shared/product-table.tsx
[4] MethodologyFooter   src/components/shared/methodology-footer.tsx
```

---

## Canonical Components

All shared canonical components are in `src/components/shared/`. No new canonical component goes anywhere else.

### ScoreChip (`score-chip.tsx`)

- Background: `#F7F7F2` for ALL grades (A through E) â€” never varies
- Border: `rgba(17,19,24,0.10)` â€” never varies
- Content: `{numeric}/{grade}` e.g. `"72/B"` â€” no label text, no color change
- Font size: 28px (from token `layout.scoreChipSize`)
- Null score: chip renders `"â€”"`, background `#EEEEEA`

### ProductRow (`product-row.tsx`)

- Collapsed height: 72px (max 80px)
- Product image: 56Ã—56px
- Score chip: top-right of row
- Insight line: 13px, `#444444`, 1 line, â‰¤12 Hebrew words
- Alternating backgrounds: via `bari-zebra-rows` CSS class
- No border on the row element
- Tap/click anywhere on row toggles expansion

### ExpansionSection (`expansion-section.tsx`)

- Inline only â€” never sheet, modal, overlay, or portal
- Content order (fixed): nutrition grid â†’ ingredient list â†’ confidence row
- Nutrition: 5 fields only â€” calories / protein / sugar / fat / sodium (per 100g)
  - Label constants: `×§×§"×œ`, `×—×œ×‘×•×Ÿ ×’'`, `×¡×•×›×¨×™× ×’'`, `×©×•×ž×Ÿ ×’'`, `×¡×™×‘×™× ×’'`, `× ×ª×¨×Ÿ ×ž"×’`
  - `null` field â†’ hide cell entirely; `0` is valid â†’ display it
- Ingredient list: verbatim, Hebrew, clip at 4 lines, `"×”×¦×’ ×”×›×œ"` to expand
- Confidence row: `confidenceLabel` from VM (left) + `"×¡×’×•×¨"` button (right)
- No heading tags inside expansion
- No framework terms: NOVA, BSIP, cap, structural_class, matrix_integrity, pillar, dimension
- No `"×ž×” ×ž×¢×œ×”/×ž×•×¨×™×“ ××ª ×”×¦×™×•×Ÿ"` score attribution
- Max expanded height: 280px

### ProductTable (`product-table.tsx`)

- Products arrive pre-sorted (score descending, insufficient last) â€” UI never re-sorts
- 3+ rows visible at 0px scroll (375px viewport)
- One optional highlighted comparison pair: visual bracket + single driver line (â‰¤15 Hebrew words)
- Maximum 1 highlighted pair per page. Omit if no clearly strongest pair.
- Filter wired to table â€” reduces rows without page reload

### CategoryHero (`category-hero.tsx`)

- Max total height: 280px on 375px mobile viewport
- One sentence, max 12 Hebrew words, names one shelf observation
- One product image (320px desktop, 160â€“180px mobile)
- Score visible on load â€” no animation, no delay
- No aggregate statistics, no animated elements, no eyebrow text in English

### CategoryPrologue (`category-prologue.tsx`)

- 3â€“5 sentences, hard limit
- Calm declarative tone, no bullet points
- Every sentence is a verifiable shelf observation
- Does not repeat hero sentence; does not preview findings

### MethodologyFooter (`methodology-footer.tsx`)

- Plain text â€” no `<h2>/<h3>`, no border, no card, no background
- Font: 12px, color `#AAAAAA`
- 2â€“4 sentences maximum
- Contains: product count, data source, "scores are relative to category", link to full methodology
- Does NOT contain: score mechanics, NOVA, dimension names, cap/floor logic

### StickyFilterButton

- Invisible at 0px scroll
- Appears after 300px scroll, fixed bottom-right, 16px from edges
- Triggers filter panel (max 3 dimensions, single-select, Hebrew labels)
- No count badge, no pre-label
- Filter panel: full-screen modal on mobile, dismisses with Apply

---

## Route Structure for a New Category

1. **Create page file:**
   ```
   src/app/hashvaot/{category}/page.tsx
   ```

2. **Create page component:**
   ```
   src/components/comparisons/{category}-comparison-page.tsx
   ```
   Use `maadanim-comparison-page.tsx` as the canonical reference.

3. **Create page data module:**
   ```
   src/lib/comparisons/{category}-page-data.ts
   ```
   Exports: products (BariProductVM[]), corpusMeta, hero, prologueSentences, methodologyLines, metadata.

4. **Create shelf filters:**
   ```
   src/lib/comparisons/{category}-shelf-filters.ts
   ```
   Exports: `CATEGORY_SHELF_LENS_OPTIONS` and `filter{Category}Products()`.

5. **Register the category:**
   ```
   src/lib/comparisons/registry/categories/{category}.ts
   src/lib/comparisons/registry/index.ts  (add to registry object)
   ```

6. **Add frontend JSON:**
   ```
   src/data/comparisons/{category}_frontend_v1.json
   ```

---

## Data Flow for a New Category

```
C:\Bari\02_products\{category}\intelligence_bsip2\
    â†“  build_frontend_dataset.py
{category}_frontend_vN.json   (in 02_products/{category}/ or 03_operations/outputs)
    â†“  copy to
src/data/comparisons/{category}_frontend_vN.json
    â†“  corpus.ts loadComparisonCorpus()
BariProductVM[]
    â†“  {category}-page-data.ts
ComparisonCategoryPageData
    â†“  {category}-comparison-page.tsx
UI rendered page
```

The transformation from raw JSON to `BariProductVM` happens in `{category}-page-data.ts` via `corpus.ts`. The UI receives only `BariProductVM` â€” no raw BSIP fields.

---

## Content Generation Workflow (per category)

### Step 1 â€” Data prerequisites
- BSIP2 run complete
- Batch summary reviewed, false positives removed
- Minimum 30 scored products in editorial scope

### Step 2 â€” Hero sentence
Identify the single most surprising product (known brand, unexpected score, or "healthy" product below average).  
Write one Hebrew sentence â‰¤12 words naming the product and the observation.

### Step 3 â€” Prologue
Answer in â‰¤5 sentences total:
1. What products are on this shelf?
2. What did we look at?
3. What is not obvious from the front of the package?

### Step 4 â€” Highlighted pair (optional)
Identify the single clearest score gap between two comparable products.  
Write one driver line â‰¤15 Hebrew words, observational.  
If no clearly strongest pair exists: **omit entirely**.

### Step 5 â€” Insight lines
One per product, â‰¤12 Hebrew words. Must be independently observable (not a score explanation).

Approved forms:
- `"×¨×©×™×ž×ª ×¨×›×™×‘×™× ×§×¦×¨×” ×ž-5 ×ž×¨×›×™×‘×™×"`
- `"10 ×’×¨× ×—×œ×‘×•×Ÿ ×œ-100 ×’×¨×"`
- `"×ž×•×¦×¨ ×”×“×™××˜ ×¢× ×™×•×ª×¨ ×ª×•×¡×¤×™× ×ž×”×’×¨×¡×” ×”×¨×’×™×œ×”"`

Forbidden forms:
- Any causal explanation of the score
- "×ž×•×¦×¨ ×œ× ×‘×¨×™×" / "×›×“××™ ×œ×”×™×ž× ×¢" / "×”×¦×™×•×Ÿ × ×ž×•×š ×›×™..."

### Step 6 â€” Filter configuration
2â€“3 filter dimensions. Hebrew consumer labels (not internal cluster names).

Examples:
- Not: `milky_style` â†’ Use: `"×ž×™×œ×§×™ ×•×“×•×ž×™×”×"`
- Not: `whole_grain_sourdough` â†’ Use: `"×œ×—× ×©××•×¨"`

Grade filter values: B / C / D / E only (no numeric ranges, no adjectives).

### Step 7 â€” Methodology text
2â€“4 sentences. No framework terms. No score mechanics. No NOVA.

### Step 8 â€” Leakage + drift check (before launch)

**Leakage checklist:**
- [ ] No filter label contains a framework term
- [ ] No row insight explains the score mechanism
- [ ] Methodology section does not name any dimension
- [ ] Hero/prologue contain no NOVA, cap, or routing language
- [ ] Expanded row shows only nutrition, ingredients, data note, confidence
- [ ] Highlighted pair driver line references no framework logic

**Drift warning signs (remove if present):**
- Chart or visualization above first product row
- User must make a choice before seeing any product
- Summary statistic before product rows
- Color-coding that encodes score
- Multiple filter dimensions open by default
- Score with verbal interpretation beside it

---

## Filter Specification per Category Type

| Category | Filter 1 | Filter 2 | Filter 3 |
|---|---|---|---|
| ×ž×¢×“× ×™× | ×¡×•×’ ×ž×•×¦×¨ | ×¦×™×•×Ÿ | â€” |
| ×œ×—× | ×¡×•×’ ×œ×—× | ×¦×™×•×Ÿ | â€” |
| ×—×˜×™×¤×™× | ×¡×•×’ ×—×˜×™×£ | ×¦×™×•×Ÿ | â€” |
| ×™×•×’×•×¨×˜×™× | ×¡×•×’ ×™×•×’×•×¨×˜ | ×¦×™×•×Ÿ | â€” |

Filter behavior:
- Single-select (radio)
- First option is always "×”×›×œ" (all)
- Count pre-computed, not dynamic
- "× ×§×”" (clear) shown only when 2+ filters active

---

## Public Language Rules

### Score display
- Primary: `72/B` â€” no suffix, no label, no color
- Do not map grades to adjectives
- Do not say "×¦×™×•×Ÿ ×’×‘×•×”" / "×¦×™×•×Ÿ × ×ž×•×š"

### Approved terms
| Concept | Public Hebrew |
|---|---|
| Score | ×¦×™×•×Ÿ |
| High processing | ×¨×ž×ª ×¢×™×‘×•×“ ×’×‘×•×”×” / ×ž×•×¦×¨ ×ž×¢×•×‘×“ |
| Additives | ×ª×•×¡×¤×™× |
| Short ingredient list | ×¨×©×™×ž×ª ×¨×›×™×‘×™× ×§×¦×¨×” |
| Protein | ×—×œ×‘×•×Ÿ (g amount) |
| Sugar | ×¡×•×›×¨ (g amount from label) |
| Confidence | × ×ª×•× ×™× ×ž×œ××™× / × ×ª×•× ×™× ×—×œ×§×™×™× |

### Forbidden terms (never appear publicly)
BSIP, NOVA, cap, floor, routing, dimension (processing_quality etc.), structural class, anchor, confidence band, framework, pipeline, ontology, "×ž×” ×ž×¢×œ×”/×ž×•×¨×™×“ ××ª ×”×¦×™×•×Ÿ"

---

## Component Approval Checkpoints (Build Gates)

| Checkpoint | Component | Hard gate |
|---|---|---|
| 1 | ScoreChip | STOP. Visual approval required before ProductRow |
| 2 | ProductRow | STOP. Visual approval required before ExpansionSection |
| 3 | ExpansionSection | STOP. Visual approval required before ProductTable |
| 4 | ProductTable | STOP. Visual approval required before full page assembly |
| 5 | Full page assembly | STOP. Full mobile QA + leakage + drift sweep before launch |

The `cursor_handoff_protocol_v1.md` defines exact QA checklists for each checkpoint.

---

## Excluded Elements (Do Not Add)

These were considered and excluded. Require explicit re-approval to introduce.

| Excluded | Reason |
|---|---|
| Score distribution chart | Analytics register, no consumer utility |
| Color-coded score chips | Creates good/bad framing |
| Dimension bars per product | Framework exposure |
| "Understanding the score" modal | Framework exposure risk |
| Radar/spider charts | Exposes dimension architecture |
| Category average benchmarks | Requires explanation |
| Animated score reveal | Disconnected from shelf-native feeling |
| Multiple comparison scenes | Hard to scale, theatrical |
| "Recommended" / "best" labels | Editorial claim too strong |

---

## Existing Canonical Reference

**First canonical category:** ×ž×¢×“× ×™×  
**Component:** `src/components/comparisons/maadanim-comparison-page.tsx`  
**Page data:** `src/lib/comparisons/maadanim-page-data.ts`  
**Filters:** `src/lib/comparisons/maadanim-shelf-filters.ts`  
**Registry:** `src/lib/comparisons/registry/categories/maadanim.ts`  
**Data:** `src/data/comparisons/maadanim_frontend_v2.json`

When implementing a new category, use the maadanim pattern as the template.

---

## Sources

- `C:\Bari\01_framework\frontend\comparison_template_v1.md`
- `C:\Bari\01_framework\frontend\component_build_sequence_v1.md`
- `C:\Bari\01_framework\frontend\cursor_handoff_protocol_v1.md`
- `C:\Bari\01_framework\frontend\comparison_view_model_v1.md`
- `C:\Bari\01_framework\frontend\architecture_generations_registry_v1.md`
- `C:\Bari\01_framework\bsip2_framework\ui_language.md`
- `C:\bari-web\src\components\comparisons\maadanim-comparison-page.tsx`
- `C:\bari-web\src\lib\comparisons\maadanim-page-data.ts`
- `C:\bari-web\src\lib\comparisons\registry\`
- `C:\bari-web\src\lib\view-models\index.ts`
