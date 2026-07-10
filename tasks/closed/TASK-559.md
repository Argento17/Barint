---
id: TASK-559
title: CI wave 2: a11y hard-fail flip + validate_return.py C0 gate on return PRs
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10, commit e11d48f5 on branch task559-a11y-hardfail (pushed; PR awaits
  owner). Shipped with TASK-512 as one PR since the flip depends on 512 clearing. (1) a11y step
  continue-on-error REMOVED — gate is now hard on serious/critical WCAG 2 A/AA; verify-first caught that
  the planned flip was PREMATURE (full suite still 6/8 after PR #95 merged, failing on TASK-512 residual
  debt), so 512 was cleared first rather than shipping a knowingly-red hard gate. (2) New
  .github/workflows/c0_return_gate.yml: validator selftest + validate_return.py --md on return files
  CHANGED in the PR (git diff base...HEAD, --diff-filter=AM). Changed-files-only is deliberate and
  evidence-backed: running it over P554_contract.md post-merge FAILS C2 on sha256 drift (claimed hashes
  are of the pre-merge blobs) — a whole-directory gate would red-X every PR. Verified: YAML parses (all
  4 workflows), `validate_return.py --selftest` exit 0, C2-mismatch behavior reproduced live. Nothing
  merged to master by me; deploy remains owner-gated.
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-510 merged (PR #95) so the a11y advisory condition expired — delete continue-on-error from barint_ci e2e-smoke. Plus the queued audit item: new workflow running validate_return.py --md on return files changed in a PR under tasks/returns/ (C0 contract gate in CI; only changed files — legacy returns predate the gate). Lane: flip inline (deletion), workflow via C1-CURSOR in worktree branch task559-a11y-hardfail off merged origin/master.
---

# TASK-559 — CI wave 2: a11y hard-fail flip + validate_return.py C0 gate on return PRs

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
