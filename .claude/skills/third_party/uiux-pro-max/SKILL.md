---
name: ui-ux-pro-max
description: "UI/UX design intelligence for web and mobile. Includes 50+ styles, 161 color palettes, 57 font pairings, 161 product types, 99 UX guidelines, and 25 chart types across 10 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, and HTML/CSS). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, and check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, and mobile app. Elements: button, modal, navbar, sidebar, card, table, form, and chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, and flat design. Topics: color systems, accessibility, animation, layout, typography, font pairing, spacing, interaction states, shadow, and gradient. Integrations: shadcn/ui MCP for component search and examples."
---

<!-- source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/ui-ux-pro-max -->
<!-- installed: 2026-05-31 -->
<!-- version: fetched from main branch (85.2k stars, MIT license) -->
<!-- note: body content derived from source documentation summary; YAML frontmatter is verbatim -->
<!-- sync: to get full rule set, copy SKILL.md directly from source repo -->

# UI/UX Pro Max

Design intelligence skill covering professional UI/UX across multiple platforms and stacks.

## When to Use

Apply this skill whenever a task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control** — essentially whenever a change affects how something looks, feels, moves, or is interacted with.

## Rule Categories by Priority

### 1. Accessibility (CRITICAL)

- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text
- All interactive elements must have visible focus states
- Keyboard navigation must be fully supported
- All interactive elements require aria-labels or visible text labels

### 2. Touch & Interaction (CRITICAL)

- Minimum touch target size: 44×44px
- Minimum spacing between touch targets: 8px
- All async actions must have loading feedback
- Destructive actions require confirmation

### 3. Performance (HIGH)

- Images must use appropriate formats and lazy loading
- Cumulative Layout Shift (CLS) must be prevented
- Largest Contentful Paint (LCP) targets must be met

### 4. Style Selection (HIGH)

- Match visual style to product type and audience
- Maintain consistency across component instances
- Use SVG icons — never emoji as UI icons

### 5. Layout & Responsive (HIGH)

- Mobile-first design approach
- Viewport meta tag required
- No horizontal scroll on any viewport

### 6. Typography & Color (MEDIUM)

- Body text line-height: minimum 1.5
- Use semantic color tokens, not hardcoded values
- Readable line measure: 45–75 characters

### 7. Animation (MEDIUM)

- Animation timing: 150–300ms for UI transitions
- Use transform-only animations for performance
- Always respect `prefers-reduced-motion`

### 8. Forms & Feedback (MEDIUM)

- All form inputs require visible labels (not just placeholder)
- Error messages must be placed adjacent to the failing field
- Use progressive disclosure for complex forms

### 9. Navigation Patterns (HIGH)

- Back navigation must be predictable
- Bottom navigation: maximum 5 items
- Deep linking must be supported

### 10. Charts & Data (LOW)

- Use accessible color palettes for data visualization
- All charts require legends and tooltips
- Provide screen-reader alternatives for chart data

## Workflow

1. **Analyze requirements** — identify product type, target audience, style keywords
2. **Generate design system** — use `--design-system` flag to produce style tokens
3. **Apply domain guidelines** — reference stack-specific rules for the target platform
4. **Validate against rules** — check output against all applicable categories above

## Bari-Specific Notes

When used on Bari:
- Hebrew RTL layout takes precedence over any LTR-default guidance in this skill
- Defer to `bari-frontend-ui` for Bari-specific component and copy rules
- Use this skill for general UX quality checks and accessibility audits
