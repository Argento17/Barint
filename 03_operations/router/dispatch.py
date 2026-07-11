r"""
dispatch.py — Bari Capability Router v5 (TASK-583)
====================================================
Implements `01_framework/operations/capability_router_v5.md` LITERALLY.

**That document is law.** It supersedes Router v4.2 (BAND=FUNCTION) and every prior
lane/model memory that conflicts with it. If this file and the doc ever disagree, the
doc wins — fix the code, not the doc (the doc changes only on an explicit owner ruling).
`--selftest-table` asserts the two stay byte-matched on the Layer 1 and Layer 2 tables
(the doc's own operational-appendix law).

What v5 is
----------
A capability-routing library + a selftest CLI:
  - `route(TaskAttributes) -> Capability`   — Layer 1's ordered questions, first match wins.
  - `MODEL_BINDING`                          — Layer 2's model table, runtime-usable.
  - `resolve_challenge_model(vendor)`        — the cross-vendor CHALLENGE resolver.
  - Lane functions that actually dispatch: `build_heavy`, `build_light`, `grunt_primary`,
    `engineering_research` (all via `codex exec`), `vision_longread` (via `gemini -p`,
    report-only), `challenge_gpt` / `evidence_research_fallback` / `grunt_text_fallback`
    (all via the kept opencode HTTP pipe).

What v5 is NOT
---------------
It is no longer the v4.2 P-number/route-tag dispatcher. `find_prompt_file`,
`parse_route`, `strip_owner_meta`, `ROUTING_POLICY`/`recommend_route`, DISPATCH_BOARD
ticking, and `write_return_file` are RETIRED along with the v4.2 lanes they fed —
Layer 1 routes by structured task attributes ("checkable from the task spec, never a
vibe call"), never by regex-sniffing free text or a `(route: ...)` tag in a prompt
file. `tasks/prompts/*.md` and `tasks/DISPATCH_BOARD.md` are untouched by this script
now; historic P-number prompts are archival. (Known fallout: `.claude/commands/
orchestrate.md` and the `.claude/agents/*.md` files still document the old per-lane
`python dispatch.py PNN (route: <tag>)` usage for the retired v4.2 lanes below — that is
stale as of this rewrite and needs its own fast-follow pass; not done here because it
was not in this task's scope and touches 9 governed docs.)

Kill list (Layer 0 invariant 7 — retired forever, never re-add without an owner ruling)
-----------------------------------------------------------------------------------------
See `capability_router_v5.md` Layer 0 Invariant 7 for the exact, named kill list (three
retired CLI lanes + all anonymous opencode free-proxy models). None of those tools,
their CLIs, their config/auth helpers, or their model ids are referenced anywhere below
by design — this file only names the two vendor-authenticated paths it actually
dispatches through (`codex exec`, `gemini -p`) plus the kept opencode HTTP pipe.

PIN-AT-AUTH convention
-----------------------
`MODEL_BINDING[...]["primary"]` is the literal string `"PIN-AT-AUTH"` for every
Codex-backed capability (BUILD-HEAVY, BUILD-LIGHT, GRUNT, ENGINEERING-RESEARCH) and for
VISION-LONGREAD (Gemini), because:
  - Codex (`codex-cli` 0.144.1, verified 2026-07-10): authenticated via a pay-per-token
    API key — the WRONG billing path. The owner must complete ChatGPT-subscription OAuth
    (`codex login`) before real spend is safe. `resolve_primary_model()` raises
    `ModelNotPinnedError` rather than silently dispatching against the wrong plan.
  - Gemini (`gemini-cli` 0.46.0, verified 2026-07-10): `gemini -p` fails with
    `IneligibleTierError` / `UNSUPPORTED_CLIENT` ("migrate to the Antigravity suite") —
    NOT a simple stale-session issue. A plain re-login on this account's free tier will
    NOT clear it (this is the same wall that caused the 2026-06-18 migration to the
    Antigravity CLI in the v4.2 file this one replaces). Flagging precisely so nobody
    re-tries a plain re-login expecting it to work — see `resolve_primary_model()` and
    `cmd_selftest_gemini()`.
Once the owner completes the real step, replace the placeholder with the exact tier ID
in `MODEL_BINDING` AND in `capability_router_v5.md` footnote 1/2 (doc and code must stay
byte-matched — rerun `--selftest-table`).

Exit code convention (all `--selftest*` flags)
------------------------------------------------
  0  = PASS
  1  = FAIL (a real problem)
  3  = DispatchBusy — another dispatch.py holds the single-instance opencode lock
  75 = EX_TEMPFAIL — external dependency not ready (PIN-AT-AUTH skip, or a clean
       pending-auth failure); not a router bug, nothing to fix in this file

Usage
-----
  python dispatch.py --selftest            # PONG through opencode (openai/gpt-5.4-mini-fast)
  python dispatch.py --selftest-codex       # PONG through `codex exec`; skipped while PIN-AT-AUTH
  python dispatch.py --selftest-gemini      # stdout-token PONG through `agy --print`
  python dispatch.py --selftest-table       # doc<->code byte-match assertion
  python dispatch.py --selftest-route       # route() fixture battery
  python dispatch.py --selftest --timeout 300   # override the shared timeout

Rules (unchanged from v4.2)
-----------------------------
- Only touches: 03_operations/router/, its own telemetry directory.
- No network beyond what opencode/codex/gemini themselves do.
- No OFF (Open Food Facts) anything, ever.
- Never `danger-full-access` for any Codex sandbox, ever (Layer 0 law).
"""

from __future__ import annotations

