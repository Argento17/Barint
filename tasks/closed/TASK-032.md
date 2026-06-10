---
id: TASK-032
title: Bari Category Expansion Wave 2
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-05-30
completed_at: 2026-05-30
depends_on: []
blocks: []
category_id: null
summary: >
  Bari Category Expansion Wave 2. Frontmatter added by TASK-125 (the file existed with a full body
  but no YAML block, so it surfaced as REGISTRY_UNPARSEABLE). Body unchanged.
---

# TASK-032 — Bari Category Expansion Wave 2

**Status:** Complete  
**Owner:** Head of Product  
**Date:** 2026-05-30  
**Inputs:** TASK-014 (Category Expansion Plan), TASK-026 (Scope Decision), TASK-030  
**Decision type:** Acquisition wave scope selection

---

## Decision

**Option C — Combined Tahini + Nut Butter acquisition wave.**

Run a single BSIP0 acquisition pass covering both Tahini and Nut Butters. Process them through a unified BSIP1/BSIP2 run under the `whole_food_fat` archetype. Ship as a single Wave 2 factory cycle.

---

## Rationale

### 1. Factory efficiency is decisive

Both categories share the `whole_food_fat` archetype — same calorie density table (already calibrated to 900 kcal/100g), same router signals ("טחינה" at 0.90, "חמאת" prefix at 0.88), same BSIP pipeline, no new BSIP2 dimensions required. Running them as separate waves means two BSIP0 scrapes, two BSIP1 runs, two BSIP2 batches, two corpus filter governance cycles — for categories that are architecturally identical sub-pools. The combined wave eliminates one full factory pass with no scoring tradeoff.

### 2. Neither category is thick enough to stand alone

| Category | Estimated shelf SKUs | Expected displayable |
|----------|---------------------|----------------------|
| Tahini only | 25–40 | 18–30 |
| Nut butters only | 20–30 | 14–22 |
| Combined | 45–70 | 32–52 |

Tahini alone sits at the lower boundary of a coherent shelf page. Nut butters alone is thin. Combined reaches a shelf depth that supports meaningful comparison — enough spread across NOVA levels, processing tiers, and wellness claim patterns to produce editorial insight.

### 3. The routing infrastructure is already unified

BSIP2 `whole_food_fat` already handles both explicitly:

| Signal | Target archetype | Sub-archetype | Weight |
|--------|-----------------|---------------|--------|
| טחינה | whole_food_fat | nut_butter | 0.90 |
| חמאת (prefix: חמאת בוטנים, חמאת שקדים) | whole_food_fat | nut_butter | 0.88 |

No router changes required. No new dimensions required. Wave 2 is primarily a data acquisition and corpus filter exercise, not an engineering sprint.

### 4. The consumer value story is stronger combined

Tahini and natural peanut butter are the two most frequent whole-food-fat purchases in Israeli households. Their comparison is editorially productive:

- Tahini is structurally simple (sesame seeds, water, salt) — most variants are NOVA 1–2. Its quality axis is ingredient purity and minimal additives.
- Peanut butter is the highest-distortion product in the category — industrial variants add palm oil, glucose syrup, and hydrogenated fat to what could be a 2-ingredient product. The NOVA spread across peanut butter products (NOVA 2 → NOVA 4) is among the widest of any Israeli retail category.

Together they create the clearest whole-food-fat editorial story Bari can tell: *sesame paste that stays simple vs. a category where the gap between natural and industrial is 30 grade points*.

### 5. Scope containment is achievable

The combination does not require expanding to all of `whole_food_fat`. Corpus filter gates:
- **IN:** Raw tahini, flavored/ready-to-eat tahini, natural peanut butter, commercial peanut butter, almond butter, mixed nut butters
- **OUT (strict):** Whole nuts and seed mixes (separate category, lower urgency), coconut butter (small shelf, defer), chocolate hazelnut spreads (Nutella-type → route to `dessert`), avocado-based spreads (separate category), fish/meat-based spreads

Scope risk is manageable because the corpus filter pattern from Hummus (TASK-026) is proven. Wave 2 applies the same locked-filter approach.

### 6. One maintenance burden, not two

A single `whole_food_fat` archetype module, one frontend page (or two linked pages under a shared archetype banner), one editorial framework. Splitting into separate waves creates two thin category pages with separate maintenance cycles, separate calibration queues, and separate distortion review obligations — for categories that will never need independent architectural treatment.

---

## Why not Option A (Tahini only)?

Tahini is ready and natural — but thin as a standalone page. Its editorial story is limited because tahini products are nutritionally homogeneous: most are NOVA 1–2, most score B or higher, few carry deceptive wellness claims. The comparison landscape is narrow. The most interesting editorial tension in the whole-food-fat category is not within tahini — it is *between* natural tahini and industrial peanut butter. Running tahini alone delays the more compelling story by one full factory cycle.

---

## Why not Option B (Nut Butters only)?

