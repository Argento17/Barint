# Dropdown Appeal Polish v1
**Date:** 2026-06-19  
**Author:** Design Agent  
**Paired spec:** `product-dropdown-spec.md` (accepted direction, not modified here)  
**Source of truth prototype:** `Bari Product Dropdown.html`  
**Handoff target:** Frontend Agent — implement in `expansion-section.tsx` / `AdditivePanel.tsx`

This document lists prioritized, specific refinements that make the expansion
feel more premium and considered without touching any frozen invariant. Every
item references the spec section it acts on, the exact token it uses, and
carries a mobile + RTL note. Priority 1 = highest impact.

---

## Priority 1 — Structural rhythm (high ROI, zero risk)

### R-01 · Section separator spacing: 18px → 24px above each `.sec`

**What.** The prototype uses `padding-top: 18px` on every `.sec`. Increasing to
`24px` (three 8px grid steps) gives the five sections a clear breath between
them. The sections read as one run of content at 18px; at 24px they read as
five distinct chapters inside one container.

**Why.** At 375px, expansion content is tall and the sections merge visually
into a wall. Consistent 24px gaps create scanning landmarks without adding any
visual chrome.

**Spec.** §3 (section scaffold). No new token — 24px is a standard 8px-grid step.

**Mobile note.** At `< 640px`, tighten to `20px` top on each `.sec` (the
tighter inline padding already applies; reduce block spacing proportionally).

**RTL note.** Block spacing is direction-neutral; no change.

---

### R-02 · Assessment panel top padding: 15px → 18px; item row padding: 7px → 9px

**What.** Both `.panel` elements have `padding: 15px 16px`. Increase to
`18px 16px`. Also increase `.wlItem` block padding from `7px 0` to `9px 0`.

**Why.** At 15px top padding the panel title sits very close to the card
edge. At 18px it breathes. The `.wlItem` row height at 7px is borderline
cramped for Hebrew text which has taller ascenders; 9px makes each bullet
feel like a considered statement, not a list entry. The prototype currently
reads as a checklist widget. This is the single largest "feels premium"
improvement.

**Spec.** §3.1. Tokens: `--radius-xl`, `--hairline-soft` (unchanged).

**Mobile note.** Applies at all breakpoints (inline tightens; block can stay 18px).

**RTL note.** Padding is symmetric; direction-neutral.

---

### R-03 · Magnitude bars: raise track from 4px to 5px; add `border-radius: 4px`

**What.** The `.limMag` track is 4px with `border-radius: 3px`. Spec §7 names
`#E7E7E0` (track) and `#B9BEB7` (fill). Change height to 5px on both the
`.limMag` track and its `<i>` fill, and match `border-radius: 4px` to the
slightly heavier geometry.

**Why.** At 4px on a retina screen, the bars read as a hairline artefact
rather than a signal. 5px reads as an intentional data element. The track
fill `#B9BEB7` has low contrast on `#E7E7E0` — this is intentional
(limits are neutral) but the bar needs enough physical weight to be legible
as a bar. 5px achieves that without violating the neutral-ink rule.

**Spec.** §3.1 (magnitude bar). Spec says "4px track" — this refinement
proposes 5px. The spec's 4px is a minimum gesture; 5px is the same token
palette applied slightly more deliberately. No new tokens; literals are
unchanged.

**Mobile note.** Same height at all breakpoints.

**RTL note.** The bar fills from `inset-inline-start` — if implemented with
logical fill direction, RTL-safe. Confirm `direction: rtl` on the containing
`.limBody` so any future fill-direction logic reads correctly.

---

### R-04 · Nutrition cells: increase `nv` numeral size from 19px → 21px; tighten unit tracking

**What.** The `.nutri .nv` numeral is `font-size: 19px`. Increase to `21px`.
The unit `<i>` (11px, `--fg3`) already sits inline via `margin-inline-start: 2px`.
Also increase unit size from `11px` to `12px` to keep proportion.

