---
id: TASK-603
title: Vercel deployment gating: implement the actual mechanism (repository-dispatch snippet) so the 6 checks gate promotion
owner: qa-agent
status: IN_PROGRESS
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
