# Bari Category Production Simulation — חלב (Milk) v1

**Classification:** Production Simulation — Internal  
**Issued:** 2026-05-29  
**Author:** CE Controller 1 — Chief Nutrition, Scoring & Content Architect  
**Status:** Active — governance application document; not a framework document  
**Governance applied:** Comparison Governance Constitution v1 (as amended), Consumer Use-Case & Purpose Guardrails v2 (as amended), Distortion Registry DISTORTION-001 through -010  
**Precondition:** Cereals Gap Resolution Report v1 amendments applied to governing documents  
**Data assumption:** BSIP0/1/2 pipeline data is assumed to exist for simulation purposes

---

## 1. Executive Summary

**Category selected: חלב — Milk**

Milk was selected over Bread, Yellow Cheese, and Protein Bars because it simultaneously exercises the highest number of governance provisions. No other candidate category activates all four cereals amendments, two endemic distortions across distinct pools, a genuine Lens 3 scenario, and a Section 5.2.1 calibration test in a single production run.

**What milk validates in the governance stack:**

| Governance provision | Application in milk |
|---|---|
| Section 2.8 — Developmental definition | Growing-up formulas on the dairy shelf |
| Section 2.9 — Architectural divergence | Plant-based vs. dairy (proxy limitation surfaces) |
| Section 6.4 — Endemic Distortion Protocol | DISTORTION-004 endemic in plant-based pool; DISTORTION-007 endemic in dairy pool |
| Section 5.2.1 — Claim threshold table | Protein milk threshold tests the general ≥8g/100ml threshold and breaks it |
| Lens 3 — Restriction-driven | Vegan and lactose-intolerant consumers with binding constraints |
| DISTORTION-007 — Natural sugar | Lactose penalty in dairy milk — maximum relevance |
| DISTORTION-004 — Fortification | B12, calcium, vitamin D in plant-based alternatives |
| Marketing Divergence Finding | Protein claims, "natural" claims, nutritional equivalence claims |

**Simulation verdict: B — Yes with Conditions.**

The governance handles the category correctly on all structural questions. Two conditions remain before launch: protein milk threshold calibration (Section 5.2.1 D6 block) and "light" milk threshold documentation. Three genuine friction points emerged. None require new governance — all are calibration or presentation decisions within existing frameworks.

**One amendment tested at its limit:** Section 2.9's proxy indicators do not cleanly identify plant-based milk as a distinct sub-category because the divergence is qualitative (protein source, food matrix origin) rather than the quantitative excess pattern (high sugar + high fat + NOVA 4) the proxies were calibrated for. The lens framework handled the milk case correctly. This is a genuine limitation of the proxy indicators, documented in Section 8.

---

## 2. Category Definition

### 2.1 Category Scope

**Category name:** חלב — Milk and Milk Alternatives  
**Hebrew shelf position:** Refrigerated dairy aisle and UHT/ambient shelf, plus plant-based alternatives section

**Included:**

| Sub-group | Examples | Governance notes |
|---|---|---|
| Dairy milk — all fat percentages | Tnuva 1%, Tara 3%, Yotvata 5% | Pool A; Lens 1 default |
| Flavored dairy milk | Chocolate milk, strawberry, vanilla | Pool B; sub-pool per Section 2.9 |
| Lactose-free dairy milk | Tnuva Lactose-Free, Tara Lactose-Free | Pool A/E; Lens 1 default (see 2.2) |
| Protein-enriched dairy milk | Tene Protein (Tnuva), similar | Pool C; Lens 2 pending threshold |
| Oat milk | Oatly, local brands | Pool D; Lens 1 within-pool / Lens 3 cross-pool |
| Almond milk | Alpro Almond, local brands | Pool D |
| Soy milk | Alpro Soy, Silk | Pool D |
| Rice milk | Available in health-food segment | Pool D |
| Coconut milk (drinking, carton format) | Alpro Coconut | Pool D; not cooking coconut cream |

**Excluded:**

| Product type | Reason | Governance basis |
|---|---|---|
| Infant formula (0–12 months) | Absolute restriction — different regulatory framework | Article II, Section 2.3 |
| Growing-up formula age 1–3 | Developmental classification per Section 2.8 — excluded from adult pools | Section 2.8, Indicators D2 + D3 |
| Growing-up formula age 3+ | Section 2.8 evaluation — see boundary product ruling (2.3) | Section 2.8 |
| Heavy cream / whipping cream | Different caloric role; primary purpose fails Article II, Section 2.1 test | Article II, Sections 2.1–2.2 |
| Sour cream / crème fraîche | Condiment / cooking context; different consumption unit | Article II, Section 2.2, Criterion B |
| Evaporated / condensed milk | Different preparation context; consumed diluted or cooked; incomparable unit | Article II, Section 2.2, Criterion B |
| Drinkable yogurt / kefir | Fermented dairy — belongs to yogurt category | Category boundary — different primary purpose |
| Milk-based protein shakes | Supplement-adjacent; caloric role of meal replacement | Article II, Section 2.3 |
| Cooking coconut cream | High-fat cooking product; different primary purpose | Article II, Section 2.1 |

### 2.2 Lactose-Free Milk Classification

Lactose-free milk presents a Lens 3 ambiguity. Many lactose-free buyers are medically intolerant (binding restriction); many others are lifestyle buyers (non-binding preference). Guardrails v2, Rule 5: ambiguous cases default to Lens 1.

**Ruling:** Lactose-free dairy milk is assigned to Pool A under Lens 1 unless a specific comparison is constructed specifically for lactose-intolerant consumers, in which case Lens 3 disclosure is required before the score.

**Nutritional note:** Lactose-free milk is enzymatically treated (lactase added to split lactose into glucose and galactose). Caloric and protein profiles are essentially identical to standard dairy milk at the same fat percentage. DISTORTION-007 (natural sugar) applies: the sugar row on the label of standard milk reads ~5g/100ml (lactose); lactose-free milk reads ~5g/100ml (glucose + galactose) — equally penalized. No distortion amplification or reduction from the conversion.

### 2.3 Boundary Product Rulings

