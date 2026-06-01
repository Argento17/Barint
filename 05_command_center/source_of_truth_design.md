# Bari Command Center v2 — Source of Truth Design

**Task:** TASK-070  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**Purpose:** Define the authoritative source and derivation rule for every field in `command_center.json`.

---

## Principle

Each field in the dashboard has exactly one authoritative source. The generator reads that source and writes the field. No field in `command_center.json` is ever edited by hand.

Fields that cannot be derived automatically must come from a structured registry file. Registry files are the minimum viable maintenance surface — they contain only what cannot be derived from existing filesystem artifacts.

---

## Source 1 — Category Pipeline State

**Location:** `C:\Bari\02_products\{category_id}\`  
**Maintenance burden:** None — pipeline artifacts are created by existing pipeline operations.

### Category discovery

The generator scans `C:\Bari\02_products\` for subdirectories. Each subdirectory is a category. The category ID is the directory name (e.g., `hummus`, `maadanim`).

**Exception:** A `category_config.json` file in the category directory (optional) provides display metadata that cannot be derived:

```json
{
  "category_id": "hummus",
  "name_he": "חומוס",
  "name_en": "Hummus"
}
```

If this file is absent, the generator uses the directory name as both ID and display name. The file need only be created once per category — it never changes once set.

---

### BSIP0 Status

**Source:** `C:\Bari\02_products\{category_id}\reports\bsip0_gate_result_*.md`

**Derivation rules:**

```python
bsip0_reports = glob("reports/bsip0_gate_result_*.md")

if not bsip0_reports:
    status = "NOT_STARTED"

else:
    content = read_latest(bsip0_reports)
    if "VERDICT: PASS" in content:
        status = "PASS"
        gate_date = extract_date_from_filename(bsip0_reports[-1])
        report = basename(bsip0_reports[-1])
    elif "VERDICT: FAIL" in content:
        status = "FAIL"
    else:
        status = "IN_PROGRESS"
```

**Observed example:** `reports/bsip0_gate_result_20260530_204340.md` contains `VERDICT: PASS` → `status: PASS`, `gate_date: 2026-05-30`.

---

### BSIP1 Status

**Source:** `C:\Bari\02_products\{category_id}\canonical_bsip1\`

**Derivation rules:**

```python
bsip1_files = glob("canonical_bsip1/bsip1_*.json")

if not exists("canonical_bsip1/"):
    status = "NOT_STARTED"
elif len(bsip1_files) == 0:
    status = "IN_PROGRESS"
else:
    status = "COMPLETE"
    record_count = len(bsip1_files)
```

**Known issues** cannot be auto-derived (e.g., `fat_g corrupted in 59/69 records`). These come from the `category_config.json` or a separate `known_issues.json` in the category directory.

---

### BSIP2 Status

**Source:** `C:\Bari\02_products\{category_id}\intelligence_bsip2\run_*\`

**Derivation rules:**

```python
run_dirs = glob("intelligence_bsip2/run_*/")
authoritative_runs = [d for d in run_dirs if exists(d + "AUTHORITATIVE.md")]
invalid_runs = [d for d in run_dirs if exists(d + "INVALID.md")]

if not run_dirs:
    status = "NOT_STARTED"
elif authoritative_runs:
    status = "AUTHORITATIVE"
    run_id = basename(authoritative_runs[-1])  # e.g., "run_hummus_002"
    invalid_run_ids = [basename(d) for d in invalid_runs]
elif invalid_runs and len(invalid_runs) == len(run_dirs):
    status = "INVALID"
else:
    status = "IN_PROGRESS"
```

**Score distribution:** Read from `AUTHORITATIVE.md` if it contains a score summary, or from `reports/{run_id}_summary.json` if it exists. If neither, leave as `null`.

**Observed example:** `run_hummus_001/INVALID.md` + `run_hummus_002/AUTHORITATIVE.md` → `status: AUTHORITATIVE`, `run_id: run_hummus_002`, `invalid_runs: ["run_hummus_001"]`.

---

### QA Status

**Source:** `C:\Bari\02_products\{category_id}\qa\reports\qa_report_*.md`  
**Alt source:** `C:\Bari\03_operations\qa\reports\qa_report_{category_id}.md`

**Derivation rules:**

```python
qa_files = (
    glob("qa/reports/qa_report_*.md") or
    glob(f"../../03_operations/qa/reports/qa_report_{category_id}.md")
)

if not qa_files:
    status = "NOT_STARTED" if bsip2_status == "AUTHORITATIVE" else "NOT_STARTED"
