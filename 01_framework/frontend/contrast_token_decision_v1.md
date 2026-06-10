# Contrast Token Decision — Editorial Greys + Grade Chips — v1

**Owner:** Design Agent
**Authority:** D12 (design-token governance) + the grade-chip color-contrast a11y finding (this agent's External Data Access lane)
**Status:** Decided — Frontend Agent to implement (token + binding values only; no geometry, no copy, no scoring)
**Evaluated at:** 375px mobile first
**Date:** 2026-06-10
**Tripwire check:** None fires. Reversible token recolor; no score/data/copy move; no category go-live. Decided autonomously.

---

## 0. Summary

Two distinct `color-contrast` (WCAG 1.4.3) finding classes, resolved in one note:

- **(a) Editorial-grey small text.** `--fg3` (#7A817C) and `--fg4` (#AAAAAA) fall below AA 4.5:1
  for small text on every Bari surface. Measured: `--fg3` ≈ 3.99:1 on white (3.43:1 on #EEEEEA);
  `--fg4` ≈ 2.32:1 on white (2.00:1 on #EEEEEA). These classes carry the methodology footer, the
  additive panel meta, and — per `score_confidence_indicators_spec_v1.md` §2/§4 — the new confidence
  expansion label (`.bari-meta`/`--fg3`) and tooltip (`.bari-footnote`/`--fg4`).
- **(b) Grade chip.** axe flags the collapsed-row chip on `/hashvaot/maadanim`. Root cause confirmed
  in code: the `card` variant of `SnackScoreChip` renders the score number **and** grade letter in
  `gradePalette[grade].accent` on `…bg`, not in the palette's purpose-built `text` value. Three
  grades fail AA and two fail even the 3:1 large-text floor at the chip's small label size
  (C accent 3.47:1, D accent 3.28:1, B accent 4.19:1).

**Decision: Option C** for the greys; **bind-to-`text`** recolor for the chips. Both stay inside the
existing register and the existing grade ramp.

---

## 1. Chosen option — C (usage-split tokens)

**Why C, not A or B.** Bari's calm editorial register is a real design asset — flattening every
quiet grey to one dark "essential" value (Option A) would coarsen the methodology footer and the
confidence tooltip, the exact places the quiet was deliberate. But a blanket waiver (Option B) is
indefensible: the confidence layer is *informational* text a user is meant to read, and the
methodology footer is the page's evidentiary backbone — neither is decorative. So we split by
*function*, not by aesthetic preference: any grey carrying **readable text** gets an AA-compliant
value; the only thing allowed to stay quieter is genuinely **non-essential, non-load-bearing**
ornament. In practice almost everything currently on `--fg3`/`--fg4` is readable text, so the
honest outcome of Option C is: **both editorial greys get darkened to clear AA**, and we keep a
single explicitly-scoped decorative token in reserve rather than waiving real content. This gives
the defensible a11y floor without a single piece of meaningful text dropping below 4.5:1.

The chips need no waiver and no new value at all — see §2.2.

---

## 2. Exact values

### 2.1 Editorial-grey tokens (Option C)

| Token | Old | New | Role after split |
|---|---|---|---|
| `--fg3` | `#7A817C` | **`#5E6560`** | AA small-text grey — meta, captions, confidence **label** (`.bari-meta`) |
| `--fg4` | `#AAAAAA` | **`#666C67`** | AA small-text faint — methodology footnote, confidence **tooltip** (`.bari-footnote`) |
| `--fg-decorative` | — (new) | **`#9A9F9B`** | **Decorative only.** Non-text ornament / disabled-state hints. Never on readable copy. Not AA — allowed because it carries no information. |

Computed ratios (small-text AA gate = 4.5:1):

**`--fg3` = `#5E6560`** — white 5.99 · #F9F9F9 5.69 · #FAFAF8 5.73 · #F7F7F2 5.57 · #EEEEEA 5.15. All ≥4.5. PASS.
**`--fg4` = `#666C67`** — white 5.38 · #F9F9F9 5.13 · #FAFAF8 5.17 · #F7F7F2 5.01 · #EEEEEA 4.62. All ≥4.5. PASS.

Register preserved: `--fg4` stays measurably quieter than `--fg3` (luminance 0.145 vs 0.125), and
both stay well below body ink `--fg2` (#4E5663) — the three-step hierarchy (body → meta → footnote)
is intact, just lifted above the legibility floor. `--fg-decorative` (#9A9F9B) holds the old quiet
tone for anything that is truly ornament.

> Note: `--fg4`'s prose comment in `colors_and_type.css` ("methodology footnotes") and the frozen
> methodology spec say `#AAAAAA`. That frozen value is **superseded for legibility** by this
> decision — the methodology footer keeps its 12px size, no card, no border, no heading; only the
> hex darkens to clear AA. This is a contrast fix within the same visual register, not a redesign of
> the methodology block.

### 2.2 Grade chips — recolor by binding, no ramp change

The `gradePalette` already carries a darker, AA-compliant `text` value per grade. The fix is to make
the chip glyphs use it instead of `accent`. **No palette hex changes; ramp structure unchanged.**

| Grade | Glyph color NOW (`accent`) on `bg` | Glyph color FIXED (`text`) on `bg` |
|---|---|---|
| A | `#1E7A4F` → 4.69:1 (borderline) | **`#155C3C` → 7.06:1** PASS |
| B | `#5F7D17` → 4.19:1 FAIL | **`#4C6314` → 5.99:1** PASS |
| C | `#A87A0C` → 3.47:1 FAIL | **`#7E5800` → 5.76:1** PASS |
| D | `#D85C1C` → 3.28:1 FAIL | **`#9A4012` → 5.75:1** PASS |
| E | `#A52121` → 6.00:1 (passes) | **`#7A1A1A` → 8.56:1** PASS |

- **Monotonic good→poor preserved.** Hue order A green → B olive → C gold → D orange → E red is
  unchanged on every channel (bg, border, the 4px accent bar, and the glyph).
- **Ramp structure unchanged.** Five grades, one hue family each, same chip geometry. Values only.
- **The grade hue is still loud where it should be.** The 4px `accent` side-bar (`borderInlineStart`)
  keeps the bright `accent` hue — it is a decorative bar, not text, so its contrast is not an AA
  text gate. The grade color therefore still reads instantly; only the *small glyph text* moves to
  the darker same-family `text` value. Legibility is gained without flattening the color that earns
  the chip.

This is a recolor within the approved A→E ramp (permitted under Hard Rule 1). It is **not** a change
to the ramp's structure, so it is not an exception request.

---

## 3. Affected components / pages

| Surface | Class / token touched | Finding class |
|---|---|---|
| Methodology footer | `.bari-footnote` / `--fg4` | (a) |
| Additive / ingredient meta panel | `.bari-meta` / `--fg3` | (a) |
| Confidence **expansion label** (confidence-indicator spec §4) | `.bari-meta` / `--fg3` | (a) |
| Confidence **expansion tooltip** (confidence-indicator spec §4) | `.bari-footnote` / `--fg4` | (a) |
| Confidence collapsed-row grey **dot** `•` (spec §2) | `--fg3` | (a) — darkens with token; geometry unchanged |
| Grade chip — `card` variant (collapsed rows) | `SnackScoreChip` glyph binding `accent`→`text` | (b) |
| Routes: `/`, `/hashvaot/maadanim`, `/hashvaot/hummus` (and every comparison route using the chip) | both | (a)+(b) |

The chip `comparison` and `hero` variants already render glyphs in `colors.text` — they are
**already compliant** and must not be changed.

---

## 4. Implementation instruction for the Frontend Agent

In `bari-web/colors_and_type.css`: set `--fg3: #5E6560;` and `--fg4: #666C67;`, and add a new
`--fg-decorative: #9A9F9B;` (decorative/non-text only). In
`bari-web/src/lib/design/bari-comparison-tokens.ts` the `gradePalette` hexes are **unchanged**; in
`bari-web/src/components/snack/snack-score-chip.tsx` `card` variant, change the two glyph `style={{
color: colors.accent }}` bindings (score span + grade-letter span) to `colors.text` — the 4px
`borderInlineStart` accent bar stays `colors.accent`. **Do not change confidence-marker geometry
(dotted ring, 6px dot, 72px row, chip footprint), do not add any new hue/color axis, do not change
gradePalette mapping/logic (values are untouched — this is a binding change only), and do not touch
scoring, data, or copy.** After the change, re-run `npm run test:a11y` on `/`, `/hashvaot/maadanim`,
`/hashvaot/hummus` — `color-contrast` must clear on all three.

---

## 5. Verdict

**PASS WITH FIXES.** The decision and exact values are approved (D12). The page is not yet compliant
on the live build — it becomes compliant once the Frontend Agent applies the three token values and
the one chip binding change above and `test:a11y` clears `color-contrast` on the three routes. No
geometry, hue-axis, grade-logic, scoring, data, or copy change is permitted in this implementation.
