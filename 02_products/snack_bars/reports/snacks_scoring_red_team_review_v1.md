# Snacks Scoring Red Team Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — External Challenge Mode  
**Scope:** 18 displayed products, /hashvaot/snacks

---

## Opening Finding

Before any product-level analysis, one structural fact invalidates confidence across the entire category:

**All 18 snacks products have null nutritional data and null ingredient strings.**

Every score is computed from structural proxies only:
- Processing classification (NOVA-equivalent)
- Ingredient count
- Structural base classification
- Sweetener pattern category
- Additive load bracket

No protein gram, no sugar gram, no fiber gram, no calorie count, no actual ingredient list is used in any snack score. This is a category-wide confidence problem that must be disclosed upfront.

---

## Part 1: Product-by-Product CE Assessment

| ID | Product | Score | Grade | CE Assessment | Confidence | Critical Notes |
|---|---|---|---|---|---|---|
| snk-001 | חטיף תמרים במילוי חמאת שקדים | 70 | B | Plausible as best-in-class structurally. Possibly inflated. | LOW | Score based on "4 ingredients." No nutrition. Dates are 60–70g sugar per 100g. Date Sugar Halo active. |
| snk-004 | מרבה סלים דליס שוקולד מריר | 58 | C | Unverifiable. Partial confidence. | VERY LOW | No ingredient string. "Multi-grain base" is an inference. 58/C with zero nutritional data is undefendable under challenge. |
| snk-002 | חטיף תמרים בציפוי שוקולד 100% קקאו | 56 | C | Plausible. 14-point gap from snk-001 questionable. | LOW | Penalty for adding cocoa coating to an almost identical base. Is 14 points proportionate? No data to verify. |
| snk-015 | חטיף תמרים במילוי חמאת בוטנים | 55 | C | Plausible. 15-point gap from snk-001 questionable. | LOW | Peanut butter vs almond butter = 15 points? Compositionally nearly identical. Gap feels like noise not signal. |
| snk-003 | קראנצ'י שיבולת שועל עם דבש | 53 | C | Reasonable. Oats first, syrup second is defensible. | MEDIUM | Nature Valley Crunchy is well-known. "Oats first" claim needs verification — ingredients.html exists in BSIP0 but was not parsed. |
| snk-016 | מרבה סלים טופינג אגוזי לוז | 51 | C | Unverifiable. Partial confidence. | VERY LOW | 7-point gap below snk-004 (same brand) has no stated mechanism. |
| snk-009 | נייצ'ר וואלי פרוטאין בוטנים ושוקולד | 47 | D | Reasonable penalty for NOVA4 processing. | LOW-MEDIUM | 15-ingredient engineered bar. But protein content unknown. If this delivers 15g protein per bar, the consumer deserves to know. |
| snk-005 | חטיפי דגנים פיטנס קלאסי | 46 | D | Fair: flour + syrup base. | MEDIUM | One of the better-justified scores — "flour before oats" is a real finding. But without ingredient verification, still an inference. |
| snk-018 | קראנצ'י שיבולת שועל עם חתיכות שוקולד | 46 | D | 7-point gap from snk-003 for adding chocolate — plausible but unverified. | LOW-MEDIUM | Same brand/format as snk-003. Gap is reasonable directionally but 7 points feels arbitrary without sugar data. |
| snk-010 | נייצ'ר וואלי פרוטאין בוטנים קרמל מלוח | 45 | D | 2-point gap from snk-009. Near-noise. | LOW | Same product line, different flavor. 45 vs 47 is within statistical noise. These two cannot be meaningfully ranked against each other. |
| snk-011 | פרי מארז תמרים ואגוזי לוז | 43 | D | Reasonable: natural-gap cluster. | LOW | Partial confidence. "Added sugar in the list" is the key claim — unverified without parsed ingredient string. |
| snk-012 | פרי מארז תמרים ושברי קקאו | 42 | D | 1-point gap from snk-011. Noise. | LOW | 43 vs 42 between near-identical products in the same brand is false precision. Indistinguishable. |
| snk-019 | חטיפי פיטנס שיבולת שועל דבש | 41 | D | Reasonable directionally. | LOW-MEDIUM | 5 points below snk-005 (same brand). Mechanism is "HFCS + honey = double sweetener." Plausible but unverified. |
| snk-017 | נייצ'ר וואלי צ'ואי שוקולד מריר | 39 | D | 8 points below NV Protein. Directionally plausible. | LOW | "Chewy line is lower quality than Protein line" is the claim. Reasonable. But 8 points for the same brand/category feels large without nutrition data. |
| snk-020 | מרבה סלים דליס קריספי אוכמניות | 32 | E | 19-point gap below snk-016 (same brand). Hard to defend. | VERY LOW | Partial confidence. The 19-point spread within Slim brand (51→32) requires explanation that isn't present. |
| snk-007 | חטיפי דגנים פיטנס שוקולד מריר | 29 | E | Partial confidence. Directionally reasonable. | VERY LOW | "Engineered base + multiple sweeteners" — but these are inferences without parsed ingredients. |
| snk-006 | פיטנס בר גרנולה שוקולד מריר | 17 | E | 17 is EXTREMELY low. Lower than milky (27). Is a granola bar worse than milky? | VERY LOW | "10+ additives" and "engineered base" claim drives the score. Even if true, 17 is at the bottom of the entire Bari universe. This needs verification. |
| snk-013 | שחור ולבן קורני שוקולד | 13 | E | Likely correct category placement, but: this is a confectionery product, not a snack bar. | MEDIUM | The 13 score is consistent with a candy-bar comparison. But Corny Schoko is being judged as a snack bar when it is effectively a chocolate sandwich wafer. Category mismatch may be penalizing it unjustly within the snack comparison. |

