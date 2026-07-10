# TASK-579 Return — Fan out `deriveComparisonCardStats` to remaining hashvaot featured cards

## Scope enumeration (all 19 `featured-*-intelligence-card.tsx` files)

| # | Card | Status |
|---|---|---|
| 1 | cheese | Already converted (TASK-568 pilot) |
| 2 | protein-bars | Already converted (TASK-568 pilot) |
| 3 | granola | Already converted (TASK-568 pilot) |
| 4 | breakfast-cereals | **Converted this task** |
| 5 | brined-cheeses | **Converted this task** |
| 6 | cakes-hard-cookies | **Converted this task** |
| 7 | chocolate-bars | **Converted this task (partial — see below)** |
| 8 | chocolate-tablets | **Converted this task (partial — see below)** |
| 9 | cookies-coffee | **Converted this task** |
| 10 | crackers | **Converted this task** |
| 11 | hard-cheeses | **Converted this task** |
| 12 | hummus | **Converted this task** |
| 13 | juices | **Converted this task** |
| 14 | milk | **Converted this task** |
| 15 | snacks | **Converted this task** |
| 16 | yogurt (spoonable) | **Converted this task** |
| 17 | yogurt-drinks | **Converted this task** |
| 18 | magnesium | **Excluded** — tracked as TASK-578 |
| 19 | bread (featured-bread-intelligence-card-lite.tsx) | **Excluded** — see below |

17/19 now read from `deriveComparisonCardStats`. 2/19 explicitly excluded with reasons.

## Excluded cards, with reasons

- **magnesium** (`featured-magnesium-intelligence-card.tsx`): `updatedLabel="עודכן יוני 2026"` is
  still a hardcoded literal. `magnesium-page-data.ts` is a fully hand-authored `BariProductVM[]`
  array with **no raw JSON import at all** — no `loadComparisonCorpus`, no `_meta.generated` field
  to derive a date from. This is a structural gap in the data layer, not something a card-level
  conversion can fix. Tracked as **TASK-578** per the coordinator's message; not touched here.
- **bread** (`featured-bread-intelligence-card-lite.tsx`): genuinely cannot map onto
  `ComparisonCardStats` without changing what the stats mean. Its stats come from
  `BREAD_REPORT_STATS = { scanned: 256, sufficient: 81, featured: 31, transparencyGapPercent: 46 }`
  — a hand-typed **pipeline funnel** stat (how many were scanned vs. had enough data vs. were
  curated for display), not a product/grade/score distribution. The underlying data is also a
  different shape entirely: `BreadProduct` (fields: `product_id`, `category_label_he`,
  `displayable`, `confidence_level`), not `BariProductVM`, and bread is not migrated onto
  `loadComparisonCorpus` the way every converted category is. Forcing `deriveComparisonCardStats`
  onto this would either be a type error or would silently redefine what the numbers mean —
  exactly what the "do not force a conversion that alters layout/meaning" instruction warns
  against. Left unconverted; `BREAD_REPORT_STATS` itself remains a real (undisclosed) drift risk
  worth a dedicated follow-up given bread already has one closed drift investigation (TASK-519).

## Two partial conversions (documented, not forced)

- **chocolate-bars**: `productCount` and the "ציון כל המוצרים" (all-products score) stat convert
  cleanly to `stats.productCount` / `stats.ceilingGrade` — verified all 23 products are graded E,
  so ceiling==floor=="E" and the label's uniformity claim holds. The sugar-range stat
  (`"27–60"`) converts via a new `deriveMetricRange` call over `expansion.nutrition.sugar`,
  rounded to whole grams in the label (view-model doctrine: rounding lives in the derivation
  layer, not JSX) — JSON gives 27–59.6, `Math.round` gives 27–60, identical to the literal it
  replaces.
- **chocolate-tablets**: `productCount` and `"B"` ceiling-grade convert cleanly (grades present:
  B/C/D/E, ceiling B — matches). The `"90%"` max-cocoa-percentage stat has **no source field
  anywhere on the product JSON** (checked `expansion.nutrition` and every top-level product key —
  no cocoa/percentage field exists). Left as a literal with an inline comment explaining why; not
  forced.

## Consumer-visible changes: NONE

Every converted stat in this PR is byte-identical to its value before conversion. This was true
by construction for the 12 cards that previously ran a live `.filter((p) => p.grade === "X").length`
or `.filter((p) => p.score != null).length` over the exact same product array
`deriveComparisonCardStats` now receives (mathematically the same computation, just relocated into
the shared module) — cross-checked against the parity script's output for every category (see
Verification). For the 3 cards where a **literal** was being replaced by a **derived** value
(genuine risk of a value changing), each was checked against the real JSON before shipping:

| Card | Field | Old (literal) | New (derived) | Changed? |
|---|---|---|---|---|
| chocolate-bars | sugar g/100g range | `"27–60"` | `Math.round(27)`–`Math.round(59.6)` = `"27–60"` | No |
| chocolate-tablets | category ceiling grade | `"B"` | `stats.ceilingGrade` = `"B"` (grades present: B/C/D/E) | No |
| milk | productCount/scoredCount stats | `milkCorpusMeta.product_count` (18) / `scored_count ?? length` (18) | `stats.productCount` (18) / `stats.scoredCount` (18) | No |

## Bug found and fixed while extending the parity script (not a card change)

While building the manifest entry for cheese in the extended parity script, `node
scripts/validate-corpus.mjs --all` flagged `cheese_frontend_v4.json` as an **orphaned dataset
version** (§4.3). Checked: `cheese-page-data.ts` actually imports `cheese_frontend_v5.json`
(cheese de-anchor go-live, commit `e953c8d6`) — the TASK-568 pilot's parity manifest pointed at
the wrong (orphaned v4) file. **This did not affect any shipped card value** — the cheese card
itself has always consumed `cheeseProducts`/`cheeseCorpusMeta` re-exported from
`cheese-page-data.ts` (which correctly reads v5), never the raw JSON filename directly — only the
*standalone parity script's* file reference was wrong. Verified v4 and v5 carry identical
product/grade/count data as of this writing (47 products, 2×A both files; `scoreLow` differs by
0.4 — 23.4 vs 23.8 — a field neither card renders). Fixed the manifest entry to `v5` with an
inline comment; re-ran the full parity script — still exit 0, cheese numbers unchanged (see
Verification).

## CI wiring

Read `.github/workflows/barint_ci.yml` first (existing style: `frontend` job runs
`actions/setup-node@v4` once, then `npm ci` / `npm run build` / `npm run lint` /
`node scripts/validate-corpus.mjs --all` as sequential named steps under
`working-directory: bari-web`). Added a matching step:

> `- name: Validate featured-card derived stats` / `  run: npm run validate-card-stats`

**Required a same-job Node version bump, disclosed prominently rather than silently changed:**
`validate-card-stats.mjs` dynamic-imports `src/lib/derived/comparison-card-stats.ts` directly (no
build/transpile step) using Node's native TypeScript type-stripping. That capability does not
exist on Node 20 at all — a bare `.ts` import fails immediately with `ERR_UNKNOWN_FILE_EXTENSION`
before any syntax is even parsed (Node 20 only recognizes `.js`/`.mjs`/`.cjs`/`.json`/`.node`/`.wasm`).
It needs Node ≥23.6 to run flag-free, or ≥22.6 with `--experimental-strip-types`. No Node 20
environment was available locally to reproduce the failure directly (only Node 24.15.0 was
installed), so this is stated as a documented fact about Node's ESM loader rather than an
empirical local reproduction — flagging that distinction rather than overclaiming. Bumped the
`frontend` job's `node-version` from `"20"` to `"24"` (matching the version this was verified
against locally) with an inline comment explaining why. The job's other steps (`npm ci`,
`npm run build`, `npm run lint`, `validate-corpus.mjs`) have no Node-20-specific dependency and
were re-verified passing locally under Node 24 (see Verification) — this is a scoped, justified
bump required by the feature being wired in, not a broader infra change. Did not touch the
`e2e-smoke` job's separate Node 20 pin (out of scope — it doesn't run this script).

## Verification

- `npx tsc --noEmit` — 0 errors.
- `npm run lint` — 0 errors, 19 pre-existing warnings (same set as before this task; none in any
  touched file).
- `npm run build` — exit 0, all 305 static pages + all `/hashvaot/*` dynamic routes compiled,
  including all 14 newly-converted cards' import graphs.
- `npm run validate-card-stats` (proved green **before** wiring into CI, per the instruction) —
  exit 0, all 17 converted categories print `productCount`/`scoredCount`/`gradeCounts`/
  `ceilingGrade`/`scoreLow`/`scoreHigh`/`scoreSpread`/`updatedLabel` straight from the raw JSON via
  the real shared module. Full output included below.
- `node scripts/validate-corpus.mjs --all` — exit 0 (0 errors, 1149 pre-existing warnings across
  the whole corpus — unrelated to this task; re-run to confirm the frontend job's other step still
  passes under the bumped Node 24).
