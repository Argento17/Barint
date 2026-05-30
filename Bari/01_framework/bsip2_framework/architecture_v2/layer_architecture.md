# BSIP2 Layer Architecture — v2 Design

**Status:** Architecture specification  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Supersedes:** Single-layer weighted dimension model (BSIP2 proto_v0)

---

## Preamble

BSIP2 v2 introduces a **four-layer interpretive architecture** that replaces the single weighted-dimension model. The change is not cosmetic. It reflects a fundamental shift in how food intelligence is conceptualized:

> The current model asks: "How do these ten signals add up?"  
> The v2 model asks: "What are four different things true about this food, and how do those truths interact?"

The four layers are not scores. They are **interpretive lenses** — each trained on a different question, each producing a different type of understanding. The orchestration system then coordinates their outputs into a final assessment.

This document defines each layer, its philosophy, its scope, and its candidate signals.

---

## Why Four Layers

The existing 10-dimension model suffers from **hidden collinearity**: NOVA level controls three dimensions (Processing Quality, Whole Food Integrity, Additive Quality) that together represent roughly 29% of nominal weight. In practice, NOVA's effective influence on the final score exceeds 40%. This is not intentional — it is an emergent property of the architecture.

The four-layer model decentralizes NOVA by placing it inside Layer 1 as one signal among several. The other three layers evaluate dimensions that NOVA cannot see: what the food actually delivers nutritionally, how it is likely to behave metabolically, and whether its design implies optimization for overconsumption.

No single layer should dominate. The architecture is designed for **productive tension** between layers, not convergence.

---

## The Four Layers

### Layer 1 — Structural Integrity

**Governing question:**  
*Does this still behave like food?*

**What this layer assesses:**  
The relationship between a product and its source material. Structural integrity is not a judgment about processing per se — pasteurization, fermentation, and cooking are recognized as compatible with integrity. The layer asks how far a product has traveled from its biological origin through the specific combination of fragmentation, reconstruction, and additive supplementation.

**Core philosophy:**  
A food's structure carries information. When an oat is rolled, the matrix is modified. When it is pulverized, extracted, and recombined into a puffed pellet with emulsifiers and flavoring, the matrix is largely destroyed and a new one is constructed. Structural integrity tracks this trajectory.

**Candidate signals:**

| Signal | Description | Source |
|--------|-------------|--------|
| NOVA classification | Processing level (1–4) | L3 inference |
| Reconstruction intensity | How far from source material (spectrum: intact → fragmented → extracted → reconstructed) | L3 inference |
| Ingredient topology | Number, complexity, and relational structure of the ingredient list | L1 observed |
| Additive architecture | Count, functional class, and density of additive categories | L3 inference |
| Ingredient fragmentation | Presence of fractionated ingredient forms (isolates, concentrates, hydrolyzates) | L3 inference |
| Matrix coherence | Whether declared ingredients plausibly form a coherent food matrix | L3 inference |
| Beneficial processing credit | Fermentation, pasteurization: recognized as integrity-compatible | L3 inference |
| Whole-food continuity | Proportion of ingredient list that remains close to whole-food form | L3 inference |

**What this layer does NOT assess:**  
Nutrition. A product can have poor structural integrity and excellent nutrition (fortified isolate protein drink), or high structural integrity and poor nutrition (whole-fat coconut cream). Structural integrity is agnostic about nutritional delivery.

**Output:**  
A Structural Integrity Index (0–100) representing how much this product retains the structural properties associated with food rather than a manufactured food-like construction.

**Relationship to NOVA:**  
NOVA is a primary signal within this layer. A NOVA 4 classification is strong evidence of low structural integrity. But it is not the only signal. A product with NOVA 3, multiple protein isolates, and 12 functional additive categories may have lower structural integrity than its NOVA classification suggests. Conversely, a NOVA 4 product with a legitimate functional additive and an otherwise intact matrix may score better on structural integrity than a raw NOVA mapping would predict.

---

### Layer 2 — Nutritional Contribution

**Governing question:**  
*Does this materially nourish?*

**What this layer assesses:**  
Whether the product genuinely delivers nutritional value — protein, fiber, micro-coverage, macro coherence — as opposed to merely filling caloric space without contribution. This layer is explicitly **positive**: it rewards what is present, not just penalizes what is absent.

**Core philosophy:**  
The current architecture is primarily punitive: it detects structural failures and applies penalties. Layer 2 is designed to be the primary positive signal in the system. A product that genuinely delivers 15g of high-quality protein, substantial dietary fiber, and a coherent macro profile should receive meaningful credit regardless of its NOVA level.

This layer also applies **fortification skepticism**: nutrients added through synthetic fortification do not carry the same credibility as nutrients present in the whole-food matrix. Vitamin D in fortified cereal is not nutritionally equivalent to vitamin D in whole fish. Layer 2 credits the former less than the latter.

**Candidate signals:**

