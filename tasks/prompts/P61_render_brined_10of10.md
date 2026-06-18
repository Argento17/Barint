# P61 / Brined render to 10/10: brand-in-titles + additives dropdown + copy propagate (route: C1-CURSOR)
Spec-complete render. Apply the owner's 10/10 items to the brined page. Do NOT close — propose RETURNED.

## Sources of truth (do not edit)
- Copy (final, just polished): `C:\Bari\02_products\brined_cheeses\brined_cheeses_copy_v1.json`
  (pageShell: eyebrow, heroTitle, prologueSentences, methodologyLines, categoryNote; products by barcode: insightLine, rowVerdict, score, grade).
- Brand map (all 48): `C:\Bari\02_products\brined_cheeses\reports\brand_map_v1.json` (barcode → brand).
- Additive map (AdditiveEntry-ready): `C:\Bari\02_products\brined_cheeses\reports\additive_map_v1.json`.

## Targets
1. `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
2. `C:\Bari\bari-web\src\lib\comparisons\brined-cheeses-page-data.ts`

## TASK 1 — Brand in EVERY product title (owner rule)
For each product, append its brand from brand_map_v1.json to the display `name`, format:
`"<name> — <brand>"` (e.g. "גבינה צפתית במים 5% — מחלבת המושבה"). All 48 have a brand; none skipped.
Match by barcode.

## TASK 2 — Additives dropdown (owner: reuse AdditivePanel — replace bare "preservative")
The page must show the additives panel (`AdditivePanel.tsx`, already rendered by
`expansion-section.tsx` when `GLASSBOX_D5D6_ON && product.d4_additives !== undefined`).
- For EACH product, build a `d4_additives` array of `AdditiveEntry` (type in
  `src/lib/view-models/index.ts`): for every additive E-number present in that product's PARSED
  ingredients (`expansion.ingredients` / limitingFactors — they list E202/E575/E252/E406/E410 and
  Hebrew aliases like "פוטסיום סורבט"), emit the matching entry from additive_map_v1.json
  (`by_e_number`, matching on e_number OR any alias). Dedup. A product with no recognised additive
  gets `d4_additives: []` (panel renders an "אין תוספים" empty state — NOT undefined, so it shows).
- Map `d4_additives` into the row VM in page-data.ts (see how bread/cereals/hummus page-data do it —
  `bari-web/src/data/comparisons/cereals_frontend_v2.json` has populated `d4_additives`; mirror it).
- Ensure the `NEXT_PUBLIC_GLASSBOX_D5D6` frontend flag is ON (it already is for bread/cereals/hummus —
  confirm; do NOT turn other flags on/off).
- Remove/replace the bare "תוספות מזוהות: preservative" limitingFactor IF the additives panel now
  conveys it (avoid duplicate). Keep limitingFactors that are non-additive (sodium/fat).

## TASK 3 — Propagate the polished copy
Update insightLine + rowVerdict (all 48) and pageShell (prologueSentences, methodologyLines,
categoryNote, heroTitle) from copy_v1.json, verbatim, by barcode. Scores display as rounded int.

## Guards
- OFF ban absolute. Do NOT change any score/grade/nutrition value, barcode, imageUrl, or confidence field.
- Preserve confidence verified=33/partial=15. Preserve grade_dist A:9 B:28 C:9 D:2.

## Gate + return
- `npm run build` in bari-web → exit 0, route present.
- Return: files+shas; confirm 48/48 brands appended; d4_additives populated (count of products with
  >=1 additive entry; show 2 example entries); copy propagated (0 mismatch vs copy_v1); 0 score/conf
  changes; flag state; build tail. Do NOT close — propose RETURNED. End with the return contract.
