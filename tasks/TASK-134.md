---
id: TASK-134
title: Consolidate website into Agent OS monorepo (C:\bari-web -> C:\bari\bari-web)
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-01
depends_on: [TASK-131]
blocks: []
category_id: null
summary: >
  Reverse the TASK-131 two-homes split into a single monorepo. Fold the standalone
  website repo (C:\bari-web, remote Argento17/bari) into the Agent OS repo as a git
  subtree under bari-web/, preserving full website history. Repoint all C:\bari-web
  path references to C:\bari\bari-web, reconcile governance (CLAUDE.md, ARCHITECTURE,
  REPO_MAP, structure_guard), point the monorepo at a new remote (Barint), and retire
  the standalone folder.
---

# TASK-134 — Consolidate website into Agent OS monorepo

## Context
TASK-131 deliberately split the Agent OS (`C:\Bari`) and the website into two homes
(`C:\bari-web`). Owner decision on 2026-06-01 reversed this into a **monorepo**: one
repo containing both concerns. This task records that consolidation.

## What changed
- **Subtree merge** — `git subtree add --prefix=bari-web` brought the website's full
  commit history into `C:\Bari` under `bari-web/`. Website's tracked files only;
  `node_modules`/`.next` remain gitignored. Merge commit folds 2 histories into one.
- **Runtime restored** at the new path: `.env.local` copied, `npm install`,
  `npm run build` (exit 0) and `npm run lint` (0 errors) all green from `C:\bari\bari-web`.
- **Path repoint** — 53 files repointed `C:\bari-web` → `C:\bari\bari-web` (functional
  scripts + `.claude` agents/skills + docs), preserving UTF-8/no-BOM. Historical records
  (this task's predecessor `TASK-131.md`, `directory_consolidation_plan_v1.md`,
  `rename_website_phase3.ps1`) intentionally left unchanged.
- **Governance reconciled** — `CLAUDE.md` reframed (monorepo, no Next.js at root),
  `ARCHITECTURE.md` + `REPO_MAP.md` updated to show `bari-web/`,
  `structure_guard.py` rewritten to assert the monorepo invariants,
  `directory_consolidation_plan_v1.md` banner-marked SUPERSEDED.
- **Remote** — monorepo points at a new GitHub remote (`Barint`). The old website
  remote (`Argento17/bari`) is left untouched as an archival backup of the site.
- **Old folder** — standalone `C:\bari-web` retired after verification.

## Backups
- `C:\bari_backups\<ts>\` — full-history git bundles + worktree zips of both repos.
- `Argento17/bari` GitHub remote holds the website at the pre-merge baseline.

## Return note
Mechanics complete and verified (build/lint green, structure guard clean, no dangling
`C:\bari-web` references outside historical records). Proposing **RETURNED**; Central
Controller to record CLOSED.
