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

Output (all generated — do not edit):
    command_center.json          full board; CLOSED tasks trimmed (summary -> archive)
    command_center_live.json     lean ~19KB read path (open tasks only) — default agent read
    command_center_archive.json  full CLOSED-task detail (summaries preserved)

    python generate_dashboard.py --digest   prints the morning report (no files written)

The HTML renderer (command_center.html) reads command_center.json via fetch() and
never touches a CLOSED task's summary, so the trim is invisible to it.

Optional task frontmatter (all default-safe):
    work_type: execution|coordination|decision   only `execution` counts toward WIP
    drift_ack: "<reason>"                         suppress a KNOWN-GOOD closure-drift
    (a `reopened_at:` value auto-suppresses closure-drift — deliverable is expected-invalid)
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
TASKS_CLOSED_DIR = BARI_ROOT / "tasks" / "closed"   # archived CLOSED files
DECISIONS_FILE = BARI_ROOT / "decisions" / "decisions.json"
QA_OPS_DIR     = BARI_ROOT / "03_operations" / "qa" / "reports"

WEBSITE_SRC    = Path(r"C:\bari\bari-web\src")
DATA_DIR       = WEBSITE_SRC / "data" / "comparisons"
TYPES_TS       = WEBSITE_SRC / "lib" / "comparisons" / "registry" / "types.ts"
INDEX_TS       = WEBSITE_SRC / "lib" / "comparisons" / "registry" / "index.ts"
HASHVAOT_DIR   = WEBSITE_SRC / "app" / "hashvaot"

HERE           = Path(__file__).resolve().parent
OUTPUT_FILE    = HERE / "command_center.json"
LIVE_FILE      = HERE / "command_center_live.json"      # lean default read (~6-8KB)
ARCHIVE_FILE   = HERE / "command_center_archive.json"   # full closed-task detail
STRATEGY_FILE  = HERE / "strategy.json"                 # P1–P5 strategy checkpoints

TASK_CAPACITY   = 3       # legacy global reference (kept in meta for context)
OWNER_WIP_LIMIT = 2       # ★ per-OWNER execution WIP cap (kanban per-column limit).
                          # RED fires only when a single agent exceeds this — a real
                          # bottleneck — not when N agents each carry one task.
STALE_TASK_DAYS = 7        # IN_PROGRESS longer than this with no deliverable -> alert
TODAY          = date.today()

SEV_ORDER  = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
# Registry Protocol v1 lifecycle (TASK-114/115/116). The only five task states:
# IN_PROGRESS, BLOCKED, RETURNED, CHANGES_REQUESTED, CLOSED. CLOSED is terminal.
TASK_ORDER = {"IN_PROGRESS": 0, "CHANGES_REQUESTED": 1, "BLOCKED": 2,
              "RETURNED": 3, "CLOSED": 4}
PRI_ORDER  = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def id_sortkey(tid):
    """Natural sort for TASK ids: TASK-99 < TASK-180 < TASK-180A < TASK-180B.
    Used to break ties between tasks that share a date-only completed_at (the
    registry has no sub-day close timestamp). A higher id is a weak proxy for
    'more recently closed' within a single day — strictly better than the
    lexical default, which made the lowest id win."""
    mm = re.match(r"TASK-(\d+)([A-Z]*)", tid or "")
    return (int(mm.group(1)), mm.group(2)) if mm else (0, tid or "")

# Single source of truth for what "active" means (used everywhere — v3 unify).
# ACTIVE  = work consuming a slot (Active Work + rework). RETURNED is awaiting
# review, so it is OPEN but not ACTIVE (it does not consume agent capacity).
ACTIVE_STATUSES   = ("IN_PROGRESS", "BLOCKED", "CHANGES_REQUESTED")
OPEN_STATUSES     = ("IN_PROGRESS", "BLOCKED", "CHANGES_REQUESTED", "RETURNED")  # not CLOSED
TERMINAL_STATUSES = ("CLOSED",)
# States where a deliverable is EXPECTED to exist — so its presence is not
# closure drift (RETURNED/CHANGES_REQUESTED have been delivered at least once).
DELIVERED_STATUSES = ("RETURNED", "CHANGES_REQUESTED", "CLOSED")

