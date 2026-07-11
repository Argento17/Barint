# Magnesium guide v32 — dose-axis start, RDA band, education findability (TASK-587)

Design Agent visual spec, owner-confirmed 2026-07-10. Component: `threshold-bar-row.tsx`
(worktree `C:\bari_wt_582\bari-web`, live commit `e9157158` — TASK-580 RTL mirror already
live). Page assembly: `guide-page-template-v3.tsx`. Data: `magnesium-guide-data.ts`. Types:
`src/lib/view-models/guide.ts`. Evidence reviewed: `mag_guide_gauge_rtl_spec.md` (TASK-580,
prior ruling, superseded only where this doc explicitly says so), current-state screenshots
`live2-first-card-expanded.png` and the `v31-rtl-fixed-*` series (read as images), plus the
live component/data/type source at the paths above. This spec **supersedes** the TASK-580
dose-gauge percentage table (§2 "מינון" table) for the domain-start change only — the RTL
mirroring math (mirror-the-value convention, `left`/`transform` unchanged) it established
stays the load-bearing mechanism and is reused here unmodified.

**Scope discipline (Hard Rule 3):** all three fixes below are conformance/bug-fix work
against an already-frozen anatomy (a documented dead-zone, a mis-rendered band, an unfindable
disclosure) — no new layout, no new component family, no new interaction pattern. The
education-section fix reuses the exact `ChevronDown` expander already shipped in
`guide-product-row-v3.tsx:159-182`, not a new affordance.

---

## 1. Dose gauge — domain starts at the corpus minimum (76, not 0)

### 1.1 Root cause

`MAGNESIUM_DOSE_GAUGE` (`magnesium-guide-data.ts:118-148`) sets `domainMax: 520` and
`hideZeroTick: true`, but the shared `pct()` helper (`threshold-bar-row.tsx:74-77`) always
computes `value / domainMax * 100` — i.e. the domain is hard-coded to start at **0** even
though the geometry's own header comment says the range is "76–520 mg, the actual observed
min/max." Suppressing the "0" tick only hid the label; the 0–76 stretch of track is still
live space, so "76" renders at `76/520 = 14.6%` from the right (matching the TASK-580 table,
§"מינון" row 1) with a dead, unlabeled 14.6%-wide strip beyond it before any content starts.
That strip is exactly what the owner flagged.

### 1.2 Fix — add a real `domainMin`, not another suppression flag

**Type contract** (`src/lib/view-models/guide.ts`, `GuideGaugeGeometry`, after line 144):
```ts
/** Domain floor. Default 0 (every existing gauge — safety, and every gauge built
 *  before this field existed). Set to a real value (e.g. 76) when "0" is not a
 *  meaningful anchor and the reviewed range itself starts at an observed minimum —
 *  replaces the old hideZeroTick + implicit-0 pairing, which only hid the label
 *  without moving the domain, leaving a dead unlabeled lead-in (TASK-587). */
domainMin?: number;
```
Retire `hideZeroTick` for the dose gauge specifically (the boolean suppressed a symptom;
`domainMin` fixes the cause). Leave the field itself in the type for any other gauge that
still wants a bare `0` suppressed without a `domainMin` shift — but the dose gauge no longer
uses it (see §1.3).

**Formula contract** (`threshold-bar-row.tsx:74-77`):
```ts
function pct(value: number, domainMin: number, domainMax: number): number {
  const clamped = Math.max(domainMin, Math.min(value, domainMax));
  return ((clamped - domainMin) / (domainMax - domainMin)) * 100;
}
```
Every existing call site (`buildGaugeRender`'s zones/boundaries/ticks/markerPct/
referenceLines/contextBand — `threshold-bar-row.tsx:148-206`) passes `geometry.domainMin ??
0` as the new middle argument. This is a **single-root-cause fix**, same discipline as
TASK-580: one helper change propagates correctly to every positioned element, because they
all already route through `pct()`. Safety gauge (`domainMax: 400`, no `domainMin` set) is
byte-for-byte unaffected — `?? 0` preserves its existing 0-based math exactly.

