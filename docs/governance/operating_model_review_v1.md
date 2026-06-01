# Operating Model Review v1

Audit date: 2026-05-29  
Scope: CE, Cursor, and Codex workflow signals from the Snacks rollout  
Mode: audit only

## What Worked

| Area | Evidence | Result |
|---|---|---|
| Frozen UI reference | `docs/comparison_ui_reference_v1.md` defines the canonical route, component tree, display-order ownership, and v2 field behavior. | Kept Snacks aligned with Maadanim without redesign. |
| Shared shelf shell | `src/components/comparisons/comparison-shelf-page.tsx` is reused by Maadanim and Snacks. | The rollout did not fork the shelf UI. |
| Category registry | `src/lib/comparisons/registry/index.ts` includes Maadanim, Bread, and Snacks category definitions. | Category discovery is moving toward a scalable model. |
| CE handoff integration | `src/data/comparisons/snacks_frontend_v2.json` has 18 scored products and complete v2 reasoning fields. | Snacks reached shelf readiness for displayed rows. |
| Legacy route containment | `src/app/hashvaot/snack-bars/page.tsx` and `src/app/compare/snack-bars/page.tsx` redirect to `/hashvaot/snacks`. | Reduces duplicate public entry points. |
| Manual QA | `npm run lint` completed with 0 errors and 9 warnings. | Current audit verified lint does not fail. |

## What Created Friction

| Friction | Evidence | Impact |
|---|---|---|
| Governance source missing | No governance/constitution file found under repo. | Governance review cannot be fully grounded. |
| Dirty/untracked repo state | `git status --short` shows many modified and untracked files, including comparison outputs and new comparison modules. | Clean-checkout reproducibility is not guaranteed. |
| Stale rollout docs | `docs/snacks_rollout_report_v1.md` still contains older 14-row language while current Snacks corpus has 18 products. | Future auditors may inspect the wrong state. |
| Deprecated generator still targets live file | `scripts/build-snacks-frontend-v2.ts` says it is deprecated but still writes `src/data/comparisons/snacks_frontend_v2.json`. | A well-intentioned rerun can regress the CE-approved corpus. |
| No package validation script | `package.json` includes `dev`, `build`, `start`, and `lint`, but no corpus validation or typecheck script. | QA relies on manual one-off checks. |
| Category modules not fully self-contained | Snacks imports hero/filter/methodology data from legacy snack/blog modules. | Category rollout work has hidden dependencies outside the comparison module. |

## Repeated Work Observed

| Repeated work | Files / pattern | Standardization opportunity |
|---|---|---|
| Thin category wrappers | `maadanim-comparison-page.tsx`, `snacks-comparison-page.tsx`, `bread-comparison-page.tsx` | Generate or standardize a minimal category wrapper pattern. |
| Page-data loaders | `maadanim-page-data.ts`, `snacks-comparison-page-data.ts`, `bread-comparison-page-data.ts` | Standardize metadata-line construction, internal-field stripping, and filter validation. |
| Shelf filter modules | `maadanim-shelf-filters.ts`, `snacks-shelf-filters.ts`, `bread-shelf-filters.ts` | Keep the pattern, but require filters to read from the comparison corpus or category-local VM fields. |
| Legacy redirect pages | `src/app/compare/*`, `src/app/hashvaot/*` legacy routes | Maintain a route migration checklist per category. |
| Manual corpus checks | Ad hoc scans for v2 fields, score order, and forbidden terms | Add a repeatable `validate:comparison-corpus` script. |

## What Should Be Standardized Before Category #3

1. A discoverable governance source path.
2. A category rollout checklist covering corpus, route, registry, redirects, docs, QA, and launch state.
3. A corpus validation command that checks:
   - product count vs `_meta.product_count`
   - scored count vs `_meta.scored_count`
   - v2 reasoning field completeness
   - score-descending order
   - forbidden vocabulary in product-facing fields
   - internal field stripping
4. A rule that deprecated scripts cannot write canonical production JSON.
5. A self-contained category comparison module boundary.
6. A documentation update gate that prevents stale row counts and stale readiness claims.
7. A clean git baseline before declaring a category live.
8. A status label for routes that exist in code but are not part of the declared production category list.

## Verification Notes

- Lint was run during this audit: `npm run lint` passed with 0 errors and 9 warnings.
- Build was not rerun during this audit.
- Typecheck was not rerun during this audit. `package.json` does not expose a `typecheck` script.
- User-reported build/lint/typecheck pass is recorded, but build/typecheck are `NOT VERIFIED` by this audit.
