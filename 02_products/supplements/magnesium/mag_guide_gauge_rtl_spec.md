# Magnesium guide — threshold-gauge RTL axis fix (TASK-580)

Design Agent ruling + visual spec. Vision-grounded: rendered evidence (screenshots + measured
`getBoundingClientRect` percentages) reviewed before writing this verdict, per Design Agent operating
model. Component: `threshold-bar-row.tsx` (worktree `C:\bari_wt_578\bari-web`, live commit `9f3f74f1`).
Applies to the LIVE page `bari.digital/madrichim/magnesium` and every guide that reuses `ThresholdBarRow`
(currently magnesium only, per `magnesium-guide-data.ts`; the fix lives in the shared component so it
also protects the creatine guide placeholder and any future guide).

---

## 1. Verdict

**Confirmed. This is a real, single-root-cause conformance bug, not a matter of taste.**

Root cause, read directly in code: `threshold-bar-row.tsx:360`

```
<div className="w-full md:w-[260px] md:shrink-0" dir="ltr">
```

`ThresholdTrack`'s own wrapper forces `dir="ltr"` on the track, while its parent `ThresholdBarRow`
(line 571) is `dir="rtl"`, and the track's own children — the reference-line caption (line 498,
`dir="rtl"`) and the context-band label (line 513, `dir="rtl"`) — are ALSO explicitly forced back to
`dir="rtl"`. The component is internally inconsistent: it deliberately RTLs its own caption text one
`<div>` below the exact track it LTRs. That is the tell that the `dir="ltr"` on line 360 is a stray,
not a considered choice.

Because every positioned element inside the track (`zones`, `boundaries`, ticks, the marker, the
context-band bracket, reference lines) is placed with the **physical** CSS property `left` (never a
logical `inset-inline-start`), `dir="ltr"` doesn't even do the thing it looks like it does — `left`
means physical left regardless of `dir`. So removing `dir="ltr"` alone fixes nothing; the percentage
math itself has to be mirrored (see §2).

**Checked "is it already inconsistent between bar types?" — no, it is not.** I read the live render for
all four bar types (מינון dose, בטיחות safety, צורה וספיגה form, שקיפות תווית label-transparency) across
6 products + the cannot_verify state, desktop and mobile (evidence: `crop_oxide_row.png`,
`crop_bisgly_row.png`, `v31-gauge-live-desktop-{76mg-min,520mg-max}.png`,
`v31-gauge-live-mobile-190mg.png`, `v31-gauge-desktop-overview.png`, `v31-gauge-mobile-overview.png`).
All four bar types render through the same `ThresholdTrack`, so all four are wrong the same way:
- Dose (numeric): "76" (corpus min) sits physically left, "520" (corpus max) physically right.
- Safety (numeric): "0" physically left, "350" physically right.
- Form/absorption (semantic ladder): "נמוכה" (low/worst) physically left, "גבוהה" (high/best) physically
  right.
- Label transparency (semantic ladder): "לא גלוי כלל" (worst) physically left, "גלוי במלואו" (best)
  physically right.

So there is no numeric-vs-semantic split to reconcile — one fix (mirror the track) corrects all four.

**On the counter-argument that numeric scales sometimes stay LTR in RTL UIs:** true in general, but it
doesn't apply here, and this codebase already draws that exact line correctly elsewhere:
- `milk-analysis-scatter.tsx:163` forces `dir="ltr"` on an actual X/Y **scatter chart** — a genuinely
  different reading paradigm (a 2-axis coordinate plot read as a map, not progressively like text).
  That LTR override is legitimate and out of scope here.
- `upf-confidence-ladder.tsx` — the closest same-codebase precedent to this component (a single
  proportional/ordinal bar, "medium" vs "low" confidence) — sets **no** `dir` override at all. It lets
  the bar's fill inherit the page's ambient RTL, so the fill naturally grows from the reading-start
  edge (the right). That is the existing house style for exactly this shape of component.

The dose/safety gauges are not an isolated chart torn out of the page's reading flow — they sit directly
under Hebrew prose, beside Hebrew badges, with their own reference-line and context-band captions
already rendered RTL one element below. Per the owner's own read of the live screenshot ("everything
else on the page IS RTL") and per the `upf-confidence-ladder` precedent, the ruling for this design
system is: **all four bar types get an RTL-ascending axis — domain minimum / worst tier at the track's
right end (the reading-start edge), domain maximum / best tier at the left end.** No LTR exception for
any of the four. Any future numeric gauge in a guide page follows the same rule unless it is a true
multi-axis chart (scatter/line-over-time), which is a different component family and not this one.

