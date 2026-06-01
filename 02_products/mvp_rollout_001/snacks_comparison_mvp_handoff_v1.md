# Snacks Comparison — MVP Handoff v1
**Date:** 2026-05-30
**Route:** `/hashvaot/snacks`
**Status:** LIVE ✅ — Needs scoring recalibration + re-run

---

## A. Category Status

| Dimension | Status |
|---|---|
| Data | ✓ 18 products in `src/data/comparisons/snacks_frontend_v2.json` |
| Scoring | 🟡 BSIP2-derived; recalibration required |
| Explanations | ✓ All 18 products have positiveSignals, limitingFactors, bottomLine, comparisonContext |
| Images | ✓ Yochananof CDN URLs |
| Component | ✓ `SnacksComparisonDesktopPage` — milk-aligned format |
| Route | ✓ `/hashvaot/snacks` |
| MVP readiness | ✅ LIVE — rescore before promotion |

---

## B. Data Structure

**File:** `src/data/comparisons/snacks_frontend_v2.json`  
**Schema:** BariProductVM (canonical)  
**Loaded via:** `src/lib/comparisons/snacks-comparison-page-data.ts`  
**Products:** 18

**Score distribution (current):**
- B (≥65): 1 product (snk-001: 70)
- C (50–64): 7 products
- D (35–49): 5 products
- E (<35): 5 products

**Known data gaps:**
- `nutrition` fields are mostly null — incomplete scrape
- `ingredients` text present on ~60% of products
- Both nulls are acceptable for MVP

**Internal cluster field:** `_internal_cluster` (stripped before rendering, not BariProductVM)

---

## C. Scoring Guidance (Post-Recalibration)

Apply recalibration changes R-01, R-02, R-03 then re-run BSIP2 on snacks corpus.

**Expected score changes:**
- snk-001 (תמרים/שקדים, NOVA2, 70/B): +0–2 pts → stays B
- snk-015 (תמרים/בוטנים, NOVA2, 63/C): +0–2 pts → stays C (already had RC-01 relief)
- snk-002 (תמרים ציפוי שוקולד, 57/C): +0–3 pts (no fermentation, no whole grain)
- snk-011 (קרנץ'י שיבולת שועל, 44/D): +1–3 pts from R-03 (high fiber)
- snk-007 (פנטהאוס/אנרגיה, 28/E): no change (NOVA4 territory)
- snk-013 (בר קלוריות חרוב, 17/E): no change

**What should NOT change:**
- Relative ranking within the corpus
- Grade E products — they are correctly E

**Grades likely to change:**
- Products in 62–67 range may cross B threshold (65) post-R-03

**Run the existing batch runner** after engine changes. Update `snacks_frontend_v2.json` scores, grades, and any `bottomLine`/`insightLine` references that quote the old score.

---

## D. Explanation Guidance

All 18 explanations were rebuilt in Explanation Engine v2 (2026-05-29). They use real BSIP2 trace data.

**What explanations must say:**
- Observable product attributes (ingredient count, fiber, protein, processing markers)
- Specific numbers from the trace: "3 מרכיבים בלבד", "10.4g סיבים"
- Comparative positioning ("הבסיס הנקי ביותר בקטגוריה")

**Phrases to avoid (enforced in v2):**
- "NOVA", "NOVA3", "NOVA4"
- "ממד", "גורם הגנה", "BSIP"
- Generic non-specific lines: "מוצר לא בריא" without evidence
- "חזק/בינוני/חלש" label language

**After rescore:** Update any `bottomLine` text that contains the old score numeric (e.g., "29/E:") to new score. Grep for `/[0-9]+\/(A|B|C|D|E)/` in snacks_frontend_v2.json.

---

## E. Methodology Disclosure

Current methodology lines in `src/lib/blog/snack-analysis-content.ts`. Use as-is.

Verify these lines are present:
1. Scope note: "ניתוח מדף יוחננוף בלבד — לא סקר שוק ישראלי"
2. Signal explanation (without NOVA)
3. Confidence caveat for products with partial data

---

## F. Post-Rescore Checklist

After BSIP2 re-run with R-01/R-02/R-03:

- [ ] All 18 products have updated scores in `snacks_frontend_v2.json`
- [ ] All grades recalculated (score_to_grade function, threshold ≥80=A, ≥65=B, ≥50=C, ≥35=D)
- [ ] All `insightLine` fields that reference old scores updated
- [ ] `bottomLine` texts with score references updated
- [ ] `comparisonContext` texts with relative score differences updated (e.g., "X נקודות מתחת ל-Y")
- [ ] Product order re-sorted by new score (descending)
- [ ] `_meta.generated` timestamp updated
- [ ] `snack-page-data.ts` score values synced

---

## G. Launch Readiness

**Status: ✅ LIVE — rescore before promotion**

The component is live and correct. The only required work is running the recalibration and updating the JSON.

Estimated time: 2–3 hours (engine changes + re-run + JSON update + text sync).
