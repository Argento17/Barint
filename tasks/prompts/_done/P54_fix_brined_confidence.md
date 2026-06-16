# P54 / Fix brined-cheeses confidence over-flagging (H1) (route: C1-CURSOR)

Spec-complete data transform. Correct the confidence labels on the brined-cheeses page per a
verified Nutrition ruling. Mechanical + fully specified — no judgment, no copy/score changes.

## Single target file
`C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
(page-data.ts does NOT carry confidence — do not touch it.)

## Ruling (verified) — see `C:\Bari\02_products\brined_cheeses\reports\confidence_archetype_ruling_v1.md`
Fiber is structurally absent in cheese, so `fiber=null` is an EXPECTED absence, NOT a data gap.
Products currently flagged partial ONLY because fiber is null must become "verified".

## Exact transform
For each product in `.products[]` where BOTH:
  (a) `confidence_sub_reason == "partial_field"`, AND
  (b) within `expansion.nutrition`, the ONLY field whose value is null is `fiber`
      (i.e. energyKcal, protein, fat, satFat, sugar, sodium are ALL non-null),
set these fields to EXACTLY match the page's existing "verified" products:
  - `confidence`: "verified"
  - `confidence_label_he`: "מבוסס על נתונים מלאים"
  - `confidence_tooltip_he`: "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים."
  - `confidence_sub_reason`: null
  - `expansion.confidenceLabel`: "מבוסס על נתונים מלאים"

Change NOTHING else on these products, and do NOT touch any product that does not meet both (a)+(b).

## Hard guards — must hold after the change (these are the acceptance test)
- Products changed: exactly 30.
- Final confidence distribution: `verified` = 33, `partial` = 15.
- The 15 remaining partial = 12 with `confidence_sub_reason=="missing_ingredients"` + 3 with
  `"missing_nutrition"`. NONE of those 15 may change (honesty guard — they have real gaps:
  missing ingredients, or null sugar which IS required).
- ZERO changes to any `score`, `grade`, `insightLine`, `rowVerdict`, `imageUrl`, `barcode`,
  `expansion.nutrition` values, or `expansion.ingredients`. Confidence fields only.
- OFF ban: introduce no external data.

## Gate + return
- Run `npm run build` in `C:\Bari\bari-web` — MUST exit 0, route `/hashvaot/brined-cheeses` present.
- Return: count changed (expect 30); before/after confidence distribution; confirm the 15 partials
  are the 12 missing_ingredients + 3 missing_nutrition (list their barcodes); confirm zero
  score/grade/copy/nutrition changes; build exit code; new sha256 of the file.
- Do NOT close — propose RETURNED. End with the machine-readable return contract
  (`C:\Bari\01_framework\operations\return_contract_v1.md`).
