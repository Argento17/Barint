---
id: TASK-137E
title: "CC/QA: standardize the verdict-first pattern across all comparisons + QA gate (hummus first, then maadanim/bread/snacks/yogurts)"
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "TASK-148 COLLISON. WILL SOLVE UNDER TASK-148"
depends_on: [TASK-137D]
blocks: []
category_id: null
summary: >
  After hummus validates, drive the identical pattern (verdict-first row + why-headline-metric prologue + boundary sweep) across every comparison category, reusing the shared component. Per category: Content authors verdicts+prologue, Nutrition/Data run the boundary sweep. QA gate: build/lint, route checks, mobile+lg baselines, no stale data, verify +/- moved into the expansion and rows show the verdict.
---

# TASK-137E — CC/QA: standardize the verdict-first pattern across all comparisons + QA gate (hummus first, then maadanim/bread/snacks/yogurts)

137D closed (verdicts go straight into the JSON, no builder). Hummus is the validated **reference**.

## The standard — "every comparison the exact same way" (derived from hummus)
1. **No hero intelligence-card box** — it duplicates the `/hashvaot` featured card.
   `showHeroCard={false}` on `BariComparisonDesktopPage` → lightweight H1 title instead.
2. **No "תובנות מרכזיות" box** — `showInsights={false}` on the hero.
3. **Prologue teaches before it ranks** — what was measured / how / **why the headline metric**
   (+ guardrail + any data caveat). Style is already global: right-aligned, high-contrast `#2A2F36`.
4. **Verdict-first rows** — each product shows a 2–3 sentence editorial `rowVerdict`; the +/− lives
   only inside "למה קיבל את הציון?". Requires the v2 row surface (`v2Slice`) ON.
5. **A headline row metric chosen per category, with the reason stated in the prologue**
   (hummus = protein). Nutrition picks the metric per category.

## Per-category state & lift
| Category | Route | v2 row? | Lift to reach the standard |
|----------|-------|---------|----------------------------|
| **hummus** | /hashvaot/hummus | ✅ rowVerdict | **DONE — reference** |
| **maadanim** | /hashvaot/maadanim | ✅ rowVerdict | **DONE (TASK-137F)** — 87 verdicts, protein prologue, boxes off |
| **bread** | /hashvaot/bread | ❌ | turn on v2 + metric + ~31 verdicts + prologue + boxes off |
| **snacks** | /hashvaot/snacks | ❌ | turn on v2 + metric + ~18 verdicts + prologue + boxes off |
| ~~yogurts~~ | /hashvaot/yogurts | — | **REMOVED from index (2026-06-01)** — redundant with maadanim (which tags "מעדנים · יוגורטים · מוצרי חלבון"). Standalone route still exists but unlinked; candidate for deletion. |
| **milk** | /hashvaot/milk-comparison | ❌ | **frozen scores (CNO ruling)** — copy/layout only, no score touch |
| **vegetable-spreads** | /hashvaot/vegetable-spreads | ❌ | same as the others (hummus spinoff) |

## Recommended sequence
maadanim (closest — v2 infra already live) → bread → snacks → yogurts → vegetable-spreads → milk
(milk last and copy-only, given the frozen-score invariant).

## Per-category work split (each is its own content-heavy effort → own sub-task)
- **Nutrition:** pick the headline metric + 1-line rationale; boundary sweep (raw vs prepared, the
  tahini+sodium+energy rule — see [[feedback_raw_vs_prepared_boundary]]).
- **Content:** prologue rewrite + per-product verdicts (grounded in each corpus trace).
- **Frontend:** `v2Slice` on, `showHeroCard={false}`, `showInsights={false}`; inject verdicts into the
  category JSON; **mobile** (`ComparisonShelfPage`) hero/box parity — separate from the desktop path.
- **QA:** per-category gate — build/lint, route check, mobile+lg baselines, no stale data, verify
  +/− moved into the expansion and the row shows the verdict; re-freeze if scores/grades change.

## Status
Standard defined. **Not bulk-applying to 4 live pages unsupervised** (each needs authored content +
review, like hummus did). Proposing to execute **one category at a time**, maadanim next, each as a
sub-task. Awaiting go on the next category.
