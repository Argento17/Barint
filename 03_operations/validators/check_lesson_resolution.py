#!/usr/bin/env python3
r"""
check_lesson_resolution.py — lesson-resolution CLOSE gate (TASK-604)
======================================================================

Contract: 01_framework/operations/lesson_resolution_contract_v1.md
Source:   STF verdict memo 01_framework/governance/stf_memos/2026-07-11_lesson-resolution-mechanism.md

Bari lessons currently die as passive prose. This gate makes a `TASK-NNN` CLOSE transition
BLOCK unless the task carries a `lesson_trigger` and — for any non-`none` trigger — exactly ONE
`lesson_outcome` whose referent is machine-verified (a tracked artifact exists AND a named
validator/test command actually passes; a generated follow-up task actually exists and points
back; an owner-decision ref is actually recorded). This is the ONE validator; it is invoked by
BOTH the close hook (`.claude/hooks/guard-lesson-on-close.ps1`, fails open on infra error) and the
required CI job (`.github/workflows/lesson_resolution_gate.yml`, fails closed) — single
interpretation, never divergent copies.

Frontmatter is parsed the same FLAT, line-based way `tasks/board_check.py` does — no YAML
library, because board_check.py is a hand-rolled parser and a nested map would be mis-parsed.

Exit codes (house convention, mirrors validate_return.py):
  0  PASS  — nothing CLOSE-blocking found (WARN allowed; RED is blocking, counted in FAIL)
  1  FAIL  — >=1 HARD or RED check failed — the CLOSE transition is blocked
  2  USAGE — bad input / target not found / no target given

Usage:
  python check_lesson_resolution.py tasks\TASK-604.md
  python check_lesson_resolution.py tasks\TASK-604.md --root C:\Bari
  python check_lesson_resolution.py --staged                # git-staged tasks/TASK-*.md files
  python check_lesson_resolution.py --selftest               # fixture matrix (required by DoD)
  python check_lesson_resolution.py --demo                   # blocked -> exit 1, then fixed -> exit 0
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows consoles default to cp1252; task files carry Hebrew copy and unicode.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

BARI_ROOT_DEFAULT = Path(r"C:\Bari")

TRIGGERS = {"failure", "correction", "recurrence", "user_complaint", "none"}
OUTCOMES = {
    "immediate_fix", "rule_change", "implementation_task",
    "regression_test", "human_decision", "not_applicable",
}
STRUCTURAL_OUTCOMES = {"immediate_fix", "rule_change", "regression_test"}
OPEN_STATES = {"IN_PROGRESS", "BLOCKED", "RETURNED", "CHANGES_REQUESTED"}

FAILURE_SIGNAL_PATTERNS = [
    (re.compile(r"status:\s*RETURNED", re.I), "prior 'status: RETURNED' mention"),
    (re.compile(r"\bCHANGES_REQUESTED\b"), "CHANGES_REQUESTED mention"),
    (re.compile(r"\bRED\b"), "RED mention"),
    (re.compile(r"gate[- ]fail", re.I), "gate-fail mention"),
    (re.compile(r"\bretry\b", re.I), "retry mention"),
    (re.compile(r"\battempt\s*[:=#]?\s*[2-9]", re.I), "attempt>1 mention"),
]


# ── frontmatter parsing (flat, line-based — matches tasks/board_check.py) ──────
def parse_frontmatter_text(text: str) -> dict:
    """Flat key: value scan between the leading '---' markers. Handles YAML block
    scalars (`summary: >`) by skipping their indented body so it is never mis-read
    as more keys — same technique board_check.py uses. No YAML library."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data: dict = {}
    in_block_scalar = False
    for line in block.splitlines():
        if in_block_scalar:
            if line and (line[0] in (" ", "\t")):
                continue
            in_block_scalar = False
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, raw_value = line.partition(":")
        key = key.strip()
        value = raw_value.strip()
        if value in (">", "|"):
            in_block_scalar = True
            data.setdefault(key, "")
            continue
        data[key] = value
    return data


def parse_list(raw: str) -> list[str]:
    """'[TASK-100, TASK-101]' -> ['TASK-100', 'TASK-101']; '' -> []."""
    raw = (raw or "").strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    if not raw.strip():
        return []
    return [p.strip() for p in raw.split(",") if p.strip()]


def find_task_file(root: Path, task_id: str) -> Path | None:
    for sub in ("tasks", "tasks/closed"):
        p = root / sub / f"{task_id}.md"
        if p.exists():
            return p
    return None


