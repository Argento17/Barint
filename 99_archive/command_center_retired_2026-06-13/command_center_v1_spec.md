# Bari Command Center v1 — Specification

**Task:** TASK-059  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**Status:** SPEC ONLY — do not build until MVP scope confirmed  
**Companion documents:** command_center_data_model.md, command_center_mvp_scope.md, implementation_recommendation.md

---

## Purpose

The Bari Command Center is a single-view operational dashboard for the Product Agent. It answers one question at the start of every session: **what is the current state of Bari, and what needs a decision right now?**

It is not a project management tool. It is not a reporting tool. It is a situational awareness surface — the equivalent of the display a pilot checks before takeoff. It tells you what is running, what is stuck, and what needs your attention in the next 30 minutes.

---

## Design Principles

1. **Read in 60 seconds.** Every section should be scannable without drilling into linked documents.
2. **Decisions first.** The thing most likely to unblock work appears before the thing that is merely interesting.
3. **Errors before status.** Red before green. Alerts before metrics.
4. **No inferred data.** The dashboard shows only what has been explicitly recorded. It does not guess or synthesize — Claude does the synthesis; the dashboard holds the state.
5. **One source of truth.** All data lives in `command_center.json`. The dashboard is a renderer, not a database.
6. **No animations, no gimmicks.** Static render. Refresh manually when you open it.

---

## Section 1 — Executive Status

**Purpose:** 10-second read of where Bari stands right now.

**Display items:**

| Field | Description | Example |
|---|---|---|
| Active task count | Number of tasks currently in-flight out of max 3 | `2 / 3` |
| Active tasks | Task IDs and one-line summaries | `TASK-059 (Command Center spec), TASK-060 (HUM-001 decision)` |
| Task capacity bar | Visual fill indicator (3 slots) | `[██░] 2/3` |
| Latest completed task | Task ID, title, completion date | `TASK-058 — Hummus Status Audit (2026-05-31)` |
| Current blocker | The single highest-priority thing blocking progress | `HUM-001 fat data decision required before hummus frontend build begins` |
| Next recommended decision | One-line prompt for what Product Agent should do next | `Confirm Option B fat suppression → unblocks TASK-058 Phase 1 (Data Agent)` |
| System health | Green / Yellow / Red | `YELLOW — 1 active blocker` |

**Update trigger:** Updated whenever a task is created, completed, or its status changes.

---

## Section 2 — Agent Board

**Purpose:** See all 9 agents at once. Identify who is idle, who is blocked, and where handoffs are queued.

**Display:** One row per agent.

| Column | Description | Possible values |
|---|---|---|
| Agent | Agent name | Product Agent, Nutrition Agent, etc. |
| Status | Current operational state | `Available`, `Working`, `Blocked`, `Waiting for handoff`, `Idle` |
| Active task | Task ID currently assigned | `TASK-059` or `—` |
| Last output | Most recent deliverable (title + date) | `hummus_status_audit.md (2026-05-31)` |
| Blocker | What is preventing progress | Free text or `—` |
| Next handoff | Who receives the next output from this agent | `Data Agent → Frontend Agent` or `—` |

**Status color coding (text labels, no color dependency):**

| Status | Meaning |
|---|---|
| `WORKING` | Has an active assigned task, in progress |
| `BLOCKED` | Has a task but cannot proceed — blocker recorded |
| `WAITING` | Output delivered, waiting for another agent to receive/act |
| `AVAILABLE` | No active task |
| `IDLE` | No task assigned for > 7 days |

**Alert trigger:** Any agent with status `BLOCKED` or `IDLE` for > 7 days surfaces in Section 6 Alerts.

**Agent roster (all 9 must appear):**

1. Product Agent
2. Nutrition Agent
3. Research Agent
4. Data Agent
5. Frontend Agent
6. Design Agent
7. QA Agent
8. Content Agent
9. Marketing Agent

---

## Section 3 — Category Factory Board

**Purpose:** One-row-per-category view of pipeline progress and website status.

**Display:** One row per category (live + in-flight + queued).

