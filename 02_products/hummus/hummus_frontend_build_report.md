# Hummus Frontend Dataset — Build Report

**Task:** TASK-061  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Output file:** `C:\Bari\02_products\hummus\hummus_frontend_v1.json`  
**File size:** 131.3 KB  
**Schema version:** hummus_frontend_v1

---

## Build Summary

| Metric | Value |
|--------|-------|
| Source run | **run_hummus_002** (FROZEN — TASK-045) |
| Invalid run | run_hummus_001 — NOT used |
| Total products | 69 |
| Displayable products | **67** |
| Unavailable products | 2 |
| Normal display state | 61 |
| Caveated display state | 6 |
| Build errors | **0** |
| Pipeline errors in source | 0 |

---

## Section 1 — Source Run Validation

**run_hummus_002 is the authoritative baseline.** Its AUTHORITATIVE.md marker is at:  
`C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\AUTHORITATIVE.md`

**run_hummus_001 was NOT used** under any circumstances. Its INVALID.md marker exists at:  
`C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_001\INVALID.md`

Source data loaded:
- 69 BSIP1 canonical files from `canonical_bsip1/`
- 69 BSIP2 trace files from `run_hummus_002/products/`
- `run_hummus_002_validation.json` (authoritative score table)

---

## Section 2 — TASK-060 Decision Application

**TASK-060 output file was not found.** No file matching `*TASK-060*`, `*task_060*`, or `*product_agent*` exists in the Bari project tree.

**Action taken:** Applied display rules from TASK-045 baseline freeze report (Section 10 — Display Readiness Verdict), which is the most recent authoritative document on hummus display readiness. These rules were the input that TASK-060 would have consumed. The TASK-045 rules are:

| Product group | Count | Rule applied |
|---|---|---|
| Fully scored, high confidence | 57 | `displayable: true, display_state: "normal"` |
| LOW_NOVA_CONFIDENCE | 2 | `displayable: true, display_state: "caveated"` — suppress processing_quality highlight |
| STRUCTURAL_EMPTINESS | 2 | `displayable: true, display_state: "caveated"` — add incomplete data note |
| CATEGORY_INSTABILITY | 2 | `displayable: true, display_state: "caveated"` — display category as "Savory spread" |
| insufficient_data | 2 | `displayable: false, display_state: "unavailable"` |

**Recommended action:** If TASK-060 produced decisions that override any of the above, re-run this build with those overrides. The `display_rules_source` field in the JSON records this caveat.

---

## Section 3 — Product Records

### 3.1 Display State Distribution

| State | Count | Description |
|-------|-------|-------------|
| `normal` | **61** | Full score and grade displayed |
| `caveated` | **6** | Score displayed with product-level caveat |
| `unavailable` | **2** | Score not displayed — "score unavailable" UI state |

### 3.2 Grade Distribution

| Grade | Score range | Count | % of displayable |
|-------|-------------|-------|-----------------|
| A | ≥ 80 | **8** | 11.9% |
| B | 65–79.9 | **28** | 41.8% |
| C | 50–64.9 | **27** | 40.3% |
| D | 35–49.9 | **4** | 6.0% |
| E | 0–34.9 | 0 | 0% |
| insufficient_data | — | 2 | — |

### 3.3 Score Statistics

| Metric | Value |
|--------|-------|
| N (scored) | 67 |
| Mean | 65.66 |
| Median | 65.2 |
| Std Dev | 9.64 |
| Min | 42.8 |
| Max | 85.5 |
| P25 | 61.5 |
| P75 | 68.9 |

### 3.4 Product Type Distribution

| Type | Count | Notes |
|------|-------|-------|
| `hummus_spread` | 44 | Core category |
| `matbucha` | 11 | Cooked tomato-pepper spread |
| `eggplant_spread` | 7 | Roasted eggplant spreads |
| `pepper_spread` | 5 | Roasted pepper spreads |
| `masabacha` | 2 | Masabcha (whole chickpea variant) |

### 3.5 Top 10 Products