def detect_failure_shaped(raw_text: str) -> tuple[bool, list[str]]:
    signals = [label for pat, label in FAILURE_SIGNAL_PATTERNS if pat.search(raw_text)]
    return bool(signals), signals


def run_validator(cmd: str, root: Path) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=root, capture_output=True, timeout=120,
            text=True, encoding="utf-8", errors="replace",
        )
        ok = proc.returncode == 0
        detail = f"`{cmd}` -> exit {proc.returncode}"
        if not ok:
            tail = [ln for ln in (proc.stdout or "").strip().splitlines()[-3:] if ln]
            if tail:
                detail += "  | " + " / ".join(tail)
            etail = [ln for ln in (proc.stderr or "").strip().splitlines()[-3:] if ln]
            if etail:
                detail += "  | stderr: " + " / ".join(etail)
        return ok, detail
    except subprocess.TimeoutExpired:
        return False, f"`{cmd}` TIMEOUT (>120s)"
    except Exception as e:  # noqa: BLE001
        return False, f"`{cmd}` exec error: {e}"


# ── report ──────────────────────────────────────────────────────────────────────
class Report:
    """Collects HARD / WARN / RED findings. HARD and RED block (FAIL); WARN never does."""

    def __init__(self) -> None:
        self.checks: list[tuple[str, str, str, str]] = []  # (id, level, status, detail)

    def hard(self, cid: str, ok: bool, detail: str) -> None:
        self.checks.append((cid, "HARD", "PASS" if ok else "FAIL", detail))

    def warn(self, cid: str, ok: bool, detail: str) -> None:
        self.checks.append((cid, "WARN", "PASS" if ok else "WARN", detail))

    def red(self, cid: str, ok: bool, detail: str) -> None:
        """RED: blocks like HARD, but rendered distinctly — forces escalation to a
        validator/test rather than a silent re-waive (recurrence w/ documentation-only
        prevention)."""
        self.checks.append((cid, "RED", "PASS" if ok else "FAIL", detail))

    @property
    def failed(self) -> bool:
        return any(lvl in ("HARD", "RED") and st == "FAIL" for _, lvl, st, _ in self.checks)

    def render(self, task: str) -> str:
        lines = [f"check_lesson_resolution :: {task}", "-" * 68]
        for cid, lvl, st, detail in self.checks:
            mark = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}[st] if lvl != "RED" else (
                "RED-FAIL" if st == "FAIL" else "PASS")
            lines.append(f"  [{mark:<9}] {cid:<28} {detail}")
        verdict = "FAIL" if self.failed else "PASS"
        lines.append("-" * 68)
        lines.append(f"  VERDICT: {verdict}")
        return "\n".join(lines)

    def as_json(self, task: str) -> dict:
        return {
            "task": task,
            "verdict": "FAIL" if self.failed else "PASS",
            "findings": [
                {"check": cid, "level": lvl, "detail": detail}
                for cid, lvl, st, detail in self.checks if st in ("FAIL", "WARN")
            ],
            "checks_run": [c[0] for c in self.checks],
        }


# ── per-outcome verification ────────────────────────────────────────────────────
def check_immediate_fix(fm: dict, root: Path, rep: Report) -> None:
    artifact = fm.get("lesson_artifact", "").strip()
    if not artifact:
        rep.hard("immediate_fix.artifact", False,
                 "lesson_outcome=immediate_fix requires lesson_artifact")
        return
    fpath = root / artifact.replace("\\", "/")
    exists = fpath.exists()
    rep.hard("immediate_fix.exists", exists,
             f"lesson_artifact {artifact} " + ("exists" if exists else "NOT FOUND"))
    validator = fm.get("lesson_validator", "").strip()
    if not validator:
        rep.hard("immediate_fix.validator", False, "lesson_validator command required")
        return
    ok, detail = run_validator(validator, root)
    rep.hard("immediate_fix.validator_pass", ok, detail)


def check_rule_change(fm: dict, root: Path, rep: Report) -> None:
    artifact = fm.get("lesson_artifact", "").strip()
    if not artifact:
        rep.hard("rule_change.artifact", False,
                 "lesson_outcome=rule_change requires lesson_artifact (changed rule/validator file)")
        return
    fpath = root / artifact.replace("\\", "/")
    exists = fpath.exists()
    rep.hard("rule_change.exists", exists,
             f"lesson_artifact {artifact} " + ("exists" if exists else "NOT FOUND"))
    if not exists:
        return
    validator = fm.get("lesson_validator", "").strip()
    if not validator:
        if artifact.endswith(".py"):
            validator = f'python "{artifact}" --selftest'
        else:
            rep.hard("rule_change.validator", False,
                     "lesson_validator required (no default verification for a non-.py artifact)")
            return
    ok, detail = run_validator(validator, root)
    rep.hard("rule_change.selftest_pass", ok, detail)


