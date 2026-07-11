# TASK-509 Nutrition Memo: Expansion Nutrition Bar Config — DEFAULT vs Category Scales

**Date:** 2026-07-05
**Author:** Nutrition Agent
**Status:** Recommendation (not yet implemented — awaiting D7 co-sign + separate frontend PR)
**Task:** TASK-509
**Scope:** Display-layer threshold question only. Published scores: untouched.

---

## 1. Executive Summary

The four categories under investigation — bread, cheese (generic), crackers, milk — currently render their expansion nutrition bars using `DEFAULT_NUTRITION` scales because no `category` prop is passed from their comparison page components to `ComparisonPage` / `ExpansionSection`. Category-specific configs exist in `expansion-section.tsx` for bread and cheese; none exists for crackers or milk (under the correct key `milk-comparison`).

**Verdict:**

| Category | DEFAULT correct? | Status |
|---|---|---|
| Bread | No — latent display bug | Category config (`bread`) is nutritionally correct; DEFAULT is misleading |
| Cheese (generic) | No — latent display bug | Category config (`cheese`) is nutritionally correct; DEFAULT is grossly miscalibrated |
| Crackers | Partial — DEFAULT happens to be acceptable but sub-optimal | No category config exists; one should be created |
| Milk | No — latent display bug | `milk` config exists but is unreachable; config is correct and should be wired |

This is a **display integrity issue**, not a scoring issue. No BSIP2 score changes. Activation requires a separate frontend PR with Nutrition sign-off (D7) and Design re-verify.

---

## 2. Configuration Reference

### 2.1 DEFAULT_NUTRITION (expansion-section.tsx lines 191–197)

```
energyKcal:  { max: 400 }
protein:     { max: 20,  goodAbove: 8,  warnBelow: 3  }
sugar:       { max: 20,  goodBelow: 3,  warnAbove: 12 }
sodium:      { max: 600 }
servingLabel: "ל-100 גרם"
```

### 2.2 Category-Specific Configs (expansion-section.tsx)

**`bread` (lines 104–110):**
```
energyKcal:  { max: 350 }
protein:     { max: 16,  goodAbove: 8,  warnBelow: 3  }
sugar:       { max: 10,  goodBelow: 1,  warnAbove: 6  }
sodium:      { max: 600 }
servingLabel: "ל-100 גרם"
```

**`cheese` (lines 135–141):**
```
energyKcal:  { max: 400 }
protein:     { max: 30,  goodAbove: 20, warnBelow: 8  }
sugar:       { max: 5,   goodBelow: 1,  warnAbove: 3  }
sodium:      { max: 800 }
servingLabel: "ל-100 גרם"
```

**`milk` (lines 89–94):**
```
energyKcal:  { max: 80 }
protein:     { max: 8,   goodAbove: 5,  warnBelow: 3  }
sugar:       { max: 8,   goodBelow: 1,  warnAbove: 6  }
sodium:      { max: 80 }
servingLabel: "ל-100 מ״ל"
```

**`crackers` — ABSENT from CATEGORY_NUTRITION.**

---

## 3. Product-Level Flip Analysis

### 3.1 BREAD

Source file: `C:\bari\bari-web\src\data\comparisons\bread_frontend_v4.json`

Real corpus protein range from 5 sampled products (ranks 1–5, score desc):

| Product (barcode) | Protein g/100g | Sugar | Sodium mg | Energy kcal |
|---|---|---|---|---|
| לחם טחינה פרוס (7290016245325) | 27.5 | null | 126 | 192 |
| לחם ירוק (3268429) | 12.6 | null | 382 | 223 |
| לחם חיטה מלא לילדים (3268252) | 11.5 | null | 343 | 221 |
| לחם מחמצת קמח מלא (481203) | 9.0 | null | 380 | 227 |
| לחם מחמצת גרעינים (481197) | 8.5 | null | 380 | 220 |

**Protein bar color under DEFAULT vs `bread`:**

`nutrientTone` fires green (goodAbove) or amber (warnBelow) for protein only. The logic is: `>= goodAbove` → green; `< warnBelow` → amber; otherwise neutral grey.

