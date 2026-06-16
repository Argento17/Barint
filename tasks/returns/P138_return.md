# P138 Return — TASK-278 Phase-12: EV-094 Hummus x Sodium SR Wire + Pilot

**Agent:** Data Agent
**Phase:** Phase-12 (P138)
**Date:** 2026-06-14
**Status:** RETURNED — 2 criteria failures (C1, C2b); structural conflict flagged; C10 CRITICAL PASS; awaiting Nutrition Agent / Product Agent ruling on C1/C2b

---

## What Was Done

### Step 1: Template Read
Read EV-093 wiring in `constants.py` (lines 650-661) and `score_engine.py` (import block lines 70-79, SR call site lines 2315-2349, Stage 7i lines 3690-3716, extraction at line 3299, result dict lines 3800-3803).

### Step 2: EV-094 Constants (constants.py)
Added after the EV-093 block:
- `SODIUM_SHELF_REL_HUMMUS_MEDIAN = 390.0`
- `SODIUM_SHELF_REL_HUMMUS_IQR = 43.0`
- `SODIUM_SHELF_REL_HUMMUS_SCALE = 31.88`
- `SODIUM_SHELF_REL_HUMMUS_FLOOR = 62`
- `SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG = 395.0`
- `SODIUM_SHELF_REL_HUMMUS_P_MAX = 6`
- `SODIUM_SHELF_REL_HUMMUS_B_MAX = 3`
- `SODIUM_SHELF_SCALE_GUARD_HUMMUS = 10.0` — hummus-specific variance guard (IQR-scale=31.88 > 10mg); separate from salty_snack guard (100mg) which would suppress all SR for hummus
- `HUMMUS_PRODUCT_CATEGORIES = frozenset({"hummus_spread", "hummus_and_savory_dips"})`

### Step 3: score_engine.py Wiring (5 sub-steps)
**3a. Import:** Added `SODIUM_SHELF_SCALE_GUARD_HUMMUS` and all EV-094 constants to import block.

**3b. evaluate_guardrails signature:** Added `bsip_hummus_product_category: str | None = None` parameter.

**3c. EV-094 SR call site** (after EV-093 block, in SODIUM_LOAD family):
- Scope guard: `bsip_hummus_product_category in HUMMUS_PRODUCT_CATEGORIES`
- Q4 guard: `sodium < 700`
- Q5-B guard: `evaluation_status != "insufficient_data"`
- `scope_categories = frozenset({"sauce_spread"} | set(HUMMUS_PRODUCT_CATEGORIES))` — includes router category since hummus routes to `sauce_spread`
- `low_variance_guard = SODIUM_SHELF_SCALE_GUARD_HUMMUS` (10mg) — critical fix: original `SODIUM_SHELF_SCALE_GUARD_SALTY_SNACK` (100mg) suppressed ALL hummus SR since scale=31.88 < 100
- `direction="asymmetric"`, `normalize_distance=True`

**3d. Stage 7j floor** (true floor using `max()`, not ceiling):
- Fires when: flag=on AND in-scope AND sodium in [395mg, 700mg) — Q4 guard added to exclude Na>=700
- `score_after_penalty = max(score_after_penalty, 62)` — raises low-scoring products to 62 minimum
- Original implementation used `min()` (ceiling) which was a bug; corrected to `max()` (floor)

**3e. score_product extraction:**
```python
bsip_hummus_product_category = (
    product.get("bsip0_source", {}).get("product_category")
    if isinstance(product.get("bsip0_source"), dict)
    else None
)
```

**3f. Result dict:**
- `ev094_hummus_floor_applied` and `ev094_hummus_floor_note` in score_result

### Step 4: Engine Invariants
Created `03_operations/bsip2/proto_v0/tests/test_engine_invariants.py` (thin wrapper delegating to shadow invariant suite).
Result: **342 products, 6/6 invariants PASS** (BARI_SHELF_RELATIVE_V1=off for flag-off safety check).