**Ruling 1 — Growing-up formula age 1–3 (Materna, Similac Go&Grow, NAN):**
Section 2.8 assessment:
- D2: Explicit developmental language ("מגיל שנה," "for toddlers," age-range labeling) — PRESENT
- D3: Pediatric serving size (powder typically yields 150–200ml per serving; formula volume is pediatric-calibrated) — PRESENT
- Two indicators present → developmental classification confirmed
- Action: Excluded from all adult comparison pools. If corpus contains sufficient developmental products (≥5) for a developmental milk comparison, a separate developmental pool may be constructed. If fewer than 5, editorial statement only — no ranking.

**Ruling 2 — Growing-up formula age 3+ ("Junior" or "Growing Up" milks):**
Section 2.8 assessment:
- D2: "Junior," "grow," "3+" language typically present — PRESENT
- D3: Serving size calibrated for children (150–200ml); not adult-sized — PRESENT
- Two indicators → developmental classification confirmed → excluded from adult pools

**Ruling 3 — Protein milk with functional sports claims:**
Products marketed with "sports recovery," "post-workout," or similar language. Lens 2 assessment: both the functional claim AND architectural support required. If protein content does not meet the milk-specific threshold (pending D6 calibration), Lens 2 is not available. Conservative default: Lens 1, with Marketing Divergence Finding evaluation deferred pending threshold calibration.

**Ruling 4 — Barista oat milk editions:**
Same product, variant under Pool D. Article II, Section 2.5: product variants are eligible for comparison with each other. Barista and standard versions of the same oat milk are variant-comparable. No separate sub-pool required.

**Ruling 5 — "Functional" milk with added probiotics or omega-3:**
Lens 2 candidate. Architectural support required: probiotics require documented CFU (Guardrails v2, Section 5.2, Condition 2 — see Example 2 in Section 5.5). Omega-3 claims require documented dose against an established functional threshold (not defined in Section 5.2.1 — D6 blocks Findings for omega-3 claims until documented). Default: Lens 1 unless CFU is documented.

---

## 3. Comparison Blueprint

### 3.1 Pool Structure

**Pool A — Standard Dairy Milk (Lens 1, default)**

- Products: Unflavored dairy milk at all fat percentages (skim/0.1%, 1%, 3%, 5%)
- Comparison basis: Direct comparison on nutritional architecture; fat percentage is the primary driver of score difference
- DISTORTION-007 active: Lactose penalty applies to all products; endemic within Pool A
- Section 6.4 activated: Pool A requires a DISTORTION-007 category-level disclosure
- Cross-pool rules: Pool B comparison (flavored) permitted with added-sugar disclosure. Pool D comparison permitted with lens disclosure. Pool C comparison permitted with protein threshold caveat.
- Score delta expectations: Pool A products are nutritionally similar; most comparisons will fall in the noise-to-marginal range (0–6 points); equivalence finding is a likely and valid outcome

**Pool B — Flavored Dairy Milk (Lens 1, sub-pool)**

- Products: Chocolate milk, strawberry milk, vanilla milk — all dairy-based
- Sub-pool basis: Section 2.9 proxy indicators — added sugar in chocolate milk typically ≥10g/100ml (chocolate milk commonly runs 10–12g sugar/100ml, of which 5–6g is lactose and 5–7g is added sucrose/cocoa solids); parent category (Pool A) median sugar is ~5g/100ml (lactose only). Proxy indicators: added sugar ≥10g vs. median ≤5g — ONE proxy triggered. NOVA: standard chocolate milk is NOVA 3 (added sugar, processing) vs. Pool A NOVA 1–2 — SECOND proxy triggered.
- Two proxy indicators confirmed → Pool B is a distinct sub-category under Section 2.9
- Comparison: Within-pool direct comparison on nutritional architecture; sugar load and additive profile are primary drivers
- Cross-pool: Pool A comparison permitted with added-sugar delta disclosure

**Pool C — Protein-Enriched Dairy Milk (Lens 2 pending; Lens 1 default)**

- Products: Dairy milk with meaningfully elevated protein concentration relative to Pool A baseline (~3.2g/100ml)
- Threshold status: Section 5.2.1 general beverage threshold ≥8g/100ml. Israeli protein milk products typically deliver 5–6g/100ml. The general threshold is not calibrated for milk.
- D6 governance response: Lens 2 cannot be formally assigned, and Marketing Divergence Findings for protein claims cannot be issued, until a milk-specific protein threshold is documented. Pool C is provisionally held under Lens 1.
- Provisional comparison: Protein milk products compared against Pool A products under Lens 1, with a note that the protein difference is observable but its functional significance is not evaluated until the threshold is calibrated.
- Action required before full Pool C function: CE Controller 1 to document milk-specific protein threshold (proposed: ≥5.5g/100ml as "protein positioning" threshold — approximately 70% above dairy baseline; requires external validation before formal adoption)

**Pool D — Plant-Based Milk Alternatives (Lens 1 within-pool; Lens 3 cross-pool for restricted consumers)**

- Products: Oat milk, almond milk, soy milk, rice milk, coconut milk (carton/drinking format)
- Pool basis: Section 2.9 proxy indicators do not cleanly identify this sub-group for reasons documented in Section 8 (Framework Retrospective). Pool D is established through the primary purpose test (Article II, Section 2.1) and the lens framework instead.
  - Within-pool: All plant-based alternatives serve the same primary purpose for the same consumer decision (dairy-free milk substitute). Direct comparison under Lens 1.
  - Cross-pool: For non-vegan, non-restricted consumers who could choose either dairy or plant-based: cross-pool comparison is valid with lens disclosure per Constitution v1, Article III, Section 3.4.
  - For vegan or dairy-intolerant consumers: Lens 3 applies to Pool D products. The restriction drove formulation — plant-based milks were formulated without dairy. Cross-lens disclosure required before any comparison with Pool A.
- DISTORTION-004 endemic: Virtually 100% of Pool D products are fortified with calcium, B12, vitamin D. Section 6.4 activates. Pool D requires a DISTORTION-004 category-level disclosure.
- Score expectations: Within Pool D, protein content is the primary differentiator. Soy milk (~3.3g protein/100ml) scores significantly higher than almond milk (~0.4g protein/100ml). This is a material score difference (15–25+ points) driven by a genuine nutritional gap. The comparison is valid and informative.

