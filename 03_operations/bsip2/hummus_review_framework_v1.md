# Hummus BSIP2 Review Framework — v1

**Version:** 1.0  
**Date:** 2026-05-30  
**Owner:** Chief Nutrition Officer  
**Purpose:** Category-specific evaluation criteria to establish expectations before the first BSIP2 scoring run  
**Category:** Hummus and Savory Dips (69 products — Shufersal corpus, TASK-034)  
**Status:** Pre-scoring reference. Do not modify BSIP2 engine based on this document without a separate CNO ruling.

---

## What This Document Is

This framework answers a single question: **what does "structurally better" mean for a hummus product?**

It is written before scoring begins to force explicit expectations. When the BSIP2 run is complete, the distribution should be checked against these expectations. Surprises — products that score much higher or lower than predicted — are diagnostic signals. They either reveal a calibration gap in the engine or a gap in this framework.

This document does not propose formula changes. It does not rank products. It describes the food architecture of a well-made versus a poorly-made hummus product and identifies where the current engine is likely to succeed, fail, or need attention.

---

## Section 1 — What Makes a Hummus Product Genuinely Better?

### The central question for hummus

Hummus is architecturally simple in its ideal form: cooked chickpeas, tahini (sesame paste), water, lemon acid, and garlic. Five ingredients. Minimal processing. A product that delivers protein, fiber, and unsaturated fat from whole-food sources without structural reconstruction.

The question Bari asks is not "does this product match a caloric threshold?" but "how far has this product drifted from its natural architectural baseline, and what did the drift achieve?"

### The architecture of a well-made hummus

A well-made hummus has three structural characteristics:

**1. Chickpeas as the first, dominant ingredient**  
The chickpea proportion signals whether this is actually a hummus product or a hummus-adjacent spread. Products listing `חומוס מבושל X%` with X ≥ 50 are architecturally anchored. Products where chickpeas are preceded by water, oil, or fillers have drifted from the structural center.

**2. Tahini (טחינה גולמית) as a named, whole-food fat contributor**  
Raw tahini (טחינה גולמית) contributes sesame fat in a natural matrix: unsaturated fatty acids, protein, minerals, in a whole-food paste structure. It is the legitimate fat source for hummus. When tahini is present as a named ingredient at a meaningful percentage (5–20%), it is a structural positive. When fat is contributed instead by refined oils (שמן סויה, שמן קנולה), the fat source has been reconstructed — cheaper, but structurally inferior.

**3. Short, recognizable ingredient list**  
The simple hummus baseline requires 3–6 ingredients. A product at 3–6 ingredients with all recognizable whole-food items (chickpeas, tahini, water, lemon acid, salt, garlic) is structurally excellent. Products at 10–15 ingredients have introduced reconstruction: thickeners, stabilizers, preservatives, or multiple oil sources. Ingredient count is one of the clearest structural signals in this category.

### What constitutes structural improvement vs. structural noise

**Genuine improvements:**
- Higher chickpea percentage (declared %)
- Named tahini with declared percentage
- Olive oil rather than refined seed oils
- Shorter ingredient list (≤ 6 ingredients is excellent; 7–9 is typical; 10+ is reconstruction)
- Organic certification on the chickpea or tahini (signals minimally processed sourcing)
- No stabilizers, gums, or preservatives

**Structural noise — signals that appear good but do not reflect better food architecture:**
- Low calorie density — a hummus diluted with water or missing tahini will score fewer calories, but it is structurally worse, not better
- Low fat — for a tahini-containing hummus, fat is the expected metabolic contribution; removing it via reformulation is not an improvement
- Added protein claim — protein-enriched hummus often adds isolated protein rather than increasing chickpea density; the declared protein goes up but the structural architecture becomes more complex

---

## Section 2 — Signals That Should Matter Most

### S1 — Ingredient count and list simplicity (HIGH WEIGHT)

**Why it matters:** The single clearest signal of structural reconstruction in hummus is ingredient count. A 3-ingredient hummus (chickpeas, tahini, salt) and a 14-ingredient hummus (chickpea paste, modified starch, two stabilizers, preservative, flavor enhancer, two oils) represent fundamentally different food architectures. The BSIP2 engine's `additive_quality` and `whole_food_integrity` dimensions should capture this, but ingredient count alone is a strong independent signal for this category.