def check_implementation_task(fm: dict, own_id: str, root: Path, rep: Report) -> None:
    gen_id = fm.get("lesson_generated_task_id", "").strip()
    if not gen_id:
        rep.hard("implementation_task.id", False,
                 "lesson_outcome=implementation_task requires lesson_generated_task_id")
        return
    if gen_id == own_id:
        rep.hard("implementation_task.selfref", False,
                 f"lesson_generated_task_id == own id ({own_id}) — self-reference")
        return
    gp = find_task_file(root, gen_id)
    if not gp:
        rep.hard("implementation_task.dangling", False,
                 f"{gen_id} not found in tasks/ or tasks/closed/ — dangling id")
        return
    rep.hard("implementation_task.exists", True, f"{gen_id} -> {gp.as_posix()}")
    gtext = gp.read_text(encoding="utf-8-sig")
    gfm = parse_frontmatter_text(gtext)
    reciprocal = own_id in gtext
    rep.hard("implementation_task.reciprocal", reciprocal,
             (f"{gen_id} references {own_id} back (reciprocal provenance)" if reciprocal
              else f"{gen_id} does NOT mention {own_id} anywhere — no reciprocal provenance "
                   f"(generate it with new_task.py --origin-task {own_id})"))
    gstatus = gfm.get("status", "")
    if gstatus == "CLOSED":
        gclose = gfm.get("close_reason", "").strip()
        rep.hard("implementation_task.verified_close", bool(gclose),
                 f"{gen_id} is CLOSED with a close_reason" if gclose
                 else f"{gen_id} is CLOSED WITHOUT a close_reason — closed-without-verification")
    else:
        rep.warn("implementation_task.status", True,
                 f"{gen_id} status={gstatus or '?'} (open follow-up — not yet required to be verified)")


def check_regression_test(fm: dict, root: Path, rep: Report) -> None:
    artifact = fm.get("lesson_artifact", "").strip()
    if not artifact:
        rep.hard("regression_test.artifact", False,
                 "lesson_outcome=regression_test requires lesson_artifact (fixture/test file)")
        return
    fpath = root / artifact.replace("\\", "/")
    exists = fpath.exists()
    rep.hard("regression_test.exists", exists,
             f"lesson_artifact {artifact} " + ("exists" if exists else "NOT FOUND"))
    validator = fm.get("lesson_validator", "").strip()
    if not validator:
        rep.hard("regression_test.validator", False, "lesson_validator command required")
        return
    ok, detail = run_validator(validator, root)
    rep.hard("regression_test.pass", ok, detail)


def check_human_decision(fm: dict, root: Path, rep: Report) -> None:
    approval = fm.get("lesson_approval", "").strip()
    if approval:
        rep.hard("human_decision.approval", True,
                 f"lesson_approval={approval!r} (recorded owner-decision ref)")
        return
    gen_id = fm.get("lesson_generated_task_id", "").strip()
    if gen_id:
        gp = find_task_file(root, gen_id)
        if gp:
            gfm = parse_frontmatter_text(gp.read_text(encoding="utf-8-sig"))
            gstatus = gfm.get("status", "")
            ok = gstatus in OPEN_STATES
            rep.hard("human_decision.open_approval_task", ok,
                     f"{gen_id} status={gstatus} " +
                     ("(open approval task, ok)" if ok else "(not open — no valid approval path)"))
            return
        rep.hard("human_decision.open_approval_task", False,
                 f"lesson_generated_task_id {gen_id} not found")
        return
    rep.hard("human_decision.evidence", False,
             "lesson_outcome=human_decision requires lesson_approval (recorded owner-decision ref) "
             "OR lesson_generated_task_id pointing to an OPEN approval task")


