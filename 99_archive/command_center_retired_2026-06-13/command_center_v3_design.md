# Command Center v3 — Self-Healing Task State (Design)

**Task:** TASK-084
**Owner:** Data Agent
**Date:** 2026-05-31
**Builds on:** `command_center_accuracy_audit.md`, `dashboard_drift_analysis.md` (TASK-083)
**Status:** IMPLEMENTED (generator + watchdog shipped; see PART B below and the migration doc)

---

## 1. Problem (from TASK-083)

The v2 dashboard is accurate for **category / pipeline / dataset / website** state because that state is *derived from artifacts*: a route file existing **is** the proof the route exists. The same dashboard is inaccurate for **task** state because it derives from a hand-maintained `tasks/TASK-*.md` registry that is updated by a separate human act — one that reliably fails to happen. TASK-083 found 30+ task IDs in deliverables but only 14 registry files; the un-closed TASK-073 alone poisoned the Next Action, the active count, and the hummus launch state.

**Goal:** eliminate task-registry drift as a *failure mode* — not by demanding more discipline, but by making the dashboard derive (or at minimum cross-check) task state against the same artifacts that prove the work, and loudly alert on any mismatch.

---

## 2. PART A — Architecture options

A **task return** is the unit that matters: a deliverable that declares itself the output of a task. In this repo that declaration already exists as a `**Task:** TASK-0XX` markdown header or a `"source_task"/"build_task"/"reconciliation_task"` build-artifact key. A return is artifact-grade proof that a task produced work.

### Option A — Registry remains authoritative
The `TASK-*.md` files stay the single source of truth; returns are ignored.
- ➕ Simple; no new concepts; registry already carries rich metadata (owner, priority, deps).
- ➖ **This is the status quo that drifts.** Nothing forces the registry to track reality. Rejected — it does not address the failure mode at all.

