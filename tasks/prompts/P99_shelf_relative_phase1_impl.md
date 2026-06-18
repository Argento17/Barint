# P99 / Project Rescore Phase-1: implement BARI_SHELF_RELATIVE_V1 mechanism (default-off, byte-identical) (route: C1-CURSOR)

Repo: `C:\Bari`. Engine: `03_operations\bsip2\proto_v0\src\score_engine.py` + `constants.py`.
Task: **TASK-278** (read it). This is **Phase-1 = MECHANISM ONLY**. NO category is enrolled, NO published
score moves, NO pilot. Implement exactly what the two authoritative design docs specify; run the guards.

## Authoritative spec (follow these two files exactly)
1. `C:\Bari\01_framework\bsip2_framework\project_rescore\shelf_relative_design_v1.md` — §1 function contract,
   §2 flag design, §6 no-regression guards. The code in §1.2/§1.3 is the contract.
2. `C:\Bari\01_framework\bsip2_framework\project_rescore\shelf_relative_d7_cosign_v1.md` — the 6 HARD
   conditions in §6 + the asymmetric-direction call in §3. **These conditions OVERRIDE the design defaults.**

## What to implement (score_engine.py + constants.py)
1. **Flag** `BARI_SHELF_RELATIVE_V1 = os.environ.get("BARI_SHELF_RELATIVE_V1","off").lower()=="on"` — declare
   next to the other flags (~L134–158). **Default OFF.**
2. **Stats fns** (design §1.2): `set_shelf_stats(nutrient, median, scale, scale_type)`, `clear_shelf_stats()`,
   `compute_shelf_stats(products, nutrient, scale_type)`. **CONDITION 2 (HARD): the implementation default
   for the distance scale is IQR-primary** — `robust_scale = max(IQR/1.349, 1.4826*MAD, nutrient_min_scale)`,
   NOT population stdev. Keep `scale_type` as an override param but the DEFAULT path computes IQR-primary.
   Reads ONLY `normalized_nutrition_per_100g[nutrient]` (label panel field). **OFF-BAN: no external source.**
   **Backward-compat:** keep `set_shelf_sodium_stats(median, stdev)` working (it may delegate to
   `set_shelf_stats("sodium_mg", median, stdev, "stdev")`).
3. **Differentiator** (design §1.3): `shelf_relative_differentiator(...)` + `_band_lookup(...)`. **CONDITION 3
   (HARD): `min_n` default = 20** (not 10). Must SUPPORT asymmetric direction (penalty P > below-median relief
   B) per co-sign §3 — i.e. the `direction`/mapping logic can produce a bounded below-median relief, not only
   one-sided-high. (No category uses it yet; just support it.)
4. **Constants** (constants.py): add EMPTY scope constants `SUGAR_SHELF_REL_SCOPE = frozenset()`,
   `FATSAT_SHELF_REL_SCOPE = frozenset()` + any band/guard placeholders the call-sites need. **Empty = nothing
   fires until Phase-2 enrollment.**
5. **Call-sites:** add flag-gated calls (`if BARI_SHELF_RELATIVE_V1:`) in the **sugar** and **sat_fat** scoring
   blocks, passing the EMPTY scope constants → returns 0 for every product (no enrollment yet). **DO NOT touch
   the sodium EV-056 block (`_shelf_sodium_active`) — coexistence, design §2.2 / co-sign §8.** Do NOT add a
   sodium call-site (EV-056 owns sodium; its migration is a separate future D7).

## Boundaries / guards
- **Default-off byte-identical** is the contract. With the flag OFF, the engine must be byte-identical to HEAD.
- **NO category enrolled** (scopes empty). Even flag-ON must move 0 scores (empty scope + guards).
- **OFF-BAN absolute** — label fields only.
- Do NOT enroll biscuits, do NOT set any `formulation_absolute_floor`, do NOT run a pilot. That is Phase-2.

## Run the 6 no-regression guards BEFORE declaring done (CONDITION 6) — paste each command's real output:
- **G1 frozen milk byte-identical (flag ON):** re-score `run_005_headpin` with `BARI_SHELF_RELATIVE_V1=on` →
  0/20 scores move vs committed baseline.
- **G2 all published byte-identical (flag OFF):** re-score the published categories with the flag OFF →
  0 movement (this is the default-off proof).
- **G3 invariants:** `python C:\Bari\03_operations\bsip2\proto_v0\tests\engine_invariants.py` → 342 PASS.
- **G4 EV-056 path intact:** re-score brined corpus with `BARI_GRAD_SODIUM_V1=on` +
  `BARI_SODIUM_SHELF_RELATIVE_V1=on` + `BARI_SHELF_RELATIVE_V1=off` → byte-identical to brined baseline.
- **G5 monotonicity:** synthetic increasing-value suite → `shelf_relative_differentiator` penalty is
  monotonically non-decreasing for one_sided_high.
- **G6 non-scope = zero (flag ON, empty scope):** any category not in scope → 0 surcharge.
- **STOP on any published-score movement** (tripwire-1). If any guard fails, do not merge — report the failure.

## Return format (machine-readable return contract — `01_framework\operations\return_contract_v1.md`)
- Files changed + sha256 each; the 6 guard results with the exact command + output for each; confirm
  `git diff` of score_engine.py with flag OFF would produce byte-identical scores (state how you proved it);
  scope constants are EMPTY; EV-056 block untouched (show the block is unchanged).
- **Do not close — propose `status: RETURNED`.** Orchestrator re-runs G1/G2/G3/G4 independently before accept.