def check_not_applicable(fm: dict, raw_text: str, rep: Report, cid_prefix: str) -> None:
    failure_shaped, signals = detect_failure_shaped(raw_text)
    approval = fm.get("lesson_approval", "").strip()
    if approval:
        rep.warn(f"{cid_prefix}.anti_gaming", True,
                 f"not_applicable/none justified by owner waiver lesson_approval={approval!r}")
    elif not failure_shaped:
        rep.warn(f"{cid_prefix}.anti_gaming", True,
                 "not_applicable/none on a clean history (no failure-shaped signals) — no waiver needed")
    else:
        # Deliberately WARN, not HARD (STF-adjudicated mitigation for the honest residual:
        # trigger honesty is an audit problem, not a regex problem — see contract doc).
        rep.warn(f"{cid_prefix}.anti_gaming", False,
                 f"not_applicable/none on a FAILURE-SHAPED task (signals: {signals}) with NO "
                 f"lesson_approval waiver — compliance-theater risk, flagged for human/CI audit "
                 f"(non-blocking per STF anti-gaming mitigation)")


def check_recurrence(fm: dict, own_id: str, root: Path, rep: Report) -> None:
    sig = fm.get("lesson_signature", "").strip()
    if not sig:
        rep.warn("recurrence", True, "no lesson_signature set — recurrence check skipped")
        return
    matches: list[tuple[str, str]] = []
    for sub in ("tasks", "tasks/closed"):
        d = root / sub
        if not d.is_dir():
            continue
        for p in d.glob("TASK-*.md"):
            if p.stem == own_id:
                continue
            try:
                text = p.read_text(encoding="utf-8-sig")
            except OSError:
                continue
            mfm = parse_frontmatter_text(text)
            if mfm.get("lesson_signature", "").strip() == sig and mfm.get("status") == "CLOSED":
                matches.append((p.stem, mfm.get("lesson_outcome", "").strip()))
    if not matches:
        rep.warn("recurrence", True, f"signature {sig!r}: no prior recurrence in the corpus")
        return
    outcomes_seen = {fm.get("lesson_outcome", "").strip()} | {o for _, o in matches}
    has_structural = bool(outcomes_seen & STRUCTURAL_OUTCOMES)
    ids = [m[0] for m in matches]
    if has_structural:
        rep.warn("recurrence", True,
                 f"signature {sig!r} recurs across {ids} — structural prevention present "
                 f"({sorted(outcomes_seen & STRUCTURAL_OUTCOMES)})")
    else:
        rep.red("recurrence", False,
                f"signature {sig!r} recurs across {ids} with ONLY {sorted(o for o in outcomes_seen if o)} "
                f"outcomes — documentation-only prevention on a RECURRING failure; escalate to "
                f"rule_change/regression_test")


# ── driver ───────────────────────────────────────────────────────────────────────
def evaluate(path: Path, root: Path) -> Report:
    rep = Report()
    raw_text = path.read_text(encoding="utf-8-sig")
    fm = parse_frontmatter_text(raw_text)
    own_id = fm.get("id", path.stem).strip() or path.stem
    status = fm.get("status", "").strip()

    if status != "CLOSED":
        rep.warn("scope", True, f"status={status or '?'!r} — lesson-resolution only enforced at CLOSE (skip)")
        return rep

    trigger = fm.get("lesson_trigger", "").strip()
    if not trigger:
        rep.hard("trigger.present", False, "CLOSED task is missing lesson_trigger")
        return rep
    if trigger not in TRIGGERS:
        rep.hard("trigger.valid", False,
                 f"lesson_trigger={trigger!r} is not one of {sorted(TRIGGERS)}")
        return rep
    rep.hard("trigger.present", True, f"lesson_trigger={trigger}")

    outcome_raw = fm.get("lesson_outcome", "").strip()
    outcomes = [o for o in re.split(r"[,\s]+", outcome_raw) if o] if outcome_raw else []

    if trigger == "none":
        if outcome_raw and outcome_raw != "not_applicable":
            rep.hard("none.outcome", False,
                     f"lesson_trigger=none but lesson_outcome={outcome_raw!r} "
                     f"(expected 'not_applicable' or empty)")
        check_not_applicable(fm, raw_text, rep, cid_prefix="none")
        check_recurrence(fm, own_id, root, rep)
        return rep

    # non-none trigger: exactly ONE machine-verified outcome required
    if not outcomes:
        rep.hard("outcome.present", False, f"lesson_trigger={trigger} requires a lesson_outcome")
        return rep
    if len(outcomes) > 1:
        rep.hard("outcome.single", False, f"multiple lesson_outcome values not allowed: {outcomes}")
        return rep
    outcome = outcomes[0]
    if outcome not in OUTCOMES:
        rep.hard("outcome.valid", False, f"lesson_outcome={outcome!r} not one of {sorted(OUTCOMES)}")
        return rep
    rep.hard("outcome.present", True, f"lesson_outcome={outcome}")

    evidence = fm.get("lesson_evidence", "").strip()
    rep.hard("evidence.present", bool(evidence),
             f"lesson_evidence={evidence!r}" if evidence else "lesson_evidence missing")

    gen_id = fm.get("lesson_generated_task_id", "").strip()
    if gen_id and gen_id == own_id:
        rep.hard("selfref.generated", False,
                 f"lesson_generated_task_id == own id ({own_id}) — self-reference")

    related = parse_list(fm.get("lesson_related", ""))
    if own_id in related:
        rep.hard("selfref.related", False, f"lesson_related contains own id {own_id} — self-reference")
    for rid in related:
        if rid == own_id:
            continue
        rp = find_task_file(root, rid)
        rep.hard(f"dangling.related.{rid}", rp is not None,
                 f"lesson_related {rid} " + ("found" if rp else "DANGLING — no such TASK file"))

    if outcome == "immediate_fix":
        check_immediate_fix(fm, root, rep)
    elif outcome == "rule_change":
        check_rule_change(fm, root, rep)
    elif outcome == "implementation_task":
        check_implementation_task(fm, own_id, root, rep)
    elif outcome == "regression_test":
        check_regression_test(fm, root, rep)
    elif outcome == "human_decision":
        check_human_decision(fm, root, rep)
    elif outcome == "not_applicable":
        check_not_applicable(fm, raw_text, rep, cid_prefix="outcome")

    check_recurrence(fm, own_id, root, rep)
    return rep


