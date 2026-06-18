# P173 / HP carb+sodium cluster — detection method + calibration dataset (route: C1-GROK)

**Repo:** `C:\Bari` · branch `task-275-engine-fixes-abc` · HEAD `20fccbd496711d793666a264bbada4b1fa1fa20e`
**Read first:** `C:\Bari\tasks\TASK-322.md` (this is its delivery).
**Lane:** C1-GROK (spec-complete Python build + data run, repo access).

## Objective
Build a **standalone detection method** for the third Fazzino hyper-palatability cluster — **carbohydrates + sodium** — and run it across the live BSIP1 corpora to produce a **calibration / false-positive dataset**. The engine already implements the other two Fazzino clusters (fat+sodium = `HP_FAT_SODIUM`, fat+sugar = `HP_FAT_SUGAR`, see `03_operations/bsip2/proto_v0/src/constants.py:823-835`); the **carb+sodium cluster is absent** and is the one genuine gap. This task builds the METHOD + DATA to measure it. It does **NOT** activate scoring.

### Fazzino published definition for this cluster (use exactly)
- **Carbohydrates + Sodium:** `> 40% of kcal from carbohydrate` **AND** `>= 0.20% sodium by weight` (= `>= 200 mg sodium / 100 g`).
- % kcal from carbohydrate = `(carbohydrate_g_per_100g * 4) / energy_kcal_per_100g * 100`. If energy is missing, derive Atwater from macros only as a documented fallback; if macros insufficient → emit `insufficient_data`, never a fire/no-fire guess.

## What to build
1. **`03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py`** — a standalone module/CLI (run by path, no package import side-effects). For a product's normalized per-100g nutrition it returns `{fires: true|false|insufficient_data, carb_pct_kcal, sodium_mg_100g, reason}`. Import the threshold constants; if you add constants, add them as **inert module-level values prefixed `HP_CARB_SODIUM_*`, default NOT referenced by `score_engine.py`** (no scoring wiring).
2. **Calibration run** over the live shelves. Easiest reliable input: run `python 03_operations/page_generator/rescore_all.py` (produces staging traces with normalized per-100g nutrition under its staging dir), then read each product's nutrition from the traces; OR read the BSIP1 corpora the configs point at. Emit per product: barcode, shelf, carb%kcal, sodium, fires-flag, and the product name.
3. **Dataset output** under `03_operations/bsip2/proto_v0/reports/methods/hp_carb_sodium/`:
   - `calibration.json` — every evaluated product with the fields above.
   - `calibration.md` — summary: total evaluated (named denominator), N fired, N insufficient_data, fire-rate per shelf, and a **manual false-positive review table** of the fired products (is this a refined-carb+salt snack, or a defensible natural/endemic food e.g. bread/cheese — flag candidates the way `risk_of_misuse` in EV-013 warns).

## Boundaries / guards (HARD)
- **NO SCORING.** Do not edit `score_engine.py`, do not add to `HP_FAMILY_BUDGET`, do not change any published score, grade, trace, or live page. This is measurement only. If you cannot do it without touching the live scoring path, STOP and say so.
- **OFF-ban (TASK-238, absolute):** never read, fill, or fall back to Open Food Facts for any field. Nutrition comes only from the in-house BSIP0/BSIP1 panel. If a product's carbs or sodium is missing → `insufficient_data`, never substitute.
- **Do not invent data.** Missing field = insufficient_data.
- New files only (the script + the report dir). Do not modify existing engine modules. Do not commit, do not push.
- **Do not close the task — propose RETURNED** with the dataset paths.

## Return format
Prose summary + the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): `artifacts` (paths + sha256), `counts` (named denominators: products_evaluated, fired, insufficient_data, fired_per_shelf), `commands_run` (with exit codes), `not_done`, and the acceptance-test result. Acceptance test = (a) the method runs over the live corpora with exit 0, (b) `calibration.json` + `calibration.md` exist and the counts reconcile, (c) `git diff` shows **zero** changes to `score_engine.py` / `constants.py` active scoring / any live page JSON. A return without the JSON contract = CHANGES_REQUESTED.
