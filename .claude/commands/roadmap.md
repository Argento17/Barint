---
description: CC Agent — live roadmap / decision map (Done · In-flight · Left + next action)
allowed-tools: Bash, Read, Glob, Grep, Agent
---
Act as the **CC Agent** (`.claude/agents/cc-agent.md`). Work strictly from the authoritative registry
`C:\Bari\tasks\` and the derived `05_command_center\command_center.json` (the registry wins on any
disagreement).

1. **Freshness first** — run `python 05_command_center\check_drift.py`; if drift / snapshot-stale,
   run `python 05_command_center\generate_dashboard.py` and note you refreshed.
2. **Decision map** — produce the three buckets with exact TASK ids:
   - **Done** (CLOSED, newest first)
   - **In-flight** (IN_PROGRESS · BLOCKED · CHANGES_REQUESTED · RETURNED-awaiting-CC-review)
   - **Left** (not-yet-opened work implied by `blocks`/`depends_on` gaps + category launch state)
3. **Critical path** through the dependency graph, and **top unblockers**.
4. **Next action** — which ladder rung fired (BLOCKED-on-decision → CHANGES_REQUESTED → IN_PROGRESS
   blocking a launch → highest-priority IN_PROGRESS → RETURNED awaiting review).
5. **Open `ROADMAP_REVIEW` items** awaiting CC sign-off (roadmap_impact + no cc_reviewed).

Map first, prose second. Exact ids/counts only — no rounding, no "several".
