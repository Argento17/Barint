# TASK-569 return — Generate page JSON schema from BariProductVM (kill schema lag class)

## Source-type decision + rationale

`page_output_schema_v1.json` describes the **RAW served JSON** under
`bari-web/src/data/comparisons/*_frontend_v*.json` — the files each `*-page-data.ts`
module imports directly, *before* the page-data transform runs. `BariProductVM`
(`bari-web/src/lib/view-models/index.ts`) is a **different, downstream** contract: the
post-transform, UI-facing shape. The two already diverge on live data in ways that are
not typos — e.g. raw `grade` legitimately carries `"S"` (4/681 live products) while
`BariGrade` is `"A"–"E"` only (ScoreChip folds S→A at render, per the owner's
S-grade-honesty ruling); raw `confidence` uses `"full"/"partial"/"verified"` while the
VM's `BariConfidence` documents `"verified"` as the *already-converted* value
("language boundary lives here" — VM comment); the VM has no `d4_additives`,
`rank`, `categoryTotal`, `rowVerdict`, `_hash_no_rank`, etc. at all (those are raw-JSON
/ page-data-only fields).

No existing TS type describes the raw shape, so per the task's approach I wrote a
dedicated type: **`bari-web/src/lib/contracts/comparison-page-contract.ts`**
(`ComparisonPageContract`, types only, zero runtime import — never imported by
component/runtime code). Every field's required/optional/nullable status was verified
against the highest-version live dataset for **all 18 currently-served categories
(681 products)**, not inferred blindly from one sample file. Where the raw data
disagreed with either the VM's declared type or the hand-maintained schema's comment
(see Finding 1–3 below), I encoded what the pipeline actually emits, with an inline
note — not a silent "fix."

`ts-json-schema-generator` (MIT, OSS, added as `devDependency`) turns that type into
`bari-web/schema/page-output-schema.generated.json` via `npm run generate-page-schema`
(uses `--no-top-ref` so the generated schema's top level matches the hand-maintained
schema's style — inlined `type`/`required`/`properties` at the root, not a `$ref`
wrapper — to keep the diff meaningful).

## Full categorized schema diff

Produced by `npm run diff-page-schema` (script:
`bari-web/scripts/schema/diff-page-schema.mjs`, reads both schemas read-only, resolves
`$ref`/`anyOf` nullable-ref wrapping before comparing so the diff reports real
structural gaps, not `$ref`-vs-inline noise). **42 total differences**, all listed
below (none truncated):

### MISSING PROPERTY — in generated, absent from the hand-maintained schema (5)
The hand schema is lagging on these — all five are things the pipeline emits today
that the hand-maintained contract does not know about:
1. `products[].expansion.sourceLine` — declared on `BariExpansionVM`, not in the hand schema.
2. `products[].metrics.additive_count`
3. `products[].metrics.base_pct`
4. `products[].metrics.fat_saturated_g`
5. `_meta.run_id` — present on 13/18 live datasets.

### EXTRA PROPERTY — in hand-maintained schema, not in the generated TS contract (4)
Declared in the hand schema but not observed on any of the 18 live datasets (681
products) during this verification pass — either dead/historical or a still-planned
field:
1. `products[]._novaGroup` (underscore-prefixed variant — not found in any live JSON; only bare `novaGroup` is live)
2. `products[]._subPool` (same — only bare `subPool` is live, juices only)
3. `products[].d3_processing` (the VM-shaped `BariProcessingSignalVM` field — 0 live occurrences; only the differently-shaped `d3_processing_signal` raw trace object is live, hummus only)
4. `products[].rowReason` — hand schema's own comment says "Synthesized by page-data layer, not in source JSON," confirmed correct; excluded from the raw contract on purpose.

### TYPE MISMATCH (12)
| path | generated | hand |
|---|---|---|
| `totalProducts` | number | integer |
| `products[]._product_type` | string | null\|string |
| `products[].bariInterpretation` | array | array\|null |
| `products[].bestUseCases` | array | array\|null |
| `products[].categoryTotal` | number | integer |
| `products[].confidence_level` | string | null\|string |
| `products[].consumerTakeaway` | string | null\|string |
| `products[].d3_processing_signal` | object | null\|object |
| `products[].novaGroup` | null\|number | integer\|null |
| `products[].rank` | number | integer |
| `_meta.product_count` | number | integer |
| `_meta.scored_count` | number | integer |

