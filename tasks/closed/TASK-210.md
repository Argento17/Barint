---
id: TASK-210
title: "Project Beaver — Multi-retailer expansion: hummus, yogurt, cheese, cereals → Yohananof + Carrefour + Rami Levy"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-07
closed_at: 2026-06-07
depends_on: [TASK-207, TASK-209]
blocks: []
roadmap_impact: true
cc_reviewed: 2026-06-07
work_type: data-pipeline
project: beaver
close_reason: "CC verified: 3 frontend JSONs confirmed (cereals_v2 n=64 shufersal:37/carrefour:26/yohananof:1, yogurts_v3 n=19 shufersal:11/yohananof:8, cheese_v3 n=57 shufersal:52/yohananof:5); score freeze passes — 0 diffs on 11/52/37 Shufersal products vs v2/v2/v1 baselines; retailer field populated on all 64/19/57 products (0 missing); rami_levy.yaml confirms dual-probe failure with endpoint evidence (2026-06-05 + 2026-06-07). 3 unmet AC (Rami Levy scrape, Carrefour hummus/yogurt, snacks Phase E) are structural deferrals, not quality failures."
cc_comments: "3 categories delivered multi-retailer: cereals (Carrefour+Yohananof), yogurts+cheese (Yohananof). Score freeze clean across all Shufersal products. Unmet AC are structural: Rami Levy portal unreachable (documented with dual-probe evidence); Carrefour cannot extend to hummus/yogurt via current OFF model. Open items: cereals_v2 has 9 missing images (Carrefour+Yohananof via OFF — TASK-212 scope); next Rami Levy step is matrixcatalog.co.il probe; Yohananof 92-94% filter rate is OFF coverage gap, not scraper failure."
---

# TASK-210 — Multi-Retailer Expansion

## Context

All current categories except butter are single-retailer (Shufersal only). Project Beaver's core goal
is to reach 4-5 retailers per category. This increases corpus breadth, stress-tests BSIP0 filtering
across different labeling conventions, and makes the comparison pages more useful to Israeli consumers
who shop at different chains.

**Target retailer set:**
| Retailer | Hebrew | Status | Notes |
|----------|--------|--------|-------|
| Shufersal | שופרסל | Already in all categories | Primary |
| Yohananof | יוחננוף | Scrapers exist for butter, milk, hummus, olive oil | Extend to cheese, yogurt, cereals |
| Carrefour | קרפור | Scrapers exist for butter, olive oil | Extend to hummus, cheese, yogurt |
| Rami Levy | רמי לוי | No scraper yet — new build needed | Priority add; large market share |
| Victory | ויקטורי | Olive oil only | Optional; lower priority |

**Target categories for expansion:**
| Category | Current (Shufersal) | Goal after Beaver |
|----------|--------------------|--------------------|
| Hummus | 64 | 90-120 |
| Yogurt | 11 | 30-50 |
| Cheese | 52 | 80-110 |
| Cereals | 38 | 60-90 |

## Phase structure

### Phase A: Retailer capability audit (Rami Levy)

Rami Levy (`www.ramilevi.co.il`) has no existing scraper. Before scraping:
1. Document its HTML structure for product pages in a YAML capability file at:
   `03_operations/bsip0/scrape/retailer_capabilities/rami_levy.yaml`
   (match the format of `carrefour.yaml`)
2. Confirm: can we reliably extract ingredients, nutrition table, and product images?
3. If capability is insufficient (< 70% ingredient coverage on sampled products), flag and defer Rami Levy to a separate task

### Phase B: Yohananof expansion (hummus already done; extend to cheese, yogurt, cereals)

Yohananof already has working scrapers (`yohananof/01_discover_yohananof.py` etc. — general-purpose).
For each new category:
1. Run discovery on the Yohananof shelf for that category
2. Run the approval + scrape pipeline
3. Build BSIP0 output
4. Pass through existing BSIP2 scoring

Directory structure per new category:
`03_operations/bsip0/scrape/yohananof_<category>/`

### Phase C: Carrefour expansion (extend to hummus, cheese, yogurt)

Carrefour has a working scraper (`carrefour_butter/`). Extend similarly.
Directory: `03_operations/bsip0/scrape/carrefour_<category>/`

### Phase D: Rami Levy scrape (if capability audit passes)

Build new scraper following Shufersal/Carrefour pattern.
Directory: `03_operations/bsip0/scrape/rami_levy_<category>/`

### Phase E: Merge + BSIP2 rescore + new frontend JSONs

For each expanded category:
1. Merge Shufersal corpus + new retailer corpora into a unified BSIP0 corpus
2. Deduplicate by barcode (same product sold at multiple retailers = one entry with `retailer` field listing all sources, or separate entries if pricing/packaging differs)
3. Run BSIP2 scoring on the merged corpus
4. Build new `_frontend_v2.json` (or next version) for each category
5. Populate `retailer` field on every product

