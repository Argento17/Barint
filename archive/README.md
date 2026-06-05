# archive/ — local-only consolidation of agent transcripts + repo backup

This folder physically lives inside `C:\Bari` so all project material is in **one
place**, but its contents are **gitignored and never pushed** to the public remote
(`Argento17/Barint`). Only this README is tracked — as a pointer to what's here.

## Why gitignored, not committed

The raw material below is **bulky (~350 MB)** and **secret-bearing** (session logs
capture command output, which can include API keys/tokens). Committing it to a
public GitHub repo would bloat every clone and leak secrets. So it is consolidated
locally but kept off the remote. The curated, safe-to-publish layer lives elsewhere
and **is** committed: `memory-archive/` (84 knowledge notes) and `docs/`
(session index + saved plans).

## What's here (not in git)

| Path | What | Approx |
|------|------|--------|
| `transcripts/main/` | 77 main session logs (`<id>.jsonl`), May 16 – Jun 5 2026 | 159 MB |
| `transcripts/agents/<id>/` | 500 sub-agent run logs grouped by session | 61 MB |
| `repo-backup/bari-monorepo.bundle` | Full-history git bundle from the TASK-134 consolidation (2026-06-01) | 126 MB |

A readable index of the sessions (date + opening prompt) is committed at
[`docs/sessions-index.md`](../docs/sessions-index.md).

## Authority & refresh

- **Live source of truth** remains `~/.claude/projects/c--Bari/` (what the harness
  reads/writes each session). This archive is a **point-in-time mirror**, not the
  working copy.
- **Refresh** by re-running [`scripts/sync-archive.ps1`](../scripts/sync-archive.ps1),
  which re-copies memory + transcripts + the latest bundle and regenerates the index.

Last sync: 2026-06-05.
