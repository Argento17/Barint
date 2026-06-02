# TASK-128D — Maadanim v2 Activation + QA Re-baseline (mobile + lg)

**Owner:** frontend-agent
**Date:** 2026-06-01
**Action:** Flip `MAADANIM_V2_SLICE = true` and execute the §12 mobile + `lg` QA re-baseline.
**Gates cleared:** TASK-128B (CLOSED, implementation), TASK-128C (CLOSED, corpus frozen 90→87).

---

## Files changed

| File | Change |
|---|---|
| `bari-web/src/lib/comparisons/maadanim-page-data.ts` | `MAADANIM_V2_SLICE = false → true` (one value) + refreshed doc comment to record activation. v2 enrichment logic was already present (128B). |
| `bari-web/scripts/shot-maadanim-v2-128d-rebaseline.mjs` | NEW — mobile (375) + lg (1024) re-baseline capture, collapsed + expanded, plus hummus regression. |
| `02_products/maadanim/reports/128d_screenshots/` | NEW — re-baseline + crop screenshots. |

No UI/component code changed. No score changed. No corpus changed (reads the frozen
87-product `maadanim_frontend_v2.json`).

## Build / lint
- `npm run lint` → **0 errors** (9 pre-existing `<img>` warnings, none in changed files).
- `npm run build` → **green**, all 33 routes generated incl. `/hashvaot/maadanim`.

## Screenshots (`02_products/maadanim/reports/128d_screenshots/`)
- `mobile-collapsed.png`, `mobile-expanded.png` — 375px, full page.
- `lg-collapsed.png`, `lg-expanded.png` — 1024px, full page.
- `mobile-crop.png`, `lg-table-collapsed.png`, `lg-table-expanded.png` — viewport detail crops.
- `regression-hummus-lg.png`, `regression-hummus-table.png` — hummus stays v1.

## QA results

**v2 row surface active on Maadanim (both breakpoints):**
- Header reads **"87 מוצרים מוצגים מתוך 87"** → TASK-128C corpus freeze (90→87) propagated to the live page.
- **Protein metric** block renders per row (e.g. יופלה GO `10 ג`, green ≥10 bar; מעדן חצילים `1.8 ג`); null→"—".
- **Confidence promoted to the row** ("נתונים מלאים" = verified) — no longer a 10px footnote.
- **Strongest +/− row reason** shows (`+ 10 גרם חלבון…`, `− עדיין מוצר מתוק…`).
- **Footnote de-dup** holds in the expansion — single confidence line, single technical block, no second "advanced" toggle.
- Score chips unchanged (יופלה GO 70/B etc.) — display-only enrichment, no score input.

**Regression — hummus (control, lg):** rows render in **v1** style — no protein metric, no
promoted confidence label, v1 "בקצרה:" line + "למה קיבל את הציון?" expander intact;
"37 מוצרים" and chips (80/A, 76/B, 73/B) unchanged. v2 slice is correctly **Maadanim-scoped**.

## Regressions found
**None.** No layout breakage at mobile or lg; no leakage into hummus (or other categories
— only `maadanim-comparison-page.tsx` passes the flag). The 3 excluded instability survivors
(`סופר גמדים`, `גמדים לשתיה`, `דנונה מולטי קולגן`) are absent from the live shelf.

## Recommendation: ✅ GO

Activation is clean and launch-defensible. The flag is live, build/lint green, both
breakpoints validated, corpus freeze reflected, and the slice is provably scoped to Maadanim
only with zero regressions. Recommend **RETURNED** to the Central Controller to record CLOSED.

*Note:* the working tree carries the (previously uncommitted) TASK-128B v2 implementation plus
this flip. Committing is a Controller/release decision — not performed here.
