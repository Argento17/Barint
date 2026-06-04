---
description: CC Agent — live roadmap / decision map (Done · In-flight · Left + next action)
allowed-tools: Bash, Read, Glob, Grep, Agent
---
Act as the **CC Agent** (`.claude/agents/cc-agent.md`).

## Source of truth — read the LEAN view, not the raw registry
The generator pre-computes everything this map needs into **`05_command_center\command_center_live.json`**
(~16 KB). **Read that one file** — it already contains `next_action`, `critical_path`
(`longest_chain` + `top_unblockers`), `task_summary` (all counts), `drift`, `open_tasks` (every
non-closed task with detail), `category_state`, `banked_assets`, and `alerts`.

- **Do NOT** `Select-String` / `Grep` across `C:\Bari\tasks\*.md` to derive status, counts, or
  `cc_reviewed` — that data is already in the lean JSON. Sweeping 160+ files re-derives computed data
  and burns the context window.
- **Do NOT** read `command_center.json` (205 KB) or `command_center_archive.json` (292 KB) for the map.
- Open an individual `tasks\TASK-NNN.md` **only** to verify a specific claim (e.g. a close-readiness
  gate on one task) — never to build the map. The registry still wins on any disagreement with the JSON;
  if the lean JSON looks stale or contradicts a task file you happened to open, surface it and trust the
  registry.

## Steps
1. **Freshness first** — run (single command, from the command-center dir so the `generate_dashboard`
   import resolves):
   `cd C:\Bari\05_command_center; python check_drift.py --quiet`
   It prints one line of JSON (`{"clean": true/false, "counts": {...}}`) and exits 1 if drift is found.
   If not clean (or `command_center_live.json`'s `meta.stale` is true), run
   `python generate_dashboard.py` once and note you refreshed. Otherwise do **not** regenerate.
2. **Read** `command_center_live.json` and produce the **Decision map** — three buckets, exact TASK ids:
   - **Done** — report `executive.latest_completed_task` + the `task_summary.closed` total count.
     Do **not** enumerate all closed tasks (there are ~192); name only the most recent / those relevant
     to the current question.
   - **In-flight** — from `open_tasks`: IN_PROGRESS · BLOCKED · CHANGES_REQUESTED · RETURNED-awaiting-CC.
   - **Left** — not-yet-opened work implied by `blocks`/`depends_on` gaps + `category_state` launch state.
3. **Critical path** + **top unblockers** — read straight from `critical_path.longest_chain` /
   `critical_path.top_unblockers`.
4. **Next action** — read `next_action` (the generator already resolved the ladder rung:
   BLOCKED-on-decision → CHANGES_REQUESTED → IN_PROGRESS blocking a launch → highest-priority
   IN_PROGRESS → RETURNED awaiting review). State which rung fired.
5. **Open `ROADMAP_REVIEW` items** — from `open_tasks`, those with `roadmap_impact: true` and no
   `cc_reviewed` set.

Map first, prose second. Exact ids/counts only — no rounding, no "several".
