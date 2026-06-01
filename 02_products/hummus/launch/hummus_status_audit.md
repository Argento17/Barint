# Hummus Category — Status Audit

**Task:** TASK-058  
**Owner:** Frontend Agent  
**Date:** 2026-05-31  
**Scope:** Both repos — `C:\Bari` (pipeline) and `C:\Users\HP\bari` (website)

---

## Classification

**D — Factory complete, website work never started**

The full BSIP0 → BSIP1 → BSIP2 pipeline has completed with a QA PASS verdict. 69 products are scored and authoritative. No frontend dataset, category definition, route, or page component exists in the website repo.

---

## Pipeline Repo — `C:\Bari`

### BSIP0 — Observations (Shufersal)

| Item | Status | Detail |
|---|---|---|
| Discovery catalog | COMPLETE | 82 candidates traversed from Shufersal shelf A162406 |
| Product scrape | COMPLETE | 69 approved products scraped (13 excluded) |
| Exclusion log | COMPLETE | 13 rejected products with reasons |
| BSIP0 gate report | PASS | `bsip0_gate_result_20260530_204340.md` — all thresholds met |
| Yohananof supplementary | NOT STARTED | Scripts exist, corpus not populated |

**Gate result (Shufersal only):**

| Criterion | Threshold | Actual | Status |
|---|---|---|---|
| Product count | ≥30 (target 50–60) | 69 | PASS |
| Nutrition coverage | ≥80% | 92.7% | PASS |
| Ingredient coverage | ≥70% | 92.7% | PASS |
| Image coverage | ≥90% | 100% | PASS |
| Retailer traceability | 100% | 100% | PASS |

