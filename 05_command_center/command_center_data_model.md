# Bari Command Center — Data Model v1

**Task:** TASK-059  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**File:** `C:\Bari\05_command_center\command_center.json` (source of truth)

---

## Overview

All command center state lives in a single JSON file: `command_center.json`. The dashboard renderer (whatever form it takes) reads this file and displays it. Claude agents update this file at task closeout. No other data store exists.

The model is intentionally flat and human-writable. Any agent or human must be able to update a field by hand without breaking the schema.

---

## Root Structure

```json
{
  "meta": { ... },
  "executive": { ... },
  "agents": [ ... ],
  "categories": [ ... ],
  "routes": [ ... ],
  "decisions": [ ... ],
  "alerts": [ ... ]
}
```

---

## `meta` — System Metadata

```json
{
  "meta": {
    "version": "1.0",
    "last_updated": "2026-05-31",
    "updated_by": "Product Agent",
    "task_capacity": 3,
    "schema_version": "command_center_v1"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `version` | string | Document version (semver) |
| `last_updated` | date string (YYYY-MM-DD) | Date of last update |
| `updated_by` | string | Agent name that performed last update |
| `task_capacity` | integer | Maximum concurrent active tasks (currently 3) |
| `schema_version` | string | Schema identifier for validation |

---

## `executive` — Executive Status

```json
{
  "executive": {
    "system_health": "YELLOW",
    "active_task_ids": ["TASK-059", "TASK-060"],
    "latest_completed_task": {
      "id": "TASK-058",
      "title": "Hummus Status Audit",
      "completed_at": "2026-05-31"
    },
    "current_blocker": "HUM-001 fat data decision required before hummus frontend build begins",
    "next_recommended_decision": "Confirm Option B fat suppression → unblocks Data Agent Phase 1 (TASK-058)"
  }
}
```

| Field | Type | Values | Description |
|---|---|---|---|
| `system_health` | enum | `GREEN`, `YELLOW`, `RED` | Overall health signal |
| `active_task_ids` | string[] | Task IDs | Currently in-flight tasks |
| `latest_completed_task.id` | string | TASK-NNN | Last task ID to reach COMPLETE |
| `latest_completed_task.title` | string | Free text | One-line task summary |
| `latest_completed_task.completed_at` | date string | YYYY-MM-DD | Completion date |
| `current_blocker` | string | Free text | Single most critical blocker |
| `next_recommended_decision` | string | Free text | One-line prompt for next Product Agent action |

**System health rules:**

| Condition | Health |
|---|---|
| No alerts, capacity < 3, no blockers | `GREEN` |
| 1+ HIGH alerts OR 1+ blockers OR any STALE_DECISION | `YELLOW` |
| Any CRITICAL alert OR capacity exceeded OR QA_FAILURE unresolved | `RED` |

---

## `agents` — Agent Board

Array of 9 agent objects, one per agent.

```json
{
  "agents": [
    {
      "id": "product-agent",
      "name": "Product Agent",
      "status": "WORKING",
      "active_task_id": "TASK-059",
      "active_task_title": "Command Center spec",
      "last_output": {
        "title": "TASK-060 HUM-001 decision",
        "date": "2026-05-31"
      },
      "blocker": null,
      "next_handoff": {
        "to": "data-agent",
        "description": "Fat data decision → unblocks frontend JSON build"
      }
    }
  ]
}
```

### Agent object schema

| Field | Type | Values | Description |
|---|---|---|---|
| `id` | string | kebab-case agent ID | Machine identifier |
| `name` | string | Display name | Human-readable label |
| `status` | enum | `WORKING`, `BLOCKED`, `WAITING`, `AVAILABLE`, `IDLE` | Current state |
| `active_task_id` | string \| null | TASK-NNN or null | Currently assigned task |
| `active_task_title` | string \| null | Free text | One-line task description |
| `last_output.title` | string \| null | Free text | Most recent deliverable title |
| `last_output.date` | date string \| null | YYYY-MM-DD | When last output was produced |
| `blocker` | string \| null | Free text | What is preventing progress |
| `next_handoff.to` | string \| null | Agent ID | Who receives next output |
| `next_handoff.description` | string \| null | Free text | What the handoff delivers |

### Status definitions

| Status | Meaning | `active_task_id` |
|---|---|---|
| `WORKING` | Actively executing a task | Present |
| `BLOCKED` | Has a task but cannot proceed | Present |
| `WAITING` | Output delivered; awaiting another agent | Present or null |
| `AVAILABLE` | No active task; ready for assignment | null |
| `IDLE` | No task for > 7 days | null |

### Agent ID registry (all 9 must be present)

| ID | Display name |
|---|---|
| `product-agent` | Product Agent |
| `nutrition-agent` | Nutrition Agent |
| `research-agent` | Research Agent |
| `data-agent` | Data Agent |
| `frontend-agent` | Frontend Agent |
| `design-agent` | Design Agent |
| `qa-agent` | QA Agent |
| `content-agent` | Content Agent |
| `marketing-agent` | Marketing Agent |

---

## `categories` — Category Factory Board

Array of category objects, one per tracked category.

```json
{
  "categories": [
    {
      "id": "hummus",
      "name_he": "חומוס",
      "name_en": "Hummus",
      "product_count": 69,
      "factory_status": "COMPLETE",
      "bsip0": {
        "status": "PASS",
        "gate_date": "2026-05-30",
        "report": "bsip0_gate_result_20260530_204340.md"
      },
      "bsip1": {
        "status": "COMPLETE",
        "record_count": 69,
        "known_issues": ["fat_g corrupted in 59/69 records"]
      },
      "bsip2": {
        "status": "AUTHORITATIVE",
        "run_id": "run_hummus_002",
        "invalid_runs": ["run_hummus_001"],
        "score_distribution": {
          "A": 9, "B": 24, "C": 22, "D": 11, "E": 3
        }
      },
      "qa": {
        "status": "PASS",
        "verdict_date": "2026-05-31",
        "warnings": ["TRC-003", "COV-005"],
        "failures": []
      },
      "frontend_dataset": {
        "status": "NOT_BUILT",
        "filename": null,
        "built_at": null
      },
      "website": {
        "status": "NOT_STARTED",
        "route": "/hashvaot/hummus",
        "component_generation": null,
        "page_file": null
      },
      "launch": {
        "status": "PIPELINE_ONLY",
        "live_since": null,
        "blocking_issues": ["HUM-001", "GAP-05", "GAP-06", "GAP-07"]
      },
      "known_issues": [
        {
          "id": "HUM-001",
          "title": "Fat data corruption — 59/69 BSIP1 records",
          "severity": "HIGH",
          "blocking": true,
          "resolution": "Option B (suppress) pending Product Agent decision"
        },
        {
          "id": "HUM-002",
          "title": "Sugar data absent — sugars_g 0% coverage",
          "severity": "MEDIUM",
          "blocking": false,
          "resolution": "Accepted at category level"
        }
      ],
      "last_updated": "2026-05-31"
    }
  ]
}
```

### Category status enums

| Field | Allowed values |
|---|---|
| `factory_status` | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED` |
| `bsip0.status` | `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED` |
| `bsip1.status` | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED` |
| `bsip2.status` | `NOT_STARTED`, `IN_PROGRESS`, `AUTHORITATIVE`, `INVALID`, `BLOCKED` |
| `qa.status` | `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `WARN`, `PENDING` |
| `frontend_dataset.status` | `NOT_BUILT`, `BUILDING`, `BUILT`, `DEPLOYED`, `STALE` |
| `website.status` | `NOT_STARTED`, `IN_PROGRESS`, `LIVE`, `LEGACY`, `BROKEN` |
| `website.component_generation` | `gen0`, `gen1`, null |
| `launch.status` | `NOT_STARTED`, `PIPELINE_ONLY`, `PRE_LAUNCH`, `LIVE`, `BLOCKED`, `QUEUED` |

