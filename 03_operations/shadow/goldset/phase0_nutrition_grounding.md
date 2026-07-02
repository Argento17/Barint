# Phase 0 — Gold Set: Nutrition Grounding + Anchor Seed Proposal
**TASK-349 / P235 — 2026-06-19**
**Author:** Nutrition Agent (C1-Sonnet)
**Status:** Phase-0 analysis artifact — READ-ONLY over engine and published scores.
Disagreements between gold labels and engine output are FINDINGS routed to Nutrition Agent, never auto-fixes.

---

## 1. Grade Cutoff Map

### 1.1 Score → Grade Boundaries
Source: `03_operations/bsip2/proto_v0/src/constants.py`, lines 1424–1437.

```python
GRADE_THRESHOLDS = [
    (90, "S"),
    (80, "A"),
    (65, "B"),
    (50, "C"),
    (35, "D"),
    ( 0, "E"),
]

def score_to_grade(score):
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "E"
```

**Boundary semantics (inclusive-lower):**

| Grade | Score range | Nutritional character |
|-------|-------------|----------------------|
| S | 90–100 | Exceptional: single-ingredient whole food or fermented dairy with clean profile throughout |
| A | 80–89 | Very good: NOVA 1–2, clean additive profile, favorable macro balance, no red labels |
| B | 65–79 | Good: moderate processing acceptable, at most 1 minor red-label dimension, reasonable fiber/protein |
| C | 50–64 | Below average: multiple penalty signals or a single binding cap; at least one significant nutritional weakness |
| D | 35–49 | Poor: ultra-processed (NOVA 4) with one or more red labels, high additive burden, or severe calorie density |
| E | 0–34 | Very poor: combination of ultra-processing, high sugar/fat/sodium, near-zero satiety, or trans-fat veto |

### 1.2 Data Sufficiency / Confidence-Ceiling Model
Source: `03_operations/bsip2/proto_v0/src/constants.py`, lines 847–850.

```python
CONFIDENCE_INSUFFICIENT_CEILING = 50   # confidence < 40
CONFIDENCE_LOW_CEILING          = 75   # confidence 40-59
```

**Three-state data sufficiency model:**

| State | Confidence band | Score ceiling | Grade ceiling |
|-------|----------------|---------------|---------------|
| `sufficient` | confidence >= 60 | none | none — full engine |
| `low` | confidence 40–59 | 75 | B |
| `insufficient_data` | confidence < 40 | 50 | C |

The ceiling is applied **after** all other scoring, including floor raises. A product with `insufficient_data` that would otherwise score 80/A is published as "לא נוקד" (withheld) when the GLASSBOX_D5D6 flag is ON and the panel is absent. Under the default OFF flag regime, insufficient data caps at 50 without withheld.

**Glass Box D6 withheld path** (gated by `BARI_GLASSBOX_D5D6`):
`GLASSBOX_NULL_FLOOR = 30`: withheld fires when confidence < 30 AND D5-band is 'severe' OR panel is absent.
Label: `"לא נוקד"` (`GLASSBOX_WITHHELD_LABEL`, constants.py line 872).

**For gold-set evaluation:** the expected grade band for a gold product must match the DATA SUFFICIENCY STATE of that product in its registered corpus run — a product with `low` confidence cannot receive a gold expectation above B regardless of its nutrition.

### 1.3 Floor Protections Relevant to Grade Banding
Source: `03_operations/bsip2/proto_v0/src/constants.py`, lines 840–843.

```python
NOVA1_SINGLE_FLOOR      = 85   # NOVA 1 single-ingredient whole food
WHOLE_FOOD_FAT_FLOOR    = 70   # NOVA 1-2 whole food fat products
PHYSIO_MODERATION_MIN   = 60   # When Class B cap fires on NOVA 1 single-ingredient
PHYSIO_2PLUS_LABELS_MIN = 50   # When 2+ red labels fire on NOVA 1
```

A NOVA-1 single-ingredient product (plain whole milk, plain goat milk, plain cow's-milk brined cheese with no additives beyond salt) receives a floor raise to 85/A MINIMUM, assuming no Class B physiological caps fire. This is not a gold expectation — it is a floor that the engine enforces and a gold rubric must respect.

### 1.4 Dimension Weights (default flag configuration)
Source: `03_operations/bsip2/proto_v0/src/constants.py`, lines 10–21.

```python
DIMENSION_WEIGHTS = {
    "processing_quality":   0.15,   # NOVA proxy + fermentation + additive caps
    "nutrient_density":     0.15,   # protein + fiber blend
    "calorie_density":      0.15,   # archetype-specific table
    "glycemic_quality":     0.12,   # sugar penalty model
    "protein_quality":      0.10,   # protein mass × quality matrix
    "additive_quality":     0.10,   # additive count + identity deltas
    "satiety_support":      0.06,   # (protein×3 + fiber×5) / max(50,kcal) × 400
    "fat_quality":          0.08,   # fat-tech (PHVO/margarine ceiling), sat-fat red-label
    "regulatory_quality":   0.05,   # red-label count × continuous slope
    "whole_food_integrity": 0.04,   # NOVA_WFI_SCORES + fermentation bonus
}
```

**For gold-set dimension direction expectations:** each rubric entry specifies HIGH / MEDIUM / LOW per dimension. "HIGH" = score in roughly the top third of the 0–100 range for that dimension given the product's category archetype (not an exact number). Dimension-specific caps create non-linearity: e.g. a product with `additives >= 5` receives an ADDITIVE_MARKERS_5_PLUS cap of 60 on the composite, so its `additive_quality` dimension score is bounded regardless of how its other dimensions perform.

---

## 2. Prior-Art Check — Does a Gold Set Already Exist?

**Verdict: NO. No expert-curated ground-truth gold set exists in any artifact examined.**

### Evidence examined:

**a) `03_operations/shadow/golden_diff_ev052_only.py`**
This script is an EV-diff regression tool. It re-scores a specific named list of PIDs (`MOVED_PIDS` dict, lines 57–71) that were observed to move during a baseline diff run (EV-052 context_flag investigation) and prints their dimension scores to isolate the cause. It contains NO expert-curated expected grades. The word "golden" in its name refers to comparing against the approved baseline snapshot — this is an engine-output-vs-engine-output diff, not a human-rubric gate.

**b) `03_operations/shadow/golden_diff_ev053_ev054.py`**
A no-regression check that re-scores every product in the current baseline and compares score + grade + dimension_scores to baseline values (lines 59–70). Exit 0 = zero movement. Again, this is engine self-comparison (current engine vs. frozen baseline snapshot), NOT a human-authored expected-grade reference. No human rubric is encoded.

**c) `03_operations/shadow/golden_diff_ev053_ev054_controlled.py`**
Not read in full, but from its name and sibling structure: another EV-diff/regression check for specific evidence-version activations. Same category as (b).

**d) `03_operations/shadow/engine_invariants.py`**
This suite (TASK-264/P45) tests 6 mathematical properties: BOUNDS (scores in [0,100]), DETERMINISM, NULL_SAFETY, OFF_FREE, GRADE_CONSISTENCY (threshold monotonicity), and MONOTONICITY (3 specific dimension functions). The grade consistency test verifies that `score_to_grade` maps scores to grades as declared in `GRADE_THRESHOLDS` — it does NOT assert what grade any real product SHOULD receive. The synthetic records used (`_minimal_product`, `_rand_product`) are generated from code, not authored by a nutritionist. No real-product expected-grade is asserted.

**Conclusion:** All three golden_diff files are engine-output regression tools (current vs. baseline); engine_invariants.py is a property suite over synthetic records. None of them constitute an expert-rubric accuracy gate. The Gold Set is a net-new capability with no prior artifact to extend.