| Column | Description | Values |
|---|---|---|
| Category | Hebrew + English name | `חומוס / Hummus` |
| Products | Count in corpus | `69` |
| BSIP0 | Scrape gate status | `PASS` / `FAIL` / `IN PROGRESS` / `—` |
| BSIP1 | Enrichment status | `COMPLETE` / `IN PROGRESS` / `BLOCKED` / `—` |
| BSIP2 | Scoring run status | `AUTHORITATIVE` / `INVALID` / `IN PROGRESS` / `—` |
| QA | QA verdict | `PASS` / `FAIL` / `WARN` / `PENDING` / `—` |
| Frontend JSON | Dataset status | `BUILT` / `NOT BUILT` / `STALE` |
| Website | Page status | `LIVE` / `IN PROGRESS` / `NOT STARTED` / `LEGACY` / `BROKEN` |
| Launch | Overall launch status | `LIVE` / `PRE-LAUNCH` / `PIPELINE ONLY` / `QUEUED` / `BLOCKED` |
| Known issues | Count of open issues | `2` (links to issue list) |

**Category roster (all active categories):**

| Category | Hebrew | Expected status |
|---|---|---|
| Hummus | חומוס | Pipeline complete, website not started |
| Dairy desserts | מעדנים | Live |
| Bread | לחם | Live |
| Snack bars | חטיפים | Live |
| Yogurts | יוגורטים | Live |
| Milk | חלב | Live (legacy) |
| Breakfast cereals | דגני בוקר | Queued |
| (Future) | — | — |

**Alert trigger:** Any category where BSIP2 = `AUTHORITATIVE` but Website = `NOT STARTED` for > 30 days surfaces as a "website/factory mismatch" alert.

**BSIP2 invalid warning:** If any category has an `INVALID` BSIP2 run as its only run, surface as a critical alert.

---

## Section 4 — Website Readiness Board

**Purpose:** Status of every URL that Bari serves or should serve.

**Display:** One row per route.

| Column | Description | Values |
|---|---|---|
| Route | URL path | `/hashvaot/hummus` |
| Category | Category this route serves | Hummus |
| Component generation | Gen 0 (legacy) or Gen 1 (canonical) | `Gen 0` / `Gen 1` |
| Page status | Render status | `LIVE` / `MISSING` / `BROKEN` / `LEGACY` |
| Meta title (Hebrew) | Present and correct? | `YES` / `NO` / `PARTIAL` |
| hreflang | `lang="he"` set? | `YES` / `NO` |
| Structured data | ItemList schema present? | `YES` / `NO` / `PENDING` |
| Mobile QA | Last mobile layout QA date | `2026-05-20` or `NEVER` |
| Last QA | Date of last QA Agent audit | `2026-05-20` or `NEVER` |

**SEO readiness summary (footer of section):**
- Pages with complete SEO: N / Total
- Pages missing hreflang: N
- Pages never QA'd: N
- Pages with no structured data: N

**Alert trigger:** Any route with Page status = `MISSING` where the category has BSIP2 = `AUTHORITATIVE` surfaces in Alerts. Any Gen 0 page that has not had a QA audit in > 60 days surfaces as stale.

**Template generation status (sub-section):**

| Template | Status | Last updated |
|---|---|---|
| Gen 1 reference implementation | `PENDING (hummus)` | — |
| Gen 1 desktop layout | `ACTIVE` | 2026-05-30 |
| Gen 0 → Gen 1 migration plan | `NOT STARTED` | — |

---

## Section 5 — Decision Queue

**Purpose:** All pending decisions that require a named agent's input before work can proceed.

**Display:** One row per pending decision.

| Column | Description |
|---|---|
| Decision ID | `DEC-NNN` |
| Title | One-line description |
| Required from | Which agent owns the decision |
| Blocking | What cannot proceed until this decision is made |
| Options | Number of options under consideration |
| Recommendation | Who recommends, and what (if any) |
| Created | Date decision was queued |
| Urgency | `NOW` / `THIS WEEK` / `BACKLOG` |

**Sub-sections:**

**Product Agent decisions (must decide):**
Decisions requiring Product Agent action, sorted by urgency.

**Nutrition Agent decisions (must decide):**
Decisions requiring Nutrition Agent sign-off (typically accuracy approvals).

**Go / No-Go gates:**
Binary decisions that gate a launch or phase transition. These always show first within the decision queue.

