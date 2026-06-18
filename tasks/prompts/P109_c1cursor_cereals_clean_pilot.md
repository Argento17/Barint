# P109 — TASK-278 Phase-5: Cereals × Sugar Clean Corrected Pilot (route: C1-CURSOR)
# Run flag-on vs flag-off for same-engine comparison; cereal-only gate; brined byte-id

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS, Phase 5 — corrected pilot)
**Prior pilot:** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/` (REJECTED — baseline contamination)
**Engine:** `03_operations/bsip2/proto_v0/src/score_engine.py`
**Constants:** `03_operations/bsip2/proto_v0/src/constants.py`
**Harness:** `03_operations/bsip2/proto_v0/src/batch_run_cereals_001_shelfrel_pilot.py` (existing, use as template)

---

## Context

P108 pilot returned CHANGES_REQUESTED. Root causes:
1. **Corpus contamination**: The 45-product corpus includes 11 `snack_bar_granola` products alongside 34 `cereal` products. These granola products are OUT OF SCOPE for the cereal shelf-relative enrollment.
2. **Stale baseline**: P108 compared pilot (current engine, flag-on) against synthesis_001 (older engine). Engine drift (W4, FIBER_FERMENT, etc.) caused phantom movements in the 11 granola products and contaminated delta measurements.
3. **Named Inversion A invalid**: 7290100000029 routes to `snack_bar_granola`, not `cereal`. The inversion between a granola product and a cereal product cannot be corrected by the cereal enrollment.

**Engine wiring is CORRECT** (verified by orchestrator):
- `constants.py:516`: `SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit", "cereal"})` ✓
- `constants.py:566-567`: `SUGAR_SHELF_REL_CEREAL_FLOOR = 62`, `SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G = 25.0` ✓
- `score_engine.py:3287-3299`: EV-087 cereal floor branch, uses `min()` as ceiling, category=="cereal" guard ✓
- `shelf_relative_differentiator` at line 2101-2120: asymmetric direction, relief fires as negative penalty through `_coordinate_family` ✓

**This task**: Run a CLEAN pilot that compares flag-on vs flag-off within the SAME current engine, for cereal-only products only. This eliminates baseline contamination.

---

## Step 1: Identify cereal-routed products

From the existing pilot traces at `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/products/`, read the `category` field from each trace's JSON.

Expected split (confirmed by orchestrator):
- 34 products route to `cereal`
- 11 products route to `snack_bar_granola`

Build two lists:
- `cereal_barcodes`: the 34 barcode/product_id strings that route to `cereal`
- `granola_barcodes`: the 11 that route to `snack_bar_granola` (out of scope, excluded from gate)

---

## Step 2: Create a corrected dual-run pilot script

Create: `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py`

This script must:

1. **Load all 45 BSIP1 products** from `03_operations/bsip1/run_cereals_001/output/`
2. **Score each product TWICE:**
   - **Flag-on run**: `BARI_SHELF_RELATIVE_V1 = True` (cereal scope enrolled)
   - **Flag-off run**: `BARI_SHELF_RELATIVE_V1 = False` (disabled)
   - All other flags identical between the two runs (same defaults)
   - Do NOT use synthesis_001 as baseline — the baseline IS the flag-off run
3. **Compute clean delta**: `delta = flag_on_score - flag_off_score` for each product
4. **Filter to cereal-only**: only report gate criteria for the 34 cereal-routed products
5. **Output to**: `02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/`

**Flag settings for BOTH runs (identical except BARI_SHELF_RELATIVE_V1):**
```python
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
# BARI_GLASSBOX_W4: engine default (do NOT override)
```

**Important**: score_engine.py uses module-level `BARI_SHELF_RELATIVE_V1` constant. To run two states:
- Option A: set `os.environ["BARI_SHELF_RELATIVE_V1"]` before `import score_engine`, reload between runs
- Option B: importlib.reload(score_engine) after changing the env var — or better:
- **Option C (recommended)**: Don't reload. Instead, set env var, import score_engine ONCE per process. To get both flag-on and flag-off from the same process, you may need to:
  - Run flag-on pass first (results in memory)
  - Set env var to "off", reload constants + score_engine (importlib.reload)
  - Run flag-off pass
  - OR: run as two separate subprocess calls and combine results

If subprocess approach: write a helper script `batch_run_cereals_002_flagoff.py` that sets flag=off and runs, then combine in the main script.

The cleanest approach: subprocess the two runs, save results to separate JSON files, then combine in a results script. Whichever is simpler — pick one approach and be explicit about what you did.

---

## Step 3: Report gate criteria (cereal-only, clean delta basis)

For the 34 cereal-routed products, using `delta = flag_on_score - flag_off_score`:

Report all 11 criteria from the revised gate (P110 Product Agent will provide a revised gate — use this as the interim gate pending P110):

