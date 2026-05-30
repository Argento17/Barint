# Bari Frontend Integration Checklist — v1

**Status:** Canonical  
**Date:** 2026-05-28  
**Purpose:** Standardize how any implementer enters a Bari frontend environment — assess what exists, identify gaps, detect drift, establish build order.

**Use:** Complete every section before writing a single line of implementation code. Each section produces a STATUS value: PASS / GAP / FAIL / UNKNOWN. Do not proceed to Section 8 (build) until Sections 1–7 are complete.

---

## How to Use This Checklist

Run each section top-to-bottom. Fill in the answer fields. Assign the section status. Carry unresolved FAIL or UNKNOWN items into the Risk Map (Section 9) before beginning implementation.

**Status definitions:**
- **PASS** — confirmed, meets Bari spec
- **GAP** — exists but incomplete or non-conformant; fixable before launch
- **FAIL** — does not exist or directly violates Bari spec; must be resolved before launch
- **UNKNOWN** — not yet inspectable; blockers implementation decisions

---

## Section 1 — Repo Discovery

**Goal:** Establish the physical and logical boundaries of the frontend codebase.

| Question | Answer | Status |
|---|---|---|
| Frontend repo path or URL | | |
| Active development branch | | |
| Framework (Next.js / React / Vue / other) | | |
| Framework version | | |
| Routing system (file-based / react-router / other) | | |
| Node version in use | | |
| Package manager (npm / yarn / pnpm) | | |
| Deployment target (Vercel / Netlify / self-hosted / unknown) | | |
| Staging URL exists | | |
| Production URL exists | | |
| RTL support in place (required — Hebrew content) | | |
| `dir="rtl"` or equivalent set on root | | |

**Section 1 status:** ___

**Notes:**

---

## Section 2 — Architecture Discovery

**Goal:** Understand the current page structure and where the Bari comparison page fits.

| Question | Answer | Status |
|---|---|---|
| Does a category comparison page exist at all? | | |
| If yes: path/route of an existing category page | | |
| Is there a shared page layout / shell component? | | |
| Is there a reusable list/table component for products? | | |
| Component hierarchy documented anywhere? | | |
| State management in use (none / useState / Zustand / Redux / other) | | |
| Data fetching pattern (static JSON / API / getStaticProps / other) | | |
| Is category data a static file, a database, or an API call? | | |
| Does the page support Hebrew content end-to-end (data → render)? | | |

**What you are looking for:**

The Bari comparison page has a fixed 4-section structure: Hero → Prologue → Product Table → Methodology. If the repo has an existing page template that does not match this structure, that is a GAP — not a reason to adapt the spec.

**Section 2 status:** ___

**Notes:**

---

## Section 3 — Component Discovery

**Goal:** Audit whether the 7 required Bari canonical components exist, and if they do, whether they conform to spec.

For each component, check: Does it exist? Does it match the spec in `ui_stabilization_sprint_1.md` and `comparison_template_v1.md`?

### Row Component

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| Collapsed height | 72px (mobile) | | |
| Product image size | 56×56px | | |
| Score chip slot | 28px, top-right | | |
| Insight line slot | 13px font, single line | | |
| Alternating background | #FFFFFF / #F9F9F9 | | |
| No border between rows | Confirmed | | |
| Tap target ≥ 44px | Yes | | |

### Hero Component

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| Max height on mobile | 280px total | | |
| Hero image height | 160–180px | | |
| Hero sentence max | 12 words | | |
| Score visible without scroll | Yes | | |
| Score display size | 28px | | |
| No chip container around hero score | Yes | | |

### Score Chip

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| Displays numeric + grade only | "72/B" format | | |
| No color encoding | Background not score-dependent | | |
| Size on collapsed row | 28px | | |
| Score chip visible in first 3 rows on load | Yes | | |

### Filter Component

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| Default state is collapsed | Yes | | |
| "סינון" sticky button present | Yes | | |
| Sticky button appears after scroll (not on load) | Yes | | |
| Max filter dimensions | 3 | | |
| Single-select per dimension | Yes | | |
| No filter count badge | Confirmed | | |

### Expansion Section

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| Expands inline (not modal) | Yes | | |
| Max expanded height | 280px | | |
| Nutrition grid included | Yes | | |
| Ingredient list with 4-line clip | Yes | | |
| "הצג הכל" link if ingredients > 4 lines | Yes | | |
| No framework terms in content | Confirmed | | |
| Tap anywhere inside to collapse | Yes | | |

### Prologue Component

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| 3–5 sentences only | Yes | | |
| No framework language | Confirmed | | |
| Max height mobile | 120px | | |
| Font: body weight, not bold | Yes | | |

### Methodology Footer

