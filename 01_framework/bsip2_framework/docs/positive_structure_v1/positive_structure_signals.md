# Positive Structure Signals

**Status:** Design document — candidate signal catalog. No detection thresholds or scoring weights are defined here.  
**Purpose:** Enumerate the candidate positive structural signals for BSIP2, with rigorous analysis of each signal's conceptual grounding, gaming risk, and architectural relationship.  
**Companion documents:** `matrix_integrity_framework.md`, `ingredient_fragmentation_framework.md`, `source_aware_satiety.md`, `macro_coherence_framework.md`

---

## Organization

Signals are grouped by architectural layer:

- **L3 signals:** Inferred from ingredient detection and nutritional data
- **L4 signals:** Interpreted from combinations of L1–L3 signals
- **Scoring-layer signals:** Operate in the scoring pipeline (dimension inputs, floor conditions, cap modifiers)

For each signal:
- Conceptual definition
- Why it matters
- Detection approach
- Gaming risk
- Explainability quality
- Relationship to NOVA
- Relationship to current penalties and caps
- BSIP2 implementation priority

---

## L3 Candidate Signals

---

### `intact_matrix_primary`

**Conceptual definition:**  
The primary ingredients (top 2–3 by weight) retain the structural form of their source food — cell walls intact, macronutrient components co-located as they exist in the biological source.

**Why it matters:**  
The food matrix determines digestion rate, satiety signal duration, and nutrient co-factor delivery. An intact primary matrix is the most fundamental positive structural property a food can have.

**Detection approach:**  
Ingredient detection with fragmentation-level tagging. Primary ingredients at fragmentation Level 0–1 (whole food or mechanical transformation) activate this signal. Primary ingredients at Level 4–5 (isolates, syrups, extracted fractions) suppress it. The signal is graduated — a product with two Level 0 primary ingredients and one Level 3 secondary has moderate intact_matrix; a product with all Level 0–1 ingredients has high intact_matrix.

**Gaming risk: Medium**  
The label-engineering path is to use clean-sounding names for processed ingredients ("milk protein" instead of "milk protein concentrate"; "oat flour" for heavily processed oat-derived ingredients). Detection quality depends on ingredient taxonomy completeness. The quantitative check (protein fraction plausibility) provides a backstop against this gaming path.

**Explainability quality: High**  
"The primary ingredients in this product are whole or minimally processed foods, retaining their natural food structure." This is communicable to a consumer without technical jargon.

**Relationship to NOVA:**  
Correlated but not identical. NOVA 1–2 products tend to have intact primary matrices; NOVA 4 products tend not to. But NOVA 2 pressed oils have low matrix integrity despite the clean NOVA score; some NOVA 3 fermented products have high matrix integrity despite the processing classification. The signal adds information that NOVA does not capture.

**Relationship to current architecture:**  
Currently no signal captures this. `whole_food_integrity` partially proxies it via NOVA, but is a re-encoding rather than an independent assessment. `intact_matrix_primary` would be the first genuinely independent matrix signal.

**Priority: High** — This is the most foundational positive structural signal. It is also the most demanding to implement, requiring ingredient taxonomy development.

---

### `structural_fiber_presence`

**Conceptual definition:**  
Fiber detected in the product is present as a natural component of the primary ingredient structure, not as an isolated additive from an external source.

**Why it matters:**  
Fiber in its natural matrix context (grain cell walls, legume seed coats, vegetable cell structures) is consumed with its natural co-factors: vitamins, minerals, polyphenols, and other fiber types that interact with it. Isolated fiber (chicory inulin, wheat bran extract, pea fiber isolate) provides gram quantity without structural context. The glycemic, satiety, and microbial benefits of fiber differ substantially by fiber form and source.

**Detection approach:**  
Two-level detection:
1. **Positive signal:** Primary ingredients are known high-fiber whole foods (oats, legumes, vegetables, nuts, whole grains) and the declared fiber amount is plausible for those ingredients
2. **Suppression:** Isolated fiber sources present in the ingredient list (inulin, chicory root fiber, FOS, fructooligosaccharides, wheat fiber isolate, psyllium husk added as an additive)

When isolated fiber is present, it should be identified and its gram contribution tracked separately (if estimable from ingredient position) from the structural fiber estimate.

**Gaming risk: Medium-high**  
Isolated fiber can be added without detection if labeled ambiguously ("fiber" without source specification, "dietary fiber from chicory" which could be misread as less processed than it is). The gaming path is well-established in the industry. Counter: isolated fiber at high doses causes digestive discomfort that limits real-world deployment; the plausibility check (does declared fiber make sense from declared ingredients?) provides partial defense.

**Explainability quality: High**  
"This product's fiber comes from the natural structure of its main ingredients" vs. "This product's fiber is an added extract from a different food plant." Both are communicable.

