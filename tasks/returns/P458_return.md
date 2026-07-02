# P458 return — Catalog go-live package (C1-CURSOR)

**Task:** P458 / TASK-458  
**Branch:** `golive/catalog-task458` (worktree `C:ari_wt_t458`, baseline `48811ebb`)
**Proposed status:** RETURNED

## Summary

Ported the public `/catalog` route and inventory stack from `feature/homepage-mascots` (source commit `6871d374`), added header nav **קטלוג**, fixed blog `og:image` and comparison `og:title`/`og:description`, added EAN/sku catalog search. `tsc` + `build` pass; lint exit 1 (pre-existing). No push/PR/deploy.

## Commits

| Piece | SHA |
|-------|-----|
| (a) catalog port | `c28d38c5` |
| (b) header nav | `6b80e632` |
| (c) OG fixes | `bd1e3a80` |
| (d) barcode search | `43e545fc` |

## Build oracle

| Command | Exit |
|---------|------|
| `npx tsc --noEmit` | 0 |
| `npm run build` | 0 (`/catalog` → `ƒ /catalog`) |
| `npm run lint` | 1 (pre-existing) |

## FLAG (Content pass)

Catalog description **"כל המוצרים שבארי בדקה"** overstates coverage: **7/17+** live category routes, **209** products.

## OG evidence

- `/blog/food-dyes`: `og:image` = `https://bari.digital/bari-logo-optimized.webp` (build HTML)
- `/hashvaot/hummus`: `og:title` = `השוואת חומוס | Bari`, `og:description` from existing metadata via `withComparisonOpenGraph()`
- `/catalog`: route live in build manifest; metadata title **קטלוג המוצרים | Bari**

---

