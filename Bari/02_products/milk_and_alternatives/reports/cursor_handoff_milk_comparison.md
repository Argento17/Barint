# Cursor Handoff: `/hashvaot/milk-comparison` Page

**Date:** 2026-05-20  
**Author:** Claude Code (Bari internal toolchain)  
**Purpose:** Complete implementation context for Cursor to build Bari's first flagship comparison intelligence page.

---

## CRITICAL CONTEXT FIRST

**There is no frontend.** `C:\Bari\04_frontend\` does not exist. No React, no package.json, no components, no design system, no routing, no build tooling. This comparison page is the **first** page — Cursor must choose stack, initialize the project, and build everything from scratch.

All data artifacts (BSIP0/1/2 outputs) are complete and production-ready. The intelligence layer is done. The frontend layer is entirely missing.

---

## 1. Product Image Sources

### What exists
Product images were scraped during BSIP0 for **Yohananof only** (snack bars dataset). Milk products were not scraped with image downloads.

**Scraped image path pattern (Yohananof/snack bars only):**
```
C:\Bari\03_operations\bsip0\scrape\yohananof\outputs\yohananof\{barcode}\product_image.jpg
```

### For milk products — use `image_url` from BSIP1 JSON
Every BSIP1 product record contains an `image_url` field pointing to the live CDN URL. Example from `bsip1_7290000051352.json` (Tnuva whole milk):
```json
"image_url": "https://api.yochananof.co.il/media/catalog/product/{path}/image.jpg"
```

**Action for Cursor:** On page render, fetch `image_url` from the BSIP2 trace (which inherits it from BSIP1). Do NOT attempt to serve images locally — use the CDN URL directly. Add `loading="lazy"` and a fallback placeholder for products where `image_url` is null or CDN returns 404.

### Product visual catalog
13 PNG comparison visuals are pre-generated in:
```
C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\
```
These are static analysis charts (not product photos). They can be embedded in an "Analysis" section of the page if desired, but are not required for the MVP comparison card layout.

---

## 2. Milk / Product Datasets

### Canonical products for this page

From `C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\website_candidates.md`:

| Barcode | Product | Score | Grade | Category |
|---------|---------|-------|-------|----------|
| `7290000051352` | Whole Milk 3.4% Tnuva | 75.0 | B | dairy_milk |
| `7394376619939` | Oat Barista Drink (Oatly) | 48.8 | D | plant_milk |
| `7290116936116` | Soy Drink unsweetened 1L | 66.1 | C | plant_milk |
| `5411188112709` | Alpro Almond Drink unsweetened | 43.4 | D | plant_milk |
| `7290110324773` | Go Milk Protein 27g | 39.5 | E | dairy_milk_engineered |
| `8000215204219` | Vitariz organic rice drink | ~45 | D | plant_milk |

The page comparison story (from `website_candidates.md`) is: **"Whole milk vs. plant alternatives — what the label doesn't tell you."** The narrative arc is that whole dairy milk (simple, two ingredients) outscores heavily engineered plant drinks despite the plant drinks' marketing claims.

### BSIP1 source files (enriched product records)

**Primary dataset — 20 products with full semantic enrichment:**
```
C:\Bari\03_operations\bsip1\run_milk_002\output\bsip1_{barcode}.json
```

**Secondary dataset — 8 products, older run, less enrichment:**
```
C:\Bari\02_products\milk_and_alternatives\canonical_bsip1\run_001\bsip1_{barcode}.json
```

**Use `run_milk_002` as the authoritative source.** It has the full enrichment fields (`extracted_additives`, `extracted_sweeteners`, `extracted_matrix_markers`, `extracted_protein_markers`, `extracted_fermentation_markers`, `enrichment_summary`).

### BSIP1 record schema (key fields)

```json
{
  "file_type": "product",
  "canonical_product_id": "7290000051352",
  "canonical_name_he": "חלב מלא 3.4%",
  "product_name_he": "...",
  "barcode": "7290000051352",
  "image_url": "https://...",
  "ingredients_raw": "...",
  "ingredient_order": [
    {"position": 1, "text": "חלב", "percentage_declared": null, "has_subgroup": false}
  ],
  "extracted_additives": [],
  "extracted_sweeteners": [],
  "extracted_protein_markers": [],
  "extracted_matrix_markers": [],
  "extracted_fermentation_markers": [
    {"term": "live_cultures", "category": "live_cultures"}
  ],
  "enrichment_summary": {
    "additive_count": 0,
    "sweetener_count": 0,
    "has_live_cultures": true,
    "has_flavor_descriptor": false,
    "has_prebiotic_fiber": false,
    "has_protein_isolate_or_concentrate": false
  },
  "nutrition": {
    "energy_kcal": 62,
    "protein": 3.2,
    "fat": 3.4,
    "carbs": 4.7,
    "sugar": 4.7,
    "saturated_fat": 2.2,
    "fiber": 0,
    "sodium": 0.044
  }
}
```

---

## 3. Relevant BSIP Outputs

### BSIP2 scored traces (primary data for the page)

**Path pattern:**
```
C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_004_recalibrated\products\{barcode}\bsip2_trace.json
```

Each `bsip2_trace.json` is ~400-500 lines of structured scoring output. Key fields to surface on the page:

```json
{
  "canonical_product_id": "7290000051352",
  "bsip2_score": 75.0,
  "bsip2_grade": "B",
  "bsip2_grade_label": "טוב",
  "dimensions": {
    "processing_quality": {"score": 82, "display_name": "איכות עיבוד"},
    "nutrient_density": {"score": 71, "display_name": "צפיפות תזונתית"},
    "protein_quality": {"score": 78, "display_name": "איכות חלבון"},
    "additive_quality": {"score": 100, "display_name": "עומס תוספים"},
    "fat_quality": {"score": 65, "display_name": "איכות שומן"},
    "glycemic_quality": {"score": 80, "display_name": "עומס גליקמי"},
    "whole_food_integrity": {"score": 95, "display_name": "שלמות מזון"}
  },
  "signals": {
    "nova_proxy": 1,
    "red_labels": [],
    "compensation_signals": []
  },
  "matrix_integrity": {
    "matrix_integrity_score": 97,
    "reconstruction_depth": 0,
    "structural_degradation_level": "minimal",
    "engineering_intensity": 0,
    "dominant_matrix_signals": [],
    "integrity_summary": "..."
  }
}
```

**Note:** `matrix_integrity` block may not yet be embedded in `run_004` traces. It is computed separately by `C:\Bari\03_operations\bsip2\proto_v0\src\matrix_integrity.py`. Cursor should either: (a) run matrix_integrity.py against the 6 target products and embed the output, or (b) call it at build time and write a static JSON. Do NOT compute it at runtime in the browser.

### Matrix Integrity Engine

**Source:** `C:\Bari\03_operations\bsip2\proto_v0\src\matrix_integrity.py`  
**Interface:** `compute_matrix_integrity(bsip1_product: dict) -> dict`  
**Input:** A BSIP1 JSON record  
**Output fields (already listed in section 3 above under `matrix_integrity` block)**

To generate matrix integrity data for the 6 page products:
```
cd C:\Bari\03_operations\bsip2\proto_v0\src
python run_matrix_validation.py
```
The validation runner already processes `run_milk_002`. Extract the 6 target barcodes from the output.

### Existing analysis reports (optional page content)

```
C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\executive_summary.md
C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\full_comparison_report.md
C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\website_candidates.md
```

The `website_candidates.md` has pre-written comparison narrative text that can be adapted directly for page copy. Read it before writing any UI copy.

---

## 4. Reusable Components

**There are none.** No frontend exists. Build everything from scratch.

**Recommended components to create:**

### `ProductCard`
Props: `{ barcode, name_he, image_url, score, grade, grade_label, nova_proxy, red_labels }`  
Displays: product image, Hebrew name, circular score badge with grade color, NOVA indicator, red label icons.

### `DimensionRadar` or `DimensionBar`
Props: `{ dimensions: { [key]: { score, display_name } } }`  
Choose bar chart over radar for Hebrew RTL readability. Dimensions displayed in Hebrew using `display_name` from the BSIP2 trace (see Section 3).

### `MatrixIntegrityBadge`
Props: `{ score, level, reconstruction_depth, dominant_signals }`  
Small badge showing `structural_degradation_level` with color coding. Tooltip expands to show `dominant_matrix_signals` list.

### `ComparisonGrid`
Props: `{ products: ProductCard[] }`  
RTL-aware grid. On mobile: vertical scroll, 1 card. On tablet: 2 columns. On desktop: 3 columns. Sorted by score descending by default.

### `SignalExplainer`
Props: `{ signal_key, value }`  
Tooltip/popover that explains what each signal means in plain Hebrew. Use `ui_language.md` for all copy (Section 6 below).

### `RedLabelIcon`
Props: `{ label_type }` where `label_type` ∈ `{ sugar, saturated_fat, sodium }`  
Renders the Israeli octagon red label icon. Thresholds: sugar >17.5g, sat_fat >5g, sodium >600mg per 100g.

---

## 5. Existing Comparison UX

**There is no existing comparison UX.** This is the first page.

**What the page MUST do (from `website_candidates.md` comparison story):**

1. Show the 6 products side-by-side (or in a sortable grid)
2. Make the score/grade the most prominent visual element
3. Surface NOVA proxy as a secondary signal ("רמת עיבוד")
4. Surface red labels as warning icons
5. Allow drilling into dimension breakdown (either inline or in a modal/expanded card)
6. Explain WHY the score is what it is — not just what it is. Tnuva whole milk gets B not A because of saturated fat quality. Show that.
7. Surface matrix integrity as a new "structural" insight distinct from the score

**Story angle to build toward (from website_candidates.md):**  
Lead with the headline: "חלב מלא מנצח — למה שתיית הצמחים 'הבריאה' מקבלת ציון נמוך יותר?"  
(Whole milk wins — why does the 'healthy' plant drink score lower?)

---

## 6. Design System Notes

**Source of truth for all UI language:** `C:\Bari\01_framework\bsip2_framework\ui_language.md`

Key rules from that document:

### Grade labels (Hebrew)
| Grade | Score Range | Hebrew Label | Color |
|-------|-------------|--------------|-------|
| A | 85-100 | מצוין | #2E7D32 (dark green) |
| B | 70-84 | טוב | #558B2F (light green) |
| C | 55-69 | בינוני | #F9A825 (amber) |
| D | 40-54 | חלש | #EF6C00 (orange) |
| E | 0-39 | בעייתי | #C62828 (red) |

### Dimension display names (Hebrew)
| Key | Display |
|-----|---------|
| processing_quality | איכות עיבוד |
| nutrient_density | צפיפות תזונתית |
| protein_quality | איכות חלבון |
| additive_quality | עומס תוספים |
| fat_quality | איכות שומן |
| glycemic_quality | עומס גליקמי |
| whole_food_integrity | שלמות מזון |
| calorie_density | צפיפות קלורית |
| satiety_support | תמיכה בשובע |
| regulatory_quality | עמידה ברגולציה |

### Tone rules (from ui_language.md)
- Never say "healthy" (בריא) or "unhealthy" (לא בריא) — Bari does not make health claims
- Say "more processed" (מעובד יותר) not "worse"
- Say "structural degradation" (פירוק מבני) not "artificial"
- Scores describe structure and composition, not dietary advice
- "מידע, לא המלצה" is the product philosophy — information, not recommendation

### Layout
- **RTL required throughout** — Hebrew is the primary language
- Bari brand color: no official hex documented. Use a neutral dark (#1A1A2E or similar professional dark) for headers, white cards, grade colors as defined above.
- Font: Use a system Hebrew-capable sans-serif (e.g., `Noto Sans Hebrew`, or `system-ui` which covers Hebrew on modern browsers)
- No custom iconography library documented — use either Heroicons or Radix Icons (both work well with RTL)

---

## 7. Recommended Architecture For This Page

### Stack recommendation
Given no frontend exists and the data is static/pre-computed:

**Next.js 14 (App Router) with static generation** is the strongest fit:
- Israeli product data doesn't change daily — static site generation (SSG) is appropriate
- Server components for the heavy JSON reading at build time
- `generateStaticParams` for product-level pages if you add individual product pages later
- Built-in i18n support for Hebrew RTL (`dir="rtl"` in layout)
- Easy deployment on Vercel or as static export

**Alternative:** Astro — if the team wants even simpler static output with no React overhead. But Next.js gives more flexibility as Bari grows.

### Data loading strategy

**Build-time (recommended):** Read BSIP2 trace JSONs from disk during `getStaticProps` or in a Server Component. The 6 product traces total ~3MB — completely fine to bundle as static data.

Create a single aggregated JSON at build time:
```
C:\Bari\02_products\milk_and_alternatives\reports\milk_comparison_page_data.json
```

Structure:
```json
{
  "generated_at": "2026-05-20T...",
  "comparison_title": "השוואת חלב ואלטרנטיבות",
  "story_angle": "...",
  "products": [
    {
      "barcode": "7290000051352",
      "name_he": "חלב מלא 3.4%",
      "image_url": "...",
      "score": 75,
      "grade": "B",
      "grade_label": "טוב",
      "nova_proxy": 1,
      "red_labels": [],
      "dimensions": {...},
      "matrix_integrity": {...},
      "ingredients_display": "חלב",
      "key_insight": "מרכיב אחד. ציון גבוה."
    }
  ]
}
```

**Write a Python script** (`build_page_data.py`) that:
1. Reads the 6 BSIP2 trace JSONs
2. Reads the 6 BSIP1 enrichment JSONs
3. Runs `compute_matrix_integrity()` on each
4. Merges into the page data JSON
5. Can be re-run whenever scores change

### Page structure

```
/hashvaot/milk-comparison
├── Hero section: headline + comparison story teaser
├── ComparisonGrid: 6 ProductCards sorted by score
├── DimensionBreakdown: radar/bar for selected product (click-to-expand)
├── MatrixIntegrity section: "מה הרכיבים אומרים"
├── RedLabel summary: "כמה מוצרים עוברים את הסף האדום"
└── Footer: "מה זה ציון בארי?" + methodology link
```

### File structure to create

```
C:\Bari\04_frontend\
├── package.json
├── next.config.js
├── app/
│   ├── layout.tsx          (RTL, Hebrew font, global styles)
│   ├── page.tsx            (landing/redirect)
│   └── hashvaot/
│       └── milk-comparison/
│           └── page.tsx
├── components/
│   ├── ProductCard.tsx
│   ├── ComparisonGrid.tsx
│   ├── DimensionBar.tsx
│   ├── MatrixIntegrityBadge.tsx
│   ├── RedLabelIcon.tsx
│   └── SignalExplainer.tsx
├── lib/
│   └── types.ts            (TypeScript interfaces for BSIP2 trace schema)
├── data/
│   └── milk_comparison.json  (pre-built, checked in)
└── public/
    └── images/             (optional local fallback images)
