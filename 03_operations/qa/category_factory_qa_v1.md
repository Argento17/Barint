# Bari Category Factory QA Checklist v1

**Classification:** QA Framework — Internal  
**Version:** v1  
**Date:** 2026-05-30  
**Owner:** QA & Audit Lead  
**Scope:** BSIP0 → BSIP1 pipeline only. No BSIP2, no scoring, no website changes.  
**Reference category:** Hummus (first factory run under this framework)  
**Companion file:** `category_factory_qa_v1_checklist.json`

---

## Purpose

This framework defines the reusable QA gates every Bari category must pass between BSIP0 scrape and BSIP1 enrichment output. It is a validation checklist, not an execution script. Automation of individual checks is tracked separately; the checklist is the authoritative definition of what must be true.

One instance of this checklist is completed per category per factory run. The operator fills it in manually (or with tool assistance) and files the result in the category's `reports/` directory before BSIP2 begins.

---

## How to use

1. Copy this file to `02_products/{category}/reports/qa_run_{date}.md`
2. Work through each check in order within each domain
3. Record the result for every check: PASS / FAIL / WARN / N/A
4. For any FAIL or WARN: record the count of affected products and the action taken or deferred
5. Apply the pass/fail verdict at the bottom
6. File the completed report; do not overwrite this master

**A category may not enter BSIP2 while any Hard Fail check is open.**

---

## Domain 1 — Scope Integrity

Verifies that the canonical corpus contains only in-scope products and that the exclusion decision record exists.

### SCP-001 — Corpus filter is locked

**What to check:** `02_products/{category}/corpus_filter.md` exists and contains a lock date.  
**How:** Confirm the file exists. Confirm the header or footer contains a line matching `Locked at:` or `*This document is locked.*`  
**Fail condition:** File absent, or file present but contains no lock marker (draft state).  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### SCP-002 — Exclusion register exists

**What to check:** A record exists of products that were discovered but rejected. This is the `candidate_review.csv` with `approved_for_scrape = NO` rows, or a separate `exclusion_register.csv`.  
**How:** Open `observations_bsip0/{retailer}/candidate_review.csv`. Confirm rows with `approved_for_scrape = NO` are present (if any products were rejected). If every discovered product was approved, confirm the CSV still exists and has a header row.  
**Fail condition:** `candidate_review.csv` absent entirely — there is no record of which products were seen and what was decided.  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### SCP-003 — No known out-of-scope products in approved corpus

**What to check:** Products that match exclusion criteria from `corpus_filter.md` are not present in the final approved BSIP0 observations.  
**How:** For each category, a short list of rejection signal terms is defined in the corpus filter. Check the approved product names (`name_he`) against those terms. For Hummus: reject any product whose name contains `טחינה` (standalone, not in "חומוס עם טחינה"), `לאבנה`, `גבינה לבנה`, `קוטג'`, `סחוג`, `חריסה`, `פסטו`, `קולסלאו`.  
**How to perform:** Scan `candidate_review.csv` rows where `approved_for_scrape = YES` and check names. Alternatively, list `observations_bsip0/shufersal/*.json` and inspect `name_he` fields for rejection signals.  
**Fail condition:** Any approved product matches a hard exclusion term from the corpus filter.  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### SCP-004 — Product count within expected corpus range

**What to check:** Total BSIP0 product files in `observations_bsip0/{retailer}/` (excluding `all_discovered_raw_*.json` and `candidate_review.csv`) falls within the range defined in the corpus filter.  
**How:** `ls observations_bsip0/shufersal/*.json | grep -v all_discovered | wc -l`. Compare against the `Expected product distribution` table in `corpus_filter.md`. For Hummus: expected 47–70 total.  
**Fail condition:** Count < minimum threshold from `corpus_filter.md` (hard gate: < 30 for Hummus).  
**Warn condition:** Count in lower half of expected range (30–40 when target was 47–70). Proceed but note.  
**Verdict type:** Hard Fail if below gate minimum; Warning if in lower range  