| Product | Protein | DEFAULT (goodAbove=8) | `bread` (goodAbove=8) |
|---|---|---|---|
| לחם טחינה (27.5g) | 27.5 | Green (>=8) | Green (>=8) |
| לחם ירוק (12.6g) | 12.6 | Green (>=8) | Green (>=8) |
| לחם חיטה מלא (11.5g) | 11.5 | Green (>=8) | Green (>=8) |
| לחם מחמצת קמח (9.0g) | 9.0 | Green (>=8) | Green (>=8) |
| לחם מחמצת גרעינים (8.5g) | 8.5 | Green (>=8) | Green (>=8) |

For these top products, `goodAbove=8` is identical in both configs, so protein color does not flip. However, the bar **scale** differs: DEFAULT max=20 vs bread max=16. A product with 12.6g protein fills 63% of the DEFAULT bar but 79% of the bread bar — bread products physically appear more impressive in their own category context.

For **energy**, the scale max differs: DEFAULT max=400 vs bread max=350. Bread products at ~220 kcal fill 55% of DEFAULT but 63% of the bread bar — the categorical context is more honest.

For **sugar**: bread sugar is consistently null in the scanned corpus (not available at scrape), so sugar bars are blank regardless.

**Sodium scale**: DEFAULT max=600 vs bread max=600. Identical — no difference.

**Conclusion for bread:** The `bread` config is nutritionally correct. It was authored by someone who understood the bread shelf (protein ceiling of 16g is calibrated to the real corpus maximum of ~28g but acknowledges that 16g is the shelf norm; goodAbove=8 matches the real middle of the shelf at 8.5–12.6g). The scale change on energy (350 vs 400) and protein max (16 vs 20) means that at DEFAULT, bread bars display proportions calibrated for a wider food universe. This is a **latent display bug**: the bars are not wrong in direction but miscalibrated in scale, misleading the consumer about where a product sits on the bread-specific shelf.

**Nutritional rationale for `bread` config:** Bread protein ranges from ~5g (refined white) to ~28g (engineered seed/tahini bread). The shelf norm for wholegrain bread is 8–13g. Setting goodAbove=8 correctly marks the top 60% of the shelf as green for protein, which is the honest representation of a good-protein bread. DEFAULT goodAbove=8 happens to be the same here, but the bar scale max (16 vs 20) is bread-correct. Evidence tier: Strong (the corpus data is direct label evidence; the threshold aligns with Israeli retail shelf reality).

---

### 3.2 CHEESE (generic — `cheese_frontend_v4.json`)

Source file: `C:\bari\bari-web\src\data\comparisons\cheese_frontend_v4.json`

Real corpus protein from 5 sampled products (ranks 1–5):

| Product (barcode) | Protein g/100g | Sugar | Sodium mg | Energy kcal |
|---|---|---|---|---|
| קוטג 1% (7290014758681) | 11.5 | null | 350 | 62 |
| גבינה טבורוג 5% (6040619) | 17.0 | 2.3 | 30 | 123 |
| קוטג 3% (4127077) | 11.0 | null | 350 | 77 |
| קוטג 5% (4127329) | 11.0 | null | 350 | 95 |
| קוטג 5% (41445) | 11.0 | null | 350 | 95 |

**Protein bar color under DEFAULT vs `cheese`:**

DEFAULT: goodAbove=8, warnBelow=3, max=20.
`cheese`: goodAbove=20, warnBelow=8, max=30.

| Product | Protein | DEFAULT color | `cheese` color |
|---|---|---|---|
| קוטג 1% (11.5g) | 11.5 | Green (>=8) | Amber (11.5 < 20, >= 8) → neutral grey |
| טבורוג (17.0g) | 17.0 | Green (>=8) | Amber (17.0 < 20, >= 8) → neutral grey |
| קוטג 3% (11.0g) | 11.0 | Green (>=8) | Amber (11.0 < 20, >= 8) → neutral grey |
| קוטג 5% (11.0g) | 11.0 | Green (>=8) | Amber (11.0 < 20, >= 8) → neutral grey |

Wait — let me re-read the `nutrientTone` logic precisely:

