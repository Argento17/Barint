# Bari Category Factory — Workflow v1

**Version:** 1.0  
**Date:** 2026-05-30  
**Owner:** Head of Product  
**Derived from:** Hummus category onboarding (TASK-018, TASK-024, TASK-025, TASK-026, TASK-027, TASK-031, TASK-034, TASK-035)  
**Status:** Active — applies to all category runs from Hummus (Wave 1) onward  
**Next review trigger:** Third category completed, or any stage produces a systematic failure not covered here

---

## Overview

The Category Factory is the repeatable process for taking a new food category from zero data to a scored, frontend-ready comparison. It has ten stages. Each stage has a defined owner, inputs, outputs, and pass criteria. No stage may be skipped; a category proceeds only when the prior stage gate is closed.

**Pipeline at a glance:**

```
Stage 1 — Category Selection
    ↓ decision memo
Stage 2 — Shelf Mapping
    ↓ corpus_filter.md (draft)
Stage 3 — Inclusion / Exclusion Rules
    ↓ corpus_filter.md (locked)
Stage 4 — BSIP0 Acquisition
    ↓ observations_bsip0/
Stage 5 — BSIP0 Gate
    ↓ gate_result.md (PASS)
Stage 6 — Corpus Cleanup
    ↓ clean observations + exclusion_log.json
Stage 7 — BSIP1 Enrichment
    ↓ canonical_bsip1/
Stage 8 — QA Gate (category_factory_qa_v1)
    ↓ qa_run_{date}.md (PASS)
Stage 9 — BSIP2 Readiness
    ↓ intelligence_bsip2/run_{category}_001/
Stage 10 — Website Readiness
    ↓ {category}_frontend_v1.json → /hashvaot/{category}
```

---

## Stage 1 — Category Selection

**Objective:** Confirm that a category is worth onboarding: sufficient retail presence, viable corpus size, non-overlapping with existing categories.

**Owner:** Head of Product

**Inputs:**
- Category brief (internal — what the category is, why it matters to users)
- Rough shelf survey (manual browse of Shufersal / Yohananof to estimate product count)
- Existing category list (confirm no overlap)

**Outputs:**
- Selection decision memo (1 page): category name, primary shelf code, estimated corpus size, rationale, known scope ambiguities, deferred categories
- Named task ID for tracking

**Pass criteria:**
- Estimated corpus ≥ 30 products at single retailer
- No direct overlap with an active or in-progress category
- At least one shelf category code identified at Shufersal or Yohananof
- Head of Product sign-off

**Common failure modes:**
- Category is a sub-variant of an existing one (e.g., "light hummus" when "hummus" is already planned) — resolve by expanding existing category scope, not creating a new one
- Corpus estimate is based on a category that contains many non-food items (cleaning products, pet food shelved nearby)
- No shelf code found — retailer reorganised or category is distributed across multiple unrelated codes

**Activity type:** Manual. Strategy call, no tooling required.

---

## Stage 2 — Shelf Mapping

**Objective:** Identify every Shufersal and Yohananof shelf code that contains in-scope products, quantify contamination, and decide which codes to traverse fully vs. selectively vs. skip.

**Owner:** Frontend Architect (execution) — Head of Product (sign-off on traverse decisions)

**Inputs:**
- Selection decision memo from Stage 1
- Retailer shelf hierarchy (Shufersal: browse `/online/he/c/` URLs; Yohananof: category search)
- Quick probe run of the primary shelf code (list product names, count by type)

**Outputs:**
- Shelf mapping table: one row per shelf code, columns: code, label (Hebrew), scrape strategy (Full / Selective / Search-only / Exclude), contamination estimate, notes
- List of supplementary search queries (Hebrew) for products likely outside the primary shelf
- Preliminary product count estimate by subcategory

**Pass criteria:**
- At least one code assigned Full or Selective traversal
- Contamination rate documented for every Selective code (how many products in the code are clearly out of scope)
- Search query list covers brand-name variants and organic/light/protein sub-variants

**Common failure modes:**
- Primary code has high contamination (Hummus: A162407 = 80% contamination — switched to search-only). Always probe before committing to full traversal.
- Retailer uses a flat `All Salads` code that contains dozens of unrelated products. Do not traverse blindly — contamination can inflate discovery by 5–10×.
- Search queries in Hebrew can return false positives from product descriptions. Queries should target product names (`name_he`), not descriptions.

**Activity type:** Mostly manual. Probe script is reusable (Shufersal probe_v3.py exists); decision-making on traverse strategy is manual.

**Future automation candidate:** Medium ROI. A probe tool that auto-classifies a shelf code's contamination rate (product count × % matching category keywords) would save 1–2 hours per category. Feasible with existing Shufersal HTML parser.

