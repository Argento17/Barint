#!/usr/bin/env python3
"""
Bari Command Center v2 — Dashboard Generator
=============================================

Derives command_center.json from authoritative Bari sources. Never edit
command_center.json by hand; run this script instead.

Usage:
    cd C:\\Bari\\05_command_center
    python generate_dashboard.py
    # or, using the project venv:
    C:\\Bari\\.venv\\Scripts\\python.exe generate_dashboard.py

Authoritative sources (read-only):
    C:\\Bari\\02_products\\{dir}\\category_config.json    display + baseline metadata
    C:\\Bari\\02_products\\{dir}\\...                       pipeline indicators (bsip0/1/2, qa)
    C:\\Bari\\tasks\\TASK-*.md                              task registry (YAML frontmatter)
    C:\\Bari\\decisions\\decisions.json                    decision registry (append-only)
    C:\\Users\\HP\\bari\\src\\...                            website / dataset state

Output:
    C:\\Bari\\05_command_center\\command_center.json       (generated, do not edit)

The HTML renderers (command_center_v4.html operational + audit_center.html) read
the JSON via fetch(). command_center_legacy.html is the retired v2 renderer.
"""

import os
import sys
from pathlib import Path

# ── Interpreter guard (TASK-127) ────────────────────────────────────────────
# Dashboard generation must not depend on whichever Python is on PATH. If we are
# not already running under the project venv, re-exec with it so PyYAML (and any
# other venv deps) are always present. Once running under the venv the resolved
# paths match and the guard is a no-op (no re-exec loop).
_VENV_PY = Path(r"C:\Bari") / ".venv" / "Scripts" / ("python.exe" if os.name == "nt" else "python")
if _VENV_PY.exists() and Path(sys.executable).resolve() != _VENV_PY.resolve():
    os.execv(str(_VENV_PY), [str(_VENV_PY), os.path.abspath(__file__), *sys.argv[1:]])

import json
import re
import glob
from datetime import date, datetime

try:
    import yaml
except ImportError:
    raise SystemExit(
        "PyYAML is required. Install it into the project venv:\n"
        "  C:\\Bari\\.venv\\Scripts\\python.exe -m pip install pyyaml"
    )

# ── Paths ─────────────────────────────────────────────────────────────────────
BARI_ROOT      = Path(r"C:\Bari")
PRODUCTS_DIR   = BARI_ROOT / "02_products"
TASKS_DIR      = BARI_ROOT / "tasks"
DECISIONS_FILE = BARI_ROOT / "decisions" / "decisions.json"
QA_OPS_DIR     = BARI_ROOT / "03_operations" / "qa" / "reports"

WEBSITE_SRC    = Path(r"C:\bari-web\src")
DATA_DIR       = WEBSITE_SRC / "data" / "comparisons"
TYPES_TS       = WEBSITE_SRC / "lib" / "comparisons" / "registry" / "types.ts"
INDEX_TS       = WEBSITE_SRC / "lib" / "comparisons" / "registry" / "index.ts"
HASHVAOT_DIR   = WEBSITE_SRC / "app" / "hashvaot"

HERE           = Path(__file__).resolve().parent
OUTPUT_FILE    = HERE / "command_center.json"

TASK_CAPACITY  = 3
TODAY          = date.today()

SEV_ORDER  = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
# Registry Protocol v1 lifecycle (TASK-114/115/116). The only five task states:
# IN_PROGRESS, BLOCKED, RETURNED, CHANGES_REQUESTED, CLOSED. CLOSED is terminal.
TASK_ORDER = {"IN_PROGRESS": 0, "CHANGES_REQUESTED": 1, "BLOCKED": 2,
              "RETURNED": 3, "CLOSED": 4}
PRI_ORDER  = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

# Single source of truth for what "active" means (used everywhere — v3 unify).
# ACTIVE  = work consuming a slot (Active Work + rework). RETURNED is awaiting
# review, so it is OPEN but not ACTIVE (it does not consume agent capacity).
ACTIVE_STATUSES   = ("IN_PROGRESS", "BLOCKED", "CHANGES_REQUESTED")
OPEN_STATUSES     = ("IN_PROGRESS", "BLOCKED", "CHANGES_REQUESTED", "RETURNED")  # not CLOSED
TERMINAL_STATUSES = ("CLOSED",)
# States where a deliverable is EXPECTED to exist — so its presence is not
# closure drift (RETURNED/CHANGES_REQUESTED have been delivered at least once).
DELIVERED_STATUSES = ("RETURNED", "CHANGES_REQUESTED", "CLOSED")

