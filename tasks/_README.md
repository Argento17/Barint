# Bari Task Registry — AUTHORITATIVE

**This directory (`C:\Bari\tasks\`) is the single source of truth for all tracked tasks.**

- One `TASK-NNN.md` file per task. Task state lives in the YAML frontmatter `status:` field.
- **ID allocation: scan BOTH `tasks/` AND `tasks/closed/` for the highest `TASK-NNN` before picking the next id.** Closed tasks are moved out of `tasks/`, so the live dir alone undercounts. (2026-06-10 incident: a new task was drafted as TASK-223 against the live dir only — 223/224/225 already existed in `closed/` from a parallel session — and the close-move overwrote `closed/TASK-223.md`. The new task was renumbered to TASK-226 and the original ECS-v1 record reconstructed from artifacts.)
- States (Registry Protocol v1, no others): `IN_PROGRESS` · `BLOCKED` · `RETURNED` · `CHANGES_REQUESTED` · `CLOSED`.
- **This directory contains live (non-CLOSED) tasks only.** Closed tasks live in `tasks/closed/`. CC moves them on close.
- The dashboard is **derived** from these files: `python 05_command_center/generate_dashboard.py` reads both `tasks/` and `tasks/closed/`. Never hand-edit `command_center.json`.
- Only the **Central Controller** records `CLOSED` and immediately moves the file to `tasks/closed/`. Agents propose `RETURNED` / `BLOCKED` in their return block.

## Governance
- `01_framework/operations/work_classification_v1.md` — Conversation Work vs Registry Work (what becomes a task at all).
- `01_framework/operations/registry_first_rule_v1.md` — consult this registry before any TASK-XXX operation.
- `01_framework/operations/registry_protocol_v1.md` — lifecycle, return format, acceptance/rejection.

## Non-authoritative
`C:\bari\bari-web\Bari\01_framework\operations\task_registry_v1.md` is a **frozen historical snapshot only** — not a live registry. Do not edit or consult it for current state.