| Signal | Description | Source |
|--------|-------------|--------|
| Protein contribution | Amount and source quality of protein per 100g | L1 + L3 |
| Fiber contribution | Amount and structure of dietary fiber | L1 + L3 |
| Macro coherence | Whether the macronutrient profile is internally consistent and plausible for the stated product | L2 derived |
| Calorie context | Whether caloric content is proportional to nutritional contribution | L2 derived |
| Nutrient density | Combined protein + fiber per calorie | L2 derived |
| Fortification skepticism | Synthetic fortification credited at reduced rate vs. matrix-present nutrients | L3 inference |
| Micronutrient plausibility | Whether declared micronutrients are plausible given the ingredient list | L3 inference |
| Protein realism | Whether the declared protein is plausible given ingredient list | L3 inference |

**What this layer does NOT assess:**  
Metabolic effects, palatability, or structural integrity. A product can have high nutritional contribution and poor structural integrity (whey isolate) or low nutritional contribution and high structural integrity (olive oil — nutritionally coherent but not a protein or fiber source).

**Output:**  
A Nutritional Contribution Index (0–100) representing how much genuine nourishment this product delivers relative to its energy content and category context.

**The low-calorie trap:**  
This layer explicitly guards against the "low calorie = healthy" fallacy. A product at 30 kcal with zero protein, zero fiber, and zero meaningful fat — but with vitamins sprayed on — scores low on Layer 2. Calorie density is useful only when it is accompanied by proportional nutritional content.

---

### Layer 3 — Metabolic Stability

**Governing question:**  
*How physiologically stable is this likely to be?*

**What this layer assesses:**  
The probable metabolic trajectory of consuming this product — glycemic behavior, satiety response, digestion dynamics, and energy delivery characteristics. This layer operates at the population-level hypothesis layer (L5 in the signal taxonomy): it does not make individual predictions, but evaluates structural plausibility of stability signals.

**Core philosophy:**  
Two products can have identical macros but very different metabolic profiles. White rice and lentils both deliver carbohydrates, but the fiber-protein matrix of lentils produces a substantially different glycemic response. Layer 3 evaluates whether a product's composition suggests metabolic stability — slower absorption, sustained satiety, moderate glycemic pressure — or metabolic volatility — rapid absorption, short satiety, glycemic spike risk.

This layer is **explicitly probabilistic**. It does not claim to know how any individual metabolizes any product. It evaluates structural plausibility based on population-level nutritional science.

**Candidate signals:**

| Signal | Description | Source |
|--------|-------------|--------|
| Glycemic plausibility | Fiber/sugar ratio, sugar type (natural vs. added), matrix context | L2 + L3 |
| Satiety plausibility | Protein + fiber as predictors of satiety durability | L2 + L3 |
| Calorie density context | Caloric content relative to physical volume and matrix | L2 |
| Liquid calorie effect | Liquid form reduces satiety signaling regardless of caloric content | L3 (category) |
| Fat/carbohydrate interaction | Presence of fat as glycemic moderator vs. triglyceride concern | L2 |
| Digestion speed signal | Physical form and matrix structure as proxies for digestion rate | L3 |
| Sugar-fiber dynamic | Whether fiber is present in sufficient proportion to modulate sugar absorption | L2 |
| Satiety architecture | Whether protein, fiber, and fat are co-present in a satiety-supporting configuration | L3 |

**What this layer does NOT assess:**  
Whether the food is "good" or "bad" in an absolute sense. A product can be metabolically stable and nutritionally poor (plain water). It can be metabolically challenging and nutritionally rich (fruit juice with high natural sugar but real micronutrients). Layer 3 evaluates stability dynamics only.

**Output:**  
A Metabolic Stability Index (0–100) representing the likelihood that this product produces a stable physiological response when consumed in normal portions, based on structural composition alone.

**The satiety-calorie interaction:**  
Calorie density is evaluated here in the context of what accompanies the calories. A 400 kcal/100g product with 20g protein and 8g fiber is metabolically very different from a 400 kcal/100g product with zero protein and zero fiber. The former may be more metabolically stable than a 150 kcal/100g product with no structural satiety support.

---

### Layer 4 — Consumption Engineering

**Governing question:**  
*Was this optimized for overconsumption?*

**What this layer assesses:**  
Whether the product shows evidence of having been engineered to circumvent or suppress satiety signaling — to encourage consumption beyond physiological need through sensory, chemical, or structural manipulation.

**Core philosophy:**  
This layer is the most novel in the architecture. It is also the most philosophically charged, and must be applied with precision. Not all engineering is manipulation. Not all palatability is engineering. A well-made croissant is pleasurable; that is different from a product designed to have an addictive neurochemical profile.