---

## Summary Assessment

**Justified scores (structural logic holds):** snk-001, snk-003, snk-005, snk-013  
**Plausible but unverifiable:** snk-002, snk-009, snk-011, snk-017, snk-018, snk-019  
**Weak confidence, partial data:** snk-004, snk-007, snk-010, snk-015, snk-016, snk-020  
**Noise-level precision (indistinguishable):** snk-010/snk-009, snk-011/snk-012  
**Potentially incorrect:** snk-006 (17 is a very aggressive floor without verified data), snk-020 (19-point gap from sibling unexplained)

**Overriding problem:** Zero nutritional data. Every score is an inference from structural metadata. This is acceptable for a relative ranking within the category but fails as an absolute grade system. The snacks corpus is structurally graded, not nutritionally graded.

---

## Key Structural Problems

### 1. All-null nutrition layer
Snacks is the only active category with 18/18 products having null energyKcal, null protein, null sugar, null fiber, null ingredients. Maadanim has 89/90 products with full data. This means snack scores are not comparable in confidence to any other category score.

### 2. False precision in the D-band
Eight products cluster between 39–47 (8-point range). Within this band:
- snk-009 (47) vs snk-010 (45): 2-point gap, same product line
- snk-011 (43) vs snk-012 (42): 1-point gap, same brand
- snk-005 (46) vs snk-018 (46): tied

Micro-gaps below 5 points between near-identical products are scoring artifacts, not real distinctions.

### 3. Category-inappropriate product included
snk-013 (Corny Schoko, 13/E) is a chocolate wafer sandwich, not a snack bar. Its inclusion in the snack comparison introduces a category mismatch that anchors the bottom of the scale artificially.

### 4. The 70 ceiling is shared with maadanim
Both categories top out at exactly 70/B. This is not a coincidence — it reflects a shared cap architecture. The ceiling should vary by category.

### 5. BSIP0 data exists but was not used
The `observations_bsip0/yohananof/` directory contains parsed ingredients.html and nutrition.html files for most products. These were not ingested during BSIP2 scoring. The data exists; it was skipped.
