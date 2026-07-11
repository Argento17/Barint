# TASK-600 Return

Proposed status: RETURNED. Router v5.2 pins the orchestrator/main-loop default to Opus 4.8; the SST Fable participant is explicit and convened only for `/stf` Strategy Task Force consultation, alongside the read-only Sol seat. Runtime routing, fallback triggers, telemetry, and all other capability bindings remain unchanged.

Verification output:

python -m py_compile 03_operations/router/dispatch.py
exit 0

[selftest-table] Layer 1: 13 rows byte-match capability_router_v5.md. OK
[selftest-table] Layer 2: 12 rows byte-match capability_router_v5.md. OK
[selftest-table] PASS

[selftest-route] PASS (15 fixtures)
[selftest-telemetry] PASS — start row, end duration/tokens, and pre-run crash entry

Changed files to verify:

- `01_framework/operations/capability_router_v5.md`: the new default-pin invariant and the STRATEGY-CONSULT row.
- `03_operations/router/dispatch.py`: byte-matched Layer 2 table transcription and v5.2 module prose.
- `tasks/returns/TASK-600_return.md`: return record.

```json
{
  "task": "TASK-600",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "01_framework/operations/capability_router_v5.md", "action": "modified", "sha256": "7ecb7d8325eccf418a3e7132925beb3671939cd728cd62f406d3eb362debb786"},
    {"path": "03_operations/router/dispatch.py", "action": "modified", "sha256": "5466d98f4af813b740d1a450d34b50ed2f3ed2d9b2d1d51cf08f32e8ee2eaa8b"}
  ],
  "counts": {
    "law_table_rows": "25/25 (13 Layer 1 + 12 Layer 2 rows; capability_router_v5.md and LAYER1_TABLE/LAYER2_TABLE; distribution: all rows byte-matched; median: PASS)",
    "route_fixtures": "15/15 (ROUTE_FIXTURES; distribution: all fixture capabilities passed; median: PASS)"
  },
  "commands_run": [
    {"cmd": "python -m py_compile 03_operations/router/dispatch.py", "exit_code": 0},
    {"cmd": "python 03_operations/router/dispatch.py --selftest-table", "exit_code": 0},
    {"cmd": "python 03_operations/router/dispatch.py --selftest-route", "exit_code": 0},
    {"cmd": "python 03_operations/router/dispatch.py --selftest-telemetry", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "--selftest-table passed: all 25 Layer 1/Layer 2 rows byte-match the edited router law."
}
```
