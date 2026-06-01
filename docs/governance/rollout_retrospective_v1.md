# Rollout Retrospective v1

Audit date: 2026-05-29  
Scope: Lessons from first multi-category comparison rollout, Maadanim to Snacks  
Mode: audit only

## Executive Summary

The Snacks rollout proved that the comparison platform can scale beyond Maadanim without redesigning the shelf UI. The shared shelf architecture held. The main problems are around governance traceability, corpus operations, stale documentation, and hidden coupling to legacy category modules.

## Successes

| Success | Evidence | Why it matters |
|---|---|---|
| Shared shelf architecture held | Snacks uses `SnacksComparisonPage -> ComparisonShelfPage`; Maadanim uses `MaadanimComparisonPage -> ComparisonShelfPage`. | The second category did not create a forked UI system. |
| v2 expansion fields are complete for Snacks | 18 / 18 products have `positiveSignals`, `limitingFactors`, `bottomLine`, and `comparisonContext`. | The canonical reasoning model scaled to a second category. |
| Product order is corpus-owned | Snacks corpus order is score-descending/non-increasing, and `ProductTable` does not sort. | Ranking logic stayed out of the UI. |
| No shelf-facing NOVA exposure found | Product-level scan found no forbidden vocabulary hits in Snacks. | Supports the stated no-NOVA shelf requirement. |
| Legacy snack routes redirect | `src/app/hashvaot/snack-bars/page.tsx` and `src/app/compare/snack-bars/page.tsx`. | Reduces duplicate live experiences. |
| Lint passes | `npm run lint` passed with 0 errors. | Basic code hygiene is intact. |

## Failures / Gaps

| Gap | Evidence | Impact |
|---|---|---|
| Governance constitution missing | Repo search found no governance/constitution file. | Compliance cannot be fully verified. |
| Stale rollout documentation | `docs/snacks_rollout_report_v1.md` still contains older 14-row language. | Audit and future rollout decisions can rely on wrong facts. |
| Deprecated corpus builder still writes live JSON | `scripts/build-snacks-frontend-v2.ts`. | A rerun can overwrite the CE-approved Snacks corpus. |
| Full source cohort not verifiable | Current repo has the 18-product display corpus, not the full 53 scanned / 48 scored source set. | Selection governance and ranking integrity for the full cohort are not independently auditable. |
| Snacks category module is not fully self-contained | Snacks imports from `snack-page-data.ts` and `snack-analysis-content.ts`. | Legacy changes can affect comparison behavior. |
| No automated corpus validator | `package.json` has no validation script. | QA depends on manual checks. |
| Dirty/untracked worktree | `git status --short` shows many modified/untracked files. | Production state is hard to reproduce from a clean checkout. |

## Risks

| Risk | Priority | Notes |
|---|---|---|
| Bread may appear architecturally ready while missing `limitingFactors` for all products. | HIGH | Category #3 should not use Snacks readiness as proof of Bread readiness. |
| Deprecated scripts can regress production JSON. | HIGH | This is an operational safety issue. |
| Governance reviews are subjective without the constitution file. | HIGH | The requested governance source is `NOT VERIFIED`. |
| Stale docs will compound by Category #5. | MEDIUM | Snacks already has current-state/report mismatch. |
| Legacy category dependencies can create hidden product/filter drift. | MEDIUM | Snacks filters rely on legacy `snackProducts`. |

## Recommendations

1. Add or link the canonical governance constitution in the repo.
2. Make corpus validation a package command before any new category launches.
3. Prevent deprecated builders from writing production JSON.
4. Require each category to declare whether it is production, preview, or legacy redirect.
5. Update rollout reports in the same PR as corpus count changes.
6. Standardize a self-contained category module template.
7. Keep full scanned/scored handoff manifests available for audit.
8. Commit or otherwise freeze the post-launch baseline before Category #3 work continues.

## Lesson Learned

The platform scaled technically before the operating model fully caught up. The next rollout should treat governance artifacts, validation scripts, and documentation freshness as launch requirements, not cleanup tasks.