# work_type classification (★④ real-WIP). Only EXECUTION work consumes a build
# slot. COORDINATION (umbrella/CC tasks) and DECISION (awaiting an operator call)
# are open and tracked but are NOT hands-on-keyboard capacity. Default: execution.
WIP_WORK_TYPES = ("execution",)
# Fields the HTML task board never reads for a CLOSED task. Dropping them from the
# *main* JSON (kept in command_center_archive.json) cuts ~65% of the file with no
# loss of live signal. id/title/owner/status/completed_at/close_reason are kept.
CLOSED_DROP_FIELDS = ("summary", "depends_on", "blocks", "blocker",
                      "category_id", "drift_ack", "reopened_at", "work_type")

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
    # editorial-product tasks (blog posts, copy) are visible in open_work but
    # do not block the launch state of a category that is already LIVE.
    NON_BLOCKING_WORK_TYPES = frozenset(["editorial-product"])
    open_by_cat = {}
    blocking_by_cat = {}
    for t in tasks:
        cid = t.get("category_id")
        if cid and t["status"] not in TERMINAL_STATUSES:
            open_by_cat.setdefault(cid, []).append(t["id"])
            if t.get("work_type") not in NON_BLOCKING_WORK_TYPES:
                blocking_by_cat.setdefault(cid, []).append(t["id"])

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
        open_tasks    = open_by_cat.get(config["category_id"], [])
        blocking_tasks = blocking_by_cat.get(config["category_id"], [])
        launch  = compute_launch(config, bsip2, qa, website, dataset, blocking_tasks)

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


def _norm_cc_comments(raw):
    """Normalize the optional `cc_comments` frontmatter into a render-ready list.

    CC Agent leaves review notes ON a task by adding `cc_comments:` to that task's
    .md frontmatter (the authoritative source — command_center.json is derived and
    never hand-edited). Accepts a plain string, a list of strings, or a list of
    dicts `{date, text, flag}`. `flag` ∈ {fyi, verify, blocker} (default fyi) drives
    the dashboard styling. Always returns a list of dicts so the HTML can render it
    uniformly near the task row.
    """
    if not raw:
        return []
    if isinstance(raw, str):
        raw = [raw]
    out = []
    for item in raw:
        if isinstance(item, dict):
            text = str(item.get("text", "")).strip()
            if not text:
                continue
            flag = str(item.get("flag", "fyi")).strip().lower()
            out.append({
                "text": text,
                "date": str(item["date"]) if item.get("date") else None,
                "flag": flag if flag in ("fyi", "verify", "blocker") else "fyi",
            })
        else:
            text = str(item).strip()
            if text:
                out.append({"text": text, "date": None, "flag": "fyi"})
    return out


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
    _task_files = sorted(TASKS_DIR.glob("TASK-*.md")) + sorted(TASKS_CLOSED_DIR.glob("TASK-*.md") if TASKS_CLOSED_DIR.exists() else [])
    for f in _task_files:
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
        created = str(data.get("created_at")) if data.get("created_at") else None
        age_days = None
        if created:
            try:
                age_days = (TODAY - date.fromisoformat(created[:10])).days
            except Exception:
                age_days = None
        tasks.append({
            "id":           data.get("id"),
            "title":        data.get("title", ""),
            "owner":        data.get("owner"),
            "status":       data.get("status", "IN_PROGRESS"),
            "priority":     data.get("priority", "MEDIUM"),
            "created_at":   created,
            # `closed_at` is a synonym used by ~35 legacy tasks; normalize both to
            # completed_at so close-date logic (latest-completed, closed-today) sees them.
            "completed_at": (lambda v: str(v) if v else None)(data.get("completed_at") or data.get("closed_at")),
            "depends_on":   data.get("depends_on") or [],
            "blocks":       data.get("blocks") or [],
            "category_id":  data.get("category_id"),
            "blocker":      data.get("blocker"),
            "close_reason": data.get("close_reason"),
            "summary":      (data.get("summary") or "").strip(),
            # ★ new fields (all optional; safe defaults preserve old behavior)
            "work_type":    (data.get("work_type") or "execution").strip().lower(),
            "drift_ack":    (str(data.get("drift_ack")).strip() if data.get("drift_ack") else None),
            "reopened_at":  str(data.get("reopened_at")) if data.get("reopened_at") else None,
            "age_days":     age_days,
            # ★ CC Agent review notes — surface near the task on the board
            "cc_comments":  _norm_cc_comments(data.get("cc_comments")),
            # ★ roadmap-impacting return → must get a CC Agent review before CLOSE
            "roadmap_impact": bool(data.get("roadmap_impact")),
            "cc_reviewed":  (str(data.get("cc_reviewed")) if data.get("cc_reviewed") else None),
            # ★ Banked Asset — a proven program parked (not launched). Stays visible
            # on the roadmap forever, even after the task CLOSES (≠ in-flight work).
            "banked_asset": (data.get("banked_asset")
                             if isinstance(data.get("banked_asset"), dict) else None),
            # ★ deferred — explicitly parked work. Stays open/visible in Pending,
            # but is excluded from the next_action BLOCKED rung so a deliberately
            # shelved task can't masquerade as "what to do next".
            "deferred":     bool(data.get("deferred")),
        })
    tasks.sort(key=lambda t: (TASK_ORDER.get(t["status"], 9),
                              PRI_ORDER.get(t["priority"], 9),
                              t["id"]))
    return tasks, unparseable


