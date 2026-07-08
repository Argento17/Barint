# P511 / re-score yogurt pages against fixed modified-starch classifier — mechanical (route: C2)

The classifier fix from P510 (`03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py`, already
applied and verified — do not re-touch that file) is committed to the working tree. This ticket
re-scores ONLY the yogurt-affected products through the now-fixed pipeline and updates the two
PRE-LAUNCH yogurt frontend JSONs. No live category is touched by this ticket (that is a separate,
owner-gated follow-up — explicitly out of scope here).

## Read first
`02_products/yogurt_system/bsip2_task515_v3/TAPIOCA_STARCH_FIX_COSIGN.md` — full co-sign record
(Nutrition + Product both YES). Both gates are already granted; you are implementing, not deciding.

## Exact scope — 16 barcodes across 2 pages
**Drinkable (3 of 20), run dir `02_products/yogurt_system/bsip2_task515_v3/drinkable/products`:**
7290110573737, 7290110552244, 7290107938396

**Spoonable (13 of 78), run dir `02_products/yogurt_system/bsip2_task515_v3/products`:**
408354, 6664693, 7290010471669, 7290110578053, 7290110578572, 7290119370177, 7290119370955,
7290119372997, 7290119377404, 7290119377411, 7290119380916, 7290119384242, 7290119386642

## Task
1. For each of the 16 barcodes, re-run BSIP2 scoring (using the existing per-product BSIP1 input +
   the now-fixed `ingredient_taxonomy.py`) to produce a corrected `bsip2_trace.json`. Use the same
   BSIP2 entrypoint/script this corpus was originally scored with (check
   `02_products/yogurt_system/bsip2_task515_v3/` for the run script used to produce the existing
   traces — reuse it, do not write a new one).
2. Confirm each product's NEW `tax_modified_starch=True` and the ECS `modified_starch_stabilizer`
   penalty now fires (where the position≥4 gate condition is met — 3 of the 16 may show 0 score
   delta because they fail that gate, per the earlier sandbox measurement; that's expected, not a
   bug).
3. Update the frontend JSON for BOTH pages (score/grade/d4_additives ONLY — do not touch any copy
   field):
   - `bari-web/src/data/comparisons/yogurt_drinkable_frontend_v1.json` AND
     `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_drinkable_FINAL_v3.json`
   - `bari-web/src/data/comparisons/yogurt_spoonable_frontend_v1.json` AND
     `02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_spoonable_FINAL_v2.json`
   Each pair must stay byte-identical to each other on every field you touch.
4. **Expected grade crossings (verify these land exactly, report any deviation):**
   - Drinkable: 7290110573737 B→C, 7290107938396 C→D
   - Spoonable: 7290010471669 D→E, 7290110578572 C→D, 7290119377404 B→C
5. **Everything else byte-identical.** The other 62 products in drinkable/spoonable-not-in-this-list
   AND every non-score/grade/d4 field on the 16 changed products (barcodes, names, images, all copy
   strings) must be UNCHANGED. Prove this — diff before/after and report exactly which fields on
   which products changed.
6. Re-run `python 03_operations/spine/validate_comparison_page.py --json <each page> --traces <run
   dir> --http` on both pages after the update. score==trace must PASS 78/78 and 20/20 respectively
   (with the NEW scores). Report both exit codes + gate breakdown. (Expect the "superlative"/"copy"
   gates to now show new failures where copy references stale scores — that's expected, DO NOT fix
   copy, just report which products' copy is now stale so Content can re-author them.)

## Guards (hard)
- Do NOT re-touch `ingredient_taxonomy.py` (already fixed and verified).
- Do NOT edit `score_engine.py`, `signal_extractor.py`, or `constants.py`.
- Do NOT touch any copy field (`rowVerdict`, `insightLine`, `consumerTakeaway`, `expansion.*`,
  `page_copy`) on any product — Content owns that, in a separate follow-up.
- Do NOT touch any product outside the 16 listed barcodes.
- Do NOT touch any non-yogurt category/page.
- Do not commit.

## Return
Per-barcode before→after (score, grade, d4_additives modified-starch entry) for all 16. Confirm the
5 expected grade crossings landed exactly (flag any that didn't, or any unexpected 6th+ crossing).
Confirm byte-identity everywhere else (diff proof). Both validator exit codes + gate breakdown +
list of which products' copy is now stale (score changed but copy text unchanged). Then the
machine-readable return contract per `01_framework/operations/return_contract_v1.md`.