| Result | Actual count | Expected range | Note |
|--------|-------------|----------------|------|
| | | | |

---

### SCP-005 — No multi-pack or catering-size products

**What to check:** Products with multi-pack marketing (e.g. "מארז 3×", "מארז 4×") or catering sizes (≥ 1 kg) are not in the approved corpus.  
**How:** Scan `name_he` fields for `מארז`, `3×`, `4×`, `1 ק"ג`, `1.5 ק"ג`, or `weight_g ≥ 1000`.  
**Fail condition:** Any such product is in the approved BSIP0 files.  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

## Domain 2 — Traceability

Verifies that every BSIP1 enriched record can be traced back to its BSIP0 source observation.

### TRC-001 — Every BSIP1 file has a populated source_retailers field

**What to check:** In every `bsip1_*.json` in `03_operations/bsip1/run_{category}_001/output/`, the `source_retailers` array is non-empty.  
**How:** For each file: `source_retailers` must be a non-empty list (e.g. `["shufersal"]` or `["shufersal", "yohananof"]`).  
**Fail condition:** Any file has `source_retailers: []` or the field is absent.  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### TRC-002 — Every BSIP1 barcode traces to a BSIP0 source file

**What to check:** The barcode in every `bsip1_*.json` corresponds to a product that was scraped in BSIP0.  
**How:** Extract the barcode from each BSIP1 filename (`bsip1_{BARCODE}.json` → `{BARCODE}`). Verify a file matching `P_{BARCODE}.json` or `{BARCODE}/` exists in `observations_bsip0/{retailer}/`. Note: Shufersal uses `P_{code}.json`; Yohananof uses a barcode subdirectory.  
**Fail condition:** Any BSIP1 barcode has no matching BSIP0 observation file across any scraped retailer.  
**Verdict type:** Hard Fail  

| Result | Unmatched BSIP1 count | Note |
|--------|----------------------|------|
| | | |

---

### TRC-003 — ingredients_raw_provenance.source is "bsip0_scrape" for all products

**What to check:** In every BSIP1 file that has an ingredients list, `ingredients_raw_provenance.source` must equal `"bsip0_scrape"`.  
**How:** Scan BSIP1 files: where `ingredients_list` is non-empty, check `ingredients_raw_provenance.source`.  
**Fail condition:** Any product has a provenance source other than `"bsip0_scrape"` (e.g. manual entry, LLM-generated, unknown).  
**Warn condition:** `ingredients_raw_provenance` field is absent but `ingredients_list` is non-empty.  
**Verdict type:** Hard Fail for non-bsip0 source; Warning for absent provenance field  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### TRC-004 — BSIP0 source files retain scraped_at timestamp and source_url

**What to check:** Every BSIP0 `P_*.json` file has a non-null `scraped_at` (ISO timestamp) and a non-empty `source_url` containing the retailer domain.  
**How:** Sample 10 files. Check both fields. If sampling reveals any issue, check all.  
**Fail condition:** Any approved product file missing `scraped_at` or `source_url`.  
**Verdict type:** Hard Fail  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

### TRC-005 — audit_ref file exists for every BSIP1 product

**What to check:** Every BSIP1 product file has an `audit_ref` field, and the referenced audit file (`bsip1_audit_{barcode}.json`) exists in the same output directory.  
**How:** For each BSIP1 file: confirm `audit_ref` field is present and non-null. Confirm `bsip1_audit_{barcode}.json` exists in the run output directory.  
**Warn condition:** `audit_ref` present but referenced file is absent (audit lost).  
**Fail condition:** `audit_ref` field absent entirely.  
**Verdict type:** Warning for missing audit file; Hard Fail for absent audit_ref field  

| Result | Affected count | Note |
|--------|---------------|------|
| | | |

---

## Domain 3 — Coverage

Verifies that the corpus has sufficient nutritional, ingredient, image, and barcode data to support BSIP2 scoring.

Coverage thresholds are set per category in `corpus_filter.md`. The values below are the Hummus defaults; other categories may define different minimums.