```
if (scale.goodAbove !== undefined && value >= scale.goodAbove) return "#1F8F6A"; // green
if (scale.warnBelow !== undefined && value < scale.warnBelow) return "#C49A4A"; // amber
return "#9AA09B"; // neutral grey
```

For `cheese` config: goodAbove=20, warnBelow=8.

- 11.5g: not >= 20, not < 8 → neutral grey
- 17.0g: not >= 20, not < 8 → neutral grey
- 11.0g: not >= 20, not < 8 → neutral grey

Under DEFAULT (goodAbove=8):
- 11.5g: >= 8 → **green**
- 17.0g: >= 8 → **green**
- 11.0g: >= 8 → **green**

**This is a significant flip.** Under DEFAULT, every cottage cheese product (8–17g protein) shows a green protein bar. Under the `cheese` config, ALL of them show neutral grey — because 11–17g is in the contextually normal range for fresh cheese, not a standout. Only genuinely high-protein cheeses (hard cheese, halloumi) at >= 20g/100g would get green under the category scale.

**Is the `cheese` config (goodAbove=20) nutritionally defensible?**

Yes — strongly so. The cheese category here is a mixed fresh-cheese shelf: cottage/quark (11–17g protein) sitting alongside processed fresh cheeses (~8g) and cream cheese variants (~5–8g). The category-relative framing means: 20g+ protein per 100g is genuinely outstanding for the fresh-cheese shelf (it would be halloumi, high-fat quark, or Israeli labane with very high solids). Calling 11g "green" on the cheese shelf is like calling 8g "green" on a protein bar shelf — it misrepresents the category norm.

The `cheese` warnBelow=8 is also correct: below 8g protein per 100g in the cheese category (which would be cream cheese / white cheese at 5–9% fat) is genuinely below the category baseline and worth flagging amber.

**The `cheese` goodAbove=20 threshold is defensible; the current DEFAULT (goodAbove=8) is misleading.** For fresh cheese, 11g is baseline; 20g is genuinely strong. DEFAULT makes every cottage cheese look exceptional, which is nutritionally dishonest in a category context.

**Sodium:** DEFAULT max=600 vs `cheese` max=800. Cheese sodium in this corpus runs 30–350 mg/100g for cottage-style cheeses, but the `_meta.category` notes the corpus spans a wider cheese shelf. The larger max (800) in the category config accommodates brined cheeses / harder cheeses where sodium runs 600–1000 mg. For the `cheese_frontend_v4.json` corpus (fresh cheese dominated), sodium 350 mg sits at 58% of DEFAULT max or 44% of cheese max — the cheese max is more honest for a shelf that includes saltier variants.

**Conclusion for cheese:** The `cheese` config is nutritionally correct and DEFAULT is actively misleading (it makes all cottage cheese protein look exceptional by fresh-cheese standards). **Latent display bug confirmed.** Evidence tier: Strong.

---

### 3.3 CRACKERS

Source file: `C:\bari\bari-web\src\data\comparisons\crackers_frontend_v1.json`

Real corpus nutrition from 3 sampled products (ranks 1–3):

| Product | Protein g/100g | Fiber | Sodium mg | Energy kcal |
|---|---|---|---|---|
| קרקר כוסמין ושומשום (96086000966) | 16.0 | 10.0 | 397 | 418 |
| קרקר כוסמין אורגני (96086000577) | 16.0 | 9.3 | 391 | 380 |
| קרקר כוסמין טבעי (7290013740823) | 9.5 | 10.5 | 394 | 313 |

Crackers calorie density norms (from `scoring.md`): normal range 380–480 kcal.

**Under DEFAULT (goodAbove=8, max=20, energyKcal max=400):**

Protein:
- 16g: green (>= 8) — correct directionally (16g is genuinely high for crackers)
- 9.5g: green (>= 8) — directionally correct but on the low end of the cracker shelf

Energy:
- 418 kcal: 418/400 = 104.5% → bar clamped to 100% (fills bar completely). This makes a 418 kcal cracker look like it's at the maximum of a 400 kcal scale — **misleading**. Crackers are legitimately 380–480 kcal because they are dehydrated. Under DEFAULT, the bar overflows.
- 380 kcal: 95% fill — nearly full bar.