### Option B — Task returns become authoritative
Completion is *derived entirely* from deliverables: if a return exists for TASK-0XX, the task is done; the registry is discarded or auto-generated.
- ➕ Fully artifact-derived, matching the pipeline layer that already works; impossible to "forget to close" a task.
- ➖ **Loses the forward-looking half.** A planned/open task has *no deliverable yet* — so READY/IN_PROGRESS/BLOCKED state, ownership, priority, dependencies, and the Next-Action queue have nowhere to live. A deliverable also proves *work happened*, not that a task is *fully closed* (e.g. TASK-073's go-live gate DEC-002 is still pending even though its boundary-review deliverable exists). Auto-closing on return presence would be wrong here. Rejected as the sole model.

### Option C — Hybrid (RECOMMENDED)
Split authority by what each source is actually good at:

| Concern | Authoritative source | Why |
|---|---|---|
| **Intent / planning** — open work, owner, priority, dependencies, Next-Action queue | **Registry** (`TASK-*.md`) | Only the registry can describe work that has *not produced an artifact yet*. |
| **Proof of work / completion evidence** | **Returns** (deliverables) | A deliverable is artifact-grade proof, exactly like a route file proves a route. |
| **Reconciliation / truth** | **Generator** (`generate_dashboard.py`) | Cross-checks the two and treats any disagreement as a first-class, alertable defect. |

The generator never silently overrides either side. It **detects** every divergence and emits a drift alert that names the fix. Completion stays a human judgment (a return *prompts* closure; it does not *force* it), which is correct because "done" can include gates a deliverable doesn't capture.

**Recommendation: Option C.** It keeps the planning power of the registry, gains the artifact-truth of returns, and converts "the registry silently drifted" from an invisible failure into a visible, RED, named alert. It is the same "derive from artifacts" principle that already makes the pipeline layer trustworthy, applied as a *cross-check* rather than a replacement — because task state legitimately has a forward-looking component that pure derivation cannot represent.

---

## 3. The v3 model in one diagram

```
 registry (intent)        returns (proof)          pipeline artifacts
 tasks/TASK-*.md          **Task:** / *_task        bsip*/qa/routes/datasets
      │                        │                          │
      │  open/owner/pri/deps   │  proof of work           │  derived (v2, works)
      ▼                        ▼                          ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │  generate_dashboard.py  —  reconcile + DERIVE + DETECT DRIFT       │
 │                                                                    │
 │   PHANTOM_TASK   return exists, no registry file      (CRITICAL)   │
 │   CLOSURE_DRIFT  registry open, but return exists      (HIGH)      │
 │   SNAPSHOT_DRIFT source newer than served json         (HIGH)      │
 └──────────────────────────────────────────────────────────────────┘
      │                                  │
      ▼                                  ▼
 command_center.json  (+ drift block)   ALERTS  (dashboard turns RED on drift)
```

---

## 4. PART B — Implementation (shipped)

All logic lives in the **updated generator** `generate_dashboard.py` (shared) plus the **drift watchdog** `check_drift.py` (runs without regenerating). Mapping to the five requirements:

| # | Requirement | Implementation | Verified |
|---|---|---|---|
| 1 | Detect deliverables referencing task IDs with no registry record | `scan_task_returns()` scans `01–05_*`, `decisions/`, `research/` (excludes `99_archive`) for `**Task:**` headers and `*_task` build keys; `build_drift_alerts()` emits **PHANTOM_TASK** for any return id not in the registry | ✅ 17 found, incl. **TASK-075** (the named success case) |
| 2 | Detect tasks marked READY when later deliverables prove completion | `build_drift_alerts()` emits **CLOSURE_DRIFT** for any registry task not `COMPLETE` that has a return | ✅ **TASK-073** flagged |
| 3 | Detect source files newer than command_center.json | `newest_source_mtime()` vs the served file's mtime → **SNAPSHOT_DRIFT** (computed by `check_drift.py` at read-time; a fresh `generate` run is by definition not stale) | ✅ fires after touching a source |
| 4 | Create dashboard alerts for all drift conditions | All three become standard alert objects (type/severity/message/related_task/resolution_path), merged with operational alerts and `finalize_alerts()`-ordered; a `drift` summary block is added to the JSON | ✅ shown in `command_center.json.drift` |
| 5 | Unify active-task definitions | Single `ACTIVE_STATUSES = (READY, IN_PROGRESS, BLOCKED)` constant drives `compute_task_summary`, `compute_executive` (incl. `active_task_ids`), capacity, and health | ✅ `executive.active_task_ids` now equals `task_summary.active` |

**Severity rationale:** PHANTOM_TASK is CRITICAL because the work is *entirely invisible* to the dashboard (the dangerous case). CLOSURE_DRIFT is HIGH because the task is at least visible, just mis-stated. SNAPSHOT_DRIFT is HIGH because every field may be stale until a regenerate. Any open CRITICAL/HIGH alert turns `system_health` RED/YELLOW — so a drifting registry can no longer present as false-GREEN (the exact trap in TASK-083).

**Schema additions (v2 → v3):**
- `meta.version = "3.0"`, `meta.schema_version = "command_center_v3"`
- `meta.generated_at`, `meta.newest_source_at` (ISO timestamps — freshness is now inspectable)
- `meta.drift_checked_at` (written by `check_drift.py`)
- top-level `drift` block: `{checked_at, clean, counts, phantom_tasks[], closure_drift_tasks[]}`
- new alert types: `PHANTOM_TASK`, `CLOSURE_DRIFT`, `SNAPSHOT_DRIFT`

**Self-healing semantics — detect, don't silently mutate.** v3 does not auto-rewrite `TASK-*.md` files. Each drift alert carries a `resolution_path` that names the one corrective edit; a human (or a future `--heal` flag) applies it and re-runs. This was validated live: responding to the TASK-075 PHANTOM_TASK alert by creating `tasks/TASK-075.md` dropped drift 18→17 and corrected the completed count 11→12. Auto-closing was deliberately *not* implemented, because completion can depend on gates a deliverable doesn't encode (TASK-073's go-live decision DEC-002 is still pending) — silently closing on return-presence would reintroduce inaccuracy.

**Watchdog vs generator.** `generate_dashboard.py` is the full rebuild (all sections + phantom/closure drift). `check_drift.py` is the cheap, frequent watchdog: it re-runs all three drift checks against the *served* JSON without rebuilding, refreshes only the drift alerts + `drift` block, and exits non-zero when drift is present — so it can gate a pre-commit / CI / file-watch hook.

---

## 5. Success criterion — satisfied

> If TASK-075 completes and nobody updates a registry file, the dashboard must detect the inconsistency automatically and alert it.

Demonstrated: with `tasks/TASK-075.md` absent but `hummus_content_count_reconciliation.md` ("W-1 is resolved…") present, both the generator and `check_drift.py` emit:

```
[CRITICAL] PHANTOM_TASK  TASK-075: deliverable(s) exist but no tasks/TASK-075.md
           registry record — work is invisible to the dashboard
```

and `system_health` is RED. No human input required to surface it.

---

## 6. Limitations & next steps

- **Heuristic return detection.** Recognises `**Task:**` headers and `*_task` keys. A deliverable that names its task differently is missed. Mitigation: the convention is documented in the migration doc and is now part of "definition of done."
- **No auto-heal.** By design. A `generate_dashboard.py --heal` that scaffolds a `COMPLETE` `TASK-*.md` from a return (for human confirmation) is a natural v3.1.
- **Mention vs authorship.** Only authorship signals are used, so a doc merely *citing* a task ID won't false-positive — but a genuine return that only cites won't be caught either. Acceptable for MVP.

See `command_center_v3_migration.md` for retire/keep, workflow changes, and the backfill list.

---
*Data Agent — TASK-084 — 2026-05-31*
