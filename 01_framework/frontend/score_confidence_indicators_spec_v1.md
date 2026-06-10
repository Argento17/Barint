# Score Confidence / Data-Completeness Indicators — Visual Spec v1

**Owner:** Design Agent
**Status:** Approved spec (D12 authority) — required before Frontend Agent builds (D11/Hard Rule 8)
**Scope:** Consumer-facing confidence layer on product cards (collapsed row + inline expansion)
**Evaluated at:** 375px mobile first
**Date:** 2026-06-10

> **Amendment 2026-06-10 (TASK-226, owner-approved):** the achromatic marker / null-pill
> grey `--fg3` is recorded as **`#5E6560`** (darker, higher-contrast), superseding the
> original `#7A817C` to align with the concurrent contrast-token decision
> (`contrast_token_decision_v1.md`) and clear the WCAG 1.4.3 finding. All `#7A817C`
> references below are updated accordingly; `--fg3` everywhere in this spec = `#5E6560`.

---

## 0. Purpose & Boundary

Make *how much to lean on a score* visible at a glance, without ever showing a normal-looking
score on top of missing essential data — and without weakening consumer confidence in the scores
that *are* fully backed.

This layer sits **around** the gradePalette score chip. It does **not** recolor, restyle, or
replace the chip. The chip remains the only color axis (Hard Rule 1). Confidence is encoded on a
**separate, non-hue channel**: a small dotted/text caveat marker that carries no grade hue.

**Relationship to existing model.** The View Model already exposes 3 confidence states
(`verified` / `partial` / `insufficient`, `comparison_view_model_v1.md`). These 7 consumer states
are a **display refinement that maps onto those 3** — they do not add a new VM field. The mapping
is defined in §6. Nothing here changes scoring, the chip, or the 3-state VM contract.

---

## 1. The Two Display Tiers (collapsed vs. expansion)

The collapsed 72px row is the 15–20-second comprehension surface. It must not become a dashboard
of caveats. Therefore:

- **Collapsed row carries ONE bit of confidence**, and only when it matters: *is this a fully-backed
  score, or not?* If not fully backed, a single quiet dotted marker rides next to the chip. The
  *type* of gap is never shown on the collapsed row.
- **The expansion carries the full story** — the specific Hebrew confidence label + tooltip
  sentence, in the existing confidence row at the bottom of the expansion (no new section, no
  heading — Gen 1 expansion rule preserved).

This keeps the collapsed shelf calm and honest: a chip with a dotted ring reads as "real score,
read the note"; a chip with no marker reads as "fully backed." State 7 is the only state that
suppresses the chip outright.

---

## 2. The Confidence Marker — non-hue channel (Hard Rule 1 compliance)

The confidence marker must never compete with the grade chip's color. It therefore uses **zero
grade hue** and lives on channels the grade ramp does not use:

| Channel | Grade chip uses it? | Confidence marker uses it? |
|---|---|---|
| Hue (A green → E red) | Yes — this is the grade axis | **Never.** Marker is achromatic. |
| Fill / solid background | Yes — tinted `--grade-*-bg` | No — marker has no fill |
| Border style | No — chip border is a solid hairline | **Yes — dotted/dashed `--hairline` (achromatic)** |
| Glyph / icon | No | **Yes — a single dotted-ring or small dot glyph** |
| Text label | Yes — `72 · B · טוב` | Yes — but only inside the expansion, never on the row |

**Collapsed-row marker treatment (states 2–6):**
- A **dotted ring** drawn *outside* the existing chip, 1px, color `--hairline` (`rgba(17,19,24,0.08)`)
  — achromatic, no grade hue. Ring radius follows the chip's `--radius-lg`.
- Plus a single **dot glyph** (`•`, 6px) in `--fg3` (`#5E6560`) sitting in the inline-start gutter
  of the chip (RTL: to the *right* of the chip, before the name). The dot is the tap target that
  expands the row; it is also a visual "there is a note here" affordance.
- No text on the row. No second color. The chip's own grade color is untouched.

Because the only difference between a fully-backed chip and a caveated chip is *dotted ring +
grey dot vs. nothing*, the eye reads confidence as texture, not as a second color scale. A
color-blind user gets the same signal (dotted vs. solid is a shape channel, axe-safe).

**Expansion marker treatment (all states):** the existing confidence row at the bottom of the
expansion renders the Hebrew label (§4 column) in `.bari-footnote` style — `0.625rem` (10px) /
`--fg4` (`#AAAAAA`) for the supporting tooltip sentence, and `.bari-meta` (`0.8125rem` / `--fg3`)
for the badge label itself so it is legible without shouting. No card, no border, no heading.

---

## 3. State Table (7 states)

