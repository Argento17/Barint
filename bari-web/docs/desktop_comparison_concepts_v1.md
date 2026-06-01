# Desktop Comparison Concepts v1

**Date:** 2026-05-29  
**Category:** Snacks (`/hashvaot/snacks`)  
**Status:** Concept only — no implementation  
**Scope:** Desktop UX (`lg+`) only. Mobile shelf frozen. Scoring, corpus, methodology unchanged.

---

## Context

Recent desktop work treated Snacks as a **width problem** (wider shell, table grid, near-full viewport). That did not fix the real issue.

The regression is **hierarchy and reading experience**:

| Layer | What Snacks already has (CE v2) | What stretched table does poorly |
|-------|----------------------------------|----------------------------------|
| Shelf scan | `insightLine` — one-line shelf reasoning per product | Insight competes with grid columns; feels like spreadsheet filler |
| Rank story | Fixed corpus order (18 products, ranked) | Rank column is decorative; sort is not interactive |
| Score | Grade chip + numeric score | Score isolated in narrow column, disconnected from narrative |
| Deep read | `positiveSignals`, `limitingFactors`, `bottomLine`, `comparisonContext` | Expansion trapped under product column; signals feel cramped or orphaned |
| Filters | Multi-select lenses (e.g. clean label, protein) | Filters unchanged but table does not reward filtered re-scan |

**Constraint:** All three concepts use the same `BariProductVM` fields and Hebrew copy. No new scores, no re-authored explanations, no methodology edits.

---

## Bari philosophy (evaluation lens)

| Principle | Implication for desktop |
|-----------|-------------------------|
| Structured food intelligence | Layout should expose **rank → insight → score → reasoning** as a clear stack, not flat cells |
| Comparison as visual identity | Side-by-side or list-versus-list reading; avoid “admin table” or generic data grid |
| Editorial, calm, premium | Generous typography rhythm, restrained chrome, no dashboard density |
| Off-white / graphite / soft emerald | Same tokens; layout carries hierarchy, not new color systems |
| No floating products / orbit / neon | Products stay on a **surface** (list, card, panel)—grounded, not hero-shot marketing |
| No wellness-blog tone | Interpretive blocks stay labeled (מה עובד / מה מגביל / בשורה התחתונה / הקשר במדף) |

---

## Shared desktop chrome (all options)

Unchanged across concepts:

- Hero → prologue → lens filters → product comparison → methodology footer  
- Single expanded product at a time (matches current shelf behavior)  
- Zebra or equivalent row rhythm for scanability  
- RTL, Hebrew strings verbatim from corpus  

---

## Option A — Ranked shelf list

**Idea:** Scale the proven mobile shelf to desktop width without becoming a spreadsheet. One vertical **reading column** per product; expansion opens **below** the row as an editorial block, not a table cell.

### Wireframe (1920px, RTL)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ [Hero]  חטיפי חלבון · מטא                                                        │
│ [Prologue] 2–3 sentences                                                       │
│ [Lenses]  ○ הכל  ○ תווית נקייה  ○ חלבון  ○ …                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  #1  ┌────┐  שם מוצר — ציון 70 · B                              [▼]          │
│      │img │  insightLine (full width, 1–2 lines, primary read)               │
│      └────┘                                                                   │
│      ┌─ expansion (full list width, inset) ─────────────────────────────┐    │
│      │  מה עובד?          │  מה מגביל?     (2 cols when both exist)   │    │
│      │  · signal          │  · signal                                 │    │
│      │  בשורה התחתונה (full width)                                      │    │
│      │  הקשר במדף (full width)                                          │    │
│      │  [nutrition / ingredients]                    [סגור]            │    │
│      └──────────────────────────────────────────────────────────────────┘    │
│  #2  ┌────┐  … (zebra #F9F9F9)                                               │
│  #3  …                                                                        │
│  … (18 rows)                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Methodology]                                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
     ↑ max ~720–840px content column, centered OR aligned start in RTL
     ↑ NOT full-bleed table; whitespace is intentional margin, not “empty gutters”
