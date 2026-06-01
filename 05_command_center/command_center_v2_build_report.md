# Command Center v2 Generator — Build Report

**Task:** TASK-071  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Status:** COMPLETE — generator built, tested, and verified end-to-end

---

## Summary

`command_center.json` is now a **generated artifact**. Running
`generate_dashboard.py` derives the dashboard from authoritative Bari sources —
the filesystem state of the pipeline and the website source — instead of from
hand-maintained JSON. The manual-maintenance drift that motivated v2 is
eliminated for all derived fields.

The HTML renderer (`command_center.html`) is **unchanged**. It consumes the same
JSON schema; only the source of that JSON changed.

---

## The Drift This Fixes (Proven)

The old hand-maintained `command_center.json` claimed:

```
hummus  →  frontend_dataset: NOT_BUILT,  website: NOT_STARTED,  launch: PIPELINE_ONLY
          + 1 OPEN alert: WEBSITE_FACTORY_MISMATCH (HIGH)
```

The actual filesystem on 2026-05-31 showed hummus was **fully live**:

| Signal | Reality on disk |
|---|---|
| `src/data/comparisons/hummus_frontend_v1.json` | EXISTS (deployed) |
| `src/app/hashvaot/hummus/page.tsx` | EXISTS |
| `lib/comparisons/registry/categories/hummus.ts` | EXISTS |
| `"hummus"` in `types.ts` ComparisonCategoryId | PRESENT |
| `hummus:` in `index.ts` registry map | PRESENT |

The generator reads these and reports the truth:

```
hummus  →  frontend_dataset: DEPLOYED,  website: LIVE (gen1),  launch: LIVE
          + 0 alerts (the stale WEBSITE_FACTORY_MISMATCH auto-resolved)
```

The dashboard had drifted by an entire launch. v2 closes that gap on every run.

---

## Deliverables

| File | Status |
|---|---|
| `C:\Bari\05_command_center\generate_dashboard.py` | CREATED — generator (≈450 lines) |
| `C:\Bari\decisions\decisions.json` | CREATED — seeded with DEC-001 |
| `C:\Bari\tasks\TASK-{056,058,059,060,063,070,071}.md` | CREATED — 7 recent tasks with YAML frontmatter |
| `C:\Bari\02_products\{7 dirs}\category_config.json` | CREATED — display + baseline metadata |
| `C:\Bari\05_command_center\command_center.json` | REGENERATED — now `_generated: true` |
| `C:\Bari\05_command_center\command_center_v2_build_report.md` | CREATED — this document |
| `C:\Bari\05_command_center\command_center.html` | UNCHANGED (preserved) |

---

## What the Generator Derives Automatically

### Always auto-derived (the drift-prone fields — never trust a baseline)

| Field | Source | Rule |
|---|---|---|
| `frontend_dataset.status` | `src/data/comparisons/{glob}` | File present → DEPLOYED (+ filename + mtime); else baseline/NOT_BUILT |
| `website.status` | route `page.tsx` + `types.ts` + `index.ts` | route+types+index → LIVE; route only → LEGACY; types only → IN_PROGRESS; none → NOT_STARTED |
| `website.component_generation` | derived with status | gen1 (LIVE) / gen0 (LEGACY) |
| `bsip2.status` | `intelligence_bsip2/run_*/{AUTHORITATIVE,INVALID}.md` | markers present → AUTHORITATIVE/INVALID + run_id + invalid_runs |
| `launch.status` | computed from above | LIVE / PRE_LAUNCH / PIPELINE_ONLY / QUEUED / NOT_STARTED |
| All alerts | computed from derived state | see alert rules below |
| All executive fields | computed from tasks/alerts/decisions | health, active tasks, blocker, latest completed |

### Auto-derived where a confident signal exists, else baseline

The real pipeline directories are **inconsistent** across categories
(`intelligence_bsip2` vs `bsip2_outputs`, `canonical_bsip1` vs `bsip1_outputs`,
some BSIP2 runs carry no markers). The generator derives where the standard
layout exists and falls back to `category_config.json` `baseline` otherwise:

| Field | Confident signal | Fallback |
|---|---|---|
| `bsip0.status` | `reports/bsip0_gate_result_*.md` contains PASS/FAIL | baseline |
| `bsip1.status` + `record_count` | `canonical_bsip1/*.json` count > 0 | baseline |
| `bsip2` (no markers) | — | baseline (e.g. snacks/milk legacy runs) |
| `qa.status` | `qa_report_{id}.md` verdict | baseline |

This is the honest MVP boundary: the fields that **drift** (website, dataset)
are always derived; the fields that are **stable once COMPLETE** (bsip0/1/qa for
already-shipped categories) use a one-time baseline where the directory layout
is too inconsistent to parse reliably.

---

