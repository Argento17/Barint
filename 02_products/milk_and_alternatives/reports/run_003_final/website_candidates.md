# Bari Intelligence — Website & Blog Candidates
## Milk & Alternatives — run_003

**Date:** 2026-05-18

---

## Top 3 Comparison Stories

### Story 1: Dairy vs Plant — The Gap Is Bigger Than You Think

**Comparison:** Whole Milk 3.4% (75, B) vs Oat Barista Drink (48.8, D)

**The story:** Israeli consumers increasingly swap dairy for plant alternatives
in the belief that plant-based is 'healthier.' Bari's structural analysis tells
a different story: whole cow's milk — unprocessed, naturally protein-rich, NOVA 1 —
scores 26 points higher than the leading oat barista drink.

**Why it works for Bari:** Concrete, counterintuitive, backed by transparent scoring.
No vague health claims. Just: here's the structure, here's the matrix, here's the gap.

**Products to show:** `7290000051352` vs `7394376619939`  
**Visuals:** radar_dairy_vs_plant.png, leaderboard.png

---

### Story 2: The Soy Advantage — Why Soy Outperforms Every Other Plant Milk

**Comparison:** Soy Drink no sugar 1L (66.1, C) vs Oat Drink (46.6, D) vs Almond Drink (43.4, D)

**The story:** Among plant milks, soy consistently outperforms oat, almond, and rice.
The reason is simple and structural: soy provides 3.4g protein per 100g — roughly
10× more than almond (0.5g) and 6× more than rice. BSIP2 rewards this protein
contribution across nutrient density, protein quality, and satiety support dimensions.

**Consumer insight:** The 'oat milk boom' is largely aesthetic and cultural, not nutritional.
If plant milk consumers care about protein, soy is the clear structural choice.

**Products to show:** `7290116936116`, `7394376619939`, `5411188112709`  
**Visuals:** category_clusters.png, comparison_tables.md (Soy vs Oat vs Almond)

---

### Story 3: The Hidden Cost of 'Protein Enrichment' — Go Milk vs Whole Milk

**Comparison:** Go Milk Protein 27g (39.5, E) vs Whole Milk 3.4% (75, B)

**The story:** Go Milk boasts 27g protein per serving — a compelling number.
But Bari scores it 35.5 points lower than plain whole milk. Why?
NOVA 4 (sweeteners, flavoring, fortification complex), calorie density penalty
(340 kcal in a 340ml drink), and engineering load all fire simultaneously.
The protein signal is real — but it arrives wrapped in a formulation that
Bari's architecture reads as nutritionally compromised.

**Why it works:** 'More protein = better' is one of the most widespread consumer
misconceptions. This comparison quantifies the tradeoff in a way consumers can see.

**Products to show:** `7290110324773` vs `7290000051352`  
**Visuals:** waterfall_go_milk.png, waterfall_whole_milk.png

---

## Most Surprising Findings

1. **Alpro Almond scored E in run_002** due to a category classification error
   (misclassified as whole_food_fat). After Fix 1 correction, it moved to D (43.4).
   This is architecturally honest: the product is dilute and heavily processed (NOVA 4).

2. **The two Oatly barista variants scored identically.** 'Barista Edition' vs
   'Barista Frothing Edition' — same formula, same score (48.8). Bari does not
   reward packaging claims or marketing positioning.

3. **Alpro Soy Barista 500ml scored lower than basic soy drink 1L.** The barista
   format's acidity regulator pushes it from NOVA 3 to NOVA 4, dropping the score
   by ~19 points. A single additive costs nearly a grade tier.

4. **Organic certification doesn't protect against NOVA 4.** Both Vitariz organic
   rice drinks score D despite their organic claim. Organic does not equal unprocessed.

---

## Best 'Consumer Misconception' Examples for Content

| Misconception | Reality (Bari data) | Products |
|--------------|---------------------|---------|
| Plant milk is healthier | Dairy scores B, best plant milk scores C | 7290000051352 vs 7290116936116 |
| Unsweetened = clean | Alpro Almond unsweetened is NOVA 4 | 5411188112709 |
| More protein = better | Go Milk (27g protein) scores E | 7290110324773 |
| Organic = less processed | Vitariz organic drinks score D | 8000215204219 |
| Barista = premium | Oatly barista = oat drink = 48.8 D | 7394376619939 |
