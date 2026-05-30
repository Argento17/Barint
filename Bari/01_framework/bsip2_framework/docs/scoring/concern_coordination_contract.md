# Concern Coordination Contract

**Purpose:** Define exactly how Bari prevents the same root concern from reducing the score more than once.

---

## The problem this solves

A product that is high in sugar may trigger five separate rules: a sugar concentration cap, a calorie-density interaction cap, a red-label cap, a multiple-added-sugars penalty, and a hyper-palatability penalty. Without coordination, all five would reduce the score independently — punishing the same underlying concern five times.

The concern coordinator is a gate between rule evaluation and score application. It inspects every cap and penalty that has fired, groups them by root concern, and enforces two decisions:

**For caps:** when multiple caps share a root concern, only the strictest (lowest value) cap survives. The others are discarded.

**For penalties:** when multiple penalties share a root concern, the largest penalty wins at full value. Every other penalty in the group is scaled down to a defined `supporting_evidence_factor` (typically 40–50% of its raw value) before being applied. They still contribute — as supporting evidence — but they cannot repeat the full weight of the primary signal.

After coordination, a separate family budget clamp limits the total penalty that can accumulate from any one concern category, regardless of how many supporting penalties survived the coordination step.

---

## How to read each section

| Field | Meaning |
|-------|---------|
| **Primary signal** | The rule that acts as the winner when this concern fires — the one whose value is used in full |
| **Supporting signals** | Rules that share this concern; after coordination, their value is scaled by the supporting factor |
| **Allowed caps** | The hard ceiling(s) that can apply; when multiple fire, only the strictest survives |
| **Allowed penalties** | The subtractive adjustments; the largest wins at full weight; others scaled down |
| **Supporting evidence factor** | The fraction applied to non-winner penalties (e.g. 0.4 means 40% of raw value) |
| **Max penalty budget** | Ceiling on the total penalty from this family, regardless of coordination outcome |
| **Cap floor** | The lowest a cap in this family can push the score — caps cannot go below this value |
| **Max total score impact** | Combined ceiling + penalty budget: the most this concern can reduce a score |

---

## Concern families

---

### Sugar Load (`SUGAR_LOAD`)

The broadest concern family. Sugar appears in multiple contexts — as a direct concentration problem, as part of a calorie-density interaction, as a red-label trigger, and as a component of hyper-palatability patterns. All of these share the same root concern.

**Primary signal (caps — strictest wins):**
- `HIGH_CAL_HIGH_SUGAR_SEVERE`: cap at **50** — triggered when kcal ≥ 500 AND sugar ≥ 25g/100g

**Other cap rules (reduced or discarded after coordination):**
- `HIGH_CAL_HIGH_SUGAR_MODERATE`: cap at **60** — kcal ≥ 470 AND sugar ≥ 20g/100g
- `HIGH_SUGAR_25G_PLUS`: cap at **60** — sugar ≥ 25g/100g
- `SNACK_BAR_HIGH_CAL_SUGAR`: cap at **60** — snack bar with kcal ≥ 470 AND sugar ≥ 15g/100g
- `SNACK_BAR_RED_SUGAR_LABEL`: cap at **55** — snack bar carrying an Israeli red-sugar label
- `ISRAELI_RED_LABEL_1` *(when red label is sugar)*: cap at **55**
- `ISRAELI_RED_LABELS_2_PLUS` *(when sugar is one of the red labels)*: cap at **45**

When multiple caps fire, only the strictest applies. A product triggering both `HIGH_CAL_HIGH_SUGAR_SEVERE` (50) and `ISRAELI_RED_LABELS_2_PLUS` (45) faces a cap at **45**, not two separate caps.

**Penalty rules (winner full value; others scaled to 40%):**
- `MULTIPLE_ADDED_SUGAR_MARKERS`: −5 — two or more distinct added-sugar sources in the ingredient list
- `HIGH_CAL_HIGH_SUGAR_SOFT`: −5 — kcal ≥ 430 AND sugar ≥ 15g/100g (softer version of the interaction rule)
- `HP_FAT_SUGAR_COMBO`: HP-engine penalty — fat-sugar hyper-palatability pattern
- `HP_CRUNCH_SWEET_COMBO`: HP-engine penalty — crunch-sweet hyper-palatability pattern

**Supporting evidence factor:** 0.4 (non-winner penalties reduced to 40%)

**Max penalty budget:** 10 points (`sugar` family)

**Cap floor:** 45 (a cap in the sugar family cannot push the score below 45)

**Max total score impact:** cap at 45 (floor-protected) + up to 10 points in penalties = **score floored at 35** in an extreme scenario