| Check | Expected | Found | Status |
|---|---|---|---|
| Component exists | Yes | | |
| No heading | Confirmed | | |
| No border or card container | Confirmed | | |
| Font size | 12px | | |
| Color | #AAAAAA | | |
| Last visible element on page | Yes | | |

**Section 3 status:** ___

**Missing components (list):**

---

## Section 4 — Design-System Discovery

**Goal:** Establish what token / design system infrastructure exists and whether Bari's 18 canonical design tokens are represented.

| Question | Answer | Status |
|---|---|---|
| Design system exists (Storybook / tokens.json / other) | | |
| Typography scale defined | | |
| Spacing scale defined | | |
| Color scale defined | | |
| Breakpoint system defined | | |

### Bari Canonical Design Tokens — Audit

Verify each token is either present in the existing system or must be added. Source of truth: `ui_stabilization_sprint_1.md`.

| Token name | Required value | Existing value | Action |
|---|---|---|---|
| row-height-mobile | 72px | | |
| row-height-mobile-max | 80px | | |
| row-image-size | 56×56px | | |
| score-chip-size | 28px | | |
| insight-line-font | 13px | | |
| insight-line-color | #444444 | | |
| product-name-font | 15px | | |
| product-name-weight | 600 | | |
| row-bg-primary | #FFFFFF | | |
| row-bg-alternate | #F9F9F9 | | |
| hero-image-height | 160–180px | | |
| hero-sentence-font | 15px | | |
| hero-sentence-line-height | 1.4 | | |
| hero-score-font | 28px | | |
| prologue-font | 15px | | |
| prologue-line-height | 1.6 | | |
| methodology-font | 12px | | |
| methodology-color | #AAAAAA | | |

**Tokens missing or mismatched:** ___

**Section 4 status:** ___

---

## Section 5 — Styling-System Discovery

**Goal:** Understand the styling approach so token implementation and component isolation are done correctly.

| Question | Answer | Status |
|---|---|---|
| Styling system (Tailwind / CSS Modules / styled-components / Emotion / plain CSS / other) | | |
| Global styles exist and location | | |
| Is there a CSS reset in place? | | |
| Are there existing utility class overrides that could conflict with Bari token values? | | |
| Are component styles isolated (no leakage between components)? | | |

### Risk checks

| Risk | How to check | Status |
|---|---|---|
| Tailwind typography plugin overrides Bari font sizes | Check `tailwind.config.js` for `typography` plugin | |
| Global `a` or `p` styles conflict with insight line rendering | Check global CSS reset or base styles | |
| Existing card class adds border/shadow to rows | Grep for `.card`, `box-shadow`, `border-radius` on list items | |
| Inherited color scheme conflicts with #AAAAAA methodology text | Check CSS custom properties or theme files | |

**Section 5 status:** ___

**Notes:**

---

## Section 6 — Responsive-System Discovery

**Goal:** Confirm the frontend can deliver Bari's exact mobile geometry requirements.

| Question | Answer | Status |
|---|---|---|
| Mobile-first or desktop-first baseline | | |
| Primary breakpoint for mobile (expected: 375px) | | |
| Do viewport-specific styles exist? | | |
| Is there existing sticky header/nav? If so, height? | | |
| Is there existing sticky footer or FAB? | | |
| Scroll event handling: native CSS or JS-managed? | | |
| Is there existing `overscroll-behavior` or scroll-snap? | | |
| Safe-area inset handling for iPhone notch? | | |

### Bari geometry requirements — verify feasibility

| Requirement | Constraint | Feasible? |
|---|---|---|
| Primary viewport | 375×812px, 724px usable | |
| Minimum viewport | 375×667px, 579px usable | |
| Max pre-table height | 480px hard ceiling | |
| Min rows visible on load | 3 rows (primary) / 1 row (minimum) | |
| Sticky nav deducted from usable height | 44px Bari nav + 44px iOS bar = 88px | |
| Sticky "סינון" button | Fixed bottom-right, 16px from edges, appears after 300px scroll | |

**Section 6 status:** ___

**Notes:**

---

## Section 7 — Existing Drift Detection

**Goal:** Before building, identify any existing patterns that must not propagate into Bari components.

Run each check against the existing codebase. Mark CLEAN if absent, PRESENT if found, BLOCKED if cannot inspect.

### Dashboard patterns

| Pattern | Grep / visual check | Status |
|---|---|---|
| Score trend charts / sparklines | grep -r "chart\|Chart\|recharts\|d3\|plotly" | |
| Aggregate statistics (averages, distributions) | grep -r "average\|distribution\|statistic" | |
| Radar/spider charts | grep -r "radar\|RadarChart\|PolarGrid" | |
| Category-level summary cards | grep -r "CategoryCard\|SummaryCard\|CategorySummary" | |
| Score histograms | grep -r "histogram\|Histogram\|BarChart" | |

