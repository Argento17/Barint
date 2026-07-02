# P474 Contract — TASK-466 rework: manifest derives from app routes (not registry)

**Worktree:** `C:\bari_wt_t466` (branch `feat/task466-live-manifest`)
**Status proposed:** RETURNED

## Summary

Reworked `live_manifest.py` so the source of truth is `bari-web/src/app/hashvaot/*/page.tsx` (22 routes: 16 comparison, 2 hub, 4 other-vertical). Each comparison route statically resolves `page.tsx → page-data TS → comparisons JSON → config stem`. `comparisonCategoryRegistry` is now an annotation (`in_comparison_registry`), not the filter. `conformance.py --all` reads 16 manifest-derived config stems (superset of old 18 minus 2 provable non-page staging/discard configs). Added `.gitignore` entries for regenerable regression reports (and removed them from git tracking) so local router runs no longer dirty the tree.

## Full manifest table (22/22 routes)

| route_slug | type | in_registry | frontend_json | config_stem | gaps |
|------------|------|:-----------:|---------------|-------------|------|
| (index) | hub | no | — | — | — |
| bread | comparison | yes | bread_frontend_v4.json | bread | — |
| breakfast-cereals | comparison | yes | cereals_frontend_v2.json | cereals | — |
| brined-cheeses | comparison | no | brined_cheeses_frontend_v2.json | brined_cheeses | — |
| cakes | comparison | no | cakes_hard_cookies_frontend_v1.json | cakes | — |
| cheese | comparison | yes | cheese_frontend_v5.json | cheese | — |
| chocolate-bars | comparison | no | chocolate_bars_frontend_v1.json | chocolate_bars | — |
| chocolate-tablets | comparison | no | chocolate_tablets_frontend_v1.json | chocolate_tablets | — |
| cookies-coffee | comparison | no | cookies_coffee_frontend_v2.json | cookies_coffee | — |
| crackers | comparison | yes | crackers_frontend_v1.json | crackers | — |
| granola | comparison | yes | granola_frontend_v2.json | granola | — |
| hard-cheeses | comparison | no | hard_cheeses_frontend_v4.json | hard_cheeses | — |
| hummus | comparison | yes | hummus_frontend_v5.json | hummus_shelfrel_002 | — |
| juices | comparison | no | juices_frontend_v3.json | juices | — |
| magnesium | other-vertical | no | — | — | — |
| milk-comparison | comparison | no | milk_frontend_v1.json (+ milk-comparison.json aux) | milk | — |
| personal-care | other-vertical | no | — | — | — |
| protein-bars | comparison | no | protein_combined_frontend_v2.json | protein_bars | — |
| raw-foods | other-vertical | no | — | — | — |
| snacks | comparison | yes | snacks_frontend_v5.json | snacks | — |
| supermarket | hub | no | — | — | — |
| supplements | other-vertical | no | — | — | — |

**Catalog:** `/hashvaot/catalog` page.tsx not present (noted in manifest `_meta.catalog_note`).
**Comparison gaps:** 0/16 comparison routes carry a `gaps[]` field (all chains + configs resolve).
**Headline finding:** 9/16 live comparison routes are bespoke adapters outside `comparisonCategoryRegistry` (brined-cheeses, cakes, chocolate-bars, chocolate-tablets, cookies-coffee, hard-cheeses, juices, milk-comparison, protein-bars). P473's registry-only manifest missed these entirely.

### Stem-vs-route naming mismatches (explicit)

| route_slug | config stem | page-data module | notes |
|------------|-------------|------------------|-------|
| milk-comparison | milk | milk-page-data.ts | also imports legacy `bari-web/src/data/milk-comparison.json` |
| breakfast-cereals | cereals | cereals-page-data.ts | route slug ≠ config stem |
| hummus | hummus_shelfrel_002 | hummus-comparison-page-data.ts | shelfrel config name |
| cakes | cakes | cakes-hard-cookies-page-data.ts | route `cakes`, JSON `cakes_hard_cookies_*` |
| protein-bars | protein_bars | protein-bars-comparison-page-data.ts | JSON `protein_combined_frontend_v2.json` |

