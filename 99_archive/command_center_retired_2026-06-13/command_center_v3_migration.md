# Command Center v3 — Migration from v2 (PART C)

**Task:** TASK-084
**Owner:** Data Agent
**Date:** 2026-05-31
**Companion:** `command_center_v3_design.md`

This is a **non-breaking, in-place upgrade.** The HTML renderer, the JSON path, and the v2 derivation logic for categories/pipeline are unchanged. v3 only *adds* drift detection, freshness metadata, a `drift` block, and the unified active definition. No data is lost; the migration is mostly a one-time registry backfill plus two workflow changes.

---

## 1. Files to RETIRE

| File / thing | Action | Why |
|---|---|---|
| The "`_do_not_edit` ⇒ therefore trustworthy" assumption | Retire the *belief*, not a file | v2's banner implied freshness it didn't have. v3's `meta.generated_at` / `newest_source_at` / `drift` block make staleness inspectable instead of assumed. |
| Split "active" definitions (`active_task_ids` = IN_PROGRESS+BLOCKED vs `task_summary.active` = +READY) | Retired in code | Replaced by the single `ACTIVE_STATUSES` constant. No file to delete; the divergent logic is gone. |
| `command_center.json` schema `command_center_v2` | Superseded | Auto-replaced on first v3 run (now `command_center_v3`). The old file is overwritten by the generator; nothing to hand-migrate. |

**Nothing is physically deleted.** No generator, spec, or data file is removed — v3 is additive. Archived items under `99_archive/` stay archived and are intentionally **excluded** from return scanning (retired work is not live drift).

## 2. Files to KEEP (unchanged)

| File | Role |
|---|---|
| `command_center.html` | Renderer — reads the same JSON via `fetch()`; can optionally surface the new `drift` block and `meta.*_at` timestamps (enhancement, not required). |
| `command_center.json` | Same path, same consumer; gains `drift` + `meta` fields and new alert types only. |
| `tasks/TASK-*.md`, `decisions/decisions.json`, `02_products/*/category_config.json` | Same authoritative sources. |
| v2 derivation functions (`derive_bsip*`, `derive_qa`, `derive_dataset`, `derive_website`, `compute_launch`, …) | Untouched — the pipeline layer already works. |

## 3. Files ADDED / CHANGED

| File | Status | Contents |
|---|---|---|
| `generate_dashboard.py` | **changed** | `ACTIVE_STATUSES`; `scan_task_returns()`; `newest_source_mtime()`; `build_drift_alerts()`; `finalize_alerts()`; `summarize_drift()`; main() merges drift alerts + writes `drift` block + freshness meta. |
| `check_drift.py` | **new** | Standalone drift watchdog — re-checks the three conditions against the served JSON without a full rebuild; refreshes drift alerts; exits non-zero on drift (hook/CI gate). |
| `command_center_v3_design.md`, `command_center_v3_migration.md` | **new** | This design + migration. |
| `tasks/TASK-075.md` | **new (backfill demo)** | First backfilled record — created in response to its PHANTOM_TASK alert to prove the heal loop closes. |

---

## 4. Workflow changes (the durable fix)

v3 makes drift *visible*; these two changes make it *rare*.

1. **Definition of done now includes the registry.** A task is not complete until both (a) its deliverable carries a `**Task:** TASK-0XX` header (or `*_task` build key), and (b) its `tasks/TASK-0XX.md` is set `status: COMPLETE` with `completed_at`. New tasks get a `TASK-*.md` file at creation (status READY), so they can never be phantom.
   - *Enforcement:* run `check_drift.py` as a **pre-commit / CI gate**. It exits 1 on any drift, blocking a commit that adds a deliverable without its registry record. This is the mechanical guarantee that replaces "remember to update the registry."

