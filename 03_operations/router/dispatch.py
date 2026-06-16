"""
dispatch.py — Bari C2 dispatch router
======================================
Routes P-numbered prompt files to the correct execution lane.
C2 (DeepSeek via opencode) is dispatched programmatically.
C1 (Claude) is dispatched natively via the orchestrator.

Implementation
--------------
opencode is a TUI/console application; its `opencode run` command does not emit
output through stdout/stderr when invoked non-interactively (no TTY available in
subprocess).  The correct headless API is the HTTP server:

  1. Spawn `opencode serve --port PORT` as a background process.
  2. Subscribe to the SSE event stream at GET /api/event (persists for the session).
  3. Create a new session via POST /api/session.
  4. Send the prompt message via POST /session/{id}/message  (SSE stream; events
     arrive on the /api/event channel).
  5. Collect all SSE events until `session.idle` arrives, then tear down.
  6. Poll GET /api/session/{id}/message for the final assistant message.

Discovered model IDs (via `opencode models`):
  opencode/deepseek-v4-flash-free   ← C2 target (authenticated via opencode proxy)
  openai/gpt-5.4-mini               ← authenticated (OpenAI OAuth)

Lanes
-----
  C2        → DeepSeek via opencode HTTP API (mechanical / zero-judgment)
  C1-GROK   → xAI Grok Build CLI (C1-grade spec-complete work, repo access;
              owner's SuperGrok subscription; route tag `(route: C1-GROK)`).
              REPLACED the retired Cursor lane 2026-06-14.
  C1-CURSOR → RETIRED 2026-06-14 — legacy tag still routes transparently to C1-GROK.
  C1-GEMINI → Google Gemini CLI (C1-grade judgment work, repo access;
              owner route tag C1-GEMINI
  C3        → OpenAI (gpt-5.5) via opencode HTTP API — the orchestrator's
              independent outside-the-family ADVISOR (red-team 2nd opinion,
              fresh-eyes Hebrew copy review, critique). Advice only: never edits
              files, produces data, or closes work. Programmatic — NOT owner-paste.
  C1        → native Claude subagent — the orchestrator dispatches, not this script

Usage
-----
  python dispatch.py P35                  # dispatch P35 (C2 / C1-CURSOR / C1-GEMINI by route tag)
  python dispatch.py P35 --dry-run        # show the command without running
  python dispatch.py --selftest           # send a PONG round-trip through opencode
  python dispatch.py --selftest-gemini    # send a PONG through the Gemini CLI
  python dispatch.py --selftest-grok      # send a PONG through the Grok CLI
  python dispatch.py P35 --timeout 3600   # custom timeout in seconds (default: 1800)

Rules
-----
- Only touches: 03_operations/router/, tasks/returns/, tasks/DISPATCH_BOARD.md
- Never dispatches a prompt during --dry-run
- Never touches any other repo file
- No network beyond what opencode itself does
- No OFF (Open Food Facts) anything, ever
"""

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 output on Windows so Unicode characters in prompt files
# (arrows, Hebrew, etc.) don't crash the console encoder.
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Constants ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # C:\Bari
PROMPTS_DIR = REPO_ROOT / "tasks" / "prompts"
RETURNS_DIR = REPO_ROOT / "tasks" / "returns"
DISPATCH_BOARD = REPO_ROOT / "tasks" / "DISPATCH_BOARD.md"

# Discovered via `opencode models` — the DeepSeek model available through
# opencode's own proxy (no separate API key required).
C2_MODEL_ID = "deepseek-v4-flash-free"
C2_PROVIDER_ID = "opencode"

# ── C3 lane (independent strong reviewer) ────────────────────────────────────
# C3 = the orchestrator's outside-the-family advisor (red-team 2nd opinions,
# fresh-eyes Hebrew copy review, Deep-Research-style critique). Reachable
# PROGRAMMATICALLY through the same opencode HTTP path as C2, but against a
# strong OpenAI model authenticated via OpenAI OAuth — NOT owner-paste.
# Advice-only: never edits files, never produces product/nutrition data,
# never closes work. The orchestrator dispatches it itself.
C3_MODEL_ID = "gpt-5.5"
C3_PROVIDER_ID = "openai"

# ── Cursor lane (C1-CURSOR) — RETIRED 2026-06-14 ─────────────────────────────
# Replaced by the Grok lane (see run_via_grok_cli below). These functions are
# kept dormant (no active route reaches them; the C1-CURSOR tag now aliases to
# C1-GROK) so the change is reversible. Do not wire new work here.
# Cursor's headless agent CLI ("cursor-agent"), authenticated via the owner's
# Cursor subscription.  C1-grade executor: real repo access + file edits.
# The top-level wrapper (%LOCALAPPDATA%\cursor-agent\agent.cmd) has a
# version-dir regex bug (rejects the YYYY.MM.DD-HH-MM-SS-hash naming), so we
# resolve the newest version directory ourselves and invoke its cmd directly.
_CURSOR_VERSIONS_DIR = (
    Path(os.environ.get("LOCALAPPDATA", "")) / "cursor-agent" / "versions"
)


def find_cursor_agent_cmd() -> Path:
    """Resolve the newest installed cursor-agent.cmd. Raises if not found."""
    if not _CURSOR_VERSIONS_DIR.exists():
        raise FileNotFoundError(
            f"cursor-agent not installed (no {_CURSOR_VERSIONS_DIR}). "
            "Install: irm 'https://cursor.com/install?win32=true' | iex"
        )
    candidates = sorted(
        (d for d in _CURSOR_VERSIONS_DIR.iterdir()
         if d.is_dir() and (d / "cursor-agent.cmd").exists()),
        key=lambda d: d.name,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            f"No cursor-agent version directories under {_CURSOR_VERSIONS_DIR}"
        )
    return candidates[0] / "cursor-agent.cmd"
# Gemini lane
_GEMINI_CMD_DEFAULT = Path(
    r"C:\Users\HP\AppData\Roaming\npm\gemini.cmd"
)