| # | State | Data condition (when it fires) | Score chip behavior | Collapsed marker | Hebrew badge label | Hebrew tooltip copy |
|---|---|---|---|---|---|---|
| 1 | Complete data | Ingredient list **and** nutrition panel both present and parsed; extraction high-confidence | Shown normally (grade chip, full color) | **None** (solid, no dot) | מבוסס על נתונים מלאים | הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים. |
| 2 | Partial data | One non-essential field missing (e.g. fiber absent) but both core sources present | Shown normally with dotted marker | Dotted ring + grey dot | מבוסס על נתונים חלקיים | הציון מבוסס על נתונים חלקיים. חלק מהפרטים לא היו זמינים. |
| 3 | Missing ingredient list | Nutrition panel present, ingredient list absent | Shown with caveat (chip + dotted marker) | Dotted ring + grey dot | חסרים נתוני רכיבים | רשימת הרכיבים לא הייתה זמינה — הציון מבוסס על נתוני התזונה בלבד. |
| 4 | Thin nutrition panel | Nutrition panel **present but thin/incomplete** — one or more non-fatal nutrition fields missing (panel **not** absent; ≥1 macro driver still present). A **fully absent** panel routes to State 7, not here. | Shown with caveat (chip + dotted marker) | Dotted ring + grey dot | חסרים נתוני תזונה | חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים. |
| 5 | Inferred category | Product scored under a category assigned by inference, not confirmed labeling | Shown with caveat (chip + dotted marker) | Dotted ring + grey dot | קטגוריה משוערת | הקטגוריה זוהתה באופן משוער. הציון עשוי להתעדכן כשיתווספו נתונים. |
| 6 | Low-confidence extraction | Both sources present but OCR/parse confidence below threshold | Shown with caveat (chip + dotted marker) | Dotted ring + grey dot | נתונים בבדיקה | חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים. |
| 7 | Not enough data to score safely | Essential data missing such that no defensible grade exists | **Suppressed — no chip.** Renders null-state pill instead (§5) | Null pill replaces chip | טרם נוקד | המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים. |

**Why states 3, 4, 6 visibly differ from state 1:** state 1 has a *solid* chip, no ring, no dot.
States 3/4/6 carry the dotted ring + grey dot on the row, and on expansion they spell out exactly
which source is missing. A fully-backed score is therefore never mistaken for a partially-backed
one — the difference is visible at row level (texture) and explicit at expansion level (text).

**Copy compliance:** no state says "bad data," "unreliable," "low quality," or blames the product.
States 5 and 6 carry the owner-approved forward-looking line "הציון עשוי להתעדכן כשיתווספו נתונים."
State 7 uses "טרם נוקד" (not yet scored) — a neutral, non-apologetic register consistent with the
Uncertainty Principle in `explainability_v1.md` (§6.1: "uncertainty is information, not failure").

---

## 4. Badge Visual Spec (within frozen Gen 1 constraints)

| Property | Collapsed row | Expansion confidence row |
|---|---|---|
| Where | Inline-start gutter of chip (RTL: right of chip) | Bottom of expansion, existing confidence row |
| What renders | Dotted ring on chip + 6px grey dot `•` | Badge label + one tooltip sentence |
| Label type | none | `.bari-meta` — `0.8125rem` / `--fg3` (`#5E6560`) |
| Tooltip type | none | `.bari-footnote` — `0.625rem` (10px) / `--fg4` (`#AAAAAA`) |
| Color | `--hairline` ring + `--fg3` dot — **achromatic** | text only — no fill, no border |
| Ring | 1px dotted, `--radius-lg`, `--hairline` | n/a |
| Card / border / heading | none (Gen 1: expansion has no headings) | none |
| Tap behavior | dot + chip expand the row | "סגור" closes (existing) |
| Tooltip trigger (desktop) | hover/focus on dot shows label as title | label always visible in expansion |

Tooltip on the collapsed row (desktop hover) shows only the **badge label** (column 6), not the
full sentence — the full sentence lives in the expansion. On mobile there is no hover; the dot is a
tap affordance that opens the expansion where the full sentence sits. This keeps the row honest
without a hover-only dependency (mobile-first).

**Distinct-from-grade guarantee:** the marker is dotted + achromatic + shape-based. The grade chip
is solid + hued + fill-based. The two never share a channel, so the confidence layer can never be
read as a second grade scale.

---

## 5. Suppressed-Score Treatment (State 7)

State 7 must NOT render anything that looks like a real numeric/grade chip.

**What replaces the chip:** a **null-state pill** in the chip's footprint:
- Same geometry as the chip (same width band, same `--radius-lg`, same 72px row height) so the row
  stays structurally a product row — but it is unmistakably *not a score*.
- Background `#EEEEEA` (the existing `insufficient` null-state surface from the VM mapping), no
  grade hue, no number, no grade letter.