**Corpus evidence:** Ingredient count in the corpus ranges from ~1 (chickpea pastes, missing ingredient data) to 15, with a corpus average of 7.8. Products at 3–6 ingredients are likely architecturally excellent; products at 12+ are heavily reformulated.

**BSIP2 relevance:** `additive_quality` (10%), `whole_food_integrity` (4%), `processing_quality` (15% via NOVA inference).

---

### S2 — Additive burden and specific additive classes (HIGH WEIGHT)

**Why it matters:** The enrichment identified three additive classes that are structurally meaningful for hummus:

| Additive class | Count in corpus | What it means |
|---|---|---|
| Raising agents (bicarbonate/soda) | 72 instances | Acidity buffering — common and neutral in hummus; used to maintain pH during chickpea cooking |
| Acidity regulators | 44 instances | Citric acid, lemon acid — legitimate in hummus; natural preservatives |
| Stabilizers (מייצבים, קסנטן, גואר) | 21 instances | Structural reconstruction signal — hummus does not need gums |
| Stabilizer/thickeners combined | 18 instances | Same concern |
| Preservatives | 2 instances | Potassium sorbate — genuine quality flag |

**What should matter most:** Gums (xanthan, guar, carrageenan) and modified starches in the stabilizer and thickener categories are the most meaningful quality differentiators. They appear in products where the chickpea-tahini ratio is too low to achieve natural emulsification — the gums compensate for chickpea deficit. Their presence is a structural proxy for "diluted hummus with reconstruction."

**Acidity regulators (סודיום ביקרבונט, חומצת לימון)** are expected in commercial hummus and should carry minimal weight as negative signals. The enricher flags these heavily (72 instances); this inflation requires calibration for this category.

**BSIP2 relevance:** `additive_quality` (10%). The specific breakdown matters more than total count — the engine should be checked to confirm it distinguishes sodium bicarbonate (expected/neutral) from xanthan gum (reconstruction signal).

---

### S3 — Sodium level (MEDIUM-HIGH WEIGHT)

**Why it matters:** Hummus is a savory category with legitimate sodium (salt, acidity regulators). But the corpus shows a range from 6mg to 864mg sodium/100g — a 144× range that reflects genuine formulation differences, not label formatting variation. High sodium in hummus is often an additive-concentration signal: industrial hummus with high additive burdens tends to have higher sodium.

**Corpus data:** avg = 363mg, max = 864mg. The Israeli red-label threshold is 600mg/100g. Several products in the corpus will trigger the sodium red label.

**Calibration note:** The sodium dimension should fire meaningfully at the high end (>600mg red label) without over-penalizing typical commercial hummus (300–450mg), which is within the normal range for a savory spread.

---

### S4 — Protein density from chickpeas (MEDIUM WEIGHT)

**Why it matters:** Chickpeas provide ~7–9g protein per 100g cooked. A hummus with good chickpea density should deliver ~4–8g protein per 100g. This is distinguishable from products that claim high protein through added protein isolates (which produce a different structural architecture).

**Corpus data:** avg protein = 7.4g, range = 0.7g–22g. Products above 12g protein almost certainly contain added protein isolate or are chickpea-kernel raw-ingredient products that weren't fully excluded. Products at 4–9g are consistent with natural chickpea density. The single 22g outlier is likely a protein-enriched product.

**BSIP2 relevance:** `nutrient_density` (15%) and `protein_quality` (10%). Protein source quality matters here — declared protein from whole chickpeas is structurally different from protein concentrate.

---

### S5 — Fiber density (MEDIUM WEIGHT)

**Why it matters:** Chickpeas are a meaningful fiber source (~5–7g fiber per 100g cooked). Fiber in hummus is both structurally expected and nutritionally genuine. A well-made hummus with good chickpea density will deliver 4–7g fiber/100g naturally.

**Corpus data:** Only 21/69 products have fiber data (COV-005 gap from Shufersal scraper). Of those, range = 0.8–17.4g, avg = 5.2g. The fiber data that exists is consistent with a chickpea-dense product.