import argparse
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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 output on Windows so Unicode characters (arrows, Hebrew, footnote
# superscripts) don't crash the console encoder.
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # C:\Bari
CAPABILITY_ROUTER_DOC = REPO_ROOT / "01_framework" / "operations" / "capability_router_v5.md"
TELEMETRY_V5_LOG = REPO_ROOT / "03_operations" / "router" / "telemetry" / "router_v5_log.jsonl"

DEFAULT_TIMEOUT = 1800  # seconds
GEMINI_HARD_TIMEOUT_SECONDS = 600  # 10-minute hard cap (Layer 2 VISION-LONGREAD fallback trigger)
SERVER_PORT_RANGE = (19000, 19999)


# ── Single-instance guard (Layer 0 hazard: never two dispatch.py in parallel) ────────────────
# The concrete, documented hazard is opencode-specific: every opencode-HTTP call spawns its own
# local `opencode serve`; two concurrent dispatch.py processes racing their own `serve`
# instances cross-contaminate sessions/returns (dispatch_journal.py's own docstring). `codex
# exec` and `gemini -p` are one-shot subprocesses with no shared local server, so they are not
# in scope for this lock — locking them would add friction with no matching hazard. If the
# durability module is unavailable for any reason, fall back to a no-op context manager so the
# router never depends on it to function; the guard is defense in depth, not a hard dependency.
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agentos"))
    from dispatch_journal import dispatch_lock, DispatchBusy  # type: ignore
except Exception:  # noqa: BLE001 — the guard must never be why the router fails to import
    class DispatchBusy(RuntimeError):
        """Fallback stand-in when dispatch_journal is unavailable — never actually raised."""

    from contextlib import contextmanager

    @contextmanager
    def dispatch_lock(*_a, **_kw):
        yield


# ── Generic helpers ──────────────────────────────────────────────────────────

def git_status_porcelain(repo: Path) -> str:
    """Return the output of `git status --porcelain` in `repo`."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def find_free_port(start: int = SERVER_PORT_RANGE[0], end: int = SERVER_PORT_RANGE[1]) -> int:
    """Find an available TCP port in the given range."""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found in {start}-{end}")


# ============================================================================
# LAW TRANSCRIPTION — capability_router_v5.md Layer 1 + Layer 2, verbatim.
# `--selftest-table` parses the .md file itself and asserts these two constants
# byte-match its Layer 1 / Layer 2 markdown tables. Edit the .md first (owner
# ruling required), then mirror the edit here — never the other way around.
# ============================================================================

# (n, question, capability, exit_criterion) — order IS the FIRST-MATCH-WINS order.
LAYER1_TABLE: list[tuple[int, str, str, str]] = [
    (1, "Output fully determined by written rules, validator exists?", "DETERMINISTIC",
     "Validator exit 0"),
    (2, "Explicit strategist consultation? (owner-invoked /stf, or an owner-ordered strategist debate/second-strategist opinion)", "STRATEGY-CONSULT",
     "Verdict memo: positions, cruxes, converged recommendation, dissent recorded honestly"),
    (3, "Needs decomposition, architecture, or ambiguous scope?", "PLANNING",
     "Written spec with acceptance criteria + the re-routing decision for the implementation"),
    (4, "Produces consumer-facing Hebrew copy?", "CONTENT",
     "Copy validators pass AND both gates signed, sha256-pinned"),
    (5, "Coding with ANY complexity signal (checklist below)?", "BUILD-HEAVY",
     "Builds clean, tests pass, reviewed diff, return contract validates"),
    (6, "Coding with NO complexity signal?", "BUILD-LIGHT", "Same as BUILD-HEAVY"),
    (7, "Mechanical non-code work (renames, fills, conversions)?", "GRUNT",
     "Re-verified by validator/orchestrator; zero unexplained diffs"),
    (8, "Evidence research (papers, regulation, government sources, nutrition science, "
        "competitors)?", "EVIDENCE-RESEARCH",
     "Every claim carries a source; citations pass verify_citations.py"),
    (9, "Engineering research (GitHub, libraries, frameworks, APIs, implementation patterns)?",
     "ENGINEERING-RESEARCH",
     "Recommendation names exact versions + licenses + a working proof snippet"),
    (10, "Bulk one-pass reading, or judging images / rendered pages?", "VISION-LONGREAD",
     "Structured report produced (only artifact type accepted)"),
    (11, "Scoring or nutrition philosophy?", "DOMAIN-JUDGMENT",
     "Reasoned recommendation citing the governing framework docs"),
    (12, "Needs an independent second opinion (or follows any delivery above)?", "CHALLENGE",
     "Verdict with evidence, produced cross-vendor per Invariant 3"),
    (13, "Anything else", "GENERAL", "Return contract validates"),
]

# (capability, primary_exact, fallback_exact, pipe, fallback_trigger) — raw doc prose,
# byte-for-byte, INCLUDING markdown (backticks, bold, footnote superscripts). This is the
# doc-sync copy; MODEL_BINDING (below) holds the clean, runtime-usable derivative.
LAYER2_TABLE: list[tuple[str, str, str, str, str]] = [
    ("PLANNING", "claude-fable-5", "claude-opus-4-8", "Main chat / Plan agent",
     "Model unavailable"),
    ("CONTENT", "claude-fable-5", "claude-sonnet-5", "Content Agent, pinned",
     "Spawn failure or 2 consecutive rejected drafts"),
    ("BUILD-HEAVY", "codex gpt-5.6-terra¹",
     "claude-sonnet-5 (Frontend/Data agent)",
     "`codex exec` in a worktree, sandbox `workspace-write`",
     "Nonzero exit, empty diff, sandbox refusal, or auth pending"),
    ("BUILD-LIGHT", "codex gpt-5.6-terra¹", "claude-sonnet-5 agent", "same",
     "same"),
    ("STRATEGY-CONSULT", "codex gpt-5.6-sol via `codex exec` READ-ONLY sandbox (the Claude side of the debate is the orchestrator session itself = Fable 5)",
     "fable-only debate (degraded: cross-vendor lost - flag it)",
     "`codex exec`, sandbox `read-only`", "API/CLI error or auth pending"),
    ("GRUNT", "codex gpt-5.6-luna¹", "claude-haiku-4-5 (Agent tool)",
     "`codex exec`, sandbox `workspace-write`; deliberately cross-vendor fallback",
     "API/CLI error, or any output failing its validator once"),
    ("EVIDENCE-RESEARCH", "gpt-5.5 + web search", "Claude Research Agent (sonnet pin)",
     "Codex web-search config / opencode API", "API error or timeout 120s"),
    ("ENGINEERING-RESEARCH", "codex gpt-5.6-terra + web search¹",
     "Claude Research Agent (sonnet pin)", "`codex exec -c tools.web_search=true`, read-only sandbox", "same"),
    ("VISION-LONGREAD", "Gemini 3.1 Pro (High) via agy²",
     "claude-sonnet-5 subagent reading screenshots",
     "`agy --print` headless, report-only",
     "CLI hang > 10 min, crash, or empty output"),
    ("DOMAIN-JUDGMENT", "claude-fable-5", "claude-opus-4-8", "Nutrition/Product agents, pinned",
     "Spawn failure"),
    ("CHALLENGE",
     "claude-opus-4-8 **when producer was Codex/GPT** · gpt-5.5-pro **when producer was "
     "Claude or Gemini**",
     "the other one", "Agent tool (opus pin) / opencode API", "Producer-vendor outage"),
    ("GENERAL", "claude-sonnet-5 (explicit pin)", "claude-haiku-4-5 for trivial", "Agent tool",
     "Spawn failure"),
]


# ============================================================================
# ROUTER CORE — route(TaskAttributes) -> Capability
# ============================================================================

@dataclass
class TaskAttributes:
    """Structured answers to the Layer 1 ordered questions. Every field is a named
    boolean/str the CALLER sets from the task spec — "checkable from the task spec,
    never a vibe call" (capability_router_v5.md, complexity checklist). `route()` asks
    them in doc order and returns on the first True: Layer 1's "FIRST MATCH WINS".
    """
    # Q1 — DETERMINISTIC
    deterministic_validator_exists: bool = False
    # Explicit owner invocation only; never inferred.
    strategist_consult: bool = False
    # Q2 — PLANNING (sits above ALL implementation; an ambiguous build never reaches a
    # builder directly)
    needs_planning: bool = False
    # Q3 — CONTENT
    consumer_hebrew_copy: bool = False
    # Q4/Q5 — BUILD-HEAVY / BUILD-LIGHT. One gate (is this coding at all?), then the
    # complexity checklist below splits it. Named booleans per the task spec — never a
    # vibe call:
    is_coding: bool = False
    cross_module: bool = False   # Touches >= 2 modules/packages
    migration: bool = False      # Any migration (schema, data, framework)
    refactor: bool = False       # A refactor intended to preserve behavior
    ui_plus_data: bool = False   # A feature spanning UI + data layers
    over_one_day: bool = False   # PLANNING estimated it above ~1 day
    # Q6 — GRUNT
    mechanical: bool = False
    # Q7 — EVIDENCE-RESEARCH
    evidence_research: bool = False
    # Q8 — ENGINEERING-RESEARCH
    engineering_research: bool = False
    # Q9 — VISION-LONGREAD
    vision_longread: bool = False
    # Q10 — DOMAIN-JUDGMENT
    domain_judgment: bool = False
    # Q11 — CHALLENGE
    needs_challenge: bool = False
    producer_vendor: str | None = None  # feeds resolve_challenge_model() when needs_challenge


def has_complexity_signal(attrs: TaskAttributes) -> bool:
    """Complexity checklist (Layer 1 Q4 note): ANY single signal routes BUILD-HEAVY."""
    return any((attrs.cross_module, attrs.migration, attrs.refactor,
                attrs.ui_plus_data, attrs.over_one_day))


def route(attrs: TaskAttributes) -> str:
    """THE router. Implements Layer 1's ordered questions literally — first match wins.
    Returns a Capability name (a LAYER1_TABLE capability / a MODEL_BINDING key)."""
    if attrs.deterministic_validator_exists:       # Q1
        return "DETERMINISTIC"
    if attrs.strategist_consult:                   # Q2
        return "STRATEGY-CONSULT"
    if attrs.needs_planning:                       # Q3
        return "PLANNING"
    if attrs.consumer_hebrew_copy:                 # Q4
        return "CONTENT"
    if attrs.is_coding:                             # Q5 / Q6
        return "BUILD-HEAVY" if has_complexity_signal(attrs) else "BUILD-LIGHT"
    if attrs.mechanical:                            # Q7
        return "GRUNT"
    if attrs.evidence_research:                     # Q8
        return "EVIDENCE-RESEARCH"
    if attrs.engineering_research:                  # Q9
        return "ENGINEERING-RESEARCH"
    if attrs.vision_longread:                       # Q10
        return "VISION-LONGREAD"
    if attrs.domain_judgment:                       # Q11
        return "DOMAIN-JUDGMENT"
    if attrs.needs_challenge:                       # Q12
        return "CHALLENGE"
    return "GENERAL"                                 # Q13


def resolve_challenge_model(producer_vendor: str | None) -> tuple[str, str]:
    """Cross-vendor CHALLENGE resolver (Layer 2 CHALLENGE row + Layer 0 Invariant 3:
    whoever challenges is from a different company than whoever produced). Returns
    (primary_challenger, fallback_challenger).

    claude-opus-4-8 challenges when the producer was Codex/GPT (OpenAI family);
    gpt-5.5-pro challenges when the producer was Claude or Gemini. The doc's fallback is
    "the other one" — note that for an OpenAI-family producer, the fallback
    (gpt-5.5-pro) is SAME-VENDOR as the producer; that degradation is only acceptable on
    the documented trigger ("Producer-vendor outage", i.e. the cross-vendor challenger
    itself is unreachable) and MUST be logged (was_fallback=True) so it is auditable,
    never silent — see `challenge_gpt(..., was_fallback=...)`.
    """
    openai_family = {"codex", "gpt", "openai", "gpt-5.5", "gpt-5.5-pro"}
    v = (producer_vendor or "").strip().lower()
    if v in openai_family:
        return "claude-opus-4-8", "gpt-5.5-pro"
    return "gpt-5.5-pro", "claude-opus-4-8"  # claude / gemini / unknown producer


# ============================================================================
# MODEL_BINDING — Layer 2, runtime-usable derivative of LAYER2_TABLE.
# ============================================================================

class ModelNotPinnedError(RuntimeError):
    """Raised when a MODEL_BINDING primary is still the PIN-AT-AUTH placeholder — the
    caller tried to dispatch real work through an unpinned lane. Layer 2 footnotes 1/2
    name the exact owner step; resolve_primary_model() repeats it so it is actionable
    from a stack trace alone (Layer 0 Invariant 5: fail loudly, never silently
    downgrade)."""


MODEL_BINDING: dict[str, dict[str, str]] = {
    "PLANNING": {
        "primary": "claude-fable-5", "fallback": "claude-opus-4-8",
        "pipe": "Main chat / Plan agent", "fallback_trigger": "Model unavailable",
    },
    "CONTENT": {
        "primary": "claude-fable-5", "fallback": "claude-sonnet-5",
        "pipe": "Content Agent, pinned",
        "fallback_trigger": "Spawn failure or 2 consecutive rejected drafts",
    },
    "BUILD-HEAVY": {
        "primary": "gpt-5.6-terra", "fallback": "claude-sonnet-5",
        "pipe": "codex exec in a worktree, sandbox workspace-write",
        "fallback_trigger": "Nonzero exit, empty diff, sandbox refusal, or auth pending",
    },
    "BUILD-LIGHT": {
        "primary": "gpt-5.6-terra", "fallback": "claude-sonnet-5",
        "pipe": "codex exec in a worktree, sandbox workspace-write",
        "fallback_trigger": "Nonzero exit, empty diff, sandbox refusal, or auth pending",
    },
    "STRATEGY-CONSULT": {
        "primary": "gpt-5.6-sol",
        "fallback": "fable-only debate (degraded: cross-vendor lost - flag it)",
        "pipe": "codex exec, sandbox read-only",
        "fallback_trigger": "API/CLI error or auth pending",
    },
    "GRUNT": {
        "primary": "gpt-5.6-luna", "fallback": "claude-haiku-4-5",
        "pipe": "codex exec, sandbox workspace-write; deliberately cross-vendor fallback",
        "fallback_trigger": "API/CLI error, or any output failing its validator once",
    },
    "EVIDENCE-RESEARCH": {
        "primary": "gpt-5.5", "fallback": "claude-sonnet-5 (Research Agent)",
        "pipe": "Codex web-search config / opencode API",
        "fallback_trigger": "API error or timeout 120s",
    },
    "ENGINEERING-RESEARCH": {
        "primary": "gpt-5.6-terra", "fallback": "claude-sonnet-5 (Research Agent)",
        "pipe": "codex exec --search, read-only sandbox",
        "fallback_trigger": "API error or timeout 120s",
    },
    "VISION-LONGREAD": {
        "primary": "Gemini 3.1 Pro (High)", "fallback": "claude-sonnet-5 (subagent reading screenshots)",
        "pipe": "agy --print headless, report-only",
        "fallback_trigger": "CLI hang > 10 min, crash, or empty output",
    },
    "DOMAIN-JUDGMENT": {
        "primary": "claude-fable-5", "fallback": "claude-opus-4-8",
        "pipe": "Nutrition/Product agents, pinned", "fallback_trigger": "Spawn failure",
    },
    "CHALLENGE": {
        "primary": "claude-opus-4-8 or gpt-5.5-pro (see resolve_challenge_model)",
        "fallback": "the other one",
        "pipe": "Agent tool (opus pin) / opencode API",
        "fallback_trigger": "Producer-vendor outage",
    },
    "GENERAL": {
        "primary": "claude-sonnet-5", "fallback": "claude-haiku-4-5",
        "pipe": "Agent tool", "fallback_trigger": "Spawn failure",
    },
}


def resolve_primary_model(capability: str) -> str:
    """Layer 2 lookup: the primary model id bound to `capability`. Raises
    ModelNotPinnedError (never silently substitutes the fallback) if the primary is
    still a PIN-AT-AUTH placeholder."""
    if capability not in MODEL_BINDING:
        raise KeyError(f"{capability!r} is not a known Capability (see LAYER1_TABLE).")
    primary = MODEL_BINDING[capability]["primary"]
    if primary == "PIN-AT-AUTH":
        if capability == "VISION-LONGREAD":
            owner_step = (
                "`gemini` interactive login (Google OAuth) against an ELIGIBLE Gemini plan. "
                "NOTE (verified 2026-07-10): the currently-configured Google account hits "
                "IneligibleTierError/UNSUPPORTED_CLIENT ('migrate to the Antigravity suite'), "
                "so a plain re-login on the free tier will NOT clear this — the owner must "
                "either put this account on an eligible paid Gemini plan or confirm the router "
                "should target Antigravity instead. See capability_router_v5.md footnote 2, "
                "then `python dispatch.py --selftest-gemini`."
            )
        else:
            owner_step = (
                "ChatGPT-subscription OAuth via `codex login` — confirm with "
                "`codex login status` that it shows a subscription, not an API key "
                "(verified 2026-07-10: authenticated via a pay-per-token API key, the WRONG "
                "billing path). Then read the exact tier id and replace "
                f"MODEL_BINDING[{capability!r}]['primary'] here, and update "
                "capability_router_v5.md footnote 1 to match (doc and code must stay "
                "byte-matched — rerun --selftest-table)."
            )
        raise ModelNotPinnedError(
            f"{capability}: primary model is still the PIN-AT-AUTH placeholder — refusing to "
            f"dispatch. Owner step: {owner_step}"
        )
    return primary


@dataclass
class LaneResult:
    """Structured result from a capability dispatch. Every lane function returns this
    except `vision_longread()`, which returns bare report text per its literal
    report-only contract."""
    exit_code: int
    output: str
    model_used: str
    was_fallback: bool
    trigger: str
    exit_criterion_met: bool


# ============================================================================
# TELEMETRY v5 — one JSON line per dispatch.
# ============================================================================

def log_telemetry_v5(*, task: str, capability: str, model_used: str, was_fallback: bool,
                     trigger: str, exit_criterion_met: bool, event: str = "dispatch_end",
                     duration_s: float | None = None, tokens_used: int | None = None) -> None:
    """Append one JSON line.  Old rows without ``event`` remain valid for readers.
    Never raises — telemetry is best-effort by design and must
    never be why a real dispatch fails."""
    try:
        TELEMETRY_V5_LOG.parent.mkdir(parents=True, exist_ok=True)
        gi = TELEMETRY_V5_LOG.parent / ".gitignore"
        if not gi.exists():
            gi.write_text("# router telemetry — runtime data, not committed\n*\n!.gitignore\n",
                           encoding="utf-8")
        rec = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "task": task,
            "capability": capability,
            "model_used": model_used,
            "was_fallback": bool(was_fallback),
            "trigger": trigger or "",
            "exit_criterion_met": bool(exit_criterion_met),
            "event": event,
        }
        if duration_s is not None:
            rec["duration_s"] = duration_s
        if tokens_used is not None:
            rec["tokens_used"] = tokens_used
        with open(TELEMETRY_V5_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:  # noqa: BLE001 — telemetry is best-effort by design
        print(f"[dispatch] telemetry write failed (non-fatal): {e}", file=sys.stderr)


def log_dispatch_start(*, task: str, capability: str, model_used: str,
                       was_fallback: bool = False) -> None:
    """Record a lane entry before anything that may invoke its external runner."""
    log_telemetry_v5(task=task, capability=capability, model_used=model_used,
                     was_fallback=was_fallback, trigger="", exit_criterion_met=False,
                     event="dispatch_start")


# ============================================================================
# opencode HTTP plumbing — KEPT from v4.2, repointed. opencode is a TUI app; its
# `opencode run` emits nothing over stdout/stderr non-interactively (no TTY in a
# subprocess), so the headless path is the HTTP server:
#   1. Spawn `opencode serve --port PORT`.
#   2. Subscribe to the SSE stream at GET /api/event.
#   3. Create a session via POST /api/session.
#   4. Send the message via POST /session/{id}/message (SSE).
#   5. Collect events until `session.idle`, then tear down.
#   6. Poll GET /api/session/{id}/message for the final assistant message.
# Authenticated models used by this file (via `opencode models`): openai/gpt-5.5-pro
# (CHALLENGE-GPT), openai/gpt-5.5 (EVIDENCE-RESEARCH fallback), openai/gpt-5.4-mini-fast
# falling back to openai/gpt-5.4-mini (GRUNT text-fallback / --selftest).
# ============================================================================

_OPENCODE_EXE = Path(
    r"C:\Users\HP\AppData\Roaming\npm\node_modules\opencode-ai\bin\opencode.exe"
)
if not _OPENCODE_EXE.exists():
    import shutil as _shutil
    _alt = _shutil.which("opencode")
    if _alt and Path(_alt).suffix.lower() == ".exe":
        _OPENCODE_EXE = Path(_alt)


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
    """Reads Server-Sent Events from a streaming HTTP response in a background thread;
    events are accumulated and streamed to console."""

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
        req = urllib.request.Request(self.url, headers={"Accept": "text/event-stream"})
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
                        raw = "".join(event_data)
                        try:
                            evt = json.loads(raw)
                            with self._lock:
                                self.events.append(evt)
                            print(f"[SSE] {evt.get('type', 'unknown')}", flush=True)
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


def run_via_opencode_api(message: str, model_id: str, provider_id: str,
                          timeout: int) -> tuple[int, str]:
    """Dispatch a message to opencode via the headless HTTP API. Returns (exit_code,
    combined_output_text). Wrapped in the single-instance guard (see module header)."""
    with dispatch_lock():
        return _run_via_opencode_api_inner(message, model_id, provider_id, timeout)


def _run_via_opencode_api_inner(message: str, model_id: str, provider_id: str,
                                 timeout: int) -> tuple[int, str]:
    if not _OPENCODE_EXE.exists():
        raise FileNotFoundError(f"opencode executable not found at {_OPENCODE_EXE}.")

    port = find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    serve_proc = subprocess.Popen(
        [str(_OPENCODE_EXE), "serve", "--port", str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(REPO_ROOT),
        text=True, encoding="utf-8", errors="replace",
    )
    print(f"[opencode] Server starting on port {port} (pid={serve_proc.pid})", flush=True)

    output_parts: list[str] = []
    exit_code = 0
    sse_reader: SSEReader | None = None

    try:
        if not _wait_for_server(base_url):
            raise RuntimeError("opencode server did not start in time.")
        print("[opencode] Server ready.", flush=True)

        deadline = time.time() + timeout
        sse_reader = SSEReader(f"{base_url}/api/event", timeout=timeout)
        sse_reader.start()
        time.sleep(0.5)  # give the SSE connection a moment to establish

        session_resp = _api_call(
            base_url, "/api/session", method="POST",
            body={"model": {"id": model_id, "providerID": provider_id}},
        )
        session_id = session_resp["data"]["id"]
        print(f"[opencode] Session created: {session_id}", flush=True)

        msg_url = f"{base_url}/session/{session_id}/message"
        msg_body = json.dumps({"parts": [{"type": "text", "text": message}]}).encode("utf-8")
        msg_req = urllib.request.Request(
            msg_url, data=msg_body, headers={"Content-Type": "application/json"}, method="POST",
        )
        print(f"[opencode] Sending message ({len(message)} chars)...", flush=True)

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

        idle = sse_reader.wait_for_idle(session_id, deadline)
        if not idle:
            print("[opencode] WARNING: session.idle not received before timeout.", flush=True)

        try:
            msg_list = _api_call(base_url, f"/api/session/{session_id}/message")
            for msg in msg_list.get("data", []):
                role = msg.get("role", "")
                for part in (msg.get("parts") or []):
                    if part.get("type") == "text":
                        text = part.get("text", "").strip()
                        if text:
                            output_parts.append(f"[{role}] {text}")
        except Exception as e:
            print(f"[opencode] Could not fetch final messages: {e}", flush=True)

        seen: set[str] = set()
        deduped: list[str] = []
        for p in output_parts:
            if p not in seen:
                seen.add(p)
                deduped.append(p)

        with sse_reader._lock:
            all_events = list(sse_reader.events)

        for evt in reversed(all_events):
            if evt.get("type") in ("message.part.updated", "message.part"):
                part = (evt.get("data") or {}).get("part", {})
                if part.get("type") == "text":
                    text = part.get("text", "").strip()
                    if text and text not in seen:
                        seen.add(text)
                        deduped.insert(0, text)
                        output_parts.append(text)
                    break

        sse_summary = "\n".join(
            f"  {e.get('type', '?')}: {json.dumps(e.get('data', {}))[:200]}" for e in all_events
        )
        combined = "\n".join(deduped) + "\n\n--- SSE Events ---\n" + sse_summary

    except Exception as e:
        print(f"[opencode] ERROR: {e}", flush=True)
        exit_code = 1
        combined = f"ERROR: {e}"

    finally:
        if sse_reader:
            sse_reader.stop()
        try:
            serve_proc.terminate()
            serve_proc.wait(timeout=5)
        except Exception:
            serve_proc.kill()
        print("[opencode] Server stopped.", flush=True)

    return exit_code, combined


# ── opencode-backed capability functions ──────────────────────────────────────

def challenge_gpt(message: str, *, task: str, was_fallback: bool = False,
                   timeout: int = DEFAULT_TIMEOUT) -> LaneResult:
    """CHALLENGE lane, GPT side — pinned openai/gpt-5.5-pro via opencode HTTP. The
    caller runs resolve_challenge_model() first; when it picks gpt-5.5-pro, dispatch
    here. When it picks claude-opus-4-8 instead, that side goes through the orchestrator
    Agent tool, outside this script's reach. Pass was_fallback=True if gpt-5.5-pro is
    being used as the FALLBACK challenger (producer was Codex/GPT, so claude-opus-4-8
    was primary and is unavailable) — Invariant 3 same-vendor-risk must stay auditable.
    """
    log_dispatch_start(task=task, capability="CHALLENGE", model_used="openai/gpt-5.5-pro",
                       was_fallback=was_fallback)
    started = time.monotonic()
    exit_code, output = run_via_opencode_api(message=message, model_id="gpt-5.5-pro",
                                              provider_id="openai", timeout=timeout)
    duration_s = time.monotonic() - started
    ok = exit_code == 0 and bool(output.strip())
    result = LaneResult(exit_code, output, "openai/gpt-5.5-pro", was_fallback,
                         "" if ok else "Producer-vendor outage", ok)
    log_telemetry_v5(task=task, capability="CHALLENGE", model_used=result.model_used,
                      was_fallback=was_fallback, trigger=result.trigger,
                       exit_criterion_met=ok, duration_s=duration_s)
    return result


def evidence_research_fallback(message: str, *, task: str, timeout: int = 120) -> LaneResult:
    """EVIDENCE-RESEARCH fallback pipe — openai/gpt-5.5 via opencode HTTP. Layer 2
    fallback trigger: API error or timeout 120s (default timeout matches the law)."""
    log_dispatch_start(task=task, capability="EVIDENCE-RESEARCH", model_used="openai/gpt-5.5",
                       was_fallback=True)
    started = time.monotonic()
    exit_code, output = run_via_opencode_api(message=message, model_id="gpt-5.5",
                                              provider_id="openai", timeout=timeout)
    duration_s = time.monotonic() - started
    ok = exit_code == 0 and bool(output.strip())
    result = LaneResult(exit_code, output, "openai/gpt-5.5", True,
                         "" if ok else "API error or timeout 120s", ok)
    log_telemetry_v5(task=task, capability="EVIDENCE-RESEARCH", model_used=result.model_used,
                       was_fallback=True, trigger=result.trigger, exit_criterion_met=ok,
                       duration_s=duration_s)
    return result


def grunt_text_fallback(message: str, *, task: str, timeout: int = DEFAULT_TIMEOUT) -> LaneResult:
    """GRUNT text-fallback pipe (non-file, text-only mechanical work) — openai/
    gpt-5.4-mini-fast via opencode HTTP, sub-falling back to openai/gpt-5.4-mini if the
    -fast tier errors."""
    model_id = "gpt-5.4-mini-fast"
    log_dispatch_start(task=task, capability="GRUNT", model_used=f"openai/{model_id}",
                       was_fallback=True)
    started = time.monotonic()
    exit_code, output = run_via_opencode_api(message=message, model_id=model_id,
                                              provider_id="openai", timeout=timeout)
    if exit_code != 0:
        model_id = "gpt-5.4-mini"
        exit_code, output = run_via_opencode_api(message=message, model_id=model_id,
                                                  provider_id="openai", timeout=timeout)
    ok = exit_code == 0 and bool(output.strip())
    result = LaneResult(exit_code, output, f"openai/{model_id}", True,
                         "" if ok else "API/CLI error, or any output failing its validator once",
                         ok)
    log_telemetry_v5(task=task, capability="GRUNT", model_used=result.model_used,
                       was_fallback=True, trigger=result.trigger, exit_criterion_met=ok,
                       duration_s=time.monotonic() - started)
    return result


# ============================================================================
# Codex lane — BUILD-HEAVY / BUILD-LIGHT / GRUNT-primary / ENGINEERING-RESEARCH.
# All via `codex exec`. Sandbox is always explicit and validated against an allow-list —
# Layer 0 law: NEVER `danger-full-access`, regardless of caller input.
# ============================================================================

_CODEX_EXE_DEFAULT = Path(os.environ.get("APPDATA", "")) / "npm" / "codex.cmd"
_CODEX_ALLOWED_SANDBOX = {"read-only", "workspace-write"}
_CODEX_TOKEN_PATTERNS = (
    re.compile(r"\btoken usage\s*[:=]\s*([\d,]+)\b", re.IGNORECASE),
    re.compile(r"\btokens? used\s*[:=]\s*([\d,]+)\b", re.IGNORECASE),
)


def _parse_codex_tokens(output: str) -> int | None:
    """Best-effort extraction from Codex CLI's end-of-run usage summary."""
    try:
        for pattern in _CODEX_TOKEN_PATTERNS:
            match = pattern.search(output or "")
            if match:
                return int(match.group(1).replace(",", ""))
    except Exception:  # noqa: BLE001 — telemetry parsing must never affect a lane
        pass
    return None


def _resolve_codex_cmd() -> Path:
    if _CODEX_EXE_DEFAULT.exists():
        return _CODEX_EXE_DEFAULT
    import shutil as _shutil
    alt = _shutil.which("codex")
    if alt:
        return Path(alt)
    raise FileNotFoundError(
        f"Codex CLI not found at {_CODEX_EXE_DEFAULT} or on PATH. "
        "Install per current OpenAI docs, then `codex login`."
    )


def _run_codex_exec(prompt: str, *, model: str, sandbox: str, cwd: Path, timeout: int,
                     search: bool = False, skip_git_repo_check: bool = False) -> tuple[int, str, int | None]:
    """Low-level `codex exec` invocation.

    CLI-version note (verified 2026-07-10 against codex-cli 0.144.1): `codex exec
    --search` itself errors ("unexpected argument found") — `--search` is currently
    wired only to the top-level interactive `codex` command, not the `exec` subcommand;
    `codex features list` has no stable enabled-by-default web-search feature to
    substitute via --enable either (search_tool/tool_search=removed,
    standalone_web_search=under development, web_search_cached/request=deprecated). This
    function still issues the law-prescribed `--search` flag when `search=True`
    (capability_router_v5.md Layer 2 ENGINEERING-RESEARCH pipe cell, byte-matched by
    --selftest-table) so the LAW and the CODE state the same intent; it will surface
    this exact CLI error if ever actually invoked. Harmless today —
    ENGINEERING-RESEARCH sits behind the same PIN-AT-AUTH gate as every other Codex
    lane, so it cannot dispatch for real until the owner pins a model anyway.
    Re-verify --search against the then-current codex-cli version at pin time (fast-
    follow, not a blocker for TASK-583).
    """
    if sandbox not in _CODEX_ALLOWED_SANDBOX:
        raise ValueError(
            f"sandbox={sandbox!r} is not permitted — Layer 0 law forbids danger-full-access; "
            f"allowed: {sorted(_CODEX_ALLOWED_SANDBOX)}"
        )
    codex_exe = _resolve_codex_cmd()
    cmd = [str(codex_exe), "exec", "-s", sandbox, "-C", str(cwd), "-m", model]
    if skip_git_repo_check:
        cmd.append("--skip-git-repo-check")
    if search:
        cmd += ["-c", "tools.web_search=true"]  # verified 2026-07-10; top-level --search does not exist on `exec`
    # Prompt goes via STDIN, never argv (fix 2026-07-10, first real BUILD-HEAVY dispatch):
    # on Windows `codex` resolves through an npm .cmd shim, and cmd.exe batch argv cannot
    # carry newlines — a multi-line 5-part spec silently truncated to its FIRST LINE and
    # Codex (correctly) refused to act on a one-line spec. `codex exec -` reads the prompt
    # from stdin, which preserves every byte.
    cmd.append("-")
    print(f"[codex] Invoking `codex exec` (sandbox={sandbox}, model={model}, cwd={cwd}, "
          f"prompt via stdin)...", flush=True)
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=timeout, shell=False,
                               input=prompt)
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") if isinstance(e.stdout, str) else ""
        output = f"TIMEOUT after {timeout}s.\n{partial}"
        return 1, output, _parse_codex_tokens(output)
    output = (proc.stdout or "")
    if proc.stderr and proc.stderr.strip():
        output += "\n\n--- STDERR ---\n" + proc.stderr
    return proc.returncode, output, _parse_codex_tokens(output)


