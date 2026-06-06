---
id: TASK-185
title: Breakfast-cereals cover image — replace oats visual (no longer representative after granola/muesli split)
owner: design-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
closed_at: 2026-06-05
depends_on: []
blocks: []
category_id: breakfast-cereals
cc_close_note: >
  Close-readiness gate PASS (orchestrator-verified 2026-06-05). The oats photo was reassigned to the
  new גרנולה ומוזלי card (public/hashvaot/themes/granola.jpg). The cereals cover was COMPLETED per
  owner directive: a real cornflakes photo sourced from Pexels (photo 3886613, Pexels License —
  free commercial use, no attribution), 1700x2550 portrait, viewed/verified as cornflakes (not oats/
  granola), committed to public/hashvaot/themes/breakfast-cereals.jpg and wired to the featured card
  (theme.photo restored). next build PASS, both routes render. Scope: only the two featured cards +
  theme assets touched.
summary: >
  The breakfast-cereals hashvaot cover photo is rolled oats (/hashvaot/themes/breakfast-cereals.jpg). After the granola/muesli split the cereals page is cornflakes + kids cereals + puffed (only a couple of oat items), so the oats hero misrepresents the page. Design selects a representative cereals visual (e.g. cornflakes / mixed bowl); consider re-using the oats photo for the new granola/muesli category. Frontend swaps the asset + featured-card theme.
---

# TASK-185 — Breakfast-cereals cover image — replace oats visual (no longer representative)

## Why
The breakfast-cereals hashvaot cover photo (`bari-web/public/hashvaot/themes/breakfast-cereals.jpg`)
is **rolled oats**. After the granola/muesli split, the breakfast-cereals page is dominated by
cornflakes, kids' cereals (Nesquik/Lion/Trix/Cini Minis), puffed rice and oat bran — only a couple of
oat items remain (שיבולת שועל עבה, קוואקר). The oats hero now misrepresents the page, and oats read as
the visual identity of the *granola/muesli* category instead.

## Scope (Design owns the choice; Frontend implements)
1. **Design:** select a cover image that represents the cereals page — e.g. cornflakes / a mixed cereal
   bowl / assorted boxed cereals. Match the existing card treatment (accent `#7A8C5E`, dark gradient
   overlay, no too-bright center per `category_factory_v1.md` Stage 11).
2. Decide whether to **re-use the current oats photo for the new גרנולה ומוזלי category**
   (`featured-granola-intelligence-card.tsx` currently borrows `breakfast-cereals.jpg`) or source a
   distinct granola visual.
3. **Frontend:** place the asset(s) under `public/hashvaot/themes/`, update the `theme.photo` in
   `featured-breakfast-cereals-intelligence-card.tsx` (and granola card if reassigned), verify on
   `/hashvaot`. `next build` passes.

## Definition of Done
- Cereals cover no longer shows oats and is representative; granola/muesli card has an appropriate
  (oats or dedicated) image; both render correctly on `/hashvaot`; build green.
- Proposes RETURNED; CC records CLOSED.

**Assigned:** design-agent (+ frontend-agent for implementation). **Related:** TASK-140, TASK-184.