**BSIP2 relevance:** `nutrient_density` (15%), `glycemic_quality` (12% — fiber provides the glycemic buffer), `satiety_support` (6%). Fiber's triple contribution through multiple dimensions means the engine should be checked for the collinearity risk identified in the architecture documentation.

---

## Section 3 — Signals That Should Matter Less

### NS1 — Calorie density (LOW WEIGHT FOR THIS CATEGORY)

**Why it should be de-emphasized:** Hummus is a calorie-dense category by design. A well-made hummus with chickpeas (120–150 kcal/100g), tahini (600 kcal/100g), and olive oil (900 kcal/100g) will land at 150–300 kcal/100g depending on composition. The `sauce_spread` calorie density table in `constants.py` rewards products at ≤150 kcal with a score of 90, and penalizes products at 450–600 kcal.

**The failure mode:** The engine should not reward a diluted, low-tahini hummus for being lower in calories. The calories in a well-made hummus come from chickpeas (complex carbohydrate + protein) and tahini (whole-food fat). Penalizing these calories is penalizing the structural content of the product.

**Expected corpus range:** Most hummus spreads will fall in the 150–280 kcal/100g range. The sauce_spread table rates this as "moderate" (score ~75). This is acceptable; the concern is if the engine rewards the bottom of the range unconditionally.

**Corpus data:** avg = 213 kcal, range = 32–599 kcal. The 32 kcal outlier is almost certainly a data extraction artifact. The 599 kcal product is likely a tahini-heavy or oil-heavy variant — not a structural problem.

---

### NS2 — Total fat (LOW WEIGHT, with a critical caveat)

**Why it should be de-emphasized:** For hummus, fat from tahini is **structurally appropriate and nutritionally coherent**. The unsaturated fat in sesame paste (linoleic acid, oleic acid) is a functional part of the food matrix. A hummus with genuine tahini content at 15% will contribute approximately 8–12g fat per 100g. This should not be penalized.

**The critical caveat — data quality:** The corpus shows an average fat of **0.7g/100g** — physically impossible for any tahini-containing hummus. This is a Shufersal scraper artifact: the scraper's NUTR_LABEL_MAP extracts `שומן` (fat), but Shufersal's HTML frequently returns the saturated fat sub-row (שומן רווי) in the position where total fat is expected. The result: most hummus products show `<0.5g fat` when the actual total fat is likely 5–12g.

**BSIP2 consequence:** The `fat_quality` dimension will operate on erroneous data for this corpus. A product showing 0.5g fat will score well on fat_quality not because it is a good product, but because the scraper failed. This is one of the highest-priority known issues before BSIP2 runs.

**Recommendation:** BSIP2 operators must be aware that `fat_quality` scores in this corpus are derived from incorrect data. The dimension's output should be noted as unreliable in the run report.

---

### NS3 — Saturated fat proportion (LOW WEIGHT)

**Why it should be de-emphasized:** Sesame tahini contains approximately 15–20% saturated fat (a normal profile for a whole seed). A hummus with meaningful tahini content will have saturated fat above 1g/100g. This is structurally expected and should not trigger the fat_quality dimension's saturated fat penalty at meaningful weight. This is analogous to the whole-food-fat protection that Bari applies to nuts and olive oil.

**BSIP2 relevance:** The engine protects whole-food fats through the `WHOLE_FOOD_FAT_FLOOR` mechanism for nuts and seeds. Tahini-based fat in hummus deserves the same treatment — but since total fat data is corrupt (see NS2), this is moot until the fat data is corrected.

---

### NS4 — Carbohydrate quantity (LOW WEIGHT)

**Why it should be de-emphasized:** Chickpeas contribute ~12–20g carbohydrates per 100g cooked — this is the natural carbohydrate content of a legume. The carbohydrate in hummus is primarily complex (starch + fiber from chickpeas), not simple sugar. The `glycemic_quality` dimension would apply sugar penalties only if sugar content is elevated; in a well-made hummus, sugar should be near zero.

