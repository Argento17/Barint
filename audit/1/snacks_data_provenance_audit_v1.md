# Snacks Data Provenance Audit v1

Audit date: 2026-05-29  
Scope: creation and trust path for `src/data/comparisons/snacks_frontend_v2.json`  
Mode: forensic audit only. No code changes.

## Provenance Verdict

The current production JSON is structurally consistent with a CE v2 production corpus: it has 18 products, 18 scored rows, complete v2 expansion fields, score-descending order, and metadata declaring CE approval.

But the provenance chain is incomplete. The authoritative CE handoff file named in the task, `snacks_ce_handoff_v2.md`, was not found. The repo contains a deprecated builder script that still writes to the canonical production JSON path. Therefore production JSON is usable as the current checked-in source, but its upstream CE provenance is `NOT VERIFIED`.

## Current Production JSON Metadata

Source: `src/data/comparisons/snacks_frontend_v2.json`

| Field | Value |
|---|---|
| `_meta.generated` | `2026-05-29T00:00:00Z` |
| `_meta.category` | `snacks` |
| `_meta.product_count` | 18 |
| `_meta.scored_count` | 18 |
| `_meta.schema` | `BariProductVM[]` |
| `_meta.version` | `v2-production` |
| `_meta.expansion` | `interpretive_expansion_system_v2` |
| `_meta.source_run_id` | `yochananof_snack_retail_v1` |
| `_meta.production_pass` | Declares CE-approved corpus v2, no shelf-facing NOVA terminology, limiting factors added to all products, and products `snk-015` through `snk-020` added. |

Important metadata note:

- `_meta.editorial_note` mentions `BSIP2`.
- `_meta.production_pass` mentions `NOVA`.
- These are metadata strings, not product-facing row/expansion fields, but they are still inside frontend JSON.

## Source / Handoff Search

| Artifact searched | Result |
|---|---|
| `snacks_ce_handoff_v2.md` | `NOT VERIFIED`: file not found. |
| Files matching `snacks*handoff`, `handoff*snacks`, `ce*snacks`, `snacks*ce` | No matching handoff file found. |
| `docs/snacks_rollout_report_v1.md` | Found, but contains stale statements from an earlier 14-row state. |
| `src/lib/comparisons/snack-page-data.ts` | Found. Contains 18 displayable Snack products and scores matching production JSON. |
| `scripts/build-snacks-frontend-v2.ts` | Found. Marked deprecated but still writes the canonical JSON path. |

## Transformation Path Observed

Current production route:

```text
src/app/hashvaot/snacks/page.tsx
  -> src/lib/comparisons/snacks-comparison-page-data.ts
  -> import rawCorpus from src/data/comparisons/snacks_frontend_v2.json
  -> loadComparisonCorpus(rawCorpus)
  -> strip _internal_cluster
  -> SnacksComparisonPage
  -> ComparisonShelfPage
```

Local score source alignment:

```text
src/lib/comparisons/snack-page-data.ts
  -> contains snackProducts scores/grades
  -> all 18 displayed scores/grades match snacks_frontend_v2.json
```

Deprecated generation path still present:

```text
scripts/build-snacks-frontend-v2.ts
  -> imports snackProducts from snack-page-data.ts
  -> maps raw.score with Math.round(raw.score)
  -> maps raw.grade directly
  -> filters displayable products
  -> writes src/data/comparisons/snacks_frontend_v2.json
```

## Builder / Adapter Risk

`scripts/build-snacks-frontend-v2.ts` has an internal warning:

- It is deprecated for the production shelf.
- It says the CE Handoff v2 corpus is canonical at `src/data/comparisons/snacks_frontend_v2.json`.
- It says not to run the script after CE v2.
- It says the script maps `snack-page-data.ts` without `limitingFactors`.
- It says it uses fixture order, not CE score-descending order.

Despite that, the same script still contains:

- `const outPath = join(root, "src/data/comparisons/snacks_frontend_v2.json")`
- `score: raw.score == null ? null : Math.round(raw.score)`
- `grade: raw.grade`
- `writeFileSync(outPath, ...)`

This is a high-risk provenance issue. A deprecated script can overwrite the production corpus with a legacy-mapped version.

## Was The CE Corpus Overwritten?

`NOT VERIFIED`.

Evidence supporting current corpus being post-CE:

- JSON metadata date is `2026-05-29T00:00:00Z`.
- JSON metadata says `CE-approved corpus v2`.
- All 18 products include `limitingFactors`.
- Products `snk-015` through `snk-020` exist.
- Product order is score-descending/non-increasing.

Evidence preventing full verification:

- No independent CE handoff file was found.
- The deprecated script still targets the production JSON path.
- `docs/snacks_rollout_report_v1.md` contains stale 14-row language and cannot be treated as current source of truth.
- The repo has a dirty/untracked state, so historical overwrite status cannot be concluded from the current working tree alone.

## Authoritative Score Source

| Candidate | Status | Notes |
|---|---|---|
| `src/data/comparisons/snacks_frontend_v2.json` | Current production source | This is what `/hashvaot/snacks` imports. |
| `src/lib/comparisons/snack-page-data.ts` | Local score source mirror | Scores/grades match all 18 displayed production rows. |
| `snacks_ce_handoff_v2.md` | `NOT VERIFIED` | Not found in repo. |
| `scripts/build-snacks-frontend-v2.ts` | Deprecated transformer | Should not be trusted as current production generation path. |
| Full 53 scanned / 48 scored source corpus | `NOT VERIFIED` | Metadata claims it, but full source artifact was not found. |

## Production JSON Trust Assessment

| Question | Answer |
|---|---|
| Does production route use `snacks_frontend_v2.json`? | Yes. |
| Does JSON score order look correct? | Yes, score-descending/non-increasing. |
| Do scores match local Snacks source? | Yes, 18/18 match `snack-page-data.ts`. |
| Was Maadanim used in Snacks score transformation? | No evidence found. |
| Is CE handoff provenance complete? | No, `NOT VERIFIED`. |
| Can a deprecated script overwrite production JSON? | Yes. |
| Is production JSON safe as the only source of truth? | No, not without handoff verification or script quarantine. |

## Data Provenance Verdict

The checked-in Snacks JSON is internally consistent and appears intentionally authored for v2. But the provenance chain has a stop-ship gap: the authoritative CE handoff/source file is absent, and a deprecated writer still targets the production JSON. Keep the page paused or under heightened review until the CE source artifact is verified and overwrite risk is removed.
