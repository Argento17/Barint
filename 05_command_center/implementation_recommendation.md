# Bari Command Center — Implementation Recommendation

**Task:** TASK-059  
**Owner:** Product Agent  
**Date:** 2026-05-31

---

## Recommendation Summary

**Build:** A single self-contained HTML file (`command_center.html`) that reads `command_center.json` from the same directory and renders it as a static dashboard. No server, no framework, no dependencies, no build step.

**Maintain:** A companion JSON file (`command_center.json`) that any agent updates as a task closeout step. Human-writable, human-readable without a renderer.

**Do not build yet:** A React component, a Next.js page, a real-time sync layer, or any form of animated UI.

---

## Rejected Alternatives

### Option A: Markdown snapshot (Claude-generated per session)

Claude reads the key state files at session start and generates a formatted markdown brief.

**Why rejected for MVP:**
- Not persistent — regenerated fresh every session, so state can drift between reads
- No single source of truth — Claude derives state from 10+ separate files, each of which may be partially out of date
- No ability to track alert history or decision resolution over time
- Useful as a fallback if the JSON file gets stale, but not as the primary system

**Keep as fallback:** If `command_center.json` is more than 7 days stale, Claude should note this and offer to regenerate the state from current files.

---

### Option B: Next.js page in the website repo (`/internal/command-center`)

Add an internal route to `C:\bari-web`.

**Why rejected for MVP:**
- Requires a running dev server or production deploy to view
- Couples an internal operational tool to the consumer website deployment cycle
- `C:\bari-web` is the consumer product — internal tooling should not live there
- Significantly higher implementation effort (TypeScript types, routing, data fetching contract)

**Viable for v2** if the team wants to access the command center from a URL rather than the filesystem.

---

### Option C: YAML file only (no renderer)

Maintain the state in a human-readable YAML file. Claude reads it at session start. No HTML renderer at all.

**Why rejected:**
- YAML is more readable than JSON but still requires mental parsing of nested structures
- No visual grouping — the eye cannot quickly scan 9 agents + 7 categories + N alerts as a table
- A minimal HTML table is 2–4 hours of work and pays for itself on first use

**Keep as fallback:** `command_center.json` is human-readable enough that a session without the renderer is acceptable.

---

## Recommended Implementation

### Two files

```
C:\Bari\05_command_center\
├── command_center.json       ← source of truth (maintained by agents)
├── command_center.html       ← renderer (maintained by Frontend Agent)
├── command_center_v1_spec.md
├── command_center_data_model.md
├── command_center_mvp_scope.md
└── implementation_recommendation.md
```

Open `command_center.html` in a browser. It reads `command_center.json` from the same directory via `fetch('./command_center.json')`.

**Constraint:** Modern browsers block `fetch()` for local `file://` URLs due to CORS policy. Two solutions, in order of preference:

1. **Serve with a one-command Python server** (preferred):
   ```powershell
   # From C:\Bari\05_command_center\
   python -m http.server 8080
   # Then open http://localhost:8080/command_center.html
   ```
   This is a single command, no installation required (Python is already present in the Bari environment), and takes under 5 seconds to start.

2. **Embed JSON inline in the HTML** (fallback):
   Instead of `fetch()`, embed the JSON directly as a JavaScript variable inside `command_center.html`. Update it by replacing the variable content when the JSON changes. This works from `file://` but requires an extra copy step on every update.

**Recommendation:** Use Option 1 (Python server). Add a PowerShell one-liner to the `command_center.html` header as a comment so the command is always visible.

---

### HTML Renderer — What to build

The renderer is intentionally minimal. It uses zero CSS frameworks, zero JavaScript libraries, zero CDN calls. Everything is inline.

**Layout:**

```
┌─────────────────────────────────────────┐
│ BARI COMMAND CENTER    [2/3 tasks] [1 HIGH] [1 NOW]
├─────────────────────────────────────────┤
│ ALERTS (if any)                          │
│  ▲ HIGH  ALT-001: Hummus — website/factory mismatch
├─────────────────────────────────────────┤
│ DECISION QUEUE                           │
│  DEC-001 [DECIDED] HUM-001 fat strategy...
├─────────────────────────────────────────┤
│ CATEGORY FACTORY BOARD                   │
│  Category  │ Products │ BSIP0 │ BSIP1 │ BSIP2 │ QA │ Dataset │ Website │ Launch
│  חומוס     │ 69       │ PASS  │ DONE  │ AUTH  │ P  │ NOT BUILT│ NOT STARTED │ PIPELINE
│  מעדנים   │ ~90      │ PASS  │ DONE  │ AUTH  │ P  │ DEPLOYED │ LIVE   │ LIVE
│  ...        │          │       │       │       │    │          │        │
└─────────────────────────────────────────┘
```

**Technology:**
- HTML5 + vanilla JavaScript (no framework)
- CSS: inline `<style>` block, monospace font, minimal color (black text, light grey alternating rows, red for CRITICAL/HIGH alerts, amber for MEDIUM, no other colors)
- JavaScript: one `fetch()` call to load JSON, then DOM manipulation to build tables
- Total file size target: < 150 lines of HTML + JS

**Color use (minimal, intentional):**

