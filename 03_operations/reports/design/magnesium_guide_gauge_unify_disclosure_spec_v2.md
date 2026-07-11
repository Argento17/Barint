# Magnesium Guide — Gauge Unification + Progressive Disclosure — Visual Spec v2

**Component:** revision to the existing `ThresholdBarRow`/`ThresholdGauge`/`ThresholdLadder` (`threshold-bar-row.tsx`) and `GuideProductRow` (`guide-product-row.tsx`) — same guide-surface-only component family as spec v1, not a new component family.
**Route reviewed live:** `http://localhost:4700/madrichim/magnesium` (worktree `C:\bari_wt_t504\bari-web`, TASK-504), rendered 2026-07-04.
**Author:** Design Agent — spec only. No production code touched or edited.
**Supersedes:** `magnesium_guide_threshold_infographic_spec_v1.md` §2/§3 (anatomy) and its marker geometry (§2 "Product marker" bullet). Spec v1's bucket-header pattern (§5), suppression rule (§4 last bullet), WCAG divider discipline (§2/§7.1), and CANNOT_VERIFY honesty rule are UNCHANGED and remain in force — this is an amendment, not a rewrite.
**Trigger:** three owner directives given 2026-07-04 after viewing the live page.
**Decision right:** D11/D12 — this spec is the approval Frontend needs before building. Do not build a variant.

---

## 0. What I actually saw (evidence, not assertion)

Rendered at 375×812 and 1440×900 against the live route via a Playwright script run against the worktree's own `node_modules` (`chromium.launch()`, `page.screenshot()` on `[data-testid="guide-product-row"]` and `[data-testid="threshold-bar-row"]`, plus `getBoundingClientRect`-equivalent `boundingBox()` geometry dumps). 18 product rows found at both viewports.