| Gate | Category | What is gated | Status |
|---|---|---|---|
| HUM-001 fat data strategy | Hummus | Frontend JSON build | `PENDING → Product Agent` |
| Hummus go-live | Hummus | Merge to main | `NOT YET OPEN` |

**Exceptions pending:**
Decisions where an agent has requested an exception to a hard rule or standard process.

**Alert trigger:** Any decision with urgency = `NOW` that is > 2 days old surfaces in Section 6 Alerts.

---

## Section 6 — Alerts

**Purpose:** The first thing to read. If there are no alerts, everything is operating normally.

**Display:** Sorted by severity (CRITICAL → HIGH → MEDIUM → LOW). Resolved alerts are hidden by default.

| Column | Description |
|---|---|
| Alert ID | `ALT-NNN` |
| Severity | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` |
| Type | See alert types below |
| Message | One-line description |
| Related | Task ID, category, or agent |
| Age | How long this alert has been open |
| Status | `OPEN` / `RESOLVED` |

**Alert types and trigger conditions:**

| Type | Trigger condition | Default severity |
|---|---|---|
| `BLOCKED_TASK` | Any task with status = `BLOCKED` | HIGH |
| `STALE_CATEGORY` | Category with BSIP2 `AUTHORITATIVE` > 9 months without website refresh | MEDIUM |
| `QA_FAILURE` | Any QA verdict = `FAIL` | HIGH |
| `MISSING_OWNER` | Any task with no assigned agent | HIGH |
| `CAPACITY_EXCEEDED` | Active task count > 3 | CRITICAL |
| `WEBSITE_FACTORY_MISMATCH` | Category: BSIP2 `AUTHORITATIVE` and Website = `NOT STARTED` for > 30 days | HIGH |
| `INVALID_BSIP2` | Any category where only available BSIP2 run is `INVALID` | CRITICAL |
| `STALE_DECISION` | Decision queue item with urgency `NOW` open for > 2 days | HIGH |
| `IDLE_AGENT` | Any agent with no active task for > 7 days | LOW |
| `LEGACY_PAGE_UNAUDITED` | Gen 0 page with no QA audit in > 60 days | LOW |
| `MISSING_CONTENT` | Category where frontend JSON has empty insight lines > 30 days post-build | MEDIUM |

**Alert count summary (top of section):**
`3 alerts — 0 CRITICAL / 1 HIGH / 2 MEDIUM / 0 LOW`

---

## Section Layout (Recommended Order)

When rendered, sections appear in this order:

```
[ALERTS]             ← read first; skip section if 0 alerts
[EXECUTIVE STATUS]   ← always visible
[DECISION QUEUE]     ← read before checking boards
[CATEGORY FACTORY]   ← primary operational board
[WEBSITE READINESS]  ← secondary; check when launching
[AGENT BOARD]        ← check when a handoff is expected
```

The Agent Board is last because it is the most granular. Most sessions start with alerts and decisions, not agent status.

---

## Update Protocol

The command center is only as useful as its accuracy. The following update triggers are mandatory:

| Event | What to update |
|---|---|
| Task created | Section 1 (active tasks), Section 2 (agent status), Section 6 (if capacity exceeded) |
| Task completed | Section 1 (completed tasks), Section 2 (agent status → available), Section 5 (resolved decisions) |
| Task blocked | Section 2 (agent status → blocked), Section 6 (add BLOCKED_TASK alert) |
| BSIP stage completes | Section 3 (category row) |
| QA verdict issued | Section 3 (QA column), Section 4 (last QA date), Section 6 (if FAIL) |
| Decision made | Section 5 (mark decided), Section 6 (resolve STALE_DECISION alert) |
| Page goes live | Section 3 (website column), Section 4 (route row) |
| New category queued | Section 3 (new row) |

**Who updates:** The agent completing a task updates the command center JSON as part of task closeout. Product Agent is the fallback updater if an agent does not update.

---

## What This Is Not

- It is not a ticketing system. Tasks are not created here.
- It is not a communication tool. Handoffs happen in task files.
- It is not a scoring engine. It reads BSIP2 outputs; it does not compute them.
- It is not a content management system. Category copy is not authored here.
- It is not a real-time system. It reflects state at last update, not live pipeline state.
