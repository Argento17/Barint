# Shelf Watch — Pilot v1 (TASK-570)

**Status:** BUILT, first supervised run executed 2026-07-10. Alert-only. Owner-approved
2026-07-10, pilot scope only (cereals + bread).

## 0. What this is / is not

Shelf Watch is a **weekly label-change monitor**, not a re-scoring pipeline. It re-fetches
the nutrition panel + ingredients text for every product currently **live and displayed**
in the cereals and bread comparison pages, diffs the fresh fetch against what is currently
shown, classifies each product's delta, and writes a report. It never touches a score, never
writes to `bari-web/src/data/comparisons/`, never auto-publishes anything. Its only output is
a report file plus (when something is worth a human's attention) a flag consumed by the
owner digest.

This is a pilot: 2 categories, weekly cadence, hand-reviewed for at least the first several
runs before any auto-escalation logic is trusted.

## 1. Snapshot source — "last known" per product

**Decision: the baseline is the LIVE SERVED frontend JSON, not a BSIP0/BSIP1 run-dir
artifact.**

- Cereals: `C:\bari\bari-web\src\data\comparisons\cereals_frontend_v2.json` (confirmed live
  via `cereals-page-data.ts` import — `import rawCorpus from
  "@/data/comparisons/cereals_frontend_v2.json"`). 20 products, all retailer `shufersal`.
- Bread: `C:\bari\bari-web\src\data\comparisons\bread_frontend_v4.json` (confirmed live via
  `bread-comparison-page-data.ts`). 23 products, all retailer `shufersal`.

**Why not the BSIP1/BSIP0 run directory** (e.g. `03_operations/bsip1/run_cereals_008/output`
named in `cereals_frontend_v2.json`'s own `_meta.corpus_dirs`): memory
`published_scores_not_trace_derivable` (TASK-563) established that for 14/16 live shelves the
served `run_id` does not match the config's run directory — the run-dir↔served mapping is
**not reliable ground truth** right now. The frontend JSON has no such ambiguity: it is
*mechanically* what a shopper sees today. A label-change monitor exists to protect what is
currently shown, so diffing against the served JSON is the only choice that can't be
undermined by the TASK-563 landmine. This is a **scope-fit decision, not a workaround** — if
BSIP0 run-dir traceability is fixed later, Shelf Watch can re-point at the true run artifact,
but until then the served JSON is the more honest "last known" reference.

**Field mapping used for the diff** (frontend JSON → canonical, both per-100g):
`expansion.nutrition.energyKcal → energy_kcal`, `.protein → protein_g`, `.sugar → sugars_g`,
`.fat → fat_g`, `.fiber → dietary_fiber_g`, `.sodium → sodium_mg`, `.ingredients → ingredients
text`. The frontend JSON does not carry `carbs`/`saturated_fat` — those two fields are excluded
from the diff (nothing to compare against); this is a known, documented gap, not silently
dropped data.

## 2. Re-fetch method — reusing the real engine, not a new one

**Retailer scope for THIS pilot: Shufersal only.** Both live corpora are 100% Shufersal
identity (`retailer: "shufersal"` on every one of the 43 products, confirmed by census over
both frontend JSONs). The BSIP0 fleet also includes Hazi Hinam / Yohananof / Tiv Taam, but
none of those retailers appear in the corpus being watched — running canary/health checks
against retailers with zero products in scope would be theater, not verification. **This is a
deliberate scope-fit, flagged rather than silently narrowed**: if a future category pulls
products from the other 3 fleet members, Shelf Watch's canary step must be extended to cover
them before that category is added to its watch list.

**Fetch path:** direct product-page GET, same technique the corpus was actually built with
(`03_operations/bsip0/scrape/shufersal_cereals/01_scrape_cereals.py::_parse_product_page`) —
plain `requests` + `BeautifulSoup`, **not** the newer `crawlee`/Playwright-based
`shufersal/01_acquire_shufersal.py` engine. That engine was probed live during this task's
build and returns **HTTP 404 on every request** — its `SHUFERSAL_PRODUCT_URL =
".../online/he/A{barcode}"` URL template is stale (Shufersal's real per-product path is
`/online/he/p/p_<barcode>`, confirmed live below). This is a **found defect**, not a
workaround choice: `01_acquire_shufersal.py` is currently non-functional for direct-barcode
fetch and should not be relied on elsewhere until fixed (flagged to Product/whoever owns that
file next; out of scope to fix here).

**Verified live 2026-07-10** (3 canary barcodes, see §3): `GET
https://www.shufersal.co.il/online/he/p/p_<barcode>` → HTTP 200, redirects to the canonical
category-path URL, page's `ld+json` `Product.gtin13` matches the requested barcode. Shufersal's
internal product code is literally `P_<EAN13>` for every product checked. No search step
needed — barcode fetch is direct.

**Parsing:** nutrition via the shared canonical parser
`03_operations/bsip0/scrape/_shared/bsip0_nutrition.py::parse_nutrition_list` +
`parse_nutrition_numeric` (the same module every Shufersal BSIP0 scraper already routes
through — the EV-026/TASK-142A total-fat-overwrite fix lives there once, not per-scraper).
Ingredients via the same `"רכיב"`-label-then-container-text technique as
`01_scrape_cereals.py`. No OFF, no fallback source, ever.

## 3. Canary / adapter-health check (build order step 2)

Before any diffing, fetch **2-3 known-stable barcodes** and require ALL of them to come back
with a parseable panel (gtin13 match + at least one numeric nutrition field). If any canary
fails, the whole run **aborts with `adapter_unhealthy`** — no diff, no report content beyond
the abort record — rather than emitting comparisons built on a broken fetch.

Canary set (one from each category, arbitrary but real, first product in each corpus by
served rank):
- `5010029000061` — cereals rank 1 ("דגני בוקר" / wheat biscuit cereal)
- `7297488098688` — cereals rank 2 ("פצפוצי אורז ללת\"ס" / puffed rice)
- `7290016245325` — bread rank 1

All 3 verified live 2026-07-10 (see run log) with HTTP 200 + gtin13 match. Real run's own
canary step re-verifies this on every scheduled invocation — a canary pass today does not
exempt future runs.

## 4. Diff fields + classification thresholds

Six nutrition fields are compared where present in the baseline: `energy_kcal`, `protein_g`,
`sugars_g`, `fat_g`, `dietary_fiber_g`, `sodium_mg`. Plus the ingredients text.

**Per-product classification (most severe wins; a product can trip more than one, the report
keeps the full list, the summary bucket uses the max):**

| Class | Trigger | Severity |
|---|---|---|
| `scrape_failed` | Fetch/parse failed this run (timeout, exception, HTTP non-200/404 with ambiguous cause, no `ld+json` Product block, panel yields zero nutrition fields AND zero ingredients text). **Discarded from the diff — never counted as drift, never re-sourced from another provider** (missing-data discard rule). | n/a — excluded |
| `page_gone` | HTTP 404 **specifically** on the direct `/p/p_<barcode>` URL (a positive "this exact page is gone" signal), OR the page loads (200) but its `ld+json` `gtin13` resolves to a **different** barcode than requested (redirected to an unrelated product). Reserved for strong positive evidence only — anything less certain falls back to `scrape_failed`, per the same discard-not-drift discipline. | High (surfaced) |
| `nutrition_drift` | **Any** numeric change in any of the 6 compared fields, using an epsilon of `0.05` (float/rounding noise only — not a business tolerance band). Per the build-order instruction, this threshold is deliberately NOT lenient: a real reformulation is exactly the kind of small delta (e.g. sodium 110→95) this monitor exists to catch. | High (surfaced) |
| `ingredient_change` | The ingredient list's **token set** differs after cosmetic normalization (see below) — an item added, removed, or its text changed (e.g. a percentage annotation moved) counts as a token-set change. | Medium (surfaced) |
| `cosmetic` | Ingredients differ only in whitespace, punctuation, or ordering — the normalized item-set is identical. | Low (report-only, never flagged for the digest) |
| `no_change` | Nothing differs after normalization. | none |

**Ingredient normalization (defines "cosmetic" conservatively):**
1. Split the ingredient string on `,` / `;` into items.
2. Per item: Unicode NFKC-normalize, collapse internal whitespace to single spaces, strip
   leading/trailing whitespace and stray punctuation (`.`, quotes).
3. Compare the two item lists as **multisets** (`collections.Counter`) — order doesn't matter.
4. Multiset equal → `cosmetic` (or `no_change` if the raw normalized full string was already
   identical). Multiset different → `ingredient_change`.

This means a percentage change inside an item (`"חיטה (95%)"` → `"חיטה (90%)"`) is **not**
silently treated as reordering — the item text differs, so it shows as one item removed / one
item added, correctly bucketed `ingredient_change`. Nothing that changes stated composition can
land in `cosmetic` under this scheme.

**Why no fuzzy tolerance band on nutrition:** the build order explicitly says "any numeric
nutrition change = nutrition_drift." A tolerance band risks the exact failure mode this
monitor exists to prevent (masking a real small reformulation as noise). The only slack is a
`0.05` epsilon to absorb float representation, not measurement variance. If repeated runs on
unchanged products show spurious `nutrition_drift` from HTML-parsing jitter, that is a data
quality finding for a **future** iteration to tune (flagged as a risk below, not assumed away).

## 5. Report format

One JSON file per run at
`03_operations/shelf_watch/runs/shelf_watch_<category_set>_<UTC timestamp>.json`:

```json
{
  "run_id": "shelf_watch_20260710T...",
  "categories": ["breakfast_cereals", "bread"],
  "adapter_health": {"shufersal": "healthy", "canary_results": [...]},
  "baseline_sources": {
    "breakfast_cereals": "bari-web/src/data/comparisons/cereals_frontend_v2.json",
    "bread": "bari-web/src/data/comparisons/bread_frontend_v4.json"
  },
  "products_total": 43,
  "counts": {"no_change": N, "cosmetic": N, "ingredient_change": N, "nutrition_drift": N, "page_gone": N, "scrape_failed": N},
  "flagged_for_digest": [ ...only nutrition_drift / ingredient_change / page_gone items... ],
  "products": [ {barcode, category, name, class, nutrition_diff, ingredients_diff, notes}, ... ]
}
```

**Silent-when-nothing-new:** the report file always writes, every run, whether or not
anything changed — that's the audit trail. But it only counts as **digest-worthy** when
`flagged_for_digest` is non-empty (i.e., at least one `nutrition_drift` / `ingredient_change` /
`page_gone`). All-cosmetic or all-no-change runs write a report and produce **zero** owner-
facing noise. A `scrape_failed`-only run also produces no digest flag by itself (per the
discard rule) but its failure rate is visible in `counts` for the Data Agent to notice if it
trends up.

## 6. Failure semantics

- **Adapter unhealthy** (canary fails): abort before touching the real corpus. Report a
  minimal record (`status: "adapter_unhealthy"`) and nothing else. This IS worth a digest
  flag — a broken monitor is itself a finding.
- **Per-product scrape failure**: discarded from the diff per the missing-data rule. Never
  re-sourced from OFF or any other provider. Logged with a reason string for audit but not
  treated as evidence of anything.
- **Partial corpus failure** (e.g. >30% of one category's products `scrape_failed` in one
  run): not a hard abort in this pilot (a single elevated failure rate could be a transient
  site issue), but the report's `counts.scrape_failed` makes it visible, and repeated high
  failure rates across consecutive runs is a signal to escalate to Product (corpus-scope
  decision) per the Data Agent's standing escalation rule, not something Shelf Watch
  auto-decides.

## 7. Schedule

Weekly, off-hours, LOCAL Windows Scheduled Task — same mechanism as the Hebrew Health Scan
(`01_framework/operations/hebrew_health_scan/register_local_scan_task.ps1` /
`local_scan.py` precedent, itself owner-ruled 2026-07-01 because this repo's cloud lanes
cannot reach `.co.il` domains / cannot push). Registered via
`03_operations/shelf_watch/register_shelf_watch_task.ps1`:
- Task name: `Bari - Shelf Watch (local)`
- Trigger: weekly, Sunday 03:00 local (off-hours, distinct from the Hebrew Health Scan's
  08:30 daily slot and Project Comp's 20:30 evening slot)
- Action: `python 03_operations\shelf_watch\shelf_watch.py`
- `-StartWhenAvailable` so a missed slot (machine off) still fires on next boot.

## 8. Encoding discipline

All Hebrew I/O goes through script files with `sys.stdout.reconfigure(encoding="utf-8",
errors="replace")` at the top and `encoding="utf-8"` (read: `utf-8-sig` tolerant) on every
file open — never Hebrew through `python -c` or a PowerShell text cmdlet (both corrupt
Hebrew in this environment; see memory `hebrew_shell_corruption_and_verify_gotchas`).

## 9. Known risks / not yet built (honest gaps for a pilot)

- No auto-tuning of the nutrition epsilon — if parser jitter produces false-positive drift on
  unchanged products across a few runs, that needs a follow-up, not a silent threshold change.
- `page_gone` detection is conservative by design (HTTP 404 or barcode-mismatch only); a
  product that starts permanently redirecting to a category page for the SAME barcode's
  storefront listing would currently read as `scrape_failed`, not `page_gone`. Acceptable for
  a pilot; would need a real observed case to design against rather than guessing.
- Single-retailer scope (Shufersal only) matches the current corpus exactly but is NOT a
  general BSIP0-fleet health check — do not read a Shelf Watch canary pass as fleet-wide
  health for Hazi Hinam/Yohananof/Tiv Taam.
- This pilot does not yet feed a structured owner digest queue — it writes the report file;
  wiring `flagged_for_digest` into the actual weekly digest mechanism is a follow-up if the
  pilot is extended past cereals + bread.
