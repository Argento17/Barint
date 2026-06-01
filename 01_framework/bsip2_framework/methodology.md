# BSIP2 Analytical Methodology

## What Bari evaluates

Bari does not evaluate foods by a single nutrient or a simple checklist. It evaluates the **nutritional architecture** of a product — how its composition functions together — and produces a score that reflects genuine food quality relative to what that product is.

The system is deterministic: the same product data always produces the same score. Every component of the score is traceable to the input signals that triggered it.

---

## The scoring pipeline

A product moves through six stages before a final score is assigned.

### Stage 1 — Feature extraction

Raw product data (nutrition panel, ingredient list, category, regulatory labels) is parsed into a structured set of over 50 analytical features. These include direct nutritional values, derived ratios, ingredient presence markers, regulatory flags, and inferred food classification signals.

Nothing is imputed or assumed. If a field is missing, the system records the absence and adjusts confidence accordingly.

### Stage 2 — Dimension scoring

Ten independent analytical dimensions are each scored 0–100. Each dimension examines a distinct aspect of the product's nutritional character. They are scored independently before being combined, so strengths and weaknesses in each dimension remain transparent.

Dimensions and their weight in the final score:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Processing Quality | 15% | Degree of industrial processing; NOVA classification; additive burden |
| Nutrient Density | 15% | Protein, fiber, and micronutrient contribution per 100g |
| Calorie Density Quality | 15% | Whether calorie content is appropriate for this product's category |
| Glycemic Quality | 12% | Sugar load and carbohydrate composition |
| Protein Quality | 10% | Protein quantity, sourcing method, and **matrix form** (a reconstructed-protein/collagen discount applies to the quality contribution in bar formats; protein *mass* is unaffected — TASK-133B) |
| Additive Quality | 10% | Presence of artificial stabilizers, emulsifiers, sweeteners; **named-additive identity** (emulsifier tiering, BHA) — TASK-133C/D |
| Fat Quality | 8% | Saturated fat proportion; fat source quality |
| Satiety Support | 6% | Whether the product's composition supports fullness (protein + fiber + food structure) |
| Regulatory Quality | 5% | Israeli red-label warnings (sugar, sodium, saturated fat) |
| Whole Food Integrity | 4% | Structural proximity to minimally processed whole food |

*(Weights re-synced to the proto_v0 engine — source-of-truth — per DEC-004 G3, 2026-06-01. The earlier 18/16/12/11/9/7/6/6/4/1 table had drifted from the running engine.)*

Hyper-Palatability (see Stage 4) is an additional signal that applies penalties across relevant dimensions rather than standing alone.

### Stage 3 — Guardrail evaluation

Before dimensions are combined, a separate guardrail layer evaluates structural concerns:

- **Veto rules** — A small set of hard disqualifiers. Trans fat above a threshold triggers an immediate score floor of 20 regardless of other signals.
- **Hard caps** — Binding upper limits on the final score, triggered by clear structural issues: NOVA 4 classification, multiple red labels, high sugar concentration, high sodium concentration, significant additive burden. When multiple caps apply, the most restrictive wins.
- **Soft penalties** — Subtractive adjustments for concerns that lower the score without hard-capping it.
- **Floors** — Minimum score protections. Single-ingredient whole foods and whole-food fat products receive score floors that prevent the system from penalizing them for attributes that are intrinsic to their category (e.g., nuts are calorie-dense by nature).

### Stage 4 — Hyper-palatability detection

A dedicated engine evaluates whether the product's nutritional architecture reflects **engineered taste reward** — combinations of fat, sugar, sodium, and refined carbohydrates that are associated with overconsumption patterns independent of nutritional value.

Four combination patterns are evaluated: fat-sodium, fat-sugar, refined carb with fat, and crunch-sweet. Each triggered combination applies a score penalty. Amplifiers (chocolate coatings, glucose syrup, emulsifiers, flavourings) increase the strength of each penalty. Food matrix factors (whole nuts, whole grains, dates) provide partial relief.

### Stage 5 — Concern coordination

Multiple analytical rules can identify the same underlying concern. The concern coordinator prevents the same root issue from penalizing the score more than once.

Concerns are grouped into families (sugar load, sodium load, processing load, fat quality, calorie load). When multiple rules within the same family fire, the system selects the primary signal and demotes the others to supporting evidence at a reduced weight. The result is a final score that reflects the real burden — not an inflated pile-up from the same concern being counted five times.

### Stage 6 — Final resolution

After dimensions, guardrails, hyper-palatability, and concern coordination are applied:

1. All caps are applied in order, with family-specific floors preventing caps from pushing scores below a reasonable minimum for that concern type.
2. All penalties are applied, with per-family budget limits preventing cumulative penalization beyond what is analytically justified.
3. Floor rules are enforced — if the score falls below the applicable floor, it is raised to the floor value.
4. A confidence ceiling is applied: products with low analytical confidence cannot receive high scores regardless of what other signals indicate.
5. The score is clamped to [0, 100].

---

## Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 85–100 | Strong across most dimensions; no significant structural concerns |
| B | 70–84 | Good overall; minor concerns in one or more dimensions |
| C | 55–69 | Meaningful concerns present; acceptable in context |
| D | 40–54 | Multiple concerns; not recommended as a regular choice |
| E | 0–39 | Significant structural issues; hard caps or veto applied |

Grades are not moral judgements. A D-grade product is not "bad food" — it is a product whose nutritional architecture places it at the lower end of the analytical range for its category and across its dimensions.

---

## What makes this different from a Nutri-Score or traffic light

**Category awareness.** Calorie density, fat content, and sugar thresholds are evaluated relative to the product's category. A nut butter is not evaluated against the same calorie benchmark as a flavoured drink.

**Whole-food protection.** Naturally calorie-dense whole foods are not penalized using thresholds built for engineered products. The system explicitly protects them with score floors and matrix relief adjustments.

**No double-counting.** Every structural concern is counted once, at its true weight, through the concern coordination layer.

**Transparent traceability.** Every score can be decomposed into the signals and rules that produced it. There are no black boxes.

**Hyper-palatability as a dimension.** The system evaluates not just what is in a product, but whether its composition pattern is characteristic of products engineered to drive consumption beyond satiety signals.

---

## Algorithm version

Current: `0.4.0`

**0.4.0** (2026-06-01, TASK-133) — Protein Quality is now matrix-aware (reconstructed-protein / collagen quality discount, bar-format gated, quality-contribution only); named-additive identity in Additive Quality (emulsifier tiering via the ingredient taxonomy; BHA named penalty, BHT differentiated); ingredient fragmentation-level signals (matrix-integrity Req 1 implemented). Dimension-weight table re-synced to the engine (DEC-004 G3). Magnitudes ratified under DEC-004.
