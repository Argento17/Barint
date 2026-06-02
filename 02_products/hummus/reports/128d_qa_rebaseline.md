# TASK-128D — Hummus v2 Activation + QA Re-baseline (mobile + lg)

**Owner:** frontend-agent
**Date:** 2026-06-01
**Action:** Flip `HUMMUS_V2_SLICE = true` and execute the §12 mobile + `lg` QA re-baseline.
**Gates cleared:** TASK-128D (CLOSED, implementation), TASK-129D (CLOSED, confidence-gate
hardening — disposes the activation blocker).

---

## Activation-blocker disposition
TASK-128D's return surfaced a blocker: promoting confidence to the row header amplifies the
re-audit P0 #1 "~15 marketing-prose `verified`" defect. **Dispositioned by TASK-129D (CLOSED):**
the displayed-set audit found **0 over-verified rows** on the shipping 37-row shelf — the
"~15" was a 66-row *file-view* artifact inflated by substring false positives — and the
ingredient-quality hardening pass was applied (5 relabels, **all already excluded**, 0
consumer-facing change). 129D recommendation: **GO**. Blocker cleared; flip authorized.

## Files changed

| File | Change |
|---|---|
| `bari-web/src/lib/comparisons/hummus-comparison-page-data.ts` | `HUMMUS_V2_SLICE = false → true` (one value) + refreshed doc comment recording the 129D disposition. v2 enrichment logic already present (128D impl). |
| `bari-web/scripts/shot-hummus-v2-128d-rebaseline.mjs` | NEW — mobile (375) + lg (1024) re-baseline capture, collapsed + expanded, + maadanim regression. |
| `02_products/hummus/reports/128d_rebaseline_screenshots/` | NEW — re-baseline + crop screenshots. |

No UI/component code changed (the `v2Slice` machinery is reused verbatim). No score changed.
No corpus changed — reads the frozen `hummus_frontend_v3.json` (TASK-129D hardening applied;
file dist verified 53 · partial 11 · insufficient 2; displayed 37 = verified 35 · partial 2).

## Build / lint
- `npm run lint` → **0 errors** (9 pre-existing `<img>` warnings only).
- `npm run build` → **green**, all 33 routes incl. `/hashvaot/hummus`.

## Screenshots (`02_products/hummus/reports/128d_rebaseline_screenshots/`)
- `mobile-collapsed.png`, `mobile-expanded.png` — 375px, full page.
- `lg-collapsed.png`, `lg-expanded.png` — 1024px, full page.
- `mobile-crop.png`, `lg-table-collapsed.png`, `lg-table-expanded.png` — viewport detail crops.
- `regression-maadanim-lg.png` — maadanim (other live v2 category) unaffected.

## QA results

**v2 row surface active on Hummus (both breakpoints):**
- Header reads **"37 מוצרים מוצגים מתוך 37"** → page-level exclusions (TASK-087) intact; matches 129D displayed shelf.
- **Protein metric** block per row (סלט חומוס `18.2 ג` green high bar; חומוס מסעדות `10.1 ג`); null→"—".
- **Confidence promoted to the row** and renders **both states correctly**: verified → "נתונים מלאים"; partial → "נתונים חלקיים" (e.g. row 3 חומוס 73/B). The 129D hardening means no over-verified row is amplified.
- **Strongest +/− row reason** shows (`+ חלבון גבוה לקטגוריה`, `− חומר משמר אחד…`).
- **Footnote de-dup** holds in the expansion — single confidence line, single technical block, no second "advanced" toggle; `מה עובד / מה מבדיל / מה שלא ניתן לאמת / רכיבים` identity intact.
- Score chips unchanged (80/A, 76/B, 73/B…) — display-only enrichment, no score input.

**Regression — maadanim (other live v2 category, lg):** still live v2 (70/B GO row + protein
surface visible at the fold), unaffected. v2 remains correctly scoped — only
`hummus-comparison-page.tsx` and `maadanim-comparison-page.tsx` pass the flag; snacks/bread/
yogurts untouched.

## Regressions found
**None.** No layout breakage at mobile or lg; no leakage into other categories; partial vs
verified confidence states both render correctly post-hardening.

## Recommendation: ✅ GO

Activation is clean and launch-defensible. Flag live, build/lint green, both breakpoints
validated, 129D hardening reflected (0 over-verified displayed rows), and the slice is scoped
to Hummus with zero regressions. Recommend **RETURNED** to the Central Controller to record CLOSED.

*Note:* the working tree carries the (previously uncommitted) TASK-128D v2 implementation plus
this flip. Committing is a Controller/release decision — not performed here.
