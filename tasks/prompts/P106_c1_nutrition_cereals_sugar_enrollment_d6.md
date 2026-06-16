# P106 — TASK-278 Phase-4: Cereals × Sugar Enrollment D6 Ruling (route: C1)
# Nutrition Agent — Design the shelf-relative sugar enrollment for breakfast cereals

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS, Phase 4 starting)
**Program design:** `01_framework/bsip2_framework/project_rescore/shelf_relative_design_v1.md`
**D7 co-sign basis:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Prior enrollment example:** `cookies_coffee/methodology/shelf_relative_sugar_enrollment_v1.md` (biscuits)
**Rollout analysis:** `01_framework/bsip2_framework/project_rescore/rollout_spread_analysis_v1.md`

---

## Context

TASK-278 is a Bari-wide program replacing binary Israeli red-label caps with shelf-relative continuous
scoring. The mechanism is implemented (P99: `BARI_SHELF_RELATIVE_V1` default-off in score_engine.py + 
constants.py). The biscuits pilot (P102) failed because biscuits is floor-saturated (0 grade changes).
The yogurt diagnostic (P103) proved the mechanism LANDS on spread categories (8 grade changes, 0% absorption).

**Phase 4 begins here: cereals×sugar is the first PRODUCTION enrollment.**

Why cereals:
- `spread_analysis_raw_v1.json` classifies cereals LAND: IQR 11.0 / scale 8.896 / stdev 17.03 / only
  11.1% floored. Best spread of all surveyed categories.
- Sugar range 0.5g–39g: kids' cereal (39g) vs bran/muesli (0.5g) = the largest honest contrast in Bari's
  product universe. Shelf-relative gives kids' cereal an extra penalty relative to its shelf peers.
- n=45, well above min_n=20 gate.

**This is a D6 ruling only (proposal + stats + spec). NO engine edits, NO rescore, NO EV yet.**

---

## Cereals corpus

Run: `run_cereals_synthesis_001`
Products dir: `C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_synthesis_001\products`

Pre-computed stats (from spread_analysis_raw_v1.json, re-verify from traces):
```
n=45, sugar median=14.0, Q1=8.0, Q3=19.0, IQR=11.0, scale(IQR-primary)=8.896
min=0.5, max=39.0, stdev=10.36
```

**Important note:** some cereals products may LACK sugar data. Count n_with_sugar vs n_total. If n_with_sugar
< 20, flag — may need a fallback or reduced scope.

---

## Your tasks

### 1. Re-derive cereals sugar stats from the 45 trace files

Read the BSIP2 trace JSONs in `run_cereals_synthesis_001/products/`. For each product, extract
`observed_signals.sugars_g` (or `sugars_g` from the nutrition block). Compute:
- n_with_sugar (products that have a non-null sugar value)
- median, Q1, Q3, IQR, MAD
- robust_scale = max(IQR/1.349, 1.4826·MAD, 1.0) [IQR-primary per D7]
- min, max

Confirm they match the pre-computed values above (or explain any discrepancy).

### 2. Identify the router category for cereals

Read `03_operations/bsip2/proto_v0/src/router_v2.py` (or the current router). Find what router category
cereals products are assigned to. The scope constant to update would be something like:
`SUGAR_SHELF_REL_SCOPE` (currently a frozenset around `biscuit`).

For cereals, determine:
- What router category key does a typical cereal like "קורנפלקס" or "גרנולה" or "ברנפלקס" get assigned to?
- Is there a risk of bleed into yogurt/dairy routes? (cereals should route to a category isolated from dairy)
- Name the exact scope key to use (e.g. `cereal`, `breakfast_cereal`, etc.)

### 3. Design the surcharge and relief bands

The biscuit enrollment used: P=6>B=3, scale=5.115, floor=55.
The yogurt diagnostic used: P surcharge [0.5/1.0/1.5/2.5] = [0/1/2/4/8], relief [0.5/1.5/3.0] = [0/2/3/4].