def _dispatch_codex_build(capability: str, prompt: str, *, task: str, cwd: Path, sandbox: str,
                           timeout: int, search: bool = False) -> LaneResult:
    model = resolve_primary_model(capability)  # raises ModelNotPinnedError while PIN-AT-AUTH
    git_before = git_status_porcelain(cwd)
    started = time.monotonic()
    exit_code, output, tokens_used = _run_codex_exec(prompt, model=model, sandbox=sandbox,
                                                       cwd=cwd, timeout=timeout, search=search)
    duration_s = time.monotonic() - started
    git_after = git_status_porcelain(cwd)
    empty_diff = sandbox == "workspace-write" and git_before == git_after
    if exit_code != 0:
        trigger = "Nonzero exit"
    elif empty_diff:
        trigger = "empty diff"
    else:
        trigger = ""
    ok = exit_code == 0 and not empty_diff
    result = LaneResult(exit_code, output, model, False, trigger, ok)
    log_telemetry_v5(task=task, capability=capability, model_used=model, was_fallback=False,
                       trigger=trigger, exit_criterion_met=ok, duration_s=duration_s,
                       tokens_used=tokens_used)
    return result


def build_heavy(prompt: str, *, task: str, worktree: Path, timeout: int = DEFAULT_TIMEOUT
                 ) -> LaneResult:
    """BUILD-HEAVY (Layer 1 Q5): coding with any complexity signal. `codex exec`,
    model gpt-5.6-terra, sandbox workspace-write, explicit --cd <worktree>. `worktree` is required — this
    never dispatches against the live tree."""
    log_dispatch_start(task=task, capability="BUILD-HEAVY",
                       model_used=MODEL_BINDING["BUILD-HEAVY"]["primary"])
    return _dispatch_codex_build("BUILD-HEAVY", prompt, task=task, cwd=worktree,
                                  sandbox="workspace-write", timeout=timeout)


