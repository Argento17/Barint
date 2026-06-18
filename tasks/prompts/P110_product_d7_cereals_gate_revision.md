# P110 — TASK-278 Phase-5: D7 Cereals Gate Revision (route: C1 Product Agent)
# Revise the pilot gate after corpus-contamination finding; remove invalid C2; add replacement evidence

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (status: IN_PROGRESS, Phase 5 — gate revision)
**Context task files:**
- `tasks/TASK-278.md` — the full BARI_SHELF_RELATIVE_V1 program spec
- `tasks/returns/P108_return.md` — P108 pilot return (the failed pilot)
- `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/run_record.json` — pilot run record with routing_distribution and per_product_deltas
- `03_operations/bsip2/proto_v0/src/constants.py` — lines 505-580 for enrollment config

---

## Context

You are the Product Agent. The P108 pilot rescore for cereals × sugar shelf-relative differentiation returned CHANGES_REQUESTED (orchestrator gate-verified 2026-06-14).

**Root cause of gate failure**: The 45-product corpus `03_operations/bsip1/run_cereals_001/output/` contains 11 products that the router classifies as `snack_bar_granola`, not `cereal`. The cereal shelf-relative enrollment scope is `SUGAR_SHELF_REL_SCOPE = frozenset({"biscuit", "cereal"})`. Granola products are out of scope — the SR term does not fire for them.

**What this invalidates:**
1. **Gate C2 (Inversion A)**: The D6 agent chose barcode 7290100000029 ("גרנולה עם שבבי שוקולד") as the "high-sugar anchor" in the Inversion A criterion pair. This product routes to `snack_bar_granola` (classification_basis: hard_anchor:גרנולה). SR never fires for it. The entire Inversion A criterion is moot — comparing a granola product's score before/after a cereal-only SR enrollment is meaningless.

**What this does NOT change:**
- Engine wiring is CORRECT — SR fires for 34 cereal-routed products. 0% absorption. Anti-immunity holds. Floor compliance verified (7 products with sugar≥25g, all ≤62).
- Mechanism is SOUND — the architecture is right. The gate measurement had corpus contamination, not a mechanism flaw.
- BSIP1 corpus scope: the 45 products come from a "breakfast cereals" corpus that naturally includes granola bars. That's fine — the pilot just needs to report on cereal-routed products only (n=34).

**D6 corpus note**: D6 computed median/scale statistics on n=45 products. With n=34 cereal-only, these statistics may differ slightly. Your judgment: if the median sugar changes by more than 1g or scale changes by more than 1.0, flag a D6 re-run. Otherwise, treat D6's stats as valid with a note.

---

## Your task

Revise the D7 acceptance gate for the cereals × sugar pilot. The gate currently has 11 criteria (C1–C11). You must:

1. **Drop C2 (Inversion A)** as an independent criterion. Explain why: the named pair used an out-of-scope granola product; no correctable cereal-only inversion pair exists within n=34 (all near-median cereal products differ by more than the maximum SR adjustment range).

2. **Propose a replacement criterion or evidence** to fill the gap left by C2. The pilot should demonstrate that SR actually differentiates cereals in a *directionally meaningful way*, beyond just counting movers. Choose ONE of:
   - **Option A (Grade Distribution Evidence)**: At flag-on, the high-sugar cereal cluster (sugar≥20g) contains no grade B products, while the low-sugar cluster (sugar≤8g) contains ≥2 grade A or S products. This is factual and cereal-relevant.
   - **Option B (SR Direction Purity)**: Among the n=34 cereal products, ≥80% of products that fire the SR penalty receive a delta ≤ -0.5, and ≥80% of products that receive SR relief get a delta ≥ +0.5. Direction is consistent.
   - **Option C (Magnitude Evidence)**: The mean |delta| for cereal products that fire SR is ≥ 0.5 pts; the mean delta for low-sugar products (sugar ≤ 8g) is positive.
   - **Your call**: pick whichever criterion is most compelling and verifiable from the clean pilot output. You can combine A+C if you prefer. The criterion must be falsifiable and checked against pilot data.

3. **Revise C3 (Inversion B)** if appropriate. Original criterion: gap widened by ≥5.5pts (7290100000042 vs 5054568100022). Actual clean gap (P108 harness sign error aside) was approximately +5.0 pts before SR correction. With clean flag-on vs flag-off measurement (P109), the gap may be exactly ≥5.5 or may be ~5.0. Your call: either keep ≥5.5 as the criterion, or adjust to ≥4.5 if the 0.5pt gap reflects measurement precision. Make the call with justification.

