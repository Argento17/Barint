---
name: bari-frontend-ui
description: Guide Claude for Bari website UI work — comparison pages, Hebrew RTL layout, accessibility, component consistency, and prevention of generic AI UI patterns.
---

# Bari Frontend UI Skill

**Owner:** Frontend Agent (implementation) · Design Agent (spec/conformance authority)

## Use this skill when…

- You are building or modifying a comparison page on the Bari website
- You are implementing or adjusting Hebrew RTL layout
- You are working on accessibility for any Bari UI component
- You are creating or modifying a reusable UI component
- You are reviewing a frontend PR for UI quality
- A user says "build a comparison page", "fix the RTL layout", "add a component", "make it accessible", "review the UI", or "improve the frontend"

Authoritative companions (read for any non-trivial comparison-page work):
- `C:\Bari\.claude\agents\design-agent.md` — the frozen Gen 1 constraints table + drift detection
- `C:\Bari\.claude\agents\frontend-agent.md` — canonical component rules + key paths
- `C:\Bari\01_framework\operations\golden_comparison_page_playbook_v1.md` — the end-to-end shelf process (golden example: `/hashvaot/brined-cheeses`)

---

## Bari UI Principles

Bari is a product comparison platform for Hebrew-speaking consumers. Every UI decision must reflect:

1. **Clarity over cleverness** — the interface helps users compare products, not showcase technology
2. **Hebrew-first** — RTL layout is the primary layout, not an afterthought
3. **Trust through consistency** — reuse established components before inventing new ones
4. **Accessibility is non-negotiable** — not a post-launch task
5. **Conformance, not creativity** — Bari is in a conformance phase. The comparison-page look is FROZEN. New visual structure comes from the uniform spine / generate_page path, never from improvisation.

---

## Comparison Pages — the frozen Gen 1 architecture

Comparison pages are the core UI surface of Bari. The architecture is FROZEN
(design-agent.md, "Gen 1 Design Constraints"). There is **no** category header +
filter panel + product grid + comparison drawer layout — that architecture does
not exist on Bari and must never be built.

### Page structure (exactly 4 sections)

Every comparison page is exactly:

**Hero → Prologue → ProductTable → Methodology**

- **Hero** — max 280px mobile, single sentence, no aggregate statistics.
- **Prologue** — 2–3 pre-authored sentences. Up to 3 data-journalism charts may appear in the prologue (owner-sanctioned amendment, golden playbook Stage 6): built in **recharts** (never hand-rolled SVG, never CDN chart libs), data-driven from the frontend JSON, readable at 375px. **Grade is never color-encoded in charts** — uniform ink dots; grade appears only as a text lane label.
- **ProductTable** — one row per product, rendered in the JSON `products` array order (pre-sorted score-descending by the pipeline; the UI never sorts).
- **Methodology** — plain muted footer text: 12px / `#AAAAAA`, no card, no border, no heading (frozen table, design-agent.md). Values must be read from the token file, never hardcoded — see "Known spec-vs-code deltas" below.

Never add a section between Prologue and ProductTable. Never add page-level structure beyond the 4 sections without a design-exception registry entry.

### Rows and expansion (no drawer — ever)

- Collapsed row: **72px height (80px max), 56px product image**, verdict/insight line below the name. Token source: `BARI_COMPARISON_TOKENS.layout` (`rowHeightMobile: "72px"`, `rowHeightMobileMax: "80px"`, `rowImageSize: "56px"`).
- Expansion is **inline only** — the row expands in place to show nutrition + ingredients + confidence. **No drawer, no modal, no sheet, no overlay.** No headings inside the expansion.
- Score chip (`ScoreChip`): **color-coded by grade via `gradePalette`** (owner directive 2026-06-03) — one hue family per grade A→E (green → olive → gold → orange → red), monotonic good→poor. Same chip geometry for all grades; only accent/bg/text/border colors vary. Display format per the frozen table: `72 · B · טוב` (numeric + grade letter + tier word; grade conveyed by both letter and color). Never revert to a neutral chip; never add a second color axis or per-product color outside the A–E ramp.
- Filter: **collapsed at 0px scroll, sticky FAB appears after 300px scroll, max 3 filter dimensions.** Multiple filter dimensions must not be open by default.
- Max 1 highlighted comparison pair per page.

### Canonical components (source of truth: `src/components/shared/`)

All frontend code lives in `C:\bari\bari-web`. Key paths (frontend-agent.md):

```
src/components/shared/            Canonical Gen 1 components (source of truth)
src/components/comparisons/       Category page assemblies + legacy pages
src/lib/view-models/index.ts      BariProductVM — the only type the UI touches
src/lib/comparisons/registry/     Category registration (add new categories here)
src/lib/design/bari-comparison-tokens.ts  Design tokens
src/data/comparisons/             Frontend JSON datasets
src/app/hashvaot/                 Comparison page routes
```