def strategist_consult(prompt: str, *, task: str, worktree: Path | None = None,
                       timeout: int = DEFAULT_TIMEOUT) -> LaneResult:
    """STRATEGY-CONSULT (Layer 1 Q2): read-only Sol consultation; stdout is the deliverable.

    This lane never writes. When no worktree is supplied, it runs in an isolated temporary
    directory and explicitly skips Codex's git-repository check.
    """
    capability = "STRATEGY-CONSULT"
    log_dispatch_start(task=task, capability=capability,
                       model_used=MODEL_BINDING[capability]["primary"])
    model = resolve_primary_model(capability)
    started = time.monotonic()
    if worktree is None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            exit_code, output, tokens_used = _run_codex_exec(
                prompt, model=model, sandbox="read-only", cwd=Path(tmp), timeout=timeout,
                skip_git_repo_check=True,
            )
    else:
        exit_code, output, tokens_used = _run_codex_exec(
            prompt, model=model, sandbox="read-only", cwd=worktree, timeout=timeout,
        )
    duration_s = time.monotonic() - started
    ok = exit_code == 0 and bool(output.strip())
    trigger = "" if ok else "API/CLI error or auth pending"
    result = LaneResult(exit_code, output, model, False, trigger, ok)
    log_telemetry_v5(task=task, capability=capability, model_used=model, was_fallback=False,
                     trigger=trigger, exit_criterion_met=ok, duration_s=duration_s,
                     tokens_used=tokens_used)
    return result