- YAML sanity: `python -c "import yaml; yaml.safe_load(open('.github/workflows/barint_ci.yml'))"` —
  parses clean, `frontend` job step list confirmed to include the new step in order.

Raw output of `npm run validate-card-stats` (17/17, exit 0) — indented, not fenced, so this
return's single JSON contract block below stays unambiguous to parse:

    [cheese] cheese_frontend_v5.json
      productCount=47 scoredCount=47 gradeCounts={"A":2,"B":19,"C":9,"D":15,"E":2} ceilingGrade=A
    [protein_bars] protein_combined_frontend_v2.json
      productCount=32 scoredCount=32 gradeCounts={"A":0,"B":1,"C":23,"D":8,"E":0} ceilingGrade=B
    [granola] granola_frontend_v2.json
      productCount=22 scoredCount=22 gradeCounts={"A":0,"B":4,"C":8,"D":8,"E":2} ceilingGrade=B
    [breakfast_cereals] cereals_frontend_v2.json
      productCount=20 scoredCount=20 gradeCounts={"A":0,"B":2,"C":6,"D":10,"E":2} ceilingGrade=B
    [brined_cheeses] brined_cheeses_frontend_v2.json
      productCount=36 scoredCount=36 gradeCounts={"A":3,"B":18,"C":13,"D":2,"E":0} ceilingGrade=A
    [cakes_hard_cookies] cakes_hard_cookies_frontend_v1.json
      productCount=62 scoredCount=62 gradeCounts={"A":0,"B":0,"C":1,"D":1,"E":60} ceilingGrade=C
    [chocolate_bars] chocolate_bars_frontend_v1.json
      productCount=23 scoredCount=23 gradeCounts={"A":0,"B":0,"C":0,"D":0,"E":23} ceilingGrade=E
    [chocolate_tablets] chocolate_tablets_frontend_v1.json
      productCount=35 scoredCount=35 gradeCounts={"A":0,"B":2,"C":6,"D":10,"E":17} ceilingGrade=B
    [cookies_coffee] cookies_coffee_frontend_v2.json
      productCount=117 scoredCount=117 gradeCounts={"A":0,"B":0,"C":9,"D":27,"E":81} ceilingGrade=C
    [crackers] crackers_frontend_v1.json
      productCount=53 scoredCount=53 gradeCounts={"A":9,"B":33,"C":7,"D":4,"E":0} ceilingGrade=A
    [hard_cheeses] hard_cheeses_frontend_v4.json
      productCount=31 scoredCount=31 gradeCounts={"A":1,"B":26,"C":4,"D":0,"E":0} ceilingGrade=A
    [hummus] hummus_frontend_v5.json
      productCount=57 scoredCount=57 gradeCounts={"A":0,"B":2,"C":42,"D":13,"E":0} ceilingGrade=B
    [juices] juices_frontend_v3.json
      productCount=17 scoredCount=17 gradeCounts={"A":6,"B":0,"C":0,"D":7,"E":4} ceilingGrade=A
    [milk] milk_frontend_v1.json
      productCount=18 scoredCount=18 gradeCounts={"A":3,"B":1,"C":6,"D":7,"E":1} ceilingGrade=A
    [snacks] snacks_frontend_v5.json
      productCount=21 scoredCount=21 gradeCounts={"A":0,"B":1,"C":2,"D":6,"E":12} ceilingGrade=B
    [yogurt_spoonable] yogurt_spoonable_frontend_v1.json
      productCount=50 scoredCount=50 gradeCounts={"A":7,"B":21,"C":10,"D":9,"E":1} ceilingGrade=A
    [yogurt_drinks] yogurt_drinkable_frontend_v1.json
      productCount=17 scoredCount=17 gradeCounts={"A":0,"B":5,"C":8,"D":4,"E":0} ceilingGrade=B

**Distribution note (the 17 converted categories are an exhaustive enumeration, not a sample —
given here anyway to satisfy the return contract's Rule 5 self-verification):** per-category
`productCount` across all 17: min 17 (juices, yogurt_drinks), max 117 (cookies_coffee), median 32,
stdev ≈25.1 (n=17; raw values 47,32,22,20,36,62,23,35,117,53,31,57,17,18,21,50,17 — see the full
`validate-card-stats` output above for the per-category source). The 19/19 and 14/14 enumerations
above are the complete file listing (`ls featured-*-intelligence-card.tsx`) and the complete diff
(`git diff --stat`), not samples — both independently reproducible from the artifacts list.

## Not done / out of scope

- magnesium and bread-lite unconverted (reasons above).
- chocolate-tablets cocoa% and the funnel-shaped bread stats remain hardcoded (no source field /
  bespoke shape).
- Dead-code cleanup (`insightLines`/`showInsights` on `ComparisonIntelligenceHero`) explicitly
  NOT done per the coordinator's instruction — separate concern.
- The parity script's static-source-literal-grep hardening (TODO comment in the script from
  TASK-568) still not built.
