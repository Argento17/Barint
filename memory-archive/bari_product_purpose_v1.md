---
name: ""
metadata: 
  node_type: memory
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Built 2026-05-29. Master document at `C:\Bari\01_framework\[DELETED]\product_purpose_framework_v1.md`.

**Why:** The Comparison Governance Constitution identified purpose divergence as the default condition on the Israeli shelf. This framework defines how Bari determines what a product is trying to accomplish — before scoring, before comparison — so that interpretation is purpose-aware rather than purpose-blind.

**How to apply:** Classify every product's primary purpose (from the 7-class taxonomy) before constructing comparisons. Validate marketing claims against structural signals. Flag purpose divergence as a finding. Apply detection methodology at BSIP1 enrichment stage.

## Seven Purpose Classes

**Tier I — General Integration:**
- Class 1: Everyday Nutrition — routine balanced contribution; plain yogurt, standard bread, whole milk
- Class 2: Indulgence — pleasure/experience primary; traditional desserts, chocolate spread

**Tier II — Targeted Delivery:**
- Class 3: Macro Delivery — protein (3a, ≥15g/100g threshold), fiber (3b), caloric reduction (3c)
- Class 4: Functional Nutrition — specific health function at meaningful dose (probiotic CFU, fortification RDA)
- Class 5: Sports/Performance — ≥18g/100g protein, recovery architecture, athlete need state

**Tier III — Constrained:**
- Class 6: Developmental — children's (6a), elderly (6b), prenatal (6c); different nutritional standards
- Class 7: Dietary Restriction — medical (7a: celiac, allergy), metabolic (7b: keto, diabetic), lifestyle (7c: vegan, kosher)

## Three Purpose Layers

- **Nutritional purpose** — what architecture implies (GROUND TRUTH)
- **Marketing purpose** — what manufacturer claims (DATA to evaluate)
- **Consumer purpose** — what consumers actually use it for (aspirational; requires research)

When nutritional ≠ marketing: that divergence is a Bari finding.

## Detection: 6-Step Methodology

1. Structural signal scan (protein content, calories, carbs vs. category baseline)
2. Ingredient signal validation (isolated protein, functional additives, restriction ingredients)
3. Name/claim signal evaluation (validate or challenge claim against structural signals)
4. Category context calibration (shelf placement as weak prior)
5. Confidence assessment (high/medium/low/unclassifiable)
6. Marketing purpose divergence check (compare detected vs. claimed; document gap)

## Purpose Governance Rules

- Comparison groups defined by nutritional purpose, not shelf category
- Children's products never ranked against adult products
- Restriction products never ranked against unrestricted alternatives (without disclosure)
- Purpose classification must precede scoring — never retroactive rationalization
- Marketing purpose requires structural validation to become purpose classification

## Six Failure Modes

- FM1: Marketing Purpose Manipulation — gaming comparison group membership
- FM2: Health Halo Creation — secondary claim inflates whole-product perception
- FM3: Protein Obsession — protein as universal health proxy; most active failure
- FM4: Functional Food Inflation — sub-functional doses claiming functional status
- FM5: Restriction Purpose Exploitation — incidental "free-from" claims for positioning
- FM6: Score-Purpose Circular Reasoning — post-hoc purpose to rationalize anomalous score

## Key Structural Finding

BSIP2 does not currently encode purpose. Purpose detection belongs in BSIP1 enrichment as fields: `primary_purpose`, `secondary_purpose`, `purpose_confidence`, `marketing_purpose`, `purpose_divergence_flag`. Recommended for BSIP3 implementation.

## Red Team Review Outcome (2026-05-29)

`C:\Bari\01_framework\[DELETED]\purpose_framework_critique_v1.md` — Framework v1 does NOT survive scrutiny unchanged.

**Three fatal flaws:**
1. Category error — purpose is a consumer property, not a product property; architecture ≠ consumer intent
2. Seven-class taxonomy is too fine-grained for stable classification (Greek yogurt, peanut butter, granola all break it)
3. Indulgence class creates nutritional immunity risk

**Recommendation: B — Adopt with significant modifications:**
- Reduce to 3 classes: General Nutrition / Targeted Delivery / Constrained Nutrition
- Move classification from BSIP1 upstream to comparison-time (Model C)
- Eliminate Indulgence as a purpose class; retain as editorial characterization only
- Consumer purpose is the north star; architectural purpose is a proxy, not ground truth
- Marketing divergence finding retained as editorial output, not requiring full classification

**What the critique preserved:**
- Core insight: purpose divergence exists and requires disclosure
- Three-layer model (nutritional/marketing/consumer) reframed with consumer as north star
- Six failure modes (all valid independently)
- Dietary restriction and developmental products belong in separate comparison pools

[[bari-comparison-governance-v1]]
[[bari-governance-v1]]
