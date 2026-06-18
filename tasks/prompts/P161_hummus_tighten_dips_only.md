# P161 / TASK-306 — Hummus tighten to prepared-dips-only (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Read `tasks/TASK-306.md` + `03_operations/page_generator/configs/hummus_shelfrel_002.json` (already has 6 raw-chickpea exclusions from P160).

## Owner ruling
The hummus comparison = PREPARED DIPS ONLY. Beyond the 6 single-ingredient raw-chickpea bags already excluded, the shelf still
shows canned/cooked WHOLE chickpeas (e.g. 208428, 7290018359686) and products with EMPTY ingredient data (e.g. 7296073733317,
7296073733348, 1990261) — none are prepared dips. Tighten the shelf.

## Rule (apply to the current hummus staging set, `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored.json` / corpus `02_products/hummus/canonical_bsip1/`)
EXCLUDE a product if EITHER:
  (a) its ingredient list has NO prepared-spread marker — i.e. no tahini (`טחינה`), no oil (`שמן`), and no seasoning/aromatics
      (garlic `שום`, lemon `לימון`, cumin `כמון`, etc.) — meaning it's just chickpeas ± water ± salt (canned/cooked/raw whole chickpeas), OR
  (b) its ingredient data is EMPTY/unknown (cannot confirm it's a prepared dip).
KEEP a product if its ingredients show a prepared spread (tahini and/or oil and/or seasoning present).
Add each excluded barcode to `configs/hummus_shelfrel_002.json` `exclusions` with the precise reason
(`out_of_scope: whole chickpeas, not a prepared dip` or `out_of_scope: no ingredient data, cannot confirm prepared dip`).
Be conservative: if a product clearly has tahini/oil/seasoning it STAYS; if borderline, flag it for human review rather than dropping silently.

## Then
Re-run JUST this shelf: `python 03_operations/page_generator/rescore_all.py --shelf hummus_shelfrel_002`. Re-gate: G8 PASS,
C10 milk Δ0, OFF=0, score==trace OK. Confirm the new shelf is prepared dips (the new top should be an actual tahini-bearing spread).

## Return
- The full keep/exclude decision: every excluded barcode + reason + ingredient evidence; the KEPT count.
- New product count, new grade distribution, new top-5 (barcode/grade/short ingredient).
- The list of KEPT products whose grade differs from the current LIVE hummus page (`bari-web/src/data/comparisons/hummus_frontend_v5.json`) OR that are new vs live — these need fresh copy.
- Gate results. Borderline products flagged for review.
- Boundaries: only edit configs/hummus_shelfrel_002.json + regenerate the hummus staging page. No other shelf, no engine, no bari-web, no deploy. OFF-ban absolute.
- **Do not close — propose RETURNED.** End with the return contract JSON (`01_framework/operations/return_contract_v1.md`): `task`, `proposed_status`, `artifacts[]` (path+action+sha256), `counts{}` (excluded/kept + new dist, with command), `commands_run[]`, `not_done[]`, `self_check`.
