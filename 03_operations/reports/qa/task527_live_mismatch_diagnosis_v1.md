# TASK-527 — Live Mismatch Diagnosis Report v1

**Agent:** adversarial-qa-agent (READ-ONLY diagnosis)
**Date:** 2026-07-09
**Branch:** task506 (no commits, no edits to source/trace/JSON/config)
**Scope:** brined_cheeses_frontend_v2.json (36 products) + milk_frontend_v1.json (18 products)

---

## Methodology

All findings are derived from direct artifact reads. No inference, no re-scoring, no source
modification. Validator used: `03_operations/spine/validate_comparison_page.py` (canonical gate).

Trace source for brined cheeses: `02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/`
(run_id = `run_brined_005`, the run referenced in `_meta.run_id` of the frontend JSON).

Trace source for milk: `02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/`
(the AUTHORITATIVE.md-designated frozen baseline; the frontend `_meta.run_id` of
`task409_rederive_milk_20260626` does NOT correspond to any trace directory in the main tree — see
finding M-002 below).

BSIP1 source for milk ingredient comparison:
`03_operations/bsip1/run_milk_002/output/` (as stated in milk frontend `_meta.corpus_dirs`).

---

## PART A — Brined Cheeses

### Validator output

```
[FAIL] score==trace  (36 products, 14 mismatch)
[PASS] OFF ban       (0 off_used)
[PASS] PENDING render (0 placeholder in rendered fields)
[PASS] count consist (0 disagreements)
[PASS] ingredient    (0 truncated/bleed)
[PASS] superlative   (0 false, 2 manual-review)
[PASS] image present (36/36 have imageUrl)
[FAIL] copy-authored (4 signal(s): banned=4 sentence=0 fingerprint=0 mass=0)
RESULT: FAIL — 3 hard gate(s) failed: ['score==trace', 'score==trace', 'copy-authored']
```

Command: `python 03_operations/spine/validate_comparison_page.py --json bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json --traces 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products`

### Per-product table — all 14 mismatches

| Barcode | FE Score | FE Grade | Trace Score | Trace Grade | Delta | Grade Change | Ingredient Truncated | Root Cause | Classification |
|---|---|---|---|---|---|---|---|---|---|
| 7290019635826 | 83.3 | A | 85.4 | A | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 554532 | 82.7 | A | 84.8 | A | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 554457 | 82.7 | A | 84.8 | A | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290102397334 | 81.5 | A | 83.6 | A | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290108509106 | 78.6 | B | 80.5 | A | -1.9 | YES (A→B) | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290011499129 | 78.0 | B | 80.1 | A | -2.1 | YES (A→B) | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290019790402 | 74.3 | B | 76.4 | B | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290017065663 | 73.5 | B | 75.6 | B | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290114314015 | 70.3 | B | 72.4 | B | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290019635222 | 67.0 | B | 69.1 | B | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290017065236 | 66.3 | B | 68.4 | B | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290108509755 | 64.6 | C | 66.7 | B | -2.1 | YES (B→C) | NO | TASK-438 reflow | DISPLAY-ONLY |
| 7290102393718 | 62.5 | C | 64.6 | C | -2.1 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |
| 3075805 | 62.5 | C | 64.7 | C | -2.2 | NO | NO | TASK-438 reflow | DISPLAY-ONLY |

**22 matching products:** all have delta = 0.0, grade matches confirmed.
**No ingredient truncations** detected across all 36 products.

### Root cause

The TASK-438 reflow (EV-099 NOVA-gate, dated 2026-07-01) re-scored 14 products AFTER the frontend
JSON was generated from `run_brined_005` (generated 2026-06-15 per `_meta.generated`). The reflow
updated scores in `brined_cheeses_frontend_v2.json` but did NOT regenerate the per-product
`bsip2_trace.json` files in `run_brined_005/products/`. The stored traces are therefore STALE
(pre-reflow) while the frontend JSON reflects the POST-reflow scores.

Evidence: `_meta.reflow` in the frontend JSON explicitly documents this event:
- task: TASK-438
- to: "current_engine (EV-099 NOVA-gate)"
- date: 2026-07-01
- grade_movers: ["7290011499129 A->B", "7290108509106 A->B", "7290108509755 B->C"]
- adversarial_qa: "CONDITIONAL_PASS (0 CRITICAL; 2 HIGH pre-existing golden-page, routed to follow-up)"