Caveat on the `number` vs `integer` rows (5 of the 12): this is an inherent
generator limitation, not a modeling error — TypeScript's `number` cannot express
"integer" so `ts-json-schema-generator` always emits `number` for it. It is *looser*
than the hand schema, not wrong (every integer value still validates against
`type: number`); tightening it would require a branded/`@TJS-type integer` style
annotation, a follow-up if the generated schema is adopted. The `d3_processing_signal`
and `*_level`/`*Cases`/`Takeaway`/`_product_type` rows are real: verified against all
57 hummus / 67 yogurt / etc. occurrences — the raw pipeline never emits `null` for
these, only presence-or-absence, so `null` in the hand schema is looser than reality
(not a bug in the generated one).

### REQUIRED/OPTIONAL MISMATCH (21)
| path | generated | hand |
|---|---|---|
| `products[].barcode` | required | optional |
| `products[].confidence_label_he` | required | optional |
| `products[].confidence_tooltip_he` | required | optional |
| `products[].imageUrl` | required | optional |
| `products[].expansion.positiveSignals` | optional | required |
| `products[].d3_processing_signal.confidence` | required | optional |
| `products[].d3_processing_signal.confidence_note` | required | optional |
| `products[].d3_processing_signal.materiality_note` | required | optional |
| `products[].d3_processing_signal.modifier` | required | optional |
| `products[].d3_processing_signal.modifier_note` | required | optional |
| `products[].d3_processing_signal.note_he` | required | optional |
| `products[].d3_processing_signal.note_he_mobile` | required | optional |
| `products[].d3_processing_signal.nova_class` | required | optional |
| `products[].d3_processing_signal.population_correlation` | required | optional |
| `products[].d3_processing_signal.uncertainty_materiality` | required | optional |
| `products[].expansion.nutrition.energyKcal` | required | optional |
| `products[].expansion.nutrition.fat` | required | optional |
| `products[].expansion.nutrition.fiber` | required | optional |
| `products[].expansion.nutrition.protein` | required | optional |
| `products[].expansion.nutrition.sodium` | required | optional |
| `products[].expansion.nutrition.sugar` | required | optional |

The first 4 rows (`barcode`, `confidence_label_he`, `confidence_tooltip_he`,
`imageUrl`) and the 9 `d3_processing_signal.*` rows and the 6
`expansion.nutrition.*` rows are all backed by 100% presence across the full 681/57/681
observed-product counts respectively — the generated schema's `required` is the more
accurate one there. `expansion.positiveSignals` is the one row that goes the other
way: hand schema requires it, generated makes it optional, because 3 live products
(TASK-564) ship it as `null` rather than `[]` — matches the hand schema's own
already-documented TASK-564 comment.

### Independent finding surfaced by this work (not a diff-script output — a real
production bug found while building the sanity check in step 4)
The **current, live, hand-maintained schema already FAILS validation on 3/18 shelves
today**: `chocolate_bars`, `chocolate_tablets`, `snacks`. Cause:
`expansion.limitingFactors[].magnitude` is typed `{"type":"string"}` only in the hand
schema (draft object variant), but those 3 categories emit `magnitude` as a **number**
(1–3 integers), while `cereals` emits it as a **string** enum
(`"high"|"medium"|"low"`) — both shapes are live simultaneously. The generated
contract types `magnitude: number | string` (matching observed reality) and all
18/18 shelves pass. This is out of scope to fix here (task instructs: propose, don't
adopt/patch the live schema) — flagging for the orchestrator as a pre-existing gate
gap independent of this task's deliverable.

## Per-shelf validation table (generated schema, `npm run validate-page-schema`)

All 18 live datasets — the highest version imported by a live `*-page-data.ts` module
— validated via `ajv` (MIT, devDependency) against
`schema/page-output-schema.generated.json`:

| category | file | products | result |
|---|---|---|---|
| bread | bread_frontend_v4.json | 23 | PASS |
| brined_cheeses | brined_cheeses_frontend_v2.json | 36 | PASS |
| cakes_hard_cookies | cakes_hard_cookies_frontend_v1.json | 62 | PASS |
| cereals | cereals_frontend_v2.json | 20 | PASS |
| cheese | cheese_frontend_v5.json | 47 | PASS |
| chocolate_bars | chocolate_bars_frontend_v1.json | 23 | PASS |
| chocolate_tablets | chocolate_tablets_frontend_v1.json | 35 | PASS |
| cookies_coffee | cookies_coffee_frontend_v2.json | 117 | PASS |
| crackers | crackers_frontend_v1.json | 53 | PASS |
| granola | granola_frontend_v2.json | 22 | PASS |
| hard_cheeses | hard_cheeses_frontend_v4.json | 31 | PASS |
| hummus | hummus_frontend_v5.json | 57 | PASS |
| juices | juices_frontend_v3.json | 17 | PASS |
| milk | milk_frontend_v1.json | 18 | PASS |
| protein_combined | protein_combined_frontend_v2.json | 32 | PASS |
| snacks | snacks_frontend_v5.json | 21 | PASS |
| yogurt_drinkable | yogurt_drinkable_frontend_v1.json | 17 | PASS |
| yogurt_spoonable | yogurt_spoonable_frontend_v1.json | 50 | PASS |

**18/18 PASS, 0/18 FAIL, 681/681 products validated.**