**Relationship to NOVA:**  
Moderate correlation — NOVA 4 products often have added isolated fiber. NOVA 1–2 products almost never do. But NOVA 3 products show high variance: some are whole-grain–forward with natural fiber; others are engineered with added inulin. The signal distinguishes within NOVA 3 in a way NOVA cannot.

**Relationship to current architecture:**  
Currently undetected. The `dietary_fiber_g` is observed in L1; the source type is not classified. This signal requires new L3 ingredient detection work.

**Priority: High** — One of the most immediately gaming-resistant signals and one of the most commonly abused in the snack food industry. Implementation requires only ingredient detection additions, not formula changes.

---

### `source_quality_protein`

**Conceptual definition:**  
Protein in the product comes predominantly from whole or minimally processed food sources — whole legumes, nuts, dairy, eggs, fish — rather than from protein isolates or concentrates designed to boost protein grams without structural context.

**Why it matters:**  
Whole-food protein arrives with structural co-factors that affect satiety, digestibility, and bioavailability. Protein isolates deliver the macronutrient quantity without this context. The protein score improvement achievable from isolates is not nutritionally equivalent to the same protein from whole foods.

**Detection approach:**  
Two-layer:
1. **L3 detection of protein source type:** Extend current `protein_source` classification to distinguish: whole_food / concentrate / isolate / hydrolysate / unknown
2. **Plausibility check:** If declared protein quantity exceeds what declared whole-food ingredients could reasonably deliver (~35% of calories as ceiling for whole-food sources), flag as likely isolate-supplemented regardless of label

**Gaming risk: Medium**  
Clean-label engineering (using less transparently-labeled isolates, or blend labeling that obscures the isolate fraction) is the primary vector. The plausibility check partially mitigates this. Full mitigation requires regulatory label transparency beyond what BSIP2 can enforce unilaterally.

**Explainability quality: High**  
"This product's protein comes from whole food sources" is immediately understood. "This product uses protein isolates" is also understood, and is not inherently negative — it is a structural quality distinction, not a moral judgment.

**Relationship to NOVA:**  
Moderate correlation — NOVA 4 products often use isolates; NOVA 1–2 never do. NOVA 3 shows variance. This signal adds discrimination within NOVA 3 (and sometimes between NOVA 2 products).

**Relationship to current architecture:**  
`protein_source` in L3 is a prototype. Extension is the required step. The `protein_quality` dimension already uses a quality factor; `source_quality_protein` at L3 would make the detection more granular.

**Priority: High** — Directly addresses the satiety gaming problem identified in the diagnostic. Moderately complex to implement due to ingredient taxonomy.

---

### `low_reconstruction_intensity`

**Conceptual definition:**  
The product does not require industrial reconstruction processes — fractional extraction, matrix recombination, emulsification engineering, or similar — to achieve its declared nutritional profile. Its macros are explainable from its ingredient composition without assuming reconstruction.

**Why it matters:**  
Reconstruction is the mechanism by which engineered foods simulate whole-food nutritional profiles while lacking food matrix integrity. A low reconstruction product is one where the ingredients directly produce the nutritional outcome — no hidden processing steps required to create the appearance of structural quality.

**Detection approach:**  
This is a compound L4 inference — it combines:
- Fragmentation level of primary ingredients (from ingredient taxonomy)
- Macro coherence signals (does the nutritional profile make sense for these ingredients?)
- Additive system complexity (high additive count often correlates with reconstruction)

Products with primary ingredients at fragmentation Level 0–2, coherent macro profiles, and low additive count have low reconstruction intensity. Products requiring isolates + isolated fiber + emulsifiers + texturizers to produce their claimed nutritional profile have high reconstruction intensity.

**Gaming risk: Low**  
This is a compound signal — it is harder to game simultaneously than any individual signal. A manufacturer would need to: use clean-sounding ingredients, maintain plausible macro coherence, AND avoid additive complexity, AND have structural fiber, AND have whole-food protein. Optimizing all these simultaneously while maintaining engineered nutritional targets is substantially more difficult than optimizing any one.

**Explainability quality: Medium**  
The concept is clear but the language requires care. "This product achieves its nutritional profile through whole-food ingredients without industrial reconstruction" is accurate but somewhat technical. The consumer-facing version would be simpler.

**Relationship to NOVA:**  
Strong correlation — NOVA 4 products are by definition high-reconstruction; NOVA 1 products are by definition low-reconstruction. The value is in NOVA 2–3 discrimination, where reconstruction intensity varies substantially.

**Relationship to current architecture:**  
Currently not assessed. This is a new L4 interpretation that synthesizes several L3 signals. It is the most sophisticated positive structural signal and the most important one for anti-gaming.

**Priority: Medium-high** — The most gaming-resistant signal, but also the most demanding to implement. Depends on prior implementation of ingredient fragmentation taxonomy and macro coherence signals.