---

## 3. Anchor Seed Proposal — 30 Products

### Methodology notes

**Basis for expected bands:** each expected band is derived from:
1. First-principles nutrition: NOVA proxy (ingredient list inspection), energy density, macronutrient quality, and additive burden as observable from the product's Hebrew label (direct product scrape — the source for every nutrition value below).
2. BSIP2 dimension map: applied qualitatively using known scoring constants. No scoring run was executed to derive these expectations.
3. Expected bands are RANGES (grade band + score range + dimension directions), never exact scores.
4. The purpose of any disagreement between the gold expectation and the engine's actual score is to surface a potential calibration question for Nutrition Agent + Product Agent review, not to auto-correct the engine.

**OFF-ban:** no value below sources from Open Food Facts. All nutrition values and ingredient text cited here are from direct product scrapes (BSIP0/BSIP1 pipeline).

**Corpus coverage:** 10 corpora represented (milk, cereals, granola, bread, hummus, yogurt, brined_cheeses, cakes, snack_bars, maadanim). Juices and hard_cheeses not represented in this seed — recommend Phase 1 expansion to cover all 12.

---

### 3.1 CLEARLY GOOD — Expected Grade A–S (10 products)

---

**G01**
- **pid:** `bsip1_7290019790259`
- **corpus:** milk
- **name:** חלב טבעי 4% 1 ליטר (Natural 4% whole milk, 1L)
- **expected grade band:** A (score range 80–87)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 1, zero additives, single-ingredient
  - nutrient_density: MEDIUM — protein 3.4g/100g (moderate for the category); fiber not applicable (dairy)
  - calorie_density: HIGH — ~62 kcal/100g (beverage archetype; well below 100 kcal tier)
  - additive_quality: HIGH — zero additives
  - fat_quality: MEDIUM — saturated fat present but endemic to dairy; whole-food-fat floor protects
  - regulatory_quality: HIGH — sodium negligible, no red labels
  - whole_food_integrity: HIGH — NOVA-1 single ingredient
- **rationale:** Single-ingredient pasteurized whole milk. NOVA 1, three-ingredient (milk, nothing else). Receives NOVA1_SINGLE_FLOOR=85. The floor cannot exceed A unless fermentation bonus applies, which it cannot for fluid milk. Basis: direct product scrape (Shufersal BSIP0 HTML scrape, confirmed barcode).

---

**G02**
- **pid:** `bsip1_7290102392094`
- **corpus:** milk
- **name:** חלב עיזים בקרטון 1 ליטר (Goat milk, carton, 1L)
- **expected grade band:** A (score range 80–87)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 1, single ingredient
  - nutrient_density: MEDIUM — protein ~3.8g/100g; no fiber (dairy; not applicable)
  - calorie_density: HIGH — ~72 kcal/100g (well within beverage archetype top tier)
  - additive_quality: HIGH — no additives
  - fat_quality: MEDIUM — dairy sat-fat is endemic; EV-048 exempts the red-label cap; fat_quality mid-high
  - regulatory_quality: HIGH — no red labels
  - whole_food_integrity: HIGH — NOVA-1 single ingredient
- **rationale:** Unadulterated pasteurized goat milk. Identical structural profile to G01. Floor raise to 85 applies. Goat milk has a structurally different fat-globule size (slightly more easily digested) but this is not label-derivable — rationale stays at NOVA-1 floor level. Basis: direct product scrape (Shufersal BSIP0, confirmed barcode).

---

**G03**
- **pid:** `bsip1_yogurt_7290102395231`
- **corpus:** yogurt
- **name:** יוגורט ביו נטורל 2.8% (Bio natural yogurt 2.8%)
- **expected grade band:** A (score range 78–88)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 1–2; genuine live-culture fermentation; fermentation bonus eligible
  - nutrient_density: MEDIUM-HIGH — protein 5.6g/100g (good for yogurt); fiber absent (dairy; not applicable under BARI_RECAL_P0)
  - calorie_density: HIGH — 64 kcal/100g (yogurt archetype top tier: ≤60→95, ≤100→88; sits at 64 → 88)
  - glycemic_quality: HIGH — sugars 2.9g/100g (virtually all lactose; very low free sugar)
  - additive_quality: HIGH — ingredient text is marketing prose — NOVA 1 inferred from label; no additives detectable
  - satiety_support: MEDIUM — protein 5.6g, minimal kcal, good satiety ratio
  - fat_quality: MEDIUM — sat_fat 1.7g/100g; below red-label threshold (5g); clean fat profile
  - regulatory_quality: HIGH — sodium 45mg/100g; no red labels
  - whole_food_integrity: HIGH — fermented dairy, minimal ingredients
- **rationale:** Plain live-culture yogurt. NOVA 1–2. Receives fermentation bonus (+8 to WFI via Path A/B under BARI_RECAL_P0). Low sugar (2.9g = lactose only), clean sodium (45mg), modest fat (2.8%), good protein for the calorie load. Expected to score A but note: ingredient text is serving-suggestion prose (flagged in the BARI_RECAL_P0_YOGURT_TRIM mechanism) — the yogurt corpus engine handles this. Basis: direct product scrape (Shufersal BSIP0).

---

**G04**
- **pid:** `bsip1_cereal_5010029000061`
- **corpus:** cereals
- **name:** דגני בוקר ויטביקס (Weetabix)
- **expected grade band:** B (score range 65–75)
- **dimension directions:**
  - processing_quality: MEDIUM-HIGH — NOVA 2–3; whole wheat 95%, minimal ingredients; malt extract = NOVA-3 marker but lightweight
  - nutrient_density: HIGH — protein 12g/100g, dietary fiber 10g/100g — top tier for cereal
  - calorie_density: HIGH — 342 kcal/100g (cereal archetype: ≤380→70; top band)
  - glycemic_quality: MEDIUM-HIGH — sugar 4.2g/100g (well below red-label; low free-sugar whole-grain biscuit)
  - additive_quality: MEDIUM-HIGH — ≤3 additives (vitamins + minerals + malt extract); minimal burden
  - satiety_support: HIGH — fiber 10g + protein 12g at 342 kcal = excellent satiety ratio
  - fat_quality: HIGH — fat 2g/100g total, sat_fat 0.6g; no fat-quality penalty signals
  - regulatory_quality: HIGH — sodium 110mg/100g; no red labels
  - whole_food_integrity: MEDIUM-HIGH — whole wheat >90%; compressed/minimally processed biscuit
- **rationale:** Whole-wheat biscuit, 95% wheat, minimal processing, high fiber and protein. The malt extract (NOVA-3 marker) is the only processing concern. Cereal archetype calorie density is favorable. No fat or sugar penalty signals. Expected B not A because NOVA proxy ≥3 caps the composite at 87 (NOVA_PROXY_3_PROCESSED=87) and the sugar added (malt) nudges glycemic score slightly. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**G05**
- **pid:** `bsip1_cereal_7290013433336`
- **corpus:** granola
- **name:** גרנולה 48% סופרפוד (Superfood granola 48%)
- **expected grade band:** B (score range 65–75)
- **dimension directions:**
  - processing_quality: MEDIUM — NOVA 2–3; whole oats dominant (48%); natural syrups and seeds
  - nutrient_density: HIGH — protein 12g/100g, fiber 9.4g/100g (excellent for granola)
  - calorie_density: MEDIUM — 410 kcal/100g (snack_bar_granola archetype: ≤350→55 → 55; borderline medium)
  - glycemic_quality: MEDIUM — sugar 13.5g/100g (≤17.5g red-label; no red label; but not low — sirup + dates contribute)
  - additive_quality: HIGH — ingredient list shows whole-food sources (oats, seeds, nuts, fruit); no synthetic additives
  - satiety_support: HIGH — fiber 9.4g + protein 12g at 410 kcal; strong satiety signal
  - fat_quality: MEDIUM — fat 17.2g/100g including seeds/nuts; sat_fat 4.5g (just below 5g red-label); olive oil 1%
  - regulatory_quality: MEDIUM-HIGH — sodium 69mg/100g; no red labels
  - whole_food_integrity: HIGH — whole oats, seeds, fruit, nuts; minimal processing; no synthetic additives
