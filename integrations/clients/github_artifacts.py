"""GitHub artifact-state verifier — ground truth for CC's closing gate.

For: CC Agent. CC's mandate is "verify, don't trust" — it checks a task's return-block
claims against artifacts before recording CLOSED. Today "artifact" means a file on disk.
This widens it to the *actual* git/GitHub state: did the commit land on the default
branch, did CI pass, is the PR merged. A return block that says "shipped to
src/data/comparisons/" can now be confirmed against a merged commit, not a trusted file.

Uses the already-authorized `gh` CLI (and plain `git`) via subprocess — no new token,
no HTTP client. Read-only: only query verbs (api GET, log, branch --contains).

Typical CC use:
    from integrations.clients.github_artifacts import file_on_default_branch, ci_status
    ok = file_on_default_branch("bari-web/src/data/comparisons/hummus_frontend_v2.json")
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass


def _run(args: list[str]) -> tuple[int, str, str]:
    """Run a CLI, resolving the exe on PATH (Windows needs the full path). A missing
    tool degrades to (127, '', 'not found') instead of raising — CC never crashes."""
    exe = shutil.which(args[0])
    if exe is None:
        return 127, "", f"{args[0]} not found on PATH"
    p = subprocess.run([exe, *args[1:]], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def gh_available() -> bool:
    code, _, _ = _run(["gh", "auth", "status"])
    return code == 0


@dataclass
class CommitInfo:
    sha: str
    subject: str
    date: str
    on_default: bool | None        # True / False / None=could-not-verify-against-remote
    on_local_default: bool          # reachable from the LOCAL default branch ref (offline-safe)
    default_branch: str
    note: str = ""


def _default_branch() -> str:
    """Resolve the default branch: origin/HEAD → symbolic-ref → 'master'."""
    code, out, _ = _run(["git", "rev-parse", "--abbrev-ref", "origin/HEAD"])
    if code == 0 and out:
        return out.split("/")[-1]
    code, out, _ = _run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"])
    if code == 0 and out:
        return out.split("/")[-1]
    return "master"


def _has_remote() -> bool:
    code, out, _ = _run(["git", "branch", "-r"])
    return code == 0 and bool(out.strip())


def last_commit_touching(path: str) -> CommitInfo | None:
    """Most recent commit that modified `path`, with a tri-state default-branch verdict.

    `on_default` is True/False only when a remote can actually be consulted; it is **None**
    (not a misleading False) when there is no remote / it isn't fetched. `on_local_default`
    is always computable offline. CC should treat None as "verify manually", never "not
    shipped"."""
    code, out, _ = _run(
        ["git", "log", "-1", "--format=%H%x1f%s%x1f%cI", "--", path]
    )
    if code != 0 or not out:
        return None
    sha, subject, date = (out.split("\x1f") + ["", "", ""])[:3]
    default = _default_branch()

    # Offline-safe: is the commit an ancestor of the local default branch tip?
    lcode, _, _ = _run(["git", "merge-base", "--is-ancestor", sha, default])
    on_local_default = lcode == 0

    if not _has_remote():
        return CommitInfo(sha=sha, subject=subject, date=date, on_default=None,
                          on_local_default=on_local_default, default_branch=default,
                          note="no remote fetched — remote ship-state UNVERIFIABLE; "
                               "used local default branch as a fallback signal")
    ccode, cout, _ = _run(["git", "branch", "--contains", sha, "-r"])
    if ccode != 0:
        return CommitInfo(sha=sha, subject=subject, date=date, on_default=None,
                          on_local_default=on_local_default, default_branch=default,
                          note="remote contains-check failed — UNVERIFIABLE")
    on_default = any(f"origin/{default}" in line for line in cout.splitlines())
    return CommitInfo(sha=sha, subject=subject, date=date, on_default=on_default,
                      on_local_default=on_local_default, default_branch=default)


