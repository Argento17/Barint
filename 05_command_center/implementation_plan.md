# Bari Command Center v2 — Implementation Plan

**Task:** TASK-070  
**Owner:** Product Agent  
**Date:** 2026-05-31  
**Builds on:** command_center_v2_architecture.md, source_of_truth_design.md

---

## Goal

Replace manual `command_center.json` maintenance with a generator script that derives dashboard state from existing Bari artifacts. The HTML renderer is unchanged. Running `python generate_dashboard.py` produces a fresh, accurate `command_center.json` in seconds.

---

## Phases

| Phase | Name | Duration | Owner | Unblocks |
|---|---|---|---|---|
| 0 | Seed the decision registry | 1 hour | Product Agent | Phase 2 |
| 1 | Add YAML frontmatter to task files | 2 hours | Product Agent | Phase 3 |
| 2 | Create category config files | 1 hour | Data Agent | Phase 3 |
| 3 | Build `generate_dashboard.py` | 4–6 hours | Data Agent | Phase 4 |
| 4 | Test + validate against current state | 1 hour | Data Agent + Product Agent | Phase 5 |
| 5 | Establish session protocol | 30 min | Product Agent | Ongoing |

Total effort: approximately 9–11 hours across two agents.

---

## Phase 0 — Seed the Decision Registry

**Owner:** Product Agent  
**Duration:** 1 hour  
**Output:** `C:\Bari\decisions\decisions.json`

Create the directory and seed file:

```powershell
New-Item -ItemType Directory -Path "C:\Bari\decisions" -Force
```

Create `decisions.json` with all known decisions from prior sessions:

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
    "decision": "Option B — Suppress fat_g and saturated_fat_g from hummus frontend JSON. Disclose in MethodologyFooter. v2 fix Q3 2026.",
    "urgency": "NOW",
    "blocking": ["TASK-058-P1"],
    "created_at": "2026-05-31",
    "notes": "See TASK-060 for full rationale."
  }
]
```

**Future protocol:** When a decision is made, append to this array. Do not remove entries — change `status` to `DECIDED` and populate `decided_at` and `decision` fields.

---

## Phase 1 — Add YAML Frontmatter to Task Files

**Owner:** Product Agent  
**Duration:** 2 hours  
**Output:** All known TASK-NNN.md files have machine-parseable YAML frontmatter

### 1.1 — Retrofit existing task files

For TASK-029.md and TASK-032.md, prepend YAML frontmatter without changing the prose body:

**TASK-029.md** — prepend:
```yaml
---
id: TASK-029
title: Bari Category Launch Queue v1
owner: product-agent
status: COMPLETE
priority: MEDIUM
created_at: 2026-05-30
completed_at: 2026-05-30
depends_on: []
blocks: []
category_id: null
summary: >
  Defined 5-slot post-hummus launch queue: Bread, Snack Bars, Yogurt,
  Milk, Breakfast Cereals. Priority rationale documented.
---
```

**TASK-032.md** — prepend:
```yaml
---
id: TASK-032
title: Bari Category Expansion Wave 2 — Tahini + Nut Butters
owner: product-agent
status: COMPLETE
priority: MEDIUM
created_at: 2026-05-30
completed_at: 2026-05-30
depends_on: []
blocks: []
category_id: null
summary: >
  Decision: Option C — combined Tahini + Nut Butter acquisition wave
  under whole_food_fat archetype. Single BSIP0 pass covers both.
  Deferred until post-Hummus launch.