### COV-001 — Nutrition coverage ≥ 80%

**What to check:** In BSIP1 output, `normalized_nutrition_per_100g` must contain non-null values for all four core macros: `energy_kcal`, `protein_g`, `carbohydrates_g`, `fat_g`.  
**How:** Count products where all four fields are non-null. Divide by total product count.  
**Fail condition:** Coverage < 60% (minimum viable for BSIP2).  
**Warn condition:** Coverage 60–79% (below target; proceed with note).  
**Verdict type:** Hard Fail if < 60%; Warning if 60–79%  

| Result | Covered | Total | Pct | Note |
|--------|---------|-------|-----|------|
| | | | | |

---

### COV-002 — Ingredient list coverage ≥ 70%

**What to check:** In BSIP1 output, `ingredients_list` is non-empty for ≥ 70% of products.  
**How:** Count products where `ingredients_list` has ≥ 1 entry.  
**Fail condition:** Coverage < 50%.  
**Warn condition:** Coverage 50–69%.  
**Verdict type:** Hard Fail if < 50%; Warning if 50–69%  

| Result | Covered | Total | Pct | Note |
|--------|---------|-------|-----|------|
| | | | | |

---

### COV-003 — Image coverage ≥ 90%

**What to check:** `image_url` in BSIP1 is non-null for ≥ 90% of products.  
**How:** Count products where `image_url` is not null and not an empty string.  
**Fail condition:** Coverage < 70%.  
**Warn condition:** Coverage 70–89%.  
**Note:** Image URLs are retailer-hosted. Availability at display time is a frontend concern, not a pipeline concern. This check confirms the URL was captured, not that the image loads.  
**Verdict type:** Hard Fail if < 70%; Warning if 70–89%  

| Result | Covered | Total | Pct | Note |
|--------|---------|-------|-----|------|
| | | | | |

---

### COV-004 — Barcode quality — at least 50% are valid EAN-13 or GS1 format

**What to check:** Barcodes that are 13-digit EAN-13 format (starting with a standard GS1 prefix) are preferred. Retailer-internal IDs (short codes, or 11-digit Yohananof internal codes prefixed `16000-`) are acceptable but lower confidence.  
**How:** For each BSIP1 file, check `barcode_validation_status`. Status `"gs1_ean13"` is best. `"retailer_internal_id"` is acceptable. `"unknown"` or absent is a warning.  
**Fail condition:** Any barcode is malformed (non-numeric, length < 4).  
**Warn condition:** > 50% of products are `retailer_internal_id` (reduces cross-retailer deduplication reliability in future runs).  
**Verdict type:** Hard Fail for malformed barcodes; Warning for high internal-ID ratio  

| Result | EAN-13 count | Internal ID count | Unknown count | Note |
|--------|-------------|-------------------|---------------|------|
| | | | | |

---

### COV-005 — Sodium and sugar coverage (informational)

**What to check:** `normalized_nutrition_per_100g.sodium_mg` is non-null for ≥ 60% of products. `sugars_g` is non-null for ≥ 50% of products.  
**How:** Count non-null values for each field.  
**Purpose:** These fields are not required for BSIP2 routing but affect red-label detection and sugar scoring. Low coverage is noted for BSIP2 operators.  
**Verdict type:** Warning only (does not block BSIP2 entry)  

| Field | Covered | Total | Pct | Threshold | Note |
|-------|---------|-------|-----|-----------|------|
| sodium_mg | | | | 60% | |
| sugars_g | | | | 50% | |

---

## Domain 4 — Canonical Structure

Verifies that the canonical BSIP1 output folder is correctly populated and that excluded products have not leaked into it.

### CAN-001 — canonical_bsip1 folder exists and is populated