# ── Decision registry ─────────────────────────────────────────────────────────
def load_decisions():
    data = read_json(DECISIONS_FILE, default=[])
    return data if isinstance(data, list) else []


# ── Strategy (P1–P5 checkpoints) ──────────────────────────────────────────────
def load_strategy():
    """Load strategy.json. Returns {} on any read/parse failure so the dashboard
    degrades gracefully when the file is absent (fresh installs, CI environments)."""
    data = read_json(STRATEGY_FILE, default={})
    return data if isinstance(data, dict) else {}


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
    # ★② Tasks whose open-state-with-deliverable is KNOWN-GOOD and should not fire
    # CLOSURE_DRIFT: an operator `drift_ack:` reason, or a `reopened_at:` (the
    # deliverable exists but was deliberately invalidated — e.g. cheese run_001
    # reopened on the trans-fat bug). These are surfaced separately as `acknowledged`.
    ack_ids = {t["id"] for t in tasks if t.get("drift_ack") or t.get("reopened_at")}

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
        if status not in DELIVERED_STATUSES and tid in returns and tid not in ack_ids:
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
def compute_alerts(tasks, decisions, categories, returns_ids=None):
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

    # Capacity — PER-OWNER WIP (★ kanban per-column limit). RED only when a single
    # agent is overloaded; N agents each carrying one task is healthy flow, not a jam.
    over = owners_over_wip(tasks)
    if over:
        detail = ", ".join(f"{o} ({n})" for o, n in sorted(over.items()))
        add("CAPACITY_EXCEEDED", "CRITICAL",
            f"{len(over)} owner(s) over the per-owner WIP limit of {OWNER_WIP_LIMIT}: {detail}",
            resolution="Have the overloaded owner finish or hand off a task before taking new work.")

    # Stale task — IN_PROGRESS too long with no deliverable yet (★⑥ silent stall).
    for t in tasks:
        if t["status"] == "IN_PROGRESS" and (t.get("age_days") or 0) > STALE_TASK_DAYS \
                and t["id"] not in (returns_ids or set()):
            add("STALE_TASK", "MEDIUM",
                f"{t['id']}: IN_PROGRESS {t['age_days']} days with no deliverable yet — "
                f"confirm it is moving or re-scope",
                related_task=t["id"],
                resolution="Land a deliverable, or move to BLOCKED/RETURNED with a reason.")

    # Blocked tasks
    for t in tasks:
        if t["status"] == "BLOCKED":
            add("BLOCKED_TASK", "HIGH",
                f"{t['id']}: {t.get('blocker') or 'reason not specified'}",
                related_task=t["id"],
                resolution="Resolve the blocker, then set status to IN_PROGRESS.")

    # Returned with roadmap implications, not yet reviewed by CC Agent.
    # Surfaces every roadmap-impacting return so CC review happens before CLOSE.
    for t in tasks:
        if t["status"] in ("RETURNED", "CHANGES_REQUESTED") \
                and t.get("roadmap_impact") and not t.get("cc_reviewed"):
            add("ROADMAP_REVIEW", "HIGH",
                f"{t['id']}: returned with roadmap implications — CC Agent review needed before CLOSE",
                related_task=t["id"],
                resolution="Invoke CC Agent: assess roadmap impact, add cc_comments, set "
                           "cc_reviewed: <date> in the task frontmatter, regenerate.")

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


# ── Dependency graph + critical path (★③) ─────────────────────────────────────
def _forward_edges(tasks, by_id):
    """A -> B means 'A blocks B' (B cannot proceed until A is done). Built from
    both `blocks` (A.blocks=[B]) and the inverse of `depends_on` (B.depends_on=[A])."""
    fwd = {t["id"]: set() for t in tasks}
    for t in tasks:
        for b in (t.get("blocks") or []):
            if b in by_id:
                fwd[t["id"]].add(b)
        for d in (t.get("depends_on") or []):
            if d in by_id:
                fwd.setdefault(d, set()).add(t["id"])
    return fwd