def build_light(prompt: str, *, task: str, worktree: Path, timeout: int = DEFAULT_TIMEOUT
                 ) -> LaneResult:
    """BUILD-LIGHT (Layer 1 Q5): coding with no complexity signal. Same pipe as
    BUILD-HEAVY."""
    log_dispatch_start(task=task, capability="BUILD-LIGHT",
                       model_used=MODEL_BINDING["BUILD-LIGHT"]["primary"])
    return _dispatch_codex_build("BUILD-LIGHT", prompt, task=task, cwd=worktree,
                                  sandbox="workspace-write", timeout=timeout)


def grunt_primary(prompt: str, *, task: str, worktree: Path, timeout: int = DEFAULT_TIMEOUT
                   ) -> LaneResult:
    """GRUNT primary (Layer 1 Q6): mechanical non-code work. `codex exec`, sandbox
    workspace-write — deliberately the cheapest Codex tier; the cross-vendor fallback is
    claude-haiku-4-5 (MODEL_BINDING['GRUNT'])."""
    log_dispatch_start(task=task, capability="GRUNT", model_used=MODEL_BINDING["GRUNT"]["primary"])
    return _dispatch_codex_build("GRUNT", prompt, task=task, cwd=worktree,
                                  sandbox="workspace-write", timeout=timeout)


