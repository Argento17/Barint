# לחם — Bread Calibration Patch v1

**Applied:** 2026-05-28 17:39 UTC
**Input:** `lechem_frontend_v1.json` (81 products, BSIP2 bread_retail_003)
**Output:** `lechem_frontend_v2.json`
**Approach:** Synthesis-level corrections only — no BSIP2 rerun

---

## Calibration Rationale

The BSIP2 bread scoring operated on nutrition macros only — the scorer had no access to parsed
ingredient data (`has_ingredients: true` but no ingredient list in BSIP2 files). As a result:

1. Fiber from added inulin/isolated fiber was treated identically to whole-grain fiber
2. White flour as primary base received no structural penalty
3. Fermentation credit was awarded based on name/label detection, not base-flour composition
4. Additive load (E-numbers, preservatives) had no effect on score

These four failure modes produced a 74% B distribution (60/81 products) where industrial
enriched breads occupied the same grade as genuinely clean whole-grain products.

**Editorial philosophy:** corrections are restrained — adjusted to where an honest
ingredient-aware rater would place the product, not to the minimum defensible score.
Products with genuine whole-grain bases received partial credit even when supplemented.

---

## Grade Distribution — Before / After

| Grade | Before | After | Change |
|-------|--------|-------|--------|
| A | 2 (2%) | 2 (2%) | +0 |
| B | 60 (74%) | 53 (65%) | -7 |
| C | 18 (22%) | 25 (31%) | +7 |
| D | 1 (1%) | 1 (1%) | +0 |

**B: 74% → 65%**
**C: 22% → 31%**

---

## All Corrected Products

| Barcode | Name | Before | After | Delta | Type |
|---------|------|--------|-------|-------|------|
| 2079033 | לחם דגנים לייט | 74/B | 69/B | -5 | fiber_implausible |
| 2079996 | לחם אחיד פרוס קל | 73/B | 66/B | -7 | fiber_laundering |
| 497044 | לחם ברמן אקטיב | 72/B | 68/B | -4 | inulin_augmentation |
| 481180 | לחם מחמצת שאור | 71/B | 64/C | -7 | fermentation_authenticity |
| 497570 | לחם דגנים פלוס | 68/B | 62/C | -6 | fiber_laundering |
| 7290018500316 | לחם כוסמין לבן | 68/B | 64/C | -4 | white_spelt_base |
| 2079477 | לחם אחיד פרוס | 67/B | 64/C | -3 | additive_accumulation |
| 4033736 | לחם עננים בסגנון בריוש | 66/B | 62/C | -4 | white_flour_base |
| 7290017947105 | לחם בסגנון אמריקה | 65/B | 62/C | -3 | white_flour_base |
| 7290018500231 | לחם אנג'ל WEEKEND | 65/B | 62/C | -3 | white_flour_base |

**Grade changes (B→C):** 7 products
**Score-only corrections (remain B):** 3 products

---

## Grade Change Details (B → C)