**Example — protein bar with 28g sugar, 480 kcal, and multiple sugar sources:**
- `HIGH_SUGAR_25G_PLUS` fires (cap 60); `HIGH_CAL_HIGH_SUGAR_MODERATE` fires (cap 60)
- Coordinator: both are SUGAR_LOAD, both cap at 60 → one survives, value 60
- `MULTIPLE_ADDED_SUGAR_MARKERS` fires (−5); `HIGH_CAL_HIGH_SUGAR_SOFT` fires (−5)
- Coordinator: both are SUGAR_LOAD penalties → winner (−5) at full; the other scales to −2 (5 × 0.4)
- Net: cap at 60, total penalty 7 → final score ≤ 53 before other rules

---

### Calorie Load (`CALORIE_LOAD`)

Evaluates whether a product delivers high calories without the structural properties that justify them — primarily protein and fiber. Distinct from sugar load, though the two can co-occur.

**Primary signal (caps — strictest wins):**
- `HIGH_CAL_LOW_SATIETY_SEVERE`: cap at **55** — kcal ≥ 500 AND protein < 6g AND fiber < 3g
- `SNACK_BAR_HIGH_CAL`: cap at **70** — snack bar with kcal ≥ 430 (the snack-bar health-halo rule)

When both fire, the stricter cap (55) wins.

**Penalty rules (winner full value; others scaled to 50%):**
- `HIGH_CAL_LOW_SATIETY_SOFT`: −6 — kcal ≥ 450 AND protein < 8g AND fiber < 5g

**Supporting evidence factor:** 0.5 (non-winner penalties reduced to 50%)

**Max penalty budget:** 8 points (`calorie_density` family)

**Cap floor:** 55 (a calorie-load cap cannot push the score below 55)

**Max total score impact:** cap at 55 + up to 8 points in penalties = **score minimum of ~47** in severe cases; the cap floor on the calorie_density family (55) limits how far the cap itself can go within this family

**Relationship to Sugar Load:** The calorie interaction rules `HIGH_CAL_HIGH_SUGAR_*` bridge both concerns. When a product triggers both a calorie-load cap and a sugar-load cap, concern coordination applies to each concern independently. The effective final score is the strictest cap that survives across all concerns.

**Example — dense cereal bar with 460 kcal, 5g protein, 2g fiber:**
- `HIGH_CAL_LOW_SATIETY_SOFT` fires (−6 penalty)
- No severe cap triggered (kcal < 500)
- Category is not `snack_bar_granola`, so no snack-bar cap
- Net: penalty −6, subject to family budget of 8 → penalty applied in full

---

### Processing Load (`PROCESSING_LOAD`)

The concern that captures degree of industrial processing. NOVA level and additive burden are both processing signals; without coordination, a NOVA 4 product could face both a NOVA cap and multiple additive caps simultaneously for the same underlying quality failure.

**Primary signal (caps — strictest wins):**
- `NOVA_PROXY_4_ULTRA_PROCESSED`: cap at **60** — product inferred as NOVA 4

**Other cap rules (reduced or discarded after coordination):**
- `ADDITIVE_MARKERS_5_PLUS`: cap at **55** — 5 or more additive markers present
- `ADDITIVE_MARKERS_3_PLUS`: cap at **65** — 3 or more additive markers present
- `NOVA_PROXY_3_PROCESSED`: cap at **75** — product inferred as NOVA 3

When a product is NOVA 4 with 5+ additive markers, the coordinator sees both as PROCESSING_LOAD caps and keeps only the strictest: cap at **55** (`ADDITIVE_MARKERS_5_PLUS` in this case).

**Penalty rules (winner full value; others scaled to 50%):**
- `LONG_INGREDIENT_LIST`: −4 — more than 12 ingredients

**Supporting evidence factor:** 0.5

**Max penalty budget:** 12 points (`processing` family)

**Cap floor:** 55

**Max total score impact:** cap at 55 (floor-protected) + up to 12 points in penalties = **score minimum of ~43** before other families

**Example — ultra-processed bar with NOVA 4 and 6 additive markers:**
- `NOVA_PROXY_4_ULTRA_PROCESSED` fires (cap 60)
- `ADDITIVE_MARKERS_5_PLUS` fires (cap 55)
- Coordinator: both are PROCESSING_LOAD → keeps strictest → cap at **55**
- `LONG_INGREDIENT_LIST` fires (−4 penalty)
- Net: cap at 55, penalty −4

---

### Additive Load

