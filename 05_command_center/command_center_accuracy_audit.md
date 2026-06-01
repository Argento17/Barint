# Command Center Accuracy Audit

**Task:** TASK-083
**Owner:** Data Agent
**Date:** 2026-05-31
**Audited artifact:** `05_command_center/command_center.json` (generated 10:03) + `command_center.html` renderer
**Generator:** `05_command_center/generate_dashboard.py` (v2.1)

---

## 1. How the dashboard derives each item

`generate_dashboard.py` is the only writer of `command_center.json` (the file is flagged `_do_not_edit`). It reads four authoritative source classes and computes everything from them:

| Source | Path | Feeds |
|--------|------|-------|
| **Task registry** | `C:\Bari\tasks\TASK-*.md` (YAML frontmatter) | tasks, task_summary, next_action, executive, launch gating, alerts |
| **Decision registry** | `C:\Bari\decisions\decisions.json` | decisions, pending-decision alerts, next_recommended_decision |
| **Category config + pipeline files** | `C:\Bari\02_products\{cat}\category_config.json` + `reports/`, `canonical_bsip1/`, `intelligence_bsip2/`, `qa/` | category factory/bsip/qa state |
| **Website / dataset** | `C:\bari-web\src\...` | website status, frontend_dataset status |

Derivation logic per dashboard item:

- **Active tasks** — `task_summary.active = READY + IN_PROGRESS + BLOCKED` over the registry (`load_tasks` → `compute_task_summary`). Note: `executive.active_task_ids` uses a *different* definition (`IN_PROGRESS + BLOCKED` only).
- **Completed tasks** — `task_summary.completed = count(status == COMPLETE)`; `executive.latest_completed_task = max(completed_at)`.
- **Next action** — `compute_next_action()` priority ladder: (1) BLOCKED task → (2) READY task tagged to a not-LIVE category → (3) highest-priority READY → (4) highest-priority IN_PROGRESS. **Operates entirely on the registry.**
- **Pending decisions** — read verbatim from `decisions.json`; `status == PENDING` drives the decision queue and `STALE_DECISION` alerts.
- **Category status** — derived from the filesystem (`derive_bsip0/1/2`, `derive_qa`, `derive_dataset`, `derive_website`) and `compute_launch()`. Launch is gated on **open registry tasks tagged to the category** (`open_work`).

**Architectural consequence:** category/website/dataset state is derived from real pipeline artifacts and is self-healing. **Task state, next action, and launch gating are only as accurate as the hand-maintained `tasks/TASK-*.md` registry.** That registry is the single point of failure for this dashboard, and it is where all observed drift originates.

---

## 2. Item-by-item audit (displayed vs authoritative vs expected)

### Executive / Next Action / Task counts

| Dashboard item | Displayed value | Authoritative source | Expected value | Status |
|---|---|---|---|---|
| `next_action` | **TASK-073** "Resolve Hummus QA warning W-1" (READY) | W-1 resolved by **TASK-075** → `hummus_content_count_reconciliation.md` ("W-1 is resolved in hummus_content_v3.json") | No open W-1 work; next action should be DEC-002 go-live approval (or none) | ❌ **STALE** |
| `task_summary.active` | **1** | Registry; TASK-073's actual deliverable (`hummus_boundary_review.md`) is delivered + co-signed (TASK-076) | **0** open tasks (all hummus launch work done) | ❌ **INCORRECT** |
| `task_summary.completed` | **11** | ≥ 30+ task IDs referenced in deliverables (TASK-034, -039, -061, -062, -064, -075, -076, -080 …) | Far higher; registry holds only 14 of the project's tasks | ❌ **UNDERCOUNT** |
| `executive.active_task_ids` | **[]** (empty) | Same registry, different definition (`IN_PROGRESS+BLOCKED`) | Internally inconsistent with `task_summary.active = 1` | ⚠️ **SELF-CONTRADICTORY** |
| `executive.latest_completed_task` | TASK-058 (2026-05-31) | Newest actual completion is TASK-075/076/080 (~13:00) | TASK-080 / TASK-076 | ❌ **STALE** |
| `executive.system_health` | GREEN | No critical alerts in stale snapshot | GREEN is accidentally right (no alerts because no open work is *visible*) | ⚠️ **RIGHT FOR WRONG REASON** |
| `current_blocker` | null | DEC-002 go-live still PENDING | DEC-002 (pending decision) | ⚠️ stale |