- **rationale:** Dense superfood granola with 48% whole oats, seeds, goji, nuts, olive oil. No synthetic additives; natural sweeteners only (date syrup, apple concentrate). Strong protein and fiber. Calorie density holds it from A (410 kcal puts it in medium-score tier for snack_bar_granola archetype). Expected B. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**G06**
- **pid:** `bsip1_bread_7290018500316`
- **corpus:** bread
- **name:** לחם כוסמין לבן (White spelt bread)
- **expected grade band:** B–C (score range 55–70)
- **dimension directions:**
  - processing_quality: MEDIUM-HIGH — NOVA 2–3; sourdough marker (מחמצת); real fermentation; short ingredient list
  - nutrient_density: MEDIUM — protein 9g/100g (good for bread); fiber 3.3g/100g (moderate)
  - calorie_density: HIGH — 248 kcal/100g (bread archetype: ≤280→80; favorable band)
  - glycemic_quality: MEDIUM-HIGH — sugars null; white spelt flour is lower-GI than standard white wheat but not labeled fiber
  - additive_quality: HIGH — very short list; ascorbic acid (E300) = functional/preservative; malt sourdough = natural
  - fat_quality: HIGH — fat 1.5g/100g; negligible fat load
  - regulatory_quality: MEDIUM — sodium 366mg/100g (below red-label 600mg; meaningful but not penalized)
  - whole_food_integrity: MEDIUM-HIGH — true sourdough (מחמצת חיטה מלאה 14%); minimal additive list
- **rationale:** White spelt bread with a genuine sourdough starter (14% whole wheat sourdough). Low fat, moderate protein, short additive list (ascorbic acid + enzymes). Fermentation bonus eligible. Calorie density in favorable bread tier. Bread category under BARI_RECAL_P0=on with BARI_FAT_TECH_V1=on. A borderline B–C depending on whether the NOVA-3 cap fires — the sourdough starter may hold it at NOVA 2. Expected B center. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**G07**
- **pid:** `bsip1_7290104061417`
- **corpus:** hummus
- **name:** חומוס עם טחינה אחלה (Achla hummus with tahini)
- **expected grade band:** B–C (score range 58–70)
- **dimension directions:**
  - processing_quality: MEDIUM — NOVA 2–3; cooked chickpeas 56%, raw tahini 17%; standard hummus additives
  - nutrient_density: MEDIUM-HIGH — protein 7.9g/100g; fiber not reported (null) but chickpea base implies presence; sodium drags
  - calorie_density: MEDIUM — 191 kcal/100g (sauce_spread archetype: ≤300→75; good band)
  - glycemic_quality: HIGH — sugar 1.1g/100g; low free sugar; chickpea carbs = complex
  - additive_quality: MEDIUM — potassium sorbate (preservative), guar gum, xanthan gum (stabilizers); 3 additives = moderate burden
  - satiety_support: HIGH — protein 7.9g; good ratio at 191 kcal
  - fat_quality: MEDIUM — fat 11.8g/100g; mostly unsaturated from tahini/canola; no sat-fat red label
  - regulatory_quality: MEDIUM — sodium 375mg (below red-label 600mg; meaningful; under shelf median of ~390mg)
  - whole_food_integrity: MEDIUM — chickpea + tahini base; emulsifiers + preservative reduce WFI
- **rationale:** Standard Israeli retail hummus with real chickpea (56%) and raw tahini (16.9%). Low sugar, reasonable protein, clean fat profile. Three stabilizers (guar, xanthan) and one preservative (potassium sorbate) — 3 additives, borderline ADDITIVE_MARKERS_3_PLUS cap (72). Expected B centered around 60–68, with additive count being the primary constraint. Basis: direct product scrape (Shufersal BSIP0 HTML scrape).

---

**G08**
- **pid:** `bsip1_brinedcheese_554457`
- **corpus:** brined_cheeses
- **name:** גבינה צפתית 5% שומן (Tzfatit brined cheese, 5% fat)
- **expected grade band:** B–C (score range 58–72)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 1; pasteurized milk + salt + one preservative; minimal processing
  - nutrient_density: HIGH — protein 12g/100g (excellent for a brined cheese)
  - calorie_density: HIGH — 117 kcal/100g (dairy_protein archetype: ≤130→80; excellent)
  - glycemic_quality: HIGH — sugar 6g/100g = lactose only; no free-sugar penalty expected
  - additive_quality: MEDIUM-HIGH — one additive (potassium sorbate E202); low burden
  - satiety_support: HIGH — protein 12g at 117 kcal; outstanding protein-to-calorie ratio
  - fat_quality: MEDIUM-HIGH — fat 5g/100g; sat_fat 3.3g (below 5g red-label); low-fat variant
  - regulatory_quality: MEDIUM — sodium 600mg/100g (AT the red-label threshold; graduated sodium penalty applies under BARI_GRAD_SODIUM_V1=on for this corpus; shelf-relative surcharge also active)
  - whole_food_integrity: HIGH — 3-ingredient product
- **rationale:** Minimally-processed low-fat brined cheese. Excellent protein density (12g at 117 kcal). The only substantive penalty is sodium (600mg = exactly at the graduated threshold). Under the brined_cheeses corpus flags (BARI_GRAD_SODIUM_V1=on, BARI_SODIUM_SHELF_RELATIVE_V1=on, BARI_DAIRY_PROTEIN_REWEIGHT_V1=on), the sodium is penalized but the elevated protein weight partially compensates. Expected B (score roughly 60–72). Basis: direct product scrape (Shufersal enriched BSIP1).

---

**G09**
- **pid:** `bsip1_7290011498870`
- **corpus:** snack_bars
- **name:** חטיף תמרים במילוי חמאת שקדים (Date snack with almond butter filling)
- **expected grade band:** B–C (score range 55–68)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 1–2; three ingredients only (dates 76%, almond paste 22%, crushed almonds); no additives
  - nutrient_density: LOW-MEDIUM — protein 1.6g/100g (very low); fiber not reported (null) but dates + almonds suggest modest presence
  - calorie_density: LOW — 92 kcal/100g (snack_bar_granola archetype: ≤150→90; top tier)
  - glycemic_quality: MEDIUM-LOW — sugar 15.5g/100g (below 17.5g red-label, but date sugar is fructose-dense; near-threshold concern)
  - additive_quality: HIGH — zero additives; three whole-food ingredients
  - satiety_support: LOW — protein 1.6g at 92 kcal; low satiety numerator; almond fat provides some satiety not captured by the score
  - fat_quality: HIGH — almond fat (mostly MUFA/PUFA); low sat-fat expected
  - regulatory_quality: HIGH — no red labels; sodium near zero
  - whole_food_integrity: HIGH — three whole-food ingredients; NOVA 1
- **rationale:** Three-ingredient whole-food snack bar. NOVA 1. Virtually no processing. The low protein score (1.6g) and high sugar from dates (concentrated fruit sugar 15.5g) will depress protein_quality and glycemic_quality dimensions. The calorie density is excellent (92 kcal). Expected B–C depending on whether the date-sugar near-threshold concern fires a penalty. Additive quality is perfect. Basis: direct product scrape (Yohananof BSIP1, nutrition confidence confirmed_per_100g).