### Card overuse

| Pattern | Grep / visual check | Status |
|---|---|---|
| Product rendered as card (border + shadow + radius) | grep -r "card\|Card\|shadow-md\|rounded-lg" on product list items | |
| Multiple nested card containers on one product | Visual inspection | |

### Typography drift

| Pattern | Check | Status |
|---|---|---|
| Section headings inside product list | grep for `<h2>`, `<h3>` inside product list component | |
| Labels above product name (brand label, category label) | Visual inspection of row | |
| Score label text ("ציון", "grade", "rating") beside score | Visual inspection | |

### Analytics leakage

| Pattern | Grep | Status |
|---|---|---|
| NOVA term in consumer-facing content | grep -r "NOVA\|nova" --include="*.tsx" --include="*.jsx" | |
| BSIP term in consumer-facing content | grep -r "BSIP\|bsip" --include="*.tsx" | |
| "cap" used as a UI label | grep -r '"cap"\|cap score\|binding cap' | |
| "structural_class" in UI | grep -r "structural_class" | |

### Tooltip proliferation

| Pattern | Check | Status |
|---|---|---|
| Tooltip count across page > 1 | Count all Tooltip components rendered per page | |
| Tooltip on score chip | Inspect score chip component | |
| Tooltip on ingredient | Inspect expansion section | |
| Tooltip on row item | Inspect row component | |

**Drift items found (list):**

**Section 7 status:** ___

---

## Section 8 — Required Canonical Components

These are the only components required for Bari v1. Do not build anything not on this list during the initial rollout.

| # | Component | File name convention | Spec reference | Build priority |
|---|---|---|---|---|
| 1 | ProductRow | `ProductRow.tsx` | `ui_stabilization_sprint_1.md` §Row Rhythm | 1 — everything else depends on this |
| 2 | ScoreChip | `ScoreChip.tsx` | `bari_score_presentation_v1.md` | 1 — part of ProductRow |
| 3 | ExpansionSection | `ExpansionSection.tsx` | `comparison_template_v1.md` §Expansion | 2 — extends ProductRow |
| 4 | CategoryHero | `CategoryHero.tsx` | `ui_stabilization_sprint_1.md` §Hero | 3 — above-fold section |
| 5 | CategoryPrologue | `CategoryPrologue.tsx` | `comparison_template_v1.md` §Prologue | 4 — below hero |
| 6 | StickyFilterButton | `StickyFilterButton.tsx` | `mobile_geometry_checklist_v1.md` §Stage 1 | 5 — after row list renders |
| 7 | MethodologyFooter | `MethodologyFooter.tsx` | `comparison_template_v1.md` §Methodology | 6 — page tail |

**Nothing else ships in v1.** If a component not on this list is proposed during implementation, stop and check against `comparison_template_v1.md`. If it does not appear there, it does not ship.

---

## Section 9 — Implementation Risk Mapping

Complete this section after Sections 1–7. Carry every FAIL and GAP forward. Assign severity and owner.

| Risk | Source | Severity (H/M/L) | Trigger condition | Mitigation |
|---|---|---|---|---|
| Token drift | Existing design system overrides Bari token values | H | Any token mismatch in Section 4 | Bari tokens override via CSS custom properties; document override explicitly |
| Mobile density failure | Pre-table height exceeds 480px | H | Hero or prologue taller than spec | Run geometry checklist before any launch; enforce pixel budgets in component props |
| Score hierarchy collapse | Score chip color-coded or labeled with "חזק/בינוני/חלש" | H | Section 3 score chip audit | Accept only numeric/grade display; reject color prop on ScoreChip |
| Border creep | Row component receives card styling from shared style | M | Global `.card` styles applied to product list | Component-level isolation; ProductRow must not inherit `.card` |
| Filter creep | Fourth filter dimension added per category | M | Category team adds dimension beyond 3 | Filter component max-dimensions prop; hard-code max=3 |
| Tooltip proliferation | Second tooltip added to any page | M | Any ⓘ icon outside EXCEPTION-001 | Exception registry check before merge; lint rule if feasible |
| RTL rendering failure | Hebrew text direction broken in component | H | Arabic numerals or icons misaligned | Test all components with `dir="rtl"` from first render |
| Expansion modal drift | Row expansion opens as sheet/modal instead of inline | H | Bottom sheet or React Native modal used | ExpansionSection component spec: inline only; no portal, no overlay |
| Framework term exposure | NOVA, BSIP, cap appear in insight line or expansion | H | Data pipeline field names leaked to UI | UI layer maps pipeline fields to display values; raw field names never reach JSX |
| Insight line overflow | Insight line wraps to 2 lines at 13px in Hebrew | M | Long Hebrew line at narrow viewport | Max 12-word spec + test at 320px width (even though out of support scope, a leading indicator) |

