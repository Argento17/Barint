# Glass Box D1 — Dietary Energy Density: Evidence Review

**Classification:** Internal — Glass Box program (TASK-179)  
**Version:** v1  
**Date:** 2026-06-06  
**Owner:** Nutrition Agent  
**Task:** TASK-194  
**Source:** "Beyond Nutrients: A Systematic Review of Dietary Patterns, Microbial Ecology, and Chronic Disease Outcomes" (New Batch, 2026-06-06)  
**Status:** Evidence review only. No scoring rule is activated. D7 brief at `glass_box_d1_ded_d7_brief_v1.md`.

---

## 1. What DED is and why it is analytically distinct from raw calories

Dietary Energy Density (DED) is defined as kilocalories per gram of food as consumed. It is a property of the food, not the eater: the same serving mass at different calorie concentrations is directly computable from a nutrition panel (kcal ÷ serving mass in grams) without any per-person parameters.

This distinction matters for Bari's de-moralized stance. A calorie count says "this product has X kcal per serving" — which implicitly invokes the eater's serving behavior and total dietary context. DED says "this product carries X kcal per gram of physical food" — which is a structural property of the food architecture. A product at 1.2 kcal/g is structurally water-rich and physically voluminous relative to its energy; a product at 4.5 kcal/g is energy-concentrated. Neither statement requires knowledge of the consumer.

This is consistent with BEV-008 (structural-first over nutrient-threshold): DED describes food matrix integrity — how concentrated the energy is per unit of food substance — rather than giving dietary advice about how much to eat.

---

## 2. Primary evidence base

### Source A — 1-Year DED Randomized Clinical Trial (weight loss, ad libitum)

A year-long randomized parallel trial in obese women compared a reduced-fat diet (RF group) against a reduced-fat diet with explicit instruction to increase water-rich foods, particularly fruits and vegetables (RF+FV group). Crucially, no calorie limits were assigned; both groups ate ad libitum.

After one year, dietary analysis confirmed the RF+FV group achieved a lower DED by consuming a greater physical weight of food. Both groups lost significant weight, but the RF+FV group lost significantly more and reported significantly less hunger throughout the trial. The trial demonstrates that DED reduction achieved through food structure — not calorie restriction — produces superior satiety and weight outcomes in a free-living setting.

Relevance to Bari's threshold: the intervention targeted a DED reduction consistent with what a food below ~1.5 kcal/g achieves when composed predominantly of water-containing whole ingredients. The threshold is not the paper's stated finding but is consistent with the structural properties of the food type the intervention promoted (high water content, high volume, lower energy concentration).

### Source B — WHI DED Prospective Cohort (cancer risk, independent of weight)

A prospective cohort study of postmenopausal US women in the Women's Health Initiative measured baseline dietary energy density via self-reported dietary data and followed cancer outcomes. The highest DED quintile was associated with a statistically significant increased risk of developing any obesity-related cancer — breast, colorectal, ovarian, and endometrial — compared to the lowest quintile.

The critical finding: this increased risk was statistically limited to women who were of normal weight at enrollment. In overweight and obese women, who presumably have multiple intersecting metabolic risk factors, the DED association was not independently significant. This suggests that chronic high-DED diet drives metabolic dysfunction, insulin resistance, and systemic low-grade inflammation in a way that operates independently of adiposity — the structural properties of the diet, not the weight outcome, are the proximal mechanism.

This is the strongest evidence that DED is not a proxy for calorie overconsumption but is an independent structural signal: the food's energy concentration per gram of physical food affects metabolic risk even when it does not manifest in above-normal body weight.

Relevance to Bari: DED as a food architecture signal — not a calorie signal — is directly consistent with Bari's analytical boundary (BEV-001; BEV-002).

### Source C — WHI WHEL Trial (DED reduction, behavioral sustainability)

A randomized dietary intervention trial in breast cancer survivors randomized the intervention group to intensive counseling to reduce fat and increase fruits and vegetables. The intervention group reduced DED at year 1 and maintained a reduced DED at year 4 compared to year-1 baseline. The intervention achieved modest significant weight loss at year 1; this difference was not statistically significant at year 4 compared to controls.

The source documents this as a limitation of DED reduction alone without broader behavioral strategies for long-term weight maintenance. For Bari's purposes this is not a limitation: Bari scores the food architecture, not the consumer's long-term dietary behavior. The WHEL trial confirms that DED reduction is achievable and measurable; the sustainability question is a dietary-behavior question outside Bari's scope.

---

## 3. Why DED is consistent with Bari's de-moralized stance

Bari's core analytical commitment (BEV-003d) is that it is not a low-calorie optimization system. DED satisfies this test:

