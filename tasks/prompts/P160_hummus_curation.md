# P160 / TASK-304 — Hummus curation: drop raw-chickpea products (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Read `tasks/TASK-304.md` + the exemplar `03_operations/page_generator/configs/cereals.json` (exclusions shape).

## Problem
The prepared-hummus comparison shelf is topped by RAW/DRIED CHICKPEA products, not hummus dip. On the staging page
`_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json`, the top 5 (all grade A) are single-ingredient
chickpeas: 7296073733324, 7296073733331 ("100% חומוס"), 7296073005889, 7296073006015 ("גרגרי/גרגירי חומוס"), 7296073705505 ("חומוס").
Real prepared hummus dips start at B/76.8. These raw-chickpea products do not belong on a prepared-hummus comparison.

## Do this
1. Identify EVERY product on the hummus shelf whose ingredient list is a single raw-chickpea term (e.g. `חומוס`, `גרגרי חומוס`,
   `גרגירי חומוס`, `100% חומוס`, or equivalently a 1-item ingredient list that is just chickpeas) — i.e. dried/frozen/canned
   chickpeas, NOT a prepared spread (which has tahini, oil, lemon, garlic, salt, etc.). List them with barcode + ingredient.
2. Add them to `03_operations/page_generator/configs/hummus_shelfrel_002.json` `exclusions` with reason
   `out_of_scope: raw/dried chickpeas, not a prepared hummus spread`.
3. Re-run JUST this shelf: `python 03_operations/page_generator/rescore_all.py --shelf hummus_shelfrel_002`.
4. Re-gate / verify on the regenerated staging page: G8 PASS, C10 milk Δ0, OFF=0, score==trace OK, and confirm the new top of
   the shelf is an actual prepared hummus dip (not a chickpea bag). Report the new product count + new top-5.

## Boundaries
- Only edit `configs/hummus_shelfrel_002.json` (exclusions) + regenerate the hummus staging page. Touch NO other shelf, NO engine,
  NO bari-web, NO data files. OFF-ban absolute. Staging-only. No commit, no deploy.
- Be conservative: exclude ONLY genuine single-ingredient raw chickpeas. If a product is a borderline prepared spread, KEEP it and
  flag it for human review rather than dropping it.

## Return
The list of excluded barcodes (+ ingredient evidence), the new hummus product count, the new top-5 (barcode/grade/ingredient),
and the gate results (G8/C10/OFF/score==trace). **Do not close — propose RETURNED.** End with the return contract JSON
(`01_framework/operations/return_contract_v1.md`): `task`, `proposed_status`, `artifacts[]` (path+action+sha256), `counts{}`
(excluded count + new count, with command), `commands_run[]` (cmd+exit), `not_done[]`, `self_check`.
