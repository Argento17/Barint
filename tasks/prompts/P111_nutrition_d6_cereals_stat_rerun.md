# P111 — TASK-278 Phase-5: D6 Cereals Stats Re-run (route: C1 Nutrition Agent)
# Recompute shelf-relative stats on cereal-only n=34 corpus; update constants.py

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md`
**Prior D6 enrollment:** `02_products/breakfast_cereals/intelligence_bsip2/cereals_sugar_enrollment_v1.md` (n=45 stats, now superseded)
**Pilot traces (source of truth):** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/products/`
**Constants file:** `03_operations/bsip2/proto_v0/src/constants.py`

---

## Context

D6 (P106) computed cereal×sugar shelf-relative stats on the full 45-product corpus:
- `n=45`, `median=14.0g`, `IQR=11.0`, `robust_scale=8.896` (MAD-primary: 1.4826×6.0=8.896)

These stats are WRONG for the enrollment scope. The corpus contains 11 `snack_bar_granola` products alongside 34 `cereal` products. Granola is OUT OF SCOPE for `SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit", "cereal"})`. The stats must be recomputed on the cereal-only n=34 subset.

**Product Agent D7 ruling (P110)**: flagged for D6 re-run because estimated median shift ≥1g (granola products cluster above median; removing them lowers the cereal-only median from ~14g to ~12–13g).

---

## Step 1: Identify the 34 cereal-routed barcodes

From the existing pilot traces at `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/products/`:

For each `bsip1_<barcode>/bsip2_trace.json`, read:
- `category` field
- `L1_observed_signals.sugars_g` (or however sugars_g is stored in the trace)

Build two lists:
- **cereal_products**: barcode + sugars_g for all products where `category == "cereal"` (expected n=34)
- **granola_products**: barcode + sugars_g for all products where `category == "snack_bar_granola"` (expected n=11)

Report both lists in the return.

---

## Step 2: Recompute stats on cereal-only n=34

Using the 34 cereal products' `sugars_g` values:

1. **Median**: `median_cereal = numpy.median([sugars_g for cereal products])`
2. **IQR**: `IQR_cereal = numpy.percentile(sugars_g, 75) - numpy.percentile(sugars_g, 25)`
3. **MAD**: `MAD_cereal = numpy.median(abs(sugars_g - median_cereal))`
4. **Robust scale**: `scale_cereal = max(IQR_cereal/1.349, 1.4826*MAD_cereal, 1.4)` (IQR-primary formula from D7 design)
5. **Low-variance guard**: If `scale_cereal < 1.4`, raise ValueError — do NOT proceed (guard G2 from design)
6. **n≥20 guard**: 34 > 20 ✓ (no issue)

Report all derived values. Verify that `scale_cereal ≠ 8.896` (confirm it changed from the n=45 value).

**IMPORTANT: Do not use n=45 stats in your computation. The input is only the 34 cereal-routed products.**

---

## Step 3: Update constants.py with corrected cereal stats

In `03_operations/bsip2/proto_v0/src/constants.py`, find the existing cereal shelf-relative constants (the ones D6 set in P106 near the SUGAR_SHELF_REL_CEREAL_FLOOR / SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G block, around line 566).

Update:
- `SUGAR_SHELF_REL_CEREAL_MEDIAN` → new median_cereal value
- `SUGAR_SHELF_REL_CEREAL_IQR` → new IQR_cereal value
- `SUGAR_SHELF_REL_CEREAL_SCALE` → new scale_cereal value

