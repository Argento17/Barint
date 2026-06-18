# Nutrition Reference KB v1

**Classification:** Internal — Nutrition Knowledge (reference layer, NOT scoring)
**Version:** 1.0
**Established:** 2026-06-15
**Owner:** Nutrition Agent
**Status:** Forward-looking reference layer for planned whole-food / combination / expanded
consumer-product categories (owner directive, 2026-06-15).

---

## Charter

This file is a **Bari-owned, provenance-stamped general-nutrition reference**. It is a
**different artifact** from the scoring Evidence Registry
(`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`).

**What it is for:** accumulating foundational nutrition knowledge ahead of future categories
where it becomes relevant — **fruits, vegetables, whole foods, and food combinations** — and as
a single, citable source of truth for future consumer copy. Owner established this layer
2026-06-15 on the reasoning that Bari will grow beyond packaged foods, and a curated/auditable
KB is worth more than relying on model-internal knowledge.

**Inclusion bar (intentionally relaxed vs. the scoring registry).** For *this* layer we keep an
entry even when a strong nutrition model already knows the fact, **provided** it is foundational
reference for a planned future category. Provenance + a single source of truth are the point.
This deliberately reverses the "drop if the model already knows it" bar — which still governs the
scoring Evidence Registry. We do **not** keep trivia with no plausible future-category use.

**Firewall (unchanged).** Nothing in this file moves a published score. Reference knowledge that
later wants to inform scoring must be **promoted** to an `EV-###` entry in the scoring Evidence
Registry with a primary `source_doi` and **D7 co-sign (Nutrition Agent + Product Agent)**. A
popular-science book flags a finding; it never proves one. (See `off_ban_hard_rule`,
`citations_discipline`.)

---

## Entry schema