### Known issue object

| Field | Type | Description |
|---|---|---|
| `id` | string | Issue ID (e.g., `HUM-001`) |
| `title` | string | One-line description |
| `severity` | enum | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `blocking` | boolean | True if this issue prevents the next step |
| `resolution` | string | Current resolution path or status |

---

## `routes` — Website Readiness Board

Array of route objects, one per URL the website serves or should serve.

```json
{
  "routes": [
    {
      "path": "/hashvaot/maadanim",
      "category_id": "maadanim",
      "page_status": "LIVE",
      "component_generation": "gen1",
      "meta": {
        "title_he": "השוואת מעדנים — 2026 | ברי",
        "description_he": "...",
        "title_present": true,
        "description_present": true
      },
      "seo": {
        "hreflang_set": true,
        "lang_he_set": true,
        "dir_rtl_set": true,
        "structured_data": false,
        "sitemap_included": true
      },
      "qa": {
        "last_audit_date": "2026-05-30",
        "last_verdict": "PASS",
        "mobile_verified": true,
        "desktop_verified": true
      },
      "notes": null
    },
    {
      "path": "/hashvaot/hummus",
      "category_id": "hummus",
      "page_status": "MISSING",
      "component_generation": null,
      "meta": {
        "title_he": null,
        "description_he": null,
        "title_present": false,
        "description_present": false
      },
      "seo": {
        "hreflang_set": false,
        "lang_he_set": false,
        "dir_rtl_set": false,
        "structured_data": false,
        "sitemap_included": false
      },
      "qa": {
        "last_audit_date": null,
        "last_verdict": null,
        "mobile_verified": false,
        "desktop_verified": false
      },
      "notes": "Page not yet created. BSIP2 pipeline complete."
    }
  ]
}
```

