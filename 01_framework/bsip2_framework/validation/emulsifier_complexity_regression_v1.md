# Emulsifier Complexity Score — 20 Regression Examples

**Purpose:** Define 20 canonical product scenarios that the emulsifier complexity score must handle correctly. Each entry describes the expected penalty output, the reasoning, and the dangerous trap to avoid.

**Spec reference:** `docs/scoring/emulsifier_complexity_spec_v1.md` (ECS-v1, EV-045)

**Scoring function interface:**
```
emulsifier_complexity_score(agents: list[dict]) -> tuple[highest_penalty, complexity_adj, total]
```

---

## Example 1 — Plain almond butter (no emulsifiers)

**Ingredient list:** Almonds, salt

**Detected agents:** None (0)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 0 | — |
| `complexity_tier` | none | — |
| `highest_penalty` | 0 | — |
| `complexity_adj` | 0 | — |
| `total_penalty` | **0** | — |

**Why:** Single-ingredient whole food with salt. No emulsifiers or stabilisers present. No penalty applies.

**Dangerous trap:** The system must not confuse "no emulsifiers" with "low additive burden" — this product should score zero on the complexity axis specifically, even though its overall additive quality score may be high for unrelated reasons.

---

## Example 2 — Peanut butter with lecithin

**Ingredient list:** Peanuts, soy lecithin (E322), salt

**Detected agents:** `soy_lecithin` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 1 | — |
| `complexity_tier` | simple | — |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | 0 | single agent, no adj |
| `total_penalty` | **−1** | — |

**Why:** Lecithin is a low/contextual concern. Single agent = simple complexity. Total penalty: −1.

**Dangerous trap:** Lecithin should NOT trigger the same penalty as CMC. A −5 penalty here would be an evidence failure — lecithin lacks the gut-barrier mechanism of the high-concern agents.

---

## Example 3 — Hummus with guar gum and xanthan gum

**Ingredient list:** Chickpeas, tahini, water, guar gum (E412), xanthan gum (E415), salt, citric acid