| Field | Meaning |
|---|---|
| `id` | `KB-###` |
| `topic` | what it covers |
| `summary` | the reference content |
| `source` | book / author / page (provenance) |
| `source_tier` | `popular_science_secondary` etc. — a popularizer is a pointer, not primary evidence |
| `applies_to_future_categories` | which planned categories this seeds |
| `scoring_relevance` | `none` (reference only) · `future-candidate` (could seed an EV-### later) |
| `consumer_copy_usable` | whether Content Agent may draw on it (still subject to editorial standards) |
| `notes` | caveats, promotion notes |

---

## KB-001 — Dietary minerals: roles + whole-food sources

| Field | Value |
|---|---|
| **id** | KB-001 |
| **topic** | Essential dietary minerals — macro vs. trace, physiological role, and food sources |
| **source** | *The Science of Nutrition: Debunk the Diet Myths and Learn How to Eat Well for Health and Happiness*, Rhiannon Lambert (DK, 2021) — "What Are Minerals?" spread |
| **source_tier** | `popular_science_secondary` — consensus-level textbook content; reliable as reference, not citable as primary evidence |
| **applies_to_future_categories** | fruits, vegetables, whole_foods, food_combinations |
| **scoring_relevance** | none — Bari scores nutritional *architecture* (processing, additives, sugar, sodium, fat quality, fiber), not micronutrient completeness. Minerals are handled *implicitly* via whole-food / matrix-integrity logic. No signal here today. |
| **consumer_copy_usable** | yes — food-source lists are the reusable part for future whole-food category copy (still subject to editorial standards: insight-first, no encyclopedia register) |

**Definition.** Unlike vitamins (organic compounds made by plants/animals), minerals are
**inorganic chemical elements** from soil, rock, or water — absorbed by plants as they grow and
passed up to the animals that eat them. **Macrominerals** (needed in larger amounts): calcium,
chloride, magnesium, phosphorus, potassium, sodium. **Trace minerals** (needed in small amounts):
iodine, iron, selenium, zinc, manganese.

| Mineral | Role (reference) | Whole-food sources |
|---|---|---|
| **Calcium** | Bone & teeth; nervous system, muscle, heart function | milk, yogurt, spinach |
| **Iodine** | Thyroid function & thyroid-hormone production (growth, brain development, bone maintenance, metabolic rate). *Deficiency affects ~⅓ of world population.* | fish, dairy, eggs, seaweed |
| **Iron** | Oxygen-carrying capacity of blood; immune & brain function. *Most common nutritional deficiency worldwide; the only one prevalent in developed countries — >30% have anaemia.* | shellfish, broccoli, red meat, tofu |
| **Magnesium** | Role in 600+ cellular processes — energy production, nervous system, muscle contraction | avocados, nuts, leafy greens |
| **Manganese** | Makes/activates enzymes for chemical reactions (e.g. breaking down food) | bread, nuts, breakfast cereals, green veg |
| **Potassium** | Blood-pressure control, fluid balance, muscle & nerve function | bananas, spinach, potatoes, apricots |
| **Phosphorus** | Strong bones; releasing energy from food | red meat, dairy, fish, poultry, oats, bread |
| **Selenium** | Immune function; protects cells/tissues from damage; reproductive health | Brazil nuts, eggs, meat, fish |
| **Zinc** | Immune system, hormone production, fertility; reduces skin inflammation, wound healing, UV protection | shellfish, red meat, eggs, chickpeas |

**Notes.** Two epidemiological claims worth a primary citation **if** ever promoted toward
scoring/copy authority: iodine deficiency ≈ ⅓ global population; iron deficiency = most common
nutritional deficiency. Sodium/potassium → blood pressure overlaps Bari's existing sodium logic,
but adds nothing to it today. Promotion path to any score move = `EV-###` + D7.

---

## KB-002 — Dried fruit: minerals AND sugars concentrate together

| Field | Value |
|---|---|
| **id** | KB-002 |
| **topic** | Dried fruit as a concentrated source of *both* minerals and fruit sugars (the concentration double-edge) |
| **source** | *The Science of Nutrition*, Rhiannon Lambert (DK, 2021) — dried-fruit spread (goji berries, dates, mango, raisins, figs) |
| **source_tier** | `popular_science_secondary` |
| **applies_to_future_categories** | fruits, dried_fruit, whole_foods, snacks_adjacent |
| **scoring_relevance** | **future-candidate** — when Bari scores a fruit / dried-fruit category, the same drying step that concentrates minerals *also* concentrates sugar (and energy density). A naïve engine could reward mineral density while ignoring sugar density, or penalise sugar while missing the mineral concentration. Flag both, weigh deliberately. NOT a rule today; promotion = `EV-###` + D7. |
| **consumer_copy_usable** | yes — "more minerals, but also more sugar — easy to over-consume" is a clean Bari-style honest-tradeoff line for a future dried-fruit page (subject to no-health-claims: state the architecture, don't advise intake). |

**Reference.** Drying removes water, concentrating everything per gram — minerals *and* intrinsic
fruit sugars (and calories). The book's framing: a more concentrated mineral source than the fresh
equivalent, *"but also of fruit sugars so take care not to over-consume."* Per-fruit reference
labels from the spread: **goji berries** — iron (oxygen transport to tissues); **mango** — calcium
(bones/teeth), iron (immunity), potassium (nerve function).

**Why this is the one keeper in its batch.** It is the only fact in the dried-fruit / supplements /
hydration / digestion set that is *non-obvious as architecture* and *not already modelled*: it names
a concentration tradeoff that directly anticipates a future-category scoring decision. (Contrast:
supplement UL/toxicity is already encoded in the SIE EFSA-TUL ceiling; colonic SCFA absorption is
already encoded in the fiber-fermentability tier EV-006/EV-060; hydration/dehydration is health
advice Bari does not give.)

---

## KB-003 — In-vitro digestion bioavailability (INFOGEST / Caco-2) and the phytate "nutrient trap"

| Field | Value |
|---|---|
| **id** | KB-003 |
| **topic** | Bioaccessibility vs. theoretical nutrient content: INFOGEST static digestion model + Caco-2 intestinal absorption model as predictors of actual mineral and carotenoid uptake; phytic acid as a chelating antinutrient in high-phytate plant matrices |
| **source** | (1) INFOGEST static in-vitro digestion protocol — Minekus et al. (2014), *Food & Function* 5(6):1113–1124 (DOI: 10.1039/c3fo60702j) — the internationally harmonized static digestion model standardizing oral/gastric/intestinal phases for bioaccessibility research. (2) Caco-2 cell monolayer uptake assay — well-established in-vitro intestinal absorption proxy; widely used in food bioavailability literature (no single founding DOI; methodology routinely paired with INFOGEST). (3) Brazilian tropical fruits — carotenoid and anthocyanin bioaccessibility in exotic fruits studied via INFOGEST + Caco-2: *directional, specific study DOI pending confirmation* (TASK-285 research dump cited a Brazilian-fruits bioaccessibility study; DOI not confirmed at time of KB entry — do not cite as primary evidence until verified). (4) Phytic acid (inositol hexaphosphate, IP6) as a mineral chelator: Gupta et al. (2015), *Food Chemistry* 173:814–821 (DOI: 10.1016/j.foodchem.2014.10.069) — reviews phytate reduction strategies and mineral bioavailability impact. |
| **source_tier** | `primary_peer_reviewed` for the INFOGEST protocol DOI and phytate review. `directional_source_pending` for the specific Brazilian-fruits Caco-2 study (DOI unconfirmed). |
| **applies_to_future_categories** | whole_foods, legumes, fruits, vegetables, cereals, food_combinations |
| **scoring_relevance** | **future-candidate** — when Bari scores whole-food / legume / fruit categories, nominal nutrient content from the product label is a ceiling, not a guarantee. Bioavailability is not label-observable (no bioaccessibility % appears on any Israeli product label), and Caco-2 / INFOGEST data are not parseable from BSIP0. **Firewall fully applies: this entry does NOT move any published score and is NOT label-parseable; promotion to scoring action requires EV-### + D7 co-sign.** |
| **consumer_copy_usable** | yes — "high iron on the label doesn't mean all of it reaches the bloodstream" is a Bari-style honest-architecture observation for future legume/whole-grain copy, provided the source-DOI is confirmed before any consumer claim ships. Do not cite the Brazilian-fruits study specifically until the DOI is verified. |

**Core concept.** A food matrix's declared nutrient content (e.g., iron 4 mg/100g on the label) is the
total chemical quantity — not what the gut actually absorbs. The gap between declared and absorbed has
two layers:

- **Bioaccessibility** (release from the matrix during digestion) — measured by INFOGEST static
  digestion, which simulates oral, gastric, and small-intestinal phases to quantify how much of a
  nutrient is released into solution and thus *available* for absorption. This is the most
  standardized in-vitro proxy today.
- **Bioavailability / intestinal uptake** (transport across the epithelium) — measured by Caco-2 cell
  monolayer assays, which add an intestinal transport step on top of bioaccessibility, giving a more
  physiologically grounded estimate of actual cellular uptake.

**Phytate as the principal antinutrient in plant-based high-iron matrices.** Phytic acid (IP6) —
prevalent in legumes, whole grains, seeds, and some cereals — chelates divalent minerals (Fe²⁺,
Zn²⁺, Ca²⁺, Mg²⁺) in the gut lumen, reducing their bioaccessibility substantially. A high-iron
legume with high phytate load can deliver a fraction of its labeled iron as absorbable mineral. The
exact reduction is matrix-specific (moisture, pH, food combination, fermentation, cooking method all
modulate IP6 degradation by endogenous phytase activity).

**Carotenoid and anthocyanin case (Brazilian fruits, directional).** The research dump flagged a
Brazilian-tropical-fruits study applying INFOGEST + Caco-2 to carotenoid and anthocyanin
bioaccessibility. Finding: exotic fruit matrices showed variable but meaningfully lower bioaccessibility
of carotenoids and anthocyanins than their total-extract content suggests — processing, cell-wall
integrity, and lipid co-presence all modulate uptake. This is consistent with the general principle but
the specific DOI is unconfirmed; treat as directional until verified.

**Partial existing engine proxy (gap disclosure).** EV-009 provides a whole-grain structural credit
(intrinsic fiber / intact grain matrix) that implicitly rewards food-matrix integrity — the same
matrix that tends to modulate mineral bioaccessibility. EV-007 distinguishes intrinsic vs. isolated
fiber on mechanistic grounds, which overlaps with the matrix-integrity concept. KB-003 does NOT imply
these are absent; it frames the *bioavailability gap* (nutrient in vs. nutrient absorbed) as a
distinct future-scoring dimension not currently captured by any live EV, because it requires
bioaccessibility inputs that are not label-observable today.

**Firewall.** Nothing in this entry modifies scoring logic, activates a signal, or moves any published
score. Promotion path: confirm Brazilian-fruits DOI → `EV-###` proposal → D7 co-sign (Nutrition Agent
+ Product Agent). The phytate chelation principle itself could seed a future legume/whole-grain
bioaccessibility signal if label-parseable proxy inputs become available (e.g., declared phytate
content, if Israeli labels adopt it).