### Route status enums

| Field | Allowed values |
|---|---|
| `page_status` | `LIVE`, `MISSING`, `BROKEN`, `LEGACY`, `IN_PROGRESS` |
| `component_generation` | `gen0`, `gen1`, null |
| `seo.*` (booleans) | true, false |
| `qa.last_verdict` | `PASS`, `FAIL`, `WARN`, null |

---

## `decisions` — Decision Queue

Array of decision objects.

```json
{
  "decisions": [
    {
      "id": "DEC-001",
      "title": "HUM-001 fat data strategy for Hummus v1",
      "type": "go_nogo_gate",
      "required_from": "product-agent",
      "status": "DECIDED",
      "options": ["A - Display despite corruption", "B - Suppress fat display", "C - Delay until corrected"],
      "recommendation": "Option B — Product Agent (TASK-060)",
      "decided_at": "2026-05-31",
      "decision": "Option B — Suppress fat display",
      "urgency": "NOW",
      "blocking": ["GAP-02 frontend JSON build"],
      "created_at": "2026-05-31",
      "notes": "See TASK-060 for full rationale"
    }
  ]
}
```

### Decision object schema

| Field | Type | Values | Description |
|---|---|---|---|
| `id` | string | DEC-NNN | Decision identifier |
| `title` | string | Free text | One-line description |
| `type` | enum | `product_agent`, `nutrition_agent`, `go_nogo_gate`, `exception` | Decision category |
| `required_from` | string | Agent ID | Who must decide |
| `status` | enum | `PENDING`, `DECIDED`, `BLOCKED`, `WITHDRAWN` | Current state |
| `options` | string[] | Free text array | Options under consideration |
| `recommendation` | string \| null | Free text | Who recommends, and what |
| `decided_at` | date string \| null | YYYY-MM-DD | When decided |
| `decision` | string \| null | Free text | What was decided |
| `urgency` | enum | `NOW`, `THIS_WEEK`, `BACKLOG` | How soon needed |
| `blocking` | string[] | Free text | What cannot proceed |
| `created_at` | date string | YYYY-MM-DD | When queued |
| `notes` | string \| null | Free text | Optional additional context |

---

## `alerts` — Alerts

Array of alert objects. Resolved alerts remain in the array with `status: "RESOLVED"`.

```json
{
  "alerts": [
    {
      "id": "ALT-001",
      "type": "WEBSITE_FACTORY_MISMATCH",
      "severity": "HIGH",
      "message": "Hummus: BSIP2 AUTHORITATIVE since 2026-05-31 but website NOT STARTED",
      "related_category": "hummus",
      "related_task": "TASK-058",
      "related_agent": null,
      "created_at": "2026-05-31",
      "resolved_at": null,
      "status": "OPEN",
      "resolution_path": "Complete TASK-058 Phase 2 (Frontend Agent)"
    }
  ]
}
```