```

---

## 8. Missing Pieces / Risks

### High severity

1. **No frontend infrastructure at all.** Stack choice, package.json, build pipeline, deployment — all must be decided and initialized before writing a single component. Suggest starting with `npx create-next-app@latest` with TypeScript + Tailwind.

2. **Matrix integrity not embedded in run_004 traces.** The `matrix_integrity.py` module was written AFTER `run_004_recalibrated`. Cursor must either re-run BSIP2 with the new module integrated, or generate matrix integrity separately and merge at build time. The latter (merge at build time via Python script) is faster and lower risk.

3. **Plant drink barcodes may not be in run_milk_002.** The Oatly, Alpro, and Vitariz products are non-Israeli brands. Their BSIP1 records exist in `run_milk_002` but their image CDN URLs may be from a different retailer's API and could 404. Verify each `image_url` before going live.

### Medium severity

4. **No design spec.** The grade color table and tone rules exist in `ui_language.md` but there is no Figma, no spacing system, no component spec. Cursor is designing AND building. Keep it minimal for the first version — don't try to make it beautiful, make it clear.

5. **Score changes are possible.** BSIP2 calibration is ongoing (currently `run_004_recalibrated`). If scores shift, the page data must be rebuilt. The Python build script (recommended in Section 7) makes this a one-command operation.

6. **Hebrew font loading.** Server-side rendering with Next.js + Google Fonts (Noto Sans Hebrew) works well, but font must be explicitly configured. Do NOT rely on system fallback for production — Hebrew rendering varies wildly across devices without an explicit font.

### Low severity

7. **No sorting/filtering UX spec.** The `website_candidates.md` implies a specific ordering (by score, dairy first, then plant alternatives). If the page needs filtering by category (dairy/plant), that's an additional component not described here. Start with fixed ordering.

8. **Red label thresholds are per-100g.** When displaying red labels for milk, note that the standard Israeli serving size for milk is 240ml (~247g). A product might not trigger a red label per 100g but could be relevant per serving. The BSIP2 trace computes per-100g. Decide which basis to display and be consistent.

9. **`run_003_final` vs `run_004_recalibrated`.** The `website_candidates.md` report was generated from `run_003_final`. The authoritative scores are now in `run_004_recalibrated`. Scores may differ slightly. Always use `run_004_recalibrated` for the actual page — the `website_candidates.md` file is for narrative/story context only, not for exact score display.

---

## Quick-start checklist for Cursor

- [ ] Read `C:\Bari\02_products\milk_and_alternatives\reports\run_003_final\website_candidates.md` — understand the story before writing code
- [ ] Read `C:\Bari\01_framework\bsip2_framework\ui_language.md` — understand all language rules before writing any copy
- [ ] Run `python C:\Bari\03_operations\bsip2\proto_v0\src\run_matrix_validation.py` to regenerate matrix integrity data
- [ ] Write `build_page_data.py` to merge BSIP2 trace + matrix integrity for the 6 products into `milk_comparison.json`
- [ ] Initialize Next.js in `C:\Bari\04_frontend\`
- [ ] Build `ProductCard` with grade color + image fallback first — validate it against the 6 products
- [ ] Verify all 6 `image_url` fields return 200 before going live
- [ ] Test RTL layout on mobile — Hebrew text reflow is the most common failure mode

---

*Document generated 2026-05-20 by Claude Code (Bari internal toolchain)*  
*All data paths are Windows absolute paths. All BSIP data is pre-computed — no runtime API calls to Bari backend required.*
