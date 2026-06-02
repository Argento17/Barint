---
id: TASK-137
title: Hummus page editorial upgrade (verdict-first rows + why-protein prologue) + raw/salad boundary fix; then standardize all comparisons
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "TASK-148 COLLISON. WILL SOLVE UNDER TASK-148"
depends_on: []
blocks: []
category_id: hummus
drift_ack: "Parent task. Its hummus deliverables were authored by sub-tasks 137A/137B (both CLOSED); the parent stays IN_PROGRESS only for the cross-category generalization tracked by TASK-137E. Known-good — not a closure-drift."
summary: >
  Owner-directed (Product) upgrade to the hummus comparison page: (1) prologue must state what was measured, how, and why protein is the headline metric; (2) replace the collapsed-row +/- with a 2-3 sentence editorial verdict, moving the +/- bullets into the 'why this score' expansion; (3) fix the boundary bug where raw/salad hummus still shows on a spreads-only shelf. After hummus is validated, apply the identical pattern to every comparison category.
---

# TASK-137 — Hummus page editorial upgrade + standardize all comparisons

Owner-directed by Product (2026-06-01) after reviewing the live hummus page. Three
defects + one rollout directive. Reference architecture for the row/expansion model:
`bari-web/src/components/comparisons/bari-product-shelf-row.tsx` (v2 slice), the VM
contract at `bari-web/src/lib/view-models/index.ts`, and the canonical Maadanim page.

## What Product asked for (verbatim intent)

1. **Prologue must teach before it ranks.** The table prologue must say **what we
   measured, how we measured it, and what is important** — the reader must understand
   that **protein was chosen as the headline metric for a reason**. Choosing protein as
   the row metric is the right call; the *explanation* of that choice is currently weak.
2. **Rows lead with an opinion, not +/−.** Putting `+ / −` at the front of the product
   is the wrong model. The collapsed row should carry **2–3 sentences of our opinion of
   the product**. The `+ / −` detail belongs **inside** the "למה קיבל את הציון?"
   disclosure (double-click) — not on the row face.
3. **Boundary bug — raw/salad hummus still on a spreads-only shelf.** "סלט חומוס"
   (`bsip1_6666307`, 80/A) renders at rank 1, but the shelf is meant to be prepared
   spreads only. Two sibling "סלט" items are also present
   (`bsip1_7296073725374` "סלט חומוס עם טחינה", and the masabacha "סלט חומוס+מסבחה").
   **RESOLVED 2026-06-01.** The real defect was **raw/dry chickpeas** mis-tagged as spreads —
   `bsip1_1990261` + `bsip1_3643714` ("חומוס" 73/B, sodium 12 mg, energy 380 kcal, no tahini,
   no ingredient list). Excluded via `EXCLUDED_RAW_CHICKPEA_IDS` (37→35 displayed). All prepared
   tahini-based salads/spreads KEPT, incl. `bsip1_6666307` "סלט חומוס" 80/A (Product ruling:
   "DO NOT EXCLUDE HUMUS SPREADS/SALAD"). **Boundary rule (reusable): prepared vs raw is decided
   by tahini + sodium + energy — never by protein or the word "סלט".**
4. **Then standardize.** Once hummus is right, **every** comparison category adopts the
   identical pattern (verdict-first row + why-headline-metric prologue).

## Root-cause / current state (verified in code)

- **Row +/−** is `DesktopRowReason` in `bari-product-shelf-row.tsx` (lines 31–56),
  rendered on the collapsed v2 row (line 96) from `product.rowReason.{positive,limiting}`
  (derived in `hummus-comparison-page-data.ts:enrichHummusV2Slice`). The same
  `positiveSignals`/`limitingFactors` arrays are **already** rendered inside the
  expansion (lines 148–168) — so the +/− detail is not lost when we drop it from the row.
- **Prologue** = `hummusPrologueSentences` in `hummus-comparison-page-data.ts:147`.
  States what/where but **never says why protein is the metric**.
- **Boundary** = exclusion sets in `hummus-comparison-page-data.ts:28–65`. The three
  "סלט" items are tagged `_product_type: "hummus_spread"` so they pass the existing
  vegetable-spread filter; whether they are *salads* (whole-bean) vs *spreads* is a
  Nutrition ruling, not a code default.
- **No `rowVerdict` field exists yet** in the VM (`index.ts`). It must be added.

## Cross-agent split (sub-tasks)

| Sub | Owner | Deliverable | Deps |
|-----|-------|-------------|------|
| **137A** | Nutrition | Why-protein-is-headline rationale (feeds prologue) + exclude/keep ruling on the 3 "סלט" items, one-line reason each | — (first) |
| **137B** | Content | Rewrite prologue (what/how/why-protein) + author the 2–3-sentence `rowVerdict` per displayed product | 137A |
| **137C** | Frontend | Add `rowVerdict?: string` to VM; swap `DesktopRowReason` (+/−) on the row for `rowVerdict`; keep +/− inside the expansion. Shared component → propagates to all v2 categories. Design signs off on row density | — (parallel) |
| **137D** | Data | Implement the exclusions (audit record + re-derive counts/grade tally/hero stats/prologue counts); wire authored `rowVerdict` through the builder → `hummus_frontend_v3.json` → sync to `bari-web` | 137A, 137B, 137C |
| **137E** | QA / CC | After hummus validates, roll the identical pattern to maadanim/bread/snacks/yogurts (per-category Content verdicts + prologue + Nutrition/Data boundary sweep); QA gate (build/lint, routes, mobile+lg baselines, no stale data, +/− confirmed moved into the expansion) | 137D |

**Note on owners:** Product named CC/Content/Nutrition/Data. The +/− → verdict change is a
React **component + VM** edit, which is **Frontend Agent** territory (137C) — added
explicitly. Design reviews row density; QA owns the rollout gate (137E).

## Sequencing

```
137A (Nutrition ruling + rationale)
   ├──> 137B (Content: prologue + verdicts)
   └──> 137D ──┐
137C (Frontend VM + row) ──> 137D (Data: exclude + wire + sync) ──> 137E (rollout + QA gate)
```

137A and 137C can start now in parallel. 137D is the integration point. 137E generalizes
only after hummus passes QA.

## Design decision for the new row field

Add **`rowVerdict?: string`** to `BariProductVM` (not a reuse of `bottomLine`, which keeps
its distinct role as "בשורה התחתונה" *inside* the expansion). `rowVerdict` is display-only,
authored by Content, never a score input — same contract discipline as `metrics`/`rowReason`.

## DoD (parent)

- Hummus page: prologue explains what/how/why-protein; every displayed row shows a 2–3
  sentence verdict; +/− appears only inside "למה קיבל את הציון?"; no raw/salad item on the
  spreads shelf; counts/grade tally/hero stats re-derived and consistent.
- Pattern generalized to all comparison categories via the shared component; QA green.
- Per OS rule, only the Central Controller records CLOSED; sub-task owners propose RETURNED.
