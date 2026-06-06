#!/usr/bin/env python3
"""
Bari Command Center — freshness-guaranteed server + local task actions
======================================================================

Use this INSTEAD of `python -m http.server` to view the dashboard. It runs the
drift/freshness check (check_drift.py) before serving, so the served snapshot's
`meta.stale` flag is current the moment the page loads — the operator can never
open a stale dashboard without the red banner appearing. The page also re-checks
itself every 60s (see command_center_v4.html), so leaving a tab open stays honest.

Usage:
    cd C:\\Bari\\05_command_center
    python serve.py            # serves on 127.0.0.1:8080
    python serve.py 9000       # custom port
    open http://localhost:8080/command_center.html   (task board)  ·  /seo.html (SEO)

Note: a stale result is surfaced as a banner, not auto-fixed — fixing means a
full regenerate (python generate_dashboard.py), which is a deliberate action.

──────────────────────────────────────────────────────────────────────────────
LOCAL TASK ACTIONS (TASK-124)
──────────────────────────────────────────────────────────────────────────────
This server also exposes ONE local-only mutation endpoint so the Central
Controller can change a task's state from the dashboard without prompting Claude:

    POST /api/action   {"task_id": "TASK-120", "action": "accept", "reason": null}

Task shapes (derived from the id, no extra field):
    OBJECTIVE  TASK-125   — the goal. Only `close` (from any open state, reason
                            required). Closing it CASCADES: every open sub-task closes too.
    SUB-TASK   TASK-125A  — the work. Full lifecycle below.

Sub-task actions (action → legal source state(s) → target):
    mark_returned   IN_PROGRESS                              → RETURNED
    accept          RETURNED                                 → CLOSED  (+ completed_at)
    request_changes RETURNED                                 → CHANGES_REQUESTED  (reason)
    block           IN_PROGRESS                              → BLOCKED  (reason)
    resume          BLOCKED | CHANGES_REQUESTED              → IN_PROGRESS  (clears blocker/change note)
    close           IN_PROGRESS | CHANGES_REQUESTED | BLOCKED → CLOSED  (+ completed_at, reason)

On each click the server: validates the task id, the current state, and the
requested transition; rewrites ONLY the YAML frontmatter of tasks/TASK-XXX.md
(the registry stays the source of truth — the dashboard is still derived);
appends to task_action_audit.log; runs generate_dashboard.py; the page then
re-fetches command_center.json. The registry / lifecycle states / task-creation
protocol / Bari product code are never touched. No DB, no cloud, no WebSocket.

The endpoint binds to 127.0.0.1 only — it is a single-operator local tool.

──────────────────────────────────────────────────────────────────────────────
TOM'S PRIVATE LOCAL STORE (TASK-186, owner decisions 2026-06-05)
──────────────────────────────────────────────────────────────────────────────
Two more local-only endpoints back Tom's personal Chief-of-Staff surface:

    GET  /api/personal_store           → the whole private doc ({} → defaults)
    POST /api/personal_store {op:...}   → upsert/delete one item

ops: todo_add / todo_toggle / todo_remove (Tom's OWN to-dos, NOT TASK-NNN) ·
     note_set (Tom's private per-task note, distinct from CC's cc_comments) ·
     fault_dismiss / fault_restore (soft "it's fine" — quiets a warning on Tom's
     board only, NO registry change, reversible).

These persist to ~/.bari/cc_personal.json — the same git-IGNORED dir as the
Google token, OUTSIDE the C:\\Bari repo. Personal data is NEVER written to a
tracked file and NEVER to Gmail. Real task state changes still go through
/api/action (which rewrites the registry); the personal store is purely Tom's.
"""

import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import check_drift  # importing does not run it (guarded by __main__)

HERE = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# ── Task-action config ────────────────────────────────────────────────────────
BARI_ROOT = Path(r"C:\Bari")
# Make `integrations.clients.google_workspace` importable (repo root on sys.path).
if str(BARI_ROOT) not in sys.path:
    sys.path.insert(0, str(BARI_ROOT))
