# Governance Compliance Review v1

Audit date: 2026-05-29  
Scope: Snacks implementation for `/hashvaot/snacks`  
Reference requested: Bari Comparison Governance Constitution v1

## Constitution Availability

`NOT VERIFIED`: No file matching "Bari Comparison Governance Constitution v1", "governance", or "constitution" was found under the repo during this audit.

This review therefore assesses the Snacks rollout against the governance dimensions named in the task:

- category coherence
- comparison eligibility
- ranking integrity
- distortion handling
- explanation quality

## Summary Verdict

Snacks is mostly compliant for the displayed shelf experience. The 18 displayed products are scored, ordered by score, and have complete v2 expansion reasoning fields. The largest governance gaps are traceability gaps rather than visible UI failures:

- The requested constitution source is not present in the repo.
- The full 53 scanned / 48 scored CE source corpus is not independently verifiable from the current repo snapshot.
- Distortion policy implementation, including `DISTORTION-001`, is `NOT VERIFIED`.
- Internal metadata in the Snacks JSON still mentions `BSIP2` and `NOVA`, although product-level and shelf-facing strings did not expose those terms.

## Criteria Review

| Criterion | Result | Evidence | Gap |
|---|---|---|---|
| Category coherence | Mostly compliant | `src/data/comparisons/snacks_frontend_v2.json` has `_meta.category = "snacks"` and 18 products. Route is `/hashvaot/snacks`. | The shelf is a selected 18-product display cohort from a larger stated scan. Full scan corpus is `NOT VERIFIED`. |
| Comparison eligibility | Partially verified | JSON `_meta` states 53 scanned, 48 scored, 18 selected. All 18 displayed rows are scored. | The underlying 48 scored products are not present as a verifiable source artifact in this repo snapshot. |
| Ranking integrity | Compliant for displayed set | Product order in `snacks_frontend_v2.json` was verified as score-descending/non-increasing across all 18 products. `ProductTable` does not sort. | Ranking integrity of the larger 48-product source set is `NOT VERIFIED`. |
| Distortion handling | Partially verified | JSON `_meta.editorial_note` documents exclusions including duplicate/indistinguishable variants and products lacking verification. | `DISTORTION-001` was not found as implemented policy. Constitution rules are `NOT VERIFIED`. |
| Explanation quality | Compliant structurally | All 18 products include `positiveSignals`, `limitingFactors`, `bottomLine`, and `comparisonContext`. `ExpansionSection` renders all four shared v2 fields. | Snacks has no ingredients and no populated nutrition values for the technical block. This may be acceptable by category, but it reduces explanation depth. |

## v2 Reasoning Field Coverage

| Field | Snacks coverage | UI integration |
|---|---:|---|
| `positiveSignals` | 18 / 18 | Rendered by `src/components/shared/expansion-section.tsx` |
| `limitingFactors` | 18 / 18 | Rendered by `src/components/shared/expansion-section.tsx` |
| `bottomLine` | 18 / 18 | Rendered by `src/components/shared/expansion-section.tsx` |
| `comparisonContext` | 18 / 18 | Rendered with label `הקשר במדף` in `src/components/shared/expansion-section.tsx` |

## Forbidden Vocabulary / Internal Exposure

Product-level Snacks strings were manually scanned for:

`BSIP`, `NOVA`, `cap`, `caps`, `dimension`, `GSS`, `ferm_q`, `fiber_q`, `routing`, `audit trace`, `scoring engine`

Result: no product-level hits.

Internal metadata in `src/data/comparisons/snacks_frontend_v2.json` still contains references to `BSIP2` and `NOVA` inside `_meta.editorial_note` and `_meta.production_pass`. This is not currently shelf-facing, but it should be treated as a hygiene risk if future tooling exposes metadata.

## Governance Gaps

| Gap | Location | Severity | Recommended action |
|---|---|---|---|
| Governance constitution not discoverable. | Repo-wide search | HIGH | Add or reference the canonical constitution in a stable docs path before Category #3 approval. |
| Full Snacks source cohort not verifiable. | `src/data/comparisons/snacks_frontend_v2.json` only contains the displayed 18 products. | HIGH | Keep the 53 scanned / 48 scored source artifact or an immutable handoff manifest in the repo or release bundle. |
| `DISTORTION-001` not found as implementation. | Repo-wide search | HIGH | Document current distortion handling status before relying on it for Bread or Category #5. |
| Deprecated script can overwrite CE-approved corpus. | `scripts/build-snacks-frontend-v2.ts` | HIGH | Retire, quarantine, or make the script non-writing. |
| Internal scoring vocabulary remains in JSON metadata. | `src/data/comparisons/snacks_frontend_v2.json` | MEDIUM | Either move internal metadata out of frontend JSON or enforce that metadata is never surfaced. |
| No automated corpus/governance validation script in `package.json`. | `package.json` | MEDIUM | Add a repeatable validation command for v2 fields, forbidden vocabulary, score order, and cohort counts. |

## Compliance Conclusion

Snacks is governance-compliant enough for the displayed shelf route, based on the visible implementation and local corpus. It is not yet governance-complete as an operating system because the constitution, full source cohort, and distortion policy are not independently verifiable from the repo.