Consumption Engineering detects specific patterns:
- **Reward stacking**: simultaneously maximizing multiple reward dimensions (fat + sugar + salt + texture + flavor)
- **Satiety suppression**: sweetener systems that promise sweetness without caloric satiety, creating appetite displacement
- **Liquid calorie delivery**: high-calorie liquids that bypass the reduced-appetite signal triggered by solid food
- **Sensory amplification**: artificial flavoring systems that amplify palatability beyond what the food matrix naturally supports
- **Texture engineering**: structural manipulation (aeration, extrusion, homogenization) that modifies the oral experience to encourage continued consumption

Layer 4 is NOT:
- Anti-palatability: it is not a penalty for tasting good
- Anti-processing: it is not triggered by cooking, fermentation, or even standard food manufacture
- Anti-convenience: it is not triggered by packaging or portion format alone

**Candidate signals:**

| Signal | Description | Source |
|--------|-------------|--------|
| Hyper-palatability pattern | Fat+sugar, fat+salt combo in concentrations above natural food range | L2 + L3 |
| Sweetener system | Presence of non-nutritive sweeteners, especially in combination | L3 |
| Flavor amplification | Synthetic flavor enhancers (MSG, E-621, etc.) or synthetic flavor systems | L3 |
| Reward stacking index | Number of simultaneously-active reward dimensions | L3 |
| Liquid calorie delivery | High-calorie beverage that reduces satiety signaling | L3 (category) |
| Sensory engineering markers | Texture agents engineered for experience rather than structure | L3 |
| Artificial color | Colors added for visual appeal rather than food identity | L3 |
| Additive convergence | Multiple additive categories targeting the same sensory dimension | L3 |

**What this layer does NOT assess:**  
Structural integrity, nutritional contribution, or metabolic behavior. A product can score high on Consumption Engineering and have excellent nutrition (a highly palatable protein shake). It can score low on Consumption Engineering and have terrible nutrition (a nutritionally empty plain rice cracker). Layer 4 is specifically about the design intent for overconsumption.

**Output:**  
A Consumption Engineering Index (0–100) representing the degree to which this product shows evidence of engineering for consumption beyond satiety. Unlike the other layers, a HIGH score on this layer is a CONCERN, not a positive signal. It functions as a concern multiplier in the orchestration phase.

**The direction of this layer:**  
Layer 4 is inverted. A score of 0 means no detected engineering for overconsumption. A score of 100 means maximal detected engineering. This inversion is made explicit in the orchestration contract.

---

## Layer Relationships

The four layers are not independent. They interact in predictable and structured ways:

```
Layer 1 (Structural Integrity)
  └─ Establishes the ground floor. Low integrity sets a ceiling on final score.
  └─ Feeds Layer 4: certain additive architectures suggest engineering intent.

Layer 2 (Nutritional Contribution)
  └─ Primary positive signal. High contribution lifts the floor.
  └─ Contextualizes Layer 3: nutrition density changes metabolic interpretation.

Layer 3 (Metabolic Stability)
  └─ Modifier, not anchor. Adjusts within the range set by Layers 1 and 2.
  └─ Interacts with Layer 4: sweetener systems affect both.

Layer 4 (Consumption Engineering)
  └─ Concern gate. High engineering score exerts downward pressure on final output.
  └─ Cannot fully override Layer 2: genuine nutrition is not nullified by palatability.
```

**Cross-layer tensions (expected and productive):**
- High Layer 2 + High Layer 4: "Nutritious but engineered for overconsumption" → visible tension, not resolved to a mean
- High Layer 1 + Low Layer 2: "Structurally intact but nutritionally empty" → whole food with low contribution
- Low Layer 1 + High Layer 2: "Reconstructed but nutritionally dense" → protein isolate territory
- Low Layer 3 + Low Layer 4: "Metabolically unstable but not engineered" → whole food with high sugar (dates, fruit juice)

---

## Layer Weighting Philosophy

The four layers are **not equal in their architectural function:**

| Layer | Function | Role in Orchestration |
|-------|----------|-----------------------|
| Structural Integrity | Ground floor | Sets ceiling: low integrity limits maximum score |
| Nutritional Contribution | Primary positive signal | Sets floor: high contribution limits minimum score |
| Metabolic Stability | Contextual modifier | Adjusts within established range |
| Consumption Engineering | Concern gate (inverted) | Applies downward pressure when active |

This asymmetry is intentional. See `orchestration_v2.md` for the full negotiation logic.

---

## What This Architecture Is NOT

- **Not a democratic scoring system.** The four layers do not average their outputs. They negotiate.
- **Not a NOVA replacement.** NOVA belongs inside Layer 1. It is one important signal among several.
- **Not category-specific.** These four layers apply to every food category. Category context adjusts signal calibration but does not change the interpretive framework.
- **Not a reformulation guide.** Bari does not tell manufacturers how to score better. It evaluates structure as-found.
- **Not static.** The candidate signals listed in each layer are the initial population. The architecture is designed to accept new signals without requiring redesign.

---

*Next: See `dimension_mapping.md` for the mapping of current BSIP2 dimensions into this layer structure.*
