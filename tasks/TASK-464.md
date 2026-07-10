---
id: TASK-464
title: Product-image white-background audit: find all comparison-page thumbnails that fail to blend with the card background
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-reported (2026-07-02, with bad/good visual examples): some product images render as an opaque white box against the card background instead of blending. Audit ALL live comparison pages: classify every product imageUrl (transparent cutout vs opaque white bg vs other), check the rendering container's actual background color, produce a per-category defect list + recommended fix path (CSS blend vs rembg cutout regeneration). Read-only audit; zero git writes (sibling chat owns git).
---

# TASK-464 — Product-image white-background audit: find all comparison-page thumbnails that fail to blend with the card background

## Dispatch log (orchestrator; board tick deferred to sibling-chat handover per owner no-commit ruling)
- 2026-07-02 **P464-AUDIT** → C1 native (Sonnet): (1) read rendering components off origin/master to
  define container backgrounds per image slot; (2) download+classify all ~580 product images
  (transparent-blends / white-box / other-opaque / dead) via Pillow border sampling; (3) per-category
  defect table + ranked fix path (CSS containment chip vs rembg cutouts vs re-scrape). Read-only,
  zero git writes, outputs in session scratchpad\t464.
- 2026-07-02 **P464-AUDIT ✅ RETURNED + ORCHESTRATOR-VERIFIED.** Component wiring confirmed at
  origin/master (BariProductThumbnail cream #F7F7F2 default; `blendWhite` fires only for magnesium at
  comparison-row.tsx:189); metrics re-counted (580 records: BLENDS 318 / WHITE_BOX 201 / OTHER_OPAQUE 61 /
  DEAD 0). **262/580 (45%) fail to blend; 12/16 categories mixed on-shelf (the owner's screenshot case).**
  Root cause: Yochananof images 100% opaque (74); Shufersal/Cloudinary per-product inconsistent (504).
- 2026-07-02 **HANDOVER WRITTEN → `tasks/returns/TASK-464_handover.md`:** Stage-1 one-line fix (white
  tile default project-wide, fixes 77% of defects; render-verify + Design glance required — site-wide
  visual change, owner sees PR preview); Stage-2 = scoped rembg cutout regen over the 262 ids (self-host
  + repoint imageUrls) — propose as own task, owner-gated. Audit report + per-product verdict JSON
  copied to tasks/returns/. Status stays IN_PROGRESS pending sibling implementation + owner PR.
- 2026-07-03 **STAGE-1 IMPLEMENTED + BOTH GATES GREEN (unattended pass) — branch
  `fix/task464-thumbnail-blend` (worktree C:\bari_wt_t461x_a, commit `9d8bf49c`, off origin/master
  06f85de4).** Frontend native lane: `blendWhite` default false→true (bari-product-thumbnail.tsx:13)
  + magnesium-only override removed (comparison-row.tsx:189, sole call-site — grep + live-DOM
  audited); tsc 0 / build 0. Orchestrator verified the diff directly (2 files, minimal) and eyeballed
  screenshots. Render-verify: 9 PNGs in `tasks/returns/TASK-464_render_verify/` — milk (worst, 78%)
  uniform, granola control unregressed, hummus uniform, magnesium regression PASS, hub unaffected.
  **Design-conformance glance (Design Agent): GO — 0 CRITICAL / 0 HIGH / 2 MEDIUM non-blocking**
  (F8 even-row hairline pre-existing; F9 61 OTHER_OPAQUE residual = Stage-2 rembg scope);
  report `TASK-464_design_glance.md`. **NO push/PR unattended → morning kick: push branch + owner PR
  (owner sees preview; visual change is deliberate + reversible).** Stage-2 (rembg 262 ids) still to
  be proposed as its own owner-gated task. Status stays IN_PROGRESS.
