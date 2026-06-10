# Emulsifier Complexity Score — Methodology Spec v1

**Document ID:** ECS-v1  
**Date:** 2026-06-10  
**Evidence registry:** EV-045  
**Status:** Design spec — not implemented  
**Owner:** Scoring Governance Lead  

---

## 1. Purpose and Scope

The emulsifier complexity score measures the **aggregate burden** of texture-stabilizing additives in a product. It is distinct from the existing per-agent identity deltas (`ADDITIVE_IDENTITY_DELTAS`, F1/TASK-222A), which penalise individual high-concern emulsifiers by name. This score captures what identity deltas miss:

- **Medium-concern agents**: mono/diglycerides, modified starches used as stabilisers/thickeners
- **Low/contextual agents**: gums (guar, xanthan, acacia, locust bean), pectin, lecithin
- **Complexity**: the compounding effect of having multiple distinct agents acting in concert

**The score is labelled `emulsifier_complexity_score`, NOT `emulsifier_load_score`.** The "load" naming is reserved until serving-level concentration data is label-observable (currently not available on Israeli retail labels).

### 1.1 Relationship to existing scoring

| Component | Existing (F1/TASK-222A) | This spec (EV-045) |
|-----------|------------------------|---------------------|
| High concern penalty | −3 each, cap −6 (CMC/P80/carrageenan) | Highest-tier penalty + complexity adj |
| Medium concern | Not penalised by name | Counted via tier weight |
| Low/contextual | Lecithin gets +2 relief; gums exempted | Counted via tier weight (lighter) |
| Multi-agent complexity | None | Complexity adjustment on top |
| Double-count risk | — | **Fully additive** — identity deltas fire first on `additive_quality` dimension; complexity score fires on a new `emulsifier_complexity` signal |

---

## 2. Concern Tier Definitions

### 2.1 High concern

Agents with strong mechanistic evidence of gut barrier disruption (EV-003) at label-relevant exposures.

| Agent | E-number | Evidence | Signal in scoring |
|-------|----------|----------|-------------------|
| Polysorbate 80 | E433 | EV-003: Strong (mouse model + consistent in vitro); EFSA ADI 0–25 mg/kg | `tax_emulsifier_concern` (existing) |
| CMC / carboxymethylcellulose | E466 | EV-003: Strong (human RCT, Chassaing 2022); `contested` in tiered library | `tax_emulsifier_concern` (existing) |

Individual concern weight: **−5** (per agent detected)

### 2.2 Medium concern

Agents with documented functional utility as stabilisers/emulsifiers and some mechanistic or epidemiological signal, but weaker evidence than the high tier.

| Agent | E-number | Evidence | Signal in scoring |
|-------|----------|----------|-------------------|
| Mono- and diglycerides | E471 | EV-043: `likely-neutral`; NutriNet-Santé class-level observational signal | New: `tax_emulsifier_medium` |
| DATEM | E472e | EV-043: `likely-neutral`; no DATEM-specific mechanistic concern | New: `tax_emulsifier_medium` |
| SSL (sodium stearoyl-2-lactylate) | E481 | EV-043: `likely-neutral`; ADI 20 mg/kg, exposure << ADI | New: `tax_emulsifier_medium` |
| PGPR (polyglycerol polyricinoleate) | E476 | EV-043: `likely-neutral`; structurally distinct from polysorbates | New: `tax_emulsifier_medium` |
| Carrageenan | E407 | EV-003: Moderate-Strong; `contested` in tiered library. **Note:** carrageenan is `emulsifier_concern` in F1 (existing) for per-agent identity deltas (−3). Under ECS-v1 it receives medium weight for complexity purposes because its gut-barrier evidence, while real, is at food-grade rather than degraded-poligeenan level and does not warrant the highest complexity tier. | `tax_emulsifier_concern` (existing) + separate medium tracking |
| Modified starches (E1400–E1450) where functionally acting as stabilisers/thickeners | E1400–E1450 | EV-043: `likely-neutral`; metabolised as carbohydrate; no harm signal | New: `tax_emulsifier_medium` (when category = thickener/stabilizer) |

Individual concern weight: **−3** (per agent detected)

#### Distinguishing modified starch use

Modified starch in a product whose primary structure is grain-based counts as a **structural ingredient** (starch form → `reconstructed` fragmentation) rather than an emulsifier/stabiliser additive. For the complexity score, modified starch is counted only when its function is clearly a stabiliser/thickener rather than a primary structural flour.

**Signal-based counting rule (not category-scoped):**

