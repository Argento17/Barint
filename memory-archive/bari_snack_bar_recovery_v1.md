---
name: bari-snack-bar-recovery-v1
description: "Snack bar editorial recovery v1 — corrects drift from milk standard back to guided investigation; blog/engine separated; comparisons rebuilt as large visual moments; filters collapsed; product imagery mandatory; BarCompositionBreakdown moved to engine; 3 findings max; map repositioned"
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

Built 2026-05-28. Master document at `C:\Bari\02_products\snack_bars\snack_bar_editorial_recovery_v1.md`.
Analytical data in `snack_bar_blog_v1.md` remains valid — this is a UX philosophy and page architecture correction only.

**Why:** Implementation drifted into dashboard/analytics energy. Blog and comparison engine were merged. Filters, maps, and taxonomy dominated before the user had emotional context. Product presence collapsed. Comparisons were buried in data tables.

**How to apply:** This supersedes snack_bar_blog_v1.md for page hierarchy, component order, and UX philosophy. snack_bar_blog_v1.md data (scores, drivers, comparison pairs, component content) remains valid reference.

## Three Failure Diagnoses

1. **Blog ≠ Comparison Engine** — main architectural mistake. Now separated: blog = guided investigation, engine = calm archive.
2. **Maps and filters before products** — maps appeared before packaging. Product presence collapsed.
3. **Comparisons were buried** — the emotional core appeared below multi-section dimension breakdowns inside data tables.

## New Blog Architecture

```
Hero (tension, specific gap, packaging imagery)
↓ Shelf intro (160 words, makes shelf feel real)
↓ Key Findings (3 max, not 4)
↓ ONE quiet map (medium width, 3 annotations, no controls)
↓ BIG comparison moments (largest visual units on page)
↓ Calm synthesis
↓ CTA → Comparison engine (only here, only once)
```

BarCompositionBreakdown **moved out of blog** — now lives in engine product detail only.

## Comparison Moment Spec

Not tables. Visual format: packaging images (180px tall min) + score chips + 1 driver sentence (max 25 words) + collapsed detail. ComparisonMoment is the first component to build.

## Engine Architecture

- Above the fold: search bar + product grid (filters dormant behind single "סינון" button)
- Map: collapsed behind "מפת המדף ▼", below grid
- Product detail: WhyThisLandedHere + BarCompositionBreakdown + score drivers
- 3 preset comparisons from the blog available as engine shortcuts

## Product Imagery Rule

`image_url` from BSIP1 is mandatory (was optional). 6 comparison products must have verified image URLs. Fallback: flat bar silhouette placeholder. No broken image icons.

## What Did NOT Change

- All dataset constants and scores from snack_bar_blog_v1.md
- All 5 comparison pairs (same products, same score data)
- BarCompositionBreakdown content (moved to engine, not removed)
- GlossaryAccordion and MethodologyNote
- Pre-implementation BSIP2 re-run requirement

[[bari-snack-bar-blog-v1]]
[[bari-explainability-v1]]
[[bari-governance-v1]]
