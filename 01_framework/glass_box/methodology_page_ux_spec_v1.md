---
document: methodology_page_ux_spec_v1
task: TASK-181P
status: APPROVED
created_at: 2026-06-05
author: design-agent
blocks: [TASK-181Q]
---

# Glass Box — Methodology Page UX Spec v1

**Covers:**
1. Methodology page structure and visual treatment (5 sections from TASK-181O)
2. AdditivePanel targeted polish notes

**Canonical reference:** מעדנים comparison page.
**Generation constraint:** Gen 1 only. All token values from `bari-comparison-tokens.ts`.
**Primary viewport:** 375px mobile. Desktop is secondary.

---

## Part 1 — Methodology Page UX Spec

### Route

`/hashvaot` is the comparison section. The methodology page is a standalone public page, not a comparison. Looking at the existing structure — `/blog/`, `/research/`, `/categories/` — the closest match for a methodology page is `/research/` (already contains a transparency-facing entry: `bread-transparency-shufersal`). The Glass Box methodology page routes to:

```
/research/glass-box
```

This keeps it next to the transparency canon in site structure. If the Frontend Agent identifies a reason to use a different parent (e.g., a new `/methodology/` segment), it must document the deviation from this recommendation before building.

---

### Page Structure

This is not a comparison page. It does not use the 4-section comparison template (CategoryHero → CategoryPrologue → ProductTable → MethodologyFooter). It is a standalone editorial page with its own 5-section structure. The Gen 1 constraint on 4 sections applies only to comparison pages.

The page is RTL (Hebrew) throughout. `dir="rtl"` on the page root.

---

### Section 1 — Lead

**Visual weight:** Highest on the page. This is the single most prominent surface.

| Property | Value | Token / source |
|---|---|---|
| Page-level eyebrow | `font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80` | `BARI_COMPARISON_TOKENS.typography.sectionEyebrow` |
| Lead headline (`<h1>`) | `text-[1.35rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318]` | Inherits from `CategoryHero` h1 spec |
| Body lines (1–2 sentences) | `text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]` | `CategoryPrologue` sentence style |
| Section outer padding | `px-4 pt-5 pb-4` | Tailwind — no token needed |

**Mobile geometry:** The lead section (eyebrow + h1 + 2 body lines) must not exceed 180px on the primary viewport. This is a reading page, not a comparison page — there is no pre-table ceiling to manage, but compactness at the top ensures the second section begins in the viewport.

**No image.** No product image, no score chip. The lead stands on text only. The eyebrow text is drawn from the page's editorial category (e.g., "שיטה · עדכון").

---

### Section 2 — מה השתנה ולמה

**Visual weight:** Body text register. No elevated treatment.

| Property | Value | Token / source |
|---|---|---|
| Section label (≤120 words runs as flowing text — no heading) | None. No `<h2>` or `<h3>`. | Gen 1 methodology rule: no headings |
| Body text | `text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]` | `CategoryPrologue` sentence style |
| Top separator | `border-t border-[rgba(17,19,24,0.06)]` followed by `pt-4` | Same border token used in `ExpansionSection` technical divider |
| Bottom padding | `pb-4` | Tailwind |

**No section heading is rendered.** The separation comes from the border-t divider and the paragraph rhythm alone. This is consistent with the Gen 1 ruling that prohibits section headings inside the methodology register.

The ≤120-word constraint (from 181O) means the text fits in 3–5 body lines on mobile at 13px/1.55. No overflow treatment needed.

---

### Section 3 — מה ברי בודקת עכשיו (D-dimension items)

**Visual weight:** Equal to the body. The dimensions are explanatory prose, not a feature list.

**Decision: inline paragraphs with a bold lead phrase.**

The three options were:
- Inline paragraphs — minimal chrome, framework invisible
- Icon+text rows — adds visual scent, risks feature-list reading
- Compact card grid — Gen 0 risk, hard to justify without score chrome

The correct choice is **inline paragraphs with a bold lead phrase** — not card grid, not icon rows. The rationale is the Bari editorial principle of framework invisibility: the methodology page must not look like a product feature page. Four icon+text rows would signal "here are Bari's four features" — the exact pattern that makes Bari look like analytics software. A card grid carries Gen 0 risk even without score chrome (the card shape itself reads as a product card). Inline paragraphs with a bold lead phrase ("**מה כתוב על התווית**") carry meaning via the text, not the component. The bold lead is not a heading — it is typographic emphasis within the paragraph flow.