**Detected agents:** `guar_gum` (low), `xanthan_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | 2 agents |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−2** | −1 + (−1) |

**Why:** Two low-concern agents. The complexity adjustment acknowledges that two distinct stabilisers in a hummus signal intentional texture engineering, even though each agent is individually benign.

**Dangerous trap:** The system must not collapse 2 low agents to "zero complexity." Two gums in hummus are a formulation choice — a reasonable single-gum hummus exists as a benchmark. The penalty should be modest but non-zero.

---

## Example 4 — Greek yogurt (plain, no additives)

**Ingredient list:** Cultured milk, live active cultures

**Detected agents:** None (0)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 0 | — |
| `complexity_tier` | none | — |
| `highest_penalty` | 0 | — |
| `complexity_adj` | 0 | — |
| `total_penalty` | **0** | — |

**Why:** Plain yogurt. No emulsifiers, no stabilisers. Zero penalty.

**Dangerous trap:** A clean yogurt should score the same as Example 1 on the complexity axis, even though they are very different products. The complexity score measures only emulsifier/stabiliser load, not overall nutritional quality.

---

## Example 5 — Flavored yogurt with modified starch and pectin

**Ingredient list:** Cultured milk, sugar, strawberry puree, modified corn starch (E1422), pectin (E440), natural flavor, live cultures

**Detected agents:** `modified_starch_stabilizer` (medium), `pectin` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −3 | medium (−3) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−4** | −3 + (−1) |

**Why:** Modified starch (medium) provides the highest individual concern weight. Pectin adds a second agent, triggering the moderate complexity adjustment. The modified starch is correctly counted because flavored yogurt is not a bread/cereal category — it is a stabiliser use, not a structural starch.

**Dangerous trap:** Modified starch in dairy is a stabiliser, not a structural ingredient. The signal-based gate must count it here (yogurt is not a grain-based staple). If the system incorrectly exempts modified starch when the product is not grain-based, this scenario would under-penalise.

---

## Example 6 — Ice cream with CMC and carrageenan

**Ingredient list:** Milk, cream, sugar, dextrose, CMC (E466), carrageenan (E407), mono- and diglycerides (E471), natural vanilla flavor

**Detected agents:** `cmc` (high), `carrageenan` (medium), `mono_diglyceride` (medium)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 3 | — |
| `complexity_tier` | high | 3+ agents |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3) |

**Why:** CMC (high) sets the highest individual penalty at −5. Three distinct agents across three categories (high/medium/medium) = high complexity. This is an engineered ice cream with a multi-agent stabiliser system.

**Dangerous trap:** The system must correctly count carrageenan only once, even though it appears in both `tax_emulsifier_concern` (for F1 identity deltas) and `tax_emulsifier_medium` (for complexity). Deduplication must use the canonical identity, not the additive class.

---

## Example 7 — Diet protein shake with CMC, lecithin, and gum arabic

**Ingredient list:** Water, whey protein isolate, CMC (E466), soy lecithin (E322), gum arabic (E414), natural flavor, acesulfame-K, vitamins

**Detected agents:** `cmc` (high), `soy_lecithin` (low), `gum_arabic` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 3 | — |
| `complexity_tier` | high | 3+ agents |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3) |

**Why:** CMC dominates (high tier, −5). Three distinct agents (CMC + lecithin + gum arabic) = high complexity. The complexity adjustment accounts for the engineered texture system, even though the low-tier agents are individually benign.

**Dangerous trap:** Gum arabic is prebiotic — its presence should not increase the concern penalty at the individual level, but it DOES count as one of the 3+ agents for complexity counting. The complexity score is about formulation complexity, not per-agent risk.

---

## Example 8 — Whole milk (no emulsifiers)

**Ingredient list:** Milk

**Detected agents:** None (0)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 0 | — |
| `complexity_tier` | none | — |
| `highest_penalty` | 0 | — |
| `complexity_adj` | 0 | — |
| `total_penalty` | **0** | — |

**Why:** Single-ingredient whole food. Zero emulsifiers, zero stabilisers.

**Dangerous trap:** The frozen milk invariant (85/A) must be unaffected. This regression example anchors the "zero" baseline for the entire dairy category.

---

## Example 9 — Bread (plain whole wheat, no additives)

**Ingredient list:** Whole wheat flour, water, yeast, salt

**Detected agents:** None (0)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 0 | — |
| `complexity_tier` | none | — |
| `highest_penalty` | 0 | — |
| `complexity_adj` | 0 | — |
| `total_penalty` | **0** | — |

**Why:** Simple bread. No emulsifiers or stabilisers. The frozen bread retail_003 corpus must remain unchanged for clean baseline products.

**Dangerous trap:** Flour is not an emulsifier. Modified starch is absent. Even though bread has a "structural" starch matrix, the complexity score only counts added emulsifier/stabiliser agents.

---

## Example 10 — Bread light with E471, E481, E466

**Ingredient list:** Water, wheat flour, whole wheat flour, dietary fiber (inulin), wheat gluten, yeast, salt, E471 (mono- and diglycerides), E481 (sodium stearoyl-2-lactylate), E466 (CMC), preservative (calcium propionate)

**Detected agents:** `mono_diglyceride` (medium), `ssl` (medium), `cmc` (high)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 3 | — |
| `complexity_tier` | high | 3+ agents |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3) |

**Why:** Bread light products are the canonical engineered-bread case. Three distinct agents (CMC + E471 + E481). CMC dominates. The bread-1000 dataset has multiple products matching this profile.

**Dangerous trap:** Bread light products are NOT exempt from the modified-starch gate — but there is no modified starch in this example. All three agents are conventional emulsifiers, counted normally regardless of bread category.

---

## Example 11 — Mayonnaise with guar gum and xanthan gum

**Ingredient list:** Vegetable oil, water, egg yolk, vinegar, guar gum (E412), xanthan gum (E415), salt, mustard, citric acid

**Detected agents:** `guar_gum` (low), `xanthan_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−2** | −1 + (−1) |

**Why:** Two low-concern agents. Identical structure to Example 3 (hummus). The penalty is the same regardless of category — only agent identity and count matter.

**Dangerous trap:** The system must be category-agnostic for gum counting. A hummus with guar + xanthan and a mayonnaise with guar + xanthan must produce the same complexity score. The category only matters for the modified-starch gate.

---

## Example 12 — Snack bar with lecithin, guar gum, and date paste

**Ingredient list:** Dates, oats, peanut butter, soy lecithin (E322), guar gum (E412), honey, salt

