# BSIP0 Scope Audit — Shufersal Frozen Vegetables

**Audited file:** `02_products/frozen_vegetables/bsip0_outputs/bsip0_shufersal_frozen_vegetables_v3.json`
**Auditors:** QA Agent + Data Agent (run inline by orchestrator)
**Date:** 2026-06-10
**Trigger:** DeepSeek reported scrape complete + ready for BSIP1. Conclusion independently re-verified against the JSON — **not trusted**.

---

## Verdict: **FAIL (as delivered)** → scope-clean file produced → **HOLD** before BSIP1

- The delivered 164-product set is **65% out of scope** (107/164 contaminants).
- The manifest carries a **false data-completeness claim**: `completeness.with_ingredients: 144`, but only the bare label `"רכיבים"` was captured — **true real-ingredient coverage = 0/164**.
- A scope-clean file of **50 true products** was produced; it is scope-pure but still carries the 0% ingredient defect, so it is **not** clear for BSIP1 yet.

---

## Headline numbers

| Metric | File / DeepSeek claim | True (this audit) |
|---|---|---|
| Products "in scope" | 164 | **50** |
| Out of scope inside the 164 | (85 pre-excluded only) | **107** |
| Manual review | 0 | **7** |
| Nutrition coverage (in-scope) | 145/164 | **50/50 = 100%** |
| Real-ingredient coverage | 144/164 | **0/50 = 0%** (whole file 1/164, and that 1 is out-of-scope fresh) |
| Duplicate SKUs / barcodes | — | **0** |

---

## Classification (164 → 10 buckets; full partition, no overlap, no gap)

| Bucket | Count | Disposition |
|---|---|---|
| in_scope_frozen_vegetable | 29 | KEEP |
| frozen_legume_sold_as_vegetable | 13 | KEEP |
| frozen_herb_or_seasoning | 8 | KEEP |
| manual_review | 7 | REVIEW |
| fresh_produce_out | 23 | EXCLUDE |
| pantry_legume_out | 18 | EXCLUDE |
| canned_or_preserved_out | 7 | EXCLUDE |
| snack_out | 19 | EXCLUDE |
| hummus_or_salad_out | 8 | EXCLUDE |
| other_out | 32 | EXCLUDE |
| **TOTAL** | **164** | 50 keep / 7 review / 107 exclude |

---

## INCLUDED — 50 true products (populate the scope-clean file)

### in_scope_frozen_vegetable (29)
ארטישוק ירושלמי קפוא · ארטישוק תחתיות · במיה קפואה 600 גרם · ברוקולי מוקפא (×2) · גרגירי תירס קפוא אורגני · גרעיני תירס קפוא · כרובית מוקפאת (×3) · לקט ירקות מעורבים · לקט ירקות קפוא אורגני · לקט כפרי · לקט לקוסקוס מוקפא · לקט נורמנדי מוקפא · מדליוני תרד קפוא · מיני ברוקולי מוקפא · מיני כרובית · עלי תרד מוקפאים · צמד ברוקולי וכרובית · שעועית ירוקה חתוכה (×2) · שעועית ירוקה עדינה · שעועית ירוקה קפוא אורגני · שעועית ירוקה שלמה · שעועית ירוקה שלמה מוקפאת · שעועית עדינה שלמה קפואה · שעועית צהובה חתוכה · תחתיות ארטישוק

### frozen_legume_sold_as_vegetable (13)
אפונה ירוקה מוקפאת (×2) · אפונה ירוקה עדינה מוקפאת · אפונה עדינה מוקפאת · אפונה עדינה קפוא אורגני · גרגרי חומוס מבושל מוקפא · פול ירוק מוקפא · פולי סויה קלופים מוקפאים · פולי סויה שלמים מוקפאים (×3) · שעועית לבנה מבושלת מוקפא · שעועית לבנה מוקפאת

### frozen_herb_or_seasoning (8)
ג'ינג'ר קצוץ מוקפא · ממרח שום מוקפא · פטרוזיליה קצוצה מוקפאת · שום כתוש דורות · שום כתוש מוקפא · שום כתוש קפוא במגשית (×2) · שום כתוש קפוא בצנצנת

All 50 carry category `A1605`/`A160501` (frozen vegetables) or `A160510` (frozen herbs/seasoning), or an explicit `מוקפא/קפוא` name token. Full per-product list with codes is in `bsip0_shufersal_frozen_vegetables_scope_clean_v1.json`.

---

## MANUAL REVIEW — 7 (NOT in clean file, NOT cleared for BSIP1)