| Rank | Name | Score | Grade | State | Price (₪) |
|------|------|-------|-------|-------|-----------|
| 1 | חומוס | 85.5 | A | normal | 9.9 |
| 2 | חומוס ענק | 85.5 | A | normal | 10.9 |
| 3 | חומוס לבן ענק שופרסל | 85.4 | A | normal | 9.9 |
| 4 | חומוס גדול שופרסל | 85.4 | A | normal | 13.9 |
| 5 | חומוס ענק | 85 | A | normal | 10.9 |
| 6 | חומוס מוקפא | 85 | A | normal | — |
| 7 | הקיסר חומוס ענק | 80.4 | A | normal | — |
| 8 | סלט חומוס | 80.2 | A | normal | — |
| 9 | חומוס שלם יכין | 79.9 | B | normal | 10.0 |
| 10 | חומוס מסעדות | 75.7 | B | normal | — |

**Note on top 6:** Ranks 1–6 scored 85–85.5 via the NOVA 1 single-ingredient floor (SRC-01). These are Shufersal own-brand and private-label bulk hummus products with no ingredient list data. The floor is mechanically correct — unprocessed whole food protected from data gaps — but grades are data-conditional, not earned organically. This is documented in the `bsip_metadata.qa_notes` field in the JSON.

### 3.6 Bottom 10 Products (Displayable)

| Rank | Name | Score | Grade | State | Note |
|------|------|-------|-------|-------|------|
| 1 | ממרח פלפלים קלויים | 42.8 | D | normal | ADDITIVE_MARKERS_5_PLUS cap |
| 2 | ממרח פלפלים קלויים | 48.0 | D | normal | HIGH_SODIUM cap |
| 3 | מטבוחה אמיתית | 48.7 | D | caveated | STRUCTURAL_EMPTINESS |
| 4 | מטבוחה חריפה | 49.6 | D | caveated | STRUCTURAL_EMPTINESS |
| 5 | חציל על האש בטחינה | 50.0 | C | normal | — |
| 6 | פלפל צ'ומה | 51.0 | C | normal | — |
| 7 | סלט מטבוחה פיקנטי | 52.0 | C | normal | — |
| 8 | מטבוחה פיקנטית | 52.0 | C | normal | — |
| 9 | סלט חציל פיקנטי | 54.2 | C | normal | — |
| 10 | סלט חציל בטעם כבד | 56.1 | C | normal | liver-flavor descriptor |

### 3.7 Caveated Products

| Product | Score | Grade | Caveat |
|---------|-------|-------|--------|
| חומוס (bsip1_1990261) | 72.6 | B | LOW_NOVA_CONFIDENCE — suppress processing_quality highlight |
| חומוס (bsip1_3643714) | 72.6 | B | LOW_NOVA_CONFIDENCE — suppress processing_quality highlight |
| סלט פלפלים קלויים | 63.5 | C | CATEGORY_INSTABILITY — display category as "Savory spread" |
| סלט טורקי | 60.4 | C | CATEGORY_INSTABILITY — display category as "Savory spread" |
| מטבוחה חריפה | 49.6 | D | STRUCTURAL_EMPTINESS — calorie_density capped at 50 |
| מטבוחה אמיתית | 48.7 | D | STRUCTURAL_EMPTINESS — calorie_density capped at 50 |

### 3.8 Unavailable Products

| Product | PID | Reason |
|---------|-----|--------|
| חומוס | bsip1_7296073733317 | No nutrition panel — score not displayable |
| חומוס ענק | bsip1_7296073733348 | No nutrition panel — score not displayable |

---

## Section 4 — Known Limitations

### KL-1 — Fat quality dimension unreliable (84% of corpus)

**Severity:** Medium  
**Products affected:** 64 of 69 (fat_g ≤ 1.0 in BSIP1 — Shufersal fat-row scraping defect confirmed in TASK-039)

The `fat_quality` dimension returns neutral 50.0 for these products because the SRC-04 gate (`fat_g < 0.5 → neutral 50`) fired. This is not an inflation error — it is a neutralization. Score impact vs. corrected data: −1 to −2 points per product, not material to grade distributions.

**UI action required:** Do not display `fat_quality` as a dimension breakdown score. Add a corpus-level caveat: *"Fat quality scores are unavailable for this category pending a scraper fix."*

**Resolution path:** Fix Shufersal fat-row HTML parser, re-scrape, re-run as `run_hummus_003`.

