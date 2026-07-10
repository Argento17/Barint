---
id: TASK-580
title: Magnesium guide v3.1 - dose-gauge geometry bug in card disclosures (all products) + intro expanded to explain assessed dimensions
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Both owner items LIVE on bari.digital/madrichim/magnesium (master 55654f3d -> d3da95af,
  branch deploy/mag-guide-v31: aa65af9c intro, da0567fa gauge, d3da95af metadata; live
  confirmed ~30s post-push on strict markers; orchestrator live-render vision check passed;
  noindex preserved). GAUGE: root cause = dir="ltr" override at threshold-bar-row.tsx:360 +
  physical `left` positioning, so ALL FOUR bar types rendered an LTR-ascending axis on the
  RTL page. Design Agent D12 ruling + spec (mag_guide_gauge_rtl_spec.md), Frontend mirrored
  pct->100-pct (30/30 scripted RTL assertions), Design vision-verified 14/14 with independent
  pixel-math recomputation, QA gate-2 GO re-measured all 12 assertions independently.
  INTRO: Content gate-1 addendum (package sha 7cf39f4c...); v3.1-SLOT-2 four-dimension
  variant wired byte-exact (372/372); QA RT-4 (intro/metadata count mismatch) resolved by
  restoring the TASK-575 two-gate-signed four-dimension metadata description (141/141).
  Notable process catch: the first Frontend pass declared "cannot reproduce" after 208
  boundingBox assertions - they validated LTR self-consistency, the wrong invariant; the
  orchestrator's image-read of the agent's own screenshots confirmed the owner's report.
depends_on: []
blocks: []
category_id: null
summary: >
  Owner 2026-07-10 (screenshot): gauge bug on all products + intro "not good enough", must detail the measured dimensions. Fixed via Design ruling + full two-gate loop; v3.1 live.
---

# TASK-580 — Magnesium guide v3.1 — gauge RTL fix + four-dimension intro

## Delivered (LIVE, noindex, master @ d3da95af)
1. **Gauge axis now RTL-ascending on all four bar types** (מינון, בטיחות, צורה וספיגה,
   שקיפות תווית): min/worst at the track's right edge, max/best at the left; RDA 310-420
   band, median-190 tick, over-max "+" clamp all mirrored; evidence_limited and
   cannot_verify center markers direction-invariant and unregressed (TASK-575 monitor items).
   Component: bari-web/src/components/guides/threshold-bar-row.tsx (only file in the gauge
   commit; zero consumer strings changed).
2. **Intro explains the four assessed dimensions** (v3.1-SLOT-2, 60 words): dose vs the
   76-520 corpus, form/absorption, safety as a digestive-comfort threshold, label
   transparency. Metadata description restored to the TASK-575-signed four-dimension string
   so the page no longer contradicts its own meta (QA RT-4).

## OWNER ACCEPT-OR-REVERT BUNDLE (pending, flagged, one unit)
The owner's dictated intro said "שלושה דברים"; the page assesses four bars. Shipped the
honest four-count (intro + matching metadata) as the orchestrator's recommended default.
Owner may revert to his exact original sentence (SLOT-1 variant, one-line change) — but the
metadata must move in lockstep either way.

## Artifacts
- `02_products/supplements/magnesium/mag_guide_gauge_rtl_spec.md` (Design D12; sha256 43f689b8b6c5fc81293d6bbe4e2829aae70d81270706de81de9a22fedfd0d827)
- `02_products/supplements/magnesium/mag_guide_v3_copy_package.md` ADDENDUM v3.1 (final sha256 7cf39f4c22e161497fae226907e76608f54fac13e780d04ae3feefca13153e47)
- Render evidence: scratchpad v31-rtl-fixed-*.png (12), qa-v31-*.png, live-v31-gauge-min.png

## Process lesson (recorded in memory)
A 208-assertion boundingBox sweep "could not reproduce" the owner's visual bug because it
asserted the rendered math was self-consistent without asking which DIRECTION is correct.
Visual bugs are adjudicated by reading screenshots AS IMAGES (owner screenshot -> orchestrator
vision read -> Design Agent ruling), never by geometry containment alone. Also: dir="ltr" +
physical `left` positioning is a trap — the dir attribute controls nothing when positions are
physical; mirroring must happen in the math.

## Open follow-ups (none block)
- Owner bundle above (שלושה→ארבעה intro + metadata).
- RT-1 heading-2/median tension — unchanged from TASK-577, still gates the index flip.
- Servings-per-day label re-parse (Data Agent) — unchanged from TASK-577.
- Design spec wording gap noted by Design itself: summary table said "flush left edge" while
  the 11px halo-clip inset is correct behavior; spec updated ruling recorded (ACCEPT inset).