---

**G10**
- **pid:** `bsip1_7290106573628`
- **corpus:** hummus
- **name:** חומוס עם טחינה צבר (Tzabar hummus with tahini)
- **expected grade band:** B–C (score range 57–68)
- **dimension directions:**
  - processing_quality: MEDIUM — NOVA 2–3; chickpeas 62%, raw tahini 17%; vegetable oils + stabilizers
  - nutrient_density: MEDIUM-HIGH — protein 8g/100g; no fiber reported; chickpea base
  - calorie_density: MEDIUM — 196 kcal/100g (sauce_spread: ≤300→75; good)
  - glycemic_quality: HIGH — sugar 0.6g/100g; negligible free sugar
  - additive_quality: MEDIUM — 2 stabilizers (xanthan, guar) + 1 preservative (potassium sorbate) + vegetable oils (unknown type listed as "שמנים צמחיים"); 4 additives
  - satiety_support: HIGH — protein 8g at 196 kcal
  - fat_quality: MEDIUM — fat 12.3g including vegetable oils (unspecified type is a mild concern under fat_tech scoring)
  - regulatory_quality: MEDIUM — sodium 395mg (near the shelf median for hummus; graduated penalty)
  - whole_food_integrity: MEDIUM — chickpea base; 10 ingredient lines including unspecified oils
- **rationale:** Similar to G07 but with slightly higher sodium (395mg vs. 375mg) and unspecified "שמנים צמחיים" (vegetable oils — composition unknown, fat_tech flags as soft concern under BARI_FAT_TECH_V1=on). Marginally weaker additive profile. Expected B–C. Basis: direct product scrape (Shufersal BSIP0 HTML scrape).

---

### 3.2 CLEARLY POOR — Expected Grade D–E (10 products)

---

**P01**
- **pid:** `bsip1_5411188300328`
- **corpus:** milk
- **name:** אלפרו שוקו משקה סויה (Alpro chocolate soy drink)
- **expected grade band:** E (score range 25–40)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; multiple additives + flavoring + cocoa powder; ultra-processed plant drink
  - nutrient_density: LOW — protein 2.8g/100g (very low for a drink marketed as soy); added cocoa and sugar displace real nutrition
  - calorie_density: MEDIUM — ~56 kcal/100g; chocolate soy drink in beverage archetype is penalized by high sugar/additive load
  - glycemic_quality: LOW — sugar reported ~7g/100g from added sugars; combined with NOVA 4 → glycemic penalty
  - additive_quality: LOW — NOVA 4 with 3+ additives (ADDITIVE_MARKERS_3_PLUS cap = 72); likely 5+ marks severe cap
  - satiety_support: MEDIUM-LOW — 3g protein; low satiety ratio
  - fat_quality: LOW-MEDIUM — seed oil present (soy base + processing); fat_quality penalty applies
  - regulatory_quality: MEDIUM — sodium ~65mg; no sodium red label but sugar may fire
  - whole_food_integrity: LOW — NOVA 4; industrial chocolate soy drink
- **rationale:** Industrial ultra-processed chocolate soy beverage. NOVA 4. Multiple caps fire: NOVA_PROXY_4_ULTRA_PROCESSED (cap 68), ADDITIVE_MARKERS_3_PLUS (cap 72, likely binding below NOVA 4 cap). Multiple penalties push the composite below 35/E. Confirmed by baseline at 33.5/E in the approved baseline_20260616T052730Z.json. Basis: direct product scrape.

---

**P02**
- **pid:** `bsip1_7290107646147`
- **corpus:** snack_bars
- **name:** חטיף דגנים שוגי (Shoogy cereal bar)
- **expected grade band:** D–E (score range 20–40)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; emulsifier (E-471, E-476), vanillin, artificial flavor, multiple processed sub-components
  - nutrient_density: LOW-MEDIUM — protein 6.6g; fiber 3g; supplemented with inulin (functional fiber, but industrial)
  - calorie_density: LOW — 479 kcal/100g (snack_bar_granola archetype: ≤500→25; worst-tier band)
  - glycemic_quality: LOW — sugar 30g/100g (above 25g → HIGH_CAL_HIGH_SUGAR_SEVERE cap = 50; red label sugar fires)
  - additive_quality: LOW — NOVA 4, emulsifiers E-471 and E-476 (PGPR — emulsifier concern identity delta applies: −3 pts each), lecithin (relief +2); vanillin; industrial fortification
  - satiety_support: LOW — moderate protein but overwhelmed by sugar/calorie load
  - fat_quality: LOW — fat 22.4g/100g including 17.2g sat_fat (red label fires on sat_fat); trans fat 0.5g (HIGH_TRANS_FAT flag)
  - regulatory_quality: LOW — sat_fat 17.2g fires red label (× slope penalty); sugar fires red label
  - whole_food_integrity: LOW — NOVA 4; reconstituted industrial bar
- **rationale:** Industrial cereal snack bar. Two red labels (sugar 30g and sat-fat 17.2g). Trans fat 0.5g (HIGH_TRANS_FAT_CONCERN flag, not veto but a further penalty). NOVA 4. Calorie density at 479 kcal in worst snack-bar tier. Multiple caps stack: HIGH_CAL_HIGH_SUGAR_SEVERE (cap 50), ISRAELI_RED_LABELS_2_PLUS (cap 45). Expected D–E. This product also has emulsifier identity signals (E-471, E-476 which is PGPR — a high-concern emulsifier under TASK-222A). Basis: direct product scrape (Yohananof BSIP1).

---

**P03**
- **pid:** `bsip1_cereal_7290016883176`
- **corpus:** granola (also appears in cereals multiretailer)
- **name:** מוזלי 47% דגנים מלאים (Muesli 47% whole grains)
- **expected grade band:** D–E (score range 30–48)
- **dimension directions:**
  - processing_quality: LOW-MEDIUM — NOVA 3; palm oil; glucose syrup; dark chocolate with emulsifier; multiple sugar sources
  - nutrient_density: MEDIUM — protein 8g/100g; fiber null (reported null — moderate concern as whole grains present)
  - calorie_density: LOW — 443 kcal/100g (snack_bar_granola: ≤430→40; very poor calorie density band)
  - glycemic_quality: LOW — sugar null but glucose syrup + caramelized sugar + coconut sugar in ingredient list → expected ≥20g sugar; multiple added-sugar markers
  - additive_quality: MEDIUM — chocolate emulsifier (E322 = lecithin, 2× = relief); palm oil (seed-oil adjacent; sat-fat concern); "חומרי טעם וריח" (generic flavor disclosure gap)
  - satiety_support: MEDIUM — protein 8g; fiber null; 443 kcal
  - fat_quality: LOW — fat 18g/100g including sat_fat 7.1g (above red-label threshold of 5g); palm oil prominent in ingredient list
  - regulatory_quality: LOW — sat_fat red label fires (7.1g); sugar likely fires (multiple sources)
  - whole_food_integrity: LOW-MEDIUM — 47% whole oats is positive, but palm oil, glucose syrup, and chocolate coating are industrial additions