def file_on_default_branch(path: str) -> bool:
    """True only if the file's latest commit is *verifiably* on origin/<default>. Returns
    False when not shipped OR when it can't be verified — use `verify_artifact()` for the
    honest tri-state; this boolean errs safe (a close gate should not trust an unverifiable)."""
    info = last_commit_touching(path)
    return bool(info and info.on_default is True)


def verify_artifact(path: str) -> dict:
    """One-call close-gate verdict for a return-block artifact claim. Combines on-disk
    existence + last commit + tri-state ship-state into a verdict CC can paste, and is
    explicit when it is BLIND rather than asserting a false negative.

    verdict ∈ {"shipped", "committed-not-on-default", "unverifiable", "uncommitted", "missing"}.
    """
    exists = os.path.exists(os.path.join(_repo_root(), path)) or os.path.exists(path)
    info = last_commit_touching(path)
    if info is None:
        return {"path": path, "verdict": "missing" if not exists else "uncommitted",
                "exists_on_disk": exists, "note": "no commit history for this path"}
    if info.on_default is True:
        verdict = "shipped"
    elif info.on_default is False:
        verdict = "committed-not-on-default"
    else:
        verdict = "unverifiable"
    return {"path": path, "verdict": verdict, "exists_on_disk": exists,
            "sha": info.sha[:10], "subject": info.subject, "date": info.date,
            "default_branch": info.default_branch, "on_default": info.on_default,
            "on_local_default": info.on_local_default, "note": info.note}


def _repo_root() -> str:
    code, out, _ = _run(["git", "rev-parse", "--show-toplevel"])
    return out if code == 0 and out else "."


def ci_status(ref: str = "HEAD") -> dict:
    """Latest CI conclusion for a ref via gh. ALWAYS returns an `available` flag so callers
    can tell BLIND ('available': False — gh missing/unauthed) apart from genuinely no-CI
    ('available': True, 'found': False). CC must never read an empty result as 'CI passed'."""
    if not gh_available():
        return {"available": False, "reason": "gh CLI not installed or not authenticated"}
    code, out, err = _run([
        "gh", "run", "list", "--branch", ref, "--limit", "1",
        "--json", "status,conclusion,workflowName,headSha",
    ])
    if code != 0:
        return {"available": False, "reason": f"gh run list failed: {err[:80]}"}
    try:
        runs = json.loads(out) if out else []
    except json.JSONDecodeError:
        return {"available": False, "reason": "gh returned unparseable JSON"}
    if not runs:
        return {"available": True, "found": False, "note": "no CI runs for this ref"}
    return {"available": True, "found": True, **runs[0]}


def pr_for_commit(sha: str) -> dict:
    """PR that introduced a commit (merged state, number, title). Carries an `available`
    flag so BLIND (gh unauthed) is distinct from 'no PR found'."""
    if not gh_available():
        return {"available": False, "reason": "gh CLI not installed or not authenticated"}
    code, out, _ = _run([
        "gh", "api", f"/repos/{{owner}}/{{repo}}/commits/{sha}/pulls",
        "--jq", "[.[] | {number, state, merged_at, title}]",
    ])
    if code != 0:
        return {"available": False, "reason": "gh api call failed"}
    try:
        prs = json.loads(out) if out else []
        return {"available": True, "found": bool(prs), **(prs[0] if prs else {})}
    except (json.JSONDecodeError, IndexError):
        return {"available": False, "reason": "unparseable gh response"}


if __name__ == "__main__":
    print(f"gh available: {gh_available()}")
    sample = "bari-web/src/data/comparisons"
    print(f"verify_artifact({sample}):")
    v = verify_artifact(sample)
    for k in ("verdict", "exists_on_disk", "sha", "on_default", "on_local_default",
              "default_branch", "note"):
        if k in v and v[k] not in (None, ""):
            print(f"    {k}: {v[k]}")
    ci = ci_status()
    print(f"CI status (HEAD): {'BLIND — ' + ci['reason'] if not ci.get('available') else ci}")