---

## Stage 3 — Inclusion / Exclusion Rules

**Objective:** Produce a locked, human-readable document that defines exactly which products are in scope and which are not — including edge cases, blend rules, and scope-adjacent decisions.

**Owner:** Head of Product (rules) — Frontend Architect (document format)

**Inputs:**
- Shelf mapping output from Stage 2
- Product name list from probe run (to ground the rules in real examples)
- Any prior scope decisions from similar categories (e.g., Hummus/Tahini boundary decision TASK-026)

**Outputs:**
- `corpus_filter.md` in `02_products/{category}/` — locked with date and version
  - IN-scope table (product types, Hebrew names, notes)
  - OUT-scope table (types, reasons)
  - Edge-case rules (blend rules, size exclusions, format exclusions)
  - BSIP0 gate thresholds (minimum counts and coverage %)
  - Expected score distribution (for Stage 8 / 9 calibration)

**Pass criteria:**
- Document contains a lock statement (`*This document is locked.*` or equivalent)
- Every edge case identified in Stage 2 is resolved with an explicit rule
- Gate thresholds are set (minimum product count ≥ 30, nutrition ≥ 80%, ingredients ≥ 70%, images ≥ 90%)
- Head of Product sign-off recorded in document or task note

**Common failure modes:**
- Rules too vague ("include if it looks like hummus") — every rule must have a positive example and a rejection example
- Tahini / hummus boundary not resolved before scraping. Any two adjacent categories (hummus/tahini, yogurt/dairy desserts, snack bars/protein bars) need an explicit blend rule before acquisition starts. Lack of clarity generates rework at Stages 4–6.
- Catering sizes not excluded: default rule for all categories — exclude single-unit formats ≥ 1 kg and multi-packs
- Rules written for the primary product type but not for the secondary types (e.g., corpus_filter covers hummus well but is vague on eggplant spreads)

**Activity type:** Manual. Document writing is manual; format can be templated.

**Future automation candidate:** Low ROI. Rules require domain knowledge. A checklist template is sufficient.

---

## Stage 4 — BSIP0 Acquisition

**Objective:** Discover and scrape all in-scope products from at least one retailer, producing raw JSON observations in `observations_bsip0/{retailer}/`.

**Owner:** Frontend Architect

**Inputs:**
- `corpus_filter.md` (locked) from Stage 3
- Shufersal shelf codes and search query plan from Stage 2
- Scraper scripts for the relevant retailer(s) — `shufersal_hummus/01_discover_*.py` and `02_scrape_*.py`

**Outputs:**
- `all_discovered_raw_{date}.json` — full raw discovery list (all candidates before approval)
- `candidate_review.csv` — one row per candidate; columns: code, name, suggested_decision, decision_reason, approved_for_scrape
- One `P_{code}.json` per approved product (Shufersal format) — containing: name, barcode, source_url, scraped_at, nutrition (raw strings), ingredients_raw, image_urls

**Process (Shufersal):**
1. Run `01_discover_hummus_shufersal.py` — traverses shelf codes + search queries, writes CSV
2. Review `candidate_review.csv`:
   - Rows where `suggested_decision = YES` — set `approved_for_scrape = YES`
   - Rows where `suggested_decision = REVIEW` — apply corpus_filter rules, set YES or NO manually
   - Rows where `suggested_decision = REJECT` — leave as NO (trust the hard-exclude filter)
3. Run `02_scrape_hummus_shufersal.py` — reads approved rows, scrapes product pages

**Pass criteria:**
- `candidate_review.csv` exists with a non-empty header
- All REVIEW rows have a manual decision (no blank `approved_for_scrape` cells in REVIEW rows)
- Approved product file count in `observations_bsip0/{retailer}/` ≥ corpus_filter.md minimum