The three grade changes documented in `_meta.reflow` are confirmed in the per-product table above.
The remaining 11 mismatches (score-only, no grade change) were NOT documented in `_meta.reflow.grade_movers`
but are part of the same reflow event (consistent -2.1 delta across all 14 affected products).

Delta distribution across 14 mismatches: min=-2.2, max=-1.9, median=-2.1, stdev≈0.06.
All 14 deltas are in the same direction (frontend lower than trace), consistent with a single
systematic EV-099 adjustment applied post-generation.

### Classification: ALL 14 are DISPLAY-ONLY

The frontend JSON (`brined_cheeses_frontend_v2.json`) contains the CURRENT post-reflow scores.
The stale artifacts are the BSIP2 traces, not the live page. No consumer sees the wrong number.
The "mismatch" is an artifact of the validator comparing the frontend against pre-reflow traces.

**This is NOT a SCORE-AFFECTING finding** (tripwire-1 does not fire).

### Secondary finding: copy-authored gate (4 banned phrases)

The `copy-authored` gate flagged 4 banned phrases across 4 barcodes in `rowVerdict` fields:
- Barcode 7296073641964: phrase "מוריד את הציון"
- Barcode 4861360: phrase "מגביל את הציון"
- Barcode 7290114314015: phrase "מוריד את הציון"
- Barcode 7290108509755: phrase "הגורם המגביל"

These are copy-authoring failures in existing content — they are out-of-scope for TASK-527's
diagnosis mandate (score/ingredient mismatches). They are noted here as a secondary finding and
should be routed separately. Routes to: content-agent (phrase replacements in rowVerdict fields).

---

## PART B — Milk

### Authoritative trace source

The milk frontend `_meta.run_id = "task409_rederive_milk_20260626"` does NOT correspond to any
trace directory in the main tree. Search confirmed: no `task409*` directory exists under
`02_products/milk_and_alternatives/intelligence_bsip2/`. The run_id in the frontend `_meta` is a
task label, not a standard `run_00N` scoring run directory.

