# Bari Cursor Implementation Handoff Protocol — v1

**Status:** Active  
**Date:** 2026-05-28  
**Purpose:** Ensure consistent component implementation across multiple Cursor sessions.  
**Use:** Every Cursor session that touches canonical Bari comparison components begins by reading this document.

---

## Section 1 — Required Context Before Starting Any Session

A Cursor session must load the following documents before writing any code. If a document is not loaded, do not begin.

| Priority | Document | Path | What it provides |
|---|---|---|---|
| 1 | This protocol | `C:\Bari\01_framework\cursor_handoff_protocol_v1.md` | Session rules |
| 2 | Component build sequence | `C:\Bari\01_framework\component_build_sequence_v1.md` | Build order, forbidden patterns, completion criteria |
| 3 | Comparison template | `C:\Bari\01_framework\comparison_template_v1.md` | Frozen page architecture |
| 4 | UI stabilization sprint | `C:\Bari\01_framework\ui_stabilization_sprint_1.md` | Exact pixel values, row rhythm, design tokens |
| 5 | Design token governance | `C:\Bari\01_framework\design_token_governance_v1.md` | Token file rules, what to add before building |
| 6 | Legacy isolation policy | `C:\Bari\01_framework\legacy_isolation_policy_v1.md` | What not to touch |
| 7 | Architecture generations | `C:\Bari\01_framework\architecture_generations_registry_v1.md` | Gen 0 pattern list — do not reproduce |
| 8 | Exception registry | `C:\Bari\01_framework\exception_registry_v1.md` | Only approved deviations |

**Also read before building a specific component:**
- `frontend_integration_checklist_v1.md` Section 3 — the audit table for that component
- `mobile_geometry_checklist_v1.md` — viewport assumptions and auto-fail conditions

**Current token file:** `C:\Users\HP\bari\src\lib\design\bari-comparison-tokens.ts` — read before building any component that consumes tokens.

---

## Section 2 — Mandatory Frozen References

These values, structures, and behaviors are frozen. A Cursor session must implement them exactly. No judgment, no optimization, no "cleaner" alternative.

### Pixel values (non-negotiable)

| Thing | Value | Source |
|---|---|---|
| Row height, collapsed | 72px | `ui_stabilization_sprint_1.md` |
| Row height, max | 80px | same |
| Product image | 56×56px | same |
| Score chip font size | 28px | same |
| Insight line font size | 13px | same |
| Insight line color | #444444 | same |
| Hero max height (mobile) | 280px | `mobile_geometry_checklist_v1.md` |
| Hero image height | 160–180px | same |
| Pre-table max height | 480px | same |
| Methodology font size | 12px | same |
| Methodology color | #AAAAAA | same |
| Row background (odd) | #FFFFFF | `bari-comparison-tokens.ts` |
| Row background (even) | #F9F9F9 | `bari-comparison-tokens.ts` |
| Sticky filter button margin | 16px from edges | `mobile_geometry_checklist_v1.md` |

### Structural behaviors (non-negotiable)

| Behavior | Required implementation |
|---|---|
| Score chip color | Neutral — `#F7F7F2` background, `rgba(17,19,24,0.10)` border for all grades |
| Score chip content | `{numeric}/{grade}` only — e.g. "72/B" — no label text, no grade description |
| Row expansion | Inline only — `useState` toggle, no portal, no sheet, no dialog, no drawer |
| Filter default state | Collapsed — invisible at 0px scroll |
| Sticky filter appearance | After 300px scroll, fixed bottom-right, 16px from edges |
| Methodology | Plain text, no `<h2>/<h3>`, no border, no card container |
| Page sections | Exactly 4: Hero → Prologue → ProductTable → Methodology |
| Alternating rows | Via `bari-zebra-rows` CSS class — not inline conditional styles |

### Component file locations (non-negotiable)

All new canonical components go in `src/components/shared/`. No exceptions.

```
src/components/shared/score-chip.tsx
src/components/shared/product-row.tsx
src/components/shared/expansion-section.tsx
src/components/shared/product-table.tsx
src/components/shared/category-hero.tsx
src/components/shared/category-prologue.tsx
src/components/shared/methodology-footer.tsx
src/components/shared/sticky-filter-button.tsx
```

---

## Section 3 — Prohibited Improvisation Zones

These are areas where Cursor must not make independent design or implementation decisions. If the session encounters one of these zones and the frozen reference does not cover the specific case, stop and ask — do not improvise.

### Prohibited: score chip appearance changes

Do not change:
- Background color of the score chip
- Border color of the score chip
- Font weight, size, or color of the score numeral
- Font weight, size, or color of the grade letter
- Chip container shape, border-radius, or padding beyond what the token specifies

Do not add:
- Any color variation tied to grade value
- Any label text beside the grade (no "נמוך", "גבוה", "בינוני", "חזק", "מצוין")
- Any animation on the score chip in row context
- Any tooltip or hover state on the score chip

### Prohibited: expansion content additions