**Common failure modes:**
- Scraper constants not defined — Hummus: `PRODUCT_PAGE_DELAY` was missing, caused immediate crash after product 1. Check all constant definitions before the first run.
- Maintenance mode — Shufersal occasionally returns a maintenance page mid-scrape. The scraper checks for this but can silently skip products. Check scrape completion log for gaps.
- Keyword hard-exclude too narrow — "גרגרי חומוס" (chickpea kernels) passed through because the exclude list targeted product-type terms (tahini, labane) not raw-ingredient terms. Add raw-ingredient signals to hard-exclude for every category that sells both spread and raw-ingredient forms.
- Suggested YES includes items with "חומוס" in a product description rather than the product name — dairy products, organic produce, and noodle meals triggered this. Always sample 5–10 auto-YES names before approving the full batch.
- UTF-8 encoding not set — Windows cp1252 shells will silently truncate or corrupt Hebrew output. All scripts must call `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.

**Activity type:** Mix. Scraper execution is automated; candidate review (REVIEW rows) is manual, 30–60 minutes depending on contamination rate.

**Future automation candidates:**
1. **Auto-classify REVIEW rows using product-type classifier** — High ROI. The current keyword filter produces ~97 REVIEW items per category. A lightweight Hebrew product-type classifier (trained on the hard-exclude/positive-type lists) could reduce manual review to <10 items per run.
2. **Auto-detect constant definition errors before run** — Low ROI but very cheap: a pre-flight check script that imports the scraper and validates all required constants are defined.
3. **Maintenance-mode retry with exponential backoff** — Medium ROI. Currently a maintenance-mode response silently drops a product. A retry wrapper would recover 2–5 products per run.

---

## Stage 5 — BSIP0 Gate

**Objective:** Confirm the scraped corpus meets minimum quality thresholds before the expensive cleanup and enrichment stages begin.

**Owner:** Frontend Architect

**Inputs:**
- All `P_*.json` files in `observations_bsip0/{retailer}/`
- `corpus_filter.md` for gate thresholds

**Outputs:**
- `reports/bsip0_gate_result_{timestamp}.md` — PASS or FAIL with per-criterion breakdown

**Gate criteria (Hummus defaults — override in corpus_filter.md for other categories):**

| Criterion | Minimum | Hard gate |
|---|---|---|
| Total approved products | ≥ 30 (target 50–60) | Yes |
| Nutrition coverage (energy+protein+carbs+fat) | ≥ 80% | Yes |
| Ingredient list coverage | ≥ 70% | Yes |
| Image URL availability | ≥ 90% | Yes |
| Retailer traceability (source_url present) | 100% | Yes |
| corpus_filter.md exists and is locked | Yes | Yes |

**Pass criteria:** All six criteria pass.

**Common failure modes:**
- Emoji in print statements cause `UnicodeEncodeError` on Windows cp1252 shells — `03_audit_bsip0_hummus.py` had this issue. Fix: add `sys.stdout.reconfigure(encoding="utf-8")` to every audit script.
- Gate passes on the full scrape count (82) but some of those products are out-of-scope (e.g., chickpea kernels). The gate counts total files, not in-scope files. Always run a rough type classification (Stage 6 pre-check) before treating the gate as a final corpus quality signal.
- If product count fails, uncomment the optional shelf code (A162405 for Hummus) before concluding the category is too small.

**Activity type:** Automated. Gate script runs in seconds.

**Future automation candidate:** Low additional ROI (already automated). Enhancement: add an OOS-product quick-scan to the gate script so out-of-scope slippage is caught here rather than in Stage 6.

---

## Stage 6 — Corpus Cleanup

**Objective:** Remove out-of-scope products that passed Stage 4's keyword filter, preserve an audit trail, and confirm the clean corpus count before enrichment.

**Owner:** Frontend Architect

**Inputs:**
- All `P_*.json` files in `observations_bsip0/{retailer}/`
- `corpus_filter.md` (OUT-scope rules)
- Optionally: `bsip0_gate_result_*.md` for the total pre-cleanup count

**Outputs:**
- `observations_bsip0/{retailer}/_excluded_bsip0/` — quarantine directory for OOS files
- `_excluded_bsip0/exclusion_log.json` — one entry per excluded product: file, barcode, name_he, reason, excluded_at, excluded_by (task ID)
- Remaining `P_*.json` in the parent directory = clean in-scope corpus
- Updated count confirmed in task report

**Process:**
1. List all `P_*.json` files; inspect names against OOS signal terms
2. For every flagged product: load JSON, verify via `source_category` + ingredient text that it is genuinely OOS
3. Call `shutil.move()` to quarantine, write entry to exclusion_log.json
4. Count remaining files; confirm ≥ corpus_filter.md minimum

**Pass criteria:**
- Exclusion log written with a non-zero entry count (or an explicit "no exclusions" entry if the corpus was clean)
- No flagged product remains in the parent observations directory
- False-positive check: every excluded product's `source_category` and `ingredients_raw` were inspected before exclusion — products with both nutrition and ingredient data from a shelf code (not just search) need a second look before exclusion

**Common failure modes:**
- **False positives from keyword-based OOS detection** — Hummus: `חומוס גרגרים בתטבילה` (hummus with whole chickpeas in sauce) was initially classified as OOS based on the "גרגר" keyword. Saved from exclusion by checking `source_category` (A162406 = hummus shelf) and `ingredients_raw` (confirmed chickpea-tahini paste). Rule: never exclude a product solely on name keywords if it has ingredient data confirming it is a spread/dip.
- **Quarantine directory created inside observations directory without .gitignore** — excluded files remain visible to the pipeline. The `_excluded_bsip0/` naming convention (leading underscore) is deliberately chosen to be excluded by glob patterns (`P_*.json`) but a `.gitignore` entry is also recommended.
- **No audit trail** — if OOS products are simply deleted without logging, it is impossible to reconstruct what was removed or why. The exclusion_log.json is mandatory even if it contains only 1 entry.
- **Aggressive exclusion of boundary products** — it is better to include a borderline product and flag it for BSIP2 attention than to exclude and lose a real data point. The standard is: exclude only products whose ingredient text confirms they are not a dip/spread, or products with no ingredient data at all from a known-OOS product type.

**Activity type:** Semi-automated. OOS detection can be scripted; the false-positive verification for each flagged product requires human judgment (5–15 minutes for a hummus-size corpus).

**Future automation candidate:** High ROI. A reusable `corpus_cleanup.py` that:
- Takes the observations directory + a list of OOS signal terms from corpus_filter.md
- Flags candidates automatically
- Requires human confirmation only for candidates from a shelf code (not just search)
- Writes exclusion_log.json automatically
Would reduce this stage to a 5-minute human confirmation step.

---

## Stage 7 — BSIP1 Enrichment

**Objective:** Convert BSIP0 raw observations to the BSIP1 canonical schema, normalize nutrition fields, clean ingredient text, and run the ingredient enricher to extract semantic signals.

**Owner:** Frontend Architect

**Inputs:**
- Clean `P_*.json` files in `observations_bsip0/{retailer}/` (post-cleanup)
- `enrich_runner.py` and `ingredient_enricher.py` from `03_operations/bsip1/core/`
- The `bsip1_v0_1` schema

**Outputs:**
- `03_operations/bsip1/run_{category}_001/output/bsip1_{barcode}.json` — one enriched BSIP1 file per product
- `03_operations/bsip1/reports/enrichment_validation_001.md` — coverage and signal report
- `02_products/{category}/canonical_bsip1/bsip1_{barcode}.json` — mirror of run output (copy, not symlink)
- `02_products/{category}/canonical_bsip1/manifest.json` — lists every canonical file by barcode and product ID

**Process:**
1. Write `run_{category}_001/convert_bsip0_to_bsip1.py` — converts raw BSIP0 fields to BSIP1 schema
   - Normalize nutrition (parse Hebrew strings like `"פחות מ 0.5"` → 0.0)
   - Clean ingredients_raw (strip trailing metadata: `"ערכים תזונתיים..."`, `"מאפיינים נוספים..."`)
   - Populate `bsip0_source` provenance block
2. Run converter → produces `bsip1_*.json` in run output directory
3. Register run in `enrich_runner.py` RUNS dict
4. Run `enrich_runner.py --run run_{category}_001` → applies enrichment in-place
5. Copy enriched files to `canonical_bsip1/`
6. Write `canonical_bsip1/manifest.json`

**Pass criteria:**
- Conversion: 0 errors
- Enrichment: runs without crash
- Raw ingredient text available for ≥ 70% of products
- All files present in `canonical_bsip1/`

**Common failure modes:**
- **`enrich_runner.py` BSIP0 lookup targets Yohananof only** — the enricher's `_try_bsip0_raw()` function looks in `03_operations/bsip0/scrape/yohananof/outputs/`. For Shufersal products, it returns `bsip0_file_not_found` and falls back to `ingredients_text_he`. This is correct behaviour — the ingredient text is still available — but provenance will show `bsip1_text_fallback`, not `bsip0_scrape`. This is expected and acceptable for Shufersal runs. Document in the run report; do not treat as an error.
- **Ingredient text contains marketing copy** — Shufersal HTML embeds nutritional tables and marketing text in the same HTML block as ingredients. The converter must strip these (marker-based truncation on `"ערכים תזונתיים"`, `"מאפיינים נוספים"`, `"ttrn"`, `"הנתונים המדויקים"`). Products where this fails produce parsing artefacts in enrichment (average ingredient count inflated). Identified at Stage 8 by checking samples.
- **`run_{category}_001` not added to `RUNS` dict** — the enricher silently skips unknown runs. Always add the run entry before calling `enrich_runner.py`.
- **Nutrition raw string edge cases** — Shufersal encodes values like `"פחות מ 0.5"` (less than 0.5) and `"<0.5"` for trace amounts. The converter must use regex for the first numeric value (`_NUM_RE`) rather than `float()` directly.
- **Weight extraction from product name** — many products have no `weight_g` field because the scraper failed to parse it. The BSIP1 converter should attempt weight extraction from `name_he` as a fallback (patterns: `גרם`, `ג'`, `g`, `ק"ג`, `מ"ל`).

