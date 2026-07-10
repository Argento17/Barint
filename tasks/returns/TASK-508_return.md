# TASK-508 Return — Registry nameHe drift: snacks identity fix + category audit

**Status proposed:** RETURNED
**Worktree:** `C:\bari_wt_t508` (branch `fix/task508-registry-namehe`)
**Commit SHA:** `2c27c68c`
**Date:** 2026-07-05

---

## Summary

Fixed the one proven identity drift in the comparison category registry: `snacks.ts` `nameHe` was
`'חטיפים מלוחים'` (salty snacks — the retired/fabricated identity, pre-TASK-228) and has been
corrected to `'חטיפי דגנים'` (grain/cereal bars — the live post-TASK-228 identity).

All other 6 registered categories were audited against their live page-data source of truth and
found to be MATCH or correctly styled per the `types.ts` nameHe contract
("Author a clean consumer-facing short name, not a hero headline").

---

## Change

**File:** `bari-web/src/lib/comparisons/registry/categories/snacks.ts:11`

```
- nameHe: "חטיפים מלוחים",
+ nameHe: "חטיפי דגנים",
```

No other files changed. No scoring changes. No comparison-JSON edits. No copy strings touched.

---

## Full Category Audit Table

7 categories checked of 7 in `bari-web/src/lib/comparisons/registry/categories/`.

| # | Category ID | Registry nameHe | Live page identity (source) | MATCH / DRIFT | Evidence: Registry file:line | Evidence: Live page source file:line |
|---|---|---|---|---|---|---|
| 1 | `snacks` | `חטיפים מלוחים` (pre-fix) | `חטיפי דגנים` | **DRIFT — FIXED** | `registry/categories/snacks.ts:11` | `snacks-comparison-page-data.ts:63` (eyebrow), `:58` (metadataLine `חטיפי דגנים בדף`) |
| 2 | `bread` | `לחם ומאפים` | Live eyebrow: `מנוע השוואה · לחמים` (headline format) | **MATCH** | `registry/categories/bread.ts:11` | `bread-comparison-page-data.ts:62` — eyebrow is a hero-headline; `לחם ומאפים` is the correct short consumer label per types.ts contract |
| 3 | `breakfast-cereals` | `דגני בוקר` | `דגני בוקר` | **MATCH** | `registry/categories/breakfast-cereals.ts:11` | `cereals-page-data.ts:64` (eyebrow exact match) |
| 4 | `cheese` | `גבינות` | Live page_copy.hero.eyebrow: `גבינות לבנות ומרחים`; metadata title: `השוואת גבינות לבנות וממרחים` | **MATCH** | `registry/categories/cheese.ts:11` | `cheese_frontend_v5.json page_copy.hero.eyebrow`; `cheese-page-data.ts:59`. `גבינות` is the correct SHORT label (types.ts: "e.g. גבינות, not a hero headline"); the JSON's longer eyebrow is the rendered hero string, not the registry's role |
| 5 | `crackers` | `קרקרים` | Live eyebrow: `השוואת קרקרים` (headline form) | **MATCH** | `registry/categories/crackers.ts:11` | `crackers-page-data.ts:70` — eyebrow is prefixed; `קרקרים` is the correct short label |
| 6 | `granola` | `גרנולה ומוזלי` | `גרנולה ומוזלי` | **MATCH** | `registry/categories/granola.ts:11` | `granola-page-data.ts:54` (eyebrow exact match) |
| 7 | `hummus` | `חומוס וממרחים` | Live eyebrow: `מנוע השוואה · חומוס` (headline form) | **MATCH** | `registry/categories/hummus.ts:11` | `hummus-comparison-page-data.ts:139` — eyebrow is `מנוע השוואה · חומוס`; `חומוס וממרחים` is the correct short category label (includes spreads scope; the eyebrow is a hero string) |

**Methodology note:** `nameHe` is the short consumer-facing category label used in the inventory catalog and admin panel (`loader.ts:78,114`, `admin/page.tsx:331`). Its source of truth is the live category identity, not the hero eyebrow which may carry a longer headline format. The `types.ts:44` JSDoc is explicit: "Author a clean consumer-facing short name (e.g. 'גבינות'), not a hero headline." The only case where the registry's nameHe encodes a **retired identity** (not just a format difference) is `snacks`.

---

## Verification

### Old string gone from registry
```
Grep 'חטיפים מלוחים' in bari-web/src/lib/comparisons/registry/ → 0 matches
```

### New string present
```
Grep 'חטיפי דגנים' in bari-web/src/lib/comparisons/registry/categories/snacks.ts:11 → 1 match
```

### TypeScript check
The full-project `tsc --noEmit` passes clean on the main tree (exit 0) — this is the
authoritative baseline. The worktree has no `node_modules/` so running tsc directly against it
produces `Cannot find module 'next'` / playwright errors (pre-existing, not introduced).
The change is a pure string literal `nameHe: string` — no type constraint can fail on this
substitution. The `ComparisonCategoryDefinition.nameHe` field is typed `string` (types.ts:45).

---

## OFF audit
No Open Food Facts references found anywhere in the changed or audited files.
Grep `open.food.facts|OFF` across `registry/categories/*.ts` → 0 matches.

---

```json
{
  "task": "TASK-508",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "bari-web/src/lib/comparisons/registry/categories/snacks.ts",
      "action": "modified",
      "sha256": "7C1161071F07B11F6DC2754E0C45AD330576D2BB0C57A0E3AFA592DD5EC104FD"
    }
  ],
  "counts": {
    "registry_categories_audited": "7/7 (all files in bari-web/src/lib/comparisons/registry/categories/)",
    "drift_found": "1/7 (snacks.ts:11, verified by Grep)",
    "drift_fixed": "1/1 (snacks.ts:11 old string 0 matches post-fix, new string 1 match)",
    "other_stale_salty_identity_strings_in_registry": "0/7 (Grep 'מלוחים' in registry/categories/*.ts = 0 matches)",
    "tsc_errors_introduced": "0 (change is string literal on nameHe: string field; main tree tsc exit 0 unchanged)"
  },
  "commands_run": [
    {"cmd": "git -C C:/Bari worktree add C:/bari_wt_t508 -b fix/task508-registry-namehe origin/master", "exit_code": 0},
    {"cmd": "Grep 'חטיפים מלוחים' path=C:/bari_wt_t508/bari-web output_mode=count", "exit_code": 0},
    {"cmd": "Grep 'חטיפי דגנים' path=C:/bari_wt_t508/bari-web/src/lib/comparisons/registry output_mode=content", "exit_code": 0},
    {"cmd": "C:/Bari/bari-web/node_modules/.bin/tsc --noEmit --project C:/Bari/bari-web/tsconfig.json (main tree baseline)", "exit_code": 0},
    {"cmd": "git -C C:/bari_wt_t508 add bari-web/src/lib/comparisons/registry/categories/snacks.ts", "exit_code": 0},
    {"cmd": "git -C C:/bari_wt_t508 commit -m 'TASK-508: registry nameHe drift...'", "exit_code": 0},
    {"cmd": "Get-FileHash snacks.ts -Algorithm SHA256", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Grep 'חטיפים מלוחים' in registry/ = 0 matches; Grep 'חטיפי דגנים' in snacks.ts:11 = 1 match; tsc baseline exits 0 on main tree unchanged."
}
```