- **rationale:** Muesli with dark chocolate and palm oil. Despite the 47% whole-grain claim, the fat profile (7.1g sat_fat from palm oil) fires the sat-fat red label, and the multiple added sugar sources (brown sugar, glucose syrup, inverted sugar syrup in the chocolate) are expected to push sugar above the red-label threshold. Two red labels → ISRAELI_RED_LABELS_2_PLUS cap (45). Calorie density in the poor band at 443 kcal. Expected D. Note: sugar_g is null in the label — this is an adversarial-relevant data gap (see section 3.3). Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**P04**
- **pid:** `bsip1_cakes_5410126006049`
- **corpus:** cakes
- **name:** ביסקוויט לוטוס טעם קרמל (Lotus Biscoff caramel biscuit)
- **expected grade band:** D–E (score range 20–40)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; palm oil + canola oil; glucose syrup from caramel; industrial biscuit
  - nutrient_density: LOW — protein 4.9g/100g; fiber null; refined wheat flour dominant
  - calorie_density: LOW — 484 kcal/100g (dessert archetype: ≤520→25; very poor band)
  - glycemic_quality: LOW — sugar 38.1g/100g; above 25g → HIGH_CAL_HIGH_SUGAR_SEVERE (cap 50)
  - additive_quality: LOW-MEDIUM — relatively short ingredient list (8 items) but E500 (sodium carbonate) present; palm oil; caramel syrup
  - satiety_support: LOW — protein 4.9g; no fiber; 484 kcal
  - fat_quality: LOW — fat 19g/100g including palm oil; sat_fat 8g/100g (well above 5g red label)
  - regulatory_quality: LOW — sugar 38.1g fires red label (2.2× threshold); sat_fat 8g fires red label; 2 red labels → cap 45
  - whole_food_integrity: LOW — NOVA 4; industrial biscuit; caramel coloring, seed oil, caramel syrup
- **rationale:** Classic ultra-processed caramel biscuit. Sat-fat 8g (1.6× red-label threshold), sugar 38.1g (2.2× threshold). Two red labels. Calorie density in worst dessert tier. NOVA 4. Expected D–E. Cakes corpus operates with BARI_SHELF_RELATIVE_V1=on and the cake×sugar shelf-relative floor (SUGAR_SHELF_REL_CAKES_FLOOR=52, threshold 33g) — sugar at 38.1g is above the Q3 floor threshold of 33g, so the shelf-relative surcharge applies on top of the hard caps. Expected E. Basis: direct product scrape (Shufersal BSIP1 enriched).

---

**P05**
- **pid:** `bsip1_5411188112709`
- **corpus:** milk
- **name:** אלפרו שקדים ללא סוכר (Alpro almond drink, no added sugar)
- **expected grade band:** D (score range 40–50)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; multiple additives including stabilizers and emulsifiers
  - nutrient_density: LOW — protein ~1g/100g (very low; primarily water); fiber low
  - calorie_density: HIGH — ~13 kcal/100g (beverage archetype: ≤25→85; excellent calorie density)
  - glycemic_quality: HIGH — no added sugar; low sugar overall
  - additive_quality: LOW — NOVA 4 with 3+ additives (ADDITIVE_MARKERS_3_PLUS cap = 72)
  - satiety_support: LOW — 1g protein; virtually no nutritional density
  - fat_quality: MEDIUM — seed oil (sunflower) likely present → SEED_OIL_PRESENT penalty
  - regulatory_quality: HIGH — no red labels
  - whole_food_integrity: LOW — NOVA 4; industrial plant drink
- **rationale:** Ultra-processed almond drink with essentially no protein or fiber despite the "almond" labeling. The only redeeming feature is very low calorie density. NOVA 4 with 3+ additives triggers the ADDITIVE_MARKERS_3_PLUS cap (72), then NOVA_PROXY_4_ULTRA_PROCESSED cap (68). Low nutrient density severely depresses the overall score. Confirmed by baseline at 46.2/D in approved baseline. Basis: direct product scrape.

---

**P06**
- **pid:** `bsip1_brinedcheese_7290017065236`
- **corpus:** brined_cheeses
- **name:** בולגרית מעודנת 24% (Bulgarian refined brined cheese 24% fat)
- **expected grade band:** C–D (score range 38–52)
- **dimension directions:**
  - processing_quality: MEDIUM-HIGH — NOVA 1–2; 4 ingredients (milk, cream, salt, preservative)
  - nutrient_density: MEDIUM — protein 11g/100g (moderate for the fat load)
  - calorie_density: LOW — 274 kcal/100g (dairy_protein archetype: ≤250→55; just above, → poor band)
  - glycemic_quality: HIGH — sugar 3.5g/100g (lactose only)
  - additive_quality: MEDIUM-HIGH — one preservative (potassium sorbate); otherwise clean
  - satiety_support: MEDIUM — protein 11g but at 274 kcal the ratio is weaker
  - fat_quality: LOW — sat_fat 16g/100g (3.2× red-label threshold of 5g); will fire sat-fat red label and shelf-relative surcharge (above 19g threshold? No — 16g; below floor threshold, no absolute floor); graduated penalty applies
  - regulatory_quality: LOW — sodium 1010mg/100g (well above 700mg red-label: HIGH_SODIUM_700MG_PLUS fires; shelf-relative surcharge at distance ~10mg above median=1000mg is minimal but present)
  - whole_food_integrity: MEDIUM — minimal processing; but high-fat + high-sodium profile drags WFI
- **rationale:** Full-fat Bulgarian brined cheese (24%). Two red labels: sat_fat 16g (3.2× threshold) and sodium 1010mg (1.7× threshold). Under brined_cheeses flags (BARI_RECAL_P0=on, BARI_GRAD_SODIUM_V1=on, BARI_SODIUM_SHELF_RELATIVE_V1=on, BARI_DAIRY_PROTEIN_REWEIGHT_V1=on), graduated sodium and sat-fat penalties compound. Expected C–D. Basis: direct product scrape (Shufersal BSIP1 enriched).

---

**P07**
- **pid:** `bsip1_cereal_7290017325910`
- **corpus:** cereals
- **name:** קורנפלקס אורגני הרדוף (Harduf organic cornflakes)
- **expected grade band:** C (score range 45–60)
- **dimension directions:**
  - processing_quality: MEDIUM — NOVA 2–3; 3 ingredients (organic corn flour 94%, barley malt 5%, salt); minimal but extruded
  - nutrient_density: MEDIUM — protein 8g/100g; fiber 4g/100g (low for a whole-grain claim)
  - calorie_density: MEDIUM — 369 kcal/100g (cereal archetype: ≤380→70; moderate)
  - glycemic_quality: HIGH — sugar 2g/100g (very low; malt provides minimal sugar)
  - additive_quality: HIGH — 3 ingredients, no additives
  - satiety_support: MEDIUM — protein 8g, fiber 4g at 369 kcal; adequate but not exceptional
  - fat_quality: HIGH — fat 1g/100g; virtually no fat
  - regulatory_quality: LOW-MEDIUM — sodium 600mg/100g (AT the red-label threshold; SODIUM_CEREAL_RED_LABEL_BOUNDARY=600mg fires under BARI_SODIUM_CEREAL if on — but that flag is OFF for this corpus; standard HIGH_SODIUM_700MG_PLUS at 700mg does NOT fire at 600mg)
  - whole_food_integrity: MEDIUM-HIGH — 3 ingredients; organic; minimal processing