```

### Row anatomy

```text
[rank] [thumb] [ name + insightLine (flex) ] [ grade chip + chevron ]
─────────────────────────────────────────────────────────────────────
[ optional expansion — same width as row content area ]
```

### Strengths

- **Preserves mobile mental model** — lowest regression risk; team already validated shelf IA  
- **Insight line is the hero** of each row (matches CE intent for shelf scan)  
- **Expansion hierarchy maps 1:1** to existing `ExpansionSection` blocks (2-col signals → bottom line → context)  
- **Editorial tone** — reads like a ranked briefing, not Excel  
- **Implementation complexity: Low–Medium** — mostly layout/CSS; reuse `ProductRow` mobile path with desktop spacing tokens  

### Weaknesses

- **Less “comparison” at a glance** — hard to compare two products without opening two (not supported today anyway)  
- **Narrow content column** can feel conservative on ultrawide unless max-width is tuned (~800px)  
- **18 accordion rows** — long page scroll; no spatial shortcut to jump ranks  

### Implementation complexity

| Area | Effort |
|------|--------|
| Shell / width | Revert wide table grid; cap reading column (~800px) with modest page padding |
| `ProductRow` | One code path for desktop: flex row + below-row expansion |
| `ProductTableHeader` | Remove or replace with minimal “18 מוצרים” meta, not column headers |
| Filters / data | None |

### Fit with Bari philosophy

**Strong.** Closest to “structured food intelligence as editorial list.” Comparison happens through **ordered rank + insight + labeled reasoning**, not column alignment. Risk: if content column is too narrow, feels phone-blown-up; if too wide, insight lines become hard to read.

---

## Option B — Desktop comparison cards

**Idea:** Ranked **cards** in a responsive grid (1 col tablet, 2 cols desktop, optional 3 on ultrawide). Each card surfaces image, name, score, and `insightLine`; expand **in-card** or **inline below card** for full expansion stack.

### Wireframe (1920px, RTL)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ [Hero] [Prologue] [Lenses]                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │ #1        [B] 70    │  │ #2        [C] 63    │  │ #3        [C] 59    │ │
│  │ ┌────┐              │  │ ┌────┐              │  │ ┌────┐              │ │
│  │ │img │  שם מוצר    │  │ │img │  שם מוצר    │  │ │img │  שם מוצר    │ │
│  │ └────┘              │  │ └────┘              │  │ └────┘              │ │
│  │ insightLine (2–3    │  │ insightLine         │  │ insightLine         │ │
│  │ lines, clamped)     │  │                     │  │                     │ │
│  │ [הרחב]              │  │                     │  │                     │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │
│  ┌─ expanded card #1 spans 2 cols ─────────────────────────────────────┐  │
│  │  signals (2 col) · bottom line · context · technical · סגור          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  … rows 4–6 …                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Methodology]                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Card collapsed state

```text
┌──────────────────────────┐
│  #rank          [grade]  │
│  [image]  product name   │
│  insightLine (clamped)   │
│  ─────────────────────── │
│  הרחב ▼                  │
└──────────────────────────┘
```

### Strengths

- **Visual product presence** — thumbnails at parity with score (good for snack category recognition)  
- **Grid scan** — users see more products above the fold (2×3 vs 5–6 list rows)  
- **Feels like a “comparison board”** without a literal table  
- **Filters** — grid reflow after lens toggle is intuitive  

### Weaknesses

- **Insight hierarchy risk** — clamped `insightLine` in cards may **truncate** CE shelf copy (insights are dense Hebrew, often >12 words visually)  
- **Expansion awkwardness** — spanning 2 cols for one expanded card breaks grid rhythm; animated height jumps  
- **Rank order** — grid reading order (RTL row-major) must match corpus rank strictly or story breaks  
- **Not native to current components** — new card primitive; highest UI design surface area  

### Implementation complexity

| Area | Effort |
|------|--------|
| New `ProductComparisonCard` | Medium–High |
| Grid + expanded span logic | Medium |
| Expansion in card | Medium (reuse `ExpansionSection`) |
| Accessibility (grid, expand) | Medium |
| Mobile | Must stay shelf list — **branch layout at `lg`** |

### Fit with Bari philosophy

**Medium.** Delivers “comparison as visual identity” through product tiles, but cards can drift toward **marketplace / catalog** if shadows, grids, and clamps dominate. Needs strict editorial restraint (flat cards, no floating pack shots). Best if insight stays fully visible on expand, never the primary truncated tease.

---

## Option C — Master-detail comparison workspace

**Idea:** Desktop **split view**: ranked **master list** (compact rows) + **detail panel** (full expansion for selected product). List stays scannable; detail panel holds the full interpretive hierarchy without crushing it into a table cell.

### Wireframe (1920px, RTL)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ [Hero] [Prologue] [Lenses]                                                   │
├──────────────────────────────┬──────────────────────────────────────────────┤
│  MASTER (≈38–42%)            │  DETAIL (≈58–62%)                            │
│  ┌────┐ #1 שם      [B] 70 ◀ │  ┌────────────────────────────────────────┐  │
│  ├────┤ #2 שם      [C] 63   │  │ [large image]  שם מוצר · 70/B          │  │
│  ├────┤ #3 שם      [C] 59   │  │ insightLine (repeated or omitted)      │  │
│  ├────┤ #4 …                 │  ├────────────────────────────────────────┤  │
│  │ scroll 18 items │         │  │ מה עובד │ מה מגביל  (2 col)            │  │
│  │ zebra list      │         │  │ בשורה התחתונה                          │  │
│  │                 │         │  │ הקשר במדף                              │  │
│  │                 │         │  │ nutrition · ingredients                │  │
│  └─────────────────┘         │  └────────────────────────────────────────┘  │
│                              │  (empty state: “בחר מוצר מהרשימה”)          │
├──────────────────────────────┴──────────────────────────────────────────────┤
│ [Methodology]                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Master row (compact)

```text
[thumb] [#] [name truncated] ——— [chip]
        ↑ selected: emerald rail or bg tint
```

### Strengths

- **Best separation of hierarchies** — list = rank + score scan; panel = full explanation stack  
- **No accordion scroll collapse** — detail always visible while browsing list  
- **Uses full desktop width purposefully** — not stretched cells, but **two roles**  
- **Strong “workspace” feel** — calm analyst layout (compare to IDE / mail master-detail)  
- **Expansion content breathes** — 2-col signals, bottom line, context at readable measure  

### Weaknesses

- **Loses mobile parity** on desktop — intentional, but two mental models to maintain  
- **Initial state** — must default-select rank #1 (already behavior) or show empty detail  
- **RTL split** — master on right, detail on left; needs careful keyboard/focus order  
- **List-only insight** — `insightLine` may only appear in detail panel (list shows name + score only) unless duplicated  

### Implementation complexity

| Area | Effort |
|------|--------|
| Split layout shell | Medium |
| Master list component | Medium (compact row variant) |
| Detail panel | Medium–High (reuse expansion, add hero product header) |
| State: selection + scroll-into-view | Medium |
| Mobile | Unchanged shelf; `lg` breakpoint switches layout mode |

### Fit with Bari philosophy

**Strong–Very strong** if panel typography stays editorial. Aligns with **structured intelligence workspace**: list is the index, panel is the analysis. Avoids spreadsheet metaphor entirely. Risk: panel can feel empty for `insufficient` confidence products — needs graceful empty states.

---

## Side-by-side summary

| Criterion | A — Ranked shelf list | B — Comparison cards | C — Master-detail |
|-----------|----------------------|----------------------|-------------------|
| Preserves mobile IA on desktop | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ |
| Insight line prominence | ★★★★★ | ★★★☆☆ (clamp risk) | ★★★★☆ (panel) |
| Explanation hierarchy | ★★★★☆ | ★★★☆☆ | ★★★★★ |
| Comparison-at-a-glance | ★★☆☆☆ | ★★★★☆ | ★★★★☆ |
| Implementation risk | Low | High | Medium |
| Regression from current table | Low (revert + widen list) | High (new pattern) | Medium (new shell) |
| Bari editorial fit | ★★★★★ | ★★★☆☆ | ★★★★★ |

---

## Recommendation (for decision, not implementation)

1. **Stop width-first fixes** on the current table grid — they will not restore hierarchy.  
2. **Short-term stabilize:** Option **A** is the fastest path to undo regression while keeping CE shelf narrative intact.  
3. **Strategic desktop bet:** Option **C** best matches “desktop app surface” *and* Bari’s interpretive depth without turning explanations into table debris.  
4. **Option B** only if leadership wants a more visual, product-forward catalog scan — with explicit rules against truncating `insightLine` and against marketplace styling.

### Suggested decision workflow

```text
1. Stakeholder review of this doc (wireframes + fit scores)
2. Pick A (safe) or C (workspace) for Snacks v1 desktop
3. Prototype ONE option in Figma or coded spike (single route, no corpus change)
4. QA: 1920 + 1280 + mobile shelf unchanged
5. Only then replace Comparison Web Template v1 table implementation
```

---

## Explicit non-goals (all options)

- Rescoring, grade changes, or corpus regeneration  
- New filters, sort, or multi-select compare  
- Rewriting `positiveSignals`, `bottomLine`, or methodology copy  
- Milk-style orbit / floating product visuals  
- Horizontal scroll “comparison tables” with 18 columns  

---

## Appendix: current regression (diagnosis)

The stretched **4-column table** inverts the reading order:

```text
Current (problem):  rank | image | name | score
                    └── expansion buried in col 3, narrow measure

Intended (CE):      rank → name + insight → score
                    └── expansion: signals → bottom line → context (full measure)
```

Width to 1600px amplified the wrong pattern: more empty grid space, not more clarity.

---

## Files

| Document | Path |
|----------|------|
| This concepts doc | `docs/desktop_comparison_concepts_v1.md` |
| Prior layout spec (reference only) | `docs/comparison_web_template_v1.md` |
| Corpus (unchanged) | `src/data/comparisons/snacks_frontend_v2.json` |
