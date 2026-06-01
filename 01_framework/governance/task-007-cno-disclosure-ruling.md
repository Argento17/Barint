TASK-007
Status: Partial
Owner: Chief Nutrition Officer

---

# Consumer Disclosure Ruling — v1

**Date:** 2026-05-30  
**Scope reviewed:** Gap 05 (Endemic Distortion Protocol), Gap 07 (Purpose Divergence Disclosure), Gap 09 (Date Sugar Halo), Distortion Registry (DIST-001 through DIST-010), active live categories  
**Basis:** Current live state only. No prospective categories assessed.  

---

## Active Live Categories at Time of Review

| Category | Route | Scoring basis | Status |
|---|---|---|---|
| מעדנים | /hashvaot/maadanim | BSIP2 | Live |
| לחם | /hashvaot/bread | BSIP2 | Live |
| חטיפים | /hashvaot/snacks | BSIP2 (partial — Layers 2–3 inactive) | Live, unrescore pending |
| יוגורטים | /hashvaot/yogurts | BSIP2 | Live (limited) |
| חלב | /hashvaot/milk-comparison | Hand-curated | Live (legacy) |

---

## Gap 05 — Endemic Distortion Disclosure

### Distortion-by-distortion assessment against live categories

**DIST-001 — Dairy Fiber Penalty**

- יוגורטים: scored through BSIP2 formula; dairy fiber penalty is active. Disclosure required before this category is promoted externally.
- חלב: hand-curated scores — BSIP2 formula may not have been applied directly. **Pending confirmation: QA must confirm whether milk scores were derived from or informed by BSIP2 output.** If yes, the fiber penalty is embedded and disclosure is required. If no, the distortion does not apply to milk scores.
- מעדנים: dairy dessert products scored through BSIP2. Affects dairy-dominant products (cream puddings, milky variants). Disclosure deferred to coordinated dairy disclosure package — but this category requires it before external promotion.

**DIST-002 — Date Sugar Halo**

- חטיפים: active in the corpus. Date-dominant bars are in the snack category and score differently from refined-sugar-equivalent products. Disclosure required. This is Gap 09. Covered below.

**DIST-005 — Inactive Scoring Layers**

- חטיפים: all 18 products scored without nutritional data. Layers 2 and 3 inactive. Disclosure required. This is Gap 08. Covered below.

**DIST-007 — Structural Emptiness**

- מעדנים: the corpus likely includes diet or low-fat dairy dessert variants (e.g., פודינג דיאט, מוצרי גבינה דל-שומן). These products may score in the 60s because nothing fires against them, not because they deliver nutritional value. **Pending confirmation: QA or Research Analyst must identify how many products in the מעדנים corpus are diet/low-fat variants. If the fraction is ≥ 15%, disclosure is required.** If it is below that, the distortion is not endemic enough to warrant a category-level note.

**Fortification**

- No live category is currently subject to a BSIP2 fortification distortion. Fortification scoring (BEV-028) is deferred and not in the active engine. No disclosure required today.

### Gap 05 disclosure ruling — today

| Distortion | Category | Disclosure required today? | Trigger condition |
|---|---|---|---|
| DIST-001 (Dairy fiber) | יוגורטים | Yes | Category is live and scored through BSIP2 |
| DIST-001 (Dairy fiber) | חלב | Pending | Requires QA confirmation on scoring basis |
| DIST-001 (Dairy fiber) | מעדנים | Deferred | Before external promotion |
| DIST-002 (Date sugar) | חטיפים | Yes | Covered in Gap 09 below |
| DIST-005 (Inactive layers) | חטיפים | Yes | Covered in Gap 08 / this document below |
| DIST-007 (Structural emptiness) | מעדנים | Pending | Requires corpus prevalence check (≥15% diet variants) |

---

## Gap 07 — Purpose Divergence Disclosure

### Which live categories have confirmed purpose divergence?

**מעדנים — Confirmed divergence**

The מעדנים corpus contains at least two distinct product purposes:
1. Traditional dairy desserts — milky, cream puddings, chocolate mousse (dessert context, occasional consumption)
2. High-protein dairy products — protein puddings, quark, high-protein yogurt variants (functional nutrition context)

These products are scored on the same thresholds. A direct score comparison between a milky-style chocolate pudding and a high-protein protein pudding produces a number that implies they are alternatives. They are not always alternatives. A consumer choosing between them for dessert is making a different decision than a consumer choosing between them for post-workout protein intake.

**Disclosure required: Yes**

**חלב — Partial divergence**

The milk category includes whole dairy, plant milks, and engineered protein shakes. The CE Advisory confirmed this divergence and corrected three consumer misconceptions. Review whether the current milk prologue already addresses this — if so, no additional disclosure is needed.

**Disclosure required: Conditional on current prologue content. Review before next update to milk page.**

**חטיפים — Present but secondary**

