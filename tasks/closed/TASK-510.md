---
id: TASK-510
title: category-hero eyebrow contrast fails WCAG 1.4.3 (live a11y gate red on all category pages)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-04
closed_at: 2026-07-05
close_reason: >
  Scoped objective DONE + orchestrator-verified (2026-07-05 unattended run). category-hero.tsx:28
  eyebrow 'text-[#1F8F6A]/80' (composites 2.981:1 on white, WCAG FAIL) → 'text-[#176F53]'
  (--bari-green-deep, 6.113:1 PASS). Commit 2e216193 on fix/task510-hero-contrast (worktree
  C:\bari_wt_t510, off origin/master c6993b48). Orchestrator confirmed: git diff = exactly 1 file /
  1 line (so it cannot have introduced any other defect); contrast math re-derived; mobile a11y
  4/4 routes 0 serious/critical (exit 0); tsc 0, lint 0 errors; C0 validate_return PASS.
  NOTE — full desktop test:a11y still exits 1, but on PRE-EXISTING sibling defects NOT in this
  task's scope (carousel category chips #1F8F6A/#E8F5EF 3.6:1; rank chips #7a817c 3.85-3.99:1; +5
  other-page eyebrows) → captured as TASK-512. This close covers ONLY the CategoryHero eyebrow, which
  is fixed; the a11y gate is NOT claimed globally green. Branch NOT pushed — push+PR queued for
  supervised morning.
depends_on: []
blocks: []
category_id: null
summary: >
  Pre-existing WCAG 1.4.3 SERIOUS fail confirmed LIVE by TASK-507 Design review (untouched by 507). category-hero.tsx:28 'text-[#1F8F6A]/80' composites to #4ca588 on white = 2.98:1 (needs 4.5:1); fails 2/4 a11y gate routes; affects every page using CategoryHero. Ready fix (Design spec): change to 'text-[#176F53]' (--bari-green-deep token, colors_and_type.css:15) = 6.11:1, keeps brand-green kicker; one line. Re-verify: npm run test:a11y (expect 0 serious/critical across 4 routes). Ship as its own small PR, separate from the TASK-507 nav module.
---

# TASK-510 — category-hero eyebrow contrast fails WCAG 1.4.3 (live a11y gate red on all category pages)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