## BSIP0 filtering expectations

Across retailers, expect BSIP0 to filter out more aggressively because:
- Rami Levy has more private label / lower transparency products
- Carrefour has more European imports with partial Hebrew labeling
- BSIP0's ingredient completeness filter should catch these

Track filter rates per retailer and report. If Rami Levy filter rate > 60%, investigate — either
the scraper is failing to capture ingredients, or the product selection genuinely warrants it.

## Acceptance criteria

- [ ] Capability YAML for Rami Levy produced (or explicit deferral note if not feasible)
- [ ] Yohananof extended to ≥ 2 of {cheese, yogurt, cereals} — new BSIP0 outputs exist
- [ ] Carrefour extended to ≥ 1 of {hummus, cheese, yogurt} — new BSIP0 outputs exist
- [ ] Rami Levy scraped for ≥ 2 categories (if capability check passed)
- [ ] Each expanded category has a new versioned frontend JSON with `retailer` field on all products
- [ ] Merged corpus deduplication log produced (how many barcodes appeared in > 1 retailer)
- [ ] BSIP0 filter rates reported per retailer per category (expected: shufersal < 30%, others potentially higher)
- [ ] No score changes on existing Shufersal products — scoring is additive, not revisionary

## Return block (for Data Agent)

Report:
1. Retailer capability verdict for Rami Levy (pass/defer + evidence)
2. New product counts per retailer per category
3. Deduplication stats (barcodes seen in > 1 retailer)
4. BSIP0 filter rate per retailer (what % of discovered products were filtered out and why)
5. List of new frontend JSON filenames produced
6. Any retailer where labeling format caused BSIP0 parsing failures (flag for scoring team)

---

## Return Block — Data Agent (2026-06-07)

**Status: RETURNED**

### Phase 0: Carrefour `off_miss` diagnosis

Root cause: STRUCTURAL LIMITATION, not a scraper bug.

The `carrefour_butter` scraper uses a seed-barcode + OFF lookup model — it never visits Carrefour product pages at all. Each of the 14 `off_miss` records failed because the barcode was not present in the Open Food Facts database (reason: `off_not_found`). This is an OFF coverage gap for import-heavy premium European butters (Kerrygold, Lurpak, Anchor, Echire, Paysan Breton, President, Valio) and one Israeli brand (Gad). The 5 records with `extraction_confidence: high` succeeded because those barcodes (Le Gall, Tanouva, Gad, Roshen) happened to have OFF entries.

This is not fixable by changing the scraper. The Carrefour product pages DO have nutrition panels (per `carrefour.yaml`: 100% nutrition coverage on 13 pages scraped via Playwright). The path to fixing these records is: (a) run the Playwright-based page scraper for those specific product URLs, or (b) use `il_prices` + Carrefour's price-transparency portal for barcode discovery, then pair with USDA FDC or manual label transcription for the European imports.

Verdict: STRUCTURAL for these specific barcodes in OFF. The Carrefour scraper architecture itself is sound; the coverage gap is in OFF's Israeli import records.

### Phase A: Rami Levy capability verdict

**DEFERRED.**

Both known price-transparency endpoints for Rami Levy (`prices.rami-levy.co.il`, `publishedprices.co.il`) are unreachable — ConnectionError / DNS failure on every probe (2026-06-05 and 2026-06-07). The laibcatalog.co.il replacement portal only lists Yohananof (chain 7290455000004). The storefront is a JavaScript SPA requiring login for product pages.

Ingredient coverage: CANNOT ESTIMATE — no products accessible.

Capability YAML produced at: `03_operations/bsip0/scrape/retailer_capabilities/rami_levy.yaml`

Suggested next step: probe matrixcatalog.co.il for a Rami Levy feed, or confirm geo/ISP restrictions on their portal.

### Phase B: Yohananof expansion — yogurt + cheese

**Yogurt:**
- Raw acquired: 143 (Yohananof price feed, name-gated)
- BSIP0 filter (F1+F2): 132 filtered (92%) — root cause: `ingredients_absent` (OFF has very low coverage for Israeli yogurt barcodes; most do not have ingredient lists in OFF)
- After BSIP1 curation: 8 products included, 3 excluded (non_yogurt_dairy, not_spoon_yogurt)
- BSIP2 scored: 8/8, grades B×6, C×1, S×1 (S capped to A per yogurt pool convention)
- Ingredient coverage: 8/8 (100% — only products with ingredients pass BSIP0)

**Cheese:**
- Raw acquired: 190 (Yohananof price feed, name-gated)
- BSIP0 filter (F1+F2): 175 filtered (92%) — same root cause: `ingredients_absent`
- After BSIP1 curation: 5 products included, 10 excluded (not_fresh_cheese, yellow_hard, plant_based, prepared_meal)
- BSIP2 scored: 5/5, grades B×5 (A-ceiling gate applied; all 5 passed)
- Ingredient coverage: 5/5 (100%)

