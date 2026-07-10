# TASK-464 HANDOVER → git-owning sibling lane (thumbnail white-box fix)

**From:** description-overhaul session (no-commit ruling). Owner-reported defect (bad/good screenshots,
2026-07-02): product thumbnails that render as an opaque white box against the tile instead of blending.

## Audit result (verified by orchestrator: 580/580 classified, component wiring confirmed at file:line)
- **262/580 product images (45%) fail to blend** on the cream tile: 201 opaque white-box + 61 opaque
  gray/tan. 318 have real alpha and blend. 0 dead links. 12/16 categories are MIXED on the same shelf
  (worst UX — exactly the owner's side-by-side example). Worst: milk 78% (uniform bad), hummus 70%,
  juices 53%, hard_cheeses 52%, cheese 51%. Cleanest: granola 4.5%.
- **Root cause:** all categories render through ONE component — `BariProductThumbnail`
  (`bari-web/src/components/comparisons/bari-product-thumbnail.tsx`), tile fill cream `#F7F7F2`;
  a `blendWhite` prop (white tile) exists but fires ONLY for magnesium
  (`bari-web/src/components/shared/comparison-row.tsx:189`). Yochananof-sourced images (74) are 100%
  opaque; Shufersal/Cloudinary (504) is per-product inconsistent (same CDN path pattern yields RGBA
  cutouts for some products, baked white squares for others).
- Full report: `TASK-464_image_audit.md` (this dir) + per-product verdicts `TASK-464_image_metrics.json`.

## Recommended fix (Frontend-lane recommendation, orchestrator-endorsed): TWO stages
**Stage 1 — ship now (one-line, fixes the visible defect for 201/262 = 77%):** make the white tile the
default for ALL categories — flip `blendWhite` default to true in `bari-product-thumbnail.tsx:13` (and
its fallback at :84), or set `blendWhite` unconditionally at `comparison-row.tsx:189`. White-box images
dissolve; transparent images sit on white identically; every shelf becomes uniform (the owner's ask:
"aligned in all comparison pages"). Check any OTHER call-sites of BariProductThumbnail for consistency
(hashvaot cards etc.). **Requires render-verify (real DOM screenshots across ≥3 categories incl. milk +
granola) + a Design-conformance glance before PR** — this changes tile color site-wide (cream → white
in the thumb column), a deliberate, reversible design choice.
- Residual after stage 1: the 61 OTHER_OPAQUE (gray/tan, mostly Yochananof: milk/juices) still show a
  colored box on the now-white tile. Per-product ids in the metrics JSON (`verdict: OTHER_OPAQUE`).
**Stage 2 — queued program (true blend, owner-gated):** scoped rembg cutout regeneration over the 262
flagged ids (owner has rembg installed). Bigger scope: cutouts must be self-hosted (public/) and the 16
JSONs' imageUrl repointed — a Data+Design pipeline change, propose as its own task before starting.

## Git steps
Stage 1: implement in worktree off origin/master → render-verify + Design check → branch
`fix/task464-thumbnail-blend` → push origin → owner PR (visual change; owner sees preview). Tick board.