| Property | Value |
|---|---|
| Container | A single `<div>` with `space-y-4` between D-items. No wrapping card, no border, no background. |
| Bold lead phrase | `font-semibold text-[14px] text-[#2F3531]` — inline, not a separate element |
| Body text | `text-[13px] leading-[1.55] text-[#3E444A]` |
| Top separator (from section 2) | `border-t border-[rgba(17,19,24,0.06)] pt-4` |
| Bottom padding | `pb-3` |

Each D-dimension item is a single `<p>` element where the lead phrase is a `<strong>` span with the above bold style, followed by the body sentence. No list element (`<ul>`/`<li>`), no `<dt>`/`<dd>`, no card wrapper. Four items, four paragraphs.

**Framework term guard:** The dimension identifiers D3/D4/D5/D6 must not appear in any consumer-facing string. The bold lead phrases ("מה כתוב על התווית", "כמה בטוחים אנחנו", "אילו תוספים נמצאים ומה ידוע עליהם", "אות עיבוד — בהתאם לביטחון") are the consumer-facing labels already authored in `methodology_glass_box_page_v1.md`. The D-number identifiers are for internal reference only.

---

### Section 4 — על הציונים שזעו

**Visual weight:** Lower than section 3. This is a contextualizing footnote-register paragraph, not a new claim.

| Property | Value |
|---|---|
| Body text | `text-[13px] leading-[1.55] text-[#6A716E]` — one shade lighter than the main body color, signaling reduced register |
| Top separator | `border-t border-[rgba(17,19,24,0.06)] pt-4` |
| Bottom padding | `pb-3` |
| Link to hummus page | Inline `<a>` with `text-[#1F8F6A] underline-offset-2 underline` — no button, no arrow, no chip |
| Link to maadanim page | Same treatment as hummus link |

The links anchor to `/hashvaot/hummus` and `/hashvaot/maadanim` respectively. They are inline within the prose sentence, not rendered as separate rows, buttons, or callout cards. This preserves the footnote register and avoids implying these links are navigation items.

**No bold text in this section.** The light color (`#6A716E`) handles the reduced weight without needing font-weight contrast.

---

### Section 5 — תאריך (date/version stamp)

**Visual weight:** Lowest on the page. Methodology register. Matches the comparison page MethodologyFooter.

| Property | Value | Token |
|---|---|---|
| Font size | `11px` | Near `BARI_COMPARISON_TOKENS.methodology.fontSize` (12px); see note below |
| Color | `#AAAAAA` | `BARI_COMPARISON_TOKENS.methodology.color` |
| Leading | `leading-relaxed` | Matches `MethodologyFooter` `<p>` style |
| Padding | `px-4 pt-3 pb-6` | Tailwind — no token needed |
| Heading | None | Methodology register: no heading |
| Card/border | None | No border, no background |

**Note on font size:** The `methodology.fontSize` token is `12px`. The date stamp renders at `11px` — one pixel smaller — to signal that it is lower register than even the methodology text. This is a local component decision, not a token change. The token is `12px` and is consumed for methodology body text; the date line uses Tailwind `text-[11px]` directly, consistent with how `MethodologyFooter` uses `text-[11px]` in practice.

**Format:** "עדכון אחרון: [date]" — single line, date in day.month.year format (e.g. "5.6.2026").

---

### Full Page Hierarchy Summary

```
/research/glass-box
  dir="rtl"
  max-w-[680px] mx-auto   (desktop cap — same reading width as blog pages)

  Section 1: Lead
    px-4 pt-5 pb-4
    eyebrow (sectionEyebrow token)
    <h1> (CategoryHero h1 spec)
    1–2 body lines (CategoryPrologue sentence style)

  Section 2: מה השתנה ולמה
    border-t + px-4 pt-4 pb-4
    flowing body paragraphs (CategoryPrologue sentence style)
    no heading

  Section 3: מה ברי בודקת עכשיו
    border-t + px-4 pt-4 pb-3
    4 × inline paragraphs, bold lead phrase + body sentence
    no card, no icon, no list

  Section 4: על הציונים שזעו
    border-t + px-4 pt-4 pb-3
    light-register body paragraph (#6A716E)
    inline links to hummus + maadanim pages

  Section 5: תאריך
    px-4 pt-3 pb-6
    11px / #AAAAAA / no heading / no border
```

---

### Mobile Geometry

This page has no comparison table, no hero image, no product rows. The mobile geometry checklist governs comparison pages; it does not apply here. However, the following mobile constraints hold:

| Constraint | Value | Rationale |
|---|---|---|
| Maximum content width (mobile) | 375px — full width | No side margins beyond `px-4` |
| Section border-t separators | `rgba(17,19,24,0.06)` — same as `ExpansionSection` divider | Visual consistency with comparison pages |
| Tap targets (links in section 4) | Minimum 44px tall touch target | Same as AdditivePanel "עוד" tap target |
| No sticky elements | None | The page has no filter, no FAB, no comparison-specific sticky chrome |
| Scroll behavior | Native | No custom scroll behavior — the page is linear reading content |

**Desktop:** At `sm:` breakpoint and above, add `max-w-[680px] mx-auto` to center the reading column. All section padding switches to `px-6`. No layout change beyond column centering — no two-column layout, no sidebar.

---

### Link Surface — How Comparison Pages Link Here

TASK-181N established that the comparison pages (hummus, maadanim) will carry a dated methodology note at the bottom — in the methodology footer register, not in a card or callout. The link from those pages to `/research/glass-box` renders as follows:

**Treatment:** An inline link appended to the last methodology sentence on each comparison page. Not a separate row. Not a "read more" card. Not a tooltip.

**Spec:**

```
Render location: Inside the MethodologyFooter <p> on the hummus and maadanim pages,
as the final sentence of the per-page note.

Link text: "פירוט המתודולוגיה"
Link target: /research/glass-box
Link style: text-[#1F8F6A] underline underline-offset-2
            (the comparison page's brand green, inline within 11px/#AAAAAA footer text)
Font size: Inherits from the MethodologyFooter paragraph — 11px
```

This is the lowest-visibility surface: an 11px inline link within the methodology footer. It is discoverable only by users who read the footer. That is correct behavior — the methodology page is for curious users who want more, not a feature being pushed at every consumer.

**No badge, no arrow, no "learn more" button.** Those patterns introduce a hierarchy that the footer does not have.

---

### New Design Tokens Required

No new tokens are required. This spec uses only existing tokens and Tailwind utilities. The page does not introduce a new component type, a new color, or a new typographic scale.

The `methodology.color` token (`#AAAAAA`) and `methodology.fontSize` (`12px`) tokens are both available and consumed in section 5. The `sectionEyebrow` typography token is available for section 1. The `CategoryPrologue` sentence style (`text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]`) is a Tailwind class string, not a named token — applied inline in this page component, consistent with how `CategoryPrologue` itself applies it.

---

## Part 2 — AdditivePanel Polish Notes

### Audit Findings

The AdditivePanel (`bari-web/src/components/shared/AdditivePanel.tsx`) was read in full. The component is structurally sound: inline-only, no modal, Gen 1 compliant, DEC-006 compliant. The following three friction points were identified.

---

### Polish Item 1 — TierChip label text is too small at 11px for Hebrew at 375px

**Current state:** `TierChip` renders at `fontSize: "11px"`, `fontWeight: 600`. Hebrew characters at 11px bold on a tinted background are legible on desktop but compress on mobile. The chip label text is the first thing a user reads — it signals the tier — so it carries more interpretive weight than its size suggests.

**Observed friction:** "תפקיד טכנולוגי" at 11px on a green chip and "קיים ויכוח מדעי" at 11px on the yellow chip both read as fine-print on mobile. The word "תפקיד" especially compresses because it has a final-letter ף that sits below the baseline.

**Proposed change:** Increase TierChip font size from `11px` to `12px`. Adjust chip height from `24px` to `26px` to accommodate the line-height increase without clipping. The h-padding (`8px` left/right) stays unchanged.

**Before:** `fontSize: "11px"`, `height: "24px"`
**After:** `fontSize: "12px"`, `height: "26px"`

**Achievable with existing tokens/Tailwind:** Yes. `12px` maps to the `methodology.fontSize` token value — this is a known-good floor for small Hebrew text. No new token needed.

**Scope:** TierChip component only. No change to tier color values, no change to TIER_VISUALS mapping.

---

### Polish Item 2 — Collapsed entry-point label mixes two weights in a way that loses hierarchy

**Current state:** The collapsed entry-point button renders:
- A TierChip (chip label at 11px bold)
- A count+action string at `fontSize: "13px"`, `fontWeight: 600`: `"${count} תוספים זוהו — הצג פירוט"`