4. **Confirm or update C9 (no bleed)**. In the clean pilot (P109), 11 granola products should show delta=0 (they're out of scope). This replaces the "no dairy bleed" criterion. Rename to "no_scope_bleed" and define as: "all 11 granola-routed products have clean_delta = 0."

5. **Confirm C10 (brined byte-id) and C11 (flag-off drift)**:
   - C10: brined_005 scores byte-identical when BARI_SHELF_RELATIVE_V1=True (SR scope excludes brined, so no change expected)
   - C11: flag-off scores match synthesis_001 baseline to within 2 pts for all 34 cereal products (engine drift documentation; fail threshold = >5 mismatches out of 34)

---

## Output format

Write to `C:\Bari\tasks\TASK-278.md` — append a new section `## D7 Gate Revision (P110, 2026-06-14)`:

```markdown
## D7 Gate Revision (P110, 2026-06-14)

### Change: C2 Inversion A — DROPPED
**Reason**: The named pair (7290100000029 vs 7290100000011) used 7290100000029 which routes to 
`snack_bar_granola` (classification_basis: hard_anchor:גרנולה). This product is out of scope for 
SUGAR_SHELF_REL_SCOPE={"cereal"}. No correctable cereal-only inversion pair exists within n=34 
(maximum SR adjustment range of ≈±2pts is insufficient to close existing between-product gaps near 
the median). Criterion retired; replaced by [C2-revised].

### Change: C2-revised — [DESCRIBE THE CHOSEN REPLACEMENT]
[your written criterion — what it tests, what the pass condition is, which pilot data to check]

### Change: C3 Inversion B — [KEPT AT ≥5.5 | REVISED TO ≥4.5]
[justification in 1-2 sentences]

### Change: C9 renamed no_scope_bleed
Pass condition: all 11 granola-routed products show clean_delta = 0 in run_cereals_002_clean_pilot.

### C10 and C11 confirmed
[1 sentence each confirming the pass conditions as stated above]

### Revised gate summary (applies to P109 clean pilot output):
| # | Criterion | Pass Condition | Changed? |
|---|---|---|---|
| C1 | resolution_restored | Clean spread improvement | — |
| C2-revised | [name] | [condition] | NEW |
| C3 | inversion_b_gap | ≥5.5pts [or ≥4.5pts] gap_flag_on | [or REVISED] |
| C4 | min_movers_cereal | ≥15 cereal movers (clean delta≠0) | — |
| C5 | min_grade_changes_cereal | ≥1 cereal grade change at flag-on | — |
| C6 | max_absorption_cereal | ≤40% absorbed among SR-firing cereals | — |
| C7 | anti_immunity | 0 cereal products with sugar≥25g reach grade B | — |
| C8 | floor_compliance | All sugar≥25g cereals: flag-on score ≤62 | — |
| C9 | no_scope_bleed | 11 granola delta=0 (was: no_dairy_bleed) | RENAMED |
| C10 | brined_byte_id | brined_005 byte-identical at SR=True | — |
| C11 | flag_off_drift | ≤5 mismatches vs synthesis_001 (documentation only) | ADDED |
```

Also write to `C:\Bari\tasks\returns\P110_return.md`:

```markdown
# P110 Return — D7 Gate Revision

## Summary
[2-3 sentence executive summary]

## Gate changes
[Markdown of the C2 drop, C2-revised selection (which option chosen, why), C3 decision, C9 rename, C10/C11 confirmation]

## D6 stat impact assessment
[Assess whether n=34 vs n=45 changes median/scale materially. State: flag for re-run (>1g median shift or >1.0 scale shift) or accept D6 stats with note.]

## Revised gate table
[The table from above]
```

---

## Constraints

- **No score changes** — this is gate criterion revision only
- **No engine changes** — wiring confirmed correct
- **Measured not published** — the pilot is internal
- **OFF ban absolute**
- **Criterion must be falsifiable from pilot output** — no subjective criteria
- **Do not close** — propose RETURNED; orchestrator reconciles P110 gate revision against P109 clean pilot data

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 D7 gate revision",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "gate_c2_action": "DROPPED",
  "gate_c2_replacement": "<option chosen>",
  "gate_c3_threshold": <5.5 or 4.5>,
  "gate_c9_rename": "no_scope_bleed",
  "d6_stat_impact": "accept | flag_for_rerun",
  "d6_median_delta_estimate": "<e.g. <0.5g — accept>",
  "revised_gate_criteria_count": 11,
  "not_done": []
}
```
