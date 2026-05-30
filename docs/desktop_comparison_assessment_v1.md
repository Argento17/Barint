# Desktop Comparison Experience Assessment v1

**Role:** Engineering assessment (no implementation)  
**Date:** 2026-05-29  
**Inputs:** Codex Desktop Layout Audit (`audit/1/desktop_layout_audit_v1.md`), frozen `docs/comparison_ui_reference_v1.md`, shared `ComparisonShelfPage` implementation  
**Question:** Should Bari author **Comparison UI Reference v2** and move from a **desktop phone-frame** to a **desktop comparison experience**?

---

## Executive summary

The narrow desktop layout is **not a defect**. It is enforced in one place (`ComparisonShelfPage`: `sm:max-w-[375px]`) and explicitly frozen in Comparison UI Reference v1 as an **editorial shelf prototype**, not a production-grade desktop comparator.

Moving to a desktop comparison experience is a **product and design decision**, not a Snacks (or category) bug fix. Engineering can support either path, but **v2 is a new reference**, not a CSS tweak: it implies layout IA, interaction model, QA baselines, and possibly different density rules for corpus copy.

**Recommendation:** Author **Comparison UI Reference v2** only after product signs a target desktop model (see §8). Until then, v1 remains the correct implementation standard; widening the shell without v2 will create category drift and void frozen QA.

---

## Current baseline (v1)

| Aspect | Behavior |
|--------|----------|
| **Shell** | Full-viewport `#EFEFEB`; centered white card; mobile `w-full`; desktop `sm:max-w-[375px]`, rounded frame, shadow |
| **IA** | Hero → Prologue → Shelf lenses → Zebra accordion list → Methodology |
| **Interaction** | One expanded product at a time; tap row toggles; first filtered row opens by default |
| **Data** | Pre-ordered `BariProductVM[]` from corpus; **no client re-sort** |
| **Expansion** | Interpretive blocks first; nutrition/ingredients muted below hairline |
| **Categories on shelf** | `/hashvaot/maadanim`, `/hashvaot/bread`, `/hashvaot/snacks` (same shell) |
| **Legacy contrast** | Milk comparison, bread dashboard, snack engine use **full-width** `HomeContainer` patterns — not the frozen shelf |

**Strategic intent (inferred):** Mobile-native reading rhythm, calm editorial pacing, “shelf in your hand” metaphor on desktop, single-product depth over spreadsheet scan.

---

## What “desktop comparison experience” could mean

Not one implementation — a spectrum product must choose from:

| Option | Description | Distance from v1 |
|--------|-------------|------------------|
| **A. Wide shell** | Same accordion IA; max-width 640–960px (or `max-w-3xl`); optional two-column expansion text | Low |
| **B. List + detail pane** | Product list left/right; fixed detail panel for expansion (one selection) | Medium |
| **C. Comparison table** | Rows = products; columns = score, grade, key signals; expansion drawer or row stretch | High |
| **D. Responsive hybrid** | v1 phone frame below `md`; B or C from `lg` up | Medium–high |

v2 should name **one** primary desktop model (and mobile parity rules). Engineering cost and migration risk scale with A → D.

---

## Assessment by dimension

### 1. Information density

| | Phone-frame (v1) | Desktop comparison (v2) |
|---|------------------|-------------------------|
| **Gain** | — | More products visible without scrolling; room for secondary columns (grade, segment, 1-line signal); nutrition grid can sit beside interpretive copy; filters + list header can show counts |
| **Lose** | — | Forced vertical focus; whitespace as editorial pacing; less “data dashboard” noise |

**Engineering note:** Corpus and tokens assume **mobile row density** (`rowImageSize` 56px, `insightLine` max ~12 words in tokens). Wider UI does not automatically add information — CE must author **wider-surface copy** (e.g. longer `insightLine`, optional columnar fields) or desktop will look empty/gappy.

**Verdict:** v2 **gains density** only if product defines **what** fills the width (columns vs. prose vs. multi-expand). Width alone is insufficient.

---

### 2. Product comparison efficiency

| | Phone-frame (v1) | Desktop comparison (v2) |
|---|------------------|-------------------------|
| **Gain** | — | Faster score/grade scanning across N products; easier “who’s best on this shelf” task; reduces accordion open-close cycles when comparing 3–5 SKUs |
| **Lose** | — | Deliberate one-product-at-a-time reading; comparison-as-story (prologue → lenses → deep dive) |

**Engineering note:** v1 **forbids client-side re-sorting**. A desktop table naturally invites sortable columns — that would conflict with corpus order ownership unless v2 explicitly allows sort (and defines which fields).