## Old-18 vs new-16 reconciliation

| set | count | members |
|-----|------:|---------|
| **Before** (`--all` = every `configs/*.json` stem) | 18/18 | bread, brined_cheeses, cakes, cereals, cheese, chocolate_bars, chocolate_tablets, cookies_coffee, crackers, crackers_frontend_discards_v1, granola, hard_cheeses, hummus_shelfrel_002, juices, milk, protein_bars, snacks, snacks_task413_staging |
| **After** (`--all` = manifest comparison routes with config) | 16/16 | bread, brined_cheeses, cakes, cereals, cheese, chocolate_bars, chocolate_tablets, cookies_coffee, crackers, granola, hard_cheeses, hummus_shelfrel_002, juices, milk, protein_bars, snacks |

**Excluded (2), with justification:**

1. **crackers_frontend_discards_v1** — discard-record schema (`schema: crackers_frontend_discards_v1`), not a live page config. No `hashvaot/*/page.tsx` import chain references it; only audit-text mention in `crackers_frontend_v1.json` `_meta`. Provable non-page.
2. **snacks_task413_staging** — staging reproducer config. Live route chain is `snacks/page.tsx` → `snacks-comparison-page-data.ts` → `snacks_frontend_v5.json` → `configs/snacks.json`. No route imports the staging baseline. Provable non-page.

**Net:** new set is a proper superset of live pages vs P473's 7-stem registry narrowing; recovers 9 bespoke routes P473 dropped.

## Conformance per-category (`--all`, 16 stems)

| stem | route | result | notes |
|------|-------|--------|-------|
| bread | bread | **NON-CONFORMING** | pre-existing HARD-3 baseline_served (config v3 vs page v4) |
| brined_cheeses | brined-cheeses | CONFORMS | |
| cakes | cakes | CONFORMS | |
| cereals | breakfast-cereals | CONFORMS | |
| cheese | cheese | **NON-CONFORMING** | pre-existing HARD-3 baseline_served (config v4 vs page v5) |
| chocolate_bars | chocolate-bars | CONFORMS | |
| chocolate_tablets | chocolate-tablets | CONFORMS | |
| cookies_coffee | cookies-coffee | CONFORMS | |
| crackers | crackers | CONFORMS | |
| granola | granola | CONFORMS | |
| hard_cheeses | hard-cheeses | CONFORMS | |
| hummus_shelfrel_002 | hummus | CONFORMS | |
| juices | juices | CONFORMS | |
| milk | milk-comparison | CONFORMS | |
| protein_bars | protein-bars | CONFORMS | |
| snacks | snacks | CONFORMS | |

**Summary:** 14/16 conform, 2/16 non-conforming (bread, cheese HARD-3 only — pre-existing, not introduced by P474).

## Router regression: local vs CI at 6284546a

Re-ran `run_router_regression.py` locally. **Process exit code is 0** (the script logs `WARNING ROUTER REGRESSION: 1 failures` but never calls `sys.exit(1)` — P473 incorrectly reported exit 1). CI at `6284546a` is also green for the same reason: GitHub Actions checks shell exit code only.

The one **internal corpus FAIL** is `dairy_flavor_contamination_biscuit`: router returns `category=biscuit, anchor_override=True` (expected `snack_bar_granola, anchor_override=False`). Root cause: EV-058 biscuit hard anchor `("ביסקוויט", "biscuit", "plain_biscuit", 0.88)` in `router_v2.py` matches the synthetic product name `ביסקוויט בטעם יוגורט` before snack_bar_granola scoring wins. `router_v2.py` is **byte-identical** between `6284546a` and this branch (`git diff 6284546a HEAD -- router_v2.py` empty) — CI would hit the same internal FAIL on a fresh run. The committed `router_regression_001.md` (dated 2026-06-09) shows PASS because it predates the biscuit anchor; it is now untracked + gitignored so reruns do not dirty the tree. Not fixed per task boundary.

## Hygiene