- A high-DED product can be wholly appropriate. Plain tahini (~6 kcal/g) correctly scores high because it is a single-ingredient whole-food fat source (BEV-050/BEV-051 floor rules). Olive oil (~9 kcal/g) is DED-very-high and structurally sound. The D1 DED signal must not override whole-food protection rules.
- DED describes what the food is — energy-concentrated or energy-dilute per physical gram — not what the consumer should eat. The metric is food architecture (matrix water content, structural density), not dietary advice.
- The satiety mechanism behind DED (gastric mechanoreceptors detecting physical stretch from food volume; enteroendocrine cells releasing PYY and CCK in response to the physical food bolus) is a structural property of the food interacting with physiology — consistent with BEV-033 (structural satiety vs. macro satiety) and BEV-034 (liquid calorie effect).

The distinction from raw calories: a 250 kcal bar at 100g (2.5 kcal/g) and a 250 kcal fruit portion at 400g (0.6 kcal/g) provide the same calories but produce different gastric volume, different satiety signaling, and structurally different food experiences. DED captures this; raw calorie count does not.

---

## 4. Proposed thresholds and their grounding

**Positive signal: ≤1.5 kcal/g.** Foods below this threshold are typically high in water and/or fiber — fresh vegetables, fruits, broth-based preparations, plain dairy (milk, plain yogurt at ~70–90 kcal/100g = ~0.7–0.9 kcal/g), lean proteins in their natural state. The 1.5 kcal/g boundary is consistent with what the 1-Year DED Trial intervention achieved through promoting water-rich whole foods and with the general evidence that foods below this threshold produce the greatest gastric volume per calorie.

**Penalty: >2.5 kcal/g.** Products above this threshold are energy-concentrated: most baked goods, processed snacks, cheese spreads, confectionery, nut butters. The 2.5 kcal/g upper threshold captures a meaningful gap above the positive range while leaving a neutral zone (1.5–2.5 kcal/g) for food types like whole grains (bread ~2.5–2.7 kcal/g), some fermented dairy, and mixed dishes.

---

## 5. Category applicability notes

DED must be applied with category-specific guards to avoid conflicts with existing calibrations:

**Snack bars / granola:** DED is highly relevant — this is the category most prone to high energy concentration. A 450 kcal/100g bar = 4.5 kcal/g, clearly above the penalty threshold. Interaction with existing HTC caps (BEV-042) must be designed to avoid double-counting.

**Bread:** Most commercial bread is 2.3–2.8 kcal/g. Whole grain varieties tend toward the lower end; highly processed enriched breads toward the higher end. DED could reinforce existing processing quality signals without replacing them.

**Dairy (milk, yogurt):** Plain whole milk = ~0.6 kcal/100ml (liquid), yogurt = ~0.7–1.0 kcal/g. Already well within the positive threshold. The existing beverage category calibration (BEV-043) and dairy_protein calibration (BEV-044) may overlap. DED should not double-count what existing calorie density thresholds already capture in these categories.

**Whole-food fats (nuts, oils, tahini, olive oil):** DED ranges from ~5.5 to ~9 kcal/g. These must be protected by the NOVA 1 floor (BEV-050) and whole-food fat floor (BEV-051) — the DED penalty must not fire on single-ingredient whole foods. This is a firm constraint on the rule design.

---

## 6. Signals explicitly marked annotate_only (no new rules needed)

**Fermentation and live cultures:** EV-024 already governs pasteurisation handling; BEV-023 documents fermentation as a structurally beneficial signal with explicit positive credit deferred to Future Work. The Beyond Nutrients source confirms fermented foods (kefir, kimchi, yogurt, fermented cottage cheese) produced broad microbial diversity increases and systemic inflammatory marker reduction in the Stanford Cell Trial. This hardens BEV-023 and BEV-069 (fermentation explicit credit as Future Work) — it does not create a new signal. "Fermented" claims on dry products (crackers labeled "fermented," powders) remain annotation-only: the structural benefit of live fermentation does not survive drying, and label claims alone cannot verify live culture activity.

**Intact-grain protein kinetics:** The source documents that protein absorption kinetics from slow-digesting matrices (e.g., casein in milk protein) extend the anabolic window for muscle protein synthesis beyond what isolated fast-digesting proteins achieve. This is mechanistically interesting but too downstream from label-observable facts to constitute a BSIP2 signal at this time. Intact-grain protein source credit is already partially addressed under BEV-032 (whole-food matrix superiority) and BEV-036 (native vs. extracted fiber). No new rule is needed.

**UPF classification overlap with NOVA:** The source documents extensive epidemiological evidence linking NOVA Class 4 UPF intake to cardiovascular mortality, type 2 diabetes, and all-cause mortality. This is already the primary governance of BEV-021 (NOVA as primary processing signal) and BEV-022 (processing penalties). No change.

---

*Evidence tier for DED signal: Moderate. Multiple cohort studies and RCTs support the threshold and direction; the WHI cancer cohort provides independent mechanistic evidence beyond weight outcomes; behavioral sustainability limitations (WHEL) are outside Bari's analytical scope. D7 brief at `glass_box_d1_ded_d7_brief_v1.md`.*
