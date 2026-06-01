# Future Archetype Candidates

**Status:** Research and planning
**Date:** 2026-05-18

---

## Currently Live

| Archetype | Status | Validation runs |
|---|---|---|
| cereal_system | Active, routing stabilizing | run_cereals_001 (+ run_cereals_002 pending) |
| dairy_liquid | Active, validated | run_004_recalibrated |
| snack_bar | Active, routing unstable | run_004_recalibrated, run_cereals_001 |
| whole_food_fat | Active, floor design under review | run_004_recalibrated, run_cereals_001 |
| beverage | Active, validated | run_004_recalibrated |
| sauce_spread | Defined, no data | None |

---

## Candidate Archetypes

Each candidate is assessed on five dimensions:
- **BSIP0 readiness**: can the scraping pipeline already collect useful data for this category?
- **Scientific complexity**: how well-understood is the structural interpretation of this food type?
- **Regulatory risk**: are there additional Israeli MoH frameworks beyond the three standard red labels?
- **New dimensions required**: what is not yet in the scoring engine?
- **Implementation difficulty**: how much new code does this require?

---

### yogurt_system

**Description:** Fermented dairy products — yogurt, kefir, labane, quark, skyr, plant-based equivalents.

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | HIGH — dairy section well-scraped at Yohananof |
| Scientific complexity | MEDIUM — fermentation is a genuine quality axis; live culture claims are often unverifiable |
| Regulatory risk | LOW — standard three red labels apply; no additional labeling framework for probiotics in Israel |
| New dimensions required | `fermentation_quality` — live cultures, heat treatment, strain specificity |
| Implementation difficulty | MEDIUM — requires Hebrew detection of probiotic claims, heat treatment markers |

**Key differentiators from dairy_liquid:**
Yogurt scoring is dominated by fermentation quality and protein density. Calorie density is less meaningful (yogurt has a narrow 60-120 kcal/100g range). The glycemic quality formula may need a lactose-vs-added-sugar distinction — lactose in yogurt is not the same signal as sucrose.

**Routing anchor:** "יוגורט" (0.92), "קפיר" (0.92), "לבנה" (0.90) — already partially in `category_classifier.py`.

**Recommendation: HIGH PRIORITY.** Dairy is already scraped. Yogurt is the most natural BSIP2 extension from dairy_liquid. The fermentation dimension is the only significant new engineering required.

---

### bread_system

**Description:** Sliced bread, sourdough, pita, lavash, specialty breads. Excludes pastries and sweet baked goods (those route to `dessert`).

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | MEDIUM — bread is well-represented at Israeli retailers; scraping infrastructure exists |
| Scientific complexity | HIGH — fiber type matters (isolated vs whole-grain), matrix integrity is central, sourdough fermentation is a quality signal |
| Regulatory risk | MEDIUM — bread fortification is common (folate, iron) but not separately regulated from standard labeling |
| New dimensions required | `matrix_integrity` (already designed), `fermentation_quality` (partial — sourdough vs commercial yeast) |
| Implementation difficulty | MEDIUM — fortification detection and matrix integrity signals needed |

**Key stress tests bread will expose:**
- Whole-grain bread with high ingredient count vs commercial white bread
- "Multigrain" halo (3 grain types listed but predominantly refined flour)
- Sourdough claims vs actual sourdough (fermentation time vs commercial yeast starter)
- Fiber content: isolated fiber additives vs bran-from-grain

**Routing anchor:** "לחם" (bread), "פיתה" (pita), "לביש" (lavash), "חלה" (challah). Important: sourdough detection requires Hebrew pattern "מחמצת" in ingredient text, not just product name.

**Recommendation: MEDIUM PRIORITY.** Technically straightforward but scientifically rich. Matrix integrity and fortification detection (both proposed for cereals) directly benefit bread. Schedule after cereal_system is stabilized.

---

### legume_system

