# Signal Taxonomy

**Purpose:** Create explicit separation between the six distinct types of signals that BSIP2 processes. Mixing these layers — using an interpreted concern as if it were an observed fact, or presenting a normative judgement as if it were a derived metric — is the primary source of analytical incoherence and explainability failure.

Every signal in BSIP2 belongs to exactly one layer. Understanding which layer a signal belongs to determines how certain it is, how it should be communicated, what can cause it to change, and how it should be treated if the underlying science is revised.

---

## The six signal layers

| Layer | Type | Definition | Certainty | Can be revised by |
|-------|------|------------|-----------|------------------|
| L1 | Observed fact | Declared or directly measured values from the product record | Highest — data error or fraud aside | Better source data; retailer correction |
| L2 | Derived metric | Values computed deterministically from L1 inputs | Same as L1 — deterministic | Change to L1 inputs |
| L3 | Inferred classification | Category or class assigned by inference from L1/L2 signals | Moderate — inference confidence varies | Improved classification algorithm; new signals |
| L4 | Interpreted concern | A rule or threshold applied to L1–L3 signals to identify a structural concern | Moderate — threshold values are experimental | Threshold recalibration; concern family redesign |
| L5 | Behavioral hypothesis | An assumption about how humans respond to a product's structural properties | Lower — grounded in population science, not individual data | Scientific literature; population studies |
| L6 | Normative judgement | A value decision embedded in the scoring architecture about what constitutes good or poor food quality | Lowest in terms of scientific certainty — philosophical | Explicit design review; community standard revision |

---

## Layer 1 — Observed Facts

**Definition:** Values that come directly from the product data record as declared by the manufacturer, recorded by the retailer, or measured by a regulatory body. They are treated as ground truth for the analytical session, subject to confidence scoring if suspicious.

**Examples:**
- `energy_kcal: 480` — declared calorie value per 100g
- `protein: 12.3` — declared protein per 100g
- `sugar: 18.5` — declared sugar per 100g
- `sodium: 720` — declared sodium per 100g
- `ingredient_text: "oats, dates, almonds, cocoa"` — declared ingredient list
- `barcode: 7290107646154` — product identifier
- `israeli_red_labels: ["sugar"]` — regulatory label as applied to the product

**Characteristics:**
- BSIP2 does not derive these values; it receives them
- They can be wrong (labelling errors, OCR corruption, unit confusion) — this is why confidence scoring exists
- When suspicious (sugar > carbohydrates; energy outside physiological range), confidence is reduced, not the value itself
- The raw value is stored in the compact product record; it is never modified by the scoring engine

**Why layer separation matters here:** Downstream signals are derived from or depend on L1 values. If an L1 value is wrong and the error is not detected, all derived signals built on it will also be wrong. Distinguishing L1 as the ground truth layer makes it clear where data quality problems originate and where they can be corrected.

---

## Layer 2 — Derived Metrics

**Definition:** Values computed deterministically from one or more L1 inputs. Given the same L1 inputs, the same derived metric will always result. No inference or judgment is involved.

**Examples:**
- `energy_kj_derived: 2007.3` — computed from `energy_kcal × 4.184` (stored in audit only)
- `fat_from_kcal_pct: 42.2` — fat contribution as percentage of total calories
- `protein_per_kcal: 0.026` — protein density per calorie
- `sugar_to_carb_ratio: 0.71` — ratio used for data consistency check
- `saturation_fraction: 0.58` — saturated fat as fraction of total fat
- `ingredient_count: 14` — count of distinct ingredients in parsed ingredient list
- `additive_marker_count: 4` — count of detected additive markers in ingredient text

**Characteristics:**
- Derived metrics inherit the certainty of their L1 inputs
- They can be computed fresh at any time from the same L1 inputs
- They may be stored for efficiency but are not analytically distinct from re-computation
- A change to a derived metric formula (e.g. a new kcal-to-kJ conversion constant) requires recomputation for all products, not data collection

**Why layer separation matters here:** A derived metric like `fat_from_kcal_pct` feels like a fact, but it is not — it is a computation. If the input values are wrong, the derived metric is wrong. If the formula is revised, historical derived metrics may become inconsistent with current ones. Explicitly labeling derived metrics as L2 signals prevents them from being treated as source-of-truth data.

---

## Layer 3 — Inferred Classifications

**Definition:** Categories or classes assigned to a product through inference from L1 and L2 signals. Unlike derived metrics, inferred classifications involve a judgment step: a mapping from continuous or multi-dimensional input space to a discrete output category.

