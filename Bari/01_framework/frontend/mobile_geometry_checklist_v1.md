# Bari Mobile Geometry Validation Checklist — v1

**Date:** 2026-05-28  
**Applies to:** All Bari category pages before launch approval  
**Companion docs:** comparison_template_v1.md, ui_stabilization_sprint_1.md

---

## Viewport Assumptions

All checks run against these viewports. Every check must pass on the primary viewport. Minimum viewport is verified separately.

| Viewport | Label | Dimensions | Chrome + Header | Usable Height |
|---|---|---|---|---|
| **Primary** | iPhone mid (SE2 / iPhone 13 mini) | 375 × 812px | 88px | **724px** |
| **Minimum** | iPhone 8 / SE1 legacy | 375 × 667px | 88px | **579px** |
| **Large** | iPhone 15 Pro Max | 430 × 932px | 88px | **844px** |

**Chrome + Header breakdown:**  
- iOS Safari address bar: 44px  
- Bari sticky nav bar: 44px  
- Total: 88px deducted from raw viewport height

**Note:** 320×568 (iPhone SE 1st generation) is out of support scope. Do not test against it.

---

## Section Height Budget

The page height before the first product row is consumed by:

```
[A] Hero image
[B] Hero sentence
[C] Hero score display
[D] Hero bottom padding
[E] Prologue text
[F] Prologue-to-table gap
[G] Table start
```

Each section has a maximum pixel budget. Together they must not exceed the pre-table ceiling.

| Section | Max height | Notes |
|---|---|---|
| [A] Hero image | 180px | object-fit: contain, height fixed |
| [B] Hero sentence | 44px | 15px font, 1.4 line height, max 2 lines |
| [C] Hero score display | 40px | 28px font, includes vertical rhythm |
| [D] Hero bottom padding | 20px | fixed |
| [E] Prologue text | 120px | 15px font, 1.6 line height, 3 sentences max |
| [F] Prologue-to-table gap | 24px | fixed |
| **Total pre-table budget** | **428px** | hard ceiling: 480px |

---

## Pixel Targets

| Measurement | Target | Hard Maximum | Auto-Fail if Exceeded |
|---|---|---|---|
| Hero image height | 160–180px | 200px | Yes |
| Hero total height (A+B+C+D) | 260–284px | 300px | Yes |
| Prologue text height | 80–120px | 130px | No — flag for review |
| Total pre-table height (A through F) | 390–440px | 480px | Yes |
| First product row: distance from top | 390–460px | 500px | Yes |
| Row height (collapsed) | 72px | 80px | No |
| Methodology font size | 12px | 13px | No |
| Methodology distance from last row | 48px | — | No |

---

## First-Row Visibility Thresholds

### Primary viewport (375 × 812px, 724px usable)

| Metric | Target | Minimum Pass |
|---|---|---|
| Product rows visible on initial load | 3–4 rows | 3 rows |
| First row visible without scrolling | Yes | Yes — mandatory |
| Score chip of first product visible | Yes | Yes — mandatory |
| Pre-table content ≤ 480px | Yes | Yes — mandatory |

**Calculation:** 724px usable − 440px pre-table = 284px table visible = **3.9 rows at 72px each**. Target passes.

**If pre-table = 480px:** 724 − 480 = 244px = 3.4 rows. Marginal pass.  
**If pre-table = 500px:** 724 − 500 = 224px = 3.1 rows. Minimum pass — flag for review.  
**If pre-table = 520px+:** fewer than 3 rows visible. **FAIL.**

---

### Minimum viewport (375 × 667px, 579px usable)

| Metric | Target | Minimum Pass |
|---|---|---|
| Product rows visible on initial load | 1–2 rows | 1 row |
| First row visible without scrolling | Yes | Yes — mandatory |
| Score chip of first product visible | Yes | Yes — mandatory |

**Calculation:** 579px usable − 440px pre-table = 139px table visible = **1.9 rows**. Passes minimum.  
**If pre-table = 480px:** 579 − 480 = 99px table visible = **1.4 rows**. Marginal — 1 full row barely visible.  
**If pre-table = 500px+:** 579 − 500 = 79px = partial first row only. **FAIL.**

---

## Scroll-Stage Behavior

Each stage has a pass condition. These are verified by simulating scroll in a browser dev tool or device.

### Stage 0 — Initial Load (0px scroll)

| Check | Pass condition |
|---|---|
| Hero image visible | Full image in viewport |
| Hero score visible | Score chip or score display in viewport |
| At least 1 product row visible | First row fully or mostly visible |
| No filter UI visible by default | Filter panel collapsed, "סינון" button not visible yet |
| No section heading between prologue and table | Zero headings in the pre-table content |

---

### Stage 1 — First Scroll (1px–300px scroll position)

| Check | Pass condition |
|---|---|
| Products fully dominate the viewport | ≥ 3 product rows fully visible |
| "סינון" sticky button appears | Appears between 200–350px scroll |
| Hero animates out smoothly | No layout shift when hero scrolls off screen |
| No new content appears between rows | No injected banners, tooltips, or explanations mid-list |

---

### Stage 2 — Mid-Scroll (300px–(n_products × 72px) scroll)