Whole-food snack bars (dates, nuts) and protein bars serve different purposes. The purpose divergence is real but secondary to the more urgent DIST-005 and DIST-002 disclosures. Add a brief note but do not make it the primary disclosure.

**Disclosure required: Yes, brief note alongside Gap 08/09 methodology update**

---

## Gap 09 — Date Sugar Halo Disclosure

### Assessment

The position is scientifically defensible for certain product forms. Products containing whole dates or date paste carry their sugars in a food matrix context that differs from refined sugar syrup. The scoring reflects this structural distinction.

The disclosure gap: this position is currently embedded in the scoring logic without being visible to consumers. A consumer who sees a date bar scoring well while a cane-sugar bar scores lower has no way to understand why.

**Disclosure required: Yes. One methodology sentence in the snacks category footer.**

---

## Disclosure Wording — Complete Drafts

---

### DISCLOSURE-01
**For:** חטיפים (snacks)  
**Addresses:** DIST-005 — Inactive Scoring Layers  
**Placement:** Methodology footer, first sentence  
**Mandatory:** Yes  

**Hebrew:**
ציוני קטגוריה זו מבוססים על מבנה המוצר ורמת העיבוד. נתוני תזונה כגון חלבון, סוכר וקלוריות לא היו זמינים בגרסת ניתוח זו ואינם משתקפים בציונים המוצגים.

**English reference:**
Scores in this category are based on product structure and processing level. Nutritional data — including protein, sugar, and calories — was not available at the time of this analysis and is not reflected in the scores shown.

---

### DISCLOSURE-02
**For:** חטיפים (snacks)  
**Addresses:** DIST-002 — Date Sugar Halo  
**Placement:** Methodology footer, following DISCLOSURE-01  
**Mandatory:** Yes  

**Hebrew:**
מוצרים הממותקים בתמרים שלמים או ממרח תמרים מוערכים לפי מקור הסוכר ומבנה הרכיבים, לא רק לפי כמות הסוכר הכוללת. מוצר כזה עשוי לקבל ציון שונה ממוצר עם כמות סוכר זהה ממקורות מזוקקים.

**English reference:**
Products sweetened with whole dates or date paste are assessed by the origin and structural context of their sugar, not total sugar quantity alone. Such a product may score differently from one with equivalent total sugar from refined sources.

---

### DISCLOSURE-03
**For:** מעדנים  
**Addresses:** Gap 07 — Purpose Divergence (protein puddings vs. traditional desserts)  
**Placement:** Prologue — final sentence  
**Mandatory:** Yes  

**Hebrew:**
קטגוריה זו כוללת הן קינוחי חלב מסורתיים והן מוצרים עתירי חלבון. השוואת ציונים ישירה משמעותית ביותר בין מוצרים בעלי שימוש דומה.

**English reference:**
This category includes both traditional dairy desserts and high-protein dairy products. Direct score comparisons are most meaningful between products with a similar intended use.

---

### DISCLOSURE-04
**For:** יוגורטים  
**Addresses:** DIST-001 — Dairy Fiber Penalty  
**Placement:** Methodology footer  
**Mandatory:** Yes — required before this category is promoted externally  

**Hebrew:**
ציוני קטגוריה זו אינם מביאים בחשבון היעדר סיבים תזונתיים, שהוא מאפיין ביולוגי של מוצרי חלב ואינו מייצג חולשה תזונתית. ניתן שציוני מוצרי חלב יהיו נמוכים במעט ממה שמבנהם מצדיק בהשוואה לקטגוריות אחרות.

**English reference:**
Scores in this category do not penalise the absence of dietary fiber, which is a biological property of dairy products and not a nutritional weakness. Dairy product scores may be modestly lower than their composition alone warrants when compared across categories.

---

### DISCLOSURE-05
**For:** חטיפים (snacks) — purpose divergence note  
**Addresses:** Gap 07 — partial, for snacks  
**Placement:** Methodology footer — brief addition to DISCLOSURE-01 and DISCLOSURE-02  
**Mandatory:** Optional (minimal consumer trust risk in this category for purpose divergence)  

**Hebrew:**
הקטגוריה כוללת גם חטיפים טבעיים וגם חטיפי חלבון. השוואה בין סוגי מוצרים שונים מומלצת עבור מטרה תזונתית דומה.

**English reference:**
This category includes both whole-food snacks and protein-oriented bars. Comparisons are most useful between products with a similar dietary purpose.

---

## Placement Summary

| Disclosure | Category | Location | Component | Mandatory |
|---|---|---|---|---|
| DISCLOSURE-01 | חטיפים | Methodology footer — sentence 1 | `snacksMethodologyLines` | **Yes** |
| DISCLOSURE-02 | חטיפים | Methodology footer — sentence 2 | `snacksMethodologyLines` | **Yes** |
| DISCLOSURE-03 | מעדנים | Prologue — final sentence | `maadanimPrologueSentences` | **Yes** |
| DISCLOSURE-04 | יוגורטים | Methodology footer | `yogurtsMethodologyLines` | **Yes (before external promotion)** |
| DISCLOSURE-05 | חטיפים | Methodology footer — sentence 3 | `snacksMethodologyLines` | Optional |