def find_gemini_cmd() -> Path:
    if _GEMINI_CMD_DEFAULT.exists(): return _GEMINI_CMD_DEFAULT
    import shutil as _shutil
    alt=_shutil.which("gemini")
    if alt: return Path(alt)
    raise FileNotFoundError(f"Gemini CLI not found at {_GEMINI_CMD_DEFAULT}")
# opencode on Windows is installed as a .ps1 wrapper around the actual exe.
# Python subprocess cannot invoke .ps1 files directly; we use the underlying
# exe.  Resolved once at import time so the script fails fast if not found.
_OPENCODE_EXE = Path(
    r"C:\Users\HP\AppData\Roaming\npm\node_modules\opencode-ai\bin\opencode.exe"
)
if not _OPENCODE_EXE.exists():
    import shutil as _shutil
    _alt = _shutil.which("opencode")
    if _alt and Path(_alt).suffix.lower() == ".exe":
        _OPENCODE_EXE = Path(_alt)

DEFAULT_TIMEOUT = 1800  # seconds
SERVER_PORT_RANGE = (19000, 19999)  # range to search for a free port


# ── Helpers ──────────────────────────────────────────────────────────────────

def git_status_porcelain(repo: Path) -> str:
    """Return the output of `git status --porcelain` in the repo."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    """Return hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_free_port(start: int = 19000, end: int = 19999) -> int:
    """Find an available TCP port in the given range."""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found in {start}–{end}")


