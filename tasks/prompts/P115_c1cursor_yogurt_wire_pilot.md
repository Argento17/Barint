# P115 — TASK-278 Phase-6: Wire Yogurt × Sugar SR + Run Definitive Pilot (route: C1-CURSOR)
# Implement yogurt SR constants + scope guard + EV-088 floor branch; dual-run pilot; score 11 gate criteria

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (Phase-6 wire + pilot)
**D6 doc:** `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md`
**D7 doc:** `02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md`
**Pattern:** cereals implementation at `03_operations/bsip2/proto_v0/src/score_engine.py` (EV-087 branch, ~L3278–3299) + `constants.py` (SUGAR_SHELF_REL_CEREAL_* pattern)
**Output dir:** `02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_v2/`

---

## Locked parameters (from D7 — DO NOT change these)

| Parameter | Value |
|---|---|
| SUGAR_SHELF_REL_YOGURT_MEDIAN | 5.45 |
| SUGAR_SHELF_REL_YOGURT_IQR | 5.80 |
| SUGAR_SHELF_REL_YOGURT_SCALE | 4.299 |
| SUGAR_SHELF_REL_YOGURT_FLOOR | 62 |
| SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G | 12.0 |
| SUGAR_SHELF_REL_YOGURT_P_MAX | 6 |
| SUGAR_SHELF_REL_YOGURT_B_MAX | 3 |
| Near-median z-threshold | 0.3 (products with \|z\| < 0.3 → delta = 0; still included in trace) |
| Null-sugars treatment | No adjustment (null check → skip SR, delta = 0) |
| Scope guard | `category == "dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES` |

---

## Step 1: Add constants to constants.py

File: `03_operations/bsip2/proto_v0/src/constants.py`

Read the file to find the cereal SR constants block (SUGAR_SHELF_REL_CEREAL_MEDIAN etc.). Add a yogurt block immediately after it with a comment identifying it as EV-088 / P115 / 2026-06-14:

```python
# EV-088 yogurt×sugar shelf-relative (P115, 2026-06-14; n=74 cereal-only computed from run_yogurt_006)
SUGAR_SHELF_REL_YOGURT_MEDIAN = 5.45
SUGAR_SHELF_REL_YOGURT_IQR = 5.80
SUGAR_SHELF_REL_YOGURT_SCALE = 4.299        # IQR-primary: IQR/1.349=4.299
SUGAR_SHELF_REL_YOGURT_FLOOR = 62
SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G = 12.0
SUGAR_SHELF_REL_YOGURT_P_MAX = 6
SUGAR_SHELF_REL_YOGURT_B_MAX = 3
```

Do NOT change any other constants. Do NOT change SUGAR_SHELF_REL_SCOPE (leave it as {"biscuit","cereal"}).

---

## Step 2: Add yogurt SR call site + EV-088 floor branch in score_engine.py

File: `03_operations/bsip2/proto_v0/src/score_engine.py`

### 2a. Understand the existing cereals SR pattern

Read the sugar SR call site (around line 2064) and the EV-087 cereals floor branch (around lines 3278–3299). You need to understand:
- Where `shelf_relative_differentiator()` is called for sugar
- What arguments it takes (category, sugars_g, median, scale, P_max, B_max, near_median_threshold)
- How the cereal floor branch (EV-087) checks `category == "cereal"` and applies `min(score, SUGAR_SHELF_REL_CEREAL_FLOOR)`

### 2b. Add yogurt SR call site

At the sugar SR call site (~L2064), the current code calls `shelf_relative_differentiator()` for `category in SUGAR_SHELF_REL_SCOPE`. Add a parallel branch for yogurt, using the subtype check:

The yogurt SR should fire when ALL of:
- `BARI_SHELF_RELATIVE_V1` flag is True
- `category == "dairy_protein"`
- `category_subtype in CULTURED_YOGURT_SUBTYPES` (constant already in constants.py)
- `sugars_g is not None`

Call `shelf_relative_differentiator()` with the yogurt constants:
- median = `SUGAR_SHELF_REL_YOGURT_MEDIAN`
- scale = `SUGAR_SHELF_REL_YOGURT_SCALE`
- P_max = `SUGAR_SHELF_REL_YOGURT_P_MAX`
- B_max = `SUGAR_SHELF_REL_YOGURT_B_MAX`
- near_median_threshold = `0.3`

Result: `sr_yogurt_sugar` term (analogous to `sr_sugar` for cereals/biscuits).

The `sr_yogurt_sugar` term feeds into the score through the same mechanism as `sr_sugar` (whatever accumulator or direct score modification is used for cereals — follow the exact same pattern). The intent: `score_after_penalty += sr_yogurt_sugar` (positive = relief, negative = penalty).

### 2c. Add EV-088 yogurt floor branch

After the score is accumulated (but before final clamping), add a floor branch analogous to EV-087:

```python
# EV-088: yogurt×sugar shelf-relative floor (P115, 2026-06-14)
if (BARI_SHELF_RELATIVE_V1
        and category == "dairy_protein"
        and category_subtype in CULTURED_YOGURT_SUBTYPES
        and sugars_g is not None
        and sugars_g >= SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G):
    score = min(score, SUGAR_SHELF_REL_YOGURT_FLOOR)
```

Place this branch in the same location relative to the score pipeline as EV-087 (immediately after EV-087 or in the same floor-application block). Use `min()` (not `max()`) — the floor is a CEILING on the final score for high-sugar yogurts.

### 2d. Import/expose new constants

If needed, add `SUGAR_SHELF_REL_YOGURT_*` and `CULTURED_YOGURT_SUBTYPES` to the imports at the top of score_engine.py (check whether constants are imported individually or via `from constants import *`).

---

## Step 3: Run engine_invariants FIRST (before pilot)

```
python 03_operations/shadow/engine_invariants.py
```

Must pass 342/342. If any failure → STOP, do not run pilot, diagnose first.

---

## Step 4: Create pilot script and run

Create `03_operations/bsip2/proto_v0/src/batch_run_yogurt_shelfrel_v2.py` by adapting `batch_run_cereals_002_clean_pilot.py`. Key differences:
- Corpus: run_yogurt_006 products (all 88 barcodes; the 87 yogurt + 1 non-yogurt will be included; the non-yogurt will show delta=0 for scope bleed check)
- **ALSO include milk run_005_headpin products** (all 20 or so milk products) — needed for C10 frozen_byte_id check
- Output dir: `02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_v2/`
- Run ID: `"run_yogurt_shelfrel_v2"`
- Dual run: flag-on (`BARI_SHELF_RELATIVE_V1=True`) vs flag-off (`BARI_SHELF_RELATIVE_V1=False`) — same engine instance, same all other flags
- Clean delta = flag_on_score − flag_off_score (per product)
- Write per-product results to `run_record.json`

Run the pilot:
```
python 03_operations/bsip2/proto_v0/src/batch_run_yogurt_shelfrel_v2.py
```

---

## Step 5: Score the 11 gate criteria

For each criterion, report exact evidence from pilot output:

| # | Criterion | Pass Condition |
|---|---|---|
| C1 | resolution_restored | Fewer tied-score clusters among 74 yogurt products at flag-on vs flag-off |
| C2 | grade_dist_and_magnitude | (A) 0 yogurts sugars≥12g at grade B; (B) ≥2 yogurts sugars≤5g at grade A/S; (C) mean\|delta\|≥0.5; (D) mean delta≥0 for sugars≤5g products |
| C3 | inversion_gap | 7290110321697 flag-on > 7290102397600 flag-on by ≥2.0 pts |
| C4 | min_movers | ≥25 yogurt products with clean_delta ≠ 0 |
| C5 | min_grade_changes | ≥1 yogurt grade change at flag-on vs flag-off |
| C6 | max_absorption | ≤40% absorbed among SR-firing yogurts |
| C7 | anti_immunity | 0 yogurts with sugars_g ≥ 12g at grade B (score ≥ 70) at flag-on |
| C8 | floor_compliance | All sugars≥12g yogurts: flag-on score ≤ 62 |
| C9 | no_scope_bleed | 0 non-yogurt dairy_protein products with non-zero delta; verify milk products explicitly |
| C10 | frozen_byte_id | milk run_005_headpin products byte-identical flag-on vs flag-off — CRITICAL |
| C11 | flag_off_drift | Count of mismatches vs run_yogurt_006 baseline (docs-only, non-blocking) |

**C10 is CRITICAL:** Any milk score movement at flag-on = immediate pilot FAIL. Report exact milk product delta list.

---

## Step 6: Per-product table (all yogurt products, n=87)

Report full per-product table for the yogurt-only products (sorted by sugars_g ascending):
`barcode | sugars_g | flag_off | flag_on | clean_delta | grade_off | grade_on`

Also report milk products: `barcode | flag_off | flag_on | clean_delta` (should all be 0.0).

---

## Definition of Done

- [ ] constants.py: 7 new SUGAR_SHELF_REL_YOGURT_* constants added (no other constants changed)
- [ ] score_engine.py: yogurt SR call site added (subtype guard); EV-088 floor branch added
- [ ] engine_invariants 342 PASS (post-wiring, before pilot)
- [ ] Pilot script created and run: `batch_run_yogurt_shelfrel_v2.py`
- [ ] Output: `run_yogurt_shelfrel_v2/` with traces + `run_record.json`
- [ ] All 11 gate criteria scored (cereal-only, clean delta basis per product)
- [ ] C10 (milk byte-id) explicitly verified: list all milk products with their delta (all must be 0.0)
- [ ] C9 (no scope bleed): all non-yogurt dairy_protein products listed with delta (all must be 0.0)
- [ ] Per-product table (87 yogurt products sorted by sugars_g)
- [ ] OFF=0
- [ ] MEASURED NOT PUBLISHED (no frontend JSON changes, no comp JSON, no go-live)