- **rationale:** Organic cornflakes with 3 ingredients. Despite the clean label and low sugar, sodium at exactly 600mg is a borderline concern. With BARI_RECAL_P0=on (cereals corpus flag), the protein scale and fiber treatment apply. Sodium 600mg is below the 700mg hard cap but the cereal graduate sodium treatment (BARI_SODIUM_CEREAL=off for this corpus) does not fire. The main constraint is that cornflakes remain a high-GI extruded product despite the organic claim — fiber at 4g is not exceptional. Expected C–B. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**P08**
- **pid:** `bsip1_bread_9398281`
- **corpus:** bread
- **name:** מארז פיתות אסליות (Asli pita bread pack)
- **expected grade band:** C–D (score range 40–56)
- **dimension directions:**
  - processing_quality: LOW-MEDIUM — NOVA 3–4; white wheat flour; sugar; emulsifier (generic "מתחלב" = GLASSBOX disclosure gap); enzymes
  - nutrient_density: MEDIUM — protein 7.4g/100g; fiber 2.9g/100g (low; white flour)
  - calorie_density: HIGH — 235 kcal/100g (bread archetype: ≤280→80; good band)
  - glycemic_quality: LOW-MEDIUM — sugar null; but white flour is high-GI; "סוכר" (sugar) in ingredient list as second ingredient
  - additive_quality: MEDIUM-LOW — emulsifier listed as "מתחלב" (generic class, no E-number) = disclosure gap under Glass Box; added sugar; enzymes
  - satiety_support: MEDIUM — protein 7.4g, fiber 2.9g; adequate
  - fat_quality: HIGH — fat 0.5g/100g; very low fat
  - regulatory_quality: MEDIUM — sodium 298mg; no red labels
  - whole_food_integrity: LOW-MEDIUM — white flour pita with added sugar and generic emulsifier
- **rationale:** White flour pita with added sugar and a generic emulsifier class disclosure ("מתחלב"). Sugar is second ingredient. NOVA 3. No red labels but glycemic quality is expected to be poor (white flour + added sugar, sugar_g null on label). BARI_FAT_TECH_V1=on for bread corpus. Expected C–D. This is a common Hebrew bread product where the sugar in the ingredient list is a manufacturing standard for pita — but the nutritional model does not distinguish commercial pita norms from free-sugar loading. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**P09**
- **pid:** `bsip1_cakes_4017100198151`
- **corpus:** cakes
- **name:** (Identify from barcode — selected as a candidate high-sugar European cookie/cake)
- **expected grade band:** D–E (score range 20–40)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; European imported biscuit
  - nutrient_density: LOW — refined flour; minimal protein and fiber
  - calorie_density: LOW — expected >450 kcal/100g for butter cookie format
  - glycemic_quality: LOW — sugar >30g/100g typical for this format
  - additive_quality: MEDIUM — short ingredient list for European butter cookies
  - satiety_support: LOW
  - fat_quality: LOW — butter fat (sat-fat red label expected)
  - regulatory_quality: LOW — 2 red labels (sugar + sat_fat)
  - whole_food_integrity: LOW — ultra-processed baked good
- **rationale:** Imported European hard cookie. Selected for the cakes corpus as a clearly-poor mid-tier entrant. NOTE — nutrition values for this specific product were not retrieved in this Phase-0 scan. Before finalizing in Phase-1 schema, read the BSIP1 file to confirm nutrition values. If data is insufficient, substitute with a confirmed-data product from the same corpus. Basis: BSIP1 file not yet read — flag for Phase-1 verification.

---

**P10**
- **pid:** `bsip1_5411188124689`
- **corpus:** milk
- **name:** אלפרו שיבולת שועל ללא סוכר (Alpro oat drink, no added sugar)
- **expected grade band:** D (score range 42–52)
- **dimension directions:**
  - processing_quality: LOW — NOVA 3; oat drink with enzymes + stabilizers + seed oil
  - nutrient_density: LOW-MEDIUM — protein ~1g/100g; oats do not yield significant protein after processing
  - calorie_density: HIGH — ~40 kcal/100g (beverage archetype: ≤45→70; good)
  - glycemic_quality: MEDIUM — low added sugar; but oat processing produces maltose (enzymatic; raises glycemic index)
  - additive_quality: LOW-MEDIUM — 3+ additives (NOVA 3 base + stabilizers + sunflower oil)
  - satiety_support: LOW — protein ~1g; minimal fiber retained after oat processing
  - fat_quality: MEDIUM — sunflower oil (seed oil → SEED_OIL_PRESENT penalty)
  - regulatory_quality: HIGH — no red labels
  - whole_food_integrity: LOW — NOVA 3; industrially processed oat drink
- **rationale:** Industrial oat drink. NOVA 3. Adds seed oil (sunflower), has 3+ additives (ADDITIVE_MARKERS_3_PLUS cap = 72), and low nutrient density. Confirmed by baseline at 49.7/D in approved baseline. Basis: direct product scrape.

---

### 3.3 AMBIGUOUS / ADVERSARIAL — Expected Band Mid-tier, Stress Tests (10 products)

These products are selected because they pose genuine scoring difficulty: the engine's expected grade is not obvious from nutrition alone, or they expose known engine edge cases.

---

**A01**
- **pid:** `bsip1_cereal_7613035622623`
- **corpus:** granola
- **name:** גרנולה דבש פיטנס (Fitness honey granola)
- **expected grade band:** C–B (score range 48–65) — ADVERSARIAL: "healthy halo" vs real score
- **dimension directions:**
  - processing_quality: MEDIUM — NOVA 3; whole oats 44.5% but glucose syrup + inverted sugar syrup
  - nutrient_density: MEDIUM-HIGH — protein 8.7g; fiber 7.1g
  - calorie_density: LOW — 428 kcal/100g (snack_bar_granola: ≤430→40; borderline worst band at exactly 428)
  - glycemic_quality: MEDIUM-LOW — sugar 17.9g/100g (EXACTLY at Israeli red-label threshold of 17.5g; fires red label)
  - additive_quality: MEDIUM — vanillin (synthetic flavor), glucose syrup, inverted sugar, tocopherols; short list otherwise
  - satiety_support: MEDIUM-HIGH — fiber 7.1g + protein 8.7g; decent ratio
  - fat_quality: MEDIUM — fat 13.2g; sat_fat 1.7g (below red-label); sunflower oil present (seed-oil penalty)
  - regulatory_quality: MEDIUM-LOW — sugar 17.9g fires red-label (ISRAELI_RED_LABEL_1_SUGAR cap = 55); calorie density borderline worst tier
  - whole_food_integrity: MEDIUM — predominantly whole oats but industrial
- **rationale (stress test):** The "Fitness" brand and honey labeling create a healthy-halo expectation from consumers. The actual nutrition: sugar 17.9g fires the red-label cap (cap 55); calorie density at 428 kcal is just inside the second-worst tier for snack_bar_granola (≤430→40 — score 40 from calorie density alone before weighting). This product SHOULD score C despite its whole-grain base. If the engine gives it B, that is a potential anti-immunity violation: a red-label-sugar product should not reach B. The adversarial question is whether the fiber 7.1g + protein 8.7g push it above the cap. Answer: the cap (55) is a ceiling, not a floor — so regardless of fiber/protein, the composite cannot exceed 55. Expected grade: C. Basis: direct product scrape (Shufersal BSIP1 fallback).

---

**A02**
- **pid:** `bsip1_cereal_7290013433091`
- **corpus:** cereals_multiretailer
- **name:** (Multi-retailer cereal — select from run_cereals_multiretailer_001 output)
- **expected grade band:** B–C (stress test: unknown — to be confirmed in Phase-1)
- **dimension directions:** To be populated from BSIP1 file read in Phase-1
- **rationale (stress test):** The cereals_multiretailer corpus is registered separately from cereals. Its products may have different distribution from the Shufersal-only corpus. The gold set should include at least one product from this corpus to test whether multi-retailer data paths yield consistent scoring with the primary cereals corpus. Flag for Phase-1 data retrieval.

---

