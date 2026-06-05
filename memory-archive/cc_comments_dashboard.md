---
name: cc-comments-dashboard
description: "How CC Agent leaves concrete task comments that render in the Command Center dashboard — cc_comments frontmatter, flags, where it renders"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9093f0b6-f985-49cc-890e-6109f9a49062
---

The user (as CC Agent owner) wants CC's concrete comments on a task — after agent work — to
**show up directly in the dashboard, near that task**, not only in chat.

**Why:** chat comments evaporate; the dashboard is the live decision surface he actually reads.

**How to apply:** add a `cc_comments:` block to that task's **`.md` frontmatter** in `C:\Bari\tasks\`
(the authoritative source — `command_center.json` is derived and must never be hand-edited). Shape:
```yaml
cc_comments:
  - date: 2026-06-02
    flag: verify            # fyi (default) | verify | blocker
    text: "Before CLOSE: the TASK-039 fat register is now stale — regenerate or retire it."
```
Accepts a plain string, a list of strings, or a list of `{date, text, flag}`. Then run
`python 05_command_center/generate_dashboard.py`.

**Plumbing (built 2026-06-02, this session):**
- `generate_dashboard.py`: `_norm_cc_comments()` normalizes the field into each task dict.
- **Token-efficient split (sticker model):** full comment prose lives only in `command_center.json`
  (the board the HTML renders) and the source `.md`. The lean `command_center_live.json` — the per-session
  agent read path — carries only a compact **sticker**: `_live_view` pops `cc_comments` and emits
  `cc: [flags]` (e.g. `["verify","fyi"]`). ~12 chars vs ~744 for 2 comments; scales with volume. So agents
  scanning live.json see "TASK-150 has a verify-flagged CC note → go look", detail on demand. Do NOT put
  prose back into live.json.
- The morning digest (on-demand human report) keeps full text (`↳ CC: …` under each open task).
- `command_center.html` (reads the FULL json): `ccNotes(t)` renders a **collapsed badge** — a `<details>`
  whose summary is a compact flag-count chip (`🔍1 💬1 read`); clicking expands to the full `.cc-note` text.
  Objective heads use the `obj-cc` variant. Flag colors: fyi=blue 💬, verify=amber 🔍, blocker=red ⛔. Chosen
  over full-text rows for board scannability (user ruling 2026-06-02). Screenshots:
  `screenshots/cc_sticker_{collapsed,expanded}.png`.

So the loop is: do agent-work review → write `cc_comments` into the relevant TASK-NNN.md → regenerate →
the note appears under that task on the board. Verified live (screenshot `05_command_center/screenshots/
cc_comments_demo.png`; TASK-149/150 carry the first real comments). Related: [[cc_v3_1_upgrade]],
[[feedback_cc_recommendations]].

**Auto-invoke CC on roadmap-impacting returns (built 2026-06-02).** The user wants CC engaged + dashboard
refreshed every time a task returns with roadmap implications. Convention: the returning agent sets
`roadmap_impact: true` in the task frontmatter; CC, after reviewing, sets `cc_reviewed: <date>`.
- `generate_dashboard.py` reads both; emits a HIGH `ROADMAP_REVIEW` alert for any task that is
  RETURNED/CHANGES_REQUESTED + roadmap_impact + no cc_reviewed → so it can't be silently CLOSED.
- PostToolUse hook `.claude/hooks/regen-dashboard-on-task-change.ps1` (wired in `.claude/settings.json`,
  Write|Edit block): on any `tasks/TASK-*.md` write it (1) regenerates the dashboard, (2) if the change is a
  roadmap-impacting return with no cc_reviewed, emits `additionalContext` nudging the model to invoke CC Agent.
  Hooks can't spawn the subagent; this is the closest feasible (auto-refresh + nudge + standing alert).
- Loop closes when CC reviews → adds cc_comments → sets `cc_reviewed: <date>` → alert clears (verified on TASK-150).
