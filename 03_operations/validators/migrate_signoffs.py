#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_signoffs.py -- TASK-567 one-shot migration: legacy tasks/signoffs/*.ok
markers -> sha256-pinned <json-basename>.approval.json records
(format: 01_framework/operations/signoff_record_v1.md).

For each <json-basename>.ok:
  * pins sha256 of the file's CURRENT COMMITTED content
    (`git show HEAD:bari-web/src/data/comparisons/<json-basename>`);
  * carries the .ok body's gate text into gates.content_agent.evidence /
    gates.red_team.evidence (full body preserved under legacy_marker_text);
  * writes <json-basename>.approval.json and DELETES the .ok.

If the target JSON is not committed at HEAD, or the working tree differs from
HEAD (the approved bytes would be ambiguous), the marker is left in place and
reported -- resolve by hand. Safe to re-run. --dry-run previews.

No dependencies outside the standard library.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

COMPARISONS_REL = "bari-web/src/data/comparisons"


def head_bytes(repo, relpath):
    proc = subprocess.run(["git", "-C", repo, "show", "HEAD:{0}".format(relpath)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout if proc.returncode == 0 else None


def extract_evidence(body):
    """Pull the content-gate and red-team gate text out of a legacy .ok body.

    Two observed formats:
      key-per-line:  'content_gate: ...' / 'red_team_gate: ...'
      pipe-separated: '... | content-gate: ... | red-team: ...'
    Falls back to the whole body for both gates if neither parses.
    """
    content_ev, red_ev = None, None

    for line in body.splitlines():
        stripped = line.strip()
        m = re.match(r"^content[_-]gate:\s*(.+)$", stripped, re.IGNORECASE)
        if m and not content_ev:
            content_ev = m.group(1).strip()
        m = re.match(r"^red[_-]team(?:[_-]gate)?:\s*(.+)$", stripped, re.IGNORECASE)
        if m and not red_ev:
            red_ev = m.group(1).strip()

    if not (content_ev and red_ev):
        for segment in re.split(r"\s\|\s", body):
            seg = segment.strip()
            m = re.match(r"^content[_-]gate:\s*(.+)$", seg, re.IGNORECASE | re.DOTALL)
            if m and not content_ev:
                content_ev = m.group(1).strip()
            m = re.match(r"^red[_-]team(?:[_-]gate)?:\s*(.+)$", seg, re.IGNORECASE | re.DOTALL)
            if m and not red_ev:
                red_ev = m.group(1).strip()

    fallback = " ".join(body.split())
    return content_ev or fallback, red_ev or fallback


def migrate_marker(ok_path, repo, dry_run):
    """Returns (status, message). status in {'migrated', 'skipped', 'error'}."""
    marker_name = os.path.basename(ok_path)          # e.g. milk_frontend_v1.json.ok
    json_base = marker_name[:-len(".ok")]            # milk_frontend_v1.json
    relpath = "{0}/{1}".format(COMPARISONS_REL, json_base)

    committed = head_bytes(repo, relpath)
    if committed is None:
        return "skipped", "{0}: target {1} not committed at HEAD -- left as .ok, resolve by hand".format(marker_name, relpath)

    # Content-filter-aware dirtiness check (raw byte comparison would false-positive
    # on CRLF smudge under core.autocrlf): exit 0 = working tree content == HEAD.
    dirty = subprocess.run(["git", "-C", repo, "diff", "--quiet", "HEAD", "--", relpath],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
    if dirty != 0:
        return "skipped", ("{0}: working tree differs from HEAD for {1} -- approved bytes ambiguous, "
                           "left as .ok; commit or revert the JSON first".format(marker_name, relpath))

    with open(ok_path, "r", encoding="utf-8-sig") as fh:
        body = fh.read().strip()

    content_ev, red_ev = extract_evidence(body)
    task_m = re.search(r"TASK-\d+", body)
    date_m = re.search(r"\d{4}-\d{2}-\d{2}", body)
    date = date_m.group(0) if date_m else None

    record = {
        "copy_id": json_base[:-len(".json")] if json_base.endswith(".json") else json_base,
        "file": relpath,
        "sha256": hashlib.sha256(committed).hexdigest(),
        "gates": {
            "content_agent": {"agent": "Content Agent", "date": date, "evidence": content_ev},
            "red_team": {"agent": "Adversarial QA / Red-Team", "date": date, "evidence": red_ev},
        },
        "approved_at": date,
        "task": task_m.group(0) if task_m else None,
        "migrated_from": marker_name,
        "migration_note": ("sha256 pinned to HEAD content at migration time by migrate_signoffs.py (TASK-567); "
                           "original approval predates hash pinning"),
        "legacy_marker_text": body,
    }

    record_path = ok_path[:-len(".ok")] + ".approval.json"
    if dry_run:
        return "migrated", "[dry-run] {0} -> {1} (sha256 {2})".format(marker_name, os.path.basename(record_path), record["sha256"][:12])

    with open(record_path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.remove(ok_path)
    return "migrated", "{0} -> {1} (sha256 {2}, {3})".format(marker_name, os.path.basename(record_path), record["sha256"][:12], record["task"] or "no task id")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Migrate legacy .ok sign-off markers to sha256-pinned .approval.json records.")
    parser.add_argument("--repo", default=None, help="repo root (default: cwd's git toplevel)")
    parser.add_argument("--signoffs", default=None, help="sign-off dir (default: <repo>/tasks/signoffs)")
    parser.add_argument("--dry-run", action="store_true", help="preview without writing/deleting")
    args = parser.parse_args(argv)

    repo = args.repo
    if not repo:
        proc = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        repo = proc.stdout.decode("utf-8", "replace").strip() if proc.returncode == 0 else os.getcwd()
    repo = os.path.abspath(repo)
    signoffs_dir = args.signoffs or os.path.join(repo, "tasks", "signoffs")

    if not os.path.isdir(signoffs_dir):
        print("migrate_signoffs: no such dir {0}".format(signoffs_dir), file=sys.stderr)
        return 3

    markers = sorted(f for f in os.listdir(signoffs_dir) if f.endswith(".ok"))
    if not markers:
        print("migrate_signoffs: no .ok markers in {0} -- nothing to do".format(signoffs_dir))
        return 0

    counts = {"migrated": 0, "skipped": 0, "error": 0}
    for name in markers:
        try:
            status, msg = migrate_marker(os.path.join(signoffs_dir, name), repo, args.dry_run)
        except Exception as exc:
            status, msg = "error", "{0}: {1}".format(name, exc)
        counts[status] += 1
        print("{0:8s} {1}".format(status.upper(), msg))

    print("migrate_signoffs: {migrated} migrated, {skipped} skipped, {error} errors".format(**counts))
    return 0 if counts["error"] == 0 and counts["skipped"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
