# TASK-552 Return — Scoring-engine ledger gap diagnosis

**Agent:** Nutrition Agent  
**Date:** 2026-07-11  
**Status proposed:** RETURNED  

## Summary

Root cause identified and fully reproduced. The ~4-point gap for barcode 7290102399802 is explained by the **ECS-v1 emulsifier complexity penalty** (`emul_comp_penalty = 4.0`) applied at `score_engine.py:3960` but never serialized by `trace_writer.py`. The score is arithmetically correct; the ledger field is absent.

Verified arithmetic:  
`62.89 (score_after_cap) − 2.0 (scaled_penalty) − 0.0 (polyol) − 4.0 (emul_comp) = 56.89 = score_after_penalty` ✓

The systemic scan found 1,165 / 5,747 traces with the same class of gap — all caused by `trace_writer.py` omitting `polyol_penalty` and `emulsifier_complexity_penalty` from its serialization whitelist (`trace_writer.py:78-83`). A second independent class (19 positive gaps, hummus floor) is from EV-094 floor raising `score_after_penalty` in traces pre-dating RT-10.

TASK-563 is a distinct defect (trace-to-frontend run_id mismatch). TASK-563 did not encounter the TASK-552 gap because its seed products had `emul_comp_penalty = 0`.

Recommended fix: add 6 missing fields to `trace_writer.py:assemble_trace()` penalty block. No score change required. No D7 tripwire.

---

```json
{
  "task": "TASK-552",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/nutrition/task552_ledger_gap_diagnosis_v1.md",
      "action": "created",
      "sha256": "3252705C5364EA94FE8F9C57E93D43BB2B24A131ECFD99E454A69F3B5B7D8373"
    }
  ],
  "counts": {
    "traces_scanned": "5747/5747 (all bsip2_trace.json under 02_products/; os.walk scan)",
    "traces_with_gap": "1165/5747 (gap_type=emul_field_missing: 1146 negative + 19 positive hummus floor)",
    "traces_no_gap": "4582/5747",
    "gap_negative_distribution": "min=-16.0 median=-4.0 max=-0.44 stdev varies by category (dairy_protein: 2.51, snack_bar_granola: 2.85, biscuit: 3.37)",
    "gap_positive_distribution": "19 hummus traces; min=3.97 max=29.21 (sauce_spread/default categories)",
    "traces_with_emulsifier_complexity_penalty_field": "0/5747 (field absent from all on-disk traces — trace_writer.py omits it)",
    "yogurt_task515_spoonable_traces": "99/99 missing emulsifier_complexity_penalty field",
    "seed_product_arithmetic": "62.89 - 2.0 - 0.0 - 4.0 = 56.89 matches trace score_after_penalty (tolerance 0.01)"
  },
  "commands_run": [
    {
      "cmd": "python -c '<scan 5747 traces under C:\\Bari\\02_products for score_after_cap - total_penalty_after_scaling - polyol_penalty vs score_after_penalty>'",
      "exit_code": 0
    },
    {
      "cmd": "python -c '<verify emul_comp_penalty arithmetic for barcode 7290102399802>'",
      "exit_code": 0
    },
    {
      "cmd": "python -c '<count emulsifier_complexity_penalty field presence across all 5747 traces>'",
      "exit_code": 0
    },
    {
      "cmd": "Get-FileHash '03_operations/reports/nutrition/task552_ledger_gap_diagnosis_v1.md' -Algorithm SHA256",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Spec: reproduce the arithmetic on 7290102399802 showing the unlogged delta. Result: 62.89 − 2.0 − 0.0 − 4.0 = 56.89 = trace score_after_penalty; delta is emul_comp_penalty=4.0 (ECS-v1, 2 distinct agents: modified_starch_stabilizer[med] + pectin[low]); omitted from trace_writer.py lines 78-83. Systemic scan: 1165/5747 gap traces, all gap_type=emul_field_missing. TASK-563 reconciliation: independent defects confirmed by TASK-563 close_reason citing internally-consistent arithmetic in that investigation's seed products."
}
```