def compute_critical_path(tasks):
    """Derives what today had to be traced by hand: which open task unblocks the
    most downstream work, and the longest blocking chain. Feeds next-action ranking."""
    by_id    = {t["id"]: t for t in tasks}
    open_ids = {t["id"] for t in tasks if t["status"] in OPEN_STATUSES}
    fwd      = _forward_edges(tasks, by_id)

    def downstream(tid):
        seen, stack = set(), [tid]
        while stack:
            cur = stack.pop()
            for nxt in fwd.get(cur, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen - {tid}

    unblocks = {tid: sorted(d for d in downstream(tid) if d in open_ids) for tid in open_ids}

    def longest(tid, path):
        best = [tid]
        for nxt in fwd.get(tid, ()):
            if nxt in open_ids and nxt not in path:
                cand = [tid] + longest(nxt, path | {tid})
                if len(cand) > len(best):
                    best = cand
        return best

    chains = [longest(tid, set()) for tid in open_ids] or [[]]
    longest_chain = max(chains, key=len)
    top = sorted(((tid, unblocks[tid]) for tid in open_ids if unblocks[tid]),
                 key=lambda kv: (-len(kv[1]), kv[0]))[:5]
    return {
        "longest_chain": longest_chain if len(longest_chain) > 1 else [],
        "top_unblockers": [{"task_id": tid, "unblocks_count": len(u), "unblocks": u}
                           for tid, u in top],
        "_unblocks_by_id": unblocks,   # consumed by next-action; stripped before output
    }


# ── Next Action (the single most important "what do I do now") ────────────────
def _pick(cands):
    """Highest priority, then lowest task id, deterministic."""
    return sorted(cands, key=lambda t: (PRI_ORDER.get(t.get("priority"), 9), t["id"]))[0]


# An ancestor in one of these states is something you can act on to clear the
# chain: do the work / rework it / review-and-accept it. CLOSED is satisfied;
# BLOCKED is itself stuck (we walk THROUGH it, never recommend it).
_ACTIONABLE_ROOT = ("IN_PROGRESS", "CHANGES_REQUESTED", "RETURNED")


def _blocking_root(t, by_id, seen=None):
    """★① Walk depends_on to the deepest UNSATISFIED, ACTIONABLE ancestor — the
    task you actually do to clear the chain. CLOSED deps are satisfied (skipped);
    a BLOCKED dep is itself stuck so we keep walking through it. Returns the root
    actionable task, or None when the blocker is a decision / external."""
    seen = seen if seen is not None else set()
    for dep_id in (t.get("depends_on") or []):
        if dep_id in seen:
            continue
        seen.add(dep_id)
        dep = by_id.get(dep_id)
        if not dep or dep["status"] == "CLOSED":
            continue
        deeper = _blocking_root(dep, by_id, seen)
        if deeper:
            return deeper
        if dep["status"] in _ACTIONABLE_ROOT:
            return dep
    return None


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


def compute_next_action(tasks, decisions, categories, critical=None):
    """Answer 'what should I do next?' via a fixed priority ladder (Registry
       Protocol v1 states):
       1. BLOCKED task -> recommend its ROOT UNBLOCKER (★①), not the blocked task
          itself; only surface the blocked task when nothing actionable unblocks it
          (genuine decision/external wait).
       2. CHANGES_REQUESTED task (rework the Controller asked for)
       3. IN_PROGRESS task blocking a launch (category not yet LIVE)
       4. highest-priority IN_PROGRESS task (tie-broken by how much it unblocks)
       5. RETURNED task awaiting the Controller's review/acceptance
    """
    name_by_id = {c["id"]: c["name_en"] for c in categories}
    not_live   = {c["id"] for c in categories if c["launch"]["status"] != "LIVE"}
    by_id      = {t["id"]: t for t in tasks}
    open_tasks = [t for t in tasks if t["status"] in OPEN_STATUSES]
    unblocks_by_id = (critical or {}).get("_unblocks_by_id", {})

    # 1. Blocked tasks — walk to the actionable root that clears the chain.
    #    `deferred` tasks are deliberately parked: still visible in Pending, but they
    #    do not compete to be the recommended NEXT action.
    blocked = [t for t in open_tasks if t["status"] == "BLOCKED" and not t.get("deferred")]
    if blocked:
        t = _pick(blocked)
        root = _blocking_root(t, by_id)
        if root and root["id"] != t["id"]:
            title = (t["title"][:48] + "…") if len(t["title"]) > 48 else t["title"]
            verb = ("review/accept it" if root["status"] == "RETURNED"
                    else "rework it" if root["status"] == "CHANGES_REQUESTED"
                    else "do this")
            return _build_next(
                root, f"Root unblocker for {t['id']} ({title}) — {verb} to clear the chain.",
                categories, default_unblocks=t["id"])
        reason = "Blocked — " + (t.get("blocker") or "waiting on a decision / external unblock")
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

    # 4. Highest-priority in-progress task; among equals, the one that unblocks most.
    if inprog:
        t = sorted(inprog, key=lambda x: (PRI_ORDER.get(x.get("priority"), 9),
                                          -len(unblocks_by_id.get(x["id"], [])),
                                          x["id"]))[0]
        n = len(unblocks_by_id.get(t["id"], []))
        why = "Currently in progress — finish this first."
        if n:
            why = f"Currently in progress and unblocks {n} downstream task(s) — finish this first."
        return _build_next(t, why, categories)

    # 5. Returned work awaiting the Controller's review/acceptance
    returned = [t for t in open_tasks if t["status"] == "RETURNED"]
    if returned:
        t = _pick(returned)
        return _build_next(t, "Returned — awaiting your review/acceptance.", categories)

    return None


def real_wip(tasks):
    """★④ Hands-on-keyboard work in flight: IN_PROGRESS minus coordination/decision
    tasks (which are open but not execution capacity) minus BLOCKED (not IN_PROGRESS
    anyway). This is the number worth managing against capacity — a raw 'active'
    count that lumps in umbrellas and pending decisions reads RED for the wrong reason."""
    return [t for t in tasks
            if t["status"] == "IN_PROGRESS" and t.get("work_type", "execution") in WIP_WORK_TYPES]


def wip_by_owner(tasks):
    """★ Per-owner execution load — the kanban per-column WIP view. {owner: count}."""
    counts = {}
    for t in real_wip(tasks):
        o = t.get("owner") or "—"
        counts[o] = counts.get(o, 0) + 1
    return counts


def owners_over_wip(tasks):
    """Owners exceeding OWNER_WIP_LIMIT — the only true capacity bottleneck."""
    return {o: n for o, n in wip_by_owner(tasks).items() if n > OWNER_WIP_LIMIT}


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
    wip = real_wip(tasks)
    s["wip"] = len(wip)                       # ★④ true execution load (global)
    s["wip_task_ids"] = [t["id"] for t in wip]
    s["wip_by_owner"]  = wip_by_owner(tasks)  # ★ per-owner kanban WIP
    s["owner_wip_limit"] = OWNER_WIP_LIMIT
    s["wip_over_limit"]  = sorted(owners_over_wip(tasks))
    return s


# ── Executive (computed) ──────────────────────────────────────────────────────
def compute_executive(tasks, decisions, alerts):
    open_alerts = [a for a in alerts if a["status"] == "OPEN"]
    has_critical = any(a["severity"] == "CRITICAL" for a in open_alerts)
    has_high     = any(a["severity"] == "HIGH" for a in open_alerts)
    active = [t for t in tasks if t["status"] in ACTIVE_STATUSES]

    # Health threshold uses PER-OWNER WIP (★), consistent with the capacity alert.
    if has_critical or owners_over_wip(tasks):
        health = "RED"
    elif has_high:
        health = "YELLOW"
    else:
        health = "GREEN"

    completed = [t for t in tasks if t["status"] == "CLOSED" and t.get("completed_at")]
    # Tie-break by natural id so the latest same-date batch wins (not the lowest id).
    latest = max(completed, key=lambda t: (t["completed_at"], id_sortkey(t["id"])), default=None)

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


def closure_drift_acks(tasks, returns):
    """★② Known-good open-with-deliverable cases, suppressed from CLOSURE_DRIFT.

    Returns [{id, reason}] so the dashboard can SHOW that a drift was consciously
    acknowledged (not silently hidden). 'clean' stays true when only acks remain."""
    out = []
    for t in tasks:
        if t["status"] in DELIVERED_STATUSES or t["id"] not in returns:
            continue
        reason = t.get("drift_ack")
        if not reason and t.get("reopened_at"):
            reason = (f"reopened {t['reopened_at']} — deliverable exists but was "
                      f"deliberately invalidated; BLOCKED is the truthful status")
        if reason:
            out.append({"id": t["id"], "reason": reason})
    return out


def summarize_drift(drift_alerts, acknowledged=None):
    by_type = {dt: [a["related_task"] for a in drift_alerts if a["type"] == dt]
               for dt in DRIFT_TYPES}
    return {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "clean": len(drift_alerts) == 0,
        "counts": {dt: len(by_type[dt]) for dt in DRIFT_TYPES},
        "phantom_tasks": [t for t in by_type["PHANTOM_TASK"] if t],
        "closure_drift_tasks": [t for t in by_type["CLOSURE_DRIFT"] if t],
        "registry_unparseable": [t for t in by_type["REGISTRY_UNPARSEABLE"] if t],
        # ★② consciously-acknowledged drift (does NOT count against 'clean')
        "acknowledged": acknowledged or [],
    }


# ── Category state machine (★⑤ first-class launch view) ───────────────────────
def compute_category_state(categories, tasks):
    """Compact 'what's left to launch?' rollup — each non-live category linked to
    the task that owns its next move (highest-priority open task tagged to it)."""
    by_id = {t["id"]: t for t in tasks}
    rows = []
    for c in categories:
        open_work = c.get("open_work", [])
        blocking = None
        cand = sorted((by_id[i] for i in open_work if i in by_id),
                      key=lambda t: (PRI_ORDER.get(t.get("priority"), 9), t["id"]))
        if cand:
            blocking = cand[0]["id"]
        rows.append({
            "id":            c["id"],
            "name_he":       c.get("name_he"),
            "launch":        c["launch"]["status"],
            "bsip2":         c["bsip2"]["status"],
            "dataset":       c["frontend_dataset"]["status"],
            "website":       c["website"]["status"],
            "blocking_task": blocking,
        })
    return rows


# ── Banked Assets (proven-but-not-launched programs) ──────────────────────────
def compute_banked_assets(tasks):
    """Persistent roadmap view of proven programs that were BANKED, not launched
    (e.g. SIE/TASK-171). Derived from the authoritative registry: any task whose
    frontmatter carries a `banked_asset:` block. Unlike in-flight work these never
    expire from the roadmap — a closed task would otherwise vanish from every
    bucket, hiding a strategic asset. Ordered newest-banked first."""
    out = []
    for t in tasks:
        ba = t.get("banked_asset")
        if not ba:
            continue
        out.append({
            "task_id":      t["id"],
            "title":        t["title"],
            "owner":        t.get("owner"),
            "status":       t["status"],            # typically CLOSED
            "banked_at":    str(ba.get("banked_at")) if ba.get("banked_at") else t.get("completed_at"),
            "one_liner":    (ba.get("one_liner") or "").strip(),
            "why_parked":   (ba.get("why_parked") or "").strip(),
            "revival_gate": (ba.get("revival_gate") or "").strip(),
            "reference":    (ba.get("reference") or "").strip(),
        })
    out.sort(key=lambda a: (a["banked_at"] or ""), reverse=True)
    return out


# ── Lean live view + closed-task trimming (token efficiency ①②③) ──────────────
def _trim_closed(tasks):
    """Main JSON keeps only what the task board renders for CLOSED rows; the full
    closed record (with summary) lives in command_center_archive.json."""
    out = []
    for t in tasks:
        if t["status"] == "CLOSED":
            out.append({k: v for k, v in t.items() if k not in CLOSED_DROP_FIELDS})
        else:
            out.append(t)
    return out


def _live_view(dashboard):
    """~6-8KB read path: everything an agent needs to answer 'what's the state?'
    without parsing 92 closed-task summaries. Open tasks only, full fidelity.

    CC comments are compacted to a *sticker* here (`cc`: the list of flags, e.g.
    ["verify","fyi"]) — enough to signal "this task has a CC note, go look", at a
    few tokens instead of the full prose. The full text lives in command_center.json
    (what the board renders) and the source TASK-*.md. Keeps the per-session agent
    read path lean."""
    open_tasks = []
    for t in dashboard["tasks"]:
        if t["status"] == "CLOSED":
            continue
        lt = dict(t)                       # copy — never strip prose from the full board
        cc = lt.pop("cc_comments", None)
        if cc:
            lt["cc"] = [c["flag"] for c in cc]
        open_tasks.append(lt)
    return {
        "_generated": True,
        "_note": "Lean live view. Full board: command_center.json · closed detail: command_center_archive.json",
        "meta":          dashboard["meta"],
        "executive":     dashboard["executive"],
        "next_action":   dashboard["next_action"],
        "task_summary":  dashboard["task_summary"],
        "critical_path": dashboard["critical_path"],
        "drift":         dashboard["drift"],
        "category_state": dashboard["category_state"],
        "banked_assets": dashboard["banked_assets"],
        "strategy":      dashboard["strategy"],
        "open_tasks":    open_tasks,
        "alerts":        [a for a in dashboard["alerts"] if a["status"] == "OPEN"],
    }


# ── Morning digest (★⑦) ───────────────────────────────────────────────────────
def emit_digest(dashboard):
    ex, ts = dashboard["executive"], dashboard["task_summary"]
    cp, dr = dashboard["critical_path"], dashboard["drift"]
    lines = []
    lines.append(f"# Command Center — Morning Digest ({TODAY.isoformat()})")
    lines.append("")
    wbo = ts.get("wip_by_owner", {})
    wmax = max(wbo.values(), default=0)
    owners = ", ".join(f"{o}:{n}" for o, n in sorted(wbo.items())) or "none"
    lines.append(f"Health: {ex['system_health']} · WIP {ts['wip']} "
                 f"(peak {wmax}/{OWNER_WIP_LIMIT} per owner — {owners}) · "
                 f"active {ts['active']} ({ts['in_progress']} in-progress, {ts['blocked']} blocked, "
                 f"{ts['returned']} returned) · closed {ts['closed']}")
    na = dashboard.get("next_action")
    if na:
        lines.append(f"NEXT: {na['task_id']} ({na['owner']}) — {na['reason']}  → unblocks {na['unblocks']}")
    lines.append("")
    if cp.get("longest_chain"):
        lines.append("Critical chain: " + " → ".join(cp["longest_chain"]))
    if cp.get("top_unblockers"):
        lines.append("Top unblockers: " + ", ".join(
            f"{u['task_id']} (frees {u['unblocks_count']})" for u in cp["top_unblockers"]))
    lines.append("")
    lines.append("## Open work")
    for t in dashboard["tasks"]:
        if t["status"] == "CLOSED":
            continue
        wt = "" if t.get("work_type", "execution") == "execution" else f" [{t['work_type']}]"
        lines.append(f"  {t['status']:<8} {t['priority']:<8} {t['id']:<10} {t['owner'] or '—':<14}{wt} {t['title'][:70]}")
        for c in t.get("cc_comments", []):
            tag = "CC" if c["flag"] == "fyi" else f"CC/{c['flag'].upper()}"
            lines.append(f"        ↳ {tag}: {c['text'][:96]}")
    banked = dashboard.get("banked_assets", [])
    if banked:
        lines.append("")
        lines.append(f"## Banked assets ({len(banked)} — proven, not launched)")
        for b in banked:
            lines.append(f"  {b['task_id']:<10} {b['one_liner'][:84]}")
            if b.get("revival_gate"):
                lines.append(f"        ↳ revive when: {b['revival_gate'][:88]}")
    closed_today = [t for t in dashboard["tasks"]
                    if t["status"] == "CLOSED" and t.get("completed_at") == TODAY.isoformat()]
    if closed_today:
        lines.append("")
        lines.append(f"## Closed today ({len(closed_today)})")
        for t in closed_today:
            lines.append(f"  {t['id']:<10} {t['title'][:70]}")
    lines.append("")
    issues = dr["counts"]["PHANTOM_TASK"] + dr["counts"]["CLOSURE_DRIFT"] + dr["counts"]["REGISTRY_UNPARSEABLE"]
    lines.append(f"## Registry: {'clean' if issues == 0 else str(issues)+' issue(s)'}"
                 + (f" · {len(dr.get('acknowledged', []))} acknowledged" if dr.get("acknowledged") else ""))
    for a in dr.get("acknowledged", []):
        lines.append(f"  ack {a['id']}: {a['reason'][:90]}")
    for tid in dr.get("phantom_tasks", []):
        lines.append(f"  PHANTOM {tid}")
    for tid in dr.get("closure_drift_tasks", []):
        lines.append(f"  CLOSURE_DRIFT {tid}")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Console-safe Unicode (digest uses → · …); Windows default is cp1252.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    tasks, unparseable = load_tasks()
    decisions   = load_decisions()
    strategy    = load_strategy()
    categories  = derive_categories(tasks)

    # v3 self-healing: artifact-derived task returns + drift detection.
    # registry_ids includes unparseable files (they exist on disk) so a prose-only
    # task file is never mis-flagged PHANTOM — it gets REGISTRY_UNPARSEABLE instead.
    registry_ids = {t["id"] for t in tasks} | {u["id"] for u in unparseable}
    returns      = scan_task_returns()
    returns_ids  = set(returns.keys())

    operational  = compute_alerts(tasks, decisions, categories, returns_ids)
    # ref_mtime=None: a fresh regenerate is by definition not a stale snapshot.
    drift        = build_drift_alerts(tasks, returns, registry_ids, unparseable, ref_mtime=None)
    alerts       = finalize_alerts(operational + drift)

    acknowledged   = closure_drift_acks(tasks, returns)             # ★②
    critical_path  = compute_critical_path(tasks)                   # ★③
    executive    = compute_executive(tasks, decisions, alerts)  # sees drift alerts
    next_action  = compute_next_action(tasks, decisions, categories, critical_path)
    task_summary = compute_task_summary(tasks)
    category_state = compute_category_state(categories, tasks)      # ★⑤
    banked_assets  = compute_banked_assets(tasks)                   # ★ persistent
    critical_path.pop("_unblocks_by_id", None)  # internal aid; not serialized

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
            "owner_wip_limit": OWNER_WIP_LIMIT,
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
        "critical_path": critical_path,       # ★③
        "category_state": category_state,     # ★⑤
        "banked_assets": banked_assets,       # ★ proven-but-not-launched, persistent
        "strategy": strategy,                 # P1–P5 two-month checkpoint plan
        "drift": summarize_drift(drift, acknowledged),
        "tasks": tasks,
        "decisions": decisions,
        "categories": categories,
        "alerts": alerts,
    }

    if "--digest" in sys.argv:
        print(emit_digest(dashboard))
        return

    # Main board: trim CLOSED summaries (token ①); full closed detail -> archive (③);
    # lean live view (②). The HTML reads command_center.json and never touches a
    # closed task's summary, so trimming is invisible to the renderer.
    main_doc = dict(dashboard, tasks=_trim_closed(dashboard["tasks"]))
    OUTPUT_FILE.write_text(
        json.dumps(main_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ARCHIVE_FILE.write_text(
        json.dumps({"_generated": True, "generated_at": now_iso,
                    "closed_tasks": [t for t in dashboard["tasks"] if t["status"] == "CLOSED"]},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LIVE_FILE.write_text(
        json.dumps(_live_view(dashboard), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    open_alerts = [a for a in alerts if a["status"] == "OPEN"]
    active = [t for t in tasks if t["status"] in ACTIVE_STATUSES]
    print("command_center.json generated")
    print(f"  health:     {executive['system_health']}")
    if next_action:
        print(f"  NEXT ACTION: {next_action['task_id']} — {next_action['title']} "
              f"({next_action['owner']})  -> unblocks: {next_action['unblocks']}")
    else:
        print("  NEXT ACTION: none — no open work")
    wbo = task_summary.get("wip_by_owner", {})
    print(f"  tasks:      {len(tasks)} total | WIP={task_summary['wip']} "
          f"(per-owner peak {max(wbo.values(), default=0)}/{OWNER_WIP_LIMIT}) "
          f"active={task_summary['active']} "
          f"in_progress={task_summary['in_progress']} blocked={task_summary['blocked']} "
          f"returned={task_summary['returned']} changes={task_summary['changes_requested']} "
          f"closed={task_summary['closed']}")
    if critical_path.get("longest_chain"):
        print("  crit chain: " + " -> ".join(critical_path["longest_chain"]))
    if critical_path.get("top_unblockers"):
        print("  unblockers: " + ", ".join(
            f"{u['task_id']}(+{u['unblocks_count']})" for u in critical_path["top_unblockers"]))
    if acknowledged:
        print(f"  drift-ack:  {len(acknowledged)} -> " + ", ".join(a["id"] for a in acknowledged))
    try:
        kb = lambda p: f"{p.stat().st_size/1024:.0f}KB"
        print(f"  files:      command_center.json={kb(OUTPUT_FILE)}  "
              f"live={kb(LIVE_FILE)}  archive={kb(ARCHIVE_FILE)}")
    except OSError:
        pass
    print(f"  categories: {len(categories)}")
    if banked_assets:
        print(f"  banked:     {len(banked_assets)} proven asset(s) -> "
              + ", ".join(f"{b['task_id']}" for b in banked_assets))
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
