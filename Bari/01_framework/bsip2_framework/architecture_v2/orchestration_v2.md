# BSIP2 Orchestration — v2 Design

**Status:** Architecture specification  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Companion:** layer_architecture.md, dimension_mapping.md

---

## The Problem with Averaging

The current system computes a weighted sum: ten dimensions, ten weights, one number. This design embeds a hidden assumption: that the ten things being measured are addable. That a product scoring 90 on protein quality and 10 on processing quality is equally valuable as a product scoring 50 on each.

This is false. And it leads to the pathologies that motivated this redesign:

- A heavily engineered protein shake can score C by averaging excellent Layer 2 signals against poor Layer 1 signals, producing a middle number that obscures both the strength and the failure.
- A whole-food product that happens to be high in saturated fat faces the same additive weight as a product whose saturation is accompanied by trans fats and seed oil blends.
- A product that is simultaneously high-protein, high-fiber, NOVA 4, and hyper-palatable produces a "50" — a number that communicates nothing about the actual tension.

The v2 orchestration replaces weighted averaging with **coordinated resolution**: each layer produces an interpretation, the interpretations are compared and negotiated, and the resolution is computed from the negotiation outcome — not from the mean.

---

## The Negotiated Scoring Philosophy

Bari v2 holds that food quality is irreducibly multi-dimensional. A score is not a measurement — it is a **verdict arrived at through structured deliberation**. The deliberation is explicit, traceable, and asymmetric.

The four-layer outputs are not equal voices. They have different roles in the negotiation:

| Layer | Voice Type | Function in Negotiation |
|-------|-----------|------------------------|
| L1: Structural Integrity | Ground-setting | Sets the maximum plausible ceiling |
| L2: Nutritional Contribution | Primary positive | Sets the minimum plausible floor |
| L3: Metabolic Stability | Contextual modifier | Adjusts within the space defined by L1 and L2 |
| L4: Consumption Engineering | Concern gate | Applies downward pressure when active |
| Regulatory (meta) | Hard policy | Applies hard caps outside the negotiation |

This is not a democracy. Each layer has a different type of authority.

---

## Layer Output Format

Each layer produces a structured interpretation object, not a bare number:

```
LayerOutput {
    index:       float    # 0–100 normalized score within this layer
    confidence:  float    # 0–100 confidence in this layer's assessment
    signals:     list     # up to 5 active signals that drove this assessment
    tension:     bool     # true if this layer's conclusion contradicts another layer
    tension_note: str     # description of the tension (if any)
}
```

Layer 4 outputs an inverted index: 0 = no detected engineering, 100 = maximal engineering. This is converted to a concern pressure value (100 − L4.index = remaining score headroom) before entering the orchestration.

---

## Orchestration Stages

### Stage 1: Structural Ceiling Computation

Layer 1 (Structural Integrity) establishes the **structural ceiling** for the final score.

The mapping is not linear. It is asymmetric by design:

| L1 Structural Integrity Index | Structural Ceiling |
|------------------------------|-------------------|
| 90–100 (intact whole food) | No ceiling (100) |
| 70–89 (minimally processed) | 95 |
| 50–69 (moderately processed) | 85 |
| 30–49 (substantially reconstructed) | 70 |
| 10–29 (heavily reconstructed) | 60 |
| 0–9 (near-complete deconstruction) | 50 |

The ceiling is a **soft cap by default**, not a hard wall. The orchestration can override it upward by at most 10 points when Layer 2 (Nutritional Contribution) is exceptionally strong. This accommodates the legitimate nutritional value of well-designed protein isolates or fortified products.

The ceiling can be overridden downward (set lower than the table value) by Layer 4 (Consumption Engineering) when engineering is severe.

---

### Stage 2: Nutritional Floor Computation

Layer 2 (Nutritional Contribution) establishes the **nutritional floor** for the final score.

| L2 Nutritional Contribution Index | Nutritional Floor |
|----------------------------------|------------------|
| 80–100 (exceptional contribution) | 50 |
| 60–79 (meaningful contribution) | 40 |
| 40–59 (moderate contribution) | 30 |
| 20–39 (limited contribution) | 20 |
| 0–19 (negligible contribution) | 10 |

The floor prevents a product with genuine nutritional value from being arbitrarily collapsed by structural concerns. If Layers 1 and 4 conspire to push a nutritionally rich product below its floor, the floor wins — but with an explicit annotation that structural concerns exist.

