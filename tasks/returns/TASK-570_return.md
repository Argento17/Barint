# TASK-570 Return — Shelf Watch pilot: weekly label-change monitor for cereals + bread (alert-only)

## What this is

Built and ran the Shelf Watch pilot end to end: design doc → canary/adapter-health check →
monitor script → one real supervised run → weekly Windows Scheduled Task. Alert-only —
no score touched, no write to `bari-web/src/data/comparisons/`, no auto-publish. Output is a
report JSON file only.

## Design decisions (full detail in the design doc)

`01_framework/operations/shelf_watch/shelf_watch_pilot_v1.md`

- **Snapshot baseline = the LIVE SERVED frontend JSON**
  (`bari-web/src/data/comparisons/cereals_frontend_v2.json` — confirmed the actual import in
  `cereals-page-data.ts`; `bread_frontend_v4.json` — confirmed the actual import in
  `bread-comparison-page-data.ts`), **not** a BSIP0/BSIP1 run-dir artifact. Memory
  `published_scores_not_trace_derivable` (TASK-563) established served `run_id` ≠ the
  config's run directory for 14/16 shelves — the run-dir path is not reliable ground truth
  right now, but the served JSON is mechanically what a shopper sees today, which is exactly
  what this monitor protects. Flagged as a scope-fit decision, not a workaround, in the
  design doc §1.
- **Retailer scope = Shufersal only.** Both live corpora are 100% Shufersal identity (census:
  20/20 cereals, 23/23 bread). Running canary/health checks against Hazi Hinam/Yohananof/Tiv
  Taam — retailers with zero products in the watched corpus — would be theater. Documented as
  a deliberate scope-fit in design doc §2/§9, with an explicit note that a Shelf Watch canary
  pass is NOT a fleet-wide BSIP0 health signal.
- **Found + fixed defect, disclosed rather than worked around:** the newer
  `03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py` (crawlee/Playwright engine)
  returns **HTTP 404 on every request** — its URL template
  (`.../online/he/A{barcode}`) is stale. Verified live 2026-07-10 that Shufersal's real
  per-product path is `.../online/he/p/p_{barcode}` (direct barcode fetch, no search needed;
  `ld+json` `gtin13` matches the barcode on every product checked). Shelf Watch reuses the
  `requests`+`BeautifulSoup` technique from `shufersal_cereals/01_scrape_cereals.py`
  (the engine that actually built the corpus), not the broken one. This is a standing defect
  in `01_acquire_shufersal.py` that should not be relied on elsewhere until fixed — flagging
  it here per the "raise glitches immediately" rule; not in scope to fix in this task.
- **Classification thresholds:** any numeric nutrition delta beyond a `0.05` float epsilon =
  `nutrition_drift` (no business-tolerance band, per the build order's explicit
  "any numeric change = nutrition_drift"); ingredient token-set change (comma/semicolon-split
  items compared as a whitespace-collapsed multiset) = `ingredient_change`; pure
  whitespace/punctuation/ordering = `cosmetic`; `page_gone` reserved for a positive-evidence
  signal only (HTTP 404 on the direct barcode URL, or a `gtin13` mismatch after redirect) —
  anything less certain falls back to `scrape_failed` (discarded, never drift, per the
  missing-data rule).

## A genuine finding from building this (not glossed over)

The **first** real run on the actual corpus came back with 13/43 (30%) flagged
`ingredient_change` — implausibly high for "expect mostly no-change." Rather than ship that
as the pilot's report, I traced every one of the 13 by hand (raw HTML inspection, not
assumption) and found the cause was **my own extraction, not real label drift**:

1. My first-pass extractor picked the first DOM element containing the substring "רכיב",
   which on some product templates is a marketing badge ("• רכיב מס' 1 חיטה מלאה...") that
   precedes the real ingredients section, or a broad container that bled into the adjacent
   nutrition-table/disclaimer text. Fixed by targeting the precise container
   (`div.componentsText`, confirmed via raw HTML inspection to be the sibling of the
   `div.title > div.mainInfo` "רכיבים" heading).