Additive load is not a separate CONCERNS entry — additive-marker caps are coordinated within `PROCESSING_LOAD` above. But additive signals live in two separate penalty families, and the rules for each family's budget apply independently.

**`additives` family (sweeteners, emulsifiers, stabilizers, isolates):**

| Rule | Type | Value | Family |
|------|------|-------|--------|
| `SWEETENER_PRESENT` | cap | 70 | additives |
| `ADDITIVE_MARKERS_5_PLUS` | cap | 55 | additives |
| `ADDITIVE_MARKERS_3_PLUS` | cap | 65 | additives |

**Critical note:** `SWEETENER_PRESENT` is **not registered in the CONCERNS graph**. It fires independently of the processing-load coordination — it does not compete with NOVA caps or other additive caps for the "winner" position. Its cap (70) applies in addition to whatever the processing coordinator has already resolved.

This is by design: sweetener substitution is structurally distinct from ultra-processing. A product could be NOVA 1 (minimal processing) and still use a non-nutritive sweetener. The two concerns are independent.

**Max penalty budget:** 10 points (`additives` family)

**Cap floor:** 55

**`ingredient_complexity` family:**

| Rule | Type | Value | Family |
|------|------|-------|--------|
| `LONG_INGREDIENT_LIST` | penalty | −4 | ingredient_complexity |

**Max penalty budget:** 5 points (`ingredient_complexity` family)

**Cap floor:** 65

---

### Sodium Load (`SODIUM_LOAD`)

A narrow concern family: high sodium concentration and the fat-sodium hyper-palatability pattern share the same root. Without coordination, a high-sodium savoury snack could face a direct sodium cap and an HP fat-sodium penalty independently.

**Primary signal (cap):**
- `HIGH_SODIUM_700MG_PLUS`: cap at **60** — sodium ≥ 700mg/100g

**Supporting signal:**
- `HP_FAT_SODIUM_COMBO`: HP-engine penalty — fat-sodium hyper-palatability pattern (fat ≥ 25% of kcal AND sodium ≥ 300mg/100g)

After coordination: the high-sodium cap wins at full value; the HP fat-sodium penalty scales to 40% of its raw value.

**Supporting evidence factor:** 0.4

**Max penalty budget:** 8 points (`sodium` family)

**Cap floor:** 50

**Max total score impact:** cap at 60 + up to 8 points in penalties = **score minimum of ~52** before other families (noting the cap floor at 50 in the sodium family itself)

