---
id: TASK-131
title: Consolidate the two Bari directories (C:\Bari vs C:\Users\HP\bari)
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Evaluate and plan the cleanup of the two colliding Bari roots plus the stale nested C:\Users\HP\bari\Bari snapshot (4112 tracked files) that cause operating-model confusion. Deliverable: a clear consolidation plan (target structure, migration steps, dedup, rename to end the name collision). Sibling of TASK-130 operating-model hardening.
---

# TASK-131 — Consolidate the two Bari directories (C:\Bari vs C:\Users\HP\bari)

## Decision
Chosen topology: **Option A — two clean homes with a rename** (Agent OS stays at `C:\Bari`;
website renamed `C:\Users\HP\bari` → `C:\bari-web`). Rejected a single merged folder (would
leak the internal scoring brain + research + `.venv` into the publicly deployable repo) and a
true monorepo (more rewiring, deferred).

## Deliverable
Migration plan: `C:\Bari\directory_consolidation_plan_v1.md` — 6 phases (baseline/pre-flight →
delete stale nested snapshot → consolidate governance docs → rename website → git-init Agent OS
→ guards & verify). Each phase independently revertable; awaiting go-ahead to execute.

## Key findings
- Nested `C:\Users\HP\bari\Bari\` is a stale partial Agent-OS snapshot, **4,112 files tracked**
  in the website git repo and NOT gitignored — primary confusion source.
- Name collision `C:\Bari` vs folder `bari`; governance docs scattered across both roots;
  `C:\Bari` (authoritative) has no git history while its snapshot does.

## Progress log
- 2026-06-01 — **Phase 0 + 1 done.** Pre-flight grep gate: no `src/` runtime imports from the
  snapshot; tsconfig alias is `@/*→./src/*` only. Salvaged 5 snapshot-unique files to
  `99_archive/website_snapshot_salvage_2026-06-01/` (3 bsip2 proto scripts = evaluate; 2 md =
  disposable). Removed nested `Bari/`: `git rm -r` (4,112 tracked) + `rm -rf` residual `.venv`
  (~18.9k untracked files) + `.idea`. Added `/Bari/` to website `.gitignore`. Website commit
  `938e13e`. Working-tree edits left untouched.
  - Stale refs to fix later (Phase 2/5): `AGENTS.md:17` and
    `docs/bsip2_spread_subtype_calibration_proposal_v1.md:28` point into the now-deleted snapshot;
    `scripts/audit-snacks-data-lineage.mjs` hardcodes `c:/Users/HP/bari` (breaks at Phase-3 rename).
- 2026-06-01 — **Phase 2 done.** Moved 12 root governance/operating-model docs → `C:\Bari\docs\governance\`
  and 8 data/scoring docs → `C:\Bari\docs\data\`; moved stale `command-center/index.html` →
  `05_command_center\legacy_website_render\`. Repointed the bsip2 proposal's broken snapshot link to
  the salvage folder; fixed `AGENTS.md` (no registry copy in website). Website commit `aeb632b`.
  Website root now holds only orientation files (AGENTS/CLAUDE/README/SKILL/IMPLEMENTATION_PROMPT).
  Frontend-impl docs kept in website `docs/`. **Deferred for owner classification** (borderline
  rollout/release reports left in website `docs/`): `bread_rollout_report_v1`, `snacks_rollout_report_v1`,
  `mvp_rollout_summary_v1`, `rollout_readiness_report_v1`, `hummus_v1_release_summary_v1`.
- 2026-06-01 — **Phase 4 done.** `git init` at `C:\Bari` (branch `master`, commit `18518f3`,
  4,729 files, `.git` 118M). `.gitignore` excludes `.venv` (658M, intact on disk), `__pycache__`,
  `.idea`, `*.audit_bak`, `/tmp_*`, `.claude/settings.local.json`. Tracked: framework, ops code,
  products/data, command center, tasks (60), decisions, research, `.claude` agents/skills/hooks,
  Phase-2 `docs/`. Root `tmp_audit_129a` + `tmp_*.json` scratch archived to
  `99_archive/tmp_129_audit_2026-06-01/`. The authoritative workspace now has version history.
- 2026-06-01 — **Phase 3 BLOCKED → handed off.** Stopped the dev server (node PID 7260, freed
  :3000) but `Move-Item C:\Users\HP\bari → C:\bari-web` fails: the folder is held by VS Code (19
  Code.exe — the Claude Code extension runs *inside* it) and an Explorer window; cannot kill the
  host IDE. Also discovered the old path is hardcoded in ~12 Agent-OS docs (all
  `.claude/agents/*.md`, `comparison-template.md`, `frontend.md`, `project.md`, root `CLAUDE.md`,
  `settings.local.json`); the website itself only references its own path in the non-build
  `scripts/audit-snacks-data-lineage.mjs`, so the **rename does not break the build**. Prepared
  one-shot handoff: `05_command_center/rename_website_phase3.ps1` (move + repoint both trees +
  commit; won't touch the website's uncommitted WIP). User must run it from a standalone
  PowerShell with VS Code closed. NOTE: dev server left stopped.
- 2026-06-01 — **Phase 3 DONE** (user ran the script). Website is now `C:\bari-web`; commit
  `8082bb9` repointed all Agent-OS docs. **Incident:** the script's `Get-Content`/`WriteAllText`
  round-trip misread UTF-8 as Windows-1252 and baked mojibake into 29 patched docs. Fixed in
  commit `6079711`: restored clean content from `18518f3` and re-applied the repoint UTF-8-safely
  (path replacements correct; plan doc restored encoding-only). Lesson: never round-trip non-ASCII
  files through PS5.1 `Get-Content -Raw`; use `[IO.File]::ReadAllText`/Python.
- 2026-06-01 — **Lint check (post-rename):** `npm run lint` = 2 errors + 9 warnings. 9 warnings
  are the known baseline (`<img>`, 1 unused var). 2 errors are `require()` in
  `.claude/bari-qa-validate.js` — a standalone Node CJS helper, NOT app code; `next build` doesn't
  lint `.claude/`, so build/deploy unaffected. Fix applied in website `eslint.config.mjs`: added
  `.claude/**` to `globalIgnores`. Uncommitted — user to re-run lint + commit.
- 2026-06-01 — **Phase 5 + 6 done.** Found the Phase-3 repoint was under-scoped (only root `*.md`
  + `.claude/`); completed a full UTF-8-safe repoint of the remaining 25 files across both trees
  (incl. functional scripts `propagate_frontend_dataset.ps1`, `build_hummus_*.py`,
  `rescore_mvp_frontend_v1.py`, `compare-maadanim-v1-v2.py`, `generate_dashboard.py`). Final sweep:
  **0 dangling old-path refs, 0 mojibake** (excl. intentional-keep: this log, the plan narrative,
  the guard/rename scripts, and `99_archive`). Added `05_command_center/structure_guard.py`
  (asserts the two-homes invariants) → CLEAN. Skills mirroring set to canonical-only in `CLAUDE.md`.
  Website `npm run lint` = **0 errors, 9 warnings**. `generate_dashboard.py` regenerates fine.

## Return — ready for closure
All six phases complete. Outcome: name collision gone (`C:\Bari` + `C:\bari-web`); stale nested
snapshot removed (4,112 files) with unique content salvaged to `99_archive`; governance/data docs
consolidated under `C:\Bari\docs\`; Agent OS now git-versioned; all path references repointed;
`structure_guard.py` guards against recurrence. **Proposing CLOSED** — for the Central Controller
to record.

Open follow-ups (not blockers): (1) 5 borderline rollout/release reports left in `C:\bari-web\docs\`
pending owner classification; (2) 3 salvaged bsip2 scripts in `99_archive/website_snapshot_salvage_2026-06-01/`
to evaluate for promotion; (3) website `eslint.config.mjs` + repoint of `compare-maadanim-v1-v2.py`
are committed separately in the website repo; user's in-progress component edits left untouched.