# ── v3 self-healing: where to look for "task returns" (authored deliverables) ──
# A deliverable that declares itself the output of a task is the authoritative
# proof that the task produced work. Markdown declares it with a `**Task:**`
# header; build artifacts declare it with a *_task json/py key. 99_archive is
# intentionally excluded — archived work is retired, not live drift.
RETURN_SCAN_DIRS = [
    BARI_ROOT / "01_framework",
    BARI_ROOT / "02_products",
    BARI_ROOT / "03_operations",
    BARI_ROOT / "04_growth",
    BARI_ROOT / "05_command_center",
    BARI_ROOT / "decisions",
    BARI_ROOT / "research",
]
RETURN_SCAN_EXTS = (".md", ".json", ".py")
# `**Task:** TASK-075`  (markdown deliverable header — authored-by, not a mention)
RE_MD_TASK_HEADER = re.compile(r"^\*\*Task:\*\*\s*(TASK-\d+)", re.MULTILINE)
# `"source_task": "TASK-061"` / build_task / reconciliation_task / task
RE_JSON_TASK_KEY  = re.compile(
    r'"(?:source_task|build_task|reconciliation_task|task)"\s*:\s*"(TASK-\d+)"'
)
# Sources whose mtime, if newer than the served command_center.json, means the
# served dashboard is a stale snapshot (snapshot drift).
SNAPSHOT_SOURCE_DIRS = [TASKS_DIR] + RETURN_SCAN_DIRS


# ── Safe IO helpers ───────────────────────────────────────────────────────────
def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else None


# ── Category state derivation ─────────────────────────────────────────────────
def derive_bsip0(cat_dir, baseline):
    reports = sorted(glob.glob(str(cat_dir / "reports" / "bsip0_gate_result_*.md")))
    if not reports:
        return dict(baseline.get("bsip0", {"status": "NOT_STARTED"}))
    content = read_text(reports[-1])
    if re.search(r"PASS", content):
        gate_date = None
        m = re.search(r"(\d{8})", os.path.basename(reports[-1]))
        if m:
            try:
                gate_date = datetime.strptime(m.group(1), "%Y%m%d").date().isoformat()
            except Exception:
                pass
        return {"status": "PASS", "gate_date": gate_date,
                "report": os.path.basename(reports[-1])}
    if re.search(r"FAIL", content):
        return {"status": "FAIL", "gate_date": None, "report": os.path.basename(reports[-1])}
    return dict(baseline.get("bsip0", {"status": "IN_PROGRESS"}))


def derive_bsip1(cat_dir, baseline):
    canon = cat_dir / "canonical_bsip1"
    if canon.is_dir():
        files = glob.glob(str(canon / "*.json"))
        if files:
            return {"status": "COMPLETE", "record_count": len(files)}
    return dict(baseline.get("bsip1", {"status": "NOT_STARTED", "record_count": None}))


def derive_bsip2(cat_dir, baseline):
    b2 = cat_dir / "intelligence_bsip2"
    base = dict(baseline.get("bsip2", {"status": "NOT_STARTED"}))
    base.setdefault("run_id", None)
    base.setdefault("invalid_runs", [])
    if not b2.is_dir():
        return base
    run_dirs = [d for d in b2.iterdir() if d.is_dir() and d.name.startswith("run_")]
    if not run_dirs:
        return base
    auth, invalid = [], []
    for d in run_dirs:
        if (d / "AUTHORITATIVE.md").exists():
            auth.append(d.name)
        if (d / "INVALID.md").exists():
            invalid.append(d.name)
    if auth:
        return {"status": "AUTHORITATIVE", "run_id": sorted(auth)[-1],
                "invalid_runs": sorted(invalid)}
    if invalid and len(invalid) == len(run_dirs):
        return {"status": "INVALID", "run_id": None, "invalid_runs": sorted(invalid)}
    # runs present but no markers (inconsistent legacy layout) -> trust baseline
    base["invalid_runs"] = sorted(invalid)
    return base


def derive_qa(cat_dir, category_id, baseline):
    candidates = []
    candidates += glob.glob(str(cat_dir / "qa" / "reports" / "qa_report*.md"))
    candidates += glob.glob(str(QA_OPS_DIR / f"qa_report_{category_id}.md"))
    if not candidates:
        return dict(baseline.get("qa", {"status": "NOT_STARTED"}))
    content = read_text(candidates[-1])
    if "FAIL" in content and re.search(r"\bFAIL\b", content):
        # distinguish a real fail verdict from the word in a checklist header
        if re.search(r"verdict[:\s].*FAIL", content, re.IGNORECASE):
            return {"status": "FAIL"}
    if re.search(r"PASS", content):
        return {"status": "PASS"}
    return dict(baseline.get("qa", {"status": "WARN"}))