### Step 5: Pilot Run
Created and ran `03_operations/bsip2/proto_v0/run_hummus_sodium_pilot.py`.

**Bugs found and fixed during pilot:**
1. `run_bsip2_pipeline()` returned only trace (not score_result); converted to 2-tuple `(trace, score_result)` so `ev094_hummus_floor_applied` is accessible directly from score_result
2. `SODIUM_SHELF_SCALE_GUARD_SALTY_SNACK=100mg` used as hummus guard → suppressed ALL SR (scale=31.88 < 100); fixed with `SODIUM_SHELF_SCALE_GUARD_HUMMUS=10mg`
3. Stage 7j used `min()` (ceiling) instead of `max()` (floor) → C8 compliance failure; fixed
4. Stage 7j did not exclude Q4 products (Na>=700) from the floor → C11 violations; Q4 guard added to Stage 7j
5. C8 gate criterion did not exclude Q4 products → Na>=700 products showing C8 violations; gate updated to check Na in [395mg, 700mg) only

---

## Pilot Gate Results

**Run ID:** `run_hummus_001_sodium_pilot`
**Corpus:** 60 hummus (in-scope) + 54 salty_snack + 20 milk + 88 yogurt + 59 cheese_spread + 37 hard_cheese + 65 juice + 200 maadanim = 583 total

| Criterion | Result | Detail |
|---|---|---|
| C1 directional >=70% | **FAIL** | 36.4% (20/55 correct; high_correct=1/26, low_correct=19/29) |
| C2a grade dist plausible | PASS | 5 grades at flag_on |
| C2b grade absorption <=50% | **FAIL** | 55.0% (33/60 products in grade C) |
| C2c mean abs delta movers | PASS | 8.372 pts |
| C3 named inversion | PASS | Na=6mg (77.1) > Na=12mg (72.0) |
| C4 movers_n >=5 | PASS | 39 movers |
| C5 grade_changes_n >=1 | PASS | 15 grade changes |
| C6 dead_zone <=60% | PASS | 35.0% |
| C7 anti-immunity | PASS | 0 violations |
| C8 floor compliance [395-700mg) | PASS | 0 violations |
| C9 scope bleed = 0 | PASS | 0 non-hummus EV-094 fires |
| **C10 milk delta=0 CRITICAL** | **PASS** | **20/20 (delta=0.0 for all frozen milk scores)** |
| C11 Q4 suppression Na>=700 | PASS | 3 products, delta=0 for all |

---

## SPEC CONFLICT FLAGS (mandatory — cannot self-resolve)

### SC-1: C1 (directional >=70%) vs Floor-Dominant Design

**The conflict:** C1 checks "high-sodium products show delta < 0, low-sodium products show delta > 0" and requires >= 70% correct direction. With the floor mechanism (`max(score, 62)` at Na>=395mg), 23 high-sodium products that baseline at 30-52 get RAISED to 62 (positive deltas). Only one product (Na=480, baseline=64.6) shows negative delta because it started above 62.

**Root cause:** Hummus products score very low on baseline (30-52 range) due to other scoring caps. The floor at 62 dominates the SR penalty signal for all products starting below 62. The floor raises scores by 10-32 pts for most high-sodium products.

**What C1 was designed for:** SR-penalty-dominant enrollments where the SR penalty actively LOWERS high-sodium products below their baseline.

**What EV-094 actually does:** The floor RAISES most high-sodium products (positive delta). Low-sodium products get SR relief (+1 to +3). The directional signal IS present in the FLAG_ON distribution (high-sodium → 62; low-sodium → 68-83) but not in the delta sign for high-sodium.

**Cannot self-approve a spec modification.** Routing to Nutrition Agent for ruling.