**What to check:** `02_products/{category}/canonical_bsip1/` exists and contains at least as many `bsip1_*.json` files as the approved product count from BSIP0.  
**How:** `ls 02_products/{category}/canonical_bsip1/bsip1_*.json | wc -l`. Compare to BSIP0 approved count.  
**Fail condition:** Folder absent, or contains 0 files, or product count is > 10% below BSIP0 approved count with no documented reason.  
**Warn condition:** Product count is 1–10% below BSIP0 approved count (some products failed BSIP1 enrichment — check BSIP1 error log).  
**Verdict type:** Hard Fail for absent or empty folder; Warning for count mismatch  

| Result | canonical_bsip1 count | BSIP0 approved count | Delta | Note |
|--------|----------------------|---------------------|-------|------|
| | | | | |

---

### CAN-002 — Manifest file exists in canonical_bsip1

**What to check:** A `manifest.json` (or `manifest.md`) exists in `02_products/{category}/canonical_bsip1/` listing every file by canonical_product_id and barcode.  
**How:** Check for the file. If it exists, verify the entry count matches the actual file count.  
**Fail condition:** Manifest absent.  
**Warn condition:** Manifest present but entry count differs from file count.  
**Verdict type:** Hard Fail for absent manifest; Warning for count mismatch  

| Result | Manifest entries | Actual file count | Note |
|--------|-----------------|-------------------|------|
| | | | |

---

### CAN-003 — schema_version is consistent across all canonical files

**What to check:** Every `bsip1_*.json` in `canonical_bsip1/` has `schema_version: "bsip1_v0_1"`.  
**How:** Check unique values of `schema_version` across all canonical files.  
**Fail condition:** Any file has a different or absent `schema_version`.  
**Verdict type:** Hard Fail  

| Result | Expected version | Versions found | Note |
|--------|-----------------|----------------|------|
| | bsip1_v0_1 | | |

---

### CAN-004 — No excluded products in canonical_bsip1

**What to check:** Products with `approved_for_scrape = NO` in `candidate_review.csv` are not present in `canonical_bsip1/`.  
**How:** Extract barcodes/codes from `NO` rows in `candidate_review.csv`. Check that no corresponding `bsip1_{barcode}.json` exists in `canonical_bsip1/`.  
**Fail condition:** Any excluded product appears in canonical_bsip1.  
**Verdict type:** Hard Fail  

| Result | Excluded product count | Found in canonical | Note |
|--------|----------------------|-------------------|------|
| | | 0 expected | |

---

### CAN-005 — All canonical files have file_type "product"

**What to check:** `file_type` field in every canonical file equals `"product"`. Audit files (`bsip1_audit_*.json`) must not be in the canonical folder.  
**How:** Check unique values of `file_type` across all canonical files.  
**Fail condition:** Any file has `file_type` other than `"product"`.  
**Verdict type:** Hard Fail  

| Result | file_type values found | Note |
|--------|----------------------|------|
| | | |

---

## Domain 5 — Regression Checks

Verifies that the BSIP1 output contains no fields that belong to a later pipeline stage, and that no schema changes were introduced without approval.

These checks protect against accidental contamination — a common failure mode when development branches diverge or scripts are adapted from a later-stage template.

### REG-001 — No BSIP2 scoring fields in BSIP1 output

**Forbidden fields:** `bsip2_score`, `grade`, `archetype`, `nova_score`, `score_trace`, `dimension_scores`, `bsip2_version`, `concern_flags`, `structural_emptiness`, `satiety_score`, `glycemic_score`, `engineering_score`, `nutritional_score`, `metabolic_score`, `floor_applied`, `cap_applied`, `trace_output`, `final_score`, `score_reason`.  
**What to check:** None of these field names appear as top-level keys in any BSIP1 canonical file.  
**How:** `grep -r "bsip2_score\|\"grade\"\|\"archetype\"\|nova_score\|dimension_scores\|score_trace\|concern_flags" canonical_bsip1/`  
**Fail condition:** Any forbidden field found.  
**Verdict type:** Hard Fail  

| Result | Forbidden fields found | Files affected | Note |
|--------|----------------------|----------------|------|
| | | | |

---

### REG-002 — No frontend or view-model fields in BSIP1 output

