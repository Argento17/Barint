# TASK-135A — run_yogurt_002 reconciliation & GO/NO-GO findings

**Owner:** data-agent · **Date:** 2026-06-01 · **Parent:** TASK-135 (DEC-005 retirement)
**Engine:** proto_v0 / 0.4.0 (unmodified — **no manual score edits**)
**Verdict:** 🔴 **NO-GO** for retiring DEC-005 via this run. run_yogurt_002 is **real but ingredient-blind**; it cannot replace the displayed manual-MVP shelf. DEC-005 stays; **TASK-135 cannot close.**

---

## 1. What was executed (full real BSIP0→BSIP2 cycle)

| Stage | Artifact | Result |
|---|---|---|
| BSIP0 scrape | `03_operations/bsip0/scrape/off_yogurt/` (`01_scrape_off_yogurt.py`, `raw/`, `scrape_log.json`) | 50 **real** Israeli yogurt SKUs from Open Food Facts (real 729… barcodes, real brands, provenance URL per item). No synthetic barcodes. |
| BSIP0 curation | `curation_report.json` (`02_curate_and_bsip1.py`) | 50 → **46 included / 4 excluded** (1 drinkable *Lassi*, 3 no-usable-nutrition). Dedup by barcode; no synthetic to drop. |
| BSIP1 map | `03_operations/bsip1/run_yogurt_002/output/bsip1_*.json` (46) | Nutrition normalized per-100g; **ingredients absent → recorded in `missing_fields`**; subtype inferred from name (flagged). Honest enrichment, zero fabrication. |
| BSIP2 score | `02_products/yogurt_system/bsip2_outputs/run_yogurt_002/` (46 traces) + `reports/run_yogurt_002_run_summary.json` | 46 processed, 0 errors, reproducible. |

**Source choice:** Direct Israeli retailers (Shufersal/Yohananof) remain auth-walled/blocked (memory `bsip0_retailer_access_001`); OFF is the same real-data path used for `real_bread_retail_001/003`. OFF's faceted search endpoints were 503 (overloaded) on 2026-06-01; the healthy `search-a-licious` endpoint was used.

## 2. The blocking limitation (measured, not assumed)

**OFF Israeli yogurt ingredient coverage = 0/50.** Not one SKU carries an ingredient list. Yogurt BSIP2 scoring is **ingredient-structure-driven** (router, NOVA proxy, fermentation/culture markers, additive & sweetener & stabilizer penalties, `bsip_yogurt_subtype`). With no ingredients, every one of those signals is empty.

The engine reports this itself: top scorer's `explanation_drivers` = *"DOMINANT: Confidence ceiling active at 75 (data quality limitation)"*, `unresolved_flags` = *"LOW_NOVA_CONFIDENCE: NOVA inference unreliable (0.2)"*.

## 3. run_yogurt_002 corpus result vs displayed manual-MVP

| Metric | Displayed (manual-MVP, v1) | run_yogurt_002 (real OFF machine) |
|---|---|---|
| Products | 13 | 46 (24 scored / **22 insufficient = 48%**) |
| Score range | 51–88 | 60–75 (scored only) |
| Grade-A count | **5** (80–88) | **0** |
| Ceiling | 88/A | **75/B** (confidence-ceiling capped) |
| Category routing | yogurt-native | **32/46 "default"** (router can't ID yogurt without ingredients), 14 dairy_protein |
| NOVA | n/a | 2 for all, confidence 0.2 (unreliable) |
| Names | clean Hebrew | English/noisy, typos ("Yoghort", "Yugort", "Danona"); `product_name_he` empty on all 50 |
| Explanations | ingredient-structure insight lines | **none** — engine produced no consumer-facing positiveSignals/limitingFactors/insightLine |

**The run inverts the shelf's editorial logic.** Ingredient-blind, protein mass becomes the dominant signal, so high-protein functional products (Muller Active 25g, Strauss Pro 20) top the machine run at 75/B — the exact products the displayed shelf ranks **below** plain yogurt (the displayed #1 is plain חלב+תרבית at 88/A, which the machine run scores INSUFFICIENT because it cannot see "2 ingredients only").

## 4. Best-effort 1:1 overlap (no clean mapping exists; identity by brand+subtype)

| Displayed | Manual | Machine | Δ | Note |
|---|---:|---|---:|---|
| יוגורט מלא 3% תנובה | 88/A | 71.4/B | −16.6 | A→B |
| יוגורט ביו 1.5% תנובה | 87/A | 69.5/B | −17.5 | A→B |
| יוגורט יווני 5% שטראוס | 85/A | INSUFFICIENT | n/a | dropped out |
| יוגורט 0% שומן | 82/A | INSUFFICIENT | n/a | dropped out |
| יוגורט יווני 0% שטראוס | 80/A | 75/B | −5.0 | A→B |
| אקטיביה/ביו שטראוס 3% | 78/B | 69.4/B | −8.6 | |
| יופלה GO פירות יער | 69/B | INSUFFICIENT | n/a | dropped out |

Every identifiable match drops 5–17.5 pts (3 of 4 scoreable flip A→B) or goes INSUFFICIENT (3 of 7). Same wall TASK-129B hit, now confirmed against **real** products rather than the synthetic run_yogurt_001.

## 5. validate-corpus

- **Live `yogurts_frontend_v1.json`:** `0 errors, 6 warnings` (LIVE/dev mode) — the displayed shelf is contract-clean (warnings are §2.4v2 advisory + §2.8 heuristic-vocab false positives on "כדאי/נקי").
- **A run_yogurt_002-derived dataset was NOT built/shipped**, per the contract ("produce frontend output only if validation passes"). It would fail `--handoff` hard: §5 data-sufficiency (48% insufficient), §2.4 explanation completeness (0 scored products have signals/insightLine), §2.5 unknowns (all nutrition partial). Building it would create a failing orphan in the live data dir.

## 6. Recommendation

- 🔴 **NO-GO** — do not promote run_yogurt_002 to the frontend; do not rescore the live shelf from it.
- **DEC-005 stays open** (manual-MVP provenance exception remains the disclosed state). Yogurts remains LIVE on the manual shelf; this is governance debt, not a launch regression.
- **TASK-135 cannot close.** run_yogurt_002 is preserved as **non-authoritative evidence** (`NON_AUTHORITATIVE.md` in the run dir), not a shippable shelf.
- **Exact unblock for a future retire (run_yogurt_003):** a real-product run with **ingredient panels + Hebrew names** is required. OFF cannot supply these for Israeli yogurts (measured 0% coverage). Path: an authenticated retailer scrape (Shufersal/Yohananof product pages carry ingredient lists + Hebrew names) — the same acquisition gap that blocks deeper bread confidence (`run_bread_retail_004`). Until that data source exists, no machine run can reconcile this category.

*data-agent · TASK-135A · 2026-06-01 · engine 0.4.0 unmodified · no manual score edits*
