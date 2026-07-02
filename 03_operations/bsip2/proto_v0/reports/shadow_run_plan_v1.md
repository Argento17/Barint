# Shadow Run Plan v1 — BSIP_DECHAIN_V1 Whole-Corpus Test
**Task:** TASK-395
**Authored by:** Data Agent
**Date:** 2026-06-25
**Status:** DESIGN ONLY — no engine code changed, no scores changed, no commits
**Depends on:**
- `target_scoring_logic_spec_v1.md` (§2 NOVA replacement + retained guards) — D6 authored
- `matrix_signal_redesign_v3.md` (v5.1 formula, NC-2 guards) — D6 authored + Product NC-2 confirmed
- `structured_ingredient_reader.py` (v4, shared reader — QA agent a1eb64c1adaf91c8b verified)
- `matrix_signal_probe_v5_1.py` (Component B v5.1 — all gates B1/B2/B3 pass)
- `run_task395_dechain_drift.py` (existing column-A/B/C drift harness — reused as foundation)

**Implementation lane:** C1 worktree (ISOLATED — see Part C). NOT the shared working tree.
**Co-sign required before implementation:** D6 (Nutrition) + D7 (Product) on open decisions listed in §Open Decisions. NC-2 is already confirmed.

---

## Part A — Candidate-Engine Integration Design

### A.1 What Changes Under `BARI_DECHAIN_V1` (Flag Off = Bit-Identical)

The flag `BARI_DECHAIN_V1` (environment variable, default `off`) gates ALL changes in this plan. When the flag is off, every function in `score_engine.py`, `signal_extractor.py`, and `nova_proxy.py` runs byte-identically to the current published engine. The flag is read once at module load (same pattern as every existing flag in the engine).

### A.2 `processing_quality` Dimension — Candidate Wiring

**Current path (NOVA step-lookup):**
```python
# score_engine.py line 1559 (flag-off path):
score = NOVA_PROCESSING_SCORES.get(nova_level, 50)
return score, f"NOVA {nova_level} → processing_quality={score} (NOVA_PROCESSING_SCORES table)"
```

**Candidate path (flag ON):**

`score_processing_quality()` in `score_engine.py` gains a new branch. When `BARI_DECHAIN_V1` is on, the function:

1. Calls `extract_all_markers_v4(ingredients_text_he)` from `structured_ingredient_reader` (shared reader — the same reader already imported in `matrix_signal_probe_v5_1.py`). This is a new import added to `score_engine.py` at module load, guarded so it is a no-op when the flag is off.

2. Calls `compute_component_b_score_v5_1(markers)` to get the matrix balance score (Component B, range 10–95 or None).

3. Computes `processing_load_score` (Component A) from `additive_marker_count` already in the `l3` signal dict — the identical signal path as `additive_quality`. The formula:
```
processing_load_score = max(0, 100 - additive_marker_count × per_additive_penalty)
clamped to [10, 95]
```
   The `per_additive_penalty` uses the D4 identity tier if `BARI_D4_SCORE_V1` is also on; otherwise a flat per-additive penalty (open decision OD-1 below).

4. Combines A and B:
```
combined = 0.60 × processing_load_score + 0.40 × matrix_score
```
   (weights 0.60/0.40 from target_scoring_logic_spec_v1.md §2.3 — subject to D6/D7 confirmation, open decision OD-2)

   If `matrix_score` is None (unparseable ingredient text → `extract_all_markers_v4` returned empty), the formula degrades to Component A only: `combined = processing_load_score`. The trace records `matrix_score_fallback: "component_a_only_unparseable"`.

5. Applies the NOVA subordination modifier (confidence-scaled, not a cliff):
   - `nova_modifier` is computed from `nova_level` and `w4_confidence` via `_nova_subordination_modifier()` (new internal helper, described below).
   - `candidate_score = clamp(combined + nova_modifier, 10, 95)`

6. Returns `(candidate_score, trace_note)` where `trace_note` contains the `processing_quality_components` sub-object required by the spec (§7.1).