**Example — salted cracker with 850mg sodium and high fat:**
- `HIGH_SODIUM_700MG_PLUS` fires (cap 60)
- `HP_FAT_SODIUM_COMBO` fires (HP penalty, say −8 raw)
- Coordinator: both are SODIUM_LOAD → cap winner: HIGH_SODIUM_700MG_PLUS (only one cap); penalty winner: HP_FAT_SODIUM_COMBO (only one penalty, applied at full value since it's the winner even as the only entrant)
- Net: cap at 60, HP penalty at full (subject to hyper_palatability family budget separately)

---

### Fat Quality (`FAT_QUALITY`)

Fat quality coordination covers two distinct scenarios: industrial seed oils and saturated fat red labels. The shared concern prevents a single-red-label product from facing both a regulatory cap and a seed-oil penalty as if they were independent concerns.

**Primary signal (context-aware):**
- `ISRAELI_RED_LABEL_1` *(when the red label is for saturated fat)*: cap at **55**

**Supporting signal:**
- `SEED_OIL_PRESENT`: penalty −3 — refined seed oil in the ingredient list

**Context-aware routing:** The rule `ISRAELI_RED_LABEL_1` is mapped to different concerns depending on which red label fired. If the red label is for saturated fat, it routes to `FAT_QUALITY`. If it is for sugar, it routes to `SUGAR_LOAD`. If it is for sodium, it routes to `SODIUM_LOAD`. This is the only context-sensitive routing in the system.

**Note on saturated fat:** The saturated fat dimension penalty in the fat quality dimension (−max((sat_fat − 2g) × 4, 0)) is a **dimension-level calculation**, not a guardrail rule. It is not subject to concern coordination because dimension scoring runs independently of the guardrail layer. Concern coordination applies only to guardrail caps and penalties.

**Supporting evidence factor:** 0.5

**Max penalty budget:** 8 points (`fat_quality` family)

**Cap floor:** 55

**Max total score impact:** cap at 55 + up to 8 points in penalties = **score minimum of ~47**

---

### Low Satiety

Low satiety is not a standalone concern family in the coordinator. Its rules live within `CALORIE_LOAD` (see above). They are documented separately here because the UI and design language treat satiety as a distinct signal.

**Rules:**

| Rule | Type | Value | Trigger condition |
|------|------|-------|------------------|
| `HIGH_CAL_LOW_SATIETY_SEVERE` | cap | 55 | kcal ≥ 500 AND protein < 6g AND fiber < 3g |
| `HIGH_CAL_LOW_SATIETY_SOFT` | penalty | −6 | kcal ≥ 450 AND protein < 8g AND fiber < 5g |

**Key distinction:** Low satiety rules only fire when calorie density is high. A low-calorie product with low protein and low fiber does not trigger these rules — low satiety in a low-calorie product is not the same structural concern as low satiety in a calorie-dense product.

**How they coordinate:** Both rules are in CALORIE_LOAD. If both fire (a product at 510 kcal with 4g protein and 1g fiber would trigger both), coordination picks the cap as the primary structural signal. The penalty is applied as supporting evidence.

**Dimension-level low satiety:** The satiety support dimension (6% weight) scores protein and fiber contribution independently of these guardrail rules, and is not capped or coordinated. A product can receive a low satiety dimension score without triggering a guardrail — the guardrail fires only at the high-calorie-density threshold.

---

### Confidence and Data Quality

Confidence is a separate ceiling mechanism — not part of the CONCERNS graph. It runs after all guardrail coordination and family budget clamping have completed.

**How it works:**

| Confidence band | Score ceiling applied |
|----------------|----------------------|
| High (≥ 80) | None — score is not constrained by confidence |
| Medium (60–79) | None |
| Low (40–59) | Final score capped at **70** |
| Insufficient (< 40) | Final score capped at **50** |

**What reduces confidence:**

| Missing or suspicious field | Reduction |
|-----------------------------|-----------|
| Energy (kcal) absent | −10 |
| Protein absent | −10 |
| Carbohydrates absent | −10 |
| Fat absent | −10 |
| Fiber absent | −5 |
| Sodium absent | −5 |
| Ingredient list entirely absent | −25 |
| Sugar > total carbohydrates | −20 |
| Saturated fat > total fat | −20 |
| Energy outside physiological range | −10 |
| Low NOVA classification confidence | up to −10 |
| Low category classification confidence | up to −15 |

**Why it is separate from concern coordination:**

Concern coordination handles competing analytical signals about the same food quality issue. Confidence handles the reliability of the analysis itself. They are orthogonal. A product with perfect nutritional data and clear NOVA classification has no confidence ceiling applied — its score is fully determined by the quality signals. A product with missing critical fields cannot receive a grade that would require trusting signals the system does not have.

**Score impact:**

The confidence ceiling is binding regardless of what other rules have produced. A product that would otherwise score 85 (grade A) on the basis of its available signals, but is missing energy and protein data, has confidence ≤ 80 and may face a ceiling of 70 — returning grade B at most.

Confidence ceilings cannot be overridden by floor rules. A whole-food floor of 75 does not protect against a confidence ceiling of 50. The floor applies to the analytical result; the ceiling applies to how much that result can be trusted.

---

## Coordination happens before family budget clamping

The execution order matters:

1. All guardrail rules evaluate independently and produce a raw list of caps and penalties
2. The concern coordinator runs: winner selected per concern for caps (strictest wins); winner selected per concern for penalties (largest wins, others scaled to supporting factor)
3. The family budget clamp runs on the coordinated penalty list: if total penalties in a family exceed the budget, all are scaled proportionally until the total equals the budget
4. Caps are applied per family, with the family's cap floor as the lower bound
5. Floors are applied
6. The confidence ceiling is applied

This sequence means the family budget limits what survives even after coordination has already reduced the raw list. Coordination and budgeting are both necessary: coordination prevents the same concern from contributing full weight multiple times; budgeting prevents any single concern from dominating the score even after coordination.

---

## Complete family budget reference

| Family | Max penalty | Cap floor | Primary concern |
|--------|------------|-----------|----------------|
| `sugar` | 10 | 45 | Sugar Load |
| `sodium` | 8 | 50 | Sodium Load |
| `fat_quality` | 8 | 55 | Fat Quality |
| `processing` | 12 | 55 | Processing Load |
| `additives` | 10 | 55 | Additive Load |
| `regulatory` | 12 | 45 | Red labels |
| `calorie_density` | 8 | 55 | Calorie Load / Low Satiety |
| `hyper_palatability` | 12 | 50 | HP patterns |
| `ingredient_complexity` | 5 | 65 | Ingredient count |
| `general` | 6 | 50 | Veto and floors |
