---
id: TASK-512
title: Residual WCAG 1.4.3 a11y debt: carousel category chips + rank number chips + 5 non-gate-page eyebrows (#1F8F6A/80, #7a817c)
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-05
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10, commit e11d48f5 (branch task559-a11y-hardfail, pushed; PR awaits
  owner). All three debt classes from the spec cleared, display-only: (a) every remaining
  text-[#1F8F6A]/80 eyebrow (2.98:1) → text-[#176F53] (6.11:1) in hashvaot/page.tsx, newsletter/page.tsx,
  products/demo/page.tsx (×2), hashvaot-category-landing.tsx; (b) carousel category chips #1F8F6A on
  #E8F5EF → #176F53 (found in micro-comparison-snapshot-card.tsx BADGE_COLORS, plus its metric + footer
  greens); (c) rank chips #7a817c (3.85–3.99:1) → var(--fg3, #5E6560) (~6:1). C1-CURSOR built; the
  orchestrator caught and fixed a REAL DEFECT it introduced: it emitted a bare `var(--fg3)`, but --fg3 is
  never declared at :root anywhere in the repo (grep: it exists only as `var(--fg3, #5E6560)` in 6 other
  files) — so the bare form resolved invalid and the rank chips silently inherited their parent color,
  i.e. the "fix" was broken. Fallback restored to match the documented convention
  (inventory-grade-chip.tsx: "--fg3 (#5E6560) — ≥4.5:1 on white"). Cursor also stripped a BOM and
  ASCII-fied box-drawing comment chars (kept: net-positive given repo mojibake history). Evidence:
  grep proves 0 residual `1F8F6A]/80` or `7a817c` in bari-web/src/; full a11y suite 8/8 PASS (was 6/8) on
  a production server (next start :3100, both mobile+desktop projects); smoke 10/10; lint 0 errors; build
  clean. Diff reviewed line-by-line: colors only, no layout/DOM/copy/logic change. Cursor lane note: the
  agent hung on output flush after completing all edits (0 bytes stdout, tree stable across checks) —
  killed; deliverable was complete and independently verified.
depends_on: []
blocks: []
category_id: null
summary: >
  Surfaced by TASK-510. Pre-existing on origin/master (NOT introduced by 510's one-line hero fix, confirmed by 1-line diff). Desktop test:a11y still red on: (1) carousel category chips #1F8F6A on #E8F5EF bg = 3.6:1; (2) rank number chips #7a817c on white = 3.85-3.99:1; plus 5 remaining text-[#1F8F6A]/80 (2.98:1) eyebrow occurrences in 4 non-gate-route pages: app/hashvaot/page.tsx:26, app/newsletter/page.tsx:27, app/products/demo/page.tsx:799+808, components/hashvaot/hashvaot-category-landing.tsx:35. Apply same darkening pattern (#176F53 for eyebrows; pick AA-passing shades for chips). Own PR; display-only.
---

# TASK-512 — Residual WCAG 1.4.3 a11y debt: carousel category chips + rank number chips + 5 non-gate-page eyebrows (#1F8F6A/80, #7a817c)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