**The concern:** The `glycemic_quality` formula (`90 − sugar_penalty + fiber_bonus + whole_grain_bonus`) should work correctly for hummus — low sugar, high fiber bonus. The carbohydrate quantity itself should not be an independent penalty signal for this category.

---

### NS5 — Calorie density penalties from tahini and olive oil content

**Why it should be de-emphasized:** "Premium" hummus variants (with declared tahini at 20%+, olive oil, pine nuts) will score higher calories. The olive oil-topped hummus at 280 kcal is not worse than the water-diluted hummus at 160 kcal. If the calorie density dimension systematically rewards diluted products, it inverts the quality signal for this category.

---

## Section 4 — Expected BSIP2 Failure Modes

### FM-1 — Rewarding low-fat / low-tahini hummus

**Mechanism:** The fat_quality dimension (8% weight) will score products with near-zero fat as structurally excellent. In the current corpus with corrupt fat data (Section NS2), this will affect the majority of products. The products that show <0.5g fat are not better products — they either have a data extraction error or they genuinely have very little tahini.

**Expected impact:** Systematic overscoring of products with missing or artificially low fat values. Products that should score C-D (low-tahini, water-diluted formulations) may score B on fat_quality alone.

**Detection:** After the BSIP2 run, sort products by `fat_quality` dimension score. If the highest fat_quality scores go to products named "חומוס 0% שומן" or products with `<0.5g fat`, the failure mode has fired.

**Mitigation:** Before running BSIP2, flag products with `fat_g < 1.0` for data review. Consider whether fat_quality should be suppressed or marked unreliable for products where fat data is suspicious.

---

### FM-2 — Over-penalizing tahini via sodium bicarbonate additive inflation

**Mechanism:** The BSIP1 enricher detected 72 raising_agent signals across the corpus — the highest single additive category. Sodium bicarbonate (סודיום ביקרבונט) is used in the chickpea cooking step and in acidity buffering of tahini, and is classified as a raising_agent in the enricher's ADDITIVE_TERMS list. This means virtually every product in the corpus will have multiple additive flags from a functionally neutral ingredient.

**Expected impact:** `additive_quality` will penalize products based heavily on raising_agent counts, not on the structurally significant additives (stabilizers, gums, preservatives). This inflates the apparent additive burden of traditional hummus products.

**Detection:** After the BSIP2 run, check products that score poorly on `additive_quality`. If they are traditional-style products (short ingredient list, chickpeas + tahini) penalized primarily for sodium bicarbonate, the failure mode has fired.

**Mitigation:** The additive engine should apply a category-specific weight reduction for `raising_agent` in the `sauce_spread` archetype. Sodium bicarbonate and citric acid in hummus are functional processing aids, not quality-degrading additives. This is a BSIP2 calibration note, not a framework change request — it requires a separate CNO ruling to implement.

---

### FM-3 — Over-penalizing natural sesame fat from tahini

**Mechanism:** If the fat data quality issue (FM-1) is resolved for some products but not others, the fat_quality dimension may penalize tahini's natural saturated fat fraction (~15–20% of sesame fat is saturated). A hummus with 10g total fat (mostly unsaturated from tahini) and ~1.5g saturated fat would have a 15% saturated fat ratio — within the acceptable range, but near the engine's penalty zone.

**Expected impact:** Systematic mild penalty on products that accurately report fat composition, while products with corrupt fat data escape the penalty. This creates an inverted quality signal.

**Detection:** Compare fat_quality scores between products with `fat_g > 3` (accurate) and products with `fat_g < 1` (likely corrupt or very low tahini). If the former group scores consistently lower, the failure mode is active.

---

### FM-4 — Missing high-quality traditional products

**Mechanism:** Premium traditional hummus (e.g., "מלך החומוס" style — very short ingredient list, high chickpea and tahini content, minimal additives) may score poorly on `calorie_density` (higher kcal from tahini), `nutrient_density` (protein and fiber are good, but not exceptional compared to a protein-fortified variant), and `processing_quality` (NOVA inference may land on NOVA 3 due to processing steps for commercial production).

**Expected impact:** Traditional high-quality products score B rather than A because the engine is not calibrated to reward "simple, whole-food, high-tahini" architecture specifically.

