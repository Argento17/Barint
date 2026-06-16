# Yogurts — OFF Remediation Decision Brief

**Date:** 2026-06-11  
**Prepared by:** Nutrition Agent (Product Agent co-sign)  
**Routes to:** Owner (Tripwire #2 — irreversible consumer-facing category state)  
**Scope:** Decision only. No data changes, no engine, no copy.  
**Related:** TASK-238 (OFF hard-rule), contamination audit `reports/open_food_facts_contamination_audit_v1.md`

---

## 1. Actual current state (corrects the task brief)

The contamination audit (2026-06-10) found `yogurts_frontend_v3.json` contained 6 OFF images and an OFF-sourced corpus. That file has since been regenerated as part of ongoing TASK-238 remediation. **The live file as of this brief has 0 OFF dependencies.**

| Fact | Value |
|---|---|
| Live file | `bari-web/src/data/comparisons/yogurts_frontend_v3.json` |
| Generated | 2026-06-07 |
| OFF images | **0** (confirmed by grep) |
| OFF in source chain | **0** (v3 provenance: "TASK-238: OFF removed") |
| Products | **11** (down from 86 in run_004) |
| Source | All Shufersal direct scrape (Cloudinary images, html_parse) |
| Grade distribution | 6A / 3B / 1C / 1D |
| Ingredients | **0 / 11** — null for every product |

What happened: the 7 Yohananof products that had OFF-only identity (il_prices barcode + OFF panel) were de-listed when OFF was removed, leaving the 11 Shufersal products whose nutrition came from a real HTML scrape. The page is OFF-clean but thin and ingredient-blind.

---

## 2. What the consumer sees today

The page is **live**, showing 11 products. Every product has `"ingredients": null`. All confidence labels read partial or "data under review" because without ingredient text the engine cannot fire NOVA classification, fermentation/culture markers, additive/sweetener/stabilizer signals, or subtype routing.

The 11 products that survived are high-protein functional items (Danone Pro, Muller Active, Yoplait GO) plus two plain Tnuva Bio products. **The mainstream יוגורט plain shelf, sour cream-adjacent, Greek, flavored, and drinkable subtypes are absent.** A consumer looking for a plain 3% bio yogurt sees a shelf dominated by protein-enriched products.

---

## 3. The actual decision

The page is already OFF-clean, so the choice is not "contaminated vs. pulled." It is:

**Option A — Full re-acquisition from Shufersal (run_yogurt_005)**  
**Option B — Keep the existing 11-product thin shelf as-is**

(Pulling the category is also possible but is the worst outcome: the page is already clean and Shufersal access is proven. Pulling adds consumer disruption with no data-integrity benefit.)

---

## 4. Option comparison

| | **Option B: Keep thin shelf** | **Option A: Full re-acquisition** |
|---|---|---|
| Consumer sees | 11 products, no ingredient data | ~30–50 curated products, ~75% ingredient coverage |
| Shelf representation | High-protein bias; plain/bio shelf absent | Full mainstream shelf |
| Score accuracy | Nutrition-only; NOVA estimated; no fermentation/additive signals | Full engine signal set |
| OFF risk | 0 | 0 (Shufersal html_parse; no OFF in pipeline) |
| Images | Real Cloudinary/Shufersal | Real Cloudinary/Shufersal |
| Engineering effort | None | **Low** — scraper already fully built and proven |
| Hard dependency | None | **Israeli-IP VPN** (operational, not engineering) |
| Timeline | Done | 1–2 days to run + QA once VPN available |
| Score stability | Stable (no change) | Scores will change — that is correct (real ingredient signals) |

---

## 5. Effort calibration (TASK-237 salty pattern)

TASK-237 re-sourced 38 salty-snacks products from Yohananof in ~1–2 days. The yogurt re-acquisition is **simpler**:

- Scraper: `03_operations/bsip0/scrape/shufersal_yogurt/01_scrape_yogurt.py` — fully written, 20 query terms, category-browse phase, proven against live Shufersal HTML
- BSIP1 builder: `shufersal_yogurt/02_build_bsip1_yogurt_004.py` — proven, 86-product run with 100% ingredient + 95% nutrition coverage (run_004 QA gate: PASS)
- BSIP2: unchanged engine, standard invocation
- Precedent: run_004 scraped 93 products, BSIP1 included 86, scored 86, 0 pipeline errors

Effort is dominated by the VPN operational step, not engineering. Once VPN is available: scrape → BSIP1 → BSIP2 → frontend in ~4 hours of pipeline execution + ~1 day of QA/content.

**Single hard dependency:** Israeli-IP VPN at scrape time (Shufersal blocks non-IL IPs; confirmed in `source_assessment_135_run_yogurt_003.md`). Run_003 and run_004 both executed cleanly once VPN was available.

---

## 6. Scores will change — that is expected and correct

run_yogurt_002 (OFF corpus, ingredient-blind) showed the damage of absent ingredients: ~50% of products scored 50 ("insufficient_data"), English/French names like "Yaourt", "Yoghort", "Greek yogurt", no NOVA routing. The real run_004 on Shufersal data scored 86 products with ingredient-driven NOVA, fermentation markers, and additive penalties. Score moves on re-acquisition are correct corrections, not instability.

---

## 7. Recommendation

**Option A: Run the full re-acquisition.** The scraper exists, the pipeline is proven, and the existing 11-product shelf is a poor representation of the category — ingredient-blind, high-protein-biased, and missing the mainstream plain/bio shelf that most consumers visit this page for. The effort is low relative to the consumer-experience gain. The OFF risk is zero by construction (Shufersal html_parse, no OFF in the pipeline).

**Option B is acceptable only as a holding position** if VPN is unavailable in the near term. In that case the page should carry an honest category caveat (הערת קטגוריה) stating "this shelf covers functional/high-protein products; the full plain yogurt segment is not yet represented."

---

## 8. What owner approval authorizes

Approving Option A authorizes:
1. Running `01_scrape_yogurt.py` against Shufersal (requires Israeli-IP VPN at execution time)
2. Running the existing BSIP1/BSIP2 pipeline on the fresh scrape (unchanged engine)
3. Replacing `yogurts_frontend_v3.json` with the re-acquired output
4. Score/grade changes relative to the current v3 are expected and authorized

No scoring philosophy change. No engine change. No new categories.

---

*Nutrition Agent · 2026-06-11 · decision brief only, no data changed · routes to owner (tripwire #2)*
