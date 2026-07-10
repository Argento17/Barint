# TASK-589 Return

Proposed status: RETURNED (not closed).

Changed [dispatch.py](../../03_operations/router/dispatch.py):

- `dispatch.py:460` emits explicit `dispatch_start` and `dispatch_end` events, preserving compatibility with historical rows that have no event field.
- `dispatch.py:755`, `dispatch.py:773`, `dispatch.py:793`, `dispatch.py:930`, `dispatch.py:940`, `dispatch.py:951`, `dispatch.py:961`, and `dispatch.py:1050` write an entry row before their lane runner can be invoked.
- `dispatch.py:826` parses Codex token-usage summaries best-effort; `dispatch.py:904` records monotonic elapsed time and passes both values to completion telemetry.
- `dispatch.py:1306` adds the pure-Python mocked-runner telemetry check.

Verification output:

```
python 03_operations/router/dispatch.py --selftest-table
[selftest-table] Layer 1: 12 rows byte-match capability_router_v5.md. OK
[selftest-table] Layer 2: 11 rows byte-match capability_router_v5.md. OK
[selftest-table] PASS

python 03_operations/router/dispatch.py --selftest-route
[selftest-route] PASS (14 fixtures)

python 03_operations/router/dispatch.py --selftest-telemetry
[selftest-telemetry] PASS — start row, end duration/tokens, and pre-run crash entry
```

Verify the telemetry selftest uses a temporary log, mocks the Codex runner, proves a start row, duration and token fields on its end row, and retains the second call's start row when the mocked runner raises.

```json
{
  "task": "TASK-589",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/router/dispatch.py", "action": "modified", "sha256": "f2dc36ec03e83a37fe1880cca4a989a7dfc99c2e7053d38247aaa3aa0e2b9835"}
  ],
  "counts": {
    "mocked_telemetry_assertions_passed": "4/4 (cmd_selftest_telemetry: start, end duration/tokens, crash entry, token parser)"
  },
  "commands_run": [
    {"cmd": "python -m py_compile 03_operations\\router\\dispatch.py", "exit_code": 0},
    {"cmd": "python 03_operations\\router\\dispatch.py --selftest-table", "exit_code": 0},
    {"cmd": "python 03_operations\\router\\dispatch.py --selftest-route", "exit_code": 0},
    {"cmd": "python 03_operations\\router\\dispatch.py --selftest-telemetry", "exit_code": 0},
    {"cmd": "git diff --check", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\TASK-589_return.md --root .", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Offline mocked-runner telemetry check passed: start row is written before runner invocation, completion includes duration_s and tokens_used, and a runner exception leaves its entry row."
}
```