**Forbidden fields:** `display_name`, `slug`, `frontend_*`, `view_model`, `comparison_rank`, `shelf_position`, `insight_line`, `explanation_text`, `ui_*`, `page_*`, `is_displayable`, `display_score`.  
**What to check:** None of these field names appear in any BSIP1 canonical file.  
**How:** `grep -r "display_name\|\"slug\"\|frontend_\|view_model\|comparison_rank\|insight_line" canonical_bsip1/`  
**Fail condition:** Any forbidden field found.  
**Verdict type:** Hard Fail  

| Result | Forbidden fields found | Files affected | Note |
|--------|----------------------|----------------|------|
| | | | |

---

### REG-003 — enrichment_version matches the currently approved BSIP1 version

**What to check:** `enrichment_version` in all BSIP1 files equals the version currently approved in `03_operations/bsip1/core/enrich_runner.py` or the BSIP1 version log.  
**Current approved version:** `bsip1_enrichment_v1`  
**How:** Check unique values of `enrichment_version` across canonical files.  
**Fail condition:** A newer or older version string appears without a documented approval.  
**Verdict type:** Hard Fail if unapproved version; Warning if version string is unrecognised  

| Result | Expected version | Versions found | Note |
|--------|-----------------|----------------|------|
| | bsip1_enrichment_v1 | | |

---

### REG-004 — No new unexpected top-level fields in BSIP1 output

**Approved top-level fields** (complete list from `bsip1_v0_1` schema):  
`schema_version`, `file_type`, `canonical_product_id`, `barcode`, `canonical_name_he`, `canonical_name_en`, `brand`, `package_size_g`, `unit_count`, `unit_size_g`, `serving_size_g`, `country_of_origin`, `kosher_certification`, `image_url`, `source_retailers`, `normalized_nutrition_per_100g`, `energy_source_unit`, `ingredients_text_he`, `ingredients_list`, `allergens_contains`, `allergens_may_contain`, `claims`, `confidence`, `barcode_validation_status`, `barcode_confidence_reason`, `nutrition_basis_claimed`, `nutrition_basis_detected`, `nutrition_consistency_status`, `nutrition_consistency_warnings`, `ingredient_text_quality`, `ingredient_warnings`, `canonical_trust_score`, `canonical_trust_level`, `canonical_risk_flags`, `conflicts_summary`, `missing_fields`, `inferred_fields`, `audit_ref`, `ingredients_raw`, `ingredients_raw_provenance`, `ingredient_order`, `extracted_additives`, `extracted_flavors`, `extracted_sweeteners`, `extracted_protein_markers`, `extracted_matrix_markers`, `extracted_fermentation_markers`, `extracted_roasting_markers`, `enrichment_summary`, `enrichment_version`, `enrichment_warnings`.  

**What to check:** Collect the union of all top-level keys across all canonical BSIP1 files. Any key not in the list above is unexpected.  
**How:** `python -c "import json,pathlib; keys=set(); [keys.update(json.loads(f.read_text()).keys()) for f in pathlib.Path('canonical_bsip1').glob('bsip1_*.json')]; print(keys)"`  
**Fail condition:** Any unexpected top-level key found that is not in the approved list above AND is not a BSIP2 or frontend field (those are Hard Fail under REG-001/REG-002). Unexpected non-scoring keys are a Warning.  
**Verdict type:** Hard Fail if key matches a known BSIP2/frontend field name; Warning otherwise  

| Result | Unexpected fields found | Note |
|--------|------------------------|------|
| | | |

---

### REG-005 — BSIP0 source files are unmodified after scrape

**What to check:** `observations_bsip0/{retailer}/*.json` files have not been modified after their `scraped_at` timestamp. BSIP0 files are immutable once written by the scraper.  
**How:** Check file system modification date vs. `scraped_at` field in each file. Any file where `mtime` is significantly later than `scraped_at` (> 60 seconds) warrants investigation.  
**Fail condition:** Any BSIP0 file where the content has been manually edited (evident from `mtime` much later than `scraped_at`, or from manual field values not matching scraper output format).  
**Warn condition:** `mtime` is later than `scraped_at` by < 5 minutes (may be filesystem timestamp artefact on copy/move).  
**Verdict type:** Hard Fail for confirmed manual edit; Warning for ambiguous mtime  