---
```

### 1.2 — Create task files for sessions without TASK-NNN.md files

Tasks from TASK-056 onward were delivered as session returns, not as `.md` files. Create them now in `C:\Bari\tasks\`:

Files to create:
- `TASK-049E.md`
- `TASK-056.md`
- `TASK-057.md` (Firecrawl MCP)
- `TASK-058.md`
- `TASK-058-P1.md` through `TASK-058-P4.md`
- `TASK-059.md`
- `TASK-060.md`
- `TASK-063.md`
- `TASK-070.md`

**Minimum viable format** (frontmatter only, no prose body required if content is captured elsewhere):

```yaml
---
id: TASK-056
title: Bari Growth Foundation v1
owner: marketing-agent
status: COMPLETE
priority: MEDIUM
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on: []
blocks: []
category_id: null
summary: >
  Hebrew-market growth strategy. Delivered: growth_strategy_v1.md,
  keyword_universe_v1.md, content_flywheel_v1.md.
---
```

### 1.3 — Forward protocol

**When a new task is created:**
1. Create `C:\Bari\tasks\TASK-NNN.md` with YAML frontmatter
2. Set `status: READY` or `IN_PROGRESS`
3. Run generator (or let it run at next session start)

**When a task completes:**
1. Open `TASK-NNN.md`
2. Change `status: COMPLETE`, add `completed_at: YYYY-MM-DD`
3. Run generator

This replaces the previous step of editing `command_center.json`.

---

## Phase 2 — Create Category Config Files

**Owner:** Data Agent  
**Duration:** 1 hour  
**Output:** `category_config.json` in each of 7 category directories

These files provide the display metadata and route overrides that cannot be auto-derived from the directory name alone.

**Template:**
```json
{
  "category_id": "hummus",
  "name_he": "חומוס",
  "name_en": "Hummus",
  "route_name": "hummus"
}
```

**Create for all 7 categories:**

| Directory | category_id | name_he | name_en | route_name |
|---|---|---|---|---|
| `hummus` | hummus | חומוס | Hummus | hummus |
| `maadanim` | maadanim | מעדנים | Dairy Desserts | maadanim |
| `bread` | bread | לחם | Bread | bread |
| `snack_bars` or `snacks` | snacks | חטיפים | Snack Bars | snack-bars |
| `yogurt_system` or `yogurts` | yogurts | יוגורטים | Yogurts | yogurts |
| `milk_and_alternatives` or `milk` | milk | חלב | Milk | milk-comparison |
| `breakfast_cereals` | breakfast-cereals | דגני בוקר | Breakfast Cereals | breakfast-cereals |

**Note:** For Breakfast Cereals, also set `"forced_launch_status": "QUEUED"` since the pipeline has not started. This overrides the computed launch status.

```json
{
  "category_id": "breakfast-cereals",
  "name_he": "דגני בוקר",
  "name_en": "Breakfast Cereals",
  "route_name": "breakfast-cereals",
  "forced_launch_status": "QUEUED"
}
```

---

## Phase 3 — Build `generate_dashboard.py`

**Owner:** Data Agent  
**Duration:** 4–6 hours  
**Output:** `C:\Bari\05_command_center\generate_dashboard.py`

### Script structure

```python
#!/usr/bin/env python3
"""
Bari Command Center v2 — Dashboard Generator
Usage: python generate_dashboard.py
Output: command_center.json (in the same directory)

Run at: session start, task completion, or any pipeline stage change.
"""

import json, yaml, re, glob, os
from datetime import date, datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────
BARI_ROOT      = Path(r"C:\Bari")
BARI_PRODUCTS  = BARI_ROOT / "02_products"
BARI_TASKS     = BARI_ROOT / "tasks"
BARI_DECISIONS = BARI_ROOT / "decisions" / "decisions.json"
WEBSITE_ROOT   = Path(r"C:\bari\bari-web\src")
DATA_DIR       = WEBSITE_ROOT / "data" / "comparisons"
REGISTRY_TYPES = WEBSITE_ROOT / "lib" / "comparisons" / "registry" / "types.ts"
REGISTRY_INDEX = WEBSITE_ROOT / "lib" / "comparisons" / "registry" / "index.ts"
HASHVAOT_DIR   = WEBSITE_ROOT / "app" / "hashvaot"
OUTPUT_FILE    = Path(__file__).parent / "command_center.json"
ALERT_LEDGER   = Path(__file__).parent / "alert_ledger.json"