(The exact constant names may differ — check what D6 named them. If the stats are stored differently, update however they're stored.)

Add a comment: `# n=34 cereal-only (updated P111, 2026-06-14; prior n=45 was contaminated by 11 snack_bar_granola products)`

**DO NOT change:**
- `SUGAR_SHELF_REL_CEREAL_FLOOR = 62` (unchanged)
- `SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G = 25.0` (unchanged)
- `SUGAR_SHELF_REL_SCOPE` (unchanged)
- Any biscuit constants (unchanged)

---

## Step 4: Verify the update

1. Run `python -c "from src.constants import *; print('CEREAL_MEDIAN:', SUGAR_SHELF_REL_CEREAL_MEDIAN, 'CEREAL_SCALE:', SUGAR_SHELF_REL_CEREAL_SCALE)"` from `03_operations/bsip2/proto_v0/` to confirm new values load.
2. Run engine_invariants: `python 03_operations/shadow/engine_invariants.py` — must still be 342 PASS (constants change is backward-compatible).
3. Quick brined sanity check: If a brined-cheeses batch script exists, confirm it still imports without errors (brined constants are separate; no code path change).

---

## Step 5: Update the enrollment document

Append to `02_products/breakfast_cereals/intelligence_bsip2/cereals_sugar_enrollment_v1.md`:

```markdown
## Addendum: Corpus Correction (P111, 2026-06-14)

**Root cause**: The n=45 corpus included 11 `snack_bar_granola` products. These are out of scope for
`SUGAR_SHELF_REL_SCOPE = {"cereal"}`. Stats recomputed on cereal-only n=34.

**Granola barcodes (excluded)**: [list from Step 1]
**Cereal barcodes (included)**: [list from Step 1]

**Revised stats (n=34 cereal-only):**
- n: 34
- median: <new value>g
- IQR: <new value>
- MAD: <new value>
- robust_scale: <new value>
- low_variance_guard: PASS (scale ≥ 1.4)

**Updated in constants.py:** SUGAR_SHELF_REL_CEREAL_MEDIAN, SUGAR_SHELF_REL_CEREAL_IQR,
SUGAR_SHELF_REL_CEREAL_SCALE

**Floor and threshold unchanged:** FLOOR=62, THRESHOLD=25.0g, SCOPE={"biscuit","cereal"}
```

---

## Anti-Immunity check (re-verify with new stats)

With the revised stats, the maximum SR relief is still bounded by `B_max = 3`. Re-verify:
- EV-087 floor: 62 (unchanged)
- Maximum score above floor: floor(62) + B_max(3) = 65
- 65 < 70 (grade B threshold) ✓

The Anti-Immunity rule holds regardless of median shift (floor and B_max are unchanged).

---

## Definition of Done

- [ ] 34 cereal barcode list + sugars_g extracted from pilot traces
- [ ] 11 granola barcode list extracted
- [ ] New stats computed: median, IQR, MAD, scale (all on n=34)
- [ ] Scale divergence from n=45 documented (expected: meaningful change)
- [ ] constants.py updated with new cereal median/IQR/scale
- [ ] Old values noted in comment
- [ ] engine_invariants 342 PASS with new constants
- [ ] Enrollment document addendum written
- [ ] Anti-Immunity re-verified with new stats

---

## Constraints

- **MEASURED NOT PUBLISHED** — no go-live, no comparison JSON updates, no frontend changes
- **OFF ban absolute** — no Open Food Facts for any field
- **Do NOT change score_engine.py logic** — only constants.py stat values
- **Do NOT change floor (62), threshold (25.0g), or scope** — only the median/IQR/scale
- **Do NOT change biscuit constants** — only cereal-specific ones
- **Frozen milk invariant** — milk byte-identical (unchanged)

---

## Return format

Write to `C:\Bari\tasks\returns\P111_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 D6 cereals stat re-run",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "cereal_n": 34,
  "granola_n": 11,
  "n45_stats": {"median": 14.0, "IQR": 11.0, "scale": 8.896},
  "n34_stats": {
    "median": <f>,
    "IQR": <f>,
    "MAD": <f>,
    "scale": <f>
  },
  "median_shift_g": <f>,
  "scale_shift": <f>,
  "constants_updated": ["SUGAR_SHELF_REL_CEREAL_MEDIAN", "SUGAR_SHELF_REL_CEREAL_IQR", "SUGAR_SHELF_REL_CEREAL_SCALE"],
  "floor_unchanged": 62,
  "threshold_unchanged": 25.0,
  "anti_immunity_recheck": "floor(62) + B_max(3) = 65 < 70 PASS",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "cereal_barcodes_with_sugar": [
    {"barcode": "...", "sugars_g": <f>},
    ...
  ],
  "granola_barcodes_with_sugar": [
    {"barcode": "...", "sugars_g": <f>},
    ...
  ],
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**

After orchestrator accepts P111: a new pilot run (P112) will be dispatched using corrected n=34 stats.
