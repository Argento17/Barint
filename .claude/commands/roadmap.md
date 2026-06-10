---
description: Live decision map — Done · In-flight · Left + next action
allowed-tools: Bash, Read, Glob, Grep
---
Produce the live decision map directly from the registry.

## Steps

1. **Read the live registry:** Glob `C:\Bari\tasks\TASK-*.md` and read frontmatter from each file.
   For a quick count of CLOSED work, check `C:\Bari\tasks\closed\` (do not enumerate all 190+ files
   unless asked — just count).

2. **Produce the three-bucket decision map** with exact TASK ids:
   - **Done** — total CLOSED count + the most recently closed task(s) by `completed_at`.
   - **In-flight** — all IN_PROGRESS · BLOCKED · CHANGES_REQUESTED · RETURNED tasks with owner and priority.
   - **Left** — not-yet-opened work implied by `blocks`/`depends_on` gaps; category launch state if relevant.

3. **Next action** — apply the ladder: (1) BLOCKED waiting on a decision, (2) CHANGES_REQUESTED rework,
   (3) IN_PROGRESS blocking a launch, (4) highest-priority IN_PROGRESS, (5) RETURNED awaiting closure.
   State which rung fired and name the task.

4. **Critical path** — identify the longest dependency chain through open tasks.

Map first, prose second. Exact ids/counts — no rounding, no "several."
