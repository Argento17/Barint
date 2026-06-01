# Tahini + Nut Butters — Wave 2 Acquisition Plan

**Task:** TASK-046  
**Owner:** Head of Product  
**Date:** 2026-05-31  
**Status:** Pre-acquisition planning — no scraping has begun  
**Factory reference:** `C:\Bari\03_operations\factory\category_factory_v1.md`  
**Hummus reference:** `C:\Bari\02_products\hummus\` (Wave 1 frozen baseline)

---

## Preface — Why This Category, Why Now

Tahini and nut butters are the natural Wave 2 category for three reasons:

**1. The hummus corpus already surfaces the boundary.** The hummus corpus_filter (TASK-026) explicitly deferred ready-to-eat tahini dips (`טחינה מוכנה`, `ממרח טחינה`) to a future Tahini category, creating an acknowledged gap in the current coverage. Users who browse the hummus comparison will encounter tahini-adjacent products that are not scored. Closing this gap is a quality-of-service obligation.

**2. BSIP2 routing is already provisioned.** The router has hard anchors for "טחינה" (whole_food_fat, 0.93), "חמאת בוטנים" (0.93), "חמאת שקדים" (0.93), and "חמאת קשיו" (0.93). The whole_food_fat calorie density table is the correct archetype. The engine does not need new routing logic — it needs corpus data.

**3. High user-value differentiation potential.** The tahini and nut butter market spans a wide structural quality range: from a single-ingredient, NOVA 1 pure sesame paste with 50g+ MUFA/PUFA to an industrial peanut butter with palm oil, hydrogenated fat, sugar, and emulsifiers. BSIP2 can surface this contrast clearly and credibly.

---

## Section 1 — Category Definition

### 1.1 Scope Statement

**Tahini + Nut Butters** covers paste products made from ground seeds or nuts, intended for use as a spread, dip base, or cooking ingredient, sold in retail consumer packaging (standard jar or tube formats, single-serving excluded).

The category is bounded by three structural criteria:
- **Primary ingredient** is a whole seed or nut (sesame, peanut, almond, cashew, walnut, pistachio, hazelnut — pure, not as minor ingredient in another product)
- **Format** is a paste or spread (not a powder, not a bar, not a confection)
- **Channel** is packaged retail (not prepared, not deli-counter, not catering)

---

### 1.2 IN Scope

| Product type | Hebrew name examples | Notes |
|---|---|---|
| **Raw/natural tahini** | טחינה גולמית, טחינה טבעית | Core. Single ingredient: ground sesame. May be hulled (קלוף) or whole (מלא/כל שומשום) |
| **Hulled sesame tahini** | טחינה משומשום קלוף | Most common commercial form. IN |
| **Whole sesame tahini** | טחינה משומשום מלא, טחינה כל שומשום | Higher fiber/minerals than hulled. IN |
| **Roasted tahini** | טחינה קלויה | IN — roasting is a processing step, not a reformulation |
| **Light-roasted tahini** | טחינה קלויה בהירה | IN — flavor variant |
| **Organic tahini** | טחינה אורגנית | IN — certification claim, same product type |
| **Ready-to-eat tahini dip** | טחינה מוכנה, טחינה ביתית, ממרח טחינה, סלט טחינה | IN — previously deferred from hummus; now primary target for this category. Includes lemon, garlic, salt. Distinguish from raw tahini by ingredient count and dilution |
| **Tahini with date/honey** | טחינה עם תמר, טחינה עם דבש | IN — tahini-primary product with natural sweetener addition. Note as sweet-variant in corpus |
| **Pure peanut butter** | חמאת בוטנים טבעית, חמאת בוטנים 100%, חמאת בוטנים ללא תוספות | Core. Single ingredient or peanuts + salt only |
| **Commercial peanut butter (smooth)** | חמאת בוטנים חלקה | IN — includes multi-ingredient versions with oil, sugar, emulsifiers |
| **Commercial peanut butter (crunchy)** | חמאת בוטנים פריכה | IN — same formula with peanut pieces |
| **Almond butter** | חמאת שקדים | IN |
| **Cashew butter** | חמאת קשיו | IN |
| **Walnut butter** | חמאת אגוזי מלך | IN |
| **Pistachio butter** | חמאת פיסטוקים | IN — small corpus expected |
| **Mixed nut butter** | חמאת אגוזים מעורבים, מיקס אגוזים | IN |
| **Peanut butter + almond blend** | חמאת בוטנים ושקדים | IN — tahini/nut-primary blends |
| **Sesame + peanut paste** | ממרח שומשום ובוטנים | IN |
| **Protein-enhanced nut butter** | חמאת בוטנים עשירה בחלבון | IN with flag — added protein isolates change structural architecture. Include, annotate for BSIP2 |

---

### 1.3 OUT of Scope

| Product type | Hebrew name examples | Reason |
|---|---|---|
| **Chocolate-hazelnut spread** | נוטלה, ממרח שוקולד ואגוזי לוז | Dessert, not nut butter. Sugar and cocoa are co-primary ingredients. Router: `dessert` |
| **Halva / halva spread** | חלבה, ממרח חלבה | Confection. Tahini + sugar at 1:1 or higher sugar ratio. Router: `dessert` |
| **Chocolate tahini spread** | טחינה שוקולד, ממרח שוקולד וטחינה | Dessert-spread hybrid. Exclude even if "tahini" appears in name — sugar/cocoa are structural co-equals |
| **Hazelnut butter (pure, without chocolate)** | חמאת לוז (ללא שוקולד) | Edge case — see Section 1.5. Tentative: OUT pending shelf survey confirmation |
| **Nut-based energy bars** | חטיפי אגוזים, בר אגוזים | Format is bar, not paste. Router: `snack_bar_granola` |
| **Nut powder / almond flour** | אבקת שקדים, קמח שקדים | Raw baking ingredient, not a spread |
| **Peanut powder / PB2** | אבקת בוטנים, חלבון בוטנים | Powder format; different consumer purpose; different nutritional profile |
| **Sesame oil** | שמן שומשום | Oil, not paste. Router: `whole_food_fat` — same archetype but different product class |
| **Seed mix (whole seeds, not paste)** | גרעיני שומשום, בוטנים קלויים | Raw whole ingredient, not a paste |
| **Tahini-based sauce (for cooking)** | ממרח טחינה לבישול | Ambiguous — see edge case EC-5 |
| **Jam / fruit spread** | ריבה, ממרח פרות | Different category entirely |
| **Honey** | דבש | Condiment, single-ingredient; insufficient BSIP2 differentiation surface |
| **Date syrup / date paste** | סירופ תמרים, ממרח תמרים | Sweetener/condiment. If date + nut butter blend → evaluate by primary ingredient rule |
| **Catering / food-service sizes (≥1 kg)** | טחינה 1 ק"ג (מוסדי), 5 ק"ג | Consumer retail scope only |
| **Single-serving sachets / shots** | פורשן טחינה | Insufficient nutrition data surface; no per-100g context |
| **Multi-packs** | מארז 3×, טחינה ×2 | Pack format, not product |

---

### 1.4 Blend Rules

The Tahini + Nut Butters boundary requires four explicit blend rules, because adjacent categories share primary ingredients.

**BR-1 — Tahini vs. Halva**

*Rule:* If the first two ingredients are sesame/tahini AND sugar in either order, and the product is shelf-stable confection, REJECT as halva. If sesame/tahini is first and sugar is clearly a minor ingredient (≤20g/100g declared) or absent → APPROVE as tahini.

*Test:* Declare `sugars_g > 20g` as the halva exclusion threshold. Products with `sugars_g ≤ 20g` and "טחינה" in the name → APPROVE. Products with `sugars_g > 20g` and "חלבה" anywhere → REJECT.

*Hebrew trigger signals:* `חלבה`, `ממרח חלבה`, `חלווה` → hard exclude.

**BR-2 — Tahini vs. Chocolate Spreads**

*Rule:* If a product name contains "שוקולד" AND the primary flavour is chocolate (sugar + cocoa as structural co-equals) → REJECT to `dessert`. If "שוקולד" appears as a minor flavour modifier in a tahini product (`טחינה עם נגיעת שוקולד` = tahini with a touch of chocolate) → case-by-case evaluation.

*Test:* If `sugars_g > 30g/100g` AND chocolate/cocoa is a named ingredient → REJECT. Otherwise, if "טחינה" is first ingredient with `sugars_g ≤ 20g` → borderline, include with note.

**BR-3 — Nut Butter vs. Chocolate-Nut Spread**

*Rule:* Hazelnut butter (pure ground hazelnuts, no chocolate) = APPROVE. Hazelnut butter with cocoa/chocolate = REJECT to `dessert`. Any product in the "חמאת לוז + שוקולד" family → REJECT.

*Test:* "נוטלה" → hard exclude. "לוז" alone in product name without "שוקולד" → evaluate ingredients; if hazelnuts ≥ 50% and sugar ≤ 15g/100g → APPROVE. Rare in Israeli market; expect <3 products in corpus if any.

**BR-4 — Tahini Dip vs. Hummus**

*Rule:* Products where tahini is a component of hummus (chickpeas are the first ingredient) were captured in the Hummus category. Here, tahini IS the primary ingredient. Products named "סלט טחינה", "טחינה מוכנה", "טחינה ביתית" where the ingredients lead with tahini/sesame → APPROVE. Products named "חומוס עם טחינה" where chickpeas lead → already in Hummus, DO NOT double-include.

*Test:* First ingredient is sesame/tahini → APPROVE. First ingredient is chickpeas → already in Hummus → REJECT to avoid duplication.

---

### 1.5 Edge Cases

**EC-1 — Tahini with honey or date paste ("טחינה עם דבש" / "טחינה עם תמר")**

These are legitimate tahini products with a natural sweetener addition. Include. They have structural significance: the sweetener addition is a minor modification of a whole-food paste, not a reformulation. Note the `sugars_g` value in the corpus — it will be elevated (10–25g from the sweetener) but the product architecture is still tahini-primary. Flag for BSIP2 that the `glycemic_quality` dimension will penalize these relative to plain tahini.

**EC-2 — Organic nut butters with expeller-pressed oil added ("חמאת שקדים אורגנית עם שמן קנולה")**

Some organic nut butters add an expeller-pressed oil (canola, sunflower) to achieve a smoother texture. This is structurally inferior to pure nut butter but not as problematic as hydrogenated oil addition. Include. The `has_seed_oil` signal will fire; the `fat_quality` dimension will apply the seed oil penalty (currently −3 points). This is appropriate.

**EC-3 — "Nut spread" vs. nut butter — percentage threshold**

Israeli regulations require a product to contain ≥ 90% peanuts to be called "חמאת בוטנים" (peanut butter). Products with lower nut content may be called "ממרח בוטנים" (peanut spread). Include both if nuts are the primary ingredient. The nut percentage distinction is a quality signal that will be surfaced in BSIP2 via ingredient list analysis.

**EC-4 — Protein-fortified peanut butter ("חמאת בוטנים + חלבון")**

These products add whey isolate or pea protein to achieve >30g protein/100g. Include with annotation. BSIP2 will penalize the protein-fortified structure (isolate source, longer ingredient list). The `protein_quality` dimension will apply the isolate discount factor (0.70×). This is the expected behavior — it parallels the protein-enriched hummus handling.

**EC-5 — Tahini-based cooking sauce (e.g., "ממרח טחינה לתיבול")**

Some products marketed as tahini-based cooking sauces are heavily diluted and flavored (water, lemon, garlic, spices at high proportion). If dilution is visible in the ingredient order (water first, tahini third or later), the product has left the "nut butter/paste" structural class. Apply the same first-ingredient test as BR-4: if tahini/sesame is first ingredient, APPROVE; if water is first, EVALUATE by declared tahini percentage; if no percentage declared and water is first, REJECT.

**EC-6 — Almond + date protein butter (marketed as a clean label supplement)**

Products named "חמאת שקדים ותמרים עשירה בחלבון" (almond + date protein butter) may have nuts as primary but protein isolate added. These are borderline with the supplement quarantine. Apply: if `ingredients_list` starts with nuts and the supplement quarantine check does not fire (`has_whey + maltodextrin` or sport name), APPROVE with protein-isolate flag. If the product is clearly a meal-replacement (supplement quarantine fires), EXCLUDE.

**EC-7 — Sesame tahini certified Kosher for Passover ("כשר לפסח")**

No exclusion. Pesach-certified tahini is the same product. The Pesach certification does not change the ingredient architecture. Include normally.

**EC-8 — Hazelnut butter, pure (no chocolate)**

Hazelnut butter is a rare product in the Israeli market. If found: if it is pure ground hazelnuts (≤2 ingredients: hazelnuts + salt), APPROVE. If it contains cocoa, sugar, palm oil → REJECT to dessert. Expect 0–2 products if any. Note that the router does not have a "חמאת לוז" anchor; it would route via "ממרח" (sauce_spread signal, weak) or default. Add to router pre-run check list.

---

## Section 2 — Retail Shelf Mapping

### 2.1 Shufersal

Shufersal organizes tahini and nut butters across two shelf hierarchies — one for natural/dry goods (stable shelf) and a secondary presence in the organic/health-food section.

**Primary shelf: מזון יבש → ממרחים ורוטבים (Dry Foods → Spreads and Sauces)**

| Subcategory | Expected Label | Scrape strategy | Contamination estimate | Notes |
|---|---|---|---|---|
| טחינה | Tahini | **Full traversal** | ~10–15% | Core. Contains raw tahini, ready-to-eat tahini. Minor contamination from tahini-sesame energy bars |
| חמאת אגוזים ובוטנים | Nut butters and peanut butter | **Full traversal** | ~20–30% | Peanut butter, almond butter, cashew butter. Contamination from chocolate-nut spreads (Nutella-style) and nut-based protein spreads |
| ממרחים מתוקים | Sweet spreads | **Search-only / Selective** | ~70–80% | Halva spreads, jam, chocolate spreads, honey — mostly OOS. Target only confirmed nut butter brand variants shelved here |
| מזון אורגני / מזון טבעי | Organic / natural foods | **Selective — search-within** | ~40–50% | Organic tahini, organic nut butters often shelved here rather than in primary code. High quality products may only appear here |
| ממרחים מלוחים | Savory spreads | **Do not traverse** | ~80% | Contains hummus, eggplant, matbucha (already captured). Minimal tahini presence |

**Recommended Shufersal search queries (Hebrew):**

| Query | Expected results | Priority |
|---|---|---|
| `טחינה` | All tahini products | HIGH |
| `חמאת בוטנים` | Peanut butter | HIGH |
| `חמאת שקדים` | Almond butter | HIGH |
| `חמאת קשיו` | Cashew butter | MEDIUM |
| `חמאת אגוזים` | Mixed nut butter | MEDIUM |
| `ממרח שומשום` | Sesame spread (alt naming) | MEDIUM |
| `טחינה גולמית` | Raw tahini | HIGH |
| `טחינה מוכנה` | Ready-to-eat tahini dip | HIGH |
| `טחינה ביתית` | Home-style tahini | MEDIUM |
| `חמאת פיסטוקים` | Pistachio butter | LOW |
| `חמאת לוז` | Hazelnut butter | LOW (EC-8 flag) |
| `טחינה אורגנית` | Organic tahini | MEDIUM |
| `חמאת בוטנים טבעית` | Natural peanut butter | MEDIUM |

**Known contamination sources at Shufersal:**

| Contamination type | Hebrew | Volume estimate | Exclusion mechanism |
|---|---|---|---|
| Nutella + chocolate-nut spreads | נוטלה, ממרח שוקולד ואגוזי לוז | 8–12 products | BR-3 / hard-exclude on "שוקולד" in name |
| Halva and halva spreads | חלבה, ממרח חלבה | 5–10 products | BR-1 / hard-exclude on "חלבה" |
| Nut-based protein powder | אבקת בוטנים, PB2 | 3–5 products | Format hard-exclude: "אבקת" in name |
| Energy bars (nut-based) | חטיפי אגוזים, בר אגוזים | 4–8 products | Format hard-exclude: "חטיף", "בר" in name |
| Sesame-flavored snacks | ביסלי שומשום, קרקרים שומשום | 3–5 products | Format hard-exclude: "ביסלי", "קרקר", "חטיף" |
| Whole seeds (not paste) | גרעיני שומשום, בוטנים שלמים | 3–6 products | Format: "גרעין" + not "ממרח"/"חמאת" |
| Sesame oil | שמן שומשום | 2–4 products | Format: "שמן" in name |
| Date paste / date butter (OOS) | ממרח תמרים, חמאת תמרים | 3–5 products | Reject by primary ingredient (date, not nut/seed) |

---

### 2.2 Yohananof

Yohananof is the secondary retailer. It has a different shelf hierarchy and covers a subset of the same brands, plus some private-label and local brands not listed at Shufersal.

**Strategy:** Run search queries for the same term list as Shufersal. Do NOT attempt full shelf traversal at Yohananof — the shelf hierarchy differs and contamination risk without probing is high. Search-first, then inspect results.

**Yohananof-specific considerations:**
- Private-label nut butters under the Yohananof brand (if any) — include
- Local brands more common at Yohananof: expect 5–10 tahini products not found at Shufersal
- Nutrition data quality from Yohananof scraper is generally comparable to Shufersal
- Barcode cross-matching: EAN-13 barcodes on nut butters tend to be clean; short-code risk is lower than in hummus (where many private-label products had internal IDs)

**Retailer difference note:** Some premium organic nut butters (e.g., brands like Artisana, Once Again, if distributed in Israel) may appear on Yohananof and not Shufersal. These are worth capturing — they represent the structural quality ceiling for the category (often NOVA 1, single ingredient, cold-pressed).

---

### 2.3 Contamination Risk Ranking

| Risk level | Source | Mitigation |
|---|---|---|
| **High** | Chocolate-nut spreads (Nutella-style) shelved alongside nut butters | Hard-exclude: "שוקולד" + "לוז" OR "נוטלה" in product name |
| **High** | Halva / halva spread (same primary ingredient as tahini) | Hard-exclude: "חלבה" in product name |
| **Medium** | Protein-enriched nut butters borderline with supplements | Supplement quarantine signal; allow through if not meal-replacement format |
| **Medium** | Nut-based snack bars shelved in same section | Hard-exclude: "חטיף", "בר", "ברים" in product name |
| **Medium** | Sesame seed bags / whole seeds | Hard-exclude: "גרעיני שומשום" without paste/spread term |
| **Low** | Tahini-containing sauces heavily diluted with water | Apply EC-5 first-ingredient test in candidate review |
| **Low** | Ready-to-eat hummus with tahini as secondary ingredient | Apply BR-4; chickpea-first = already in hummus, reject |

**Critical shelf probe before full scrape (required):** Before committing to full traversal of any shelf code, run the probe script (shufersal_probe_v3.py or equivalent) on the raw product list for that code. Calculate: (OOS names in first 30 products / 30). If contamination rate > 40%, switch to search-only for that code. Hummus learned this the hard way with A162407 (80% contamination).

---

## Section 3 — Corpus Estimate

### 3.1 Discovery Estimates by Product Type

| Product type | Expected discovery (raw) | Expected approval | Expected after cleanup |
|---|---|---|---|
| Raw/natural tahini (all variants) | 30–45 | 28–42 | 25–38 |
| Ready-to-eat tahini dip | 8–15 | 7–13 | 6–12 |
| Tahini with sweetener (date/honey) | 4–8 | 4–8 | 4–7 |
| Pure peanut butter (natural/100%) | 6–10 | 6–10 | 5–9 |
| Commercial peanut butter (multi-ingredient) | 10–18 | 9–16 | 8–14 |
| Almond butter | 6–12 | 5–11 | 4–10 |
| Cashew butter | 4–8 | 3–7 | 3–6 |
| Mixed nut butter | 3–6 | 3–5 | 2–5 |
| Other nut butters (walnut, pistachio, hazelnut) | 3–6 | 2–5 | 2–4 |
| Protein-enhanced nut butter | 4–8 | 3–6 | 3–5 |
| **Total** | **78–136** | **70–123** | **62–110** |

### 3.2 Expected Exclusions

| Exclusion type | Expected count |
|---|---|
| Chocolate-nut spreads (OOS) | 8–14 |
| Halva / halva spread (OOS) | 5–10 |
| Nut-based snack bars / energy bars | 4–8 |
| Whole seeds / peanuts (not paste) | 3–6 |
| Nut powders / PB2 / almond flour | 3–5 |
| Sesame oil (liquid, not paste) | 2–4 |
| Multi-packs / catering sizes | 3–6 |
| Date paste / honey (not nut-primary) | 2–4 |
| **Total expected exclusions** | **30–57** |

### 3.3 Final Corpus Estimate

| Scenario | Expected corpus size |
|----------|---------------------|
| Conservative | 55–65 products |
| Expected | 70–85 products |
| Optimistic (both retailers, high organic section yield) | 90–110 products |

**Minimum viable corpus for BSIP2:** 30 products (hard gate). This is comfortably exceeded in all scenarios.

**Expected corpus composition (mid-scenario, ~75 products):**
- Tahini (raw, ready-to-eat, sweetened): ~45–50 products (60%)
- Peanut butter (natural + commercial): ~15–18 products (20%)
- Almond, cashew, mixed, other: ~10–12 products (15%)
- Protein-enhanced nut butters: ~3–5 products (5%)

**Subcategory richness comparison vs. hummus:**
Hummus had a clean dominant type (hummus spread) with secondary types (matbucha, eggplant). Tahini + nut butters has TWO substantial primary types (tahini and peanut butter) each large enough to generate meaningful within-subtype comparisons. This is structurally richer than hummus and will require a subcategory tag in the BSIP1 schema (`bsip_tnb_subtype`) to enable subtype filtering on the frontend.

### 3.4 BSIP0 Gate Thresholds (proposed)

| Criterion | Threshold | Notes |
|---|---|---|
| Total approved products | ≥ 45 (target 65+) | Higher than hummus minimum (30) to ensure rich comparison |
| Nutrition coverage (kcal + protein + carbs + fat) | ≥ 85% | Nut butters are packaged goods with reliable labels; set threshold higher than hummus |
| Fat data coverage | ≥ 90% | Critical for this category — fat_quality is the primary dimension. Must verify fat_g > 30g for tahini products before proceeding |
| Ingredient list coverage | ≥ 80% | Higher than hummus because single-ingredient pastes have simple labels |
| Image URL | ≥ 90% | Standard |
| Fat anomaly spot check | Required | Before gate passes: verify that `fat_g` for a sample of 5 tahini products (expected 55–60g/100g) reflects total fat, not saturated fat sub-row. Shufersal's fat-row parsing defect (TASK-039) must not silently corrupt this category's primary scoring dimension |

---

## Section 4 — BSIP2 Relevance

### 4.1 Dimension Relevance Ranking for This Category

Unlike hummus, where calorie_density and additive_quality were the dominant differentiators, tahini + nut butters are differentiated primarily by fat quality, processing level, and ingredient purity.

| Dimension | Weight | Category relevance | Expected differentiation |
|---|---|---|---|
| **fat_quality** | 8% | **CRITICAL** | This is the primary structural differentiator. Pure sesame fat (MUFA/PUFA from sesame) vs. industrial peanut butter (partially hydrogenated + palm oil) produces the widest score spread in this dimension. Expected range: 20–90. |
| **processing_quality** | 15% | **HIGH** | Raw tahini = NOVA 1 (95 score). Natural nut butter with nuts + salt = NOVA 1–2. Industrial peanut butter with emulsifiers, palm oil, sugar = NOVA 3 (65). This dimension alone spans 30 points across the corpus. |
| **additive_quality** | 10% | **HIGH** | Single-ingredient tahini = 100. Peanut butter with palm oil, emulsifiers, sugar, stabilizers = 46–64. 10 additive categories × 18 = −180, capped at 0. Differentiates clearly within the nut butter subcategory. |
| **whole_food_integrity** | 4% | **HIGH** | Amplifies processing_quality signal. NOVA 1 whole food = 100 base minus complexity penalty. For tahini: 100 − (1 ingredient − 8 × 2) = 100. For industrial nut butter with 8 ingredients: 100 − 0 = 100 (at 8 ingredients, no penalty). For 12-ingredient nut spread: 100 − (12−8)×2 = 92. Not a large differentiator on its own, but consistent signal. |
| **calorie_density** | 15% | **MEDIUM — mostly uniform** | All products in this category are calorie-dense (500–650 kcal/100g). The whole_food_fat table rates 500–650 kcal at 85. Most products will cluster here. Discrimination is low within the category — this dimension will not distinguish tahini brands. Exception: ready-to-eat tahini dip (~300 kcal) may fall into the 85-90 tier. |
| **nutrient_density** | 15% | **MEDIUM** | Protein content is uniformly high (15–30g/100g) across the category. Fiber varies: whole sesame tahini has 3–5g fiber; hulled tahini has 1–2g. This will create modest within-tahini differentiation. Nut butter protein is similarly high. Not the primary differentiator. |
| **glycemic_quality** | 12% | **MEDIUM-LOW for most** | Plain tahini and plain nut butters have near-zero sugar → glycemic_quality ~90. Products with added honey/date (EC-1) have 10–25g sugar → glycemic_quality 40–65. This dimension cleanly flags sweetened variants. |
| **protein_quality** | 10% | **LOW-MEDIUM** | All products will score "whole_food" protein source (sesame, peanut, almond → not isolate, unless protein-fortified). Base protein score will be 70–95. Protein-fortified products (EC-4) get 0.70× discount → 49–67 range. This is a clean flag for protein-fortified variants but does not otherwise differentiate the core corpus. |
| **regulatory_quality** | 5% | **LOW** | Few if any products will exceed Israeli red label thresholds. Sodium is low in this category (plain tahini: 0–50mg/100g; commercial peanut butter: 150–350mg/100g). Saturated fat may be relevant for palm oil-heavy nut butters (palm oil is ~49% saturated). If a product crosses 5g sat_fat/100g, the sat_fat red label fires. Check: peanut butter with palm oil may have 7–9g sat_fat/100g from palm oil → red label fires → cap at 55. |
| **satiety_support** | 6% | **LOW** | All products are high in protein and fat. Satiety formula (`(prot×3 + fiber×5) / kcal × 400`) will be uniformly high. This dimension will not differentiate within the category. |

### 4.2 Fat Quality — Primary Signal Analysis

Fat quality is the primary differentiating dimension for this category and warrants detailed pre-run analysis.

**Fat composition by product type (approximate):**

| Product type | Total fat (g/100g) | Saturated (g) | MUFA (g) | PUFA (g) | sat_frac | Expected fat_quality score |
|---|---|---|---|---|---|---|
| Pure sesame tahini | 55–60 | 7–9 | 22–25 | 24–27 | 13–16% | **75–85** (low sat_frac, whole food) |
| Ready-to-eat tahini dip | 15–25 | 2–4 | 6–10 | 6–10 | 14–17% | **75–85** (diluted but good sat profile) |
| Natural peanut butter (nuts only) | 48–55 | 8–12 | 24–28 | 12–16 | 17–22% | **60–75** (higher sat_frac than tahini) |
| Commercial peanut butter (+ palm oil) | 50–58 | 12–18 | 20–24 | 10–14 | 23–32% | **35–55** (palm oil elevates sat, seed_oil penalty −3) |
| Almond butter (natural) | 52–58 | 4–6 | 35–38 | 11–14 | 8–11% | **85–92** (best fat profile in category) |
| Cashew butter | 44–50 | 8–10 | 23–26 | 7–9 | 18–22% | **60–72** |
| Walnut butter | 60–65 | 6–8 | 14–16 | 38–42 | 10–12% | **80–88** (highest PUFA, omega-3) |

**Engine fat_quality formula review:**
```
base = max(0, 100 - sat_f × 3.0 - sat_frac × 25)
seed_pen = 10 if has_seed_oil else 0
score = max(0, base - seed_pen - trans_pen)
```

For almond butter (sat_f=5g, sat_frac=0.10): `base = 100 - 15 - 2.5 = 82.5`. No seed oil penalty. Expected: **82–85**.
For palm-oil peanut butter (sat_f=15g, sat_frac=0.28): `base = 100 - 45 - 7 = 48`. Plus seed oil penalty −10. Expected: **~38**.

The formula correctly differentiates. Almond butter will be the fat_quality leader; palm-oil peanut butter will be the trailer.

**Critical data quality check for this category:**
The Shufersal fat-row scraping defect (TASK-039) corrupted hummus fat data by capturing saturated fat instead of total fat. For tahini (total fat ~55g, saturated fat ~8g), the same bug would produce `fat_g = 8` instead of `fat_g = 55`. This is a different failure mode than hummus (where `fat_g = 0.5` was visibly implausible). For tahini, `fat_g = 8` might appear plausible as a saturated fat reading.

**Required pre-run fat audit:** Before BSIP2 can run on this category, execute a caloric gap analysis (per TASK-039 methodology) on all tahini products:
- Implied fat from kcal: `(kcal − protein×4 − carbs×4) / 9`
- For tahini at 600 kcal, 20g protein, 15g carbs: `(600 − 80 − 60) / 9 = 51.1g`
- If `fat_g` scraped = 8 (saturated fat) but implied fat = 51g → gap = 43g → critical anomaly
- This audit must be a mandatory gate item for BSIP0

### 4.3 Emulsifier Differentiation (EV-003 relevance)

The BSIP2 evidence registry EV-003 flags CMC (E466) and Polysorbate 80 (E433) as high-risk emulsifiers, distinct from soy lecithin (E322, neutral) and gum arabic (prebiotic). For nut butters, this distinction is highly relevant:

- Natural nut butter: no emulsifiers — oil separation is natural and expected
- Industrial nut butter: often contains mono- and diglycerides (מונו ודי גליצרידים) or lecithin (לציטין) to prevent oil separation
- Some nut butters use hydrogenated palm oil as a stabilizer, which is structural rather than an additive

**Current BSIP2 handling:** The `additive_quality` dimension treats all additive categories with uniform penalty weight. For this category, the distinction between lecithin (functionally benign) and mono/diglycerides (different risk profile) matters more than in hummus.

**Pre-run check:** Verify which emulsifier types appear in the corpus before scoring. If CMC or Polysorbate 80 are present, the EV-003 differentiation (pending full implementation) would most benefit this category. Flag for the CNO if confirmed.

### 4.4 Matrix Quality

`whole_food_integrity` (4% weight) uses NOVA level and ingredient count. For this category:
- NOVA 1 (pure sesame/nut): WFI = 100
- NOVA 2 (minimally processed with natural additives like salt): WFI = 85
- NOVA 3 (commercial nut butter with palm oil, sugar, emulsifiers): WFI = 60 − complexity_penalty

The complexity penalty (`max(0, (ing_count − 8) × 2)`) will apply to any nut butter with more than 8 ingredients. Industrial peanut butter with 10–12 ingredients will incur a penalty of 4–8 points on WFI.

**Note:** For single-ingredient tahini (1 ingredient: sesame), the NOVA 1 single-ingredient floor (85) applies via SRC-01 if confidence is high. This means simple tahini products are protected from data gaps — even if nutrition data is partly missing, they cannot score below 85. This is the correct behavior for a pure whole food.

---

## Section 5 — New Category Questions

### 5.1 Category-Specific Signals — Identify Only, Do Not Implement

These signals are not currently detectable or not currently in the scoring engine. They represent hypotheses about structural quality that require a CNO ruling before implementation.

**Q-1 — Sesame hull status signal**

*Question:* Does whole sesame tahini ("כל שומשום", "שומשום מלא") warrant a positive quality adjustment relative to hulled tahini ("שומשום קלוף")?

*Why it matters:* The sesame hull contains a meaningful fraction of fiber, calcium, and antioxidants (sesamin, sesamolin). Removing the hull produces a smoother, lighter-flavored tahini but reduces the food's whole-food nutritional density. A consumer comparing "גולמי כל שומשום" vs. "גולמי שומשום קלוף" at the same price should know which is more nutritionally complete.

*Signal candidate:* Presence of `כל שומשום`, `שומשום מלא`, `שומשום בלתי קלוף` → `is_whole_sesame = True` → positive signal.

*Current state:* Not in any existing signal layer. Would require addition to `ADDITIVE_TERMS` or a new dedicated signal in L3.

**Q-2 — Oil addition to nut butter signal**

*Question:* Should nut butter products that add refined oil to achieve smoother texture be penalized relative to pure nut pastes?

*Why it matters:* Adding refined oil (e.g., "שמן קנולה" or "שמן ניצן") to peanut or almond butter changes the fat profile and ingredient count without improving the structural food architecture. It is a formulation shortcut to reduce viscosity and prevent hardening.

*Signal candidate:* If `ingredients_list` contains any refined oil term AND `protein_g_per_kcal < threshold` → flag as oil-diluted. Or: any oil listed beyond position 3 in the ingredient order, in a product whose first ingredient is a nut/seed.

*Current state:* Partially captured by `has_seed_oil` → −3 penalty on `fat_quality`. May not fire consistently if the oil is listed as a sub-ingredient.

**Q-3 — Natural separation declaration signal**

*Question:* Should products explicitly marketed as "oil separates naturally" (a proxy for no emulsifiers, no hydrogenated fat) receive a quality signal?

*Why it matters:* "Natural" peanut butter that separates is structurally superior to "non-separating" commercial peanut butter stabilized with hydrogenated oil or mono/diglycerides. The absence of these stabilizers is currently only detectable via ingredient list analysis (checking for emulsifiers absent), not via a positive claim.

*Signal candidate:* Presence of claim "מפריד שמן טבעי", "שמן נפרד טבעית", "ללא תוספת שמן" → `has_natural_separation = True` → positive signal or emulsifier penalty suppression.

*Current state:* Not in any signal layer.

**Q-4 — Declared nut percentage signal**

*Question:* Should a declared nut content percentage on the label (e.g., "100% שקדים") carry a quality signal?

*Why it matters:* Products declaring 100% nut content have no hidden diluting ingredients. A product that declares "חמאת בוטנים 100%" is structurally different from "ממרח בוטנים" with unstated peanut percentage. The declaration is a transparency signal, like tahini percentage in hummus.

*Signal candidate:* Presence of `100%` adjacent to the nut/seed name in the ingredient text or product name → `has_declared_nut_percentage = True`.

*Current state:* The `ingredient_order[position].percentage_declared` field exists in BSIP1. The enricher does not currently generate a summary flag from this.

**Q-5 — Palm oil stabilizer signal**

*Question:* Should palm oil used as a nut butter stabilizer carry a higher penalty than other seed oils?

*Why it matters:* Palm oil in nut butter serves as a hydrogenated-oil substitute — it prevents oil separation at the cost of elevated saturated fat (palm oil is ~49% saturated). The current `has_seed_oil` penalty (−3 on `fat_quality`) does not distinguish between expeller-pressed canola (minimal structural impact) and palm oil (saturated fat elevation + sustainability concern). The EV-003 evidence registry does not address this specifically (it focuses on emulsifiers), but from a fat quality standpoint, palm oil addition is categorically more impactful than canola addition.

*Signal candidate:* Hebrew terms "שמן דקלים", "שמן דקל" in ingredients → `has_palm_oil = True` → additional fat_quality penalty beyond the existing seed_oil penalty.

*Current state:* The `has_seed_oil` signal fires generically. No palm-specific detection.

**Q-6 — Tahini roasting level signal**

*Question:* Does roasting level (light, medium, dark) of sesame carry a meaningful quality distinction?

*Why it matters:* Dark-roasted tahini has a more intense flavor and lower lignan content than lightly roasted tahini. Some health-food literature suggests lighter roasting preserves more antioxidant compounds. However, the difference is modest and the scientific evidence is less conclusive than for sesame hull status (Q-1).

*Signal candidate:* "קלוי כהה" (dark roasted) vs. "קלוי בהיר" (light roasted) vs. "קלוי" (roasted, unspecified) → `tahini_roast_level`.

*Assessment:* Lower priority than Q-1 through Q-5. Defer pending clearer scientific consensus.

**Q-7 — No-salt-added signal for nut butters**

*Question:* Should "ללא תוספת מלח" (no added salt) nut butters receive a quality signal?

*Why it matters:* Many consumers choose nut butters for controlled sodium intake. "ללא מלח" nut butter at 5mg sodium/100g is structurally different from the same product with 150mg sodium/100g (standard salted version). The regulatory_quality dimension does not capture sub-threshold sodium differences — both are below the 600mg red-label threshold.

*Signal candidate:* Presence of "ללא מלח", "ללא תוספת מלח", "unsalted" → `is_unsalted = True`. Or: `sodium_mg < 20` as a data-driven proxy.

*Current state:* Not in any signal layer. The `sodium_mg` field is available in BSIP1 but no "low sodium" positive signal exists.

**Q-8 — Tahini origin and pressing method**

*Question:* Should cold-pressed sesame, Ethiopian sesame (אתיופי), or Ethiopian humera-type sesame declarations carry a quality signal?

*Why it matters:* Ethiopian humera sesame is widely considered the premium sesame variety for tahini. Some brands explicitly market this. Pressing method (cold-pressed vs. expeller-pressed) may affect oxidation and lignan retention.

*Assessment:* This is a brand-level quality signal, not reliably detectable from ingredient text. Defer — would require a brand database, not an ingredient signal. Document in known-gap register.

---

## Section 6 — Factory Execution Plan

### 6.1 Stage Map with Effort Estimates

| Stage | Activity | Owner | Est. effort | Key risks and mitigations |
|---|---|---|---|---|
| **BSIP0** | Discovery + scrape | Frontend Architect | 1.5–2 days | See below |
| **Gate** | Threshold audit | Frontend Architect | 0.5 day | Include fat anomaly spot-check (mandatory) |
| **Cleanup** | OOS exclusion + exclusion log | Frontend Architect | 0.5–1 day | Halva/chocolate confection contamination higher than hummus |
| **BSIP1** | Conversion + enrichment | Frontend Architect | 0.5–1 day | Mostly reusable from hummus converter |
| **QA** | QA checklist execution | QA & Audit Lead | 0.5–1 day | Add fat_g spot-check as mandatory QA item |
| **BSIP2** | Review framework + batch run + post-run review | Frontend Architect + CNO | 1.5–2 days | Router pre-validation required; fat_quality is key dimension |
| **Total** | — | — | **5–8 working days** | Lean run if hummus factory patterns hold |

### 6.2 BSIP0 Stage Detail

**Step 1 — Probe runs (0.5 day)**

Before any full traversal, run the shufersal probe script on the candidate shelf codes:
- Primary nut butter shelf (expected code in the ממרחים section)
- Primary tahini shelf (expected under טחינה subcategory)
- Organic/health-food section

For each code: list first 30–50 product names, estimate contamination rate. If rate > 40%, switch to search-only.

**Step 2 — Discovery script (0.5 day)**

Adapt `01_discover_hummus_shufersal.py` for this category:
- Replace category codes with tahini/nut butter codes (identified from probe)
- Add search queries from Section 2.1
- Add hard-exclude terms: "נוטלה", "חלבה", "חלווה", "שוקולד" (combined with "לוז" or "ממרח"), "חטיף", "בר", "אבקת"
- Add positive-type terms: "טחינה", "חמאת בוטנים", "חמאת שקדים", "חמאת קשיו", "ממרח שומשום"

**Step 3 — Candidate review (0.5 day, manual)**

Expected ~130–180 raw candidates, of which ~40–60 are REVIEW (not hard-YES or hard-NO). Review REVIEW candidates against the corpus_filter rules and edge cases. Pay special attention to:
- Products with "שוקולד" in name → check BR-2 (chocolate content, sugar level)
- Products with "חלבה" → hard exclude
- Products with "100%" and a nut name → likely high-quality, approve
- Products from the organic section with unfamiliar brands → approve if primary ingredient is nut/seed

**Step 4 — Scrape (0.5 day)**

Run `02_scrape_*.py` on approved candidates. Monitor for:
- Maintenance-mode responses (retry logic required — use existing maintenance check)
- Missing nutrition panels (more common for specialty/organic brands)
- Ingredient text containing marketing copy (truncate at known Shufersal junk markers)

### 6.3 Gate Stage Detail

**Standard gate criteria:** Same as hummus (Section 3.4 above).

**Mandatory non-standard gate item — fat data quality check:**

Before BSIP0 gate can pass, execute:
1. Select a sample of 5 tahini products from the scraped corpus (raw tahini preferred)
2. For each: compute implied fat from caloric balance: `(kcal − protein×4 − carbs×4) / 9`
3. Compare to scraped `fat_g`
4. Accept if gap < 5g. Reject (block gate) if gap > 10g for any sample product.

This check catches the Shufersal fat-row scraping defect before it propagates into BSIP1. Unlike hummus (where the defect produced an obviously implausible 0.5g), for tahini the corrupted value would be plausible-looking (~8g sat fat vs. ~55g total fat). The gate is the only reliable checkpoint.

**Additional gate check — subtype distribution:**

Confirm at least 3 subcategories represented in the approved corpus:
- ≥ 10 raw/natural tahini products
- ≥ 5 peanut butter products
- ≥ 3 other nut butter products (almond, cashew, or mixed)

If any subcategory falls short, supplement with additional Yohananof search before proceeding.

### 6.4 BSIP1 Stage Detail

**Reuse opportunities:**

The hummus BSIP0→BSIP1 converter is approximately 85% reusable. Changes required:
- Update `product_category` field from "hummus_and_savory_dips" to "tahini_nut_butters"
- Add `bsip_tnb_subtype` field (tahini_raw, tahini_prepared, peanut_butter, almond_butter, cashew_butter, mixed_nut_butter, other)
- Subtype inference logic: keyword match on product name (same pattern as hummus `_infer_product_type`)

**Enrichment expectations:**

- Additive extraction: expect fewer additives than hummus (many products are single-ingredient). Additive-heavy products will stand out clearly.
- Sweetener extraction: "דבש" (honey) in ADDED_SUGAR_MARKERS_HE may fire for tahini-with-honey products — this is correct behavior, but note it inflates the "added sugar" signal for a natural product.
- Roasting marker: sesame roasting (`קלוי`, `טחינה קלויה`) will be captured by the existing roasting_markers extraction.
- Matrix markers: starch addition (`עמילן`) in some lower-quality tahini preparations — will fire correctly.
- Fermentation markers: none expected.

**New BSIP1 field required: `tahini_pct_declared`**

Tahini products sometimes declare sesame content percentage (e.g., "100% שומשום"). Add `tahini_pct_declared` (float or null) to the converter, parsed from ingredient text using the same regex as `tahini_pct_declared` in the hummus corpus. This field feeds a future signal (Q-4 declared nut percentage).

### 6.5 QA Stage Detail

**Standard QA checklist:** Apply `category_factory_qa_v1.md` in full.

**Additional category-specific QA checks:**

| Check | Test | Pass criterion |
|---|---|---|
| Fat data plausibility | For all tahini products: `fat_g > 30g` | If any tahini product shows `fat_g < 15g`, flag as potential fat-row anomaly (TASK-039 class defect) |
| Subtype coverage | Count products per `bsip_tnb_subtype` | ≥ 3 subcategories with ≥ 5 products each |
| Ingredient coverage for nut butters | Check `ingredients_list` length | ≥ 85% of products have ≥ 1 ingredient |
| Halva exclusion | Check exclusion_log for "חלבה" entries | At least 1 halva product should appear in exclusion_log (if 0, the acquisition may have missed the shelf code that contains halva) |
| Sugar flag for sweetened tahini | For products with "דבש" or "תמר" in name: `sugars_g > 5` | If any honey-tahini product shows `sugars_g < 2`, check for sugar data corruption |

### 6.6 BSIP2 Stage Detail

**Router validation (pre-run):**

Before the batch run, validate routing for a test sample:
1. Products with "טחינה" in name → must route to `whole_food_fat` via hard anchor ✓ (existing)
2. Products with "חמאת בוטנים" → must route to `whole_food_fat` ✓ (existing)
3. Products with "ממרח שקדים" (almond spread, not using "חמאת") → may route to `sauce_spread` via `ממרח` signal — check and add anchor if needed
4. Products with "חמאת שומשום" (sesame butter, alt naming) → does not hit "טחינה" anchor → check routing; add anchor if needed
5. Products with "ממרח אגוזים" (nut spread, generic) → check routing

**Known router gap to verify:**
- "ממרח שקדים" or "ממרח קשיו" products: the `ממרח` signal scores both sauce_spread (0.65×2=1.30) and whole_food_fat (0.40×2=0.80). Sauce_spread would win if no WFF context signals fire. These products should route to whole_food_fat. Consider adding:
  - "חמאת" → already anchored (covers "חמאת שקדים", "חמאת בוטנים")
  - "ממרח שקדים" → potential anchor needed if significant corpus presence
  - "ממרח אגוזים" → potential anchor needed

**BSIP2 review framework:** Write before the first run (following the hummus_review_framework_v1.md pattern), covering:
- Expected top archetypes: pure single-ingredient tahini, natural almond butter, natural walnut butter
- Expected bottom archetypes: industrial peanut butter with palm oil + hydrogenated fat + sugar + emulsifiers
- NOVA distribution expectations: heavy NOVA 1 corpus (unlike hummus which was NOVA 3-dominant)
- Known failure modes specific to this category (primary: fat_quality data quality if fat-row anomaly persists)

**Expected score distribution:**

| Grade | Expected count (75-product corpus) | Notes |
|---|---|---|
| A (85–100) | 15–25 | Pure single-ingredient NOVA 1 products; floor protection will apply to many |
| B (70–84) | 20–28 | Natural nut butters with minor additions (salt), tahini with lemon/garlic |
| C (55–69) | 15–22 | Commercial nut butters with oil + sugar addition; prepared tahini with stabilizers |
| D (40–54) | 5–10 | Industrial peanut butter with palm oil + hydrogenated fat + sugar + emulsifiers |
| E (0–39) | 0–3 | Possible for products with multiple red labels (high sodium, high sat fat) |
| insufficient_data | 2–5 | Private-label products with no ingredient text |

**The NOVA 1 floor effect will be more pronounced here than in hummus.** With 20–30 single-ingredient NOVA 1 products expected, the floor will protect a larger fraction of the corpus. This is structurally correct — a 1-ingredient sesame paste deserves grade A protection — but it compresses the top of the distribution. The review framework should document this expectation explicitly.

---

## Section 7 — Hummus Factory Lessons Applied

The following lessons from the Hummus Wave 1 experience are directly applicable:

| Lesson | Applied how |
|---|---|
| Fat-row scraping defect can silently corrupt the most important scoring dimension | Mandatory fat plausibility audit at BSIP0 gate (Section 3.4) |
| Hard anchors in the router prevent substring collisions (e.g., "מוס" in "חומוס") | Pre-run router validation for "ממרח שקדים" and "ממרח אגוזים" routing (Section 6.6) |
| Category contamination is higher than expected from shelf codes alone | Probe before full traversal (Section 6.2 Step 1); use Section 2.3 contamination risk table |
| Exclusion logs are mandatory even if the exclusion count is small | exclusion_log.json required; expect 30–57 exclusions to document |
| QA checklist flags issues that pipeline automation misses | Apply full category_factory_qa_v1.md + category-specific checks (Section 6.5) |
| Subcategory diversity requires a subtype tag in BSIP1 for frontend filtering | Add `bsip_tnb_subtype` field in converter (Section 6.4) |
| Products with missing ingredient data can still score (NOVA 1 floor), but grade should be data-conditional | same handling as hummus; `insufficient_data` grade for missing nutrition panels |

---

## Summary

| Dimension | Value |
|-----------|-------|
| **Corpus estimate** | 62–110 products (expected mid-point: ~75) |
| **Subcategory split** | Tahini ~60%, Peanut butter ~20%, Other nut butters ~20% |
| **Shelf strategy** | Full traversal: tahini shelf + nut butter shelf; Search-only: organic section, sweet spreads shelf |
| **Contamination sources** | Halva (BR-1), chocolate-nut spreads (BR-3), nut bars (format), nut powders (format) |
| **Primary BSIP2 differentiator** | `fat_quality` — almond butter (score ~85) vs. palm-oil peanut butter (score ~38) |
| **Secondary differentiators** | `processing_quality` (NOVA 1 vs. NOVA 3 corpus split), `additive_quality` (emulsifier presence) |
| **Category-specific scoring risks** | Fat data anomaly (Shufersal fat-row defect may corrupt primary dimension); NOVA 1 floor dominance; "ממרח שקדים" router gap |
| **Estimated factory effort** | 5–8 working days |
| **Blocking pre-conditions** | corpus_filter.md locked before BSIP0 starts; fat plausibility audit at gate; router gap check before BSIP2 |
| **New signals identified** | 8 (Q-1 through Q-8) — none implemented here; require CNO ruling |
| **Ready to begin BSIP0?** | Not yet — corpus_filter.md for this category must be written and locked first (Stage 3 of factory workflow) |

---

*Wave 2 Acquisition Plan — Tahini + Nut Butters — TASK-046*  
*Owner: Head of Product*  
*Pre-acquisition planning only. No scraping may begin until corpus_filter.md is locked and Head of Product sign-off is recorded.*