### לחם מחמצת שאור (BC=481180)\n**71/B → 64/C** (Δ-7)\n\nWhite wheat flour comprises 75% of all flour fractions (40% of total product weight). The sourdough starter itself (מחמצת חיטה לבן 18%) is white-flour based. Fiber=2.5g — the lowest among all B-grade non-cracker products in this corpus. Score 71 places this product level with genuinely whole-grain sourdoughs at 70–74. Insight line states 'הבסיס לבן, המחמצת שלישית ברשימה' — the score was contradicting this. Corrected to 64/C, consistent with white-flour sourdoughs in the C cluster (62–64).\n
### לחם דגנים פלוס (BC=497570)\n**68/B → 62/C** (Δ-6)\n\nReported fiber=12.7g from 35% whole wheat + 10% grain mix. Maximum plausible from grain alone: ~4.5g. Remaining 8g comes from supplemented fiber (grain mix includes oat flakes, rye flakes, barley flakes — concentrated bran sources likely added as fiber booster). Insight line already states 'ה-פלוס הוא תוספת סיבים, לא גרעין שלם' — score 68/B directly contradicts this. Corrected to 62/C.\n
### לחם כוסמין לבן (BC=7290018500316)\n**68/B → 64/C** (Δ-4)\n\nכוסמין לבן = sifted spelt: germ and most bran removed. 88% of flour fraction (61% of product) is sifted spelt. Fiber=3.3g — consistent with white flour, not whole grain. Scored 68 alongside genuinely whole-grain products at 68–72. Insight line: 'גרעין כוסמין מנופה. 3.3 גרם סיבים בלבד, פחות מגרסת הכוסמין המלא'. Corrected to 64/C.\n
### לחם אחיד פרוס (BC=2079477)\n**67/B → 64/C** (Δ-3)\n\nTwo distinct preservatives: קלציום פרופיונט (E282) + פוטסיום סורבט (E202) — unique in corpus. Two emulsifiers (E471, E481). Fiber=3.0g from dark wheat base. Insight line: 'שני חומרים משמרים... לחם אחיד, שיא התוספות'. Score 67/B contradicts 'שיא התוספות'. Corrected to 64/C.\n
### לחם עננים בסגנון בריוש (BC=4033736)\n**66/B → 62/C** (Δ-4)\n\n100% white flour (60% of product weight). Sugar is ingredient #3. Three emulsifiers (E471, E481, E472e) + preservative (E282). Added isolated fiber later in list. Insight line: 'קמח לבן 100%, סוכר שני ברשימה, מתחלבים — הסגנון מסביר את הרכב'. A score of 66/B implies parity with products containing 70–80% whole grain. Corrected to 62/C.\n
### לחם בסגנון אמריקה (BC=7290017947105)\n**65/B → 62/C** (Δ-3)\n\nWhite flour is primary flour. Sugar is ingredient #3. Five E-numbers including three emulsifiers (E471, E472e, E481) + preservative (E282). Composition identical to WEEKEND profile. Insight line: 'קמח לבן ראשון, סוכר שני, מתחלבים שלישי. הסגנון מסביר את הרכב'. Corrected to 62/C. Consistent with WEEKEND correction.\n
### לחם אנג'ל WEEKEND (BC=7290018500231)\n**65/B → 62/C** (Δ-3)\n\nWhite flour is primary flour. Sugar is ingredient #3. Emulsifier (E481) + preservative (E282). Added isolated fiber (ingredient #7). Insight line: 'קמח לבן, סוכר, מתחלבים. אנג'ל לשבת, לא לשבוע'. Score 65/B = same letter as לחם ירוק מקמח מלא (80/B), a 100% whole-wheat clean-label product. Corrected to 62/C.\n

---

## Score-Only Corrections (Remain B)

### לחם דגנים לייט (BC=2079033)\n**74/B → 69/B** (Δ-5)\n\nReported fiber=14.2g. Declared grain fractions: whole wheat 32%, whole rye 11%, dark wheat ~7%, grain mix 8% = ~58% total grain. At 10g fiber/100g whole grain flour, ~58% grain → ~5.8g fiber. The gap to 14.2g (≈8g) requires undisclosed supplemented fiber. Water is ingredient #1, suggesting high hydration that concentrates reported values. Base is genuinely whole grain. Moderate correction to 69 — preserves whole-grain credit while removing implausible fiber premium.\n
### לחם אחיד פרוס קל (BC=2079996)\n**73/B → 66/B** (Δ-7)\n\nסיבים תזונתיים (isolated fiber) is the 3rd ingredient — immediately after dark wheat flour and water. Reported fiber=10.4g; dark wheat flour at ~50% of product produces ≤3g naturally. The remaining 7g is supplement. Whole flour fractions (whole wheat, whole rye) appear 7th–8th. Score 73 assumed all 10.4g fiber is structural. Corrected to 66, consistent with a dark-flour bread with partial whole-grain addition.\n
### לחם ברמן אקטיב (BC=497044)\n**72/B → 68/B** (Δ-4)\n\nExplicit label: 'סיבים פרה ביוטיים (אינולין) 3%'. At 3g/100g added inulin, roughly 26% of reported fiber=11.4g is supplemented. Base is genuinely 100% whole wheat (53% of product) — a real grain foundation. Correction is moderate: preserves whole-grain credit, removes inulin inflation. Corrected to 68.\n

---