---

## Constraints

- **MEASURED NOT PUBLISHED** — no comparison JSON, no frontend changes, no go-live, no published scores
- **OFF ban absolute**
- **Do NOT change SUGAR_SHELF_REL_SCOPE** — yogurt uses a separate subtype-based gate, not the scope set
- **Frozen invariant:** milk run_005_headpin byte-identical is MANDATORY. Any milk score movement at flag-on = STOP and report as pilot FAIL.
- **Flag default-off**: `BARI_SHELF_RELATIVE_V1` default remains False; only the pilot script sets it True for the flag-on run
- **Do NOT change cereals or biscuits constants** — only add yogurt constants
- **Do NOT re-run or modify run_yogurt_006** — read it as input only

---

## Return format

Write to `C:\Bari\tasks\returns\P115_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar wire + pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "pilot_run_dir": "run_yogurt_shelfrel_v2",
  "constants_used": {
    "SUGAR_SHELF_REL_YOGURT_MEDIAN": 5.45,
    "SUGAR_SHELF_REL_YOGURT_SCALE": 4.299,
    "SUGAR_SHELF_REL_YOGURT_FLOOR": 62,
    "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": 12.0,
    "SUGAR_SHELF_REL_YOGURT_P_MAX": 6,
    "SUGAR_SHELF_REL_YOGURT_B_MAX": 3
  },
  "scope_guard_used": "category == dairy_protein AND category_subtype in CULTURED_YOGURT_SUBTYPES",
  "milk_byte_id": {
    "pass": true/false,
    "milk_products_checked": <n>,
    "milk_deltas": [{"barcode": "...", "delta": <f>}, ...],
    "any_nonzero_delta": false
  },
  "non_yogurt_dairy_bleed": {
    "non_yogurt_dairy_protein_products": <n>,
    "non_yogurt_delta_nonzero": <n>
  },
  "inversion_1": {
    "7290110321697": {"sugars_g": 9.8, "flag_off": <f>, "flag_on": <f>},
    "7290102397600": {"sugars_g": 13.6, "flag_off": <f>, "flag_on": <f>},
    "gap_flag_on": <f>,
    "criterion_pass_c3": true/false
  },
  "yogurt_movers": <n>,
  "yogurt_grade_changes": <n>,
  "absorption": <f>,
  "gate_results": [
    {"criterion": "C1", "name": "resolution_restored", "pass": true/false, "evidence": "..."},
    {"criterion": "C2", "name": "grade_dist_and_magnitude", "pass": true/false, "evidence": "A: ...; B: ...; C: ...; D: ..."},
    {"criterion": "C3", "name": "inversion_gap", "pass": true/false, "evidence": "gap=<f>"},
    {"criterion": "C4", "name": "min_movers", "pass": true/false, "evidence": "n=<n>"},
    {"criterion": "C5", "name": "min_grade_changes", "pass": true/false, "evidence": "n=<n>"},
    {"criterion": "C6", "name": "max_absorption", "pass": true/false, "evidence": "<n>/<n>=<pct>%"},
    {"criterion": "C7", "name": "anti_immunity", "pass": true/false, "evidence": "..."},
    {"criterion": "C8", "name": "floor_compliance", "pass": true/false, "evidence": "..."},
    {"criterion": "C9", "name": "no_scope_bleed", "pass": true/false, "evidence": "..."},
    {"criterion": "C10", "name": "frozen_byte_id", "pass": true/false, "evidence": "milk products all delta=0: true/false"},
    {"criterion": "C11", "name": "flag_off_drift", "pass": "n/a-docs-only", "evidence": "<n> mismatches"}
  ],
  "per_product_table": [
    {"barcode": "...", "sugars_g": <f>, "flag_off": <f>, "flag_on": <f>, "delta": <f>, "grade_off": "...", "grade_on": "..."},
    ...
  ],
  "engine_invariants": "342 PASS",
  "off_used": false,
  "not_done": []
}
```

**Do not close. Propose RETURNED — orchestrator verifies gate + closes Phase-6 if all 11 criteria pass.**

Machine-readable return contract:

```json
{
  "artifacts_claimed": [
    {"path": "03_operations/bsip2/proto_v0/src/constants.py", "change": "7 SUGAR_SHELF_REL_YOGURT_* constants added"},
    {"path": "03_operations/bsip2/proto_v0/src/score_engine.py", "change": "yogurt SR call site + EV-088 floor branch added"},
    {"path": "03_operations/bsip2/proto_v0/src/batch_run_yogurt_shelfrel_v2.py", "change": "new pilot script"},
    {"path": "02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_v2/run_record.json", "sha256": "<sha>"}
  ],
  "claims_verified_by_agent": false,
  "propose": "RETURNED"
}
```