**Developmental Pool (Section 2.8) — Not ranked; editorial statement only if corpus too small**

- Products: Growing-up formulas age 1–3 and age 3+
- Excluded from Pools A–D
- If ≥5 developmental milk products exist in corpus: developmental sub-pool constructed with its own editorial treatment
- Score and architecture reported honestly; developmental context stated before any score; no ranking against adult products

### 3.2 Exclusion Application

| Product | Pool assignment | Exclusion basis |
|---|---|---|
| Infant formula 0–12 months | EXCLUDED | Article II, Section 2.3 (absolute restriction) |
| Growing-up formula 1–3 | EXCLUDED from adult pools | Section 2.8 (D2 + D3 confirmed) |
| Growing-up formula 3+ | EXCLUDED from adult pools | Section 2.8 (D2 + D3 confirmed) |
| Drinking yogurt / kefir | EXCLUDED | Different primary purpose — yogurt category |
| Protein shake (meal replacement) | EXCLUDED | Article II, Section 2.3 (meal replacement) |
| Cooking coconut cream | EXCLUDED | Article II, Section 2.1 (purpose test fails) |

### 3.3 Endemic Distortion Handling

**DISTORTION-007 (Natural Sugar) — Endemic in Pool A**  
Prevalence: 100% of Pool A (dairy milk universally contains lactose)  
Section 6.4 trigger: ACTIVATED  
Category-level disclosure text (approved for Pool A):

```
CATEGORY NOTE — Natural Sugars

Dairy milk contains lactose — milk's naturally occurring sugar — which 
appears as "sugars" on the nutritional label. Bari's current scores 
assess all sugar types identically. 

This applies to all dairy milk products. Scores reflect the full 
nutritional architecture including lactose content. Lactose is 
structurally part of the dairy matrix and has a different metabolic 
role from added sugars; this distinction is not yet captured in scoring.
```

**DISTORTION-004 (Fortification) — Endemic in Pool D**  
Prevalence: ~95–100% of Pool D (fortification is standard practice in all commercial plant-based milks)  
Section 6.4 trigger: ACTIVATED  
Category-level disclosure text (approved for Pool D):

```
CATEGORY NOTE — Fortification

Plant-based milk alternatives are routinely enriched with calcium, 
vitamin D, and vitamin B12 to compensate for nutrients that dairy 
milk provides naturally. Bari's current scores do not credit these 
added vitamins and minerals as positive nutritional factors.

This applies to most plant-based milk products. A fortified oat milk 
or almond milk may deliver meaningful calcium and B12 that is not 
visible in its Bari score. The score reflects macronutrient 
architecture and ingredient integrity only.
```

**Multiple endemic distortions on one shelf:** Pool A and Pool D are distinct pools. Each carries its own category note. The notes are not consolidated — they apply to different product groups. Presentation decision (for Cursor): Pool A products display the natural sugar note; Pool D products display the fortification note. A consumer viewing the full milk shelf sees both notes in their respective pool sections — not a combined notice, since they describe different products.

### 3.4 Claim Threshold Status

| Claim type | Section 5.2.1 status | D6 consequence |
|---|---|---|
| "Protein milk" / "high protein milk" | NOT in table (general ≥8g/100ml too high for milk context) | Lens 2 assignment blocked; Marketing Divergence Findings for protein claims blocked until milk-specific threshold documented |
| "Calcium rich" | NOT in table | Marketing Divergence Findings blocked for calcium claims |
| "Light" / "דל שומן" | NOT in table | Marketing Divergence Findings blocked for light claims |
| Probiotic / CFU | Threshold defined (functional threshold range 1–10bn CFU per serving, Guardrails v2, Section 5.5 Example 2) | Finding can proceed if CFU claim is present without documentation |
| "Keto" | ≤5g net carbs/100g — in table | Finding applicable if carb content exceeds threshold |

D6 checklist criterion: PARTIALLY BLOCKED at launch. Three claim types require threshold documentation before full Marketing Divergence Finding coverage is operational. This does not block launch — it blocks specific Findings for specific claims. The category can launch with the Finding infrastructure incomplete for these three claim types, provided the limitation is disclosed.

---

## 4. Distortion Analysis

### 4.1 Distortion Map

**DISTORTION-001 — Dairy fiber (not applicable)**  
Milk has no meaningful fiber content. The fiber dimension is irrelevant for liquid dairy. Pool A, B, C products score near-zero on fiber. Not a distortion risk; a category-architecture note. Non-applicable per C1 checklist.

**DISTORTION-002 — Protein Inflation (moderate, Pool C and Pool D)**  
Pool C: Protein milk products may use whey protein concentrate additions. If the protein addition is isolated/industrial rather than whole-food, DISTORTION-002 applies. Prevalence: moderate — not all protein milk products use isolated protein additions; some are simply reduced-dilution (more concentrated milk). Evaluation required at BSIP1 ingredient parsing level. Product-level disclosure where applicable.  
Pool D: Soy milk contains whole-food soy protein. DISTORTION-002 does not apply to soy milk protein (intact food matrix). No distortion for soy milk protein.

**DISTORTION-003 — Fiber Inflation (not applicable)**  
No products in the milk category are enriched with isolated fiber as a primary positioning claim. Non-applicable.

**DISTORTION-004 — Fortification (CATEGORY-CRITICAL in Pool D; moderate in Pool C)**  
Pool D: Endemic (see 3.3). Section 6.4 activated.  
Pool C: Protein milk may carry additional vitamin fortification. Moderate prevalence; product-level disclosure.  
Pool A: Standard dairy milk is not heavily fortified in Israel. Vitamin D addition is common but not universal. Low-moderate prevalence in Pool A; product-level disclosure where applicable, not endemic.