For comparison, the same 18 files run through the CURRENT hand-maintained schema
(read-only check, ad hoc — not committed as a script since it's a one-time sanity
comparison, not a durable gate): **15/18 PASS, 3/18 FAIL** (chocolate_bars,
chocolate_tablets, snacks — see finding above). No case exists where the generated
schema fails a shelf the hand schema passes — the sanity condition in the task spec
("if the generated schema fails shelves the current schema passes, your contract type
is wrong") is satisfied in the safe direction.

## Build/verification results

- `npx tsc --noEmit` → exit 0, no errors.
- `npm run lint` → 0 errors, 19 warnings (all 19 pre-existing/unrelated to this change;
  0 new warnings from the 4 new files).
- `npm run generate-page-schema` → exit 0, writes `schema/page-output-schema.generated.json`.
- `npm run diff-page-schema` → exit 0 (diagnostic script, not a gate — see full diff above).
- `npm run validate-page-schema` → exit 0 (18/18 PASS).
- `next build` was **not** run: this change is types + two new devDependencies
  (`ts-json-schema-generator`, `ajv`) + new scripts under `scripts/schema/` — it touches
  no page-data `.ts`, no route, no component, and no comparison JSON, so it is outside
  the self-gating page-data duty's trigger condition. The task's own verification bar
  (tsc / lint / generated-schema validation) is fully green.

## Scope discipline

- Zero changes to `03_operations/page_generator/contract/page_output_schema_v1.json`
  (read-only comparison target).
- Zero changes to any `bari-web/src/data/comparisons/*.json` (verified: `git diff
  --cached --stat` shows only `package.json`, `package-lock.json`, `.gitignore`, and
  the 4 new files under `src/lib/contracts/`, `scripts/schema/`, `schema/`).
- Zero copy changes.
- No commits made in `C:\Bari` — all work done and committed in worktree
  `C:/bari_wt_569` on branch `task569-vm-schema`.

## Commit + PR

- Branch: `task569-vm-schema` (pushed to `origin`).
- Commit: `b382d9a6` — "TASK-569: generate page JSON schema from a dedicated TS
  contract (kill schema lag class)".
- PR: no `gh` CLI available in this environment (known environment gap — see
  `worktree_and_pr_creation_gotchas` memory). Printed by `git push`:
  **https://github.com/Argento17/Barint/pull/new/task569-vm-schema**

```json
{
  "task": "TASK-569",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/lib/contracts/comparison-page-contract.ts", "action": "created", "sha256": "b0ccc0ad363d6254358258013d28ec14047ee91b657750b3809afdecad7d78e3"},
    {"path": "bari-web/scripts/schema/diff-page-schema.mjs", "action": "created", "sha256": "11165a87822d4d3102618a046b84e28a4ebf2e43c17dcd38a50b12f8e0d14cdb"},
    {"path": "bari-web/scripts/schema/validate-against-generated-schema.mjs", "action": "created", "sha256": "fab3c4186b61d1427fe260e2667e3ca4b37102cdd330e13c94079971d5a60bf9"},
    {"path": "bari-web/schema/page-output-schema.generated.json", "action": "created", "sha256": "e89140e9519c224d9b47265c6dac54f4df045449ff6cef23ee192071fd7a0b5e"},
    {"path": "bari-web/package.json", "action": "modified", "sha256": "046f8a90e7b9d3fbfb628f95307af1221bea116ba6b8700223ab5e4fe1655c64"},
    {"path": "bari-web/package-lock.json", "action": "modified", "sha256": "6c4cfdb477a606a74b5b40f1c29ef553cdcc3ab2f309ebd0ffeba45b72f41b1c"},
    {"path": "bari-web/.gitignore", "action": "modified", "sha256": "c82e2b48a1f68217cc11dcd373ea6230842294cdf33c6e31039feb11bd1ec416"}
  ],
  "counts": {
    "live_shelf_product_count_distribution": "18 shelves, per-shelf product counts: min=17 (juices/yogurt_drinkable), max=117 (cookies_coffee), median=31.5, mean=37.8, stdev=24.0, most_common=17(x2) — full per-shelf breakdown in the validation table above; source: bari-web/src/data/comparisons/*_frontend_v*.json products[].length",
    "live_shelves_validated_against_generated_schema": "18/18 (npm run validate-page-schema, source: bari-web/src/data/comparisons/*_frontend_v*.json highest-version-per-category imported by live *-page-data.ts modules)",
    "live_shelves_passing_generated_schema": "18/18 (schema/validation-report.json, regenerable)",
    "live_shelves_passing_hand_maintained_schema": "15/18 (ad hoc ajv check vs 03_operations/page_generator/contract/page_output_schema_v1.json — chocolate_bars, chocolate_tablets, snacks fail on expansion.limitingFactors[].magnitude type)",
    "total_products_verified": "681/681 (sum of products[].length across all 18 live datasets, source: same 18 files)",
    "schema_diff_total_findings": "42/42 (bari-web/schema/schema-diff-report.json: missing_in_hand=5, extra_in_hand=4, type_mismatch=12, required_mismatch=21)",
    "tsc_errors": "0/0 (npx tsc --noEmit, exit 0)",
    "lint_errors": "0/0 (npm run lint, exit 0)",
    "lint_new_warnings": "0/19 (19 total warnings all pre-existing/unrelated; 0 attributable to the 4 new files)"
  },
  "commands_run": [
    {"cmd": "npm ci", "exit_code": 0},
    {"cmd": "npm install --save-dev ts-json-schema-generator ajv", "exit_code": 0},
    {"cmd": "npm run generate-page-schema", "exit_code": 0},
    {"cmd": "npm run diff-page-schema", "exit_code": 0},
    {"cmd": "npm run validate-page-schema", "exit_code": 0},
    {"cmd": "npx tsc --noEmit", "exit_code": 0},
    {"cmd": "npm run lint", "exit_code": 0},
    {"cmd": "git commit -F <msgfile>", "exit_code": 0},
    {"cmd": "git push -u origin task569-vm-schema", "exit_code": 0}
  ],
  "not_done": [
    "Adoption of the generated schema as the live page_output_schema_v1.json is explicitly NOT done here (task scope: propose only, per instructions).",
    "The pre-existing hand-schema bug found (magnitude type failing 3/18 live shelves) is reported, not fixed, per task scope.",
    "Did not add integer-precision (vs plain number) to the generated schema for count/rank fields — a follow-up if/when the generated schema is adopted; noted as a caveat in the diff, not a defect."
  ],
  "self_check": "Acceptance test from the spec: 'validate all 16+ served comparison JSONs ... against the GENERATED schema; report pass/fail per shelf. If the generated schema fails shelves the current schema passes, your contract type is wrong.' Observed: 18/18 live shelves (681 products) pass the generated schema; the hand-maintained schema itself only passes 15/18 (chocolate_bars/chocolate_tablets/snacks fail there on a pre-existing magnitude-type bug) — so the generated schema strictly dominates the current one on live data, satisfying the acceptance condition."
}
```
