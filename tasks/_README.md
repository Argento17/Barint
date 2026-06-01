# Bari Task Registry — AUTHORITATIVE

**This directory (`C:\Bari\tasks\`) is the single source of truth for all tracked tasks.**

- One `TASK-NNN.md` file per task. Task state lives in the YAML frontmatter `status:` field.
- States (Registry Protocol v1, no others): `IN_PROGRESS` · `BLOCKED` · `RETURNED` · `CHANGES_REQUESTED` · `CLOSED`.
- The dashboard is **derived** from these files: `python 05_command_center/generate_dashboard.py` → `command_center.json` → `command_center_v4.html`. Never hand-edit `command_center.json`.
- Only the **Central Controller** records `CLOSED`. Agents propose `RETURNED` / `BLOCKED` in their return block.

## Governance
- `01_framework/operations/work_classification_v1.md` — Conversation Work vs Registry Work (what becomes a task at all).
- `01_framework/operations/registry_first_rule_v1.md` — consult this registry before any TASK-XXX operation.
- `01_framework/operations/registry_protocol_v1.md` — lifecycle, return format, acceptance/rejection.

## Non-authoritative
`C:\bari\bari-web\Bari\01_framework\operations\task_registry_v1.md` is a **frozen historical snapshot only** — not a live registry. Do not edit or consult it for current state.
