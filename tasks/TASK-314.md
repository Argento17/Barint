---
id: TASK-314
title: Monorepo → live reconciliation — get the re-baseline publish (and future work) onto the actual bari.digital deploy source
owner: orchestrator
status: BLOCKED
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-310, TASK-312, TASK-313]
blocks: []
category_id: null
blocked_on: final confirmation that origin/master (Argento17/Barint) is the Vercel production branch (owner doesn't know offhand; strong evidence points to it)
deploy_source_finding: >
  STRONG LEAD (2026-06-17): the local repo has TWO remotes — `bari` (Argento17/bari = OLD standalone, root layout,
  the WRONG target I pushed to earlier) and `origin` (Argento17/Barint = the monorepo). origin/Barint `master` HAS
  `bari-web/` and already carries 4 of the 7 pages (cereals_v2, granola_v1, juices_v3, hummus_v5) → almost certainly
  the real bari.digital deploy source (Vercel root=bari-web, prod branch likely origin/master). Could not 100% confirm
  the Vercel production branch (no dashboard access; owner unsure). Relationship: task-275 is 27 ahead / 18 behind
  origin/master (DIVERGENT); local master 21 ahead / 18 behind. 3 publish pages MISSING on origin/master
  (cakes_hard_cookies, cookies_coffee, brined_cheeses) = new categories to add. So landing = a reconciliation of the
  18-commit divergence + add 3 new pages + overlay the 4 existing — NOT a fast-forward. ⚠️ Pushing to origin/master
  triggers the live deploy (irreversible) → owner-gated.
summary: >
  The 7-page re-baseline publish is verified, committed (ecc515d30 + 0edac53c9), and pushed on branch
  task-275-engine-fixes-abc — but it CANNOT cleanly reach the live site. Discovered 2026-06-17 at the push/PR step:
  the GitHub remote (Argento17/bari) default branch `main` is the OLD STANDALONE website (Next.js app at repo ROOT,
  comparison JSONs at `src/data/comparisons/`), while ALL current work is in the NEWER MONOREPO layout (website as a
  subtree under `bari-web/`, JSONs at `bari-web/src/data/comparisons/`). The two share one remote but have DIVERGENT
  history (local master/task-275 is 93–98 commits ahead of `bari/main`; `bari/main` has 22 commits not in our line)
  AND DIFFERENT FILE LAYOUTS. main has no `bari-web/` dir; 4 of the 7 pages (cakes_hard_cookies, cookies_coffee,
  juices_v3, brined_cheeses) don't exist on main at all; main still carries older versions (cereals_v1, hummus_v3/v4)
  + wiped categories (butter/cheese/maadanim/yogurts/bread). So this is a REPO MIGRATION, not a publish.

  UNKNOWN to resolve first: where bari.digital ACTUALLY deploys from (this old `main`? a different branch? a Vercel
  project rooted at the monorepo's `bari-web/`?). No vercel.json in-repo; CI workflows are gates, not deploy.

  Scope when unblocked: (1) confirm the true deploy source (owner/Vercel dashboard); (2) decide reconciliation strategy
  — migrate monorepo `bari-web/` into the live structure, or repoint Vercel to the monorepo, or merge lines; (3) reconcile
  the 93/22 divergent histories safely; (4) land the 7 verified pages on the real deploy source; (5) re-run the gate
  (build/score==trace/OFF/contradictions) against the deployed frontend. Owner ruling 2026-06-17: HOLD — do this
  deliberately, not under remote-control time pressure. Branch stays safely pushed; nothing deployed; nothing lost.
---

# TASK-314 — Monorepo → live reconciliation (BLOCKED on deploy-source confirmation)

The publish work is done and verified (TASK-308/309/310/312/313, red-team 0 CRITICAL). The blocker is purely topological:
the live GitHub branch is a structurally different (older, standalone) tree than the monorepo where the work lives.
Resolve the true deploy source first, then choose the migration/reconciliation path. See DISPATCH_BOARD for the full trail.

## Progress 2026-06-17 (owner: "if you found it, might as well fix it")
- Deploy repo identified = **Argento17/Barint** (`origin`); `master` has `bari-web/`. It already has routes for 4 of the 7
  pages (cereals/granola/juices/hummus + /vegetable-spreads) but NOT for cakes/cookies-coffee/brined.
- **✅ PR #7 opened on Argento17/Barint** (https://github.com/Argento17/Barint/pull/7), base `master` ← `publish/rebaseline-4pages`:
  data-only overlay of the 4 verified route-ready pages (cereals_v2, granola_v1, juices_v3, hummus_v5). Vercel preview = build check.
  **Merge = go-live for those 4 (owner-gated).** Nothing merged/deployed.
- **REMAINING (task stays open):** (1) confirm origin/master IS the Vercel production branch; (2) port FRONTEND (route +
  page-data loader + components) for cakes / cookies-coffee / brined onto Barint so their re-baselined pages can land; (3) reconcile
  the broader 18/27-commit divergence. Mistaken push to Argento17/bari (old standalone) is harmless; clean up later.