| Product | Code | category_raw | Why |
|---|---|---|---|
| חומוס מוקפא | P_7296073705505 | `A160501,A510102,A51,A16,A5101,A1605` | frozen chickpeas vs. frozen hummus paste ambiguous |
| ירקות ופסטה א-לה איטליה | P_107622 | `A160501,A16,A1605` | frozen veg medley that contains pasta |
| לקט להקפצה פסטה פוזילי | P_103730 | `A160501,A16,A1605` | frozen stir-fry mix containing fusilli pasta |
| קטניות מן הטבע | P_8830690 | (none) | no category, no nutrition, no frozen indicator |
| קטניות מן הטבע | P_7290113194625 | (none) | no category, no nutrition, no frozen indicator |
| קטניות מן הטבע | P_7290113194601 | (none) | no category, no nutrition, no frozen indicator |
| קטניות מן הטבע | P_7290113195851 | (none) | no category, no nutrition, no frozen indicator |

---

## EXCLUDED — 107 (summary)

- **fresh_produce_out (23)** — `A04` fresh produce, no frozen indicator: אספרגוס (×2), ארטישוק, ארטישוק/תפו"א ירושלמי, ברוקולי ארוז, ברוקלי וכרובית שטופים, זוג תירס מתוק מבושל, כרובית, כרובית ארוזה, כרובית פיורטי, לקט סלנובה ועלי בייבי, מארז אפונת שלג, מארז כרובית וברוקולי, מארז נבטי אפונה, מיקס עלי מיקרו, עלי בייבי (×2), עלי מיקרו (×2), עלי תרד בייבי (×2), תירס, תרד עלים.
- **pantry_legume_out (18)** — `A22/A2211` dry legumes: אפונה (×4), אפונה ירוקה שופרסל, חומוס (×4), שעועית ארגנטינאית, שעועית לבנה (×6), שעועית מעורבת שופרסל, שעועית מש.
- **canned_or_preserved_out (7)** — `A2217` / tetra-pak / vacuum: אפונה וגזר, אפונת גינה וגזר, שעועית אדומה טטרה פק, שעועית לבנה טטרה פק, שעועית שחורה, שעועית שחורה טטרה פק, תירס מתוק ארוז בואקום.
- **snack_out (19)** — chocolate / fried / breaded snacks: אפונה מטוגנת בקופסא, חטיף סויה בקופסא, חטיף קידס שוקולד חלב, חטיף שוקולד לבן יוגורט, חטיפוני גזר (×2), חטיפי כרובית, טבעול חטיפי כרובית, לביבות כרובית (×2), מקלוני ירקות כרובית, סלים דליס/טופינג (×6), פול מטוגן בקליפה, תירס קלוי בקופסא.
- **hummus_or_salad_out (8)** — `A1624` hummus & spreads: חומוס (×5 incl. אבו גוש/אסלי/מסבחה/מסעדות), ממרח ארטישוק (×3).
- **other_out (32)** — soy/fruit beverages (משקה סויה ×11, נורדיק ×4, משקה מוגז), pasta (MANTANINO/ברילה ×7), פתיתים אפויים (×2), פירורי לחם, קרוטונים (×3), ממרח לחיץ, טחון עגל 100% (ground veal).

Full code-level lists for every excluded item are reproducible from the classification map in this audit; the clean file retains only the 50.

---

## Data-quality findings (independent of scope)

1. **CRITICAL — ingredient parser broken.** `ingredients_raw` = the literal heading word `"רכיבים"` for every product; no ingredient list was extracted. `completeness.with_ingredients: 144` counts the heading, not content. True real-ingredient coverage = **0** across all 164 (the single exception, `מארז נבטי אפונה`, is out-of-scope fresh produce). Frozen-veg scoring needs ingredient text for seasoned mixes / additive detection (e.g. לקט נורמנדי, ירקות ופסטה).
2. **GOOD — nutrition panels are real.** `nutrition_raw` holds proper per-100g values (energy / protein / carb / fat / sodium / fiber). 50/50 in-scope products carry a populated nutrition dict.
3. **GOOD — no duplicate SKUs / barcodes** across the search vs. category sources.
4. **Manifest integrity issue.** `scope_notes` claims only fresh flowers + a few fresh items were excluded; in reality 107 of the retained 164 are out of scope. The v3 manifest cannot be trusted as a scope statement.

---

## Recommendation

- **redo_scope_filter: DONE** — `bsip0_shufersal_frozen_vegetables_scope_clean_v1.json` (50 products; all source artifacts preserved: `raw_html_path`, `product_url`, barcodes, `nutrition_raw`; each tagged with `scope_class` + `ingredients_present`).
- **hold before BSIP1:** the scope-clean set is scope-pure, but **0% real ingredient coverage** is a blocker for a category where additives/sauces matter. Re-scrape ingredient lists for the 50 (product pages exist — `raw_html_path` present), then re-verify.
- **proceed_to_bsip1: NOT yet.** Permitted only after (a) the ingredient re-scrape lands real text and (b) the 7 manual_review items are adjudicated.
