# Hummus Fat Anomaly — Investigation Report

**Task:** TASK-039  
**Owner:** QA & Audit Lead  
**Date:** 2026-05-30  
**Category:** Hummus and Savory Dips (69 products, Shufersal corpus)  
**Triggered by:** TASK-038 — fat_raw = "פחות מ 0.5" flagged as biologically implausible  

---

## Executive Summary

**59 of 69 products (86%) have incorrect fat data in the BSIP1 canonical corpus.**

The Shufersal HTML scraper captured the *saturated fat* sub-row value instead of the *total fat* row for the majority of the hummus corpus. Caloric gap analysis confirms the actual fat content of tahini-containing hummus products is 10–27g per 100g — physically consistent with declared tahini percentages — not the "<0.5g" value stored in `fat_raw`.

**BSIP2 decision: Allowed with warning.** The fat_quality dimension (8% weight) is unreliable for 58/69 products in this run. All other dimensions are unaffected. The issue register at `02_products/hummus/audit/fat_anomaly_TASK039.json` contains corrected fat values derived from caloric gap analysis for use by the BSIP2 operator and as input for a future scraper fix.

---

## 1. Scope and Counts

| Condition | Count |
|---|---|
| Total products analysed | 69 |
| `fat_raw = "פחות מ 0.5"` (less than 0.5) | 55 |
| `fat_raw` is a numeric string but caloric gap implies wrong value | 4 |
| `fat_raw` missing (null) | 5 |
| Fat value plausibly consistent with caloric balance | 5 |
| **Products with confirmed fat anomaly** | **59** |

| Severity | Count | Description |
|---|---|---|
| CRITICAL | 15 | Gap > 15g, tahini declared in ingredients |
| HIGH | 21 | Gap 10–15g, tahini present |
| MEDIUM | 23 | Gap 5–10g |
| LOW | 5 | Gap 2–5g |
| NONE | 5 | Consistent with caloric balance |

---

## 2. Root Cause Analysis

### Root Cause 1: Saturated fat sub-row capture (59 products)

**What happened:** The Shufersal nutrition label HTML renders total fat and saturated fat in a nested row structure:

```
שומנים:        [total fat value]
  מתוכם שומן רווי:  [saturated fat sub-value] ← "פחות מ 0.5"
```

The scraper's `NUTR_LABEL_MAP` maps Hebrew labels to field names:
```python
"שומנים": "fat", "שומן": "fat"
```

The parser iterates through HTML `div.nutritionItem` blocks in DOM order. For most Shufersal product pages, the first match for a "שומן"-containing label was the **saturated fat sub-row** (שומן רווי = saturated fat), not the parent total fat row. The saturated fat for chickpea-based hummus is legitimately low (`<0.5g` or 1–3g), which is why the extracted value is plausible on its face but inconsistent with declared tahini content.

**Proof from caloric balance:**

| Product | Declared tahini | fat_scraped | kcal | fat_implied (kcal gap) | Gap |
|---|---|---|---|---|---|
| חומוס עשיר ב40% טחינה | 40% | 0.5g | 311 | 26.6g | +26.1g |
| חומוס מועשר 40% עם חריף | 37% | 0.5g | 294 | 24.9g | +24.4g |
| חומוס אבו מרוואן 26% | 26% | 0.5g | 275 | 21.0g | +20.5g |
| חומוס עם טחינה אחלה 16.9% | 16.9% | 0.5g | 191 | 13.3g | +12.8g |
| חומוס עם טחינה צבר 17% | 17% | 0.5g | 196 | 12.3g | +11.8g |

The caloric gap is perfectly explained by fat. For `חומוס עשיר ב40% טחינה`:
- Tahini contains approximately 58g fat per 100g
- At 40% tahini: ~23g fat contribution from tahini alone
- Implied fat from energy balance: 26.6g ✓

This is consistent, systematic, and mechanistically explained.

---

### Root Cause 2: Nutrition values embedded in ingredient text (1 product)

**Product:** `סלט חומוס` (barcode 6666307)

**What happened:** For this product, the Shufersal page returned nutritional data embedded within the ingredient text block. The raw ingredient string contains:

```
גרגירי חומוס, טחינה שומשומין, מים, תבלינים, חומר משמר .E202
ערכים תזונתיים 100 גרם 257 קל אנרגיה 18.2 גרם חלבונים
12.4 גרם פחמימות 18.2 גרם שומנים 480 מג ...
```