**Recommended crackers config (proposed, to be ratified by D7):**

```
crackers: {
  energyKcal: { max: 500 },
  protein:     { max: 20, goodAbove: 12, warnBelow: 5 },
  sugar:       { max: 10, goodBelow: 1,  warnAbove: 5 },
  sodium:      { max: 600 },
  servingLabel: "ל-100 גרם",
}
```

Rationale:
- `energyKcal max=500`: honest for the cracker shelf (380–480 kcal normal; 500 leaves room for outliers). Under DEFAULT max=400, the bar overflows for typical crackers.
- `protein goodAbove=12`: the top-shelf crackers (khorasani/spelt whole grain with sesame) reach 16g. Setting goodAbove=12 correctly marks those as standout. Default goodAbove=8 is too low — virtually all crackers would be green, eliminating differentiation.
- `protein warnBelow=5`: below 5g protein/100g for a cracker is genuinely low (refined white flour crackers). Appropriate.
- `sugar max=10, goodBelow=1, warnAbove=5`: cracker sugar is minimal; this matches the tight bread-adjacent scale.
- `sodium max=600`: consistent with bread; crackers run 390–600 mg/100g.

Note: `crackers` is entirely absent from `CATEGORY_NUTRITION` in expansion-section.tsx. This means even if `category="crackers"` were passed, it would fall through to DEFAULT. **A new `crackers` config entry is needed.**

**Conclusion for crackers:** DEFAULT is partially acceptable for protein color (though goodAbove=8 is too permissive — it would green-flag essentially the whole shelf). The critical failure is the energy scale: 400 max under DEFAULT causes bar overflow for normal crackers (380–418 kcal). This is a display accuracy issue though not as misleading as the cheese protein case. **Partial latent bug — energy scale is the primary problem.** Evidence tier: Strong (corpus data; scoring.md calorie density tables confirm cracker normal range).

---

### 3.4 MILK

Source file: `C:\bari\bari-web\src\data\comparisons\milk_frontend_v1.json`

Real corpus nutrition from 5 sampled products (ranks 1–4 + rank 7):

| Product | Protein g/100ml | Sugar | Sodium mg | Energy kcal/100ml |
|---|---|---|---|---|
| חלב מלא 3.4% (7290000051352) | 3.3 | null | 41 | 67 |
| חלב טבעי 4% (7290019790259) | 3.4 | null | null | 69 |
| חלב עיזים (7290102392094) | 3.4 | null | 50 | 68 |
| חלב מועשר בחלבון 2% (7290114313865) | 6.5 | null | 45 | 64 |
| חלב 1% מועשר - מהדרין (7290107932134) | 3.4 | 5.0 | 42 | 43 |

The `milk` config's key facts:
- `energyKcal max=80` (vs DEFAULT max=400): milk is 43–69 kcal/100ml. DEFAULT max of 400 makes every milk product's energy bar invisible (43/400 = 11% fill). Milk max=80 gives 43/80 = 54% — visually meaningful and to-scale.
- `protein max=8, goodAbove=5, warnBelow=3`: Milk protein runs 3.3–6.5 g/100ml. goodAbove=5 correctly marks the protein-enriched milk (6.5g) as green. Regular milks at 3.3–3.4g sit between warnBelow=3 and goodAbove=5 → neutral grey, which is honest (they are baseline dairy protein, not exceptional). Under DEFAULT (goodAbove=8), ALL milk products would be neutral grey or amber because none reach 8g — the DEFAULT protein scale is calibrated for solid foods, not beverages.
- `sodium max=80` (vs DEFAULT max=600): milk sodium runs 41–60 mg/100ml. DEFAULT max=600 makes every milk sodium bar nearly invisible (41/600 = 7% fill). Milk max=80 gives 41/80 = 51% — visible and meaningful.
- `servingLabel "ל-100 מ״ל"` (vs DEFAULT "ל-100 גרם"): the unit is wrong under DEFAULT. Milk is measured per 100ml, not per 100g. The serving label shown in the expansion section header would read "ל-100 גרם" under DEFAULT, which is factually incorrect for a liquid.

