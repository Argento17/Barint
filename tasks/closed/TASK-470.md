---
id: TASK-470
title: Mascots: mobile visibility + port catalog/magnesium placements to production
owner: frontend-agent
status: CLOSED
close_reason: >
  PR #54 merged (a85abec2), production-verified 2026-07-03 (cache-busted): catalog OLI mascot
  (mascot-oli-catalog) live in served /catalog HTML + magnesium hero mascot (mascot-mg-magnesium)
  live in served /hashvaot/magnesium HTML — both were absent before. Homepage mascots un-hidden on
  mobile (CSS shipped in same merge). Design vision-critic GO_WITH_FIXES (fixes applied: radar
  w-24, PNGs 3.16MB→193KB −94% + width/height/sizes). tsc/build/lint 0; 0 h-scroll @390px on 3 routes.
  Decorative aria-hidden mascots (no Content gate). Did NOT merge the stale feature/homepage-mascots
  branch — only the mascot pieces re-applied on current master. Screenshots: tasks/returns/TASK-470_screenshots/.
priority: HIGH
created_at: 2026-07-03
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-reported: homepage mascots hidden on mobile (hidden sm/md/lg gating) + catalog & magnesium comparison mascots never shipped (stranded on unmerged feature/homepage-mascots branch). Fix: (A) make 3 homepage mascots mobile-visible with tuned sizing; (B) port OLI catalog mascot + Mg magnesium hero mascot onto current origin/master incl. mascot-mg-magnesium.png asset. Decorative/aria-hidden => Design gate (no Content). Render mobile+desktop, screenshots for owner, PR.
---

# TASK-470 — Mascots: mobile visibility + port catalog/magnesium placements to production

## Status — 2026-07-03: OWNER PR OPEN, awaiting inspection + merge
- **PR #54: https://github.com/Argento17/Barint/pull/54** — branch `feat/task470-mascots` (3 commits, worktree C:\bari_wt_t470 off origin/master). Does NOT merge the stale feature/homepage-mascots branch — only the mascot pieces re-applied on current master.
- Diagnosis (orchestrator, verified vs LIVE): (A) 3/4 homepage mascots gated hidden sm/md/lg → phone showed only NORI; (B) catalog OLI + Mg hero mascots existed only on stale unmerged feature/homepage-mascots (121 behind master), never shipped; mascot-mg-magnesium.png branch-only.
- Chain: build (P488, 5a4f4988+849ddf73: un-hid 3 homepage mascots mobile-tuned, ported OLI-catalog + Mg-hero incl. asset, added CategoryHero optional `mascot` slot + comparison-page `heroMascot` passthrough — no-op for other cats) → Design vision-critic GO_WITH_FIXES (P490: 0 CRIT, RTL ok, desktop unregressed, no-op confirmed; flagged radar mobile proportion + 2 oversized eager PNGs) → polish (P491, 51c52f99: radar w-32→w-24; PNGs 3.16MB→193KB (−94%) via 700px downscale + width/height/sizes props).
- Gate: Design vision-critic (decorative aria-hidden mascots → no Content gate). Screenshots tasks/returns/TASK-470_screenshots/ (5 surfaces × mobile+desktop, all re-verified post-polish). tsc/build/lint 0; 0 h-scroll @390px on /, /catalog, /hashvaot/magnesium.
- **Pending owner:** inspect (Vercel preview on PR #54) + merge.
- **Related (separate, awaiting owner):** snapshot audit (6871d374) = safe to abandon stale branch; open Q to owner = is Gen-Z homepage redesign still live + preserve project_gen_z/OWNER_DECISIONS.md before branch drop.