---

## Section 10 — First Live Category Rollout Plan

**Target category:** מעדנים  
**Data source:** `C:\Bari\02_products\maadanim\bsip2_outputs\`  
**Insight lines:** `C:\Bari\02_products\maadanim\maadanim_insight_lines_v1.md` (64 lines, validated)  
**Validator:** `C:\Bari\03_operations\tools\validate_insight_lines.py`

### Step 1 — Data wire-up

- [ ] Confirm BSIP2 output JSON structure matches the UI data contract (product name, score, grade, insight line, type, ingredients, nutrition)
- [ ] Build or confirm data adapter: pipeline JSON → component props
- [ ] Verify Hebrew strings are UTF-8 end-to-end (file → JSON → render)
- [ ] Run `validate_insight_lines.py` on the final מעדנים set; confirm PASS before wiring

### Step 2 — Component build order

Build in dependency order. Do not skip ahead.

```
1. ScoreChip          — isolated, no dependencies
2. ProductRow         — depends on ScoreChip
3. ExpansionSection   — depends on ProductRow
4. CategoryHero       — isolated
5. CategoryPrologue   — isolated
6. StickyFilterButton — depends on scroll position signal
7. MethodologyFooter  — isolated
8. CategoryPage       — composes all of the above
```

Each component is considered complete only when:
- It renders correctly with Hebrew content in RTL context
- It passes the Section 3 audit table for its component type
- It has been visually inspected at 375px viewport width

### Step 3 — Mobile geometry validation

Run `mobile_geometry_checklist_v1.md` validation procedure in full after CategoryPage is assembled.

- [ ] Measure sections A–F in browser dev tools at 375×812 emulation
- [ ] Confirm pre-table height ≤ 480px
- [ ] Confirm ≥ 3 product rows visible at 0px scroll
- [ ] Confirm score chip visible at 0px scroll
- [ ] Simulate scroll through all 4 stages
- [ ] Expand 3 rows: first, mid-list, last
- [ ] Run 10 auto-fail conditions
- [ ] Run 8 flag-for-review conditions
- [ ] Switch to 375×667, confirm ≥ 1 row visible at 0px scroll
- [ ] Fill in "Per-Category Status" table in `mobile_geometry_checklist_v1.md`

### Step 4 — Drift audit

Run Section 7 checks against the newly built category page specifically.

- [ ] No framework terms in rendered HTML (NOVA, BSIP, cap, structural_class)
- [ ] Tooltip count = 0 (מעדנים has no approved exception)
- [ ] No section headings between prologue and first product row
- [ ] Score chip has no color encoding
- [ ] Filter panel collapsed on load

### Step 5 — QA checkpoints (sign-off gates)

| Gate | Condition | Sign-off required |
|---|---|---|
| Component complete | All Section 3 checks PASS for that component | Implementation |
| Page assembled | Pre-table height ≤ 480px confirmed | Mobile geometry checklist |
| Drift clear | Section 7 re-run on assembled page: all CLEAN | Editorial |
| Insight lines wired | Validator PASS on wired set | validate_insight_lines.py |
| Launch ready | All auto-fail conditions clear | Full checklist PASS |

### Step 6 — Minimum viable mobile validation steps

If a full device is not available, use browser devtools (Chrome mobile emulation):

1. Open at 375×812 (iPhone SE2 / 13 mini preset)
2. Scroll from 0 to bottom, 1 finger gesture simulated
3. Tap first row — confirm inline expansion, not modal
4. Tap within expanded row — confirm collapse
5. Scroll to filter button appearance point (~300px scroll)
6. Tap "סינון" — confirm panel opens inline, not full-screen
7. Switch to 375×667 — confirm row 1 still visible at 0px scroll
8. Open at 430×932 (iPhone 15 Pro Max) — confirm no layout breaks at wider viewport

---

## Checklist Status Summary

Complete this table after running all sections.

| Section | Status | Blocking issues |
|---|---|---|
| 1. Repo Discovery | | |
| 2. Architecture Discovery | | |
| 3. Component Discovery | | |
| 4. Design-System Discovery | | |
| 5. Styling-System Discovery | | |
| 6. Responsive-System Discovery | | |
| 7. Drift Detection | | |
| **Overall** | | |

**Ready to begin implementation:** Yes / No  
**Blocking items before build:** (list)

---

*This checklist governs all frontend integrations for Bari. It is not a substitute for reading `comparison_template_v1.md`, `ui_stabilization_sprint_1.md`, and `mobile_geometry_checklist_v1.md` in full — this document tells you what to check; those tell you what the correct answers are.*
