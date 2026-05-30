# Category Scaling Readiness v1

Audit date: 2026-05-29  
Scope: readiness after Maadanim and Snacks production comparison rollout  
Mode: audit only

## Current Evidence

| Signal | Evidence | Assessment |
|---|---|---|
| Production categories named by current status | Maadanim and Snacks | Category #3 is still treated as next rollout for this review. |
| Registry categories in code | `ComparisonCategoryId = "maadanim" | "bread" | "snacks"` | Bread is already wired in code. |
| Maadanim corpus | `maadanim_frontend_v2.json`: 90 products, 90 scored, v2 reasoning fields populated. | Mature reference category. |
| Snacks corpus | `snacks_frontend_v2.json`: 18 products, 18 scored, v2 reasoning fields populated. | Post-rollout category is live and aligned with shared shelf. |
| Bread corpus | `bread_frontend_v2.json`: 24 products, 24 scored, 24 positive signals, 0 limiting factors, 24 bottom lines, 24 comparison contexts. | Architecturally wired, not v2-complete by the same reasoning-field standard. |
| Shared shelf architecture | `ComparisonShelfPage` reused by Maadanim, Snacks, and Bread wrappers. | Architecture foundation is viable. |
| Validation automation | No validation script in `package.json`. | Scaling risk. |
| Documentation consistency | Snacks rollout doc contains stale 14-row language. | Scaling risk. |
| Governance source | Constitution file not found. | Scaling blocker for formal governance signoff. |

## Category #3: Bread

Verdict: architecturally close, governance/content readiness not complete.

Evidence:

- `/hashvaot/bread` exists in code.
- `src/components/comparisons/bread-comparison-page.tsx` uses the shared comparison shelf pattern.
- `src/lib/comparisons/registry/categories/bread.ts` registers Bread.
- `src/app/compare/bread-comparison/page.tsx` redirects to the canonical Bread comparison href.
- `src/data/comparisons/bread_frontend_v2.json` contains 24 products and all 24 are scored.

Blocking or near-blocking gaps:

- Bread has `limitingFactors` populated for 0 / 24 products. If BariProductVM v2 field completeness is mandatory, Bread is not ready.
- Bread route/code exists even though current production comparison categories are listed as Maadanim and Snacks. Actual production exposure state is `NOT VERIFIED`.
- Bread rollout should not proceed until governance rules, corpus validation, and route status are explicit.

## Category #5

Verdict: not ready without process hardening.

The shared architecture can probably support a fifth category, but the operating model is already showing drift at category two:

- Manual validation is replacing repeatable QA.
- Docs and corpus counts can diverge.
- Deprecated generators can still write production JSON.
- Category wrappers and data modules repeat patterns manually.
- Snacks filters still depend on legacy non-comparison data.
- Governance source is not discoverable.

Required before Category #5:

- Automated corpus validation.
- Self-contained category module contract.
- Clean route/status governance.
- Deprecation policy for old scripts and preview implementations.
- Clean committed baseline for production comparison assets.

## Category #10

Verdict: not ready.

At 10 categories, current risks become systemic:

- Manual audits will miss stale docs, hidden coupling, and route exposure drift.
- Repeated wrappers and page-data modules will create uneven behavior.
- Category filters may diverge into category-specific legacy dependencies.
- Without a validation command, v2 field completeness will be inconsistent.
- Without a discoverable governance source, compliance reviews will become subjective.
- Without a corpus manifest model, displayed subsets will be hard to trace back to full scanned/scored cohorts.

## Scaling Risk Matrix

| Risk class | 1 category | 3 categories | 10 categories |
|---|---|---|---|
| Architecture | Low | Medium if Bread ships with incomplete v2 fields | High without category module standardization |
| Performance | Low | Low to medium, based on current corpus sizes | Medium, especially if all categories add client-side filtering and large corpora |
| Maintenance | Low | Medium due repeated wrappers/data modules | High due duplicated route, data, filter, and docs patterns |
| Data/model compatibility | Low for Maadanim | Medium because Bread lacks `limitingFactors` | High unless validation becomes mandatory |
| Regression risk | Low | Medium due deprecated scripts and dirty baseline | High without automated checks and route governance |

## Readiness Conclusion

Bari is ready to continue with Category #3 only after Bread v2 field completeness and route exposure status are resolved. Bari is not ready for Category #5 or #10 as an operating model until validation, governance, documentation, and category-module standards are formalized.
