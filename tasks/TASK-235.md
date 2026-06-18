---
id: TASK-235
title: "Frozen Vegetables v2 — score-free use-case guide (4 segments · benefit highlights · USDA generic reference)"
owner: product
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
completed_at: null
depends_on: []
blocks: []
related: [TASK-233, TASK-236]
category_id: frozen-vegetables
roadmap_impact: true
work_type: objective
deferred: false
summary: >
  Reconceive the frozen-vegetables comparison as a score-free, benefit-first
  use-case guide. The processing-quality score (0-100/A-E) is removed for this
  category — it answered "how minimally processed per 100g," which collapses 35/53
  products at exactly 85/A and punishes seasonings (crushed garlic 60/C for the
  oil+salt that make it garlic paste). Replaced by 4 use-case segment bands, each
  with its own lens, surfacing what a realistic portion delivers (benefit highlights),
  with USDA FDC used as generic reference enrichment for the micronutrients Israeli
  labels omit. Owner-approved 2026-06-10. Frozen-vegetables-ONLY; not a precedent.
---

# TASK-235 — Frozen Vegetables v2 (score-free use-case guide)

## Status
**IN_PROGRESS — Phase 1 LOCKED (owner-approved 2026-06-10).** No implementation yet.

## Owner decisions (locked 2026-06-10)
- Frozen-vegetables-only; **not** a precedent for other categories.
- Remove the score chip + A/B/C/D for this category.
- Segment bands instead of global ranking.
- **Highlights only — no replacement benefit score, no hidden benefit number.**
- Aromatics stay inside the page under **תיבול ובישול** (not split out).
- USDA FDC = generic reference enrichment only, never product-label fact.
- "Missing fiber = 0" is a broader engine issue → logged separately (**TASK-236**), not solved here.

## Approved segments
1. **ירקות בודדים** (single vegetables) — `plain-veg` (21)
2. **קטניות** (legumes) — `legumes` (14)
3. **תערובות וארוחות** (blends & meals) — `mixes` + `pasta-blends` + blend `processed`
4. **תיבול ובישול** (seasoning & cooking) — `herbs-seasonings` (8) + single-veg `processed`

## Hard rules (binding all phases)
No "best overall" · No A/B/C/D or 0-100 · No hidden benefit score · No recommendation language
(מומלץ/בריא יותר/כדאי) · No USDA-derived exact product claims without Nutrition sign-off ·
No consumer copy before Content + Nutrition approval.