**Activity type:** Mix. Converter script is written once per category (15–30 minutes). Enrichment is fully automated.

**Future automation candidates:**
1. **Universal BSIP0→BSIP1 converter** — High ROI. The conversion logic (nutrition normalization, ingredient cleaning, schema mapping) is >90% identical across categories. A parameterized `convert_bsip0_to_bsip1.py` with a category configuration dict (retailer, shelf code, nutrition field map) would eliminate the per-category script entirely.
2. **Extend `_try_bsip0_raw()` to Shufersal** — Medium ROI. Currently only Yohananof BSIP0 data is indexed for ingredient lookup. Adding Shufersal lookup would improve provenance traceability.
3. **Ingredients text quality classifier** — Medium ROI. A simple classifier that detects marketing copy contamination in the ingredient field would flag affected products before enrichment runs.

---

## Stage 8 — QA Gate

**Objective:** Validate that the canonical BSIP1 corpus meets all structural, coverage, traceability, and regression criteria before BSIP2 scoring begins.

**Owner:** QA & Audit Lead

**Inputs:**
- `canonical_bsip1/` (populated)
- `observations_bsip0/{retailer}/candidate_review.csv`
- `observations_bsip0/{retailer}/_excluded_bsip0/exclusion_log.json`
- `corpus_filter.md`
- `03_operations/qa/category_factory_qa_v1.md` (the QA checklist)