**Examples:**
- `category: snack_bar_granola` — assigned through name matching, ingredient signals, retailer classification
- `nova_level: 4` — inferred from ingredient marker presence (NOVA proxy)
- `nova_classification_confidence: 0.73` — confidence in the NOVA assignment
- `category_confidence: 0.81` — confidence in the category assignment
- `hp_pattern_detected: [fat_sugar, crunch_sweet]` — hyper-palatability pattern inference from compositional signals
- `protein_source: whole_food | isolate` — classification of protein sourcing context

**Characteristics:**
- Inferred classifications carry explicit confidence scores (where possible)
- The same L1 data can produce a different classification if the classification algorithm changes — this is fundamentally different from derived metrics
- Classification confidence propagates into analytical confidence (L4, L5 signals that depend on L3 outputs are less certain when L3 confidence is low)
- Inferred classifications are the layer most vulnerable to edge-case failure (see `classification_instability.md`)

**Why layer separation matters here:** The most consequential classification errors in BSIP2 — a whole-food bar classified as `snack_bar_granola`, a NOVA 2 product classified as NOVA 4 — come from this layer. Explicitly treating L3 signals as inferences with confidence rather than facts forces the system to propagate uncertainty correctly. A rule that fires on an L3 signal with 60% confidence is a different analytical claim than one that fires on an L1 signal.

---

## Layer 4 — Interpreted Concerns

**Definition:** Rules and thresholds that transform L1–L3 signals into concern signals — cap or penalty activations that represent the scoring engine's analytical judgment about whether a specific structural property rises to the level of a scoring concern.

**Examples:**
- `HIGH_SUGAR_25G_PLUS fires: true` — L1 sugar value of 28g exceeds the 25g threshold; a concern is activated
- `NOVA_PROXY_4_ULTRA_PROCESSED fires: true` — L3 NOVA classification of 4 activates the cap rule
- `HIGH_CAL_HIGH_SUGAR_SEVERE fires: false` — L1 kcal is 480, which is below the 500 threshold; the concern does not fire
- `SWEETENER_PRESENT fires: true` — L1/L2 ingredient analysis detected a sweetener marker
- Cap value applied: 60 — the resolved cap value after concern coordination

**Characteristics:**
- Interpreted concerns are binary (fire / not fire) for caps; the threshold defines the boundary
- Threshold values in L4 are experimental and subject to calibration — they are not scientific constants
- The concern coordination system operates entirely at this layer (resolving which caps and penalties survive when multiple rules fire)
- Family budget clamping operates at this layer
- L4 signals are the primary source of cliff-threshold behaviour

**Why layer separation matters here:** An interpreted concern is not a fact and not a classification — it is a scored judgment. When a user sees a score reduced by a sugar cap, they are experiencing an L4 signal: the analytical engine has judged that 28g of sugar per 100g represents a structural concern of sufficient magnitude to impose a cap at 60. That judgment is legitimate, but it is a judgment — based on thresholds that are experimental and calibrated by design.

Mixing L4 signals with L1 signals in explanations produces language like "this product has too much sugar" — which sounds like a factual statement but is actually an interpreted concern. The correct explanation is "this product exceeds the sugar concentration threshold above which Bari applies a structural scoring constraint." This is less convenient but more honest.

---

## Layer 5 — Behavioral Hypotheses

**Definition:** Assumptions embedded in the scoring architecture about how humans respond to specific structural properties of food. These are grounded in nutritional science and epidemiology, but they are population-level hypotheses, not individual facts.

**Examples:**
- The hyper-palatability patterns assume that specific fat-sugar-sodium combinations override normal appetite regulation in a population sense
- The low-satiety rules assume that high-calorie-low-protein-low-fiber products produce less satiation than high-calorie products with protein and fiber
- The calorie density dimension assumes that higher calorie density produces less satiation per gram in most consumption contexts
- The NOVA penalty assumes that ultra-processed foods, as a population-level category, are associated with poorer health outcomes

**Characteristics:**
- Behavioral hypotheses are not falsified by individual exceptions — a person who is sated by a highly processed snack does not disprove the population hypothesis
- They can be revised when scientific evidence changes — if the evidence base for hyper-palatability patterns shifts, the corresponding scoring mechanism should be revisited
- They are the layer most vulnerable to scientific revision and ideological drift
- BSIP2 should not claim that these are established scientific facts for individual products; they are population-level risk patterns