**Description:** Canned and dried beans, lentils, chickpeas, peas. Hummus routes to `whole_food_fat` or a separate `legume_spread` subtype.

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | MEDIUM — legumes are common at Israeli retailers |
| Scientific complexity | LOW-MEDIUM — legumes are nutritionally coherent; NOVA 1/2; protein+fiber are clear quality anchors |
| Regulatory risk | LOW — standard labeling applies |
| New dimensions required | None required; existing dimensions work well |
| Implementation difficulty | LOW — primarily a calorie density table calibration (legumes: 80-120 kcal cooked) |

**Expected behavior:**
Plain lentils and chickpeas → NOVA 1, high protein, high fiber → A. Canned in salt brine → sodium flag. Flavored or spiced → NOVA 2-3. Legume-based "meat alternatives" (heavily engineered) → NOVA 4, routed to a protein_engineered subtype.

**Routing anchor:** "עדשים" (lentils), "חומוס גרגרים" (chickpeas — different from "חומוס" spread), "פול" (fava), "שעועית" (beans).

**Recommendation: LOW-MEDIUM PRIORITY.** Simple category scientifically. Builds confidence in v3 architecture with a straightforward test case after yogurt_system.

---

### oil_system

**Description:** Cooking oils — olive oil, sunflower, canola, sesame, coconut. Distinct from `whole_food_fat` (nuts, seeds, nut butters).

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | MEDIUM — oils are scraped; extra-virgin vs refined information is often in product name |
| Scientific complexity | HIGH — fat quality for oils requires fatty acid profile, not just sat_fat ratio; polyphenol content matters for EVOO |
| Regulatory risk | LOW — standard labeling; no oil-specific Israeli regulatory framework |
| New dimensions required | `fat_complexity` — oleic acid content, polyphenol markers, cold-press indicators |
| Implementation difficulty | HIGH — fatty acid profiles are not on Israeli nutrition labels; must be inferred from oil type and processing claims |

**The fundamental problem for oil_system:**
Israeli nutrition labels do not include fatty acid breakdown (omega-3, omega-6, oleic acid percentage). This is the most important quality signal for oils and it is not available in scraped data. The `fat_quality` dimension's `sat_fat ratio` metric is meaningful for olive oil vs butter comparisons but cannot distinguish extra-virgin from refined olive oil.

**Routing anchor:** "שמן" (oil) + contextual: "שמן זית" (olive), "שמן חמניות" (sunflower), "שמן קנולה" (canola).

**Recommendation: LATER (post-yogurt, post-bread).** Scientific complexity is high and available data is insufficient for meaningful differentiation. Without fatty acid profiles, oil_system scores will be driven almost entirely by NOVA level, which cannot distinguish cold-pressed from refined. Wait until a data enrichment strategy is developed.

---

### frozen_meal_system

**Description:** Frozen prepared meals — pasta dishes, rice dishes, vegetable combinations, protein-with-side products.

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | LOW — frozen section scraping is not yet a priority; portion sizes complicate per-100g interpretation |
| Scientific complexity | VERY HIGH — multi-ingredient composite products; matrix integrity is completely destroyed; sodium is often very high; fortification is common |
| Regulatory risk | MEDIUM — sodium and sat_fat red labels fire frequently; potential for multiple red labels per product |
| New dimensions required | Composite food handling (no single ingredient characterization is possible) |
| Implementation difficulty | VERY HIGH — composite products require entirely different ingredient analysis logic |

**The fundamental problem for frozen meals:**
A frozen pasta with tomato sauce, cheese, and meat has no meaningful "ingredient integrity" — the product is the result of industrial assembly. NOVA proxy logic assumes ingredient lists tell a coherent story; for composite products, the ingredient list is a portfolio of sub-ingredients. BSIP2's current architecture handles the ingredient list as a flat list; it cannot parse "tomato sauce (tomatoes, salt, olive oil, herbs)" as a nested composition.

**Recommendation: VERY LATER.** Frozen meals require architectural work that does not benefit any current category. The composite-ingredient parsing problem is a v4+ issue. Do not attempt this category in v3.

---

### supplement_system