**DISTORTION-005 — Premium Product (moderate, Pool A)**  
Organic dairy milk (if present in corpus) at premium price vs. conventional dairy milk at similar or identical nutritional profile. A consumer who paid extra for organic milk receives the same score as conventional. Standard DISTORTION-005 scenario. Product-level explanation protocol (Constitution v1, Article V, DISTORTION-005): "Bari's score reflects nutritional architecture only. Organic certification, farming practice, and environmental credentials are not scored."

**DISTORTION-006 — Low-Calorie Halo (low-moderate, skim milk)**  
Skim/0.1% milk at ~35 kcal/100ml. The product has non-negligible protein (~3.5g/100ml) but its score may appear moderate in absolute terms because all dimensions (sugar, fat, protein) are at low absolute values. Not a significant distortion risk in milk — skim milk genuinely has a different nutritional profile from whole milk, and the score should reflect that. Low-moderate risk; monitor in scoring output.

**DISTORTION-007 — Natural Sugar (ENDEMIC in Pool A; active in Pool B)**  
Pool A: 100% endemic. Section 6.4 activated.  
Pool B: Chocolate milk contains both lactose (~5g/100ml) and added sugar (~5–7g/100ml). The added-sugar component is correctly penalized; the lactose component is penalized identically to added sugar. Moderate distortion — the effect exists but is partially correct (added sugar in chocolate milk does warrant some penalty; lactose penalty is overcorrection). Product-level disclosure for Pool B.

**DISTORTION-008 — Category Mismatch (low, managed by pool structure)**  
Cross-pool comparisons between Pool A (dairy) and Pool D (plant-based) are the primary category mismatch risk. The pool structure and cross-pool disclosure requirement in the comparison blueprint address this. Residual risk is low with proper lens disclosure.

**DISTORTION-009 — Additive Overreaction (moderate, Pool D)**  
Plant-based milks contain technical additives: calcium carbonate, dipotassium phosphate, gellan gum, xanthan gum, sunflower lecithin. These are functional additives (stability, calcium delivery, emulsification) rather than cosmetic additives (colors, synthetic flavors, sweeteners). DISTORTION-009 (safety/technical additive penalty = cosmetic additive penalty) applies. Prevalence: moderate in Pool D (most plant-based milks have 4–7 additives from this category). Product-level disclosure.

**DISTORTION-010 — Macro Obsession (low, Pool A; moderate, Pool D)**  
Pool A: Dairy milk's macronutrient profile is relatively balanced. Saturated fat in whole milk is not penalized. Low risk — the scoring architecture doesn't reward dairy milk for saturated fat; it also doesn't penalize it strongly. Net effect is neutral.  
Pool D: Very low protein in almond and rice milk, with a carbohydrate base from oats or rice. BSIP2's protein emphasis will correctly score soy milk higher and almond milk lower. This reflects a genuine nutritional difference rather than a distortion. Low macro obsession risk in Pool D.

### 4.2 Distortion Priority Table

| Distortion | Pool A | Pool B | Pool C | Pool D | Action |
|---|---|---|---|---|---|
| DISTORTION-001 | N/A | N/A | N/A | N/A | No action |
| DISTORTION-002 | Low | Low | Moderate | Low (soy exempt) | Product-level where applicable |
| DISTORTION-003 | N/A | N/A | N/A | N/A | No action |
| DISTORTION-004 | Low-mod | Low | Moderate | **ENDEMIC** | Section 6.4 activated (Pool D) |
| DISTORTION-005 | Moderate | Low | Low | Low | Explanation protocol |
| DISTORTION-006 | Low-mod | Low | Low | Low | Monitor |
| DISTORTION-007 | **ENDEMIC** | Active | Active | Low | Section 6.4 activated (Pool A) |
| DISTORTION-008 | Low | Low | Low | Low | Managed by pool structure |
| DISTORTION-009 | Low | Low | Low | Moderate | Product-level (Pool D) |
| DISTORTION-010 | Low | Low | Low-mod | Moderate | Product-level |

---

## 5. Marketing Divergence Analysis

### 5.1 Claim Landscape

The milk category contains six distinct marketing claim types that meet Condition 1 of the Marketing Divergence Finding standard (a specific purposive claim, not generic marketing language). Three are blocked by D6; three can proceed.

### 5.2 Claims That Cannot Produce Findings at Launch (D6 Block)

**Claim type: "Protein milk" / "protein"**  
Block reason: Section 5.2.1 general beverage threshold (≥8g/100ml) is not calibrated for milk. Israeli protein milk at 5–6g/100ml would fail this threshold, producing false positive Findings against products that may legitimately deliver meaningful protein elevation over the 3.2g/100ml dairy baseline. Applying the uncalibrated threshold would generate incorrect findings.  
Required action: CE Controller 1 to document milk-specific threshold before Pool C launches. Proposed threshold (not yet ratified): ≥5.5g/100ml (~70% above dairy baseline); requires external validation.

**Claim type: "Calcium rich" / "rich in calcium"**  
Block reason: No threshold in Section 5.2.1. Calcium content of fortified plant-based milk is observable, but "rich in calcium" requires a reference value (what quantity constitutes "rich"?). European claim regulation uses 15% NRV per 100ml as the threshold for "source of calcium" — this is a candidate external reference but is not yet adopted in Section 5.2.1.

**Claim type: "Light" / "דל שומן" / "reduced fat"**  
Block reason: No threshold in Section 5.2.1. The distinction between "1% fat" and "3% fat" is real, but what constitutes a meaningful "light" positioning relative to the category reference product is undefined. A 33% fat reduction (3% → 2%) vs. a 67% fat reduction (3% → 1%) both could carry a "light" label. Without a percentage reduction threshold, the Finding cannot be applied.

### 5.3 Claims That Can Produce Findings Now

**Finding Scenario 1 — Probiotic claim without CFU documentation**

Trigger: Any pool D oat milk or functional milk carrying "עם פרוביוטיקה" or "live cultures" claim without declared CFU count.

```
MARKETING DIVERGENCE FINDING

Claim: "מכיל תרביות חיות" (contains live cultures)
Observed: Live cultures declared on label; no CFU count available
Expected: Functional probiotic effect requires documented CFU count
          (typical functional range: 1–10 billion CFU per serving)
Gap: CFU count not declared — functional claim cannot be verified
Finding: The probiotic claim cannot be assessed from available data.
         Bari cannot confirm the product delivers live cultures at a
         functionally relevant dose.

The presence of live cultures is stated; their quantity is not.
```