**Detection:** After the BSIP2 run, locate products with ≤6 ingredients and explicitly named raw tahini at a declared percentage. If these products score below 75, examine which dimensions drove the reduction.

---

### FM-5 — Protein-enriched hummus scored too favorably

**Mechanism:** Products like `חומוס עשיר ב40% טחינה` (protein-enriched hummus) will score well on `nutrient_density` and `protein_quality` due to declared high protein (12–22g). These products often have more complex formulations — added protein isolates, longer ingredient lists, modified starches for texture after protein addition.

**Expected impact:** The protein and nutrient_density dimensions reward declared protein without accounting for the structural complexity introduced to achieve it. A product with 22g protein from isolated chickpea protein and 12 ingredients may outscore a product with 7g protein from whole chickpeas and 5 ingredients.

**Detection:** After the BSIP2 run, sort by `protein_quality` score. Products with >12g protein that have ingredient lists > 10 items are candidates for this failure mode. Check if their final scores are inflated relative to their structural complexity.

---

### FM-6 — Calorie density penalty misfire on matbucha and eggplant spreads

**Mechanism:** Matbucha (cooked tomato-pepper spread) and plain eggplant spreads have very low calorie density — typically 30–80 kcal/100g. The `sauce_spread` calorie density table rewards ≤150 kcal with a score of 90. These products will score very high on calorie_density not because they are structurally excellent, but because they are low-energy vegetables.

**Expected impact:** Matbucha and eggplant spreads systematically score high on calorie_density, which may inflate their overall scores relative to higher-calorie but structurally superior hummus products. This is not necessarily wrong — these are genuinely low-fat, high-vegetable products — but it should be expected and documented.

**Detection:** After the BSIP2 run, compare the average score of matbucha/eggplant products vs. hummus spreads. If the vegetable-based secondary products consistently outscore hummus, examine whether the calorie_density dimension is the primary driver.

---

## Section 5 — Expected Top 10%

These are **archetypes**, not rankings. They describe the structural characteristics of products that should score in the A range (85–100) or high-B range (75–85).

### Archetype A — Traditional Pure Hummus (3–6 ingredients)

**Profile:**
- Named ingredient list: cooked chickpeas (≥60%) + raw tahini (declared %, typically 10–18%) + water + lemon acid + salt
- No gums, no stabilizers, no preservatives, no added oil
- Protein: 5–8g (natural chickpea-based)
- Sodium: 200–400mg (from salt and acidity management)
- Ingredient count: 3–6

**Why they should be in the top 10%:** This is the structural ideal. The fat comes from a named whole-food source (tahini). The protein and fiber come from intact cooked chickpeas. There is no reconstruction. The product's architecture is transparent and coherent.

**BSIP2 expectation:** High `processing_quality` (NOVA 1–2), high `additive_quality` (few additives), high `whole_food_integrity`. The risk is that fat data corruption (FM-1) and bicarbonate over-counting (FM-2) may suppress the expected grade. These products should be the first diagnostic check after the run.

---

### Archetype B — Traditional Hummus with Declared Tahini Percentage and Single Fat Source

**Profile:**
- Named ingredient list: cooked chickpeas (50–65%) + raw tahini (15–20% declared) + olive oil (single natural oil source) + traditional seasonings
- Ingredient count: 7–10 (pine nuts, spices, garlic — added for flavor, not reconstruction)
- No stabilizers or preservatives

**Why they should be in the top 10%:** The declared tahini percentage signals authentic formulation. Olive oil as the only added fat is a quality marker. Pine nuts and za'atar are whole-food additions, not reconstruction ingredients.

**BSIP2 expectation:** Grade A or high B. The natural fat and good ingredient quality should drive strong scores across multiple dimensions.

---

### Archetype C — Simple Eggplant Spread (3–5 ingredients)

**Profile:**
- Roasted eggplant (primary ingredient, ≥60%) + lemon/acid + salt + optional oil
- No gums, no preservatives, no starch
- Very low calorie density (40–70 kcal/100g), low sodium
- Ingredient count: 3–5

**Why they should be in the top 10%:** Structurally simple roasted vegetable products with no reconstruction. The calorie_density dimension will score these very highly; the additive_quality and processing_quality dimensions should be clean.