**Known issue:** Yohananof supplementary corpus not populated. Scripts exist at `C:\Bari\03_operations\bsip0\scrape\yohananof_hummus\`. Non-blocking for launch — Shufersal alone meets gate thresholds.

---

### BSIP1 — Canonical Enrichment

| Item | Status | Detail |
|---|---|---|
| Enriched records | COMPLETE | 69 files in `canonical_bsip1/` |
| Schema version | bsip1_v0_1 | Enrichment version: bsip1_enrichment_v1 |
| Nutrition fields | PARTIAL | energy, protein, carbs, fat, sodium, fiber present; **sugars_g absent** (0/69) |
| Ingredient fields | COMPLETE | ingredients_list (array), ingredients_text_he, tahini_pct_declared, chickpea_pct_declared |
| Retailer traceability | COMPLETE | 100% Shufersal source |

**Known issue — Fat data corruption (HIGH):**
59 of 69 BSIP1 files contain corrupted `fat_g` values. Shufersal's HTML scraper extracted the saturated fat sub-row instead of total fat. Affected products show `fat_g = 0.5` when true total fat is 5–12g for tahini-containing hummus. Detailed per-product analysis: `C:\Bari\02_products\hummus\audit\fat_anomaly_TASK039.json`.

| Severity | Product count |
|---|---|
| CRITICAL | 15 |
| HIGH | 21 |
| MEDIUM | 23 |
| NONE | 10 |

BSIP2 disposition: 58 products `allowed_with_warning`, 11 `allowed`, 0 `blocked`. Fat corruption affects display quality, not score computability.

**Known issue — Sugar data absent (MEDIUM):**
`sugars_g` coverage is 0% (0/69 products). Glycemic quality dimension cannot be fully computed. QA report classifies this as a non-blocking warning — accepted at category level.

---

### BSIP2 — Scoring

| Item | Status | Detail |
|---|---|---|
| run_hummus_001 | INVALID | 44/69 products misrouted to `dessert` via `"מוס"` substring collision in `"חומוס"` |
| run_hummus_002 | AUTHORITATIVE | Routing fixed (TASK-044). 67/69 products route to `sauce_spread`, 2 to `default` |
| Routing fix documentation | COMPLETE | `routing_fix_hummus_v1.md` — root cause, fix, delta per product |
| Production runner output | COMPLETE | `sprint1/outputs/production_hummus.json` |
| Score distribution (run_002) | See below | |

**Score distribution (run_hummus_002, authoritative):**

| Grade | Expected | Actual | Status |
|---|---|---|---|
| A | 5–10 | ~9 | Within range |
| B | 20–28 | ~24 | Within range |
| C | 20–25 | ~22 | Within range |
| D | 10–15 | ~11 | Within range |
| E | 2–5 | ~3 | Within range |

Distribution matches pre-scoring expectations from `hummus_review_framework_v1.md`. No anomalous clustering detected.

**Notable score impacts from routing fix:**

| Product | run_001 score | run_002 score | Grade change |
|---|---|---|---|
| הקיסר חומוס ענק | 79.7 | 80.4 | C→B |
| מלך החומוס אבו מרוואן | 62.2 | 65.2 | C→B |
| 7 products (corrected calorie table) | various | −2.2 to −4.5 | No grade change |

---

### QA Validation

| Item | Status | Detail |
|---|---|---|
| QA report | PASS | `qa\reports\qa_report_hummus.md` — 13/15 checks pass |
| TRC-003 | WARN (non-blocking) | `ingredients_raw_provenance.source = 'bsip1_text_fallback'` — expected exception |
| COV-005 | WARN (non-blocking) | `sugars_g` coverage 0% — accepted at category level |
| Traceability report | PASS | `qa\reports\traceability_report_hummus.md` — 100% Shufersal trace |
| Fat anomaly analysis | DOCUMENTED | `fat_anomaly_TASK039.json` — 59/69 products flagged |

---

### Frontend Dataset

| Item | Status | Detail |
|---|---|---|
| `hummus_frontend_v1.json` | NOT BUILT | No frontend-formatted JSON exists |
| `production_hummus.json` | EXISTS | BSIP2 output at `sprint1/outputs/` — not yet transformed to frontend format |
| `build_frontend_dataset.py` | NEEDS RUN | Must be adapted for hummus category and executed |

The BSIP2 output exists. The frontend-formatted JSON (matching the `BariCategoryPageVM` schema) has not been generated.

---

## Website Repo — `C:\Users\HP\bari`

### Route

| Item | Status | Path |
|---|---|---|
| `/hashvaot/hummus` directory | ABSENT | `src/app/hashvaot/hummus/` does not exist |
| `page.tsx` | ABSENT | — |

Existing routes for reference: `bread/`, `maadanim/`, `snack-bars/`, `yogurts/`, `milk-comparison/`

---

### Category Registry

| Item | Status | File |
|---|---|---|
| `ComparisonCategoryId` type | ABSENT | `"hummus"` not in union: `"maadanim" | "bread" | "snacks" | "yogurts"` |
| Registry import | ABSENT | `index.ts` does not import hummus definition |
| Category definition file | ABSENT | No `hummus.ts` in `src/lib/comparisons/registry/categories/` |

---

### Frontend Data

| Item | Status | Path |
|---|---|---|
| `hummus_frontend_v1.json` | ABSENT | `src/data/comparisons/` has no hummus file |

---

### Component

| Item | Status | Notes |
|---|---|---|
| Comparison page component | ABSENT | No hummus-specific component or Gen 1 page file exists |

---

## Asset Inventory Summary

### `C:\Bari` — Pipeline workspace

| Layer | Files | Status |
|---|---|---|
| BSIP0 observations | 82 product JSON + master discovery JSON + exclusion log | COMPLETE |
| BSIP1 canonical | 69 enriched JSON | COMPLETE (with fat/sugar caveats) |
| BSIP2 traces (run_001) | 69 trace JSON | INVALID — do not use |
| BSIP2 traces (run_002) | 69 trace JSON | AUTHORITATIVE |
| Pipeline scripts | 16 Python files | COMPLETE |
| Reports + documentation | 20+ MD/JSON files | COMPLETE |
| Frontend dataset JSON | 0 files | NOT BUILT |

### `C:\Users\HP\bari` — Website

| Layer | Files | Status |
|---|---|---|
| Route | 0 | NOT CREATED |
| Category registry | 0 | NOT CREATED |
| Category definition | 0 | NOT CREATED |
| Frontend data | 0 | NOT CREATED |
| Page component | 0 | NOT CREATED |

---

## Known Issues Register

| ID | Issue | Severity | Blocking? | Resolution path |
|---|---|---|---|---|
| HUM-001 | Fat data corruption — 59/69 BSIP1 records have wrong `fat_g` (sat fat sub-row captured instead of total fat) | HIGH | No — scores computed with `allowed_with_warning`; display quality affected | Option A: Re-scrape fat values for 59 products before launch. Option B: Suppress fat display or add data caveat label in frontend. |
| HUM-002 | Sugar data absent — `sugars_g` = 0% coverage | MEDIUM | No — QA accepted as category-level limitation | Accept as-is for v1. Document in MethodologyFooter. |
| HUM-003 | run_hummus_001 INVALID — misrouting artifact | LOW | No — run_002 is authoritative; run_001 marked INVALID | Do not reference run_001 in any launch artifact. Use run_002 exclusively. |
| HUM-004 | Yohananof supplementary corpus not populated | LOW | No — Shufersal alone passes gate | Defer to post-launch category expansion. |
| HUM-005 | Frontend dataset not built | BLOCKING | Yes — no JSON to serve | Must run `build_frontend_dataset.py` for hummus before website integration. |
| HUM-006 | All website integration absent | BLOCKING | Yes | Full frontend implementation task required (see gap analysis). |