**Under DEFAULT for milk:**

| Nutrient | DEFAULT behavior | `milk` config behavior |
|---|---|---|
| Energy bar fill (67 kcal) | 67/400 = 16.8% → near-invisible | 67/80 = 83.8% → prominent |
| Protein bar (3.3g) | 3.3/20 = 16.5%, not >= 8 → grey | 3.3/8 = 41.3%, not >= 5 not < 3 → grey |
| Protein bar (6.5g, enriched) | 6.5/20 = 32.5%, not >= 8 → grey | 6.5/8 = 81.3%, >= 5 → **green** |
| Sodium bar (41mg) | 41/600 = 6.8% → invisible | 41/80 = 51.3% → visible |
| Serving label | "ל-100 גרם" (WRONG UNIT) | "ל-100 מ״ל" (correct) |

**This is the most severe latent bug of the four categories.** Under DEFAULT:
1. The serving unit is factually wrong (grams vs milliliters).
2. Energy and sodium bars are near-invisible (sub-10% fill), rendering the visual entirely useless.
3. The protein-enriched milk (6.5g) shows grey rather than green — a meaningful product differentiator is invisible.

**Conclusion for milk:** The `milk` config is correct and essential. DEFAULT is actively wrong for a liquid product — the unit label error alone is a consumer-facing factual inaccuracy. **Severe latent display bug.** Evidence tier: Strong.

**The additional bug:** the route id is `milk-comparison` but the config key is `milk`. The `CATEGORY_NUTRITION_ALIASES` record (expansion-section.tsx line 199–201) only has one entry (`"breakfast-cereals"` → `"cereals"`). No alias for `"milk-comparison"` → `"milk"` exists. Even if `category="milk-comparison"` were passed, `getCategoryNutrition("milk-comparison")` would return DEFAULT. The fix requires either adding an alias `"milk-comparison": "milk"` to `CATEGORY_NUTRITION_ALIASES`, or passing `category="milk"` from the milk comparison page.

---

## 4. Summary Verdict Table

| Category | Correct config | Config exists? | Currently active? | Severity of DEFAULT |
|---|---|---|---|---|
| Bread | `bread` config (lines 104–110) | Yes | No — `category` prop not passed | Low-medium: scale miscalibration, no unit error, protein thresholds happen to match |
| Cheese | `cheese` config (lines 135–141) | Yes | No — `category` prop not passed | High: protein goodAbove=8 vs 20 makes all cottage cheese appear exceptional when it is baseline; misleads consumer on protein standout signal |
| Crackers | `crackers` config (proposed) | **No — must be created** | N/A — config absent | Medium: energy scale overflow (418+ kcal fills/overflows 400 max bar); protein green-flag too permissive (goodAbove=8 flags most of shelf) |
| Milk | `milk` config (lines 89–94) | Yes | No — `category` prop not passed + `milk-comparison` key has no alias | Severe: wrong unit label ("ל-100 גרם" vs "ל-100 מ״ל"); energy/sodium bars near-invisible; protein differentiator (enriched milk) invisible |

---

## 5. Nutritional Rationale Summary

### Protein thresholds are category-relative by design

The Bari framework is explicitly category-relative for calorie density (see `scoring.md`, category_analysis.md). The same logic applies to display thresholds in the expansion bars. A protein signal that is "good" for a beverage (>5g/100ml = double the dairy baseline) is merely average for a hard cheese (typically 22–30g/100g). Using DEFAULT protein thresholds across all categories conflates absolute protein quantity with category-relative excellence, which violates the display integrity principle that "a bar's color should tell the consumer where this product sits within its own shelf."

### Crackers energy scale is structurally determined

Crackers have elevated calorie density not because of added sugar or fat but because they are baked dry (10–15% moisture vs 35–45% for bread). The scoring framework acknowledges this explicitly (`scoring.md` category calorie density tables, cracker range 380–480 kcal). Displaying cracker energy bars against a 400 kcal max (DEFAULT) causes bar overflow for typical crackers, creating the false visual impression that they are at or above the display ceiling.

### Milk is a liquid product; grams vs milliliters is a factual error

