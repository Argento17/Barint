#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_signoffs.py -- TASK-567 tamper-proof two-gate sign-off verifier.

Replaces the existence/mtime check on tasks/signoffs/<json-basename>.ok with a
sha256 equality check against tasks/signoffs/<json-basename>.approval.json
(format: 01_framework/operations/signoff_record_v1.md).

For each given comparison-JSON path the verifier:
  1. locates the approval record by basename;
  2. hashes the file's EXACT bytes (working tree by default, or the staged
     index blob with --staged -- i.e. the bytes the commit will contain);
  3. fails unless the hash equals the record's pinned sha256.

A file with no .approval.json record FAILS, unless --allow-legacy-ok is given
and a legacy <basename>.ok marker exists, in which case it PASSES with a
printed DEPRECATION warning (transition aid only; migrate_signoffs.py removes
the need).

Exit codes:
  0  all files verified (or nothing to verify)
  1  violation: missing record, malformed record, or sha256 mismatch
  3  infrastructure error (callers should treat as "verifier unavailable",
     NOT as approval)

No dependencies outside the standard library.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RECORD_SUFFIX = ".approval.json"
LEGACY_SUFFIX = ".ok"
REQUIRED_KEYS = ("copy_id", "file", "sha256", "gates", "approved_at", "task")
REQUIRED_GATES = ("content_agent", "red_team")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def repo_relpath(path, repo):
    """Normalize a possibly-absolute path to a forward-slash repo-relative path."""
    p = os.path.abspath(path) if os.path.isabs(path) else os.path.abspath(os.path.join(repo, path))
    rel = os.path.relpath(p, os.path.abspath(repo))
    return rel.replace("\\", "/")