### Decisions

| Dashboard item | Displayed | Authoritative source | Expected | Status |
|---|---|---|---|---|
| DEC-001 | DECIDED (Option B) | `decisions.json` | DECIDED | ✅ correct |
| DEC-002 "Hummus go-live" | **PENDING**, recommendation "Hold until TASK-073 resolves W-1" | W-1 is resolved (TASK-075); boundary approved (TASK-076) | Still legitimately PENDING (go-live not yet signed), but the **recommendation text is stale** — the hold condition is already met | ⚠️ **STALE RATIONALE** |

### Categories (pipeline / website / dataset)

| Category | Item | Displayed | Authoritative | Status |
|---|---|---|---|---|
| Bread, Dairy Desserts, Milk, Snack Bars, Yogurts | launch | LIVE | filesystem (routes + registry present) | ✅ correct |
| **Hummus** | `launch.status` | **PRE_LAUNCH**, blocking = [TASK-073] | W-1 resolved, boundary approved, dataset reconciled (TASK-080), content v3 done | ❌ **STALE** — gated on a task that is functionally complete |
| Hummus | `open_work` | [TASK-073] | should be [] | ❌ stale (drives the PRE_LAUNCH above) |
| Hummus | `product_count` | **69** | 69 total corpus / **63 displayed / 61 scored** (reconciliation + QA report) | ⚠️ **AMBIGUOUS** — shows raw BSIP1 corpus, not the displayed count users see |
| Hummus | bsip0/1/2, qa, website, dataset | PASS / COMPLETE / AUTHORITATIVE / PASS / LIVE / DEPLOYED | matches pipeline artifacts | ✅ correct |
| Breakfast Cereals, Tahini | launch | QUEUED / NOT_STARTED | no pipeline artifacts | ✅ correct |

### Alerts

| Item | Displayed | Expected | Status |
|---|---|---|---|
| `alerts` | **[]** (empty) | A `STALE_DECISION`-class signal would be appropriate once DEC-002's hold condition is met but unresolved; and the registry/reality gap itself is unalerted | ⚠️ no false alerts, but **no coverage** of the drift class that actually bit this dashboard |

---

## 3. Stale or incorrect values (summary)

1. **Next Action = TASK-073** — stale; W-1 already resolved by TASK-075.
2. **TASK-073 status = READY** — should be COMPLETE (its deliverable `hummus_boundary_review.md` is delivered and co-signed by TASK-076).
3. **TASK-073 registry description ≠ its real deliverable** — registry frontmatter calls it a content/W-1 task owned by `content-agent`; the actual TASK-073 artifact is a Product-Agent boundary review. The ID means two different things.
4. **Hummus launch = PRE_LAUNCH** — stale; only the unrecorded DEC-002 sign-off remains.
5. **task_summary.active = 1** — incorrect; no genuinely open registry work.
6. **task_summary.completed = 11 / latest = TASK-058** — undercount; TASK-061, -062, -064, -075, -076, -080 completed but are absent from the registry.
7. **DEC-002 recommendation text** — stale ("hold until W-1 resolved" — already met).
8. **`executive.active_task_ids` (=[]) vs `task_summary.active` (=1)** — two contradictory "active" definitions in one file.
9. **Hummus product_count = 69** — shows corpus, not the 63 displayed / 61 scored figure users actually see.
10. **Generator not re-run** — JSON generated 10:03; deliverables continued until 13:03. Even correctly-derived sections are a snapshot 3 hours stale.

---

## 4. Why each value was not updated