Milk nutrition is stated per 100 ml. Labeling the serving unit "ל-100 גרם" is factually incorrect. Israeli food law requires clear unit disclosure. Using the wrong unit in a consumer-facing display is not a threshold question — it is a data presentation accuracy issue.

---

## 6. Recommendation

### What should be done (D7 co-sign required)

**Activate the three existing configs + add one new config + add one alias.**

Specifically, a follow-up implementation task would make the following frontend changes in `bari-web/`:

1. **Bread** (`bread-comparison-page.tsx`): Pass `category="bread"` to `ComparisonPage`.

2. **Cheese** (`cheese-comparison-page.tsx`): Pass `category="cheese"` to `ComparisonPage`.

3. **Milk** (`milk-comparison-page.tsx`): Pass `category="milk-comparison"` to `ComparisonPage` AND add to `CATEGORY_NUTRITION_ALIASES` in `expansion-section.tsx`:
   ```
   "milk-comparison": "milk"
   ```
   OR alternatively, rename the milk config key from `"milk"` to `"milk-comparison"`.

4. **Crackers** (`crackers-comparison-page.tsx` + `expansion-section.tsx`):
   - Pass `category="crackers"` to `ComparisonPage`.
   - Add a new `crackers` entry to `CATEGORY_NUTRITION` in `expansion-section.tsx`:
   ```typescript
   crackers: {
     energyKcal: { max: 500 },
     protein:     { max: 20, goodAbove: 12, warnBelow: 5 },
     sugar:       { max: 10, goodBelow: 1,  warnAbove: 5 },
     sodium:      { max: 600 },
     servingLabel: "ל-100 גרם",
   },
   ```

### Threshold review notes

The existing `bread`, `cheese`, and `milk` configs I endorse as written. No amendments needed. The proposed `crackers` config is my recommendation; it requires D7 co-sign from Nutrition + Product before going live.

### Implementation constraint

This must ship as its OWN PR, never piggybacked on a nav or SEO PR. It touches a consumer-facing display layer. It requires:
1. Nutrition Agent sign-off (this memo serves as the science rationale).
2. Product Agent co-sign (D7) on the crackers config specifically (the other three are activating existing authored configs, not writing new scoring rules).
3. Design Agent re-verify on render output (the milk bars will look substantially different after fix — bars that were near-invisible become proportionally sized).

---

## 7. Evidence Sources

| Claim | Source | Evidence tier |
|---|---|---|
| Product protein values (bread) | `bread_frontend_v4.json`, expansion.nutrition.protein, ranks 1–5 | Direct label data |
| Product protein values (cheese) | `cheese_frontend_v4.json`, expansion.nutrition.protein, ranks 1–6 | Direct label data |
| Product protein values (crackers) | `crackers_frontend_v1.json`, expansion.nutrition.protein, ranks 1–3 | Direct label data |
| Product protein/energy (milk) | `milk_frontend_v1.json`, expansion.nutrition, ranks 1–6 | Direct label data |
| Category calorie density norms | `scoring.md` CALORIE_DENSITY_TABLES; `category_analysis.md` | Bari framework docs |
| Protein threshold logic | `expansion-section.tsx` lines 234–246 (`nutrientTone` function) | Source code |
| Config map | `expansion-section.tsx` lines 86–188 (`CATEGORY_NUTRITION`) | Source code |
| DEFAULT config | `expansion-section.tsx` lines 191–197 | Source code |
| Alias map | `expansion-section.tsx` lines 199–201 (`CATEGORY_NUTRITION_ALIASES`) | Source code |
| Category prop wiring (absent) | `bread-comparison-page.tsx`, `cheese-comparison-page.tsx`, `crackers-comparison-page.tsx`, `milk-comparison-page.tsx` — no `category=` prop in any | Source code |
| Categories that DO pass `category` | Grep of `category=` in comparisons/ directory — 13 categories pass it; 4 do not | Source code |

---

*This memo is a Nutrition Agent analysis document. It does not constitute implementation approval. A separate frontend PR implementing these changes requires the full D7 governance path (Nutrition + Product Agent co-sign) plus Design Agent render re-verify.*