The scraper extracted protein=18.2g correctly (matched first occurrence of a protein-like value) but fat=3.2g incorrectly. The actual fat from the embedded label text is 18.2g. Caloric gap: 257 kcal − (18.2 × 4) − (12.4 × 4) = 134.6 kcal → implied fat = **15.0g**. A discrepancy exists between the embedded "18.2g שומנים" and the caloric-implied 15.0g, likely due to label rounding or alcohol content not captured. The scraped 3.2g is wrong regardless.

---

### Root Cause 3: "Legitimate trace fat" — not present in this corpus

No products were classified as having legitimately near-zero fat. Even the vegetable-based secondary products (matbucha, eggplant spreads) that use added oil show fat values where the scraper has a gap.

---

## 3. Products NOT Affected (Fat is Correct)

Five products have fat values consistent with caloric balance (gap < 2g):

| Product | fat_scraped | fat_implied | Gap | Notes |
|---|---|---|---|---|
| חומוס שלם יכין | 1.9g | 2.8g | +0.9g | Dry chickpea product, low tahini, plausible |
| סלט מטבוחה | 5.9g | 5.9g | 0.0g | Oil-based matbucha, correctly captured |
| הקיסר חומוס ענק | 1.9g | 3.2g | +1.3g | Low tahini, minor gap within rounding |
| חומוס מוקפא | 2.1g | 1.6g | −0.5g | Within label rounding tolerance |
| סלט פלפלים קלויים | 0.0g | 0.3g | +0.3g | No fat (pepper spread), consistent |

---

## 4. This Is NOT a BSIP0→BSIP1 Normalization Error

**The error originates in the BSIP0 scraper, not the BSIP1 conversion.**

The converter script (`convert_bsip0_to_bsip1.py`) uses `parse_num()` which extracts the first numeric value from `fat_raw`. For `"פחות מ 0.5"`, it correctly extracts 0.5 — this is the expected behavior. The BSIP1 `fat_g = 0.5` accurately reflects what BSIP0 scraped. The scraper is the source of the error, not the converter.

**The fix must be applied to** `03_operations/bsip0/scrape/shufersal_hummus/02_scrape_hummus_shufersal.py` — specifically the nutrition panel parsing logic that iterates over `div.nutritionItem` blocks. The parser must distinguish the parent total fat row from the saturated fat sub-row.

**Scraper fix required (not in scope of TASK-039, per rules):**  
The `NUTR_LABEL_MAP` should reject any match on a label containing "רווי" (saturated). The total fat row should be identified by labels "שומנים" or "שומן" that do NOT contain "רווי". Alternatively, the HTML traversal should skip rows that are children (sub-items) of the fat row.

---

## 5. Impact on BSIP2 Dimensions

| Dimension | Weight | Impact from fat anomaly |
|---|---|---|
| `fat_quality` | 8% | **Severely affected.** Saturated fat fraction, total fat, seed oil penalty — all computed from wrong base. Scores will be systematically inflated (low fat = no penalty). |
| `calorie_density` | 15% | **Unaffected.** Energy (kcal) is scraped correctly; calorie density uses kcal directly. |
| `glycemic_quality` | 12% | **Unaffected.** Sugar and fiber values not affected by fat error. |
| `nutrient_density` | 15% | **Unaffected.** Protein and fiber values correct. |
| `processing_quality` | 15% | **Unaffected.** NOVA inference from ingredient list, not nutrition panel. |
| `additive_quality` | 10% | **Unaffected.** Based on ingredient list signals. |
| `satiety_support` | 6% | **Minor effect.** Formula uses protein and fiber; fat not directly included. However, calorie floor (50 kcal) may interact differently if fat contribution is missing. Marginal. |
| `protein_quality` | 10% | **Unaffected.** Protein values correct. |
| `regulatory_quality` | 5% | **Minor effect.** Saturated fat red label threshold (5g/100g) will NOT fire for products where actual sat fat may be 1–3g — but this is likely correct, as most hummus products genuinely don't exceed the sat fat threshold. The missed sat fat value doesn't create a false regulatory flag. |
| `whole_food_integrity` | 4% | **Unaffected.** NOVA inference and ingredient count. |

**Fat quality is the only dimension materially corrupted. Its 8% weight means the maximum impact on the final score is ~8 points (if fat_quality scores 100 instead of its true value). In practice, the distortion is lower because other dimensions constrain the range.**

---

## 6. Severity by Product Type

