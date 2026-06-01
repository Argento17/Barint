# Milk Comparison — MVP Handoff v1
**Date:** 2026-05-30
**Route:** `/hashvaot/milk-comparison`
**Status:** LIVE ✅ — No implementation work required for MVP

---

## A. Category Status

| Dimension | Status |
|---|---|
| Data | ✓ 18 products in `src/data/milk-comparison.json` |
| Scoring | ✓ Hand-curated, range 70–90, A/B grades |
| Explanations | ✓ `consumerExplanation.takeaway`, `whatToKnow`, `raisesScore`, `lowersScore`, `relativeToPeers` |
| Images | ✓ Yochananof CDN URLs, mostly loading |
| Component | ✓ `MilkComparisonPage` — reference implementation |
| Route | ✓ `/hashvaot/milk-comparison` |
| MVP readiness | ✅ LIVE |

---

## B. Data Structure

Milk uses a **custom schema** (NOT BariProductVM). This is the only category with this structure.

**File:** `src/data/milk-comparison.json`  
**Loaded via:** `src/lib/comparisons/milk-page-data.ts`  
**Type:** `MilkComparisonProduct` (see `milk-types.ts`)

Key fields per product:
- `barcode`, `shortName`, `displayTitle`, `brandLine`
- `productType`, `productTypeLabel`
- `image_url`, `score`, `grade`, `grade_label`
- `proteinPer100ml`, `sugarPer100ml`, `additivesLabel`, `mainIngredient`
- `consumerExplanation`: `{takeaway, whyRated, good[], watchOut[], context}`
- `bariInterpretation`: pillars array with `{key, label, score, strength, interpretation}`

**18 products**: cow's milk (full fat, 1%, 3%), oat milk, soy milk, almond milk, rice milk, lactose-free, etc.

---

## C. Scoring Guidance

**Current scores:** 70–90, A/B range.  
Scoring is hand-curated, not from BSIP2 engine. The scores reflect:
- NOVA1 cow's milk: 85–90/A (clean label, minimal processing)
- Fortified non-dairy: 72–80/B (additives and fortification discount)
- Sweetened/flavored variants: 70–75/B

**Recalibration impact:** None for this sprint. Hand-curated scores are already in the right range.  

**Post-MVP:** If milk is eventually run through BSIP2:
- Apply R-04 (dairy sugar relief) — lactose should not trigger added-sugar guardrails
- Apply R-02 (fermentation bonus) — fermented milks (kefir, etc.) would gain +6

---

## D. Explanation Guidance

Milk uses `consumerExplanation` (not BariExpansionVM). The rendered fields:

**מה חשוב לדעת?** → `whyRated`  
**מה מעלה את הציון?** → `raisesScore` (list)  
**מה מוריד את הציון?** → `lowersScore` (list)  
**בהשוואה למוצרים דומים** → `relativeToPeers`

**What explanations must say:**
- Source: what is the main ingredient (raw milk, plant base, etc.)
- Processing: whether additives are present
- Protein level in context
- Honest tradeoffs (e.g., oat milk has added oils; almond milk is very low protein)

**Phrases to avoid:**
- Any mention of NOVA levels
- Score mechanics or dimension names
- "גליקמי", "BSIP", "מדד", "ממד"

---

## E. Methodology Disclosure

Use this text in methodology footer:

> ההשוואה מבוססת על מוצרי חלב ותחליפי חלב שנבדקו על בסיס מידע גלוי לצרכן. לכל מוצר נבחנו הרכב הרכיבים, הערכים התזונתיים, רמת העיבוד וההקשר הקטגורי. הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה רפואית או תזונתית.

No BSIP2 reference (scores are hand-curated). No "algorithmic" language.

---

## F. Launch Readiness

**Status: ✅ LIVE NOW**

No implementation tasks required for MVP. This is the reference category.

Post-MVP improvements (optional):
- Add 3–4 more products (drinking yogurt, kefir)
- Add more filter options (calcium, lactose-free)
- Consider BSIP2 re-derivation for engine consistency