**Proposed resolution (for Nutrition Agent consideration):** Replace C1 with "at flag_on, high-sodium hummus (Na>390mg) score <= low-sodium hummus (Na<390mg) at the 25th percentile" — i.e., the differentiation is in the distribution gap, not delta signs. Alternatively, waive C1 and C2b for floor-dominated enrollments where the floor is the primary mechanism.

### SC-2: C2b (grade absorption <=50%) vs Floor Collapsing to Grade C

**The conflict:** 33/60 products (55%) score exactly 62 at flag_on → grade C. The 50% absorption limit is exceeded by 5 percentage points.

**Root cause:** 22 products with Na in [395mg, 700mg) that previously scored below 62 are all raised to exactly 62 → all grade C. The floor creates a grade singularity at 62.

**Cannot self-resolve.** Same ruling request to Nutrition Agent.

**Proposed resolution:** Accept C2b as a known structural characteristic of floor-based enrollment. The differentiation is preserved (5 distinct grade regions), absorption exceeds threshold by 5pp only. Or set floor to 61 (just below C-grade boundary) so products stay at their penalized grades.

---

## Guardrail Confirmations (all binding)

- **OFF ban:** Zero OFF data used. All nutrition from direct product scrape via `normalized_nutrition_per_100g`. `off_used=false` in run_record.
- **Milk frozen scores (C10 CRITICAL):** 20/20 delta=0.0. Run_005_headpin scores UNCHANGED.
- **BARI_SHELF_RELATIVE_V1 default=False:** Engine default unchanged. Pilot sets flag on only for measurement.
- **Engine invariants:** 342 products, 6/6 PASS at flag-off.
- **MEASURED NOT PUBLISHED:** No frontend JSON updated, no live category edits, no deploy.

---

## Artifacts

| Path | SHA256 |
|---|---|
| `03_operations/bsip2/proto_v0/src/constants.py` | `b8ae765eb20840233bddd5c26c1b9f2d921cbd6709dc759036cbb6a58d0e4e42` |
| `03_operations/bsip2/proto_v0/src/score_engine.py` | `8c4fb2837af3d028207aea03b832b5048034ba8226b729b01445d5eb1ff6ac9e` |
| `03_operations/bsip2/proto_v0/run_hummus_sodium_pilot.py` | `aa41474f7c8be8004d3b9981f5dd572c94588e91067c91b8de46f0d24226c899` |
| `03_operations/bsip2/proto_v0/tests/test_engine_invariants.py` | `691f00d0869c88bfd5cda3d79fc9474dcd814b86c1cf89a0ec2995a1a6e6d437` |
| `02_products/hummus/bsip2_outputs/run_hummus_001_sodium_pilot/run_record.json` | `54ddf67d790cb1f557d7b1f0e2972bc6336bcb0be9a9a25e83fa1171d760c9af` |
| `02_products/hummus/bsip2_outputs/run_hummus_001_sodium_pilot/score_table_all.json` | `043f14afdabcea1a734b54921f9a52abe279591ab3438c6f72c5b9e0d56376bf` |

---

## Return Contract (machine-readable)