TASK_CAPACITY  = 3

# ── Main ─────────────────────────────────────────────────────────
def main():
    tasks      = load_tasks()
    decisions  = load_decisions()
    categories = derive_categories()
    alerts     = compute_alerts(tasks, decisions, categories)
    executive  = compute_executive(tasks, decisions, alerts)

    dashboard = {
        "_update_guide": (
            "This file is generated. Do not edit by hand. "
            "Run generate_dashboard.py to refresh."
        ),
        "meta": {
            "version": "2.0",
            "last_updated": date.today().isoformat(),
            "updated_by": "generate_dashboard.py",
            "task_capacity": TASK_CAPACITY,
            "schema_version": "command_center_v2"
        },
        "executive": executive,
        "tasks": tasks,
        "decisions": decisions,
        "categories": categories,
        "alerts": alerts,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, ensure_ascii=False, indent=2)

    print(f"✓ command_center.json generated")
    print(f"  tasks: {len(tasks)} | categories: {len(categories)} "
          f"| open alerts: {sum(1 for a in alerts if a['status']=='OPEN')}")
```

### Key function: `derive_categories()`

```python
def derive_categories():
    categories = []
    for cat_dir in sorted(BARI_PRODUCTS.iterdir()):
        if not cat_dir.is_dir(): continue
        config_file = cat_dir / "category_config.json"
        if not config_file.exists(): continue  # skip non-category dirs
        config = json.loads(config_file.read_text(encoding="utf-8"))

        bsip0    = derive_bsip0(cat_dir)
        bsip1    = derive_bsip1(cat_dir)
        bsip2    = derive_bsip2(cat_dir)
        qa       = derive_qa(cat_dir, config["category_id"])
        dataset  = derive_dataset(config)
        website  = derive_website(config)
        issues   = load_known_issues(cat_dir)
        launch   = compute_launch(bsip2, qa, website, dataset, config)

        categories.append({
            "id":              config["category_id"],
            "name_he":         config["name_he"],
            "name_en":         config["name_en"],
            "product_count":   bsip1.get("record_count", 0),
            "factory_status":  compute_factory_status(bsip0, bsip1, bsip2),
            "bsip0":           bsip0,
            "bsip1":           bsip1,
            "bsip2":           bsip2,
            "qa":              qa,
            "frontend_dataset":dataset,
            "website":         website,
            "launch":          launch,
            "known_issues":    issues,
            "last_updated":    date.today().isoformat(),
        })
    return categories
```

### Key function: `load_tasks()`

```python
def load_tasks():
    tasks = []
    for task_file in sorted(BARI_TASKS.glob("TASK-*.md")):
        content = task_file.read_text(encoding="utf-8")
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            continue  # no frontmatter — skip silently
        try:
            data = yaml.safe_load(match.group(1))
            if data and "id" in data:
                tasks.append(normalize_task(data))
        except yaml.YAMLError:
            continue  # malformed frontmatter — skip silently
    
    # Sort: IN_PROGRESS → BLOCKED → READY → PAUSED → COMPLETE
    order = {"IN_PROGRESS":0,"BLOCKED":1,"READY":2,"PAUSED":3,"COMPLETE":4}
    tasks.sort(key=lambda t: (order.get(t["status"],9), t.get("priority","LOW")))
    return tasks
