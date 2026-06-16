# P58 / Consolidated re-render brined page: run_005 scores + new copy + image-render fix + index card + hero (route: C1-CURSOR)

Spec-complete render. Propagate the finalized scores + copy into the brined-cheeses page and fix the
render gaps the owner found. Mechanical/wiring only — no new copy, no score changes. Do NOT close —
propose RETURNED.

## Sources of truth (DO NOT edit these)
- Copy: `C:\Bari\02_products\brined_cheeses\brined_cheeses_copy_v1.json`
  (pageShell: eyebrow, heroTitle, prologueSentences[2], methodologyLines[3], categoryNote;
   products keyed by barcode: score [FLOAT], grade, insightLine, rowVerdict).
- Scores authority: `02_products\brined_cheeses\bsip2_outputs\run_brined_005\verification_table.csv`.

## Targets to update
1. `C:\Bari\bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json`
2. `C:\Bari\bari-web\src\lib\comparisons\brined-cheeses-page-data.ts`
3. `C:\Bari\bari-web\src\app\hashvaot\page.tsx` (the index)
4. component if needed: `...\components\comparisons\brined-cheeses-comparison-page.tsx`

## Tasks
1. **Scores → run_005:** set each product's displayed `score` to the ROUNDED INT of its run_005 value
   (e.g. 85.4→85), `grade` to run_005 grade. New dist A:9 B:28 C:9 D:2. Match by barcode.
2. **Copy → from copy_v1.json:** propagate every product's `insightLine` + `rowVerdict`; and the
   pageShell `prologueSentences`, `methodologyLines`, `categoryNote`, `heroTitle`, `eyebrow` into
   page-data.ts. Verbatim; match by barcode. The hero must show the new heroTitle, and the page must
   render the 2 prologueSentences + 3 methodologyLines (wire them if the component doesn't already).
3. **FIX PRODUCT IMAGE RENDERING (owner "made up" finding):** the frontend JSON has a valid,
   barcode-matched `imageUrl` for all 48 (real PNGs, domain whitelisted) but they DON'T render in the
   row — `brined-cheeses-page-data.ts` doesn't map imageUrl into the row VM the way
   `milk-comparison-page-data.ts` does (`imageUrl: product.image_url`). Wire it so EVERY product's
   image renders in its row, matching the milk/hard-cheeses pattern. Verify in the built page that
   images display (not just resolve).
4. **Category card on `/hashvaot` index:** add a card for brined cheeses (label גבינות מלוחות, route
   `/hashvaot/brined-cheeses`, A:9 B:28 C:9 D:2, 48 products) matching the existing index cards' shape.
5. **Category hero image:** wire a representative product image as the page/category hero — use the
   top-scored product's imageUrl (barcode 7290019635826, פטה עיזים מעודנת 5%) if the page/card needs
   one. (Auto-extraction is generalized later in TASK-268; for now plant this one.)

## Guards
- OFF ban absolute — no external data. - Change ONLY copy strings, displayed score/grade, image
  wiring, and the index card. Do NOT alter nutrition values, confidence fields, barcodes, or ordering.
- The confidence fields (verified=33/partial=15) from the prior fix MUST be preserved.

## Gate + return
- `npm run build` in `C:\Bari\bari-web` → exit 0, route `/hashvaot/brined-cheeses` present.
- Return: files changed + shas; confirm 48/48 scores=run_005 int, copy propagated (0 mismatch vs
  copy_v1), images wired (show the page-data mapping line), index card added, prologue/methodology
  rendered; build tail. Do NOT close — propose RETURNED. End with the return contract.