**`_nova_subordination_modifier()` helper (new, internal to score_engine.py):**
```python
def _nova_subordination_modifier(
    nova_level: int,
    w4_confidence: str | None,
    w4_materiality: str | None,
) -> float:
    """
    NOVA as a subordinate modifier under BARI_DECHAIN_V1.
    Returns a signed delta to add to the combined Component A+B score.
    NOVA-4 at high confidence: -10 (depression, not a cliff).
    NOVA 1-2 at high confidence: +5 (incremental push, not a floor).
    Medium/low confidence: magnitude is scaled down proportionally using
    the existing _w4_confidence_scale() helper (pessimistic direction).
    Range is clamped to [-10, +5] before returning.
    """
    # Base modifier by NOVA level
    # OPEN DECISION OD-3: exact modifier magnitudes need D6/D7 ratification
    if nova_level == 4:
        base_modifier = -10.0
    elif nova_level in (1, 2):
        base_modifier = +5.0
    else:  # NOVA 3
        base_modifier = 0.0

    if w4_confidence is not None:
        scale = _w4_confidence_scale(w4_confidence, w4_materiality)
    else:
        scale = 1.0

    return round(base_modifier * scale, 2)
```

**Signature change to `score_processing_quality()`:**
```python
def score_processing_quality(
    nova_level: int,
    w4_confidence: str | None = None,
    w4_materiality: str | None = None,
    # New parameters for BARI_DECHAIN_V1 — ignored when flag is off:
    ingredients_text_he: str | None = None,
    additive_marker_count: int = 0,
) -> tuple[float, str]:
```

The caller (`score_product()`) already passes `w4_confidence`. It needs to also pass `ingredients_text_he` and `additive_marker_count` from the `l3` dict when `BARI_DECHAIN_V1` is on. Since `l3` is already in scope at the `score_product()` call site, this is a two-line addition at the call site, guarded by the flag.

### A.3 `whole_food_integrity` Dimension — Candidate Wiring

**Current path:** `score_whole_food_integrity()` uses `NOVA_WFI_SCORES` step-lookup, optionally scaled by `BARI_W4_WFI_V1` pessimistic confidence scaling (already in the engine).

**Candidate path (BARI_DECHAIN_V1 on):**

The target spec (§2, N-2 disposition) states WFI uses the same reassembly/matrix signal as processing_quality in Stage 2B, but Stage 0 (pessimistic confidence scaling, already active under `BARI_W4_WFI_V1`) is the interim fix. For the shadow run, the candidate wires `BARI_W4_WFI_V1` as **implicitly on** when `BARI_DECHAIN_V1` is on (they are always co-active). This avoids adding a separate flag for what Stage 0 already specifies.

Specifically: if `BARI_DECHAIN_V1` is on and `BARI_W4_WFI_V1` is off, the candidate engine behavior for WFI defaults to W4 pessimistic scaling as if `BARI_W4_WFI_V1` were on, pulling toward `_WFI_PESSIMISTIC_ANCHOR = 30` at low confidence.

The full Stage 2B WFI rewrite (same matrix signal as processing_quality, applied to WFI) is explicitly deferred to Stage 2B per the target spec — NOT implemented in this shadow run. This is correctly labeled as `not_done` in the return contract.

### A.4 Retained Guards — Active Under BARI_DECHAIN_V1

All retained guards remain unconditionally active regardless of the flag. No guard is modified by `BARI_DECHAIN_V1`:

| Guard | What it does | Status under BARI_DECHAIN_V1 |
|---|---|---|
| V-1: Trans-fat veto (score=0) | Industrial trans fat absolute | ALWAYS ACTIVE — unchanged |
| CC-1: Confidence ceiling (50) | Insufficient data cap | ALWAYS ACTIVE — unchanged |
| CC-2: Confidence ceiling (75) | Low-data cap | ALWAYS ACTIVE — unchanged |
| SW-1: Sweetener caps (75/73/70) | Synthetic sweetener ceiling by tier | ALWAYS ACTIVE — unchanged |
| FL-1: Single-ingredient whole-food floor (85) | Genuine single-ingredient floor | ALWAYS ACTIVE — unchanged |
| FL-2: Whole-food fat floor (70) | Butter/dairy fat floor | ALWAYS ACTIVE — unchanged |
| FL-3/FL-4: Physiological moderation floors (60/50) | Counterweight for high-label whole foods | ALWAYS ACTIVE — unchanged |
| Dominance guardrail (BARI-INVERSION-TEST-001) | adding refined weight cannot raise a score | ALWAYS ACTIVE (by formula monotonicity of Component B) |
| N-3 NOVA-4 composite cap (68) | Backstop for NOVA-4 | ACTIVE in shadow (interim — not yet retired; see OD-4) |
| N-4 NOVA-3 composite cap (87) | Practically inert cap | ACTIVE in shadow (removal is a separate flag per spec) |