# ── CLI plumbing ─────────────────────────────────────────────────────────────────
def _write_task(d: Path, tid: str, frontmatter_lines: list[str], closed_dir: bool = False) -> Path:
    sub = d / "tasks" / ("closed" if closed_dir else "")
    sub.mkdir(parents=True, exist_ok=True)
    p = sub / f"{tid}.md"
    body = "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# " + tid + "\n"
    p.write_text(body, encoding="utf-8")
    return p


def _build_fixture_root(tmp: Path) -> None:
    """A minimal registry: one artifact + one passing/failing validator script, and a
    couple of ordinary (non-CLOSED) tasks used as dangling/generated-task fixtures."""
    (tmp / "tasks").mkdir(parents=True, exist_ok=True)
    (tmp / "tasks" / "closed").mkdir(parents=True, exist_ok=True)

    art_dir = tmp / "03_operations" / "validators"
    art_dir.mkdir(parents=True, exist_ok=True)
    (art_dir / "fixed_rule.py").write_text(
        "print('fixed_rule selftest ok')\n", encoding="utf-8")

    # A real generated follow-up task carrying reciprocal provenance back to TASK-900.
    _write_task(tmp, "TASK-901", [
        "id: TASK-901", "title: generated follow-up", "owner: qa-agent",
        "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
        "origin_task: TASK-900",
        "close_reason: verified via fixed_rule.py --selftest",
        "depends_on: []", "blocks: []", "category_id: null",
        "summary: >", "  generated follow-up with reciprocal provenance",
    ], closed_dir=True)

    # An open (not-yet-closed) approval task for the human_decision fixture.
    _write_task(tmp, "TASK-902", [
        "id: TASK-902", "title: owner approval pending", "owner: product-agent",
        "status: IN_PROGRESS", "priority: HIGH", "created_at: 2026-07-11",
        "depends_on: []", "blocks: []", "category_id: null",
        "summary: >", "  awaiting owner go/no-go",
    ])