| Result | Files with late mtime | Note |
|--------|----------------------|------|
| | | |

---

## Domain 6 — Pass / Fail Criteria

### Hard Fail — BSIP2 entry blocked

Any of the following conditions blocks the category from entering BSIP2. The issue must be resolved and the affected check re-run before proceeding.

| Code | Condition |
|------|-----------|
| SCP-001 | Corpus filter not filed or not locked |
| SCP-002 | Exclusion register (candidate_review.csv) absent |
| SCP-003 | Known out-of-scope product in approved corpus |
| SCP-005 | Multi-pack or catering-size product in corpus |
| TRC-001 | BSIP1 file with empty source_retailers |
| TRC-002 | BSIP1 barcode with no matching BSIP0 source file |
| TRC-003 | ingredients_raw_provenance.source ≠ "bsip0_scrape" |
| TRC-004 | BSIP0 product missing scraped_at or source_url |
| COV-001 | Nutrition coverage < 60% |
| COV-001 | Total product count < 30 (corpus_filter.md minimum) |
| CAN-001 | canonical_bsip1 folder absent or empty |
| CAN-002 | Manifest absent |
| CAN-003 | Schema version inconsistency in canonical files |
| CAN-004 | Excluded product found in canonical_bsip1 |
| CAN-005 | file_type ≠ "product" in canonical corpus |
| REG-001 | BSIP2 scoring field found in BSIP1 output |
| REG-002 | Frontend/view-model field found in BSIP1 output |
| REG-003 | Unapproved enrichment_version in canonical files |
| REG-005 | Confirmed manual edit of BSIP0 source file |

---

### Warning — Proceed with documented note

These conditions do not block BSIP2 entry but must be recorded in the QA report. The BSIP2 operator must be informed of each warning before scoring begins.

| Code | Condition | Note requirement |
|------|-----------|-----------------|
| SCP-004 | Product count in lower half of expected range | Record actual count; note corpus is thin |
| TRC-005 | Audit file missing (audit_ref present, file absent) | List missing barcodes |
| COV-001 | Nutrition coverage 60–79% | Record coverage %; note fields at risk for BSIP2 |
| COV-002 | Ingredient coverage 50–69% | Note which products lack ingredients |
| COV-003 | Image coverage 70–89% | List products without images |
| COV-004 | > 50% of products are retailer internal IDs | Note cross-retailer deduplication risk |
| COV-005 | Sodium coverage < 60% or sugar coverage < 50% | Note red-label detection risk for BSIP2 |
| CAN-001 | canonical_bsip1 count 1–10% below BSIP0 approved | List missing barcodes; check BSIP1 error log |
| CAN-002 | Manifest entry count differs from file count | Re-generate manifest before BSIP2 |
| REG-004 | Unexpected non-scoring top-level field in BSIP1 | Document field; assess whether it is a schema evolution or an error |
| REG-005 | BSIP0 mtime ambiguously later than scraped_at | Note file and check for manual edits |

---

### Acceptable Known Issue — Documented, does not block

These patterns are expected and do not require action. They must be visible in the report but generate no Warning or Fail verdict.