**Geometry data change** (`MAGNESIUM_DOSE_GAUGE`):
- `domainMin: 76` (new), `domainMax: 520` (unchanged).
- Drop `hideZeroTick: true` — no longer needed; the domain now genuinely starts at 76, so
  the generic "min tick" should render, just relabeled.
- The two-zone split at 76 (`{ upTo: 76, ... tickLabel: "76" }`, `{ upTo: 520, ... }`) is now
  **degenerate** — with `domainMin: 76`, a zone from 76 to 76 has zero width. Collapse to
  **one zone**: `{ upTo: 520, tone: "cannot_verify", dividerStyle: "solid" }`. No interior
  boundary divider remains (there was never a real pass/fail reason for one — the comment at
  `magnesium-guide-data.ts:123-125` says the split existed only "to give the corpus minimum
  a real visual boundary," which the domain-min tick below now supplies natively).
- Add `minTickLabel: "76"` — new optional field on `GuideGaugeGeometry`, symmetric with the
  existing `maxTickLabel`. In `buildGaugeRender`, replace the current hard-coded `"0"` label
  in the `hideZeroTick`-gated tick (`threshold-bar-row.tsx:166`) with:
  `label: geometry.minTickLabel ?? String(geometry.domainMin ?? 0), anchor: "start"` and gate
  it on `!geometry.suppressMinTick` (rename `hideZeroTick`→`suppressMinTick` for the one
  remaining caller, if any, else delete the flag entirely — none of today's four bar
  geometries need it once the dose gauge moves to `domainMin`). This is the same "start"
  anchor already used for the safety gauge's "0" tick — same flush-to-track's-right-edge
  rule, unchanged rendering path, only the label source changes.
- `maxTickLabel: "520"` unchanged.
- `referenceTicks: [{ at: 190, ... }]` unchanged (value stays 190 — it's the raw mg value,
  the pct conversion is what shifts).
- `contextBand: { from: 310, to: 420, ... }` unchanged (same reason).

### 1.3 Recomputed geometry table (dose gauge only — supersedes TASK-580 §2 "מינון" table)

Reference frame unchanged from TASK-580: 0% = track's right edge (reading-start, RTL), 100%
= track's left edge. `span = domainMax − domainMin = 520 − 76 = 444`. General formula:
**`pctFromRight(V) = (V − 76) / 444 × 100`**, clamped to `[0, 100]`.

| Element | Value | Position (from track's RIGHT edge) |
|---|---|---|
| "76" tick (`minTickLabel`, anchor `start`, flush) | 76 mg | **0%** — flush at the track's **right** edge |
| Reference line — corpus median (dashed) | 190 mg | **25.6757%** (≈ 25.68%) |
| Context band start (RDA all-sources) | 310 mg | **52.7027%** (≈ 52.70%) |
| Context band end (RDA all-sources) | 420 mg | **77.4775%** (≈ 77.48%) — band width 24.7748% |
| "520" tick (`maxTickLabel`, anchor `end`, flush) | 520 mg | **100%** — flush at the track's **left** edge |
| Marker, general | value V | `min(max((V−76)/444×100, 0), 100)`% from the right |

Worked examples (live corpus, `magnesium-guide-data.ts`):

| Product (barcode) | doseMg | pctFromRight | Reads as |
|---|---|---|---|
| Nutricare Taurate (`7290018439579`) — **corpus min** | 76 | 0% | flush right, **exactly on** the "76" tick — no dead lead-in |
| Solgar Ca+Mg+D3 (`0033984005181`) | 100 | 5.4054% | |
| Full-Mag Hadas (`7290001943700`) | 122 | 10.3604% | |
| Tink Malate (`7290015318532`) | 136 | 13.5135% | |
| Magnesium WELL (`...`, 168mg) | 168 | 20.7207% | |
| NT L.C. Anti Leg Cramps (`7290010207640`) — **corpus median** | 190 | 25.6757% | sits exactly under the median reference line |
| Altman Citrate (200mg) | 200 | 27.9279% | |
| Altman Bisglicinate (250mg) | 250 | 39.1892% | |
| Nutricare Oxide-520 (`7290001065662`) — **corpus max** | 520 | 100% | flush left, **exactly on** the "520" tick, NOT the 24px clamp inset (520 = domainMax exactly, `clamped` is only set when `doseMg > domainMax` — see `magnesium-guide-data.ts:243`) |
| TRIOMAG + 2 others | `null` | n/a | `cannot_verify` fallback — see §1.4 |

**Over-max case:** no live product currently has `doseMg > 520` on the dose gauge (520 is
the corpus max by construction), so this path is **verified by formula/code-path only, not
by a live render** — flag this honestly rather than imply it was screenshot-tested. If one
ever appears: `clamped = true`, marker anchors **24px in from the track's left edge** (the
existing TASK-580 clamp treatment, `threshold-bar-row.tsx:265-289`, completely unaffected by
this domain change — it keys off `placement.clamped`, not `pct()`), "+" glyph trails 13px
further left, exactly as already spec'd.

**Under-min monitor item (not blocking):** `pct()`'s clamp (`Math.max(domainMin, ...)`)
means a hypothetical product below 76mg would silently render at the same flush-right spot
as an exactly-76mg product — there is no "−" glyph mirroring the over-max "+" glyph. Since
76 is the observed corpus minimum by construction, no live product triggers this today. If a
future corpus refresh ever produces a sub-76mg product, that asymmetry needs a design
decision (new glyph vs. accept the silent floor) — out of scope for this task, noted so it
isn't rediscovered as a "new" bug later.

### 1.4 Direction/domain-invariant states — confirm unchanged, don't infer

- **`cannot_verify` fallback** (`ThresholdMarkerFallback`, `threshold-bar-row.tsx:341-384`):
  hardcoded `left: "50%"`, never calls `pct()`. Completely unaffected by `domainMin` — stays
  dead-center. Confirm explicitly against a live render (TRIOMAG, barcode with `doseMg:
  null`), don't infer it from the axis fix, per the same warning TASK-580 §2 issued for this
  exact state.
- **Safety gauge** (`MAGNESIUM_SAFETY_GAUGE`): no `domainMin` set → `?? 0` preserves its
  existing 0-based domain, ticks ("0"/"250"/"350"), and clamp behavior byte-for-byte. Zero
  code change to this geometry object; it is documented here only to confirm it is
  intentionally out of scope, not silently broken by the shared `pct()` signature change.
- **Halo-clip 11px edge guard** (`clamp(11px, calc(100% − ${markerPct}%), calc(100% −
  11px))`, non-clamped marker branch): operates purely on the already-computed `markerPct`
  number, agnostic to how that number was derived. The 76mg product (now `pct=0`) and the
  520mg product (now `pct=100`) both exercise this guard exactly the way any old value=0 or
  value=domainMax product already did — proven code path, unchanged.

---

## 2. RDA context band — on-track shaded zone, not a floating outline

### 2.1 Root cause

`contextBand` (`threshold-bar-row.tsx:483-499`) is positioned `top: "17px"` with `height:
"6px"`, a **3-sided** dashed border (`borderTop` + `borderInlineStart` + `borderInlineEnd`,
no `borderBottom`). The 24px row's track itself is vertically centered at `top: 50%`,
`height: 6px`, `translateY(-50%)` — i.e. the track's own 6px band spans roughly y=9–15 within
the row, while the context band's fixed `top:17px` spans y=17–23, **below** the track, with
no fill and an open bottom edge. It reads as a dashed, hollow, disconnected rectangle
hovering near the track — exactly the "glitch" read the owner flagged. It also renders
**after** the marker/reference-lines in DOM order (`threshold-bar-row.tsx` JSX sequence:
zones → boundaries → marker → referenceLines → contextBand last), so if a product's marker
ever lands inside the RDA range, the band currently paints on top of it.

### 2.2 Fix — on-track fill + closed border, correct paint order

Replace the block with an element that shares the track's own vertical center and is only
marginally taller than it (spec calls for "same y/height as the track or slightly taller" —
ruling: **slightly taller**, 8px vs. the track's 6px, so it visibly "hugs" the pill from
both sides rather than exactly overlapping it 1:1, which would make the fill read as part of
the base track color rather than an overlay):

```ts
{render.contextBand ? (
  <div
    aria-hidden
    className="absolute rounded-full"
    style={{
      top: "50%",
      left: `${100 - render.contextBand.endPct}%`,       // unchanged x-math (TASK-580 mirror)
      width: `${render.contextBand.endPct - render.contextBand.startPct}%`,
      height: "8px",
      transform: "translateY(-50%)",
      background: "rgba(107, 112, 112, 0.16)",            // #6B7070 tint — see §2.3
      border: "1.5px dashed #6B7070",                      // closed 4-sided box now
    }}
  />
) : null}
```

**Paint order fix:** move this block to render **immediately after the zones' color-fill
div and before the `boundaries` map** (i.e., first child painted inside the 6px track
wrapper, right after `render.zones.map(...)`), not last. This keeps it stacked ON the base
zone-tint layer but UNDER every boundary divider, the marker, and the reference lines —
so a marker that lands inside 310–420 still paints visibly on top of the band, matching
how the marker already paints on top of ordinary zone-tone fills everywhere else on the
track. No other element's stacking order changes.

### 2.3 Token choice + WCAG contrast ruling

**Token:** reuse `#6B7070` — already the exact color this component uses for zone-boundary
dividers and the median reference line (`threshold-bar-row.tsx:446`, `:474`) — at two
strengths: **16% alpha for the fill** (a quiet tint, not a competing zone color), **full
opacity for the border** (matching the dividers it sits beside). No new hex value enters the
component; this is an alpha variant of a token already in use in this exact file. Per the
owner's constraint, this deliberately avoids the pass/flag/fail palette
(`GUIDE_BAR_TONE`'s green/gold/red) — `#6B7070` carries zero pass/fail connotation anywhere
else in the codebase.

**Border kept dashed, not solid — one recommendation, not a menu:** dashed is already this
component's own established vocabulary for "advisory/context, not a hard boundary" (the EFSA
soft-caution divider on the safety gauge and the median reference line are both dashed;
solid is reserved for hard boundaries like the NIH/IOM UL divider). Keeping the RDA band
dashed keeps that internal grammar consistent — a solid border would visually claim the same
weight as a real pass/fail boundary, which the geometry's own comment explicitly forbids
("must never be rendered as 'your supplement should give you 310-420 mg'").

**Contrast rulings (WCAG), computed against the dose gauge's own track — the only gauge with
a `contextBand` today:**

| Pair | Ratio | Verdict |
|---|---|---|
| Border `#6B7070` (opaque) vs. track fill `#F3F4F2` | **4.55:1** | Passes the ≥3:1 non-text/graphical-object floor (WCAG 1.4.11) with headroom — same color already proven at this exact contrast for the zone-boundary/reference-line strokes elsewhere in this file. |
| Fill `rgba(107,112,112,0.16)` vs. track fill `#F3F4F2` | **≈1.3:1** | Does **not** reach 3:1 on its own — by design. The fill is a legibility aid for a sighted scan, never the sole signal. The **border carries the actual WCAG boundary signal**, consistent with this component's own stated rule (its header comment: "every zone boundary/tier divider is a real 1px line, independent of color," WCAG 1.4.1). Do not treat the tint alone as satisfying contrast. |
| Caption text `#6B7070` (11px) vs. page background `#FCFCF9` | **≈5.0:1** | Passes AA for normal text (≥4.5:1). Pre-existing, unchanged by this fix — confirmed as a floor-check, not part of what's being fixed. |

---

## 3. Collapsed education section — made findable, stays collapsed

### 3.1 Current state (why it's unfindable)

`guide-page-template-v3.tsx:82-108`: a native `<details>` wrapped in a `rounded-2xl border`
card; the `<summary>` is a single 13px bold line with the disclosure marker explicitly hidden
(`marker:content-none [&::-webkit-details-marker]:hidden`) and **no replacement chevron/icon
of any kind**. Compared to the page's real section headings — `GuideBulletBox`'s non-boxed
heading (`text-[15px] font-extrabold tracking-[-0.02em] text-[#111318]`, used for "איך לקרוא
תווית מגנזיום" immediately above it) and `GuideEducationSpine`'s own per-subsection `h2`
(identical classes) — this trigger is smaller (13px vs 15px), sits inside a bordered card
(a "callout" idiom this codebase already reserves for the boxed "מה גילינו" treatment, not
for a plain section), and gives zero visual signal that clicking reveals anything. That
combination is why it reads as a misc utility widget, not a page section.

### 3.2 Fix — heading + teaser stay always-visible; only the deep body toggles

Keep the native `<details>`/`<summary>` (the code's own comment documents a real reason: zero
JS, works pre-hydration — a legitimate engineering property, not a Design concern to
relitigate). The fix is entirely inside what `<summary>` renders, since `<summary>` accepts
arbitrary markup and — critically — **`<summary>`'s own content is always visible**, open or
closed; only the sibling content after it is hidden. That means heading + teaser + affordance
can all live inside `<summary>` and still satisfy "stays collapsed, but becomes a real,
findable section."

**Drop the `rounded-2xl border` card wrapper.** Render as a plain section, matching the
non-boxed idiom already used one section above it (`GuideBulletBox boxed={false}` / bare
`GuideEducationSpine` sections) — no border, no rounded corners, just the standard
`comparisonWebSectionPaddingClass()` padding. The bordered-card treatment is itself part of
why this reads as "a different kind of thing" than the rest of the page; removing it is as
load-bearing as anything added.

**New `<summary>` content, three stacked pieces:**

1. **Heading** — `<h2 className="text-[15px] font-extrabold tracking-[-0.02em]
   text-[#111318]">` — byte-identical classes to `GuideBulletBox`'s non-boxed heading and
   `GuideEducationSpine`'s own `h2`. Text: the existing signed string
   (`guide.collapsedEvidenceSectionTitleHe` — Content Agent's territory, not re-authored
   here; if Content wants a different title now that this is a visible heading rather than a
   small accordion label, that's a content-sign-off decision, not a Design one).
2. **Teaser** — one line, `className="mt-1 text-[13px] leading-[1.6] text-[#3E444A]"` —
   same type scale/color as `GuideEducationSpine`'s own body paragraphs and
   `GuideBulletBox`'s bullet text, so it reads as page body copy, not disclosure chrome. New
   VM field: `guide.educationTeaserHe: string | null` (Frontend adds; Content authors the
   string — **not specified here**, only the slot). Constraint for Content: must hold to one
   visual line at 375px width minus the section's horizontal padding — budget ≈ 40–46
   Hebrew characters at 13px to guarantee no wrap; if the sign-off string runs longer, that's
   a content-length bounce back to Content, not a Design override.
3. **Expand affordance row** — `mt-2`, `flex items-center justify-between` (RTL: label
   visually right/reading-start, chevron visually left/trailing — matching the product-row
   expander's own layout), reusing **byte-identical** tokens from the proven
   `guide-product-row-v3.tsx:159-182` expander:
   - Label: reuse the existing two-state `expanderLabels.collapsed` /
     `expanderLabels.expanded` convention (add a matching `guide.educationExpanderLabelsV3:
     { collapsed: string; expanded: string }` field, same shape as the product row's) —
     `text-[12px] font-semibold`, color `#4E5663`.
   - Icon: `<ChevronDown strokeWidth={1.75} className="size-[15px] transition-transform
     duration-200 motion-reduce:transition-none" />`, `rotate-180` when open, color
     `#B5BBB6` collapsed / `#9A9FA6` open — the exact same four values as the product-row
     expander. No new icon, no new color introduced.

**Expanded state:** on native `<details>` toggle, chevron rotates 180°, label swaps to the
`.expanded` string, and the existing `border-t border-black/[0.05]` divider + full
`<GuideEducationSpine sections={guide.educationSpine} wide={false} />` render below —
this part of the current implementation already works correctly and is unchanged.

### 3.3 Placement ruling

**Stays exactly where it is** — after the "איך לקרוא תווית מגנזיום" bullets, immediately
before `MethodologyFooter`, at the page's bottom. Ruling, not a default-by-omission: this
section is a "go deeper" doorway, and its natural reading position is *after* the primary
path (H1 → what-we-found → products → how-to-read basics) — moving it earlier (e.g. directly
under the product table) would insert a branch point into the primary reading flow, which is
the same shape of problem the Drift Detection rubric flags for a comparison page ("the user
must make a choice before seeing a product"). The fix here is **findability**, not
**relocation**: the owner's own words were "can't find it," not "it's in the wrong place."
Moving it would also be a bigger structural change than what was asked, which cuts against
Hard Rule 3 (conformance, not creativity) for a task that started as a bug report.

---

## 4. Acceptance checklist

All assertions in RTL terms per the TASK-580 convention: `trackRight`/`trackLeft` = the dose
track's own bounding-box edges (physical viewport coordinates from `vision-in` /
`getBoundingClientRect`), `trackWidth = trackRight − trackLeft`. Run at **375px mobile**
first, then **1280px desktop** — repeat every numbered item at both viewports (item 15).

### Dose axis (§1)
1. **76mg product (Nutricare Taurate, `7290018439579`) — corpus min:** marker center x ≈
   `trackRight` (± the 11px halo-clip guard), i.e. flush at the track's right edge, with
   **zero** gap to the "76" tick label's own anchor point.
2. **"76" tick position:** tick label's right-anchor point ≈ `trackRight` (flush), NOT at
   `trackRight − 0.146 × trackWidth` (the old, now-superseded position) — this is the
   headline regression check for the whole fix.
3. **190mg product (NT L.C. Anti Leg Cramps, `7290010207640`) — corpus median:** marker
   center x ≈ `trackRight − 0.25676 × trackWidth`, and lands within 2px of the median
   reference line's own x-position (both derive from the same `pct(190, 76, 520)` value —
   they must coincide).
4. **520mg product (Nutricare Oxide-520, `7290001065662`) — corpus max:** marker center x ≈
   `trackLeft` (flush, NOT the 24px clamp inset — confirm `clamped === false` for this
   product per `magnesium-guide-data.ts:243`, since 520 equals `domainMax` exactly).
5. **"520" tick position:** unchanged from TASK-580 — flush at `trackLeft`. Regression check
   only (this task doesn't touch the max end).
6. **RDA band position:** band's right edge x ≈ `trackRight − 0.52703 × trackWidth`; left
   edge x ≈ `trackRight − 0.77477 × trackWidth` (band width ≈ 0.24775 × trackWidth).
7. **No dead lead-in:** confirm by eye (vision check, not just geometry) that reading
   right-to-left, the FIRST thing encountered at the track's right edge is the "76" tick
   with the corpus-min marker sitting directly on it — no blank track segment before either.
8. **Safety gauge unchanged:** re-run TASK-580 acceptance items 6–7 (0/250/350 tick
   positions, 450mg-oxide clamped-marker position) and confirm byte-identical results to the
   already-shipped TASK-580 render — this task must not move anything on the safety gauge.
9. **`cannot_verify` marker (any of the 3 null-dose products, e.g. TRIOMAG):** marker center
   x ≈ `trackLeft + 0.5 × trackWidth` — unchanged, confirmed explicitly (not inferred).

### RDA band rendering (§2)
10. **Band is on-track, not floating:** band element's vertical center y ≈ track's own
    vertical center y (± 1px, since band height 8px vs. track height 6px is intentional).
    Band's `top` must NOT be a fixed offset independent of the track's own centering — this
    is the literal regression check for the "hovering" bug.
11. **Band has all 4 border sides:** confirm via computed style / vision check that the
    band's border is closed (top + bottom + both insets), not the old 3-sided open box.
12. **Band paint order:** with a synthetic/dev-only product whose dose value falls inside
    310–420 (or by temporarily setting a test placement), confirm the marker renders VISIBLY
    ON TOP of the band fill, not obscured by it.
13. **Fill contrast is NOT relied upon alone:** confirm the border (`#6B7070` opaque) is
    present and is the element actually carrying the ≥3:1 non-text contrast — a QA pass that
    only checks "is there a colored region" without checking the border would miss a
    regression where the fill ships but the border silently drops.

### Education section (§3)
14. **Collapsed state, always-visible parts:** with the `<details>` closed, the heading
    (15px, `#111318`, extrabold), the teaser (13px, `#3E444A`, one line, no wrap at 375px),
    and the expander row (label + `ChevronDown` at `rotate-0`, color `#B5BBB6`) are all
    present in the DOM and visible without any interaction. The `rounded-2xl border` card
    wrapper is gone (no `border` computed style around the outer container).
15. **Expanded state:** after toggling, `ChevronDown` computed `rotate-180`, color changes to
    `#9A9FA6`, label text swaps to the `.expanded` string, and the full
    `GuideEducationSpine` content (all sections, including sources) is present with the
    `border-t border-black/[0.05]` divider above it — regression check against the existing,
    already-working expanded-state render.
16. **Heading visually matches its sibling section:** side-by-side crop of this heading and
    the "איך לקרוא תווית מגנזיום" heading directly above it — same font size, weight,
    tracking, color (vision check, not just class-name diffing, since a class typo could
    still compute to a visually-close-but-wrong size).

### Cross-cutting
17. Repeat items 1–16 at both **375px mobile** and **1280px desktop**. Item 6 (band) and
    item 3 (median) are percentage-based and should hold at both widths if the mirror is
    correct; a pixel-offset error (the 11px/24px/13px constants, all unaffected by this task
    but worth re-confirming) would only show up at one width, same caution TASK-580 raised.

**Vision check (mandatory, screenshots read as images):** re-capture the dose gauge for the
76mg/190mg/520mg/cannot_verify products plus one card with the RDA band visible, both
viewports. Confirm by eye: (a) the "76" tick sits flush against the track's right edge with
no gap, (b) the RDA band reads as a shaded strip running through the track, not a rectangle
floating near it, (c) the education section at the page bottom looks like a real section
(matching heading weight/size to its neighbor) with a visible reason to click it, before
trusting any single boundingBox number in isolation — this is the exact discipline
`visual_bugs_image_read_not_geometry` exists to enforce (TASK-580 passed 208 boundingBox
asserts on a page that was still visibly wrong).

---

## 5. Frozen invariants — everything else on the page must NOT change

- Track width (260px desktop / fluid mobile), track height (6px — the RDA band is
  *additively* 8px, it does not resize the track itself), row/marker vertical geometry (24px
  container, 12px marker core + 3px halo + 1.5px ring).
- Safety gauge geometry, ticks, zones, and clamp behavior — completely untouched (§1.4).
- Form/absorption ladder and label-transparency ladder — untouched; this task is dose-gauge
  and contextBand-generic only, no ladder geometry changes.
- All zone/tier/marker color tokens (`GUIDE_BAR_TONE`) — untouched. The RDA band's new fill/
  border reuse `#6B7070`, already in the file; no new hue enters the palette.
- Boundary divider styles elsewhere (EFSA dashed / NIH-IOM solid on the safety gauge) —
  domain content, not touched.
- The honest cannot_verify/evidence_limited fallback behavior itself — no marker fabricated,
  still dead-center, still direction/domain-invariant (§1.4).
- `GuideEducationSpine`'s own internal rendering (heading/body/sources per subsection) —
  untouched; only its OUTER wrapper (the `<details>`/summary/card) changes.
- Page section order (H1 → what-we-found → products → how-to-read → education disclosure →
  methodology) — unchanged (§3.3 ruling: findability fix, not relocation).
- `MethodologyFooter` and everything below the education disclosure — untouched.
- RTL mirroring convention established by TASK-580 (mirror the value, keep `left` +
  `transform` unchanged) — reused, not re-litigated, for every position math in this spec.

---

## Return contract

```json
{
  "task": "TASK-587",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\magnesium\\mag_guide_v32_visual_spec.md",
      "sha256": "4cbc796c55c9e0bbb6110a3cb35a49114b7b67c7ed581a9a65d395d2592cce75"
    }
  ],
  "counts": {
    "fixes_specified": 3,
    "acceptance_assertions_specified": 17,
    "dose_gauge_worked_examples": 10,
    "viewports_covered": 2,
    "new_type_fields_specified": 3,
    "tokens_reused_not_invented": 1
  },
  "commands_run": [],
  "verdict": "SPEC_COMPLETE — (1) dose gauge gets a real domainMin=76 (not another suppression flag), single-root-cause via pct() helper, recomputed table (median 25.68%, RDA band 52.70%-77.48%, marker=(V-76)/444); safety gauge and cannot_verify/evidence_limited fallback confirmed domain-invariant/unaffected. (2) RDA band becomes an on-track 8px tinted+bordered zone (#6B7070 at 16% fill / 100% border), paint-order-fixed to sit under the marker, contrast ruled (border 4.55:1 passes graphical-object floor, fill ~1.3:1 does NOT and is not relied upon alone, caption text ~5.0:1 pre-existing pass). (3) Collapsed education section gets an always-visible 15px heading + 1-line teaser + reused ChevronDown affordance inside <summary>, card wrapper dropped, position unchanged (findability fix, not relocation) per Hard Rule 3.",
  "not_done": [
    "No live Playwright/vision-in render was executed against an actual code change — this is a spec only (component source at C:\\bari_wt_582\\bari-web was read for the CURRENT/broken state; the fixed state is derived analytically from the existing pct()/RTL-mirror mechanism, same methodology TASK-580 used). Frontend Agent's implementation must be verified against a fresh vision-in render (375px + desktop) before this spec's acceptance checklist can be marked passed.",
    "Content Agent has not yet authored: the education-section teaser string (guide.educationTeaserHe) or the education expander's collapsed/expanded label pair (guide.educationExpanderLabelsV3) — both are new VM slots this spec defines geometry/typography for but explicitly does not author copy for (two-gate discipline).",
    "Implementation not performed — spec only, per Design Agent charter (D11: approves before Frontend builds)."
  ],
  "acceptance_test": "See 'Section 4: Acceptance checklist' — 17 numbered assertions + 1 mandatory vision check, both viewports (375px then 1280px), covering min/median/max/cannot_verify dose cases (no live over-max dose product exists in the current corpus; that path is specified formula-only and flagged as such), RDA band on-track/paint-order/contrast, and both collapsed/expanded education-section states. Not yet run against an implementation (no implementation exists yet)."
}
```
