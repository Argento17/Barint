# Cookies-near-coffee (עוגיות לקפה) — Scoring Interpretation v1

**Task:** TASK-275 (factory run #7, `cookies-coffee`)
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** DRAFT — proposed RETURNED; awaiting orchestrator review
**Dependency for:** Factory run #7 corpus filter, BSIP1 enrichment config, and frontend packaging
**Category ID:** `cookies-coffee`

---

## 1. Category Scope and Boundaries

### 1.1 Defining characteristic

The "coffee cookie" (עוגיית לקפה) is defined by a single use-case property: **a small, firm-textured,
sweet biscuit sold as an accompaniment to hot beverages — principally coffee**. The archetype is the
speculoos / Lotus Biscoff biscuit. The category is structurally distinct from general baked goods by
three properties that hold across the entire shelf:

1. **Form factor:** crisp/crunchable biscuit, thin or stackable, individual weight typically 5–25g.
2. **Beverage pairing:** products are recognized by Israeli consumers as coffee or tea companions
   (this is a consumer-occasion category, not a composition category).
3. **NOVA status:** virtually all retail members of this shelf are NOVA 3 or NOVA 4. No genuine
   NOVA-1 product exists on the Israeli coffee-biscuit shelf.

The purpose of this document is to define which products belong inside this definition (for the
corpus filter after the broad BSIP0 scrape) and how the committed engine behaves on them.

### 1.2 In scope

| Type | Hebrew / Example | Notes |
|---|---|---|
| Speculoos / Belgian biscuits | ביסקוויט בלגי / לוטוס | The category archetype; caramelized spiced shortbread |
| Petit beurre | פטי-בר | Classic rectangular butter biscuit; dominant on Israeli shelf |
| Tea / Marie biscuits | ביסקוויט תה / מרי | Thin, lightly sweetened; often sold in cylindrical rolls |
| Butter cookies | עוגיות חמאה | Round or pressed; butter as named primary fat |
| Shortbread | שורטברד | Scottish-style; high butter content, minimal sugar |
| Digestive | דייג'סטיב | Whole-wheat or mixed-flour; slightly higher fiber than plain butter types |
| Biscotti / cantuccini | ביסקוטי | Twice-baked; anise or almond varieties; Italian origin |
| Plain crisp biscuit variants | ביסקוויט פשוט, ביסקוויט דיאטטי | Simple flour + fat + sugar formulations without filling or coating |

### 1.3 Out of scope — and the in/out rule

**The in/out rule:** A product is in scope if and only if (a) it is a dry, crisp-textured biscuit
(not soft/cake-like), (b) it is sweet (sugars present as a primary design feature), (c) it has no
filling or cream layer integrated into the product architecture, (d) it is not coated in chocolate
or compound coating as a primary design feature, and (e) it is plausibly consumed as a coffee
accompaniment rather than as a standalone confection or children's snack.

Excluded product types:

| Type | Reason for exclusion | Disposition |
|---|---|---|
| Chocolate-coated biscuits (כריות ממולאות, בורבון, toffee-bar format) | Coating is a primary architecture feature, not incidental. Different sugar+fat profile, different consumer occasion. | **OUT** — separate confection category |
| Cream-filled sandwich cookies (אוראו-style, כריות קרמיות) | Structural filling creates a different caloric and sugar architecture; not a coffee-companion shortbread. | **OUT** — cream-filled biscuit own category |
| Wafers (וופלים, קרנדולה-style) | Different matrix entirely: layered, aerated cream sheets. Not a biscuit. | **OUT** — wafers own category |
| Cake-like / soft cookies (עוגיות רכות, מאפינס בשקית) | Fails the dry/crisp condition. Moisture-retained baked goods belong to "baked goods" category, not coffee biscuits. | **OUT** — soft baked goods |
| Children's character cookies (עוגיות ספרים, בחשנים, Leibniz Zoo, animal-shaped) | Primary consumer occasion is children's snacking, not coffee. Packaging confirms this. | **OUT** — children's biscuits category |
| Protein / "functional" biscuits (ביסקוויט חלבון, עוגיות ספורט) | Macro architecture (protein >10g/100g, engineered fiber) diverges from coffee-biscuit shelf. | **OUT** — functional/supplement category |
| Gluten-free coffee biscuits | **AMBIGUOUS — see §1.4** | Ruling below |
| Vegan coffee biscuits | **IN** — vegan label does not change structural scope. Fat source (margarine vs butter) is a scoring signal, not a scope filter. Evaluate with the standard engine. | **IN** |
| Organic coffee biscuits | **IN** — organic certification is a process claim, not a structural category split. | **IN** |
| Rice cakes (קרקרים, פצפוצי אורז) | Not sweet biscuits; beverage pairing is incidental. | **OUT** — crackers / rice cakes category |
| Energy / muesli bars shaped as biscuits | Fails coffee-companion occasion test if primary positioning is sports/active nutrition. | **OUT** — snack bar category |

### 1.4 Ambiguous cases — rulings

**Gluten-free coffee biscuits:** Include if the product's evident consumer occasion is
coffee-accompaniment (speculoos-style, petit beurre shape, similar packaging) and the ingredient
architecture is analogous to the in-scope set (flour substitute + fat + sugar; no protein
fortification; no filling). Gluten-free is a formulation variant, not a structural split. Exclude
if the product is primarily positioned as a health/medical dietary specialty with macro architecture
diverging from the coffee-biscuit shelf. At the corpus-filter stage: default to IN unless packaging
signals medical/clinical positioning. If in doubt, DISCARD per the owner's missing-data discard rule
(never punish / never over-invest in re-sourcing).

**Biscuits with flavoring (chocolate chip, lemon, vanilla cream on top):** Minor flavoring (a
drizzle, chip inclusions, or a flavored glaze applied to a structurally plain biscuit) does not
exclude the product. The **structural test** determines scope: is the primary architecture a crisp
biscuit body? If yes, it is in scope even with flavoring. A biscuit where the chocolate or cream
content represents >30% of the total by volume or completely coats the outside is structurally a
confection and is OUT.

**Whole-grain variants (digestive with whole wheat, oat digestive):** IN. Whole grain is a
quality-differentiating ingredient, not a scope exclusion. These are the products where the engine's
whole-grain signal adds meaningful differentiation (see §4.3).

---

## 2. Scoring Philosophy for an Indulgence Category

### 2.1 What this category is

Coffee biscuits are an indulgence accompaniment. They are sweet, energy-dense, and processed.
Consumers understand this. Bari's job is not to punish the category for being what it is; it is to
score **within the category** so a consumer choosing a coffee biscuit can identify which product has
a better nutritional architecture relative to its peers.

### 2.2 Engine NOVA classification for this shelf

The NOVA proxy classifier (`nova_proxy.py`) assigns NOVA based on additive markers, ingredient count,
and structural signals. The coffee-biscuit shelf will overwhelmingly land at:

- **NOVA 3** (most products): refined wheat flour + fat + sugar + leavening + flavoring. Additive
  categories fire for: preservative, emulsifier (lecithin, E471/E472), leavening_agent (baking
  powder = acidity_regulator + leavening). These are the classic NOVA-3 signals at
  `nova_proxy.py` lines 41–46 (`NOVA3_SIGNALS`). The score-based classifier at line 539
  (`additive_count >= 1 or added_sugar_ct >= 1 or ing_count > 5 → level = 3`) fires on virtually
  every multi-ingredient biscuit.
- **NOVA 4** (minority, higher-processed variants): artificial colors, synthetic flavor enhancers
  (`חומרי טעם וריח`), humectant + emulsifier combinations, or very long ingredient lists (>15).
  These are the `nova4_score >= 4` path at `nova_proxy.py` line 527.
- **NOVA 1 or 2:** Not achievable on this shelf. A true single-ingredient biscuit does not exist.
  Even "natural" shortbread contains flour, butter, and sugar minimum — this is a multi-ingredient
  NOVA-3 product at best. The NOVA-3→2 demotion guard (R4 at `nova_proxy.py` line 571) does not
  apply: that guard is for PLAIN DAIRY only (`product_type_dairy` check). Cookie products will
  never receive R4 demotion.

The **NOVA_PROXY_3_PROCESSED** cap fires at `score_engine.py` lines 1963–1964:

```python
check_cap("NOVA_PROXY_3_PROCESSED", nova_level == 3, _nova3_cap_val, proc_caps_fired)
```

The `_nova3_cap_val` is determined by `PROCESSING_CAPS` in `constants.py`. When `BARI_GLASSBOX_W4`
is ON (it is ON as of TASK-181S, 2026-06-05), the cap scales with NOVA-inference confidence via
`_d3_scaled_cap()`. For a high-confidence NOVA-3 product, the effective cap is the table value.
For a NOVA-4 product, `NOVA_PROXY_4_ULTRA_PROCESSED` caps at 68 (line 1960).

### 2.3 The realistic grade ceiling

**The committed engine produces a realistic ceiling of B (70–79) for the best-in-class
coffee biscuits, with the bulk of the shelf sitting in C (55–69).** This is not a manufactured
constraint — it is the honest outcome of the engine's NOVA-3 processing cap applying to what is
genuinely a processed-food shelf. The reasoning:

A best-in-class coffee biscuit has:
- NOVA 3 (clean: flour + butter + sugar + natural flavoring; no synthetic flavor enhancers,
  no artificial colors, no engineered fat substitutes)
- Sugar: typically 15–22g/100g (below the Israeli red-label threshold of 17.5g — just)
- Fat: typically 15–25g/100g; saturated fat typically 8–14g/100g (above 5.0g red-label threshold)
- Fiber: minimal unless whole-grain variant (0–4g/100g)
- Sodium: low — typically 100–300mg/100g (not the story here)
- Calories: 430–500 kcal/100g (energy-dense)

For such a product:
- NOVA_PROXY_3_PROCESSED cap fires. The PROCESSING_LOAD family is the binding guardrail for most
  products on this shelf.
- ISRAELI_RED_LABEL_1_SAT_FAT (cap at 55) fires for high-butter variants (sat-fat > 5g/100g,
  which is virtually every full-fat butter biscuit). RECAL_P0 is currently OFF for this category,
  so the cliff cap at 55 is the operative rule (`score_engine.py` line 2256).
- HIGH_CAL_LOW_SATIETY_SEVERE (cap at 55) fires when kcal >= 500 and protein < 6 and fiber < 3
  (line 1924). Many refined-flour biscuits at 470–500 kcal/100g with minimal protein/fiber hit this
  or the soft variant.

With multiple caps coordinating (see `_coordinate_family()`, line 2370–2394), the binding cap for
a typical full-butter refined-flour biscuit lands around 55–68, producing grades C to low-B.

A clean shortbread or digestive with whole-grain flour, cleaner sat-fat (still high but not at the
top of the shelf), and no synthetic additives achieves the best feasible score — landing in the
68–75 range, supporting a B grade. The NOVA-3 cap remains but the sat-fat cap and calorie-density
cap may or may not fire depending on exact composition.

**A grades are not achievable on this shelf with the committed engine.** The structural reason:
A requires score >= 80 (`constants.py`, `score_to_grade()`), which would require not hitting any
meaningful cap. A clean NOVA-3 biscuit with high fat and sugar cannot avoid at least one cap that
limits the score below 80. This is an honest finding, not a ceiling imposed by the Nutrition Agent.

**D or E grades are also possible** for heavily processed variants: a NOVA-4 biscuit with
artificial flavor enhancers, synthetic colors, multiple emulsifiers, and sugar above the red-label
threshold can score in the 40–55 range (grade D), particularly if the HIGH_CAL_HIGH_SUGAR_SEVERE
cap (score 50, line 1857) fires alongside the NOVA-4 cap.

**The honest ceiling is B. The honest floor is D.** C is the modal grade for this shelf. This
is the analogue of the snk-001 ceiling for snack bars, but one grade higher: the coffee-biscuit
shelf has a marginally more diverse nutritional architecture than the snack-bar shelf, and the
engine reflects that difference correctly.

### 2.4 Honest clustering acknowledgment

If the real scrape finds that Israeli retail coffee biscuits cluster tightly at 20g sugar, 12g
sat-fat, 460 kcal/100g across most SKUs — producing a narrow C band — that is a valid finding.
The engine should not be adjusted to manufacture differentiation. Report the cluster honestly
(category caveat, §6), alongside whatever genuine variation exists.

---

## 3. What Actually Differentiates Quality on This Shelf

### 3.1 The thesis: fat type and additive load, not sodium

The brined-cheese category's thesis chart is "sodium vs grade" — sodium is the dominant dimension.
For coffee biscuits, sodium is NOT the story. Sodium on this shelf is low (100–300mg/100g in almost
all products) and will almost never fire `HIGH_SODIUM_700MG_PLUS` (engine requires >=700mg at
`score_engine.py` line 2141). The sodium evaluation status will be "standard"
(`evaluation_scope.py` assigns no `brined_food` context_flag because none of the name keywords
match any coffee-biscuit name — `evaluation_scope.py` lines 39–68). No context modification to
sodium scoring is needed or warranted.

**The signature thesis chart for this category: sugar x fat-type (saturated vs unsaturated ratio), colored by grade.** The chart shows that products with a lower saturated-fat burden (higher
unsatFat/satFat ratio) and lower sugar land in B, while products with high sat-fat and
high-sugar pile into C/D. This surfaces the real quality question on this shelf: is the fat
palm oil / hydrogenated fat / margarine, or is it genuine butter? Are there multiple synthetic
additives, or is the ingredient list short and clean?

### 3.2 Primary differentiators, ranked by scoring relevance

**Rank 1 — Fat type (saturated fat content and unsatFat/satFat ratio): the most important signal**

Fat is the biggest single composition variable across this shelf:
- Low-satFat products (digestive, whole-grain, partial-veg-fat): typically 5–8g sat-fat/100g. May
  or may not trigger the sat-fat red label depending on exact value. The ratio-based fat quality
  score (`score_engine.py` line 1262–1268, `EV-012 fat_ratio`) rewards products with a better
  unsaturated/saturated ratio.
- High-satFat products (full-butter shortbread, Lotus-type palm-oil rich biscuits): typically
  10–15g sat-fat/100g. `ISRAELI_RED_LABEL_1_SAT_FAT` cap fires at 55 (`score_engine.py` line 2256).
  The sat-fat signal is the hardest cap on this shelf.

**Margarine vs butter vs palm oil is the single most impactful quality divergence on this shelf.**
Hydrogenated vegetable fats or palm oil as the primary fat source will typically present higher
sat-fat fractions than butter variants, AND may trigger the trans-fat status detection (`trans_fat_status`
at `nova_proxy.py` — the `TRANS_FAT_VETO_THRESHOLD` path if declared industrial trans fat is
present). The veto at `score_engine.py` lines 1804–1819 sets score=0 for confirmed trans-fat
products — an absolute disqualifier.

**Engine behavior (fires correctly, no modification needed):** fat quality scoring via `EV-012`
ratio path + sat-fat red-label cap. No modification needed.

**Rank 2 — Sugar level: the second most impactful signal**

Sugar on the coffee-biscuit shelf typically ranges from 10g (plain digestive, plain tea biscuit)
to 28g/100g (heavily sweetened decorative types, petit beurre variants with icing). The Israeli
red-label threshold is 17.5g. The `ISRAELI_RED_LABEL_1_SUGAR` cap fires at 55 when the threshold
is crossed (`score_engine.py` line 1870). Sugar context classification: these are `SC-5` products
(refined sugar explicitly listed — "סוכר" is an explicit ingredient in virtually every coffee
biscuit, `_classify_sugar_context()` at lines 2397–2427). The elevated SC-5 caps (not SC-2) apply.

The `HIGH_CAL_HIGH_SUGAR_SEVERE` cap (score 50) fires when kcal >= 500 AND sugar >= 25g (line
1857). The `HIGH_SUGAR_25G_PLUS` cap (score 60) fires when sugar >= 25g without the calorie gate
(line 1860). Products at the high end of the sugar range (25–30g/100g) are hard-capped at 50–60.

**Engine behavior (fires correctly, no modification needed):** sugar scoring correctly penalizes
the high-sugar end of this shelf.

**Rank 3 — NOVA class / additive load: the differentiator between "clean" and "processed"**

Within the NOVA-3 band (which covers most of the shelf), additive complexity creates real score
differentiation:

- **Clean NOVA-3 (short ingredient list, benign additives only):** flour, fat, sugar, eggs/milk,
  leavening (baking powder), natural vanilla or cinnamon. Additive category count = 1–2
  (leavening_agent, possibly acidity_regulator). Additive quality score (`score_engine.py`
  line 1456–1464): `base = max(0, 100 - ac * 18)` with `ac = 1–2` → base = 64–82.
- **Typical NOVA-3 with emulsifiers:** adds E471 (mono/diglycerides), lecithin, or similar.
  Additive count rises to 2–3. The identity delta system (`_identity_additive_deltas()`,
  line 1325–1360) applies: lecithin gets +2 relief; more concern-class emulsifiers (carrageenan,
  CMC, P80) get −3 each. The emulsifier complexity penalty (`_emulsifier_complexity()`,
  line 1363–1443) stacks on top.
- **NOVA-4 (synthetic flavor enhancers, artificial colors):** nova4_score >= 4 in `nova_proxy.py`
  line 527. NOVA_PROXY_4_ULTRA_PROCESSED cap fires at 68 (`score_engine.py` line 1960). The
  NOVA-4 products in this category are those using generic flavor systems ("חומרי טעם וריח"
  or "ערוב חומרי טעם וריח") or artificial coloring.

**Flavor enhancers are the key NOVA-4 trigger on this shelf.** The `has_flavor_enhancer` flag in
`nova_proxy.py` line 187 adds 3 to `nova4_score`, sufficient to push most products to NOVA 4 on
its own. An Israeli cookie declaring "חומרי טעם וריח" in the ingredient list is NOVA 4 by engine
logic. This correctly distinguishes a simply-formulated petit beurre from a heavily engineered
industrial biscuit.

**Engine behavior (fires correctly, no modification needed):** NOVA inference, additive quality
scoring, and emulsifier complexity all apply without category-specific modification.

**Rank 4 — Whole-grain vs refined flour**

Digestive-type and whole-grain-variant biscuits present a genuine (if modest) nutritional advantage:
higher fiber, different glycemic profile, lower NOVA class by signal accumulation. The engine
rewards this through:
- `has_whole_grain` bonus of +5 in the glycemic quality score (`score_engine.py` line 1295) and
  `evidence_against` in NOVA via `nova_proxy.py` line 347 (−1 to nova4_score).
- Higher fiber → higher fiber_score in `score_nutrient_density()` (lines 1136–1142).
- Better satiety_support score (`score_satiety_support()`, line 1566).

For coffee biscuits, the whole-grain signal is typically modest in magnitude — a digestive may have
2–4g fiber/100g vs <1g for a plain butter biscuit. This produces real but not dramatic score
separation. **The whole-grain signal fires correctly; no modification needed.**

**Rank 5 — Calorie density**

Coffee biscuits are uniformly energy-dense (430–520 kcal/100g). The `lookup_calorie_density()`
function at `score_engine.py` line 1189 assigns a calorie-density dimension score. Most of the
shelf will land in the penalized mid-range. The calorie-load caps (`HIGH_CAL_LOW_SATIETY_SEVERE`
at 55, line 1924) fire for products with kcal >= 500 and minimal protein/fiber — which describes
a large portion of the shelf.

**Engine behavior (fires correctly, no modification needed).** Calorie density is not differentiating
enough within this shelf to be the "thesis signal" — almost all products are energy-dense.

### 3.3 Signals that do NOT fire meaningfully on this shelf (no action needed)

| Signal | Why it self-gates |
|---|---|
| `HP_FAT_SODIUM_COMBO` (`score_engine.py` lines 2276, 2292–2316) | Sodium on this shelf is low (100–300mg). `HP_FAT_SODIUM_FAT_PCT` threshold fires only when both fat_pct >= threshold AND sodium >= the sodium threshold. With sodium < 300mg, the sodium leg fails, and the combo never fires. No suppression needed; it self-gates. |
| `HP_FAT_SUGAR_COMBO` (`score_engine.py` lines 2275, 2280–2290) | Technically could fire: fat_pct may be high (>35% of kcal) and sugar may exceed the threshold. This IS a legitimate signal for this category — a high-fat + high-sugar biscuit IS a hyper-palatability concern by the engine's definition. **Do not suppress.** Let it fire when it fires. |
| `HP_CRUNCH_SWEET_COMBO` (line 2277) | Category-gated to `category == "cereal"` only. Will never fire for `cookies-coffee` category ID regardless of composition. Self-gates. |
| `brined_food` context flag (`evaluation_scope.py` lines 39–61) | No coffee biscuit name contains "זיתים", "פטה", "בולגרית", etc. Self-gates. Sodium weight = 1.0 for all products in this category (correct). |
| Fermentation bonus | Coffee biscuits contain no live cultures. `has_fermentation` will be False for all products. The fermentation bonus in `score_whole_food_integrity()` (line 1695) never fires. Correct; no action. |
| `concentrated_sweetener` context flag | Only fires for honey, maple syrup, agave. Not applicable. |

### 3.4 HP_FAT_SUGAR_COMBO — ruling on whether to suppress

**Do not suppress HP_FAT_SUGAR_COMBO for this category.** A cookie with 40%+ fat-calories and
22g+ sugar per 100g IS engineered to be highly palatable by the combined fat+sugar mechanism. This
is exactly what the signal was designed to detect. Unlike brined cheese — where fat is structural
dairy fat and sodium is preservation brine — a cookie's fat+sugar profile is an active formulation
choice. The signal fires correctly and should not be suppressed.

---

## 4. Category Caveat Text (Hebrew)

The following is the standard yellow "הערת קטגוריה" box text, grounded in real engine behavior:

---

**הערת קטגוריה: עוגיות לקפה**

כל המוצרים בקטגוריה זו הם מאפים מתוקים מעובדים — ציון A אינו קיים בקטגוריה זו. ציון B (70–79)
מייצג את הטוב ביותר שניתן לצפות לו: מאפה עם שמן איכותי יחסית, פחות סוכר ואדיטיבים בסיסיים בלבד.
רוב הקטגוריה מקבלת ציון C. ההבדלים המשמעותיים ביותר בין המוצרים הם: **סוג השומן** (חמאה / שמן
דקל / שמן מוקשה), **כמות הסוכר** (האם חצה את סף התווית האדומה של 17.5 גרם ל-100 גרם), ו**רמת
הפירוט של רשימת הרכיבים** — מוצרים עם חומרי טעם מלאכותיים, מחמצים מרובים ומשפרי מרקם מקבלים
ציון נמוך יותר. נתרן אינו הנושא בקטגוריה זו — הוא נמוך בכל המוצרים.

---

**English translation (internal reference only):**
All products in this category are processed sweet biscuits — an A grade does not exist in this
category. A B score (70–79) represents the best achievable: a biscuit with relatively better fat
quality, less sugar, and only basic additives. Most of the category scores C. The most meaningful
differences between products are: **fat type** (butter / palm oil / hydrogenated fat), **sugar
level** (whether the 17.5g/100g Israeli red-label threshold is crossed), and **ingredient-list
clarity** — products with artificial flavor agents, multiple emulsifiers, and texture modifiers
score lower. Sodium is not the story here — it is low across all products.

---

## 5. Anti-Collapse Check

### 5.1 What the engine produces without modification

The committed engine (no new rules, no flag changes) produces the following outcomes for this shelf:

- **NOVA-3, low-to-moderate sugar (<17.5g), moderate sat-fat (7–9g), no artificial flavoring:**
  Score range 63–72 (grade C to low B). The NOVA-3 processing cap is the binding ceiling. Sat-fat
  red label may or may not fire depending on exact value. The result is a realistic C to B spread.
- **NOVA-3, high sugar (>17.5g), high sat-fat (>10g), basic additives:**
  Multiple caps coordinate: ISRAELI_RED_LABEL_1_SUGAR at 55, ISRAELI_RED_LABEL_1_SAT_FAT at 55.
  Binding cap = 55. Grade C.
- **NOVA-3, sugar < 17.5g, high sat-fat (palm-oil dominant):**
  ISRAELI_RED_LABEL_1_SAT_FAT cap at 55 is binding. Score 55–62. Grade C.
- **NOVA-4, any composition:**
  NOVA_PROXY_4_ULTRA_PROCESSED cap at 68, plus any sugar/fat caps that fire.
  Score typically 45–65. Grade C or D.
- **Best case (digestive, whole-grain, moderate fat, <17.5g sugar, no additives beyond leavening):**
  No cap fires except NOVA-3 cap. Score 68–75. Grade B.

This produces **genuine spread**: approximately D (40–54) to B (70–79), with C as the modal grade.
The spread is honest — it reflects real composition differences. It is not manufactured.

### 5.2 Is this spread genuine?

Yes. The differentiation between a clean digestive biscuit (whole-grain flour, butter, minimal sugar,
short ingredient list) and a NOVA-4 industrial biscuit with artificial flavor systems, palm oil, and
sugar above the red-label threshold is real and architecturally significant. The engine captures it
through the NOVA cap, the sat-fat red-label cap, and the sugar cap — all applying simultaneously
where warranted.

### 5.3 Possible clustering scenario

If the Israeli retail scrape finds that 80%+ of the shelf sits at very similar composition
(e.g., 18–22g sugar, 12g sat-fat, 460–480 kcal), the engine will produce clustering around
score 55–63 (grade C) across most products, with only a handful of digestive/whole-grain variants
scoring B. **This is an honest finding, not a failure of the methodology.** Report it in the
category caveat (§4) and in the frontend prologue. Do not add signals to manufacture
differentiation that does not exist in the real corpus.

---

## 6. The Question of New Scoring Rules

### 6.1 Strong default: no new rule needed

The committed engine scores this category correctly:

- NOVA-3/4 processing caps fire as designed.
- Sat-fat red-label cap fires for high-butter/high-palm-fat products.
- Sugar red-label cap fires for high-sugar products.
- Additive quality scoring with emulsifier complexity correctly differentiates clean vs. loaded.
- HP_FAT_SUGAR fires legitimately when both legs are met.
- Sodium self-gates (always low, never fires).
- The `brined_food` flag correctly never fires (no name signals match).

No new scoring rule is needed. Proceed with the committed engine for the corpus run.

### 6.2 Potential future D7 proposal (do not implement now)

After the first real-corpus run, if the engine produces a distribution where nearly all products
sit at 55 (i.e., the sat-fat red-label cap alone is the binding cap for 80%+ of the shelf because
virtually all products have >5g sat-fat/100g), the Nutrition Agent would consider a **category-
specific endemic sat-fat gate** analogous to the `whole_food_fat` endemic gate (`score_engine.py`
lines 2238–2256, `EV-048`). The rationale would be: saturated fat in a butter/shortbread biscuit
is compositionally intrinsic, and the red-label cap was designed to penalize reformulable excess.
The sat-fat signal in regulatory_quality would still register.

**This is a default-off flag-gated proposal only.** It is NOT implemented here and does NOT move
any live score. It requires:
- Full evidence-registry entry (EV-###)
- Nutrition Agent + Product Agent D7 co-sign
- No-regression proof on all live categories
- C3 consult mandatory before shipment ("is the endemic collapse real, and does attenuation
  manufacture spread that does not exist?")

The strong default — no rule change — ships first. This potential proposal is raised for
transparency only.

---

## 7. Summary Table

| Question | Answer |
|---|---|
| In scope | Speculoos/Lotus, petit beurre, tea/marie, butter cookies, shortbread, digestive, biscotti, plain crisp biscuits |
| Chocolate-coated biscuits | OUT. Structural confection, not coffee biscuit. |
| Cream-filled sandwich cookies | OUT. Filled structure, own category. |
| Wafers | OUT. Different matrix entirely. |
| Soft/cake-like cookies | OUT. Fails dry/crisp condition. |
| Children's character cookies | OUT. Consumer occasion mismatch. |
| Protein/functional biscuits | OUT. Macro architecture diverges. |
| Vegan variants | IN. Fat source is a scoring signal, not a scope filter. |
| Gluten-free variants | IN by default if occasion matches; discard if medical/clinical positioning. |
| Organic variants | IN. Certification is process, not structure. |
| Whole-grain variants (digestive) | IN. Whole-grain is a quality differentiator, not an exclusion. |
| NOVA class on this shelf | NOVA 3 (modal); NOVA 4 (engineered/flavor-enhanced variants); NOVA 1/2 not achievable. |
| Grade ceiling | B (70–79). A is not achievable. Confirmed by NOVA-3 cap + sat-fat/sugar cap mechanics. |
| Grade floor | D (40–54) for NOVA-4 heavily engineered products. |
| Primary differentiator | Fat type (sat-fat fraction / unsatFat ratio). |
| Second differentiator | Sugar level (crossing 17.5g red-label threshold). |
| Third differentiator | Additive load and NOVA class (clean NOVA-3 vs NOVA-4 with synthetic flavors). |
| Signature thesis chart | Sugar × sat-fat, colored by grade. Not sodium. |
| Sodium role | Self-gating. Low on all products (100–300mg). No context flag. No sodium modification. |
| HP_FAT_SODIUM | Self-gates (sodium never meets the sodium threshold). No suppression needed. |
| HP_FAT_SUGAR | Fires legitimately. Do not suppress. |
| brined_food context flag | Never fires on this shelf. sodium_weight = 1.0 (correct). |
| Engine changes needed | NONE. Score with the committed engine as-is. |
| Future D7 proposal | Endemic sat-fat gate if collapse is confirmed in real corpus. Default-off. C3 mandatory. |
| New scoring rule shipped here | NONE. |