def engineering_research(prompt: str, *, task: str, cwd: Path = REPO_ROOT,
                          timeout: int = DEFAULT_TIMEOUT) -> LaneResult:
    """ENGINEERING-RESEARCH (Layer 1 Q8): GitHub/libraries/frameworks/APIs/
    implementation patterns. `codex exec -c tools.web_search=true`, read-only sandbox — never writes.
    See `_run_codex_exec` docstring for a known --search CLI-version caveat."""
    log_dispatch_start(task=task, capability="ENGINEERING-RESEARCH",
                       model_used=MODEL_BINDING["ENGINEERING-RESEARCH"]["primary"])
    return _dispatch_codex_build("ENGINEERING-RESEARCH", prompt, task=task, cwd=cwd,
                                  sandbox="read-only", timeout=timeout, search=True)


# ============================================================================
# Gemini lane — VISION-LONGREAD only. Report-only: refuses (raises) BEFORE dispatch if
# the prompt reads as a request for code or consumer copy (Layer 0 Prohibition 8:
# "Gemini writes zero consumer copy and zero code — reports only").
# ============================================================================

_GEMINI_EXE_DEFAULT = Path(os.environ.get("APPDATA", "")) / "npm" / "gemini.cmd"

_CODE_OR_COPY_REFUSAL_PATTERN = re.compile(
    r"\b(write|generate|produce|author|create|draft)\b[^.\n]{0,60}"
    r"\b(code|component|function|script|patch|diff|pull\s?request|"
    r"copy|headline|tagline|insight\s?line|row\s?verdict|"
    r"hebrew\s+(?:copy|text|string)|consumer.facing\s+(?:text|copy|string))\b",
    re.IGNORECASE,
)


class GeminiScopeRefusal(RuntimeError):
    """Raised BEFORE any gemini dispatch — Layer 0 Prohibition 8."""


def _refuse_if_code_or_copy_request(prompt: str) -> None:
    m = _CODE_OR_COPY_REFUSAL_PATTERN.search(prompt or "")
    if m:
        raise GeminiScopeRefusal(
            f"VISION-LONGREAD refuses this prompt before dispatch — it reads as a request for "
            f"code or consumer copy ({m.group(0)!r} matched). Layer 0 Prohibition 8: 'Gemini "
            f"writes zero consumer copy and zero code (reports only).' Route code to a BUILD "
            f"lane and copy to CONTENT (Content Agent) instead."
        )


def _resolve_gemini_cmd() -> Path:
    """Antigravity CLI (`agy`) — the ONLY supported Gemini client for this subscription.
    The npm `gemini` CLI is UNSUPPORTED_CLIENT on this account tier (law doc fn.2);
    never fall back to it."""
    agy = Path(os.path.expandvars(r"%LOCALAPPDATA%gyingy.exe"))
    if agy.exists():
        return agy
    import shutil as _shutil
    alt = _shutil.which("agy")
    if alt:
        return Path(alt)
    raise FileNotFoundError(
        f"Antigravity CLI not found at {agy} or on PATH. Reinstall Antigravity, then "
        "verify with: agy models (auth lives in Windows Credential Manager)."
    )


def _run_gemini_cli(prompt: str, *, model: str | None, cwd: Path, timeout: int
                     ) -> tuple[int, str]:
    """Low-level headless `gemini -p` invocation. report-only: caller treats stdout as
    the report. Never passes a PIN-AT-AUTH placeholder as -m; omit -m entirely when
    model is None/placeholder so the CLI's own default is used instead of a nonsense
    flag value."""
    gemini_exe = _resolve_gemini_cmd()
    cmd = [str(gemini_exe)]
    if model and model != "PIN-AT-AUTH":
        cmd += ["--model", model]
    cmd += ["--print", prompt]  # agy 1.1: --print = single-prompt headless; bare -p WITHOUT a value prints help
    env = dict(os.environ)
    hard_timeout = min(timeout, GEMINI_HARD_TIMEOUT_SECONDS)
    print(f"[gemini] Invoking `gemini -p` (cwd={cwd}, hard timeout {hard_timeout}s)...",
          flush=True)
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=hard_timeout,
                               env=env, stdin=subprocess.DEVNULL, shell=False)
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") if isinstance(e.stdout, str) else ""
        return 1, f"TIMEOUT after {hard_timeout}s (10-min hard cap).\n{partial}"
    output = (proc.stdout or "")
    if proc.stderr and proc.stderr.strip():
        output += "\n\n--- STDERR ---\n" + proc.stderr
    return proc.returncode, output


def vision_longread(prompt: str, *, task: str, cwd: Path = REPO_ROOT,
                     timeout: int = GEMINI_HARD_TIMEOUT_SECONDS) -> str:
    """VISION-LONGREAD lane (Layer 1 Q9): bulk one-pass reading, or judging images /
    rendered pages. report-only contract — returns the report TEXT (str), nothing else.
    Refuses BEFORE dispatch (raises GeminiScopeRefusal) if the prompt reads as a request
    for code or consumer copy."""
    log_dispatch_start(task=task, capability="VISION-LONGREAD",
                       model_used=MODEL_BINDING["VISION-LONGREAD"]["primary"])
    _refuse_if_code_or_copy_request(prompt)
    model = resolve_primary_model("VISION-LONGREAD")  # raises ModelNotPinnedError while PIN-AT-AUTH
    started = time.monotonic()
    exit_code, output = _run_gemini_cli(prompt, model=model, cwd=cwd, timeout=timeout)
    duration_s = time.monotonic() - started
    ok = exit_code == 0 and bool(output.strip())
    log_telemetry_v5(task=task, capability="VISION-LONGREAD", model_used=model,
                      was_fallback=False,
                      trigger="" if ok else "CLI hang > 10 min, crash, or empty output",
                       exit_criterion_met=ok, duration_s=duration_s)
    if not ok:
        raise RuntimeError(
            f"VISION-LONGREAD dispatch failed (exit {exit_code}); report text empty or the "
            f"lane errored:\n{output[:1000]}"
        )
    return output