**Why.** The 4-up nutrition grid is the most data-dense part of the expansion.
The 19px numeral reads as body size — not a data focal point. At 21px it
reads as a display value inside a card, which is what it is. The rest of the
cell (mono label + mini-bar) stays unchanged; only the numeral gains presence.

**Spec.** §3.4. Tokens: `--font-heading`, `font-weight: 800`, `--fg1` (unchanged).

**Mobile note.** 21px at all sizes — at 2-col mobile (< 640px) the cells are
still 50%+ wide so 21px fits comfortably.

**RTL note.** Numeral is direction-neutral; unit `<i>` is `margin-inline-start`
(already logical in the prototype).

---

## Priority 2 — Signal clarity

### R-05 · Assessment panel count pill: reduce pill background opacity; add 1px border

**What.** The count pill on the works panel uses `background: #E0F0E8`. Change
to `background: rgba(31,143,106,0.10)` (equivalent to `--bari-green` at ~10%
opacity, slightly lighter than the current literal) and add
`border: 1px solid rgba(31,143,106,0.18)` (close to `--grade-a-border`).

For the limits panel pill (`background: #EEEEE8`), change to
`background: rgba(17,19,24,0.05)` (equivalent to `--hairline-faint`) with
`border: 1px solid var(--hairline)`.

**Why.** The solid-fill pills read as badges from a design system rather than
a quiet count. A ringed pill with a near-transparent fill reads as a count
annotation — informational, not a call to action. The ring gives it legibility
without weight.

**Spec.** §3.1. Tokens: `--bari-green`, `--grade-a-border`, `--hairline-faint`,
`--hairline` — all existing. No new literals beyond alpha variants of approved
tokens.

**Mobile note.** Pill geometry stays `padding: 2px 7px; border-radius: 999px`
— unchanged.

**RTL note.** Pill is inline-end of panel title — logical placement, no change.

---

### R-06 · Bottom-line card: increase inline-start border from 3px → 4px; add `--shadow-sm`

**What.** The `.bottomLine` card has `border-inline-start: 3px solid var(--bari-green)`.
Change to `4px`. Add `box-shadow: var(--shadow-sm)`.

**Why.** The 3px left-border accent is the only hard brand-green element in the
lower half of the expansion. At 3px it is easy to miss. At 4px it reads as the
intentional editorial mark it is — the accent that says "this sentence is the
whole point." The `--shadow-sm` (0 1px 2px rgba(17,19,24,0.05)) lifts the card
barely off the canvas, distinguishing it from the background surface.

**Spec.** §3.3. Tokens: `--bari-green`, `--shadow-sm` — both existing.

**Mobile note.** Applies at all breakpoints.

**RTL note.** `border-inline-start` is already a logical property — renders on
the right edge in RTL, which is correct (reading direction start).

---

### R-07 · Shelf context position track: raise opacity from 0.5 → 0.65; increase marker border from 2.5px → 3px

**What.** `.ctxTrack` has `opacity: 0.5`. Change to `0.65`. The `.ctxMarker`
border is `2.5px solid var(--fg1)`. Change to `3px`.

**Why.** At 0.5 opacity the grade gradient is faint enough to read as a
decorative line. At 0.65 it reads as a positional instrument — you can
distinguish green end from orange end at a glance. The heavier marker border
makes the rank dot land with visual authority on the track instead of
floating ambiguously.

**Spec.** §3.2. Gradient literals already in spec (`#C77F5A → #1F8F6A`).
Tokens: `--fg1` (marker border, unchanged).

**Mobile note.** Track is full-width fluid; marker position is computed;
no changes at breakpoints.

**RTL note.** The marker uses `inset-inline-start` with the RTL-flipped
formula from the spec. No change to that logic; this refinement is opacity
only.

---

### R-08 · Additives header icon tile: increase border-radius from 8px → 10px; standardize clean/has icon size to 17px

**What.** `.addIcon` has `border-radius: 8px`. Change to `10px`. The SVG
icons inside are currently 16×16; change to 17×17 viewBox-equivalent (keep
`width/height: 17px`).