- Content: the word **`טרם נוקד`** in `.bari-meta` `--fg3`, centered. No digits anywhere in the pill.
- Border: `rgba(17,19,24,0.07)` solid hairline (the VM `insufficient` border) — **not** dotted,
  because there is no score to caveat; this is a clean null, not a hedged score.

**How the row still reads as a real product:**
- 56px product image renders normally.
- Product name renders normally in `.bari-h3`.
- The insight line slot renders a neutral, non-apologetic line (CE-authored), e.g.
  "המוצר נמצא על המדף — טרם התקבלו נתונים לניתוח." — same `.bari-meta` treatment as any insight line.
- Expansion still opens (Gen 1 rule preserved) and shows the confidence row with the state-7 label +
  tooltip, no nutrition, no ingredients.

The product is present, named, pictured, and explained — it simply carries "not yet scored" where a
grade would be. Nothing on the row mimics a score.

---

## 6. Mapping to the 3-state VM (no VM change required for the common path)

| 7-state (this spec) | Existing VM `confidence` | Chip | Notes |
|---|---|---|---|
| 1 Complete | `verified` | grade chip, solid | — |
| 2 Partial | `partial` | grade chip + dotted | — |
| 3 Missing ingredients | `partial` | grade chip + dotted | label specializes the partial copy |
| 4 Thin nutrition panel | `partial` | grade chip + dotted | **only** for a thin/incomplete (but present) panel — label specializes the partial copy |
| 4a Fully absent nutrition panel | `insufficient` | suppressed → null pill | a **totally absent** panel is NOT partial — it routes to State 7 / `insufficient` (suppress). See note below. |
| 5 Inferred category | `partial` | grade chip + dotted | **needs a data flag** (see §8) |
| 6 Low-confidence extraction | `partial` | grade chip + dotted | **needs a data flag** (see §8) |
| 7 Not enough data | `insufficient` | suppressed → null pill | maps to existing `insufficient` null state |

States 1, 2, 7 map cleanly onto existing VM states with no engine work. States 3–6 are all
`partial` at the VM level but need a **display sub-reason** to pick the right Hebrew label. The
cleanest path is a pre-rendered string the backend already owns (`confidence_label_he`) plus a small
enum sub-reason — see open questions §8.

**Threshold ownership note (not a visual-design decision).** The line that splits State 4 (thin
panel → `partial`, caveat) from State 7 (fully absent panel → `insufficient`, suppress) is a
**threshold policy owned by Nutrition + Product**, resolved in
`03_operations/bsip2/proto_v0/reports/state7_suppression_threshold_policy_v1.md` (rule R2:
"NOT panel — no macro driver at all → SUPPRESS"). Design does not set this line; it designs the UX
of both sides of it. A fully absent nutrition panel (no macro driver present) is therefore never a
`partial` caveat — it has no defensible grade and routes to State 7. This spec must not imply
absent-panel = partial anywhere.

---

## 7. Mobile-First Note (375px)

At 375px the collapsed row budget is 72px (80px max), 56px image, name + insight line stacked in the
remaining inline space. The confidence layer adds:

- **Dotted ring:** drawn on the chip's existing footprint — **0 extra width**. It is a border style,
  not a new box.
- **Grey dot `•` (6px) + 4px gap:** ~10px in the chip gutter. The chip already sits at the inline-end
  of the row (RTL: leftmost); the dot sits between chip and name, inside existing inter-element
  padding. It does **not** push the insight line, which lives on its own row below the name.
- **RTL:** in RTL the chip is at the inline-end (visually left), name + insight at inline-start
  (right). The dot renders on the chip's inline-start edge (its right side) — between chip and name —
  so reading order is name → dot → chip, matching RTL flow. The dotted ring is symmetric so it is
  direction-agnostic.
- **State 7 null pill:** occupies the same footprint as the chip — **no layout shift** vs. a normal
  row, so a shelf mixing scored and not-yet-scored products has a stable grid (no CLS).

Confirmed: badge fits the 72px row, does not push the insight line, does not break RTL.

---

## 8. Open Questions (do not block — surfaced for after-the-fact review)

**To Nutrition / Product (data-condition thresholds — may imply engine/data work):**
1. States 5 (inferred category) and 6 (low-confidence extraction) are not distinguishable in the
   current 3-state VM — both collapse to `partial`. Picking their specific Hebrew label needs either
   (a) a backend `confidence_sub_reason` enum (`missing_ingredients | missing_nutrition |
   inferred_category | low_extraction`) or (b) the backend pre-rendering the right
   `confidence_label_he` string per product. Recommend (b) — keeps UI dumb, matches the existing
   "backend renders Hebrew" contract. **This is a data-feed change, not a scoring change.**
