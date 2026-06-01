# UI Language Guide

## The design principle

Every piece of language the Bari interface uses to describe a product should be grounded in a specific analytical signal — not marketing copy, not algorithmic generalities, and not health advice.

The system produces precise, traceable results. The UI language should be equally precise. If a product triggers a fat-sugar hyper-palatability pattern, the interface says something specific about that. It does not say "this product may not be the best choice."

---

## Grade language

Grades (A–E) require framing that communicates analytical position without moral judgement.

**Recommended:**
- "Strong nutritional structure" (A)
- "Good overall profile" (B)
- "Some areas of concern" (C)
- "Notable structural concerns" (D)
- "Significant analytical concerns" (E)

**Avoid:**
- "Healthy" / "Unhealthy" (binary and value-laden)
- "Clean" / "Dirty" (not an analytical concept)
- "Good for you" / "Bad for you" (personalised health advice, which Bari does not give)
- "Approved" / "Not approved" (suggests certification that doesn't exist)
- "Natural" (not defined; not used in the analysis)

---

## Score explanations — positive signals

When a product has clear positive signals, name them specifically.

| Signal | UI language |
|--------|-------------|
| High protein from whole food sources | "High protein — whole food source" |
| High fiber content | "Good fiber content" or "Fiber-rich" |
| Minimal ingredient list (≤ 8 ingredients) | "Simple ingredient list" |
| NOVA 1 classification | "Minimally processed" |
| No red labels | "No regulatory warnings" |
| Confirmed per-100g nutrition basis | (no note needed — this is baseline) |
| Nuts/seeds as primary ingredient | "Whole food fat source" |
| Whole grains present | "Contains whole grain" |
| No hyper-palatability patterns triggered | (no note needed — absence of concern is not a feature) |

---

## Score explanations — negative signals

When a product has concerns, name the signal precisely. Avoid vague language that gestures at a problem without identifying it.

| Signal | UI language |
|--------|-------------|
| NOVA 4 classification | "Ultra-processed" |
| NOVA 3 classification | "Processed" |
| Red label — sugar | "Israeli red label: sugar" |
| Red label — sodium | "Israeli red label: sodium" |
| Red label — saturated fat | "Israeli red label: saturated fat" |
| 2+ red labels | "Multiple regulatory warnings" |
| Sweetener present | "Contains non-nutritive sweetener" |
| High additive burden (3–4 markers) | "High additive complexity" |
| High additive burden (5+ markers) | "Very high additive complexity" |
| Hyper-palatability: fat-sugar pattern | "Engineered fat-sugar combination" |
| Hyper-palatability: fat-sodium pattern | "High fat-sodium concentration" |
| Hyper-palatability: refined carb + fat | "Refined carb and fat combination" |
| Hyper-palatability: crunch-sweet pattern | "High sugar, low fiber cereal pattern" |
| Glucose syrup or maltodextrin present | "Contains refined starch derivative" |
| Trans fat (veto triggered) | "Contains trans fat" |
| Long ingredient list (>12) | "Complex ingredient list" |
| Multiple added sugar sources | "Multiple added sugar sources" |
| Protein from isolate (not whole food) | "Protein from isolate" |
| Reconstructed protein in a bar format (TASK-133B) | "Protein from a reconstructed source" |
| Collagen protein (TASK-133B) | "Collagen — incomplete protein profile" |
| Concern emulsifier — carrageenan / CMC / polysorbate-80 (TASK-133C) | "Contains a high-load emulsifier" |
| BHA preservative present (TASK-133D) | "Contains BHA (preservative under review)" |
| Calorie density high for category | "High calorie density for [category]" |
| High sugar + high calories (combined) | "High calorie, high sugar combination" |
| Low satiety signals (low protein + fiber) | "Low satiety signals" |
| Missing ingredient data | "Ingredient data unavailable" |

---

## Category labels

When displaying a product, always show its category classification alongside its grade.

| Category | Display label |
|----------|--------------|
| `whole_food_fat` | "Nut & seed products" |
| `snack_bar_granola` | "Bars & granola" |
| `dessert` | "Desserts & confectionery" |
| `beverage` | "Beverages" |
| `dairy_protein` | "Dairy & protein" |
| `cereal` | "Breakfast cereals" |
| `sauce_spread` | "Spreads & condiments" |
| `default` | "General food" |

---

## Confidence language

Confidence affects how results should be framed, not just whether to display a score.

| Band | UI approach |
|------|-------------|
| High (80–100) | Display score and grade without qualification |
| Medium (60–79) | Display score and grade with a brief note: "Based on available data" |
| Low (40–59) | Display score with explicit caveat: "Some nutrition data missing — result is an estimate" |
| Insufficient (< 40) | Do not lead with the score. Surface the data gap: "Not enough information to assess this product reliably" |

Do not display a grade without surfacing confidence level when confidence is medium or lower.

---

## Tradeoff language

Some products have genuine tradeoffs that the UI should acknowledge rather than collapse into a single verdict.

**Example pattern:** A protein bar with high protein content but protein from isolates and a sweetener.

Avoid: "High protein snack with some concerns."

Better: "High protein content from isolate. Contains non-nutritive sweetener. Hard cap applied."

**Example pattern:** A nut butter with high calorie density that scores well.

Avoid: "Good choice despite high calories."

Better: "Whole food fat source. High calorie density evaluated against nut product thresholds."

The language explains the analysis. It does not perform reassurance.

---

## Language that does not belong in Bari

| What not to say | Why |
|----------------|-----|
| "Superfoods" | Not an analytical category |
| "Clean eating" | Not defined in the analysis |
| "Guilt-free" | Moralises food choice |
| "Detox" | No analytical basis |
| "Boosts immunity" / "Supports [organ]" | Health claims Bari does not make |
| "AI-powered analysis" | Technically inaccurate (deterministic rule engine, not ML); also unnecessary |
| "Our algorithm thinks..." | Not the right framing — signals are specific and can be named |
| "Better for you" | Personalised comparison Bari does not make |
| "Nutritionist approved" | Not a claim Bari makes |

---

## Hyper-palatability — framing guidance

Hyper-palatability is analytically precise but requires care in the UI. The term itself should generally not appear in consumer-facing language — it describes a structural property of a product's composition, not a quality judgement about the product or the consumer.

Recommended consumer framing:

| Pattern | Consumer-facing description |
|---------|---------------------------|
| Fat-sugar | "This product combines high fat and high sugar — a pattern associated with engineered taste reward" |
| Fat-sodium | "High fat and sodium concentration" |
| Refined carb + fat | "Low-fiber refined grain and fat combination" |
| Crunch-sweet | "High sugar, low fiber cereal structure" |

The UI can surface these as named concern signals without using the clinical terminology.

---

## Displaying the dimension breakdown

When showing dimension scores, use precise labels — not interpretive descriptions.

| Dimension | Display label |
|-----------|--------------|
| Processing Quality | "Processing" |
| Nutrient Density | "Nutrient density" |
| Calorie Density Quality | "Calorie density" |
| Glycemic Quality | "Glycemic quality" |
| Protein Quality | "Protein" |
| Additive Quality | "Additives" |
| Satiety Support | "Satiety" |
| Fat Quality | "Fat quality" |
| Regulatory Quality | "Regulatory signals" |
| Whole Food Integrity | "Whole food character" |

Dimension scores are 0–100. A dimension score below 40 is a meaningful concern. A dimension score above 70 is a meaningful strength. The gap between the weakest and strongest dimension tells the user something specific about where the product's profile is uneven.

---

## Tone

Bari's analytical voice is:
- **Precise** — grounded in specific signals
- **Direct** — states what is, not what might be
- **Neutral** — doesn't moralize, doesn't celebrate
- **Informative** — the user leaves with more understanding than they arrived with

It is not:
- Reassuring (food choice is personal; Bari informs, it does not comfort)
- Alarming (concern signals are presented proportionately)
- Promotional (even for products that score well)
- Hedged into meaninglessness ("may," "possibly," "could")
