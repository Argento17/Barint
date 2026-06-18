# Return: P209

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P209_c1cursor_additive_burden_dedupe.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-18T10:54:01.231094+00:00 |
| Finished | 2026-06-18T10:55:59.836572+00:00 |
| Exit code | 0 |

---

## Output

```
## P209 / TASK-329 — RETURNED

Fixed EV-002/EV-003 double-count in `evaluate_additive_burden()`: high-risk emulsifiers already present in the EV-002 at-risk list (matched by canonical name or E-number via `ingredient_taxonomy.resolve_additive`) are excluded from the EV-003 weighted count. EV-002 ×3 remains authoritative.

### Change

In `method_additive_burden.py`:
- Added `_additive_identity_keys()` and `_dedupe_high_risk_against_at_risk()`
- EV-003 `high_risk` component now carries `emulsifiers_raw`, `deduped_against_ev002`, and a one-line `trace_note`

### Acceptance

**1. Cakes barcode 2472148 (before → after)**

| | Index | Breakdown |
|---|---|---|
| Before | **13.0** | 3×3 (EV-002) + 2×2 (EV-003) |
| After | **9.0** | 3×3 (EV-002) + 0×2 (both E466/cmc and E407/carrageenan deduped) |
| Drop | **−4.0** | 2 overlaps × weight 2.0 |

**2. `--calibrate` (821 live traces)**

`burden_band_distribution`: `{"HIGH": 28, "LOW": 4, "MED": 283, "NONE": 506}`

Index distribution: min −1.0, max 10.0, median 0.0, stdev 1.9075, most_common 0.0 (504). Histogram: `{-1:2, 0:504, 2:4, 3:271, 5:12, 6:14, 8:2, 9:8, 10:4}`.

**Products with index changed: 60/821** (all decreases; overlap-only products).

**3. Scope:** `git diff --stat -- 03_operations/bsip2/proto_v0/src/method_additive_burden.py` — 1 file only (+50/−3).

No scoring path touched. OFF-ban preserved.

```json
{
  "task": "TASK-329",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/src/method_additive_burden.py",
      "action": "modified",
      "sha256": "15993dd45a4086b5019691bf1985c1e70a58dc13651f584b6ff9f96062bc4bcc"
    }
  ],
  "counts": {
    "cakes_2472148_index_before_after": "13.0→9.0 (bsip2_trace.json cakes shelfrel)",
    "products_index_changed": "60/821 (live shelf BSIP2 traces via page_generator configs)",
    "burden_band_HIGH": "28/821",
    "burden_band_LOW": "4/821",
    "burden_band_MED": "283/821",
    "burden_band_NONE": "506/821",
    "additive_burden_index_min": "-1.0/821",
    "additive_burden_index_max": "10.0/821",
    "additive_burden_index_median": "0.0/821",
    "additive_burden_index_stdev": "1.9075/821",
    "additive_burden_index_most_common": "0.0(504)/821"
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/bsip2/proto_v0/src/method_additive_burden.py --single 02_products/cakes_hard_cookies/bsip2_outputs/run_cakes_shelfrel_001/products/bsip1_cakes_2472148/bsip2_trace.json",
      "exit_code": 0
    },
    {
      "cmd": "python 03_operations/bsip2/proto_v0/src/method_additive_burden.py --calibrate",
      "exit_code": 0
    },
    {
      "cmd": "git diff --stat -- 03_operations/bsip2/proto_v0/src/method_additive_burden.py",
      "exit_code": 0
    },
    {
      "cmd": "cd 03_operations/bsip2/proto_v0/src && python -c \"...old vs new index comparison across 821 traces...\"",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "cakes 2472148: additive_burden_index 13.0→9.0 (−4.0 = 2 deduped high-risk emulsifiers E466+E407 already in EV-002); --calibrate burden_band_distribution {HIGH:28, LOW:4, MED:283, NONE:506}; 60/821 products index changed; git diff touches only method_additive_burden.py"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
D "research/Bari Ingredient Parser Gap Analysis.pdf"
?? 03_operations/page_generator/scaffold_category.py
?? research/16.08/
?? tasks/TASK-327.md
?? tasks/TASK-328.md
?? tasks/TASK-329.md
?? tasks/prompts/P206_c3_palm_hydro_severity_redteam.md
?? tasks/prompts/P207_c1gemini_palm_hydro_engine_gated.md
?? tasks/prompts/P208_c1grok_parser_identity_additions.md
?? tasks/prompts/P209_c1cursor_additive_burden_dedupe.md
?? tasks/prompts/P210_c2_doublecount_and_scope_verify.md
```

### After dispatch

```
M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
 M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
 M 03_operations/bsip2/proto_v0/src/method_additive_burden.py
 D "research/Bari Ingredient Parser Gap Analysis.pdf"
 M tasks/DISPATCH_BOARD.md
?? 03_operations/page_generator/scaffold_category.py
?? research/16.08/
?? tasks/TASK-327.md
?? tasks/TASK-328.md
?? tasks/TASK-329.md
?? tasks/prompts/P206_c3_palm_hydro_severity_redteam.md
?? tasks/prompts/P207_c1gemini_palm_hydro_engine_gated.md
?? tasks/prompts/P208_c1grok_parser_identity_additions.md
?? tasks/prompts/P209_c1cursor_additive_burden_dedupe.md
?? tasks/prompts/P210_c2_doublecount_and_scope_verify.md
?? tasks/returns/P210_return.md
```

### Delta

### New / modified since dispatch
   D "research/Bari Ingredient Parser Gap Analysis.pdf"
   M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md
   M 03_operations/bsip2/proto_v0/src/method_additive_burden.py
   M tasks/DISPATCH_BOARD.md
  ?? tasks/returns/P210_return.md
  M 03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json
### Removed / cleaned since dispatch
  D "research/Bari Ingredient Parser Gap Analysis.pdf"