### Alert object schema

| Field | Type | Values | Description |
|---|---|---|---|
| `id` | string | ALT-NNN | Alert identifier |
| `type` | enum | See alert types below | Machine-readable alert category |
| `severity` | enum | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` | Urgency level |
| `message` | string | Free text | Human-readable description |
| `related_category` | string \| null | Category ID | Which category this concerns |
| `related_task` | string \| null | TASK-NNN | Which task this concerns |
| `related_agent` | string \| null | Agent ID | Which agent this concerns |
| `created_at` | date string | YYYY-MM-DD | When alert was raised |
| `resolved_at` | date string \| null | YYYY-MM-DD | When resolved |
| `status` | enum | `OPEN`, `RESOLVED`, `SUPPRESSED` | Current state |
| `resolution_path` | string \| null | Free text | How to resolve |

### Alert type registry

| Type constant | Trigger | Default severity |
|---|---|---|
| `BLOCKED_TASK` | Task status = BLOCKED | HIGH |
| `STALE_CATEGORY` | Category last updated > 9 months + website live | MEDIUM |
| `QA_FAILURE` | QA verdict = FAIL | HIGH |
| `MISSING_OWNER` | Task with no assigned agent | HIGH |
| `CAPACITY_EXCEEDED` | Active tasks > task_capacity | CRITICAL |
| `WEBSITE_FACTORY_MISMATCH` | BSIP2 AUTHORITATIVE + website NOT_STARTED for > 30 days | HIGH |
| `INVALID_BSIP2_ONLY` | Only available BSIP2 run is INVALID | CRITICAL |
| `STALE_DECISION` | Decision urgency=NOW open > 2 days | HIGH |
| `IDLE_AGENT` | Agent status = IDLE | LOW |
| `LEGACY_PAGE_UNAUDITED` | Gen0 page + no QA audit in > 60 days | LOW |
| `MISSING_CONTENT` | Frontend JSON built + any insightLine = "" for > 30 days | MEDIUM |

---

## Full Schema: `command_center.json`

```json
{
  "meta": {
    "version": "string",
    "last_updated": "YYYY-MM-DD",
    "updated_by": "string",
    "task_capacity": 3,
    "schema_version": "command_center_v1"
  },
  "executive": {
    "system_health": "GREEN|YELLOW|RED",
    "active_task_ids": ["string"],
    "latest_completed_task": {
      "id": "string",
      "title": "string",
      "completed_at": "YYYY-MM-DD"
    },
    "current_blocker": "string|null",
    "next_recommended_decision": "string|null"
  },
  "agents": [
    {
      "id": "string",
      "name": "string",
      "status": "WORKING|BLOCKED|WAITING|AVAILABLE|IDLE",
      "active_task_id": "string|null",
      "active_task_title": "string|null",
      "last_output": {
        "title": "string|null",
        "date": "YYYY-MM-DD|null"
      },
      "blocker": "string|null",
      "next_handoff": {
        "to": "string|null",
        "description": "string|null"
      }
    }
  ],
  "categories": [
    {
      "id": "string",
      "name_he": "string",
      "name_en": "string",
      "product_count": "integer",
      "factory_status": "NOT_STARTED|IN_PROGRESS|COMPLETE|BLOCKED",
      "bsip0": {
        "status": "NOT_STARTED|IN_PROGRESS|PASS|FAIL|BLOCKED",
        "gate_date": "YYYY-MM-DD|null",
        "report": "string|null"
      },
      "bsip1": {
        "status": "NOT_STARTED|IN_PROGRESS|COMPLETE|BLOCKED",
        "record_count": "integer|null",
        "known_issues": ["string"]
      },
      "bsip2": {
        "status": "NOT_STARTED|IN_PROGRESS|AUTHORITATIVE|INVALID|BLOCKED",
        "run_id": "string|null",
        "invalid_runs": ["string"],
        "score_distribution": {
          "A": "integer", "B": "integer", "C": "integer",
          "D": "integer", "E": "integer"
        }
      },
      "qa": {
        "status": "NOT_STARTED|IN_PROGRESS|PASS|FAIL|WARN|PENDING",
        "verdict_date": "YYYY-MM-DD|null",
        "warnings": ["string"],
        "failures": ["string"]
      },
      "frontend_dataset": {
        "status": "NOT_BUILT|BUILDING|BUILT|DEPLOYED|STALE",
        "filename": "string|null",
        "built_at": "YYYY-MM-DD|null"
      },
      "website": {
        "status": "NOT_STARTED|IN_PROGRESS|LIVE|LEGACY|BROKEN",
        "route": "string|null",
        "component_generation": "gen0|gen1|null",
        "page_file": "string|null"
      },
      "launch": {
        "status": "NOT_STARTED|PIPELINE_ONLY|PRE_LAUNCH|LIVE|BLOCKED|QUEUED",
        "live_since": "YYYY-MM-DD|null",
        "blocking_issues": ["string"]
      },
      "known_issues": [
        {
          "id": "string",
          "title": "string",
          "severity": "CRITICAL|HIGH|MEDIUM|LOW",
          "blocking": "boolean",
          "resolution": "string"
        }
      ],
      "last_updated": "YYYY-MM-DD"
    }
  ],
  "routes": [
    {
      "path": "string",
      "category_id": "string",
      "page_status": "LIVE|MISSING|BROKEN|LEGACY|IN_PROGRESS",
      "component_generation": "gen0|gen1|null",
      "meta": {
        "title_he": "string|null",
        "description_he": "string|null",
        "title_present": "boolean",
        "description_present": "boolean"
      },
      "seo": {
        "hreflang_set": "boolean",
        "lang_he_set": "boolean",
        "dir_rtl_set": "boolean",
        "structured_data": "boolean",
        "sitemap_included": "boolean"
      },
      "qa": {
        "last_audit_date": "YYYY-MM-DD|null",
        "last_verdict": "PASS|FAIL|WARN|null",
        "mobile_verified": "boolean",
        "desktop_verified": "boolean"
      },
      "notes": "string|null"
    }
  ],
  "decisions": [
    {
      "id": "string",
      "title": "string",
      "type": "product_agent|nutrition_agent|go_nogo_gate|exception",
      "required_from": "string",
      "status": "PENDING|DECIDED|BLOCKED|WITHDRAWN",
      "options": ["string"],
      "recommendation": "string|null",
      "decided_at": "YYYY-MM-DD|null",
      "decision": "string|null",
      "urgency": "NOW|THIS_WEEK|BACKLOG",
      "blocking": ["string"],
      "created_at": "YYYY-MM-DD",
      "notes": "string|null"
    }
  ],
  "alerts": [
    {
      "id": "string",
      "type": "string",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "message": "string",
      "related_category": "string|null",
      "related_task": "string|null",
      "related_agent": "string|null",
      "created_at": "YYYY-MM-DD",
      "resolved_at": "YYYY-MM-DD|null",
      "status": "OPEN|RESOLVED|SUPPRESSED",
      "resolution_path": "string|null"
    }
  ]
}
```

---

## Update Rules

1. **Immutable IDs.** Once assigned, `DEC-NNN` and `ALT-NNN` IDs never change.
2. **Resolved ≠ deleted.** Resolved alerts and decided decisions remain in the array. Status changes from `OPEN` to `RESOLVED`.
3. **Invalid runs stay listed.** BSIP2 `invalid_runs` array accumulates — invalid run IDs are never removed.
4. **Date format.** All dates are `YYYY-MM-DD`. No timestamps, no timezones.
5. **Null is not empty string.** Missing data is `null`, not `""` or `"—"`.
6. **Sequential IDs.** New decisions and alerts get the next available sequential ID. Do not reuse IDs.
7. **Agent IDs are kebab-case.** Use the ID registry values; do not invent new IDs.
8. **Category IDs match frontend registry.** `category.id` must match `ComparisonCategoryId` in `src/lib/comparisons/registry/types.ts` once the category is registered.