2. Shufersal's own live HTML contains a genuine rendering quirk: an internal line break
   sometimes serializes as a bare literal `n`/`r` character (confirmed in raw response bytes,
   e.g. `"(54%)n(מכיל גלוטן)"` instead of `"(54%) (מכיל גלוטן)"`) — not a parsing artifact.
   Collapsed via a regex that protects vitamin/additive codes (`B3`, `E920`, `E341iii`).
3. The baseline corpus's original scraper inconsistently concatenated the ingredients section
   with a trailing allergen/claims clause ("... מכיל גלוטן חיטה" / "עלול להכיל..."). Rather
   than try to reproduce that inconsistency, both baseline and fresh text are now trimmed to
   the same "core ingredients only" scope (boundary markers + trailing-claim-sentence trim,
   applied symmetrically) before diffing.

After the fix: **37/43 no_change, 4/43 cosmetic (site-side spacing noise, correctly
downgraded), 2/43 ingredient_change (genuine — see below), 0 nutrition_drift, 0 page_gone,
0 scrape_failed.** Re-ran twice on the corrected code — identical result both times
(`shelf_watch_20260710T153036Z.json` and `shelf_watch_20260710T153237Z.json`), confirming
this isn't flaky. This distribution matches "expect mostly no-change; that is a valid
result" from the build order. The two flagged findings are real, substantive composition
differences on two bread products (see below) — not artifacts.

## The real supervised run (acceptance test) — full result

Run ID `shelf_watch_20260710T153237Z` (report:
`03_operations/shelf_watch/runs/shelf_watch_20260710T153237Z.json`):

- Canary: 3/3 healthy (`5010029000061`/cereals, `7297488098688`/cereals,
  `7290016245325`/bread — all `status: scraped` with a parsed nutrition panel).
- `products_total: 43` (20 cereals + 23 bread, byte-matching each frontend JSON's
  `_meta.product_count`).
- Class distribution: `{"no_change": 37, "cosmetic": 4, "ingredient_change": 2}` — by
  category: cereals `{no_change: 16, cosmetic: 4}`, bread `{no_change: 21,
  ingredient_change: 2}`.
- `flagged_for_digest`: 2 items, `digest_worthy: true`.

**The 2 flagged items (genuine ingredient_change, digest-worthy):**
- `2079927` ("לחם דגנים מלא"): whole-wheat-flour weight-share changed 83%→100% (of flours) /
  45%→57% (of the loaf); grain-blend share 7%→5%; sesame/flax/pumpkin seed composition
  reworded; emulsifier `E471` no longer listed, `E481` still present.
- `7290016967074` ("לחם חיטה מלאה"): loaf weight-share 50%→47.4%; seed blend 25.4%→8.2%;
  emulsifier set changed (`E471`/`E481` combination → `E472e` alone alongside `E330`/`E300`).

Neither product showed a nutrition_drift (all 6 compared macros matched within epsilon on
both) — these are ingredient-composition-only deltas, exactly the `ingredient_change` class
they're bucketed under.

**The 4 cosmetic items** (cereals `5900020036407`, `5900020012814`, `7290107647731`,
`72968`): all pure site-side whitespace noise inside an otherwise-identical ingredient list
(e.g. `"תערובת"` rendered `"תע רובת"` on the live fetch — confirmed present in Shufersal's own
raw HTML, not a BeautifulSoup artifact) — correctly downgraded to `cosmetic`, not flagged.

## Scheduled task registration proof

`schtasks /query /tn "Bari - Shelf Watch (local)" /v /fo list`:

```
TaskName:                             \Bari - Shelf Watch (local)
Next Run Time:                        7/12/2026 3:00:00 AM
Status:                               Ready
Logon Mode:                           Interactive only
Task To Run:                          c:\Bari\.venv\Scripts\python.exe "C:\Bari\03_operations\shelf_watch\shelf_watch.py"
Start In:                             C:\Bari\03_operations\shelf_watch
Scheduled Task State:                 Enabled
Schedule Type:                        Weekly
Start Time:                           3:00:00 AM
Start Date:                           7/10/2026
Days:                                 SUN
Months:                               Every 1 week(s)
```

