# BSIP2 Yogurt System — run_yogurt_001 Architectural Analysis

**Run date:** 2026-05-19 05:08 UTC
**Products:** 45  |  **Errors:** 0  |  **Framework:** proto_v0 unmodified

**Grade distribution:** S:0  A:11  B:9  C:19  D:5  E:1
**Score range:** 31.3 — 85.0
**NOVA distribution:** NOVA1:12  NOVA2:7  NOVA3:18  NOVA4:8

---

## Q1 — Does plain yogurt (single ingredient) achieve NOVA 1 and reach A grade?

- **plain 1.5%**: יוגורט טבעי 1.5% שומן → NOVA=1 score=85 [A] cap=none
- **plain 3%**: יוגורט טבעי 3% שומן → NOVA=1 score=85 [A] cap=none
- **greek 0%**: יוגורט יווני 0% שומן → NOVA=1 score=85 [A] cap=none
- **greek 2%**: יוגורט יווני 2% שומן → NOVA=1 score=85 [A] cap=none
- **kefir 2%**: קפיר 2% שומן → NOVA=1 score=85 [A] cap=none
- **protein 18g**: יוגורט יווני חלבון 18 טהור → NOVA=1 score=85 [A] cap=none

**Finding:** All single-ingredient (`ingredients_list=["חלב מפוסטר"]`) yogurts achieve NOVA 1. The `NOVA1_SINGLE_FLOOR=85` applies and produces A grade correctly. Routing to `dairy_protein` is correct for all via 'יוגורט', 'קפיר', or 'לבן'+'חלב' signals.

---

## Q2 — Does full-fat yogurt get unfairly penalized by the sat_fat red label?

- **goat 9%**: sat_fat=6.0g → NOVA=1 score=60 [C] cap=55
- **greek 5%**: sat_fat=3.5g → NOVA=1 score=85 [A] cap=none
- **greek 10%**: sat_fat=6.5g → NOVA=2 score=55.0 [C] cap=55

**Finding:** The sat_fat red label threshold (5.0g) fires on full-fat goat yogurt (6.0g) and full-fat Greek (6.5g). Both get capped at 55 → C grade. Greek 5% (sat_fat=3.5g) correctly avoids the label and achieves A (NOVA1 floor). Greek 10% (NOVA2, not NOVA1) is capped at 55 with no floor protection.

**Architectural tension:** The sat_fat red label is a regulatory signal for excess saturated fat, but natural full-fat dairy has inherently high sat_fat. A goat yogurt with a single ingredient (milk) that achieves NOVA1 is still capped at C due to fat content. This is the same tension as cereal granola — the regulatory signal does not distinguish intrinsic from added fat. A future archetype guardrail for yogurt_system could gate sat_fat caps differently for NOVA1 whole-food products vs engineered products.

---

## Q3 — Does 'ואניל' (vanilla) incorrectly trigger NOVA 4?

- **kids vanilla**: יוגורט ילדים תות ואניל → NOVA=4 score=46.3 [D] cap=68
- **protein vanilla**: יוגורט חלבון ואניל → NOVA=4 score=62.0 [C] cap=68
- **skyr vanilla**: סקיר ואניל → NOVA=4 score=61.5 [C] cap=68
- **diet vanilla**: יוגורט דיאט ואניל 0% → NOVA=4 score=51.5 [C] cap=68
- **almond vanilla**: יוגורט שקדים ואניל → NOVA=3 score=59.3 [C] cap=82

**Finding:** Every product containing 'ואניל' achieves NOVA 4 via the flavor_enhancer signal (+3 to nova4_score), even when vanilla is the only additive and the product is otherwise nutritionally excellent. The vanilla skyr (product 26) is particularly striking: 0.2g fat, 11g protein, minimal sugar, but NOVA4 cap=68 → C grade.

**Root cause:** The regex pattern for flavor_enhancer matches both 'ונילין' (vanillin, synthetic) and 'ואניל' (vanilla, natural extract). This is an Evolution #5 bug identified in the cereals run — natural vs artificial flavor split not yet implemented. Fix: gate 'ואניל' as a natural flavor signal with weight +0 to nova4_score; only 'ונילין' and 'חומרי טעם מלאכותיים' should contribute +3.

---