---

## 2. Visual spec (RTL terms) — for the Frontend Agent

**General rule for every bar type:** every position that is currently expressed as `X% from the left
edge` must become `X% from the right edge`, i.e. the percentage number is unchanged (the domain math in
`buildGaugeRender`/`buildCategoricalRender` does not need to change), only the anchor edge flips. A
tick/marker/zone/band currently placed via CSS `left: X%` moves to `right: X%` (or equivalently the
component computes `100 - X` and keeps `left`) — pick one convention and apply it uniformly across
zones, boundaries, ticks, the marker (both the plain and clamped case), reference lines, and the
context-band bracket. `marginInlineStart` on the clamped "+" glyph (line 295) must become
`marginInlineEnd` so it keeps trailing away from the marker in the "further past the max" direction,
which is now leftward, not rightward. Track container should carry `dir="rtl"` (or simply drop the
override and let it inherit — either is fine) once the position math is mirrored; changing only `dir`
without mirroring the physical `left`/`right` values fixes nothing (see §1).

Reference frame for all percentages below: 0% = track's right edge (reading-start), 100% = track's left
edge. Desktop track width is the frozen **260px** (`md:w-[260px]`); mobile is fluid (`w-full`) — treat
all figures below as percentages of the track's own rendered width, not fixed px, except where a fixed
px offset is called out explicitly (marker clamp offsets).

