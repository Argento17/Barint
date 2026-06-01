# Bari — Web UI Kit

High-fidelity, interactive recreation of the **Bari comparison experience** — the core product surface (`/hashvaot/<category>`). This kit reflects the **accepted v-next-2 direction** (TASK-098), the second design iteration of the comparison page, built and validated against the live site at `bari.digital/hashvaot/hummus`.

## Files

| File | What it is |
|---|---|
| `index.html` | The comparison page — self-contained React (inline Babel) prototype with real Shufersal hummus data, in corpus order. **Open this.** |
| `README.md` | This file |

`index.html` links the system foundations at `../../colors_and_type.css` (colors, type scale, radii, shadows, motion). No build step — open it directly.

## What it demonstrates (interactive)

- **Compact category header** — merged hero + intro; persistent "category-relative, not absolute health score" framing; a score-distribution histogram; the single category-level fat-data disclosure.
- **Sticky control bar** — sub-category filter with counts (חומוס / מטבוחה / חצילים / פלפלים), live result count, and a **density toggle** (compact ⇄ comfortable).
- **Score-band jump rail** (left) — 80+ / 70–79 / 60–69 / 50–59 / <50 with per-band counts; click to smooth-scroll. Bands are **contiguous in corpus order**, so navigation never reorders.
- **Comparison rows** — rank · packshot · name · strongest **+** / strongest **−** · grade-led score chip · **promoted confidence** · a **column-aligned metric block** (protein · additive-load pips · base %) on a shared scale so equivalent products read equivalent and outliers pop.
- **Explanation panel** (expand any row) — confidence + source at the top, "works / limits (with magnitude bars) / can't-verify", nutrition at the same level as reasons (no nested "advanced" toggle), product-specific unknowns only.
- **Honest no-score state** — insufficient-data products stay visible with a "—" chip, never hidden.
- **Design-decision overlay** — the "הצג החלטות עיצוב" button (bottom-left) annotates every change vs. the live site.

## Core principles honored

1. **Every product remains individually visible** — no clustering, no hiding, no pagination-by-default.
2. **Corpus-owned ordering is preserved** — score-descending as served; filters narrow but never re-sort; no alternative sort modes.
3. **Trust before marketing** — confidence promoted and (per `confidence_label_audit_v1`) accuracy-gated; relativity stated at the point of reading; gaps disclosed once at category level.

## Governance

This is **Comparison UI Reference v2 territory**. The dense rows, jump rail, aligned metric block, and band dividers each diverge from the frozen v1 reference (375px phone-frame, fixed expansion structure). See `../../handoff/comparison-v2-spec.md` for the engineering-facing decision spec, and the root `Bari TASK-091 DEC-002 Decision.html` for what ships pre-launch vs. in v2.

## Data

Real products, copy, scores and grades from `bari.digital/hashvaot/hummus` (Shufersal, May 2026), embedded in `index.html` in corpus order. Hebrew is verbatim from the live site.
