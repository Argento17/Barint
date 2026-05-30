# Milk & Alternatives — BSIP2 Run 001 Visual Comparisons

**Generated:** 2026-05-17  
**Source scores:** live BSIP2 pipeline output (batch_run_milk.py)

---

## Score Ranking — All 8 Products

```
Rank  Score  Grade  NOVA  Product
────────────────────────────────────────────────────────────
  1    75.0    B      1    חלב מלא 3.5%           (Whole dairy milk)
  2    71.2    B      2    חלב עשיר בחלבון 6%     (High-protein dairy)
  3    61.4    C      3    משקה סויה ללא סוכר     (Unsweetened soy)
  4    58.5    C      3    משקה שקדים עשיר חלבון  (Protein almond)
  5    49.4    D      4    חלב שוקולד ממותק       (Chocolate dairy)
  6    45.9    D      3    משקה שקדים ללא סוכר   [SE] (Ultra-low-cal almond)
  7    44.6    D      3    משקה שיבולת שועל ברסיטה (Barista oat)
  8    44.3    D      4    משקה שיבולת שועל ללא סוכר (No-sugar-added oat)
```

[SE] = Structural Emptiness gate triggered

---

## Grade Distribution

```
Grade A (≥85)  ▏  0 products   
Grade B (70–84) ██▏  2 products   Whole dairy milk, High-protein dairy
Grade C (55–69) ██▏  2 products   Unsweetened soy, Protein almond
Grade D (40–54) ████▏  4 products   Chocolate dairy, Ultra-low-cal almond, Barista oat, No-sugar-added oat
Grade E (<40)  ▏  0 products   
```

---

## Dimension Waterfall: Whole Dairy Milk (75, B)

```
Dimension              Weight   Score   Contribution
─────────────────────────────────────────────────────
processing_quality     0.15  ×   95  =  +14.25
nutrient_density       0.15  ×  10.4 =  + 1.56   ← WEAKEST (fiber=0)
calorie_density        0.15  ×   90  =  +13.50
glycemic_quality       0.12  ×   78  =  + 9.36
protein_quality        0.10  ×   16  =  + 1.60
additive_quality       0.10  ×  100  =  +10.00
satiety_support        0.06  ×   60  =  + 3.60
fat_quality            0.08  ×  77.7 =  + 6.22
regulatory_quality     0.05  ×   95  =  + 4.75
whole_food_integrity   0.04  ×  100  =  + 4.00
                                      ────────
Weighted sum                          = 68.84
Floor applied (nova1_single_ingredient → 75)
FINAL SCORE                           = 75.0  [B]
```

---

## Dimension Waterfall: Ultra-Low-Cal Almond Milk (45.9, D)

```
Dimension              Weight   Score   Contribution
─────────────────────────────────────────────────────
processing_quality     0.15  ×   55  =  + 8.25   NOVA 3 penalty
nutrient_density       0.15  ×   2.7 =  + 0.41   ← NEAR ZERO (protein=0.4g)
calorie_density        0.15  ×  50** =  + 7.50   SE gate: would be 85 without gate
glycemic_quality       0.12  ×  90.5 =  +10.86   ← HIGHEST (no sugar!)
protein_quality        0.10  ×   2.0 =  + 0.20   ← NEAR ZERO
additive_quality       0.10  ×   64  =  + 6.40
satiety_support        0.06  ×  25.6 =  + 1.54
fat_quality            0.08  ×  50** =  + 4.00   SE gate: would be ~97.5 without gate
regulatory_quality     0.05  ×   95  =  + 4.75   ← HIGHEST (no red labels!)
whole_food_integrity   0.04  ×   50  =  + 2.00
                                      ────────
Weighted sum                          = 45.91
Binding cap (NOVA_PROXY_3_PROCESSED=75): not binding
FINAL SCORE                           = 45.9  [D]

** SE gate active — these values are capped at 50
```

**Without SE gate:** calorie_density=85, fat_quality=97.5 → score would be ~55 (C)

---

## Comparison A: Dairy vs Hollow Almond

```
                    Whole Dairy    Ultra-Low Almond
                    (75, B)        (45.9, D)
Score:              75.0           45.9
                    ████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░
                    75.0                                        45.9

processing_quality: 95             55
nutrient_density:   10.4           2.7
calorie_density:    90.0           50.0  [SE CAP]
protein_quality:    16.0           2.0
additive_quality:   100            64
fat_quality:        77.7           50.0  [SE CAP]
whole_food_integrity: 100          50

Gap: 29.1 points  B vs D  ✓ CORRECT DIRECTION
```

---

## Comparison B: Intact Dairy Protein vs Isolate-Enriched Almond

