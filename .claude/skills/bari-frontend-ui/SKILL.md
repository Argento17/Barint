---
name: bari-frontend-ui
description: Guide Claude for Bari website UI work — comparison pages, Hebrew RTL layout, accessibility, component consistency, and prevention of generic AI UI patterns.
---

# Bari Frontend UI Skill

**Owner:** Frontend Architect

## Use this skill when…

- You are building or modifying a comparison page on the Bari website
- You are implementing or adjusting Hebrew RTL layout
- You are working on accessibility for any Bari UI component
- You are creating or modifying a reusable UI component
- You are reviewing a frontend PR for UI quality
- A user says "build a comparison page", "fix the RTL layout", "add a component", "make it accessible", "review the UI", or "improve the frontend"

---

## Bari UI Principles

Bari is a product comparison platform for Hebrew-speaking consumers. Every UI decision must reflect:

1. **Clarity over cleverness** — the interface helps users compare products, not showcase technology
2. **Hebrew-first** — RTL layout is the primary layout, not an afterthought
3. **Trust through consistency** — reuse established components before inventing new ones
4. **Accessibility is non-negotiable** — not a post-launch task

---

## Comparison Pages

Comparison pages are the core UI surface of Bari. Follow these rules:

### Structure

- Every comparison page must have: category header, filter panel, product grid, comparison drawer
- Do not add structural elements that do not serve the comparison task
- Product grid must support at least 3 and at most 12 products in a single view without horizontal scroll on desktop

### Data Display

- Attribute labels must be pulled from the approved label registry — do not invent display names
- Attribute values must be traceable to enrichment output — do not hardcode product data
- Missing values must render as an explicit empty state ("לא ידוע" or equivalent), not as blank cells
- Do not show raw internal slugs or IDs to users

### Comparison Drawer

- The comparison drawer must show a max of 4 products side-by-side
- Attributes shown in the drawer must be the same set for all selected products
- Highlight winning values per attribute only when the comparison is unambiguous
- Do not highlight when comparison is subjective

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

---

## Accessibility

All Bari UI must meet WCAG 2.1 AA as a minimum.

### Required

- All interactive elements must have accessible labels (`aria-label` or visible text)
- Color contrast must meet AA ratios — do not use color alone to convey meaning
- Keyboard navigation must work for the full comparison flow: filter, select products, open drawer, navigate attributes
- Focus indicators must be visible — do not remove the default outline without providing a replacement
- Images must have `alt` text — product images must describe the product

### Forbidden

- Do not use `aria-hidden` on elements that convey meaning
- Do not suppress focus rings globally
- Do not rely on hover-only interactions for any core comparison functionality
- Do not use placeholder text as a substitute for visible labels

---

## Component Consistency

Before creating a new component:

1. Check the Bari component library for an existing component that covers the use case
2. If an existing component almost fits: extend it, do not fork it
3. If no existing component fits: propose the new component to the Frontend Architect before building

When building a component:

- Props must be typed and documented
- Component must handle empty/loading/error states explicitly
- Component must be tested in RTL and LTR contexts even if only RTL is expected in production

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
- Do not ship RTL layout that was not tested in a Hebrew locale environment
- Do not add a new component without checking the existing component library first
- Do not remove or suppress accessibility features to meet a visual design preference
- Do not use generic AI UI patterns listed above
- Do not add new page-level UI structure without Frontend Architect approval

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
| Comparison Page Structure | Frontend Architect |
| Hebrew RTL Layout | Frontend Architect |
| Accessibility | Frontend Architect + QA Lead |
| Component Library | Frontend Architect |
| Copy and Labels | Category Team |
| Visual Design Approval | Product Owner |
