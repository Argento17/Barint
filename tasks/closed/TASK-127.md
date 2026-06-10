---
id: TASK-127
title: Pin Command Center tooling to C:\Bari\.venv interpreter
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Seems alright"
depends_on: []
blocks: []
category_id: null
summary: >
  Make dashboard generation interpreter-independent: new_task.py must invoke the venv Python for the regenerate (not sys.executable / whatever is on PATH), and generate_dashboard.py must re-exec under C:\Bari\.venv if not already running there. Fixes the PyYAML-missing regen failure observed when new_task.py ran under system Python (TASK-126).
---

# TASK-127 — Pin Command Center tooling to C:\Bari\.venv interpreter

Dashboard generation no longer depends on whichever Python is on PATH.

**Changes**
- `generate_dashboard.py` — added an interpreter guard at module top: if the
  running interpreter is not `C:\Bari\.venv\Scripts\python.exe`, it re-execs under
  the venv (no-op once already there; no re-exec loop). PyYAML-missing message now
  points at the venv pip.
- `new_task.py` — the regenerate subprocess now invokes `REGEN_PY` (the venv Python),
  not `sys.executable`. Falls back to `sys.executable` only if the venv is absent.

**Verification**
- `py generate_dashboard.py` and `python generate_dashboard.py` (system Python at
  `C:\Python314`, no PyYAML) both re-exec under the venv and regenerate cleanly —
  the exact failure mode seen in TASK-126.
- Dashboard remains GREEN, 0 drift.

## Proposed disposition: RETURNED — awaiting Central Controller close
Agent does not self-CLOSE (registry_protocol_v1).