- `git checkout -- 03_operations/reports/regression/*.md` restored committed snapshots, then `git rm --cached` on both report files.
- Added both paths to `.gitignore` — every regression run regenerates them under repo-relative `REPORT_ROOT` (`_REPO_ROOT / "03_operations/reports/regression"`).

## Gate outputs

| # | command | exit |
|---|---------|-----:|
| 1 | `python 03_operations/page_generator/live_manifest.py` | 0 |
| 2 | `python 03_operations/page_generator/live_manifest.py --check` | 0 |
| 3 | `python 03_operations/page_generator/live_manifest.py --check --simulate-drift` | 1 |
| 4 | `python 03_operations/page_generator/conformance.py --all` | 1 |
| 5 | `python 03_operations/bsip2/proto_v0/src/run_router_regression.py` | 0 |
| 6 | `python 03_operations\validators\validate_return.py --md tasks\returns\P474_contract.md --root C:\bari_wt_t466` | 0 |

## Files changed

| file | action |
|------|--------|
| `03_operations/page_generator/live_manifest.py` | modified (route-derived rewrite) |
| `03_operations/page_generator/live_manifest.json` | modified (22 routes, 16 comparison) |
| `03_operations/page_generator/conformance.py` | modified (`routes[]` schema + comparison-only stems) |
| `.gitignore` | modified (regression report paths) |
| `03_operations/reports/regression/router_regression_001.md` | deleted from index (still on disk, gitignored) |
| `03_operations/reports/regression/regression_check_001.md` | deleted from index (still on disk, gitignored) |

```json
{
  "task": "P474",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/page_generator/live_manifest.py", "action": "modified", "sha256": "f74df06cad4ba1920045552845caed563214ad9bf6f0c44a58b98e241d55b785"},
    {"path": "03_operations/page_generator/live_manifest.json", "action": "modified", "sha256": "14a2a93aa8c13fa36c6949ca67729970fe39ec164f7d8cf21778cdf66e998030"},
    {"path": "03_operations/page_generator/conformance.py", "action": "modified", "sha256": "03860015f5f7871a9bb3cc50ecd07b81426f9cdb67f98d1e967238486cf83e1c"},
    {"path": ".gitignore", "action": "modified", "sha256": "f4d8e79d0c1767e18b1e923954c353b1a920659e621f91a500689a84f7edf804"}
  ],
  "counts": {
    "manifest_routes": "22/22 (live_manifest.json routes[] vs hashvaot/*/page.tsx dirs; histogram: comparison=16, hub=2, other-vertical=4; most_common=comparison(16))",
    "manifest_comparison_routes": "16/16 (type=comparison in live_manifest.json; 0 gaps[] entries)",
    "manifest_registry_annotation": "7/16 (in_comparison_registry=true on comparison routes; bespoke-outside-registry=9/16)",
    "conformance_stems_before": "18/18 (configs/*.json non-_generated stems; histogram: 1 stem each, min/max=1/1)",
    "conformance_stems_after": "16/16 (manifest_config_stems from live_manifest.json routes[] type=comparison with config_json)",
    "conformance_conforming": "14/16 (conformance.py --all; non_conforming=2 bread+cheese HARD-3; most_common outcome=conform; min/max conform per stem=0/1)",
    "orphan_config_warns": "2/2 (live_manifest.py --check; crackers_frontend_discards_v1 + snacks_task413_staging; most_common=1 warn each)",
    "router_regression_internal": "15/16 PASS, 1/16 FAIL (run_router_regression.py corpus; FAIL=dairy_flavor_contamination_biscuit; most_common=PASS)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/page_generator/live_manifest.py", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/live_manifest.py --check", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/live_manifest.py --check --simulate-drift", "exit_code": 1},
    {"cmd": "python 03_operations/page_generator/conformance.py --all", "exit_code": 1},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_router_regression.py", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P474_contract.md --root C:\\bari_wt_t466", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "live_manifest.py --check exits 0 on committed tree; conformance --all evaluates 16 manifest-derived stems (superset of live pages vs P473's 7); --simulate-drift exits 1"
}
```