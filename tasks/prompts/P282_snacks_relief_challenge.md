# P282 / TASK-373 — snacks whole-food relief, independent CHALLENGE (route: C3)

You are an independent challenger (ChatGPT). Advice only — you do NOT build, do NOT edit files, do NOT close anything. Evidence-based reasoning only; flag where you are uncertain.

## Context
Bari scores Israeli supermarket products 0–100 / A–E on nutritional architecture. The snacks ("חטיפים") shelf has 21 products. Current published distribution: **B:1, C:1, D:3, E:16** — 76% in the worst grade. The owner finds this "too low and punishing."

Diagnosis (verified against the engine): clean whole-food date bars — e.g. dates + cashew/almond/coconut butter + 100% cocoa, **zero additives, no added sugar** — score **32/E**, because:
- the date's **intrinsic fruit sugar** (>17.5 g/100g) trips the Israeli regulatory "red label" sugar cap;
- the nut/cocoa **intrinsic fat** (sat-fat >5.0 g/100g) trips the sat-fat red label;
- two red labels → a hard cap of 45, then a fat+sugar "hyper-palatability" penalty (−8) and a soft penalty (−5) → ~32/E.
These caps were designed for engineered confectionery (added sugar, palm oil, syrups).

## Proposed fix (the thing you must challenge)
A flag `BARI_SNACK_WHOLEFOOD_V1` (default OFF) that, for products passing a "whole-food fruit/nut bar" predicate (category snack_bar_granola/whole_food_fat; zero added sugar after negation-correction; no syrup/glucose/refined-sugar/added-oil markers; ≤6 clean ingredients; zero additives):
1. Classifies the intrinsic fruit sugar as SC-2 (whole-fruit) so the added-sugar caps relax to their existing "natural sugar" values;
2. Treats the nut/cocoa sat-fat as endemic (excluded from the ≥2-red-label cap), so a clean date+nut bar is not hit by the cap-45;
3. Suppresses the fat+sugar hyper-palatability penalty for these whole-food bars.
The regulatory red label itself still displays; only the cap/penalty severity changes.

## Your challenge — argue BOTH directions, then give a verdict
1. **Over-correction risk.** A clean date+nut bar is still ~400–540 kcal/100g and ~40 g sugar/100g (intrinsic, but real). Does relieving the caps risk telling a consumer a calorie-dense, sugar-dense product is "good"? Where SHOULD such a bar land — is E genuinely too harsh, and what grade band is defensible (E? D? C? B?) and why? Is the owner right, or is E partly defensible on consumer-outcome grounds?
2. **Loophole / gaming.** Could a manufacturer engineer a product to pass the predicate (few ingredients, "no added sugar", fruit-sugar-dominant) yet still be nutritionally poor? Name concrete failure cases the predicate would wrongly reward.
3. **Calorie/satiety backstop.** If we relax the sugar/fat caps, what should still hold the line so a 540 kcal/100g bar can't reach a high grade? (e.g. a calorie-density or satiety floor that is NOT relieved.)
4. **Coherence.** The clean fiber bar at the top scores 66.8/B (9.9 g sugar). The syrup-and-palm-oil "granola" bars score E. After relief, where should the clean date bars sit RELATIVE to those two anchors to keep the shelf's ranking honest?
5. **Cross-category leakage.** The negation-aware "no added sugar" correction — could it unintentionally help confectionery or other categories if it ever generalized? What guard keeps it snacks/whole-food-scoped?
6. **Intrinsic-vs-added principle.** Bari already de-anchors intrinsic sat-fat for dairy/whole-food fats. Is extending the SAME principle to fruit sugar in whole-food bars consistent and defensible, or is fruit sugar different enough that it shouldn't get the same pass?

## Return
A concise written verdict: for each of the 6 points, your position with reasoning; a single recommended grade band for a clean date+nut bar; the top 2 guardrails you would REQUIRE before this flag is flipped live; and an explicit "over-corrects / correctly-corrects / under-corrects" call. No code. End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`).
