# P472 / TASK-465 catalog redesign: sharp data-dashboard (PowerBI-grade) for /catalog (route: C1-CURSOR)

## 1. Context
- You are ALREADY in isolated worktree `C:\bari_wt_t465`, branch `feat/task465-catalog-dashboard`, cut from origin/master `6284546a` (includes the merged catalog + the empty-state fix + green CI). Never touch `C:\Bari`. Commit here; NO push/PR. `npm ci` in `bari-web\` first.
- Owner directive (2026-07-02, verbatim intent): the current `/catalog` "looks kinda cheap" — redesign it to look like a **sharp PowerBI-grade data dashboard**. This is a visual/layout overhaul of `bari-web/src/app/catalog/page.tsx` + `_catalog-client.tsx` (and any new components you extract under `bari-web/src/components/inventory/`). The catalog is NOT part of the frozen comparison-page system, but it must stay coherent with the site's design tokens and Hebrew RTL.

## 2. Objective — dashboard anatomy (all data DERIVED live from the loaded corpus; zero hardcoded numbers)
1. **KPI header strip** (the PowerBI "card row"): compact stat cards — total products, categories covered, grade distribution (S/A/B/C/D/E counts as a segmented horizontal bar with counts), % full-data products if derivable from `confidence`. Big numerals, small muted labels, hairline borders, subtle shadow. Every number computed from `buildInventoryRows`/`buildInventoryProductDetails` output at render time (the TASK-460 lesson: hardcoded stats rot).
2. **Slicer/filter bar:** the existing category/search/grade controls restyled as a tight professional toolbar — segmented controls / compact chips, clear active state, result-count readout ("N מוצרים"). Keep all existing filtering behavior and the barcode-in-search capability.
3. **Data grid:** dense, spreadsheet-sharp rows — sticky header row, tabular-nums right-aligned score column, grade chip (reuse the site's existing grade-chip visual language), category tag, retailer, product name+thumbnail leading. Hairline row dividers, subtle hover, consistent 8px-grid spacing. Column sort on score/name/category (client-side). The existing per-product expansion panel must keep working unchanged (it is the shared expansion-section — do NOT modify that component).
4. **Distribution visual:** one compact grade-distribution bar (or per-category mini-bars) integrated into the KPI strip or above the grid — CSS/inline-SVG only, no new chart dependency. IMPORTANT site rule: score VALUES are never color-encoded; grades use the existing site grade colors only.
5. **Responsive:** ≥1024px = full dashboard; mobile = KPI cards 2-up, grid degrades to the current card-like rows. RTL correct throughout (right-aligned Hebrew, mirrored layout).
6. **Perf sanity:** no new heavy deps (no chart libs, no CSS frameworks); bundle delta reported.

## 3. Boundaries (HARD)
- **Zero data changes** — loader (`src/lib/inventory/loader.ts`), registry, JSONs untouched (visual layer only; if a derived stat needs a tiny pure helper, put it in the client component, not the loader).
- **Consumer copy:** reuse existing strings wherever possible. Any NEW micro-label (KPI titles, column headers, sort tooltips) must be plain, factual Hebrew with NO claims — and you must LIST every new string verbatim in the return (they go through the content two-gate before the owner sees the page). No marketing language, no "X, not Y" phrasing, no em dashes.
- **Do not touch** `expansion-section.tsx`, comparison pages, hashvaot routes, or any `src/data/` file. Owner description freeze in force.
- OFF ban absolute. You are the EXECUTOR — do NOT spawn subagents.

## 4. Gates + return
1. `npm run lint` exit 0 (CI is now genuinely green — keep it that way; no new warnings beyond baseline). 2. `npx tsc --noEmit` exit 0. 3. `npm run build` exit 0, `/catalog` in route list. 4. **Render verification (real DOM, Playwright or dev-server screenshots): desktop 1280px + mobile 390px screenshots of the full page saved under `tasks/returns/P472_screens/`** — the orchestrator and Design critic review these. 5. KPI numbers on the rendered page must equal counts you compute independently from the registry data (state both).
Return to `tasks\returns\P472_contract.md` (NOT P472_return.md): component inventory (files created/modified + real sha256s), every new consumer string verbatim, the 5 gate results with exit codes, bundle-size delta, screenshot paths. Full Return Contract v1 JSON. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P472_contract.md --root C:\bari_wt_t465` exit 0 (PowerShell). Commit code + contract + screenshots. Propose RETURNED.