**Why layer separation matters here:** The most significant risk of the behavioral hypothesis layer is that hypotheses calcify into assumed facts. If BSIP2 treats the assumption that "fat-sugar combinations override appetite regulation" as an established truth rather than a population-level pattern, it will resist revision when evidence is mixed — and will communicate to users a certainty it does not have.

Explicit L5 labeling provides a mechanism for future review: "all behavioral hypotheses in the system should be audited against current scientific evidence on a defined schedule."

---

## Layer 6 — Normative Judgements

**Definition:** Value decisions embedded in the architecture about what constitutes quality, concerning, or good food. These are philosophical positions, not analytical conclusions. They cannot be falsified by data.

**Examples:**
- The decision that sweetener substitution is not equivalent to quality improvement — a product with 2g sugar and acesulfame K should not score higher than one with 10g natural sugar and no sweetener
- The decision that NOVA 4 processing represents a structural quality concern regardless of macronutrient profile
- The decision that protein from isolates is analytically different from protein in a whole-food matrix
- The decision that fortification with vitamins post-processing does not credit the product's analytical quality
- The whole-food floor: a minimum score for single-ingredient NOVA 1 products regardless of other signals

**Characteristics:**
- Normative judgements are stable by design — they represent architectural commitments
- They can be revised, but only through explicit design review, not through data analysis
- They should be documented as normative judgements, not presented as analytical conclusions
- If a stakeholder disagrees with a normative judgement (e.g. believes that sweetener substitution is beneficial), they are engaging with a philosophical design choice, not disputing an analytical finding

**Why layer separation matters here:** The biggest risk of the normative judgment layer is invisibility. When "NOVA 4 represents a structural quality concern" is embedded in a scoring algorithm without being labeled as a normative position, it appears to be an analytical finding. Users who dispute it are told "this is what the data shows" — when in fact the data shows processing signals, and the normative judgment converts that into a quality concern.

Making L6 signals explicit does not weaken the architecture. It makes the architecture honest about what it is doing and allows the normative positions to be reviewed and defended rather than silently embedded.

---

## Why mixing layers is dangerous

**Mixing L1 and L4 in explanations** produces false precision: "this product has too much sugar" (sounds like a fact) rather than "this product's sugar concentration exceeds the threshold above which Bari applies a structural cap" (identifies the interpreted concern correctly).

**Mixing L3 and L1 in the scoring engine** produces confidence inflation: applying rules designed for high-confidence L1 inputs to L3 inferences without propagating the L3 confidence penalty.

**Mixing L5 and L1 in communications** produces unwarranted authority: "this product will drive overconsumption" (sounds like a prediction about this consumer's behavior) rather than "this product matches compositional patterns associated with appetite dysregulation in population studies."

**Mixing L6 and L2 in architecture** produces invisible ideology: a normative position about what food should be is operationalized as a derived metric, and anyone who disputes the result is told they are disputing the math.

---

## Implications for explainability

Every score explanation should be traceable to a specific layer. The UI explanation should identify:
- Which L1 facts drove the score
- Which L3 inferences were used and with what confidence
- Which L4 concern rules fired and at what threshold
- Which L5/L6 positions are embedded in those rules

A score that can only be explained by reference to all six layers simultaneously is too complex to explain at the UI level. This defines the explainability budget: the dominant driver of the score should be identifiable, and it should belong to at most two or three signal layers.

---

## Implications for future ML systems

If BSIP2 is ever partially replaced or augmented by a machine learning component, the signal taxonomy becomes critical:
- ML models trained on L1 inputs and L4 concern labels will learn the embedded L6 normative positions as if they were ground truth
- ML predictions cannot distinguish between "this product scored low because of objective structural properties" and "this product scored low because of a normative design choice"
- The signal taxonomy provides the vocabulary for correctly labeling training data: L1 inputs, L3 targets (for classification), L4 outputs (for rule prediction), with L5/L6 positions documented as the normative frame

---

## Implications for scientific revision

When the scientific literature evolves — better evidence on hyper-palatability, revised understanding of fiber types, new evidence on sweetener safety — the signal taxonomy determines what needs to change:
- A revision to an L5 behavioral hypothesis may require redesigning the corresponding L4 concern rules
- A revision to an L3 classification algorithm (better NOVA proxy inference) requires recalculating all L4 downstream signals for affected products
- A revision to an L6 normative judgement (e.g. if the position on sweeteners changes) is a design review decision, not a recalibration

Without the taxonomy, "update the scoring for new evidence" is ambiguous. With the taxonomy, the update target is specific.
