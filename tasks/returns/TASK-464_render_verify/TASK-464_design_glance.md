# TASK-464 Design-Conformance Glance — Stage-1 White Tile

**Reviewer:** Design Agent (Bari v2)  
**Date:** 2026-07-03  
**Branch under review:** `fix/task464-thumbnail-blend` (commit `9d8bf49c`)  
**Viewports reviewed:** 375/390px mobile first, 1280px desktop  
**Screenshots reviewed:** 12 (all files in `tasks/returns/TASK-464_render_verify/`)  
**Verdict: GO**

---

## What was reviewed

One-line change: `blendWhite` default flipped `false → true` in
`bari-web/src/components/comparisons/bari-product-thumbnail.tsx:13`; the explicit
`blendWhite={category === "magnesium"}` override removed from
`bari-web/src/components/shared/comparison-row.tsx:189`. Effect: all product thumbnail
tiles swap from cream `#F7F7F2` to pure white `#FFFFFF` site-wide.

---

## Design-system surface model (establishes the contrast chain)

From `bari-web/colors_and_type.css` and `bari-web/src/lib/design/bari-comparison-tokens.ts`:

| Surface | Hex | Role |
|---|---|---|
| `--canvas` | `#F7F7F2` | Page body / canvas (was also the old tile fill) |
| `--surface` | `#FFFFFF` | Row surface / card surface (now also the tile fill) |
| `--surface-2` | `#F9F9F9` | Even zebra rows |
| Even row per CSS | `#fbfbf9` | `bari-cmp-row:nth-child(even)` from `globals.css:450` |

Row background is `transparent` (`.bari-cmp-rowhead { background: transparent }`) over a parent whose background alternates between the canvas cream `#F7F7F2` (odd rows, body default) and `#fbfbf9` (even rows). The white tile (`#FFFFFF`) is therefore nested INSIDE a row surface that is slightly tinted relative to pure white.

The tile border is `border-black/[0.06]` = `rgba(17,19,24,0.06)` retained in both `blendWhite` branches — meaning card edge definition does not change between `true` and `false`. Shadow `shadow-sm` = `0 1px 2px rgba(17,19,24,0.05)` also retained identically. This was confirmed at `bari-product-thumbnail.tsx:47-48`.

---

## Findings

### PASS — F1: Card edge definition (border + shadow)

**Observed in:** `milk_desktop_rows.png`, `milk_mobile390_rows.png`, `hummus_desktop_rows.png`

The rounded thumbnail tile (border `rgba(17,19,24,0.06)`, shadow `shadow-sm`) is visually retained on all screenshots at both mobile and desktop. The border is sufficient to separate the white tile from the white/near-white row surface. On milk desktop rows the Tnuva carton thumbnail shows a clear tile boundary at the corners — no bleed-into-row, no geometry change. The `rounded-2xl` corner radius is intact.