| Root cause | Items affected | Mechanism |
|---|---|---|
| **Task registry is hand-maintained and was never updated when work completed.** TASK-075/076/080/061/062/064 produced deliverables but no `TASK-*.md` file was ever created; TASK-073 was never flipped to COMPLETE. | 1, 2, 3, 4, 5, 6 | The generator can only see tasks that exist as files in `tasks/`. Closing work in reality (writing a deliverable) does not touch the registry, so the dashboard never learns the task finished. |
| **No regeneration trigger.** `generate_dashboard.py` runs only when a human runs it. | 7, 10 | The 10:03 snapshot predates the 13:00 work. Nothing re-runs it on source change. |
| **Two definitions of "active" in the generator.** | 8 | `compute_executive` uses `IN_PROGRESS+BLOCKED`; `compute_task_summary` uses `READY+IN_PROGRESS+BLOCKED`. |
| **`product_count` bound to BSIP1 record_count, not displayed corpus.** | 9 | `derive_categories` sets `product_count = bsip1.record_count`; the displayed/scored split lives only in the dataset + reconciliation doc, which the generator does not read. |
| **DEC-002 left PENDING with original rationale.** | 7 | Decisions are append-only and hand-edited; no step updated the recommendation when its hold condition was satisfied. |

The unifying cause: **the dashboard's task layer depends on a manual registry that no workflow keeps in sync, and the generator is not re-run on change.** The pipeline/website layer, which *is* derived from artifacts, stayed accurate.

---

## 5. Recommended fixes (classified)

| # | Fix | Classification |
|---|---|---|
| F1 | Create the missing registry files (TASK-061, -062, -064, -075, -076, -080) and set TASK-073 → COMPLETE with `completed_at`. Immediately corrects Next Action, active/completed counts, latest-completed, and hummus launch gating. | **source data issue** |
| F2 | Reconcile TASK-073's identity: the registry entry and the `hummus_boundary_review.md` deliverable describe different work under one ID. Split or relabel so one ID = one task. | **source data issue** |
| F3 | Add a **workflow gate**: a task is not "done" until its `TASK-*.md` frontmatter is set to COMPLETE. Enforce via the agent operating procedure (ownership_matrix / agent_os) and ideally a pre-commit/CI check that every `source_task`/`Task:` referenced in a new deliverable has a matching registry file. | **workflow issue** |
| F4 | Auto-regenerate: run `generate_dashboard.py` on a hook (post-task, file-watch, or scheduled) so the JSON is never hours behind its sources. At minimum, the renderer should display the JSON `meta.last_updated` and warn when source files are newer. | **workflow issue** + **generator issue** |
| F5 | Unify the "active" definition — `compute_executive` and `compute_task_summary` must use the same set. | **generator issue** |
| F6 | Surface both numbers for categories: `corpus_count` (BSIP1) and `displayed_count` / `scored_count` (from the dataset), so 63/61 are visible, not just 69. | **generator issue** |
| F7 | Refresh DEC-002: either record the go-live decision or update its recommendation text now that the W-1 hold condition is met. | **manual maintenance issue** |
| F8 | Add a **drift alert**: generator flags any task ID referenced in a deliverable (`Task:`/`source_task:`) that has no registry file, and any source file newer than the last generation. This is the alert class that would have caught TASK-083's findings automatically. | **generator issue** |

---

## 6. Can the Command Center operate as a true source-of-truth dashboard?

**Partly — and not yet for the part that matters most.**

- ✅ **Pipeline / website / dataset / category state is genuinely source-of-truth.** It is derived directly from filesystem artifacts (`bsip*`, `qa`, routes, datasets) and was accurate in every category checked. This half of the v2 architecture works as designed.

- ❌ **The task / next-action / launch-gating layer is *not* source-of-truth.** It derives from a hand-maintained registry that no workflow keeps in sync. Reality (a written deliverable) and the registry (a `TASK-*.md` file) are updated by two independent acts, and only the first reliably happens. Every drift finding in this audit traces to that gap. The "do-not-edit, generated" framing creates false confidence: the JSON is faithfully generated *from stale input*, so it looks authoritative while being wrong.

**Verdict:** The Command Center cannot be trusted as a source-of-truth for "what should I do next" until task state is either (a) **derived from the same artifacts that prove the work** (e.g., a deliverable with a `Task:` header flips the task to done), or (b) **protected by a workflow gate** that makes registry-update a non-skippable part of closing a task — combined with **automatic regeneration** so the view is never a stale snapshot. With F1–F8 applied, the architecture is sound enough to reach true source-of-truth status; without them, it is a source-of-truth for pipeline state and a lagging manual report for task state.

See `dashboard_drift_analysis.md` for the failure-mechanism deep-dive and the generic drift taxonomy.

---
*Data Agent — TASK-083 — 2026-05-31*