**BSIP2 expectation:** Grade A or A-. The low calorie density will drive high calorie_density scores; low additive burden will drive clean additive_quality. The main risk is low nutrient_density (eggplant has less protein than chickpeas), which may keep the final score in high-B rather than A.

---

### Archetype D — Traditional Matbucha (4–6 ingredients)

**Profile:**
- Cooked tomato + red pepper + garlic + oil + spices
- No gums, no stabilizers
- Low sodium (150–350mg), no red labels
- Ingredient count: 4–7

**Why they should be in the top 10%:** Matbucha in its traditional form is a cooked vegetable spread with minimal reconstruction. The calorie density advantage will help; the clean ingredient list will prevent additive penalties.

**BSIP2 expectation:** Grade A or high B. FM-6 (calorie density bonus for low-calorie vegetable products) will operate here; the question is whether nutrient_density (lower protein in vegetable-based products) balances this favorably.

---

## Section 6 — Expected Bottom 10%

These are **archetypes**, not rankings. They describe structural characteristics that should produce grades D–E (40–54 or below).

### Archetype X — Industrially Reconstructed Hummus (10–15 ingredients)

**Profile:**
- Chickpea paste at low declared percentage (30–45%) — water or oil listed before chickpeas
- Multiple reconstruction ingredients: modified starch, xanthan gum, guar gum, potassium sorbate, sodium sorbate
- Added oil is a refined seed oil (שמן סויה), not tahini
- High sodium (600–850mg)
- Ingredient count: 10–15

**Why they should be in the bottom 10%:** The chickpea and tahini content has been diluted. Gums compensate for the structural deficit created by lowering the natural emulsifiers. Preservatives extend shelf life to compensate for lower natural acidity from tahini reduction. Refined seed oil replaces tahini's whole-food fat. This is a reconstructed approximation of hummus architecture.

**BSIP2 expectation:** Grades C–D. High `additive_quality` penalty, low `whole_food_integrity`, possible sodium red label at >600mg. If the engine is properly calibrated for gum-containing products, these should score 40–60.

---

### Archetype Y — "Light" or "0% Fat" Reformulated Hummus

**Profile:**
- Low or no tahini (to reduce fat and calories)
- Compensated with added water, modified starch, and gums to maintain texture
- Sodium often elevated (seasoning compensation for loss of tahini flavor)
- Protein lower than traditional (less tahini contribution)
- May carry a "0% שומן" or "קל" marketing claim

**Why they should be in the bottom 10%:** Light hummus achieves its caloric reduction by removing the most architecturally valuable ingredient (tahini) and compensating with reconstruction. The fat is lower — but the structural quality is lower for the same reason. The low calorie score should not rescue a product that has been systematically reformulated to appear virtuous.

**BSIP2 failure risk (FM-1):** If the engine rewards low fat unconditionally, these products will be inflated relative to their true structural quality. This is the clearest test case for FM-1.

**BSIP2 expectation:** If the engine works correctly: Grade C–D. If FM-1 fires: Grade B (inflated). Post-run diagnostic: locate all products with "קל", "0%", "דל שומן" in the name and check their scores. If any score above 70, FM-1 is active.

---

### Archetype Z — Calorie-Dense Reconstructed Hummus with Multiple Oil Sources

**Profile:**
- Multiple oil types listed (שמן סויה + שמן קנולה + שמן דקלים combination)
- High calorie density from refined oils rather than tahini
- Medium ingredient count (8–12) with additives
- High calorie density (250–350 kcal) without the structural justification of natural tahini content

**Why they should be in the bottom 10%:** High calories from reconstructed oil sources, not from whole-food fat. The calorie_density dimension may penalize this product correctly; the fat_quality dimension should penalize the refined seed oil concentration.

**BSIP2 expectation:** Grade C–D. Depends on whether the engine distinguishes reconstructed multi-oil sources from natural tahini fat.

---

### Archetype W — Eggplant "Spread" with Artificial Flavor or Liver Flavor Descriptor

