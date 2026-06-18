# P108 — TASK-278 Phase-5: Cereals × Sugar Pilot Rescore (route: C1-CURSOR)
# Wire cereal scope + run measured pilot rescore

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS, Phase 5)
**EV:** EV-087 (D7 co-signed 2026-06-14 by Product Agent, registered at evidence registry line 2093)
**D7 co-sign:** `01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md`
**D6 enrollment spec:** `01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md`
**Engine:** `03_operations/bsip2/proto_v0/src/score_engine.py`
**Constants:** `03_operations/bsip2/proto_v0/src/constants.py`
**Cereals corpus:** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/products/` (45 traces)
**Biscuit biscuit floor branch reference:** find `EV-085` or `SUGAR_SHELF_BISCUIT` in score_engine.py for pattern

---

## Context

TASK-278 Phase-4 governance is complete:
- D6 (Nutrition): cereals × sugar enrolled, stats confirmed (n=45, median=14.0g, IQR=11.0, scale=8.896)
- D7 (Product): scope ratified ("cereal"), bands P6/B3 confirmed, floor=62 at sugar≥25g, EV-087 registered
- Budget raise: **NONE** (Option A) — no SUGAR_CEREAL_BUDGET_RAISE needed

The mechanism (`BARI_SHELF_RELATIVE_V1`) is already in the engine from Phase-1 (P99). The scope is currently
an empty frozenset (`SUGAR_SHELF_REL_SCOPE = frozenset()`). Phase-5 = wire cereals in + run pilot.

**This pilot is MEASURED, NOT PUBLISHED.** No go-live happens here. The orchestrator evaluates the 11-criterion
gate. If it passes, a separate owner go-live step follows (tripwire-1 — first published movement).

---

## Step 1: Read the current engine constants and score_engine

Read `constants.py` to understand the current structure:
- Find `SUGAR_SHELF_REL_SCOPE` — currently `frozenset()` or `frozenset({'biscuit'})`
- Find `SUGAR_SHELF_BISCUIT_BUDGET_RAISE` (or similar) — understand the biscuit budget raise pattern
- Find any floor-related constants (e.g. `SUGAR_SHELF_REL_BISCUIT_FLOOR` or similar)

Read `score_engine.py` to understand the biscuit EV-085 floor branch:
- Find the section where the biscuit formulation_absolute_floor is applied (search for `EV-085` or `biscuit_floor`)
- Understand the exact pattern so you can replicate it for cereals

---

## Step 2: Wire the cereal enrollment into constants.py

Make the following changes to `constants.py`:

```python
# Add "cereal" to the scope (alongside "biscuit" if present, or alone)
SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit", "cereal"})  # or {"cereal"} if biscuit not yet there

# Add cereal-specific floor constants (EV-087)
SUGAR_SHELF_REL_CEREAL_FLOOR = 62          # Anti-Immunity: high-sugar cereal cannot reach B
SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G = 25.0  # Trigger: floor fires when sugars_g >= 25g
```

No SUGAR_CEREAL_BUDGET_RAISE — Product D7 decided Option A (no raise).

---

## Step 3: Wire the cereal floor branch into score_engine.py

Add a cereal floor branch parallel to the existing biscuit EV-085 floor branch. The pattern should be:

```python
# EV-087: cereals × sugar shelf-relative floor (D7 co-signed 2026-06-14)
if router_category == "cereal" and sugars_g is not None and sugars_g >= SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G:
    score = max(score, SUGAR_SHELF_REL_CEREAL_FLOOR)  # or min(score, ...) depending on direction
    # Wait — check the biscuit pattern first. The floor is a CEILING that prevents high-sugar
    # cereals from scoring too high (it's an upper bound, not a lower bound)
    # floor here means: score = min(score, SUGAR_SHELF_REL_CEREAL_FLOOR)
    # because the floor PREVENTS them from reaching B (70), not keeps them from going too low
