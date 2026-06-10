# Bari Task Registry — CLOSED Archive

CLOSED task files live here. This directory is an archive — do not edit files here.

- `generate_dashboard.py` reads both `tasks/` and `tasks/closed/` for full history.
- CC Agent reads `tasks/closed/` only for specific historical lookups, not on every audit.
- When CC closes a task, it sets `status: CLOSED` in the frontmatter **and** moves the file here.