# ============================================================================
# LAW-DOC PARSER — capability_router_v5.md's Layer 1 / Layer 2 markdown tables, for
# --selftest-table's byte-match assertion.
# ============================================================================

def _extract_section_lines(lines: list[str], start_pat: str, end_pat: str) -> list[str]:
    start_idx = None
    for i, ln in enumerate(lines):
        if re.match(start_pat, ln):
            start_idx = i
            break
    if start_idx is None:
        raise ValueError(f"section heading not found: {start_pat!r}")
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if re.match(end_pat, lines[i]):
            end_idx = i
            break
    return lines[start_idx:end_idx]


def _parse_md_table_rows(section_lines: list[str]) -> list[list[str]]:
    """Header + separator + data rows -> data rows only, as lists of stripped cell
    strings (outer pipes discarded)."""
    table_lines = [ln.strip() for ln in section_lines if ln.strip().startswith("|")]
    if len(table_lines) < 2:
        return []
    data_lines = table_lines[2:]  # drop header row + |---|---| separator row
    return [[c.strip() for c in ln.strip("|").split("|")] for ln in data_lines]


def load_law_tables(md_path: Path | None = None) -> tuple[list[list[str]], list[list[str]]]:
    """Parse capability_router_v5.md's Layer 1 and Layer 2 markdown tables into row
    lists — the source of truth --selftest-table checks LAYER1_TABLE/LAYER2_TABLE
    against."""
    md_path = md_path or CAPABILITY_ROUTER_DOC
    lines = md_path.read_text(encoding="utf-8").splitlines()
    layer1_lines = _extract_section_lines(lines, r"^## Layer 1\b", r"^## Layer 2\b")
    layer2_lines = _extract_section_lines(lines, r"^## Layer 2\b", r"^## Operational appendix\b")
    return _parse_md_table_rows(layer1_lines), _parse_md_table_rows(layer2_lines)


# ============================================================================
# SELFTESTS
# ============================================================================

def _rows_equal_report(label: str, code_rows: list[list[str]], doc_rows: list[list[str]]) -> bool:
    ok = code_rows == doc_rows
    if ok:
        print(f"[selftest-table] {label}: {len(code_rows)} rows byte-match "
              f"capability_router_v5.md. OK")
        return True
    print(f"[selftest-table] {label}: MISMATCH", file=sys.stderr)
    for i, (c, d) in enumerate(zip(code_rows, doc_rows)):
        if c != d:
            print(f"  row {i}: code={c!r}", file=sys.stderr)
            print(f"  row {i}:  doc={d!r}", file=sys.stderr)
    if len(code_rows) != len(doc_rows):
        print(f"  row count differs: code={len(code_rows)} doc={len(doc_rows)}", file=sys.stderr)
    return False