2. **Regenerate-on-change, not on-demand.** Wire `generate_dashboard.py` (full) on task/decision/config change, and `check_drift.py` (cheap) on a short interval or file-watch. SNAPSHOT_DRIFT covers the gap: if sources move ahead of the served JSON, the dashboard says so in HIGH-severity RED rather than showing a silent stale snapshot.

Convention to publish in `ownership_matrix` / `agent_os`: **"Every task return declares its task ID; every closed task has a COMPLETE registry record. The dashboard will flag you if it doesn't."**

---

## 5. One-time backfill (clearing pre-existing drift)

The first v3 run surfaced **18 real, pre-existing drift conditions** that v2 hid. Clearing them is data entry against existing deliverables (no new work):

**CLOSURE_DRIFT (1) — verify then close:**
- `TASK-073` — boundary review delivered + co-signed (TASK-076); W-1 resolved (TASK-075). **Do not blind-close:** go-live gate **DEC-002 is still PENDING**. Resolve DEC-002, then set COMPLETE. (This is exactly why v3 alerts rather than auto-closes.)

**PHANTOM_TASK (17 → 16 after TASK-075 backfill) — create a `COMPLETE` registry record from each deliverable:**

| Task | Evidence (deliverable) |
|---|---|
| TASK-075 | `hummus_content_count_reconciliation.md` ✅ **done in this migration** |
| TASK-061 | `frontend/hummus_frontend_build_report.md`, `hummus_frontend_v1.json` |
| TASK-062 | `content/content_generation_report.md`, `hummus_insights_v1.md` |
| TASK-064 | `content/hummus_content_review.md` |
| TASK-076 | `launch/hummus_boundary_review_nutrition_verdict.md` |
| TASK-080 | `frontend/hummus_dataset_reconciliation_report.md` |
| TASK-081 | `hummus_insight_integration_report.md` |
| TASK-039 | `qa/reports/hummus_fat_anomaly_TASK039.md` |
| TASK-044 | `03_operations/bsip2/routing_fix_hummus_v1.md` |
| TASK-045 | `bsip2/run_hummus_002/baseline_freeze_report.md` |
| TASK-046 | `bsip2/sprint1/production_decision_v1.md` |
| TASK-047 | `bsip2/sprint1/production_release_v1.md` |
| TASK-048 | `bsip2/experimental/bsip2_061_water_predominance_pilot.md` |
| TASK-051 | `bsip2/experimental/pilot_rerun_spec_bsip2_061.md` |
| TASK-054 | `02_products/tahini/category_boundary_definition.md` |
| TASK-004 | `01_framework/governance/cno-distortion-classification-v1.md` |
| TASK-083 | `command_center_accuracy_audit.md`, `dashboard_drift_analysis.md` |

> Backfilling these is a candidate follow-up (e.g. TASK-085). It is *data entry*, not engineering — each file is a short frontmatter stub mirroring its deliverable. Until done, the dashboard correctly stays RED: it is now honestly reporting drift that was previously invisible.

---

## 6. Rollout steps

1. ✅ Land `generate_dashboard.py` (v3) and `check_drift.py`.
2. ✅ Run `python generate_dashboard.py` — confirm `schema_version: command_center_v3`, `drift` block present, `executive.active_task_ids == task_summary.active`.
3. ✅ Confirm the success criterion: TASK-075 PHANTOM_TASK fires with no registry file; clears when `tasks/TASK-075.md` is added.
4. ⬜ Backfill the remaining 16 phantom + verify/close TASK-073 (§5).
5. ⬜ Add `check_drift.py` to the pre-commit / CI gate and a regenerate-on-change hook (§4).
6. ⬜ (Optional) Update `command_center.html` to render the `drift` block and `meta.*_at` freshness.

## 7. Rollback

Pure additive change. To revert: restore the previous `generate_dashboard.py` and delete `check_drift.py`; the next run rewrites `command_center.json` in the v2 shape. No data migration to undo. (Not recommended — rollback reinstates the invisible-drift failure mode.)

---
*Data Agent — TASK-084 — 2026-05-31*