Registered via `03_operations/shelf_watch/register_shelf_watch_task.ps1` (mirrors
`hebrew_health_scan/register_local_scan_task.ps1` — `-StartWhenAvailable`, idempotent
re-registration, `-Unregister` switch available). Weekly Sunday 03:00 local, off-hours,
distinct from the Hebrew Health Scan's daily 08:30 slot and Project Comp's 20:30 slot.

## Encoding discipline

All Hebrew I/O in `shelf_watch.py` goes through `sys.stdout.reconfigure(encoding="utf-8",
errors="replace")` / `sys.stderr.reconfigure(...)` at the top of the script and
`encoding="utf-8"` / `"utf-8-sig"` on every file read/write — no Hebrew was ever piped through
`python -c` or a PowerShell text cmdlet in the shipped script (the debugging session used
`python -c` with file-based `utf-8` writes + the Read tool to inspect Hebrew safely, per the
same discipline, never printing Hebrew to the corrupting cp1252 console).

## Not done / out of scope (honest gaps)

- No structured owner-digest queue wired up yet — `flagged_for_digest` /
  `digest_worthy` are computed and written into the report, but plugging them into the actual
  weekly digest mechanism is a follow-up if this pilot is extended past cereals + bread
  (documented in the design doc §9).
- `page_gone` detection is conservative by design (HTTP 404 or barcode-mismatch on redirect
  only) — no live case of this class was observed in the real run, so it is untested against
  a genuine example, only against the abort-path logic.
- Single-retailer (Shufersal) scope matches the current corpus exactly but is not a
  general BSIP0-fleet health check.
- The stale `01_acquire_shufersal.py` URL-template defect found during this task is flagged,
  not fixed — out of scope for this pilot.
- Nutrition epsilon (`0.05`) has not been stress-tested against repeated real-world parser
  jitter beyond this pilot's 2 consecutive identical runs; if a future run shows spurious
  nutrition_drift on an unchanged product, that is a tuning follow-up, not assumed away here.

## Validator

```
python 03_operations\validators\validate_return.py --md tasks\returns\TASK-570_return.md
```

Exit code: 0 (PASS) — see `commands_run`.

