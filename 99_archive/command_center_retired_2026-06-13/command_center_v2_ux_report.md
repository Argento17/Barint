# Command Center v2.1 — UX & Operational-Usefulness Report

**Task:** TASK-074
**Owner:** Frontend Agent
**Date:** 2026-05-31
**Status:** COMPLETE — generator + renderer updated, before/after captured, all checks pass

---

## Summary

The dashboard was good at showing history and poor at showing what needs action.
This release fixes the "0 ACTIVE" defect, makes completed tasks readable, and adds
a **Next Action** hero card that answers "what should I do next?" — plus task
summary counters. The Hummus launch state is now represented honestly: integrated
in the website but **not launched** (PRE-LAUNCH), with one open task gating go-live.

Screenshots: `screenshots/before.png`, `screenshots/after.png`,
`screenshots/after_completed_expanded.png`.

---

## PART A — Active task logic audit (root cause + fix)

### Investigation

| Layer | Finding |
|---|---|
| Task registry parsing | Correct. `load_tasks()` parses YAML frontmatter, skips files without it. |
| Generator active logic | Correct. `active = status in (READY, IN_PROGRESS, BLOCKED)`. |
| Status mapping | Correct. The five statuses map as designed. |
| Dependency-derived tasks | N/A — tasks are explicit `.md` files, not derived. Not the cause. |
| READY vs IN_PROGRESS handling | Correct. Both count as active. |

**The logic was never broken. The data was.**

### Root cause (two compounding faults)

1. **The registry contained only COMPLETE tasks.** TASK-071 seeded 7 task files
   and marked every one COMPLETE. It never recorded the open Hummus launch work
   (insight content, QA warning, go-live). With zero non-COMPLETE tasks,
   `active = 0` — a correct count of an incomplete dataset.

2. **Launch status was derived from file presence alone.** `compute_launch()`
   returned `LIVE` for Hummus because `page.tsx` + registry entries existed. This
   masked the remaining work — nothing anywhere signalled that Hummus still had
   open tasks. The category board *agreed* with the empty task board, so the
   drift was invisible.

The real Hummus state, recovered from the launch artifacts:
`TASK-067` (content spec) → `TASK-069` (blocker fixes) → `TASK-072` (pre-launch QA,
**verdict WARN**) → **open:** resolve QA warning **W-1** + Product go-live approval.

### Fix

- **Recorded the real work** as tasks: the completed Hummus history (TASK-067/069/072)
  and the one open task **TASK-073** (READY — resolve W-1, clear go-live).
- **Gated launch on open category work** (generator): a category with any
  non-COMPLETE task tagged to it is **PRE_LAUNCH**, never LIVE, regardless of file
  presence. This ties the category board to the task board.
- **Guarantee:** `task_summary.active = READY + IN_PROGRESS + BLOCKED`. If any
  category has open work, that work is a task, so ACTIVE ≥ 1.

**Verification:** `active=1` (TASK-073); 0 completed tasks appear as active.

---

## PART B — Completed task readability

**Before:** `.task-row.done { opacity: 0.45; }` — title and summary were hard to read.

**After:** removed the opacity wash entirely. Completed rows are now distinct *and*
readable:

```css
.task-row.done { background: rgba(63,185,80,0.04); border-left: 2px solid rgba(63,185,80,0.45); }
.task-row.done .t-title { color: var(--text); }      /* full-strength title */
.task-row.done .t-sum   { color: var(--text-muted); } /* readable summary */
```

Distinction now comes from a green left accent + the green `DONE` status pill, not
from fading. Verified in `after_completed_expanded.png` — all 11 completed tasks
are legible as reference history.

---

## PART C — Next Action card

New top-level hero card (rendered first, above Alerts). Computed in the generator
(`compute_next_action`) so the selection logic lives in one place.

**Selection ladder (first match wins):**

1. BLOCKED task waiting on a decision
2. READY task blocking a launch (tagged to a category that is not LIVE)
3. Highest-priority READY task
4. Highest-priority IN_PROGRESS task

Ties break by priority, then task id (deterministic).

**Current output:**

```
NEXT ACTION
TASK-073  Resolve Hummus QA warning W-1 and clear go-live   [READY] [HIGH]
Owner:    content
Reason:   Last gate before Hummus launch.
Unblocks: Hummus launch
```

Matched via rule 2 (READY task tagged to Hummus, which is PRE-LAUNCH). Shape and
intent match the brief's example.

---

## PART D — Task board summary counters

Four counters render above the task table, computed from the registry:

| Counter | Definition | Current |
|---|---|---|
| **Active** | READY + IN_PROGRESS + BLOCKED (anything not finished) | 1 |
| **Ready** | READY | 1 |
| **Blocked** | BLOCKED | 0 |
| **Completed** | COMPLETE | 11 |

"Active" is the umbrella count PART A guarantees non-zero; Ready/Blocked are its
breakdown; Completed is separate. Zero-value Active/Blocked chips dim to avoid
false emphasis.

---

## PART E — Current Bari state (verified)

| Expectation | Result | Evidence |
|---|---|---|
| Hummus = not yet launched | **PASS** | `launch = PRE_LAUNCH` |
| Hummus still has open work | **PASS** | `open_work = [TASK-073]`, active = 1 |
| Command Center = complete | **PASS** | TASK-063/070/071/074 all COMPLETE |
| Tahini = not started | **PASS** | `launch = NOT_STARTED` (tracked, no pipeline) |
| No completed task appears as active | **PASS** | completed-but-active count = 0 |

Generator remains **idempotent** (identical output across consecutive runs).

---

## Changes by File

| File | Change |
|---|---|
| `generate_dashboard.py` | `compute_launch()` gates on open category tasks → PRE_LAUNCH; added `compute_next_action()` and `compute_task_summary()`; categories carry `open_work`; output adds `next_action` + `task_summary`; version → 2.1 |
| `command_center.html` | Next Action hero card; task summary counters; readable `.done` styling; `PRE_LAUNCH` status color/label; badge → v2.1 |
| `tasks/TASK-067,069,072.md` | Created — completed Hummus launch history |
| `tasks/TASK-073.md` | Created — **open** work (READY), the next action |
| `tasks/TASK-074.md` | Created — this task (COMPLETE) |
| `02_products/tahini/category_config.json` | Created — Tahini tracked as not started |
| `decisions/decisions.json` | Added DEC-002 (Hummus go-live, PENDING) |
| `screenshots/` | before.png, after.png, after_completed_expanded.png |

---

## How to Reproduce

```powershell
cd C:\Bari\05_command_center
C:\Bari\.venv\Scripts\python.exe generate_dashboard.py
C:\Bari\.venv\Scripts\python.exe -m http.server 8080
# open http://localhost:8080/command_center.html
```

Screenshots regenerate via `screenshot_dashboard.py <url> <out.png>` and
`screenshot_expanded.py <url> <out.png>` (Playwright + Chromium, both already
installed in the venv).

---

## Note on the "no alerts / GREEN" state

With Hummus correctly PRE-LAUNCH (not a NOT_STARTED website), the old false
`WEBSITE_FACTORY_MISMATCH` alert no longer fires. The dashboard is GREEN with 0
alerts — but it is **not** empty of signal: the Next Action card and the PRE-LAUNCH
launch state make the open Hummus work and the pending go-live decision visible.
"What needs action now" is answered without needing an alert to fire.