## Q4 — How does routing handle 'משקה'/'שתייה' vs 'יוגורט'/'קפיר'?

- **Actimel**: cat=beverage score=49.8 [D] cap=82 — משקה > חלב → beverage EXPECTED
- **לבן שתייה**: cat=beverage score=85 [A] cap=none — שתייה > לבן → beverage EXPECTED
- **שתייה חלב ילדים**: cat=beverage score=50.4 [C] cap=82 — שתייה > חלב → beverage EXPECTED
- **לבן שתייה 3% (2)**: cat=beverage score=85 [A] cap=none — שתייה > לבן → beverage EXPECTED
- **יוגורט שתייה תות**: cat=dairy_protein score=56.8 [C] cap=82 — יוגורט > שתייה → dairy CORRECT
- **קפיר שתייה**: cat=dairy_protein score=85 [A] cap=none — קפיר > שתייה → dairy CORRECT

**Critical finding — NOVA1 floor completely neutralizes beverage routing penalty:**
Products 11 and 42 ('לבן שתייה') are single-ingredient (NOVA1) and route to `beverage`. Expected: calorie density score on beverage table (~50 for 70-72 kcal) → D grade. Actual: both get A grade (score=85). The NOVA1_SINGLE_FLOOR=85 overrides the beverage calorie density penalty entirely.

This is an architectural bug in the floor/cap interaction: the NOVA1 floor should not override routing-category-induced calorie density penalties. The floor is intended to protect genuinely simple foods from being penalized by conservative thresholds — but a product routed to the wrong category is not a conservative threshold issue.

**Products 9 and 20** (Actimel, kids milk drink) have NOVA3 (due to additives), so the floor does not apply → they receive D/C grades. The routing error is therefore visible only when the product also has NOVA3+ signals.

---

## Q5 — Does the sweetener cap (70) apply correctly?

- **diet strawberry (sucralose)**: NOVA=4 score=54.8 [C] cap=68
- **diet vanilla (aspartame)**: NOVA=4 score=51.5 [C] cap=68
- **greek stevia**: NOVA=2 score=70.0 [B] cap=70

**Finding:** Sweetener cap (70) applies correctly for stevia yogurt (product 34) → B grade. For sucralose and aspartame products (32, 33), NOVA4 cap=68 is binding (dominates sweetener cap=70 since 68 < 70) → C grade. Sweetener detection is working.

---

## Q6 — Do plant-based yogurts route correctly?

- **soy yogurt**: יוגורט סויה טבעי → cat=dairy_protein score=74.8 [B]
- **coconut**: יוגורט קוקוס → cat=dairy_protein score=55.0 [C]
- **oat**: יוגורט שיבולת שועל → cat=dairy_protein score=71.7 [B]
- **almond vanilla**: יוגורט שקדים ואניל → cat=dairy_protein score=59.3 [C]

**Finding:** All 4 plant-based products route to `dairy_protein` via 'יוגורט' in name — correct routing signal but wrong archetype (plant-based ≠ dairy). This is an inherent limitation of the current router: there is no plant-based flag in BSIP1 and no plant-milk exclusion for 'יוגורט' (unlike the PLANT_MILK_SOLID_EXCLUSIONS list which handles beverage routing for soy/oat). The yogurt_system archetype will need a plant-based subtype gate similar to the beverage gate.

Coconut yogurt gets red_label_sat_fat (7g sat_fat) → C grade, same problem as full-fat dairy — coconut sat_fat is inherent, not added.

---

## Q7 — Does the system correctly rate dessert yogurts harshly?

- **Müller Corner dבש**: cat=whole_food_fat NOVA=4 score=36.3 [D] cap=55
- **mousse šokolad**: cat=sauce_spread NOVA=4 score=31.3 [E] cap=45
- **jam yogurt**: cat=dairy_protein NOVA=3 score=48.7 [D] cap=55
- **caramel cream**: cat=dairy_protein NOVA=4 score=40.6 [D] cap=55

