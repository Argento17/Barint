# Return: P216

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P216_c1cursor_comparisoncontext_carry.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-18T11:26:32.440825+00:00 |
| Finished | 2026-06-18T11:27:56.339750+00:00 |
| Exit code | 0 |

---

## Output

```
## P216 — RETURNED (TASK-330 copy_stage `comparisonContext` carry-forward)

### Problem
Live cereals/hummus baselines predate the required `expansion.comparisonContext` field. `copy_stage.py` carries copy by barcode, then `_schema_match_product` strips fields absent from the live schema — so carried products lost `comparisonContext` and G1 failed on every flip (37+ products across cereals + hummus).

### Fix
After all products are processed, a post-pass derives missing `comparisonContext` via the existing `author_copy._comparison_context(...)` helper (with `compute_corpus_stats` for peer medians). Copy text fields (`insightLine`, `rowVerdict`, `verdict`) are untouched.

```314:371:03_operations/page_generator/copy_stage.py
def _product_as_sheet(prod: dict) -> dict:
    """Minimal fact-sheet shape for _comparison_context from a page product."""
    nut = (prod.get("expansion") or {}).get("nutrition") or {}
    return {
        ...
    }

def _derive_missing_expansion_fields(...):
    ...
    exp["comparisonContext"] = _comparison_context(
        sheet, prod.get("grade"), prod.get("score"), corpus_stats,
    )
```

### Acceptance test results

| Check | Before | After |
|-------|--------|-------|
| **G1 SCHEMA cereals** | FAIL — 20× `missing required field 'comparisonContext'` | **PASS** |
| **G1 SCHEMA hummus** | FAIL — 37× missing | **PASS** |
| **comparisonContext derived** | 0 | cereals **20/20**, hummus **57/57** |
| **score_moves / grade_moves** | — | **0 / 0** per shelf |
| **frozen breach** | — | **none** |
| **G6 COPY-SAFETY** | FAIL | still FAIL (Content lane — out of scope) |

Command run:
```bash
python 03_operations/page_generator/spine_flip.py --set BARI_PALM_HYDRO_V1=on --note "TASK-330 verify"
```

### Files changed
Only `03_operations/page_generator/copy_stage.py` (+72 lines). Other dirty files in the working tree (`additive_burden`, `DISPATCH_BOARD.md`) were pre-existing and not touched by this task.

### Verify
- `git diff --stat -- 03_operations/page_generator/copy_stage.py` → single file
- Post-copy gate reports: `_rescore_staging/cereals/cereals_rescored_gates_report.md` and `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored_gates_report.md` → G1 PASS
- Spine bundle: `_rescore_staging/_spine_runs/20260618T112736Z/spine_run_report.json` → `score_moves: 0`, `grade_moves: 0`, `frozen_breaches: []`

```json
{
  "task": "P216",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/page_generator/copy_stage.py",
      "action": "modified",
      "sha256": "48567c4810954ae59610cbb316d106f6841f38c92e652ac03696124f36a2e1ca"
    }
  ],
  "counts": {
    "g1_cereals": "PASS/1 gate (cereals_rescored_gates_report.md post-copy)",
    "g1_hummus": "PASS/1 gate (hummus_shelfrel_002_rescored_gates_report.md post-copy)",
    "comparisonContext_cereals": "20/20 (cereals_rescored.json expansion.comparisonContext non-null non-PENDING)",
    "comparisonContext_hummus": "57/57 (hummus_shelfrel_002_rescored.json expansion.comparisonContext non-null non-PENDING)",
    "score_moves_cereals": "0/0 (spine_run_report.json per-shelf)",
    "grade_moves_cereals": "0/0 (spine_run_report.json per-shelf)",
    "score_moves_hummus": "0/0 (spine_run_report.json per-shelf)",
    "grade_moves_hummus": "0/0 (spine_run_report.json per-shelf)",
    "frozen_breaches": "0/none (spine_run_report.json frozen_breaches=[])"
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/page_generator/spine_flip.py --set BARI_PALM_HYDRO_V1=on --note \"TASK-330 verify\"",
      "exit_code": 1
    },
    {
      "cmd": "git diff --stat -- 03_operations/page_generator/copy_stage.py",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "spine_flip G1: cereals FAIL(20 missing comparisonContext)→PASS; hummus FAIL(37 missing)→PASS; score_moves=0 grade_moves=0 frozen breach none; git diff touches only copy_stage.py (+72). G6 still FAIL (Content lane)."
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
 M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
 M tasks/DISPATCH_BOARD.md
?? affected_set_spine.json
?? tasks/prompts/P216_c1cursor_comparisoncontext_carry.md
?? test_acceptance.py
```

### After dispatch

```
M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
 M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
 M 03_operations/page_generator/copy_stage.py
 M tasks/DISPATCH_BOARD.md
?? affected_set_spine.json
?? tasks/prompts/P216_c1cursor_comparisoncontext_carry.md
?? test_acceptance.py
```

### Delta

### New / modified since dispatch
   M 03_operations/page_generator/copy_stage.py
