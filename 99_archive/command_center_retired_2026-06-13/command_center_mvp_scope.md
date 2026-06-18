# Bari Command Center — MVP Scope

**Task:** TASK-059  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**Principle:** The smallest command center that is actually used beats the most complete one that is occasionally consulted.

---

## The Core Question

What does the Product Agent need to know at the start of every session to make a good first decision?

The answer is three things — in this order:
1. Is anything on fire? (Alerts)
2. What decisions are waiting for me? (Decision Queue)
3. Where are the active categories in the pipeline? (Category Board)

Everything else — Agent Board detail, Website SEO readiness, full route audits — is useful occasionally, not daily. It belongs in v2.

---

## MVP Scope

### IN — Core three sections (the "decision brief")

**Section 1: Alerts**
All open alerts, sorted by severity. If there are no open alerts, this section shows "No alerts." This section alone justifies the command center's existence — a single view of everything that is broken or blocked.

**Section 2: Decision Queue**
All pending decisions with urgency = `NOW` or `THIS_WEEK`. One row per decision: who needs to decide, what is blocking, what the recommendation is. Product Agent reads this list and can act immediately.

**Section 3: Category Factory Board**
One row per category. Columns: category name, product count, BSIP0/BSIP1/BSIP2 status, QA verdict, frontend dataset status, website status, launch status. No sub-rows, no drill-down in MVP — the row is the entry.

### IN — Lightweight executive header

Three numbers across the top, always visible:
- Active tasks: `2 / 3`
- Open alerts: `1 HIGH`
- Pending decisions (NOW): `1`

That is the full executive status in MVP. No "next recommended decision" field (too easy to get stale and misleading). The decision queue below it serves this purpose.

---

### OUT of MVP — Deferred to v2

**Agent Board (full detail):** The per-agent status table (active task, last output, blocker, next handoff) is genuinely useful, but it requires the highest update discipline — agents must update it after every output. In MVP, agent status is implied by the task and category boards. If the hummus frontend JSON is `NOT_BUILT`, we know Data Agent has work to do. We don't need a separate agent status row to tell us that.

**Website Readiness Board (full):** SEO field completeness, hreflang audits, structured data tracking — useful, but requires an external audit to populate accurately. The category board's `website.status` column provides the essential signal (LIVE / MISSING / BROKEN). Full route-level SEO tracking belongs in a dedicated SEO audit workflow, not the command center.

**Template generation tracker:** Too narrow to justify a section in MVP. Track in category known_issues if relevant.

**Historical alert archive:** Resolved alerts in MVP are hidden (not deleted, but not rendered). The view shows only open alerts.

**System health color indicator:** Useful but easy to implement incorrectly. The three numbers in the executive header convey the same information without a single signal that can be misleading.

---

## MVP Data Scope

### Categories to populate at launch

All 6 active categories + hummus pipeline:

| Category | MVP data status |
|---|---|
| חומוס (Hummus) | Full — pipeline documented in TASK-058 |
| מעדנים (Dairy desserts) | Approximate — website live, details to verify |
| לחם (Bread) | Approximate — website live |
| חטיפים (Snack bars) | Approximate — website live |
| יוגורטים (Yogurts) | Approximate — website live |
| חלב (Milk) | Approximate — website live (legacy) |
| דגני בוקר (Breakfast cereals) | Skeleton — queued, no pipeline started |

"Approximate" means the category row is populated with best-known values — launch status is clearly LIVE; detailed BSIP stage dates are populated where known and left null where unknown.

### Agents to populate at launch

All 9 agents. Status for most will be `AVAILABLE` or `WAITING` at first population. Populate `last_output` only where a specific recent output is known. Set `active_task_id: null` for agents not currently assigned.

### Decisions at launch

Populate with DEC-001 (HUM-001 fat data decision, already resolved). Any other known pending decisions. Decision queue will likely be short at first — that is correct; an empty queue is a healthy state.

### Alerts at launch

Populate ALT-001 (WEBSITE_FACTORY_MISMATCH for hummus). Any additional known open alerts. Most live categories likely have no open alerts — leave the section empty for them.

---

## MVP Maintenance Protocol

The command center is only useful if it is accurate. In MVP, the update burden is deliberately low:

**Mandatory updates (every time):**
- When a task completes: update `executive.active_task_ids`, mark the task done in agent status
- When a category moves a pipeline stage: update the category row
- When a decision is made: mark `status: DECIDED` in decisions array
- When an alert is resolved: mark `status: RESOLVED`

**Optional updates (encouraged but not required for MVP):**
- Agent `last_output` field
- Agent `next_handoff` field
- Category `known_issues` list

**Never required in MVP:**
- Route-level SEO fields (deferred to v2)
- `system_health` computed field (derive from alert count instead)

**Update owner:** Any agent completing a task updates the command center JSON. If an agent does not update it, Product Agent updates it at the start of the next session.

**Target update frequency:** Once per task boundary. Not per conversation turn. Not in real time.

---

## MVP Non-Functional Requirements

- **No server required.** MVP must work without running a local server.
- **No build step.** Open the dashboard, it works.
- **No database.** One JSON file.
- **No authentication.** Internal tool, filesystem access is security enough.
- **No animations.** Static render, refresh manually.
- **No dependencies.** The HTML renderer has zero npm dependencies, zero CDN calls. Everything is inline.
- **Readable without the renderer.** The `command_center.json` file must be human-readable on its own. A Product Agent who opens the JSON file directly should be able to extract the current state without the HTML renderer.

---

## MVP Success Criteria

The command center MVP is useful if, after 2 weeks of use, the Product Agent answers YES to at least 3 of these 4:

1. "I open the command center at the start of most sessions."
2. "It has told me something I would have otherwise missed."
3. "The data is accurate enough to trust without double-checking."
4. "I am not spending more time maintaining it than it saves me."

If the answer is NO to 3+ after 2 weeks, stop using it and diagnose why. Do not add features to a dashboard that isn't being used.

---

## Upgrade Path (v2)

Once MVP is validated:

| v2 addition | Trigger condition |
|---|---|
| Full Agent Board | When agent handoff tracking becomes a frequent pain point |
| Website SEO detail | When SEO is an active work stream (Q3 2026 per growth strategy) |
| Route-level audit table | When 8+ categories are live |
| Alert auto-generation | When manual alert creation becomes unreliable |
| Historical trend view | When retrospectives require it |
| Slack/email notification on RED alerts | When team size > 1 person |

Do not add any of these to v1. The rule is: add a feature to the command center when the absence of that feature has caused a real problem at least once.
