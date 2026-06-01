# Bari Architecture Generations Registry — v1

**Status:** Active  
**Date:** 2026-05-28  
**Purpose:** Prevent accidental reuse of deprecated UX patterns from exploratory phases. Each generation is a named, bounded era with specific characteristics, known weaknesses, and a canonical status. When a pattern is proposed during implementation, check it against this registry before building.

---

## How to Use This Registry

When a pattern is proposed — in code, in design, or in conversation — ask: which generation does this pattern belong to?

- If Gen 0: do not use. Document why it was proposed and what Gen 1 alternative exists.
- If Gen 1: verify it matches the canonical spec before building.
- If generation is unclear: treat as Gen 0 until confirmed otherwise.

---

## Generation 0 — Exploratory / Dashboard Phase

**Era:** Pre-2026-05 through first bread/snack/milk comparison pages  
**Canonical status:** Deprecated  
**Surviving files:** `bread-comparison-dashboard.tsx`, `snack-comparison-engine.tsx`, `milk-comparison-page.tsx`, `milk-editorial/` directory, `snack/` directory  
**Governed by:** Legacy Isolation Policy v1 — these files are quarantined, not deleted

---

### Defining Characteristics

**Score display**
- Score chip uses color encoding tied to grade value (A/B = green, C = yellow, D/E = red/dark-red) via `gradePalette`
- Grade letter accompanied by label text: "D · נמוך", "B · גבוה" — label text is consumer-visible
- Comparison variant uses full color background + colored border per grade
- Score presented at multiple sizes (sm/md/lg) with different visual weights per context