Nut butters have the better editorial story (industrial vs. natural distortion is the widest in the archetype). But the corpus is thin without tahini and the category faces a shelf-depth risk at Israeli retailers — premium nut butters have growing but still limited shelf presence. Nut butters also benefit from tahini as an internal reference: a high-scoring tahini product provides a natural anchor for the comparison table that makes the peanut butter distortion legible.

---

## Estimated SKU Impact

| Sub-category | In scope | Count estimate | Notes |
|---|---|---|---|
| Raw tahini (גולמית) | YES | 8–12 | Core: plain sesame, hulled, whole sesame |
| Flavored / ready-to-eat tahini | YES | 8–14 | Lemon, garlic, herbs, lighter styles |
| Light / reduced-fat tahini | YES | 3–6 | "Light" claim — D6 threshold required |
| Organic tahini | YES | 3–5 | Organic certification; simple ingredient profile |
| Natural peanut butter (100% bוטנים) | YES | 6–10 | NOVA 2; 2-ingredient; typically A or B |
| Commercial peanut butter (industrial) | YES | 8–14 | NOVA 3–4; added palm oil, sugar, emulsifiers; typically C–D |
| Almond butter | YES | 4–8 | Growing shelf presence; NOVA 2–3 |
| Mixed nut butters | YES | 3–6 | Cashew, macadamia blends; small segment |
| Chocolate hazelnut spreads | NO | — | Route to `dessert`; excluded from scope |
| Whole nut packs | NO | — | Separate future category |
| Seed mixes | NO | — | Separate future category |
| **TOTAL DISPLAYABLE (estimated)** | | **45–75 scraped / 32–52 displayable** | After BSIP0 gate + BSIP2 filtering |

---

## Factory Impact

| Stage | Effort | Notes |
|---|---|---|
| BSIP0 corpus filter | 1 session | One document covering both sub-categories; apply Hummus filter pattern |
| BSIP0 scrape | 1 scrape pass | Shufersal: ממרחים (spreads shelf) + natural foods aisle; Yohananof: supplementary for net-new barcodes |
| BSIP1 enrichment | Standard | No schema changes; identical to all prior whole_food_fat processing |
| BSIP2 scoring | Standard | `whole_food_fat` archetype; no new modules; NOVA proxy already handles nut butter additives |
| Corpus validation | 1 session | Check routing: chocolate hazelnut spreads must NOT route here; verify "חמאת" prefix catches all variants |
| D6 threshold documentation | ½ session | "Light" tahini threshold; "natural" / "100% X" peanut butter threshold for Marketing Divergence Findings |
| Frontend | Standard | One page or two linked pages; shared archetype; Hummus page design is the reference |
| Editorial | 1 session | 2 articles: (1) tahini — purity is the only story, (2) peanut butter — the gap between what should be simple and what industrial does to it |

**Comparison to running two separate waves:** Combined wave saves approximately one full factory cycle (one BSIP0 scrape + one BSIP1 run + one BSIP2 batch + one corpus filter session + one editorial brief). Estimated saving: 3–5 sessions.

---

## Dependencies

| Dependency | Status | Notes |
|---|---|---|
| Hummus BSIP0 scrape complete (Stage 3) | ⏳ Pending | Wave 2 corpus filter should not be locked until the tahini-hummus blend boundary is validated in real data |
| Tahini-hummus blend rule confirmed | ✅ Locked (TASK-026) | "Chickpeas first ingredient → Hummus; Tahini first ingredient → Wave 2" |
| `whole_food_fat` router "חמאת" validation | ⏳ Recommended | Run 5–10 real nut butter products through BSIP2 before corpus is built; confirm prefix routing catches variants (natural, crunchy, sugar-free) |
| D6 threshold: "light" tahini | ⏳ Pre-launch | Proposed: ≥30% fat reduction from standard tahini (~55g fat/100g → ≤38g fat/100g); requires food science confirmation |
| D6 threshold: "100% bוטנים" / "natural" peanut butter | ⏳ Pre-launch | Proposed: ≤2 ingredients (peanuts + optional salt); any added oil or sweetener disqualifies the claim |
| Chocolate-hazelnut spread exclusion validated | ⏳ Corpus filter | Must be explicit in filter; Nutella-type products will appear in retailer spread aisles; rejection rule needed |

---

## Recommended Next Step

**Lock Wave 2 corpus filter after Hummus Stage 3 completes.** The Hummus scrape will encounter real tahini products at the shelf boundary and provide ground truth for the blend rule. Once the blend rule is confirmed in live data, the Wave 2 corpus filter can be drafted and locked in one session using the Hummus corpus filter as the structural template.

**While waiting on Hummus Stage 3:** Validate "חמאת" prefix routing against 5–8 real nut butter products from prior BSIP1 data or manual test inputs. This is a 1-hour check that de-risks the BSIP2 pass before the corpus is built.

**Do not start Wave 2 BSIP0** until Hummus BSIP0 gate is passed. The categories share a shelf boundary. Starting Wave 2 before Hummus is gated risks scope contamination in both directions.

---

*TASK-032 — Bari Category Expansion Wave 2*  
*Head of Product — 2026-05-30*  
*Next review: After Hummus Stage 3 gate passes*