**Profile:**
- Contains "בטעם כבד" (liver-flavored) or artificial flavor markers
- Eggplant spread formulated to resemble a different product category through artificial flavoring
- Typically 8–12 ingredients including flavor additives

**Why they should be in the bottom of the eggplant segment:** The flavor descriptor signals that the product has been engineered away from its natural food identity. Eggplant spread flavored to taste like liver is not structurally what it claims to be. The `has_flavor_descriptor` enrichment signal (from "בטעם") should influence this product's grade.

**BSIP2 expectation:** Grade C. The flavor descriptor marker in the enrichment should carry some weight if the engine is connected to it. If the engine ignores the flavor descriptor, this product may score the same as a clean eggplant spread — which would be a calibration gap.

---

## Section 7 — Pre-Run Checklist for BSIP2 Operators

Before running the hummus BSIP2 batch, confirm:

| Check | Action | Priority |
|---|---|---|
| Fat data quality | Verify whether `fat_g` for hummus products reflects total fat or saturated fat. Flag products with `fat_g < 1.0` and cross-check against ingredient list (if tahini is present, total fat should be ≥ 4g). | **Critical** |
| Sodium bicarbonate additive classification | Confirm whether `raising_agent` additive signals are weighted at full additive penalty or reduced weight for the `sauce_spread` archetype | **High** |
| Sauce/spread calorie density table | Confirm the engine routes hummus to `sauce_spread` calorie density table (not `default` or `snack_bar_granola`) | **High** |
| NOVA routing | Confirm what NOVA level the engine infers for a standard hummus product. Expected: NOVA 2–3 (lightly processed, cooked legume with natural emulsifier). NOVA 4 would be a routing error for a simple 5-ingredient product. | **High** |
| Protein source classification | Confirm the engine classifies chickpea protein as `whole_food` or `plant` source, not `unknown` | **Medium** |
| Flavor descriptor signal | Confirm whether `has_flavor_descriptor` from the enrichment influences any dimension score | **Medium** |

---

## Section 8 — Category Context for BSIP2 Score Distribution

The expected distribution for 69 hummus and savory dip products, absent the failure modes described above:

| Grade | Expected count | Typical products |
|---|---|---|
| A (85–100) | 5–10 | Artisanal 3–6-ingredient hummus; simple clean eggplant spreads |
| B (70–84) | 20–28 | Standard commercial hummus (6–10 ingredients, tahini present, no gums); matbucha; roasted pepper spread |
| C (55–69) | 20–25 | Commercial hummus with gums/stabilizers; light hummus; hummus-adjacent with extended ingredient lists |
| D (40–54) | 10–15 | Heavily reconstructed; 12+ ingredients; multiple gums; high sodium |
| E (0–39) | 2–5 | Missing data products; suspected preparation errors; products with multiple red labels |

**If the actual distribution deviates significantly from this** (e.g., > 20 products at grade A, or fewer than 10 at grade B–C), the most likely causes are:

1. FM-1 (fat data corruption inflating fat_quality across the board) → check average `fat_quality` dimension score
2. FM-2 (raising agent over-counting in additive_quality) → check additive_quality distribution
3. NOVA routing error → check NOVA inference distribution across the corpus
4. Sodium data missing for many products → check whether sodium red-label triggers are firing correctly

---

## Section 9 — Key Inputs Used

| Input | Source |
|---|---|
| Corpus composition | TASK-034 BSIP1 enrichment — 69 products |
| Nutrition statistics | Computed from `canonical_bsip1/` (TASK-038 analysis) |
| Enrichment signals | `enrichment_validation_001.md` — additive categories, roasting markers |
| Scoring architecture | `scoring.md`, `constants.py`, `dimension_mapping.md` |
| Framework philosophy | `framework_philosophy.md` — structural intelligence standard |
| Fat data quality finding | TASK-038 BSIP0 audit — `fat_raw = "פחות מ 0.5"` for majority of corpus |

---

*Hummus BSIP2 Review Framework v1 — Chief Nutrition Officer*  
*Pre-scoring reference. Check Section 7 before the first batch run.*  
*Post-scoring: compare actual distribution against Section 8. Open a CNO ruling for any failure mode confirmed above D-level prevalence.*