```

### Key function: `compute_alerts()`

```python
def compute_alerts(tasks, decisions, categories):
    ledger = load_alert_ledger()
    new_alerts = []

    # Task alerts
    for t in tasks:
        if t["status"] == "BLOCKED":
            new_alerts.append(make_alert(
                "BLOCKED_TASK", "HIGH",
                f"{t['id']}: {t.get('blocker', 'reason not specified')}",
                related_task=t["id"], ledger=ledger
            ))

    active = [t for t in tasks if t["status"] in ("READY","IN_PROGRESS","BLOCKED")]
    if len(active) > TASK_CAPACITY:
        new_alerts.append(make_alert("CAPACITY_EXCEEDED", "CRITICAL",
            f"{len(active)} active tasks exceeds capacity of {TASK_CAPACITY}",
            ledger=ledger))

    # Decision alerts
    today = date.today()
    for d in decisions:
        if d["status"] == "PENDING":
            age = (today - date.fromisoformat(d["created_at"])).days
            if d.get("urgency") == "NOW" and age > 2:
                new_alerts.append(make_alert("STALE_DECISION", "HIGH",
                    f"{d['id']}: {d['title']} — pending {age} days",
                    related_task=(d.get("blocking") or [None])[0],
                    ledger=ledger))

    # Category alerts
    for c in categories:
        bsip2_s  = c["bsip2"]["status"]
        web_s    = c["website"]["status"]
        qa_s     = c["qa"]["status"]
        inv_runs = c["bsip2"].get("invalid_runs", [])

        if bsip2_s == "AUTHORITATIVE" and web_s == "NOT_STARTED":
            new_alerts.append(make_alert("WEBSITE_FACTORY_MISMATCH", "HIGH",
                f"{c['name_en']}: BSIP2 AUTHORITATIVE but website NOT_STARTED",
                related_category=c["id"], ledger=ledger))

        if inv_runs and bsip2_s not in ("AUTHORITATIVE",):
            new_alerts.append(make_alert("INVALID_BSIP2_ONLY", "CRITICAL",
                f"{c['name_en']}: only BSIP2 runs are INVALID — no authoritative run",
                related_category=c["id"], ledger=ledger))

        if qa_s == "FAIL":
            new_alerts.append(make_alert("QA_FAILURE", "HIGH",
                f"{c['name_en']}: QA verdict FAIL",
                related_category=c["id"], ledger=ledger))

    save_alert_ledger(ledger, new_alerts)
    return [a for a in new_alerts if a["status"] == "OPEN"]
```

### Implementation notes

- **YAML parsing:** Use `PyYAML` (`pip install pyyaml`) — available in the existing `.venv`.
- **Error tolerance:** Every parse function catches exceptions and returns a safe default. A missing file, malformed YAML, or unreadable TypeScript never crashes the generator.
- **Alert ID stability:** `alert_ledger.json` maps alert type + related entity → alert ID. This ensures the same alert gets the same ID across generator runs, so IDs in documentation remain stable.
- **Encoding:** All file reads use `encoding="utf-8"` to handle Hebrew in category names and insight lines.

---

## Phase 4 — Test and Validate

**Owner:** Data Agent + Product Agent  
**Duration:** 1 hour

### 4.1 — Baseline comparison

Run the generator and compare output against the existing hand-maintained `command_center.json`. Acceptable discrepancies:

| Discrepancy type | Action |
|---|---|
| Category state differs (e.g., `hummus_frontend_v1.json` now DEPLOYED) | Accept the generator output — it is more accurate |
| Task status differs | Verify frontmatter; update if frontmatter is wrong |
| Alert exists in generator but not in JSON | Accept — generator is finding real conditions |
| Field in JSON but not in generator output | Check if field is still needed; add derivation rule if so |

### 4.2 — Smoke tests

```powershell
cd C:\Bari\05_command_center
python generate_dashboard.py

# Verify output
python -c "
import json
d = json.load(open('command_center.json', encoding='utf-8'))
assert d['meta']['schema_version'] == 'command_center_v2'
assert len(d['categories']) >= 7
assert all('bsip0' in c for c in d['categories'])
assert all('website' in c for c in d['categories'])
print('All checks passed')
"
```

### 4.3 — Visual verification

Open `http://localhost:8080/command_center.html`. Verify:
- All 7 categories render
- Hummus shows `frontend_dataset: DEPLOYED` (correcting the drift)
- Active tasks show correctly
- DEC-001 appears as DECIDED in the decision queue
- No unexpected alerts

---

## Phase 5 — Establish Session Protocol