**Detected agents:** `soy_lecithin` (low), `guar_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−2** | −1 + (−1) |

**Why:** Two low agents. Even in a snack bar context, the complexity score remains −2. The existing `snack_bar_granola` category rules (calorie/sugar caps) handle the broader scoring — this is purely about emulsifier/stabiliser complexity.

**Dangerous trap:** A snack bar with no high-concern agents should not receive a large emulsifier complexity penalty just because the category is `snack_bar_granola`. The complexity score measures agents, not category assumptions.

---

## Example 13 — Snack bar with polysorbate 80, mono/diglycerides, soy lecithin, and xanthan gum

**Ingredient list:** Oats, glucose syrup, sugar, palm oil, polysorbate 80 (E433), mono- and diglycerides (E471), soy lecithin (E322), xanthan gum (E415), salt, natural flavor

**Detected agents:** `polysorbate_80` (high), `mono_diglyceride` (medium), `soy_lecithin` (low), `xanthan_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 4 | — |
| `complexity_tier` | high | 3+ |
| `highest_penalty` | −5 | high (P80, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3) |

**Why:** Four separate agents across all three tiers. Polysorbate 80 dominates. High complexity. This is a heavily engineered snack bar with a complex emulsifier system. The total penalty (−8) hits the maximum family budget (8 pts, per concern coordination).

**Dangerous trap:** The low-tier agents (lecithin, xanthan) each contribute only −1 to the highest-penalty calculation, but they count toward the 3+ threshold for the high complexity adjustment. Removing them would reduce the total penalty from −8 to −5. This is correct — complexity is about the number of agents, not just the worst one.

---

## Example 14 — Cream cheese with carrageenan and locust bean gum

**Ingredient list:** Cream, milk, salt, carrageenan (E407), locust bean gum (E410), cheese culture

**Detected agents:** `carrageenan` (medium), `locust_bean_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −3 | medium (carrageenan, −3) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−4** | −3 + (−1) |

**Why:** Carrageenan (medium) + locust bean gum (low) = 2 agents. Highest individual penalty is −3 (medium tier). Complexity adjustment adds −1 for moderate complexity.

**Dangerous trap:** Cream cheese stabiliser systems are standard — but the complexity score must distinguish between a single-agent system (carrageenan only) and a dual-agent system (carrageenan + gum). The moderate adjustment captures this distinction without over-penalising a normal formulation.

---

## Example 15 — Instant pudding mix with CMC, carrageenan, guar gum, and DATEM

**Ingredient list:** Sugar, modified corn starch (E1422), dextrose, CMC (E466), carrageenan (E407), guar gum (E412), DATEM (E472e), salt, natural flavor, color

**Detected agents:** `cmc` (high), `carrageenan` (medium), `guar_gum` (low), `datem` (medium), `modified_starch_stabilizer` (medium)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 5 | — |
| `complexity_tier` | high | 3+ |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3), capped at budget max |

**Why:** Five agents across all three tiers. CMC dominates at −5. High complexity adjustment. The total penalty hits the −8 family budget cap — this is the maximum the complexity score can contribute.

**Dangerous trap:** The system must not exceed the family budget of 8 points even with 5+ agents. The concern coordination contract sets this ceiling. If more agents than 3 do not increase per-agent evidence, they should not increase the penalty beyond the cap.

---

## Example 16 — Oat milk (plain, with CMC and gum arabic)

**Ingredient list:** Oat base (water, oats), CMC (E466), gum arabic (E414), calcium carbonate, salt, vitamins

**Detected agents:** `cmc` (high), `gum_arabic` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−6** | −5 + (−1) |

**Why:** CMC (high) + gum arabic (low) = 2 agents. CMC dominates at −5. Moderate complexity adjustment. Note: gum arabic is prebiotic (EV-019) but still counts as an agent for complexity counting.

**Dangerous trap:** The oat milk example from the golden products suite warns against penalising oat milk with added calcium the same as a product with six emulsifiers. Here, CMC + gum arabic is 2 agents producing −6 total — moderate, not extreme. This correctly differentiates from the 5-agent pudding mix at −8.

---

## Example 17 — Coconut milk (canned) with guar gum only

**Ingredient list:** Coconut extract, water, guar gum (E412)

**Detected agents:** `guar_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 1 | — |
| `complexity_tier` | simple | — |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | 0 | simple |
| `total_penalty` | **−1** | — |