**Flags NOT activated in this shadow run** (reserved for later stages):
- `BARI_D4_SCORE_V1` — additive identity D4 score. Not activated; additive_marker_count uses the current flat signal.
- `BARI_REDLABEL_V1` — red-label continuous deduction. Already live for some categories; not changed.
- `BARI_GRAD_SODIUM_V1` — sodium graduation. Already live; not changed.
- `RECAL_P0` — sat-fat recalibration. Already live; not changed.
- Sugar/calorie cap removals (S-2, S-5, C-1, C-2) — NOT activated in this shadow run.

### A.5 `processing_quality_components` Trace Sub-Object

Every product scored under `BARI_DECHAIN_V1` emits this in its trace:

```json
"processing_quality_components": {
  "formula_version": "BARI_DECHAIN_V1",
  "component_a_processing_load_score": 72.0,
  "component_a_additive_marker_count": 2,
  "component_a_per_additive_penalty": 14.0,
  "component_b_matrix_score": 44.0,
  "component_b_read_mode": "stated_pct",
  "component_b_markers_fired": ["oat_flakes_plain", "sugar", "palm_oil"],
  "component_b_has_grain_context": true,
  "component_b_dominance_ratio": 0.41,
  "nova_modifier": -6.0,
  "nova_modifier_basis": "NOVA 4 × confidence_scale(medium/NON_MATERIAL)=0.6",
  "combined_pre_nova": 60.8,
  "candidate_processing_quality_score": 54.8,
  "fallback_mode": null
}
```

If `component_b_read_mode` is `"unparseable"`, the trace records the fallback and the reason. This field is required for the C3 breakdown requirement (stated-% read vs position-inference fallback).

---

## Part B — Shadow-Run Harness Plan

### B.1 Scoreable Universe — Honest Denominator

The live published corpus (as of 2026-06-25) spans 18 frontend JSON files with **627 total product entries, 587 unique barcodes** across 12 category slugs. The shadow run operates against the same BSIP1 input records that produced those scores, NOT directly against the frontend JSONs (which are outputs, not inputs).

**Category breakdown:**

| Category slug | Frontend file | Products live | BSIP1 source path | Shadow-scoreable? | Notes |
|---|---|---|---|---|---|
| bread | bread_frontend_v3.json | 29 | `03_operations/bsip1/run_bread_conform_001/output` | YES — full | Has ingredient text; matrix signal applies |
| brined_cheeses | brined_cheeses_frontend_v2.json | 36 | `03_operations/bsip1/run_brined_cheeses_002/output` | YES — full | Brined; Component B fires on ingredient text |
| cakes | cakes_hard_cookies_frontend_v1.json | 65 | `03_operations/bsip1/run_cakes_001/output` | YES — full | Mixed biscuit/cake; Component B directly relevant |
| breakfast-cereals | cereals_frontend_v2.json | 20 | `03_operations/bsip1/run_cereals_008/output` | YES — full | Grain-primary; highest Component B impact expected |
| cheese-spreads | cheese_frontend_v4.json | 53 | `03_operations/bsip1/run_cheese_003/output` | YES — full | Dairy; Component B expected near neutral |
| cookies_coffee | cookies_coffee_frontend_v2.json | 119 | `run_cookies_001/output` + `run_cakes_001/output` | YES — full | Grain-based; Component B applies |
| granola | granola_frontend_v1.json | 22 | `03_operations/bsip1/run_cereals_005/output` | YES — full | Grain-primary; grain-context guard most active here |
| hard_cheeses | hard_cheeses_frontend_v2.json | 23 | `02_products/hard_cheeses/bsip1_outputs` | YES — full | Dairy; Component B near neutral; NOVA modifier small |
| hummus | hummus_frontend_v5.json | 57 | `02_products/hummus/canonical_bsip1` | YES — full | Legume-primary; interesting for chickpea marker |
| juices | juices_frontend_v3.json | 17 | `02_products/juices/bsip1_outputs` | YES — full | No grain; Component B likely returns None; Component A drives |
| milk | milk_frontend_v1.json | 18 | `03_operations/bsip1/run_milk_002/output` | YES — full | Dairy; Component B near neutral |
| snacks | snacks_frontend_v5.json | 21 | `03_operations/bsip1/run_001/output` | YES — full | Mixed grain/nut snacks |