---

### `fermentation_credit`

**Conceptual definition:**  
The product has undergone fermentation by microbial or enzymatic activity in a form that enhances the food's structural and nutritional properties — distinct from adding "vinegar" or "citric acid" (which are fermentation products but not structural fermentation).

**Why it matters:**  
Fermentation is the paradigm case of beneficial processing that BSIP2 currently handles correctly (it doesn't penalize yogurt) but doesn't credit positively. Fermentation-specific benefits — phytate reduction, protein digestibility improvement, probiotic presence, organic acid and SCFA precursor production — are structural nutritional positives that a detection system could capture.

**Detection approach:**  
Ingredient signal detection in L3:
- "Live cultures," "active cultures," "cultured [dairy product]" → positive fermentation signal
- "Yeast," "sourdough starter," "levain" → grain fermentation signal (with distinction between traditional sourdough and commercial yeast)
- "Miso," "tempeh," "kimchi," "kefir" → whole-product fermentation declarations
- "Vinegar," "citric acid," "lactic acid" as standalone additives → NOT fermentation credit (these are fermentation-derived additives, not structural fermentation)

The distinction between structural fermentation (transforming the food matrix) and additive use of fermentation byproducts is essential.

**Gaming risk: Low**  
Declaring "live cultures" without actual live cultures is a regulatory fraud, not a BSIP2 gaming problem. The fermentation label is commercially meaningful enough that false declaration would attract regulatory attention. This is one of the most robust positive signals.

**Explainability quality: Very high**  
Fermentation is a well-understood concept with strong consumer association with health benefits (yogurt, kefir, kimchi). The credit is immediately communicable.

**Relationship to NOVA:**  
Fermented whole foods are NOVA 1–2; some processed fermented products (flavored yogurt, fortified kefir) are NOVA 2–3. The signal is not NOVA-redundant for NOVA 2–3 fermented products where the NOVA classification adds processing concern that the fermentation signal would partially offset.

**Relationship to current architecture:**  
Currently no fermentation credit exists. The `beneficial_processing.md` document discusses this as a future direction. A fermentation signal in L3 that activates a modest structural positive in scoring is the natural implementation.

**Priority: Medium** — Implementable relatively easily; clear gaming resistance; limited population in current dataset (the 53-product batch has limited fermented product representation). High priority for future dataset expansion.

---

### `ingredient_simplicity_positive`

**Conceptual definition:**  
The ingredient list is short, contains recognizable whole-food sources in primary positions, and does not require processed additives to maintain structure, palatability, or shelf life.

**Why it matters:**  
A short ingredient list of recognizable foods is a strong proxy for low reconstruction intensity. Products that cannot be made without complex additive systems — emulsifiers to prevent separation, hydrocolloids for texture, preservatives for shelf life, flavor compounds for palatability — are inherently more reconstructed than products stable with minimal additives. The BSIP2 additive quality dimension currently penalizes additive presence; ingredient simplicity is the complementary positive.

**Critical distinction from additive_quality:**  
`additive_quality` starts at 100 and subtracts penalties for additive presence. `ingredient_simplicity_positive` starts from zero and adds positive signal for whole-food simplicity. A product with 3 ingredients (all additives) scores well on additive_quality (low additive count) but should not score well on ingredient simplicity. The signals are complementary, not redundant.

**Detection approach:**  
1. Total ingredient count (short = positive, but not sufficient alone)
2. Fraction of primary ingredients at fragmentation Level 0–2 (whole or minimally processed)
3. Absence of structural engineering additives (emulsifiers, hydrocolloids, modified starches, flavor compounds) in top-5 positions
4. Recognizability: primary ingredients are named whole foods, not chemical compounds or obscured-processing terms

**Gaming risk: High**  
Short clean ingredient lists are achievable without matrix integrity — 3 ingredients of palm oil, sugar, and cocoa butter is a very short list of recognizable-sounding ingredients that describes a highly engineered product. This signal must not operate independently of fragmentation level and macro coherence. It is a supporting signal, not a primary one.

**Explainability quality: Very high**  
"This product has a simple ingredient list of recognizable foods" is immediately communicable and commercially resonant.

**Relationship to NOVA:**  
Moderate correlation. NOVA 2 products tend toward shorter ingredient lists. NOVA 4 products tend toward longer ones. But length alone is not NOVA-discriminating.

**Relationship to current architecture:**  
The `additive_quality` dimension is the negative-direction equivalent. The LONG_INGREDIENT_LIST penalty (4 pts in the processing_load family) is a weak version of this signal applied in the penalty direction. Ingredient simplicity as a positive is the complement.

**Priority: Medium** — Easily computed from ingredient count; meaningful signal with known limitations; must be combined with other signals to be robust. Relatively low implementation cost.

---

## L4 Candidate Signals (composite interpretations)

---

### `macro_coherence_index`

**Conceptual definition:**  
A composite inference from multiple macro signals (fiber/sugar ratio, protein fraction plausibility, fat composition consistency, calorie density context) that assesses whether the product's nutritional profile is consistent with what its declared ingredients could naturally produce.

**Why it matters:**  
This is the broadest single test for macro engineering. It captures what no individual signal captures alone — the overall coherence between the ingredient declaration and the nutritional reality.

**Detection approach:**  
Synthesizes the five coherence signals from `macro_coherence_framework.md`:
1. Fiber/sugar ratio (computed from L1 data)
2. Protein fraction plausibility (computed from L1 data)
3. Fat composition fingerprint (L1 + L3 fat source detection)
4. Calorie density in ingredient context (L1 + L3 ingredient detection)
5. Macro disproportion flag (L4 synthesis)

**Gaming risk: Low**  
The compound nature of this signal makes it substantially more resistant to gaming than any individual signal. Simultaneously achieving: plausible protein fraction, good fiber/sugar ratio from structural sources, coherent fat composition, and non-extreme macro disproportion — while maintaining engineered nutritional targets — is difficult without genuinely whole-food ingredients.

**Explainability quality: Medium**  
The composite nature makes it harder to explain than individual signals. "This product's nutritional profile is consistent with its declared ingredients" is accurate but abstract. Decomposing the explanation into the failed signals (e.g., "protein level exceeds what oats and nuts could provide") is more actionable.

**Relationship to NOVA:**  
Partially independent. NOVA 3 products show wide variance on this signal — exactly where the discrimination value lies.

**Priority: High** — The most gaming-resistant compound signal. Priority 1 for L4 implementation once L3 signals are sufficiently developed.

---

### `structural_satiety_quality`

**Conceptual definition:**  
A composite inference from protein source quality, fiber structural context, physical form, and matrix coherence that assesses whether the product's satiety properties arise from food structure or from engineered macronutrient density.

**Why it matters:**  
This replaces the current `satiety_support` dimension with a structurally grounded equivalent. It is the L4 interpretation of the source-aware satiety framework.

**Detection approach:**  
Synthesizes:
- `source_quality_protein` (L3) — protein quality factor
- `structural_fiber_presence` (L3) — fiber context factor
- Physical form inference from category and product description (L3)
- Matrix coherence bonus (whether protein and fiber co-occur from same source)

**Gaming risk: Low-medium**  
More gaming resistant than the current formula due to the quality factors. The remaining gaming paths (adding high-quality protein isolates, adding diverse fiber sources to activate coherence) are more expensive and technically challenging than simply adding cheap whey isolate + chicory.

**Priority: High** — Direct replacement for current satiety_support dimension's worst failure mode.

---

## Signal relationship matrix

| Signal | Independent of NOVA | Hard to game individually | Computable from current L1/L3 data |
|---|---|---|---|
| `intact_matrix_primary` | Yes (substantial) | Medium | No — needs ingredient taxonomy |
| `structural_fiber_presence` | Yes | Medium-high | No — needs fiber source detection |
| `source_quality_protein` | Yes (within NOVA 3) | Medium | Partial — `protein_source` exists |
| `low_reconstruction_intensity` | Yes | Low (compound) | No — needs L3 synthesis |
| `fermentation_credit` | Yes | Low (regulatory backstop) | Partial — needs label term detection |
| `ingredient_simplicity_positive` | Moderate | High risk alone | Yes — ingredient count available |
| `macro_coherence_index` | Yes | Low (compound) | Partial — ratio computable, source detection needed |
| `structural_satiety_quality` | Yes (within NOVA 3) | Low-medium | Partial — protein_source partial; fiber source needed |

---

## Implementation sequencing recommendation

**Phase 1 (requires only L1 data and existing L3 signals):**
- `fermentation_credit` — label term detection addition to L3
- `ingredient_simplicity_positive` — ingredient count + additive pattern detection
- `macro_coherence_index` partial — fiber/sugar ratio and protein fraction plausibility (fully computable from L1)

**Phase 2 (requires ingredient taxonomy development):**
- `structural_fiber_presence` — fiber source type detection
- `source_quality_protein` — extend protein_source classification
- `macro_coherence_index` full — add fat composition and ingredient-calorie coherence

**Phase 3 (requires Phase 2 completion + synthesis layer):**
- `intact_matrix_primary` — compound ingredient assessment
- `low_reconstruction_intensity` — compound L4 inference
- `structural_satiety_quality` — replaces satiety_support dimension

**The Phase 1 signals are meaningful even without Phase 2.** A fermentation credit and a macro coherence partial signal (fiber/sugar + protein plausibility) would immediately improve architectural symmetry without requiring full ingredient taxonomy development.