**Outputs:**
- `02_products/{category}/reports/qa_run_{date}.md` — completed QA checklist with verdict
- List of open items to resolve before BSIP2 entry (if any)

**QA domains (from `category_factory_qa_v1.md`):**
1. **Scope Integrity** (SCP-001–SCP-005) — corpus filter locked, exclusion register exists, no OOS products, count in range, no multi-packs
2. **Traceability** (TRC-001–TRC-005) — source_retailers set, barcodes traceable, ingredient provenance recorded, timestamps present
3. **Coverage** (COV-001–COV-005) — nutrition ≥ 80%, ingredients ≥ 70%, images ≥ 90%, barcode quality, sodium/sugar informational
4. **Canonical Structure** (CAN-001–CAN-005) — folder populated, manifest exists, schema consistent, no excluded products in canonical, file_type = product
5. **Regression Checks** (REG-001–REG-005) — no BSIP2 fields, no frontend fields, enrichment version approved, no unexpected fields, BSIP0 files unmodified

**Pass criteria:**
- Zero Hard Fail items open
- All Warnings documented with action note or explicit deferral reason
- QA report filed in category reports directory

**A category may not enter BSIP2 while any Hard Fail check is open.**

**Common failure modes:**
- `manifest.json` missing from canonical_bsip1 (CAN-002 Hard Fail) — always generate manifest as part of Stage 7
- `ingredients_raw_provenance.source ≠ "bsip0_scrape"` (TRC-003 Hard Fail) — triggered on all Shufersal products because the enricher's BSIP0 lookup only covers Yohananof. This check needs to be updated to accept `bsip1_text_fallback` as a valid provenance source when the retailer is `shufersal` and `ingredients_text_he` is populated. *Current status: open issue for QA v1.1.*
- `audit_ref` field absent (TRC-005 Warning) — the current BSIP1 schema does not populate `audit_ref` for Shufersal-sourced products. Acceptable as a Warning for Wave 1; add to converter in Wave 2.
- Unexpected top-level fields (REG-004 Warning) — TASK-034 converter adds `bsip0_source` and `bsip1_converted_at` and `bsip1_conversion_source`, which are not in the approved schema. These are provenance fields, not scoring fields — acceptable as Warnings; add to schema whitelist in v0_2.

**Activity type:** Manual (checklist completion). Some checks can be scripted (see automation section).

**Future automation candidates:**
1. **Automated QA runner** — High ROI. 15 of the 21 checks are mechanical verifications (file existence, field counts, field values). A script that runs all mechanical checks and outputs a pre-filled QA report with PASS/FAIL for each item would reduce QA from 60 minutes to a 10-minute human review of flagged items.
2. **OOS product detector** — Medium ROI (already partially built in the corpus cleanup stage). Integrating it into the QA check for SCP-003 would catch any OOS slippage not caught in Stage 6.

---

## Stage 9 — BSIP2 Readiness

**Objective:** Confirm that the BSIP2 scoring engine can accept the category's canonical BSIP1 records, run the batch scorer, and produce `bsip2_trace.json` per product.

**Owner:** Frontend Architect

