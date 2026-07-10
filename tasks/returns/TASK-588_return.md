# TASK-588 return — Catalog/registry alignment

Proposed status: **RETURNED**

## Registered categories and copy provenance

All category display names are references to existing exported hero eyebrow values; no new consumer-facing string was authored.

| Route | `nameHe` source |
|---|---|
| `brined-cheeses` | `brined-cheeses-page-data.ts:brinedCheesesHero.eyebrow` |
| `cakes` | `cakes-hard-cookies-page-data.ts:cakesHardCookiesHero.eyebrow`, derived from `cakes_hard_cookies_frontend_v1.json:page_copy.hero.title` |
| `chocolate-bars` | `chocolate-bars-comparison-page-data.ts:chocolateBarsHero.eyebrow` |
| `chocolate-tablets` | `chocolate-tablets-comparison-page-data.ts:chocolateTabletsHero.eyebrow` |
| `cookies-coffee` | `cookies-coffee-page-data.ts:cookiesCoffeeHero.eyebrow` |
| `hard-cheeses` | `hard-cheeses-page-data.ts:hardCheesesHero.eyebrow` |
| `juices` | `juices-page-data.ts:juicesHero.eyebrow` |
| `milk-comparison` | `milk-page-data.ts:milkHero.eyebrow`, derived from `milk_frontend_v1.json:page_copy.hero.eyebrow` |
| `protein-bars` | `protein-bars-comparison-page-data.ts:proteinBarsHero.eyebrow` |
| `yogurt` | `yogurt-spoonable-page-data.ts:yogurtSpoonableHero.eyebrow`, derived from `yogurt_spoonable_frontend_v1.json:page_copy.hero.eyebrow` |
| `yogurt-drinks` | `yogurt-drinks-page-data.ts:yogurtDrinksHero.eyebrow`, derived from `yogurt_drinkable_frontend_v1.json:page_copy.hero.eyebrow` |

The cakes registry wrapper needed the already-derivable `ComparisonCategoryPageData` and metadata exports. Its filter labels remain sourced from `cakes_hard_cookies_frontend_v1.json:page_copy.filters[].label_he`; hero/prologue/methodology remain sourced from that JSON's `page_copy`; its metadata title and description reuse the existing strings from `src/app/hashvaot/cakes/page.tsx:metadata` verbatim. The filter logic mirrors the existing cakes comparison component (`least_bad` grade D, PHVO id sets, and high-sugar id sets).

## Skipped

None. Every candidate's required registry fields were derivable from its existing served JSON and loader/page wiring.

## CI parity gate output

    Catalog/registry parity
  live product-comparison routes: 18
  registered catalog routes: 18
  LIVE  bread <- bread-comparison-page-data.ts <- bread_frontend_v4.json
  LIVE  breakfast-cereals <- cereals-page-data.ts <- cereals_frontend_v2.json
  LIVE  brined-cheeses <- brined-cheeses-page-data.ts <- brined_cheeses_frontend_v2.json
  LIVE  cakes <- cakes-hard-cookies-page-data.ts <- cakes_hard_cookies_frontend_v1.json
  LIVE  cheese <- cheese-page-data.ts <- cheese_frontend_v5.json
  LIVE  chocolate-bars <- chocolate-bars-comparison-page-data.ts <- chocolate_bars_frontend_v1.json
  LIVE  chocolate-tablets <- chocolate-tablets-comparison-page-data.ts <- chocolate_tablets_frontend_v1.json
  LIVE  cookies-coffee <- cookies-coffee-page-data.ts <- cookies_coffee_frontend_v2.json
  LIVE  crackers <- crackers-page-data.ts <- crackers_frontend_v1.json
  LIVE  granola <- granola-page-data.ts <- granola_frontend_v2.json
  LIVE  hard-cheeses <- hard-cheeses-page-data.ts <- hard_cheeses_frontend_v4.json
  LIVE  hummus <- hummus-comparison-page-data.ts <- hummus_frontend_v5.json
  LIVE  juices <- juices-page-data.ts <- juices_frontend_v3.json
  LIVE  milk-comparison <- milk-page-data.ts <- milk_frontend_v1.json
  LIVE  protein-bars <- protein-bars-comparison-page-data.ts <- protein_combined_frontend_v2.json
  LIVE  snacks <- snacks-comparison-page-data.ts <- snacks_frontend_v5.json
  LIVE  yogurt <- yogurt-spoonable-page-data.ts <- yogurt_spoonable_frontend_v1.json
  LIVE  yogurt-drinks <- yogurt-drinks-page-data.ts <- yogurt_drinkable_frontend_v1.json
    PASS: catalog registry exactly matches the live product-comparison routes.

## Verification