### מינון — dose gauge (domainMax = 520, `hideZeroTick: true`)
| Element | Value | Position (from track's RIGHT edge) |
|---|---|---|
| Zone boundary / "76" tick (corpus min, dashed divider) | 76 mg | 14.6154% |
| Reference line — corpus median (dashed, own caption line below) | 190 mg | 36.5385% |
| Context band (RDA all-sources, dashed bracket) | 310–420 mg | starts 59.6154%, ends 80.7692% (width 21.1538%) |
| "520" max tick (`maxTickLabel`, anchor flush) | 520 mg | flush at the track's **left** edge (0% from left) |
| Marker | value V, clamped to 100 at V≥520 | `min(V/520·100, 100)`% from the right |
| Corpus-min product (76mg) marker | — | sits at ~14.6% from the right, over the "76" tick |
| Corpus-max product (520mg) marker | — | sits at the track's **left** edge |

### בטיחות — safety gauge (domainMax = 400, no `maxTickLabel`)
| Element | Value | Position (from track's RIGHT edge) |
|---|---|---|
| "0" tick (anchor "start") | 0 mg | flush at the track's **right** edge (0% from right) |
| "250" tick + dashed EFSA divider | 250 mg | 62.5% |
| "350" tick + solid NIH/IOM UL divider | 350 mg | 87.5% |
| Marker | value V, clamped to 100 at V≥400 | `min(V/400·100, 100)`% from the right |
| Clamped marker (any product ≥400mg, e.g. the 520mg product) | — | anchored **24px in from the LEFT edge** (mirrors today's "24px in from the right" in the broken LTR version), with the "+" glyph trailing 13px further **left** of the marker (`marginInlineEnd`, not `marginInlineStart`) |

### צורה וספיגה — form/absorption ladder (3 equal tiers, no numeric domain)
| Tier | Label | Zone span (from track's RIGHT edge) | Tick center |
|---|---|---|---|
| Worst | נמוכה | 0%–33.333% | 16.667% |
| Middle | בינונית | 33.333%–66.667% | 50% |
| Best | גבוהה | 66.667%–100% | 83.333% |

Marker for a resolved tier: center of its zone, same table. `evidence_limited` fallback marker
(TASK-575 monitor item — solid gray disc, distinct from the hollow dashed cannot_verify ring): **fixed
at 50%, dead-center** — this is direction-invariant (50% mirrors to 50%), so it must render in exactly
the same visual spot it does today; **this is the one place regression is easy to miss because the bug
is invisible on this specific state** — verify it explicitly, don't infer it from the tick fix.

### שקיפות תווית — label-transparency ladder (3 equal tiers)
| Tier | Label | Zone span (from track's RIGHT edge) | Tick center |
|---|---|---|---|
| Worst | לא גלוי כלל | 0%–33.333% | 16.667% |
| Middle | חלקי | 33.333%–66.667% | 50% |
| Best | גלוי במלואו | 66.667%–100% | 83.333% |

### cannot_verify fallback (all four bar types)
Hollow dashed ring, **fixed at 50%, dead-center** — same direction-invariance note as `evidence_limited`
above. No marker/tier position is fabricated (owner's explicit "keep it honest" ask, spec v1 §2/§3) —
this behavior does not change.

### Label anchoring
- Every center-anchored tick label stays centered under its own tick (`transform: translateX` by half
  its own width off the mirrored anchor point — same centering math, opposite edge).
- The two flush-anchored labels ("76"/"0" today at `anchor: "start"`, and "520" today at
  `anchor: "end"`) must swap which physical edge they flush against: the domain-minimum label flushes to
  the track's **right** edge, the domain-maximum label flushes to the track's **left** edge. This is the
  exact inverse of today's TASK-575 fix (that fix stopped a pct:100 center-anchored tick from rendering
  half outside the row's clipping ancestor by flush-anchoring it to `right:0`; the mirrored version must
  flush-anchor the max label to `left:0` instead, preserving the same "must not overflow the clipping
  ancestor" guarantee on the new side).

### What must NOT change
- Track width (260px desktop / fluid mobile), track height (6px), row/marker vertical geometry (24px
  container height, 12px marker core + 3px halo + 1.5px ring).
- All zone/tier/marker colors and tokens (`GUIDE_BAR_TONE` — pass `#0B5D52`/`#E2F2EF`, flag
  `#8A5300`/`#FCEFD6`, fail `#A02318`/`#FBE4E1`, cannot_verify/evidence_limited `#4E5663`/`#F3F4F2`).
- Boundary divider styles (dashed vs solid — this is domain content, e.g. EFSA soft line vs NIH/IOM hard
  UL, not a direction concern).
- The honest-fallback behavior itself (no marker fabricated for cannot_verify / evidence_limited) —
  only which physical spot "mid-track" resolves to, and it resolves to the same spot (50%).
- Everything else already confirmed correct in this review: badge pill order/RTL, card layout, prose,
  reference-line and context-band caption text/RTL (`dir="rtl"` on those was already right — do not
  touch lines 498/513).

---

## 3. Acceptance checklist

Numeric boundingBox assertions, RTL terms — `trackRight` = track box's right edge x-coordinate,
`trackLeft` = track box's left edge x-coordinate, `trackWidth = trackRight - trackLeft` (all in the
existing `vision-in` / Playwright geometry-capture convention, i.e. physical viewport coordinates, not
CSS logical values):

1. **Dose gauge, corpus-min product (76mg):** marker center x ≈ `trackRight - 0.146154 * trackWidth`
   (± the 11px edge-clamp already specced), i.e. marker sits in the right ~15% of the track, NOT the
   left edge.
2. **Dose gauge, corpus-max product (520mg):** marker center x ≈ `trackLeft` (clamped 24px in per the
   clamp rule if the product is flagged clamped — the 520mg corpus-max product is NOT clamped since
   domainMax=520 equals the observed max exactly, so it should sit flush at `trackLeft`, not 24px in;
   only a >520mg value would trigger the 24px clamp inset — confirm which applies before asserting).
3. **Dose gauge tick order, read right→left:** `"76"` tick's left edge > `"520"` tick's left edge (76's
   box must be closer to `trackRight`; 520's box must be closer to `trackLeft`).
4. **Dose gauge context band:** band's right edge x ≈ `trackRight - 0.596154 * trackWidth`; band's left
   edge x ≈ `trackRight - 0.807692 * trackWidth` — i.e. band sits in the LEFT half of the track (58–81%
   of the way from the right), not the right half.
5. **Dose gauge median reference line (190mg):** x ≈ `trackRight - 0.365385 * trackWidth`.
6. **Safety gauge:** `"0"` tick's left edge ≈ `trackRight` (flush right); `"350"` tick's left edge <
   `"250"` tick's left edge < `"0"` tick's left edge (three ticks descend left-to-right as you move away
   from `trackRight`... i.e., reading right→left you meet 0, then 250, then 350).
7. **Safety gauge, 520mg product (clamped):** marker center x ≈ `trackLeft + 24px`; "+" glyph's bounding
   box left edge < marker's bounding box left edge (further left, not further right).
8. **Form ladder:** "נמוכה" tick center x ≈ `trackRight - 0.16667 * trackWidth`; "גבוהה" tick center x ≈
   `trackRight - 0.83333 * trackWidth` (i.e. "נמוכה" is the RIGHTMOST label, "גבוהה" the LEFTMOST).
9. **Transparency ladder:** same pattern — "לא גלוי כלל" rightmost, "גלוי במלואו" leftmost.
10. **evidence_limited / cannot_verify markers (any bar):** marker center x ≈
    `trackLeft + 0.5 * trackWidth` (unchanged from today — regression check, not a new assertion).
11. **No label overflow:** every tick label's bounding box stays within
    `[trackLeft, trackRight]` inclusive (the exact invariant the TASK-575 flush-anchor fix protected —
    confirm it still holds on the new side).
12. Repeat 1–11 at both **375px mobile** and desktop (1280px) viewports — this is a fluid-width
    component; a percentage-based mirror bug could pass at one width and fail at another if any pixel
    offset (11px/13px/24px marker clamps) was mirrored incorrectly.

**Vision check (screenshots read as images, not just geometry):** re-capture the same product set as
`v31-gauge-live-desktop-{76mg-min,520mg-max}.png` + `crop_oxide_row.png` (form ladder) +
`crop_bisgly_row.png` (form ladder, opposite tier) + one `cannotverify` state, both viewports, and
confirm by eye: reading right-to-left, the FIRST thing encountered on every bar is the domain minimum /
worst tier, and the LAST thing encountered (leftmost) is the domain maximum / best tier — i.e. the axis
reads in the same direction as the Hebrew text around it. Do not rely on the boundingBox numbers alone;
a self-consistent-but-mirrored implementation (e.g. accidentally mirroring only the marker and not the
ticks) will fail this check even if some individual assertions above pass.

---

## Additional visual observations while in there (not fixed, severities only)

- **No other conformance defects found** in the reviewed evidence. Badge pill order/RTL, card layout,
  prose direction, reference-line/context-band caption RTL, tick-label spacing (no overlap), and mobile
  wrap behavior all read correctly across every screenshot reviewed (`v31-gauge-desktop-overview.png`,
  `v31-gauge-mobile-overview.png`, `crop_oxide_row.png`, `crop_bisgly_row.png`).
- **LOW / out-of-scope:** the cookie-consent banner visible at the bottom of `v31-gauge-*-overview.png`
  is a third-party-style overlay, not part of `ThresholdBarRow` or any guide component this task
  touches — noted only so it isn't mistaken for a capture artifact of the gauge bug; not a finding.

---

## Return contract

```json
{
  "task": "TASK-580",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\magnesium\\mag_guide_gauge_rtl_spec.md",
      "sha256": "43f689b8b6c5fc81293d6bbe4e2829aae70d81270706de81de9a22fedfd0d827"
    }
  ],
  "counts": {
    "bar_types_reviewed": 4,
    "bar_types_confirmed_broken": 4,
    "products_visually_reviewed": 8,
    "viewports_reviewed": 2,
    "acceptance_assertions_specified": 12
  },
  "commands_run": [],
  "verdict": "CONFIRMED_BUG — dir=\"ltr\" on threshold-bar-row.tsx:360 forces a physical LTR axis on all four bar types on an RTL page; ruling is RTL-ascending axis (min/worst at track right, max/best at track left), no LTR exception for this component family",
  "not_done": [
    "No live Playwright render was executed by this review — verdict and spec are built from the code at C:\\bari_wt_578\\bari-web (commit 9f3f74f1) plus the pre-captured screenshot+geometry evidence already on disk in the scratchpad (v31-gauge-* series, crop_*_row.png, gauge_geometry_before.json). Frontend Agent's fix must be re-verified against a fresh vision-in render, not assumed correct from this spec alone.",
    "Implementation not performed — spec only, per Design Agent charter (D11: approves before Frontend builds)."
  ],
  "acceptance_test": "See '3. Acceptance checklist' — 12 boundingBox assertions + 1 vision check, both viewports. Not yet run against a fix (no fix exists yet)."
}
```