```

⚠️ IMPORTANT: Read how the biscuit floor is applied in the existing EV-085 branch before implementing.
The "formulation_absolute_floor" is a MAXIMUM SCORE CEILING for high-sugar products (prevents them from
reaching A/B), not a minimum floor. Apply the same logic.

---

## Step 4: Verify compute_shelf_stats() yields scale ≈ 8.896

Before running the rescore, call `compute_shelf_stats()` (or equivalent) on the cereals corpus sugar values.
Extract `sugars_g` from all 45 traces' `L1_observed_signals` and compute IQR-primary scale:
```
scale = max(IQR/1.349, 1.4826 * MAD, 1.4)
```
Confirm scale ≈ 8.896. If it diverges >0.5 from 8.896, STOP and flag — recalibration needed before pilot.

---

## Step 5: Run the pilot rescore

Run the engine on all 45 cereals products with:
- `BARI_SHELF_RELATIVE_V1 = True` (flag on)
- Scope containing `"cereal"`
- Stats: median=14.0, scale=8.896
- Bands: Surcharge [0,0.5)→0, [0.5,1.0)→1, [1.0,1.5)→2, [1.5,2.5)→4, [2.5,∞)→6
- Relief: [0,0.5)→0, [0.5,1.5)→1, [1.5,3.0)→2, [3.0,∞)→3
- Floor: 62 at sugar≥25g

Save results to: `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/`

Include a `run_record.json` with:
- engine_flag: BARI_SHELF_RELATIVE_V1=True
- scope: ["cereal"]
- stats_used: {median: 14.0, scale: 8.896}
- bands: [surcharge list, relief list]
- floor: {value: 62, threshold_g: 25.0}
- n_total: 45
- n_movers: <count>
- n_grade_changes: <count>
- absorption_summary: {absorbed: <count>, fired: <count>, absorption_rate: <float>}
- grade_changes: [list of {barcode, from_grade, to_grade, score_before, score_after}]
- flag_off_vs_committed_mismatches: <count (pre-existing TASK-271 harness artifact acceptable)>
- safety: {dairy_bleed: false, brined_byte_identical: true}
- off_used: false

---

## Step 6: Report all 11 pilot gate criteria

For each criterion, state PASS or FAIL with evidence:

| # | Criterion | Pass Condition | Result |
|---|---|---|---|
| 1 | Resolution restored | Fewer tied scores vs baseline | ? |
| 2 | Inversion A corrected | 7290100000029 ranks ABOVE 5054568100011 post-SR | ? |
| 3 | Inversion B gap widened | gap 7290100000042 vs 5054568100022 ≥ 5.5pts | ? |
| 4 | Min movers | n_movers ≥ 15 | ? |
| 5 | Min grade changes | n_grade_changes ≥ 1 | ? |
| 6 | Max absorption | ≤ 40% (≤18/45) show zero net movement despite term firing | ? |
| 7 | Anti-Immunity | No cereal with sugar≥25g reaches grade B (≥70) | ? |
| 8 | Floor compliance | All 9 products with sugar≥25g: composite score ≤ 62 | ? |
| 9 | No dairy bleed | 0 non-cereal products moved | ? |
| 10 | Brined byte-id | run_brined_004 (or run_brined_005) byte-identical at flag-on | ? |
| 11 | Flag-off byte-id | BARI_SHELF_RELATIVE_V1=off → zero movement vs committed baseline | ? |

**Agent does NOT decide the gate pass/fail — report the raw numbers and let the orchestrator judge.**

---

## Definition of Done

- [ ] constants.py updated: "cereal" in SUGAR_SHELF_REL_SCOPE, SUGAR_SHELF_REL_CEREAL_FLOOR=62, threshold=25g
- [ ] score_engine.py updated: EV-087 cereal floor branch added
- [ ] compute_shelf_stats() scale verified ≈ 8.896 from actual trace values
- [ ] Pilot rescore run: `run_cereals_001_shelfrel_pilot/` created with 45 traces + run_record.json
- [ ] All 11 gate criteria reported (PASS/FAIL with evidence)
- [ ] No-regression: flag-off byte-identical + brined byte-identical (criteria 10+11)
- [ ] Distribution reported: new dist vs baseline dist (C/D/E counts + score range)
- [ ] engine_invariants 342 PASS confirmed
- [ ] OFF=0 confirmed (no Open Food Facts)
- [ ] Engine edits COMMITTED (this is the first time the engine actually changes for cereals)

---

## Constraints

- **MEASURED NOT PUBLISHED** — no go-live, no comparison JSON updates
- **OFF ban absolute** — no Open Food Facts
- **EV-085 biscuit path must remain byte-identical** — adding cereal scope must not alter biscuit behavior
- **Frozen milk invariant** — milk 20/20 byte-identical under any flag combination
- **No invented data** — all stats from actual traces only

---

## Return format

Write return to `C:\Bari\tasks\returns\P108_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 cereals pilot rescore",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "scale_verified": {"computed": <float>, "expected": 8.896, "within_tolerance": true},
  "pilot_run_dir": "02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot",
  "n_total": 45,
  "n_movers": <n>,
  "n_grade_changes": <n>,
  "absorption_rate": <float>,
  "baseline_dist": {"C": n, "D": n, "E": n},
  "pilot_dist": {"A": n, "B": n, "C": n, "D": n, "E": n},
  "inversion_a": {"barcode_a_score_after": <float>, "barcode_b_score_after": <float>, "direction_correct": true/false},
  "inversion_b": {"gap_after": <float>, "gap_before": 4.5, "gap_widened": true/false},
  "gate_results": [
    {"criterion": 1, "name": "resolution_restored", "pass": true/false, "evidence": "..."},
    ... all 11 criteria ...
  ],
  "gate_overall": "PASS|FAIL",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "constants_modified": true,
  "score_engine_modified": true,
  "engine_edits_committed": true,
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify the gate.**