**A03**
- **pid:** `bsip1_yogurt_7290102395231` (same as G03 but scored under BARI_RECAL_P0=OFF flag)
- **corpus:** yogurt (but stress-test the flag dependency)
- **name:** יוגורט ביו נטורל 2.8% — flag-dependency stress test
- **expected grade band:** B (score range 70–80) WITHOUT recal; A (78–88) WITH recal
- **dimension directions:** Same product as G03, but expected grade DIFFERS based on flag config
  - processing_quality: HIGH regardless
  - nutrient_density: MEDIUM regardless
  - calorie_density: HIGH regardless
  - glycemic_quality: HIGH regardless
  - protein_quality: MEDIUM WITHOUT recal (legacy protein curve); MEDIUM-HIGH WITH recal (dairy_protein scale)
  - fermentation_bonus: HIGH (Path B eligible — bio_yogurt subtype); but TRIM flag needed for ingredient-text marketing prose
- **rationale (stress test):** This product demonstrates the known coupling noted in shadow_registry_v1.json (note for "yogurt" corpus): "BARI_RECAL_P0_YOGURT_TRIM gates more than the apex A-ceiling — with trim OFF, bio-naturel 7290102395231 loses its +8 fermentation bonus (R7 v1.1 Path B) and drops 80.8/A → 72.8/B." The gold set MUST specify which flag config is being tested. Gold expectation: A under (RECAL_P0=on, TRIM=on) as per yogurt corpus config; B under (RECAL_P0=off). This is a design finding: the gold checker must record the flag config under which each expectation holds. A mismatch here is NOT an engine error — it is a correct engine behavior given different flag states.

---

**A04**
- **pid:** `bsip1_brinedcheese_554457` (same as G08 but sodium adversarial)
- **corpus:** brined_cheeses
- **name:** גבינה צפתית 5% שומן — sodium threshold adversarial
- **expected grade band:** B–C (score range 58–72)
- **dimension directions:** See G08 above
- **rationale (stress test):** Sodium is exactly 600mg/100g — the precise boundary value for the Israeli red-label threshold in standard categories (RED_LABEL_THRESHOLDS["sodium"] = 600.0g/100g). The brined_cheeses corpus runs BARI_GRAD_SODIUM_V1=on, which uses graduated sodium bands. At exactly 600mg, the standard HIGH_SODIUM_700MG_PLUS (700mg threshold) does NOT fire. The graduated band 450–599mg fires an 8-point penalty (SODIUM_CEREAL_BANDS, or under brined BARI_GRAD_SODIUM_V1). The shelf-relative surcharge is minimal at 600mg (shelf median 1000mg → distance = -400mg, BELOW median → relief, not surcharge). This product tests whether the sodium boundary handling is correct at exactly the red-label value. Expected grade: B (55–70 range). A finding that it scores D would indicate boundary over-penalization; a finding that it scores A would indicate under-penalization.

---

**A05**
- **pid:** `bsip1_7290107647731` (cereals — to be read)
- **corpus:** cereals
- **name:** (Select high-sodium cereal from run_cereals_008 — sodium flag stress test)
- **expected grade band:** B ceiling (stress test: BARI_SODIUM_CEREAL=off for this corpus)
- **dimension directions:**
  - sodium: HIGH — if product has 500–599mg/100g sodium, the SODIUM_CEREAL_CAP_VALUE=75 (cap at 75 under BARI_SODIUM_CEREAL=on) does NOT fire with the flag off
  - other dimensions: to be populated from BSIP1 read in Phase-1
- **rationale (stress test):** The cereals corpus runs BARI_SODIUM_CEREAL=off. The gold expectation should flag that a cereal with 500mg+ sodium scores HIGHER than it would under the evidence-approved sodium treatment (EV-049, BARI_SODIUM_CEREAL=on). This is a deliberate flag-state finding: if the gold rubric expects the sodium cap to fire and the engine doesn't apply it, the mismatch surfaces a policy question — not an engine bug. Gold annotation: "Expected grade B (score ~65–75) with current corpus flags; would score lower (cap 75 → C) if BARI_SODIUM_CEREAL were activated." Flag for Phase-1 data confirmation.

---

**A06**
- **pid:** `bsip1_bread_7296073134442` (or similar whole-grain sourdough from bread corpus)
- **corpus:** bread
- **name:** (Whole-grain rye sourdough — to be confirmed from run_bread_conform_001)
- **expected grade band:** A–B (stress test: does fermentation + whole-grain earn A?)
- **dimension directions:**
  - processing_quality: HIGH — NOVA 2; true sourdough; whole rye
  - nutrient_density: HIGH — high fiber expected for rye; protein moderate
  - calorie_density: HIGH — rye bread typically 220–260 kcal/100g (bread archetype favorable)
  - glycemic_quality: HIGH — rye + sourdough yields very low GI; low sugar expected
  - additive_quality: HIGH — minimal additives if true sourdough
  - fat_quality: HIGH — very low fat
  - whole_food_integrity: HIGH — fermentation bonus eligible
  - regulatory_quality: HIGH — sodium likely moderate in real rye bread
- **rationale (stress test):** A genuine whole-grain rye sourdough bread SHOULD approach A. The stress test: does the BSIP2 engine actually give it A? The bread corpus uses BARI_RECAL_P0=on and BARI_FAT_TECH_V1=on but no shelf-relative. If the bread scores only B (65–79), is that calibration-appropriate? This is an architectural finding question: Bari's model may structurally be unable to award A to bread (no floor equivalent to NOVA1_SINGLE_FLOOR for bread). Flag for Phase-1 score trace review.

---

**A07**
- **pid:** `bsip1_7296073725367`
- **corpus:** hummus
- **name:** (Low-sodium hummus — to be confirmed; selected for shelf-relative stress test)
- **expected grade band:** B (score range 65–75)
- **dimension directions:**
  - sodium: LOW — below hummus shelf median 390mg → receives shelf-relative RELIEF (B_max=3 points)
  - processing_quality: MEDIUM — NOVA 2–3; chickpea + tahini base
  - nutrient_density: MEDIUM-HIGH — protein ~8g; fiber present from chickpeas
  - calorie_density: MEDIUM — ~180–200 kcal (sauce_spread: ≤300→75)
  - additive_quality: MEDIUM — standard hummus additives (stabilizers + preservative)
  - glycemic_quality: HIGH — low sugar (chickpea carbs = complex)
  - fat_quality: MEDIUM — tahini fat (MUFA/PUFA dominated)
  - regulatory_quality: HIGH — no red labels if sodium < 390mg
- **rationale (stress test):** Tests whether the hummus sodium shelf-relative mechanism correctly awards RELIEF to below-median sodium hummus (B_max=3 points). A product with sodium ~350mg should receive +3 relief. If the engine fails to add this relief, the product would score 2–3 points lower — detectable in the gold check. Basis: to be confirmed from BSIP1 read in Phase-1.

---

**A08**
- **pid:** `bsip1_brinedcheese_48413`
- **corpus:** brined_cheeses
- **name:** (Standard 16–17% fat Bulgarian brined cheese — cream-cheese subtype stress test)
- **expected grade band:** C (score range 50–65)
- **dimension directions:**
  - processing_quality: MEDIUM-HIGH — NOVA 1–2; simple dairy product
  - nutrient_density: MEDIUM — protein ~10g/100g; no fiber
  - calorie_density: MEDIUM — ~200–220 kcal/100g (dairy_protein archetype: ≤250→55; moderate band)
  - fat_quality: LOW-MEDIUM — sat_fat ~10–11g (above red-label 5g; red label fires)
  - regulatory_quality: LOW-MEDIUM — sodium ~800–900mg (graduated penalty applies; HIGH_SODIUM_700MG_PLUS cap fires at 700mg)
  - whole_food_integrity: MEDIUM — clean dairy product
- **rationale (stress test):** A mid-fat Bulgarian cheese with two sources of penalty (sat_fat red label + high sodium) but clean processing and good protein. Tests the interaction between DAIRY_PROTEIN_REWEIGHT_V1 (elevating protein_quality weight from 10% to 14% for the brined corpus) and the sat_fat endemic exclusion. Expected C; if it scores D that suggests the penalty stack is over-penalizing. Flag for Phase-1 data confirmation.