| Context | Counted? | Rationale |
|---------|----------|-----------|
| Dairy dessert / pudding | Yes | Thickener in a non-starch matrix |
| Soup / sauce | Yes | Stabiliser in water-based system |
| Bread (as listed ingredient, position 1–3) | No | Structural flour ingredient (already penalised via fragmentation) |
| Snack bar with added modified starch | Yes | Texture engineering in a multi-component system |
| Bread light / diet bread | Yes | Light/diet signal indicates fat-replacer or texturiser function |
| Plain bread with modified starch at position 4+ | Yes | Late position indicates additive/thickener function, not structural |

Two independent triggers count modified starch for emulsifier_complexity:
- **Position-based trigger:** the modified starch ingredient appears at position 4 or later in the ingredient list (indicating additive/thickener function, not primary structural flour)
- **Signal-based trigger:** the product name or marketing claims include light/diet/reduced-calorie signals: Hebrew `קל`, `דיאט`, `לייט`

If either trigger fires, modified starch is counted. If neither fires and the product is a grain-based staple (bread, cereal, cracker), the starch is treated as a structural ingredient and excluded from complexity counting only.

**Downstream processing unaffected:** This exclusion applies **only** to emulsifier_complexity counting. Modified starch is still evaluated under all other matrix/processing rules (NOVA proxy, fragmentation → `reconstructed`, additive_marker_count) regardless of this gate.

### 2.3 Low / contextual concern

Agents with neutral-to-positive evidence profiles (EV-003, EV-019, EV-043) — safe at label exposures, often functional or prebiotic.

| Agent | E-number | Evidence | Signal in scoring |
|-------|----------|----------|-------------------|
| Lecithin (soy/sunflower) | E322 | EV-003: Moderate; `emulsifier_benign`; → +2 relief in F1 | `tax_emulsifier_benign` (existing) |
| Pectin | E440 | EV-043: `functional`; soluble dietary fibre, prebiotic | New: `tax_emulsifier_low` |
| Gum arabic / acacia gum | E414 | EV-019: Prebiotic gum exemption | New: `tax_emulsifier_low` |
| Guar gum | E412 | EV-043: `functional`; soluble fibre | New: `tax_emulsifier_low` |
| Xanthan gum | E415 | EV-043: `functional`; fermentation-derived polysaccharide | New: `tax_emulsifier_low` |
| Locust bean gum / carob gum | E410 | EV-043: `functional`; classified dietary fibre | New: `tax_emulsifier_low` |
| Agar | E406 | No concern; seaweed-derived gelling agent | New: `tax_emulsifier_low` |
| Gellan gum | E418 | No concern; fermentation-derived stabiliser | New: `tax_emulsifier_low` |
| Sodium alginate | E401 | EV-043: `functional`; seaweed polysaccharide, not absorbed intact | New: `tax_emulsifier_low` |

Individual concern weight: **−1** (per agent detected)

**Important — low-tier agents are still counted in the complexity score.** Their individual weight is small, but the aggregate complexity of 3+ low-tier agents (e.g., lecithin + guar + xanthan) signals formulation engineering that warrants a modest adjustment.

---

## 3. Ingredient Registry Mapping

The full mapping of known emulsifier/stabiliser agents to their concern tier, detection patterns, and E-numbers. This table is the source of truth for downstream implementation.

### 3.1 High concern

| Canonical | E-number | Hebrew detection patterns | Existing taxonomy |
|-----------|----------|--------------------------|-------------------|
| `polysorbate_80` | E433 | פוליסורבט 80, פוליסורבט-80, טווין 80, E433 | `emulsifier_concern` ✓ |
| `cmc` | E466 | CMC, קרבוקסי מתיל צלולוז, קרבוקסימתיל צלולוז, צלולוז גליקולט, E466 | `emulsifier_concern` ✓ |

### 3.2 Medium concern

| Canonical | E-number | Hebrew detection patterns | Existing taxonomy | Category gate |
|-----------|----------|--------------------------|-------------------|---------------|
| `carrageenan` | E407 | קרגינן, קרגינאן, קרגן, כרכן ים, E407 | `emulsifier_concern` ✓ | None — always counted |
| `mono_diglyceride` | E471 | מונו-גליצריד, מונוגליצריד, דיגליצריד, E471 | Not in taxonomy | None |
| `datem` | E472e | DATEM, E472e, E472 | Not in taxonomy | None |
| `ssl` | E481 | E481, סודיום סטיארויל לקטילט | Not in taxonomy | None |
| `pgpr` | E476 | E476, פוליגליצרול פוליריצינולאט | Not in taxonomy | None |
| `modified_starch_stabilizer` | E1400–E1450 | עמילן מעובד, עמילן מוקשה, עמילן משונה, E14XX | `modified_starch` (fragmentation) | Position ≥ 4 or product name has light/diet signal |