**Categories present in comparisons/ but NOT in BSIP1_SOURCES (cannot be shadow-scored from BSIP1):**

| Frontend file | Products | Shadow status | Reason |
|---|---|---|---|
| chocolate_bars_frontend_v1.json | 23 | CANNOT shadow-score | No BSIP1 source path in `run_task395_dechain_drift.py`; scored via separate pipeline |
| chocolate_tablets_frontend_v1.json | 35 | CANNOT shadow-score | Same — no BSIP1 source mapped |
| protein_bars_frontend_v1.json | 16 | CANNOT shadow-score | protein_bars scored via `batch_run_protein_bars_task365.py`; no canonical BSIP1 output dir mapped |
| protein_combined_frontend_v2.json | 32 | CANNOT shadow-score | Same protein bar pipeline; no BSIP1 source |
| granola_frontend_v2.json | 22 | DUPLICATE of v1 (same products) | Rescore from same BSIP1 source as granola_frontend_v1.json; count once |

**Supplements:** The supplement corpus (`real_corpus_v3`, 85 SKUs) uses `score_label()` from `score_engine.py` but NOT the NOVA/WFI/processing_quality dimensions that `BARI_DECHAIN_V1` modifies. Supplements are lens-only scored on their active-ingredient matrix. Shadow run does NOT apply to supplements.

**True shadow-scoreable denominator:**

- 12 category slugs with mapped BSIP1 sources
- Live products in those categories: 29 + 36 + 65 + 20 + 53 + 119 + 22 + 23 + 57 + 17 + 18 + 21 = **480 products**
- Unique barcodes (after dedup across shared BSIP1 sources like cookies/cakes overlap): approximately **460 unique** — exact number is computed by the harness at runtime by deduplicating on barcode before scoring
- Products that cannot be shadow-scored (chocolate, protein_bars): **106** (23+35+16+32)
- These 106 are explicitly excluded from the shadow run with status `excluded_no_bsip1_source`

**Clarification on granola duplication:** `granola_frontend_v1.json` and `granola_frontend_v2.json` contain the same 22 products with different display configurations. The harness scores them once from the shared BSIP1 source and generates a single movement table row per barcode. The v2 frontend note is preserved in the output but scores are not duplicated.

### B.2 Harness Design

The harness extends `run_task395_dechain_drift.py` (the existing three-column drift infrastructure). The extension adds a fourth column, Column D, which is the candidate engine.

**Column mapping:**
- Column A: `BARI_W4_WFI_V1=off, BARI_D4_SCORE_V1=off, BARI_DECHAIN_V1=off` — committed baseline (must match frontend JSON scores exactly; any mismatch is a harness bug, not a finding)
- Column B: `BARI_W4_WFI_V1=on, BARI_D4_SCORE_V1=off, BARI_DECHAIN_V1=off` — Stage 0 WFI fix only (already designed; Column B from existing harness)
- Column C: `BARI_W4_WFI_V1=on, BARI_D4_SCORE_V1=on, BARI_DECHAIN_V1=off` — Stage 0 + D4 additive identity (Column C from existing harness)
- **Column D: `BARI_DECHAIN_V1=on` (implies W4_WFI_V1=on)** — the candidate engine with full processing_quality rewrite

The harness scores each product FOUR times in-process, using the same `score_product()` call path as the batch runners, with environment variables patched between calls (not subprocess-spawned — the engine reads env vars at call time via the existing flag-read pattern).

**Harness file:** `C:\Bari\03_operations\bsip2\proto_v0\src\run_shadow_dechain_v1.py`