**Inputs:**
- `canonical_bsip1/` (QA gate passed)
- `03_operations/bsip2/proto_v0/src/batch_runner.py`
- BSIP2 category configuration (archetype routing, score formula parameters)

**Outputs:**
- `intelligence_bsip2/run_{category}_001/products/bsip1_{barcode}/bsip2_trace.json` — one scored trace per product
- Run summary report

**Pass criteria:**
- All products produce a `bsip2_trace.json` (no silent failures)
- Score distribution aligns with expected ranges from `corpus_filter.md` (e.g., plain 3-ingredient hummus should score A; industrial hummus with gums should score C–D)
- No product scores outside 0–100 range
- `grade` field populated for all products with ≥ 60% nutrition coverage

**Common failure modes:**
- BSIP2 archetype router does not recognise the new category — requires a new archetype config entry. Categories with a new primary ingredient type (e.g., chickpea/eggplant/pepper) may need a new routing rule.
- Score formula constants written for bread or snacks do not transfer to spreads — degradation signals, engineering intensity, and assembly drag weights may need recalibration. Do not change existing category weights; create a category-specific config.
- Products with marketing copy in `ingredients_text_he` (see Stage 7 failure modes) produce inflated NOVA scores — they appear to have more ingredients than they do. Fix at source (Stage 7 converter) before re-running BSIP2.

**Activity type:** Automated (batch runner). Configuration additions are manual.

---

## Stage 10 — Website Readiness

**Objective:** Generate the frontend JSON dataset, copy it to the website repo, and confirm the comparison page renders correctly.

**Owner:** Frontend Architect (data pipeline) — Cursor (frontend implementation)

**Inputs:**
- `intelligence_bsip2/run_{category}_001/` (BSIP2 completed)
- `build_frontend_dataset.py` (or equivalent builder)
- Frontend comparison template spec (`01_framework/frontend/comparison_template_v1.md`)
- Category definition in `src/lib/comparisons/registry/categories/`

