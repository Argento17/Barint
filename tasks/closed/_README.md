# Bari Task Registry — CLOSED Archive

CLOSED task files live here. This directory is an archive — do not edit files here.

- `generate_dashboard.py` reads both `tasks/` and `tasks/closed/` for full history (run manually when needed).
- When the orchestrator closes a task, it sets `status: CLOSED` in the frontmatter **and** moves the file here.
- All CLOSED tasks carry `close_reason` citing the artifact or evidence that satisfied the DoD.
