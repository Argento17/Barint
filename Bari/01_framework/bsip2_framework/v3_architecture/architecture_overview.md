# BSIP2 v3 Architecture Overview

**Status:** Architectural design — implementation pending
**Supersedes:** `architecture_v2/layer_architecture.md`
**Date:** 2026-05-18

---

## The Three Universal Layers

Bari's pipeline is a three-layer system. The first two layers are category-agnostic. The third is where interpretation begins.

```
BSIP0  — Universal observation
BSIP1  — Universal normalization
BSIP2  — Archetype-specific interpretation
            ↑
         Divergence begins here
```

### BSIP0: Universal Observation Layer

BSIP0 is a scraping and evidence collection system. It does not understand food. It records what it sees. Inputs are retailer-specific (Yohananof, Rami Levy, etc.); outputs are raw observation records — one JSON per retailer product observation.

BSIP0 has no food category logic. A nutrition panel is a nutrition panel. Ingredient text is ingredient text. The schema is identical whether the product is a cereal or a cooking oil.

**Nothing in BSIP0 is category-specific. This is correct and must not change.**

### BSIP1: Universal Normalization Layer

BSIP1 resolves retailer-specific observations into canonical product objects. Its responsibilities:

- Merge multiple retailer observations for the same product (barcode-anchored)
- Normalize nutrition to per-100g basis
- Resolve conflicts across observations
- Assign confidence and trust scores
- Produce a single `bsip1_<barcode>.json` per canonical product

BSIP1's output schema is food-category-agnostic. The `canonical_product_id`, `normalized_nutrition_per_100g`, `ingredients_list`, `confidence`, and all required fields in `input_loader.py:REQUIRED_FIELDS` are identical for a breakfast cereal, a cooking oil, and a protein drink.

**BSIP1 does not score products. It does not assign categories. It does not interpret.**

The custom field `bsip_cereal_subtype` added in `run_cereals_001/create_bsip1_cereals.py` is an annotation, not a category decision. Annotations are permitted and useful, but they are informational, not structural.

**Nothing in BSIP1 is category-specific. This is correct and must not change.**

### BSIP2: Archetype Interpretation Layer

BSIP2 is where category knowledge lives. It answers: "What does this nutritional profile mean for a product of this structural type?"

The current BSIP2 (`proto_v0/src/`) is a valid monolith for a single-category prototype. It has already demonstrated that the framework can score milk and cereals from the same codebase. But its flat file structure cannot scale:

- `category_classifier.py` encodes category logic as a flat signal-weight dictionary
- `score_engine.py` embeds category-specific guardrail logic inline (the `is_snack_bar` check, the `category == "cereal"` HP_CRUNCH gate, the `satiety_rules_gated` cooking-oil exemption)
- `constants.py` has a single `CALORIE_DENSITY_TABLES` dict that conflates all categories in one flat structure
- There is no formal concept of "archetype" — category is used informally and inconsistently

The cereals stress test exposed the scaling failure concretely: granola products were misrouted to `whole_food_fat` because the category classifier had no hard anchor logic. The misrouting caused 20-25 point scoring errors — not because the scoring math was wrong, but because the product ended up in the wrong interpretation context.

**The divergence between products should begin exactly at BSIP2, and the architecture should make that divergence explicit, controlled, and traceable.**

---

## What "Universal" Means in BSIP2

The v3 architecture does not make BSIP2 category-agnostic — that would be wrong. Products are physically different. An oat grain and a cooking oil require different frameworks for their calorie density to be interpretable.

"Universal" in BSIP2 means:

1. **Shared scoring mathematics.** The 10-dimension scoring engine, the concern coordination system, the confidence calculation, and the waterfall trace format are identical for every product.

2. **Shared ontology.** The signal vocabulary — Hebrew ingredient patterns, NOVA proxy algorithm, red-label threshold rules, additive category definitions — is maintained once and used everywhere.

3. **Shared orchestration.** The pipeline stages (extract signals → classify → infer NOVA → assign scope → score → write trace) are identical for every product.

4. **Archetype-specific parameters.** Calorie density tables, which guardrail caps activate, dimension weight profiles, local signals, and floor definitions vary by archetype. These differences are isolated in archetype modules and injected into the shared engine.

The key insight is that an archetype is not a different algorithm. It is a different **interpretation context** for the same algorithm. The math that evaluates glycemic quality is identical for a cereal and a snack bar; what differs is which caps apply downstream, which calorie density table the score is compared against, and which local signals (e.g., extrusion integrity for cereals, fermentation markers for yogurt) are relevant.

---

## Why This Improves Scalability

The current monolith has four scaling problems:

**Problem 1: Category logic is scattered.**
Category-specific rules live in `score_engine.py` (HP_CRUNCH gate), `constants.py` (calorie density tables), and `category_classifier.py` (signal weights). Adding a new category requires touching all three files. There is no single place to look to understand "how does cereal scoring work."

**Problem 2: The router is a single-pass signal accumulator.**
`category_classifier.py` scores all categories simultaneously and picks the highest. There are no hard anchors, no two-stage resolution, no hybrid product handling. The cereals run showed that a 2.35 signal score for `whole_food_fat` routinely beats a 0.9 signal for `snack_bar_granola` when a granola product contains nuts. The router is the first thing that breaks when product diversity increases.

**Problem 3: New categories require forking the batch runner.**
`batch_run_cereals_001.py` is a copy of `batch_run_milk_004.py` with output paths changed. The pipeline logic is duplicated. As categories multiply, maintenance diverges.

**Problem 4: There is no ontology.**
Signal vocabularies, NOVA proxy patterns, and fortification markers are inline in `signal_extractor.py`. Adding a new signal requires reading and editing 600+ lines of code. There is nowhere to reason about the signal system abstractly.

**The v3 architecture solves all four problems** by separating: shared engine (touches nothing when adding a new archetype) → ontology (one place for signal vocabulary) → router (explicit, testable routing logic) → archetype modules (isolated interpretation contexts).

---

## What Stays the Same

The following components are correct and should not be restructured; they should simply be relocated to the appropriate core module:

- NOVA proxy algorithm (`nova_proxy.py`)
- Dimension scoring formulas (`score_engine.py:score_*` functions)
- Concern coordination engine (`score_engine.py:_coordinate_family`)
- Confidence calculation (`score_engine.py:compute_confidence`)
- Structural emptiness gate (`score_engine.py:detect_structural_emptiness`)
- Floor/cap application hierarchy (`score_engine.py:apply_floors`)
- Waterfall trace format (`trace_writer.py`)
- Israeli red-label threshold values
- Grade thresholds (S/A/B/C/D/E)

**The scoring math has been validated across two categories (milk, cereals) and two calibration runs. It is not being redesigned.**