**Owner:** Product Agent  
**Duration:** 30 minutes

The protocol replaces "remember to update command_center.json" with a single command.

### Session start protocol (append to session opening checklist)

```powershell
# Step 1: Generate fresh dashboard
cd C:\Bari\05_command_center
python generate_dashboard.py

# Step 2: Open dashboard
# (Python server should already be running, or start it)
# http://localhost:8080/command_center.html

# Step 3: Read alerts and task board before beginning work
```

### Task completion protocol (replaces: "update command_center.json")

```
1. Update TASK-NNN.md frontmatter: status → COMPLETE, add completed_at
2. If a decision was made: append to decisions.json
3. Run: python generate_dashboard.py
```

### Category stage change protocol (replaces: nothing — was never being done)

```
No action required. The next generator run will detect the stage change automatically.
Run python generate_dashboard.py after any BSIP stage completes.
```

### How to add a new task

```
1. Create C:\Bari\tasks\TASK-NNN.md with YAML frontmatter
2. Set status: READY or IN_PROGRESS
3. Run python generate_dashboard.py
```

### How to record a decision

```
1. Open C:\Bari\decisions\decisions.json
2. Append new decision object with status: DECIDED
3. Run python generate_dashboard.py
```

---

## What Changes for Each Agent

| Agent | v1 behavior | v2 behavior |
|---|---|---|
| Product Agent | Edit command_center.json at task boundaries | Update TASK-NNN.md frontmatter; append decisions.json; run generator |
| Data Agent | Edit command_center.json for category state | Nothing — category state is auto-derived |
| Frontend Agent | Nothing (did not update JSON) | Nothing — website state is auto-derived |
| QA Agent | Nothing | Nothing — QA state is auto-derived from qa_report files |
| All agents | Must remember to update JSON | Must update task frontmatter only |

The key behavioral change is small: one field in a task file (`status: COMPLETE`) instead of a full JSON edit. Category, website, QA, and alert state require no agent action — they are always derived fresh.

---

## Migration Checklist

- [ ] Phase 0: Create `C:\Bari\decisions\decisions.json` with DEC-001
- [ ] Phase 1a: Add YAML frontmatter to TASK-029.md and TASK-032.md
- [ ] Phase 1b: Create TASK-NNN.md files for TASK-049E through TASK-070
- [ ] Phase 2: Create `category_config.json` in all 7 category directories
- [ ] Phase 3: Build and test `generate_dashboard.py` locally
- [ ] Phase 4: Run baseline comparison; resolve discrepancies
- [ ] Phase 5: Remove `_update_guide` from command_center.json (it is now generated)
- [ ] Phase 5: Add `"_generated": true, "_do_not_edit": true` to command_center.json header
- [ ] Phase 5: Add generator run to session opening checklist

---

## Post-Migration: How to Know the Generator is Working

The generator is working if, after running it:

1. Hummus `frontend_dataset.status` shows `DEPLOYED` (not `NOT_BUILT`)
2. Any category where you created `AUTHORITATIVE.md` shows `AUTHORITATIVE` in BSIP2
3. Any live category's website status shows `LIVE` automatically (no entry in JSON required)
4. Alert ALT-001 (hummus website/factory mismatch) resolves automatically when `/hashvaot/hummus/page.tsx` is created

If any of these fail, there is a bug in the corresponding derivation function. Fix the function, not the JSON.

---

## The Rule That Replaces All Others

In v2, there is one rule for command center maintenance:

> **Never edit `command_center.json` by hand. Run `generate_dashboard.py` instead.**

If something is missing from the dashboard, the fix is always one of:
1. The pipeline artifact doesn't exist yet (correct — create it by doing the pipeline work)
2. The task frontmatter is wrong or missing (fix the .md file)
3. The category_config.json is missing a field (add it)
4. The decisions.json is missing an entry (append it)
5. The generator has a bug (fix the generator)

Option 6 — "edit command_center.json" — does not exist in v2.