Do not add to the expansion section:
- Headings of any size (`h1`–`h6`, bold text that serves as a section heading)
- Score attribution patterns ("מה מעלה את הציון", "מה מוריד את הציון", "למה קיבל את הציון")
- Dimension bars or pillar breakdowns
- Matrix integrity display
- Any string containing: NOVA, BSIP, cap, structural_class, matrix_integrity, pillar, dimension, routing
- A second "הצג הכל" link or any secondary expansion layer
- An "advanced" toggle

### Prohibited: filter additions

Do not add to the filter:
- A NOVA filter dimension
- A grade filter dimension (grade is visible from score chip — filtering by grade creates a second score representation)
- A score range slider
- A count badge on the sticky button
- More than 3 filter dimensions total

### Prohibited: hero additions

Do not add to the hero:
- Aggregate statistics (total scanned, total scored, score range)
- Multiple product images
- Animated floating elements
- A second sentence beyond the single hero line
- Any English uppercase eyebrow text

### Prohibited: methodology changes

Do not:
- Wrap methodology in a card (`rounded-*`, `border`, `bg-*`, `shadow-*` on the container)
- Add a heading above the methodology text
- Make methodology collapsible (`<details>` / `<summary>`)
- Increase font size above 12px
- Use a color darker than #AAAAAA

### Prohibited: imports from legacy components

Do not import into canonical components:
- `BariGradeBadge` from `comparisons/bari-grade-badge.tsx`
- `SnackScoreChip` from `snack/snack-score-chip.tsx`
- `DimensionBars` from `comparisons/dimension-bars.tsx`
- `BariInterpretationPanel` from `comparisons/bari-interpretation-panel.tsx`
- `MatrixIntegrityBadge` from `comparisons/matrix-integrity-badge.tsx`
- Any component from `src/components/snack/`
- Any component from `src/components/comparisons/milk-editorial/`

Do not modify any of these legacy files.

---

## Section 4 — Component Approval Checkpoints

Implementation stops at each checkpoint. Do not proceed to the next component until the current one is explicitly approved.

### Checkpoint 1 — ScoreChip (hard gate entry)

Stop after building `score-chip.tsx`. Required before proceeding:

- [ ] Rendered at 375px viewport width with Hebrew RTL content
- [ ] Score displays as "{number}/{grade}" — no label text
- [ ] Background is `#F7F7F2` for all grades A through E
- [ ] Border is `rgba(17,19,24,0.10)` for all grades
- [ ] No color changes when grade changes
- [ ] Chip size visually approximates 28px numeral
- [ ] **Explicit visual approval received**

Do not begin ProductRow until Checkpoint 1 is passed.

### Checkpoint 2 — ProductRow (hard gate exit)

Stop after building `product-row.tsx`. Required before proceeding:

- [ ] Row renders at 72px collapsed height on mobile
- [ ] Product image renders at 56×56px
- [ ] ScoreChip is positioned correctly (top-right of row)
- [ ] Insight line slot is present (13px, #444444, below product name)
- [ ] Alternating row backgrounds work via `bari-zebra-rows`
- [ ] No border on the row element
- [ ] Tap/click anywhere on row toggles expansion (no separate button)
- [ ] **Explicit visual approval received**

Do not begin ExpansionSection until Checkpoint 2 is passed.

### Checkpoint 3 — ExpansionSection (hard gate exit)

Stop after building `expansion-section.tsx`. Required before proceeding:

- [ ] Expansion is inline — no sheet, no modal, no overlay, no portal
- [ ] Nutrition grid renders correctly in RTL
- [ ] Ingredient list clips at 4 lines with "הצג הכל" link
- [ ] No headings inside expansion
- [ ] No framework terms in any rendered text
- [ ] Expanded height does not exceed 280px
- [ ] Tapping inside expanded area collapses the row
- [ ] **Explicit visual approval received**

### Checkpoint 4 — ProductTable

Stop after building `product-table.tsx`. Required before proceeding:

- [ ] 3+ rows visible at 0px scroll on primary viewport (375×812)
- [ ] Score chip visible in first row without scrolling
- [ ] Row heights consistent — no row taller than 80px collapsed
- [ ] Zebra pattern uninterrupted across all rows
- [ ] Filter wiring confirmed (table responds to active filter)
- [ ] **Explicit visual approval received**

### Checkpoint 5 — Full page assembly

Stop after assembling `[category]-comparison-page.tsx`. Required before launch:

- [ ] Full `mobile_geometry_checklist_v1.md` validation procedure completed
- [ ] All 10 auto-fail conditions confirmed clear
- [ ] All 8 flag-for-review conditions documented
- [ ] `validate_insight_lines.py` PASS on wired insight line set
- [ ] Drift sweep (Section 7 of `frontend_integration_checklist_v1.md`) re-run on assembled page
- [ ] **Explicit launch approval received**

---

## Section 5 — Visual QA Checklist

Run before each checkpoint approval. Check at 375px viewport width (Chrome devtools, iPhone SE2 / 13 mini preset).

### Score chip

- [ ] Same background for product with grade A and product with grade E
- [ ] No text label beside the grade letter
- [ ] Score numeral is the visually dominant element in the chip
- [ ] Chip is visually distinct from the product name (different weight/size)

### Product row

- [ ] Row height feels consistent across all rows — no taller rows visually
- [ ] Product image is flush with row edge or has consistent padding
- [ ] Insight line is visually subordinate to product name (smaller, lighter)
- [ ] Score chip sits in a stable position — does not shift on expand/collapse
- [ ] Zebra pattern is visible and consistent — no two adjacent rows the same color

### Expansion

- [ ] Expansion feels inline — it pushes content below, not overlays it
- [ ] Ingredient text clips cleanly at 4 lines — no orphaned half-line
- [ ] "הצג הכל" link is visible if ingredients exceed 4 lines
- [ ] No heading text visible inside expansion at any size
- [ ] Nutrition grid values are right-aligned (RTL)

### Hero

- [ ] Total hero height does not exceed 280px — measure with devtools ruler
- [ ] Hero sentence is one line or wraps to two lines maximum at 375px
- [ ] Score visible without scrolling on primary viewport

### Filter

- [ ] No filter element visible at 0px scroll
- [ ] Sticky filter button appears between 200–350px scroll
- [ ] Button is fixed bottom-right, not in document flow

### Methodology

- [ ] No visual container around methodology text (no card, no border, no bg)
- [ ] Text visually smaller and lighter than any product row text
- [ ] No heading above methodology text

---

## Section 6 — Mobile QA Checklist

Run at primary viewport (375×812) and minimum viewport (375×667) using Chrome mobile emulation.

### Primary viewport (375×812, 724px usable)

- [ ] Pre-table height ≤ 480px — measure sections A–F in devtools
- [ ] 3+ full product rows visible at 0px scroll
- [ ] Score chip of first product visible at 0px scroll
- [ ] Scroll from 0 to 300px — sticky filter button appears
- [ ] Tap first row — expansion opens inline, no overlay
- [ ] Tap inside expanded row — row collapses
- [ ] Scroll to bottom — methodology visible, no content below it
- [ ] Sticky filter button disappears when methodology is in viewport

### Minimum viewport (375×667, 579px usable)

- [ ] At least 1 full product row visible at 0px scroll
- [ ] Score chip of first product visible at 0px scroll
- [ ] Pre-table height ≤ 500px — if exceeded, flag for review

### Interaction

- [ ] Expand 3 rows: first, mid-list, last — all inline, none modal
- [ ] Collapse each — confirm behavior
- [ ] Tap "סינון" — filter panel opens; confirm it does not cover the entire viewport
- [ ] Select a filter option — table updates, row count changes
- [ ] Clear filter — all rows restore

### RTL

- [ ] Product names right-aligned
- [ ] Insight lines right-aligned
- [ ] Score chip right-positioned in row
- [ ] Nutrition grid labels and values right-aligned in expansion
- [ ] "הצג הכל" link right-aligned
- [ ] Sticky filter button in correct bottom-right position (not bottom-left)

---

## Section 7 — Drift Escalation Rules

These conditions require the session to stop and escalate before continuing.

| Condition | Required action |
|---|---|
| A Gen 0 pattern is proposed or half-implemented | Stop. Remove the implementation. Reference `architecture_generations_registry_v1.md` for the Gen 0 pattern and its Gen 1 replacement. |
| A legacy component is imported into a canonical component | Stop. Remove the import. Re-read `legacy_isolation_policy_v1.md`. |
| A second tooltip is placed anywhere on the page | Stop. Remove it. The only permitted tooltip is EXCEPTION-001 (bread fermentation filter label only). |
| A framework term appears in a component's JSX | Stop. Identify how the term entered the render path. Fix at the data adapter layer. |
| The score chip background or border color differs by grade | Stop. Remove the color variation. Re-read ScoreChip spec. |
| The page section count exceeds 4 | Stop. Identify the extra section. Remove or fold it into an existing section. |
| A component is added to `src/components/snack/` or `src/components/comparisons/[legacy file]` | Stop. New components go to `src/components/shared/` only. |
| An inline hardcoded value duplicates a token | Stop. Replace with token reference. |
| An approval checkpoint is skipped | Stop. Return to the skipped checkpoint. Do not proceed past it. |

**Escalation procedure:**

1. Stop writing code
2. Note the exact condition that triggered escalation
3. Reference the governing document that defines the correct behavior
4. Implement the correction
5. If the governing document does not cover the case: do not guess. Flag it as an unspecified case and halt the session at that point

---

## Session Handoff Format

When a Cursor session ends mid-build, record the following before closing:

```
SESSION HANDOFF — [date]
Component in progress: [name]
Last checkpoint passed: [checkpoint number or "none"]
Files modified this session: [list]
Files created this session: [list]
Tokens added this session: [list or "none"]
Open issues: [list or "none"]
Next action: [exact next step]
```

This note goes in a comment at the top of the in-progress component file, or in `CE_DIRECTION_V1.md` in the repo root if that file exists.

The next session reads the handoff note and the required context docs before writing any code.

---

*This protocol is updated when a new component type is added to the canonical set, or when a drift pattern appears in production that was not anticipated here.*