All five disclosures are plain-text additions to existing arrays in the respective `{category}-page-data.ts` files. No new UI components are required. No design decisions are required. No scoring changes are required.

---

## Implementation Notes

**DISCLOSURE-01 and DISCLOSURE-02 (snacks, methodology):**
These must be batched together. DISCLOSURE-02 without DISCLOSURE-01 would confuse consumers — the date sugar note would float without context about why scoring is structural-only. Ship both in one update to `snacksMethodologyLines`.

**DISCLOSURE-03 (maadanim, prologue):**
The prologue currently ends with a shelf observation. DISCLOSURE-03 should be appended as a final sentence, not replace existing copy. The sentence sets category scope; it does not explain the score. Keep it factual and brief — the current draft meets that standard.

**DISCLOSURE-04 (yogurts, methodology):**
Not urgent today since yogurts has not been externally promoted. Stage this text now; ship it with the yogurts promotion window. If the yogurts page is being updated for any other reason before promotion, include it then.

**DISCLOSURE-05 (snacks, optional):**
Only add if the date sugar disclosure (DISCLOSURE-02) is felt to be insufficient context for consumers encountering both whole-food bars and protein bars in the same list. If the methodology already calls the category "חטיפים", consumers have some expectation of category diversity. Make this judgment at the time of the snacks update.

---

## Boundary Notes

**What these disclosures do not cover:**

- They do not explain the scoring formula, dimension weights, or cap logic. None of those appear in consumer copy.
- They do not contain the words NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, or dimension.
- They do not say scores are wrong or unreliable. They contextualise specific analytical choices.
- They do not recommend or advise. They describe.

**What is deferred:**

- DIST-007 (structural emptiness in מעדנים): Pending corpus prevalence check. If ≥15% of מעדנים products are diet/low-fat variants, a disclosure should be drafted and added to the מעדנים methodology footer.
- DIST-001 (dairy fiber, milk-comparison): Pending QA confirmation that milk-comparison scores were not BSIP2-derived. If confirmed, no disclosure needed for milk.

---

## Open Issues

**OI-001 — Yogurts promotion timing is not set.**
DISCLOSURE-04 is mandatory before yogurts is promoted externally. The current "not promoted" status is not a stable condition — it needs a named target date or milestone. Without one, the disclosure will be missed. Owner: Head of Product to confirm yogurts promotion timeline so DISCLOSURE-04 can be staged correctly.

**OI-002 — מעדנים corpus diet-variant prevalence is unmeasured.**
The DIST-007 structural emptiness disclosure is pending a count of diet/low-fat מעדנים products in the corpus. If ≥15% of the category are products that score well primarily by being nutritionally absent, a disclosure is required. Owner: Research Analyst or QA & Audit Lead to run this count before the next מעדנים content update.

**OI-003 — Milk-comparison scoring basis requires confirmation.**
The DIST-001 dairy fiber disclosure for milk-comparison depends on whether BSIP2 informed the hand-curated scores. If scores were set without the BSIP2 formula, the fiber distortion does not apply. Owner: QA & Audit Lead to confirm and file the answer in the governance record.

**OI-004 — Gap 07 for חלב requires prologue review.**
The milk-comparison prologue may already address the purpose divergence between dairy milks, plant milks, and protein shakes (three separate consumer misconceptions were corrected in the CE Advisory). Before adding a purpose divergence note to the milk page, review the existing prologue copy to determine whether it already provides sufficient context. Owner: Chief Nutrition Officer at next milk page review.

---

## Recommended Next Step

**Immediate (this sprint):**

The Frontend Architect should add DISCLOSURE-01 and DISCLOSURE-02 to `snacksMethodologyLines` in `snacks-comparison-page-data.ts` as part of the same deployment as Gap 08 (snacks layer disclosure). These are the same file, the same component, and the same deployment window — batching them costs nothing.

**Before next מעדנים content update:**

Add DISCLOSURE-03 as the final sentence of `maadanimPrologueSentences` in `maadanim-page-data.ts`. This is a one-line change. No design decision is required.

**Before yogurts is promoted:**

Stage DISCLOSURE-04 in `yogurtsMethodologyLines`. Do not ship it without setting a promotion date first — it should be reviewed at that point to confirm accuracy against the then-current corpus.

**Resolve OI-002 before next מעדנים scoring cycle:**

Run the diet-variant count in the מעדנים corpus. If ≥15% are structural-emptiness candidates, draft and add a methodology line at that time. Do not draft speculative disclosure copy before the count confirms it is needed.

---

*TASK-007 — Chief Nutrition Officer*  
*2026-05-30*