## Intentionally Unchanged (Ambiguous Cases)

These products showed calibration concerns but were left unchanged because the insight line
already carries the editorial correction, or the correction would be punitive rather than honest.

| Product | Score | Name | Reason |
|---------|-------|------|--------|
| BC=481197 | 76/B | לחם מחמצת גרעינים | White flour is first among flour types (24% of product) but overall flour blend is mixed; 40% of product is whole grain. Ambiguous — insight line flags it without score contradiction. |
| BC=497044-note | 72→68/B | לחם ברמן אקטיב (partial) | Inulin corrected from 72→68 but not pushed to C: whole-wheat base (53% of product) is genuine. Moderate correction only — the product has real structural quality beneath the supplement. |
| BC=2079033-note | 74→69/B | לחם דגנים לייט (partial) | Fiber corrected from implausible 14.2g but not pushed to C: grain fractions are genuinely whole. Water-first high-hydration bread with real grain base. |
| BC=7290016967074 | 72/B | לחם אנג'ל חיטה מלאה | 9 E-numbers — highest additive count in B-grade. But 100% whole wheat, 8g fiber. Additive load is editorially covered by insight line. High E-count alone does not trigger correction. |
| BC=7290014940901 | 70/B | לחם פשוט מלא | 6 E-numbers on a product named 'פשוט'. Insight line 'הפשטות מגיעה עד הרכיב הרביעי' already carries the editorial load. Score 70 for 100% whole wheat is defensible; correction would be punitive. |
| BC=4685157 | 70/B | לחם שיפון 100% פרוס | 100% whole rye, emulsifiers present. Score 70 with genuine whole-rye base is correct. |
| BC=7296073659945 | 66/B | קרקר דק רוזמרין | Only 25% whole wheat but cracker format concentrates fiber. Palm oil present. Applying flour-base correction to crackers requires category-specific thresholds not yet defined. |
| BC=574035 | 66/B | לחם אחיד פרוס (תנובה) | Dark wheat + vegetable oils + emulsifiers. Insight line notes absence of extended improvers — not contradicted by B score. One preservative only (not dual). Left unchanged. |
| BC=497112 | 66/B | לחם פרוס אחיד | Dark wheat, E282 + E481. Insight 'הנוסחה הבסיסית' describes without contradicting B. Fiber=4.8g from dark wheat is genuine. Left unchanged. |
| BC=8713917 | 67/B | לחם שיפון כהה | 7 E-numbers — concerning. But dark wheat 66% + whole rye 34%, fiber=6.1g is real mixed grain. Additive count alone is not sufficient without insight line contradiction. |

---

## Score-Insight Line Contradiction Check

After patch, the following score/insight contradictions are resolved:

| Barcode | Insight | Old Score | New Score | Resolution |
|---------|---------|-----------|-----------|------------|
| 2079477 | שיא התוספות | 67/B | 64/C | B said "acceptable"; C says "maximum additives = lower half" |
| 481180 | הבסיס לבן, המחמצת שלישית | 71/B | 64/C | B parity with whole-grain sourdoughs; C matches white-flour cluster |
| 497570 | ה'פלוס' הוא תוספת סיבים, לא גרעין שלם | 68/B | 62/C | B said "adequate"; C matches the editorial judgment |
| 4033736 | קמח לבן 100%, סוכר שני, מתחלבים | 66/B | 62/C | B for enriched white brioche-style was unjustifiable |
| 7290018500231 | אנג'ל לשבת, לא לשבוע | 65/B | 62/C | Score now matches occasion-framing in insight |
| 7290017947105 | הסגנון מסביר את הרכב | 65/B | 62/C | "Style explains composition" lands correctly at C |
| 7290018500316 | גרעין כוסמין מנופה. 3.3 גרם סיבים בלבד | 68/B | 64/C | Sifted spelt described as C-grade; score now confirms |

---

## Verdict

**Safe to wire as v2.**

The corrected distribution (B: 53, C: 25, A: 2, D: 1) improves
grade discrimination without destabilizing the corpus. A-grade products are unchanged.
The top of the B band (77–80) remains intact — the genuinely strong products were not touched.
Seven grade changes move products to where their composition and insight lines already placed them.