**Why.** The 30px tile at 8px radius sits between "square" and "rounded" — it
reads as a generic icon container. At 10px radius it aligns with the panel
card radius family without matching the full pill shape. The extra 1px on the
icon itself fills the tile more decisively — at 16px in a 30px tile the icon
is noticeably small.

**Spec.** §3.5. No new tokens — `border-radius: 10px` is between `--radius-md`
(8px) and `--radius-lg` (12px). Use `border-radius: calc(var(--radius-md) + 2px)`
as a non-token expression rather than a new token, since the tile is a
one-off element.

**Mobile note.** Icon tile is 30px fixed; applies at all breakpoints.

**RTL note.** Icon tile is block-direction neutral; no change.

---

### R-09 · `.wlItem` check and dash glyphs: add 1px soft ring on the `Check` SVG circle

**What.** The green `Check` SVG already has a circle stroke at `opacity: 0.55,
stroke-width: 1.3`. Increase circle stroke `opacity` to `0.7`. The `Dash` SVG
circle is `stroke: #C2C7C0, stroke-width: 1.3` — increase to `stroke-width: 1.5`.

**Why.** At 0.55 opacity the ring check feels tentative. The glyph is the
primary positive signal in the expansion; it should land with quiet confidence.
The dash circle at 1.3px is thinner than the check; equalizing to 1.5px makes
the two glyphs feel like a matched set rather than two unrelated icons.

**Spec.** §3.1 (glyphs). SVGs are inline in the component; this is a
stroke-weight adjustment only. No token change.

**Mobile note.** Applies at all sizes; glyphs are 15px fixed.

**RTL note.** SVG is direction-neutral.

---

## Priority 3 — Interaction polish

### R-10 · Row hover state: add `--shadow-sm` to `.rowhead:hover` behind the background

**What.** `.rowhead:hover` currently only applies `background: #FBFBF9` (a
literal just above `--surface`). Add `box-shadow: var(--shadow-sm)` to the
hover state — scoped to the row button, not the row container.

**Why.** The hover state at present is a very subtle background shift that is
hard to perceive on the warm canvas. A `--shadow-sm` inset-0 lift on the hover
row gives the row a clear "liftable" affordance without any color outside the
token system. Users scanning the list benefit from a tactile hover signal.

**Spec.** §4 (interaction). Token: `--shadow-sm` (existing).

**Reduced-motion note.** The shadow itself is not animated — it snaps on/off
with the background. The existing `transition: background var(--dur) ...` rule
would also transition `box-shadow`; scope the transition to `background` only
by specifying `transition-property: background` to avoid animating shadows
under `prefers-reduced-motion` inadvertently.

**Mobile note.** Touch devices don't have hover; no impact on mobile.

**RTL note.** Shadow is geometry-neutral.

---

### R-11 · Additives row open animation: add `opacity: 0 → 1` on the `.addList .inner`

**What.** The additives body uses `grid-template-rows: 0fr → 1fr` for
reveal. Add a companion `opacity` fade on the `.addList .inner` element:
`opacity: 0` when parent `.addExp` is in default state; `opacity: 1` when
`.addExp.open`. Transition: `opacity var(--dur-fast) var(--ease-out-soft)`.

**Why.** The grid-rows reveal animates height but not content visibility.
On a fast machine the content "snaps" into the expanding space rather than
revealing with it. The opacity fade makes the reveal feel intentional rather
than mechanical. This is the same technique that makes the expansion of the
main row feel soft — it should carry through to the sub-dropdown.

**Spec.** §4. Tokens: `--dur-fast`, `--ease-out-soft` (both existing).

**Reduced-motion note.** Under `prefers-reduced-motion: reduce`, skip the
opacity transition alongside the grid-rows transition (the prototype's media
query at line 195 already covers `.addExp` — add `.addList .inner` to the
same rule: `transition: none`).

**Mobile note.** Applies at all breakpoints.

**RTL note.** Opacity is direction-neutral.

---

### R-12 · Footer confidence tag: replace the dot with a 9px ring (hollow circle) for `partial` and `insufficient`

