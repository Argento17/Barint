#!/usr/bin/env python3
r"""
promote.py — gated staging->live promotion with one-command rollback (TASK-423 / W4c)
=====================================================================================

Bari serves no live traffic, so "canary / rainbow deployment" (2026 LLMOps) maps to:
stage a candidate, PROVE it against gates, and promote to the live path ONLY if the gates
pass — while recording enough to roll back in one command. Today that staging->live step is
a manual file copy with no gate and no undo; this makes it gated, logged, and reversible.

Flow:
  promote  --candidate staging/cheese.json --live bari-web/.../cheese_frontend_v4.json
           1. run the GATE on the candidate (rank_check.py by default; --gate-cmd to override,
              --no-gate to stage without gating). Refuse to promote a failing candidate.
           2. back up the current live file under tasks/_journal/promotions_backup/<id>/.
           3. copy candidate -> live.
           4. append a promotion record (id, ts, live path, from-sha, to-sha, gate verdict).
  rollback --last            restore the live file from the most recent promotion's backup.
  rollback --id <id>         restore a specific promotion.
  ledger                     show promotion history.

GOVERNANCE: promote.py performs the FILE-level promotion only. The consumer-facing DEPLOY
(git commit + push to master -> Vercel) stays owner-gated — this tool never commits or pushes.

Self-test: python promote.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(r"C:\Bari")
LEDGER_DIR = REPO_ROOT / "tasks" / "_journal"
LEDGER = LEDGER_DIR / "promotions.jsonl"
BACKUP_DIR = LEDGER_DIR / "promotions_backup"
RANK_CHECK = REPO_ROOT / "03_operations" / "validators" / "rank_check.py"

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass


def _sha(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _now_id() -> str:
    # promotion id from wall-clock (this is a CLI tool, not a replay-sensitive workflow script)
    return time.strftime("%Y%m%dT%H%M%S", time.gmtime())


def _read_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _run_gate(candidate: Path, gate_cmd: str | None) -> tuple[bool, str]:
    """Return (passed, detail). Default gate = rank_check.py exit 0 on the candidate."""
    if gate_cmd:
        proc = subprocess.run(gate_cmd, shell=True, capture_output=True, text=True, timeout=300)
        return proc.returncode == 0, f"custom gate exit {proc.returncode}"
    if not RANK_CHECK.exists():
        return False, "rank_check.py not found (pass --gate-cmd or --no-gate)"
    proc = subprocess.run([sys.executable, str(RANK_CHECK), "--json", str(candidate)],
                          capture_output=True, text=True, timeout=300)
    verdict = "PASS" if proc.returncode == 0 else "FAIL"
    return proc.returncode == 0, f"rank_check {verdict} (exit {proc.returncode})"


def cmd_promote(candidate: Path, live: Path, gate_cmd: str | None, no_gate: bool) -> int:
    if not candidate.exists():
        print(f"promote: candidate not found: {candidate}", file=sys.stderr)
        return 2
    try:
        json.loads(candidate.read_text(encoding="utf-8"))  # candidate must be valid JSON
    except (json.JSONDecodeError, OSError) as e:
        print(f"promote: candidate is not valid JSON: {e}", file=sys.stderr)
        return 2

    if no_gate:
        passed, detail = True, "GATE SKIPPED (--no-gate)"
    else:
        passed, detail = _run_gate(candidate, gate_cmd)
    print(f"[promote] gate: {detail}")
    if not passed:
        print("[promote] REFUSED — candidate failed the gate; live untouched.", file=sys.stderr)
        return 1

    pid = _now_id()
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    from_sha = _sha(live)
    backup = BACKUP_DIR / pid / live.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    if live.exists():
        shutil.copy2(live, backup)         # snapshot current live for rollback
    else:
        backup = None                       # first-time promotion, nothing to back up

    live.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate, live)
    to_sha = _sha(live)

    rec = {"id": pid, "ts": round(time.time(), 3), "live": str(live),
           "candidate": str(candidate), "from_sha": from_sha, "to_sha": to_sha,
           "gate": detail, "backup": str(backup) if backup else None}
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"[promote] PROMOTED {candidate.name} -> {live}")
    print(f"[promote]   id={pid}  from={from_sha[:12] or '(new)'}  to={to_sha[:12]}")
    print(f"[promote]   rollback: python promote.py rollback --id {pid}")
    print("[promote]   NOTE: file promoted in the working tree; the git deploy stays owner-gated.")
    return 0


def cmd_rollback(pid: str | None, last: bool) -> int:
    ledger = _read_ledger()
    if not ledger:
        print("rollback: no promotions recorded.", file=sys.stderr)
        return 1
    rec = ledger[-1] if last else next((r for r in reversed(ledger) if r["id"] == pid), None)
    if not rec:
        print(f"rollback: promotion id {pid} not found.", file=sys.stderr)
        return 1
    if not rec.get("backup"):
        print(f"rollback: promotion {rec['id']} had no backup (was a first-time promotion); "
              f"cannot restore. Delete the live file manually if intended.", file=sys.stderr)
        return 1
    backup = Path(rec["backup"])
    live = Path(rec["live"])
    if not backup.exists():
        print(f"rollback: backup file missing: {backup}", file=sys.stderr)
        return 1
    shutil.copy2(backup, live)
    restored = _sha(live)
    match = "OK" if restored == rec["from_sha"] else "WARN sha differs"
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"id": rec["id"], "ts": round(time.time(), 3),
                            "event": "rollback", "live": str(live),
                            "restored_sha": restored}, ensure_ascii=False) + "\n")
    print(f"[rollback] restored {live} from promotion {rec['id']} ({match})")
    print("[rollback]   NOTE: working-tree file restored; commit/push if it must reach live.")
    return 0


def cmd_ledger() -> int:
    ledger = _read_ledger()
    if not ledger:
        print("no promotions recorded.")
        return 0
    print(f"promotion ledger ({LEDGER}):")
    for r in ledger:
        if r.get("event") == "rollback":
            print(f"  {r['id']}  ROLLBACK -> {Path(r['live']).name}")
        else:
            print(f"  {r['id']}  {Path(r['live']).name}  "
                  f"{(r.get('from_sha') or '(new)')[:10]} -> {r.get('to_sha','')[:10]}  [{r.get('gate','')}]")
    return 0


def _selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="promote_selftest_"))
    global LEDGER, BACKUP_DIR, LEDGER_DIR
    saved = (LEDGER, BACKUP_DIR, LEDGER_DIR)
    LEDGER_DIR = tmp
    LEDGER = tmp / "promotions.jsonl"
    BACKUP_DIR = tmp / "backup"
    ok = True
    try:
        live = tmp / "live.json"
        live.write_text(json.dumps({"products": [{"id": "A"}], "v": 1}), encoding="utf-8")
        cand = tmp / "cand.json"
        cand.write_text(json.dumps({"products": [{"id": "A"}, {"id": "B"}], "v": 2}), encoding="utf-8")
        live_v1_sha = _sha(live)

        rc = cmd_promote(cand, live, gate_cmd="exit 0", no_gate=False)   # passing gate
        promoted = json.loads(live.read_text())["v"] == 2
        print(f"  promote(pass): exit={rc}, live-now-v2={promoted} {'ok' if rc == 0 and promoted else 'WRONG'}")
        ok = ok and rc == 0 and promoted

        rc2 = cmd_promote(cand, live, gate_cmd="exit 1", no_gate=False)  # failing gate → refuse
        still_v2 = json.loads(live.read_text())["v"] == 2
        print(f"  promote(fail-gate): exit={rc2}, live-unchanged={still_v2} "
              f"{'ok' if rc2 == 1 and still_v2 else 'WRONG'}")
        ok = ok and rc2 == 1 and still_v2

        rc3 = cmd_rollback(None, last=True)                              # roll back to v1
        back_v1 = json.loads(live.read_text())["v"] == 1 and _sha(live) == live_v1_sha
        print(f"  rollback(last): exit={rc3}, live-back-to-v1={back_v1} "
              f"{'ok' if rc3 == 0 and back_v1 else 'WRONG'}")
        ok = ok and rc3 == 0 and back_v1

        print(f"SELFTEST: {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        LEDGER, BACKUP_DIR, LEDGER_DIR = saved
        import shutil as _sh
        _sh.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Gated staging->live promotion with rollback.")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("promote", help="gate a candidate and promote it to live")
    p.add_argument("--candidate", required=True)
    p.add_argument("--live", required=True)
    p.add_argument("--gate-cmd", help="custom gate command (exit 0 = pass); default = rank_check.py")
    p.add_argument("--no-gate", action="store_true", help="stage without gating (records the skip)")

    r = sub.add_parser("rollback", help="restore live from a promotion backup")
    r.add_argument("--id", help="promotion id to roll back to")
    r.add_argument("--last", action="store_true", help="roll back the most recent promotion")

    sub.add_parser("ledger", help="show promotion history")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if args.cmd == "promote":
        return cmd_promote(Path(args.candidate), Path(args.live), args.gate_cmd, args.no_gate)
    if args.cmd == "rollback":
        if not args.id and not args.last:
            print("rollback: pass --last or --id <id>", file=sys.stderr)
            return 2
        return cmd_rollback(args.id, args.last)
    if args.cmd == "ledger":
        return cmd_ledger()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