def run_selftest() -> int:
    """Fixture matrix (DoD #1): a well-formed resolution PASSES; each malformed case
    is REJECTED. 'gamed none on a failure-shaped task' is deliberately a non-blocking
    WARN (STF-adjudicated anti-gaming mitigation) — flagged, not hard-blocked; the
    selftest asserts the WARN fires (i.e. the gaming attempt is CAUGHT) rather than
    asserting exit-1, since the design intentionally does not hard-block trigger honesty."""
    tmp = Path(tempfile.mkdtemp(prefix="check_lesson_resolution_selftest_"))
    try:
        _build_fixture_root(tmp)
        results: list[tuple[str, Report, bool]] = []  # (name, report, expected_fail)

        # 1. well-formed immediate_fix -> PASS
        p = _write_task(tmp, "TASK-910", [
            "id: TASK-910", "title: well-formed immediate_fix", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: immediate_fix",
            "lesson_evidence: run output showed a NullRef at foo.py:42",
            "lesson_artifact: 03_operations/validators/fixed_rule.py",
            "lesson_validator: python 03_operations/validators/fixed_rule.py",
            "lesson_signature: nullref-foo-42",
            "close_reason: fixed and verified",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  well-formed",
        ])
        results.append(("well-formed immediate_fix (expect PASS)", evaluate(p, tmp), False))

        # 2. missing lesson_trigger -> HARD FAIL
        p = _write_task(tmp, "TASK-911", [
            "id: TASK-911", "title: missing trigger", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "close_reason: closed with no lesson fields at all",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  missing trigger",
        ])
        results.append(("missing lesson_trigger (expect FAIL)", evaluate(p, tmp), True))

        # 3. dangling id -> HARD FAIL
        p = _write_task(tmp, "TASK-912", [
            "id: TASK-912", "title: dangling generated task", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: implementation_task",
            "lesson_evidence: some failure",
            "lesson_generated_task_id: TASK-999999",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  dangling id",
        ])
        results.append(("dangling lesson_generated_task_id (expect FAIL)", evaluate(p, tmp), True))

        # 4. multiple outcomes -> HARD FAIL
        p = _write_task(tmp, "TASK-913", [
            "id: TASK-913", "title: multiple outcomes", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: immediate_fix, rule_change",
            "lesson_evidence: some failure",
            "lesson_artifact: 03_operations/validators/fixed_rule.py",
            "lesson_validator: python 03_operations/validators/fixed_rule.py",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  multiple outcomes",
        ])
        results.append(("multiple lesson_outcome values (expect FAIL)", evaluate(p, tmp), True))

        # 5. unverified artifact (missing file) -> HARD FAIL
        p = _write_task(tmp, "TASK-914", [
            "id: TASK-914", "title: unverified artifact", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: immediate_fix",
            "lesson_evidence: some failure",
            "lesson_artifact: 03_operations/validators/does_not_exist.py",
            "lesson_validator: python 03_operations/validators/does_not_exist.py",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  unverified artifact",
        ])
        results.append(("unverified artifact — file missing (expect FAIL)", evaluate(p, tmp), True))

        # 5b. unverified artifact — file exists but validator command FAILS -> HARD FAIL
        (tmp / "03_operations" / "validators" / "broken_rule.py").write_text(
            "import sys; sys.exit(1)\n", encoding="utf-8")
        p = _write_task(tmp, "TASK-915", [
            "id: TASK-915", "title: unverified artifact - failing validator", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: rule_change",
            "lesson_evidence: some failure",
            "lesson_artifact: 03_operations/validators/broken_rule.py",
            "lesson_validator: python 03_operations/validators/broken_rule.py --selftest",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  validator fails",
        ])
        results.append(("unverified artifact — validator command fails (expect FAIL)", evaluate(p, tmp), True))

        # 6. gamed 'none' on a failure-shaped task -> WARN (non-blocking) — the anti-gaming case
        p = _write_task(tmp, "TASK-916", [
            "id: TASK-916", "title: gamed none", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: none",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  This task went through CHANGES_REQUESTED after a RED gate-fail, "
            "  then retry attempt 2 fixed it silently with no lesson recorded.",
        ])
        gamed_report = evaluate(p, tmp)
        gamed_anti_gaming = [c for c in gamed_report.checks if c[0].endswith("anti_gaming")]
        gamed_warn_fired = bool(gamed_anti_gaming) and gamed_anti_gaming[0][2] == "WARN"
        results.append(("gamed none on failure-shaped task (expect WARN fired, non-blocking)",
                         gamed_report, False))

        # 7. valid human_decision (owner waiver) -> PASS
        p = _write_task(tmp, "TASK-917", [
            "id: TASK-917", "title: human decision", "owner: product-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: recurrence",
            "lesson_outcome: human_decision",
            "lesson_evidence: recurring scope question, tripwire 5",
            "lesson_approval: memory/owner_ruling_2026_07_11.md",
            "close_reason: owner decided",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  human decision",
        ])
        results.append(("valid human_decision w/ owner ref (expect PASS)", evaluate(p, tmp), False))

        # 8. valid implementation_task w/ reciprocal provenance -> PASS
        p = _write_task(tmp, "TASK-900", [
            "id: TASK-900", "title: spawned a follow-up", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: implementation_task",
            "lesson_evidence: found during TASK-900 review",
            "lesson_generated_task_id: TASK-901",
            "close_reason: follow-up generated and verified",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  spawned TASK-901",
        ])
        results.append(("valid implementation_task w/ reciprocal provenance (expect PASS)",
                         evaluate(p, tmp), False))

        # 9. self-reference -> HARD FAIL
        p = _write_task(tmp, "TASK-918", [
            "id: TASK-918", "title: self reference", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: implementation_task",
            "lesson_evidence: some failure",
            "lesson_generated_task_id: TASK-918",
            "close_reason: n/a",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  self reference",
        ])
        results.append(("self-referencing lesson_generated_task_id (expect FAIL)", evaluate(p, tmp), True))

        # ── render + assert ──────────────────────────────────────────────
        ok = True
        for name, rep, expect_fail in results:
            print(rep.render(name))
            print()
            got_fail = rep.failed
            case_ok = (got_fail == expect_fail)
            print(f"  case: {'FAIL(correct)' if got_fail and expect_fail else 'PASS(correct)' if not got_fail and not expect_fail else 'WRONG'}")
            print()
            ok = ok and case_ok
        ok = ok and gamed_warn_fired
        print(f"gamed-none anti-gaming WARN fired: {gamed_warn_fired}")
        print(f"SELFTEST: {len(results)} fixtures checked => {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_demo() -> int:
    """DoD #2 demo: a scratch TASK md set to CLOSED with no valid resolution -> exit 1
    (blocked); the SAME task amended with a valid immediate_fix + existing artifact +
    passing validator -> exit 0."""
    tmp = Path(tempfile.mkdtemp(prefix="check_lesson_resolution_demo_"))
    try:
        _build_fixture_root(tmp)
        blocked = _write_task(tmp, "TASK-950", [
            "id: TASK-950", "title: demo task, no lesson resolution", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "close_reason: closing without any lesson_* fields",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  demo — no valid resolution",
        ])
        print("=== DEMO 1: CLOSED task, NO lesson resolution ===")
        rep1 = evaluate(blocked, tmp)
        print(rep1.render("TASK-950 (before fix)"))
        rc1 = 1 if rep1.failed else 0
        print(f"\n>>> exit code: {rc1} (expected 1 / blocked)\n")

        fixed = _write_task(tmp, "TASK-950", [
            "id: TASK-950", "title: demo task, valid lesson resolution", "owner: qa-agent",
            "status: CLOSED", "priority: MEDIUM", "created_at: 2026-07-11",
            "lesson_trigger: failure",
            "lesson_outcome: immediate_fix",
            "lesson_evidence: demo failure evidence",
            "lesson_artifact: 03_operations/validators/fixed_rule.py",
            "lesson_validator: python 03_operations/validators/fixed_rule.py",
            "lesson_signature: demo-fixture",
            "close_reason: fixed and verified",
            "depends_on: []", "blocks: []", "category_id: null",
            "summary: >", "  demo — valid resolution",
        ])
        print("=== DEMO 2: SAME task, valid immediate_fix + existing artifact + passing validator ===")
        rep2 = evaluate(fixed, tmp)
        print(rep2.render("TASK-950 (after fix)"))
        rc2 = 1 if rep2.failed else 0
        print(f"\n>>> exit code: {rc2} (expected 0 / unblocked)\n")

        ok = (rc1 == 1 and rc2 == 0)
        print(f"DEMO: {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _iter_task_frontmatter(root: Path):
    """Yield (task_id, frontmatter_dict) for every TASK-*.md across the live + closed registry."""
    for sub in ("tasks", "tasks/closed"):
        d = root / sub
        if not d.is_dir():
            continue
        for p in sorted(d.glob("TASK-*.md")):
            try:
                fm = parse_frontmatter_text(p.read_text(encoding="utf-8-sig"))
            except OSError:
                continue
            yield (fm.get("id", p.stem).strip() or p.stem, fm)


def cmd_report(root: Path, emit_json: bool = False) -> int:
    """Scenario-10 summary: open lessons, unverified prevention, repeated failures, overdue fixes.
    Read-only; never blocks (a reporting surface, not a gate). Exit 0 always."""
    open_lessons, unverified, overdue = [], [], []
    by_sig: dict[str, list[str]] = {}
    closed_ids = set()

    all_fm = list(_iter_task_frontmatter(root))
    for tid, fm in all_fm:
        if fm.get("status", "").strip() == "CLOSED":
            closed_ids.add(tid)
    for tid, fm in all_fm:
        trigger = fm.get("lesson_trigger", "").strip()
        outcome = fm.get("lesson_outcome", "").strip()
        status = fm.get("status", "").strip()
        sig = fm.get("lesson_signature", "").strip()
        meaningful = trigger and trigger != "none"
        # open lesson: a meaningful trigger on a task not yet closed
        if meaningful and status != "CLOSED":
            open_lessons.append((tid, trigger, outcome or "—", status or "?"))
        # unverified prevention: a CLOSED task whose lesson-resolution no longer verifies
        if status == "CLOSED" and meaningful:
            rep = evaluate((root / "tasks" / f"{tid}.md") if (root / "tasks" / f"{tid}.md").exists()
                           else (root / "tasks" / "closed" / f"{tid}.md"), root)
            if rep.failed:
                unverified.append((tid, outcome or "—"))
        # repeated failures: cluster by signature
        if sig:
            by_sig.setdefault(sig, []).append(tid)
        # overdue fix: an implementation_task outcome whose generated task is still open
        if outcome == "implementation_task":
            gen = fm.get("lesson_generated_task_id", "").strip()
            if gen and gen not in closed_ids:
                overdue.append((tid, gen))

    repeated = {s: ids for s, ids in by_sig.items() if len(ids) > 1}

    if emit_json:
        print(json.dumps({
            "open_lessons": open_lessons, "unverified_prevention": unverified,
            "repeated_failures": repeated, "overdue_fixes": overdue,
        }, indent=2))
        return 0

    def _section(title, rows, fmt):
        print(f"\n== {title} ({len(rows)}) ==")
        if not rows:
            print("  (none)")
        for r in rows:
            print(f"  {fmt(r)}")

    print("=== Lesson-resolution corpus report (TASK-604) ===")
    _section("Open lessons (meaningful trigger, not yet closed)", open_lessons,
             lambda r: f"{r[0]}  trigger={r[1]}  outcome={r[2]}  status={r[3]}")
    _section("Unverified prevention (CLOSED but resolution no longer verifies)", unverified,
             lambda r: f"{r[0]}  outcome={r[1]}")
    _section("Repeated failures (signature seen >1)", list(repeated.items()),
             lambda r: f"signature={r[0]!r}  tasks={r[1]}")
    _section("Overdue fixes (implementation_task whose generated task is still open)", overdue,
             lambda r: f"{r[0]} -> {r[1]} (still open)")
    print(f"\nscanned {len(all_fm)} task files.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Bari lesson-resolution CLOSE gate (TASK-604).")
    ap.add_argument("task_md", nargs="?", help="path to a tasks/TASK-NNN.md file")
    ap.add_argument("--staged", action="store_true",
                    help="check all git-staged tasks/TASK-*.md files")
    ap.add_argument("--root", default=str(BARI_ROOT_DEFAULT), help="repo root")
    ap.add_argument("--emit-json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the fixture matrix and exit")
    ap.add_argument("--demo", action="store_true", help="run the blocked->fixed demo and exit")
    ap.add_argument("--report", action="store_true",
                    help="corpus summary: open lessons, unverified prevention, repeated failures, overdue fixes")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if args.demo:
        return run_demo()
    if args.report:
        return cmd_report(Path(args.root), emit_json=args.emit_json)

    root = Path(args.root)
    targets: list[Path] = []
    if args.staged:
        try:
            proc = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                cwd=root, capture_output=True, text=True, timeout=30,
            )
            for line in proc.stdout.splitlines():
                line = line.strip()
                if re.match(r"^tasks[\\/]TASK-[^\\/]+\.md$", line):
                    targets.append(root / line)
        except Exception as e:  # noqa: BLE001
            print(f"check_lesson_resolution: git staged lookup failed: {e}", file=sys.stderr)
            return 2
    elif args.task_md:
        targets.append(Path(args.task_md))
    else:
        print("usage: check_lesson_resolution.py <tasks/TASK-NNN.md> | --staged | --selftest | --demo",
              file=sys.stderr)
        return 2

    if not targets:
        print("check_lesson_resolution: no tasks/TASK-*.md targets — nothing to gate.")
        return 0

    overall_fail = False
    for t in targets:
        if not t.exists():
            print(f"check_lesson_resolution: LOAD ERROR — {t} not found", file=sys.stderr)
            return 2
        rep = evaluate(t, root)
        if args.emit_json:
            print(json.dumps(rep.as_json(t.stem), ensure_ascii=False, indent=2))
        else:
            print(rep.render(t.stem))
        overall_fail = overall_fail or rep.failed
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