For cereals, design bands appropriate to:
- Scale ≈ 8.896 (bigger than biscuits 5.115 and yogurt 4.299)
- Asymmetric P>B (required by D7)
- The band breakpoints should be in units of robust z-score (r = (x−median)/scale)
- Typical products:
  - Low sugar (0.5–8g): plain bran, muesli, shredded wheat
  - Medium (8–19g): many standard cereals
  - High (19–39g): sweetened kids' cereal
- Relief for low-sugar is genuine (muesli/bran is nutritionally different from Frosties)
- Surcharge for high-sugar should LAND on the high-sugar kids cereal (unlike biscuits)

Propose your bands. Show the implied surcharge/relief for a 39g-sugar product and a 0.5g-sugar product
(confirm the mechanism has room to move on these extremes).

### 4. Design the formulation_absolute_floor (Anti-Immunity gate)

The floor prevents high-sugar cereals from reaching A/B via relief if they're in a wrong bin.
Per D7: `score = clamp(absolute + rel_term, floor, ceiling)` where floor is set so that:
- A product with sugar≥30g CANNOT reach A (≥90 or per category_ceiling)
- The floor should be ≤70 (below B) for anything with sugar≥30g

Given that cereals max score without floor could be ~90+ for a nutrient-dense cereal:
- What absolute floor prevents curve-grading immunity?
- Show: floor + max_relief < 70 (Anti-Immunity proof)

### 5. Find 2+ named ranking inversions

Identify 2 real product pairs in run_cereals_synthesis_001 where the shelf-relative mechanism
should produce a better-justified ranking. For example:
- Product A scores 72/B (medium sugar 15g, lots of fiber/protein) and Product B scores 71/B
  (high sugar 30g, minimal nutrition). After shelf-relative, B should drop relative to A.
- Identify real barcodes from the run traces.

### 6. Check EV registry for next available number

Read `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` and find the highest
existing EV-NNN entry. EV-086 = PHVO governance (line 2064). The next available should be EV-087 or
higher — confirm. Do NOT use EV-084 (project_rescore design) or EV-085 (biscuit enrollment).

---

## Definition of Done

- [ ] Sugar stats re-derived from traces (n_with_sugar, median/IQR/scale confirmed or explained)
- [ ] Router category for cereals named (exact scope key, no bleed risk stated)
- [ ] Surcharge + relief bands specified (asymmetric P>B, band breakpoints in robust z-score units)
- [ ] formulation_absolute_floor specified with Anti-Immunity proof
- [ ] min_n gate confirmed (n_with_sugar ≥ 20)
- [ ] 2+ named inversions with real barcodes from run_cereals_synthesis_001
- [ ] EV number confirmed (next free, ≥ EV-087, not EV-084/085/086)
- [ ] Deliverable written to `01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md`
- [ ] NO engine files modified
- [ ] NO comparison JSON files modified
- [ ] OFF ban absolute (no Open Food Facts)

---

## Constraints

- **DO NOT modify any engine source files** — this is a proposal only
- **DO NOT run any scoring** — stats from existing traces only
- **OFF ban absolute** — no Open Food Facts for any field
- **No existing published score changes** — this task produces a spec, not an outcome

---

## Return format

Write return to `C:\Bari\tasks\returns\P106_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-4 D6 cereals sugar enrollment",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "stats_confirmed": {
    "n_with_sugar": <number>,
    "median": <number>,
    "iqr": <number>,
    "robust_scale": <number>,
    "pre_computed_match": true
  },
  "router_category": "<exact scope key>",
  "router_bleed_risk": "none|low|medium|high",
  "surcharge_bands": [...],
  "relief_bands": [...],
  "formulation_absolute_floor": <number>,
  "anti_immunity_proof": "<floor> + <max_relief> = <sum> < 70",
  "min_n_gate": "PASS",
  "named_inversions": [
    {"barcode_a": "...", "sugar_a": ..., "score_a": ..., "barcode_b": "...", "sugar_b": ..., "score_b": ..., "expected_after": "A drops relative to B"},
    ...
  ],
  "ev_number": "EV-0XX",
  "ev_number_confirmed_free": true,
  "deliverable": "01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md",
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