```
                    High-Protein Dairy    Protein Almond (Isolate)
                    (71.2, B)             (58.5, C)
Score:              71.2                  58.5
                    ████████████████████████████████░░░░░░░░░░░░░░░
                    71.2                          58.5

Key dimension differences:
  protein_quality:  30.0           14.9  (whole_food sf=1.0 vs mixed sf=0.85)
  processing_qual:  80             55    (NOVA 2 vs NOVA 3)
  additive_quality: 100            49    (no additives vs thickener+sweetener)
  satiety_support:  100            100   (both capped — liquid form issue)

Gap: 12.7 points  B vs C
Source penalty contribution to gap: ~0.3 pts on final score (protein_quality × weight)
Additive/processing contribution: ~12.4 pts
```

---

## Comparison C: Intact Soy vs Engineered Barista Oat

```
                    Unsweetened Soy    Barista Oat
                    (61.4, C)          (44.6, D)
Score:              61.4               44.6
                    ███████████████████████████░░░░░░░░░░░░░░░░░░░░░
                    61.4                   44.6

Key differences:
  protein_quality:  16.5           5.5   (3.3g intact soy vs 1.1g oat)
  additive_quality: 82             46    (1 cat vs 3 cats — E412 triggers stabilizer)
  satiety_support:  99.2           38.9  (protein-driven satiety gap)
  calorie_density:  70             50    (33 kcal vs 70 kcal at table boundary)
  SEED_OIL penalty: none           -3 pts (שמן קנולה)
  Binding cap:      75             65    (ADDITIVE_MARKERS_3_PLUS)

Gap: 16.8 points  C vs D  ✓ CORRECT DIRECTION
```

---

## Comparison D: Barista Oat vs No-Sugar-Added Oat (Sweetener)

```
                    Barista Oat        No-Sugar-Added Oat (Stevia)
                    (44.6, D)          (44.3, D)
Score:              44.6               44.3
                    ████████████████████████░░
                    44.6               44.3

Structural differences:
  NOVA:             3                  4  (flavor eng + sweetener → NOVA 4)
  processing_qual:  55                 25  (NOVA penalty: −30 pts dimension)
  additive_quality: 46                 31  (sweetener penalty: −15 pts)
  fat_quality:      86.6               95.8 (seed oil vs no seed oil)
  Binding cap:      65 (ADD_3+)        60 (NOVA_4)

Score gap: 0.3 points — EFFECTIVELY INDISTINGUISHABLE
✗ ARCHITECTURAL FAILURE: Cannot distinguish sweetener substitution from plain product
```

---

## Category × NOVA Map

```
             NOVA 1    NOVA 2    NOVA 3           NOVA 4
             ──────    ──────    ──────           ──────
dairy_prot   75 (B)    71.2 (B)  —                49.4 (D)
             W.Dairy   Hi-Prot                    Choc Milk

beverage     —         —         61.4 (C)  45.9   44.3 (D)
                                 U.Soy     Almond  NSA Oat
                                 58.5 (C)  44.6
                                 P.Almond  B.Oat
```

Observation: All NOVA 4 products land in the D range regardless of base food quality (chocolate dairy and no-sugar-added oat both score D). The NOVA 4 cap (60) is the dominant driver for all NOVA 4 products.

---

## Structural Emptiness Gate — Condition Matrix

| Product | kcal<20? | prot<3? | fiber<1.5? | fat<2? | eng(sw/add≥2)? | SE=True? |
|---------|----------|---------|------------|--------|----------------|---------|
| Ultra-low-cal almond | ✓ 13 | ✓ 0.4 | ✓ 0.4 | ✓ 1.1 | ✓ (add=2) | **YES** |
| Protein almond | ✗ 35 | — | — | — | — | No |
| Unsweetened soy | ✗ 33 | — | — | — | — | No |
| Barista oat | ✗ 70 | — | — | — | — | No |
| No-sugar-added oat | ✗ 30 | — | — | — | — | No |

Only product 3 satisfies all 5 SE conditions. The kcal threshold (20 kcal/100ml for beverages) is the primary gate.

---

## Key Risks Identified

```
RISK 1 (HIGH):   Pea isolate + water = C grade in ~3 products' territory
                 Gap between isolate-enriched and intact whole-food plant milk: 2.9 pts

RISK 2 (HIGH):   Dairy matrix advantage requires a policy floor (75), not structural score
                 Natural dairy milk score without floor: 68.8 (B only via floor)

RISK 3 (SIG):    Liquid satiety logic uncorrected — protein in beverage = 100 satiety
                 A 13-kcal almond milk with protein would score satiety=100

RISK 4 (MOD):    Sweetener taxonomy: 0.3-point gap between no-sugar-added and plain oat
                 Cannot be used to distinguish marketing claim from nutritional reality

RISK 5 (MOD):    Oat beverages unstable in category classifier (beverage vs cereal ambiguity)
                 Would shift score 10-15 pts if classified as cereal instead of beverage
```
