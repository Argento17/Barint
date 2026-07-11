---
id: TASK-587
title: Magnesium guide v3.2 - dose axis starts at corpus min 76, RDA band as on-track shaded zone, collapsed education section made findable (visible heading + teaser)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-11
close_reason: >
  All three owner-confirmed fixes LIVE on bari.digital/madrichim/magnesium (master
  7b035a90 -> ba64bed7, branch deploy/mag-guide-v32, implementation commit 84fd4ed0
  rebased; live ~75s post-push on strict markers; orchestrator live-render vision check
  passed; noindex preserved). Chain: Design D12 spec (mag_guide_v32_visual_spec.md) with
  in-code root causes (pct() hard-wired 0-domain; band top:17px open dashed border;
  summary-styled toggle) -> Content gate-1 ADDENDUM v3.2 (package sha 8bd401e4...:
  heading "ההסבר המלא ומקורות המידע" + 15-word teaser, fact-checked vs all 6 spine
  sections) -> Frontend implementation (5 files; domainMin/minTickLabel VM fields;
  hideZeroTick deleted, zero callers; strings byte-exact by script) -> Design vision
  verify 17/17 (incl. gap-closing evidence: safety-gauge screenshots + synthetic in-band
  dose proving paint order, reverted clean) -> QA gate-2 GO (Track V green, 0 CRITICAL/
  HIGH, 2 MEDIUM monitors; geometry re-measured independently 25.68% / 52.71-77.48%;
  strings re-gated independently).
depends_on: []
blocks: []
category_id: null
summary: >
  Owner 2026-07-10 (AskUserQuestion, both scale options + deep-content option chosen): dose axis 76-520, RDA band on-track zone, education section findable. v3.2 live.
---

# TASK-587 — Magnesium guide v3.2 — axis, band, findable education

## Delivered (LIVE, noindex, master @ ba64bed7)
1. **Dose axis 76-520**: "76" tick+label flush at the track's right end, "520" at the left,
   no dead 0-76 lead-in; median 190 line at 25.68% from right; marker (V-76)/444. Safety
   gauge unchanged (0-based, 0/250/350). cannot_verify / evidence_limited markers stay
   dead-center. Axis now matches the intro's "בין 76 ל-520".
2. **RDA 310-420 band = on-track shaded+bordered zone** (8px, #6B7070 16% fill + dashed
   border, centered on the track, marker paints above) at 52.70-77.48% from right; the old
   floating dashed outline is gone.
3. **Education section findable**: always-visible section heading "ההסבר המלא ומקורות
   המידע" + 15-word teaser + chevron; still collapsed by default; all 6 sections + 3
   clickable sources inside; card border dropped, heading style matches sibling sections.

## Formal amendments recorded (per implementer request)
- **Spec item 14 amended by orchestrator ruling**: "one-line teaser" = ONE SENTENCE,
  ≤2 rendered lines at 375px, no truncation/overflow (not one literal visual line).
  Current teaser: 1 line desktop, 2 lines mobile — PASS under the amendment.
- **Process**: scope amendments must go DIRECTLY from orchestrator to the implementer,
  not by peer relay (frontend-587 correctly refused to act on a secondhand amendment
  until file-hash evidence converged; a Content shorter-teaser revision was authored and
  cleanly retracted, package restored byte-identical to the signed state).

## Artifacts
- `02_products/supplements/magnesium/mag_guide_v32_visual_spec.md` (Design D12; note: its
  embedded return-contract hash self-references and trails by one save, by construction)
- `02_products/supplements/magnesium/mag_guide_v3_copy_package.md` ADDENDUM v3.2 (final
  sha256 8bd401e47eeb5718b622a366ce09bc7364ecf3d678c23ed3cd087c9786389168)
- Render evidence: scratchpad v32-*.png (16), qa-v32-*.png (5), live2-first-card-expanded.png

## Monitors / follow-ups (none block)
- **RT-M1 (design/product monitor)**: truncated axis (76-origin) can visually amplify
  inter-product gaps; defensible (neutral un-toned zone, both ends labeled, range
  disclosed, owner-confirmed choice). Revisit only if the owner reacts.
- **RT-M2 (informational)**: band-under-marker paint order unreachable in today's corpus
  (no clear dose in 310-420); proven via synthetic placement; re-verify on the first real
  in-band product.
- Standing items unchanged: RT-1 heading-2/median tension + שלושה→ארבעה bundle +
  servings-per-day re-parse + index flip (all owner-side, tracked in TASK-577/580).
- New owner ruling intersection (2026-07-10, no-cited-nutritional-values-in-prose): the
  guide's 18 one-liners cite mg doses; owner-dictated card fact lines are structured
  fields (fine), but the prose one-liners belong to the corpus-wide rewrite program's
  sweep — flagged there, deliberately NOT rewritten in this task.