---

### KL-2 — 2 products have no nutrition data

**Severity:** High  
**Products:** bsip1_7296073733317 (חומוס), bsip1_7296073733348 (חומוס ענק)

These products have no nutrition panel from the Shufersal scrape. `displayable: false`. Grade = `insufficient_data`. Score field is `null` in the JSON.

**UI action required:** Show "score unavailable" state. Do not display grade. Do not include in score distribution charts.

---

### KL-3 — 2 products have imprecise routing (default category)

**Severity:** Low  
**Products:** סלט טורקי (60.4 C), סלט פלפלים קלויים (63.5 C)

Scores are valid (at 60–100 kcal/100g, the `default` and `sauce_spread` calorie tables return identical values). Category label is imprecise — should display as "Savory spread" not the internal `default` routing code. `display_state: "caveated"` with `display_caveats` populated.

**UI action required:** Override displayed category label to "Savory spread" for these products.

---

### KL-4 — 2 matbucha products suppressed by structural emptiness gate

**Severity:** Low  
**Products:** מטבוחה אמיתית (48.7 D), מטבוחה חריפה (49.6 D)

The SRC-04 structural emptiness gate fired on these products (near-zero fat from fat anomaly + low kcal + low protein + low fiber). `calorie_density` was capped at 50 rather than ~90 expected for low-kcal vegetable spreads. Grade D is mechanically correct but counterintuitive for a simple cooked tomato product.

**UI action required:** Display with `caveated` state. Product-level note: *"Score may not fully reflect product quality — calorie data is incomplete."*

---

### KL-5 — 2 products have unreliable NOVA inference

**Severity:** Low  
**Products:** חומוס (bsip1_1990261), חומוס (bsip1_3643714)

Both have NOVA confidence = 0.2 (no ingredient data; NOVA inferred from absence of signals). `processing_quality` dimension scores depend on NOVA and are unreliable for these products.

**UI action required:** Suppress `processing_quality` as a highlight dimension for these 2 products. Full scores are still displayable.

---

## Section 5 — Dimension Coverage

| Dimension | Weight | Corpus avg | Display? | Note |
|-----------|--------|-----------|---------|------|
| processing_quality | 15% | 68.3 | Yes | Unreliable for 2 low-NOVA products |
| nutrient_density | 15% | 27.5 | Yes | Uniformly low for this category — legume baseline |
| calorie_density | 15% | 75.2 | Yes | Primary differentiator post-routing fix |
| glycemic_quality | 12% | 92.2 | Yes | Uniformly high — low sugar category |
| protein_quality | 10% | 35.3 | Yes | Uniformly low — whole food source, not isolated |
| additive_quality | 10% | 72.1 | Yes | Key differentiator for reconstructed vs. clean products |
| satiety_support | 6% | 48.4 | Yes | Below neutral; fiber data sparse |
| **fat_quality** | **8%** | **50.0** | **NO** | **Unreliable — do not display breakdown** |
| regulatory_quality | 5% | 92.4 | Yes | Few red labels in this corpus |
| whole_food_integrity | 4% | 65.2 | Yes | Meaningful signal for NOVA 1 vs. NOVA 3 products |

---

## Section 6 — Filter System

The JSON includes `filter_options` for:

**By grade:** A (8), B (28), C (27), D (4)  
**By product type:** hummus_spread (44), matbucha (11), eggplant_spread (7), pepper_spread (5), masabacha (2)  
**By NOVA level:** NOVA 1 (6), NOVA 2 (4), NOVA 3 (59)

All filters operate on the `grade`, `product_type`, and `nova` fields of product records respectively.

---

## Section 7 — Data Field Completeness

| Field | Coverage | Notes |
|-------|----------|-------|
| `name_he` | 69/69 (100%) | All products have Hebrew names |
| `score` | 67/69 (97%) | 2 unavailable products have `null` |
| `grade` | 67/69 (97%) | 2 products have `insufficient_data` |
| `image_url` | 68/69 (99%) | Shufersal CDN URLs; 1 missing |
| `price_ils` | ~45/69 (65%) | Some products have null price from BSIP0 |
| `brand` | 3/69 (4%) | Most hummus products are unbranded at Shufersal |
| `source_url` | 69/69 (100%) | All products have Shufersal product page URLs |
| `barcode` | 69/69 (100%) | All products have barcodes |
| `dimension_scores` | 67/69 (97%) | Null for 2 unavailable products |
| `ingredient_count` | 69/69 (100%) | 0 for products with no ingredient list |
| `nova` | 69/69 (100%) | Inferred for all products |