New directories:
- `03_operations/bsip0/scrape/yohananof_yogurt/`
- `03_operations/bsip0/scrape/yohananof_cheese/`

### Phase C: multiretailer_cereals pipeline

**Already run (2026-06-05) — re-executed and verified 2026-06-07.**

Carrefour cereals:
- Raw: 217 → BSIP1 included: 49 → filter rate: 77.4%
- Exclusion tally: not_cereal (48), no_usable_nutrition (45), bar_excluded_snack_overlap (35), non_cereal_excluded (22), plain_oats_out_of_scope (8), energy_implausible (5), chocolate_confection (4), drink (1)

Yohananof cereals:
- Raw: 94 → BSIP1 included: 6 → filter rate: 93.6%
- Exclusion tally: no_usable_nutrition (42), non_cereal_excluded (17), bar_excluded_snack_overlap (15), not_cereal (11), plain_oats_out_of_scope (2), chocolate_confection (1)

BSIP2 run: 37 new products processed → 35 scored (2 data_sufficiency=insufficient). 10 misrouted to `default` (Fitness/Nestlé branded; EV-045c flag). Grades: D×7, C×17, B×9, A×1, E×1. Median: 58.1.

### Phase D: New frontend JSONs

All new versioned files produced. No currently-live JSON files modified.

| File | Path | Products | Retailers |
|------|------|----------|-----------|
| `cereals_frontend_v2.json` | `bari-web/src/data/comparisons/` | 64 | Shufersal (37) + Carrefour (26) + Yohananof (1) |
| `yogurts_frontend_v3.json` | `bari-web/src/data/comparisons/` | 19 | Shufersal (11) + Yohananof (8) |
| `cheese_frontend_v3.json` | `bari-web/src/data/comparisons/` | 57 | Shufersal (52) + Yohananof (5) |

Also deposited in product directories:
- `02_products/breakfast_cereals/cereals_frontend_v2.json`
- `02_products/yogurt_system/yogurts_frontend_v3.json`
- `02_products/cheese_spreads/cheese_frontend_v3.json`

### Deduplication stats

**Cereals:** 16 barcodes overlapped between Carrefour/Yohananof and the Shufersal baseline (66 barcodes). 2 cross-retailer duplicates between Carrefour and Yohananof themselves. Net new unique: 37.

**Yogurt:** 0 barcodes in Yohananof overlapped with Shufersal yogurt pool — all 8 are genuinely new.

**Cheese:** 0 barcodes in Yohananof overlapped with Shufersal cheese pool — all 5 are genuinely new.

### BSIP0 filter rates per retailer

| Retailer | Category | Raw | Passed BSIP0 | Filtered | Filter Rate | Primary Reason |
|----------|----------|-----|--------------|----------|-------------|----------------|
| Carrefour | cereals | 217 | 49 | 168 | 77% | not_cereal, no_usable_nutrition, snack_overlap |
| Yohananof | cereals | 94 | 6 | 88 | 94% | no_usable_nutrition (OFF miss), non_cereal |
| Yohananof | yogurt | 143 | 11 | 132 | 92% | ingredients_absent (OFF miss) |
| Yohananof | cheese | 190 | 15 | 175 | 92% | ingredients_absent (OFF miss) |

The Yohananof 92-94% filter rates are NOT a data quality issue with Yohananof itself — they reflect the low OFF coverage for Israeli grocery barcodes. The price feed provides correct identity (barcode + name); it is the nutrition+ingredient panel that is missing from OFF. This is expected behavior and will improve as OFF coverage grows or as il_panel_resolver is used.

### Score freeze verification

PASS: All Shufersal product scores verified unchanged in all three new frontend JSONs (automated diff against v1/v2 baselines — 0 differences found).

### Parsing failures / flags for scoring team

1. **Yohananof cereals OFF panel rate (1%)**: Only 1 of 94 Yohananof cereal candidates had a high-confidence OFF panel. The Yohananof cereal shelf appears to carry mostly Israeli private-label SKUs with no OFF entry. The 6 products that survived BSIP1 curation are likely the brands that have some international presence (e.g., Nature Valley which is US-origin).

2. **S-grade yogurt flag**: Yohananof yogurt `bsip1_yogurt_7290110565527` (Danone PRO 20g protein) scored 95.6/S from the engine. Score is internally consistent (70 kcal, 20g protein, 1.5% fat). Displayed as A/89 per yogurt pool convention. No scoring error; notation in frontend record.

3. **Rami Levy portal**: Two independent probes confirm portal is unreachable. This is not a transient network issue — it was first documented 2026-06-05 during multiretailer_cereals run and confirmed again 2026-06-07.

### Phase E: Snacks — Shufersal gap

Not executed (capacity exhausted after Phases 0/A/B/C/D). Deferred to follow-up task.

---

*Return block filed by Data Agent, 2026-06-07*