def derive_dataset(config):
    glob_pat = config.get("dataset_glob", f"{config['category_id']}*.json")
    matches = sorted(glob.glob(str(DATA_DIR / glob_pat)))
    if matches:
        latest = matches[-1]
        try:
            built = datetime.fromtimestamp(os.path.getmtime(latest)).date().isoformat()
        except Exception:
            built = None
        return {"status": "DEPLOYED", "filename": os.path.basename(latest), "built_at": built}
    # fall back to baseline (covers legacy datasets stored elsewhere, e.g. milk)
    base = config.get("baseline", {}).get("frontend_dataset")
    if base:
        return dict(base)
    return {"status": "NOT_BUILT", "filename": None, "built_at": None}


def derive_website(config):
    category_id = config["category_id"]
    route_name  = config.get("route_name", category_id)

    route_exists = (HASHVAOT_DIR / route_name / "page.tsx").exists()
    types_text   = read_text(TYPES_TS)
    index_text   = read_text(INDEX_TS)
    in_types = f'"{category_id}"' in types_text
    in_index = (f"{category_id}:" in index_text) or (f"/categories/{category_id}" in index_text)

    if route_exists and in_types and in_index:
        status, gen = "LIVE", "gen1"
    elif route_exists and not in_types:
        status, gen = "LEGACY", "gen0"
    elif in_types and not route_exists:
        status, gen = "IN_PROGRESS", None
    else:
        status, gen = "NOT_STARTED", None

    return {
        "status": status,
        "route": f"/hashvaot/{route_name}",
        "component_generation": gen,
        "page_file": "page.tsx" if route_exists else None,
    }


def compute_factory_status(bsip0, bsip1, bsip2):
    if bsip2.get("status") == "AUTHORITATIVE":
        return "COMPLETE"
    started = any(s.get("status") not in (None, "NOT_STARTED")
                  for s in (bsip0, bsip1, bsip2))
    return "IN_PROGRESS" if started else "NOT_STARTED"


def compute_launch(config, bsip2, qa, website, dataset, open_cat_tasks):
    """A category is LIVE only when integrated AND no open work is tagged to it.
    Website files can exist (page + registry) while the category is still
    pre-launch (insight content, QA warnings, go-live approval outstanding).
    Open tasks tagged to the category are the authoritative 'not launched' signal."""
    forced = config.get("forced_launch_status")
    if forced:
        return {"status": forced, "live_since": None, "blocking_issues": []}
    ws = website.get("status")
    if ws in ("LIVE", "LEGACY"):
        if open_cat_tasks:
            return {"status": "PRE_LAUNCH", "live_since": None,
                    "blocking_issues": list(open_cat_tasks)}
        return {"status": "LIVE", "live_since": None, "blocking_issues": []}
    b2 = bsip2.get("status")
    if b2 == "AUTHORITATIVE" and dataset.get("status") in ("DEPLOYED", "BUILT") and ws == "NOT_STARTED":
        return {"status": "PRE_LAUNCH", "live_since": None, "blocking_issues": []}
    if b2 == "AUTHORITATIVE":
        return {"status": "PIPELINE_ONLY", "live_since": None, "blocking_issues": []}
    if b2 in ("IN_PROGRESS",):
        return {"status": "IN_PROGRESS", "live_since": None, "blocking_issues": []}
    return {"status": "NOT_STARTED", "live_since": None, "blocking_issues": []}