else:
    content = read_latest(qa_files)
    if "PASS" in content and "FAIL" not in content:
        status = "PASS"
    elif "FAIL" in content:
        status = "FAIL"
    else:
        status = "WARN"
    
    warnings = extract_lines_matching(content, r"^\| (TRC|COV|WARN)-\d+")
    failures = extract_lines_matching(content, r"^\| FAIL")
```

---

## Source 2 — Website State

**Location:** `C:\Users\HP\bari\src\`  
**Maintenance burden:** None — these files are created by normal frontend development.

### Frontend Dataset Status

**Source:** `C:\Users\HP\bari\src\data\comparisons\`

```python
data_dir = r"C:\Users\HP\bari\src\data\comparisons"
matching = glob(f"{data_dir}/{category_id}*.json")

if matching:
    status = "DEPLOYED"
    filename = basename(matching[-1])
    built_at = file_mtime(matching[-1])
else:
    # Check if built but not yet deployed (in pipeline output directory)
    pipeline_file = glob(f"../../03_operations/bsip2/outputs/{category_id}*.json")
    status = "BUILT" if pipeline_file else "NOT_BUILT"
    filename = None
```

**Observed drift example:** `hummus_frontend_v1.json` exists in `src/data/comparisons/` as of 2026-05-31, but `command_center.json` shows `NOT_BUILT`. The generator resolves this immediately.

---

### Website / Route Status

**Source:** Three checks against `C:\Users\HP\bari\src\`

```python
check_route = exists(f"app/hashvaot/{route_name}/page.tsx")
check_types = category_id in read_file("lib/comparisons/registry/types.ts")
check_index = category_id in read_file("lib/comparisons/registry/index.ts")

if check_route and check_types and check_index:
    status = "LIVE"
    component_gen = "gen1"  # if not using legacy component names
elif check_route and not check_types:
    status = "LEGACY"       # route exists but not in registry (old architecture)
    component_gen = "gen0"
elif check_types and not check_route:
    status = "IN_PROGRESS"  # registered but route not yet created
else:
    status = "NOT_STARTED"
```

**Route name mapping:** Most categories: `route_name = category_id`. Exceptions: `milk` → `milk-comparison`, `snacks` → `snack-bars`. This mapping is stored in `category_config.json` as `route_name`.

```json
{
  "category_id": "milk",
  "route_name": "milk-comparison",
  "name_he": "חלב",
  "name_en": "Milk"
}
```

---

### Launch Status (computed)

**Source:** Derived from other derived fields — no direct source.

```python
def compute_launch_status(bsip2, qa, website, dataset):
    if website == "LIVE":
        return "LIVE"
    elif bsip2 == "AUTHORITATIVE" and qa == "PASS" and website == "NOT_STARTED":
        return "PRE_LAUNCH"
    elif bsip2 == "AUTHORITATIVE" and dataset == "DEPLOYED" and website == "NOT_STARTED":
        return "PRE_LAUNCH"
    elif bsip2 == "AUTHORITATIVE":
        return "PIPELINE_ONLY"
    elif bsip2 in ("IN_PROGRESS", "NOT_STARTED") and exists_category_dir:
        return "IN_PROGRESS"
    else:
        return "NOT_STARTED"
    # QUEUED is set via category_config.json — cannot be auto-derived
```

`QUEUED` status (e.g., Breakfast Cereals) must be set in `category_config.json` as `"forced_launch_status": "QUEUED"`. This overrides the computed value.

---

### System Health (computed)

```python
open_alerts = [a for a in alerts if a["status"] == "OPEN"]
critical = [a for a in open_alerts if a["severity"] == "CRITICAL"]
high = [a for a in open_alerts if a["severity"] == "HIGH"]

if critical or capacity_exceeded:
    system_health = "RED"
elif high or any_decision_overdue:
    system_health = "YELLOW"
else:
    system_health = "GREEN"
```

---

## Source 3 — Task Registry

**Location:** `C:\Bari\tasks\TASK-NNN.md`  
**Maintenance burden:** Low — YAML frontmatter written once at task creation, `status` field updated at task close.

### Task file format (TASK-NNN.md with YAML frontmatter)

```yaml
---
id: TASK-063
title: Command Center v1.1 build
owner: frontend-agent
status: COMPLETE
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on:
  - TASK-059
blocks: []
category_id: null
summary: >
  Build local HTML command center with Task Registry. Single-file,
  vanilla JS, reads command_center.json via fetch().
---

