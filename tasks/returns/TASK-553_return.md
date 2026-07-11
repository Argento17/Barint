# TASK-553 Return — build_copy_inputs.py hygiene: margin gate + de-hardcode S_VERBATIM

**Date:** 2026-07-11
**Agent:** Data Agent (claude-sonnet-4-6)
**Status:** RETURNED

---

## What was done

### Fix 1: Superlative margin gate (superlatives_allowed_policy_v1.md rules 2–3)

`superlatives_for()` in `build_copy_inputs.py` now enforces all 5 policy conditions from `superlatives_allowed_policy_v1.md`:

**Rule 1 (Uniqueness):** was already enforced — unchanged.

**Rule 2 (Corpus n >= 12):** added `passes_n_gate()` — withholds any token when the metric has fewer than 12 non-null observations in the corpus. All three cereals metrics clear this (protein n=20, kcal n=20, sugar n=19). A category with fewer than 12 scorable products will not mint any superlative.

**Rule 3 (Margin >= 10% of corpus range):** added `passes_margin_gate()` — collects all non-null values for the metric, sorts them, computes the gap from the extreme to the next-closest value, and checks `margin >= (max - min) * 0.10`. If the corpus range is 0 (all values identical), gate fails.

**Rule 4 (Null-awareness):** enforced downstream in `superlatives_context_for()` which attaches `n_measured` / `phrase_as_among_measured` to every granted token. No change needed in this function.

**Rule 5 (Driver relevance):** the whitelist already covers only core metrics (protein, energyKcal, sugar). Sodium is excluded by explicit ruling comment. Tier-2 non-core metric driver-chain check is a CANNOT-COMPUTE condition documented in code comment — it requires the BSIP2 trace to be passed to `superlatives_for()` and no non-core metric is in the whitelist today, so the check is vacuously satisfied by omission.

**CANNOT-COMPUTE conditions explicitly flagged in code:**
- Rule 5 tier-2 driver-chain check for non-core metrics: requires passing the trace to `superlatives_for()`. Since no non-core metric is in the whitelist, this is satisfied by omission. A code comment at the function's docstring explicitly states this.

**Effect on existing double-call:** Lines 369–370 in the original code called `superlatives_for(p, stats)` twice. Fixed to compute once into `sup_allowed` and pass the variable to both `superlatives_allowed` and `superlatives_context_for()`.

---

### Fix 2: De-hardcode S_VERBATIM

The module-level `S_VERBATIM` global (hardcoded with yogurt barcodes + Hebrew text) is **removed** from `build_copy_inputs.py`.

**New architecture:**
1. Approved S-grade verbatim copy lives in `s_verbatim/<category-slug>.json` (same directory as the script). Each file is a JSON dict: barcode → `{insightLine, s_grade_explanation}`. Metadata keys prefixed with `_` are stripped. Missing file = empty dict (safe for categories with no S products).
2. `_load_s_verbatim(category)` loads the file for this category slug at runtime.
3. `s_products` in `_meta` is now derived from the run's actual products whose `grade == "S"` (read from page JSON), not from any hardcoded dict.
4. Per-product `s_verbatim` field is populated from the external file. If a product is grade=S but has no verbatim entry, the script logs a WARNING (escalation to Nutrition Agent required) and the author writes normal copy.

**New file created:** `s_verbatim/yogurt-spoonable.json` — contains the two Nutrition-approved yogurt S-grade verbatim entries (moved byte-for-byte from the old global, approval provenance preserved in `_source` metadata).

---

## Proof runs

### Cereals

```
python 03_operations/page_generator/copy/build_copy_inputs.py \
  --config 03_operations/page_generator/configs/cereals.json \
  --page 03_operations/page_generator/outputs/cereals_generated_v2.json \
  --out 03_operations/reports/scratch/task553_cereals_fact_sheets.json
```

Output: `Wrote 20 fact sheets`, `Ambiguous drivers: 0`, `cap_misclaim_risk flagged: 16/20`

**s_products = []** — cereals has no S-grade products (derived from page grades, not from a hardcoded dict).

**Rice-apple (7297488199590) before/after:**
- BEFORE: `superlatives_allowed: ["lowest_sugar"]`
- AFTER: `superlatives_allowed: []` — revoked by margin gate (gap=0.4g, threshold=2.61g = 10% of 26.1g range)

**Before/after diff (all 20 cereals products):**
- BEFORE: 3 tokens granted — `highest_protein:1, lowest_kcal:1, lowest_sugar:1`
- AFTER: 1 token granted — `highest_protein:1`
- REVOKED: `lowest_kcal` (Vitabix, gap=9.0kcal < threshold=9.8kcal; margin tight but below gate) + `lowest_sugar` (rice-apple, gap=0.4g < threshold=2.61g)
- NEW GRANTS: 0

Note on `lowest_kcal` revocation: The gap is 9.0kcal on a 98kcal range (9.2%). This is a genuinely meaningful gap, but the policy states exactly "10% of corpus range." The gate correctly implements the policy as written. If the owner and Nutrition Agent decide to lower the threshold for kcal, that is a scoring-rule change requiring co-sign — flagged here as a data observation, not a blocker.

### Yogurt (spoonable)

```
python 03_operations/page_generator/copy/build_copy_inputs.py \
  --config 03_operations/page_generator/configs/yogurt_spoonable.json \
  --page 02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_spoonable_FINAL_v2.json \
  --out 03_operations/reports/scratch/task553_yogurt_spoonable_fact_sheets.json
```

Output: `Wrote 52 fact sheets`, `Ambiguous drivers: 0`, `cap_misclaim_risk flagged: 31/52`

**s_products = ['7290112336712', '7290110565527']** — derived from page JSON grade==S.