Both elements are at weight 600. When the TierChip is "קיים ויכוח מדעי" and the label is "3 תוספים זוהו — הצג פירוט", the two bold elements compete for attention. The tier chip is the informative signal; the action string is a tap affordance. They should read at different weights.

**Proposed change:** Reduce the count+action string from `fontWeight: 600` to `fontWeight: 500`. The TierChip remains at 600. This restores the intended hierarchy: chip = signal, label = affordance.

**Before:** `fontWeight: 600` on the count+action span.
**After:** `fontWeight: 500` on the count+action span.

**Achievable with existing tokens/Tailwind:** Yes. `fontWeight: 500` is a standard value — no token needed, just an inline style change.

**Scope:** The count+action `<span>` in the collapsed button only. No change to chip weight, no change to the expanded header.

---

### Polish Item 3 — explanation_he truncation at 80 characters cuts mid-word in Hebrew

**Current state:** `truncate(entry.explanation_he ?? "", 80)` appends an ellipsis at character position 80. Hebrew words can be long (e.g. "אמולסיפיקטור" = 13 chars), and a hard character cut at 80 frequently bisects a word, producing a broken-looking line like "אמולסיפיק…" that reads as a rendering error.

**Observed friction:** The truncated string loses meaning when the cut falls inside a word. The ellipsis signals "more text exists" correctly, but the truncated word undermines the confidence of the panel.

**Proposed change:** Change the truncation to cut at the last word boundary before 80 characters, not at the character boundary. Concretely: after slicing to 80 characters, trim to the last space character before the end. If the slice already ends at a space or the full string is ≤80 chars, no change.

**Revised logic:**
```
function truncate(text: string, maxChars: number): string {
  if (text.length <= maxChars) return text;
  const slice = text.slice(0, maxChars);
  const lastSpace = slice.lastIndexOf(" ");
  const cut = lastSpace > 0 ? slice.slice(0, lastSpace) : slice;
  return cut.trimEnd() + "…";
}
```

This is a logic change to one helper function. No visual token involved. The output is still a single truncated line — the information architecture is unchanged. The improvement is purely that the visible text ends on a complete word.

**Before:** Hard char cut at 80: can produce "אמולסיפיק…"
**After:** Word-boundary cut near 80: produces "אמולסיפיקטור…" or "תפקיד…"

**Achievable without restructuring:** Yes. The `truncate` helper is local to `AdditivePanel.tsx`, called once. This is a targeted logic fix, not a component restructuring.

---

### Out-of-Scope Items (noted, not proposed)

The following were observed but are not within the ≤3 targeted-improvement constraint, and several touch information architecture:

- The `maxHeight: "480px"` cap on the expanded panel body creates an internal scrollable zone inside the page scroll — this is a UX friction point, but resolving it would require rethinking the panel's overflow behavior (information architecture change, not visual polish).
- The "עוד" expand trigger for `function_he` has a negative-margin touch-target trick that is unusual but correct per the 44×44 spec.
- The `‹` chevron uses `scaleX(-1)` to flip direction for RTL — this is correct behavior, not a visual defect.

---

## Design Judgment Calls

1. **D-dimension presentation (Section 3): inline paragraphs over icon+text rows.** Four inline paragraphs with a bold lead phrase carry the same information as icon+text rows without the feature-list framing. The decision trades discoverability of individual D-items for framework invisibility. This is the correct trade given Bari's editorial principles. Icon rows would be acceptable only if content testing showed that users were failing to distinguish the four items without visual separation — that condition has not been met and should not be assumed.

2. **Route: `/research/glass-box` over a new `/methodology/` segment.** Introducing a new top-level segment for a single page adds routing overhead and creates an orphaned segment. The `research/` parent already holds transparency-adjacent content and is structurally appropriate. This can be revised if the Frontend Agent identifies a different convention in the existing routing.

3. **Link surface: inline footnote within MethodologyFooter.** The task specification asked whether the link renders as an inline footnote, a "learn more" row, or a tooltip. The inline footnote was selected because it maintains the methodology register and avoids introducing a new visual element (a row or tooltip) that would require a new component. The tooltip was rejected because EXCEPTION-001 (the sole approved tooltip) covers the fermentation filter label on bread only — a second tooltip anywhere in the product requires removal per the flag-for-review rules.

4. **No new design tokens registered.** Every value in this spec is either a direct consumption of an existing token or a local Tailwind utility. The single exception is the `11px` date stamp in section 5, which is explicitly local (not a cross-component design decision) and uses Tailwind `text-[11px]` inline, not a token.