- `e2e-smoke` job's Node 20 pin left untouched (doesn't run this script; separate concern).

## Commit / PR

Branch `task579-cards-fanout`, stacked on `task568-derived-cards` (per instruction — not rebased).
Commit `2dcecb0d`. Pushed to `origin`. PR (will show pilot+fan-out commits until the pilot merges,
as expected):
https://github.com/Argento17/Barint/pull/new/task579-cards-fanout

```json
{
  "task": "TASK-579",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "ae50de7029311df6785ec6569297751f23d7bf475bb757d5904e817b3d04ccc4"},
    {"path": "bari-web/scripts/validate-card-stats.mjs", "action": "modified", "sha256": "c88f5b88d415635f759799782cb186c3a67ff96b259508d6c98337270eea6789"},
    {"path": "bari-web/src/components/hashvaot/featured-breakfast-cereals-intelligence-card.tsx", "action": "modified", "sha256": "cb1bc7b125da4b742773a87dbc85f5be4dc09fbaa951fa1d0160068e9696144c"},
    {"path": "bari-web/src/components/hashvaot/featured-brined-cheeses-intelligence-card.tsx", "action": "modified", "sha256": "ce81aae77959492ae08a36027c590334ab23c5bbf45d2e805bbdceef25c63c44"},
    {"path": "bari-web/src/components/hashvaot/featured-cakes-hard-cookies-intelligence-card.tsx", "action": "modified", "sha256": "7b74c8c5048d869b30c0f810c5df16d6e61a3ed2e1ca48877d20f3543052d656"},
    {"path": "bari-web/src/components/hashvaot/featured-chocolate-bars-intelligence-card.tsx", "action": "modified", "sha256": "9d5eb1f93f36a889986d8b800f2d11c343e4bca4a5549e8b870d707f6b850eae"},
    {"path": "bari-web/src/components/hashvaot/featured-chocolate-tablets-intelligence-card.tsx", "action": "modified", "sha256": "7767e82bdc8ef31f776a239e116ee0cbd489ae0b299ab0af5f18633a6c241694"},
    {"path": "bari-web/src/components/hashvaot/featured-cookies-coffee-intelligence-card.tsx", "action": "modified", "sha256": "1c7ebeeac3bc151f76ee20e514004e6760fcab91e67eda06a8adfcec8da15bdc"},
    {"path": "bari-web/src/components/hashvaot/featured-crackers-intelligence-card.tsx", "action": "modified", "sha256": "d306fc608a45f802718aed3fed7671afdec488116d43475f485beb79316bc287"},
    {"path": "bari-web/src/components/hashvaot/featured-hard-cheeses-intelligence-card.tsx", "action": "modified", "sha256": "1323bb456352893be7dce118dae76d6ccc152cb6bb20cd7755c56154cbd3a391"},
    {"path": "bari-web/src/components/hashvaot/featured-hummus-intelligence-card.tsx", "action": "modified", "sha256": "9e311e9dead19416a10d20b752471cf23ea9d15b514a370b33a485e254dacd1b"},
    {"path": "bari-web/src/components/hashvaot/featured-juices-intelligence-card.tsx", "action": "modified", "sha256": "a16075e0b894be95c45855728a4bfd1d9e7f179439ee8ad086b381290680672d"},
    {"path": "bari-web/src/components/hashvaot/featured-milk-intelligence-card.tsx", "action": "modified", "sha256": "bceaf233910e9961873df08f97d0f0f62931bb86f447db389dda4230176fcf3b"},
    {"path": "bari-web/src/components/hashvaot/featured-snacks-intelligence-card.tsx", "action": "modified", "sha256": "9150f13d4139097372b70c23fa300eef4a78139139c1ecad2e519397ac8180f7"},
    {"path": "bari-web/src/components/hashvaot/featured-yogurt-drinks-intelligence-card.tsx", "action": "modified", "sha256": "9d31fd9bb74cdfe31cf9ee57ea29d9bc889c4cd64b0c35c0e046186aeca5ecc4"},
    {"path": "bari-web/src/components/hashvaot/featured-yogurt-intelligence-card.tsx", "action": "modified", "sha256": "c1d11e5817ab58e1512bd5423020f6f8a85598f4bba6e0cc68f55bcb41fc9a88"}
  ],
  "counts": {
    "featured_cards_total": "19/19 (ls bari-web/src/components/hashvaot/featured-*-intelligence-card.tsx; exhaustive listing, not a sample)",
    "cards_converted_cumulative": "17/19 (3 pilot TASK-568 + 14 this task)",
    "cards_converted_this_task": "14/14 (breakfast-cereals, brined-cheeses, cakes-hard-cookies, chocolate-bars, chocolate-tablets, cookies-coffee, crackers, hard-cheeses, hummus, juices, milk, snacks, yogurt, yogurt-drinks; exhaustive list, not a sample)",
    "cards_excluded_with_reason": "2/19 (magnesium=TASK-578 no date source, bread-lite=bespoke funnel-stat shape)",
    "partial_conversions": "2/14 (chocolate-bars: sugar range derived, all-products-E ceiling derived; chocolate-tablets: productCount+ceiling derived, cocoa% stays literal, no source field)",
    "consumer_visible_value_changes": "0/17 (every converted stat verified byte-identical to its prior value; 3 literal-to-derived cases cross-checked individually against live JSON, see return body table)",
    "parity_script_categories_passing": "17/17 (npm run validate-card-stats, exit 0)",
    "parity_script_productCount_distribution": "n=17, min=17, max=117, median=32, stdev=25.1 (raw: 47,32,22,20,36,62,23,35,117,53,31,57,17,18,21,50,17 -- source: npm run validate-card-stats output, verbatim per-category productCount)",
    "lint_errors": "0/0 (npm run lint, touched files)",
    "tsc_errors": "0/0 (npx tsc --noEmit)",
    "build_routes_compiled": "305 static + all /hashvaot/* dynamic routes (npm run build, exit 0)",
    "orphaned_dataset_bug_found_and_fixed": "1/1 (cheese parity manifest pointed at orphaned cheese_frontend_v4.json instead of the live cheese_frontend_v5.json; fixed, re-verified identical values)"
  },
  "commands_run": [
    {"cmd": "npx tsc --noEmit", "exit_code": 0},
    {"cmd": "npm run lint", "exit_code": 0},
    {"cmd": "npm run build", "exit_code": 0},
    {"cmd": "npm run validate-card-stats", "exit_code": 0},
    {"cmd": "node scripts/validate-corpus.mjs --all", "exit_code": 0},
    {"cmd": "python -c \"import yaml; yaml.safe_load(open('.github/workflows/barint_ci.yml'))\"", "exit_code": 0},
    {"cmd": "git push -u origin task579-cards-fanout", "exit_code": 0}
  ],
  "not_done": [
    "magnesium not converted (TASK-578, no JSON generated field to derive updatedLabel from)",
    "bread-lite not converted (BreadProduct is a different shape than BariProductVM; BREAD_REPORT_STATS is a scan-funnel stat, not a grade/score distribution -- forcing the mapping would redefine what the numbers mean)",
    "chocolate-tablets cocoa% stat stays a hardcoded literal (no source field on the product JSON)",
    "insightLines/showInsights dead-code cleanup on ComparisonIntelligenceHero NOT done, per explicit instruction (separate concern)",
    "parity script's static-source-literal-grep hardening (TODO from TASK-568) still not built",
    "e2e-smoke job's separate Node 20 pin left untouched (does not run validate-card-stats)",
    "no Node 20 environment was available locally to empirically reproduce the ERR_UNKNOWN_FILE_EXTENSION failure that motivates the CI Node bump -- stated as a documented fact about Node's ESM loader, not a local repro; flagging this rather than overclaiming direct verification"
  ],
  "self_check": "Acceptance test: 'every non-excluded featured card converted with npm run build/lint/validate-card-stats all exit 0, zero consumer-visible stat changes, and the new CI step proven green locally before being wired in.' Observed: all commands exited 0 (see commands_run); read back all 14 converted card files plus the 3 pilot files after editing and confirmed no residual hand-typed count for productCount/scoredCount/gradeCounts/ceilingGrade fields where a shared-module derivation was possible; the two genuinely non-derivable literals (chocolate-tablets cocoa%, bread funnel stats) were left untouched with an inline reason; validate-card-stats.mjs was run and confirmed exit-0 BEFORE editing barint_ci.yml to add the step, satisfying 'never ship a knowingly-red gate.'"
}
```