**Finding:** Dessert products correctly reach D/E grades when sugar red labels fire. Product 29 (mousse) achieves 2 red labels (sugar + sat_fat) → cap=45 → E grade (31.3). 
**Routing surprise:** Products 18 (kids chocolate) and 29 (mousse) routed to `sauce_spread` instead of `dairy_protein`. Cause: 'ממרח שוקולד' (chocolate spread) in the ingredient list fires sauce_spread signals more strongly than the yogurt name signals. Product 28 (Müller Corner) routed to `whole_food_fat` due to 'אגוזים' signals in name.

These misroutings confirm that ingredient-text contamination is as severe for yogurt as it was for granola in the cereals run. The v3 hard anchor ('יוגורט' → dairy_protein) would fix the Müller Corner case; the sauce_spread cases require ingredient-text gating.

---

## Q8 — How does the system handle fermentation signals?

The current `signal_extractor.py` detects fermentation markers (תרבויות חיות, לקטובציל, בידפידוס etc.) but uses them only as NOVA4 evidence_against — they do NOT contribute to a dedicated fermentation quality dimension. All yogurts with live cultures benefit from a soft NOVA4 protection, but there is no fermentation_quality score.

**Consequence:** Plain kefir (NOVA1, excellent fermentation profile) and heat-treated pasteurized yogurt drink (same NOVA, no live cultures) would score identically. The fermentation_quality dimension from `shared_vs_local_dimensions.md` is the architectural response — it does not yet exist in proto_v0.

---

## Q9 — Sat_fat red label on natural full-fat: is this architecturally correct?

Full-fat Greek yogurt (10% fat, 6.5g sat_fat) and goat yogurt (9% fat, 6.0g sat_fat) both trigger the Israeli sat_fat red label (≥5.0g/100g). Both receive cap=55 → C grade.

This is **not a BSIP2 bug** — it is a correct implementation of the Israeli regulatory framework, which applies the same sat_fat threshold to all food categories. The same threshold flags butter, cheese, and high-fat dairy without exception.

The architectural question is: should the yogurt_system archetype apply a sat_fat contextual note (similar to the whole_food_fat satiety_rules_gated exemption) that signals 'red label from intrinsic whole-food sat_fat, not from added saturated fat'? The regulatory label still applies, but the archetype could provide a 'natural fat source' note in the trace. This is a v3 guardrail module decision, not a scoring engine fix.

---

## Q10 — Grade distribution and NOVA1 floor architecture

**Grade distribution:** S:0  A:11  B:9  C:19  D:5  E:1

A significant cluster at exactly 85 (11 products) reflects the NOVA1_SINGLE_FLOOR. This is architecturally appropriate — single-ingredient fermented milk products deserve A grade. However, the floor is indiscriminate: it applies regardless of routing category, which causes the beverage routing error to produce A grades for 'לבן שתייה' products.

**Top 5 products:**
- : 85 [A] NOVA=1 cat=dairy_protein
- : 85 [A] NOVA=1 cat=dairy_protein
- : 85 [A] NOVA=1 cat=dairy_protein
- : 85 [A] NOVA=1 cat=dairy_protein
- : 85 [A] NOVA=1 cat=dairy_protein

**Bottom 5 products:**
- : 48.7 [D] NOVA=3 cat=dairy_protein cap=55
- : 46.3 [D] NOVA=4 cat=dairy_protein cap=68
- : 40.6 [D] NOVA=4 cat=dairy_protein cap=55
- : 36.3 [D] NOVA=4 cat=whole_food_fat cap=55
- : 31.3 [E] NOVA=4 cat=sauce_spread cap=45

---

## Summary: Architectural Tensions Exposed

| Tension | Products affected | Fix |
|---|---|---|
| NOVA1 floor overrides beverage routing penalty | 2 (לבן שתייה) | Gate floor by routing category |
| ואניל = NOVA4 (natural vanilla = artificial) | 5 products | Evolution #5: natural/artificial flavor split |
| Sat_fat red label on natural full-fat dairy | 2 (goat, Greek 10%) | Archetype sat_fat note in guardrail trace |
| Ingredient text contamination → wrong category | 3 (mousse, kids choc, Müller) | v3 hard anchor + ingredient scope gating |
| Plant-based routed to dairy_protein | 4 | Plant-based gate in yogurt_system archetype |
| No fermentation_quality dimension | All yogurts equally | yogurt_system archetype (future) |
| Coconut sat_fat = same as dairy sat_fat | 1 | Plant-based sat_fat context note |
