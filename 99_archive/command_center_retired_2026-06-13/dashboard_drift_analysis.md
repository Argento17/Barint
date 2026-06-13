# Dashboard Drift Analysis

**Task:** TASK-083
**Owner:** Data Agent
**Date:** 2026-05-31
**Companion:** `command_center_accuracy_audit.md` (item-by-item findings)

This document explains *why* the Command Center drifts, traces the specific failure that produced the stale Next Action, and generalizes it into a drift taxonomy with the controls that close each gap.

---

## 1. The data-flow model

```
                 derived, self-healing  ┌─────────────────────────┐
   pipeline artifacts ─────────────────▶│ categories / website /  │
   (bsip*, qa, routes, datasets)        │ dataset / launch state  │  ✅ accurate
                                         └─────────────────────────┘
                                                    ▲
   reality of work done ───┐                        │ compute_launch()
   (a written deliverable) │   *no automatic link*  │ gates on open tasks
                           ▼                         │
   tasks/TASK-*.md  ──────────────────────▶ tasks / next_action / counts
   (HAND-MAINTAINED)        manual edit            ❌ drifts
   decisions.json   ──────────────────────▶ decisions / blocker
   (HAND-MAINTAINED)        manual edit            ⚠️ drifts
```

The generator is deterministic and correct. Drift is entirely an **input-freshness** problem on the two hand-maintained inputs (task registry, decisions), amplified by the fact that **launch gating reads from the task registry**, so a single stale task poisons the category view as well.

---

## 2. Anatomy of the headline drift: TASK-073 as Next Action

Step-by-step, the exact mechanism:

1. **TASK-072** (QA) returned verdict **WARN** with warning **W-1** (stale post-NOVA-1 counts in the content spec). It created/left **TASK-073** open as "resolve W-1 + go-live."
2. The team then did the work — but recorded it under **new task IDs that never entered the registry**:
   - **TASK-075** → `hummus_content_count_reconciliation.md`: corrected 8 stale fields, explicitly states *"W-1 is resolved in hummus_content_v3.json."*
   - **TASK-076** → nutrition boundary-review verdict: **APPROVE**.
   - **TASK-080** → dataset reconciliation (archived `*.PRE-TASK080.json`).
   - The TASK-073 ID was *also* reused for a Product-Agent boundary review (`hummus_boundary_review.md`), which differs from the registry's description of TASK-073.
3. **No one edited `tasks/TASK-073.md`** to `status: COMPLETE`, and **no `TASK-075.md` was ever created.**
4. `generate_dashboard.py` ran at 10:03. It saw exactly one open task tagged to a not-LIVE flow — TASK-073, READY, HIGH — and the Next-Action ladder rung #2 ("READY task blocking a launch") selected it.
5. Because `compute_launch()` gates on `open_work`, TASK-073 also forced hummus to **PRE_LAUNCH** with `blocking_issues: [TASK-073]`.

**One un-closed task produced three visible errors** (stale next action, wrong active count, stale launch state) plus an invisible one (six completed tasks missing from the count). This is the leverage that makes registry drift dangerous: the task layer is upstream of the launch layer.

---

## 3. Two compounding failures

| | Failure | Evidence |
|---|---|---|
| **A. Stale inputs** | Work is closed by *writing a deliverable*, not by *updating the registry*. The two acts are decoupled and only the first happens reliably. | 30+ task IDs appear in deliverables (TASK-034 ×157, TASK-039 ×119, TASK-064, -061, -062, -075, -076, -080…); only **14** exist as registry files. |
| **B. Stale snapshot** | The generator is run by hand and was not re-run after the latest work. | `command_center.json` mtime **10:03**; newest hummus deliverable **13:03**; newest registry file **09:58**. The dashboard is a 3-hour-old photo of an already-incomplete registry. |

A is the structural defect; B guarantees that even the correctly-derived sections lag. Either alone degrades trust; together they make the "generated, do-not-edit" label actively misleading — it signals freshness the file does not have.

---

## 4. Why the v2 "source-of-truth" design only half-worked

The v2 redesign (TASK-070/071) correctly moved category/website/dataset state from hand-maintained JSON to *derived-from-artifacts*. That layer is accurate today precisely because **its source of truth is the work product itself** — a route file existing *is* the proof the route exists.

The task layer kept a **proxy** source of truth: a `TASK-*.md` file that is supposed to mirror reality but is updated by a separate human act. A proxy that requires discipline to stay true is not a source of truth — it is a second copy that drifts. The design applied the right principle (derive from artifacts) to pipeline state and the wrong principle (trust a manual mirror) to task state.

---

## 5. Drift taxonomy & controls

| Drift class | Definition | Seen here? | Control that closes it |
|---|---|---|---|
| **Closure drift** | Work finished in reality; registry status not advanced. | ✅ TASK-073 still READY | Derive task-done from deliverable, OR a non-skippable close-the-task gate. |
| **Phantom-task drift** | Work exists with an ID that has no registry record. | ✅ TASK-075/076/080/061/062/064 | Generator scans deliverables for `Task:`/`source_task:` IDs and alerts on any with no registry file. |
| **Identity drift** | One ID describes two different pieces of work. | ✅ TASK-073 (W-1 task vs boundary review) | One ID = one task invariant; lint on duplicate-ID divergent titles. |
| **Snapshot drift** | Sources changed after last generation. | ✅ 10:03 vs 13:03 | Auto-regenerate on change; renderer warns when any source mtime > `meta.last_updated`. |
| **Definition drift** | Same concept computed two ways. | ✅ `active_task_ids` vs `task_summary.active` | Single shared helper for "active." |
| **Granularity drift** | Displayed number doesn't match what the user sees on the live page. | ✅ product_count 69 vs displayed 63 | Surface corpus + displayed + scored counts distinctly. |
| **Rationale drift** | Status field correct, but its explanatory text is stale. | ✅ DEC-002 "hold until W-1" (already met) | Recompute/timestamp decision recommendations; flag PENDING decisions whose stated condition is satisfied. |

---

## 6. Priority of remediation

1. **Stop the bleeding (workflow):** make registry-update part of "done." No deliverable merges without its `TASK-*.md` set COMPLETE (F3). This prevents new closure/phantom drift.
2. **Make drift visible (generator):** add the phantom-task + stale-snapshot alerts (F8, F4). The dashboard should have *told us* about TASK-083's findings.
3. **Backfill (source data):** create the six missing task files and close TASK-073 (F1), resolve the ID collision (F2), refresh DEC-002 (F7).
4. **Polish (generator):** unify "active" (F5), split corpus/displayed counts (F6).

Long-term, the durable fix is to **derive task state from the artifacts that prove the work** — the same principle that already makes the pipeline layer trustworthy — rather than from a parallel manual registry. Until then, controls 1–2 are mandatory for the Command Center to be relied on for "what do I do next."

---
*Data Agent — TASK-083 — 2026-05-31*
