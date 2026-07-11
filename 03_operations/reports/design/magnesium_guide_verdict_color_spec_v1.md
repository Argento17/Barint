# Magnesium Guide — Verdict Color Spec v1 (TASK-504, final polish)

**Author:** Design Agent · **Date:** 2026-07-04 · **Route reviewed:** `http://localhost:4700/madrichim/magnesium` (worktree `C:\bari_wt_t504\bari-web`)
**Decision rights:** D12 (Design Spec Approval) — this doc IS the approval artifact. D11 (Frontend
Implementation) requires this spec before either change is built; **do not implement from the owner's
verbal directive alone.**

**Status:** spec only. No source file under `bari-web/` was edited to produce this document.

---

## 0. What I looked at (vision-in, before writing anything)

Rendered the live route at 375×812 and 1280×720 via `vision-in.mjs` (pointed `--base` at the worktree's
running dev server on :4700) and cropped the PNG around the exact `y` coordinates `geometry.json` reported
for the tier `<h2>`s and `[data-testid="bar-state-badge"]`. Evidence:

- `verdict-spec-mobile/madrichim-magnesium__mobile.png` + `.geometry.json` (113 elements measured)
- `verdict-spec-desktop/madrichim-magnesium__desktop.png` + `.geometry.json` (113 elements measured, 1280px — the vision-in script's fixed desktop viewport; owner asked for 1440, delta is 160px of extra whitespace on a single-column layout, not a layout-bearing difference, confirmed by the desktop crop below)
- Crops: `crop-tier-headers.png`, `crop-badge-row.png`, `crop-good-tier.png`, `crop-desktop-tier.png`

**Measured BEFORE state (confirms both owner complaints):**

| Element | Measured |
|---|---|
| Tier `<h2>` ("מומלץ מאוד") | `font-size: 10.4px`, `color: rgb(78,86,99)` = `#4E5663`, no background, mono uppercase, sits beside a 1px hairline divider. Identical treatment on mobile and desktop (1280px) — single-column layout, no grid reflow. |
| `bar-state-badge` (first compact-row chip, product 1) | `font-size: 11px`, `color: rgb(46,60,134)` = `#2E3C86` (indigo), `background: rgb(234,237,248)` = `#EAEDF8`, text = **"עם דגל"** (the *state word*, not the bar's name) |

Both match the source exactly (`bar-state-badge.tsx`, `guide-product-table.tsx`) — no drift between code and
render. The crops show 4 pill chips per product, each carrying a state word ("עומד בסף" / "עם דגל" / "לא
עומד" / "לא ניתן לאמת") with no indication of *which of the six bars* fired that state unless you already
know the fixed `GUIDE_BAR_ORDER`. This is the literal problem the owner is naming.

---

## 1. Directive 1 — the chip becomes the attribute name, colored by that bar's state

### 1.1 What changes, mechanically

`BarStateBadge` (`bari-web/src/components/shared/bar-state-badge.tsx`) currently renders the **state
word** (`BAR_STATE_LABELS_HE[state]`) as the chip's visible text, with `barLabel` folded only into the
`aria-label`. Invert this:

- **Visible text → `barLabel`** (e.g. "מינון"), not the state word.
- **Chip color → still driven by `state`** (unchanged data flow — only the color's own value set changes, see §3).
- **`barLabel` becomes a required prop**, not optional — it is now the chip's primary content, not an
  accessibility-only enhancement.
- **The state word does not disappear** — it moves to two redundant non-visual channels (§1.3): the
  `aria-label` and a native `title` tooltip. A sighted mouse/keyboard user who hovers or focuses the chip
  still reads the literal word ("עם דגל"), they just don't see it printed by default.

This chip is used in exactly two places — both get the same treatment, no divergence:
1. `GuideProductRow`'s always-visible compact badge row (`guide-compact-badge-row`) — 4–6 chips per product.
2. `ThresholdBarRow`'s expanded per-bar detail row, where it currently sits **next to a second, separate,
   black bold `<span>{barLabel}</span>`** (`threshold-bar-row.tsx` line ~342). That plain-text span becomes
   redundant once the chip itself shows the name in color — **remove it**, leaving only the colored chip on
   that line (still followed by the gauge/ladder and the caption line, which already states the concrete
   value: "המוצר: 200 מ״ג · ..." — that caption is a stronger redundancy than a duplicated plain label
   would be).

### 1.2 Anatomy — all four states

One shared geometry, four color+icon combinations. Geometry is unchanged from today's chip except the
icon slot is slightly larger than the old 6px dot (icons need more room than a dot to read as a
shape, not a smudge, at 11px text size).

```
┌────────────────────┐
│  ⬤icon  Name        │   pill: border-radius 999px, padding 4px 10px, gap 5px,
└────────────────────┘   font-size 11px / font-weight 600 / line-height 1.4 (unchanged from today)
```

| State | Visible text | bg | border | text + icon color | icon (lucide-react) | contrast (text/bg) |
|---|---|---|---|---|---|---|
| **PASS** | bar name (e.g. "מינון") | `#E2F2EF` | `#0F6E6333` | `#0B5D52` | `Check` | **6.73:1** |
| **FLAG** | bar name (e.g. "צורה וספיגה") | `#FCEFD6` | `#A8650033` | `#8A5300` | `TriangleAlert` | **5.56:1** |
| **FAIL** | bar name (e.g. "בטיחות") | `#FBE4E1` | `#B3261E33` | `#A02318` | `X` | **6.29:1** |
| **CANNOT_VERIFY** | bar name (e.g. "שקיפות תווית") | `#F3F4F2` | `#D8DDD9` | `#4E5663` | `HelpCircle` | **6.71:1** |

All four clear WCAG AA's 4.5:1 floor for normal-size text by a wide margin (measured via the standard
relative-luminance formula, script + full candidate table in
`scratchpad/contrast.py` — not asserted by eye). `lucide-react` is already a project dependency
(`ChevronDown` is imported from it in `guide-product-row.tsx`), so no new package.

**Icon = text color** (not a separate lighter tint). I tested a lighter "icon-only" tint first and it
failed WCAG 1.4.11's 3:1 non-text-contrast floor for the neutral state (`#8A9088` on `#F3F4F2` = 2.96:1 —
**fails**). Using the same color for icon-stroke and text sidesteps that failure mode entirely and is
simpler to implement (one color per state, not two).

### 1.3 Accessibility redundancy (mandatory — color is never the only signal)

Three independent non-color channels carry the state, on top of the color:

1. **Icon shape** — `Check` / `TriangleAlert` / `X` / `HelpCircle`. Four visually distinct glyphs, legible
   at 11px, `aria-hidden` (redundant to the accessible name below, not a second source of truth).
2. **Accessible name** (screen readers) — `aria-label="{barLabel}: {stateWordHe}{note ? ' — ' + note : ''}"`,
   e.g. `"מינון: לא עומד — המינון מתחת לטווח האפקטיבי המתועד"`. This is unchanged in spirit from today's
   badge, just re-pointed: the *visible* text is the name, the *announced* text still leads with the name
   and states the real verdict word.
3. **Native tooltip** — `title="{stateWordHe}{note ? ' — ' + note : ''}"`. Today `title` is only set when a
   `note` exists; change it to always render at minimum the plain state word, so a sighted low-vision user
   who isn't sure a green vs. teal chip means "pass" can hover/focus and get the explicit Hebrew word,
   every time, not only on flagged bars.
4. **The expanded gauge itself** (unchanged) already encodes position with a real divider line
   (`borderInlineStart`, never color-only per the existing `ThresholdTrack` comment) and a
   filled-vs-hollow marker shape for CANNOT_VERIFY — this was already correct and needs no change.

I decided **against adding a fifth channel** (a tiny sub-label word under the chip). Name + color + icon +
(on expand) the gauge and its caption is four independent signals already — a fifth is clutter the compact
row doesn't have room for at 375px with up to 6 chips per product, and it would fight the whole point of
the change, which is to let the *name* be the primary readable thing.

---

## 2. Directive 2 — color-coded, prominent tier headers

### 2.1 What changes, mechanically

`TierSectionHeader` (`guide-product-table.tsx` lines 54–64) currently renders a plain 10.4px gray mono
uppercase `<h2>` + a muted count + a 1px hairline divider — confirmed identical on mobile and desktop by
the crops above. Replace the `<h2>` itself with a colored pill in the same tint/border/text-color system as
the chip (§1.2/§3), keep the count and the divider exactly as they are today (do not touch their styling,
spacing, or the caption/empty-state text below them — this is a color/prominence change only, not a
restructure).

```
┌──────────────────────┐  ( 0 )  ────────────────────────
│ ⬤icon  מומלץ מאוד      │
└──────────────────────┘
```

- Pill: `border-radius: 999px`, `padding: 5px 12px`, `gap: 6px`, `font-size: 13px`, `font-weight: 800`
  (bold enough to read as a heading, not just a bigger badge).
- Icon: same lucide set as §1.2, 13px.
- Count `(N)` and the trailing hairline divider: **unchanged** — same 11px `#4E5663`, same position, same
  `h-px flex-1 bg-black/[0.06]` divider, just now sitting next to a colored pill instead of plain text.

### 2.2 All five groups (4 ranked tiers + the out-of-ramp cannot-assess section)

| Tier (Hebrew, exact field value) | Semantic slot | bg | border | text/icon | icon | contrast |
|---|---|---|---|---|---|---|
| מומלץ מאוד (`very_recommended`) | deepest green — reuses **PASS** exactly | `#E2F2EF` | `#0F6E6333` | `#0B5D52` | `Check` | **6.73:1** |
| מומלץ (`recommended`) | lighter green — **new bridge tone**, see §2.3 | `#E9F5F0` | `#146F5F33` | `#146F5F` | `Check` | **5.42:1** |
| טוב (`good`) | amber — reuses **FLAG** exactly | `#FCEFD6` | `#A8650033` | `#8A5300` | `TriangleAlert` | **5.56:1** |
| לא מומלץ (`not_recommended`) | red — reuses **FAIL** exactly | `#FBE4E1` | `#B3261E33` | `#A02318` | `X` | **6.29:1** |
| לא ניתן להעריך (`cannot_assess`, out-of-ramp) | neutral — reuses **CANNOT_VERIFY** exactly | `#F3F4F2` | `#D8DDD9` | `#4E5663` | `HelpCircle` | **6.71:1** |

This gives the monotonic green→red ramp the owner asked for (מומלץ מאוד = deepest green, לא מומלץ = red),
with לא ניתן להעריך staying visually *off* the ramp (neutral gray, not a "worse than red" step) — which
matches the existing structural rule that this section is a genuine data gap, never folded into לא מומלץ
(`guide-product-table.tsx` comment, line 190).

### 2.3 Why one new color ("מומלץ" / recommended)

Three of the four ranked tiers map 1:1 onto an existing bar-chip state (`very_recommended` = "every bar
PASS" → reuse PASS green; `good` = "flagged on something beyond dose" → reuse FLAG amber; `not_recommended`
= "≥1 bar FAILs" → reuse FAIL red). `recommended` doesn't: it's the **composite** case — passes every bar
except a single flagged `doseAdequacy` — a genuinely intermediate position, not identical to either
neighbor.

I did not invent a new hue for it. `#146F5F` is the **same 166° hue as PASS's `#0B5D52`**, just lighter/less
saturated — it reads as "still green, one notch down," not as an unrelated color. I tried the literal
mid-lightness step first (`#1D8770` on `#E9F5F0`) and it measured **3.95:1 — fails AA**; `#146F5F` on the
same background clears **5.42:1**. I also checked it isn't a look-alike for `gradePalette.B` (the
comparison-page olive-green, `#4C6314`/`#F0F3DF`, hue ≈83°) — 166° vs 83° is a wide hue separation, so
there's no risk of a reader pattern-matching this onto the frozen A–E ramp.

---

## 3. The shared semantic palette (one system, two surfaces)

This is the single source both changes draw from — implement as one exported object, reused by the
badge chip, the tier header, and (already, per the existing code) the gauge zone tints/marker in
`threshold-bar-row.tsx`, so a reader who has learned "amber pill = flag" reads the exact same amber inside
an expanded gauge's flagged zone, with no second amber anywhere on the page.

| Token | bg | border | text/icon | Reused by |
|---|---|---|---|---|
| `pass` / `very_recommended` | `#E2F2EF` | `#0F6E6333` | `#0B5D52` | PASS chip · gauge pass-zone tint · very_recommended tier header |
| `recommended` *(new, tier-only)* | `#E9F5F0` | `#146F5F33` | `#146F5F` | recommended tier header only — no bar-chip equivalent |
| `flag` / `good` | `#FCEFD6` | `#A8650033` | `#8A5300` | FLAG chip · gauge flag-zone tint · good tier header |
| `fail` / `not_recommended` | `#FBE4E1` | `#B3261E33` | `#A02318` | FAIL chip · gauge fail-zone tint · not_recommended tier header |
| `cannot_verify` / `cannot_assess` | `#F3F4F2` | `#D8DDD9` | `#4E5663` | CANNOT_VERIFY chip · gauge fallback marker · cannot_assess tier header |

**Ripple effect Frontend should expect, not be surprised by:** `GUIDE_BAR_TONE` (the object
`bar-state-badge.tsx` already exports and `threshold-bar-row.tsx` already imports for gauge zone
backgrounds and the marker fill) is the same object this spec is repointing. Updating its four values
automatically recolors the gauge zones and marker too — from today's teal/indigo/berry/gray to
green/amber/red/gray. This is **in scope and intentional** (it is exactly the "reuse existing gauge/marker
tokens" instruction, and it closes a gap the original teal/indigo/berry choice created: that palette was
deliberately *non*-semantic specifically to avoid the A–E lookalike risk, which the owner's directive now
explicitly overrides for guides — see the code comment at `bar-state-badge.tsx` lines 7–18 for the
superseded reasoning). Optional low-risk cleanup: rename the exported `GUIDE_BAR_TONE` /
`BAR_STATE_LABELS_HE` constants to something like `GUIDE_VERDICT_TONE`, since the object now drives a
verdict-color system, not just one badge — not required to ship this change, flagging for Frontend's
judgment.

**Delta from `gradePalette` (the frozen A–E comparison-page ramp) — checked, not assumed:**

| | gradePalette (comparison pages) | This spec (guides) | Hue delta |
|---|---|---|---|
| green | A: `#155C3C` (hue ≈152°) | pass: `#0B5D52` (hue ≈166°) | +14° (teal-shifted) |
| amber/gold | C: `#7E5800` (hue ≈45°) | flag: `#8A5300` (hue ≈34°) | −11° (more orange) |
| red | E: `#7A1A1A` (hue ≈0°, desaturated/brownish) | fail: `#A02318` (hue ≈6°, more saturated/vivid) | distinct saturation+lightness, not a repaint |

No hex value in this spec is byte-identical to any `gradePalette` entry. This is offered as due diligence,
not as the primary safety argument — the real reason this doesn't reopen Hard Rule 2 is structural: guides
carry **no numeric score and no A–E letter anywhere** (`GuideProductVM` has no `score`/`grade` field at
all, confirmed in `src/lib/view-models/guide.ts`), and a guide page never renders next to a `/hashvaot`
comparison row, so there is no page where a reader sees both systems side by side to conflate. The task
brief's own framing — "a deliberate shift toward semantic verdict color FOR THE GUIDES ONLY" — is the
owner's pre-authorized exception for this page family; this spec exercises it, it doesn't invent it.

---

## 4. Mocks at 375px (described / ASCII — geometry unchanged except icon slot)

### 4.1 Compact badge row (`GuideProductRow`, always visible)

```
BEFORE (today, live):
  ⬤ עומד בסף    ⬤ עם דגל    ⬤ עומד בסף    ⬤ עומד בסף
  (you cannot tell which bar without memorizing GUIDE_BAR_ORDER)

AFTER:
  ✓ מינון    ! צורה וספיגה    ✓ בדיקת צד שלישי
  ✓ הוגנות מחיר    ✕ בטיחות    ? שקיפות תווית
  (green)    (amber)           (green)
  (green)                      (red)          (gray)
```
Six chips, `flex-wrap`, unchanged wrapping behavior — RTL flex places the first DOM child (icon) at the
chip's right edge, text immediately to its left, matching today's dot+text order exactly (no RTL change).

### 4.2 Tier headers, full stack

```
BEFORE (today, live — all five identical gray):
  מומלץ מאוד (0)
  ──────────────────────────────────
  מומלץ (2)
  ──────────────────────────────────
  טוב (3)
  ──────────────────────────────────
  לא מומלץ (11)
  ──────────────────────────────────
  לא ניתן להעריך (2)

AFTER:
  ┌──────────────────┐
  │ ✓ מומלץ מאוד       │  (0)  ──────────────
  └──────────────────┘   deep green pill
  ┌──────────────┐
  │ ✓ מומלץ         │  (2)  ──────────────
  └──────────────┘   light green pill
  ┌────────────┐
  │ ! טוב         │  (3)  ──────────────
  └────────────┘   amber pill
  ┌────────────────┐
  │ ✕ לא מומלץ       │  (11)  ──────────────
  └────────────────┘   red pill
  ┌──────────────────────┐
  │ ? לא ניתן להעריך      │  (2)
  └──────────────────────┘   neutral gray pill (still visually offset below the ramp, mt-8 unchanged)
```

Count and divider styling are pixel-identical to today; only the label becomes a colored pill instead of
plain gray mono text.

---

## 5. WCAG / RTL risks for Frontend to watch during implementation

1. **`barLabel` goes from optional to required** on `BarStateBadge` — TypeScript will catch any call site
   that omits it, but grep both call sites (`guide-product-row.tsx`, `threshold-bar-row.tsx`) to confirm
   both already pass it (they do, today, for the `aria-label` — the fix is trivial) before treating this as
   done.
2. **Removing the duplicate plain-text `barLabel` span in `ThresholdBarRow`** (§1.1) changes that row's flex
   layout from two children (`justify-between`) to one. Confirm the single remaining chip doesn't
   left/right-collapse oddly under `justify-between` with only one flex child — switch to `justify-start`
   (RTL: chip anchors to the line's start, i.e. visually the right edge) if it does.
3. **Icon import check** — verify `TriangleAlert` and `HelpCircle` resolve in the project's installed
   `lucide-react` version (some versions ship `AlertTriangle`/`CircleHelp` as the current names with the
   old ones as deprecated aliases). Confirm at implementation time; don't assume the name without checking
   `node_modules/lucide-react`'s exports.
4. **Re-run `npm run test:a11y`** (axe, WCAG 2 A/AA incl. 1.4.3 color-contrast) and `npm run test:visual`
   after implementation — this spec's contrast numbers are computed from the hex values, not from the
   actual rendered DOM with real font rendering/anti-aliasing; axe is the ground-truth check before this
   ships. Cite the exit code in the implementation return, don't just cite this spec's table.
5. **`GUIDE_BAR_TONE` is shared with the gauge** (§3 ripple) — after recoloring, re-screenshot at least one
   expanded row per bar type (gauge + ladder anatomy) to confirm the zone tints and the CANNOT_VERIFY
   hollow-ring fallback still read correctly against the new palette; the fallback ring's stroke color
   (`#4E5663`, hardcoded in `ThresholdMarkerFallback`) is unaffected by this change but should be visually
   re-checked against the new zone backgrounds.
6. **RTL is unaffected structurally** — `dir="rtl"` stays on every touched element; only fill/text-color/
   icon swap in place. No directional CSS logic (`marginInlineStart` etc.) needs to change.

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\design\\magnesium_guide_verdict_color_spec_v1.md",
      "sha256": "5646852a97336b09462016893a676582b9c555c30e7cea762c5a8c46def27409 (computed pre-this-edit; the JSON block's own insertion changes the file's bytes after this point — re-hash post-write if a byte-exact artifact hash is required downstream)"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\verdict-spec-mobile\\madrichim-magnesium__mobile.png",
      "sha256": "NOT_COMPUTED_EVIDENCE_ONLY"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\verdict-spec-desktop\\madrichim-magnesium__desktop.png",
      "sha256": "NOT_COMPUTED_EVIDENCE_ONLY"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\contrast.py",
      "sha256": "NOT_COMPUTED_EVIDENCE_ONLY"
    }
  ],
  "counts": {
    "states_specced": 4,
    "tier_groups_specced": 5,
    "chip_call_sites_affected": 2,
    "contrast_pairs_measured": 33,
    "contrast_pairs_below_aa_floor_4_5": 0,
    "new_hue_introduced": 1,
    "reused_gradepalette_hex_values": 0
  },
  "commands_run": [
    { "cmd": "node scripts/vision-in.mjs --route /madrichim/magnesium --base http://localhost:4700 --viewport mobile --selectors ...", "exit_code": 0 },
    { "cmd": "node scripts/vision-in.mjs --route /madrichim/magnesium --base http://localhost:4700 --viewport desktop --selectors ...", "exit_code": 0 },
    { "cmd": "python contrast.py (WCAG relative-luminance contrast calc, 33 pairs)", "exit_code": 0 }
  ],
  "not_done": [
    "No code implementation — this is a D12 spec only, per task scope ('do NOT edit production code')",
    "Desktop capture used vision-in's fixed 1280px viewport, not literally 1440px; confirmed via crop that the guide's single-column layout does not reflow between the two, so this is not a layout-bearing gap",
    "axe/test:visual re-run after implementation is Frontend's responsibility, not run here (no code changed yet to test)",
    "lucide-react icon name resolution (TriangleAlert vs AlertTriangle, HelpCircle vs CircleHelp) not verified against the installed package version — flagged as a Frontend implementation check in §5.3"
  ],
  "acceptance_test": "Spec is accepted if Frontend implements exactly the token table in §3, the chip anatomy in §1.2, and the tier pill in §2.1 without introducing any additional hue, and post-implementation npm run test:a11y reports zero new color-contrast violations on /madrichim/magnesium."
}
```