- `npx.cmd tsc --noEmit`: exit 0.
- `npm.cmd run lint`: exit 0 (existing warnings only; no errors).
- `npm.cmd run validate-catalog-parity`: exit 0; full output above.
- `npm.cmd run build -- --webpack` with `NEXT_FONT_GOOGLE_MOCKED_RESPONSES` pointing to an untracked offline fixture: exit 0; compiled, type-checked, and generated all static pages.
- `npm.cmd ci` was attempted because `node_modules` was absent, but this managed environment denied the global cache and then blocked registry fetches. Verification used a worktree-local physical copy of the dependency tree from an existing Bari worktree. Exact Turbopack `npm run build` likewise could not fetch Google Fonts; the offline webpack production build passed.

## Return block

```json
{
  "task": "TASK-588",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "db9c86ba9365c6195a091f971c762e68593f34ad4142708eed29d9e1ab154020"},
    {"path": "bari-web/package.json", "action": "modified", "sha256": "499b4fcfea9d90b1b5008b3e0e1d76f04b70d6977827b1907590a78882532e86"},
    {"path": "bari-web/scripts/catalog/validate-catalog-parity.mjs", "action": "created", "sha256": "19c987cf9b87c10a951862f4d5b9291fe47affe8f68fc5ec19d8a5f31cac9426"},
    {"path": "bari-web/src/lib/comparisons/cakes-hard-cookies-page-data.ts", "action": "modified", "sha256": "20ccfb7ecba240942cdba752c021eb73f1e5820e7a97be3358fbfc1f23a85232"},
    {"path": "bari-web/src/lib/comparisons/registry/index.ts", "action": "modified", "sha256": "571cd8a8bf5eec78049c719455e92b1f6b6b14060dc2e7b6d15acb5c737e717d"},
    {"path": "bari-web/src/lib/comparisons/registry/types.ts", "action": "modified", "sha256": "e3d1533033b0212659c6a76291537a679e4343588ab2df789bf8dc27daa8daad"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/brined-cheeses.ts", "action": "created", "sha256": "fde71876697ba00b9e680a9a052e8cc3c1e0587a37054c4c3f15b3e009ba362b"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/cakes.ts", "action": "created", "sha256": "640e4b32e84fdb877fcc1aab126785da86d29451517d111cbe5522b173445397"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/chocolate-bars.ts", "action": "created", "sha256": "3c9711cbedd9950008a13d2a9cafd9026a66ab596b225908551624cb115d6690"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/chocolate-tablets.ts", "action": "created", "sha256": "38723b6ef60de80597457761c68f56835598db7b7f6fd2bb3a5fbd722f9357b1"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/cookies-coffee.ts", "action": "created", "sha256": "6b53d9954d8e6d1281a990b264dc67e82e77f276b34c5213497d62c1135141e7"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/hard-cheeses.ts", "action": "created", "sha256": "609670a3f2199f88e7f3b6f200f39f26d6fc15785bbd0fa314d9f383a095dff7"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/juices.ts", "action": "created", "sha256": "fa506037adf773abe25c2ea2b04c04793fe4b2718a72fb9113cf404e70ca0a93"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/milk-comparison.ts", "action": "created", "sha256": "7154e0f3371ca4276216059deefdf160a04f189622d1370b6cf0ee4960ac8fc8"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/protein-bars.ts", "action": "created", "sha256": "c3a445435054f9c1e32d01a7f7b4fc6f939b5ae7d4489c92dd88eb488c201093"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/yogurt-drinks.ts", "action": "created", "sha256": "4bcc49bdbec528f442ca11f4240b18a37de8364dff96462edc4f5680b2f61c56"},
    {"path": "bari-web/src/lib/comparisons/registry/categories/yogurt.ts", "action": "created", "sha256": "d9c74d036851bf5110a65ebb6a0756b5140d6962d760625bb980df0c7c6027e5"}
  ],
  "counts": {
    "registered": "11/11 candidate product-comparison routes named in TASK-588",
    "skipped": "0/11 candidate product-comparison routes named in TASK-588",
    "parity": "18/18 live product-comparison routes derived by validate-catalog-parity.mjs are registered; histogram registered=18 missing=0 dead=0; most_common state registered(18)"
  },
  "commands_run": [
    {"cmd": "npx.cmd tsc --noEmit", "exit_code": 0, "exit": 0},
    {"cmd": "npm.cmd run lint", "exit_code": 0, "exit": 0},
    {"cmd": "$env:NEXT_FONT_GOOGLE_MOCKED_RESPONSES='C:\\tmp\\next-font-mocks.cjs'; npm.cmd run build -- --webpack", "exit_code": 0, "exit": 0},
    {"cmd": "npm.cmd run validate-catalog-parity", "exit_code": 0, "exit": 0}
  ],
  "not_done": [
    "npm ci could not complete because the managed environment denied the global npm cache and blocked registry fetches; dependencies were supplied from an existing local Bari worktree.",
    "Exact Turbopack npm run build could not fetch Google Fonts in the restricted environment; the offline webpack production build completed successfully."
  ],
  "self_check": "npm.cmd run validate-catalog-parity observed 18 live product-comparison routes, 18 registered routes, no missing/dead diff, exit 0"
}
```
