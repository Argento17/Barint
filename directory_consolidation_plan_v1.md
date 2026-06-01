# Directory Consolidation Plan v1 (TASK-131)

Date: 2026-06-01 Â· Owner: data-agent Â· Status: PLAN (awaiting go-ahead to execute)
Chosen topology: **Option A â€” two clean homes with a rename** (not a monorepo, not a single merged folder).

## Problem (root causes, not symptoms)

The two roots are *supposed* to be separate (Agent OS brain vs. deployable website). The
friction comes from **duplication + a name collision**, not from having two homes:

1. **Name collision** â€” `C:\Bari` vs. a folder literally named `bari` at `C:\bari-web`.
   Agents/humans resolve the wrong one constantly.
2. **Stale nested duplicate** â€” `C:\bari-web\Bari\` is an older, *partial* snapshot of the
   Agent OS (missing `04_growth`, `05_command_center`, `tasks/`, `decisions/`). It is
   **committed to the website git repo: 4,112 tracked files**, and is **not** gitignored.
   Agents read its stale framework/operations/registry docs and act on them.
3. **Scattered governance** â€” ~17 audit/governance `.md` at the website root + a 24-file
   `docs/` + `command-center/index.html` + `handoff/`, even though `C:\Bari` is declared the
   single source of truth.
4. **Inverted versioning** â€” the authoritative workspace (`C:\Bari`) has *no* git history,
   while the disposable snapshot of it *is* versioned.

## Target end state

```
C:\Bari\               Agent OS (brain) â€” NOW a git repo
   01_framework  02_products  03_operations  04_growth  05_command_center  99_archive
   tasks\  decisions\  research\
   docs\  (governance/operating-model/research docs consolidated here)

C:\bari-web\           the website ONLY (renamed; no collision with C:\Bari)
   src\  public\  package.json  next.config.ts
   docs\  (website-implementation docs only)
   (nested Bari\ deleted; no governance .md at root)
```

Guarantees after migration: one authoritative home per concern, zero Agent-OS duplicate on
disk, no name collision, and a `.gitignore` guard so the website can never re-absorb the OS.

## Migration phases (each phase is independently revertable; stop/verify between phases)

### Phase 0 â€” Baseline & pre-flight (no destructive change)
- [ ] Website working tree is dirty (7 modified components + 3 untracked). Commit or stash to
      a clean baseline first.
- [ ] `C:\Bari` has no git â†’ make a full backup zip before any restructuring.
- [ ] Pre-flight greps (must come back empty / be resolved before deleting or renaming):
  - references to the nested snapshot: `from "./Bari`, `Bari/01_framework`, `\bari\Bari` in `src/`
  - hardcoded absolute paths: `C:\Bari` and `C:\bari-web` across both trees, scripts,
    `.idea`, `.cursor`, hooks, `new_task.py`, `generate_dashboard.py`, `serve.py`
- [ ] Inventory of governance docs to move vs. keep (see Phase 2 classification).

### Phase 1 â€” Delete the stale nested snapshot (biggest single win)
- [ ] Confirm Phase-0 grep shows no website code imports from `./Bari/...`.
- [ ] In website repo: `git rm -r Bari` (untracks 4,112 files), then remove from disk.
- [ ] Add `/Bari/` to website `.gitignore` as a permanent guard.
- [ ] Commit: "Remove stale Agent OS snapshot (TASK-131)".

### Phase 2 â€” Consolidate governance docs into C:\Bari
Classification rule:
- **MOVE to `C:\Bari\docs\`** (operating-model / governance / research / audits):
  `operating_model_review_v1`, `duplicate_systems_audit_v1`, `comparison_architecture_audit_v1`,
  `governance_compliance_review_v1`, `technical_debt_register_v1`, `rollout_retrospective_v1`,
  `rollout_risk_assessment_v1`, `snacks_post_rollout_audit_v1`, `category_scaling_readiness_v1`,
  `v2_readiness_fleet_audit_v1`, `CE_DIRECTION_V1`, `command-center/`, `handoff/`, and the
  governance subset of website `docs/` (e.g. `*_audit_v1`, `*_assessment_v1`, recovery/lineage).
- **KEEP in `C:\bari-web\docs\`** (website-implementation docs the frontend agent needs beside code):
  `comparison_ui_reference_v1`, `comparison_web_template_v1`, `canonical_route_strategy_v1`,
  `bread_migration_plan_v1`, `comparison_corpus_validation_plan_v1`, `comparison_registry_expansion_plan_v1`.
- [ ] Move per classification; leave a one-line pointer where a moved doc was referenced.
- [ ] `IMPLEMENTATION_PROMPT.md`, `Bari Design System.zip`, `colors_and_type.css`: triage
      (design-system assets â†’ website `ui_kits/`; prompts â†’ archive).

### Phase 3 â€” Rename the website folder (kills the collision)
- [ ] Stop dev server; close IDE/editors holding `C:\bari-web`.
- [ ] Rename `C:\bari-web` â†’ `C:\bari-web`. (Git remote/deploy unaffected â€” Vercel builds
      from the remote, not the local path. `node_modules`/`.next` survive the rename.)
- [ ] Update IDE project + `.idea`/`.cursor` workspace pointers.
- [ ] Verify `npm run dev`, `npm run build`, `npm run lint` all pass from the new path.

### Phase 4 â€” Version the Agent OS
- [ ] `git init` in `C:\Bari`; add `.gitignore` (`.venv/`, `__pycache__/`, `tmp_*`, `*.audit_bak`).
- [ ] Remove root cruft: `tmp_audit_129a/`, `tmp_final_rows.json`, `tmp_report_rows.json`
      (archive to `99_archive/` if any value, else delete).
- [ ] Initial commit.

### Phase 5 â€” Update canonical references & guards
- [ ] Both `CLAUDE.md` / `AGENTS.md`: replace every `C:\bari-web` with `C:\bari-web`;
      restate "the Agent OS lives ONLY at `C:\Bari`; no snapshot may exist inside the website".
- [ ] Resolve `.claude/skills` mirroring: decide canonical-only (`C:\Bari\.claude\skills`) +
      remove the mirror obligation, or keep an explicit one-way sync. Recommend canonical-only.
- [ ] Extend `05_command_center/check_drift.py` (or a hook) to assert: no `Bari/` inside the
      website, no `C:\Bari` snapshot, no stray governance `.md` at website root.

### Phase 6 â€” Verify & close
- [ ] Re-grep for dangling `C:\bari-web` references â†’ empty.
- [ ] `python new_task.py`-adjacent: confirm dashboard regenerates; `generate_dashboard.py` &
      `new_task.py` still resolve `C:\Bari` paths.
- [ ] Website lint/build green from `C:\bari-web`.
- [ ] Update TASK-131 â†’ propose RETURNED; Controller records CLOSED.

## Risks & mitigations
- **Hidden import from nested `Bari/`** â†’ Phase-0 grep gate before delete.
- **Hardcoded `C:\bari-web` paths break on rename** â†’ Phase-0 grep + Phase-3 verify build.
- **Losing un-versioned C:\Bari state** â†’ Phase-0 backup zip + Phase-4 git init.
- **Moving a doc the frontend agent needs** â†’ explicit keep/move classification in Phase 2.

## Out of scope (tracked elsewhere)
- Website internal component de-duplication (bread/snack/milk comparison systems) â†’
  `duplicate_systems_audit_v1` + TASK-130 operating-model hardening.