Canonical shared components include: `score-chip.tsx`, `comparison-row.tsx`, `comparison-table.tsx`, `expansion-section.tsx`, `methodology-footer.tsx`, `category-hero.tsx`, `category-prologue.tsx`, `comparison-metric-column.tsx`, `confidence-marker.tsx` / `confidence-indicator.tsx`, `AdditivePanel.tsx`, `glass-box-flag.tsx`. Extend these; do not fork them. Category-specific polish must be scoped (e.g. a `.bc-page` style block) so shared components never regress for other categories.

Token rule: never hardcode a value that exists in `src/lib/design/bari-comparison-tokens.ts` or `bari-web/colors_and_type.css` — read it from the token source. `colors_and_type.css` is read-only.

### Known spec-vs-code deltas (do not "fix" silently)

Verified discrepancies between the frozen-spec docs and the shipped code. If your work touches these, flag them to the Design Agent — do not resolve them unilaterally in either direction:

- **Chip tier word:** design-agent.md specifies `72 · B · טוב`; the shipped chip renders numeric + grade letter only — the tier word was deliberately removed ("FIX-2", `comparison-row.tsx`). Do not re-add the tier word without a Design Agent ruling.
- **Methodology color:** frozen table says 12px / `#AAAAAA`; the token file (`bari-comparison-tokens.ts` → `methodology`) says 12px / `#666C67`; the shipped `methodology-footer.tsx` renders `text-[11px] text-[#6B7070]`. The structural constraint (no card / no border / no heading) is unambiguous; take exact values from the token file.

### View Model boundary (hard)

- UI components consume **`BariProductVM`** (and the other VM types) from `@/lib/view-models` **only**. The UI layer never imports from `lib/comparisons/`, `lib/bsip/`, or any scoring module, and never touches raw BSIP fields.
- **The UI never sorts, never rounds, never interprets.** `products` arrive pre-ordered (scored desc, insufficient appended last); scores arrive pre-rounded; hero aggregates (`averageScore`, `topProduct`) arrive pre-computed; confidence labels (`confidence_label_he` etc.) arrive pre-rendered — render them verbatim.
- Trace/provenance fields on the VM (e.g. `nova_class`, `modifier`, `gatedScore`) are presentation-irrelevant — never rendered.

### Data Display

- Attribute labels come from the approved label registry / the pre-rendered Hebrew strings on the VM — do not invent display names.
- Attribute values must be traceable to pipeline output — do not hardcode product data.
- **Missing values render an explicit "data could not be retrieved" state** — the null-state pill / "—" / the backend's pre-rendered Hebrew label — never a blank cell, never a fabricated value, and **never a substitute source. Open Food Facts is banned project-wide for every field, including images** (off_ban_hard_rule). Unknown is acceptable; OFF is not.
- **No framework vocabulary in any rendered string:** NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, dimension, run/flag/EV ids, internal slugs. Consumer copy is plain Hebrew.
- Product images are self-hosted only (`bari-web/public/products/`, same-origin via `next/image`) — never hotlink retailer/Cloudinary/external hosts for new categories.

### Legacy quarantine (frontend-agent.md)

**Do not import** into canonical components: `bari-grade-badge.tsx`, `dimension-bars.tsx`, `bari-interpretation-panel.tsx`, or anything from `src/components/snack/`. Quarantined legacy files are not touched during canonical build sprints — document, defer. (Note: `comparison-row.tsx` currently imports `BariGradeBadge` — a pre-existing condition; do not extend the pattern to new code, and do not "clean it up" mid-task without a Design Agent ruling.)

### Drift detection (design-agent.md — flag any of these as a violation)

- A chart or visualization above the first product row (prologue charts are the sanctioned exception)
- The user must make a choice before seeing a product
- A summary statistic before rows
- Multiple filter dimensions open by default
- More than 1 comparison pair
- Score shown with a verbal interpretation beside it
- A heading inside the expansion section
- Any drawer / modal / sheet / overlay for product detail

---

## Hebrew RTL Layout

RTL is the default layout direction for the Bari website. Follow these rules:

### Direction

- Always set `dir="rtl"` at the document or page root — do not rely on CSS alone
- Text alignment for body copy: `text-align: right` (or `start` in logical properties)
- Icons that imply direction (arrows, chevrons) must be mirrored for RTL — do not rely on auto-mirroring

### Typography

