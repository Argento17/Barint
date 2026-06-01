# מעדנים — Enrichment Cycle 001 Report

**Date:** 2026-05-28  
**Trigger:** Frontend launch preparation  
**Scope:** מעדנים editorial corpus expansion + frontend JSON build  

---

## What Was Done

1. Audited 200 BSIP2 traces against finalized insight lines v1
2. Recovered 12 products missed due to name-variation mismatches (extra spaces, missing spaces before percentages)
3. Added 2 new insight lines for diet-trap products (Contradiction 3 in editorial)
4. Fixed ingredient text cleaner: stripped nutrition-facts bleed-in from BSIP1 tokenized lists
5. Added sugar recovery from BSIP0 raw for products where BSIP1 missed the field
6. Built clean `maadanim_frontend_v1.json` in `BariProductVM[]` schema
7. Verified Shufersal Cloudinary image URLs are publicly accessible (HTTP 200, no referrer restriction)

---

## Raw Scrape Summary

| Source | Products |
|--------|----------|
| BSIP2 traces | 200 |
| BSIP0 raw (Shufersal) | 200 |
| Image URLs in BSIP0 | 200 (100%) |

---

## Editorial Corpus

| Metric | Count |
|--------|-------|
| In editorial scope (insight line matched) | 90 |
| Excluded false positives | 110 |

**False positive categories excluded:** candy/mints, diet syrups, jams, jelly packets, protein noodles, pancake mix, carbonated drinks, tahini spread, cereals, oat cookies, white cheeses (bulgur, tzfatit), probiotic supplements, cheesecake mixes.

---

## Scored Product Table (Sample)

| Product | Score | Grade | Confidence |
|---------|-------|-------|------------|
| יופלה GO מועשר בחלבון | 70 | B | verified |
| מעדן סויה ביו טבעי | 57 | C | verified |
| מעדן משמש | 57 | C | verified |
| מעדן הגולן שוקולד | 53 | C | verified |
| גמדים תות בננה מארז | 53 | C | verified |
| מעדן חלבון בטעם וניל | 54 | C | verified |
| דנונה במתיקות מעודנת | 51 | C | verified |
| מלבי שמנת | 50 | C | verified |
| ... (82 more) | — | — | — |
| מילקי קייק | 27 | E | verified |

**Average score:** 43.7  
**Grade distribution:** B×1 / C×15 / D×61 / E×13

---

## Coverage Report

| Field | Coverage |
|-------|----------|
| Image URL | 90/90 (100%) |
| Nutrition (any field) | 90/90 (100%) |
| Energy kcal | 90/90 (100%) |
| Protein | 90/90 (100%) |
| Sugar | 31/90 (34%) |
| Fat | 90/90 (100%) |
| Fiber | partial |
| Sodium | 90/90 (100%) |
| Ingredients | 90/90 (100%) |
| Insight line | 90/90 (100%) |

**Sugar gap:** Shufersal scraper did not tabulate `sugar_raw` for most products. This is a structural limitation of the source — not a pipeline bug. Frontend hides null nutrition cells correctly.

---

## Top Contradictions (confirmed from corpus)

| Contradiction | Evidence |
|---------------|----------|
| Icon paradox | מילקי קייק 27/E is the lowest score; מילקי brands cluster E–D |
| Protein spread | יופלה GO 70/B vs. מעדן חלבון ללת"ס 43/D — 27pt gap, same label |
| Diet trap | מעדן דיאט שוקולד 0.2% (35/D) scores 22pts below מעדן משמש (57/C) |
| Plant-based paradox | מעדן סויה ביו טבעי (57/C) outscores most dairy; flavored soy drops to 42–46/D |
| Pudding inversion | Instant powder 49/D vs. ready cup 32/E — convenience adds processing |

---

## Insight-Line Candidates (new, from this cycle)

Two new lines written for diet-trap products not previously assigned:

| Product | Score | Line | Type |
|---------|-------|------|------|
| מעדן דיאט שוקולד 0.2% | 35/D | "תווית דיאט, ציון נמוך ב-22 נקודות ממעדן הפרי הפשוט" | T2 |
| מעדן דיאט בטעם שוקולד | 38/D | "מסומן 'דיאט', ציון נמוך ממוצרים ללא תווית" | T2 |

---

## Missing Image List

**None.** All 90 editorial-scope products have Shufersal Cloudinary image URLs.  
Image URLs are publicly accessible: verified HTTP 200 on sample URLs, no referrer restriction.

**Action required before production:**  
Add to `next.config.ts` `images.remotePatterns`:
```js
{ protocol: "https", hostname: "res.cloudinary.com", pathname: "/shufersal/**" }
```
This is a frontend task (Cursor).

---

## Confidence / Data Quality Report

| State | Count |
|-------|-------|
| verified (confidence ≥ 75) | 88 |
| partial (confidence < 75) | 2 |
| insufficient | 0 |

All 90 products have `data_sufficiency: "sufficient"` in BSIP2.  
The 2 partial products have confidence scores 65–70 (missing fiber and NOVA uncertainty).

---

## Ready for Frontend?

**Verdict: YES — PASS**

- 90 products, all scored, all with images
- Ingredient text cleaned of nutrition-facts bleed-in
- Sugar gap is structural and disclosed (null cells hidden correctly)
- Shufersal images publicly accessible
- One prerequisite: `next.config.ts` image hostname (frontend task)

**Output file:** `C:\Bari\02_products\maadanim\maadanim_frontend_v1.json`  
**Schema:** `BariProductVM[]` (matches `src/lib/view-models/index.ts`)

---

## Data Gaps Remaining

| Gap | Severity | Fix path |
|-----|----------|----------|
| Sugar missing for 66% of products | Medium | Cross-retailer scrape (Rami Levy or Mega have more complete nutrition tables) |
| Single-retailer coverage only | Low | BSIP0 cycle 2: Rami Levy or Yochananof for cross-validation |
| Müller protein products not covered | Low | 3 products in BSIP0 corpus, pending insight line authoring |
| יוגורט GO קרמי variants not covered | Low | New GO sub-line, pending editorial decision |

---

## Next Cycle Recommendation

**Priority 1:** Sugar enrichment via cross-retailer supplement  
Run Rami Levy or Yochananof scrape for the 90 מעדנים products using barcode lookup.  
These retailers display more complete nutrition tables and may fill the 34% sugar gap.

**Priority 2:** Begin לחם enrichment cycle (next category in queue).
