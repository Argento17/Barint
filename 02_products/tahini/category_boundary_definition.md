# Tahini — Category Boundary Definition

**Task:** TASK-054  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Category:** Tahini  
**Status:** Pre-lock draft — requires Head of Product sign-off before BSIP0 begins

---

## What This Category Is

**Tahini** is a Bari food category covering paste and spread products whose primary structural ingredient is **ground sesame seed** (whole or hulled), or a preparation made primarily from ground sesame (e.g., tahini blended with lemon, garlic, and water to form a ready-to-eat dip).

The category captures two distinct product sub-types under one consumer purpose: **"what should I buy when I need tahini?"**

| Sub-type | Description | Consumer context |
|---|---|---|
| **Raw tahini** | Pure ground sesame paste, ambient shelf, used as a cooking and dipping ingredient | Buying for cooking: hummus, salad dressing, dips |
| **Ready-to-eat tahini dip** | Tahini preparation with lemon, garlic, water, salt — ready for table use | Buying for immediate consumption without preparation |

Both sub-types answer the same consumer question about tahini quality. They are included together.

---

## What This Category Is Not

Tahini borders four adjacent categories, each of which has a resolved boundary rule:

### Border 1 — Hummus (TASK-026 deferred products)

**Resolved:** Products deferred from the hummus corpus where tahini is the **first ingredient** (by weight). The hummus exclusion_log (produced during Hummus BSIP0) should contain entries for "טחינה מוכנה" and similar products. These are now in scope for Tahini.

**Boundary test:** Is tahini/sesame the **first listed ingredient** by weight?
- YES → Tahini category
- NO (chickpeas first) → Hummus category (already captured in run_hummus_002)

### Border 2 — Halva and Confections

**Resolved:** Halva (חלבה) is a confection made from tahini + sugar in roughly equal proportions. It is not a tahini product in the functional sense — it is a sweet. The distinguishing signal is **declared sugars > 20g/100g** OR the word "חלבה" appearing in the product name.

**Boundary test:**
- "חלבה" in name → OUT (confection)
- "ממרח חלבה" in name → OUT (halva spread)
- Sugars_g > 20 AND primary ingredient is sesame → REVIEW (apply secondary test below)
- Secondary test: is the product sold in the confectionery aisle, or does the product form resemble a bar/block? → OUT

### Border 3 — Chocolate and Sweet Spreads

**Resolved:** Tahini products with chocolate or other dessert-primary ingredients are dessert spreads, not tahini products.

**Boundary test:** Does "שוקולד" (chocolate) appear in the product name or as a primary ingredient?
- YES AND product's primary structural intent is dessert flavoring → OUT
- YES AND "שוקולד" is a minor variant (e.g., "טחינה עם נגיעת שוקולד" = tahini with a touch of chocolate, sugars ≤ 15g/100g) → BORDERLINE; apply percentage rule

### Border 4 — Nut Butters (Deferred to Wave 3)

**Resolved:** Peanut butter, almond butter, cashew butter are NOT in this category. Despite sharing the same BSIP2 archetype (`whole_food_fat`), they are a separate product family for consumer purposes. Israeli consumers buying tahini are not cross-shopping with almond butter.

**Boundary test:** Does the product contain sesame/tahini as the primary ingredient?
- YES → Tahini category
- NO (peanuts, almonds, cashews, hazelnuts as primary) → OUT (Nut Butters, deferred)

---

## Structural Principles

Three structural criteria define what belongs in this category:

**P1 — Primary ingredient is sesame/tahini**  
The dominant ingredient by weight must be sesame paste (raw tahini), whole sesame seeds processed into paste, or sesame-derived concentrate. No other seed or nut qualifies for this category.

**P2 — Format is a paste or liquid preparation**  
The product must be a paste (ambient jar), liquid preparation (ready-to-eat dip), or sauce form. Not a solid (confection bar, cookie, cracker). Not a powder (sesame flour, sesame protein powder).

**P3 — Channel is consumer retail, packaged**  
Sold in standard consumer retail packaging (100g–1kg). Not catering sizes, not sold by weight at the deli counter, not single-serving sachets.

---

## The Ready-to-Eat Tahini Dip Sub-Type