**Confirms Directive 1 (anatomy split is real, not a hypothetical):** `mobile-row1.png` shows all four bar rows for one product stacked. The dose (`מינון`) and safety (`בטיחות`) bars render as a thin 6px pill track with tinted zones, 1px dividers, a small dot marker, and numeric tick labels below (`0 / 150 (חצי סף) / 300 (הסף)`) — this is the anatomy the owner pointed at and said "make everything look like this." The form (`צורה וספיגה`) and label-transparency (`שקיפות תווית`) bars render as a completely different anatomy: three bordered table-like cells side by side, each containing a tier name plus a 2–3 line list of chemical names, with a small ▲ caret above the current cell. Visually these read as a data table, not a scale — confirmed on both `mobile-row1.png` and `desktop-row1.png` (the ladder's boxy cells are especially pronounced at 1152px content width in `desktop-row1.png`, where each cell is ~370px wide with generous internal padding, next to a thin gauge line one section above it).

**Confirms Directive 2 (row density):** `mobile-row1-geometry.json` — measured `boundingBox()` on the four `[data-testid="threshold-bar-row"]` elements inside the first product card at 375px: heights **95.3px / 96.0px / 96.3px / 84.8px** (dose / form / safety / transparency) = **372.4px** of bar content alone, before the thumbnail+name+verdict header (~90px measured from the row screenshot) and the price/buy footer (~40px) are added. A single product card is comfortably **500–580px** tall at 375 viewport width — under 1.5 cards fit in an 812px-tall viewport before scrolling. With 18 products in the dataset this is the "too much right now" the owner is describing, confirmed by direct measurement, not by eye.

**Confirms Directive 3 (marker subtlety):** the product marker on the gauge (`ThresholdGauge`, `threshold-bar-row.tsx:128-139`) is a 10px filled circle with a 2px white border and Tailwind `shadow-sm` (`0 1px 2px rgba(17,19,24,0.05)` — a near-invisible drop shadow, not an edge-definition device). Visually confirmed on `mobile-row1.png`: the marker on the safety gauge (pass-tint zone, background `#E2F2EF`, a very light mint) is legible but low-contrast at its edge — the white 2px border sits close in luminance to the pass-tint background it's partially over, so the marker's boundary is defined mostly by the surrounding zone-tint change rather than by the marker's own edge treatment. This matches the owner's complaint precisely: it works, but it doesn't assert itself.

**Existing precedent reused below (not invented for this spec):**
- Whole-row disclosure precedent: `comparison-row.tsx:170-181,326-333` — the canonical `/hashvaot` row uses a `<button>` wrapping the row head, `aria-expanded`, and a `ChevronDown` (`lucide-react`, already a dependency) that rotates 180° on open (`size-[15px]`, `#B5BBB6` idle → `#9A9FA6` open, `duration-200`).
- Expand/collapse motion precedent: `globals.css:513-523` — `.bari-cmp-exp { display:grid; grid-template-rows: 0fr; transition: grid-template-rows 0.24s cubic-bezier(0.22,1,0.36,1); } .bari-cmp-exp.is-open { grid-template-rows: 1fr; }` wrapping a `.bari-cmp-expclip { overflow:hidden; min-height:0; }` — the exact mechanism to reuse for the guide row's expander, not a new technique.
- Focus treatment precedent: `globals.css:472-474` — `.bari-cmp-rowhead:focus-visible { outline: 2px solid #167A58; outline-offset: -2px; }`.
- On-page sibling precedent for a text+arrow toggle: `magnesium-safety-box.tsx:189-206` already ships a `אריטa"×disclosure ▼/▲" text button on this exact page (mobile safety banner) — informs but does not override the choice below (see §3.3 rationale for why the canonical chevron pattern is used instead).
- Contrast values reused verbatim from the already-computed `magnesium_guide_revision_visioncritic_v1.md` §3 table (`#4E5663` against `#E2F2EF`/`#EAEDF8`/`#F8E7EF` = 6.41 / 6.34 / 6.23 : 1) — cited again in §2.3 below rather than re-measured, since the pairing is unchanged.

---

## 1. Directive 1 — Unify all four bars onto the horizontal zoned-gauge anatomy

### 1.1 Continuous bars (dose, safety) — unchanged anatomy, carries the Directive 3 marker upgrade only

No structural change. `ThresholdGauge` keeps its real-value domain, zone tints, mandatory divider lines (solid/dashed per spec v1 §2), numeric tick labels, and clamp+`+` handling exactly as shipped. Only the marker changes — see §2.

### 1.2 Categorical bars (form, label-transparency) — NEW: rebuilt as a 3-zone gauge, not a data table

Replace `ThresholdLadder`'s bordered-cell-table rendering with the **same track anatomy as `ThresholdGauge`**, adapted for an ordinal (non-numeric) domain:

```
צורה וספיגה                                          ⬤ עומד בסף
┌──────────────────────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒|░░░◉░░░░░░░░░░░░░░░░░░░░ │  ← dir="ltr", equal 3 zones
└──────────────────────────────────────────────────────────────┘
      נמוכה              בינונית              גבוהה
                    המוצר: ציטראט · קבוצת הספיגה הגבוהה
```

- **Track:** identical construction to the gauge — 6px height, `border-radius: var(--radius-pill)`, neutral base `#EDEFEC`, painted over by 3 zone `<div>`s. The only change from a numeric gauge: the 3 zones are **fixed equal widths (33.33% each)**, not value-proportional — there is no numeric domain to be proportional to, and forcing unequal widths onto an ordinal scale would fabricate a precision that doesn't exist. (This equal-width rule is not new — it's the same rule the current `ThresholdLadder`'s three `flex-1` cells already use; only the box-table skin changes, not the width logic.)
- **Zone tint + divider direction:** unchanged left=worst→right=best convention from spec v1 §3 ("state it once, apply identically to both anatomies"). Left zone = fail-tint (`#F8E7EF`), middle = flag-tint (`#EAEDF8`), right zone = pass-tint (`#E2F2EF`) — the SAME three `GUIDE_BAR_TONE` backgrounds already used by the continuous gauges, so a reader who has decoded "pink=bad, blue=middling, green=good" on the dose bar reads it identically here with zero new color vocabulary.
- **Dividers:** both zone boundaries (33.3%, 66.7%) get the **solid** 1px divider (`#6B7070`) used for dose's hard 150/300 boundaries — categorical tier boundaries are all equally hard (a product is never "half in the moderate tier"), so there is no soft/dashed case here the way safety's EFSA line needed one.
- **Marker:** the SAME upgraded marker from §2 below, positioned at the **horizontal center of the product's current tier's zone** (16.67% / 50% / 83.3%) — a discrete marker sitting inside its zone, never at a fabricated intermediate position. This is the literal reading of the task's "an honest discrete marker sitting in its zone, NOT a fake continuous position."
- **Tick labels:** replace the gauge's numeric anchors with the **three tier names**, each centered under its own zone (not just at boundaries, since there's no "0" starting anchor for an ordinal scale): `נמוכה / בינונית / גבוהה` (form) or `לא גלוי כלל / חלקי / גלוי במלואו` (label-transparency). Same token as the gauge's tick labels: 11px, `#6B7070`.
- **Caption:** unchanged format, `המוצר: {tier value label} · {note}` — e.g. `המוצר: ציטראט · קבוצת הספיגה הגבוהה`, reusing `result.note` verbatim exactly as spec v1 §2 already mandates.
- **CANNOT_VERIFY fallback:** identical rule to the continuous gauge — all 3 zones stay painted (the tier system is a fixed external fact independent of this product) but the marker is replaced by the hollow dashed ring, **fixed at 50% of the whole track** (the same absolute rule as the continuous gauge's CANNOT_VERIFY, not a new rule per anatomy). Caption swaps to the existing `note` fallback text (`לא ניתן לקבוע רמת ספיגה · תערובת לא-גלויה`).

**Content simplification this requires — flagged, not silently dropped:** today's ladder shows a 2–3 line list of chemical names inside EACH of the three cells (e.g. `אוקסיד / קרבונט` under "נמוכה"). A thin 24px-tall gauge track has no room for that; the unified anatomy carries only the tier name in the tick label. This is not a content loss — the full chemical-form-to-tier mapping already lives verbatim in the page's education spine section (`magnesium-guide-data.ts` `educationSpine`, "הצורות הכימיות, מוסבר שוב בקצרה" per spec v1 §2 sub-label note), which is the anatomy's natural home for a static reference table, not a per-product row repeated 18 times. **Frontend/Content should confirm no reader-facing gap opens** — flagged in §5 risk register, not resolved here by assertion.

### 1.3 Geometry side-effect (a net win, not a new ask)

Because the boxy ladder cells (currently ~64-70px tall including two lines of chemical-name sublabels) collapse into the same ~24px slim-track-plus-tick-row height as a gauge, converting form/label-transparency to this anatomy **reduces** their per-bar height versus today, partially offsetting the marker-size increase in §2. Net effect on total row height is addressed together with the disclosure change in §3.4.

---

## 2. Directive 3 — More visible product marker (both anatomies)

### 2.1 What's wrong, measured

Current marker (`threshold-bar-row.tsx:128-139`): 10px diameter circle, 2px white border, Tailwind `shadow-sm`. Total visible footprint ≈ 14px. The white border is the only edge-definition device, and white against the lightest zone tint (`#E2F2EF`, pass) is a low-contrast pairing at the marker's own boundary — this is a UI-component contrast question (WCAG 1.4.11, ≥3:1 for a graphical object conveying state), not a text-contrast one, and today's construction doesn't reliably clear it against every zone tint the marker can land on.

### 2.2 New marker construction

Three concentric layers, built as a single filled circle plus two stacked `box-shadow` rings (no extra DOM nodes needed):

```css
/* core */
width: 12px; height: 12px; border-radius: 50%;
background: {tone.text};                      /* unchanged: teal #0B5D52 / indigo #2E3C86 / berry #84184F */
box-shadow:
  0 0 0 3px #FFFFFF,                           /* halo — separates core from whatever it sits on */
  0 0 0 4.5px #4E5663;                         /* definition ring — guarantees an edge on EVERY zone tint */
```

- **Core:** 12px diameter (was 10px), same three state-tone fill colors — no new hue, per spec v1's own non-goal (§8).
- **Halo:** 3px solid white ring (was a 2px `border`, now a `box-shadow` ring so it doesn't eat into the core's visible diameter). Function: lift the marker off the immediate zone-tint color underneath it, exactly as the old border did, just thicker.
- **Definition ring (NEW layer):** 1.5px solid **`#4E5663`** (existing `--fg2` token — already used for every caption/sublabel on this component, not a new hex) immediately outside the white halo. This is what actually solves Directive 3: white-on-near-white (halo-on-pass-tint) has poor edge contrast on its own; a solid mid-slate ring outside the halo guarantees a real boundary regardless of which zone the marker sits in.
  - **Contrast, cited not re-measured:** `#4E5663` against pass-tint `#E2F2EF` = 6.41:1, against flag-tint `#EAEDF8` = 6.34:1, against fail-tint `#F8E7EF` = 6.23:1, against the neutral cannot-verify track `#F3F4F2`/`#EDEFEC` ≈ 6.7:1 — these four numbers are the exact pairings already computed in `magnesium_guide_revision_visioncritic_v1.md` §3 for the ladder sublabel text (same color, same four backgrounds). All clear the WCAG 1.4.11 non-text 3:1 floor by a wide margin, and in fact clear the stricter 4.5:1 text floor too, so there is headroom.
  - **Core-vs-halo contrast:** teal/indigo/berry core fill against the white halo — the closest already-computed proxy is "text on own bg" from `bar-state-badge.tsx` (pass 6.73:1, flag 8.53:1, fail 7.94:1 against each state's own near-white tinted bg); against pure white the ratio is the same order of magnitude or slightly higher, comfortably clearing 3:1.
- **Total footprint:** 12 + 2×3 (halo) + 2×1.5 (ring) = **21px** diameter, vs. today's 14px — a 50% increase, matching the "larger diameter" ask directly.
- **Container height:** bump the gauge/zone-gauge wrapper from 18px to **24px** so the 21px marker has vertical clearance without clipping (track stays 6px, vertically centered, unchanged).
- **Colorblind-safety preserved, not re-invented:** shape (filled circle) and position (percentage along the track / center of its zone) remain the only information-bearing signals, exactly as spec v1 mandated — this change only makes the SAME shape more visible, it does not add a second encoding.
- **Clamp `+` glyph:** unchanged position and size (`threshold-bar-row.tsx:156-164`) — it sits outside the marker, no interaction with the new rings.
- **CANNOT_VERIFY fallback — explicitly UNCHANGED per the task's instruction:** the hollow dashed ring (10px, 1.5px dashed `#4E5663`, mid-track) stays exactly as shipped. Do not apply the new 3-layer treatment to it — a bigger "we don't know" glyph would work against its own purpose of reading as visually quieter than a real data point.

### 2.3 State-by-state (both anatomies, replaces spec v1 §2's marker row only)

| State | Marker |
|---|---|
| PASS | 12px teal (`#0B5D52`) core, white halo, `#4E5663` definition ring, centered on its value/zone |
| FLAG | 12px indigo (`#2E3C86`) core, same halo/ring |
| FAIL | 12px berry (`#84184F`) core, same halo/ring |
| FAIL, clamped | Same FAIL marker, pinned at domain end (gauge only), `+` glyph beside it, unchanged position rule |
| CANNOT_VERIFY | **Unchanged**: hollow dashed 10px ring, `#4E5663`, fixed at 50% — no halo/ring layers added |

---

## 3. Directive 2 — Progressive disclosure: compact row + one expander per product

### 3.1 Collapsed (default) row — compact summary anatomy

```
┌─ product card ─────────────────────────────────────────────┐
│ ┌────┐  שם המוצר · מותג                       [הבחירה...] │
│ │IMG │  המוצר — 250 מ״ג יסוד, ציטראט. עובר עם דגל:       │  ← oneLinerHe, unchanged
│ │56px│  צורה פרופיל אותו חלק (250 מתוך 300)...            │
│ └────┘                                                      │
│         ⬤מינון:עם דגל   ⬤צורה:עומד בסף                   │  ← compact badge row
│         ⬤בטיחות:עם דגל  ⬤שקיפות:עומד בסף                 │     (labeled badges, NO gauge/caption)
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │  ← hairline, matches existing
│              הצג פירוט המדדים  ⌄                            │  ← expander control (full-width)
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│  ₪1.20 / מ״ג אפקטיבי                          [קנה →]      │  ← price + buy, unchanged, always visible
└──────────────────────────────────────────────────────────────┘
```

- **Thumbnail, name, brand, `isDefaultPick` pill, `oneLinerHe` verdict:** unchanged — these already carry the single most decision-relevant content and stay always-visible (this is the line the two-gate content sign-off already approved; disclosure must never hide it).
- **Compact badge row:** the 4 `BarStateBadge` components (with their now-visible bar-name labels, per spec v1 Finding A) render in a `flex flex-wrap` row — this is exactly what rendered on the page BEFORE the threshold-gauge infographic existed, minus the old invisible-label bug. No gauge, no ladder, no caption line at this level. Gap 6-8px, wraps to 2 rows of 2 at 375px (matches current badge width behavior).
- **Price + buy button:** unchanged, always visible — this is the page's conversion action and must never be gated behind a disclosure.
- **Expander control:** see §3.3.

### 3.2 Expanded state — reveals the full `ThresholdBarRow` stack

Tapping the expander reveals, in place, the same 4 stacked bar rows spec v1 §4 already defines (bar-name + badge + gauge/zone-gauge + caption, per §1 above) — nothing about the expanded content changes from what's already built, only its default visibility.

```
┌─ product card (expanded) ──────────────────────────────────┐
│ [ ...same header as §3.1... ]                               │
│ ⬤מינון:עם דגל  ⬤צורה:עומד בסף  ⬤בטיחות:עם דגל  ⬤שקיפות... │
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│              סגור פירוט המדדים  ⌃                           │  ← same control, rotated chevron, open label
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│  מינון                                    ⬤ עם דגל          │
│  [gauge, per §1.1]                                          │
│  המוצר: 250 מ״ג · ...                                       │
│  ── (repeat for form / safety / transparency, per §1) ──    │
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│  ₪1.20 / מ״ג אפקטיבי                          [קנה →]      │
└──────────────────────────────────────────────────────────────┘
```

Note the expander control appears in the SAME position both collapsed and expanded (directly under the compact badge row) — it does not jump to the bottom of the revealed content, so the tap target doesn't move under the user's thumb after the reveal animation runs.

### 3.3 Expander control — geometry, states, a11y, copy slot

**Why one expander per product row, not one per bar (task's explicit ask to justify):**
1. The compact badge row already shows all 4 states at a glance — a reader who wants more detail on any one bar is almost always doing so to see it *in the context of the other three* for the same product (e.g., "dose flagged — is form good enough to make up for it?"), not to drill into exactly one bar in isolation. Per-bar toggles would force 4 taps to reconstruct the same picture one row-level toggle gives in one tap.
2. A per-bar toggle multiplies tap targets to 4×18 = 72 on this page alone — worse mobile ergonomics than 18, working against the very density complaint this directive exists to fix.
3. **Existing on-page precedent already made this exact call**: `MagnesiumSafetyBox` (`magnesium-safety-box.tsx`) reveals its GI-effects paragraph AND all 4 drug-interaction entries AND the disclaimer behind ONE toggle, not one per drug class. This spec's per-row (not per-bar) granularity keeps the page internally consistent with a pattern it already ships.
4. Row-level disclosure keeps every collapsed card the same height, which is what makes an 18-row list scannable — per-bar disclosure would leave the list in 2^4 possible partial-expansion states per row, breaking visual rhythm.

**Control construction** — reuses the canonical `/hashvaot` chevron idiom (`comparison-row.tsx`), not the safety-box's green-underline text-link idiom, because this control sits inside a list of 18 repeating rows (matching the site-wide "list-row disclosure" pattern) rather than a one-off inline banner (the safety box's context). Using the more site-familiar chevron here, and reserving green/underline for actual navigation and the buy CTA, avoids the expander visually competing with the buy button for "this is a link" attention.

```css
/* the control itself */
width: 100%; min-height: 40px;
display: flex; align-items: center; justify-content: center; gap: 4px;
border-top: 1px solid rgba(17,19,24,0.05);   /* same hairline already used between ThresholdBarRow blocks */
font-size: 12px; font-weight: 600; color: #4E5663;   /* --fg2, not brand green — this is disclosure, not navigation */
```

- **Icon:** `ChevronDown` (`lucide-react`, already imported site-wide), `size-[15px]`, `strokeWidth={1.75}`, color `#B5BBB6` idle → `#9A9FA6` + `rotate-180` open, `transition-transform duration-200` — identical tokens to `comparison-row.tsx:326-333`, not new values.
- **Idle label (copy slot — do not author final text here):** placeholder `"הצג פירוט המדדים"`. **Open label (copy slot):** placeholder `"סגור פירוט המדדים"`. Both route through the standard two-gate sign-off before ship, per the content sign-off hard rule — Design is specifying the SLOT (position, length budget ≈ 20 characters to fit one line at 375px, weight/color) not the shipped words.
- **Hit target:** the full 100%-width, 40px-tall bar is the button (not just the text+icon) — exceeds WCAG 2.5.5 target-size guidance comfortably and gives a thumb-friendly tap area distinct from the nested Buy-button link elsewhere in the card (this is exactly why the control is its own standalone button rather than making the whole card clickable the way `comparison-row.tsx` does — that pattern assumes no nested interactive element sits inside the collapsed head; this card's price/buy row does, so the whole-card-is-a-button idiom cannot transfer directly).
- **Motion:** reuse `.bari-cmp-exp` verbatim (`display:grid; grid-template-rows: 0fr → 1fr; transition: grid-template-rows 0.24s cubic-bezier(0.22,1,0.36,1);` + `.bari-cmp-expclip { overflow:hidden; min-height:0; }`) from `globals.css:513-523` — do not invent a second motion curve/duration for this page.
- **a11y:**
  - `<button type="button" aria-expanded={open} aria-controls="{row-id}-detail">` on the control.
  - The revealed panel: `<div id="{row-id}-detail" aria-hidden={!open}>`, same pattern as `comparison-row.tsx:337` (`aria-hidden={!open}` on `.bari-cmp-exp`).
  - `focus-visible`: reuse `outline: 2px solid #167A58; outline-offset: -2px;` from `.bari-cmp-rowhead:focus-visible` (`globals.css:472-474`).
  - The chevron icon stays `aria-hidden` (decorative); the accessible state is carried entirely by `aria-expanded` + the text label change, not by icon rotation alone.
  - Keyboard: native `<button>` gives Enter/Space activation for free — no custom `onKeyDown` needed (unlike `comparison-row.tsx`'s row-head, which needed one because it's a `<button>` wrapping a grid of non-button children; this control's content is just text+icon, so the plain native behavior suffices).

### 3.4 Net row-height effect (projected, not measured — the layout doesn't exist yet)

Collapsed-row estimate at 375px, built up from real measured sub-pieces where available: thumbnail/name/brand header ≈ 90px (measured, unchanged) + `oneLinerHe` at 2 lines ≈ 40px (measured, unchanged) + compact badge row ≈ 60px (2 wrapped rows of badges, extrapolated from the badges' own already-measured ~28px height) + expander control 40px (spec'd above) + price/buy row ≈ 40px (measured, unchanged) + card padding/gaps ≈ 40px ⇒ **≈ 310px collapsed**, versus **≈ 500–580px today** (§0). This roughly doubles the number of product rows visible per scroll without opening anything — that is the point of the directive. This number is a projection from real sub-measurements, not a rendered fact; **Frontend/Design's post-build vision-in pass must re-measure the actual collapsed height** before this is treated as confirmed.

---

## 4. Geometry / token reference (cite, don't invent)

| Element | Value | Source |
|---|---|---|
| Zone-gauge track height | `6px`, unchanged | `threshold-bar-row.tsx:90` |
| Zone-gauge container height | `18px → 24px` (bumped for marker clearance) | this spec §2.2 |
| Marker core diameter | `10px → 12px` | this spec §2.2 |
| Marker halo | `2px border → 3px box-shadow ring, #FFFFFF` | this spec §2.2 |
| Marker definition ring (NEW) | `1.5px solid #4E5663` | this spec §2.2; color = existing `--fg2` |
| Marker total footprint | `14px → 21px` | computed above |
| Categorical zone width | `33.33%` each, fixed | this spec §1.2; matches existing `ThresholdLadder` `flex-1` equal-width rule |
| Zone divider (categorical) | `1px solid #6B7070` at 33.3%/66.7% | this spec §1.2 |
| Tick label (all bars) | `11px`, `#6B7070` | `threshold-bar-row.tsx:168`, reused verbatim |
| Expander control height | `40px` min | this spec §3.3 |
| Expander hairline | `1px solid rgba(17,19,24,0.05)` | matches `threshold-bar-row.tsx:278` inter-bar divider |
| Expander icon | `ChevronDown`, `size-[15px]`, `strokeWidth 1.75`, `#B5BBB6→#9A9FA6`, `duration-200` | `comparison-row.tsx:326-333`, reused verbatim |
| Expander motion | `grid-template-rows 0fr→1fr`, `0.24s cubic-bezier(0.22,1,0.36,1)` | `globals.css:513-523` (`.bari-cmp-exp`), reused verbatim |
| Expander focus ring | `2px solid #167A58`, `outline-offset -2px` | `globals.css:472-474` (`.bari-cmp-rowhead:focus-visible`), reused verbatim |
| Expander label color | `#4E5663` (`--fg2`) | deliberate choice — not brand green, so it doesn't compete with the Buy CTA (§3.3) |
| GUIDE_BAR_TONE (all fills, unchanged) | teal `#0B5D52`/`#E2F2EF`, indigo `#2E3C86`/`#EAEDF8`, berry `#84184F`/`#F8E7EF`, gray `#4E5663`/`#F3F4F2` | `bar-state-badge.tsx:46-49` |

---

## 5. WCAG / RTL risk register for Frontend

1. **Marker definition-ring contrast — verified by citation, not fresh-measured.** The `#4E5663` ring's contrast against all 4 possible backgrounds (pass/flag/fail/neutral tints) is reused from `magnesium_guide_revision_visioncritic_v1.md` §3, which measured the *same hex against the same 4 backgrounds* for the ladder sublabel text. That prior measurement is a valid proxy for the same pairing used as a ring instead of text, but **run `npm run test:a11y` after implementation** to confirm axe has no objection to the new marker geometry specifically (a decorative `aria-hidden` marker is generally axe-invisible, but confirm no unexpected regression).
2. **Categorical tick-label collision risk (NEW, flagged here for the first time).** The longest tier label, `גלוי במלואו` (label-transparency, "fully disclosed"), is materially longer than the numeric ticks (`"0"`, `"300"`) the gauge anatomy was designed around. At the measured ~201px mobile content width, three equal 67px zones each need to fit a centered tick label without colliding with its neighbor. **Frontend must verify** the longest label doesn't clip or overlap at 375px — if it does, allow the tick label to wrap to 2 lines (unlike the numeric gauge ticks, which are short enough to never need this) rather than truncating or shrinking below 11px.
3. **Content gap from dropping the ladder's per-tier chemical-name sublabels (§1.2).** Flagged, not resolved — the mapping still exists in the page's `educationSpine`, but this spec cannot confirm on its own that removing it from the per-product row doesn't strand a reader who lands mid-page via a shared link and never scrolls to the education section. Recommend Content Agent confirm during two-gate sign-off, not a Design-only call.
4. **Expander default-state and SSR/first-paint:** the panel should render `aria-hidden="true"` and visually collapsed (`grid-template-rows: 0fr`) by default with NO client-side flash-of-expanded-content — confirm the `useState` default is `false` and the collapsed CSS class is present in the server-rendered HTML, not applied only after hydration (a one-frame "flash open then collapse" would be a real, if brief, regression).
5. **`dir="ltr"` gauge-in-RTL convention** — spec v1 §2/§7.4's open item (native-Hebrew-reader confirmation still outstanding) is unchanged and now also applies to the categorical zone-gauge, which is new territory for that same open question. Does not block this build; still flagged as outstanding.
6. **Do not let the marker upgrade migrate into `/hashvaot`** — same non-goal as spec v1 §7.6. This marker only exists inside `ThresholdGauge`/guide zone-gauges; the canonical A–E `ScoreChip`/`gradeDotOffset` marker on comparison pages is a separate, frozen system and is out of scope here.

---

## 6. Explicit non-goals (conformance discipline, carried from spec v1 §8)

- No numeric score or letter grade introduced anywhere — bars stay PASS/FLAG/FAIL/CANNOT_VERIFY; the categorical zone-gauge visualizes an ordinal tier, never a computed number.
- No new color hue anywhere in this amendment — every color cited (including the new marker ring) is an existing token (`GUIDE_BAR_TONE`, `--fg2`, white).
- No per-bar disclosure granularity — one expander per product row only, per §3.3's justification; this is a considered design call, not a placeholder pending a future "even more granular" pass.
- No change to the always-visible header content (`oneLinerHe`, price, buy button) — disclosure applies ONLY to the 4 bar-detail rows, never to the content the two-gate sign-off already approved as always-shown.
- No change to the CANNOT_VERIFY marker treatment (§2.3) — the task explicitly asked to leave it as-is, and doing so also gives users a visual cue that "we don't know" is deliberately quieter than a real, more-visible data point.

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\design\\magnesium_guide_gauge_unify_disclosure_spec_v2.md",
      "sha256": "60BA60A94265967845B68EE186CCE472BBD7F88E12FC060961927A37A28BA4A9 (hash of the pre-this-edit save; this JSON edit itself changes the file's bytes after the hash was taken, so it is a self-reference approximation, not an exact post-save hash — same caveat as spec v1's own self-hash entry)"
    },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\mobile-full.png", "sha256": "1F4464512EF5F9FBEC8DBF2C61EA71273DE68284907C45CB0BEB2627F6D03C8A" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\mobile-row1.png", "sha256": "4418E137542B66D3546B61D61436C7AEF4E9995FE020C3D9153F534A6AC71408" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\mobile-row2.png", "sha256": "6D50CD866BCBDE7C0FF75052C5AB92279C63FF47D63B0BCA455AB32C1DAFE250" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\mobile-row1-geometry.json", "sha256": "8C1AED436EA7957FA7597F7FF60ACDC129882F4B3C632C91D5875F7AB30897F0" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\desktop-full.png", "sha256": "06BCF1713A0B2193B4F29641327FEB7B97A2A55743937FDF9AE85C01F38C5499" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\desktop-row1.png", "sha256": "0873D4B066ABE59890E72DD82E7CE8F1DA60C2E5D6D7D6100893C5F70746A039" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\desktop-row2.png", "sha256": "48BAF4451746261EB70FC6C9ED1A82F7E0CD2112E0A80F8E6E7C401B5A93A41D" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-v2\\desktop-row1-geometry.json", "sha256": "C1C42EFAD36499A3425A4854A93A2D23A2FB8253F7ED3BCA845DF2C15F208AB3" }
  ],
  "counts": {
    "owner_directives_addressed": 3,
    "bars_in_scope": 4,
    "anatomies_before": 2,
    "anatomies_after": 1,
    "products_reviewed_in_dataset": 18,
    "viewports_reviewed": 2,
    "product_rows_found_per_viewport": 18,
    "marker_footprint_px_before": 14,
    "marker_footprint_px_after": 21,
    "measured_bar_row_heights_px_mobile": [95.28125, 96.03125, 96.28125, 84.78125],
    "measured_bar_row_total_height_px_mobile": 372.375,
    "projected_collapsed_row_height_px_mobile": 310,
    "contrast_pairings_cited_from_prior_measurement": 4,
    "new_contrast_pairings_flagged_for_axe_confirmation": 1
  },
  "commands_run": [
    { "command": "PowerShell Invoke-WebRequest http://localhost:4700/madrichim/magnesium (confirm dev server live)", "exit_code": 0 },
    { "command": "node scripts/_design-agent-mag-shot.mjs (ad hoc Playwright script placed inside C:\\bari_wt_t504\\bari-web, run against its own node_modules, then deleted after use) — full-page + row1/row2 screenshots + bar-row getBoundingClientRect-equivalent geometry, mobile 375x812 + desktop 1440x900", "exit_code": 0 },
    { "command": "Get-FileHash -Algorithm SHA256 on all captured PNG/JSON evidence files", "exit_code": 0 }
  ],
  "not_done": [
    "No axe/WCAG scan run against the NEW marker/zone-gauge/expander markup (it doesn't exist yet) — contrast citations in §2.2/§5.1 are carried from prior measurements of the same hex/background pairings, not independently re-measured on this exact new geometry; Frontend must run npm run test:a11y after implementation.",
    "Collapsed-row height (§3.4) is a projection built from real measured sub-pieces, not a measurement of the finished layout — flagged explicitly as such, not asserted as fact.",
    "Categorical tick-label collision risk (§5.2) is identified but not resolved — needs Frontend verification at 375px with the actual longest Hebrew tier label.",
    "Expander button copy ('הצג פירוט המדדים' / 'סגור פירוט המדדים') are Design's placeholder slot-fillers only, not Content-authored final strings — routes through the standard two-gate sign-off per the content sign-off hard rule before ship.",
    "Content gap from dropping ladder per-tier chemical-name sublabels (§5.3) needs Content Agent confirmation, not resolved unilaterally here.",
    "No static HTML/CSS mock file produced beyond the ASCII diagrams in this spec — can produce one on request if Frontend needs it before starting."
  ],
  "acceptance_test": "Frontend implements: (1) categorical bars (form, labelTransparency) rendered via the same zone-gauge track anatomy as dose/safety, 3 equal zones + solid dividers + tier-name ticks + honest mid-track hollow-ring fallback; (2) the upgraded 3-layer marker (12px core + 3px white halo + 1.5px #4E5663 ring, ~21px total) applied identically on all 4 bars' real markers, CANNOT_VERIFY fallback left untouched; (3) product rows default collapsed to thumbnail+name+oneLinerHe+compact-badge-row+price/buy, with ONE per-row expander (chevron + copy slot, aria-expanded/aria-controls, reusing the existing .bari-cmp-exp grid-template-rows motion and .bari-cmp-rowhead focus-visible ring) revealing the full 4-bar detail stack. Design Agent re-renders /madrichim/magnesium at 375px + desktop via the same method used here, confirms all three directives measure as built, and runs npm run test:a11y + npm run test:visual with new baselines attached before/after at both viewports before this is called done."
}
```