| Element | Color | Why |
|---|---|---|
| CRITICAL alert row | `#fee2e2` background | Immediate attention |
| HIGH alert row | `#fef3c7` background | Elevated attention |
| RESOLVED / PASS status | `#15803d` text | Confirmed good state |
| BLOCKED / FAIL / MISSING status | `#dc2626` text | Requires action |
| Section headers | `#111827` bold | Structure |
| All other text | `#111827` regular | Body copy |
| Table row alternating | `#f9fafb` | Readability |

No gradients. No shadows. No rounded corners. No icons (text labels only).

**Typography:**
- Font: system monospace (`font-family: ui-monospace, 'Cascadia Code', monospace`)
- Why monospace: columns align naturally; status codes are scannable at a glance; no webfont dependency
- Size: 13px body, 11px table cells, 15px section headers

---

### `command_center.json` — Seed File

A seed JSON file should be created alongside the spec documents, pre-populated with the current known state of Bari. This is the initial data that the renderer will display on first open.

**Seed state (current as of 2026-05-31):**

- Executive: 2 active tasks (TASK-059, TASK-060), latest completed is TASK-058
- Agents: All 9 present; Product Agent WORKING on TASK-059; others AVAILABLE or WAITING
- Categories: 7 rows (hummus pipeline-complete + 5 live + cereals queued)
- Decisions: DEC-001 (HUM-001, DECIDED)
- Alerts: ALT-001 (hummus website/factory mismatch, OPEN)

---

### Implementation Steps

**Step 1 — Create seed `command_center.json`** (Data Agent, 2–3 hours)
Populate the JSON file with current known state. Use the schema from `command_center_data_model.md`. Confirm all 7 categories, 9 agents, current decisions, and current alerts are represented accurately.

**Step 2 — Build `command_center.html`** (Frontend Agent, 3–5 hours)
Build the static HTML renderer per the layout and technology spec above. Three sections: Alerts, Decision Queue, Category Factory Board. Executive header. Vanilla JS, zero dependencies.

**Step 3 — Test on localhost** (Frontend Agent, 30 minutes)
```powershell
cd "C:\Bari\05_command_center"
python -m http.server 8080
```
Open `http://localhost:8080/command_center.html`. Confirm all three sections render correctly from the seed JSON.

**Step 4 — Product Agent review** (Product Agent, 30 minutes)
Open the command center. Check that:
- The alert for hummus mismatch is visible
- The category board accurately reflects known state
- The decision queue shows DEC-001 as DECIDED
- The executive header shows correct task count

**Step 5 — Document the update protocol** (Product Agent, 30 minutes)
Add a single paragraph to `command_center.json` as a top-level `"_update_guide"` comment field (not in the schema — just a reminder string):

```json
{
  "_update_guide": "Update this file when: a task completes, a category changes pipeline stage, a decision is made, or an alert changes status. Run 'python -m http.server 8080' from this directory to view the dashboard.",
  "meta": { ... }
}
```

**Total implementation effort:** 6–9 hours across Data Agent and Frontend Agent.

---

## Maintenance Model

**Who maintains `command_center.json`:** Any agent as part of task closeout. If an agent consistently does not update it, Product Agent updates it at session start.

**How often:** Once per task boundary. Not per conversation turn.

**What happens when it gets stale:** The date in `meta.last_updated` is the signal. If it is > 7 days old and there have been active tasks, the data is suspect. Claude should note this at session start.

**Renderer maintenance:** The HTML file does not need to change unless the schema changes. It is a one-time build. Frontend Agent owns it; modify only when a new section is added to the spec.

---

## When to Add the Agent Board

The Agent Board (Section 2 of the full spec) is deferred from MVP because it requires the highest update discipline — agents must record their own status changes. This works in a team but is easy to forget in a single-operator workflow.

Add the Agent Board when ONE of these conditions is true:

1. The Product Agent has been surprised by an agent being blocked and wishes they had seen it sooner — at least twice in one month
2. The number of simultaneous active tasks reliably reaches 3 and handoff coordination becomes the bottleneck
3. A second operator joins the workflow and needs to see who is doing what

Until then, agent status is derivable from the task and category boards. Do not build it speculatively.

---

## When to Add Real-Time Data

Never in v1. Real-time would require:
- A process that monitors BSIP2 run completion
- A process that monitors git commits to the website repo
- A running server with file-watch capability

This is a meaningful infrastructure investment for a dashboard that currently serves one operator. The right time to invest in real-time is when:
- Manual updates are consistently failing (>30% of task completions have no corresponding JSON update)
- The lag between actual state and dashboard state has caused a real operational mistake at least once

Until then, the 5-minute cost of updating `command_center.json` at task closeout is the right trade-off.

---

## Summary

| Dimension | Decision |
|---|---|
| Technology | HTML + vanilla JS + JSON |
| Dependencies | Zero |
| Server | `python -m http.server 8080` (one command) |
| Build step | None |
| Sections in MVP | Alerts + Decision Queue + Category Factory Board |
| Sections deferred | Agent Board, Website Readiness Board (full), Template tracker |
| Implementation effort | 6–9 hours |
| Maintenance effort | ~5 minutes per task completion |
| Owner | Data Agent (JSON), Frontend Agent (HTML) |
| Location | `C:\Bari\05_command_center\` |