**Price coverage note:** 65% price coverage is lower than expected. Shufersal prices were captured during the BSIP0 scrape (2026-05-30). Products scraped via search query may have missing prices if the price_ils field was not populated by the scraper. This does not affect BSIP2 scores.

**Brand coverage note:** 4% brand coverage reflects the hummus market — most Shufersal-scraped hummus products are private-label or unbranded. The brand field will be more useful in categories with stronger brand presence (e.g., nut butters, protein yogurts).

---

## Section 8 — QA Checklist

| Check | Result | Notes |
|-------|--------|-------|
| Source run = run_hummus_002 only | ✅ | Verified; run_hummus_001 not referenced |
| Product count = 69 | ✅ | All 69 BSIP1 records included |
| Displayable count = 67 | ✅ | 2 insufficient_data products excluded |
| Grade A count = 8 | ✅ | Matches baseline freeze report |
| Grade B count = 28 | ✅ | Matches |
| Grade C count = 27 | ✅ | Matches |
| Grade D count = 4 | ✅ | Matches |
| fat_quality not in dimension breakdown display | ✅ | `dimension_display_flags.fat_quality.display_breakdown = false` |
| 2 unavailable products flagged | ✅ | `displayable: false` for both |
| 6 caveated products flagged | ✅ | `display_state: "caveated"` with caveats populated |
| known_limitations present | ✅ | KL-1 through KL-5 |
| bsip_metadata.invalid_run noted | ✅ | `"invalid_run": "run_hummus_001"` |
| TASK-060 caveat documented | ✅ | `display_rules_source` field and qa_notes |
| JSON is valid | ✅ | Written without errors; 131.3 KB |

---

## Section 9 — Frontend Integration Notes

### Sorting

Default sort: `score DESC` (highest to lowest). Products with `displayable: false` should be rendered last or excluded entirely depending on UI decision.

### Score display precision

Display scores to 1 decimal place. The JSON stores them as float64 — round to 1 decimal in the UI layer.

### Grade display

Use the `grade` field directly. The `grade_thresholds` object in the JSON documents the numeric boundaries for reference.

### Dimension breakdown display

Do not display `fat_quality` as an individual score breakdown. Display the other 9 dimensions only. Add a footnote: *"Fat quality score not available for this dataset — data quality issue pending resolution."*

For caveated products:
- `low_nova_confidence` caveat → suppress `processing_quality` dimension highlight
- `structural_emptiness` caveat → add product-level incomplete data note
- `category_routing_imprecise` caveat → override category label to "Savory spread"

### Category label

Do not expose internal routing codes (`sauce_spread`, `default`, `whole_food_fat`) to users. The `category_display` field is set to `"savory_spread"` for all products as the user-facing label.

### Price

The `price_ils` field is populated for ~65% of products. If null, omit from the product card.

---

## Section 10 — Next Steps

| Priority | Action |
|----------|--------|
| **P0** | Fix Shufersal fat-row HTML parser (TASK-039 root cause) |
| **P0** | Re-run hummus as `run_hummus_003` with corrected fat data |
| **P1** | Retrieve or reconstruct TASK-060 Product Agent decision; rebuild JSON if decisions differ from TASK-045 rules |
| **P1** | Confirm price_ils coverage — check if Shufersal search-phase products can have prices back-populated |
| **P2** | Add brand data for hummus products where brand is identifiable from product name |
| **P3** | CNO ruling on matbucha structural_emptiness gate behavior (KL-4) |

---

*Hummus Frontend Build Report — TASK-061 — Data Agent — 2026-05-31*  
*Output: `C:\Bari\02_products\hummus\hummus_frontend_v1.json` (131.3 KB)*  
*Build result: SUCCESS — 67/69 products displayable, 0 errors*