**Contrast of tile border against odd row (#F7F7F2 canvas):** tile `#FFFFFF` against `#F7F7F2` canvas has a luminance ratio of approximately 1.05:1, meaning the tile is not separated from the canvas by luminance alone. The border (`rgba(17,19,24,0.06)`) carries the separation. Visually in the screenshot this works: the shadow + border create a readable card edge. This matches the pharmacy/e-commerce framing of the component's own JSDoc.

**Contrast of tile border against even row (#fbfbf9):** the even-row tint is very close to white, making the separation between tile and even-row effectively reliant on the same border. The border is sufficient — confirmed in `milk_desktop_multirow.png` where alternating rows show consistent tile edges.

Frozen geometry unchanged: `bari-cmp-thumbcell` fixed at `56px × 56px` per `globals.css:489-491`; tile uses `size="fill"` (h-full w-full), so the tile matches the cell. No geometry drift.

**Status: PASS**

---

### PASS — F2: WCAG contrast — no new contrast failure introduced

**Observed in:** all 12 screenshots; token chain from `colors_and_type.css`

The change moves only the tile's background fill from `#F7F7F2` to `#FFFFFF`. No text sits on the tile surface — the product image is `object-contain p-2` inside the tile, and all text (product name, brand, insight line, grade chip) lives in the `bari-cmp-namecell` and `bari-cmp-gradecell` columns, not over the image. There is no text-on-tile contrast exposure.

The fallback tile (no-photo case) renders a `✦` mark at `rgba(17,19,24,0.18)` on the new white fill. Old contrast: `rgba(17,19,24,0.18)` on `#F7F7F2` ≈ 1.2:1. New: `rgba(17,19,24,0.18)` on `#FFFFFF` ≈ 1.2:1 — identical near-unity; this mark is `aria-hidden` (decorative, non-text) so WCAG 1.4.11 non-text contrast does not apply to it. The tile `aria-label` provides the accessible name for the no-photo case regardless of fill color.

No pre-existing contrast pass changes to a fail by this color delta.

**Status: PASS — no WCAG regression introduced**

---

### PASS — F3: RTL layout intact

**Observed in:** `milk_desktop_shelf.png`, `milk_mobile390_rows.png`, `hummus_desktop_rows.png`, `hummus_mobile390_rows.png`, `granola_desktop_rows.png`

All screenshots are RTL Hebrew layout. The thumbnail column sits on the right edge of the row (rightmost column in RTL grid: `grid-template-areas: "thumb name grade"`). In all screenshots the thumbnail tile occupies the correct right-side slot with no position drift. Text flows right-to-left correctly. No layout breaks at either viewport.

**Status: PASS**

---

### PASS — F4: Drift and leakage

No new sections, no charts, no summary statistics, no modal/sheet, no filter state changes. The change is strictly the tile fill color. Hero, Prologue, ProductTable, Methodology structure is untouched and visible in `milk_desktop_shelf.png`.

**Status: PASS — no drift introduced**

---

### PASS — F5: Grade chip unchanged

**Observed in:** `milk_desktop_shelf.png` (grade A chip, score 85), `hummus_desktop_rows.png` (multiple grade C chips, score 58/68), `granola_desktop_rows.png` (grade B chips)

Grade chips render with the correct `gradePalette` color per grade (A: green `#E7F4EC` bg; B: olive `#F0F3DF`; C: gold `#FBF3D8`). Score chips are unchanged by the tile color change. No second color axis added. Conformance confirmed.

**Status: PASS**

---

### PASS — F6: Magnesium regression

**Observed in:** `magnesium_mobile390_regression.png`

Magnesium was the sole prior explicit `blendWhite=true` category. The screenshot shows supplement bottles on white tiles — visually identical to the expected prior behavior. The explicit prop removal produced no regression.

**Status: PASS**

---

### PASS — F7: /hashvaot hub unaffected

**Observed in:** `hashvaot_hub_desktop.png`

The hub page uses category feature cards, not `BariProductThumbnail`. No `.bari-cmp-thumbcell` elements present. The hub is visually unchanged and unaffected by this change.

**Status: PASS**

---

### MEDIUM — F8: Even-row white-on-white tile edge thinness (non-blocking, Stage-2 awareness)

**Observed in:** `milk_desktop_multirow.png`

On even rows, the row background is `#fbfbf9` — 3/255 luminance steps from `#FFFFFF`. The white tile on an even row has effectively no luminance separation and relies entirely on the `border-black/[0.06]` hairline (≈ 5-6% opacity black) for card-edge definition. In the screenshot this hairline is visible and sufficient on a desktop render at 1280px. At lower-DPI or in some print environments the hairline could disappear.

**Assessment:** This pre-existed the change in spirit (the cream tile `#F7F7F2` at contrast 1.05:1 against `#fbfbf9` was also near-unity). The new white tile is marginally thinner in contrast against `#fbfbf9` than the old cream. However, the stage-1 report correctly notes the visual uniformity benefit outweighs this residual edge thinness. The border is retained, the shadow is retained, and the even-row strip is itself very light — the net effect is acceptable.

**Recommendation for Stage-2 consideration:** if the Stage-2 rembg pipeline is built, assess whether a slightly stronger hairline token (e.g. `border-black/[0.09]` instead of `0.06`) would improve even-row tile definition without introducing heaviness. This is a token-level tweak, not a structural change. Not a blocker for stage-1 GO.

**Status: MEDIUM — acceptable to ship; note for Stage-2**

---

### MEDIUM — F9: 61 OTHER_OPAQUE residuals — tan/gray boxes on white tile

**Observed in:** `hummus_desktop_rows.png` (rows 3, 5, 6, 7 showing Galil hummus products with tan/kraft-paper backgrounds)

The OTHER_OPAQUE class (tan, gray, or colored studio backdrops — 61 total, 10.5% of corpus) now renders as a colored box on a white tile instead of a colored box on a cream tile. Visual effect: the colored box is more contrasted against white than it was against cream.

**From screenshots:** In `hummus_desktop_rows.png`, four Galil hummus products have tan-colored tubs on what appears to be an off-white or tan studio background. These render as a soft tan box inside the white tile. The contrast between the colored box and the white tile is slightly more pronounced than the pre-fix cream tile, but the visual does not regress significantly — the appearance is equivalent to a product photo with a natural colored backdrop, which is industry-standard in Israeli food retail contexts.

**Assessment of "does this visibly worsen any shelf vs today's mixed state?":** No. The pre-fix state had BOTH jarring white-box-inside-cream-tile AND colored-box-inside-cream-tile on the same shelf, creating maximum inconsistency. The post-fix state has colored-box-inside-white-tile, which is at worst the same inconsistency level but likely better because at least the WHITE_BOX class (201 products) now looks uniform. The mixed state is improved, not worsened. Shipping stage-1 with 61 residual OTHER_OPAQUE is acceptable.

**Status: MEDIUM — acceptable to ship; Stage-2 rembg scope already identified**

---

### NOT APPLICABLE — Component state completeness

The thumbnail component has only two states: image-present (photo tile) and image-absent (fallback tile with `aria-label`). There is no hover state on the thumbnail itself (hover is on the row, not the tile). Both states are accounted for. No additional interaction states are exposed.

---

## GO verdict rationale

All CRITICAL and HIGH checks pass:
1. Card edge definition (border + shadow) retained in both `blendWhite` branches — confirmed code at `bari-product-thumbnail.tsx:47-48` and visually in all 12 screenshots.
2. No WCAG contrast failure introduced — no text sits on the tile surface; the decorative mark is `aria-hidden`.
3. RTL layout intact — all Hebrew RTL screenshots show correct right-side thumbnail placement.
4. No drift or leakage — 4-section structure unchanged, no new UI elements.
5. Grade chips unchanged — `gradePalette` tokens unaffected.
6. Magnesium regression: none.
7. Hub unaffected: confirmed by screenshot.

Two MEDIUM findings are acknowledged and non-blocking:
- F8 (even-row hairline): pre-existing near-unity surface delta; border retained.
- F9 (61 OTHER_OPAQUE residuals): pre-fix state was worse (two conflicting defect classes on the same shelf); stage-1 is a net improvement.

**Design conformance verdict: GO — ship stage-1 PR for owner preview.**

Stage-2 (rembg cutout regen for 61 OTHER_OPAQUE, owner-gated) remains queued as a separate task per the handover spec.

---

```json
{
  "task": "TASK-464",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "tasks/returns/TASK-464_render_verify/TASK-464_design_glance.md",
      "action": "created",
      "sha256": "this-file"
    }
  ],
  "counts": {
    "screenshots_reviewed": "12/12 (all files in tasks/returns/TASK-464_render_verify/*.png, listed by Glob)",
    "viewports_covered": "2/2 (mobile 375-390px + desktop 1280px)",
    "categories_sampled": "4/4 screenshotted categories (milk, granola, hummus, magnesium) + hashvaot hub",
    "findings_critical": "0",
    "findings_high": "0",
    "findings_medium": "2 (F8 even-row hairline thinness; F9 61 OTHER_OPAQUE residuals)",
    "findings_pass": "7 (F1-F7)",
    "code_files_read": "4 (bari-product-thumbnail.tsx, comparison-row.tsx, bari-comparison-tokens.ts, colors_and_type.css + globals.css)"
  },
  "commands_run": [
    {"cmd": "Read bari-product-thumbnail.tsx", "exit_code": 0},
    {"cmd": "Read comparison-row.tsx (offset 175)", "exit_code": 0},
    {"cmd": "Read bari-comparison-tokens.ts", "exit_code": 0},
    {"cmd": "Read colors_and_type.css", "exit_code": 0},
    {"cmd": "Read globals.css (offset 440)", "exit_code": 0},
    {"cmd": "Glob *.png in TASK-464_render_verify", "exit_code": 0},
    {"cmd": "Read all 12 PNG screenshots", "exit_code": 0}
  ],
  "not_done": [
    "Live Playwright render: screenshots provided by the implementation agent cover the required categories; a separate live render was not needed and was not run. This is the v2 gap — the vision-in loop instrument is PROPOSED (not yet built). The 12 committed screenshots served as the render evidence for this review.",
    "Visual diff against committed baselines (npm run test:visual): not run — the branch has no committed baseline for comparison; this is a new default state. Baselines should be updated as part of the PR merge.",
    "axe WCAG scan (npm run test:a11y): not run in this review. No new text-on-surface exposure was introduced by the fill change, making a contrast failure structurally impossible, but the full axe scan remains the live gate and should be run in CI before merge."
  ],
  "self_check": "Spec acceptance test: 'Does the white tile hold up against the frozen system — card edge defined, no WCAG issue, RTL intact, no drift?' — PASS on all four axes (F1–F4 above), confirmed against 12 screenshots and component code at bari-product-thumbnail.tsx:47-48 and globals.css:446-491."
}
```
