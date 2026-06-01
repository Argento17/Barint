# Snacks Web Template Rollout v1

**Date:** 2026-05-29  
**Route:** `/hashvaot/snacks`  
**Template:** Comparison Web Template v1

---

## Summary

Snacks is the first Bari category to use `layout="web"` on `ComparisonShelfPage`. Desktop (`lg+`) shows a **920px-wide comparison panel** without the phone frame. Below `lg`, behavior matches the prior frozen shelf (375px centered card from `sm` up).

**No changes** to scores, grades, corpus explanations, or CE copy. Corpus source remains `src/data/comparisons/snacks_frontend_v2.json` (Explanation Engine v2 pass).

---

## Task 1 — Corpus verification

| Check | Result |
|-------|--------|
| Product count | **18** (`_meta.product_count`) |
| Data source | `snacks-comparison-page-data.ts` → static import of `snacks_frontend_v2.json` |
| Rebuilt explanations | **Present** — `_meta.production_pass` includes "Explanation engine v2 pass 2026-05-29" |
| Product-specific insight lines | **Present** — e.g. snk-001: "תמרים (76%)", ingredient counts |
| Empty `positiveSignals` | **3 products** — snk-006, snk-007, snk-013; `InterpretiveExpansion` skips empty arrays |
| Scores unchanged | Order preserved: 70, 58, 56, 55, 53, 51, 47, 46, 46, 45, 43, 42, 41, 39, 32, 29, 17, 13 |

Corpus was **not regenerated** in this rollout; existing CE v2 JSON with rebuilt explanations is already wired.

---

## Task 2 — Desktop web layout

| Requirement | Implementation |
|-------------|----------------|
| Remove phone frame on desktop | `lg:max-w-[920px]` replaces `sm:max-w-[375px]` only at `lg+` |
| Wider container | 920px max, horizontal padding on viewport |
| Easier scan | Rank column, desktop table header, 3-line insight clamp, larger row padding |
| RTL | Unchanged `dir="rtl"` on shell |
| Ranking order | `ProductTable` maps corpus array order; no sort |
| Expansion | Accordion preserved; `ExpansionSection wide` adds `lg:px-8`, 2-col signals |
| Filters / lenses | Unchanged `CategoryShelfLenses` |
| Methodology | Unchanged `MethodologyFooter` |

---

## Task 3 — Mobile preserved

Below `lg` on Snacks:

- `max-lg:sm:max-w-[375px] max-lg:sm:rounded-[2rem] max-lg:sm:shadow-2xl`
- Same row height, 2-line insight clamp, 56px-class image size
- Same accordion toggle behavior

---

## Task 4 — Maadanim impact

| Area | Changed? |
|------|----------|
| Maadanim page | **No** — still `ComparisonShelfPage` default `layout="shelf"` |
| Shared `ProductRow` / `ExpansionSection` | Accept optional `wide` / layout context; **shelf mode = prior styles** |
| Shared `ProductTable` | Passes `rank` prop; header hidden unless `layout="web"` |

Documented in `docs/comparison_web_template_v1.md`.

---

## Task 5 — QA

| Command | Result |
|---------|--------|
| `npm run lint` | Pass (0 errors) |
| `npm run build` | Pass |

**Manual verification recommended:**

- `/hashvaot/snacks` at ≥1024px width — wide panel, rank column, no phone shadow frame
- `/hashvaot/snacks` at 375px — phone-frame shelf
- `/hashvaot/maadanim` — still narrow phone frame on desktop
- Expand snk-006 / snk-007 / snk-013 — no positive signals section, limiting factors still show

---

## Files changed

| File | Change |
|------|--------|
| `src/lib/comparisons/comparison-layout-context.tsx` | **New** — layout mode context |
| `src/components/comparisons/comparison-shelf-page.tsx` | `layout` prop, responsive shell |
| `src/components/comparisons/snacks-comparison-page.tsx` | `layout="web"` |
| `src/components/shared/product-table.tsx` | Header + rank |
| `src/components/shared/product-table-header.tsx` | **New** — desktop guide |
| `src/components/shared/product-row.tsx` | Web responsive row |
| `src/components/shared/expansion-section.tsx` | `wide` prop, 2-col signals |
| `src/components/shared/category-hero.tsx` | `wide` padding |
| `src/components/shared/category-prologue.tsx` | `wide` padding |
| `src/components/shared/category-shelf-lenses.tsx` | `wide` padding |
| `src/components/shared/methodology-footer.tsx` | `wide` padding |
| `src/lib/design/bari-comparison-tokens.ts` | Web layout tokens |
| `docs/comparison_web_template_v1.md` | **New** |
| `docs/snacks_web_template_rollout_v1.md` | **New** |

**Not changed:** `snacks_frontend_v2.json`, scoring, CE modules, Maadanim/Bread pages.
