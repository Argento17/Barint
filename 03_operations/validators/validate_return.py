#!/usr/bin/env python3
r"""
validate_return.py — deterministic C0 gate on 100% of agent return contracts (TASK-420 / W1)
=============================================================================================

Bari's page-ship gates (run_gates.py, validate_comparison_page.py) fire late — at the
end of a category build. But the failures that actually reach the owner happen *upstream*,
at agent RETURN time: self-reported counts that were wrong (a run reported `0/48` when it
was `48/48`; "4/4 pairs pass" masked a 31-product collapse — see return_contract_v1.md),
fabricated PMIDs/DOIs, and superlatives with no artifact behind them. Today the orchestrator
checks the return contract by hand.

This makes that check deterministic and universal. It is a composable "Guard" (2026
defense-in-depth pattern) over the `return_contract_v1.md` JSON that runs on EVERY RETURNED
block. A model can be confident and wrong; a script can't be charmed.

Checks (all <100ms, zero model cost):
  C1 SCHEMA        — valid JSON, the 7 required keys present, correct shapes/types.
  C2 ARTIFACTS     — every artifact's sha256 matches the file on disk; deleted files are
                     actually gone; created/modified files actually exist.
  C3 COUNTS-FORM   — every `counts` value carries a denominator AND a named source
                     (Rule 1 + Rule 6 format): no bare number with nothing behind it.
  C4 COMMANDS      — commands_run entries are well-formed; with --run-commands, each is
                     re-executed and its exit_code must match the claim (Rule 6 truthfulness).
  C5 DISTRIBUTION  — a set-claim (N/M with M>=10, or a key naming scores/grades/products…)
                     must be accompanied by a distribution marker: stdev / median /
                     histogram / most_common / min-max (Rule 5).
  C6 CITATIONS     — any PMID/DOI in the contract is format-checked and, if
                     verify_citations.py is present, passed through it; never trusted raw.

Exit codes (mirrors run_gates.py):
  0  all HARD checks PASS (WARN allowed)
  1  >=1 HARD check FAILED
  2  usage / load error (bad JSON, no contract found)

Input (one of):
  --json  <path>   a .json file containing the contract object
  --md    <path>   a markdown return block; the LAST ```json fenced block is extracted
  (stdin)          the contract piped in, as JSON or a markdown block

Usage:
  python validate_return.py --md tasks/returns/TASK-399.md
  python validate_return.py --json contract.json --root C:\Bari
  python validate_return.py --md return.md --run-commands   # also re-run commands_run
  echo '<json>' | python validate_return.py
  python validate_return.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Windows consoles default to cp1252; contracts carry Hebrew copy and unicode. Never let
# the gate crash on an encoding error — reconfigure stdout/stderr to UTF-8 (replace on fail).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

BARI_ROOT_DEFAULT = Path(r"C:\Bari")
REQUIRED_KEYS = ("task", "proposed_status", "artifacts", "counts",
                 "commands_run", "not_done", "self_check")
VALID_STATUS = ("RETURNED", "BLOCKED")
VALID_ACTIONS = ("created", "modified", "deleted")

# A count value needs a distribution (Rule 5) when it is a FULL-SET report — "all N of N"
# with a large N (the 48/48, 4/4-masking-a-collapse pattern) — or its key implies a
# distribution (grade/score/dist). A partial ratio or rank (1/37, 3/57) is a legitimate
# scalar finding, so it is only a soft WARN, never a hard block (avoids false positives).
SET_DENOM_THRESHOLD = 10
DIST_KEY_RE = re.compile(r"score|grade|distribut", re.I)      # HARD: implies a distribution
SOFT_SET_KEY_RE = re.compile(r"product|pair|corpus|rank", re.I)  # WARN only
DIST_MARKER_RE = re.compile(
    r"stdev|std\b|std_?dev|median|histogram|most[_ -]?common|min\s*/\s*max|min-max|"
    r"\bmin\b.*\bmax\b|quartile|percentile",
    re.I,
)
# denominator like "80/80"; source like "(BSIP1)" or "from <x>" or ": <path>"
DENOM_RE = re.compile(r"\b\d+\s*/\s*\d+\b")
SOURCE_RE = re.compile(r"\(([^)]+)\)|\bfrom\b|\bvia\b|\btrace\b|\.json|\.md|/")
# Grab the token that FOLLOWS "PMID" whatever it is, so a fabricated id (e.g. "31douchebag")
# is caught as malformed rather than silently passing as "no PMID present".
PMID_TOKEN_RE = re.compile(r"\bPMID[:\s#]*([^\s,;)\]]+)", re.I)
PMID_CLEAN_RE = re.compile(r"^[0-9]{4,9}$")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b")


class Report:
    """Collects HARD failures and WARNs; renders a structured violation block."""

    def __init__(self) -> None:
        self.checks: list[tuple[str, str, str, str]] = []  # (id, level, status, detail)

    def hard(self, cid: str, ok: bool, detail: str) -> None:
        self.checks.append((cid, "HARD", "PASS" if ok else "FAIL", detail))

    def warn(self, cid: str, ok: bool, detail: str) -> None:
        self.checks.append((cid, "WARN", "PASS" if ok else "WARN", detail))

    @property
    def failed(self) -> bool:
        return any(lvl == "HARD" and st == "FAIL" for _, lvl, st, _ in self.checks)

    def render(self, task: str) -> str:
        lines = [f"validate_return :: {task}", "-" * 60]
        for cid, lvl, st, detail in self.checks:
            mark = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}[st]
            lines.append(f"  [{mark}] {cid:<14} {detail}")
        verdict = "FAIL" if self.failed else "PASS"
        lines.append("-" * 60)
        lines.append(f"  VERDICT: {verdict}")
        return "\n".join(lines)

    def as_json(self, task: str) -> dict:
        return {
            "task": task,
            "verdict": "FAIL" if self.failed else "PASS",
            "violations": [
                {"check": cid, "level": lvl, "detail": detail}
                for cid, lvl, st, detail in self.checks if st in ("FAIL", "WARN")
            ],
            "checks_run": [c[0] for c in self.checks],
        }


# ── contract extraction ──────────────────────────────────────────────────────
def extract_contract(text: str) -> dict:
    """Parse a contract from raw JSON, or from the LAST ```json fenced block in markdown."""
    text = text.strip()
    # try raw JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # fall back to fenced blocks — take the LAST ```json ... ``` (the contract sits at the end)
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    for block in reversed(blocks):
        try:
            obj = json.loads(block)
            if isinstance(obj, dict) and "proposed_status" in obj:
                return obj
        except json.JSONDecodeError:
            continue
    raise ValueError("no valid return-contract JSON found (raw or fenced)")


# ── checks ───────────────────────────────────────────────────────────────────
def check_schema(c: dict, rep: Report) -> bool:
    missing = [k for k in REQUIRED_KEYS if k not in c]
    rep.hard("C1.keys", not missing,
             "all 7 keys present" if not missing else f"missing keys: {missing}")
    if missing:
        return False
    ok_status = c["proposed_status"] in VALID_STATUS
    rep.hard("C1.status", ok_status,
             f"proposed_status={c['proposed_status']!r}"
             + ("" if ok_status else f" (must be one of {VALID_STATUS})"))
    ok_types = (isinstance(c["artifacts"], list)
                and isinstance(c["counts"], dict)
                and isinstance(c["commands_run"], list)
                and isinstance(c["not_done"], list))
    rep.hard("C1.types", ok_types,
             "artifacts/counts/commands_run/not_done have correct types"
             if ok_types else "type error in artifacts/counts/commands_run/not_done")
    return ok_status and ok_types


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_artifacts(c: dict, root: Path, rep: Report) -> None:
    arts = c.get("artifacts", [])
    if not arts:
        rep.warn("C2.artifacts", True, "no artifacts listed (ok for BLOCKED / advice returns)")
        return
    for i, a in enumerate(arts):
        if not isinstance(a, dict) or "path" not in a or "action" not in a:
            rep.hard(f"C2[{i}].shape", False, f"artifact {i} missing path/action: {a!r}")
            continue
        action = a["action"]
        rel = str(a["path"]).replace("\\", "/")
        fpath = (root / rel)
        if action not in VALID_ACTIONS:
            rep.hard(f"C2[{i}].action", False, f"{rel}: bad action {action!r}")
            continue
        if action == "deleted":
            rep.hard(f"C2[{i}].deleted", not fpath.exists(),
                     f"{rel}: {'gone (ok)' if not fpath.exists() else 'STILL EXISTS'}")
            continue
        # created / modified → must exist and, if a sha given, match
        if not fpath.exists():
            rep.hard(f"C2[{i}].exists", False, f"{rel}: claimed {action} but NOT FOUND")
            continue
        claimed = (a.get("sha256") or "").strip().lower()
        if not claimed:
            rep.warn(f"C2[{i}].sha", False, f"{rel}: exists, no sha256 given (cannot verify identity)")
            continue
        actual = _sha256(fpath)
        ok = actual == claimed
        rep.hard(f"C2[{i}].sha", ok,
                 f"{rel}: sha256 {'matches' if ok else f'MISMATCH claimed={claimed[:12]}.. actual={actual[:12]}..'}")


def check_counts_form(c: dict, rep: Report) -> None:
    counts = c.get("counts", {})
    if not counts:
        rep.warn("C3.counts", True, "no counts (ok if the task made no numeric claim)")
        return
    for key, val in counts.items():
        s = str(val)
        has_denom = bool(DENOM_RE.search(s)) or bool(re.search(r"\b\d+\b", s))
        has_source = bool(SOURCE_RE.search(s))
        ok = has_denom and has_source
        rep.hard(f"C3.{key}", ok,
                 f"{key}={s!r}"
                 + ("" if ok else "  (needs a number AND a named source/denominator — Rule 1/6)"))


def check_distribution(c: dict, rep: Report) -> None:
    counts = c.get("counts", {})
    blob = json.dumps(c, ensure_ascii=False)
    has_marker = bool(DIST_MARKER_RE.search(blob))
    hard_keys, soft_keys = [], []
    for key, val in counts.items():
        m = DENOM_RE.search(str(val))
        full_set = False
        partial_big = False
        if m:
            try:
                num, denom = (int(x) for x in re.split(r"\s*/\s*", m.group(0)))
                full_set = denom >= SET_DENOM_THRESHOLD and num == denom  # "all N of N"
                partial_big = denom >= SET_DENOM_THRESHOLD and num != denom
            except (ValueError, IndexError):
                pass
        if full_set or DIST_KEY_RE.search(key):
            hard_keys.append(key)
        elif partial_big or SOFT_SET_KEY_RE.search(key):
            soft_keys.append(key)
    if hard_keys:
        rep.hard("C5.dist", has_marker,
                 f"full-set/distribution claim(s) {hard_keys} "
                 + ("carry a distribution marker (stdev/median/most_common/…)" if has_marker
                    else "present but NO distribution marker — Rule 5 requires stdev + most_common "
                         "(a full-set 'N/N' pass can mask a collapse)"))
    if soft_keys and not has_marker:
        rep.warn("C5.dist.soft", False,
                 f"ratio/rank claim(s) {soft_keys}: consider a distribution or corpus-context note")
    if not hard_keys and not soft_keys:
        rep.warn("C5.dist", True, "no set-claim detected (distribution not required)")


def check_commands(c: dict, rep: Report, run: bool, root: Path) -> None:
    cmds = c.get("commands_run", [])
    if not cmds:
        rep.warn("C4.commands", True, "no commands_run listed")
        return
    for i, entry in enumerate(cmds):
        if not isinstance(entry, dict) or "cmd" not in entry or "exit_code" not in entry:
            rep.hard(f"C4[{i}].shape", False, f"command {i} missing cmd/exit_code: {entry!r}")
            continue
        if not run:
            rep.warn(f"C4[{i}]", True, f"declared (not re-run): {entry['cmd']!r} -> {entry['exit_code']}")
            continue
        try:
            proc = subprocess.run(entry["cmd"], shell=True, cwd=root,
                                  capture_output=True, timeout=300)
            ok = proc.returncode == int(entry["exit_code"])
            rep.hard(f"C4[{i}].rerun", ok,
                     f"{entry['cmd']!r}: claimed exit {entry['exit_code']}, got {proc.returncode}")
        except subprocess.TimeoutExpired:
            rep.hard(f"C4[{i}].rerun", False, f"{entry['cmd']!r}: TIMEOUT (>300s)")
        except Exception as e:  # noqa: BLE001 — surface any exec error as a hard fail
            rep.hard(f"C4[{i}].rerun", False, f"{entry['cmd']!r}: exec error {e}")


def check_citations(c: dict, rep: Report, root: Path) -> None:
    blob = json.dumps(c, ensure_ascii=False)
    pmid_tokens = PMID_TOKEN_RE.findall(blob)
    dois = DOI_RE.findall(blob)
    if not pmid_tokens and not dois:
        rep.warn("C6.cite", True, "no PMIDs/DOIs in contract")
        return
    # format sanity (deterministic, always runs): every token after "PMID" must be clean digits
    bad_pmid = [p for p in pmid_tokens if not PMID_CLEAN_RE.match(p)]
    rep.hard("C6.pmid_format", not bad_pmid,
             f"PMID tokens {pmid_tokens}"
             + ("" if not bad_pmid else f"  MALFORMED (likely fabricated): {bad_pmid}"))
    # hand off to verify_citations.py if it exists (never trust raw identifiers)
    vc = root / "03_operations" / "validators" / "verify_citations.py"
    if vc.exists():
        try:
            proc = subprocess.run([sys.executable, str(vc), "--json", "-"], input=blob,
                                  encoding="utf-8", errors="replace", capture_output=True, timeout=120)
            rep.hard("C6.verify", proc.returncode == 0,
                     f"verify_citations.py exit {proc.returncode}"
                     + ("" if proc.returncode == 0 else f": {proc.stdout[-200:]}"))
        except Exception as e:  # noqa: BLE001
            rep.warn("C6.verify", False, f"verify_citations.py present but failed to run: {e}")
    else:
        rep.warn("C6.verify", False,
                 f"{len(pmid_tokens)} PMID / {len(dois)} DOI found; verify_citations.py absent "
                 f"— FLAG for manual verification (never trust agent identifiers)")


# ── driver ───────────────────────────────────────────────────────────────────
def validate(contract: dict, root: Path, run_commands: bool) -> Report:
    rep = Report()
    if check_schema(contract, rep):
        check_artifacts(contract, root, rep)
        check_counts_form(contract, rep)
        check_distribution(contract, rep)
        check_commands(contract, rep, run_commands, root)
        check_citations(contract, rep, root)
    return rep


def _load_text(args) -> str:
    if args.json:
        return Path(args.json).read_text(encoding="utf-8")
    if args.md:
        return Path(args.md).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("no input: pass --json, --md, or pipe the contract on stdin")


def run_selftest() -> int:
    """Build a passing and a failing contract in a temp dir; assert exit codes 0 and 1."""
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="validate_return_selftest_"))
    try:
        # a real file to hash
        good_file = tmp / "artifact.txt"
        good_file.write_text("hello bari\n", encoding="utf-8")
        good_sha = _sha256(good_file)

        passing = {
            "task": "SELFTEST-PASS",
            "proposed_status": "RETURNED",
            "artifacts": [{"path": "artifact.txt", "action": "created", "sha256": good_sha}],
            "counts": {"scores_checked": "31/31 (bsip2_trace.json)",
                       "grade_dist": "A:2 B:9 C:14 D:6, median C, stdev 6.1, most_common C(14)"},
            "commands_run": [{"cmd": "echo ok", "exit_code": 0}],
            "not_done": [],
            "self_check": "all 31 displayed scores equal trace; grade_dist reported",
        }
        failing = {
            "task": "SELFTEST-FAIL",
            "proposed_status": "RETURNED",
            "artifacts": [{"path": "artifact.txt", "action": "created", "sha256": "deadbeef"},  # bad sha
                          {"path": "missing.txt", "action": "modified", "sha256": "x"}],        # missing file
            "counts": {"products": "57",                       # no source
                       "scores": "31/31"},                     # set-claim, no distribution marker
            "commands_run": [{"cmd": "echo ok"}],              # missing exit_code
            "not_done": [],
            "self_check": "n/a",
        }

        r_pass = validate(passing, tmp, run_commands=False)
        r_fail = validate(failing, tmp, run_commands=False)
        print(r_pass.render("SELFTEST-PASS"))
        print()
        print(r_fail.render("SELFTEST-FAIL"))
        print()

        ok = (not r_pass.failed) and r_fail.failed
        print(f"SELFTEST: passing->{'PASS' if not r_pass.failed else 'FAIL'}, "
              f"failing->{'FAIL(correct)' if r_fail.failed else 'PASS(WRONG)'}  =>  "
              f"{'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic C0 gate on a Bari agent return contract.")
    ap.add_argument("--json", help="path to a .json file containing the contract")
    ap.add_argument("--md", help="path to a markdown return block (last ```json fence is used)")
    ap.add_argument("--root", default=str(BARI_ROOT_DEFAULT), help="repo root for artifact paths")
    ap.add_argument("--run-commands", action="store_true",
                    help="re-execute commands_run and verify exit codes (Rule 6 truthfulness)")
    ap.add_argument("--emit-json", action="store_true", help="print the machine-readable violation block")
    ap.add_argument("--selftest", action="store_true", help="run built-in self-test and exit")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    try:
        text = _load_text(args)
        contract = extract_contract(text)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"validate_return: LOAD ERROR — {e}", file=sys.stderr)
        return 2

    root = Path(args.root)
    rep = validate(contract, root, args.run_commands)
    task = str(contract.get("task", "UNKNOWN"))

    if args.emit_json:
        print(json.dumps(rep.as_json(task), ensure_ascii=False, indent=2))
    else:
        print(rep.render(task))
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
