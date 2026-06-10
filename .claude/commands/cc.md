---
description: Registry query — task status / close / open / block / dependency / what-happened
argument-hint: <question or op about tasks / registry>
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
---
Direct registry operation. The registry wins on any disagreement.

Request:

$ARGUMENTS

Rules:
- **Registry First.** All ops consult `C:\Bari\tasks\TASK-NNN.md` directly. Unknown id → "not registered."
- **Read-only query** (status, counts, what's blocked, next action, dependency map) → read
  the relevant `tasks\TASK-NNN.md` files. For a full count, Glob `C:\Bari\tasks\TASK-*.md` and
  read frontmatter. For historical lookups, check `C:\Bari\tasks\closed\TASK-NNN.md`.
- **Close operation** → verify the return-block claims against the actual artifacts (file:line / real
  number), set `status: CLOSED` and `completed_at: YYYY-MM-DD` in the task frontmatter, add a
  `close_reason` citing evidence. Move the file from `tasks\TASK-NNN.md` → `tasks\closed\TASK-NNN.md`.
  Never close a task whose claims you cannot verify — set CHANGES_REQUESTED with the gap instead.
- **Other state changes** (block, resume, request changes) → edit the frontmatter `status:` field directly.
- Quote exact TASK ids, statuses, counts. End with the concrete next action.
