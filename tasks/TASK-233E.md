---
id: TASK-233E
title: "Comparison-page product images do not load on first paint (recurring frontend bug)"
owner: frontend-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: []
blocks: []
roadmap_impact: true
work_type: frontend-bug
---

# TASK-233E — Product images don't load on first visit

Owner-reported, recurring: "the comparison page does not parse product images at first time and
every time I need to say something about it." Images appear missing/broken on first paint and
only resolve after some interaction/re-trigger. Repeats across categories.

## Diagnose (Frontend Agent)
- Reproduce on a real comparison route; capture whether it's first-paint only, hydration-related,
  lazy-load/IntersectionObserver, `next/image` config, or URL-resolution.
- Note: several categories use **synthesized image URLs** (e.g. frozen veg builds a Cloudinary
  `MNH68_Z_P_{barcode}_1.png` string in the generator) — confirm whether the bug is a broken/slow
  URL, a missing `next/image` domain/remotePatterns entry, an `onError` fallback gap, or a
  client-side load-timing issue. Separate "wrong URL" from "right URL, loads late."
- Identify the shared image component in the collapsed row / expansion and where the defect lives.

## Outcome (Frontend Agent, 2026-06-10) — TWO distinct causes
1. **Load timing (the recurring "first visit" bug) — FIXED.** Thumbnails used `loading="lazy"`
   with no priority; lazy `<img>` in a freshly-hydrated client component defers the fetch until a
   scroll/interaction. Fix applied: `eager` + `fetchPriority="high"` for the top-6 above-the-fold
   rows (`bari-product-thumbnail.tsx`, `comparison-row.tsx`, `comparison-table.tsx`). `tsc` clean,
   build passes, verified on cheese + hummus (real 200 URLs).
2. **Frozen-veg broken images (404) — NOT a frontend bug → routed to Data.** The generator
   synthesizes `MNH68_Z_P_{barcode}_1.png`; that prefix is a guess and 404s. Scraped categories
   carry the product's real Shufersal prefix (cheese `TZE58_`, hummus `UFL56_`, …) → 200. Moved to
   **TASK-233D** as a data fix.

## DoD
- [x] Root cause identified (split into timing vs. wrong-URL) with file:line + reproduction
- [x] Timing fix applied; images load on first paint on scraped-URL categories
- [ ] **Owner to confirm** the live first-paint behavior is resolved
- [ ] Frozen-veg image URL fixed under TASK-233D (separate, Data)