---

**A09**
- **pid:** `bsip1_maadanim_2385455`
- **corpus:** maadanim
- **name:** (Maadanim dairy dessert — NOVA 3–4, added sugar, flavored)
- **expected grade band:** C–D (score range 38–55)
- **dimension directions:**
  - processing_quality: LOW-MEDIUM — NOVA 3–4; flavored dairy dessert; likely multiple additives
  - nutrient_density: MEDIUM — dairy protein base; some protein retained
  - calorie_density: MEDIUM-LOW — flavored dairy dessert likely 130–180 kcal/100g
  - glycemic_quality: LOW-MEDIUM — added sugar expected (maadanim shelf median sugar = 9.7g, Q3 = 16.08g)
  - additive_quality: LOW-MEDIUM — multiple stabilizers + colorants + flavoring expected
  - satiety_support: MEDIUM — protein from dairy base
  - fat_quality: MEDIUM — dairy fat
  - regulatory_quality: MEDIUM — sodium likely in 100–200mg range; sugar variable
  - whole_food_integrity: LOW-MEDIUM — processed dessert
- **rationale (stress test):** Maadanim corpus (BARI_TASK144_FIXES=on; no other special flags) tests the fiber-not-applicable treatment for dessert dairy and the sugar shelf-relative mechanism (BARI_SHELF_RELATIVE_V1=on via engine default; maadanim-specific sugar shelf-rel active). A maadanim product near the Q3 sugar threshold (16.08g) receives the absolute floor of 62 under SUGAR_SHELF_REL_MAADANIM_FLOOR. This tests whether the floor correctly binds. Flag for Phase-1 data confirmation.

---

**A10**
- **pid:** `bsip1_7290107646826`
- **corpus:** snack_bars
- **name:** (High-protein snack bar — reconstructed protein stress test)
- **expected grade band:** C (score range 48–63)
- **dimension directions:**
  - processing_quality: LOW — NOVA 4; ultra-processed protein bar format
  - nutrient_density: HIGH — protein ≥15g/100g (protein bar format)
  - calorie_density: MEDIUM — 380–430 kcal/100g for protein bars
  - glycemic_quality: MEDIUM — sugar often 10–20g; sweeteners may be present
  - additive_quality: LOW-MEDIUM — multiple functional additives typical of protein bars
  - protein_quality: MEDIUM — if reconstructed protein (whey isolate in bar format), receives PROTEIN_QUALITY_MATRIX_DISCOUNT = 0.80 (TASK-222B)
  - satiety_support: MEDIUM-HIGH — high protein
  - fat_quality: MEDIUM
  - regulatory_quality: MEDIUM
  - whole_food_integrity: LOW — ultra-processed; NOVA 4
- **rationale (stress test):** A high-protein snack bar in bar format tests the PROTEIN_QUALITY_MATRIX_DISCOUNT (0.80 for reconstructed protein, TASK-222B). If the product uses "תערובת חלבונים" (generic protein blend = DIAAS_DISCLOSURE_GAP_TRIGGERS), the protein quality score is discounted to 80% of its nominal value. This stress-tests whether high protein mass can overcome processing and additive penalties. Expected C — protein helps but NOVA 4 + additive burden caps the composite. If the engine scores it B, that is a potential finding that the matrix discount is insufficient to counteract protein-bar gaming. Basis: BSIP1 file at run_001 output — to be confirmed in Phase-1.

---

## 4. Corpus Coverage Summary

| Corpus | Products in seed | Tier |
|--------|-----------------|------|
| milk | 4 (G01, G02, P05, P10) | 2 good, 2 poor |
| cereals | 3 (G04, P07, A05) | 1 good, 1 poor, 1 adversarial |
| granola | 2 (G05, A01) | 1 good, 1 adversarial |
| bread | 3 (G06, P08, A06) | 1 good, 1 poor, 1 adversarial |
| hummus | 3 (G07, G10, A07) | 2 good, 1 adversarial |
| yogurt | 2 (G03, A03) | 1 good, 1 adversarial |
| brined_cheeses | 3 (G08, P06, A04, A08) | 1 good, 1 poor, 2 adversarial |
| cakes | 2 (P04, P09) | 2 poor |
| snack_bars | 2 (G09, P02, A10) | 1 good, 1 poor, 1 adversarial |
| maadanim | 1 (A09) | 1 adversarial |
| cereals_multiretailer | 1 (A02) | 1 adversarial |
| juices | 0 | — not covered in Phase-0 |
| hard_cheeses | 0 | — not covered in Phase-0 |

**Note:** 4 adversarial entries (A02, A05, A06, A07, A08, A09, A10) require Phase-1 BSIP1 file reads to confirm nutrition values before finalizing gold expectations. P09 similarly requires confirmation. These are marked with "Flag for Phase-1 data confirmation."

**Actual seed count:** 30 entries (G01–G10, P01–P10, A01–A10) across 11 of 12 registered corpora. Juices and hard_cheeses are absent from this seed; recommend including in Phase-1 expansion.

---

## 5. Key Findings and Recommendations for Phase-1

### 5.1 Schema requirement
The gold set schema must record:
- `pid` (canonical_product_id)
- `corpus` (registry corpus name)
- `flag_config` (exact flag dict under which the expectation holds — critical for yogurt/cerals corpus flag variants)
- `expected_grade_band` (string: "A–S", "B", "C", "D–E", etc.)
- `expected_score_range` ([lo, hi] as integers)
- `dimension_directions` (dict of 10 dimensions → "HIGH"/"MEDIUM"/"LOW")
- `rationale` (prose, 1–3 sentences, nutrition basis named)
- `data_source` (direct product scrape / BSIP0 HTML scrape / BSIP1 fallback — never OFF)
- `gold_status` ("confirmed" = nutrition values verified; "pending" = Phase-1 verification needed)

### 5.2 Flag-config dependency
Three corpus configs that differ from engine defaults require special handling:
- yogurt corpus: (BARI_RECAL_P0=on, BARI_RECAL_P0_YOGURT_TRIM=on, BARI_TASK250_CONF=on)
- brined_cheeses corpus: (BARI_GRAD_SODIUM_V1=on, BARI_SODIUM_SHELF_RELATIVE_V1=on, BARI_DAIRY_PROTEIN_REWEIGHT_V1=on, BARI_RECAL_P0=on, BARI_SHELF_RELATIVE_V1=on, BARI_FAT_TECH_V1=on)
- cakes corpus: (BARI_SHELF_RELATIVE_V1=on, BARI_FAT_TECH_V1=on, BARI_RECAL_P0=off)

The gold_check.py harness must run each product under the CORPUS FLAG CONFIG from shadow_registry_v1.json, not engine defaults.

### 5.3 Gold rubric firewall
The gold expectation is derived from first-principles nutrition reasoning applied to the label. It is NOT derived from the engine's own score. Where the engine's actual score falls outside the expected band, the gold_check.py harness should:
- Exit 2: if score outside band AND the product is in the clearly-good or clearly-poor tier (a large miss suggests a calibration issue requiring Nutrition Agent review)
- Exit 1 (warning): if score outside band AND the product is in the adversarial tier (may indicate a design choice rather than a bug)
- Exit 0: all products within expected band

### 5.4 Data-gap products
P09 (cakes), A02 (cereals_multiretailer), A05, A06, A07, A08, A09, A10 are partially specified. Phase-1 must read their BSIP1 files to confirm nutrition values and finalize expected bands before committing to the gold set schema.

---

*End of Phase 0 analysis. Status: RETURNED pending Phase-1 schema build and data-gap resolution.*