**What.** The `.confDot` is currently a 7px filled circle. For `confidence:
partial` (`dot: #B5882F`) and `confidence: insufficient` (`dot: #B5BBB6`),
render as a 9px hollow ring: `width: 9px; height: 9px; border-radius: 50%;
background: transparent; border: 1.5px solid <dot-color>`. For `verified`,
keep the 7px solid green fill (it reads as a definitive positive mark).

**Why.** A single visual language (filled dot) for three confidence states
blurs the distinction between them. The solid fill for `verified` reads as
"complete." A hollow ring for `partial` reads as "in progress." A hollow ring
in grey for `insufficient` reads as "absent." The three states now have
distinct semantics encoded in the shape, not only the color — which matters
for users who have difficulty distinguishing amber from green.

**Spec.** §3.6. Tokens: `--bari-green` (verified fill), `#B5882F` (partial
border), `#B5BBB6` (insufficient border) — the latter two are already in the
prototype's `CONF` object; they are not new values.

**Mobile note.** 9px ring vs 7px fill; marginal size difference; safe at all sizes.

**RTL note.** Dot is direction-neutral.

---

## What to leave unchanged (generic-AI pattern watchlist)

The following elements in the prototype are under surveillance — they skirt
the line but are not drifting in the accepted direction and should NOT be
"improved" in ways that would cross into dashboard territory:

- The grade gradient on the shelf context track is acceptable because it is a
  positional instrument, not a summary statistic. Do not add numeric axis
  labels or percentile annotations — that is dashboard drift.
- The count pills on the assessment panels are acceptable because they encode
  length of an already-displayed list, not a new derived number. Do not
  convert them to scores, percentages, or tier labels.
- The magnitude bars on limiting factors are decorative — they show relative
  weight, not a precise number. Do not add numeric magnitude labels (e.g.
  "35%") beside them. The bar is the signal; the number is not.
- The nutrition mini-bars are display-only with the numeral as source of truth.
  Do not add color-coded tile backgrounds to the nutrition cells (beyond the
  existing tone on the bar fill) — that would introduce a second color axis
  outside the A–E grade ramp.

---

## Invariant compliance check

| Invariant | Status after all 12 refinements |
|---|---|
| Fixed 5-section order | Preserved — no reorder proposed |
| Verbatim Hebrew labels | Preserved — no label text changed |
| Limits in neutral ink only | Preserved — no refinement touches limit text color |
| No red anywhere | Preserved |
| Bari-green rationed to positive side only | Preserved — R-05 uses green on works panel only; R-06/R-07 use existing green token in approved positions |
| Existing tokens only (no new values) | Preserved — R-03 uses spec-approved literals; R-08 uses a `calc()` expression on existing tokens; all others use named tokens from `colors_and_type.css` |
| RTL logical properties | Preserved — all spacing notes call out logical-property equivalents |
| Reduced-motion safe | Preserved — R-11 explicitly names the media query extension; R-10 scopes transition-property |
| No horizontal scroll | Preserved — no layout changes that exceed viewport |
| Mobile < 640px behavior per §5 | Preserved — all mobile notes maintain the 1-col / 2-col stacks |
| No algorithm/score-mechanic language | Preserved — no copy changes proposed |
| Pre-authored copy only | Preserved — no copy changes proposed |

---

## Acceptance test (self-check)

Each refinement is accepted if and only if:
1. It references only tokens already present in `colors_and_type.css` (or
   the spec-approved panel tint literals listed in §7), or a `calc()` expression
   on those tokens.
2. It does not change section order, label text, or color semantics (neutral
   on limits, green on positives).
3. It is implementable with a CSS property change or a small SVG/stroke
   adjustment — no layout restructuring.
4. It carries a mobile note (breakpoint behavior) and an RTL note (logical
   property compliance or direction-neutrality confirmation).

All 12 refinements meet all 4 criteria. Verified by cross-referencing each
against `colors_and_type.css` and spec §§0–8 before writing.