**Product layout**
- Products displayed as cards with border, border-radius, and box-shadow (`ProductCardGrid` in snack)
- Card grid: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3` — desktop-optimized grid, not a linear shelf list
- No insight line slot — each product has a separate "בקצרה" takeaway block below the row
- Product row contains inline mini nutrition panels (4 stat boxes: חלבון / סוכר / תוספים / רכיב עיקרי) as always-visible content, not expansion content

**Hero**
- Full-viewport or near-full-viewport section
- Aggregate statistics surface in hero: "256 נסרקו / 81 ניתחו / 31 נבחרו" as card grid
- Multiple animated product images floating in the hero
- Editorial eyebrow text in English uppercase: "BREAD INVESTIGATION"
- Hero height on mobile: unconstrained — exceeds 280px spec by design

**Filter**
- Bread: horizontal pill buttons, always visible, inline above the table
- Snack: `FilterPanel` with `useState(open)` dropdown, includes NOVA filter dimension (NOVA 2/3/4)
- Multi-select grade filter, multi-select NOVA filter — both consumer-facing framework terms
- No sticky filter button — filter is positionally static

**Expansion / product detail**
- Milk: inline expand via `useState(expanded)` — correct mechanism
- Expansion content includes: "מה חשוב לדעת", "מה מעלה את הציון", "מה מוריד את הציון" — score attribution exposed to consumer
- "הצג פירוט לפי היבטים (מתקדם)" toggle reveals `BariInterpretationPanel` — dimension bars with scores, pillar strength labels (חזק/בינוני/חלש/נמוך)
- `MatrixIntegrityBadge` present: renders "שלמות מטריצה" score + hover tooltip + `dominant_matrix_signals`
- Snack: `SnackProductDetailPanel` — opens as a sheet (`src/components/ui/sheet.tsx`) — modal-like overlay

**Framework exposure**
- NOVA label rendered on each snack card: `NOVA{product.nova}`
- `SnackShelfStatBar` renders aggregate: "X% NOVA4" as a consumer-visible stat
- `DimensionBars`: per-product breakdown of processing_quality, protein_quality, additive_quality, fat_quality, glycemic_quality, whole_food_integrity — rendered as horizontal bars with labels and scores
- `MatrixIntegrityBadge`: renders `structural_degradation_level` via `DEGRADATION_LABELS` map
- Pillar strength strings חזק/בינוני/חלש/נמוך rendered as colored labels in `BariInterpretationPanel`

**Methodology**
- Bread: wrapped in `<details>/<summary>` inside a `rounded-[1.25rem] border bg-[#FFFFFF]/80 p-6` card
- Summary heading: "על הניתוח והמתודולוגיה" — renders as bold consumer-visible heading
- Collapsible — content hidden by default

**Insight blocks**
- Bread: 4 "insight block" cards in a `grid gap-4 md:grid-cols-2` — each is an `<article>` with heading + body paragraph + product name pills
- These are editorial commentary cards, not product insight lines
- Pattern: section heading above grid, "ארבע תובנות שעזרו לנו לקרוא את המדף"

**Page structure**
- Bread: Hero → Filter+Table → InsightBlocks → ComparisonPairs → TransparencyArchive → Methodology → Footer
- Milk: Hero → ProductList (with inline nutrition panels) → (no separate prologue)
- Snack: StatBar → SearchInput → ProductCardGrid → FilterPanel → ComparisonMoment → MapSection
- None match the frozen 4-section template: Hero → Prologue → ProductTable → Methodology

---

### Known Weaknesses

1. **Score color encoding trains users to read color, not number** — defeats numeric score display purpose and creates accessibility dependency
2. **Grade label text ("נמוך"/"גבוה") interprets the score for the user** — removes the observation; turns it into a verdict
3. **Dashboard patterns (stat bars, aggregate counts, dimension bars) position Bari as analytics software** — not as a shelf investigation
4. **Card layout (ProductCardGrid) creates browsing-software feel** — products feel like search results, not a shelf
5. **NOVA label in consumer UI** — exposes internal classification framework; consumers don't know what NOVA means, and seeing it creates confusion without context
6. **"מה מעלה/מוריד את הציון" in expansion** — score attribution is the most direct form of ontology leakage; tells the user how the algorithm works instead of what the product contains
7. **Snack detail panel as sheet/overlay** — breaks inline expansion spec; creates a "new screen" feeling that loses shelf context
8. **Methodology as collapsible card** — hiding methodology implies it is something to reveal, not a quiet footer; the card creates visual parity with product content
9. **InsightBlocks section** — editorial commentary between table and methodology splits the page's focus; the table should lead directly to methodology
10. **Multiple comparison pairs** — bread dashboard includes 3 comparison pairs; frozen spec allows maximum 1 optional pair

---

### Migration Priority

| Component | Priority | Notes |
|---|---|---|
| Score chip (color encoding) | High — address in canonical build, not retrofit | New ScoreChip replaces in new pages only |
| Product layout (card → row) | High — address in canonical build | New ProductRow is the replacement |
| Expansion (framework terms) | High — do not copy to מעדנים | Canonical ExpansionSection spec excludes attribution |
| Filter (NOVA, always-visible) | High — address in canonical build | StickyFilterButton + max 3 dimensions, no NOVA |
| Hero (oversized, stats-heavy) | Medium — existing pages left as-is | CategoryHero spec is the replacement |
| Methodology (card, collapsible) | Medium — existing pages left as-is | MethodologyFooter is the replacement |
| InsightBlocks section | Low — does not exist in canonical spec | Not replaced — eliminated |
| Sheet/modal expansion (snack) | High — violates auto-fail condition | Snack is legacy-quarantined; new pages must not copy |

---

## Generation 1 — Frozen Comparison Template Phase

**Era:** 2026-05-28 onward  
**Canonical status:** Active — this is the authoritative architecture  
**First implementation:** מעדנים comparison page  
**Governed by:** `comparison_template_v1.md`, `component_build_sequence_v1.md`, `legacy_isolation_policy_v1.md`

---

### Defining Characteristics

**Score display**
- Neutral chip: `#F7F7F2` background, `rgba(17,19,24,0.10)` border — same for all grades
- Displays: `{numeric} / {grade}` — e.g. "72/B" — no label text, no color variation
- Single size in row context: 28px
- Hero score: 28px, no chip container, no color

**Product layout**
- Linear list — one product per row, full viewport width
- Collapsed row: 72px height (80px max), 56px product image, score chip top-right, insight line below product name
- Insight line: 13px, `#444444`, max 12 Hebrew words, single line
- Alternating backgrounds: `#FFFFFF` / `#F9F9F9` — via `bari-zebra-rows` class
- No borders between rows
- No always-visible nutrition panels

**Hero**
- Compact: max 280px total height on mobile
- Single sentence: max 12 words, describes one shelf observation
- Score displayed without chip container — number and grade only
- No aggregate statistics, no multi-product animation, no eyebrow text

**Filter**
- Collapsed by default — invisible at 0px scroll
- "סינון" sticky button: fixed bottom-right, 16px from edges, appears after 300px scroll
- Max 3 filter dimensions, single-select per dimension
- No NOVA dimension, no grade filter (grade is observable from score chip)
- No badge or count on the sticky button

**Expansion**
- Inline only — no sheet, no modal, no overlay
- Triggered by tap anywhere on collapsed row
- Content: nutrition grid + ingredient list (4-line clip + "הצג הכל") + data note
- No headings inside expansion
- No score attribution ("מה מעלה/מוריד את הציון" is prohibited)
- No framework terms: NOVA, BSIP, cap, structural_class, matrix_integrity, pillar, dimension

**Page structure**
- Exactly 4 sections: CategoryHero → CategoryPrologue → ProductTable → MethodologyFooter
- No sections between prologue and first product row
- One optional comparison pair (highlight — not a separate section, embedded in table)
- No InsightBlocks section
- No TransparencyArchive section
- No aggregate statistics section

**Methodology**
- Plain text footer, no heading, no card, no border
- 12px font, `#AAAAAA` color — low visual weight
- 2–4 sentences maximum
- Last visible element on the page

**Framework visibility**
- Zero NOVA labels in consumer UI
- Zero matrix_integrity references
- Zero dimension bars
- Zero pillar strength labels
- Zero "מה מעלה/מוריד את הציון" patterns
- Score chip conveys no color information tied to grade

---

### Known Weaknesses

Gen 1 is newly designed and has no production history. Anticipated weaknesses to monitor:

1. **Insight line quality variance** — the line type system (T1/T2/T3) is new; real-world T2 density may still skew high on first launch; validator catches ratio issues but not all weak lines
2. **Sticky filter discoverability** — the filter button does not appear until 300px of scroll; users who need filtering immediately may not find it; to be observed in first live session
3. **Expansion tap target** — the full-row tap to expand may conflict with link taps on product name or image; to be verified in first mobile test
4. **Image loading on mobile** — 56px images at 2× DPI require 112px source; image origin and sizing contract with BSIP2 output not yet confirmed for מעדנים

---

### Canonical Status

Gen 1 is authoritative. When any implementation question arises:

1. Check `comparison_template_v1.md` first
2. Check `component_build_sequence_v1.md` for build order
3. Check `exception_registry_v1.md` for approved deviations
4. If not covered: the answer is "do not add it" until a registry entry approves it

---

## Generation Comparison

| Dimension | Gen 0 | Gen 1 |
|---|---|---|
| Score chip | Color-coded by grade | Neutral — same for all grades |
| Grade label text | Visible ("D · נמוך") | None — numeric/grade only |
| Product layout | Card grid or row with nutrition panels | Plain row — insight line only |
| Filter | Inline, always-visible, NOVA-included | Sticky FAB, collapsed, max 3 dims |
| Expansion | Score attribution + framework bars | Nutrition + ingredients only |
| Framework exposure | NOVA, matrix_integrity, dimension bars, pillar labels | None |
| Hero | Full-viewport, stats-heavy, animated | Compact, single sentence, 280px max |
| Methodology | Collapsible card with heading | Plain footer, 12px/#AAAAAA |
| Page sections | 5–7 sections | 4 exactly |
| Insight lines | Not present (replaced by takeaway blocks) | T1/T2/T3 — 12-word max, per-product |
| Comparison pairs | Up to 3 (bread) | 0 or 1 |

---

*This registry is updated when a new architectural generation is introduced. A generation is introduced when a structural decision differs substantially enough from the current generation to require its own defining characteristics. Incremental component updates within Gen 1 do not constitute a new generation.*
