---
id: TASK-603
title: Vercel deployment gating: implement the actual mechanism (repository-dispatch snippet) so the 6 checks gate promotion
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-571 finding corrected 2026-07-11: the Vercel project uses the 'Connect GitHub Actions' flow (vercel/repository-dispatch/actions/status@v1), NOT auto-observed check runs - so the 6 job names never appear in 'Select checks to add' to tick. Confirm the EXACT current Vercel mechanism (does the snippet need a VERCEL_TOKEN secret + project/org IDs, or does it auth via the installed GitHub app? does 'Select checks' need a prior reported run?), then implement: add the status-report step to the 6 gating jobs (frontend, python-tests, off-sweep, e2e-smoke, conformance, off-ban-census) across barint_ci.yml + bari_page_gates.yml, and give the owner the exact remaining dashboard/secret steps. NO paid upgrade without owner opt-in. Prereq for the two-speed merge policy safety.
---

# TASK-603 — Vercel deployment gating: implement the actual mechanism (repository-dispatch snippet) so the 6 checks gate promotion

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## CLOSED (orchestrator, 2026-07-11) — mechanism determined, NO code change needed
ENGINEERING-RESEARCH (Codex terra + web, Vercel docs cited). Key corrections to TASK-571's plan:
- **The repository-dispatch snippet is NOT needed** and must not be added as a speculative
  workaround. It's only for `repository_dispatch`-triggered workflows. Both Bari workflows run on
  `push: [master]`, so Vercel gates on the GitHub checks DIRECTLY. (My interim "needs the snippet"
  guess to the owner was WRONG — corrected.)
- **No VERCEL_TOKEN / secret**; the action (if ever used) auths via `${{ github.token }}`.
- **Why the picker is empty is UNDOCUMENTED by Vercel.** Operative requirement: Vercel must have
  OBSERVED a COMPLETED CI run + production deployment on a recent master SHA. Likely cause here:
  either the six jobs aren't completing GREEN on master, or no full cycle has been observed yet.
- Research's "e2e-smoke missing" finding = LOCAL task506 staleness only; origin/master (deployed)
  has all 6 jobs (verified). Not a Vercel blocker; is a reminder the local branch trails origin CI.
- No paid tier required (GitHub deployment checks are for all projects).
Remaining action is a DIAGNOSTIC needing owner GitHub-Actions visibility (are the 6 jobs green on
latest master?) → folded into TASK-571. Research: 03_operations/reports/task603_vercel_gating_research.md.
