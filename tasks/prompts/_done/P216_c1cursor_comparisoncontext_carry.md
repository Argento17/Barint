# P216 — TASK-330 copy_stage: derive required expansion fields on carry-forward (route: C1-CURSOR)
# Data Agent build — the #1 spine-PASS prerequisite (render-contract gap)

**Repo:** `C:\Bari`
**Task to read:** `C:\Bari\tasks\TASK-330.md`
**Spine first-run evidence:** `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored_gates_report.md`
and `_rescore_staging/cereals/cereals_rescored_gates_report.md` — G1 schema FAIL:
`#.products[N].expansion: missing required field 'comparisonContext'` (37+ products).

## Root cause (confirmed)
`comparisonContext` is a REQUIRED per-product field in `products[].expansion` (page_output_schema_v2/v3 +
`copy/authoring_contract.json:153`). `author_copy._comparison_context(sheet, grade, score, corpus_stats)`
already derives it ([author_copy.py:650](03_operations/page_generator/copy/author_copy.py#L650)). The spine's
`copy_stage.py` carries existing copy forward BY BARCODE, but the carried cereals/hummus copy predates the
required field → staged expansion lacks `comparisonContext` → G1 fails on every flip → bundle never reaches PASS.

## Objective
Make the **carry-forward path in `copy_stage.py`** complete the required expansion contract: when a carried
product's `expansion` is missing `comparisonContext` (or other schema-required expansion fields), DERIVE the
missing field via the existing `author_copy._comparison_context(...)` rather than carrying an incomplete
expansion. Prefer reusing the existing derivation helper — do NOT reimplement it, do NOT invent copy.

## ONLY file you may edit: `03_operations/page_generator/copy/copy_stage.py`
- Do NOT edit product copy-TEXT fields (insightLine / rowVerdict / verdict) — a parallel lane (Content) owns
  those. You only ADD the missing structural `comparisonContext` field.
- Do NOT touch the scoring path, render_fields.py, or any page JSON under bari-web.

## Hard guards
- No score movement (this is copy-structural). OFF-ban absolute.
- comparisonContext text must come from the existing `_comparison_context` derivation (grade/score/corpus
  context) — never fabricated provenance or invented claims.

## Acceptance test (run it, put result in self_check)
Re-run the spine drill and show G1 now passes on the affected shelves:
`python 03_operations/page_generator/spine_flip.py --set BARI_PALM_HYDRO_V1=on --note "TASK-330 verify"`
- Report: previous G1 = FAIL (37+ missing) → new G1 result for cereals + hummus.
- Confirm `score_moves=0 / grade_moves=0` unchanged (you moved no score) and `frozen breach none`.
- Confirm `git diff --stat` touches ONLY `copy_stage.py`.
Note: G6 copy-safety (banned phrases) may still FAIL — that's the parallel Content lane's fix, not yours.

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.**