# TASK-063 — Command Center v1.1 Build

[Task prose content — not parsed by generator]
```

**Required fields:** `id`, `title`, `owner`, `status`, `created_at`  
**Optional fields:** `priority`, `completed_at`, `depends_on`, `blocks`, `category_id`, `summary`, `blocker`

**Status allowed values:** `READY`, `IN_PROGRESS`, `BLOCKED`, `COMPLETE`, `PAUSED`

**Migration of existing task files:** TASK-029.md and TASK-032.md are prose documents. Add YAML frontmatter blocks to the top of each file. The prose body is untouched.

**Generator reads:**

```python
import yaml, re

def parse_task_file(path):
    content = read_file(path)
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None  # file has no frontmatter — skip silently

tasks = [
    parse_task_file(f)
    for f in glob("C:/Bari/tasks/TASK-*.md")
    if parse_task_file(f) is not None
]
```

Files without frontmatter are silently skipped — no parse error, no crash. This allows legacy prose-only task files to coexist during migration.

---

### Alert auto-generation from task state

```python
for task in tasks:
    if task["status"] == "BLOCKED":
        add_alert("BLOCKED_TASK", "HIGH",
            f"{task['id']}: {task.get('blocker', 'reason not specified')}",
            related_task=task["id"])

active_tasks = [t for t in tasks if t["status"] in ("READY","IN_PROGRESS","BLOCKED")]
if len(active_tasks) > task_capacity:
    add_alert("CAPACITY_EXCEEDED", "CRITICAL",
        f"{len(active_tasks)} active tasks exceeds capacity of {task_capacity}")
```

---

## Source 4 — Decision Registry

**Location:** `C:\Bari\decisions\decisions.json`  
**Maintenance burden:** Low — append one entry when a decision is made.

### File format

Append-only JSON array. Initialize with `[]`. Each decision is a JSON object:

```json
[
  {
    "id": "DEC-001",
    "title": "HUM-001 fat data strategy for Hummus v1",
    "type": "go_nogo_gate",
    "required_from": "product-agent",
    "status": "DECIDED",
    "options": [
      "A — Display fat values despite corruption",
      "B — Suppress fat display in Hummus v1",
      "C — Delay launch until fat values corrected"
    ],
    "recommendation": "Option B — Product Agent (TASK-060)",
    "decided_at": "2026-05-31",
    "decision": "Option B — Suppress fat_g and saturated_fat_g. Add disclosure sentence to MethodologyFooter. v2 fix Q3 2026.",
    "urgency": "NOW",
    "blocking": ["TASK-058-P1"],
    "created_at": "2026-05-31",
    "notes": "See TASK-060 for full rationale."
  }
]
```

**Required fields:** `id`, `title`, `required_from`, `status`, `urgency`, `created_at`  
**Optional fields:** `type`, `options`, `recommendation`, `decided_at`, `decision`, `blocking`, `notes`

**Protocol:** When a decision is made, the deciding agent opens `decisions.json`, appends a new JSON object with `"status": "DECIDED"`, and saves. When a decision is queued (before it is made), append with `"status": "PENDING"`.

**Alert auto-generation from decisions:**

```python
from datetime import date, timedelta

for dec in decisions:
    if dec["status"] == "PENDING":
        age = (date.today() - date.fromisoformat(dec["created_at"])).days
        urgency = dec.get("urgency", "BACKLOG")
        if urgency == "NOW" and age > 2:
            add_alert("STALE_DECISION", "HIGH",
                f"{dec['id']}: {dec['title']} — pending {age} days",
                related_task=dec.get("blocking", [None])[0])
```

---

## Source 5 — Executive Fields (partly computed, partly registry)

Most executive fields are computed from other derived state. A small subset requires a registry entry.

### Computed fields

```python
executive = {
    "system_health": compute_system_health(alerts),
    "active_task_ids": [t["id"] for t in tasks if t["status"] in ("IN_PROGRESS", "BLOCKED")],
    "latest_completed_task": max(
        [t for t in tasks if t["status"] == "COMPLETE" and t.get("completed_at")],
        key=lambda t: t["completed_at"],
        default=None
    ),
    "current_blocker": derive_primary_blocker(alerts, tasks),
    "next_recommended_decision": next(
        (d for d in decisions if d["status"] == "PENDING"
         and d.get("urgency") == "NOW"),
        None
    )
}
```

### `current_blocker` derivation

```python
def derive_primary_blocker(alerts, tasks):
    # Priority 1: any CRITICAL alert
    for a in sorted(alerts, key=lambda x: SEV_ORDER[x["severity"]]):
        if a["status"] == "OPEN" and a["severity"] in ("CRITICAL", "HIGH"):
            return a["message"]
    # Priority 2: any BLOCKED task
    for t in tasks:
        if t["status"] == "BLOCKED":
            return f"{t['id']} blocked: {t.get('blocker', 'reason not specified')}"
    return None
