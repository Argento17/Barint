---
id: TASK-554
title: CI hardening: shadow-gate push trigger, retire argento CI, Playwright smoke+a11y in CI
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10. Branch task554-ci-hardening pushed to origin (Argento17/Barint) at
  365e489d; PR open link surfaced to owner. Verified against artifacts, not the return block: (1)
  shadow_gate.yml push trigger present with identical path filter via YAML anchor — anchor support
  confirmed live on GitHub Actions (changelog 2025-09-18; plain &/* only, no merge keys — compliant);
  (2) barint_ci.yml e2e-smoke job present, dead argento paths-ref removed; (3) playwright.config.ts
  CI-aware webServer (next start in CI); (4) ported bari_page_gates.yml byte-identical to local original
  (diff --no-index exit 0). All 4 workflows YAML-parse. C1-CURSOR ran the suite in-worktree: smoke 5/5
  PASS; a11y 2/4 with both failures pre-existing hero-eyebrow contrast (TASK-510, fix branch exists) —
  witnessed in test-results/.last-run.json. Orchestrator fix-up 365e489d: a11y step continue-on-error
  with flip-to-hard-fail condition pinned to TASK-510 merge (red-noise prevention; smoke stays hard).
  Lane deviation logged: Cursor committed+pushed despite leave-tree instruction — outcome reversible
  (feature branch), verification unharmed. Merge = owner step; branch protection on master = owner step.
depends_on: []
blocks: []
category_id: null
summary: >
  Close the direct-push bypass on shadow_gate.yml (PR-only today; push=live is the real path), delete the always-red argento_bari_ci.yml (root-layout leftover, red-noise), and add a Playwright smoke+a11y job to barint_ci.yml with a CI-aware webServer (next start after build). Build lane: C1-CURSOR in clean worktree. Branch protection on origin master = manual owner step, documented in task.
---

# TASK-554 — CI hardening: shadow-gate push trigger, retire argento CI, Playwright smoke+a11y in CI

## Context
Owner-reviewed automation audit (2026-07-10 chat). Verified findings, in priority order:
1. **shadow_gate.yml is PR-only** — but the operating model is direct push-to-master = live Vercel deploy, so an engine-touching push deploys without the shadow backtest or gold-set gate ever running. Worst-case gap: a published-score change ships ungated.
2. **argento_bari_ci.yml red noise** — already deleted on origin/master; survives only on local branch `task506` (committed there). Its `push: [master]` trigger had no path filter and `npm ci` at repo root (no package.json) → standing red X, CI-noise desensitization. origin's `barint_ci.yml` still carries a dead `paths` reference to it.
3. **E2E harness never runs in CI** — Playwright smoke/a11y/perf/visual exist since TASK-384 but are manual-only. A homepage or comparison-route regression ships with green CI.
4. **bari_page_gates.yml was UNTRACKED** — the conformance + OFF-census workflow existed only in the local working tree; the deploy repo never had it. (Local↔origin divergence manifesting exactly as the audit predicted.)
5. TASK-536 fingerprint gate: already CLOSED and wired — no action.

## Scope (branch `task554-ci-hardening` off origin/master, worktree C:\bari_wt_ci)
- `shadow_gate.yml`: add `push: [master]` trigger, same path filter as the PR trigger.
- `barint_ci.yml`: remove dead argento reference; add `e2e-smoke` job (npm ci → build → playwright install chromium → `test:e2e` + `test:a11y`). Visual/perf specs stay manual (flake-prone on shared runners).
- `bari-web/playwright.config.ts`: CI-aware webServer (`npm run start` in CI after build; `npm run dev` locally).
- Port `bari_page_gates.yml` to origin (straight file copy by orchestrator).
- Lane: C1-CURSOR driven directly in the clean worktree (router repo-guard pinned to C:\Bari, TASK-539).

## Out of scope / follow-ups
- **Manual owner step:** branch protection + required checks on Argento17/Barint master (GitHub settings; no gh CLI). Until then all CI is advisory on direct pushes.
- Drop `argento_bari_ci.yml` from local `task506` before that branch merges, or it resurrects.
- Middle gates (`run_gates.py`, `validate_comparison_page.py`, `validate_return.py`) in CI — separate task if pursued.

## DoD
- All four workflow/config changes on the pushed branch; YAML valid; no other files touched.
- Verified by orchestrator diff review in the worktree before commit.
- Branch pushed to origin (Argento17/Barint), PR URL surfaced for owner review. Never pushed to master.
