# Urgent Snacks Score Integrity Audit v1

Audit date: 2026-05-29  
Scope: `/hashvaot/snacks` score integrity against Maadanim and local Snacks score sources  
Mode: forensic audit only. No code changes.

## Stop-Ship Summary

No evidence was found that Snack scores or grades were copied from Maadanim. The displayed Snacks score sequence is not identical to Maadanim, and every displayed Snack score/grade matches the local legacy Snacks source module `src/lib/comparisons/snack-page-data.ts`.

However, production trust is not fully established because the CE-approved handoff source file was not found in the repo. The production JSON states it is CE-approved, but the independent handoff artifact is `NOT VERIFIED`.

## Files Audited

- `src/data/comparisons/snacks_frontend_v2.json`
- `src/data/comparisons/maadanim_frontend_v2.json`
- `src/lib/comparisons/snack-page-data.ts`
- `src/lib/comparisons/snacks-comparison-page-data.ts`
- `scripts/build-snacks-frontend-v2.ts`
- `src/components/shared/product-table.tsx`
- `src/components/shared/product-row.tsx`

## Snacks Score List

Source: `src/data/comparisons/snacks_frontend_v2.json`

| Rank | Product id | Score | Grade |
|---:|---|---:|---|
| 1 | `snk-001` | 70 | B |
| 2 | `snk-004` | 58 | C |
| 3 | `snk-002` | 56 | C |
| 4 | `snk-015` | 55 | C |
| 5 | `snk-003` | 53 | C |
| 6 | `snk-016` | 51 | C |
| 7 | `snk-009` | 47 | D |
| 8 | `snk-005` | 46 | D |
| 9 | `snk-018` | 46 | D |
| 10 | `snk-010` | 45 | D |
| 11 | `snk-011` | 43 | D |
| 12 | `snk-012` | 42 | D |
| 13 | `snk-019` | 41 | D |
| 14 | `snk-017` | 39 | D |
| 15 | `snk-020` | 32 | E |
| 16 | `snk-007` | 29 | E |
| 17 | `snk-006` | 17 | E |
| 18 | `snk-013` | 13 | E |

Snacks sequence:

```text
70, 58, 56, 55, 53, 51, 47, 46, 46, 45, 43, 42, 41, 39, 32, 29, 17, 13
```

Summary:

- Count: 18
- Min: 13
- Max: 70
- Average: 43.50
- Distinct values: 17
- Order: score-descending/non-increasing

## Maadanim Score List

Source: `src/data/comparisons/maadanim_frontend_v2.json`

Maadanim sequence:

```text
70, 57, 57, 57, 55, 54, 54, 54, 53, 53, 53, 53, 53, 52, 52, 50, 50, 50, 50, 50, 49, 49, 49, 49, 49, 49, 49, 49, 48, 48, 48, 48, 47, 46, 46, 46, 46, 46, 46, 46, 45, 45, 45, 45, 45, 44, 44, 43, 43, 43, 43, 43, 42, 42, 42, 42, 42, 42, 41, 40, 40, 40, 40, 40, 40, 39, 38, 38, 38, 38, 38, 37, 37, 37, 35, 35, 35, 35, 34, 33, 32, 32, 32, 32, 31, 31, 31, 27, 27, 27
```

Summary:

- Count: 90
- Min: 27
- Max: 70
- Average: 43.78
- Distinct values: 26

## Grade Distribution Comparison

| Grade | Snacks count | Maadanim count |
|---|---:|---:|
| B | 1 | 1 |
| C | 5 | 16 |
| D | 8 | 60 |
| E | 4 | 13 |

No A-grade products appear in either corpus.

## Similarity / Overlap Analysis

| Check | Result | Interpretation |
|---|---|---|
| Exact sequence match | No | Snacks and Maadanim score arrays differ. |
| Same first 18 positions vs Maadanim top 18 | 1 / 18 | Only rank 1 matches exactly: 70. |
| Shared distinct score values | 11 values | Shared values: 32, 39, 41, 42, 43, 45, 46, 47, 53, 55, 70. |
| Snack-only score values | 6 values | Snack-only values: 13, 17, 29, 51, 56, 58. |
| Maadanim top-18 values also found in Snacks | 3 values | 53, 55, 70. |
| Pearson correlation: Snacks sequence vs Maadanim top-18 sequence | 0.8051 | High because both sorted descending, not evidence of copying by itself. |
| Product id overlap | None found by prefix/domain | Snacks IDs are `snk-*`; Maadanim IDs are `bsip1_maadanim_*`. |

The similar averages are real: Snacks average 43.50 vs Maadanim average 43.78. But this is not accompanied by identical sequence, identical grade distribution, identical product IDs, or identical rank mapping.

## Local Source Trace For Each Snack Score

Each displayed Snack score/grade in the production JSON matches `src/lib/comparisons/snack-page-data.ts`.

| Product id | Production JSON | `snack-page-data.ts` | Result |
|---|---:|---:|---|
| `snk-001` | 70/B | 70/B | Match |
| `snk-004` | 58/C | 58/C | Match |
| `snk-002` | 56/C | 56/C | Match |
| `snk-015` | 55/C | 55/C | Match |
| `snk-003` | 53/C | 53/C | Match |
| `snk-016` | 51/C | 51/C | Match |
| `snk-009` | 47/D | 47/D | Match |
| `snk-005` | 46/D | 46/D | Match |
| `snk-018` | 46/D | 46/D | Match |
| `snk-010` | 45/D | 45/D | Match |
| `snk-011` | 43/D | 43/D | Match |
| `snk-012` | 42/D | 42/D | Match |
| `snk-019` | 41/D | 41/D | Match |
| `snk-017` | 39/D | 39/D | Match |
| `snk-020` | 32/E | 32/E | Match |
| `snk-007` | 29/E | 29/E | Match |
| `snk-006` | 17/E | 17/E | Match |
| `snk-013` | 13/E | 13/E | Match |

## Grade Derivation Check

Assumption used for audit only: A >= 80, B >= 60, C >= 50, D >= 35, E < 35.

Result: all Snacks grades match this assumed threshold model.

`NOT VERIFIED`: The canonical Bari grade threshold policy was not found as a dedicated source-of-truth file in this audit.

## Findings

| Finding | Severity | Evidence |
|---|---|---|
| Snack scores are not copied from Maadanim. | Clearing finding | Sequences differ; only 1/18 positional match against Maadanim top 18; source IDs differ. |
| Snack grades are not copied from Maadanim. | Clearing finding | Snacks grade distribution differs from Maadanim distribution. |
| Snack scores match local legacy `snack-page-data.ts`. | Evidence finding | 18/18 displayed Snack products match score/grade exactly. |
| Score order is corpus-owned and correct. | Clearing finding | Snacks JSON is score-descending/non-increasing; shared table does not sort. |
| Full CE score provenance is not independently verified. | HIGH | No `snacks_ce_handoff_v2.md` or equivalent handoff artifact found in repo. |
| Similar average score is real but not proof of contamination. | Medium | Snacks average 43.50; Maadanim average 43.78; distribution and sequences differ. |

## Score Integrity Verdict

Snack scores are locally consistent and do not appear copied from Maadanim. The production JSON score values are trustworthy relative to the local `snack-page-data.ts` source.

They are not fully trustworthy as CE-approved production scores until the authoritative CE handoff/source artifact is made available or otherwise verified.
