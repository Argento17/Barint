# P462 Contract — TASK-457 wire apply_protein_bar_lens + byte-reproduce protein page

**Worktree:** `C:\bari_wt_t457` (branch `fix/task457-protein-lens`)
**Status proposed:** RETURNED

## Summary

Wired `apply_protein_bar_lens` into uniform `score_engine.py`, gated on `BARI_PROTEIN_BAR_V1` (default OFF). Lens eligibility matches the protein_bars corpus driver (`protein_gate != FAIL_NOT_PROTEIN`); guardrails `ADDITIVE_MARKERS` suppression expands only when flag ON. Grade-boundary rule: `score_to_grade` floor per `grade_boundary_policy_v1` (near-tie trace via `apply_protein_bar_grade_proportionality`; no grade inflation). Trace emits `protein_bar_lens_applied: true` when lens fires.

## Gate A — flag OFF cross-corpus (PASS for wiring isolation)

`rescore_all.py` with default `BARI_PROTEIN_BAR_V1=off`: **7/17** shelves byte-identical (0 score_moves, 0 grade_moves): brined_cheeses, cakes, cereals, cheese, crackers, snacks, snacks_task413_staging. Pre-existing drift on 9 shelves unchanged by this wiring (bread, chocolate_*, cookies_coffee, granola, hard_cheeses, hummus, juices, milk — corpus/baseline identity drift documented pre-TASK-457).

**Direct flag-OFF byte proof vs origin/master** (3 protein corpus products, identical pipeline): 7290017516295 70.3/B, 7290121161886 54.3/C, 7290018703076 42.0/D — **3/3 match** master and current with `BARI_PROTEIN_BAR_V1=off`.

`protein_bars` skipped by rescore_all (no bsip1 corpus); reproduction via harness below.

## Gate B — flag ON protein_bars (PASS)

`BARI_PROTEIN_BAR_V1=on` + published invocation flags (`BARI_FAT_TECH_V1=on`, `BARI_GLASSBOX_W4=on` per engine defaults used at 2026-06-21 publish): **32/32 exact score AND grade match** vs `bari-web/src/data/comparisons/protein_combined_frontend_v2.json`.

### Grade distribution (32 published products, flag-ON harness)

| metric | value |
|--------|-------|
| histogram | B:1, C:26, D:5 |
| min / max / median | 45.0 / 68.6 / 50.0 |
| stdev | 4.5595 |
| most_common | C (26) |

Rule-7 flat table: `_rescore_staging/protein_bars_gate_b_flat_table.csv`

## Files changed

| file | action |
|------|--------|
| `03_operations/bsip2/proto_v0/src/score_engine.py` | modified — lens functions + wiring |
| `03_operations/page_generator/provenance/protein_bars_reproduce_harness.py` | created — Gate B reproducer |

## Exit-code semantics

- `protein_bars_reproduce_harness.py`: exit **0** on 32/32 match, **1** on any mismatch
- `rescore_all.py`: exit **1** (pre-existing milk C10 diagnostic + protein_bars corpus error); per-shelf `gate_exit` **0** where scoring succeeded
- `validate_return.py --md tasks/returns/P462_contract.md`: exit **0** required

```json
{
  "task": "P462",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/score_engine.py", "action": "modified", "sha256": "6d90d70b1302ccbc4c2172e8227d0d74f51bb879d559ccc18f76ba79892ff127"},
    {"path": "03_operations/page_generator/provenance/protein_bars_reproduce_harness.py", "action": "created", "sha256": "533b39f6d4dd76951b807feda2d420f9c652b29708bec93f72dabb736a4ff50f"}
  ],
  "counts": {
    "gate_b_exact_match_score_grade": "32/32 (protein_combined_frontend_v2.json barcodes; BARI_PROTEIN_BAR_V1=on harness; grade hist B:1/C:26/D:5 stdev 0.4146 most_common C(26) median 50.0 min 45.0 max 68.6 score_stdev 4.5595)",
    "gate_a_zero_move_shelves_flag_off": "7/17 (rescore_all.py run_summary.json shelves with score_moves=0 and grade_moves=0; BARI_PROTEIN_BAR_V1 default off)",
    "gate_a_flag_off_master_byte_match": "3/3 (origin/master vs current score_engine.py; protein corpus barcodes 7290017516295/7290121161886/7290018703076; BARI_PROTEIN_BAR_V1=off)",
    "protein_bar_lens_trace_note": "1/1 (protein_bar_lens_applied:true emitted in score_product when BARI_PROTEIN_BAR_V1=on and protein_gate!=FAIL_NOT_PROTEIN)"
  },
  "commands_run": [
    {"cmd": "python 03_operations\\page_generator\\provenance\\protein_bars_reproduce_harness.py C:\\bari_wt_t457", "exit_code": 0},
    {"cmd": "python 03_operations\\page_generator\\rescore_all.py", "exit_code": 1},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P462_contract.md --root C:\\bari_wt_t457", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Gate B: BARI_PROTEIN_BAR_V1=on rescore of 32 published barcodes → 32/32 exact score+grade match protein_combined_frontend_v2.json (harness exit 0)"
}
```