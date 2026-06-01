# Excluded Products — Hummus v1 Display

**Task:** TASK-069  
**Date:** 2026-05-31  
**Decision:** Exclude from ranked display for v1

---

## Reason for Exclusion

Six products classified as `hummus_spread` in the Shufersal scrape are single-ingredient, minimally processed (NOVA-1) whole or frozen chickpea products. They are not prepared hummus spreads and are not comparable to the rest of the corpus (prepared spreads, mashed hummus, tahini-based products).

Because NOVA-1 single-ingredient chickpeas score high on the processing_quality and whole_food_integrity dimensions by design, they appeared at the top of the ranked list — scores 85–86, grade A — above all prepared hummus brands. This is a corpus eligibility issue, not a scoring error.

---

## Excluded Products

| Product ID | Name (Hebrew) | Score | Grade | NOVA | Ingredients | Reason |
|-----------|---------------|-------|-------|------|-------------|--------|
| bsip1_7296073733324 | חומוס | 85.5 | A | 1 | 1 (100% גרגרי חומוס) | Single-ingredient raw/dried chickpeas |
| bsip1_7296073733331 | חומוס ענק | 85.5 | A | 1 | 1 | Single-ingredient giant chickpeas |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 85.4 | A | 1 | 1 | Shufersal-brand white large chickpeas |
| bsip1_7296073006015 | חומוס גדול שופרסל | 85.4 | A | 1 | 1 | Shufersal-brand large chickpeas |
| bsip1_3643820 | חומוס ענק | 85.0 | A | 1 | 1 | Giant chickpeas, single ingredient |
| bsip1_7296073705505 | חומוס מוקפא | 85.0 | A | 1 | 1 | Frozen chickpeas — not a prepared spread |

**Total excluded:** 6 products  
**Corpus impact:** 69 → 63 displayed products; 67 → 61 scored displayed products

---

## Products Reviewed But Retained

The following products are also canned/whole chickpeas but are NOVA-3 (multi-ingredient, canned with additives) and were retained in the ranked display. They are genuinely processed products with ingredient complexity.

| Product ID | Name | Score | Grade | NOVA | Ingredients | Decision |
|-----------|------|-------|-------|------|-------------|----------|
| bsip1_7290018359686 | הקיסר חומוס ענק | 80 | A | 3 | 8 | Retained — NOVA-3, multi-ingredient canned product |
| bsip1_208428 | חומוס שלם יכין | 80 | B | 3 | 4 | Retained — NOVA-3, multi-ingredient canned product |

Note: TASK-064 (Nutrition Agent) flagged these two products for unverified "ללא חומר משמר" claims in their insight lines. The insight line integration from `hummus_insights_v1.md` is pending. These products should be reviewed when insight lines are integrated.

---

## Display Count Changes

| Metric | Before | After |
|--------|--------|-------|
| Total products in corpus | 69 | 69 (unchanged — still analyzed) |
| Displayed products | 69 | 63 |
| Scored displayed products | 67 | 61 |
| Unscored displayed products | 2 | 2 |
| Grade A displayed | 8 | 2 |
| Score range (displayed) | 43–86 | 43–80 |
| Score gap | 43 pts | 37 pts |

---

## Corpus Fate

The 6 excluded products remain in the source JSON (`hummus_frontend_v1.json`). They are filtered at the data transformation layer in `hummus-comparison-page-data.ts` via the `EXCLUDED_NOVA1_IDS` set. They are not deleted and can be reinstated if a future version adds a separate "raw ingredients" or "whole chickpeas" section.

---

*TASK-069 — Frontend Agent — 2026-05-31*