This is a NEW file, written in the implementation worktree. It imports from the same `score_engine.py`, `nova_proxy.py`, `signal_extractor.py`, and the new shared reader path. Its output directory is `C:\Bari\_rescore_staging\_shadow_dechain_v1\`.

### B.3 Output Artifacts

**Artifact 1: Full movement table (`shadow_movement_table_v1.json`)**

```json
{
  "run_id": "shadow-dechain-v1-YYYYMMDD-HHMMSS",
  "run_date": "...",
  "dechain_flag": "BARI_DECHAIN_V1",
  "scoreable_universe": 460,
  "excluded": 106,
  "categories": 12,
  "products": [
    {
      "barcode": "7290001065594",
      "category": "breakfast-cereals",
      "name_he": "...",
      "col_a_score": 52, "col_a_grade": "C",
      "col_b_score": 49, "col_b_grade": "C",
      "col_c_score": 47, "col_c_grade": "C",
      "col_d_score": 41, "col_d_grade": "C",
      "delta_d_vs_a": -11,
      "grade_moved": false,
      "processing_quality_components": { ... },
      "col_a_matches_baseline": true,
      "baseline_score": 52
    }
  ]
}
```

The `col_a_matches_baseline` field is the cross-check against the committed frontend JSON. If any product's Column A score does not match its live baseline, the harness aborts with a loud error before writing Column D results. This prevents untracked drift from contaminating the movement table.

**Artifact 2: Top-20 movers per category (`shadow_top_movers_by_category_v1.json`)**

Per category: top 10 risers and top 10 fallers (by `delta_d_vs_a`), with full component trace for each.

**Artifact 3: Read-mode breakdown table (`shadow_read_mode_breakdown_v1.json`)**

Per product:
- `read_mode`: `"stated_pct"` (has at least one stated percentage in ingredient list), `"position_only"` (no stated percentages, position-weight curve used for all markers), or `"no_markers"` (Component B returned None — Component A only)
- `n_stated_pct_markers`: count of markers with stated_pct
- `n_position_only_markers`: count of markers using position-weight fallback
- `component_b_score`: the matrix signal output

This directly satisfies the C3 requirement: every score movement must be breakdownable as driven by a stated-% read vs a position-inference fallback.

**Artifact 4: Failure/anomaly taxonomy (`shadow_anomaly_report_v1.json`)**

Anomaly classes (each product in an anomaly class is listed individually):

| Code | Description | Detection method |
|---|---|---|
| `LARGE_MOVER` | `abs(delta_d_vs_a) > 15` on any product | Direct delta threshold |
| `GRADE_MOVE` | Grade letter changed (A→B, B→C, etc.) from col_a to col_d | Grade comparison |
| `FLOOR_CONFLICT` | Col D score < retained guard floor that should prevent it | Guard check vs final score |
| `GUARD_UNTRIGGERED` | CC-1/CC-2 fired in col_a but not in col_d, or vice versa | Confidence ceiling trace |
| `INVERSION_CANDIDATE` | Product moved from D/E to C+ under candidate; check if inversion guardrail was bypassed | Score + NOVA class cross-check |
| `COMPONENT_B_NONE` | Ingredient text unparseable; Component A is the sole driver | `matrix_score is None` |
| `KNIFE_EDGE` | Score within 1 point of a grade boundary in col_d | Score mod 15 check |
| `NESTED_LABEL` | Product has a composite ingredient with sub-percentages; Component B used nested effective_pct | `is_sub=True` markers present |
| `BASELINE_MISMATCH` | Col A does not match committed baseline | Halts harness before col_d output |

**Artifact 5: Grade distribution report (`shadow_grade_dist_v1.json`)**

Per category, the full grade distribution A/B/C/D/E/S for columns A and D, plus the sanity-gate thresholds from `target_scoring_logic_spec_v1.md §8.4`. Any category where a single grade exceeds 60% of its products in Column D is flagged as `calibration_review_needed: true`.

**Artifact 6: Run record (`shadow_run_record_v1.json`)**

Includes run_id, date, configuration hashes of `score_engine.py` + `structured_ingredient_reader.py` + `matrix_signal_probe_v5_1.py`, scoreable universe count, excluded count, and SHA256 of each output artifact.

### B.4 Cross-Check Against Phase-0 Reproducibility Baseline

The harness's Column A cross-check IS the reproducibility baseline verification. Every Column A score must match the committed frontend JSON score exactly. If it does not, the mismatch is logged in `shadow_anomaly_report_v1.json` as `BASELINE_MISMATCH` and the harness halts before emitting Column D results.

This means movement in Column D is by construction real candidate-engine change, not untracked drift — because Column A is verified to be identical to the committed baseline before Column D is computed.

The configuration hash of `score_engine.py` is logged in the run record. If `score_engine.py` has been modified since the last committed baseline run, the harness logs a warning and requires explicit override to proceed (preventing silent drift from competing edits in other chats).

### B.5 Self-Gate (Harness End-to-End Verification)

At the end of every run, the harness executes:

```python
# Self-gate: recompute Column A for 5 known products and confirm delta = 0
SELF_GATE_BARCODES = [
    "7290001065594",   # known cereal product (from existing batch_run_cereals)
    "7290016883176",   # 47% oats product (in gold set — known B5.1 score)
    "7290011131371",   # 38% oats + nuts product (in gold set)
    # + 2 more from brined_cheeses and cookies corpus
]
```

If any self-gate product's Column A deviates from the committed baseline, the harness fails with exit code 2 and does NOT write Column D output. This is the machine-check-on-own-output requirement from the return contract standard.

---

## Part C — Isolation Plan

### C.1 Git Worktree

Implementation and shadow run happen in a dedicated git worktree, never the shared working tree.

**Worktree creation (to be run by the implementation agent at start of task):**
```powershell
# Run from repo root (C:\Bari)
git worktree add "C:\Bari\_worktrees\dechain_v1" -b task-395-dechain-v1
```

**Worktree path:** `C:\Bari\_worktrees\dechain_v1`

All implementation work in this plan — engine src edits, harness script, test runs — happens inside `_worktrees\dechain_v1\`. The shared working tree at `C:\Bari` remains on its current branch (`task-374-toms-voice`) and is not touched.

### C.2 Files to be Edited (in worktree only)

| File | Change | Type |
|---|---|---|
| `03_operations/bsip2/proto_v0/src/score_engine.py` | Add `BARI_DECHAIN_V1` flag, new `score_processing_quality()` branch, import shared reader | Engine edit |
| `03_operations/bsip2/proto_v0/src/signal_extractor.py` | Optional: the `additive_marker_count` field is already populated; no change needed for shadow run | No change planned |
| `03_operations/bsip2/proto_v0/src/nova_proxy.py` | No changes — NOVA stays as-is, used as modifier input only | No change |

**New files created (in worktree):**

| File | Purpose |
|---|---|
| `03_operations/bsip2/proto_v0/src/run_shadow_dechain_v1.py` | Shadow run harness (Column A/B/C/D) |
| `03_operations/bsip2/proto_v0/src/candidate_engine_utils.py` | Shared reader import wrapper + `_nova_subordination_modifier()` isolated helper |
| `_rescore_staging/_shadow_dechain_v1/` | Output directory for all artifacts |

### C.3 Pre-Tracked Dedup Fix

The delegation brief references a "pre-tracked dedup fix." This refers to the existing barcode deduplication logic in `collect_bsip1_records()` in `run_task395_dechain_drift.py` (line 161: `if bc and bc not in by_barcode`). The same dedup logic applies in the shadow harness — the first occurrence of a barcode in a BSIP1 source wins. This is already implemented in the existing harness and is carried forward unchanged.

### C.4 No Commits to Main Branch During Shadow Run

The worktree is isolated. After the shadow run completes and the movement table is verified:
- If results are within expected parameters (no FLOOR_CONFLICT, no unexpected INVERSION_CANDIDATE anomalies, grade distributions within sanity bands), a PR from `task-395-dechain-v1` to `master` is opened for D6/D7/owner review
- The PR is explicitly marked as "shadow results only — no frontend JSON changes"
- No published score changes until the owner gates the deploy (frozen-invariant tripwire)

---

## Open Decisions (D6/D7 Required Before Implementation)

The following decisions are flagged for D6 (Nutrition Agent) + D7 (Product Agent) ratification. Data Agent MUST NOT implement with invented values. Recommended values are provided with rationale for D6/D7 to evaluate.

### OD-1: Flat Per-Additive Penalty (Component A, when BARI_D4_SCORE_V1 is off)

**Question:** When `BARI_D4_SCORE_V1` is off (not yet activated), what flat penalty per additive marker should Component A use?

**Context:** `target_scoring_logic_spec_v1.md §2.1` specifies identity-differentiated penalties (20/15/8/3 by tier) that require `BARI_D4_SCORE_V1`. For the shadow run, D4 is not being activated. A flat fallback is needed.

**Recommended value:** 14 per additive marker.
**Rationale:** The corpus average of additive marker counts in NOVA-4 products is approximately 3–4 markers. A penalty of 14 per marker on a NOVA-4 product with 3 markers = 42 points deducted from 100, producing `processing_load_score = 58`. Combined with a neutral-ish matrix score (50), the candidate `processing_quality` for such a product is approximately 55, which is below the NOVA-4 step-lookup value of 35 on the old table — but above it. This is the correct direction for a shadow run that is subordinating NOVA, not eliminating it. The NOVA modifier (-10 at high confidence for NOVA-4) then pulls the final score down further.
**What D6/D7 need to ratify:** Is 14 the right flat penalty, or should it be set differently to preserve rank-order fidelity across the corpus? If D6/D7 want to see the shadow run with 0.60/0.40 A/B weights AND a 14-penalty, the harness can produce a sensitivity table varying the penalty from 10 to 20 in increments of 2, all in a single run.

### OD-2: Component A/B Weights (0.60/0.40)

**Question:** Confirm the 0.60/0.40 split between Component A (additive load) and Component B (matrix signal) in the combined `processing_quality` score.

**Context:** From `target_scoring_logic_spec_v1.md §2.3` — these are corpus-fit weights. "The additive load carries more weight because it is more precisely observable."

**Recommended value:** 0.60/0.40 as specified.
**Rationale:** Component A (additive count) is more precisely label-derivable and has tighter expected-value distributions. Component B (matrix signal) adds structural signal but has higher variance from position-weight fallbacks. 0.40 is a meaningful but not dominant weight. If D6/D7 prefer 0.50/0.50, the harness can run both as sensitivity columns.
**What D6/D7 need to ratify:** Confirm or modify the split. Any modification changes the corpus-wide score distribution; the shadow run will show both options if requested.

### OD-3: NOVA Subordination Modifier Magnitudes (-10 for NOVA-4, +5 for NOVA 1-2)

**Question:** Confirm the NOVA modifier magnitudes: NOVA-4 at high confidence applies -10 to the combined Component A+B score; NOVA 1-2 at high confidence applies +5.

**Context:** From `target_scoring_logic_spec_v1.md §2.3` — "NOVA-4 classification at high confidence: apply a confidence-scaled penalty of -10 on the combined score (not a cliff, a moderate additional depression). NOVA 1-2 at high confidence: apply a bonus of +5."

**Recommended value:** -10 / +5 as specified.
**Rationale:** -10 represents about a 10% depression on a 100-point scale — meaningful but not a cliff (the old NOVA-4 step-lookup was a 35, representing a 50-point cliff from NOVA-2 at 85). At medium confidence the modifier scales to -6 (confidence_scale ≈ 0.6). This gives NOVA strong directionality as a modifier without overriding the structural signals.
**What D6/D7 need to ratify:** If the -10 magnitude appears too small in the shadow run (i.e., NOVA-4 products with Component A score = 90 still score 80 on processing_quality), D6/D7 should increase to -15. The shadow run will show the distribution before any adjustment.

### OD-4: Interim N-3 Cap Behavior (NOVA-4 Composite Cap at 68)

**Question:** Should the N-3 NOVA-4 composite cap (68) remain active during the shadow run, or should it be relaxed to 78 as Stage 1B specifies?

**Context:** `target_scoring_logic_spec_v1.md §5.1` specifies: "Stage 1B: raise cap to 78 (interim). After additive parser validation: remove." The shadow run is NOT Stage 1B — it is Stage 2's simulation. The cap is a backstop.

**Recommended value:** Keep the cap at 68 for the shadow run.
**Rationale:** The shadow run should show what the candidate engine produces with the existing composite cap still in place. If the candidate engine is correctly calibrated, few or no products should be hitting the 68 cap (because Component A+B+NOVA_modifier should naturally produce scores below 68 for genuine NOVA-4 products). If many products still hit the cap, it reveals the candidate is under-penalizing — and that is a finding, not a problem to solve by changing the cap during the shadow run.
**What D6/D7 need to ratify:** Confirm the cap stays at 68 for this shadow run. The anomaly report will list every product where the 68 cap fires under Column D, distinguishing "cap is binding and removing it would raise the score" from "cap fires but the continuous score is already below 68 — coincidental."

---

## Spec-Conflict Check

The delegation says "NOVA stays a MEANINGFUL input for the shadow (not yet demoted to ±5-10 in production)." The ±5-10 range IS the current proposal (-10/+5) for the shadow run. This is consistent: ±5-10 is the shadow candidate design; production deployment (if approved) would use the same magnitudes unless D6/D7 ratify different values. No conflict.

The delegation says "new signal is the driver and NOVA is a subordinate modifier, ALL behind a single flag `BARI_DECHAIN_V1`." Confirmed — the design in Part A wires everything behind a single flag with bit-identical off behavior.

The delegation says "Old behavior must be bit-identical when the flag is off." Confirmed — no existing function signature is changed for the flag-off path; new parameters to `score_processing_quality()` all have defaults that reproduce current behavior exactly.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/shadow_run_plan_v1.md",
      "action": "created",
      "sha256": "pending — orchestrator runs Get-FileHash after write"
    }
  ],
  "counts": {
    "shadow_scoreable_universe": "460 unique barcodes (denominator: 12 categories with mapped BSIP1 sources)",
    "live_frontend_products": "627 total entries / 587 unique barcodes across 18 frontend JSONs",
    "excluded_no_bsip1_source": "106 products (chocolate_bars 23 + chocolate_tablets 35 + protein_bars 16 + protein_combined 32)",
    "supplement_skus": "85 in real_corpus_v3 — excluded (score_label path, not processing_quality path)",
    "open_decisions_requiring_d6_d7": "4 (OD-1 through OD-4)",
    "retained_guards_confirmed_active": "9 (V-1, CC-1, CC-2, SW-1, FL-1, FL-2, FL-3/FL-4, N-3 interim, dominance guardrail)",
    "output_artifacts_designed": "6 (movement_table, top_movers, read_mode_breakdown, anomaly_report, grade_dist, run_record)",
    "anomaly_taxonomy_classes": "8 (LARGE_MOVER, GRADE_MOVE, FLOOR_CONFLICT, GUARD_UNTRIGGERED, INVERSION_CANDIDATE, COMPONENT_B_NONE, KNIFE_EDGE, NESTED_LABEL, BASELINE_MISMATCH)",
    "new_engine_files": "1 edited (score_engine.py), 2 created (run_shadow_dechain_v1.py, candidate_engine_utils.py)",
    "worktree_branch": "task-395-dechain-v1"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v3.md (v3.1 NC-2 addendum included)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/structured_ingredient_reader.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v5_1.py (full, 1281 lines)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/score_engine.py (lines 1-120, 1542-1628, 2130-2310, 2540-2620)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/nova_proxy.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/run_task395_dechain_drift.py (lines 1-120)", "exit_code": 0},
    {"cmd": "PowerShell: Get-ChildItem 03_operations/bsip2/proto_v0/src/ — inventory of existing batch runners", "exit_code": 0},
    {"cmd": "PowerShell: Get-ChildItem 02_products/ — category directory survey", "exit_code": 0},
    {"cmd": "PowerShell: Get-ChildItem bari-web/src/data/comparisons/*.json — live frontend file inventory", "exit_code": 0},
    {"cmd": "PowerShell: ConvertFrom-Json — product counts per frontend file", "exit_code": 0},
    {"cmd": "PowerShell: barcode dedup across all frontends — 627 total / 587 unique", "exit_code": 0},
    {"cmd": "PowerShell: scoring trace + ingredient field detection per frontend", "exit_code": 0},
    {"cmd": "PowerShell: supplements run_full.py score_label check", "exit_code": 0}
  ],
  "not_done": [
    "Engine src edits (score_engine.py BARI_DECHAIN_V1 branch) — deferred to implementation worktree",
    "run_shadow_dechain_v1.py harness script — not written (design only this round)",
    "candidate_engine_utils.py — not written (design only)",
    "Shadow run not executed — no movement table, no anomaly report (requires engine edit first)",
    "Stage 2B whole_food_integrity matrix-signal rewrite — explicitly deferred per spec (Stage 2B)",
    "BARI-INVERSION-TEST-001 formal spec file — not yet created (required before Stage 1B per target spec §6.7)",
    "Nut/seed/legume label-derivability signal for Component B (chickpeas/legumes already in MARKERS as whole — Data Agent confirms lentils/chickpeas are present; full validation pending)",
    "OD-1 through OD-4 D6/D7 ratification — required before implementation agent begins engine edit",
    "Git worktree creation — not yet run (implementation next round)",
    "SHA256 of this file — orchestrator runs Get-FileHash after write"
  ],
  "self_check": "Acceptance test: Implementation agent runs run_shadow_dechain_v1.py --self-gate against 5 known barcodes, all Column A scores match committed baseline (exit code 0), then produces all 6 output artifacts with no BASELINE_MISMATCH entries. The harness exit code + artifact SHA256s are returned in the implementation agent's return block. No score is published; no frontend JSON is modified. This plan does not self-certify implementation correctness — the harness's Column A cross-check is the machine gate."
}
```