**Why:** Single low-concern agent. Many canned coconut milks list only guar gum as a stabiliser. Minimal complexity penalty.

**Dangerous trap:** A single stabiliser in a canned product is normal manufacturing practice. The system must not penalise single-gum formulations as if they were multi-agent engineered systems.

---

## Example 18 — Sugar-free gum with multiple stabilisers

**Ingredient list:** Gum base, sorbitol, maltitol, xylitol, glycerol, gum arabic (E414), CMC (E466), carrageenan (E407), lecithin (E322), aspartame, acesulfame K, natural flavor, color

**Detected agents:** `cmc` (high), `carrageenan` (medium), `gum_arabic` (low), `soy_lecithin` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 4 | — |
| `complexity_tier` | high | 3+ |
| `highest_penalty` | −5 | high (CMC, −5) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−8** | −5 + (−3), cap |

**Why:** Four agents. CMC dominates. High complexity. Hits the family budget cap. This is the canonical "chemistry experiment with a food label" product from known_failure_modes.md — but the complexity score captures only the emulsifier/stabiliser dimension of that concern.

**Dangerous trap:** Gum's total additive burden includes sweeteners, colours, and flavours beyond emulsifiers/stabilisers. The complexity score must not over-claim — it measures only emulsifier/stabiliser complexity, not the full additive load.

---

## Example 19 — Ketchup with xanthan gum only

**Ingredient list:** Tomato concentrate, sugar, vinegar, salt, xanthan gum (E415), onion powder, garlic powder, natural flavor