```json
{
  "task": "TASK-570",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "01_framework/operations/shelf_watch/shelf_watch_pilot_v1.md", "action": "created", "sha256": "ebb181e6f72bec391bc53848a2c90a470359fe69038eb3fa60355a24b0b740d6"},
    {"path": "03_operations/shelf_watch/shelf_watch.py", "action": "created", "sha256": "6f2f33fc70eb133ebb6c99a9569e3a26f81c87d92e6aa0ef176db184e712743c"},
    {"path": "03_operations/shelf_watch/register_shelf_watch_task.ps1", "action": "created", "sha256": "2694dca96cdb1a78d3db2d61554638c958c449a8a34ea2106aacc8c59ba2164d"},
    {"path": "03_operations/shelf_watch/runs/shelf_watch_20260710T153036Z.json", "action": "created", "sha256": "f6b2567763cd27a75431446a006399a9d5f89bdb11a9eb932517b56eb1a35436"},
    {"path": "03_operations/shelf_watch/runs/shelf_watch_20260710T153237Z.json", "action": "created", "sha256": "e068d3f33579e079833d2857d2d14f2ffe5a5d859d8580bbe6fc0fddbe19fe8f"}
  ],
  "counts": {
    "products_total": "43/43 (20 cereals + 23 bread; matches cereals_frontend_v2.json _meta.product_count=20 and bread_frontend_v4.json _meta.product_count=23; not a sampled subset -- every product in both served corpora was fetched)",
    "canary_healthy": "3/3 (5010029000061, 7297488098688, 7290016245325 — all status=scraped with a parsed nutrition panel; source: runs/shelf_watch_20260710T153237Z.json adapter_health.canary_results)",
    "class_distribution": "6-class histogram over 43 products: no_change=37, cosmetic=4, ingredient_change=2, nutrition_drift=0, page_gone=0, scrape_failed=0 -- min=0, max=37, median=1.0, stdev(pop)=13.42, most_common=no_change(37) (source: runs/shelf_watch_20260710T153237Z.json counts, re-derivable via: python -c \"import json,statistics; d=json.load(open('03_operations/shelf_watch/runs/shelf_watch_20260710T153237Z.json',encoding='utf-8')); v=list(d['counts'].values())+[0]*(6-len(d['counts'])); print(d['counts'], 'stdev', statistics.pstdev(v), 'median', statistics.median(v))\")",
    "class_distribution_by_category": "breakfast_cereals (n=20): no_change=16, cosmetic=4, all-other-classes=0, median=0, most_common=no_change(16); bread (n=23): no_change=21, ingredient_change=2, all-other-classes=0, median=0, most_common=no_change(21) (source: same run file, grouped by product.category; full per-category listing, not a sample -- both categories' entire served corpus)",
    "flagged_for_digest": "2/43 (both bread, genuine composition deltas — barcodes 2079927 and 7290016967074; source: runs/shelf_watch_20260710T153237Z.json flagged_for_digest)",
    "reproducibility_check": "2/2 consecutive runs on the fixed code produced identical class_distribution (shelf_watch_20260710T153036Z.json and shelf_watch_20260710T153237Z.json both: no_change=37, cosmetic=4, ingredient_change=2)",
    "false_positive_ingredient_change_diagnosed_and_fixed": "13/43 on the first real run (before the componentsText/boundary-marker/stray-letter fixes described above) -> 2/43 on the corrected code, with each of the 13 individually traced to a named root cause, not assumed away"
  },
  "commands_run": [
    {"cmd": "python 03_operations/shelf_watch/shelf_watch.py --selftest", "exit_code": 0},
    {"cmd": "python 03_operations/shelf_watch/shelf_watch.py --canary-only", "exit_code": 0},
    {"cmd": "python 03_operations/shelf_watch/shelf_watch.py", "exit_code": 0},
    {"cmd": "powershell -ExecutionPolicy Bypass -File \"C:\\Bari\\03_operations\\shelf_watch\\register_shelf_watch_task.ps1\"", "exit_code": 0},
    {"cmd": "schtasks /query /tn \"Bari - Shelf Watch (local)\" /v /fo list", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\TASK-570_return.md", "exit_code": 0}
  ],
  "not_done": [
    "flagged_for_digest not yet wired into an actual owner-digest delivery mechanism (report file only, per pilot scope)",
    "page_gone class has zero real examples in this run (only exercised via the abort-path/unit logic, not a live 404 case)",
    "01_acquire_shufersal.py's stale URL template (found during this task) is flagged, not fixed -- out of scope",
    "nutrition epsilon (0.05) validated only against 2 consecutive identical runs, not stress-tested over multiple weeks of real jitter",
    "Hazi Hinam / Yohananof / Tiv Taam canary coverage intentionally NOT built -- zero products from those retailers are in the watched corpus (documented scope-fit, not a gap to silently claim as covered)"
  ],
  "self_check": "Acceptance test per the build order: 'ONE real supervised run now ... run it, include the actual report in your return. Expect mostly no-change; that is a valid result.' Observed: ran the canary (3/3 healthy) then the full corpus (43/43 products fetched, 0 scrape_failed) twice on the corrected code, both times yielding no_change=37/43 (86%), cosmetic=4/43, ingredient_change=2/43 (both genuine, individually verified against raw HTML), 0 nutrition_drift, 0 page_gone -- satisfies 'mostly no-change' while still proving the pipeline surfaces a real, non-trivial finding when one exists. The first real run's 13/43 false-positive rate was NOT shipped as the deliverable; it was traced to 3 named root causes in the extraction logic, fixed, and re-verified twice before being reported here, per the self-gating duty (never report a number without recomputing it from the committed artifact)."
}
```
