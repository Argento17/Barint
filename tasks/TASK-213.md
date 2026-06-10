---
id: TASK-213
title: "Category Launch — חטיפים מלוחים (Salty Snacks): full BSIP0→frontend pipeline"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-07
closed_at: 2026-06-07
depends_on: []
blocks: []
roadmap_impact: true
cc_reviewed: true
work_type: category-launch
category_id: salty-snacks
close_reason: "Pipeline complete. 54 products scored (6 below 60-product target — all 6 sub-pools fully populated). Frontend JSON deployed. KI-001 NOVA engine gap confirmed on Bamba and ~26 other puffed/extruded products (nova_proxy=2, engine cannot detect extrusion from ingredient text; Bamba scores 70/B, estimated correct score ~C). Scores are accurate per current engine; extrusion fix routed to TASK-189. Category is pipeline-complete; launch readiness pending KI-001 resolution decision."
---

# TASK-213 — Salty Snacks Category Pipeline

## Context

Salty snacks is the largest uncovered high-frequency category in Israeli retail — chips,
popcorn, pita chips, corn puffs, pretzels, rice cakes, crackers, and Bamba-style puffed
snacks. 100+ SKUs across the three main retailers.

This is distinct from snack bars (חטיפי אנרגיה/חלבון, already live at `/hashvaot/snack-bars`).
The salty snacks shelf is the place where "healthy" marketing claims are most divorced from
nutritional reality — "baked", "whole wheat", "no MSG", "natural" labels are widespread on
products that score very poorly under BSIP.

The strategic value of this category: NOVA penalties dominate, ingredient-list signals are
decisive, and the results will surprise most buyers (branded "health" popcorn often scores
below plain Bamba). This is Bari's highest-virality potential category.

## Workspace

`C:\Bari\02_products\salty_snacks\`

## Pipeline

### Stage 1 — BSIP0: Scrape

Scrape all three retailers for the salty snacks shelf:
- **Shufersal**: חטיפים מלוחים shelf (`/קטגוריות/חטיפים/חטיפים-מלוחים` or equivalent)
- **Yohananof**: same shelf category
- **Carrefour**: same shelf category

Collect per product: barcode, name, brand, weight/volume, full ingredient list (Hebrew),
nutrition panel (per 100g), category tag, image URL, retailer price.

Output: `02_products/salty_snacks/bsip0_outputs/` — one BSIP0 JSON per retailer.

Target corpus: **80–120 products** before deduplication.

Shelf scope (include):
- Chips / crisps (all varieties — potato, corn, wheat, root vegetables)
- Popcorn (all varieties — microwave, pre-popped, flavored)
- Pita chips / baked chips / oven-baked snacks
- Corn puffs / cheese puffs / Bamba-style puffed snacks
- Pretzels (bagged)
- Rice cakes / rice crackers / puffed grain cakes
- Multi-grain crackers / snack crackers

Shelf scope (exclude — handled by other categories):
- Energy/protein bars → snack-bars category
- Nuts and seeds → separate shelf, not in scope yet
- Chocolate-coated snacks → confectionery, not in scope yet
- Party crackers (Ritz-style) intended for cheese serving → edge, use judgment

### Stage 2 — BSIP1: Enrichment

Run standard BSIP1 enrichment on all BSIP0 outputs:
- Cross-retailer deduplication by barcode (keep richest record)
- Hebrew ingredient parsing
- NOVA group assignment — this is the dominant signal for salty snacks; most will be NOVA 4
- Additive detection (colorants, flavor enhancers, preservatives)
- Allergen tagging

Output: `02_products/salty_snacks/bsip1_outputs/` — canonical BSIP1 records.

Target post-dedup corpus: **60–90 products**.

### Stage 3 — BSIP2: Scoring

Run BSIP2 batch scorer on the canonical corpus.

Key scoring notes:
- NOVA group 4 → full degradation penalty applies. Most salty snacks will be NOVA 4.
  The few genuinely minimal-ingredient products (plain rice cakes, plain popcorn) may be
  NOVA 3 — verify ingredient list carefully before NOVA downgrade.
- Per-100g normalization required. Many products use misleading "per portion" serving
  sizes (20–30g portions on a 100g bag). Score must be per-100g basis only.
- "Whole wheat" claims: verify the actual grain fraction in the ingredient list — if wheat
  flour appears before whole wheat flour, it is NOT primarily whole wheat.
- Light/baked/reduced-fat variants: score on actual nutritional architecture, not the claim.
  These often have similar or higher sodium than the "regular" version.

Output: `02_products/salty_snacks/bsip2_outputs/` — one `bsip2_trace.json` per product.

### Stage 4 — Frontend JSON

Run `build_frontend_dataset.py` or equivalent to produce `salty_snacks_frontend_v1.json`.

Required fields per product: id, name, brand, score, grade, retailer(s), imageUrl,
insightLine, limitingFactors, subPool, confidence, ingredientCount, novaGroup.

Sub-pool taxonomy (for comparison page filtering):
- `chips` — potato/corn/wheat chips
- `popcorn` — all popcorn types
- `puffed` — corn puffs, Bamba-style
- `baked` — pita chips, baked crackers, oven snacks
- `rice_cakes` — rice/grain cakes and crackers
- `pretzels` — pretzel snacks

Copy to: `C:\bari\bari-web\src\data\comparisons\salty_snacks_frontend_v1.json`

## BSIP framework notes

- Do not create category-specific scoring rules. Work within the existing BSIP2 engine.
- If the existing engine produces unexpected results (e.g., plain rice cakes scoring
  identically to a complex chip), note it in the run summary — do not adjust scores ad hoc.
  Scoring anomalies belong in TASK-189 scope (engine improvements), not here.
- Insight lines must be drawn from the real trace data. Do not infer or fabricate.

## Acceptance criteria

- [ ] Workspace `02_products/salty_snacks/` created with all pipeline stage directories
- [ ] BSIP0 outputs from all 3 retailers (Shufersal, Yohananof, Carrefour)
- [ ] Post-dedup canonical corpus: ≥ 60 products
- [ ] BSIP2 traces complete for all corpus products
- [ ] `salty_snacks_frontend_v1.json` generated and copied to bari-web
- [ ] All 6 sub-pools populated (≥ 3 products each, or noted as empty with reason)
- [ ] Run summary with: corpus size, NOVA distribution, score distribution, top/bottom 5
- [ ] No insight lines that aren't grounded in real trace data

## Return block

Report:
1. Final corpus size (post-dedup) and NOVA distribution breakdown
2. Score range and grade distribution (how many A/B/C/D)
3. Sub-pool population counts
4. Any products where NOVA assignment was non-obvious — explain the call
5. Surprising findings (health claims vs actual scores)
6. Frontend JSON path and product count
