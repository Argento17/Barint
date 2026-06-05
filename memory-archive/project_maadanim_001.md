---
name: project_maadanim_001
description: "מעדנים (dairy desserts) full pipeline run_001 — scrape, BSIP1/2, editorial analysis, Cursor handoff"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Full pipeline completed 2026-05-28 for מעדנים category (dairy desserts).

**BSIP0:** 200 Shufersal products scraped — `C:\Bari\02_products\maadanim\maadanim_bsip0_raw_20260528T072053.json`  
**BSIP1:** 200 files — `C:\Bari\03_operations\bsip1\run_maadanim_001\output\`  
**BSIP2:** 200 processed, 169 scored, 0 errors — `C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\`  
**Editorial doc:** `C:\Bari\02_products\maadanim\reports\maadanim_editorial_v1.md`  
**Batch summary:** `C:\Bari\02_products\maadanim\reports\run_maadanim_001_batch_summary.md`

**Why:** מעדנים is the third product category after bread and snack bars; the editorial cycle closes out the pipeline-to-consumer-facing loop for dairy desserts.

**Key findings from data:**
- No A or S grades; 4 B grades (all protein yogurt variants, not traditional מעדנים)
- מילקי (the category icon) scores E (26.6–40.3) — NOVA4, additive-loaded
- 67% of shelf is NOVA4, 88% capped — almost universal ceiling
- "Protein" positioning hides a 27-point gap: יופלה GO 69.6/B (NOVA3, 0 additives) vs. מעדן חלבון ללת"ס 42.6/D (NOVA4)
- "Diet/ללא סוכר" consistently underperforms: מעדן דיאט שוקולד 35/D vs. מעדן משמש 57/C (no wellness claim)
- Soy alternative (מעדן סויה ביו טבעי 57.4/C, NOVA3) outscores most dairy מעדנים

**Corpus filter:** ~43 non-מעדנים false positives in the 200 (candy, diet syrup, jam, jelly, noodles, pancake mix, white cheese). Editorial scope ≈ 125 products.

**Router additions to router_v2.py:** מילקי, מעדן חלבון, מעדן ילדים, מעדן, עדנה, פרוביו, יופלה hard anchors added with exclusion sets.

**How to apply:** Use editorial doc for Cursor implementation. Use batch summary for any category-level analysis. Router anchors are live in proto_v0.

---

## Enrichment Cycle 001 — 2026-05-28

Built `maadanim_frontend_v1.json` — clean `BariProductVM[]` ready for frontend consumption.

- 90 editorial-scope products (78 initial + 12 recovered via name-variation fix)
- All 90 scored, all 90 with images (Shufersal Cloudinary, confirmed publicly accessible)
- Grade dist: B×1 / C×15 / D×61 / E×13 | Avg: 43.7
- 88 verified / 2 partial / 0 insufficient
- Sugar coverage: 34% (Shufersal structural limitation)
- Ingredient text cleaned (nutrition-facts bleed-in removed)
- 2 new insight lines authored: מעדן דיאט products (Contradiction 3)

**Frontend JSON:** `C:\Bari\02_products\maadanim\maadanim_frontend_v1.json`  
**Schema:** `BariProductVM[]` → matches `src/lib/view-models/index.ts`

**Action required before production:**  
Add `res.cloudinary.com` to `next.config.ts` images.remotePatterns (frontend task).

**Next enrichment priority:** Cross-retailer sugar supplement (Rami Levy / Yochananof barcode lookup).

---

## CE Quality Pass (Reasoning Completion) — 2026-05-29

Built `maadanim_frontend_v2.json` — canonical output. Wire this to frontend, not v1.

**Builder script:** `C:\Bari\02_products\maadanim\build_maadanim_v2.py`

**33 changes applied (pass 1) + 5 final fixes (pass 2):**
- **12 false-fruit signals removed**: Products with only monk fruit sweetener (רכז פרי המונק) or black carrot colorant (רכז גזר שחור) were incorrectly labeled "בסיס פרי נראה ברשימה". Removed for: מוו, מילקי variants, דני שוקולד, ירח מתוק, מלבי, ג'לי פטל, and more.
- **2 products with explicit "לא מכיל פירות"**: באדי תות שדה, דניאלה בטעם ענבים — both had fruit-presence signals. Now show honest limitingFactors quoting the on-pack declaration.
- **לימבו פטל**: Corrected to water+sugar base with zero dairy → clear bottomLine
- **1 score correction tracked**: GO דובדבן 0.7% (48→52, was applied in v1) now has `_calibration` field
- **Specific product improvements**: מלבי שמנת, מעדן הגולן וניל, מעדן חצילים, מילקי שוקולד — added honest positiveSignals and sharper limitingFactors

**Insight line fixes (already in v1, carried to v2):**
- מעדן שיבולת שועל: "4 רכיבים" → "11 רכיבים, ממתיקים ומייצבים ברשימה"
- מעדן סויה ביו טבעי: "5 רכיבים" → "הרשימה ארוכה יותר ממה שנראה על הגביע"

**Grade dist v2:** B×1 / C×16 / D×60 / E×13 (same as v1 except GO דובדבן D→C)
**29 products with zero positiveSignals** — all D/E, intentionally honest.
