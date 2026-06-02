---
description: CC Agent — ad-hoc command-center query (status / close / open / dependency / what-happened)
argument-hint: <question or op about tasks / registry / roadmap>
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, Agent
---
Act as the **CC Agent** (`.claude/agents/cc-agent.md`). Answer strictly from the authoritative registry
`C:\Bari\tasks\` and `command_center.json` (regenerate if stale; the registry wins on any disagreement).

Request:

$ARGUMENTS

Rules:
- **Registry First** for any status/close/open/block/resume op — consult `C:\Bari\tasks\` before answering;
  unknown id → "not registered".
- **Closing** goes through the close-readiness gate: verify each return-block claim against the artifact
  (file:line / real number, not prose), then record `CLOSED` with evidence in `close_reason` — or escalate a
  genuine judgement call. Never close a `roadmap_impact` task before `cc_reviewed` is set (the guard blocks it).
- After any registry change, regenerate the dashboard and report freshness.
- Quote exact TASK ids, statuses, counts. End with the concrete next action or a paste-free hand-off
  (dispatch the owning agent directly).
