# Website-snapshot salvage — 2026-06-01 (TASK-131, Phase 1)

These are the only files that existed in the stale nested snapshot
`C:\Users\HP\bari\Bari\` but had **no counterpart** in the authoritative Agent OS
(`C:\Bari\`). They were quarantined here before the snapshot was deleted so nothing
is lost. They are NOT yet promoted into the live tree — the data-agent owner should
evaluate and promote/discard.

## Triage

| File | Disposition |
|---|---|
| `01_framework/operations/task_registry_v1.md` | **Disposable.** The frozen, non-authoritative registry snapshot. Superseded by `C:\Bari\tasks\`. Kept only for reference. |
| `01_framework/operations/command_center_registry_support_v1.md` | **Disposable.** Header self-declares "MOVED — canonical now in `C:\Bari\01_framework\operations\` … NON-AUTHORITATIVE" (TASK-117). |
| `03_operations/bsip2/proto_v0/src/analyze_spread_subtype_calibration.py` | **Evaluate.** Real analysis harness; referenced by `bsip2_spread_subtype_calibration_proposal_v1.md`. Promote to live `03_operations/bsip2/proto_v0/src/` if still needed. |
| `03_operations/bsip2/proto_v0/src/run_spread_subtype_regression.py` | **Evaluate.** Companion regression runner. |
| `03_operations/bsip2/proto_v0/src/spread_subtype_impact.json` | **Evaluate.** Output of the harness above. |

## Caution before promoting the bsip2 scripts
The snapshot's shared `proto_v0/src` files (`constants.py`, `router_v2.py`,
`score_engine.py`, `signal_extractor.py`) were **older** than the live `C:\Bari`
versions. These salvaged scripts were written against those older modules and may
need reconciliation before they run against current proto_v0 code. Do not assume
drop-in compatibility.