def staged_bytes(repo, relpath):
    """Bytes of the staged (index) blob -- exactly what a commit would contain.
    Returns None if the path has no staged blob (e.g. staged deletion)."""
    proc = subprocess.run(
        ["git", "-C", repo, "show", ":{0}".format(relpath)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def load_record(record_path):
    with open(record_path, "r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def verify_one(relpath, repo, signoffs_dir, use_staged, allow_legacy_ok):
    """Returns (ok: bool, messages: list[str])."""
    msgs = []
    base = os.path.basename(relpath)
    record_path = os.path.join(signoffs_dir, base + RECORD_SUFFIX)
    legacy_path = os.path.join(signoffs_dir, base + LEGACY_SUFFIX)

    if use_staged:
        data = staged_bytes(repo, relpath)
        if data is None:
            msgs.append("SKIP  {0}: no staged blob (staged deletion or rename source) -- no copy to approve".format(relpath))
            return True, msgs
    else:
        full = os.path.join(repo, relpath.replace("/", os.sep))
        if not os.path.isfile(full):
            msgs.append("SKIP  {0}: file does not exist on disk -- no copy to approve".format(relpath))
            return True, msgs
        with open(full, "rb") as fh:
            data = fh.read()

    if not os.path.isfile(record_path):
        if allow_legacy_ok and os.path.isfile(legacy_path):
            msgs.append(
                "DEPRECATION  {0}: accepted on legacy marker {1} (existence only, NOT hash-pinned). "
                "Run 03_operations/validators/migrate_signoffs.py to convert it to a sha256-pinned "
                ".approval.json record.".format(base, os.path.basename(legacy_path))
            )
            return True, msgs
        msgs.append(
            "FAIL  {0}: no approval record {1} (two-gate sign-off missing; "
            "see 01_framework/operations/signoff_record_v1.md)".format(relpath, base + RECORD_SUFFIX)
        )
        return False, msgs

    try:
        record = load_record(record_path)
    except (ValueError, OSError) as exc:
        msgs.append("FAIL  {0}: approval record {1} unreadable/malformed: {2}".format(relpath, base + RECORD_SUFFIX, exc))
        return False, msgs

    missing_keys = [k for k in REQUIRED_KEYS if k not in record]
    gates = record.get("gates") or {}
    missing_gates = [g for g in REQUIRED_GATES if g not in gates]
    if missing_keys or missing_gates:
        msgs.append(
            "FAIL  {0}: approval record incomplete (missing keys: {1}; missing gates: {2})".format(
                relpath, ", ".join(missing_keys) or "-", ", ".join(missing_gates) or "-"
            )
        )
        return False, msgs

    actual = sha256_bytes(data)
    pinned = str(record.get("sha256", "")).lower()
    if actual != pinned and not use_staged:
        # The pinned hash is of the git BLOB (the bytes a commit contains). On Windows
        # with core.autocrlf the working-tree copy is CRLF-smudged, so raw disk bytes
        # differ even when the CONTENT is identical to HEAD. If git confirms the file
        # is clean vs HEAD, hash the HEAD blob instead -- that is exactly what
        # committing/shipping this file would produce. A truly modified file stays dirty
        # under `git diff` and therefore stays a mismatch: no weakening.
        clean = subprocess.run(["git", "-C", repo, "diff", "--quiet", "HEAD", "--", relpath],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
        if clean:
            proc = subprocess.run(["git", "-C", repo, "show", "HEAD:{0}".format(relpath)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                actual = sha256_bytes(proc.stdout)
    if actual != pinned:
        msgs.append(
            "FAIL  {0}: sha256 MISMATCH -- the bytes being shipped are not the bytes that were approved.\n"
            "      approved: {1}\n"
            "      current:  {2}\n"
            "      One changed byte voids the approval. Re-run BOTH gates (Content Agent + Adversarial QA) "
            "on the current content, then have the orchestrator write a fresh {3}.".format(
                relpath, pinned, actual, base + RECORD_SUFFIX
            )
        )
        return False, msgs

    if record.get("file") and record["file"].replace("\\", "/") != relpath:
        msgs.append("WARN  {0}: record 'file' field says {1} (basename match used)".format(relpath, record["file"]))
    msgs.append("PASS  {0}: sha256 {1} matches approval ({2})".format(relpath, actual[:12], record.get("task", "?")))
    return True, msgs


def selftest():
    """Prove both directions without touching the repo: matching record passes,
    a single flipped byte fails, missing record fails, legacy .ok passes only
    with the flag."""
    import tempfile

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        signoffs = os.path.join(tmp, "signoffs")
        os.makedirs(os.path.join(repo, "data"))
        os.makedirs(signoffs)

        rel = "data/sample_frontend_v1.json"
        content = '{"category": "selftest", "rows": ["שלום"]}'.encode("utf-8")
        with open(os.path.join(repo, "data", "sample_frontend_v1.json"), "wb") as fh:
            fh.write(content)

        record = {
            "copy_id": "sample_frontend_v1",
            "file": rel,
            "sha256": sha256_bytes(content),
            "gates": {
                "content_agent": {"agent": "Content Agent", "date": "2026-07-10", "evidence": "selftest"},
                "red_team": {"agent": "Adversarial QA", "date": "2026-07-10", "evidence": "selftest"},
            },
            "approved_at": "2026-07-10",
            "task": "TASK-567",
        }
        record_path = os.path.join(signoffs, "sample_frontend_v1.json.approval.json")
        with open(record_path, "w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)

        def check(name, expected_ok, **kw):
            ok, msgs = verify_one(rel, repo, signoffs, use_staged=False,
                                  allow_legacy_ok=kw.get("allow_legacy_ok", False))
            status = "ok" if ok == expected_ok else "SELFTEST FAILURE"
            print("[selftest] {0}: expected ok={1}, got ok={2} -> {3}".format(name, expected_ok, ok, status))
            for m in msgs:
                print("           " + m.splitlines()[0])
            if ok != expected_ok:
                failures.append(name)

        # 1. exact bytes -> PASS
        check("matching-record-passes", True)

        # 2. flip one byte in the file -> FAIL
        tampered = bytearray(content)
        tampered[10] ^= 0x01
        with open(os.path.join(repo, "data", "sample_frontend_v1.json"), "wb") as fh:
            fh.write(bytes(tampered))
        check("one-flipped-byte-fails", False)

        # restore
        with open(os.path.join(repo, "data", "sample_frontend_v1.json"), "wb") as fh:
            fh.write(content)

        # 3. record removed -> FAIL
        os.remove(record_path)
        check("missing-record-fails", False)

        # 4. legacy .ok without flag -> FAIL; with flag -> PASS + deprecation
        with open(os.path.join(signoffs, "sample_frontend_v1.json.ok"), "w", encoding="utf-8") as fh:
            fh.write("legacy marker\n")
        check("legacy-ok-without-flag-fails", False)
        check("legacy-ok-with-flag-passes", True, allow_legacy_ok=True)

        # 5. utf-8-sig record (BOM) still reads -> PASS
        with open(record_path, "w", encoding="utf-8-sig") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)
        check("bom-record-passes", True)

    if failures:
        print("[selftest] FAILED: {0}".format(", ".join(failures)))
        return 1
    print("[selftest] all 6 checks behaved as expected")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verify sha256-pinned two-gate sign-off records for comparison JSONs.")
    parser.add_argument("files", nargs="*", help="comparison JSON paths (absolute or repo-relative)")
    parser.add_argument("--repo", default=None, help="repo root the file paths are relative to (default: cwd's git toplevel)")
    parser.add_argument("--signoffs", default=None, help="sign-off registry dir (default: <main registry>/tasks/signoffs)")
    parser.add_argument("--staged", action="store_true", help="hash the STAGED index blob (git show :path) instead of the working tree")
    parser.add_argument("--allow-legacy-ok", action="store_true", help="accept legacy .ok markers with a DEPRECATION warning")
    parser.add_argument("--selftest", action="store_true", help="run the built-in tamper-detection selftest and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    try:
        repo = args.repo
        if not repo:
            proc = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            repo = proc.stdout.decode("utf-8", "replace").strip() if proc.returncode == 0 else os.getcwd()
        repo = os.path.abspath(repo)

        signoffs_dir = args.signoffs
        if not signoffs_dir:
            # Markers live in the MAIN registry even for worktree commits.
            main_root = os.environ.get("CLAUDE_PROJECT_DIR") or repo
            signoffs_dir = os.path.join(main_root, "tasks", "signoffs")

        if not args.files:
            print("verify_signoffs: no files given -- nothing to verify")
            return 0

        any_fail = False
        for f in args.files:
            rel = repo_relpath(f, repo)
            ok, msgs = verify_one(rel, repo, signoffs_dir, args.staged, args.allow_legacy_ok)
            for m in msgs:
                print(m)
            if not ok:
                any_fail = True
        return 1 if any_fail else 0
    except Exception as exc:  # infra error: never masquerade as approval OR as violation
        print("verify_signoffs: INFRA ERROR: {0}".format(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