**Verdict:** v2 wins for **analytic comparison tasks**; v1 wins for **narrative comparison tasks**. Bari’s brand rules emphasize editorial calm — tension must be resolved in design, not only engineering.

---

### 3. Table usability

| | Phone-frame (v1) | Desktop comparison (v2) |
|---|------------------|-------------------------|
| **Gain** | — | Familiar pattern for power users; sticky header row; optional column visibility; aligns with “comparison” mental model in `/hashvaot` hub copy |
| **Lose** | — | Not a table today — `ProductTable` is a **semantic name** for a zebra accordion list |

**Risks if “table” is the v2 target:**

- **RTL:** Column alignment, sticky columns, and expandable rows are harder in Hebrew RTL than a single column.
- **Expansion placement:** v1 expansion order and labels are fixed (`הקשר במדף`, etc.). Table + inline expansion often breaks on small row heights or pushes row height inconsistently.
- **Accessibility:** Sortable grids need keyboard model and announcements; accordion rows are simpler.
- **Shared components:** `ProductRow` / `ExpansionSection` are row-centric; a true table is likely a **second layout primitive** or a major refactor — not a shell width change.

**Verdict:** Table usability **improves only with a dedicated table layout** (high effort). “Wider accordion” improves usability modestly without becoming a table.

---

### 4. Reading experience

| | Phone-frame (v1) | Desktop comparison (v2) |
|---|------------------|-------------------------|
| **Gain** | — | Long Hebrew `bottomLine` and bullet lists read at comfortable line length (45–75ch); less thumb-scrolling on desktop; methodology/footer can use horizontal rhythm |
| **Lose** | — | Phone frame mimics **device-native** reading; centered narrow column reduces eye travel; premium/editorial sites often use constrained measure |

**Engineering note:** Site chrome (`SiteHeader`) is full width; shelf is narrow — users see **brand header + phone slab**. v2 full-bleed shelf may integrate better with header but can feel like a different product surface than homepage/blog.

**Verdict:** v2 can improve **long-form reading** in expansion; v1 optimizes **browsing the shelf list**. Depends whether desktop users read expansions or only scan scores.

---

### 5. Mobile parity

| | Phone-frame (v1) | Desktop comparison (v2) |
|---|------------------|-------------------------|
| **Gain** | — | Single responsive system if v2 is breakpoint-based; desktop power without forking routes |
| **Lose** | — | v1 already ships `w-full` on mobile — **mobile unchanged** if only `sm:max-w-[375px]` is relaxed on `lg+` |

**Parity risks:**

| Risk | Severity |
|------|----------|
| Desktop-only features (multi-select, column sort, side panel) | High — dual behavior to test |
| Two corpora/copy variants per breakpoint | High — CE burden |
| Visual regression: QA scripts (`scripts/qa-maadanim-production.mjs`) assume production shelf at fixed width | Medium |
| Category inconsistency if one team ships wide shell before v2 sign-off | Medium |

**Verdict:** Best parity path is **one IA, responsive width + optional layout switch at `lg`**, documented in v2. Forking “desktop site” vs “mobile site” for comparisons should be rejected.

---

### 6. Implementation complexity

Estimated relative to current platform (registry + `ComparisonShelfPage` + shared primitives):

| Change | Touch surface | Effort | Notes |
|--------|---------------|--------|-------|
| Widen shell only (`max-w` breakpoints) | `comparison-shelf-page.tsx`, reference doc, QA screenshots | **S** | Does not change comparison efficiency much |
| Token + typography scale for `md+` | `bari-comparison-tokens.ts`, `product-row`, `expansion-section` | **S–M** | Must preserve interpretive/technical hierarchy |
| List + detail pane | New layout component; selection state; possibly two scroll regions | **M** | Reuse `ExpansionSection`; watch RTL |
| Comparison table layout | New `ProductTable` variant or parallel component set | **L** | Category-specific columns debated; conflicts with no-sort rule |
| Responsive hybrid (v1 mobile / v2 desktop) | Layout switch + duplicated QA matrices | **M–L** | Two UX test matrices × 3 categories |
| Dev/preview + Playwright baselines | `public/qa/`, dev preview | **M** | All frozen references invalid until recaptured |

**Non-code work:** `comparison_ui_reference_v2.md`, CE copy guidelines for desktop line lengths, design tokens for max-width and columns.

**Categories affected:** All registry shelf routes at once (maadanim, bread, snacks) — **no isolated Snacks fix**.

---