**Hebrew detection patterns for mono/diglycerides:**
- `מונו-גליצריד` / `מונוגליצריד` / `דיגליצריד`
- `מונו ודיגליצריד` / `מונו-ודי-גליצריד`
- `E471` / `E-471`
- Existing: `NON_LECITHIN_EMULSIFIER_RE` matches `E-?471|E-?472|E-?476|E-?481|DATEM|מונו.{0,5}גליצריד|דיגליצריד` — reuse this pattern.

### 3.3 Low / contextual concern

| Canonical | E-number | Hebrew detection patterns | Existing taxonomy | Notes |
|-----------|----------|--------------------------|-------------------|-------|
| `soy_lecithin` | E322 | לציטין, לציטין סויה, E322 | `emulsifier_benign` ✓ | Already in taxonomy |
| `sunflower_lecithin` | E322 | לציטין חמניות, לציטין מחמניות | `emulsifier_benign` ✓ | Already in taxonomy |
| `pectin` | E440 | פקטין, E440 | Not in taxonomy | functional |
| `gum_arabic` | E414 | גומי ערבי, גומי אקאציה, E414 | PREBIOTIC_GUM_PATTERNS | prebiotic |
| `guar_gum` | E412 | גואר, גואר גאם, E412 | Not in taxonomy | functional |
| `xanthan_gum` | E415 | קסנטן, קסנטן גאם, E415 | Not in taxonomy | functional |
| `locust_bean_gum` | E410 | גומי חרוב, E410 | Not in taxonomy | functional |
| `agar` | E406 | אגר, אגר-אגר, E406 | Not in taxonomy | no concern |
| `gellan_gum` | E418 | ג'לאן גאם, E418 | Not in taxonomy | no concern |
| `sodium_alginate` | E401 | נתרן אלגינט, E401 | Not in taxonomy | functional |

---

## 4. Complexity Score Calculation

### 4.1 Agent counting

Count distinct agents across all three tiers. Each canonical agent is counted at most once, regardless of how many times it appears in the ingredient list.

```
agent_list = (high_concern_agents + medium_concern_agents + low_concern_agents)
agent_count = len(set(agent_list))
```

- 0 agents → complexity tier: **none**
- 1 agent → complexity tier: **simple**
- 2 agents → complexity tier: **moderate**
- 3+ agents → complexity tier: **high**

### 4.2 Penalty calculation

```
# Step 1: Highest individual concern penalty
highest_penalty = max(
    [-5 for a in high_concern_agents] +
    [-3 for a in medium_concern_agents] +
    [-1 for a in low_concern_agents],
    default=0
)

# Step 2: Complexity adjustment
complexity_adjustments = {
    "none":     0,
    "simple":   0,     # single agent: no added complexity
    "moderate": -1,    # two agents: small stacked-adjustment
    "high":     -3,    # 3+ agents: meaningful formulation complexity
}

complexity_adj = complexity_adjustments[complexity_tier]

# Step 3: Final penalty (applied to emulsifier_complexity dimension)
total_penalty = highest_penalty + complexity_adj
```

**Example calculations:**

| Scenario | Agents | Highest penalty | Complexity | Total |
|----------|--------|----------------|------------|-------|
| Lecithin only | 1 low | −1 | 0 (simple) | **−1** |
| CMC only | 1 high | −5 | 0 (simple) | **−5** |
| CMC + carrageenan | 2 (high + medium) | −5 | −1 (moderate) | **−6** |
| CMC + carrageenan + guar | 3 (high + medium + low) | −5 | −3 (high) | **−8** |
| Guar + xanthan + lecithin | 3 low | −1 | −3 (high) | **−4** |
| Mono/diglyceride + modified starch | 2 medium | −3 | −1 (moderate) | **−4** |
| CMC + P80 + lecithin | 2 high + 1 low | −5 | −3 (high) | **−8** |

### 4.3 Interaction with existing F1 identity deltas

The complexity score is **additive** to the existing `ADDITIVE_IDENTITY_DELTAS`:

- F1 identity deltas (−3 each, cap −6): fire on `additive_quality` dimension for carrageenan/CMC/P80
- Complexity penalty: fires on a separate `emulsifier_complexity` dimension signal