def cmd_selftest_table() -> int:
    """Byte-match law (capability_router_v5.md operational appendix): the routing table
    in code must match this document's Layer 1 / Layer 2 tables exactly."""
    try:
        doc_layer1, doc_layer2 = load_law_tables()
    except (OSError, ValueError) as e:
        print(f"[selftest-table] FAIL — could not load/parse {CAPABILITY_ROUTER_DOC}: {e}",
              file=sys.stderr)
        return 1

    code_layer1 = [[str(n), q, cap, exit_c] for (n, q, cap, exit_c) in LAYER1_TABLE]
    code_layer2 = [list(row) for row in LAYER2_TABLE]

    ok1 = _rows_equal_report("Layer 1", code_layer1, doc_layer1)
    ok2 = _rows_equal_report("Layer 2", code_layer2, doc_layer2)
    ok = ok1 and ok2
    print(f"[selftest-table] {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


@dataclass
class RouteFixture:
    name: str
    attrs: TaskAttributes
    expected: str


ROUTE_FIXTURES: list[RouteFixture] = [
    RouteFixture("deterministic_validator",
                 TaskAttributes(deterministic_validator_exists=True), "DETERMINISTIC"),
    RouteFixture("explicit_owner_strategist_consult",
                 TaskAttributes(strategist_consult=True, needs_planning=True, is_coding=True),
                 "STRATEGY-CONSULT"),
    RouteFixture("ambiguous_build_request",
                 TaskAttributes(needs_planning=True, is_coding=True, cross_module=True),
                 "PLANNING"),  # PLANNING must win even though complexity signals are present
    RouteFixture("hebrew_copy_task", TaskAttributes(consumer_hebrew_copy=True), "CONTENT"),
    RouteFixture("two_module_refactor",
                 TaskAttributes(is_coding=True, cross_module=True, refactor=True),
                 "BUILD-HEAVY"),
    RouteFixture("single_file_bugfix", TaskAttributes(is_coding=True), "BUILD-LIGHT"),
    RouteFixture("one_file_rename", TaskAttributes(mechanical=True), "GRUNT"),
    RouteFixture("nutrition_evidence_lookup",
                 TaskAttributes(evidence_research=True), "EVIDENCE-RESEARCH"),
    RouteFixture("library_api_lookup",
                 TaskAttributes(engineering_research=True), "ENGINEERING-RESEARCH"),
    RouteFixture("bulk_screenshot_judging",
                 TaskAttributes(vision_longread=True), "VISION-LONGREAD"),
    RouteFixture("sodium_scoring_philosophy",
                 TaskAttributes(domain_judgment=True), "DOMAIN-JUDGMENT"),
    RouteFixture("second_opinion_on_codex_diff",
                 TaskAttributes(needs_challenge=True, producer_vendor="codex"), "CHALLENGE"),
    RouteFixture("offbeat_task_no_signal", TaskAttributes(), "GENERAL"),
    RouteFixture("deterministic_beats_everything",
                 TaskAttributes(deterministic_validator_exists=True, needs_planning=True,
                                 is_coding=True, mechanical=True),
                 "DETERMINISTIC"),  # ordering proof: Q1 beats Q2/Q4/Q6
    RouteFixture("build_beats_challenge_when_both_set",
                 TaskAttributes(is_coding=True, needs_challenge=True),
                 "BUILD-LIGHT"),  # ordering proof: Q4/Q5 beats Q11
]


def cmd_selftest_route() -> int:
    """Run the route() fixture battery and assert expected Capabilities."""
    ok = True
    for fx in ROUTE_FIXTURES:
        got = route(fx.attrs)
        status = "ok" if got == fx.expected else "WRONG"
        if got != fx.expected:
            ok = False
        print(f"[selftest-route] {fx.name:<34} expected={fx.expected:<14} got={got:<14} "
              f"{status}")
    print(f"[selftest-route] {'PASS' if ok else 'FAIL'} ({len(ROUTE_FIXTURES)} fixtures)")
    return 0 if ok else 1


def cmd_selftest(timeout: int) -> int:
    """Send a harmless PONG round-trip through opencode (openai/gpt-5.4-mini-fast — the
    GRUNT text-fallback model) to verify the opencode HTTP pipe works end to end."""
    PONG_MESSAGE = "Reply with the single word PONG and do nothing else. Do not use any tools."
    model_id, provider_id = "gpt-5.4-mini-fast", "openai"
    print(f"[selftest] Sending PONG to {provider_id}/{model_id} (opencode HTTP)...")
    print("-" * 60)
    started = datetime.now(timezone.utc)
    try:
        exit_code, output = run_via_opencode_api(message=PONG_MESSAGE, model_id=model_id,
                                                  provider_id=provider_id, timeout=timeout)
    except DispatchBusy as e:
        print(f"[selftest] ABORTED — {e}", file=sys.stderr)
        return 3
    finished = datetime.now(timezone.utc)
    print("-" * 60)
    print(f"[selftest] Finished in {(finished - started).total_seconds():.1f}s, "
          f"exit code: {exit_code}")
    print(f"[selftest] Output:\n{output[:1000]}")
    if "PONG" in output.upper():
        print("[selftest] PASS — PONG received.")
        return 0
    print(
        "[selftest] WARN — PONG not detected in output.\n"
        "  This may indicate the agent responded but output capture is incomplete,\n"
        "  or openai/gpt-5.4-mini-fast is unavailable/not authenticated via opencode.\n"
        "  Check the SSE events above for session.idle confirmation.",
        file=sys.stderr,
    )
    return 1


def cmd_selftest_codex(timeout: int) -> int:
    """PONG round-trip via `codex exec` — SKIPPED (not FAILED, exit 75/EX_TEMPFAIL)
    while BUILD-LIGHT's primary is still the PIN-AT-AUTH placeholder, so this never
    spends against the wrong (pay-per-token) billing path. Once pinned, this actually
    dispatches a real PONG (sandbox read-only, so it cannot write anything)."""
    print("[selftest-codex] Checking MODEL_BINDING['BUILD-LIGHT'] pin state before "
          "dispatching...")
    try:
        model = resolve_primary_model("BUILD-LIGHT")
    except ModelNotPinnedError as e:
        print(f"[selftest-codex] SKIPPED (EX_TEMPFAIL) — {e}")
        return 75
    print(f"[selftest-codex] Pinned model: {model}. Sending PONG via `codex exec`...")
    print("-" * 60)
    PONG = ("Reply with the single word PONG and do nothing else. Do not use any tools, "
            "do not read or edit any files.")
    started = datetime.now(timezone.utc)
    try:
        exit_code, output, _tokens_used = _run_codex_exec(PONG, model=model, sandbox="read-only",
                                                           cwd=REPO_ROOT, timeout=timeout)
    except FileNotFoundError as e:
        print(f"[selftest-codex] FAIL — {e}", file=sys.stderr)
        return 1
    finished = datetime.now(timezone.utc)
    print("-" * 60)
    print(f"[selftest-codex] Finished in {(finished - started).total_seconds():.1f}s, "
          f"exit code: {exit_code}")
    print(f"[selftest-codex] Output:\n{output[:1000]}")
    if exit_code == 0 and "PONG" in output.upper():
        print("[selftest-codex] PASS — PONG received.")
        return 0
    print("[selftest-codex] FAIL — PONG not detected.", file=sys.stderr)
    return 1


def cmd_selftest_gemini(timeout: int) -> int:
    """Stdout-token PONG through the REAL lane runner (`_run_gemini_cli` -> `agy --print`).
    agy 1.1 print mode returns the model response on stdout (with occasional narration
    lines), so a unique token containment check is the signal; the old sentinel-file
    design targeted the retired npm gemini client and is obsolete (TASK-585). Clean
    failures only: never a hang (10-min hard cap), never an uncaught traceback."""
    import uuid
    token = "GEMINI_OK_" + uuid.uuid4().hex[:8]
    msg = f"Reply with exactly one line containing only this token: {token}"
    hard_timeout = min(timeout, GEMINI_HARD_TIMEOUT_SECONDS)
    print(f"[selftest-gemini] Probing the VISION-LONGREAD pipe (agy --print), hard timeout "
          f"{hard_timeout}s...")
    print("-" * 60)
    try:
        model = MODEL_BINDING["VISION-LONGREAD"]["primary"]
        started = datetime.now(timezone.utc)
        exit_code, output = _run_gemini_cli(msg, model=model, cwd=REPO_ROOT,
                                             timeout=hard_timeout)
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    except FileNotFoundError as e:
        print(f"[selftest-gemini] FAIL — {e}", file=sys.stderr)
        return 1
    print("-" * 60)
    print(f"[selftest-gemini] Finished in {elapsed:.1f}s, exit code {exit_code}")
    if token in output:
        print(f"[selftest-gemini] PASS — agy answered through the lane runner "
              f"(model pin: {model}).")
        return 0
    print(f"[selftest-gemini] FAIL — token not in agy output. Tail:\n{output[-1500:]}",
          file=sys.stderr)
    return 1


def cmd_selftest_telemetry() -> int:
    """Offline telemetry check: mocked Codex runner and a temporary JSONL log only."""
    import tempfile

    global TELEMETRY_V5_LOG, _run_codex_exec, git_status_porcelain
    original_log = TELEMETRY_V5_LOG
    original_runner = _run_codex_exec
    original_git_status = git_status_porcelain
    with tempfile.TemporaryDirectory() as tmp:
        TELEMETRY_V5_LOG = Path(tmp) / "router_v5_log.jsonl"
        try:
            _run_codex_exec = lambda *_a, **_kw: (0, "done\nToken usage: 1,234", 1234)
            # Make the second status observation differ without invoking git.
            def fake_status(_cwd: Path) -> str:
                fake_status.called = not fake_status.called
                return "before" if fake_status.called else "after"
            fake_status.called = False
            git_status_porcelain = fake_status
            build_light("offline telemetry test", task="TASK-589-telemetry", worktree=Path(tmp))
            rows = [json.loads(line) for line in TELEMETRY_V5_LOG.read_text(encoding="utf-8").splitlines()]
            start_ok = len(rows) == 2 and rows[0].get("event") == "dispatch_start"
            end_ok = (rows[-1].get("event") == "dispatch_end" and
                      isinstance(rows[-1].get("duration_s"), float) and
                      rows[-1].get("tokens_used") == 1234)

            _run_codex_exec = lambda *_a, **_kw: (_ for _ in ()).throw(RuntimeError("mock crash"))
            try:
                build_light("offline crash test", task="TASK-589-crash", worktree=Path(tmp))
            except RuntimeError:
                pass
            rows = [json.loads(line) for line in TELEMETRY_V5_LOG.read_text(encoding="utf-8").splitlines()]
            crash_start_ok = rows[-1].get("task") == "TASK-589-crash" and rows[-1].get("event") == "dispatch_start"
            token_parse_ok = _parse_codex_tokens("Token usage: 9,876") == 9876
            ok = start_ok and end_ok and crash_start_ok and token_parse_ok
            print("[selftest-telemetry] " + ("PASS" if ok else "FAIL") +
                  " — start row, end duration/tokens, and pre-run crash entry")
            return 0 if ok else 1
        finally:
            TELEMETRY_V5_LOG = original_log
            _run_codex_exec = original_runner
            git_status_porcelain = original_git_status


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bari Capability Router v5 — implements capability_router_v5.md (law).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--selftest", action="store_true",
                         help="PONG round-trip through opencode (openai/gpt-5.4-mini-fast).")
    parser.add_argument("--selftest-codex", action="store_true",
                         help="PONG round-trip through `codex exec`; skipped while PIN-AT-AUTH.")
    parser.add_argument("--selftest-gemini", action="store_true",
                         help="Stdout-token PONG through `agy --print` via the real lane runner.")
    parser.add_argument("--selftest-table", action="store_true",
                         help="Assert LAYER1_TABLE/LAYER2_TABLE byte-match "
                              "capability_router_v5.md.")
    parser.add_argument("--selftest-route", action="store_true",
                         help="Run the route() fixture battery and assert expected "
                               "capabilities.")
    parser.add_argument("--selftest-telemetry", action="store_true",
                        help="Offline mocked-runner check for start/end telemetry rows.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                         help=f"Timeout in seconds for CLI/HTTP selftests "
                              f"(default: {DEFAULT_TIMEOUT}).")
    args = parser.parse_args()

    if args.selftest_table:
        sys.exit(cmd_selftest_table())
    if args.selftest_route:
        sys.exit(cmd_selftest_route())
    if args.selftest_telemetry:
        sys.exit(cmd_selftest_telemetry())
    if args.selftest:
        sys.exit(cmd_selftest(args.timeout))
    if args.selftest_codex:
        sys.exit(cmd_selftest_codex(args.timeout))
    if args.selftest_gemini:
        sys.exit(cmd_selftest_gemini(args.timeout))

    parser.error("no action given — pass one of --selftest / --selftest-codex / "
                  "--selftest-gemini / --selftest-table / --selftest-route / --selftest-telemetry.")


if __name__ == "__main__":
    main()
