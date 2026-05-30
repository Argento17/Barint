# Frontend Dataset Schema — real_bread_retail_002_v2

**File:** `real_bread_retail_002_v2_frontend_dataset.json`
**Source:** Shufersal real-shelf scrape → BSIP0 → BSIP1 → BSIP2 pipeline
**Date:** 2026-05-25

This file is the ONLY frontend truth source for Cursor. Do not read raw BSIP2 reports directly.

---

## Top-Level Structure

```json
{
  "dataset_meta":      {},   // corpus metadata and caveats
  "featured_products": [],   // 10–15 curated display-safe products
  "products":          [],   // all 108 in-scope products (full schema)
  "comparisons":       [],   // pre-built comparison pairs
  "insights":          {},   // verified statistics for UI widgets
  "homepage_sections": {}    // pre-grouped product sets for page rendering
}
```

---

## dataset_meta

| Field | Type | Description |
|:------|:-----|:------------|
| `run_id` | string | Pipeline run identifier |
| `snapshot_date` | string | ISO date of scrape |
| `source_retailer` | string | Retailer name (Hebrew) |
| `source_retailer_en` | string | Retailer name (English) |
| `total_scraped` | int | Raw products scraped from Shufersal |
| `in_scope` | int | Products entering scoring pipeline |
| `excluded` | int | Out-of-scope products removed |
| `verified_products` | int | Products with full nutrition + ingredients |
| `nutrition_coverage_pct` | int | % products with nutrition data |
| `ingredient_coverage_pct` | int | % products with ingredient text |
| `avg_fiber_verified` | float | Average fiber in verified products (g/100g) |
| `caveats` | string[] | Mandatory display caveats |
| `mandatory_framing_he` | string | Hebrew required framing text |
| `mandatory_framing_en` | string | English required framing text |

---

## products[] — per-product fields

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Canonical product ID (`shufersal_<barcode>`) |
| `name_he` | string | Hebrew product name from Shufersal |
| `category` | string | Router category: `bread`, `cracker`, `crispbread`, `default` |
| `category_label_he` | string | Display label in Hebrew |
| `score` | int\|null | BSIP2 score (0–100). Null if not displayable |
| `grade` | string\|null | Letter grade A–E. Null if INSUFFICIENT |
| `displayable` | bool | True if CAUTIOUS/FULL degradation + ingredient text |
| `confidence_label_he` | string | Always set: נתונים חלקיים / חסרים נתונים מהותיים / לא מספיק לניתוח ודאי |
| `confidence_level` | string | `verified`, `partial`, or `insufficient` |
| `fiber_g` | float\|null | Dietary fiber per 100g |
| `protein_g` | float\|null | Protein per 100g |
| `sodium_mg` | float\|null | Sodium per 100g in mg |
| `energy_kcal` | int\|null | Energy per 100g in kcal |
| `fermentation_real` | bool | Genuine fermentation detected in ingredients |
| `fermentation_mismatch` | bool | Name claims מחמצת but ingredients show industrial yeast |
| `fiber_laundering` | bool | Fiber ≥5g but sourced from isolated additives |
| `seed_halo` | bool | Seeds present but no whole grain base |
| `whole_grain` | bool | Whole grain keywords detected in ingredients |
| `ingredient_visibility` | string | `full`, `partial`, or `none` |
| `image_url` | string | Primary Shufersal Cloudinary image URL |
| `source_url` | string | Direct Shufersal product page URL |
| `key_flags` | string[] | Human-readable Hebrew flags for display |
| `short_summary_he` | string | 1–3 sentence consumer-facing Hebrew summary |
| `ingredient_architecture_summary` | string | Brief Hebrew description of ingredient structure |
| `comparison_tags` | string[] | Tags for comparison grouping logic |

---

## featured_products[]

Subset of top-scored displayable products. Fields: `id`, `name_he`, `category`,
`category_label_he`, `score`, `grade`, `confidence_label_he`, `image_url`, `source_url`,
`fiber_g`, `fermentation_real`, `key_flags`, `short_summary_he`,
`ingredient_architecture_summary`.

Only `displayable=true` products appear here.

---

## comparisons[]

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Comparison identifier |
| `title` | string | Hebrew title for comparison card |
| `narrative` | string | Hebrew explanatory text |
| `left_product_id` | string | Product ID (usually the "better" example) |
| `right_product_id` | string | Product ID (the contrast) |
| `key_difference` | string | Single-line summary of the difference |
| `visual_direction` | string | `left_wins`, `right_wins`, or `neutral` |

---

## insights{}

Sub-objects:
- `fermentation` — genuine count, mismatch count, industrial count
- `fiber` — average, extremes, top/bottom product IDs
- `seed_halo` — count, narrative
- `fiber_laundering` — count, narrative
- `transparency` — verified vs total, no-data count
- `confidence_distribution` — verified/partial/insufficient counts
- `grade_distribution_verified` — A/B/C/D counts for verified products
- `whole_grain` — count of verified whole-grain products
- `sodium` — high sodium product count

All numbers are derived from real data. Safe to display.

---

## homepage_sections{}

| Key | Description |
|:----|:------------|
| `strongest_verified` | Top 8 verified products — for homepage hero / ranking widget |
| `interesting_patterns` | Products with fiber_laundering / seed_halo / fermentation_mismatch |
| `fermentation_examples` | `genuine[]` and `mismatch[]` product lists |
| `fiber_spectrum` | `high_end[]` and `low_end[]` — for fiber range visualization |
| `structural_examples` | `whole_grain_strong[]` and `refined_base[]` |
| `blog_titles_he` | Suggested Hebrew blog title options |
| `mandatory_framing_he` | Required transparency text in Hebrew |
| `mandatory_framing_en` | Required transparency text in English |

---

## Confidence Display Rules

| `confidence_level` | Score shown? | Grade shown? | UI note |
|:------------------|:-------------|:-------------|:--------|
| `verified` | Yes | Yes | Show grade badge |
| `partial` | Provisional | Provisional | Add asterisk or disclaimer |
| `insufficient` | No | No | Show label only |

## Score Display Rule

Only show score and grade for products where `displayable = true`.
Products with `displayable = false` should show the `confidence_label_he` only.