| # | Criterion | Pass Condition |
|---|---|---|
| 1 | Resolution restored | Fewer products at identical flag-on scores vs flag-off (cleaner spread) |
| 2 | Inversion A | **DROP** — original pair invalid (7290100000029 is snack_bar_granola). Report: "n/a — D6 corpus correction; P110 provides revised criterion" |
| 3 | Inversion B gap widened | flag_on gap (7290100000042 vs 5054568100022) ≥ 5.5pts; also report the clean delta for each |
| 4 | Min movers (cereal-only) | n_cereal_movers ≥ 15 (products where clean delta ≠ 0) |
| 5 | Min grade changes (cereal-only) | n_cereal_grade_changes ≥ 1 |
| 6 | Max absorption (cereal-only) | Among cereal products where SR term fires, ≤40% show delta=0 |
| 7 | Anti-Immunity | No cereal with sugar≥25g reaches grade B (≥70) at flag-on |
| 8 | Floor compliance | All cereal products with sugar≥25g: flag-on score ≤ 62 |
| 9 | No dairy bleed | 0 non-cereal products show non-zero delta (they should have delta=0 since they're out of scope for SR) |
| 10 | Brined byte-id (see Step 4) | run_brined_005 scores byte-identical at flag-on |
| 11 | Flag-off byte-id | For all cereal products: flag_off_score = synthesis_001 committed score (from baseline_dir) — report mismatch count |

For criterion 11: compare flag-off scores from the clean pilot vs synthesis_001 traces at `02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/products/`. Any mismatches indicate engine drift that should be documented.

**Named inversion barcodes for criteria 3:**
- 7290100000042 (5g sugar, baseline_synth=74.9) — should get +1 relief from SR
- 5054568100022 (16g sugar, baseline_synth=70.4) — should get 0 surcharge (r_above=0.22 < 0.5 band threshold)
- Report: flag_off for each, flag_on for each, clean delta for each, gap_before (flag_off diff) vs gap_after (flag_on diff)

---

## Step 4: Run brined byte-id with explicit BARI_SHELF_RELATIVE_V1=True

Run the existing brined script `batch_run_brined_cheeses_005.py` with BARI_SHELF_RELATIVE_V1 explicitly set to True (or confirm the script already does this). Compare output scores with the committed `02_products/brined_cheeses/bsip2_outputs/run_brined_005/` baseline.

Expected: 0 score changes (brined products are not in `{"biscuit", "cereal"}` scope, so the cereal enrollment adds no adjustment).

If the brined_005 script doesn't explicitly set BARI_SHELF_RELATIVE_V1=True, add this before running. Report byte-comparison result (match count / total).

---

## Step 5: Report engine_invariants 342

Run: `python 03_operations/shadow/engine_invariants.py`

Report: PASS or FAIL. This is the standard regression check.

---

## Definition of Done

- [ ] 34 cereal-routed barcodes identified (from pilot traces)
- [ ] `batch_run_cereals_002_clean_pilot.py` created with dual flag-on/flag-off scoring
- [ ] Clean pilot run: `run_cereals_002_clean_pilot/` with 45 traces + `run_record.json`
- [ ] Clean delta computed: `delta = flag_on - flag_off` for all 45 products
- [ ] Gate criteria reported on cereal-only (n=34) basis using clean delta
- [ ] Inversion B gap measured cleanly (flag_on vs flag_off, not vs synthesis_001)
- [ ] Criterion 11 (flag-off drift vs synthesis_001) documented
- [ ] Brined byte-id with BARI_SHELF_RELATIVE_V1=True: pass/fail + evidence
- [ ] engine_invariants 342 PASS confirmed
- [ ] OFF=0 (no Open Food Facts)
- [ ] Engine edits: DO NOT change constants.py or score_engine.py (wiring already correct from P108)

---

## Constraints

- **MEASURED NOT PUBLISHED** — no go-live, no comparison JSON updates
- **OFF ban absolute**
- **Do NOT change engine source files** — only run the clean pilot
- **Frozen milk invariant** — milk byte-identical under all flag combinations
- **Gate C2 (Inversion A) is suspended** — report "n/a" pending P110 gate revision

---

## Return format

Write to `C:\Bari\tasks\returns\P109_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 cereals corrected pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "cereal_barcodes_n": 34,
  "granola_barcodes_n": 11,
  "pilot_run_dir": "02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot",
  "clean_delta_method": "flag_on_score - flag_off_score (same engine, same run)",
  "inversion_b": {
    "7290100000042": {"flag_off": <f>, "flag_on": <f>, "delta": <f>},
    "5054568100022": {"flag_off": <f>, "flag_on": <f>, "delta": <f>},
    "gap_flag_off": <f>,
    "gap_flag_on": <f>,
    "gap_widened_by": <f>,
    "criterion_pass": true/false
  },
  "cereal_movers_clean": <n>,
  "cereal_grade_changes_clean": <n>,
  "absorption_cereal_clean": <f>,
  "anti_immunity_pass": true/false,
  "floor_compliance_pass": true/false,
  "flag_off_vs_synthesis_001_mismatches": <n>,
  "granola_delta_non_zero": <n>,
  "brined_byte_id": {"pass": true/false, "mismatches": <n>},
  "engine_invariants": "342 PASS",
  "off_used": false,
  "gate_results": [
    {"criterion": 1, "name": "resolution_restored", "pass": true/false, "evidence": "..."},
    {"criterion": 2, "name": "inversion_a", "pass": null, "evidence": "n/a — granola product; P110 gate revision pending"},
    {"criterion": 3, "name": "inversion_b_gap", "pass": true/false, "evidence": "gap_flag_off=X, gap_flag_on=Y"},
    {"criterion": 4, "name": "min_movers_cereal", "pass": true/false, "evidence": "n=X"},
    {"criterion": 5, "name": "min_grade_changes_cereal", "pass": true/false, "evidence": "n=X"},
    {"criterion": 6, "name": "max_absorption_cereal", "pass": true/false, "evidence": "absorbed/total=X"},
    {"criterion": 7, "name": "anti_immunity", "pass": true/false, "evidence": "..."},
    {"criterion": 8, "name": "floor_compliance", "pass": true/false, "evidence": "..."},
    {"criterion": 9, "name": "no_granola_bleed", "pass": true/false, "evidence": "granola products delta: X non-zero"},
    {"criterion": 10, "name": "brined_byte_id", "pass": true/false, "evidence": "..."},
    {"criterion": 11, "name": "flag_off_drift_check", "pass": true/false, "evidence": "X mismatches vs synthesis_001"}
  ],
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify the gate.**