**Finding Scenario 2 — Plant-based "equivalent to dairy" nutritional comparison**

Trigger: A plant-based milk carrying an explicit claim of nutritional equivalence or parity with dairy milk ("כמו חלב," "נותן כמו חלב," packaging imagery suggesting equivalence).

Condition 2 evaluation: "equivalent to dairy" implies protein, calcium, and caloric parity in the ordinary meaning of nutritional equivalence in a milk context.

Condition 3 evaluation: Almond milk with 0.4g protein/100ml vs. dairy milk's 3.2g/100ml delivers 12% of dairy's protein content. This falls materially short of "equivalent."

```
MARKETING DIVERGENCE FINDING

Claim: Nutritional equivalence to dairy milk
Observed: Protein — 0.4g / 100ml
Expected: Dairy milk provides approximately 3.2g protein / 100ml
          "Equivalent to dairy" implies comparable protein delivery
Gap: −2.8g protein / 100ml (the product provides approximately 12%
     of dairy milk's protein content)
Finding: The nutritional equivalence claim is not supported by this
         product's protein architecture. Calcium and vitamin D may
         be brought to dairy-comparable levels through fortification
         (see category fortification note) — protein is not.

The product serves as a dairy alternative; it is not nutritionally
equivalent to dairy milk on protein content.
```

**Finding Scenario 3 — "Keto" flavored milk**

Trigger: A milk product carrying a keto positioning claim that does not meet the ≤5g net carbs/100ml threshold defined in Section 5.2.1.

Standard dairy milk contains ~5g carbohydrate/100ml from lactose. A "keto dairy milk" that has not undergone specific carbohydrate reduction would fail the threshold immediately.

```
MARKETING DIVERGENCE FINDING

Claim: "מתאים לקטוגני" (suitable for keto)
Observed: 4.8g net carbohydrates / 100ml
Expected: Ketogenic suitability requires ≤ 5g net carbs / 100ml
Gap: 4.8g net carbs is at the boundary — however, per 250ml
     serving (typical milk consumption), this delivers 12g net carbs,
     exceeding ketogenic per-meal thresholds (typically ≤5–10g net carbs
     per meal) when consumed in standard quantities
Finding: The keto claim is partially supported on a per-100ml basis
         but is not supported at standard serving quantities. A consumer
         adhering to ketogenic dietary practice would need to account
         for the carbohydrate load at standard milk serving sizes.
```

Note: This Finding illustrates the serving size normalization problem identified in the cereals audit (Gap 5 — moderate). Per-100ml threshold passes; per-serving does not. The governance does not currently specify whether thresholds apply per 100ml/g or per serving. This is a calibration decision that should be documented before this Finding type is published.

---

## 6. Launch Simulation

### 6.1 Comparison Construction Walkthrough

**Scenario A — Standard Dairy, Direct Comparison (Pool A, Lens 1)**

Products: Tnuva 3% milk vs. Tara 3% milk

**Step 1 — Eligibility check:**  
Both products are unflavored dairy milk at identical fat percentages. Article II, Sections 2.1–2.2: same primary purpose, comparable consumption unit, same category definition. ELIGIBLE.

**Step 2 — Purpose divergence assessment:**  
Both products serve an identical consumer decision (choosing a standard 3% dairy milk). No purpose divergence exists. No purpose statement required before the score.

**Step 3 — Lens assignment:**  
Lens 1 — General Everyday Choice (default). No positive architectural evidence for Lens 2 or Lens 3. Conservative default applies.

**Step 4 — Pool assignment:**  
Pool A. Both products share the same structural profile.

**Step 5 — Score delta assessment:**  
Assumed delta: 2–4 points (both are standard dairy milk; primary differences are likely NOVA classification nuances, minor additive differences from processing, or label data completeness gaps).  
- If delta ≤2: Declare equivalent. Constitution v1, Article III, Section 3.3.
- If delta 3–4 (marginal): One product has a modest advantage. Identify specific driver (additive count difference, NOVA classification, or label completeness penalty).

**Step 6 — Distortion disclosure:**  
DISTORTION-007 endemic: Pool A category note displayed. No additional product-level distortion note needed unless BSIP2 identifies a specific distortion signal in one product.

**Step 7 — Explanation construction (Article IV.7):**

```
LAYER 1 — PURPOSE STATEMENT
Not required — both products serve the same consumer decision.

LAYER 2 — SCORE DIFFERENCE
[Product A]: [score]/[grade]
[Product B]: [score]/[grade]
Delta: [X points] — [Noise / Marginal]

LAYER 3 — SPECIFIC DRIVERS (if delta 3-6)
The [X]-point difference is primarily driven by:
  · Processing: [observation from BSIP1 enrichment]
  · Additive profile: [specific additive count difference, if any]

LAYER 4 — TRADEOFFS
[If delta is noise, no ranking — state equivalent finding]

LAYER 5 — KNOWN LIMITATIONS
  · Lactose note: Category note applies (Pool A).
  · Data confidence: [full / partial depending on BSIP1 coverage]

LAYER 6 — WHAT THIS SCORE DOES NOT CAPTURE
Score does not reflect: farming practice, organic certification,
brand-specific milk sourcing, packaging, price, taste preference.
```

**Most likely outcome:** Equivalent finding. Two mainstream 3% dairy milks from major Israeli processors will have closely similar nutritional profiles. Score delta will likely fall in the noise range. This is a valid and expected comparison outcome.

---

**Scenario B — Plant-Based Within-Pool (Pool D, Lens 1)**

Products: Oat milk vs. Almond milk

**Step 1 — Eligibility:**  
Both are plant-based milk alternatives serving the same consumer decision within Pool D. ELIGIBLE.

**Step 2 — Purpose divergence:**  
Within Pool D, both products serve the same primary purpose (dairy-free milk alternative). No purpose divergence statement required for within-pool comparison.

**Step 3 — Lens assignment:**  
Lens 1 within Pool D. Both products are in the same restriction-driven pool; within-pool comparison uses Lens 1.