| Pattern | Reason acceptable |
|---------|------------------|
| `missing_fields: ["serving_size_g"]` | Serving size is optional in BSIP1; Israeli retail labels often omit it |
| `missing_fields: ["canonical_name_en"]` | English name is not required; Bari is Hebrew-primary |
| `barcode_confidence: "inferred"` on retailer-internal IDs | Expected for short-code Shufersal products and 16000-prefix Yohananof codes; documented in `barcode_confidence_reason` |
| `observation_count: 1` for all products | Expected on single-retailer scrape (Shufersal only); multi-source enrichment will improve on Yohananof supplementary pass |
| `canonical_trust_level: "low"` for single-source products | Expected; `canonical_risk_flags: ["single_source_only"]` documents the reason; does not indicate bad data |
| `enrichment_warnings: [...]` for edge cases | Non-fatal enrichment notes; reviewed in BSIP2 operator briefing |
| `ingredient_text_quality: "noisy"` for a minority of products | Retailer HTML sometimes embeds nutrition text in the ingredient field; BSIP1 flags but does not fail |
| `nutrition_consistency_warnings` for minor rounding differences | Rounding artefacts from retailer display; not a data error |

---

## QA Run Record

Fill in after completing all checks.

**Category:** _______________  
**Run date:** _______________  
**Operator:** _______________  
**BSIP0 source:** _______________  
**BSIP1 run ID:** _______________

| Domain | Hard Fails | Warnings | Pass |
|--------|-----------|----------|------|
| 1 — Scope Integrity | | | |
| 2 — Traceability | | | |
| 3 — Coverage | | | |
| 4 — Canonical Structure | | | |
| 5 — Regression Checks | | | |

**Overall verdict:** [ ] PASS — clear for BSIP2 entry   [ ] FAIL — blocked

**Open items before BSIP2 entry:**

1.  
2.  
3.  

**QA report filed at:** `02_products/{category}/reports/qa_run_{date}.md`

---

## Appendix — Check ID Reference

| ID | Domain | Type | Description |
|----|--------|------|-------------|
| SCP-001 | Scope | Hard Fail | Corpus filter locked |
| SCP-002 | Scope | Hard Fail | Exclusion register exists |
| SCP-003 | Scope | Hard Fail | No out-of-scope products in approved corpus |
| SCP-004 | Scope | Warning | Product count within expected range |
| SCP-005 | Scope | Hard Fail | No multi-pack or catering sizes |
| TRC-001 | Traceability | Hard Fail | BSIP1 source_retailers non-empty |
| TRC-002 | Traceability | Hard Fail | BSIP1 barcode traces to BSIP0 file |
| TRC-003 | Traceability | Hard Fail | ingredients_raw_provenance.source = bsip0_scrape |
| TRC-004 | Traceability | Hard Fail | BSIP0 files have scraped_at and source_url |
| TRC-005 | Traceability | Warning | audit_ref file exists |
| COV-001 | Coverage | Hard Fail / Warning | Nutrition coverage ≥ 80% (HF < 60%) |
| COV-002 | Coverage | Hard Fail / Warning | Ingredient coverage ≥ 70% (HF < 50%) |
| COV-003 | Coverage | Hard Fail / Warning | Image coverage ≥ 90% (HF < 70%) |
| COV-004 | Coverage | Warning | Barcode quality — EAN-13 ratio |
| COV-005 | Coverage | Warning | Sodium and sugar coverage (informational) |
| CAN-001 | Canonical | Hard Fail / Warning | canonical_bsip1 populated |
| CAN-002 | Canonical | Hard Fail / Warning | Manifest exists and count matches |
| CAN-003 | Canonical | Hard Fail | Schema version consistent |
| CAN-004 | Canonical | Hard Fail | No excluded products in canonical |
| CAN-005 | Canonical | Hard Fail | file_type = "product" in all canonical files |
| REG-001 | Regression | Hard Fail | No BSIP2 scoring fields |
| REG-002 | Regression | Hard Fail | No frontend/view-model fields |
| REG-003 | Regression | Hard Fail | enrichment_version approved |
| REG-004 | Regression | Warning | No unexpected top-level fields |
| REG-005 | Regression | Hard Fail / Warning | BSIP0 source files unmodified |

---

*Bari Category Factory QA Checklist v1*  
*QA & Audit Lead — 2026-05-30*  
*Applies to: all category runs from Hummus (Wave 1) onward*  
*Next version trigger: new BSIP1 schema version, new retailer added, or three consecutive runs expose a gap not covered by this checklist*