Both S products have `s_verbatim` attached (keys: `insightLine`, `s_grade_explanation`) from `s_verbatim/yogurt-spoonable.json`. No `s_verbatim` field appears on any non-S product.

---

## Tests

File: `03_operations/page_generator/copy/test_build_copy_inputs.py`

9 tests covering:
- T1: margin_gate GRANT
- T2: margin_gate REVOKE (rice-apple analog)
- T3: margin_gate boundary revoke (margin = threshold - epsilon)
- T4: n_gate revoke (n=11 < 12)
- T5: S-derivation WITH S products (grade-derived + external file verbatim)
- T6: S-derivation WITHOUT S products (cereals; empty dict)
- T7: Real cereals regression (rice-apple revoked, Vitabix protein granted, s_products=[])
- T8: Flat corpus (range==0 → no grant)
- T9: Tie at extreme (rule 1 uniqueness withholds)

**Result: 9/9 PASS (pytest-9.0.3, exit 0)**

---

## Files touched

| File | Action |
|---|---|
| `03_operations/page_generator/copy/build_copy_inputs.py` | modified |
| `03_operations/page_generator/copy/s_verbatim/yogurt-spoonable.json` | created |
| `03_operations/page_generator/copy/test_build_copy_inputs.py` | created |
| `03_operations/reports/scratch/task553_cereals_fact_sheets.json` | created (scratch, proof only) |
| `03_operations/reports/scratch/task553_yogurt_spoonable_fact_sheets.json` | created (scratch, proof only) |

**NOT touched:** no live comparison JSON, no bari-web, no scores, no grades.

---

## Spec-conflict notes

None. The implementation is faithful to the spec. The `lowest_kcal` revocation on Vitabix (gap 9.0kcal vs 9.8kcal threshold) is a correct application of the policy as written — surfaced as an observation for the Nutrition Agent / Product Agent if they wish to adjust the threshold, but this is a scoring-rule decision, not an implementation decision.

---

```json
{
  "task": "TASK-553",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/page_generator/copy/build_copy_inputs.py",
      "action": "modified",
      "sha256": "94ed274c77c1b3c34f7d2afb1192306b958cebddf8911ff5003b8d519a1f5c30"
    },
    {
      "path": "03_operations/page_generator/copy/s_verbatim/yogurt-spoonable.json",
      "action": "created",
      "sha256": "dbf058ebc52f6a20834e0983abc1e2a66b7c8f7b6f23d9fa42fb2da3aadfd1d5"
    },
    {
      "path": "03_operations/page_generator/copy/test_build_copy_inputs.py",
      "action": "created",
      "sha256": "45de937c14702dbb3a30adfc5389ccdbf9a0b79e84fae2c8d5eab8a7ea1076e8"
    },
    {
      "path": "03_operations/reports/scratch/task553_cereals_fact_sheets.json",
      "action": "created",
      "sha256": "9016223746ae2f330de9536bf0fc6f3b2735993e8922b5c793bde5d84f088bbf"
    },
    {
      "path": "03_operations/reports/scratch/task553_yogurt_spoonable_fact_sheets.json",
      "action": "created",
      "sha256": "22dc03409a017b8b255b2d44b2a08cc9c4f0bca42178023b3649df7234fe02f0"
    }
  ],
  "counts": {
    "tests_pass": "9/9 (test_build_copy_inputs.py pytest exit 0)",
    "cereals_tokens_before": "3/20 products (highest_protein:1 lowest_kcal:1 lowest_sugar:1, derived from committed cereals_fact_sheets.json)",
    "cereals_tokens_after": "1/20 products (highest_protein:1 only, median 0 tokens/product, stdev ~0.2, most_common 0(19))",
    "cereals_tokens_revoked": "2/3 (lowest_sugar rice-apple gap=0.4g threshold=2.61g; lowest_kcal Vitabix gap=9.0kcal threshold=9.8kcal)",
    "cereals_s_products": "0/20 (grade==S count derived from scratch output _meta.s_products)",
    "yogurt_s_products": "2/52 (grade==S derived from page JSON: 7290112336712 score=92.6, 7290110565527 score=90.6)",
    "yogurt_s_verbatim_attached": "2/2 S-grade products (insightLine+s_grade_explanation keys confirmed in scratch output)",
    "yogurt_tokens_granted": "1/52 products (lowest_sugar:1, median 0 tokens/product, stdev ~0.14, most_common 0(51))",
    "cannot_compute_flagged": "1/1 policy conditions (Rule 5 tier-2 driver-chain check — requires trace passed to superlatives_for(); no non-core metric in whitelist so vacuously satisfied; explicit code comment at function docstring)"
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/page_generator/copy/build_copy_inputs.py --config 03_operations/page_generator/configs/cereals.json --page 03_operations/page_generator/outputs/cereals_generated_v2.json --out 03_operations/reports/scratch/task553_cereals_fact_sheets.json",
      "exit_code": 0
    },
    {
      "cmd": "python 03_operations/page_generator/copy/build_copy_inputs.py --config 03_operations/page_generator/configs/yogurt_spoonable.json --page 02_products/yogurt_system/bsip2_task515_v3/frontend_out/yogurt_spoonable_FINAL_v2.json --out 03_operations/reports/scratch/task553_yogurt_spoonable_fact_sheets.json",
      "exit_code": 0
    },
    {
      "cmd": ".venv/Scripts/python.exe -m pytest 03_operations/page_generator/copy/test_build_copy_inputs.py -v",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Spec acceptance test: cereals rice-apple lowest_sugar token REVOKED (gap=0.4g < 10%-of-range=2.61g), cereals s_products==[], yogurt s_products==['7290112336712','7290110565527'] with s_verbatim attached from per-category file, 9/9 pytest PASS. OBSERVED: all conditions met per scratch output and pytest run above."
}
```
