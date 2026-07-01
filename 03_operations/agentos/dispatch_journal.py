#!/usr/bin/env python3
r"""
dispatch_journal.py — durable execution primitives for the Bari router (TASK-423 / W4a+b)
=========================================================================================

The router (`03_operations/router/dispatch.py`) has two documented, catastrophic hazards:
  1. CONCURRENT DISPATCH RACE — two dispatch.py runs share one opencode server; their
     return-capture cross-contaminates ([[concurrent_opencode_dispatch_races]]).
  2. SHARED-TREE WIPE — a cloud CLI lane (Cursor/Grok/Gemini) at cwd=C:\Bari runs
     `git stash -u` on the WHOLE tree; it once wiped 82 untracked files
     ([[lane_dispatch_wipes_shared_tree]]).

The 2026 durable-execution answer (Temporal/LangGraph): serialize with a lock, journal every
completed step so a crashed/re-invoked run REPLAYS from the journal instead of re-doing work,
and never let a step run when its preconditions are unsafe. This module supplies those three
primitives as a small, dependency-free, well-tested library; the router wires them in minimally.

  - dispatch_lock()   — a fail-FAST cross-process lock (refuses, not waits: a second concurrent
                        dispatch is the hazard, so we surface it rather than queue into the race).
  - journal()         — append-only JSONL step-log per run under tasks/_journal/.
  - already_done()    — replay check: has this (run, step) already completed? → skip, return cache.
  - tree_is_dirty() / guard_tree_for_cloud_lane() — refuse a tree-wiping cloud lane when the
                        working tree carries uncommitted work that its `git stash -u` would destroy.

All paths are under the repo; nothing here reaches the network. Windows-safe (atomic O_EXCL lock).

Self-test: python dispatch_journal.py --selftest
"""
from __future__ import annotations

import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

REPO_ROOT = Path(r"C:\Bari")
JOURNAL_DIR = REPO_ROOT / "tasks" / "_journal"
LOCK_PATH = JOURNAL_DIR / "dispatch.lock"
DEFAULT_STALE_SECONDS = 1800  # a lock older than this is presumed abandoned (crashed run)

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass


class DispatchBusy(RuntimeError):
    """Raised when another live dispatch holds the lock (the race we refuse to enter)."""


def _ensure_dir() -> None:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)          # signal 0 = liveness probe (works on Windows Python too)
        return True
    except (OSError, ProcessLookupError):
        return False
    except PermissionError:
        return True              # exists but not ours


# ── lock ─────────────────────────────────────────────────────────────────────
def _try_acquire(lock_path: Path, stale_seconds: int) -> bool:
    _ensure_dir()
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"{os.getpid()} {time.time():.0f}".encode())
        os.close(fd)
        return True
    except FileExistsError:
        # someone holds it — reclaim only if the holder is dead or the lock is stale
        try:
            content = lock_path.read_text().split()
            held_pid = int(content[0]) if content else -1
        except (OSError, ValueError):
            held_pid = -1
        age = time.time() - lock_path.stat().st_mtime if lock_path.exists() else 1e9
        if not _pid_alive(held_pid) or age > stale_seconds:
            try:
                lock_path.unlink()
            except OSError:
                return False
            return _try_acquire(lock_path, stale_seconds)
        return False


@contextmanager
def dispatch_lock(stale_seconds: int = DEFAULT_STALE_SECONDS, lock_path: Path = LOCK_PATH):
    """Fail-fast serialization. Raises DispatchBusy if another live dispatch holds it."""
    if not _try_acquire(lock_path, stale_seconds):
        holder = ""
        try:
            holder = lock_path.read_text().strip()
        except OSError:
            pass
        raise DispatchBusy(
            f"another dispatch is running (lock {lock_path} held by [{holder}]). "
            f"Concurrent dispatch cross-contaminates the opencode server — refusing. "
            f"Wait for it, or if it crashed, remove the stale lock."
        )
    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except OSError:
            pass