**Step 4 — Score delta assessment:**  
Oat milk: ~60 kcal/100ml, 1.5g protein, 6.5g carbs, 1.5g fat.  
Almond milk: ~25 kcal/100ml, 0.4g protein, 2g carbs, 1.5g fat.  
Protein gap: ~1.1g/100ml — not large in absolute terms, but relative to the pool baseline of 0.4–3.3g/100ml, this is a significant within-pool delta.  
Assumed score delta: moderate to material (7–20 points), with protein and caloric density as primary drivers.  
Ranking: Oat milk ranks above almond milk within Pool D on protein and caloric substance metrics.

**Step 5 — Distortion disclosures:**  
DISTORTION-004 endemic: Pool D category note displayed for both.  
DISTORTION-009: Both products carry functional additives (calcium carbonate, stabilizers). Product-level note: "Additives in this product serve stability and fortification functions."

**Step 6 — Explanation construction:**

```
LAYER 1 — PURPOSE STATEMENT
Not required — both are plant-based milk alternatives.

LAYER 2 — SCORE DIFFERENCE
Oat milk: [score]/[grade]
Almond milk: [score]/[grade]
Delta: [X points] — [Moderate / Material]

LAYER 3 — SPECIFIC DRIVERS
  · Protein: Oat milk provides [X]g protein / 100ml.
    Almond milk provides [X]g protein / 100ml — approximately
    [Y]% of oat milk's protein content.
  · Caloric substance: Oat milk provides [X] kcal / 100ml.
    Almond milk provides [X] kcal / 100ml — approximately
    [Y]% of oat milk's caloric density.

LAYER 4 — TRADEOFFS
  Almond milk's lower calorie content is not primarily
  a nutritional advantage — it reflects lower nutritional
  contribution per 100ml, not a designed caloric reduction.

LAYER 5 — KNOWN LIMITATIONS
  · Both products are fortified with calcium and vitamins B12 and D.
    These micronutrients are not captured in the score (see Pool D
    category note). Both products may deliver similar micronutrient
    profiles through fortification despite score differences.
  · Functional additives (stabilizers, emulsifiers) serve technical
    functions in both products. Their contribution to NOVA
    classification reflects processing, not cosmetic engineering.

LAYER 6 — WHAT THIS SCORE DOES NOT CAPTURE
Score does not reflect: taste preference, environmental footprint,
water use in production, organic certification, price.
```

---

**Scenario C — Cross-Pool (Dairy vs. Plant-Based, Lens 1 / Lens 3 cross-pool)**

Products: Tnuva 3% dairy milk vs. Oatly oat milk

**Step 1 — Eligibility:**  
Both products serve the "milk with coffee / cereal / drinking" consumer decision for many consumers. Cross-pool comparison is permitted under Article II, Rule 4 (cross-category comparisons require explicit purpose alignment disclosure). ELIGIBLE with disclosure.

**Step 2 — Purpose divergence:**  
Partial divergence. Non-vegan, non-intolerant consumers could choose either product. Vegan/intolerant consumers cannot choose dairy. This is a Lens 1 (general) vs. Lens 3 (restriction) cross-lens comparison for a subset of consumers.

**Constitution v1, Article III, Section 3.4:** Purpose divergence statement required before score (Condition 3 — one product is restriction-compliant for a consumer group that the other is not).

**Step 3 — Lens assignment:**  
Lens 1 for the general consumer frame. Lens 3 disclosure added for restricted consumers.

**Lens disclosure (required before scores):**

```
Tnuva 3% is dairy milk. Oatly is a plant-based oat milk alternative.
Consumers who can consume dairy may choose either product. Consumers
with dairy restrictions (lactose intolerance, vegan dietary practice)
would not consider dairy milk as an option. The comparison that follows
applies to consumers who could reasonably choose either product.
For consumers with dairy restrictions, plant-based alternatives
are evaluated separately within a plant-based comparison pool.
```

**Step 4 — Score delta assessment:**  
Expected: Material to decisive delta. Dairy 3% milk has strong protein (~3.2g/100ml), NOVA 1, no additives. Oat milk has lower protein (~1.5g/100ml), NOVA 3 (additives present), but significant fortification (invisible to scoring). Score delta likely 15–30 points in favor of dairy milk.

**Step 5 — Distortion disclosures:**  
Both: DISTORTION-007 applies to dairy (lactose); DISTORTION-004 applies to oat milk (fortification). Both category notes displayed. These are distinct disclosures for distinct products in this cross-pool comparison — not consolidated.

**Step 6 — Score ranking:**  
Dairy milk ranks above oat milk on current BSIP2 architecture. The gap is material and reflects a genuine nutritional architecture difference: dairy's protein is whole-food, NOVA 1, no additives. Oat milk's protein is lower and requires additive processing.

**Critical Anti-Immunity check:** The disclosure that oat milk serves vegan consumers does not improve its score. The score reflects the nutritional architecture. The lens disclosure contextualizes the comparison; it does not change the score. Constitution v1 Anti-Immunity Rule confirmed active.

---

**Scenario D — Protein Milk (Pool C Provisional, D6 in Effect)**

Products: Tene Protein milk vs. Tnuva 3% standard

**Step 1 — Eligibility:** Both are dairy milk products. Cross-pool comparison between Pool A and Pool C. ELIGIBLE.

**Step 2 — Lens assignment:** Pool C is provisionally under Lens 1 (D6 block prevents Lens 2 assignment). Comparison proceeds as Lens 1.

**Step 3 — Protein claim handling:**  
Protein milk carries protein claim. Section 5.2.1 general threshold (≥8g/100ml) does not match the Israeli protein milk landscape. D6 block active. Marketing Divergence Finding for the protein claim cannot be issued.

**Step 4 — Score comparison:**  
Protein milk at ~5.5g/100ml vs. standard at 3.2g/100ml. The protein dimension will score higher for protein milk. Score delta: likely moderate (7–14 points). Protein milk ranks above standard milk.