**Detected agents:** `xanthan_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 1 | — |
| `complexity_tier` | simple | — |
| `highest_penalty` | −1 | low (−1) |
| `complexity_adj` | 0 | simple |
| `total_penalty` | **−1** | — |

**Why:** Single low-concern agent. Ketchup uses xanthan as a standard thickener. Minimal complexity penalty.

**Dangerous trap:** Even though ketchup has many other additives (sugar, vinegar, spices), they are not emulsifiers or stabilisers. The complexity score must not conflate general additive burden with emulsifier/stabiliser complexity.

---

## Example 20 — Plant-based yogurt alternative with pectin, guar gum, gellan gum, and modified starch

**Ingredient list:** Water, coconut cream, pea protein, modified tapioca starch (E1442), pectin (E440), guar gum (E412), gellan gum (E418), tricalcium phosphate, vitamins, live cultures, natural flavor

**Detected agents:** `modified_starch_stabilizer` (medium), `pectin` (low), `guar_gum` (low), `gellan_gum` (low)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 4 | — |
| `complexity_tier` | high | 3+ |
| `highest_penalty` | −3 | medium (modified starch, −3) |
| `complexity_adj` | −3 | high |
| `total_penalty` | **−6** | −3 + (−3) |

**Why:** Four agents — medium (modified starch) + three low. Highest individual penalty is −3 (medium). High complexity adjustment adds −3. Total: −6. This product has no high-concern agent, but the multi-agent stabiliser system signals significant formulation engineering.

**Dangerous trap:** The total penalty (−6) is lower than Example 6's (−8) because there is no high-concern agent. This is correct — the complexity score's primary driver is the highest individual concern tier. A product with four benign gums should score lower than a product with one CMC plus other agents. The system must not let agent count alone dominate the penalty — concern tier must take priority.

---

## Example 21 — Plain bread with modified starch as structural ingredient

**Ingredient list:** Whole wheat flour, water, modified wheat starch (E1442), yeast, salt, wheat gluten

**Detected agents:** None — modified starch is at position 3 in a bread product, no light/diet signal

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 0 | modified starch excluded (position 1–3 in bread, no light/diet signal) |
| `complexity_tier` | none | — |
| `highest_penalty` | 0 | — |
| `complexity_adj` | 0 | — |
| `total_penalty` | **0** | — |

**Why:** Modified starch at position 3 fails both triggers: position is < 4 (no late-position signal) and product name has no light/diet signal. The starch is treated as a structural flour ingredient in a grain-based staple. Modified starch is still evaluated under matrix/processing rules (fragmentation → reconstructed) outside the complexity score.

**Dangerous trap:** The system must NOT count modified starch here. This test verifies the signal-based gate correctly excludes structural starch in bread. The downstream fragmentation penalty (`reconstructed` level) still applies — this exclusion is complexity-score-only.

---

## Example 22 — Bread light with modified starch as fat replacer

**Ingredient list:** Water, wheat flour, whole wheat flour, dietary fiber (inulin), wheat gluten, yeast, salt, modified corn starch (E1422), E471 (mono- and diglycerides), preservative (calcium propionate)

**Detected agents:** `modified_starch_stabilizer` (medium), `mono_diglyceride` (medium)

| Component | Expected | Notes |
|-----------|----------|-------|
| `agent_count` | 2 | — |
| `complexity_tier` | moderate | — |
| `highest_penalty` | −3 | medium (both −3) |
| `complexity_adj` | −1 | moderate |
| `total_penalty` | **−4** | −3 + (−1) |

**Why:** Modified starch at position 8 fails the position trigger (≥ 4), AND the product name "bread light" contains a light/diet signal. Both triggers independently fire → counted. Two medium agents → moderate complexity.

**Dangerous trap:** If the system used the old category-scoped rule, this product (bread category) would incorrectly exclude the modified starch. The signal-based rule correctly counts it because: (a) position 8 is well past the structural flour threshold, and (b) "light" signals fat-replacer function. The downstream fragmentation penalty also still applies — double coverage of different signals is correct.

---

## Summary Table

| # | Scenario | Agent count | Agent tiers | Highest penalty | Complexity adj | Total penalty |
|---|----------|------------|-------------|----------------|---------------|-------|
| 1 | Plain almond butter | 0 | — | 0 | 0 | **0** |
| 2 | Peanut butter + lecithin | 1 | 1 low | −1 | 0 | **−1** |
| 3 | Hummus + guar + xanthan | 2 | 2 low | −1 | −1 | **−2** |
| 4 | Plain Greek yogurt | 0 | — | 0 | 0 | **0** |
| 5 | Flavored yogurt + mod starch + pectin | 2 | 1 med + 1 low | −3 | −1 | **−4** |
| 6 | Ice cream + CMC + carrageenan + mono/di | 3 | 1 high + 2 med | −5 | −3 | **−8** |
| 7 | Diet shake + CMC + lecithin + gum arabic | 3 | 1 high + 2 low | −5 | −3 | **−8** |
| 8 | Whole milk | 0 | — | 0 | 0 | **0** |
| 9 | Plain bread | 0 | — | 0 | 0 | **0** |
| 10 | Bread light + E471 + E481 + E466 | 3 | 1 high + 2 med | −5 | −3 | **−8** |
| 11 | Mayonnaise + guar + xanthan | 2 | 2 low | −1 | −1 | **−2** |
| 12 | Snack bar + lecithin + guar | 2 | 2 low | −1 | −1 | **−2** |
| 13 | Snack bar + P80 + E471 + lecithin + xanthan | 4 | 1 high + 1 med + 2 low | −5 | −3 | **−8** |
| 14 | Cream cheese + carrageenan + LBG | 2 | 1 med + 1 low | −3 | −1 | **−4** |
| 15 | Instant pudding + CMC + carra + guar + DATEM + mod starch | 5 | 1 high + 3 med + 1 low | −5 | −3 | **−8** |
| 16 | Oat milk + CMC + gum arabic | 2 | 1 high + 1 low | −5 | −1 | **−6** |
| 17 | Coconut milk + guar | 1 | 1 low | −1 | 0 | **−1** |
| 18 | Sugar-free gum + CMC + carra + gum arabic + lecithin | 4 | 1 high + 1 med + 2 low | −5 | −3 | **−8** |
| 19 | Ketchup + xanthan | 1 | 1 low | −1 | 0 | **−1** |
| 20 | Plant yogurt + mod starch + pectin + guar + gellan | 4 | 1 med + 3 low | −3 | −3 | **−6** |
| 21 | Bread + modified starch (position 3, structural) | 0 | modified starch excluded (position 1–3 in bread) | 0 | 0 | **0** |
| 22 | Bread light + modified starch (position 8, light signal) + E471 | 2 | 2 med | −3 | −1 | **−4** |