**Description:** Protein powders, meal replacements, sports nutrition products, specialized medical nutrition.

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | LOW — supplements are sometimes at Yohananof but scraping coverage is thin |
| Scientific complexity | VERY HIGH — protein powders are not "food" in the BSIP2 sense; their quality criteria are entirely different |
| Regulatory risk | HIGH — supplements are regulated differently from foods in Israel (MOPH supplement registry); red labels may not apply |
| New dimensions required | Entire new framework — BSIP2's food-structure philosophy does not apply cleanly |
| Implementation difficulty | EXTREME — would require a separate interpretation framework |

**The fundamental problem for supplements:**
BSIP2 is a structural food interpretation engine. Protein powders are not food — they are isolated macronutrient delivery systems. Their "quality" is defined by: amino acid profile, protein digestibility, heavy metal contamination risk, additive burden for the supplement context. None of these signals are available from Israeli retail scrapes. The NOVA proxy would classify every protein powder as NOVA 4 (emulsifier + sweetener + flavor_enhancer), which is technically correct but uninformative.

**Recommendation: DO NOT ADD TO BSIP2.** Supplements require a separate interpretation system (potentially BSIP_SUPPLEMENT) with its own ontology. Forcing supplements into the BSIP2 food architecture produces scores that are technically computed but meaningless.

---

### sauce_spread_system (expansion)

**Description:** The current `sauce_spread` category is defined but untested. Expands to cover: tomato sauce, tahini, hummus, mayonnaise, mustard, hot sauce, salad dressings.

| Dimension | Assessment |
|---|---|
| BSIP0 readiness | MEDIUM — condiments are scraped at Yohananof |
| Scientific complexity | MEDIUM — highly variable; tahini (whole_food_fat-like) vs ketchup (high sugar) vs mayonnaise (high fat) |
| Regulatory risk | MEDIUM — sugar and sodium red labels common for condiments |
| New dimensions required | None; existing framework covers the key signals |
| Implementation difficulty | LOW-MEDIUM — primarily routing calibration; calorie density table already defined |

**Key routing tension:**
Tahini and hummus are currently routed to `whole_food_fat` or `sauce_spread` depending on product name signals. These should be unified under a `sauce_spread` archetype (or a `spread` subtype of `whole_food_fat`). Tahini at 600 kcal is high-density but appropriate for a sesame paste product; it should not be penalized in calorie density like a meal.

**Recommendation: MEDIUM PRIORITY.** Simple category once routing is resolved. A natural second or third category after yogurt_system — gives the v3 router a stress test on a nutritionally diverse category.

---

### Summary Table

| Archetype | Priority | When | Blocking factor |
|---|---|---|---|
| yogurt_system | HIGH | After run_cereals_002 | None — ready now |
| bread_system | MEDIUM | After yogurt_system | Fortification detection (Evolution #4) needed first |
| sauce_spread_system | MEDIUM | After yogurt_system | Routing tension with whole_food_fat to resolve |
| legume_system | LOW-MEDIUM | After bread | None — simple category, low urgency |
| oil_system | LOW | After architecture Phase 4 | Fatty acid data not available; wait for data strategy |
| frozen_meal_system | VERY LOW | v4+ | Composite ingredient parsing not yet designed |
| supplement_system | DO NOT ADD | — | Fundamentally different framework required |

---

## Recommendation: Next Category After Architecture Stabilization

**yogurt_system.**

Rationale:
1. The BSIP0 scraping infrastructure already covers Yohananof's dairy section.
2. BSIP1 processing is identical to milk products — no schema changes.
3. Scientifically, yogurt introduces fermentation quality, which is the next genuinely new scoring dimension after matrix integrity.
4. Routing is simple: "יוגורט" is an unambiguous anchor.
5. Yogurt tests the archetype system's ability to extend dairy_liquid without forking it — the key architectural test for v3.

The yogurt corpus should aim for: plain yogurts (NOVA 1-2), flavored yogurts (NOVA 3), protein-fortified yogurts (NOVA 3-4), kefir, plant-based yogurts, and at least 2-3 heavily sweetened dessert-adjacent yogurt products. Same diversity principle as cereals: do not create a "healthy yogurts only" corpus.
