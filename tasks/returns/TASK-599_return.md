# TASK-599 Return

Proposed status: RETURNED. Router v5.1 now records the owner tier map, adds explicit-only
STRATEGY-CONSULT routing, sends BUILD-HEAVY to Terra, and provides a read-only Sol
consultation lane whose stdout is the deliverable.

Verification output:

python -m py_compile 03_operations/router/dispatch.py
exit 0

[selftest-table] Layer 1: 13 rows byte-match capability_router_v5.md. OK
[selftest-table] Layer 2: 12 rows byte-match capability_router_v5.md. OK
[selftest-table] PASS

[selftest-route] PASS (15 fixtures)
[selftest-telemetry] PASS — start row, end duration/tokens, and pre-run crash entry
Changed files to verify:

- `01_framework/operations/capability_router_v5.md`: Layer 0 invariant 9 and Layer 1/2 law tables.
- `03_operations/router/dispatch.py`: mirrored tables, `strategist_consult()`, and route fixture battery.

```json
{
  "task": "TASK-599",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "01_framework/operations/capability_router_v5.md", "action": "modified", "sha256": "a7d8bb7cd9337429e1e97c7650ca55697bb27325d39dc88f0900088d9d41c049"},
    {"path": "03_operations/router/dispatch.py", "action": "modified", "sha256": "03de872d62c12826cdf6debf0b8e184bdf8ca508a827294b36913202f6166d5e"}
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