2. **State 7 threshold = a scoring-engine boundary.** "Not enough data to score safely" is the line
   between `partial` (show a caveated score) and `insufficient` (suppress). That threshold is owned
   by Nutrition/Product, not Design. This spec designs the UX of both sides of the line; it does not
   set the line. **Flagged:** if tightening state 7 reclassifies any currently-displayed product, that
   is a published-score-visibility change and routes to Nutrition/Product (potential tripwire #1).

**To Frontend (feasibility):**
3. Dotted-ring-outside-chip: confirm it can be drawn as an `outline`/pseudo-element without enlarging
   the chip's layout box (must be 0 extra width at 375px).
4. Confirm the null-state pill reuses the existing `insufficient` chip footprint component so state-7
   rows cause no CLS against scored rows.

---

## 9. Product-Case Examples (10 cards across all 7 states)

Categories drawn from shelves already in play (milk, bread, snacks, spreads, cereal). Scores are
illustrative for layout, not published values.

| # | Product (illustrative) | State | Why it lands there | Card renders | Tooltip (expansion) |
|---|---|---|---|---|---|
| 1 | תנובה חלב 3% טבעי | 1 Complete | Ingredient list + nutrition panel both present, clean parse | Grade chip `85 · A · מצוין`, solid, no dot. Insight line below name. | הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים. |
| 2 | אנג'ל לחם מחמצת מלא | 1 Complete | Both sources present | Grade chip `74 · B · טוב`, solid, no marker | הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים. |
| 3 | חטיף תמרים ואגוזים (פרטי) | 2 Partial | Both core sources present, fiber value absent | Grade chip `70 · B · טוב` + dotted ring + grey dot | הציון מבוסס על נתונים חלקיים. חלק מהפרטים לא היו זמינים. |
| 4 | ממרח טחינה גולמית (מותג קטן) | 3 Missing ingredient list | Nutrition panel on jar, ingredient list not published online | Grade chip `68 · C · סביר` + dotted marker | רשימת הרכיבים לא הייתה זמינה — הציון מבוסס על נתוני התזונה בלבד. |
| 5 | קוטג' 5% (מותג חדש) | 4 Thin nutrition panel | Nutrition panel present but **thin** — energy + protein + fat listed, but sugars/sodium fields blank on the published table. Panel is present (≥1 macro driver), just incomplete — so it caveats, not suppresses. (A *fully* absent table would be State 7.) | Grade chip `71 · B · טוב` + dotted marker | חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים. |
| 6 | דגני בוקר מצופים (יבואן) | 5 Inferred category | Category assigned by inference (cereal vs. snack ambiguous), not confirmed labeling | Grade chip `52 · D · חלש` + dotted marker | הקטגוריה זוהתה באופן משוער. הציון עשוי להתעדכן כשיתווספו נתונים. |
| 7 | לחם פרוס (תצלום מדף מטושטש) | 6 Low-confidence extraction | Both sources present but OCR confidence below threshold — **this is the "updates when data is added" case** | Grade chip `64 · C · סביר` + dotted marker | חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים. |
| 8 | חטיף חלבון (מותג חו"ל) | 7 Not enough data | Neither a parseable ingredient list nor nutrition panel available in Hebrew label | **No chip.** Null pill `טרם נוקד` + neutral insight line | המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים. |
| 9 | ממרח שוקולד (מהדורה מוגבלת) | 7 Not enough data | Limited-edition SKU, no published label data | **No chip.** Null pill `טרם נוקד`, image + name render normally | המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים. |
| 10 | קורנפלקס קלאסי | 2 Partial | Both sources present, one secondary nutrient field absent | Grade chip `58 · D · חלש` + dotted ring + grey dot | הציון מבוסס על נתונים חלקיים. חלק מהפרטים לא היו זמינים. |

Case 7 is the explicit "score updates when data is added" scenario (הציון עשוי להתעדכן). Cases 8–9
demonstrate two different products both suppressing the chip while still reading as real products on
the shelf.

---

## 10. Compliance Checklist (against frozen Gen 1 + Hard Rules)

| Constraint | Status |
|---|---|
| Hard Rule 1 — no second color axis vs. gradePalette | PASS — marker is achromatic, dotted, shape-based |
| Score chip geometry unchanged (only ring added outside box) | PASS |
| No framework terms / NOVA / dimension scores in copy | PASS |
| Expansion has no headings | PASS — confidence row reused, no new heading |
| Methodology untouched (12px / `#AAAAAA`) | PASS — not modified |
| Collapsed row 72px / 56px image / insight line below name | PASS — 0 extra width, insight line not pushed |
| Inline expansion only (no modal/sheet) | PASS |
| Copy never accuses product / never reads as error | PASS — calm, forward-looking register |
| State 7 renders no score-looking chip | PASS — null pill, no digits, no grade letter |
| States 3/4/6 visibly differ from state 1 | PASS — dotted row marker + explicit expansion text |
| Evaluated at 375px first | PASS — §7 |