**Step 5 — Explanation construction:**  
Critical: the explanation cannot invoke Lens 2 (blocked), cannot issue a protein claim Marketing Divergence Finding (blocked), and cannot assign functional credit for the protein elevation without a calibrated threshold.

```
LAYER 2 — SCORE DIFFERENCE
Protein milk: [score]/[grade]
Standard milk 3%: [score]/[grade]
Delta: [X points] — Moderate

LAYER 3 — SPECIFIC DRIVERS
  · Protein: Protein milk provides approximately [X]g protein / 100ml —
    [Y]% more than standard dairy milk at the same fat percentage.

LAYER 4 — TRADEOFFS
  · Protein milk carries a higher price point and may contain additional
    ingredients to achieve protein concentration. The ingredient profile
    should be reviewed in the product detail.

LAYER 5 — KNOWN LIMITATIONS
  · Bari has not yet calibrated the threshold at which elevated milk
    protein constitutes a meaningful functional advantage. The score
    reflects the observed protein difference. Whether this difference
    represents a functional protein delivery product is a threshold
    question Bari has not yet resolved for the milk category.
  · DISTORTION-007 applies to both products (lactose).

LAYER 6 — WHAT THIS SCORE DOES NOT CAPTURE
Score does not reflect: whether the protein source is whole-food or
added isolate, price premium, or individual protein requirements.
```

This scenario demonstrates the D6 block working correctly: the comparison proceeds, the score difference is reported honestly, and the governance limitation is disclosed without suppressing information.

---

## 7. Production Readiness

### 7.1 Verdict: B — Yes with Conditions

**If Cursor delivered all BSIP0/1/2 data tomorrow, could the category launch?**

**Governance:** READY  
All structural governance questions are resolved by the amended Constitution v1 and Guardrails v2. Pool definitions are complete. Endemic distortions are identified and disclosure texts are drafted. Lens assignments and cross-pool rules are specified. Developmental products are correctly excluded.

**Conditions (must be resolved before launch approval):**

| Condition | Blocker? | Resolution path |
|---|---|---|
| 1. Protein milk threshold (milk-specific) not in Section 5.2.1 | Soft blocker — Pool C functions under Lens 1; Findings blocked for protein claims | CE Controller 1 to propose threshold (≥5.5g/100ml proposed); external validation required; 1–2 sessions |
| 2. "Light" milk threshold not in Section 5.2.1 | Soft blocker — Findings blocked for light claims | CE Controller 1 to research Israeli/EU regulatory reference; document in Section 5.2.1 |
| 3. "Calcium rich" threshold not in Section 5.2.1 | Soft blocker — Findings blocked for calcium claims | CE Controller 1 to document (EU 15% NRV per 100ml is the candidate) |
| 4. Pool D category note final approval | Pre-launch sign-off required | Draft text written in Section 3.3; CE Controller 1 approval |
| 5. Pool A category note final approval | Pre-launch sign-off required | Draft text written in Section 3.3; CE Controller 1 approval |
| 6. Growing-up formula corpus scoped | Data pipeline — verify Section 2.8 applies before BSIP0 scrape filters | Done at BSIP0 stage |
| 7. Serving size normalization protocol | Not blocking launch but affects per-serving Marketing Divergence Finding accuracy | Document normalization basis before Findings published (not before launch) |
| 8. 27-criterion checklist completed | Mandatory | All 27 criteria must pass; cannot waive any B/C/A criteria |

**What can launch immediately upon data delivery:** Pools A, B, and D within-pool comparisons; Lens 3 cross-pool disclosures; Pool D endemic distortion disclosure; cross-pool dairy-vs-plant-based comparisons with lens disclosure; all developmental product exclusions. The majority of the category's comparison value is available.

**What requires threshold documentation first:** Pool C full operation, Marketing Divergence Findings for protein/light/calcium claims, Lens 2 formal designation.

---

## 8. Framework Retrospective

Only genuine failures reported.

### 8.1 Genuine Friction 1 — Section 2.9 Proxy Indicators Are Granola-Calibrated

**Observation:** The Section 2.9 architectural divergence rule identifies sub-categories using three proxy indicators: NOVA, added sugar ≥10g, fat ≥10g. Plant-based milk's divergence from dairy milk is qualitative — different biological origin, different protein source, different food matrix — but does not necessarily meet the sugar or fat proxy thresholds. Unsweetened oat milk (sugar ~6g/100ml, fat ~1.5g/100ml) meets only the NOVA proxy. One proxy alone does not trigger Section 2.9.

**Consequence:** Plant-based milk pool separation was handled by the lens framework (Article II, Sections 2.1 and 2.7; Guardrails v2 Lens 3) rather than by Section 2.9. The correct result was reached, but via a different governance path than expected.

**Assessment:** Section 2.9 worked correctly for Pool B (chocolate milk — two proxies confirmed: NOVA and added sugar). It did not work for Pool D because the proxies are calibrated for the granola pattern (excess sugar + fat). The statistical version of the rule (1.5 standard deviations, applicable when BSIP data exists) would correctly identify plant-based milk via protein divergence — but the pre-BSIP proxies fail.

**Severity:** Low. The governance produced the correct outcome through an alternative mechanism. No consumer trust risk.

**Required action:** None to the governance documents. Note in the milk category record that Section 2.9 pool separation for plant-based milk was established via the lens framework rather than proxy indicators. When BSIP2 data exists, the statistical divergence rule confirms the pool separation independently.

---

### 8.2 Genuine Friction 2 — Two Endemic Distortions Create a Presentation Problem Section 6.4 Does Not Resolve

**Observation:** The milk shelf has two endemic distortions in two distinct pools — DISTORTION-007 in Pool A (dairy) and DISTORTION-004 in Pool D (plant-based). Section 6.4 says "if more than one distortion reaches endemic prevalence, consolidate into a single category note." But these distortions apply to different products. Consolidating them into a single note would be misleading: a consumer viewing a dairy milk product would see a note about plant-based fortification, and vice versa.

**Consequence:** The consolidation instruction in Section 6.4 was written for the case where one category has multiple endemic distortions affecting the same products. Milk has two endemic distortions affecting distinct product pools. The correct action (separate notes per pool) contradicts the Section 6.4 consolidation instruction.