This is the most important classification decision for this category.

### What it is

Ready-to-eat tahini dip ("טחינה מוכנה") is tahini paste prepared for immediate consumption: mixed with water, lemon, garlic, and sometimes parsley or other seasonings. It is sold in refrigerated containers alongside hummus. It is structurally diluted compared to raw tahini — the tahini proportion is typically 20–50% of the final product, with water making up the remainder.

### Why it is included

1. The hummus corpus_filter (TASK-026) explicitly deferred this product type with the note: "Separate category (whole_food_fat)." The deferred boundary is resolved here.
2. Israeli consumers shopping for tahini consider ready-to-eat tahini dip alongside raw tahini. The question "which tahini should I buy?" includes both forms.
3. BSIP2 can meaningfully score these products: the dilution level (water vs. sesame proportion), additive quality, and sodium content vary significantly across brands.

### How BSIP2 distinguishes it

The `whole_food_integrity` dimension will score ready-to-eat tahini dip lower than raw tahini due to higher ingredient count and reconstruction markers. The `calorie_density` dimension will score it higher (lower kcal due to water dilution, ~200–300 kcal vs. ~600 kcal for raw tahini). The net effect is that ready-to-eat dip should score in the B range while pure raw tahini should score A–B — a meaningful, correct differentiation.

### Corpus tagging

Ready-to-eat tahini dips must receive `bsip_tahini_subtype = "tahini_dip_prepared"` in the BSIP1 converter. Raw tahini receives `"tahini_raw"`. This subtype tag enables frontend filtering.

---

## Edge Cases

### EC-1 — Tahini with honey or date paste

**"טחינה עם תמר"** (tahini with date paste), **"טחינה עם דבש"** (tahini with honey)

**Decision: IN scope.**

These are tahini-primary products where a natural sweetener is a secondary ingredient. The primary structural ingredient is sesame. Sugars from honey or date are typically 10–20g/100g — below the halva threshold (20g). Include with `bsip_tahini_subtype = "tahini_sweetened"` tag.

**BSIP2 impact:** The `glycemic_quality` dimension will penalize these products relative to plain tahini (sugar penalty). This is correct — sweetened tahini is structurally different from pure tahini. The penalty is expected and defensible.

**Consumer note:** These products appeal to a different use case (dessert-adjacent dipping) than pure tahini. Including them makes the comparison more useful, not less.

### EC-2 — Organic tahini

**"טחינה אורגנית"** — organic certified sesame paste

**Decision: IN scope.**

Organic certification on tahini indicates minimally processed, pesticide-free sourcing. For a high-oil-content product like tahini (~55g fat/100g), fat-soluble pesticide concentration is a genuine concern. Organic tahini commands a meaningful price premium. Include; the BSIP2 score will not automatically reward organic certification (there is no organic bonus in the engine), but the ingredient list quality and shorter formulation will typically result in high scores on their own merits.

### EC-3 — Whole sesame vs. hulled sesame tahini

**"כל שומשום"** (whole sesame) vs. **"שומשום קלוף"** (hulled sesame)

**Decision: Both IN scope.**

Whole sesame tahini retains the sesame hull, adding fiber and minerals. Hulled sesame tahini removes the hull for a smoother texture. Both are ground sesame paste and belong in the category. Tag as `bsip_tahini_subtype` subfield.

**BSIP2 impact:** Whole sesame tahini may have slightly higher fiber, but the difference is modest. The engine will not reliably distinguish these from nutrition data alone; ingredient text analysis is required.

### EC-4 — Roasted sesame tahini

**"טחינה קלויה"** (roasted tahini)

**Decision: IN scope.**

Roasting is a processing step that does not change the fundamental product identity. Roasted tahini is still ground sesame paste. Include with roasting marker captured by the existing enricher.

### EC-5 — Cooking tahini sauces (heavily diluted)

**"טחינה לבישול"** (cooking tahini), **"רוטב טחינה"** (tahini sauce/dressing)

**Decision: BORDERLINE — apply dilution test.**

Some products are sold as cooking sauces where tahini is a minor ingredient (10–20%) and water, vinegar, and flavorings dominate. These are no longer tahini products — they are tahini-flavored condiments.