# ── journal ──────────────────────────────────────────────────────────────────
def journal(run_id: str, event: str, **data) -> None:
    """Append one step record to tasks/_journal/<run_id>.jsonl (append-only, replay-safe)."""
    _ensure_dir()
    rec = {"run": run_id, "event": event, "ts": round(time.time(), 3), **data}
    with (JOURNAL_DIR / f"{run_id}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def read_journal(run_id: str) -> list[dict]:
    path = JOURNAL_DIR / f"{run_id}.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def already_done(run_id: str, step: str) -> dict | None:
    """Replay check: return the cached completion record for `step`, or None if not yet done."""
    for rec in read_journal(run_id):
        if rec.get("event") == "step_done" and rec.get("step") == step:
            return rec
    return None


# ── tree-wipe guard ──────────────────────────────────────────────────────────
CLOUD_LANES = {"C1-GROK", "C1-CURSOR", "C1-GEMINI"}  # lanes that git-stash the whole tree


def tree_is_dirty(repo: Path = REPO_ROOT) -> tuple[bool, int]:
    """(dirty?, untracked_count). Untracked files are what `git stash -u` would destroy."""
    import subprocess
    try:
        out = subprocess.run(["git", "status", "--porcelain"], cwd=repo,
                             capture_output=True, text=True, timeout=30).stdout
    except Exception:  # noqa: BLE001
        return False, 0
    lines = [ln for ln in out.splitlines() if ln.strip()]
    untracked = sum(1 for ln in lines if ln.startswith("??"))
    return (len(lines) > 0, untracked)


def guard_tree_for_cloud_lane(route: str, repo: Path = REPO_ROOT) -> str | None:
    """Return a refusal message if `route` is a tree-wiping cloud lane and the tree is dirty
    (its `git stash -u` would wipe uncommitted/untracked work). None = safe to proceed."""
    if route not in CLOUD_LANES:
        return None
    dirty, untracked = tree_is_dirty(repo)
    if dirty:
        return (f"REFUSING {route}: working tree has uncommitted changes "
                f"({untracked} untracked). A cloud lane runs `git stash -u` on the WHOLE tree "
                f"and would wipe them (cf. the 82-file wipe). Commit/stash first, or run the "
                f"lane in an isolated `git worktree`.")
    return None


# ── selftest ─────────────────────────────────────────────────────────────────
def _selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="dispatch_journal_selftest_"))
    ok = True
    try:
        lp = tmp / "d.lock"
        # 1. lock acquires, and a second concurrent acquire is refused
        with dispatch_lock(lock_path=lp):
            second_refused = not _try_acquire(lp, DEFAULT_STALE_SECONDS)
        # after the context, lock is released → now acquirable
        reacquired = _try_acquire(lp, DEFAULT_STALE_SECONDS)
        (tmp / "d.lock").unlink(missing_ok=True)
        print(f"  lock: held-blocks-second={second_refused}, released-reacquires={reacquired} "
              f"{'ok' if second_refused and reacquired else 'WRONG'}")
        ok = ok and second_refused and reacquired

        # 2. journal append + replay check
        global JOURNAL_DIR
        saved = JOURNAL_DIR
        JOURNAL_DIR = tmp
        journal("run1", "step_done", step="scoreA", exit=0)
        journal("run1", "step_done", step="scoreB", exit=0)
        done_a = already_done("run1", "scoreA") is not None
        done_c = already_done("run1", "scoreC") is None
        recs = len(read_journal("run1"))
        JOURNAL_DIR = saved
        print(f"  journal: replay-hit(scoreA)={done_a}, replay-miss(scoreC)={done_c}, records={recs} "
              f"{'ok' if done_a and done_c and recs == 2 else 'WRONG'}")
        ok = ok and done_a and done_c and recs == 2

        # 3. tree guard: non-cloud lane always safe; cloud lane checks dirtiness
        safe_c2 = guard_tree_for_cloud_lane("C2", repo=tmp) is None
        # tmp is not a git repo → tree_is_dirty returns (False,0) → cloud lane allowed
        cloud_clean = guard_tree_for_cloud_lane("C1-GROK", repo=tmp) is None
        print(f"  guard: non-cloud-lane-safe={safe_c2}, clean-tree-allows-cloud={cloud_clean} "
              f"{'ok' if safe_c2 and cloud_clean else 'WRONG'}")
        ok = ok and safe_c2 and cloud_clean

        print(f"SELFTEST: {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    # default: print the journal ledger tail
    _ensure_dir()
    runs = sorted(JOURNAL_DIR.glob("*.jsonl"))
    print(f"journal dir: {JOURNAL_DIR}  ({len(runs)} run(s))")
    for r in runs[-5:]:
        print(f"  {r.stem}: {len(read_journal(r.stem))} events")