| Type | Products | CRITICAL | HIGH | MEDIUM | LOW/NONE |
|---|---|---|---|---|---|
| Hummus spread (tahini declared %) | ~20 | 7 | 13 | 0 | 0 |
| Hummus spread (tahini undeclared) | ~25 | 8 | 7 | 10 | 0 |
| Eggplant spread | 7 | 0 | 0 | 5 | 2 |
| Matbucha / Turkish salad | 11 | 0 | 1 | 5 | 5 |
| Pepper spreads | 5 | 0 | 0 | 3 | 2 |

Products with declared tahini percentage are the most severely affected. The fat gap scales directly with tahini content — 40% tahini products show a 25–27g gap versus 15% tahini products showing a 10–13g gap.

---

## 7. BSIP2 Decision

### **BSIP2: Allowed with warning**

The hummus category may proceed to BSIP2 scoring subject to the following conditions:

**Condition 1 — Operator must be briefed before run:**  
The `fat_quality` dimension scores for 58 of 69 products are derived from incorrect fat values. The `fat_quality` output for this run should be treated as a placeholder, not a reliable signal.

**Condition 2 — Run report must document the dimension impact:**  
The BSIP2 run report must note that `fat_quality` is systematically inflated across the corpus due to the fat_raw scraper error. Any comparative analysis that relies on `fat_quality` dimension scores from this run is invalid.

**Condition 3 — Corrected fat values are available:**  
The issue register (`fat_anomaly_TASK039.json`) provides `fat_g_implied_kcal_gap` — the caloric-gap-derived fat estimate — for all 69 products. The BSIP2 operator may optionally use these estimates to patch `fat_g` in BSIP1 records before scoring, if higher fat_quality accuracy is required for this run. This would be a CNO-approved manual correction, not a scraper fix.

**Condition 4 — Not blocked because:**
- 8 of 10 scoring dimensions are unaffected
- The score impact ceiling from fat_quality error is ~8 points
- The calorie/sodium red-label thresholds are unaffected (kcal and sodium are correctly scraped)
- Distribution analysis (grade spread) is still valid as a relative comparison
- Grade boundaries are unlikely to shift by more than one grade for most products

**Condition 5 — Scraper fix required before re-run:**  
Before any subsequent BSIP0 refresh or new scrape of the hummus corpus, the Shufersal scraper must correctly distinguish total fat from saturated fat in the nutrition panel HTML. The fix is in scope for a Wave 2 scraper maintenance task.

---

## 8. Files Created

| File | Description |
|---|---|
| `03_operations/qa/reports/hummus_fat_anomaly_TASK039.md` | This report |
| `02_products/hummus/audit/fat_anomaly_TASK039.json` | Issue register: 69 products with fat_g, implied fat, severity, BSIP2 decision |
| `03_operations/qa/hummus_fat_analysis.py` | Analysis script (reproducible; re-run from C:\Bari) |

---

## 9. Issue Register Field Reference

Each record in `fat_anomaly_TASK039.json` contains:

| Field | Description |
|---|---|
| `product_id` | Canonical BSIP1 ID (`bsip1_{barcode}`) |
| `product_name` | Hebrew product name |
| `barcode` | Shufersal barcode or internal code |
| `fat_raw_shufersal` | Raw string from scraper (e.g., `"פחות מ 0.5"`) |
| `fat_g_bsip1` | Value stored in canonical BSIP1 `normalized_nutrition_per_100g.fat_g` |
| `fat_g_scraped_parsed` | Numeric value extracted from fat_raw by parse_num |
| `fat_g_implied_kcal_gap` | Fat estimated from: `(kcal − protein×4 − carbs×4) / 9` |
| `fat_g_gap` | `fat_g_implied − fat_g_scraped_parsed` |
| `energy_kcal` | Correctly scraped kcal/100g |
| `tahini_pct_declared` | Declared tahini % from ingredient text (if present) |
| `ingredients_include_tahini` | Boolean |
| `suspected_root_cause` | `scraper_captured_sat_fat_subrow` / `scraper_html_misalignment` / `plausible_match` |
| `severity` | CRITICAL / HIGH / MEDIUM / LOW / NONE |
| `bsip2_allowed` | `allowed` / `allowed_with_warning` |
| `recommended_action` | Per-product action text |
| `source_url` | Shufersal product page URL |

---

*Report by QA & Audit Lead — TASK-039*  
*Issue register: `02_products/hummus/audit/fat_anomaly_TASK039.json`*  
*Scraper fix required before next BSIP0 run: see Section 4*
