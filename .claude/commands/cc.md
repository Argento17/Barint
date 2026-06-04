---
description: CC Agent — ad-hoc command-center query (status / close / open / dependency / what-happened)
argument-hint: <question or op about tasks / registry / roadmap>
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, Agent
---
Act as the **CC Agent** (`.claude/agents/cc-agent.md`). The registry wins on any disagreement.

Request:

$ARGUMENTS

Rules:
- **Pick the cheapest source for the request:**
  - *Read-only query* (status, counts, what's blocked, next action, dependency map) → read
    **`05_command_center\command_center_live.json`** (~16 KB; has `open_tasks`, `task_summary`,
    `next_action`, `critical_path`, `drift`). Do **not** sweep `C:\Bari\tasks\*.md` or read the
    205 KB `command_center.json` for a read. Open a single `tasks\TASK-NNN.md` only to verify one
    specific task's detail.
  - *Op* (close/open/block/resume/reopen, or close-readiness verification) → go to the specific
    `tasks\TASK-NNN.md` file directly (Registry First). Unknown id → "not registered".
- **Closing** goes through the close-readiness gate: verify each return-block claim against the artifact
  (file:line / real number, not prose), then record `CLOSED` with evidence in `close_reason` — or escalate a
  genuine judgement call. Never close a `roadmap_impact` task before `cc_reviewed` is set (the guard blocks it).
- After any registry change, regenerate the dashboard and report freshness.
- Quote exact TASK ids, statuses, counts. End with the concrete next action or a paste-free hand-off
  (dispatch the owning agent directly).