| Check | Pass condition |
|---|---|
| "סינון" button remains visible | Sticky, fixed bottom-right, 16px from edges |
| Alternating row backgrounds consistent | Every row alternates correctly, no missed rows |
| No layout jumps | No scroll position jumps caused by lazy loading or image load events |
| Filter count badge absent | No badge on "סינון" button even with filters active |

---

### Stage 3 — Row Expansion (any scroll position)

| Check | Pass condition |
|---|---|
| Expansion is inline (not modal) | Row expands in place, no overlay, no new screen |
| Scroll adjusts to keep expanded row visible | Smooth scroll to top of expanded row (200ms) |
| Expanded row height ≤ 280px | Nutrition grid + 4 lines ingredients + data note |
| Collapse on tap in expanded area | Tap anywhere inside expanded row collapses it |
| Ingredient overflow clips at 4 lines | "הצג הכל" link present if ingredients > 4 lines |
| No framework terms in expanded content | No "NOVA", "cap", "additive_marker", "structural_class" |

---

### Stage 4 — Methodology (end of scroll)

| Check | Pass condition |
|---|---|
| Methodology has no heading | Zero `<h2>`, `<h3>`, or bold label above methodology text |
| Methodology has no box or border | No border, no background color, no card container |
| Methodology font size | 12px (or rem equivalent) |
| Methodology color | #AAAAAA or equivalent (low contrast) |
| "סינון" sticky button disappears | Button hidden when methodology is in viewport |
| Methodology is the last visible element | No footer content below methodology |

---

## Auto-Fail Conditions

Any of these conditions causes automatic checklist failure. The category page cannot launch until the condition is resolved.

| # | Condition |
|---|---|
| 1 | Hero total height > 300px on primary viewport |
| 2 | Pre-table height > 480px on primary viewport |
| 3 | Zero product rows visible on initial load (primary viewport) |
| 4 | Score chip not visible on initial load without scrolling |
| 5 | Any section heading between prologue and first product row |
| 6 | Score chip uses color encoding (any background color tied to score value) |
| 7 | Filter panel visible (open) by default on page load |
| 8 | Any framework term in consumer-facing content (NOVA, cap, BSIP, routing) |
| 9 | Expanded row opens as a modal or new screen rather than inline |
| 10 | Methodology has a section heading in body font size or larger |

---

## Flag-for-Review Conditions

These do not auto-fail but require editorial sign-off before launch.

| # | Condition | What to verify |
|---|---|---|
| 1 | Prologue text height > 120px | Is this more than 3 sentences? |
| 2 | Pre-table height 460–480px | Acceptable but marginal — confirm minimum viewport still passes |
| 3 | More than 30% of insight lines are T2 (contradiction) type | Rebalance toward T1 before launch |
| 4 | Any insight line exceeds 12 words | Cut or rewrite |
| 5 | Highlighted comparison pair more than 1 | Remove additional pairs |
| 6 | A second tooltip anywhere in the product | Remove |
| 7 | Row height > 72px on mobile | Confirm padding, not content overflow |
| 8 | Score not visible in first 3 rows (products appear but chips don't) | Layout or font issue |

---

## Validation Procedure

Run in this order before any category launch:

```
Step 1 — Measure section heights
  Open page in browser dev tools, mobile emulation (375 × 812)
  Measure each section A–F using the Elements panel
  Record heights against the budget table
  Verify total pre-table ≤ 480px

Step 2 — First-row visibility
  Confirm at least 1 product row is fully visible at 0px scroll
  Confirm score chip is visible at 0px scroll

Step 3 — Scroll simulation
  Slowly scroll from 0px to page bottom
  Check each stage against the stage checklist
  Note any layout jumps, unexpected elements, or sticky failures

Step 4 — Row expansion test
  Expand 3 different rows (first, mid-list, last)
  Confirm inline expansion, correct content, no framework terms
  Confirm collapse behavior

Step 5 — Auto-fail sweep
  Read through all 10 auto-fail conditions
  Confirm none are present

Step 6 — Flag-for-review sweep
  Read through all 8 flag conditions
  Document any that apply and get editorial sign-off

Step 7 — Minimum viewport recheck
  Switch emulation to 375 × 667
  Confirm at least 1 product row visible at 0px scroll
  No additional fixes required unless auto-fail condition is triggered
```

---

## Per-Category Status

| Category | Last validated | Pre-table height | Rows visible (primary) | Status |
|---|---|---|---|---|
| חלב | — | — | — | Not yet validated |
| מעדנים | — | — | — | Not yet validated |
| לחם | — | — | — | Not yet validated |

*Update this table after each validation run.*

---

## Quick Reference Card

```
PRIMARY VIEWPORT:    375 × 812px — 88px chrome = 724px usable
MINIMUM VIEWPORT:    375 × 667px — 88px chrome = 579px usable

MAX HERO:            300px (target 280px)
MAX PRE-TABLE:       480px (target 440px)
MIN ROWS ON LOAD:    3 (primary) / 1 (minimum)
ROW HEIGHT:          72px collapsed
METHODOLOGY SIZE:    12px / #AAAAAA / no heading / no box
FILTER DEFAULT:      collapsed — appears sticky after 300px scroll

AUTO-FAIL COUNT:     10 conditions
FLAG COUNT:          8 conditions
```