**Outputs:**
- `{category}_frontend_v1.json` in `03_operations/bsip2/...` or build output
- JSON copied to `C:\bari\bari-web\src\data\comparisons\`
- Route page at `src/app/hashvaot/{category}/page.tsx`
- Frontend comparison components (Cursor build, following `component_build_sequence_v1.md`)

**Pass criteria:**
- JSON file is valid JSON and contains ≥ 30 displayable products
- All products in JSON have `displayable: true` or equivalent
- Route renders without console errors in development
- Comparison table, product detail panel, and filter system all functional

**Common failure modes:**
- Score distribution produces no A-grade products — the page is misleading if nothing is "excellent." Review corpus_filter expected distribution before publishing.
- Frontend JSON references image URLs that are no longer served by the retailer — CDN link rot. Add URL-reachability check to the build step.
- Category page build not added to site navigation — add to `navLinks` in `site-header.tsx` and to the `/hashvaot` index page.

**Activity type:** Mix. JSON build is automated; frontend route and components are built by Cursor under Frontend Architect supervision.

---

## Activity Classification

### Manual activities (require human judgment)

| Stage | Activity | Time estimate |
|---|---|---|
| 1 | Category selection decision | 2–4 hours |
| 2 | Traverse strategy decisions for shelf codes | 30–60 min |
| 3 | Writing inclusion/exclusion rules and edge cases | 2–4 hours |
| 4 | Reviewing REVIEW-flagged candidates in CSV | 30–60 min |
| 6 | False-positive verification for OOS candidates | 15–30 min |
| 8 | QA checklist completion (human judgment items) | 30–60 min |
| 9 | Score distribution review against expected ranges | 30–60 min |
| 10 | Navigation/index wiring | 15–30 min |

**Total manual time per category: ~8–14 hours** (of which ~3–6 hours is domain knowledge that cannot be automated)

### Repetitive activities (same logic every category, scriptable)

| Stage | Activity | Current state |
|---|---|---|
| 4 | Running discover + scrape scripts | Automated per-category script; not yet unified |
| 5 | Gate audit | Automated (per-category script) |
| 6 | Quarantine script + exclusion_log | Per-category script (reusable with config) |
| 7 | BSIP0→BSIP1 converter | Per-category script (90% boilerplate) |
| 7 | Enrichment runner | Automated (shared enrich_runner.py) |
| 7 | Copy to canonical_bsip1 | Manual shutil call (1 line, scriptable) |
| 7 | Write manifest.json | Not yet automated — must add to pipeline |
| 8 | Mechanical QA checks (15 of 21) | Not yet automated |
| 9 | BSIP2 batch run | Automated (shared batch_runner.py) |
| 10 | Frontend JSON build | Automated (shared builder) |

---

## Automation Candidates — Ranked by ROI

| Rank | Automation | ROI rationale | Stage | Effort |
|---|---|---|---|---|
| 1 | **Universal BSIP0→BSIP1 converter** | Eliminates 15–30 min of script writing per category; current converter is 90% boilerplate | 7 | Low — parameterize existing convert_bsip0_to_bsip1.py with a config dict |
| 2 | **Automated QA runner** | 15 of 21 checks are mechanical; script can pre-fill the report, reducing QA from 60 to 10 min | 8 | Medium — requires reading all canonical files and checking field by field |
| 3 | **REVIEW row auto-classifier** | 82–97 REVIEW items per category; classifier using the hard-exclude/positive-type lists could reduce manual review to <10 rows | 4 | Medium — Hebrew product name classification, can use the existing ADDITIVE_TERMS / POSITIVE_TYPES logic |
| 4 | **Corpus cleanup reusable script** | False-positive verification is a 15-min task that is identical in structure every run | 6 | Low — parameterize existing cleanup script; add shelf-code confidence weighting |
| 5 | **manifest.json generator** | Currently manual after Stage 7; 5-line script, always required | 7 | Very low |
| 6 | **Maintenance-mode retry wrapper** | Recovers 2–5 silently skipped products per Shufersal run | 4 | Low |
| 7 | **OOS quick-scan in BSIP0 gate** | Catches the chickpea-kernel class of error at Stage 5 instead of Stage 6 | 5 | Low — add name scan to audit script |
| 8 | **Ingredient text quality classifier** | Detects marketing-copy contamination before enrichment | 7 | Medium — needs labeled examples; 3–5 training examples per category type |
| 9 | **Extend BSIP0 ingredient lookup to Shufersal** | Improves provenance traceability; TRC-003 will pass without manual adjustment | 7/8 | Medium — requires Shufersal barcode→file mapping in ingredient_enricher.py |
| 10 | **Shelf contamination probe tool** | Automates the 30-min manual shelf browse in Stage 2 | 2 | Medium — reuse shufersal_probe_v3.py with product-type classification |

---

## Lessons Learned from Hummus

### False-positive exclusions

**Issue:** Keyword-based OOS detection in Stage 6 flagged `חומוס גרגרים בתטבילה` (hummus with whole chickpeas, Achla brand) as a chickpea-kernel product. It was a genuine hummus spread.

**Root cause:** The exclusion signal `גרגר` (kernel/grain) appears in the names of both raw chickpea beans AND hummus products marketed as having whole chickpeas.

**Rule:** Before excluding any product based on a name keyword, always check:
1. `source_category` — a product on the hummus shelf (A162406) is almost certainly a spread
2. `ingredients_raw` — if the first ingredient is `חומוס מבושל %N` or `טחינה`, it is a spread regardless of the name

**General rule:** Never exclude a product solely on name keywords if it has ingredient data confirming it is in-scope. The ingredient list is more reliable than the name.

---

### Retailer data quality issues

**Shufersal ingredient extraction:**
- The Shufersal HTML parser extracts ingredient text from a shared block that also contains nutritional tables, marketing claims, and allergen statements. A significant minority of products (~15%) have trailing metadata in the ingredient field: `"ערכים תזונתיים..."`, `"מאפיינים נוספים..."`, `"ttrn"`.
- Mitigation: truncate ingredient text at known junk markers. Add new markers to the list as they are discovered.
- One product (`חומוס שלם יכין`, P_208428) had marketing copy extracted as the entire ingredient field — nutritional benefit claims instead of ingredient list. This produces enrichment artefacts. For Hummus, this affected 1/69 products (1.4%). Accept as noise; flag for manual follow-up.

**Shufersal barcode quality:**
- Short-code products (5–7 digit codes like `P_208428`, `P_467153`) are internal IDs, not EAN-13. They are still valid for single-retailer use but cannot be cross-matched against Yohananof without a second lookup.
- About 20–25% of hummus products use short codes. Acceptable for BSIP2; reduces cross-retailer confidence to `"inferred"`.

**Shufersal nutrition raw strings:**
- Fat values frequently encoded as `"פחות מ 0.5"` (less than 0.5) for near-zero values. The converter must parse these with `_NUM_RE` (first numeric group) rather than `float()` to extract 0.5 as the maximum value. Do not assume all nutrition fields are clean numbers.

---

### Ingredient coverage problems

**Issue:** 4/69 products (5.8%) had no ingredient text. All four were generic no-brand `"חומוס"` SKUs, likely private-label products with minimal information on the retailer page.

**Pattern:** Products with generic names and no brand tend to have poor ingredient coverage. The threshold failure mode is: a category where many products are private-label (e.g., a retailer's own-brand range) will have lower ingredient coverage than a brand-rich category.

**Expected rates by product type (Hummus baseline):**
- Named-brand hummus: >95% ingredient coverage
- Private-label / no-brand: ~60–70% ingredient coverage
- Eggplant spreads and matbucha: ~90% ingredient coverage
- Chickpea kernels (which should have been excluded): ~60% — this is a signal that these are not spread products

**Rule:** If ingredient coverage for a product type is below 75%, investigate whether the type belongs in the category at all. Low coverage is often a proxy for "this product doesn't have a readable label."

---

### Audit trail requirements

Four audit artifacts must exist before a category enters BSIP2. All four were missing or incomplete in the Hummus Wave 1 run and must be added to Stage 7:

| Artifact | Location | Required content |
|---|---|---|
| `candidate_review.csv` | `observations_bsip0/{retailer}/` | All discovered products with final approved_for_scrape value |
| `exclusion_log.json` | `observations_bsip0/{retailer}/_excluded_bsip0/` | Every excluded product with reason + task ID |
| `manifest.json` | `canonical_bsip1/` | barcode, canonical_product_id, file_path for every canonical file |
| `qa_run_{date}.md` | `reports/` | Completed QA checklist with verdict |

The absence of `manifest.json` and a completed `qa_run` report are the two most common blockers at Stage 8. Both should be generated automatically at the end of Stage 7.

---

### Expected category size ranges

Based on Hummus (Wave 1) and the existing snack_bars, milk, and yogurt categories:

| Category type | Discovery count | After approval | After cleanup | Notes |
|---|---|---|---|---|
| Single-type dip/spread (hummus) | 120–200 | 70–100 | 60–80 | High name-variation; search phase finds ~40% of total |
| Dairy (milk, yogurt) | 40–80 | 30–60 | 30–60 | Low contamination; mostly shelf traversal |
| Snack bars / protein bars | 80–150 | 50–100 | 45–90 | High multi-pack contamination |
| Bread / bakery | 200–400 | 80–130 | 70–120 | Very high name variation; many private-label |
| Multi-type category (hummus + eggplant + matbucha) | 150–250 | 80–120 | 65–100 | Secondary types add 15–25 products but also add contamination |

**Minimum viable corpus for BSIP2:** 30 products (absolute minimum for meaningful comparison). Target: 50+ for a publishable page.

**Contamination rate by shelf type:**
- Dedicated category shelf (A162406): ~10–20% contamination
- Mixed salads shelf (A162407): ~70–80% contamination — use search queries only
- Search-phase results: ~30–50% contamination — requires full candidate review

---

## Workflow File Map

```
C:\Bari\
├── 01_framework\
│   └── governance\category_audit_{name}_v1.md   ← Stage 2/3 shelf + scope docs
├── 02_products\{category}\
│   ├── corpus_filter.md                          ← Stage 3 output (locked)
│   ├── README.md                                 ← workspace doc
│   ├── observations_bsip0\{retailer}\
│   │   ├── all_discovered_raw_{date}.json        ← Stage 4
│   │   ├── candidate_review.csv                  ← Stage 4 (with YES/NO column filled)
│   │   └── _excluded_bsip0\
│   │       ├── exclusion_log.json                ← Stage 6 (required)
│   │       └── P_{code}.json × N                 ← quarantined OOS products
│   ├── canonical_bsip1\
│   │   ├── manifest.json                         ← Stage 7 (required for QA)
│   │   └── bsip1_{barcode}.json × N              ← Stage 7
│   ├── intelligence_bsip2\run_{name}_001\        ← Stage 9
│   └── reports\
│       ├── bsip0_gate_result_{timestamp}.md      ← Stage 5
│       └── qa_run_{date}.md                      ← Stage 8 (required)
├── 03_operations\
│   ├── bsip0\scrape\
│   │   ├── shufersal_{category}\                 ← discover + scrape + audit scripts
│   │   └── yohananof_{category}\                 ← discover + scrape scripts
│   ├── bsip1\
│   │   ├── core\enrich_runner.py                 ← shared (add run to RUNS dict)
│   │   └── run_{category}_001\
│   │       ├── convert_bsip0_to_bsip1.py         ← Stage 7 (category-specific)
│   │       └── output\bsip1_{barcode}.json × N
│   ├── bsip2\proto_v0\src\batch_runner.py        ← Stage 9
│   ├── factory\category_factory_v1.md            ← this document
│   └── qa\category_factory_qa_v1.md              ← Stage 8 checklist
```

---

*Category Factory v1 — Bari Internal*  
*Derived from Hummus onboarding (TASK-018 → TASK-035)*  
*Owner: Head of Product*  
*Next version trigger: third category completed, or QA checklist v1.1 published*