```json
{
  "task": "P458",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/public/mascots/mascot-oli-catalog.png",
      "action": "created",
      "sha256": "cbbcc78d785ca820887e5214631dd2620a21c90a35d068c57fae1bd120d6e5ce"
    },
    {
      "path": "bari-web/src/app/blog/bread-everyday/page.tsx",
      "action": "modified",
      "sha256": "56a50d405930b8c8e87e553609fa2d09b1580a19343cc8aab229635e2a80974a"
    },
    {
      "path": "bari-web/src/app/blog/bread-standouts/page.tsx",
      "action": "modified",
      "sha256": "b367f2761248536951a2361189ff2cd4e3ce705536553f8835113d517dfdaf1e"
    },
    {
      "path": "bari-web/src/app/blog/bread-wellness-gap/page.tsx",
      "action": "modified",
      "sha256": "61f1cbd6f50b6cb67ad96e8cb5cc2a40fa1d3ff10ca88ecb76fe8b7f7cba81e6"
    },
    {
      "path": "bari-web/src/app/blog/food-dyes/page.tsx",
      "action": "modified",
      "sha256": "b835143bad51ba8349e9bc8878a7700a5b81e489699c86bce0b6599f0efd4b92"
    },
    {
      "path": "bari-web/src/app/blog/hummus/page.tsx",
      "action": "modified",
      "sha256": "137e6759dfc25e887f6df0cad637452e5344b5d14a302d7378515026c573b0f5"
    },
    {
      "path": "bari-web/src/app/blog/lechem/page.tsx",
      "action": "modified",
      "sha256": "4d09d265c177a3b3c6963aa23ac54ea1961be0f2ec65b35e5a76fc4c070a4086"
    },
    {
      "path": "bari-web/src/app/blog/milk-analysis/page.tsx",
      "action": "modified",
      "sha256": "fc04ae06f528ce60f19795e8de3346795763851da879c596206714746a52acff"
    },
    {
      "path": "bari-web/src/app/blog/shemen-zayit/page.tsx",
      "action": "modified",
      "sha256": "b9a6efbec84e4b9f21d92129455c3ebb61f42762bdd3a55d060adc0e99a43541"
    },
    {
      "path": "bari-web/src/app/blog/sugar-alcohols/page.tsx",
      "action": "modified",
      "sha256": "87846012e5c79e4860dfb0653f2aa493744e326de74d11ba5c777993f4ce25fe"
    },
    {
      "path": "bari-web/src/app/blog/yogurt/page.tsx",
      "action": "modified",
      "sha256": "277637bd2ead13f31c65884f795ca077f92af08ca497ae0120cd51eafcc96786"
    },
    {
      "path": "bari-web/src/app/catalog/_catalog-client.tsx",
      "action": "created",
      "sha256": "2217ef8cf9653277a7cb79ebc11aca880e368036e67b0dca434d0047d4e3fb5e"
    },
    {
      "path": "bari-web/src/app/catalog/page.tsx",
      "action": "created",
      "sha256": "e94db04137a0e89def3cb5448818042fb1a552e8ea0b3e40bfa6978d0868bf33"
    },
    {
      "path": "bari-web/src/app/hashvaot/breakfast-cereals/page.tsx",
      "action": "modified",
      "sha256": "857d04e27c3aa1fa270ba90cc2bb4052eaff7248011d9938864afa799fa330e3"
    },
    {
      "path": "bari-web/src/app/hashvaot/brined-cheeses/page.tsx",
      "action": "modified",
      "sha256": "f76980d0f17496f6e546dd64cfb0c0c1597a6e86ea4f8658206394b9ea926a56"
    },
    {
      "path": "bari-web/src/app/hashvaot/cakes/page.tsx",
      "action": "modified",
      "sha256": "b51bff083e7db016b991f211760ca5117b69201db695359a79a2ffc32016017e"
    },
    {
      "path": "bari-web/src/app/hashvaot/granola/page.tsx",
      "action": "modified",
      "sha256": "cfca261dc12f30679e7c3077350a4b89041db2026fd5dff436df4807a8dc2190"
    },
    {
      "path": "bari-web/src/app/hashvaot/hard-cheeses/page.tsx",
      "action": "modified",
      "sha256": "501d345884e7a8f0cf3aed5761f8821b252f30ffa7b9dc10a66b72ecbe14a6d8"
    },
    {
      "path": "bari-web/src/app/hashvaot/juices/page.tsx",
      "action": "modified",
      "sha256": "e9f9eb223f788d062ccf3b473705e19fa0d1213a86aa3db0936ddeedec932159"
    },
    {
      "path": "bari-web/src/app/hashvaot/magnesium/page.tsx",
      "action": "modified",
      "sha256": "3f235fef495848737e1c9b1507f1f9df599602e8d7f97f0005128e14fdd686f3"
    },
    {
      "path": "bari-web/src/components/inventory/inventory-grade-chip.tsx",
      "action": "created",
      "sha256": "a55c2a33e86744bc04bcd5c47df3562f6e9574ff1f39ae79065fb67c6b903395"
    },
    {
      "path": "bari-web/src/components/inventory/product-table.tsx",
      "action": "created",
      "sha256": "8f3644c1c798376bae91c2af634817e39f41778ff9d22b0df1708fcc14634b92"
    },
    {
      "path": "bari-web/src/components/inventory/retailer-donut.tsx",
      "action": "created",
      "sha256": "1ed492f2549deb9dacc2f34d5993cbaba8b3da9fcbee4ab0f53750d5c2cd7a81"
    },
    {
      "path": "bari-web/src/components/inventory/top-categories-card.tsx",
      "action": "created",
      "sha256": "ed339a7d5423fc080f06969b7a3cc9c8b7fa0b6e1e3a3022f614e364935c78e3"
    },
    {
      "path": "bari-web/src/components/site-header.tsx",
      "action": "modified",
      "sha256": "34443b45d4f3e0ceb58f292428d97545ed3400a69fbea869783e30447a626108"
    },
    {
      "path": "bari-web/src/lib/comparisons/bread-comparison-page-data.ts",
      "action": "modified",
      "sha256": "133477f0c15caae47aabfaa6b7110bd00cc97e04b44da9c0f14fade9a3351362"
    },
    {
      "path": "bari-web/src/lib/comparisons/brined-cheeses-page-data.ts",
      "action": "modified",
      "sha256": "857a2d96f5c44ed70f7b6854e258ce9896afe4d63c3997d1d2c7ddc36ce8b8c1"
    },
    {
      "path": "bari-web/src/lib/comparisons/cereals-page-data.ts",
      "action": "modified",
      "sha256": "40efd3e3d8c0df10b82d769e409009b2c9e044afe638ff1d60a7e4efaa2a7c0e"
    },
    {
      "path": "bari-web/src/lib/comparisons/cheese-page-data.ts",
      "action": "modified",
      "sha256": "ee645d69f5d41e02d8a3803d170dd63906c13ab122f8ab2d24fca53cf6dabd13"
    },
    {
      "path": "bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts",
      "action": "modified",
      "sha256": "97460855b39a8f0467895a549bb853b94a14c1d0ab08a98a9fef30d1d57f42ae"
    },
    {
      "path": "bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts",
      "action": "modified",
      "sha256": "f64b591cb2d71bca7796fd5c9f8563cd07af65b1b6e300f9f44e4be06d05d8d1"
    },
    {
      "path": "bari-web/src/lib/comparisons/cookies-coffee-page-data.ts",
      "action": "modified",
      "sha256": "793a3bebfee2c32348e82d7a0aa7038f5f47ee7ddb739dd1f304af93bc6ca697"
    },
    {
      "path": "bari-web/src/lib/comparisons/crackers-page-data.ts",
      "action": "modified",
      "sha256": "78f2eaebcac0003198a1214068e14dc13ed793a4f2494aa3f703a9e34cfef549"
    },
    {
      "path": "bari-web/src/lib/comparisons/granola-page-data.ts",
      "action": "modified",
      "sha256": "6f18a5ba7d83473c566b62d5712fa6e7856d2d6535e98884d398efa840e82c4a"
    },
    {
      "path": "bari-web/src/lib/comparisons/hard-cheeses-page-data.ts",
      "action": "modified",
      "sha256": "dea181e70c8255adada73b7a6cbec5a4ce77509957f0c1ca41a11d1c8278c70b"
    },
    {
      "path": "bari-web/src/lib/comparisons/hummus-comparison-page-data.ts",
      "action": "modified",
      "sha256": "14018e89bdacfc674c638f70b0889a9817d6b6b7c63c8cde124da3859df17b16"
    },
    {
      "path": "bari-web/src/lib/comparisons/juices-page-data.ts",
      "action": "modified",
      "sha256": "d774a4a93983cd1840bc747a8ab9a10f75a618de9006b701072cafc64f6edbb1"
    },
    {
      "path": "bari-web/src/lib/comparisons/milk-page-data.ts",
      "action": "modified",
      "sha256": "c599aee42d2f854641f5d09ffeb9eb267463bb4f21755762388e6673fdc3c250"
    },
    {
      "path": "bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts",
      "action": "modified",
      "sha256": "e419d4b00d856902ba5c89bbc87c1cc0003698b85df49015bd1765b0abba3056"
    },
    {
      "path": "bari-web/src/lib/comparisons/snacks-comparison-page-data.ts",
      "action": "modified",
      "sha256": "9ba7f8bc9306b9255d4962a8aa1abe51bf8f56ebbdbb5e3571b42292a3bcc1fc"
    },
    {
      "path": "bari-web/src/lib/inventory/loader.ts",
      "action": "created",
      "sha256": "b22c571edc8a1f35a2741ca966f2f49f7a81c0b2898fd50439a4dd2952f006b1"
    },
    {
      "path": "bari-web/src/lib/inventory/retailer-map.ts",
      "action": "created",
      "sha256": "fa50baacd54646f040d1ca0657e8f96404b7f36361985e4df0a6f7112dddea74"
    },
    {
      "path": "bari-web/src/lib/seo/open-graph.ts",
      "action": "created",
      "sha256": "d4a52d5f1a6c522d3a8d3c0af7bc037a915a30c725c84f153597a44a677f92b4"
    },
    {
      "path": "bari-web/src/lib/view-models/index.ts",
      "action": "modified",
      "sha256": "4a14ccc2081b86d05c63b4695bf4ccf6355fd8ff33473f264e7b90999b7c7d82"
    }
  ],
  "counts": {
    "catalog_products": "187/187 (curated loader payload via getComparisonCategoryCorpusPayload across 7 registry categories — NOT raw products[] sums (209): hummus ships 35 of 57 after TASK-100 vegetable-spread + NOVA1/non-spread/raw-chickpea exclusions; grades consumer-normalized per corpus.ts frontendGradeFromScore (S folds to A); per-cat bread:23 breakfast-cereals:20 cheese:47 crackers:19 granola:22 hummus:35 snacks:21; grades A:15 B:49 C:64 D:41 E:18 unscored:0; most_common C(x64); stdev n/a categorical; matches rendered totalProducts=187 per T458_redteam_gate2 F-V1)",
    "catalog_registry_categories": "7/7 (listComparisonCategoryIds())",
    "live_hashvaot_category_routes": "17+ (site sitemap / hashvaot tree; catalog covers 7)",
    "ported_files_from_feature_branch": "9/9 (catalog census table)",
    "commits_a_through_d": "4/4"
  },
  "commands_run": [
    {
      "cmd": "npm install (bari-web/)",
      "exit_code": 0
    },
    {
      "cmd": "npx tsc --noEmit (bari-web/)",
      "exit_code": 0
    },
    {
      "cmd": "npm run build (bari-web/)",
      "exit_code": 0
    },
    {
      "cmd": "npm run lint (bari-web/)",
      "exit_code": 1
    },
    {
      "cmd": "python corpus product count (7 registry JSON files)",
      "exit_code": 0
    }
  ],
  "not_done": [
    "push/PR/deploy",
    "content+adversarial QA sign-off",
    "catalog honesty wording fix",
    "pre-existing lint debt"
  ],
  "self_check": "npm run build exit 0 AND npx tsc --noEmit exit 0 in the worktree: observed exit 0 for both after all four commits."
}
```