TASKS_DIR = BARI_ROOT / "tasks"
GENERATOR = HERE / "generate_dashboard.py"
AUDIT_LOG = HERE / "task_action_audit.log"

# ── Tom's PRIVATE local store (TASK-186, owner decisions 2026-06-05) ────────────
# Tom's own to-dos, his private per-task notes, and the ids of faults he has
# soft-dismissed ("it's fine"). HARD PRIVACY CONTRACT: this is personal and lives
# in ~/.bari/ (the same git-IGNORED dir as the Google token) — NEVER in a
# git-tracked file, NEVER in Gmail. command_center.json is tracked, so personal
# data must never touch it. The dir is outside the C:\Bari repo entirely, so it
# can never be staged.
PERSONAL_STORE = Path.home() / ".bari" / "cc_personal.json"
PERSONAL_DEFAULT = {"todos": [], "task_notes": {}, "dismissed_faults": []}

TASK_ID_RE = re.compile(r"^TASK-\d+[A-Z]*$")   # objective (TASK-125) or sub-task (TASK-125A)
OBJECTIVE_RE = re.compile(r"^TASK-\d+$")        # no letter suffix = a top-level objective
SUBTASK_RE = re.compile(r"^TASK-\d+[A-Z]+$")    # trailing letter(s) = a sub-task of TASK-<n>

# action -> legal source state(s) + target + whether a reason is mandatory.
# This map is the whole authorization model: an action is only ever applied when
# the task's CURRENT status is one of `from`. `from` is a tuple, so one button can
# legally fire from several states (e.g. Close from IN_PROGRESS/CHANGES/BLOCKED)
# while still being rejected from any state not listed.
ACTIONS = {
    "mark_returned":   {"from": ("IN_PROGRESS",),                                 "to": "RETURNED",          "reason": False},
    "accept":          {"from": ("RETURNED",),                                    "to": "CLOSED",            "reason": False},
    "request_changes": {"from": ("RETURNED",),                                    "to": "CHANGES_REQUESTED", "reason": True},
    "block":           {"from": ("IN_PROGRESS",),                                 "to": "BLOCKED",           "reason": True},
    "resume":          {"from": ("BLOCKED", "CHANGES_REQUESTED"),                 "to": "IN_PROGRESS",       "reason": False},
    "close":           {"from": ("IN_PROGRESS", "CHANGES_REQUESTED", "BLOCKED"),  "to": "CLOSED",            "reason": True},
}


