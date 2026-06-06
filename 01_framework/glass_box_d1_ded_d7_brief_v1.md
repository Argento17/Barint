# Glass Box D1 — DED Signal: D7 Sign-Off Brief

**Classification:** Internal — D7 gate document  
**Version:** v1  
**Date:** 2026-06-06  
**Author:** Nutrition Agent  
**Task:** TASK-194  
**Decision required:** Owner D7 sign-off to activate DED as a scored signal in D1  
**Evidence Registry:** BEV-082 (`score_moving_pending_d7`)  
**Full evidence review:** `glass_box_d1_energy_density_review_v1.md`

---

## What the rule does

Add Dietary Energy Density (DED) as a scored signal in the D1 dimension (Nutrition / Glass Box). DED = kcal ÷ serving mass (g). It is directly computable from the nutrition panel without any per-person parameters.

The rule fires in two directions:

| Threshold | Effect |
|---|---|
| ≤1.5 kcal/g | Positive D1 signal — food is energy-dilute; structurally consistent with high water/fiber content |
| >2.5 kcal/g | Penalty D1 signal — food is energy-concentrated |
| 1.5–2.5 kcal/g | Neutral zone — no signal |

**Hard constraint:** DED penalty must NEVER fire on NOVA 1 single-ingredient whole foods (BEV-050 floor) or whole-food fat products (BEV-051 floor). Olive oil, tahini, nuts — these are correctly energy-dense and the floor rules take precedence.

---

## Why DED, not raw calories

Bari scores food architecture, not dietary advice. DED describes a structural property of the food — how much energy is packed into each gram of physical substance — not a serving-intake recommendation. A 400g fruit portion at 0.6 kcal/g and a 100g bar at 4.0 kcal/g have the same calories per serving only if portions are equal; their architecture is radically different. DED captures this without telling the consumer how much to eat.

The satiety mechanism (gastric mechanoreceptors, PYY/CCK release in response to physical food volume) is structural: the food's energy per gram of physical weight drives it. This is consistent with BEV-008 (structural-first) and BEV-033 (structural satiety).

---

## Evidence quality

Evidence tier: **Moderate.** Three studies from the source document:

1. **1-Year DED RCT** — randomized, ad libitum, obese women; RF+FV group reduced DED via food structure (not calorie counting), lost more weight, reported less hunger. Demonstrates DED reduction through food composition changes produces real satiety outcomes.

2. **WHI DED Prospective Cohort** — postmenopausal women; highest DED quintile associated with increased obesity-related cancer risk, notably in normal-weight women. This is the key finding: DED predicts metabolic risk independently of weight, suggesting it is a food-architecture signal, not a proxy for overeating.

3. **WHI WHEL Trial** — randomized intervention reduced DED; weight loss achieved at year 1, not sustained at year 4. Limitation is behavioral sustainability — outside Bari's scope.

Limitation: the RCT mixed DED reduction with increased fruit/vegetable diversity; DED alone is the leading explanatory variable but the two are correlated. The WHI cohort evidence is observational with inherent confounding. No Israeli-specific data. Evidence is **Moderate, not Strong.**

---

## Which categories it touches and expected score distribution shift

| Category | Typical DED range | Expected effect |
|---|---|---|
| Milk (beverage) | ~0.5–0.7 kcal/g (liquid) | Positive signal — most products already at/below threshold. Minimal score shift; may reinforce existing B-tier |
| Plain yogurt / quark | ~0.7–1.2 kcal/g | Positive signal for plain varieties. Flavored/sweetened yogurts 1.0–1.5 kcal/g — near boundary |
| Bread | ~2.3–2.8 kcal/g | Most bread in the penalty zone (>2.5). Whole grain breads at the lower end, white breads higher. Could reinforce processing quality penalty — double-counting risk must be managed |
| Granola / snack bars | ~3.5–5.0 kcal/g | Strongly in penalty zone. Reinforces existing HTC caps (BEV-042). Double-counting coordination required |
| Hummus / sauce spreads | ~1.5–3.0 kcal/g | Mixed — plain hummus ~1.5–1.8 kcal/g (boundary); tahini ~6 kcal/g (whole-food floor protects it) |
| Cheese spreads / cottage | ~1.0–2.0 kcal/g | Near or below positive threshold for lower-fat varieties; standard spreads toward neutral zone |
| Whole-food fats (nuts, oils) | ~5.5–9.0 kcal/g | Correctly EXCLUDED by BEV-050/BEV-051 floor rules — DED penalty must not fire |
| Cereals (dry) | ~3.5–4.0 kcal/g | Penalty zone — but already governed by BEV-045 calorie density thresholds. Double-counting risk |

**Net expected effect:** positive signals are additive in dairy and fresh-produce-adjacent categories. Penalties reinforce (and must be coordinated with) existing caps in snacks and cereals. Bread may see modest score reductions for high-density products. The main implementation risk is double-counting with existing calorie density dimension rules — this must be resolved in rule design before activation.

---

## Single recommended threshold

Recommended: **≤1.5 kcal/g positive; >2.5 kcal/g penalized; neutral zone 1.5–2.5 kcal/g.**

Rationale for this exact pair:
- 1.5 kcal/g is the structural boundary below which whole-food water-rich foods (plain dairy, vegetables, broth-based products) concentrate. The 1-Year DED Trial intervention was consistent with achieving this range. It is also well above water alone (~0 kcal/g) and captures real food at its lower density range.
- 2.5 kcal/g marks the boundary above which most processed snacks, confectionery, and enriched grain products sit. Plain whole grain bread is ~2.3–2.5 kcal/g — the neutral zone correctly leaves it uncapped by this rule while still flagging highly concentrated products above it.
- The neutral zone prevents the rule from generating noise on the large number of products in the 1.5–2.5 range (bread, mixed dishes, fermented dairy) where DED is not the informative signal.

Do NOT collapse to a single threshold: a unidirectional rule (penalty only above X, or positive only below Y) would lose the architectural symmetry the evidence supports.

---

## What this brief does not authorize

This brief is a gate document. Owner D7 sign-off enables a scored rule to be written and implemented. It does not:
- Change any existing published score
- Authorize implementation before Nutrition + Product co-sign
- Resolve the double-counting coordination question (that is a rule-design task for Phase 2 implementation)
- Affect fermentation signals, intact-grain protein kinetics, or UPF classification (all separately governed; see evidence review)

**To proceed:** owner signs off on threshold pair (1.5/2.5 kcal/g recommended) and authorizes a formal scoring rule proposal co-signed by Product Agent. Rule design must address the double-counting coordination with BEV-042/BEV-043/BEV-044/BEV-045.