**Assessment:** Genuine governance ambiguity. The resolution (two separate pool-specific notes) is correct, but it violates the literal consolidation instruction.

**Required action:** Section 6.4 requires a clarification: "Consolidation applies when multiple endemic distortions affect the same products. When endemic distortions affect distinct sub-pools, pool-specific notes are preferred over consolidation." This is a one-sentence amendment — not a new framework.

**Priority:** Low. The correct action is clear; the governance text just needs a clarifying sentence.

---

### 8.3 Genuine Friction 3 — Section 5.2.1 General Beverage Threshold Breaks for Milk

**Observation:** The general "high protein" beverage threshold (≥8g/100ml) was designed for protein drinks, shakes, and functional beverages where 8g/100ml is a plausible functional threshold. Standard dairy milk is 3.2g/100ml. Israeli protein milk is 5–6g/100ml. Applying ≥8g/100ml to protein milk claims would produce a finding that all Israeli protein milk products fail to support their protein claims — which may be correct for some products but is almost certainly wrong for all.

**Consequence:** The D6 block correctly prevented the incorrect threshold from generating false Marketing Divergence Findings. The governance worked as designed — the D6 criterion was the safeguard. But the safeguard should not be the first line of defense for every new category. Section 5.2.1 needs a category-specific row for milk protein claims before the next launch cycle.

**Assessment:** The framework handled this correctly, but the calibration gap in Section 5.2.1 is a genuine maintenance debt. The general beverage threshold was not wrong — it was applied to a context for which it was not calibrated.

**Required action:** CE Controller 1 to propose and ratify a milk-specific protein threshold (proposed: ≥5.5g/100ml — approximately 70% above the dairy protein baseline, which places protein milk in a meaningfully elevated tier without requiring industrial protein addition at the level of a protein shake). External reference: this should align with Israeli consumer expectation of what "protein milk" implies, which requires market research input. Until ratified, D6 block remains.

---

### 8.4 Amendments That Were Not Necessary (Confirmed Unnecessary: None)

All four amendments (Sections 2.8, 2.9, 6.4, 5.2.1) had direct applications in milk:
- Section 2.8: Growing-up formulas triggered this immediately; correct exclusion applied
- Section 2.9: Applied to Pool B (chocolate milk sub-pool); two proxies confirmed
- Section 6.4: Activated for both Pool A and Pool D; both disclosure texts drafted
- Section 5.2.1: Correctly identified the calibration gap for protein milk via D6 block; prevented incorrect Findings

No amendment proved unnecessary. All four generated governance value.

---

### 8.5 Unresolved Gap

**Gap: Serving size normalization for per-serving Marketing Divergence Findings**

Identified in the keto milk Finding scenario (Section 5.3, Scenario 3). A product may pass a per-100ml threshold but fail a per-serving threshold at standard consumption quantities. The governance specifies thresholds in per-100g/ml terms (consistent with Israeli nutritional labeling law). But consumers consume products in servings, not in 100ml units.

This gap is not new — it was documented as Gap 5 (moderate) in the cereals stress test. It surfaces again in milk, where standard serving sizes (200–250ml glass) create threshold discrepancies for borderline products.

**Assessment:** Moderate risk. For decisive claims (a product clearly exceeds or clearly fails the threshold), serving size normalization doesn't change the finding. For borderline products, it matters.

**Required action:** Document the normalization basis (per-100ml threshold + standard serving size note, OR per-serving threshold with stated serving size) before any borderline Marketing Divergence Findings are published. This is a documentation decision, not a governance framework change.

---

## 9. Recommendations

**Recommendation 1 — Document three milk-specific claim thresholds in Section 5.2.1 before category launch.**  
Priority: high. Three claim types (protein milk, light milk, calcium rich) are currently D6-blocked. The protein milk threshold is the most commercially significant — Pool C cannot fully function without it. Proposed protein milk threshold: ≥5.5g/100ml (to be validated). For "light" milk: ≥25% fat reduction from the reference product at the same base fat percentage. For "calcium rich": ≥120mg/100ml (15% NRV / 100ml, per EU Regulation 1924/2006 as the available external reference). These three additions to Section 5.2.1 unblock full Marketing Divergence Finding coverage for the milk category.

**Recommendation 2 — Add a one-sentence clarification to Section 6.4 for multi-pool endemic distortion scenarios.**  
The current consolidation instruction is ambiguous when endemic distortions affect distinct pools rather than the same products. Add: "Consolidation applies when multiple endemic distortions affect the same products. When endemic distortions apply to distinct sub-pools, pool-specific notes are preferred over consolidation." This closes the only genuine governance ambiguity that emerged from the simulation.

**Recommendation 3 — Document the serving size normalization protocol as a pre-launch requirement for all Marketing Divergence Findings on borderline products.**  
Add to the category launch record (not to the governance documents): which serving size convention is used when a product is within 20% of a per-100ml threshold. The governance already specifies per-100g/ml thresholds; the normalization note explains the serving size context to the consumer. This is an explanation governance decision, not a scoring governance decision.

**Recommendation 4 — Begin milk BSIP0 scrape scope definition.**  
The pool structure, exclusion criteria, developmental definitions, and corpus filter logic are now fully specified. BSIP0 can begin. The scrape scope is: all products in the refrigerated dairy aisle and UHT shelf under the milk/milk-alternative category at the target retailers, excluding infant formula (0–12 months), heavy cream, sour cream, condensed milk, drinkable yogurt, and protein shakes. Growing-up formulas are included in the scrape but segregated in a developmental pool at BSIP1 enrichment stage.

---

*Bari Category Production Simulation — חלב (Milk) v1*  
*CE Controller 1 — Chief Nutrition, Scoring & Content Architect*  
*2026-05-29*  
*Governed by: Bari Governance v1, Comparison Governance Constitution v1 (as amended), Consumer Use-Case & Purpose Guardrails v2 (as amended)*  
*Preconditions: Cereals Gap Resolution Report v1 amendments applied*  
*Next action: Document three milk-specific claim thresholds; apply Section 6.4 clarification; begin BSIP0 scrape scope.*