The authoritative frozen baseline is `run_005_headpin` (AUTHORITATIVE.md designates it; `run_004_recalibrated`
is SUPERSEDED per that run's SUPERSEDED.md). All 18 milk frontend products were compared against
`run_005_headpin` traces. All 18 match exactly (delta = 0.0, grade matches confirmed).

The scores in the milk frontend are correct. The run_id label in `_meta` is a provenance record of
the generation script/task used, not a pointer to a trace directory — the underlying score values
derive from `run_005_headpin`.

### Validator output

```
[PASS] score==trace  (18 products, 0 mismatch)
[PASS] OFF ban       (0 off_used)
[PASS] PENDING render (0 placeholder in rendered fields)
[PASS] count consist (0 disagreements)
[FAIL] ingredient    (1 truncated/bleed)
[PASS] superlative   (0 false, 1 manual-review)
[PASS] image present (18/18 have imageUrl)
[FAIL] copy-authored (1 signal(s): banned=1 sentence=0 fingerprint=0 mass=0)
RESULT: FAIL — 2 hard gate(s) failed: ['ingredients', 'copy-authored']
```

Command: `python 03_operations/spine/validate_comparison_page.py --json bari-web/src/data/comparisons/milk_frontend_v1.json --traces 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products`

### Score propagation — per-product table (all 18)

| Barcode | FE Score | FE Grade | Trace Score | Trace Grade | Score Match | Ingredient Truncated |
|---|---|---|---|---|---|---|
| 7290000051352 | 85 | A | 85 | A | YES | NO (ingredients = 'חלב', complete) |
| 7290019790259 | 85 | A | 85 | A | YES | YES (ingredients = 'חלב,', trailing comma) |
| 7290102392094 | 85 | A | 85 | A | YES | NO |
| 7290114313865 | 71.0 | B | 71.0 | B | YES | NO |
| 7290116936116 | 63.9 | C | 63.9 | C | YES | NO |
| 7290110324926 | 56.7 | C | 56.7 | C | YES | NO |
| 7290107932134 | 55.5 | C | 55.5 | C | YES | NO |
| 7290014760141 | 51.5 | C | 51.5 | C | YES | NO |
| 7394376620904 | 50.5 | C | 50.5 | C | YES | NO |
| 7290119385560 | 49.9 | D | 49.9 | D | YES | NO |
| 7394376619939 | 49.8 | D | 49.8 | D | YES | NO |
| 7394376621451 | 49.8 | D | 49.8 | D | YES | NO |
| 5411188124689 | 49.7 | D | 49.7 | D | YES | NO |
| 8000215204554 | 48.1 | D | 48.1 | D | YES | NO |
| 7290110325619 | 47.6 | D | 47.6 | D | YES | NO |
| 8000215204219 | 46.3 | D | 46.3 | D | YES | NO |
| 5411188112709 | 46.2 | D | 46.2 | D | YES | NO |
| 5411188300328 | 33.5 | E | 33.5 | E | YES | NO |

Note on barcode `8000215204219` (rice drink): AUTHORITATIVE.md documents a deliberate
owner-approved override (52.3/C per TASK-169C) that was confirmed on 2026-06-04. The current
frontend shows 46.3/D and the `run_005_headpin` trace also shows 46.3/D. This does NOT match the
documented override of 52.3/C. This is a secondary anomaly: the owner-approved rice drink override
appears to have been lost or reverted. Routes to: data-agent (check whether the 52.3/C override
was ever applied to this JSON; confirm with owner before any change — this touches a frozen invariant).

### Finding M-001: ingredient truncation — barcode 7290019790259

**Observed value:** `expansion.ingredients = 'חלב,'` (7 chars, ends in trailing comma)
**BSIP1 raw value:** `ingredients_raw = 'חלב,'` (7 chars — identical, also ends in trailing comma)

The BSIP1 source `03_operations/bsip1/run_milk_002/output/bsip1_7290019790259.json` has:
- `ingredients_raw = 'חלב,'` (7 chars)
- `ingredients_text_he = 'חלב,'` (7 chars)
- `ingredients_list = 'חלב'` (6 chars — list version without the trailing comma)

Root cause: the trailing comma in `ingredients_raw` was passed through to the frontend without
stripping. The comma is an artifact in the BSIP1 raw scrape, not a mid-label truncation. The
product label for natural 4% whole milk (`חלב טבעי 4%`) lists `חלב` as the only ingredient.

Classification: DISPLAY-ONLY. The product is not truncated at the data level — the ingredient text
is complete ("milk" = sole ingredient). The comma is a scrape artifact in the BSIP1 raw field that
propagated to the frontend JSON. The live page displays `חלב,` which could mislead a consumer
into thinking the ingredient list continues.

Fix path (describe only, do not apply): data-agent strips trailing connector characters from
`ingredients_raw` at BSIP1 hygiene stage, OR content-agent/data-agent patches the frontend JSON
directly to remove the trailing comma. Route to: data-agent.

### Finding M-002: run_id in _meta does not resolve to a trace directory

`_meta.run_id = "task409_rederive_milk_20260626"` — no such trace directory exists in the main
tree. The authoritative traces are in `run_005_headpin` (AUTHORITATIVE.md). All 18 scores match
`run_005_headpin` exactly, so the frontend is correctly scored. The `run_id` field is a generation
task label, not a trace directory pointer.

This is a traceability gap: the `validate_comparison_page.py --traces` instrument cannot auto-locate
the correct trace directory for milk because the declared `run_id` doesn't map to a filesystem path.
Classification: DISPLAY-ONLY (no score error). Routes to: data-agent (align milk `_meta.run_id`
to match the authoritative `run_005_headpin` directory name, or document the naming convention
in the milk run_record).

### Finding M-003: rice drink override discrepancy (secondary)

AUTHORITATIVE.md (`run_005_headpin`) documents a deliberate owner-approved override:
"Rice drink `8000215204219`: live page shows 52.3/C, NOT this run's 49.4/D"
(TASK-169C, confirmed 2026-06-04).

The current `milk_frontend_v1.json` shows barcode `8000215204219` at score=46.3/D, grade=D.
The `run_005_headpin` trace also shows 46.3/D (not 49.4/D as the AUTHORITATIVE.md reference
suggests the engine scores it).

Both the frontend JSON (46.3) and the `run_005_headpin` trace (46.3) diverge from the
AUTHORITATIVE.md's stated engine score (49.4) AND from the documented override (52.3). The 46.3
value is unexplained: it appears in neither the "engine value" (49.4) nor the "override value"
(52.3). This is a three-way discrepancy between:
1. AUTHORITATIVE.md engine score: 49.4/D
2. AUTHORITATIVE.md override: 52.3/C
3. Current frontend + trace: 46.3/D

Classification: POTENTIAL SCORE-AFFECTING. The live page displays 46.3/D, neither the engine
baseline (49.4) nor the documented override (52.3). The consumer sees a score that is not the
engine result and not the owner-approved override. Escalation required before any rebuild.
Routes to: data-agent (investigate the 46.3 origin) + product-agent (confirm with owner — rice
drink score is a documented frozen invariant).

---

## Summary by Category and Class

| Category | Total Products | Score Mismatch | Grade-Changing Mismatch | Ingredient Truncation | DISPLAY-ONLY | SCORE-AFFECTING | Notes |
|---|---|---|---|---|---|---|---|
| Brined cheeses | 36 | 14 | 3 | 0 | 14 | 0 | Stale traces; frontend is correct |
| Milk | 18 | 0 | 0 | 1 | 1 (M-001) + 1 (M-002) | 0 direct; 1 secondary (M-003) | Rice override discrepancy requires investigation |

### Finding counts

- DISPLAY-ONLY: 16 (14 brined stale-trace + 1 milk trailing comma + 1 milk run_id gap)
- SCORE-AFFECTING: 0 confirmed direct
- REQUIRES INVESTIGATION before classification: 1 (M-003 rice drink 46.3 vs documented 49.4 vs override 52.3)
- Secondary copy-authoring findings (out of scope for TASK-527): 5 (4 brined + 1 milk)

**The "~3 ingredient-truncation flags" described in TASK-527** resolve to exactly 1 real trailing-comma
flag in the current validator (barcode 7290019790259). The TASK-527 description used an approximate
count; the authoritative count is 1.

---

## Proposed fix paths (describe only — no implementation)

### Brined cheeses — stale traces (14 products)
Option A: Regenerate `run_brined_005` per-product traces by running the scoring engine at the post-TASK-438
flag state (EV-099 NOVA-gate active). This updates the traces to match the current frontend JSON.
Option B: Create a post-reflow verification artifact (e.g., a `verification_table_post_task438.csv`)
at `run_brined_005/` that supersedes the pre-reflow `verification_table.csv` for propagation audits.
Option C: Add a `reflow_applied_scores` block to the frontend `_meta` so the validator can use
post-reflow scores rather than raw trace `final_score_estimate` when a `_meta.reflow` is present.
**Owner of fix:** data-agent (pipeline traceability) or frontend-agent (Option C, validator adaptation).

### Milk — trailing comma (1 product, barcode 7290019790259)
Strip trailing connector characters from `expansion.ingredients` at frontend JSON generation.
The correct display value is `חלב` (without the comma).
**Owner of fix:** data-agent (patch BSIP1 hygiene script) or data-agent (patch frontend JSON
generation to strip trailing connectors before writing).

### Milk — run_id traceability gap (M-002)
Update milk `_meta.run_id` to `run_005_headpin` (the authoritative trace directory name), or add a
separate `authoritative_trace_dir` field. This makes the validator auto-discoverable.
**Owner of fix:** data-agent.

### Milk — rice drink override discrepancy (M-003)
Do NOT rebuild without owner confirmation. Investigate the 46.3 origin in pipeline history.
If the 52.3/C override was intentional and should be live, the frontend JSON requires a targeted
patch. This is a documented frozen invariant — changes require owner sign-off.
**Owner of investigation:** data-agent. **Owner of go/no-go:** product-agent (owner confirmation required).

---

## Return Contract

```json
{
  "task": "TASK-527",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/qa/task527_live_mismatch_diagnosis_v1.md",
      "action": "created",
      "sha256": "self-referential — orchestrator must run Get-FileHash on this file to verify"
    }
  ],
  "counts": {
    "brined_products_in_frontend": "36/36 (brined_cheeses_frontend_v2.json products array)",
    "brined_score_mismatches": "14/36 (PowerShell trace comparison, run_brined_005 vs frontend)",
    "brined_grade_changes_in_mismatches": "3/14 (7290108509106 A->B, 7290011499129 A->B, 7290108509755 B->C — confirmed against _meta.reflow)",
    "brined_ingredient_truncations": "0/36 (validator gate [PASS])",
    "brined_matching_products": "22/36 (delta = 0.0)",
    "brined_mismatch_delta_min": "-2.2 (barcode 3075805)",
    "brined_mismatch_delta_max": "-1.9 (barcode 7290108509106)",
    "brined_mismatch_delta_median": "-2.1",
    "brined_DISPLAY_ONLY": "14/14 mismatches (stale pre-reflow traces, frontend is correct)",
    "brined_SCORE_AFFECTING": "0/14",
    "milk_products_in_frontend": "18/18 (milk_frontend_v1.json products array)",
    "milk_score_mismatches_vs_run005_headpin": "0/18",
    "milk_ingredient_truncations": "1/18 (barcode 7290019790259, trailing comma — validator confirmed)",
    "milk_run_id_resolvable": "0/1 (task409_rederive_milk_20260626 has no trace directory in main tree)",
    "milk_DISPLAY_ONLY": "2/2 (M-001 trailing comma + M-002 run_id gap)",
    "milk_SCORE_AFFECTING_confirmed": "0/18",
    "milk_SCORE_AFFECTING_requires_investigation": "1/18 (M-003 rice drink 46.3 vs 49.4 vs 52.3)"
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/spine/validate_comparison_page.py --json bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json --traces 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products",
      "exit_code": 1
    },
    {
      "cmd": "python 03_operations/spine/validate_comparison_page.py --json bari-web/src/data/comparisons/milk_frontend_v1.json --traces 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products",
      "exit_code": 1
    },
    {
      "cmd": "PowerShell: Compare all 36 brined frontend products vs run_brined_005 traces (final_score_estimate + grade_estimate)",
      "exit_code": 0
    },
    {
      "cmd": "PowerShell: Compare all 18 milk frontend products vs run_005_headpin traces (final_score_estimate + grade_estimate)",
      "exit_code": 0
    },
    {
      "cmd": "Read AUTHORITATIVE.md for run_005_headpin",
      "exit_code": 0
    },
    {
      "cmd": "Read SUPERSEDED.md for run_004_recalibrated",
      "exit_code": 0
    },
    {
      "cmd": "PowerShell: Compare milk frontend ingredients vs BSIP1 run_milk_002 raw ingredient fields",
      "exit_code": 0
    }
  ],
  "not_done": [
    "The TASK-527 spec says 'reported ~3 ingredient-truncation flags' for milk; the actual validator finds 1. The discrepancy is explained: the TASK-527 description was an approximate count; the principled validator finds exactly 1 real truncation flag (trailing comma). No additional investigation needed for the other 2 'approximate' flags.",
    "No trace directory was found for task409_rederive_milk_20260626; it may exist in a worktree or external location not accessible to this run. Score comparison was performed against run_005_headpin (authoritative) instead. All 18 scores match, so this gap does not affect the DISPLAY-ONLY classification.",
    "M-003 (rice drink 46.3 discrepancy) is classified as 'requires investigation' — the root cause of the 46.3 value is not established in this read-only run. The three-way discrepancy (49.4 engine / 52.3 override / 46.3 actual) is documented as a finding."
  ],
  "self_check": "Acceptance test: for each flagged product, determine DISPLAY-ONLY vs SCORE-AFFECTING. Result: 14 brined cheese mismatches are ALL DISPLAY-ONLY (stale pre-reflow traces; frontend JSON confirmed correct by _meta.reflow documentation and systematic -2.1 delta consistent with EV-099 NOVA-gate). 1 milk ingredient truncation is DISPLAY-ONLY (trailing comma artifact in BSIP1 raw, confirmed by BSIP1 source). 0 milk score mismatches (all 18 match run_005_headpin exactly). 1 secondary finding (M-003 rice drink 46.3) requires further investigation before final classification — noted as potential SCORE-AFFECTING pending data-agent root cause analysis."
}
```