- Hebrew text requires adequate line-height — do not use line-height values optimized for Latin scripts
- Font stack must include a Hebrew-supporting font as the first preference
- Avoid ALL CAPS for Hebrew text — it is not conventional and reduces readability

### Layout Patterns

- Flexbox: use `flex-direction: row-reverse` or logical properties (`margin-inline-start`) — do not hardcode `left`/`right` margins for directional layout
- Do not mix RTL and LTR layout contexts without explicit `dir` attributes on the child container
- Form fields: label position must follow RTL (label to the right of the input, not left)

### Testing RTL

- Always test in a Hebrew locale browser environment, not just by flipping CSS
- Check: text overflow, truncation direction, icon placement, input cursor position
- Mobile-first: 375px is the primary viewport

---

## Accessibility

All Bari UI must meet WCAG 2.1 AA as a minimum.

### Required

- All interactive elements must have accessible labels (`aria-label` or visible text)
- Color contrast must meet AA ratios — do not use color alone to convey meaning (the grade chip carries the grade in the letter AND the color; the colorblind-safe position dot on the accent bar is part of this)
- Keyboard navigation must work for the full comparison flow: filter, expand/collapse rows inline (Enter/Space on the row button), navigate expansion content
- Focus indicators must be visible — do not remove the default outline without providing a replacement
- Images must have `alt` text — product images must describe the product
- Gate: `npm run test:a11y` (axe-core WCAG2 A/AA) must pass on touched routes

### Forbidden

- Do not use `aria-hidden` on elements that convey meaning
- Do not suppress focus rings globally
- Do not rely on hover-only interactions for any core comparison functionality
- Do not use placeholder text as a substitute for visible labels

---

## Component Consistency

Before creating a new component:

1. Check `src/components/shared/` for an existing component that covers the use case
2. If an existing component almost fits: extend it, do not fork it
3. If no existing component fits: a NEW canonical component requires the **Design Agent's approved, conforming visual spec before implementation** (design-agent.md Hard Rule 6)

When building a component:

- Props must be typed and documented
- Component must handle empty/loading/error states explicitly
- Component must be tested in RTL and LTR contexts even if only RTL is expected in production
- Consume tokens; never duplicate values that exist in `bari-comparison-tokens.ts`

---

## Avoid Generic AI UI

Bari's UI must feel like a product built for Israeli consumers, not a generic AI-generated interface. Reject the following patterns:

- Gradient hero sections with abstract shapes
- "Card grid with rounded corners and shadows everywhere" as a default layout
- Placeholder copy like "Discover amazing products" — all copy must be specific to the category
- Emoji in navigation or headers
- Dark mode toggles added without product decision
- "Powered by AI" badges or copy unless specifically approved
- Chatbot-style UI for what is a structured comparison task

When reviewing UI, explicitly flag any of the above as a violation requiring revision.

---

## Forbidden Actions

- Do not ship a comparison page with hardcoded product data
- Do not build a comparison drawer, modal, sheet, or overlay — expansion is inline only
- Do not add a 5th page section or a section between Prologue and ProductTable
- Do not sort, round, or interpret data in the UI — the VM arrives final
- Do not put framework vocabulary (NOVA, BSIP, cap, floor, structural_class, matrix_integrity, pillar, dimension) in any rendered string
- Do not use Open Food Facts for anything, ever
- Do not ship RTL layout that was not tested in a Hebrew locale environment
- Do not add a new component without checking `src/components/shared/` first, or without a Design Agent spec if it is new
- Do not import quarantined legacy files into canonical components
- Do not remove or suppress accessibility features to meet a visual design preference
- Do not use generic AI UI patterns listed above
- Do not add new page-level UI structure without a design-exception registry entry

---

## Expected Output Format

For a UI review or implementation task, produce:

```json
{
  "page_or_component": "<name>",
  "review_date": "<ISO date>",
  "reviewer": "Claude (bari-frontend-ui)",
  "checks": {
    "comparison_structure": "pass | fail | na",
    "data_traceability": "pass | fail | na",
    "rtl_layout": "pass | fail | na",
    "accessibility": "pass | fail | na",
    "component_consistency": "pass | fail | na",
    "generic_ai_ui_check": "pass | fail | na"
  },
  "violations": [],
  "required_revisions": [],
  "approved_for_merge": false
}
```

---

## Owner Mapping

| Responsibility | Owner |
|---|---|
| Comparison Page Structure | Frontend Agent (implementation) / Design Agent (spec) |
| Hebrew RTL Layout | Frontend Agent |
| Accessibility | Frontend Agent + Adversarial QA Agent |
| Component Library | Frontend Agent |
| Copy and Labels | Content pipeline (two-gate sign-off) |
| Visual Design Approval | Design Agent (Gen 1 conformance) |
