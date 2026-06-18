---
description: Orchestrator — live roadmap / decision map (Done · In-flight · Left + next action), read straight from the registry.
allowed-tools: Bash, Read, Glob, Grep
---
You are **the orchestrator** producing a decision map. There is no derived dashboard and no CC agent —
the **registry (`C:\Bari\tasks\`) is the single source of truth** and `tasks\DISPATCH_BOARD.md` is its
live view. Read those directly; don't reconstruct state from anywhere else.

## Source of truth — read the lean view first
1. **Read `tasks\DISPATCH_BOARD.md`** — it carries THE ROAD (the ordered factory plan, what's DONE vs
   the current move), orchestrator law, and lane state. This is the spine of the map.
2. **Then the live registry** for open work: list `tasks\TASK-*.md` (the ~live set; CLOSED files live in
   `tasks\closed\` and are out of the live set by design). Open the handful of open task files you need
   for status / `depends_on` / `blocks` / `priority`. Do **not** read `tasks\closed\` to build the map —
   closed work is done; name only the most recent or directly-relevant closed ids from the board.

## Produce the map — three buckets, exact TASK ids
- **Done** — the latest completed moves from THE ROAD + the most recent CLOSED ids relevant to the
  question. Don't enumerate the whole archive.
- **In-flight** — open `tasks\TASK-*.md`: IN_PROGRESS · BLOCKED · CHANGES_REQUESTED · RETURNED-awaiting-verify.
- **Left** — not-yet-opened work implied by `blocks`/`depends_on` gaps + the unfinished moves on THE ROAD.

## Critical path + next action
- **Critical path** — the longest dependency chain through the open set, and the top unblockers (tasks
  whose close frees the most downstream work).
- **Next action** — apply the ladder and state which rung fired: (1) BLOCKED waiting on a decision,
  (2) CHANGES_REQUESTED rework, (3) IN_PROGRESS blocking a launch, (4) highest-priority IN_PROGRESS,
  (5) RETURNED awaiting verification. If THE ROAD has an unfinished move, that is the next action.

Map first, prose second. Exact ids/counts only — no rounding, no "several". This command is read-only;
to actually dispatch and close, use `/orchestrate`.