## Phase plan
- **Phase 1 — Lock the model.** ✅ DONE. Deliverable: `02_products/frozen_vegetables/frozen_vegetables_v2_phase1_spec_v1.md` (final segment defs, benefit facts allowed per segment, copy model, USDA source/confidence policy).
- **Phase 2 — External-data spine.** ✅ DONE (2026-06-10, owner-authorized). Deliverable: `02_products/frozen_vegetables/frozen_vegetables_benefit_lookup_v1.json` (seed: `..._phase2_seed_v1.json`). Data Agent built the explicit reviewable USDA-generic→SKU join (17 distinct generics, Foundation/SR Legacy, all `candidate`/`is_generic_reference`-stamped; extended `usda_fdc.py` NUTRIENT_MAP additively with Vit C/A/K + folate). Nutrition Agent signed off **GO**: final joins **44 reviewed / 9 not_characterized / 0 candidate** (Jerusalem artichoke → not_characterized, raw-basis only; edamema confirmed green not mature; blends never synthesized). Phrasing block `phrasing_APPROVED` with `nutrition_signoff` stamp. No score/trace/engine/frontend touched; absence-≠-zero enforced on display side.
- **Phase 3 — Re-author all 53 copy.** ✅ DONE (2026-06-10). Deliverable: `02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json` (input: `..._phase3_copyinput_v1.json`). Content authored 53/53 score-free copy (standing marker + 2-line verdict + expansion; "מה לדעת" for seasonings). Nutrition signed off **126/126 claims APPROVED** (1 orphaned table row dropped; 0 REVISE) — claim table tags every fact label / USDA-generic-reference / composition-identity. QA leak-scan **PASS** — all 7 vectors CLEAN (no score/grade/recommendation/framework-term/OFF; USDA framing intact; 9 not_characterized carry zero benefit claims). No frontend/generator/engine touched. **Open item for Phase 4/Product:** Nutrition flagged artichoke-bottoms (107189, 7296073445159) banding — currently band 4 (תיבול); reads more like a prepped vegetable. Nutrition-honest as-is (band 4 surfaces no nutrition); re-band is a UX/Product judgment, not a blocker.
- **Phase 4 — Frontend.** ⏳ IMPLEMENTED + PUSHED TO PREVIEW (2026-06-10), gate OPEN pending owner preview review + live QA/red-team. Branch `cc-agent-v2` commit `f589fed6` pushed to origin → Vercel preview. Built in isolated worktree `C:/Bari-frozen-v2` (salty-snacks tree untouched). Self-contained score-free page (does NOT route through shared ComparisonPage — avoids its "הציון מסכם…" footer leak); 16 other categories byte-identical. Data: `frozen_vegetables_frontend_v2.json` (scoreFree, 4 bands 21/14/8/10, 53/53 images) + `frozen_vegetables_shell_copy_v2.json` (Content+Nutrition-approved shell prose). Removed A/B/C/D chip + score-sort; 4 use-case bands + standing-marker tags + 2-line verdict + expansion. **Validated:** tsc --noEmit PASS, eslint PASS, QA leak-scan PASS (all 7 static checks), 53/4-bands/9-not-char/no-old-copy/isolation confirmed. **LIVE VALIDATION (2026-06-11, local build — Vercel URL unobtainable from env, ran locally instead):** Real `next build` PASSED (✓ 5.9s, frozen route prerendered static). Against the real prerendered DOM: route resolves, **53 rows in bands 21/14/8/10**, all 4 band titles, 53 Cloudinary images present, standing markers present, expansion markup present, mobile+desktop frames + RTL present; leak scan CLEAN (3 "ציון" all negated, no grade/chip/NN-grade, no old v1 phrases). **BLOCKERS found by design+red-team:**
  - **RT-1 CRITICAL (verified):** all 53 `imageUrl` use a fabricated single prefix `MNH68` (inherited from v1); real per-product paths (WAC20/WAQ16/WBH24…) live in BSIP1 `image_url`. 53 broken images → not go-live-able. Fix = repopulate `imageUrl` from BSIP1 verbatim, regen v2 JSON, re-verify. Routes to data-agent + qa.
  - **Design B1 (desktop):** rows don't adapt at lg:1180px — verdict text stretches edge-to-edge, never picks up canonical wide layout (no `.bari-cmp-scroll` container + inline `auto 1fr auto` grid). Mobile 375px clean. Fix = cap row content measure on desktop (lg:max-w-~62rem); mobile untouched.
  - RT-2 HIGH: latent `bari-cmp-gradecell`/grid-area "grade" scaffold reused (holds only chevron now, no live leak; rename/assert-empty to harden).
  - RT-3 MEDIUM: artichoke-bottoms (44/45) in band 4 (תיבול) — spec-correct but borderline (eaten as a vegetable, ~90mg sodium suppressed); owner confirm.
  Honesty/framing axis CLEAN across red-team (USDA generic-reference framing intact, 9 not_characterized carry zero benefit claims, no OFF, no overclaim vs label, no hidden ranking). **Verdict: PASS WITH FIXES.** **FIXES APPLIED + RE-VERIFIED LOCALLY (2026-06-11, owner approved option A, uncommitted/unpushed):** RT-1 — all 53 `imageUrl` repopulated verbatim from BSIP1 `image_url`; rendered DOM now shows 53 distinct real prefixes (MNH68 = 1 legit product, was 53). B1 — `lg:max-w-[62rem]` desktop cap on bands wrapper; mobile untouched. Fresh `next build` PASSED (✓ 5.7s); re-verified DOM: 53 rows / bands 21/14/8/10 / leak-clean intact. Live image 200-resolution not network-checkable from sandbox (URLs are the authentic scraped Shufersal Cloudinary paths) — owner preview confirms visually. **Residual non-blockers for owner/preview:** RT-2 (gradecell scaffold hardening), RT-3 (artichoke-bottoms band-4 confirm), design nits (off-token hex, run test:a11y). Working tree at f589fed6 + uncommitted fixes; NOT committed/pushed pending owner go. Do NOT close until owner preview review.
- **Phase 5 — Marketing/QA.** "Frozen can beat fresh" hook + SEO pillar; validated post-launch.

## Inputs (multi-agent design, 2026-06-10)
Nutrition (benefit logic + USDA external-data plan), Content (score-free presentation + sample copy),
Marketing (positioning/SEO) proposals synthesized into the Phase 1 spec. The frozen page currently
ships LOCAL-only with real nutrition + ingredients restored (the L1-extraction fix); the score chip
and copy are unchanged pending this program.

## Notes
- Frozen frontend currently shows the OLD score/copy in production; v2 changes are not built or shipped.
- Related: TASK-233 (shared frontend_core / generator-drift program — the v2 build will route through it);
  TASK-236 (absence-as-zero engine bug, logged separately per owner).
- A computed benefit *number* (if ever proposed) = new scoring dimension → D7 co-sign + EV-### required.