This means a product with CMC + carrageenan receives:
- F1: −6 on additive_quality (two concern agents, cap at −6)
- ECS: −5 (highest: CMC) + −1 (moderate complexity, 2 agents) = −6 on emulsifier_complexity
- Combined effect is NOT double-counting because they target different dimension signals.

The concern coordination contract must be updated to include the `emulsifier_complexity` family alongside `additives` and `ingredient_complexity`.

---

## 5. Consumer-Facing Language

When the complexity tier is **moderate** or **high**, include a consumer-facing note using these rules:

| Complexity tier | Wording |
|----------------|---------|
| Simple (1 agent) | No note (unless individual concern is high — existing UI language applies: "Contains a higher-concern texture additive" per `ui_language.md`) |
| Moderate (2 agents) | "Contains several texture-stabilizing additives" |
| High (3+ agents) | "Contains several texture-stabilizing additives" — same wording, higher score impact |

**Forbidden phrases** (product liability exposure — EV-045 mandate):
- "high dose"
- "unsafe"
- "toxic"
- "exceeds safe amount"
- Any language implying regulatory limit exceedance

**Permitted framing:**
- "Contains several texture-stabilizing additives"
- "Formulated with multiple emulsifiers and stabilizers"
- "Uses [N] texture-modifying additives"
- "Contains [agent name], a texture-stabilizing additive"

---

## 6. Anti-Accumulation and Rollback

### 6.1 Rule accumulation check

| Existing rule | Overlap with ECS-v1 | Resolution |
|-------------|---------------------|------------|
| `ADDITIVE_IDENTITY_DELTAS` (F1, TASK-222A) | Both penalise high-concern emulsifiers | **Separate dimensions** — F1 targets `additive_quality`; ECS targets a new `emulsifier_complexity` signal. The concern coordination contract handles the per-family budget between them. |
| `ADDITIVE_MARKERS_3_PLUS` / `ADDITIVE_MARKERS_5_PLUS` caps | Both count additives | **Different scope** — additive marker caps count ALL additive categories (preservatives, colours, flavours, etc.). ECS counts only emulsifier/stabiliser agents. |
| `sprint1_additive_correction` (retired, zeroed) | No overlap | Already zeroed by TASK-222A. |
| `BHA_NAMED_PENALTY` (F4) | No overlap | BHA is an antioxidant, not an emulsifier/stabiliser. |
| `long_ingredient_list` penalty (−4) | Weak overlap (more agents → longer list) | **Independent** — long ingredient list can fire without any emulsifiers (e.g., 20 spices). ECS fires only on emulsifier/stabiliser agents. |

### 6.2 Rollback plan

| Layer | Previous state | Restore method |
|-------|---------------|----------------|
| Evidence registry | No EV-045 entry | `git revert` of EV-045 addition to `bsip2_evidence_registry_v1.md` |
| Taxonomy | `ingredient_taxonomy._ADDITIVES` unchanged | `git revert` of new medium/low Identity entries |
| Signal extractor | No `tax_emulsifier_medium` / `tax_emulsifier_low` signals | Revert signal additions |
| Constants | No `EMULSIFIER_COMPLEXITY` block | Remove block |
| Engine | No `_emulsifier_complexity()` function | Remove function call |
| Consumer copy | UI language unchanged | Revert UI language additions |
| Notify | Scoring Governance Lead, Data Architecture, Nutrition, Product | |

---

## 7. Category Activation Scope

| Category | Active? | Notes |
|----------|---------|-------|
| snack_bar_granola | Yes | Highest emulsifier density |
| dairy_protein | Yes | Yogurt, cheese spreads, cream cheese |
| sauce_spread | Yes | Dressings, mayonnaise, hummus with stabilisers |
| beverage | Yes | Protein shakes, plant milks, diet drinks |
| bread | Yes | Bread light (high additive burden); plain bread modified starch excluded per signal-based gate unless position ≥ 4 or light/diet signal |
| cracker | Yes | Savoury biscuits with emulsifier additions |
| dessert | Yes | Puddings, mousses, ice cream |
| cereal | Yes | Breakfast cereals with texture additives |
| whole_food_fat | Yes | Nut butters with emulsifiers (palm oil + mono/diglycerides) |
| crispbread | Yes | Some crispbread products with stabilisers |
| yogurt | Yes | Stabilised yogurts (carrageenan, modified starch, pectin) |
| default | Yes | Catch-all |

No category is excluded — emulsifiers/stabilisers can appear in any category. The modified-starch gate is signal-based (position ≥ 4 or light/diet signal per §2.2), not category-scoped.

---

## 8. Implementation Requirements

### 8.1 Taxonomy extension

Add the following entries to `ingredient_taxonomy._ADDITIVES`:

- `mono_diglyceride` (E471) → `additive_class="emulsifier_medium"`
- `datem` (E472e) → `additive_class="emulsifier_medium"`
- `ssl` (E481) → `additive_class="emulsifier_medium"`
- `pgpr` (E476) → `additive_class="emulsifier_medium"`
- `pectin` (E440) → `additive_class="emulsifier_low"`
- `guar_gum` (E412) → `additive_class="emulsifier_low"`
- `xanthan_gum` (E415) → `additive_class="emulsifier_low"`
- `locust_bean_gum` (E410) → `additive_class="emulsifier_low"`
- `agar` (E406) → `additive_class="emulsifier_low"`
- `gellan_gum` (E418) → `additive_class="emulsifier_low"`
- `sodium_alginate` (E401) → `additive_class="emulsifier_low"`
- `gum_arabic` (E414) → `additive_class="emulsifier_low"`
- `modified_starch_stabilizer` (E1400–E1450) → `additive_class="emulsifier_medium"` with signal-based gate (position ≥ 4 or product name has light/diet signal)

### 8.2 Signal extractor extension

Add new L3 signals:
- `tax_emulsifier_medium: list[str]` — mono/diglycerides, DATEM, SSL, PGPR, carrageenan (also tracked in concern), modified starch stabilisers
- `tax_emulsifier_low: list[str]` — lecithins, gums, pectin, agar, alginate, gellan

### 8.3 Engine constants

```
EMULSIFIER_COMPLEXITY = {
    "high_concern_weight":     5,   # −5 pts per high agent
    "medium_concern_weight":   3,   # −3 pts per medium agent
    "low_concern_weight":      1,   # −1 pts per low agent
    "complexity_moderate":     1,   # −1 for 2 agents
    "complexity_high":         3,   # −3 for 3+ agents
}
```

### 8.4 Engine scoring function

A new `_emulsifier_complexity(l3: dict) -> tuple[float, list[str]]` function that:
1. Collects agents from all three tiers
2. Deduplicates by canonical name
3. Computes highest individual penalty
4. Computes complexity tier and adjustment
5. Returns (total_penalty, notes)

### 8.5 Concern coordination contract update

Add a new `emulsifier_complexity` family:
- Max penalty budget: **8 points** (family-level cap on total complexity penalty)
- Supporting evidence factor for non-winning concerns in multi-family conflicts: **0.4**

Cross-family score floors belong in the concern coordination contract, not this family spec. The `emulsifier_complexity` family's max 8-pt penalty cannot single-handedly crater a product's score; any deeper score impact results from multi-family coordination governed by the contract.

---

## 9. Appendix: Full agent reference

| # | Canonical | E-number | Tier | F1 existing | Counted in complexity | Note |
|---|-----------|----------|------|-------------|----------------------|------|
| 1 | cmc | E466 | high | concern (−3) | Yes | Human RCT (Chassaing 2022) |
| 2 | polysorbate_80 | E433 | high | concern (−3) | Yes | Consistent mechanistic evidence |
| 3 | carrageenan | E407 | medium | concern (−3) | Yes | Food grade; degraded form is not food additive |
| 4 | mono_diglyceride | E471 | medium | — | Yes | NutriNet-Santé class-level signal |
| 5 | datem | E472e | medium | — | Yes | Sparse independent data |
| 6 | ssl | E481 | medium | — | Yes | ADI 20 mg/kg, exposure << ADI |
| 7 | pgpr | E476 | medium | — | Yes | Structurally distinct |
| 8 | modified_starch_stabilizer | E1400–E1450 | medium | — | Yes | Signal-gated: position ≥ 4 or light/diet signal |
| 9 | soy_lecithin | E322 | low | benign (+2) | Yes | Minimal microbiota impact |
| 10 | sunflower_lecithin | E322 | low | benign (+2) | Yes | Same E-number, different source |
| 11 | pectin | E440 | low | — | Yes | Soluble fibre, prebiotic |
| 12 | gum_arabic | E414 | low | prebiotic exempt | Yes | Bifidogenic |
| 13 | guar_gum | E412 | low | — | Yes | Soluble fibre |
| 14 | xanthan_gum | E415 | low | — | Yes | Fermentation-derived |
| 15 | locust_bean_gum | E410 | low | — | Yes | Dietary fibre |
| 16 | agar | E406 | low | — | Yes | Seaweed-derived |
| 17 | gellan_gum | E418 | low | — | Yes | Fermentation-derived |
| 18 | sodium_alginate | E401 | low | — | Yes | Not absorbed intact |