# ── Frontmatter helpers (line-based: touch ONLY the keys we change) ────────────
# We deliberately do NOT yaml.load/dump the frontmatter — that would reorder keys
# and flatten the `summary: >` block. We edit individual top-level key lines so
# everything else (and the markdown body) is byte-for-byte preserved.
def _split_frontmatter(text):
    """(opening_lines, frontmatter_lines, rest_lines) or None.

    opening = ['---\\n']; frontmatter = the lines between the fences;
    rest = the closing '---' line plus the whole markdown body."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[:1], lines[1:i], lines[i:]
    return None


def _status_of(text):
    """Current top-level `status:` value, or None if no parseable frontmatter."""
    split = _split_frontmatter(text)
    if not split:
        return None
    for ln in split[1]:
        m = re.match(r"^status:\s*(\S+)", ln)
        if m:
            return m.group(1)
    return None


def _set_key(fm, key, line):
    for idx, ln in enumerate(fm):
        if re.match(rf"^{re.escape(key)}:", ln):
            fm[idx] = line + "\n"
            return True
    return False


def _insert_after(fm, after_key, line):
    for idx, ln in enumerate(fm):
        if re.match(rf"^{re.escape(after_key)}:", ln):
            fm.insert(idx + 1, line + "\n")
            return True
    return False


def _remove_key(fm, key):
    before = len(fm)
    fm[:] = [ln for ln in fm if not re.match(rf"^{re.escape(key)}:", ln)]
    return len(fm) != before


def _upsert(fm, key, line, after_keys):
    """Set the key in place if present; else insert after the first available
    anchor key; else append. Keeps additions next to related fields."""
    if _set_key(fm, key, line):
        return
    for ak in after_keys:
        if _insert_after(fm, ak, line):
            return
    fm.append(line + "\n")


def _apply_transition(fm, to_state, reason):
    """Mutate the frontmatter line list in place for the target state.

    Keyed on the TARGET state, so it is correct no matter which source state the
    action came from (Close from IN_PROGRESS/CHANGES/BLOCKED all land here as
    CLOSED; Resume from BLOCKED/CHANGES both land as IN_PROGRESS)."""
    _upsert(fm, "status", f"status: {to_state}", ["id"])
    if to_state == "CLOSED":
        # completed_at sits right after created_at by registry convention.
        _upsert(fm, "completed_at", f"completed_at: {date.today().isoformat()}",
                ["created_at", "status", "id"])
        # accept carries no reason; close carries one — persist it when present.
        if reason:
            _upsert(fm, "close_reason", f"close_reason: {json.dumps(reason)}",
                    ["completed_at", "status", "id"])
    elif to_state == "BLOCKED":
        # `blocker` is the field generate_dashboard.py already surfaces.
        _upsert(fm, "blocker", f"blocker: {json.dumps(reason)}", ["status", "id"])
    elif to_state == "CHANGES_REQUESTED":
        _upsert(fm, "change_request", f"change_request: {json.dumps(reason)}",
                ["status", "id"])
    elif to_state == "IN_PROGRESS":
        # back to active work — neither the block reason nor the change-request
        # note applies any more (resume can come from BLOCKED or CHANGES_REQUESTED).
        _remove_key(fm, "blocker")
        _remove_key(fm, "change_request")


def _audit(task_id, action, frm, to, reason):
    ts = datetime.now().isoformat(timespec="seconds")
    row = f"{ts}\t{task_id}\t{action}\t{frm}\t{to}\t{reason or '-'}\n"
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(row)


def _is_objective(tid):
    return bool(OBJECTIVE_RE.match(tid))


def _open_subtasks(objective_id):
    """Open (non-CLOSED) sub-tasks of an objective: TASK-125 -> TASK-125A/B/...
    Returns list of (sub_id, path, current_status)."""
    out = []
    pat = re.compile(rf"^{re.escape(objective_id)}[A-Z]+$")
    for f in TASKS_DIR.glob(f"{objective_id}[A-Z]*.md"):
        if not pat.match(f.stem):
            continue
        st = _status_of(f.read_text(encoding="utf-8"))
        if st and st != "CLOSED":
            out.append((f.stem, f, st))
    return sorted(out)


def _transition_file(path, to_state, reason):
    """Rewrite ONLY the frontmatter of a task file for the target state."""
    opening, fm, rest = _split_frontmatter(path.read_text(encoding="utf-8"))
    _apply_transition(fm, to_state, reason)
    path.write_text("".join(opening) + "".join(fm) + "".join(rest), encoding="utf-8")


def perform_action(task_id, action, reason):
    """Validate → rewrite frontmatter → audit → regenerate. Returns (code, body).

    Two shapes of task:
      • OBJECTIVE  (TASK-125)  — only `close` is allowed, from any open state, with
        a reason; closing it CASCADES to close every open sub-task.
      • SUB-TASK   (TASK-125A) — the full lifecycle (ACTIONS state machine).
    """
    if not task_id or not TASK_ID_RE.match(task_id):
        return 400, {"ok": False, "error": f"invalid task id: {task_id!r}"}
    path = TASKS_DIR / f"{task_id}.md"
    if not path.exists():
        return 404, {"ok": False, "error": f"no registry file tasks/{task_id}.md"}
    current = _status_of(path.read_text(encoding="utf-8"))
    if current is None:
        return 422, {"ok": False, "error": f"{task_id}: no parseable status in frontmatter"}

    cascaded = []
    if _is_objective(task_id):
        # Objectives carry no per-step lifecycle — they are the goal, not the work.
        if action != "close":
            return 409, {"ok": False,
                         "error": f"{task_id} is an objective — only 'close' is allowed; "
                                  f"manage the lifecycle on its sub-tasks (e.g. {task_id}A)."}
        if current == "CLOSED":
            return 409, {"ok": False, "error": f"{task_id} is already CLOSED"}
        reason = (reason or "").strip()
        if not reason:
            return 400, {"ok": False, "error": "closing an objective requires a reason"}
        _transition_file(path, "CLOSED", reason)
        _audit(task_id, "close", current, "CLOSED", reason)
        for sid, sf, sst in _open_subtasks(task_id):
            _transition_file(sf, "CLOSED", f"parent {task_id} closed")
            _audit(sid, "close", sst, "CLOSED", f"cascade: parent {task_id} closed ({reason})")
            cascaded.append(sid)
        to_state = "CLOSED"
    else:
        spec = ACTIONS.get(action)
        if not spec:
            return 400, {"ok": False, "error": f"unknown action: {action!r}"}
        if spec["reason"]:
            reason = (reason or "").strip()
            if not reason:
                return 400, {"ok": False, "error": f"action '{action}' requires a reason"}
        else:
            reason = None
        if current not in spec["from"]:
            allowed = " | ".join(spec["from"])
            return 409, {"ok": False,
                         "error": f"{task_id} is {current}; '{action}' is only allowed from {allowed}"}
        _transition_file(path, spec["to"], reason)
        _audit(task_id, action, current, spec["to"], reason)
        to_state = spec["to"]

    # re-derive the dashboard from the (now updated) registry — once, after all writes.
    gen = subprocess.run([sys.executable, str(GENERATOR)],
                         cwd=str(HERE), capture_output=True, text=True)
    if gen.returncode != 0:
        return 500, {"ok": False,
                     "error": "task updated, but generate_dashboard.py failed",
                     "detail": (gen.stderr or gen.stdout)[-600:]}

    body = {"ok": True, "task_id": task_id, "from": current, "to": to_state, "reason": reason}
    if cascaded:
        body["cascaded"] = cascaded
    return 200, body


# ── Personal layer (Gmail + Calendar) — LIVE, IN-MEMORY ONLY ──────────────────
# HARD PRIVACY CONTRACT: Tom's inbox/calendar content is personal and must NEVER
# be written to a git-tracked file. `command_center.json` IS tracked. So this
# endpoint reads the read-only google_workspace connector live, on each request,
# and returns it as a JSON HTTP response only — it never persists anything to
# disk. The page fetches /api/personal client-side and renders it in the browser.
# If the connector is not linked, it returns {connected:false, hint:...} so the
# page shows a calm "link your inbox" placeholder instead of an error.
#
# TIMEZONE: gw.calendar_day() buckets "today" in UTC, which can read 0 events
# wrongly. serve.py runs on Tom's machine, so we compute the day window in LOCAL
# time and pass local-tz day boundaries into gw.list_events() — "today" = Tom's
# today.
def _local_day_bounds(days: int = 1):
    """RFC3339 [start, end] for the local calendar day(s), with the local UTC
    offset, so the Google Calendar API buckets 'today' the way Tom sees it."""
    now = datetime.now().astimezone()          # local time, tz-aware
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=days)
    return start.isoformat(), end.isoformat()


def _calendar_day_local(gw, days: int = 1) -> dict:
    """gw.calendar_day(), but with the day window computed in LOCAL time."""
    time_min, time_max = _local_day_bounds(days)
    evts = gw.list_events(time_min, time_max)
    no_prep = [e.summary for e in evts
               if e.attendees >= 2 and not e.all_day and not e.description.strip()]
    return {
        "connected": True,
        "events": [e.as_dict() for e in evts],
        "count": len(evts),
        "conflicts": gw._conflicts(evts),
        "no_prep": no_prep,
        "day_window": {"start": time_min, "end": time_max},
    }


def personal_payload() -> dict:
    """Live, never-persisted Gmail+Calendar view for the board. Degrades calmly."""
    try:
        from integrations.clients import google_workspace as gw
    except Exception as e:
        return {"connected": False, "hint": f"connector unavailable: {e}"}
    if not gw.is_connected():
        s = gw.status()  # already returns {connected:false, hint:...}
        return s if isinstance(s, dict) else {"connected": False, "hint": "not linked"}
    try:
        # NOTE: do NOT call gw.status() here — it internally re-runs inbox_triage()
        # AND calendar_day(), which we already fetch below. Calling it would triple
        # the Gmail round-trips and make the board take ~a minute to paint.
        return {
            "connected": True,
            "inbox": gw.inbox_triage(),
            "calendar": _calendar_day_local(gw, days=1),
            "week": _calendar_day_local(gw, days=7),
            "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
    except Exception as e:
        # An auth/network hiccup is an honest "can't see your inbox right now",
        # never a silent empty and never a 500.
        return {"connected": True, "error": str(e),
                "hint": "Gmail/Calendar reachable but a read failed — try again."}


# ── Personal store I/O (Tom's private to-dos / notes / dismissed faults) ───────
# Read returns {} ({...defaults}) when the file is absent — a fresh board with no
# personal data is the normal first state, never an error. Writes are whole-file
# rewrites of a small JSON doc under ~/.bari/ (created on first write). We never
# touch the registry, the dashboard json, or Gmail from here.
def _read_personal_store() -> dict:
    try:
        if not PERSONAL_STORE.exists():
            return dict(PERSONAL_DEFAULT)
        data = json.loads(PERSONAL_STORE.read_text(encoding="utf-8") or "{}")
    except Exception:
        # A corrupt/unreadable store degrades to empty rather than 500-ing the board.
        return dict(PERSONAL_DEFAULT)
    if not isinstance(data, dict):
        return dict(PERSONAL_DEFAULT)
    # normalize shape so the client can rely on the three keys always existing
    data.setdefault("todos", [])
    data.setdefault("task_notes", {})
    data.setdefault("dismissed_faults", [])
    return data


def _write_personal_store(store: dict) -> None:
    PERSONAL_STORE.parent.mkdir(parents=True, exist_ok=True)
    PERSONAL_STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2),
                              encoding="utf-8")


def mutate_personal_store(payload: dict):
    """Upsert/delete one item in the private store. Returns (code, store).

    Operations (payload.op):
      todo_add      {text}                 → append a todo {id,text,done:false}
      todo_toggle   {id, done?}            → flip/set its done flag
      todo_remove   {id}                   → drop it
      note_set      {task_id, text}        → set/replace Tom's private note (''=clear)
      fault_dismiss {fault_id}             → add id to dismissed_faults (soft "it's fine")
      fault_restore {fault_id}             → remove it (un-quiet)
    Always returns the full, current store so the client re-renders from truth.
    """
    op = (payload or {}).get("op")
    store = _read_personal_store()
    if op == "todo_add":
        text = str(payload.get("text") or "").strip()
        if not text:
            return 400, {"ok": False, "error": "todo text is empty"}
        tid = f"td-{int(datetime.now().timestamp()*1000)}"
        store["todos"].append({"id": tid, "text": text, "done": False,
                               "created_at": datetime.now().isoformat(timespec="seconds")})
    elif op == "todo_toggle":
        tid = payload.get("id")
        hit = next((t for t in store["todos"] if t.get("id") == tid), None)
        if not hit:
            return 404, {"ok": False, "error": f"no todo {tid!r}"}
        hit["done"] = bool(payload["done"]) if "done" in payload else not hit.get("done")
    elif op == "todo_remove":
        tid = payload.get("id")
        store["todos"] = [t for t in store["todos"] if t.get("id") != tid]
    elif op == "note_set":
        task_id = str(payload.get("task_id") or "").strip()
        if not task_id:
            return 400, {"ok": False, "error": "note_set requires task_id"}
        text = str(payload.get("text") or "").strip()
        if text:
            store["task_notes"][task_id] = {
                "text": text,
                "updated_at": datetime.now().isoformat(timespec="seconds")}
        else:
            store["task_notes"].pop(task_id, None)   # empty text clears the note
    elif op == "fault_dismiss":
        fid = str(payload.get("fault_id") or "").strip()
        if not fid:
            return 400, {"ok": False, "error": "fault_dismiss requires fault_id"}
        if fid not in store["dismissed_faults"]:
            store["dismissed_faults"].append(fid)
    elif op == "fault_restore":
        fid = str(payload.get("fault_id") or "").strip()
        store["dismissed_faults"] = [f for f in store["dismissed_faults"] if f != fid]
    else:
        return 400, {"ok": False, "error": f"unknown op: {op!r}"}
    _write_personal_store(store)
    return 200, {"ok": True, "store": store}


# ── HTTP server: allow_reuse_address so a fresh `python serve.py` rebinds the
# port immediately after the previous one is stopped (no TIME_WAIT wait). This is
# what http.server.HTTPServer does; socketserver.TCPServer defaults it to False.
class Server(socketserver.TCPServer):
    allow_reuse_address = True


# ── HTTP handler: static files + the one mutation endpoint ────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    def _send_json(self, code, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        # /api/personal_store — Tom's PRIVATE local store (~/.bari/cc_personal.json).
        # Returns the whole small doc; {} → defaults. no-store: never cached.
        if self.path.split("?", 1)[0] == "/api/personal_store":
            try:
                store = _read_personal_store()
            except Exception as e:
                store = {"error": f"personal store read failed: {e}"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            data = json.dumps(store, ensure_ascii=False).encode("utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        # /api/personal — live, in-memory Gmail+Calendar. NEVER written to disk.
        if self.path.split("?", 1)[0] == "/api/personal":
            try:
                payload = personal_payload()
            except Exception as e:  # last-resort guard — never 500 the board
                payload = {"connected": False, "hint": f"personal layer error: {e}"}
            # no-store: personal data must never be cached to disk by a proxy/browser
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        # everything else = static files (the dashboard, json, etc.)
        super().do_GET()

    def do_POST(self):
        route = self.path.split("?", 1)[0]
        if route not in ("/api/action", "/api/personal_store"):
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except Exception as e:
            self._send_json(400, {"ok": False, "error": f"bad request body: {e}"})
            return
        # /api/personal_store — mutate Tom's PRIVATE local store. Never the registry.
        if route == "/api/personal_store":
            try:
                code, body = mutate_personal_store(payload)
            except Exception as e:
                code, body = 500, {"ok": False, "error": f"personal store write failed: {e}"}
            if code != 200:
                print(f"[personal] REJECTED ({code}): {body.get('error')}")
            self._send_json(code, body)
            return
        code, body = perform_action(payload.get("task_id"),
                                    payload.get("action"),
                                    payload.get("reason"))
        if code == 200:
            print(f"[action] {body['task_id']}: {body['from']} -> {body['to']}"
                  + (f"  ({body['reason']})" if body.get("reason") else ""))
        else:
            print(f"[action] REJECTED ({code}): {body.get('error')}")
        self._send_json(code, body)


def main():
    os.chdir(HERE)
    rc = check_drift.check(quiet=True)
    label = {0: "CLEAN", 1: "DRIFT DETECTED", 2: "command_center.json MISSING"}.get(rc, "?")
    print(f"[serve] freshness check: {label} (rc={rc})")
    if rc == 2:
        print("[serve] run `python generate_dashboard.py` first.")
        return rc
    if rc == 1:
        print("[serve] dashboard is STALE — the page will show the stale banner. "
              "Run `python generate_dashboard.py` to refresh the data.")
    # Bind to loopback only: the action endpoint is a single-operator local tool.
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/command_center.html"
        print(f"[serve] serving {HERE}")
        print(f"[serve] task actions: POST /api/action enabled (local-only)")
        print(f"[serve] open: {url}  ·  SEO: http://localhost:{PORT}/seo.html  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[serve] stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
