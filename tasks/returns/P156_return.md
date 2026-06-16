# Return: P156

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P156_singlepath_brined_butter_bread.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-16T07:35:50.379917+00:00 |
| Finished | 2026-06-16T07:38:54.489307+00:00 |
| Exit code | 0 |

---

## Output

```
Reading the P156 task prompt and related context.
Exploring live pages, run directories, and score provenance.
Creating the brined config and running the generator; butter and bread are blocked.
## P156 / TASK-296 Piece A — Return Block

### brined_cheeses

| Field | Value |
|---|---|
| **Chosen run** | `run_brined_005` — `final_score_estimate` matches all 36 live barcodes on rounded comparison; grades match floor policy (0 grade mismatches). Evidence: `02_products/brined_cheeses/bsip2_outputs/run_brined_005/verification_table.csv` |
| **Corpus dir** | `03_operations/bsip1/run_brined_cheeses_002/output` (per live `_meta.provenance`: hygiene-cleaned) |
| **Config** | `03_operations/page_generator/configs/brined_cheeses.json` |
| **Counts** | run-universe **48**, excluded **12**, generated **36**, live **36** |
| **Score mismatch** | **33/36** (strict equality — live uses rounded integers, generator emits trace floats e.g. live `85` vs trace `84.8`) |
| **Grade mismatch** | **0/36** |
| **Self-gate** | exit **0** |
| **Verdict** | **DRIFT-FOUND** |

**Finding:** Live `_meta.product_count=48` is stale; `brined_cheeses_frontend_v2.json` contains only **36** products. The 12 exclusions are the exact v1→v2 editorial drops.

**Score distributions (36 shared barcodes):**
- Live: min/max/median/stdev/mode = `46/85/72.0/9.48/(72×6)`; grade dist `A:9 B:20 C:5 D:2`
- Generated: min/max/median/stdev/mode = `46.0/85.4/72.45/9.48/(84.8×2)`; grade dist `A:9 B:20 C:5 D:2` (identical)

---

### butter — config omitted

| Field | Value |
|---|---|
| **Chosen run** | `butter_run_003` — score/grade provenance **0/31** mismatches vs live (strict) |
| **Corpus dir** | **NONE** — no `03_operations/bsip1/<run>/output` with per-file `bsip1_*.json`; corpus exists only as merged array `02_products/butter/bsip1_outputs/butter_bsip1_merged.json` (incompatible with `generate_page.py` loader) |
| **Launch blocker** | **20/31** live displayed products carry `ingredients_raw_provenance.source: "open_food_facts"` in `butter_bsip1_merged.json` (TASK-238 / OFF ban) |
| **Verdict** | **BLOCKED** (OFF on live + no standard corpus path) |

8 run-universe barcodes excluded from live (39→31): `3274932103857`, `3451790562990`, `7290000066035`, `7290006325046`, `7290019635130`, `7290108507997`, `7290116932033`, `7290117263563` (2 OFF-banned, 1 additive_spread, 5 editorial deploy drops).

---

### bread — config omitted

| Field | Value |
|---|---|
| **Candidate run** | `run_bread_008_headpin` — **no `products/` trace tree** (`bsip2_trace.json` per subdir required by generator) |
| **Live page** | 19 products, only **4** have barcodes; **15** have `barcode: null` |
| **Score provenance** | `run_record.json` reports `exact_match_count: 2/24`, `reproduction_rate: 0.083` vs live |
| **Verdict** | **NO-MATCHING-RUN** |

Bread traces live in flat `02_products/bread_retail_003/bsip2/bsip2_*.json` (256 files), not the `generate_page.py` layout. `bread_light` correctly not used.

---

### Files changed

| File | Action |
|---|---|
| `03_operations/page_generator/configs/brined_cheeses.json` | created |
| `03_operations/page_generator/configs/_generated_brined_cheeses.json` | created (scratch) |

Side effect (not in artifacts): `configs/_generated_brined_cheeses_gates_report.md`

---

### Proposed status: **RETURNED**

```json
{
  "task": "P156 / TASK-296",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/configs/brined_cheeses.json", "action": "created", "sha256": "4e60551de6415a79622f4e8e08e9a7b9fddb30d3fd09ed68ddf4c31bc7932206"},
    {"path": "03_operations/page_generator/configs/_generated_brined_cheeses.json", "action": "created", "sha256": "59dd0d7b1a30933f48586111a5a9a0badec938e635ad96a55794345fa936bea6"}
  ],
  "counts": {
    "brined_run_universe": "48/48 (run_brined_005 trace dirs)",
    "brined_excluded": "12/48 (config exclusions list)",
    "brined_generated": "36/36 (generate_page.py _meta.product_count)",
    "brined_live": "36/36 (brined_cheeses_frontend_v2.json products[]; _meta.product_count=48 is stale)",
    "brined_barcode_set_parity": "36/36 (python parity: gen_set == live_set)",
    "brined_score_mismatch_strict": "33/36 (python parity: score != live score)",
    "brined_grade_mismatch": "0/36 (python parity)",
    "brined_self_gate": "0/0 exit_code (generate_page.py self-gate)",
    "butter_live_off_contaminated": "20/31 (butter_bsip1_merged.json ingredients_raw_provenance.source scan)",
    "butter_corpus_standard_format": "0/1 (no 03_operations/bsip1 butter run with bsip1_*.json per-file corpus)",
    "bread_trace_tree": "0/1 (run_bread_008_headpin/products/ missing)",
    "bread_live_null_barcode": "15/19 (bread_frontend_v2.json)",
    "bread_score_exact_match": "2/24 (run_bread_008_headpin/run_record.json head_vs_live)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/generate_page.py --config configs/brined_cheeses.json --out configs/_generated_brined_cheeses.json --timestamp 2026-06-16T00:00:00Z", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/configs/_p156_verify.py (barcode+score+grade parity vs live)", "exit_code": 0}
  ],
  "not_done": [
    "butter.json config — blocked: no standard BSIP1 corpus_dir + 20/31 live products OFF-contaminated in merged corpus",
    "bread.json config — blocked: no bsip2_trace.json products/ tree; 15/19 live null barcodes; run_record 2/24 exact score match",
    "_generated_butter.json scratch file",
    "_generated_bread.json scratch file",
    "brined strict score parity (33/36 float-vs-rounded-integer drift)"
  ],
  "self_check": "brined: generate_page.py self-gate exit 0; barcode set 36/36 identical; grade 0/36 mismatch; score 33/36 strict mismatch (DRIFT-FOUND). butter: STOP — 20/31 live OFF markers. bread: NO-MATCHING-RUN — no products/ trace tree."
}
```

### Verify (orchestrator)

1. `03_operations/page_generator/configs/brined_cheeses.json:1` — config shape, 12 exclusions, corpus/run paths
2. `03_operations/page_generator/configs/_generated_brined_cheeses.json` — 36 products, `_meta.scored_count=48`, `_meta.exclusions` length 12
3. Re-run generate command → exit 0
4. Confirm `butter_bsip1_merged.json` OFF markers on live barcodes (launch blocker)
5. Confirm `run_bread_008_headpin/` has no `products/` subdirectory
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
?? tasks/TASK-296.md
?? tasks/prompts/P156_singlepath_brined_butter_bread.md
```

### After dispatch

```
M tasks/DISPATCH_BOARD.md
?? 03_operations/page_generator/configs/_generated_brined_cheeses.json
?? 03_operations/page_generator/configs/_generated_brined_cheeses_gates_report.md
?? 03_operations/page_generator/configs/brined_cheeses.json
?? tasks/TASK-296.md
?? tasks/prompts/P156_singlepath_brined_butter_bread.md
```

### Delta

### New / modified since dispatch
  ?? 03_operations/page_generator/configs/_generated_brined_cheeses.json
  ?? 03_operations/page_generator/configs/_generated_brined_cheeses_gates_report.md
  ?? 03_operations/page_generator/configs/brined_cheeses.json
  M tasks/DISPATCH_BOARD.md