**Floor-ceiling interaction:**  
If the nutritional floor exceeds the structural ceiling (a reconstructed product with exceptional nutrition), the system does not average. Instead, it applies the ceiling with a prominent notation: "NUTRITION-STRUCTURE TENSION: Product delivers genuine nutritional value within a heavily reconstructed matrix."

---

### Stage 3: Metabolic Stability Adjustment

Layer 3 (Metabolic Stability) adjusts the score within the range established by Stages 1 and 2.

The metabolic stability adjustment is bounded to ±15 points from the mid-range score:
- If Layer 3 index is 75–100: +5 to +15 point adjustment (metabolically stable)
- If Layer 3 index is 50–74: 0 to +5 point adjustment (neutral)
- If Layer 3 index is 25–49: −5 to −10 point adjustment (metabolically challenging)
- If Layer 3 index is 0–24: −10 to −15 point adjustment (metabolically volatile)

This bounded range ensures Layer 3 is a modifier, not a dominant voice. It cannot rescue a product with terrible Layers 1 and 2, and it cannot sink a product with excellent Layers 1 and 2.

---

### Stage 4: Consumption Engineering Pressure

Layer 4 (Consumption Engineering) applies downward pressure when active. Unlike the other layers, this is not a floor/ceiling mechanism — it is a **concern gate**.

The Layer 4 concern pressure function:

```
engineering_pressure = L4.index × engineering_weight

Where:
  engineering_weight = 0.00   # if L4.index < 20 (no significant engineering detected)
  engineering_weight = 0.15   # if L4.index 20–50 (moderate engineering)
  engineering_weight = 0.30   # if L4.index 50–75 (significant engineering)
  engineering_weight = 0.45   # if L4.index 75–100 (severe engineering)

score_after_L4 = pre_L4_score × (1 − engineering_pressure)
```

This design means:
- A product with L4 index of 0 receives no adjustment
- A product with L4 index of 90 and a pre-L4 score of 60 would receive: 60 × (1 − 0.45) = 33 — a meaningful drop, but not annihilation
- Layer 4 cannot push a score below 20 on its own (absolute floor from Layer 2 protects)

**Why multiplicative, not additive?**  
Additive penalties interact unpredictably with confidence ceilings, floors, and caps. A multiplicative factor maintains proportional relationships: a higher-scoring product takes a proportionally larger hit from engineering concerns, which is the right behavior.

---

### Stage 5: Regulatory Resolution

Regulatory signals (Israeli red labels, trans fat veto) are applied after all layer negotiation as **hard policy constraints**:

| Regulatory condition | Action |
|--------------------|--------|
| Trans fat veto (>1.0g/100g) | Score = 0, grade = E, override all layers |
| 3+ red labels | Maximum score = 40 regardless of layers |
| 2 red labels | Maximum score = 50 regardless of layers |
| 1 red label | Score reduced by 10, floor at 45 |
| 0 red labels | No regulatory constraint |

Regulatory resolution operates **outside the layer negotiation**. It is a policy commitment, not an analytical conclusion.

---

### Stage 6: Confidence Resolution

Confidence modulation applies last, as it does in the current architecture. The output of the five prior stages is subject to confidence ceilings when data quality is insufficient.

| Confidence band | Ceiling |
|----------------|---------|
| High (80+) | None |
| Medium (60–79) | None |
| Low (40–59) | 70 |
| Insufficient (<40) | 50 |

Confidence is computed from data completeness and internal consistency checks, unchanged from the current methodology.

---

## Contradiction Handling

When layers produce contradictory signals, the contradiction is preserved in the output — not resolved into a neutral number.

**Defined contradiction types:**

### C-1: Nutritional Excellence + Structural Failure
*"The food delivers genuine nutrition, but the matrix is heavily reconstructed."*

Example: A whey protein isolate drink with 25g protein, engineered texture, and NOVA 4.

Resolution:
- Layer 2 floor prevents collapse below 50
- Layer 1 ceiling limits above 70
- Output: score in 50–70 range with explicit C-1 tension annotation
- UI: "Strong nutrition, reconstructed matrix"

---

### C-2: Structural Integrity + Nutritional Emptiness
*"The food remains close to its source, but provides little nutritional contribution."*

Example: A whole-food oil (NOVA 1, intact) with zero protein, zero fiber, maximum caloric density.

Resolution:
- Layer 1 sets high ceiling (90+)
- Layer 2 floor is low (10–30)
- Layer 3 metabolic assessment considers calorie density without satiety
- The WHOLE_FOOD_FAT floor (current: 65) is preserved as a policy commitment that whole-food fats deserve recognition regardless of nutrient density
- Output: score in 65–80 range with explicit C-2 tension annotation
- UI: "Whole food integrity, limited direct nourishment"