```

---

## Alert Rules (Complete Reference)

Alerts are computed entirely from derived state. No alert is stored or manually created in v2.

| Alert type | Trigger condition | Severity | Auto-resolves? |
|---|---|---|---|
| `BLOCKED_TASK` | `task.status == BLOCKED` | HIGH | Yes — when task unblocked |
| `CAPACITY_EXCEEDED` | `active_task_count > task_capacity` | CRITICAL | Yes — when tasks complete |
| `WEBSITE_FACTORY_MISMATCH` | `bsip2 == AUTHORITATIVE` and `website == NOT_STARTED` for > 30 days | HIGH | Yes — when website goes live |
| `INVALID_BSIP2_ONLY` | All BSIP2 runs in a category are INVALID | CRITICAL | Yes — when authoritative run created |
| `STALE_DECISION` | `decision.status == PENDING` and `urgency == NOW` and `age > 2 days` | HIGH | Yes — when decision made |
| `QA_FAILURE` | `qa.status == FAIL` | HIGH | Yes — when QA re-runs and passes |
| `MISSING_CONTENT` | `website == LIVE` and any `insightLine == ""` in deployed JSON | MEDIUM | Yes — when content added |
| `STALE_CATEGORY` | `website == LIVE` and `last_updated > 270 days` (9 months) | MEDIUM | Yes — when re-run |
| `LEGACY_PAGE` | `website.component_generation == gen0` | LOW | Yes — when migrated |

**Alert ID assignment:** `ALT-{sequential_integer}`. Sequential IDs are assigned by the generator on first creation and stored in a lightweight ledger (`C:\Bari\05_command_center\alert_ledger.json`) so that IDs are stable across generator runs. If an alert condition recurs after resolution, it gets a new ID.

---

## What Cannot Be Auto-Derived (Bounded Maintenance List)

This is the complete list of things that require a human to write something:

| Field | Where to write it | How often |
|---|---|---|
| Category `name_he`, `name_en`, `route_name` | `category_config.json` in category directory | Once per category |
| Task `title`, `owner`, `priority`, `depends_on`, `blocks`, `summary` | TASK-NNN.md YAML frontmatter | Once per task |
| Task `status` | TASK-NNN.md frontmatter `status:` field | At each status change |
| Task `blocker` | TASK-NNN.md frontmatter `blocker:` field | When task is blocked |
| Decision record | Append to `decisions.json` | Once per decision |
| Category `"forced_launch_status": "QUEUED"` | `category_config.json` | Only for pre-pipeline categories |
| Known issues | `known_issues.json` in category directory | When discovered |

Everything else is derived. If a field is not in this list, an agent should not be updating it manually.

---

## File Map — v2 Authoritative Sources

```
C:\Bari\
├── 02_products\
│   └── {category_id}\
│       ├── category_config.json          ← display metadata (one-time creation)
│       ├── known_issues.json             ← issue log (updated when discovered)
│       ├── canonical_bsip1\*.json        ← BSIP1 source of truth
│       ├── intelligence_bsip2\run_*\
│       │   ├── AUTHORITATIVE.md         ← BSIP2 authoritative marker
│       │   └── INVALID.md               ← BSIP2 invalid marker
│       ├── reports\bsip0_gate_result_*.md ← BSIP0 source of truth
│       └── qa\reports\qa_report_*.md     ← QA source of truth
├── tasks\
│   └── TASK-NNN.md                       ← task registry (YAML frontmatter)
├── decisions\
│   └── decisions.json                    ← decision registry (append-only)
└── 05_command_center\
    ├── generate_dashboard.py             ← generator script
    ├── alert_ledger.json                 ← alert ID ledger (managed by generator)
    ├── command_center.json               ← OUTPUT (never edit by hand in v2)
    └── command_center.html               ← renderer (unchanged from v1.1)

C:\Users\HP\bari\src\
├── data\comparisons\{category}*.json     ← dataset deployment state
├── lib\comparisons\registry\types.ts    ← registered categories
├── lib\comparisons\registry\index.ts    ← registered categories
└── app\hashvaot\{category}\page.tsx     ← route existence
```
