# Return: P219

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P219_c1grok_g6_sodium_wordboundary_fix.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T11:56:26.234848+00:00 |
| Finished | 2026-06-18T11:58:03.810639+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P219 task prompt and return contract first, then execute the task body below the separator.
The task is a targeted regex fix in `run_gates.py`. I'll read that file and apply the change.
Running the acceptance test and spine verification next.
Acceptance test passed. Running spine verification next.
## P219 Return — TASK-330 G6 sodium word-boundary gate fix

**Proposed status:** RETURNED

### What changed

Updated `SODIUM_CAUSAL_PATTERN` in `03_operations/page_generator/gates/run_gates.py` (~lines 105–109) to the P217/C3 prefix-aware word-boundary form:

```105:109:03_operations/page_generator/gates/run_gates.py
# Sodium causal framing: נתרן within 30 chars after כי / בגלל / בשל
# word-boundary guard (P217/C3) — stop `כי` matching inside `נמוכים` / `בשל` inside `מבשל` (EV-051 substring-collision class); optional ו/ש prefix preserves real causal forms `ובגלל`/`שבגלל`.
SODIUM_CAUSAL_PATTERN = re.compile(
    r"(?<![א-ת])(?:[וש])?(?:כי|בגלל|בשל)(?![א-ת]).{0,30}נתרן",
    re.UNICODE,
```

### Verify (orchestrator)

| File | Line | Check |
|------|------|-------|
| `03_operations/page_generator/gates/run_gates.py` | 106–108 | Comment + regex match P217/C3 spec exactly |
| `_rescore_staging/cereals/cereals_rescored_gates_report.md` | G6 section | `[PASS] G6 COPY-SAFETY`; 0 `FAIL: barcode` lines |
| `_rescore_staging/hummus_shelfrel_002/hummus_shelfrel_002_rescored_gates_report.md` | G6 section | `[PASS] G6 COPY-SAFETY`; 0 `FAIL: barcode` lines |
| `_rescore_staging/_spine_runs/20260618T115732Z/spine_run_report.json` | per_shelf | `score_moves: 0`, `grade_moves: 0`, `integrity_flags: []` |

### Spine results

- **cereals G6:** PASS — cereals false-positives cleared (7296073642046, 7296073642022 no longer flagged)
- **hummus G6:** PASS — 0 copy-safety violations
- **G1:** PASS both shelves
- **score_moves:** 0 both shelves
- **frozen breach:** none (`integrity_flags: []`)
- Overall gate FAIL is G2 PENDING_COPY coverage only — unrelated to this fix

### Scope guard

`git diff --stat 03_operations/page_generator/gates/run_gates.py` → 1 file, 2 insertions, 1 deletion.

```json
{
  "task": "P219",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/page_generator/gates/run_gates.py",
      "action": "modified",
      "sha256": "FA75B554E9977C3B1BC9007C362B1665213D1763F373C35F69074A161D7334D8"
    }
  ],
  "counts": {
    "regex_acceptance_strings": "8/8 (5 must-match + 3 must-not-match)",
    "cereals_g6_barcode_fails": "0/20 (cereals_rescored_gates_report.md grep FAIL: barcode)",
    "hummus_g6_barcode_fails": "0/57 (hummus_shelfrel_002_rescored_gates_report.md grep FAIL: barcode)",
    "cereals_score_moves": "0/20 (spine_run_report.json per_shelf cereals)",
    "hummus_score_moves": "0/57 (spine_run_report.json per_shelf hummus_shelfrel_002)"
  },
  "commands_run": [
    {"cmd": "python C:\\Bari\\_p219_self_check.py", "exit_code": 0},
    {"cmd": "python C:\\Bari\\03_operations\\page_generator\\spine_flip.py --set BARI_PALM_HYDRO_V1=on --note \"TASK-330 gate fix verify\"", "exit_code": 1},
    {"cmd": "rg \"FAIL: barcode\" C:\\Bari\\_rescore_staging\\cereals\\cereals_rescored_gates_report.md", "exit_code": 1},
    {"cmd": "rg \"FAIL: barcode\" C:\\Bari\\_rescore_staging\\hummus_shelfrel_002\\hummus_shelfrel_002_rescored_gates_report.md", "exit_code": 1},
    {"cmd": "git -C C:\\Bari diff --stat 03_operations/page_generator/gates/run_gates.py", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "SODIUM_CAUSAL_PATTERN 8-string gate: MUST MATCH 5/5 PASS — 'יורד ל-D בגלל הנתרן הגבוה'→'בגלל הנתרן', 'עוצר ב-C כי הנתרן גבוה'→'כי הנתרן', 'ירד ל-D ובגלל הנתרן'→'ובגלל הנתרן', 'מוגבל שבגלל הנתרן'→'שבגלל הנתרן', 'נחתך בשל הנתרן'→'בשל הנתרן'; MUST NOT MATCH 3/3 PASS — 'סיבים נמוכים...נתרן: 390 מ\"ג'→None, 'גריסי תירס מבושל...נתרן'→None, 'מבשל ... נתרן'→None. ALL 8 ASSERTIONS OK."
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
 M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
 M 03_operations/page_generator/affected_set.py
 M 03_operations/page_generator/copy_stage.py
 M 03_operations/page_generator/spine_flip.py
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/hummus_frontend_v5.json
 M tasks/DISPATCH_BOARD.md
?? affected_set_spine.json
?? tasks/prompts/P217_c3_g6_wordboundary_redteam.md
?? tasks/prompts/P218_c1cursor_cereals_gradeletter_fix.md
?? tasks/prompts/P219_c1grok_g6_sodium_wordboundary_fix.md
?? tasks/prompts/_done/P216_c1cursor_comparisoncontext_carry.md
?? tasks/returns/P216_return.md
?? tasks/returns/P217_return.md
?? tasks/returns/P218_return.md
?? test_acceptance.py
```

### After dispatch

```
M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
 M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
 M 03_operations/bsip2/proto_v0/src/shadow_backtest.py
 M 03_operations/page_generator/affected_set.py
 M 03_operations/page_generator/copy_stage.py
 M 03_operations/page_generator/gates/run_gates.py
 M 03_operations/page_generator/spine_flip.py
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/hummus_frontend_v5.json
 M tasks/DISPATCH_BOARD.md
?? affected_set_spine.json
?? tasks/prompts/P219_c1grok_g6_sodium_wordboundary_fix.md
?? tasks/prompts/_done/P216_c1cursor_comparisoncontext_carry.md
?? tasks/prompts/_done/P217_c3_g6_wordboundary_redteam.md
?? tasks/prompts/_done/P218_c1cursor_cereals_gradeletter_fix.md
?? tasks/returns/P216_return.md
?? tasks/returns/P217_return.md
?? tasks/returns/P218_return.md
?? test_acceptance.py
```

### Delta

### New / modified since dispatch
   M 03_operations/bsip2/proto_v0/src/shadow_backtest.py
   M 03_operations/page_generator/gates/run_gates.py
  ?? tasks/prompts/_done/P217_c3_g6_wordboundary_redteam.md
  ?? tasks/prompts/_done/P218_c1cursor_cereals_gradeletter_fix.md
### Removed / cleaned since dispatch
  ?? tasks/prompts/P217_c3_g6_wordboundary_redteam.md
  ?? tasks/prompts/P218_c1cursor_cereals_gradeletter_fix.md