### 7. Migration risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Reference violation** | Engineers widen shell without v2 → maadanim “reference” no longer reference | Freeze v1 tag; branch v2; explicit deprecation clause in v1 |
| **Corpus mismatch** | `insightLine` / expansion written for narrow column; desktop looks sparse or wraps badly | CE pass or accept truncation rules in v2 |
| **Sort/filter creep** | Desktop table requests score sorting | v2 must restate corpus order rule or define allowed sorts |
| **Legacy coexistence** | Milk / old dashboards full-width; shelf narrow → brand inconsistency | Product map: which routes are “comparison v2” vs legacy |
| **QA debt** | 375px baselines obsolete | Re-run capture scripts per category |
| **Scope coupling** | v2 bundled with new features (charts, maps, NOVA) | v2 = layout + interaction only; features stay out of scope |
| **Rollback** | Wide layout hard to revert after CE authors desktop-only copy | Feature flag or breakpoint guard for one release |

---

## Synthesis: what Bari gains and loses overall

### Gains (moving to desktop comparison)

1. **Production credibility** on large screens — matches user expectation of “comparison tool,” not mobile preview on monitor.
2. **Higher scan bandwidth** for scores, grades, and filter slices across 18–80+ products (category-dependent).
3. **Better use of desktop attention** for long Hebrew expansion copy and nutrition blocks.
4. **Alignment** with `/hashvaot` hub positioning (interactive comparisons, not article-only).
5. **Room for future v2 features** (side-by-side product pick, sticky filter bar, export) without fighting 375px constraint.

### Losses (moving away from phone-frame)

1. **Distinctive editorial identity** — phone frame is recognizable; wide shelf risks “another data table.”
2. **Forced focus** — one expansion at a time is a feature for comprehension, not only a mobile constraint.
3. **Implementation simplicity** — single column, minimal responsive logic, shared QA footprint.
4. **Frozen guarantee** — v1 is fully specified; v2 reopens design review for all categories.
5. **Copy/asset stability** — CE corpora and QA snapshots target v1 measure; migration cost non-zero.

---

## Decision guidance: should Bari create Comparison UI Reference v2?

| Criterion | Create v2 | Stay on v1 |
|-----------|-----------|--------------|
| Desktop comparisons are **primary** use case for `/hashvaot` | ✓ | |
| Users must compare **many products per minute** (buyer/analyst) | ✓ | |
| Brand priority is **editorial story** per category visit | | ✓ |
| Team wants **minimal** engineering/CE churn this quarter | | ✓ |
| Snacks/bread/maadanim must **look identical** in interaction model | Either — but v2 must be specified once | ✓ today |

**Engineering position:**

- **Do not** change `sm:max-w-[375px]` in code without a signed v2 reference — that would orphan maadanim as “reference” while changing behavior.
- **Do** author **Comparison UI Reference v2** if product rejects “phone prototype on desktop” as a **permanent** production stance.
- **Preferred v2 MVP (engineering):** Option **A** or **D** — responsive wider shell + tuned typography; defer true table (Option C) unless product mandates columnar scan as P0.

---

## Recommended next steps (non-implementation)

1. **Product decision:** Choose desktop model (A/B/C/D) and primary user task (scan vs. read).
2. **Design:** One Figma/spec for maadanim at desktop width; validate RTL and expansion order unchanged unless explicitly revised.
3. **CE:** Decide whether corpus needs desktop-length `insightLine` or optional column fields.
4. **Engineering spike (timeboxed):** Prototype Option A vs B behind `dev/preview` only — no production route change.
5. **If approved:** Write `comparison_ui_reference_v2.md`; mark v1 as superseded for layout only; keep expansion labels and corpus rules unless explicitly changed.
6. **QA:** Replace 375px-only baselines with breakpoint matrix (mobile + desktop).

---

## Appendix: evidence map

| Claim | Source |
|-------|--------|
| Desktop width `375px` intentional | `docs/comparison_ui_reference_v1.md` § Mobile/desktop behavior; item 10 “must not change” |
| Single implementation point | `src/components/comparisons/comparison-shelf-page.tsx` lines 52–53 |
| All shelf categories share shell | `maadanim-comparison-page.tsx`, `bread-comparison-page.tsx`, `snacks-comparison-page.tsx` |
| Accordion, one expand | `product-table.tsx`, `product-row.tsx` |
| No client sort | `comparison_ui_reference_v1.md` § Product order ownership |
| Codex audit classification | `audit/1/desktop_layout_audit_v1.md` |

---

**Document goal met:** Engineering input for whether to create Comparison UI Reference v2 — not an implementation plan.