```json
{
  "task_id": "TASK-278",
  "phase": "P138",
  "agent": "data-agent",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/src/constants.py",
      "sha256": "b8ae765eb20840233bddd5c26c1b9f2d921cbd6709dc759036cbb6a58d0e4e42",
      "role": "EV-094 constants + SODIUM_SHELF_SCALE_GUARD_HUMMUS added"
    },
    {
      "path": "03_operations/bsip2/proto_v0/src/score_engine.py",
      "sha256": "8c4fb2837af3d028207aea03b832b5048034ba8226b729b01445d5eb1ff6ac9e",
      "role": "EV-094 fully wired: import, signature, SR call site, Stage 7j floor (max), extraction, result dict"
    },
    {
      "path": "03_operations/bsip2/proto_v0/run_hummus_sodium_pilot.py",
      "sha256": "aa41474f7c8be8004d3b9981f5dd572c94588e91067c91b8de46f0d24226c899",
      "role": "Pilot script: 60 hummus + 6 prior corpora; 11 gate criteria"
    },
    {
      "path": "03_operations/bsip2/proto_v0/tests/test_engine_invariants.py",
      "sha256": "691f00d0869c88bfd5cda3d79fc9474dcd814b86c1cf89a0ec2995a1a6e6d437",
      "role": "Invariant wrapper; delegates to shadow suite"
    },
    {
      "path": "02_products/hummus/bsip2_outputs/run_hummus_001_sodium_pilot/run_record.json",
      "sha256": "54ddf67d790cb1f557d7b1f0e2972bc6336bcb0be9a9a25e83fa1171d760c9af",
      "role": "Run record with gate criteria, corpus counts, milk C10 verification"
    },
    {
      "path": "02_products/hummus/bsip2_outputs/run_hummus_001_sodium_pilot/score_table_all.json",
      "sha256": "043f14afdabcea1a734b54921f9a52abe279591ab3438c6f72c5b9e0d56376bf",
      "role": "Full score table: 583 products across all corpora"
    }
  ],
  "counts": {
    "hummus_in_scope_n_of_69_total": "60 (9 out-of-scope: 4 eggplant_spread + 5 matbucha_pepper_spread)",
    "hummus_movers_n": "39 of 60",
    "hummus_grade_changes_n": "15 of 60",
    "hummus_dead_zone_pct": "35.0%",
    "hummus_floor_applied_n": "22 of 60 (Na in [395,700)mg, score raised to 62)",
    "hummus_q4_suppressed_n": "3 of 60 (Na>=700: SR+floor both suppressed)",
    "milk_frozen_delta_zero": "20 of 20",
    "engine_invariants": "342 of 342 products, 6 of 6 invariants PASS",
    "total_pilot_corpus": "583 products across 8 corpora"
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/bsip2/proto_v0/tests/test_engine_invariants.py",
      "exit_code": 0,
      "result": "342 products, 6/6 invariants PASS"
    },
    {
      "cmd": "python 03_operations/bsip2/proto_v0/run_hummus_sodium_pilot.py",
      "exit_code": 1,
      "result": "11 criteria evaluated; 9 PASS, 2 FAIL (C1, C2b; structural conflict — see SC-1/SC-2)"
    }
  ],
  "not_done": [
    "C1 criterion: structural conflict between delta-sign check and floor-dominant design — requires Nutrition Agent ruling (SC-1)",
    "C2b criterion: grade absorption 55% > 50% limit due to floor pinning 22 products to grade C — requires Nutrition Agent ruling (SC-2)",
    "trace_writer.py: ev094_hummus_floor_applied not forwarded to assembled trace (read from score_result directly in pilot; trace_writer update deferred until enrollment approved)",
    "Frontend JSON: not updated (MEASURED NOT PUBLISHED)"
  ],
  "spec_conflicts": [
    {
      "id": "SC-1",
      "criterion": "C1 directional >=70%",
      "actual": "36.4% (floor dominates; high-sodium deltas are positive because floor raises them)",
      "routing": "Nutrition Agent",
      "proposed_resolution": "Redefine C1 as flag_on distribution gap test OR waive for floor-dominant enrollments"
    },
    {
      "id": "SC-2",
      "criterion": "C2b grade absorption <=50%",
      "actual": "55% (33/60 in grade C due to floor pinning 22 products to exactly 62)",
      "routing": "Nutrition Agent",
      "proposed_resolution": "Accept 55% as structural characteristic OR set floor to 61 to avoid grade singularity"
    }
  ],
  "guardrails": {
    "off_ban": "PASS — zero OFF data",
    "milk_frozen_c10_critical": "PASS — 20/20 delta=0.0",
    "flag_default_off": "PASS — BARI_SHELF_RELATIVE_V1 default unchanged",
    "invariants_342": "PASS — 342/342",
    "measured_not_published": "PASS — no frontend JSON updated"
  }
}
```
