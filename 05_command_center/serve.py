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
"""

import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import check_drift  # importing does not run it (guarded by __main__)

HERE = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# ── Task-action config ────────────────────────────────────────────────────────
BARI_ROOT = Path(r"C:\Bari")
TASKS_DIR = BARI_ROOT / "tasks"
GENERATOR = HERE / "generate_dashboard.py"
AUDIT_LOG = HERE / "task_action_audit.log"

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

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/action":
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except Exception as e:
            self._send_json(400, {"ok": False, "error": f"bad request body: {e}"})
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
