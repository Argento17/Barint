---
id: TASK-571
title: Vercel: hold production alias until checks pass (deployment gating)
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. Push-to-master keeps working, but bari.digital only switches to the new build after CI checks pass (conformance_gate + smoke + a11y as first checks; run_gates joins after TASK-565 unblocks). Orchestrator researches the current Vercel mechanism and delivers exact click-path instructions for the owner (Vercel dashboard access is owner-only). No new paid services without explicit owner opt-in - if the feature needs a plan upgrade, STOP and report.
---

# TASK-571 — Vercel: hold production alias until checks pass

## Mechanism (verified against Vercel docs, last updated 2026-07-02)
Vercel **Deployment Checks** (docs: https://vercel.com/docs/deployment-checks). Exactly the approved behavior: push to master still builds immediately; the build is NOT aliased to bari.digital until the selected GitHub checks pass; a failed check leaves the old site live; **Force Promote** on the deployment page is the manual escape hatch. Works for direct pushes (any production deployment), no repository_dispatch complexity needed for our setup — we depend on the checks directly.

## Owner click-path (only you have Vercel access)
1. Vercel dashboard → the bari.digital project → **Settings → Git**: confirm the project is linked to Argento17/Barint via "Vercel for GitHub".
2. **Settings → Environments → Production**: confirm automatic aliasing for production is ON.
3. **Settings → Build and Deployment → Deployment Checks** → **Add Checks** → provider **GitHub** → select these checks BY JOB NAME:
   - `frontend`  (barint_ci: build + lint + corpus)
   - `python-tests`  (barint_ci: engine/BSIP test suite)
   - `off-sweep`  (barint_ci: OFF ban)
   - `e2e-smoke`  (barint_ci: Playwright smoke + a11y)
   - `conformance`  (bari_page_gates: regression-protective spine gate)
   - `off-ban-census`  (bari_page_gates)
4. If any screen demands a plan upgrade: STOP and report back — no new paid services without explicit opt-in.

## Do NOT require these checks (they do not run on every master push — requiring them would strand deployments waiting forever)
- `shadow-backtest` / gold gate (shadow_gate.yml — path-filtered to engine files)
- `validate-returns` (c0_return_gate.yml — pull_request only)
- run_gates — not in CI yet (TASK-565 BLOCKED on 563/564)

## Notes
- GitHub identifies checks by JOB NAME; if we ever rename these jobs, the Deployment Checks selection must be updated or promotion stalls (documented Vercel limitation).
- After enabling, the next master push is the live test: watch the deployment page show "Checks" between Build and Promote.

# TASK-571 — Vercel: hold production alias until checks pass (deployment gating)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