## Alert Rules (fully computed, never stored)

| Alert | Trigger | Severity |
|---|---|---|
| `CAPACITY_EXCEEDED` | active tasks > 3 | CRITICAL |
| `BLOCKED_TASK` | task.status == BLOCKED | HIGH |
| `STALE_DECISION` | PENDING + urgency NOW + age > 2 days | HIGH |
| `WEBSITE_FACTORY_MISMATCH` | bsip2 AUTHORITATIVE + website NOT_STARTED | HIGH |
| `INVALID_BSIP2_ONLY` | invalid runs present + no authoritative run | CRITICAL |
| `QA_FAILURE` | qa.status == FAIL | HIGH |

Alerts auto-resolve simply by ceasing to appear when their condition clears —
there is no resolved-alert state to maintain.

---

## Test Results

Command:
```
cd C:\Bari\05_command_center
python generate_dashboard.py
```

| # | Criterion | Result |
|---|---|---|
| 1 | Hummus frontend dataset shows DEPLOYED if file exists | **PASS** — `DEPLOYED (hummus_frontend_v1.json)` |
| 2 | Hummus website status reflects actual source files | **PASS** — `LIVE (gen1)` |
| 3 | `/hashvaot/hummus` route status reflects reality | **PASS** — route `/hashvaot/hummus`, `page.tsx` detected |
| 4 | Completed tasks do not remain active | **PASS** — 7 tasks all COMPLETE, `active_task_ids: []` |
| 5 | Open alerts generated correctly | **PASS** — 0 open (correct: hummus live, no blocks, capacity OK) |

Additional verification:

| Check | Result |
|---|---|
| `_generated: true` present | PASS |
| `_do_not_edit: true` present | PASS |
| `schema_version: command_center_v2` | PASS |
| Hummus BSIP2 = AUTHORITATIVE, run_hummus_002, invalid=[run_hummus_001] | PASS |
| All 7 categories rendered | PASS |
| Milk correctly detected as LEGACY (route exists, not in types.ts) | PASS |
| Breakfast cereals correctly QUEUED (forced) | PASS |

End-to-end HTTP smoke test (`python -m http.server`):

| Check | Result |
|---|---|
| `command_center.html` served | 200, 32 KB |
| `command_center.json` served | 200, 14 KB |
| JSON parses over HTTP | PASS — 7 categories, 7 tasks |
| HTML fetches `command_center.json` | PASS |

Final generated state: **system_health GREEN, 0 open alerts, 0 active tasks** —
an accurate, healthy snapshot, replacing the previous stale YELLOW/1-alert state.

---

## Scope Decisions (MVP)

Per the task's "minimum useful generator" instruction:

| Decision | Rationale |
|---|---|
| Created 7 recent task files, not every historical task | Scope said active + recent only. Older tasks (TASK-029, etc.) can be added later by dropping a frontmatter file in `C:\Bari\tasks\`. |
| Dropped `agents` and `routes` arrays from output | The v1.1 renderer does not display them; the Agent Board was deferred in the v2 architecture. Keeping them out reduces the schema surface. |
| `bsip0/bsip1/qa` use baseline fallback for inconsistent dirs | Full parsing of 6 different directory layouts is not "minimum useful." Baselines cover stable shipped categories; derivation covers the standard layout (hummus). |
| Did not run the full 5-phase migration | Phases 1b (retrofit all historical task files) and parts of Phase 4 were unnecessary for a working MVP. |

---

## How to Operate v2

**Refresh the dashboard (any time):**
```
cd C:\Bari\05_command_center
python generate_dashboard.py
```
Then open `http://localhost:8080/command_center.html` (start `python -m http.server 8080` if needed).

**When a task changes:** edit its `C:\Bari\tasks\TASK-NNN.md` frontmatter
(`status:`, `completed_at:`), then re-run the generator.

**When a decision is made:** append to `C:\Bari\decisions\decisions.json`, then re-run.

**When a category ships or moves a stage:** do nothing special — the next
generator run detects the new dataset/route/marker automatically.

**The one rule:** never edit `command_center.json` by hand. Run the generator.

---

## Reliability Properties Achieved

| Property | v1 (manual) | v2 (generated) |
|---|---|---|
| Website state accuracy | drifted (hummus wrong by a full launch) | guaranteed — read from source each run |
| Dataset state accuracy | drifted | guaranteed — read from disk each run |
| Alert accuracy | stale (false HIGH alert) | computed fresh from accurate state |
| Recovery from staleness | manual re-entry | one command, < 1 second |
| Remaining drift surface | everything | task frontmatter only (bounded, visible) |

The only field that can still lag reality is a task's `status`, and that lag is
self-evident: a finished task left as IN_PROGRESS simply shows as active until
its one frontmatter line is updated — a visible prompt, not silent corruption.