def find_prompt_file(p_number: str) -> Path:
    """
    Locate tasks/prompts/P{N}_*.md for a given P-number (e.g. 'P35').
    Returns the Path if found, raises FileNotFoundError otherwise.
    """
    pattern = f"{p_number}_*.md"
    matches = list(PROMPTS_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(
            f"No prompt file found matching {PROMPTS_DIR / pattern}"
        )
    if len(matches) > 1:
        raise ValueError(
            f"Ambiguous: multiple files match {pattern}: {matches}"
        )
    return matches[0]


def parse_route(prompt_path: Path) -> str:
    """
    Read the first line of the prompt file and extract the route.
    Expected format:  # P35 / Some title (route: C2)
    Returns 'C1', 'C2', or 'C1-CURSOR'. Raises ValueError if not found.
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    match = re.search(r'\(route:\s*(C1-GROK|C1-CURSOR|C1-GEMINI|C[123])\)', first_line, re.IGNORECASE)
    if not match:
        raise ValueError(
            f"Cannot parse route from title line: {first_line!r}\n"
            f"Expected format: # P35 / Title (route: C2 | C1 | C1-GROK | C1-GEMINI)"
        )
    return match.group(1).upper()


def strip_owner_meta(prompt_path: Path) -> str:
    """
    Strip the owner-facing meta block from the prompt.

    The meta block is defined as everything between the title line (line 1)
    and the first `---` separator.  Specifically:
      - Line 1: the title (kept for context, then discarded)
      - Lines 2..N: the ➡️ OWNER block (discarded)
      - The `---` line itself (discarded)
      - Everything after the first `---`: the agent task body (kept)

    If no `---` is found the entire file content (minus the title line)
    is returned as-is.
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the first occurrence of a `---` separator line
    sep_index = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            sep_index = i
            break

    if sep_index is None:
        # No separator found — skip title, return the rest
        body = "".join(lines[1:]).strip()
    else:
        # Skip everything up to and including the `---`
        body = "".join(lines[sep_index + 1:]).strip()

    return body


# ── opencode HTTP API client ──────────────────────────────────────────────────

def _api_call(base_url: str, path: str, method: str = "GET",
              body: dict | None = None, timeout: int = 30) -> dict:
    """Make a JSON API call to opencode serve."""
    url = f"{base_url}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _wait_for_server(base_url: str, retries: int = 30, interval: float = 0.5) -> bool:
    """Wait for the opencode server to start accepting connections."""
    for _ in range(retries):
        try:
            urllib.request.urlopen(f"{base_url}/api/session", timeout=2)
            return True
        except Exception:
            time.sleep(interval)
    return False


class SSEReader:
    """
    Reads Server-Sent Events from a streaming HTTP response.
    Runs in a background thread; events are accumulated and streamed to console.
    """

    def __init__(self, url: str, timeout: int):
        self.url = url
        self.timeout = timeout
        self.events: list[dict] = []
        self._done = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def start(self):
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    def stop(self):
        self._done.set()
        if self._thread:
            self._thread.join(timeout=5)

    def _read(self):
        req = urllib.request.Request(
            self.url,
            headers={"Accept": "text/event-stream"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                event_data: list[str] = []
                for raw_line in resp:
                    if self._done.is_set():
                        break
                    line = raw_line.decode("utf-8", errors="replace").rstrip("\n\r")
                    if line.startswith("data: "):
                        event_data.append(line[6:])
                    elif line == "" and event_data:
                        # End of event block
                        raw = "".join(event_data)
                        try:
                            evt = json.loads(raw)
                            with self._lock:
                                self.events.append(evt)
                            # Stream to console
                            evt_type = evt.get("type", "unknown")
                            print(f"[SSE] {evt_type}", flush=True)
                        except json.JSONDecodeError:
                            pass
                        event_data = []
        except Exception as e:
            if not self._done.is_set():
                print(f"[SSE] stream ended: {e}", flush=True)

    def wait_for_idle(self, session_id: str, deadline: float) -> bool:
        """Block until session.idle arrives or deadline passes."""
        while time.time() < deadline:
            with self._lock:
                for evt in self.events:
                    if evt.get("type") == "session.idle":
                        sid = (evt.get("data") or {}).get("sessionID") or evt.get("sessionID")
                        if sid == session_id or sid is None:
                            return True
            time.sleep(0.5)
        return False


def run_via_opencode_api(
    message: str,
    model_id: str,
    provider_id: str,
    timeout: int,
) -> tuple[int, str]:
    """
    Dispatch a message to opencode via the headless HTTP API.

    Returns (exit_code, combined_output_text).

    Flow:
      1. Spawn `opencode serve --port PORT`
      2. Wait for server ready
      3. Subscribe to /api/event SSE stream
      4. Create session
      5. Send message via /session/{id}/message (streaming POST — returns SSE)
      6. Wait for session.idle event (or timeout)
      7. Collect final assistant text from message list
      8. Tear down server
    """
    if not _OPENCODE_EXE.exists():
        raise FileNotFoundError(
            f"opencode executable not found at {_OPENCODE_EXE}."
        )

    port = find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    # 1. Start opencode serve
    serve_proc = subprocess.Popen(
        [str(_OPENCODE_EXE), "serve", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(REPO_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(f"[opencode] Server starting on port {port} (pid={serve_proc.pid})", flush=True)

    output_parts: list[str] = []
    exit_code = 0
    sse_reader: SSEReader | None = None

    try:
        # 2. Wait for server ready
        if not _wait_for_server(base_url):
            raise RuntimeError("opencode server did not start in time.")
        print("[opencode] Server ready.", flush=True)

        # 3. Subscribe to global SSE event stream
        deadline = time.time() + timeout
        sse_reader = SSEReader(f"{base_url}/api/event", timeout=timeout)
        sse_reader.start()
        time.sleep(0.5)  # give SSE connection a moment to establish

        # 4. Create session
        session_resp = _api_call(
            base_url, "/api/session", method="POST",
            body={"model": {"id": model_id, "providerID": provider_id}},
        )
        session_id = session_resp["data"]["id"]
        print(f"[opencode] Session created: {session_id}", flush=True)

        # 5. Send the message (this POST returns a streaming SSE response;
        #    we don't parse it inline — events arrive on /api/event instead).
        msg_url = f"{base_url}/session/{session_id}/message"
        msg_body = json.dumps(
            {"parts": [{"type": "text", "text": message}]}
        ).encode("utf-8")
        msg_req = urllib.request.Request(
            msg_url,
            data=msg_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        print(f"[opencode] Sending message ({len(message)} chars)…", flush=True)

        # Read the streaming response from the message endpoint itself
        # (it also streams SSE events directly).
        try:
            with urllib.request.urlopen(msg_req, timeout=min(timeout, 300)) as resp:
                event_data: list[str] = []
                for raw_line in resp:
                    line = raw_line.decode("utf-8", errors="replace").rstrip("\n\r")
                    if line.startswith("data: "):
                        event_data.append(line[6:])
                    elif line == "" and event_data:
                        raw = "".join(event_data)
                        try:
                            evt = json.loads(raw)
                            evt_type = evt.get("type", "?")
                            print(f"[MSG-SSE] {evt_type}", flush=True)
                            if evt_type == "session.idle":
                                break
                            # Collect text parts from assistant messages
                            if evt_type in ("message.part", "message.part.updated"):
                                part = evt.get("data", {}).get("part", {})
                                if part.get("type") == "text":
                                    text = part.get("text", "")
                                    output_parts.append(text)
                                    print(f"[AGENT] {text}", flush=True)
                        except json.JSONDecodeError:
                            pass
                        event_data = []
        except Exception as e:
            print(f"[opencode] Message stream ended: {e}", flush=True)

        # 6. Also wait for idle on the background SSE channel (belt+suspenders)
        idle = sse_reader.wait_for_idle(session_id, deadline)
        if not idle:
            print("[opencode] WARNING: session.idle not received before timeout.", flush=True)

        # 7. Collect final messages via the message list endpoint
        try:
            msg_list = _api_call(base_url, f"/api/session/{session_id}/message")
            msgs = msg_list.get("data", [])
            for msg in msgs:
                role = msg.get("role", "")
                parts = msg.get("parts") or []
                for part in parts:
                    if part.get("type") == "text":
                        text = part.get("text", "").strip()
                        if text:
                            output_parts.append(f"[{role}] {text}")
        except Exception as e:
            print(f"[opencode] Could not fetch final messages: {e}", flush=True)

        # Deduplicate output parts
        seen: set[str] = set()
        deduped: list[str] = []
        for p in output_parts:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        combined = "\n".join(deduped)

        # Extract final assistant text from SSE events (belt+suspenders)
        with sse_reader._lock:
            all_events = list(sse_reader.events)

        # Find the last message.part.updated event with type=text — that's
        # the completed assistant response text.
        for evt in reversed(all_events):
            if evt.get("type") in ("message.part.updated", "message.part"):
                part = (evt.get("data") or {}).get("part", {})
                if part.get("type") == "text":
                    text = part.get("text", "").strip()
                    if text and text not in seen:
                        seen.add(text)
                        deduped.insert(0, text)  # prepend — this is the main response
                        output_parts.append(text)
                    break

        sse_summary = "\n".join(
            f"  {e.get('type', '?')}: {json.dumps(e.get('data', {}))[:200]}"
            for e in all_events
        )
        # Rebuild combined with the potentially updated deduped list
        combined = "\n".join(deduped) + "\n\n--- SSE Events ---\n" + sse_summary

    except Exception as e:
        print(f"[opencode] ERROR: {e}", flush=True)
        exit_code = 1
        combined = f"ERROR: {e}"

    finally:
        if sse_reader:
            sse_reader.stop()
        # Gracefully shut down the server
        try:
            serve_proc.terminate()
            serve_proc.wait(timeout=5)
        except Exception:
            serve_proc.kill()
        print(f"[opencode] Server stopped.", flush=True)

    return exit_code, combined


# ── Cursor CLI execution ─────────────────────────────────────────────────────

def run_via_cursor_cli(message: str, timeout: int) -> tuple[int, str]:
    """
    Dispatch a message to Cursor's headless agent CLI (print mode).

    The CLI runs with cwd=REPO_ROOT and full repo access, so dispatch messages
    should reference the prompt file by path rather than inline a long body
    (Windows command lines cap at ~32K chars).

    Returns (exit_code, combined_output_text).
    """
    cursor_cmd = find_cursor_agent_cmd()
    # Flag ORDER matters: global flags must precede `-p <message>`, otherwise
    # cursor-agent swallows them as part of the prompt and the workspace-trust
    # prompt still blocks file writes (P46 diagnosis 2026-06-13).
    cmd = [
        str(cursor_cmd),
        "--force",                     # allow commands without TUI approval
        "--trust",                     # trust the workspace dir without prompting
        "--output-format", "text",
        "-p", message,                 # print mode: non-interactive, prompt LAST
    ]
    print(f"[cursor] Invoking {cursor_cmd.parent.name}\\cursor-agent.cmd "
          f"({len(message)} chars)…", flush=True)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=False,
        )
        output = (proc.stdout or "")
        if proc.stderr and proc.stderr.strip():
            output += "\n\n--- STDERR ---\n" + proc.stderr
        if _looks_like_quota_exhaustion(output, proc.returncode):
            banner = (
                "⛔ C1-CURSOR LANE DOWN — Cursor usage limit appears exhausted.\n"
                "Orchestrator: re-route this P-number to native C1 (Agent tool); "
                "mark the lane DOWN on the board until the quota resets.\n\n"
            )
            print("[cursor] ⛔ Usage limit detected — lane should be marked DOWN; "
                  "re-route to native C1.", flush=True)
            return 75, banner + output  # 75 = EX_TEMPFAIL: retry elsewhere
        return proc.returncode, output
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") if isinstance(e.stdout, str) else ""
        return 1, f"TIMEOUT after {timeout}s.\n{partial}"



def run_via_gemini_cli(message: str, timeout: int, executor: bool = True):
    gemini_cmd=find_gemini_cmd()
    # --approval-mode: default=prompt (auto-denies in headless -p mode -> "Unauthorized
    # tool call"), yolo=auto-approve all tools (the executor lane, mirrors Cursor's --force),
    # plan=read-only. The lane was long mis-described as "read/plan-only" purely because this
    # flag was unset and it fell to `default`; yolo makes it a real C1-grade executor.
    approval = "yolo" if executor else "plan"
    cmd=[str(gemini_cmd),"--skip-trust",f"--approval-mode={approval}","-p",message]
    print(f"[gemini] Invoking {gemini_cmd.name} ({len(message)} chars)...", flush=True)
    try:
        proc=subprocess.run(cmd,cwd=str(REPO_ROOT),capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=timeout,shell=False)
        output=(proc.stdout or "")
        if proc.stderr and proc.stderr.strip():
            output += '\n\n--- STDERR ---\n' + proc.stderr
        if _looks_like_quota_exhaustion(output, proc.returncode):
            return 75, "LANE DOWN" + '\n' + output
        return proc.returncode, output
    except subprocess.TimeoutExpired as e:
        partial=(e.stdout or "") if isinstance(e.stdout,str) else ""
        return 1, "TIMEOUT after %ss.%s%s" % (timeout, '\n', partial)

def _looks_like_quota_exhaustion(output: str, exit_code: int) -> bool:
    """Heuristic: did the Cursor CLI refuse because the subscription quota ran out?"""
    if exit_code == 0:
        return False
    lowered = output.lower()
    markers = (
        "usage limit", "usage-limit", "rate limit", "rate-limited",
        "quota", "out of requests", "upgrade your plan", "plan limit",
        "limit reached", "too many requests", "429",
        "resource_exhausted",
    )
    return any(m in lowered for m in markers)


def build_cursor_bootstrap(p_number: str, prompt_path: Path) -> str:
    """
    Short bootstrap message for the Cursor lane: point the agent at the prompt
    file instead of inlining the body (avoids the Windows cmdline length cap,
    and Cursor has repo access anyway).
    """
    rel = prompt_path.relative_to(REPO_ROOT).as_posix()
    return (
        f"You are executing Bari task prompt {p_number}.\n"
        f"1. Read the file {rel} in this repo.\n"
        f"2. Ignore everything above the first '---' separator (owner-facing meta).\n"
        f"3. Execute the task body below the separator exactly as written, "
        f"including its rules and deliverables.\n"
        f"4. Hard rule: NEVER use Open Food Facts (OFF) as a data source for "
        f"anything. Unknown is acceptable; OFF is not.\n"
        f"5. When done, print a return block summarizing what you changed "
        f"(files + what to verify), per the prompt's return-format instructions."
    )


# ── File writing ──────────────────────────────────────────────────────────────

def write_return_file(
    p_number: str,
    prompt_path: Path,
    model_id: str,
    provider_id: str,
    started: datetime,
    finished: datetime,
    exit_code: int,
    output: str,
    git_before: str,
    git_after: str,
) -> Path:
    """Write the return file to tasks/returns/P{N}_return.md."""
    RETURNS_DIR.mkdir(parents=True, exist_ok=True)
    return_path = RETURNS_DIR / f"{p_number}_return.md"
    model_full = f"{provider_id}/{model_id}"

    # Compute changed-files diff
    before_set = set(git_before.splitlines()) if git_before else set()
    after_set = set(git_after.splitlines()) if git_after else set()
    new_lines = sorted(after_set - before_set)
    removed_lines = sorted(before_set - after_set)

    changed_section = []
    if new_lines:
        changed_section.append("### New / modified since dispatch")
        for line in new_lines:
            changed_section.append(f"  {line}")
    if removed_lines:
        changed_section.append("### Removed / cleaned since dispatch")
        for line in removed_lines:
            changed_section.append(f"  {line}")
    if not new_lines and not removed_lines:
        changed_section.append("*(no changes detected)*")

    content = f"""# Return: {p_number}

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `{prompt_path.relative_to(REPO_ROOT)}` |
| Model | `{model_full}` |
| Started | {started.isoformat()} |
| Finished | {finished.isoformat()} |
| Exit code | {exit_code} |

---

## Output

```
{output.strip() if output.strip() else "(empty)"}
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
{git_before if git_before else "(clean)"}
```

### After dispatch

```
{git_after if git_after else "(clean)"}
```

### Delta

{chr(10).join(changed_section)}
"""

    with open(return_path, "w", encoding="utf-8") as f:
        f.write(content)

    return return_path


def tick_dispatch_board(p_number: str) -> bool:
    """
    In tasks/DISPATCH_BOARD.md, change `- [ ] P{N}` to `- [x] P{N}` on its
    signal line.  If already ticked, leaves it.  Returns True if a change was made.
    """
    if not DISPATCH_BOARD.exists():
        print(f"[dispatch] WARNING: DISPATCH_BOARD not found at {DISPATCH_BOARD}", file=sys.stderr)
        return False

    with open(DISPATCH_BOARD, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r'(- \[ \] )(' + re.escape(p_number) + r'(?:\b|\s|$))',
        re.MULTILINE,
    )
    new_content, count = pattern.subn(r'- [x] \2', content)

    if count > 0:
        with open(DISPATCH_BOARD, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[dispatch] Board ticked: {p_number} marked done.", flush=True)
        return True
    else:
        print(f"[dispatch] Board: {p_number} already ticked or not found as unchecked.", flush=True)
        return False


# ── Subcommands ───────────────────────────────────────────────────────────────

def cmd_dispatch(p_number: str, dry_run: bool, timeout: int) -> int:
    """Main dispatch flow for a P-number."""
    p_number = p_number.upper()

    # Step 1: locate prompt file
    try:
        prompt_path = find_prompt_file(p_number)
    except FileNotFoundError as e:
        print(f"[dispatch] ERROR: {e}", file=sys.stderr)
        return 1

    print(f"[dispatch] Prompt file: {prompt_path}")

    # Step 1b: parse route
    try:
        route = parse_route(prompt_path)
    except ValueError as e:
        print(f"[dispatch] ERROR: {e}", file=sys.stderr)
        return 1

    print(f"[dispatch] Route: {route}")

    if route == "C1":
        print("[dispatch] C1 → dispatch natively via orchestrator")
        return 0

    if route == "C1-GROK":
        return _dispatch_grok(p_number, prompt_path, dry_run, timeout)

    if route == "C1-CURSOR":
        # RETIRED 2026-06-14 — Cursor lane replaced by Grok. Legacy tags still
        # route, transparently, to C1-GROK so old prompt files don't break.
        print("[dispatch] NOTE: C1-CURSOR is retired → routing to C1-GROK.")
        return _dispatch_grok(p_number, prompt_path, dry_run, timeout)

    if route == "C1-GEMINI":
        return _dispatch_gemini(p_number, prompt_path, dry_run, timeout)

    # C2 and C3 both ride the opencode HTTP path; only the target model differs.
    if route == "C3":
        active_model_id, active_provider_id = C3_MODEL_ID, C3_PROVIDER_ID
    else:  # C2
        active_model_id, active_provider_id = C2_MODEL_ID, C2_PROVIDER_ID

    # Step 2: strip owner meta block
    task_body = strip_owner_meta(prompt_path)
    print(f"[dispatch] Task body ({len(task_body)} chars) — meta stripped OK.")

    # Step 3: git status before
    git_before = git_status_porcelain(REPO_ROOT)

    # Build the dry-run command description
    cmd_desc = (
        f"opencode serve --port <FREE> && POST /api/session "
        f"model={active_provider_id}/{active_model_id} && "
        f"POST /session/{{id}}/message (SSE)"
    )

    if dry_run:
        print("\n[dispatch] DRY-RUN — would execute (opencode HTTP API):")
        print(f"  {cmd_desc}")
        print("\n[dispatch] Task body (first 500 chars):")
        print(task_body[:500])
        print("\n[dispatch] Git status before:")
        print(git_before if git_before else "(clean)")
        return 0

    # Step 4: invoke opencode via HTTP API
    started = datetime.now(timezone.utc)
    print(f"\n[dispatch] Invoking opencode at {started.isoformat()} …")
    print(f"[dispatch] Model: {active_provider_id}/{active_model_id}")
    print(f"[dispatch] Timeout: {timeout}s")
    print("-" * 60)

    exit_code, output = run_via_opencode_api(
        message=task_body,
        model_id=active_model_id,
        provider_id=active_provider_id,
        timeout=timeout,
    )
    finished = datetime.now(timezone.utc)

    print("-" * 60)
    print(f"[dispatch] Finished at {finished.isoformat()}, exit code: {exit_code}")

    # Step 6: git status after
    git_after = git_status_porcelain(REPO_ROOT)

    # Step 5: write return file
    return_path = write_return_file(
        p_number=p_number,
        prompt_path=prompt_path,
        model_id=active_model_id,
        provider_id=active_provider_id,
        started=started,
        finished=finished,
        exit_code=exit_code,
        output=output,
        git_before=git_before,
        git_after=git_after,
    )
    print(f"[dispatch] Return file written: {return_path}")

    # Step 7: auto-tick board
    tick_dispatch_board(p_number)

    return exit_code


def _dispatch_cursor(p_number: str, prompt_path: Path, dry_run: bool,
                     timeout: int) -> int:
    """Dispatch flow for the C1-CURSOR lane."""
    bootstrap = build_cursor_bootstrap(p_number, prompt_path)
    git_before = git_status_porcelain(REPO_ROOT)

    if dry_run:
        try:
            cursor_cmd = find_cursor_agent_cmd()
            print(f"\n[dispatch] DRY-RUN — would execute:\n  {cursor_cmd} "
                  f"-p <bootstrap> --output-format text --force")
        except FileNotFoundError as e:
            print(f"\n[dispatch] DRY-RUN — cursor-agent NOT available: {e}")
        print(f"\n[dispatch] Bootstrap message:\n{bootstrap}")
        return 0

    started = datetime.now(timezone.utc)
    print(f"\n[dispatch] Invoking cursor-agent at {started.isoformat()} …")
    print(f"[dispatch] Timeout: {timeout}s")
    print("-" * 60)

    exit_code, output = run_via_cursor_cli(bootstrap, timeout)
    finished = datetime.now(timezone.utc)

    print("-" * 60)
    print(f"[dispatch] Finished at {finished.isoformat()}, exit code: {exit_code}")

    git_after = git_status_porcelain(REPO_ROOT)
    return_path = write_return_file(
        p_number=p_number,
        prompt_path=prompt_path,
        model_id="agent-cli",
        provider_id="cursor",
        started=started,
        finished=finished,
        exit_code=exit_code,
        output=output,
        git_before=git_before,
        git_after=git_after,
    )
    print(f"[dispatch] Return file written: {return_path}")
    tick_dispatch_board(p_number)
    return exit_code



def _dispatch_gemini(p_number, prompt_path, dry_run, timeout):
    bootstrap=build_cursor_bootstrap(p_number,prompt_path)
    git_before=git_status_porcelain(REPO_ROOT)
    if dry_run: return 0
    started=datetime.now(timezone.utc); exit_code,output=run_via_gemini_cli(bootstrap,timeout); finished=datetime.now(timezone.utc)
    git_after=git_status_porcelain(REPO_ROOT)
    write_return_file(p_number=p_number,prompt_path=prompt_path,model_id="cli",provider_id="gemini",started=started,finished=finished,exit_code=exit_code,output=output,git_before=git_before,git_after=git_after)
    tick_dispatch_board(p_number); return exit_code


# ── Grok lane (C1-GROK) ──────────────────────────────────────────────────────
# xAI "Grok Build" CLI ("grok"), authenticated via the owner's SuperGrok
# subscription (one-time browser OAuth: `grok login`; creds persist in ~/.grok,
# so headless `grok -p` reuses them, flat-rate). C1-grade executor: real repo
# access + file edits. Replaced the retired Cursor lane on 2026-06-14.
_GROK_CMD_DEFAULT = Path(os.environ.get("USERPROFILE", "")) / ".grok" / "bin" / "grok.exe"


_GROK_AUTH_JSON = Path(os.environ.get("USERPROFILE", "")) / ".grok" / "auth.json"


def find_grok_cmd() -> Path:
    if _GROK_CMD_DEFAULT.exists(): return _GROK_CMD_DEFAULT
    import shutil as _shutil
    alt = _shutil.which("grok")
    if alt: return Path(alt)
    raise FileNotFoundError(
        f"Grok CLI not found at {_GROK_CMD_DEFAULT}. "
        "Install: irm https://x.ai/cli/install.ps1 | iex  then: grok login"
    )


def _grok_is_authenticated() -> bool:
    """Session token in ~/.grok/auth.json (browser/OAuth login) or an XAI_API_KEY
    fallback. Without either, headless `grok -p` blocks on the interactive welcome
    screen and burns the whole timeout — so we pre-check and fail fast instead."""
    if os.environ.get("XAI_API_KEY"):
        return True
    try:
        return _GROK_AUTH_JSON.exists() and _GROK_AUTH_JSON.stat().st_size > 2
    except OSError:
        return False


_GROK_CONFIG_TOML = Path(os.environ.get("USERPROFILE", "")) / ".grok" / "config.toml"


def _toml_set_bool(text: str, table: str, key: str, value: bool) -> str:
    """Idempotently set `key = true/false` under `[table]` in a TOML string.
    `key` is unique across our two settings, so a global key match is safe:
    replace it in place if present, else insert under the table header, else
    append the table. Avoids the duplicate-table-header TOML error."""
    v = "true" if value else "false"
    if re.search(rf"(?m)^\s*{key}\s*=", text):
        return re.sub(rf"(?m)^(\s*{key}\s*=).*$", rf"\1 {v}", text)
    if re.search(rf"(?m)^\s*\[{re.escape(table)}\]\s*$", text):
        return re.sub(rf"(?m)^(\[{re.escape(table)}\]\s*)$", rf"\1\n{key} = {v}", text, count=1)
    sep = "" if (text == "" or text.endswith("\n")) else "\n"
    return text + f"{sep}\n[{table}]\n{key} = {v}\n"


def _ensure_grok_hardening() -> tuple[bool, str]:
    """Guarantee ~/.grok/config.toml disables the whole-repo cloud upload BEFORE any
    dispatch. Grok Build defaults to codebase_indexing=true, which on session start
    bulk-uploads a ~800MB reference snapshot of the repo to xAI cloud (the C:\\Bari
    02_products tree) → hangs the lane AND exfiltrates the proprietary Agent OS brain.
    A Grok update / re-login can silently reset config.toml back to that default, so we
    re-assert it every dispatch: self-heal if drifted, FAIL CLOSED if we cannot confirm
    it (never send the repo to the cloud on an unverified config). Returns (ok, note)."""
    want_ok = lambda d: (
        (d.get("features", {}) or {}).get("codebase_indexing") is False
        and (d.get("tools", {}) or {}).get("respect_gitignore") is True
    )
    try:
        import tomllib
    except ModuleNotFoundError:
        tomllib = None
    text = ""
    try:
        if _GROK_CONFIG_TOML.exists():
            text = _GROK_CONFIG_TOML.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"cannot read {_GROK_CONFIG_TOML}: {e}"

    if tomllib is not None:
        try:
            if want_ok(tomllib.loads(text)):
                return True, "already hardened"
        except Exception:
            pass  # malformed/partial → fall through to repair

    # Repair (idempotent) and re-validate.
    patched = _toml_set_bool(text, "features", "codebase_indexing", False)
    patched = _toml_set_bool(patched, "tools", "respect_gitignore", True)
    try:
        _GROK_CONFIG_TOML.parent.mkdir(parents=True, exist_ok=True)
        _GROK_CONFIG_TOML.write_text(patched, encoding="utf-8")
    except OSError as e:
        return False, f"cannot write {_GROK_CONFIG_TOML}: {e}"
    if tomllib is None:
        return True, "repaired (unverified: no tomllib)"
    try:
        if want_ok(tomllib.loads(patched)):
            return True, "repaired"
    except Exception as e:
        return False, f"repair produced invalid TOML: {e}"
    return False, "could not harden config.toml (manual fix needed)"


def run_via_grok_cli(message: str, timeout: int) -> tuple[int, str]:
    """Dispatch to the Grok Build CLI in headless single-turn mode.

    --always-approve auto-approves every tool execution (the executor flag,
    mirrors Cursor's --force / Gemini's --approval-mode=yolo). -p prints the
    response and exits. Runs with cwd=REPO_ROOT (full repo access), so the
    bootstrap references the prompt file by path rather than inlining it.
    """
    grok_cmd = find_grok_cmd()
    if not _grok_is_authenticated():
        banner = (
            "⛔ C1-GROK LANE NOT ACTIVATED — no ~/.grok/auth.json and no XAI_API_KEY.\n"
            "Owner one-time step: run `grok login` (browser OAuth, SuperGrok account; "
            "use `grok login --device-auth` on a browserless box), then "
            "`python dispatch.py --selftest-grok` must PASS before routing work here.\n"
        )
        print("[grok] ⛔ Not authenticated — run `grok login` (fast-fail, no dispatch).", flush=True)
        return 75, banner
    hardened, note = _ensure_grok_hardening()
    if not hardened:
        banner = (
            "⛔ C1-GROK BLOCKED — could not confirm the repo-upload guard is OFF.\n"
            f"  {note}\n"
            "Refusing to dispatch: with codebase_indexing on, Grok bulk-uploads the whole\n"
            "C:\\Bari repo to xAI cloud. Fix ~/.grok/config.toml manually:\n"
            "  [features]\n  codebase_indexing = false\n  [tools]\n  respect_gitignore = true\n"
        )
        print(f"[grok] ⛔ Config guard failed ({note}) — fail-closed, no dispatch.", flush=True)
        return 75, banner
    if note != "already hardened":
        print(f"[grok] config hardening: {note} (codebase_indexing=false, respect_gitignore=true).", flush=True)
    cmd = [
        str(grok_cmd),
        "--always-approve",            # auto-approve all tool executions
        "--output-format", "plain",
        "-p", message,                 # single-turn headless prompt
    ]
    # Hardening (2026-06-14): Grok Build bulk-uploads a whole-repo "reference
    # snapshot" to xAI cloud on session start. ~/.grok/config.toml disables it
    # ([features] codebase_indexing=false, [tools] respect_gitignore=true). We
    # also force gitignore filtering via env as belt-and-suspenders so a reset
    # config.toml can't silently re-enable the ~800MB upload of the 02_products
    # tree. Without this the lane hangs AND exfiltrates the proprietary repo.
    env = dict(os.environ, GROK_RESPECT_GITIGNORE="1")
    print(f"[grok] Invoking {grok_cmd.name} ({len(message)} chars)…", flush=True)
    try:
        proc = subprocess.run(
            cmd, cwd=str(REPO_ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout, shell=False, env=env,
        )
        output = (proc.stdout or "")
        if proc.stderr and proc.stderr.strip():
            output += "\n\n--- STDERR ---\n" + proc.stderr
        # Not-logged-in detection → the lane is unactivated, not a task failure.
        low = output.lower()
        if ("not logged in" in low or "please log in" in low or "grok login" in low
                or "unauthorized" in low or "authenticate" in low) and proc.returncode != 0:
            banner = (
                "⛔ C1-GROK LANE NOT ACTIVATED — Grok CLI is not signed in.\n"
                "Owner one-time step: run `grok login` (browser OAuth, SuperGrok account), "
                "then `python dispatch.py --selftest-grok` must PASS before routing work here.\n\n"
            )
            print("[grok] ⛔ Not authenticated — run `grok login`.", flush=True)
            return 75, banner + output
        if _looks_like_quota_exhaustion(output, proc.returncode):
            banner = (
                "⛔ C1-GROK LANE DOWN — SuperGrok usage limit appears exhausted.\n"
                "Orchestrator: re-route this P-number to native C1 (Agent tool); "
                "mark the lane DOWN on the board until the quota resets.\n\n"
            )
            print("[grok] ⛔ Usage limit detected — re-route to native C1.", flush=True)
            return 75, banner + output
        return proc.returncode, output
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") if isinstance(e.stdout, str) else ""
        return 1, f"TIMEOUT after {timeout}s.\n{partial}"


def _dispatch_grok(p_number, prompt_path, dry_run, timeout):
    """Dispatch flow for the C1-GROK lane."""
    bootstrap = build_cursor_bootstrap(p_number, prompt_path)
    git_before = git_status_porcelain(REPO_ROOT)
    if dry_run:
        try:
            grok_cmd = find_grok_cmd()
            print(f"\n[dispatch] DRY-RUN — would execute:\n  {grok_cmd} "
                  f"--always-approve --output-format plain -p <bootstrap>")
        except FileNotFoundError as e:
            print(f"\n[dispatch] DRY-RUN — grok NOT available: {e}")
        print(f"\n[dispatch] Bootstrap message:\n{bootstrap}")
        return 0
    started = datetime.now(timezone.utc)
    print(f"\n[dispatch] Invoking grok at {started.isoformat()} …  Timeout: {timeout}s")
    print("-" * 60)
    exit_code, output = run_via_grok_cli(bootstrap, timeout)
    finished = datetime.now(timezone.utc)
    print("-" * 60)
    print(f"[dispatch] Finished at {finished.isoformat()}, exit code: {exit_code}")
    git_after = git_status_porcelain(REPO_ROOT)
    return_path = write_return_file(
        p_number=p_number, prompt_path=prompt_path, model_id="build-cli",
        provider_id="grok", started=started, finished=finished,
        exit_code=exit_code, output=output, git_before=git_before, git_after=git_after,
    )
    print(f"[dispatch] Return file written: {return_path}")
    tick_dispatch_board(p_number)
    return exit_code


def cmd_selftest_grok(timeout: int) -> int:
    """PONG round-trip through the Grok CLI to verify the lane works."""
    PONG = ("Reply with the single word PONG and do nothing else. "
            "Do not use any tools, do not read or edit any files.")
    print("[selftest-grok] Sending PONG to grok …")
    print("-" * 60)
    started = datetime.now(timezone.utc)
    try:
        exit_code, output = run_via_grok_cli(PONG, timeout)
    except FileNotFoundError as e:
        print(f"[selftest-grok] FAIL — {e}", file=sys.stderr)
        return 1
    finished = datetime.now(timezone.utc)
    print("-" * 60)
    print(f"[selftest-grok] Finished in {(finished-started).total_seconds():.1f}s, "
          f"exit code: {exit_code}")
    print(f"[selftest-grok] Output:\n{output[:1000]}")
    stdout_part = output.split("\n\n--- STDERR ---\n")[0]
    if exit_code == 0 and "PONG" in stdout_part.upper():
        print("[selftest-grok] PASS — PONG received.")
        return 0
    print("[selftest-grok] FAIL — PONG not detected.\n"
          "  Checklist: (1) `grok login` done (browser OAuth, SuperGrok account)?\n"
          "  (2) SuperGrok tier covers the CLI beta (Heavy / X Premium Plus)?\n"
          "  (3) flags drifted? run: grok --help and check -p / --always-approve.",
          file=sys.stderr)
    return 1
def cmd_selftest_cursor(timeout: int) -> int:
    """PONG round-trip through the Cursor CLI to verify the lane works."""
    PONG_MESSAGE = ("Reply with the single word PONG and do nothing else. "
                    "Do not use any tools, do not read or edit any files.")
    print("[selftest-cursor] Sending PONG to cursor-agent …")
    print("-" * 60)
    started = datetime.now(timezone.utc)
    try:
        exit_code, output = run_via_cursor_cli(PONG_MESSAGE, timeout)
    except FileNotFoundError as e:
        print(f"[selftest-cursor] FAIL — {e}", file=sys.stderr)
        return 1
    finished = datetime.now(timezone.utc)
    print("-" * 60)
    elapsed = (finished - started).total_seconds()
    print(f"[selftest-cursor] Finished in {elapsed:.1f}s, exit code: {exit_code}")
    print(f"[selftest-cursor] Output:\n{output[:1000]}")
    # Require a clean exit AND the token in stdout (stderr is appended after
    # the '--- STDERR ---' marker; error dumps can coincidentally contain it).
    stdout_part = output.split("\n\n--- STDERR ---\n")[0]
    if exit_code == 0 and "PONG" in stdout_part.upper():
        print("[selftest-cursor] PASS — PONG received.")
        return 0
    print(
        "[selftest-cursor] FAIL — PONG not detected.\n"
        "  Checklist: (1) machine rebooted after Smart App Control was turned\n"
        "  off? (2) authenticated? run: cursor-agent login  (3) flags drifted?\n"
        "  run: cursor-agent --help and check -p / --output-format / --force.",
        file=sys.stderr,
    )
    return 1



def cmd_selftest_gemini(timeout: int) -> int:
    PONG="Reply with the single word PONG and do nothing else. Do not use any tools, do not read or edit any files."
    print("[selftest-gemini] Sending PONG to gemini ...")
    print("-" * 60)
    started=datetime.now(timezone.utc)
    try:
        exit_code,output=run_via_gemini_cli(PONG,timeout,executor=False)
    except FileNotFoundError as e:
        print(f"[selftest-gemini] FAIL - {e}", file=__import__("sys").stderr); return 1
    finished=datetime.now(timezone.utc)
    print("-" * 60)
    elapsed=(finished-started).total_seconds()
    print(f"[selftest-gemini] Finished in {elapsed:.1f}s, exit code: {exit_code}")
    print("[selftest-gemini] Output:")
    print(output[:1000])
    stdout_part=output.split('\n\n--- STDERR ---\n')[0]
    if exit_code==0 and "PONG" in stdout_part.upper(): print("[selftest-gemini] PASS - PONG received."); return 0
    print("[selftest-gemini] FAIL - PONG not detected.",file=__import__("sys").stderr); return 1
def cmd_selftest(timeout: int) -> int:
    """
    Send a harmless PONG round-trip through opencode to verify the pipe works.
    """
    PONG_MESSAGE = "Reply with the single word PONG and do nothing else. Do not use any tools."
    print(f"[selftest] Sending PONG to {C2_PROVIDER_ID}/{C2_MODEL_ID} …")
    print("-" * 60)

    started = datetime.now(timezone.utc)
    exit_code, output = run_via_opencode_api(
        message=PONG_MESSAGE,
        model_id=C2_MODEL_ID,
        provider_id=C2_PROVIDER_ID,
        timeout=timeout,
    )
    finished = datetime.now(timezone.utc)

    print("-" * 60)
    elapsed = (finished - started).total_seconds()
    print(f"[selftest] Finished in {elapsed:.1f}s, exit code: {exit_code}")
    print(f"[selftest] Output:\n{output[:1000]}")

    if "PONG" in output.upper():
        print("[selftest] PASS — PONG received.")
        return 0
    else:
        print(
            "[selftest] WARN — PONG not detected in output.\n"
            "  This may indicate the agent responded but output capture is incomplete,\n"
            "  or the opencode/deepseek model is unavailable/not authenticated.\n"
            "  Check the SSE events above for session.idle confirmation.",
            file=sys.stderr,
        )
        return 1


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bari C2 dispatch router — routes P-numbered prompts to DeepSeek via opencode.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "p_number",
        nargs="?",
        help="P-number to dispatch, e.g. P35",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and build the command without executing it.",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="Send a harmless PONG message through opencode to verify the pipe.",
    )
    parser.add_argument(
        "--selftest-cursor",
        action="store_true",
        help="Send a harmless PONG through the Cursor CLI (C1-CURSOR lane).",
    )
    parser.add_argument(
        "--selftest-gemini",
        action="store_true",
        help="Send a harmless PONG through the Gemini CLI (C1-GEMINI lane).",
    )
    parser.add_argument(
        "--selftest-grok",
        action="store_true",
        help="Send a harmless PONG through the Grok CLI (C1-GROK lane).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds for the opencode invocation (default: {DEFAULT_TIMEOUT}).",
    )

    args = parser.parse_args()

    if args.selftest:
        sys.exit(cmd_selftest(args.timeout))

    if args.selftest_cursor:
        sys.exit(cmd_selftest_cursor(args.timeout))

    if args.selftest_gemini:
        sys.exit(cmd_selftest_gemini(args.timeout))

    if args.selftest_grok:
        sys.exit(cmd_selftest_grok(args.timeout))

    if not args.p_number:
        parser.error("p_number is required unless --selftest is used.")

    sys.exit(cmd_dispatch(args.p_number, dry_run=args.dry_run, timeout=args.timeout))


if __name__ == "__main__":
    main()