def derive_categories(tasks):
    # map category_id -> list of open (non-complete) task ids tagged to it
    open_by_cat = {}
    for t in tasks:
        cid = t.get("category_id")
        if cid and t["status"] not in TERMINAL_STATUSES:
            open_by_cat.setdefault(cid, []).append(t["id"])

    cats = []
    for cat_dir in sorted(PRODUCTS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        config = read_json(cat_dir / "category_config.json")
        if not config or "category_id" not in config:
            continue  # not a dashboard-tracked category
        baseline = config.get("baseline", {})

        bsip0   = derive_bsip0(cat_dir, baseline)
        bsip1   = derive_bsip1(cat_dir, baseline)
        bsip2   = derive_bsip2(cat_dir, baseline)
        qa      = derive_qa(cat_dir, config["category_id"], baseline)
        dataset = derive_dataset(config)
        website = derive_website(config)
        open_tasks = open_by_cat.get(config["category_id"], [])
        launch  = compute_launch(config, bsip2, qa, website, dataset, open_tasks)

        cats.append({
            "id":               config["category_id"],
            "name_he":          config.get("name_he", config["category_id"]),
            "name_en":          config.get("name_en", config["category_id"]),
            "product_count":    bsip1.get("record_count") or 0,
            "factory_status":   compute_factory_status(bsip0, bsip1, bsip2),
            "bsip0":            bsip0,
            "bsip1":            bsip1,
            "bsip2":            bsip2,
            "qa":               qa,
            "frontend_dataset": dataset,
            "website":          website,
            "launch":           launch,
            "open_work":        open_tasks,
            "known_issues":     config.get("known_issues", []),
            "last_updated":     TODAY.isoformat(),
        })
    # stable order: live categories first, then by launch state, then name
    rank = {"LIVE": 0, "PRE_LAUNCH": 1, "PIPELINE_ONLY": 2, "IN_PROGRESS": 3,
            "QUEUED": 4, "NOT_STARTED": 5}
    cats.sort(key=lambda c: (rank.get(c["launch"]["status"], 9), c["name_en"]))
    return cats


# ── Task registry ─────────────────────────────────────────────────────────────
def load_tasks():
    """Returns (tasks, unparseable).

    unparseable = registry files that exist on disk but produce no task row
    (missing YAML frontmatter, malformed YAML, or no `id`). v3 surfaces these as
    REGISTRY_UNPARSEABLE so an existing TASK-*.md can never silently disappear
    (TASK-092 finding #2)."""
    def _fid(path):
        mm = re.match(r"(TASK-\d+)", path.stem)
        return mm.group(1) if mm else path.stem

    tasks = []
    unparseable = []
    for f in sorted(TASKS_DIR.glob("TASK-*.md")):
        content = read_text(f)
        m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not m:
            unparseable.append({"id": _fid(f), "file": f.name,
                                "reason": "no YAML frontmatter block"})
            continue
        try:
            data = yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            unparseable.append({"id": _fid(f), "file": f.name,
                                "reason": f"invalid YAML frontmatter ({e.__class__.__name__})"})
            continue
        if not isinstance(data, dict) or "id" not in data:
            unparseable.append({"id": _fid(f), "file": f.name,
                                "reason": "frontmatter missing required 'id' field"})
            continue
        tasks.append({
            "id":           data.get("id"),
            "title":        data.get("title", ""),
            "owner":        data.get("owner"),
            "status":       data.get("status", "IN_PROGRESS"),
            "priority":     data.get("priority", "MEDIUM"),
            "created_at":   str(data.get("created_at")) if data.get("created_at") else None,
            "completed_at": str(data.get("completed_at")) if data.get("completed_at") else None,
            "depends_on":   data.get("depends_on") or [],
            "blocks":       data.get("blocks") or [],
            "category_id":  data.get("category_id"),
            "blocker":      data.get("blocker"),
            "close_reason": data.get("close_reason"),
            "summary":      (data.get("summary") or "").strip(),
        })
    tasks.sort(key=lambda t: (TASK_ORDER.get(t["status"], 9),
                              PRI_ORDER.get(t["priority"], 9),
                              t["id"]))
    return tasks, unparseable


# ── Decision registry ─────────────────────────────────────────────────────────
def load_decisions():
    data = read_json(DECISIONS_FILE, default=[])
    return data if isinstance(data, list) else []


# ── v3 self-healing: task returns + drift detection ───────────────────────────
def scan_task_returns():
    """Scan live deliverables for task IDs they declare themselves authored by.

    Returns: { "TASK-075": [ {"file": <relpath>, "kind": "md_header"|"build_key"} ] }

    This is the artifact-derived view of "which tasks produced work" — the same
    'derive from artifacts' principle that already makes pipeline state accurate,
    applied to task completion. It does NOT require any registry file to exist;
    that asymmetry is exactly what lets us detect registry drift.
    """
    returns = {}
    for base in RETURN_SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in RETURN_SCAN_EXTS:
                continue
            text = read_text(path)
            if "TASK-" not in text:
                continue
            try:
                rel = path.relative_to(BARI_ROOT).as_posix()
            except ValueError:
                rel = path.as_posix()
            for tid in RE_MD_TASK_HEADER.findall(text):
                returns.setdefault(tid, []).append({"file": rel, "kind": "md_header"})
            for tid in RE_JSON_TASK_KEY.findall(text):
                returns.setdefault(tid, []).append({"file": rel, "kind": "build_key"})
    return returns


def newest_source_mtime():
    """Most recent mtime across all source inputs (epoch seconds), or 0."""
    newest = 0.0
    seen = set()
    candidates = []
    for base in SNAPSHOT_SOURCE_DIRS:
        if base.is_dir():
            candidates += [p for p in base.rglob("*")
                           if p.is_file() and p.suffix.lower() in (".md", ".json", ".py")]
    if DECISIONS_FILE.exists():
        candidates.append(DECISIONS_FILE)
    for p in candidates:
        rp = str(p.resolve())
        if rp in seen or rp == str(OUTPUT_FILE.resolve()):
            continue  # never compare the served file against itself
        seen.add(rp)
        try:
            newest = max(newest, p.stat().st_mtime)
        except OSError:
            pass
    return newest


def _drift_alert(seq, atype, severity, message, related_task=None, resolution=None):
    return {
        "id": f"ALT-{seq:03d}",
        "type": atype,
        "severity": severity,
        "message": message,
        "related_category": None,
        "related_task": related_task,
        "related_agent": None,
        "created_at": TODAY.isoformat(),
        "resolved_at": None,
        "status": "OPEN",
        "resolution_path": resolution,
    }


def build_drift_alerts(tasks, returns, registry_ids, unparseable=None, ref_mtime=None):
    """The three v3 drift conditions. Returns un-finalized alert dicts.

    1. PHANTOM_TASK  — a deliverable claims a task ID with no registry file.
    2. CLOSURE_DRIFT — registry says a task is still open, but a deliverable
                       authored by that task ID exists (work is actually done).
    3. SNAPSHOT_DRIFT (only when ref_mtime given, e.g. the served json's mtime)
                       — a source file is newer than the served dashboard.
    """
    alerts = []
    by_status = {t["id"]: t["status"] for t in tasks}

    # 1. PHANTOM_TASK
    for tid in sorted(returns):
        if tid not in registry_ids:
            files = ", ".join(sorted({r["file"] for r in returns[tid]})[:3])
            alerts.append(_drift_alert(
                0, "PHANTOM_TASK", "CRITICAL",
                f"{tid}: deliverable(s) exist but no tasks/{tid}.md registry record — "
                f"work is invisible to the dashboard ({files})",
                related_task=tid,
                resolution=f"Create tasks/{tid}.md (status reflecting reality), then re-run generate_dashboard.py."))

    # 2. CLOSURE_DRIFT — a task that claims work is NOT yet delivered (IN_PROGRESS/
    #    BLOCKED) but a deliverable authored by it exists. RETURNED/CHANGES_REQUESTED/
    #    CLOSED are exempt: a deliverable is expected for them (Registry Protocol v1).
    for tid, status in sorted(by_status.items()):
        if status not in DELIVERED_STATUSES and tid in returns:
            files = ", ".join(sorted({r["file"] for r in returns[tid]})[:3])
            alerts.append(_drift_alert(
                0, "CLOSURE_DRIFT", "HIGH",
                f"{tid}: registry status is {status} but a deliverable authored by it exists "
                f"({files}) — work appears delivered, registry not updated",
                related_task=tid,
                resolution=f"Verify the deliverable; set tasks/{tid}.md status: RETURNED "
                           f"(awaiting review) or CLOSED (+ completed_at) if accepted."))

    # 4. REGISTRY_UNPARSEABLE — a TASK-*.md exists but produced no task row, so
    #    the file is invisible on the Task Board. (TASK-092 finding #2.)
    for u in (unparseable or []):
        alerts.append(_drift_alert(
            0, "REGISTRY_UNPARSEABLE", "HIGH",
            f"{u['id']}: tasks/{u['file']} exists but is not shown on the Task Board "
            f"({u['reason']}) — existing task file is invisible",
            related_task=u["id"],
            resolution=f"Add YAML frontmatter (id/title/owner/status/priority) to "
                       f"tasks/{u['file']}, then re-run generate_dashboard.py."))

    # 3. SNAPSHOT_DRIFT (served-file freshness; skipped during a fresh regenerate)
    if ref_mtime:
        newest = newest_source_mtime()
        if newest > ref_mtime + 1:  # 1s tolerance for fs granularity
            from datetime import datetime as _dt
            src_iso = _dt.fromtimestamp(newest).isoformat(timespec="seconds")
            ref_iso = _dt.fromtimestamp(ref_mtime).isoformat(timespec="seconds")
            alerts.append(_drift_alert(
                0, "SNAPSHOT_DRIFT", "HIGH",
                f"Source files changed at {src_iso}, newer than command_center.json "
                f"({ref_iso}) — dashboard is a stale snapshot",
                resolution="Re-run generate_dashboard.py."))
    return alerts


def finalize_alerts(alerts):
    """Sort by severity, then assign stable sequential ALT-### ids."""
    alerts.sort(key=lambda a: SEV_ORDER.get(a["severity"], 9))
    for i, a in enumerate(alerts, start=1):
        a["id"] = f"ALT-{i:03d}"
    return alerts


# ── Alerts (fully computed from derived state) ────────────────────────────────
def compute_alerts(tasks, decisions, categories):
    alerts = []
    seq = 1

    def add(atype, severity, message, related_category=None,
            related_task=None, resolution=None):
        nonlocal seq
        alerts.append({
            "id": f"ALT-{seq:03d}",
            "type": atype,
            "severity": severity,
            "message": message,
            "related_category": related_category,
            "related_task": related_task,
            "related_agent": None,
            "created_at": TODAY.isoformat(),
            "resolved_at": None,
            "status": "OPEN",
            "resolution_path": resolution,
        })
        seq += 1

    # Capacity
    active = [t for t in tasks if t["status"] in ACTIVE_STATUSES]
    if len(active) > TASK_CAPACITY:
        add("CAPACITY_EXCEEDED", "CRITICAL",
            f"{len(active)} active tasks exceeds capacity of {TASK_CAPACITY}",
            resolution="Close or unblock an active task (or move one to RETURNED).")

    # Blocked tasks
    for t in tasks:
        if t["status"] == "BLOCKED":
            add("BLOCKED_TASK", "HIGH",
                f"{t['id']}: {t.get('blocker') or 'reason not specified'}",
                related_task=t["id"],
                resolution="Resolve the blocker, then set status to IN_PROGRESS.")

    # Stale pending decisions
    for d in decisions:
        if d.get("status") == "PENDING":
            try:
                age = (TODAY - date.fromisoformat(str(d.get("created_at")))).days
            except Exception:
                age = 0
            if d.get("urgency") == "NOW" and age > 2:
                add("STALE_DECISION", "HIGH",
                    f"{d['id']}: {d.get('title','')} — pending {age} days",
                    related_task=(d.get("blocking") or [None])[0],
                    resolution=f"Resolve decision {d['id']}.")

    # Category-level
    for c in categories:
        b2, ws, qa = c["bsip2"]["status"], c["website"]["status"], c["qa"]["status"]
        if b2 == "AUTHORITATIVE" and ws == "NOT_STARTED":
            add("WEBSITE_FACTORY_MISMATCH", "HIGH",
                f"{c['name_en']}: BSIP2 AUTHORITATIVE but website NOT_STARTED",
                related_category=c["id"],
                resolution="Build frontend dataset and integrate website route.")
        if c["bsip2"].get("invalid_runs") and b2 not in ("AUTHORITATIVE",):
            add("INVALID_BSIP2_ONLY", "CRITICAL",
                f"{c['name_en']}: only BSIP2 runs are INVALID — no authoritative run",
                related_category=c["id"],
                resolution="Produce an authoritative BSIP2 run.")
        if qa == "FAIL":
            add("QA_FAILURE", "HIGH",
                f"{c['name_en']}: QA verdict FAIL",
                related_category=c["id"],
                resolution="Address QA failures and re-run the audit.")

    # NOTE: finalize (sort + id assignment) happens in main() after drift alerts
    # are merged in, so all alerts share one ordered ALT-### sequence.
    return alerts


# ── Next Action (the single most important "what do I do now") ────────────────
def _pick(cands):
    """Highest priority, then lowest task id, deterministic."""
    return sorted(cands, key=lambda t: (PRI_ORDER.get(t.get("priority"), 9), t["id"]))[0]


def _build_next(t, reason, categories, default_unblocks=None):
    name_by_id = {c["id"]: c["name_en"] for c in categories}
    unblocks = ", ".join(t.get("blocks") or [])
    if not unblocks:
        if default_unblocks:
            unblocks = default_unblocks
        elif t.get("category_id"):
            unblocks = f"{name_by_id.get(t['category_id'], t['category_id'])} launch"
        else:
            unblocks = "—"
    return {
        "task_id":  t["id"],
        "title":    t["title"],
        "owner":    t.get("owner"),
        "status":   t["status"],
        "priority": t.get("priority"),
        "reason":   reason,
        "unblocks": unblocks,
    }


def compute_next_action(tasks, decisions, categories):
    """Answer 'what should I do next?' via a fixed priority ladder (Registry
       Protocol v1 states):
       1. BLOCKED task waiting on a decision / external unblock
       2. CHANGES_REQUESTED task (rework the Controller asked for)
       3. IN_PROGRESS task blocking a launch (category not yet LIVE)
       4. highest-priority IN_PROGRESS task
       5. RETURNED task awaiting the Controller's review/acceptance
    """
    name_by_id = {c["id"]: c["name_en"] for c in categories}
    not_live   = {c["id"] for c in categories if c["launch"]["status"] != "LIVE"}
    open_tasks = [t for t in tasks if t["status"] in OPEN_STATUSES]

    # 1. Blocked tasks (waiting on a user decision / external unblock)
    blocked = [t for t in open_tasks if t["status"] == "BLOCKED"]
    if blocked:
        t = _pick(blocked)
        reason = "Blocked — " + (t.get("blocker") or "waiting on a decision")
        return _build_next(t, reason, categories)

    # 2. Changes requested — rework before it can return again
    changes = [t for t in open_tasks if t["status"] == "CHANGES_REQUESTED"]
    if changes:
        t = _pick(changes)
        return _build_next(t, "Changes requested — rework before it can return.", categories)

    # 3. In-progress tasks blocking a launch (tagged to a category that is not LIVE)
    inprog = [t for t in open_tasks if t["status"] == "IN_PROGRESS"]
    inprog_launch = [t for t in inprog if t.get("category_id") in not_live]
    if inprog_launch:
        t = _pick(inprog_launch)
        cat = name_by_id.get(t.get("category_id"), "the category")
        return _build_next(t, f"Last gate before {cat} launch.", categories,
                           default_unblocks=f"{cat} launch")

    # 4. Highest-priority in-progress task
    if inprog:
        t = _pick(inprog)
        return _build_next(t, "Currently in progress — finish this first.", categories)

    # 5. Returned work awaiting the Controller's review/acceptance
    returned = [t for t in open_tasks if t["status"] == "RETURNED"]
    if returned:
        t = _pick(returned)
        return _build_next(t, "Returned — awaiting your review/acceptance.", categories)

    return None


def compute_task_summary(tasks):
    # Registry Protocol v1 states. `active` = ACTIVE_STATUSES (work in flight).
    s = {"active": 0, "in_progress": 0, "blocked": 0,
         "returned": 0, "changes_requested": 0, "closed": 0}
    for t in tasks:
        st = t["status"]
        if st == "IN_PROGRESS":          s["in_progress"] += 1
        elif st == "BLOCKED":            s["blocked"] += 1
        elif st == "RETURNED":           s["returned"] += 1
        elif st == "CHANGES_REQUESTED":  s["changes_requested"] += 1
        elif st == "CLOSED":             s["closed"] += 1
    s["active"] = sum(1 for t in tasks if t["status"] in ACTIVE_STATUSES)
    return s


# ── Executive (computed) ──────────────────────────────────────────────────────
def compute_executive(tasks, decisions, alerts):
    open_alerts = [a for a in alerts if a["status"] == "OPEN"]
    has_critical = any(a["severity"] == "CRITICAL" for a in open_alerts)
    has_high     = any(a["severity"] == "HIGH" for a in open_alerts)
    active = [t for t in tasks if t["status"] in ACTIVE_STATUSES]

    if has_critical or len(active) > TASK_CAPACITY:
        health = "RED"
    elif has_high:
        health = "YELLOW"
    else:
        health = "GREEN"

    completed = [t for t in tasks if t["status"] == "CLOSED" and t.get("completed_at")]
    latest = max(completed, key=lambda t: t["completed_at"], default=None)

    # primary blocker: first critical/high alert, else first blocked task
    blocker = None
    for a in open_alerts:
        if a["severity"] in ("CRITICAL", "HIGH"):
            blocker = a["message"]
            break
    if not blocker:
        for t in tasks:
            if t["status"] == "BLOCKED":
                blocker = f"{t['id']} blocked: {t.get('blocker') or 'reason not specified'}"
                break

    next_dec = next((d for d in decisions
                     if d.get("status") == "PENDING" and d.get("urgency") == "NOW"), None)

    return {
        "system_health": health,
        # Unified definition: ACTIVE = READY+IN_PROGRESS+BLOCKED, identical to
        # task_summary.active. (v2 used IN_PROGRESS+BLOCKED here, contradicting
        # the counter — TASK-083 finding #8.)
        "active_task_ids": [t["id"] for t in tasks if t["status"] in ACTIVE_STATUSES],
        "latest_completed_task": (
            {"id": latest["id"], "title": latest["title"], "completed_at": latest["completed_at"]}
            if latest else None
        ),
        "current_blocker": blocker,
        "next_recommended_decision": (
            f"{next_dec['id']} — {next_dec.get('title','')}" if next_dec else None
        ),
    }


# ── Drift summary block ───────────────────────────────────────────────────────
DRIFT_TYPES = ("PHANTOM_TASK", "CLOSURE_DRIFT", "SNAPSHOT_DRIFT", "REGISTRY_UNPARSEABLE")


def summarize_drift(drift_alerts):
    by_type = {dt: [a["related_task"] for a in drift_alerts if a["type"] == dt]
               for dt in DRIFT_TYPES}
    return {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "clean": len(drift_alerts) == 0,
        "counts": {dt: len(by_type[dt]) for dt in DRIFT_TYPES},
        "phantom_tasks": [t for t in by_type["PHANTOM_TASK"] if t],
        "closure_drift_tasks": [t for t in by_type["CLOSURE_DRIFT"] if t],
        "registry_unparseable": [t for t in by_type["REGISTRY_UNPARSEABLE"] if t],
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    tasks, unparseable = load_tasks()
    decisions   = load_decisions()
    categories  = derive_categories(tasks)

    # v3 self-healing: artifact-derived task returns + drift detection.
    # registry_ids includes unparseable files (they exist on disk) so a prose-only
    # task file is never mis-flagged PHANTOM — it gets REGISTRY_UNPARSEABLE instead.
    registry_ids = {t["id"] for t in tasks} | {u["id"] for u in unparseable}
    returns      = scan_task_returns()

    operational  = compute_alerts(tasks, decisions, categories)
    # ref_mtime=None: a fresh regenerate is by definition not a stale snapshot.
    drift        = build_drift_alerts(tasks, returns, registry_ids, unparseable, ref_mtime=None)
    alerts       = finalize_alerts(operational + drift)

    executive    = compute_executive(tasks, decisions, alerts)  # sees drift alerts
    next_action  = compute_next_action(tasks, decisions, categories)
    task_summary = compute_task_summary(tasks)

    now_iso = datetime.now().isoformat(timespec="seconds")
    newest  = newest_source_mtime()
    newest_iso = datetime.fromtimestamp(newest).isoformat(timespec="seconds") if newest else None

    dashboard = {
        "_generated": True,
        "_do_not_edit": True,
        "_update_guide": (
            "Generated by generate_dashboard.py. Do NOT edit by hand. Update task "
            "frontmatter (C:\\Bari\\tasks\\TASK-*.md), decisions.json, or category_config.json, "
            "then re-run: python generate_dashboard.py. Between runs, "
            "python check_drift.py refreshes drift alerts without a full regenerate."
        ),
        "meta": {
            "version": "3.0",
            "last_updated": TODAY.isoformat(),
            "generated_at": now_iso,
            "newest_source_at": newest_iso,
            "updated_by": "generate_dashboard.py",
            "task_capacity": TASK_CAPACITY,
            "schema_version": "command_center_v3",
            # Freshness (TASK-092 finding #1). A fresh regenerate is current by
            # definition; check_drift.py flips `stale` true when a source file is
            # newer than the served snapshot. The HTML renders a banner from these.
            "drift_checked_at": now_iso,
            "stale": False,
            "stale_reason": None,
        },
        "executive": executive,
        "next_action": next_action,
        "task_summary": task_summary,
        "drift": summarize_drift(drift),
        "tasks": tasks,
        "decisions": decisions,
        "categories": categories,
        "alerts": alerts,
    }

    OUTPUT_FILE.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    open_alerts = [a for a in alerts if a["status"] == "OPEN"]
    active = [t for t in tasks if t["status"] in ACTIVE_STATUSES]
    print("command_center.json generated")
    print(f"  health:     {executive['system_health']}")
    if next_action:
        print(f"  NEXT ACTION: {next_action['task_id']} — {next_action['title']} "
              f"({next_action['owner']})  -> unblocks: {next_action['unblocks']}")
    else:
        print("  NEXT ACTION: none — no open work")
    print(f"  tasks:      {len(tasks)} total | active={task_summary['active']} "
          f"in_progress={task_summary['in_progress']} blocked={task_summary['blocked']} "
          f"returned={task_summary['returned']} changes={task_summary['changes_requested']} "
          f"closed={task_summary['closed']}")
    print(f"  categories: {len(categories)}")
    print(f"  decisions:  {len(decisions)} ({sum(1 for d in decisions if d.get('status')=='PENDING')} pending)")
    drift_alerts = [a for a in open_alerts if a["type"] in DRIFT_TYPES]
    print(f"  returns:    {len(returns)} task IDs found in deliverables | "
          f"registry has {len(registry_ids)} task ids")
    if unparseable:
        print(f"  UNPARSEABLE: {len(unparseable)} registry file(s) not shown as rows -> "
              + ", ".join(u["file"] for u in unparseable))
    print(f"  drift:      {len(drift_alerts)} "
          f"(phantom={sum(1 for a in drift_alerts if a['type']=='PHANTOM_TASK')} "
          f"closure={sum(1 for a in drift_alerts if a['type']=='CLOSURE_DRIFT')})")
    print(f"  alerts:     {len(open_alerts)} open")
    for c in categories:
        print(f"    - {c['id']:<18} bsip2={c['bsip2']['status']:<13} "
              f"dataset={c['frontend_dataset']['status']:<10} "
              f"website={c['website']['status']:<12} launch={c['launch']['status']}")
    for a in open_alerts:
        print(f"    ! [{a['severity']}] {a['message']}")


if __name__ == "__main__":
    main()