**Test:** Is tahini listed as the **first or second ingredient** AND is the declared tahini percentage ≥ 20%?
- YES → IN scope (it is a tahini preparation, not a tahini-flavored condiment)
- NO (water or other ingredients dominant) → OUT (too diluted to be a tahini product)

### EC-6 — Tahini with lemon flavoring only (not the full ready-to-eat dip)

**"טחינה בטעם לימון"** — tahini with lemon flavor added, but NOT a prepared dip

**Decision: IN scope.**

Lemon flavoring is a natural, minimal-processing addition to raw tahini. This is a flavored tahini, not a reconstructed product. Include with `bsip_tahini_subtype = "tahini_raw"` (it is still fundamentally raw tahini).

### EC-7 — Single-serving sachets and on-the-go formats

**"שקית טחינה"** — single-serving tahini sachet (typically 10–30g)

**Decision: OUT scope.**

Single-serving sachets do not display a full nutritional panel per 100g. They cannot be scored on a per-100g basis. Additionally, the serving size comparison is not meaningful — a 10g sachet is a condiment, not a product the consumer uses to evaluate tahini quality.

**Boundary:** Any product where the package size is < 100g AND the format is a single-serving sachet → OUT.

### EC-8 — Tahini as filling in a multi-product package

**"מארז פיתה + טחינה"** — flatbread + tahini pack

**Decision: OUT scope.**

Multi-product packages where tahini is a component (not the main product) are excluded. The tahini inside cannot be evaluated independently.

### EC-9 — Catering / bulk sizes (≥ 1 kg)

**Decision: OUT scope.** Consumer retail only — standard rule applies.

### EC-10 — Shufersal private-label tahini (store brand)

**"שופרסל טחינה"** — Shufersal own-brand tahini

**Decision: IN scope.**

Store-brand products are first-class corpus members. They often represent the mid-market formulation and are highly relevant for consumer comparison. No special handling.

---

## Classification Disputes Protocol

When a candidate product's classification is unclear during BSIP0 candidate review, apply in order:

1. **Name test:** Does the product name contain "טחינה" as the primary word? → IN scope (pending ingredient test)
2. **Ingredient test:** Is tahini/sesame the first listed ingredient? → IN scope
3. **Percentage test:** Is the tahini/sesame percentage declared, and is it ≥ 20%? → IN scope if yes
4. **Halva test:** Does the name contain "חלבה"? → OUT scope
5. **Format test:** Is the product a bar, block, candy, cookie, or cracker? → OUT scope (confection or snack)
6. **Sugar test:** Are declared sugars > 20g/100g AND no "tahini" primary? → REJECT (sweet product)
7. **Escalate:** If still unclear after steps 1–6, escalate to Head of Product with product name, ingredient list, and nutritional data. Do not approve or reject without the escalation.

---

## BSIP2 Archetype Assignment

| Product type | BSIP2 archetype | Calorie density table | NOVA expectation | Floor |
|---|---|---|---|---|
| Pure raw tahini (1–2 ingredients) | `whole_food_fat` | whole_food_fat | NOVA 1 | 85 (SRC-01) |
| Organic tahini (1–2 ingredients) | `whole_food_fat` | whole_food_fat | NOVA 1 | 85 |
| Flavored tahini (lemon, roasted) | `whole_food_fat` | whole_food_fat | NOVA 1–2 | 85 or 70 |
| Ready-to-eat tahini dip (3–7 ingredients) | `sauce_spread` | sauce_spread | NOVA 2–3 | None for NOVA 3 |
| Sweetened tahini (with date/honey) | `whole_food_fat` | whole_food_fat | NOVA 2 | 70 |

**Critical note on ready-to-eat tahini dip routing:** Unlike raw tahini, ready-to-eat tahini dip should route to `sauce_spread`, not `whole_food_fat`. The router already handles this because these products will have "טחינה מוכנה", "ממרח טחינה", or "סלט טחינה" in their names, which will hit the `sauce_spread` anchors added in TASK-044. This must be confirmed in a router pre-run check before BSIP2 executes.

---

*Category Boundary Definition — Tahini — TASK-054 — 2026-05-31*  
*Status: Pre-lock draft. Requires Head of Product sign-off.*