---

### C-3: Metabolic Stability + Engineering Presence
*"The product is likely metabolically stable, but shows engineering for overconsumption."*

Example: A sweetener-based protein bar with excellent fiber and protein ratios but multiple palatability engineering signals.

Resolution:
- Layer 3 applies positive adjustment
- Layer 4 applies concern pressure
- These partially offset
- Output: net adjustment computed from both, with explicit C-3 annotation
- UI: "Structural satiety, palatability engineering present"

---

### C-4: Fortification + Structural Reconstruction
*"The product achieves nutrient density through fortification within a heavily processed matrix."*

Example: A fortified breakfast cereal — NOVA 4, excellent declared micronutrients, low natural nutrient content.

Resolution:
- Layer 2 applies fortification skepticism discount (synthetic nutrients credited at 50–70% of whole-food equivalents)
- Layer 1 ceiling reflects reconstruction
- Output: moderate score (40–60 range) with explicit C-4 annotation
- UI: "Declared nutrition via fortification, not whole-food matrix"

---

## Cap and Floor Evolution

The current system has 17 hard-cap rules and multiple floor provisions. In v2, these are reorganized into a cleaner hierarchy:

**Preserved as structural mechanisms:**
- Trans fat veto (absolute, outside layer system)
- NOVA 1 whole-food floor (reframed as minimum Layer 2 floor elevation for structurally intact whole foods)
- Regulatory hard caps (reframed as Stage 5 policy constraints)

**Retired as standalone rules, absorbed into layer logic:**
- NOVA_PROXY_4_ULTRA_PROCESSED cap → Layer 1 structural ceiling
- ADDITIVE_MARKERS caps → Layer 1 additive architecture signal
- HIGH_CAL_LOW_SATIETY caps → Layer 3 metabolic stability signal
- HIGH_CAL_HIGH_SUGAR caps → Layer 3 + Layer 4 combined assessment
- SWEETENER_CAP → Layer 4 concern gate signal

**Why fewer hard caps?**  
Hard caps create cliff behavior: a product at sugar=24.9g and a product at sugar=25.0g receive dramatically different scores. In v2, these thresholds become signals within their respective layers, contributing to a continuous layer index rather than firing a binary rule. The concern is preserved; the cliff is smoothed.

---

## What "Negotiated, Not Averaged" Means in Practice

Given a product with:
- Layer 1 (Structural Integrity) = 30 (heavily reconstructed)
- Layer 2 (Nutritional Contribution) = 80 (exceptional protein delivery)
- Layer 3 (Metabolic Stability) = 55 (moderate)
- Layer 4 (Consumption Engineering) = 60 (significant engineering)

**Old system (averaging):**  
Might compute: 0.15×(NOVA4=25) + 0.15×(good protein) + … → somewhere around 45–55, obscuring both the strength and the failure.

**New system (negotiation):**
1. Stage 1: L1=30 → structural ceiling = 60
2. Stage 2: L2=80 → nutritional floor = 50
3. Stage 3: L3=55 → metabolic adjustment = +2
4. Working score = 52, adjusted to 54 after Stage 3
5. Stage 4: L4=60 → engineering weight = 0.30, pressure = 60×0.30 = 18% reduction: 54 × (1-0.18) = 44
6. Stage 5: No red labels, no trans fat
7. Stage 6: Confidence band = high (80), no ceiling
8. Final score: **44 [D]**

With explicit output:
- Structural ceiling was binding (60)
- Nutritional floor provided minimum protection (50)
- Engineering pressure reduced score from 54 to 44
- C-1 tension active: "Exceptional protein delivery within heavily reconstructed matrix"

The score of 44 is lower than the old system might produce, but it is more honest about what is actually happening — and it is fully traceable.

---

## Dominant Concern Detection

The v2 orchestration preserves the concept of a **dominant concern driver** — the single most important reason a product scores where it does:

```
dominant_concern = max_impact(
    L1_ceiling_delta,     # how much structural ceiling reduced the score
    L2_floor_boost,       # how much nutritional floor elevated the score
    L3_adjustment,        # how much metabolic stability modified the score
    L4_pressure_delta,    # how much engineering concern reduced the score
    regulatory_delta,     # how much regulatory signals constrained the score
)
```

The dominant concern is reported as the first explanation driver in all user-facing output. No product should require more than 3 drivers to explain (the 3-driver limit from `explainability_budget.md` is preserved).

---

*Next: See `framework_philosophy.md` for what Bari is and is not as a food intelligence system.*
