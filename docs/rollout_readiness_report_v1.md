# Rollout Readiness Report v1

**Status:** Planning assessment — no implementation.  
**Date:** 2026-05-29  
**Reference:** `docs/comparison_ui_reference_v1.md`  
**Canonical live:** `/hashvaot/maadanim` only

---

## 1. Executive summary

Bari has a **production-ready shelf platform** for מעadנים (`ComparisonShelfPage` + registry + v2 corpus). **Bread** and **snacks** are not ready: they use separate architectures, lack v2 corpora in `src/data/comparisons/`, and resolve through legacy or disabled routes.

This report classifies remaining work as **HIGH**, **MEDIUM**, or **LOW** before each category can launch on the frozen comparison template.

**Platform readiness for disciplined rollout:** Partial — foundation exists; category corpora, routes, and legacy retirement are the gating work.

---

## 2. Platform foundation (complete vs gap)

| Capability | מעadנים | Bread | Snacks |
|------------|---------|-------|--------|
| `ComparisonShelfPage` stack | Live | Not used | Not used |
| `BariProductVM` corpus in `src/data/comparisons/` | Yes | No | No |
| Registry entry | Yes | No | No |
| Canonical `/hashvaot/{slug}` | Yes | No (`/compare/...`) | No (404) |
| Category shelf filters module | Yes | No (cluster filters in dashboard) | No (engine filters) |
| Corpus validation CI | No | No | No |
| Production QA script on canonical URL | Partial | No | No |

---

## 3. Bread — readiness before frozen template launch

### HIGH (blocking)

| Item | Detail |
|------|--------|
| **v2 corpus does not exist** | No `bread_frontend_v2.json`. Curated data is `bread-retail-curated.json` with `BreadProduct` shape, not `BariProductVM`. |
| **Expansion v2 not authored** | Dashboard shows fiber, fermentation, structure in table cells — not `positiveSignals` / `limitingFactors` / `bottomLine` / `comparisonContext`. Requires editorial/export pass, not a code adapter alone. |
| **Wrong UI architecture in production** | `BreadComparisonDashboard` is full-width investigative UX (hero, stats, insight blocks, pairs, transparency archive, desktop table). Reference allows only hero → prologue → lenses → table → methodology. |
| **Route not canonical** | Live URL is `/compare/bread-comparison`; `/hashvaot/bread-comparison` redirects away from hashvaot family. |
| **Not in registry** | `ComparisonCategoryId` is maadanim-only; bread cannot use `createComparisonCategoryRoute`. |
| **Product decision: dashboard sections** | Insight blocks, pair cards, transparency archive must move to blog or be cut — cannot ship on `ComparisonShelfPage` without violating reference v1. |
| **Image coverage** | Most bread products lack `image_url` in curated data; `ProductRow` behavior vs `BreadShelfProductImage` mark must be validated for shelf UX. |

### MEDIUM

| Item | Detail |
|------|--------|
| **Shelf filter redesign** | Cluster single-select ≠ reference multi-select AND lenses. Need `bread-shelf-filters.ts` with new rules. |
| **Loader split** | `bread-page-data.ts` powers blog + dashboard; refactor risks article regressions without `bread-blog-data` split. |
| **Redirect matrix** | `/compare/bread-shufersal`, hashvaot index card, `BREAD_COMPARISON_HREF` all need coordinated updates. |
| **Metadata / copy trim** | Hero copy is stats-heavy English eyebrow; must become `CategoryHero` + `CategoryPrologue` Hebrew editorial tone. |
| **Scored vs unscored policy** | 31 scored + transparency products — confirm corpus includes insufficient rows at tail per מעadנים pattern. |
| **Corpus validation** | No CI gate; bread launch should not precede `comparison_corpus_validation_plan_v1.md` P1–P4. |

### LOW

| Item | Detail |
|------|--------|
| **Optional `BreadComparisonPage` wrapper** | Factory can render `ComparisonShelfPage` directly. |
| **`bread-comparison.json` synthetic set** | Legacy 20-product file; not wired to dashboard — retire or quarantine. |
| **Fiber in shared nutrition grid** | `ExpansionSection` omits fiber key (מעadנים parity); bread may want fiber visible — requires explicit design approval to change shared component. |

### Bread estimated critical path

1. Editorial v2 corpus export → 2. Validate → 3. `bread-page-data` + shelf filters → 4. Registry + `/hashvaot/bread` → 5. QA → 6. Redirects → 7. Retire dashboard.

---

## 4. Snacks — readiness before frozen template launch

### HIGH (blocking)

| Item | Detail |
|------|--------|
| **No repo-owned v2 corpus** | Products hardcoded in `snack-page-data.ts` (~53 fixtures), not `src/data/comparisons/snacks_frontend_v2.json`. |
| **SnackComparisonEngine is non-reference UX** | Search bar, card grid, modal `SnackProductDetailPanel`, map section, preset comparison moments, client **score sort** — all violate reference v1. |
| **Algorithm vocabulary in model/UI** | `SnackProduct` includes `nova`, `caps_applied`, `explainability_tags`; detail panel generates runtime copy via `snack-product-detail.ts` with caps/NOVA — forbidden on reference shelf. |
| **Routes disabled** | `/hashvaot/snack-bars` and `/compare/snack-bars` return `notFound()`. |
| **Not in registry** | Same as bread. |
| **Expansion v2 missing** | Snack UI uses custom sections (`why-this-landed-here`, score drivers) — not `ExpansionSection` v2 field set. |
| **Full v2 corpus authoring** | Entire snack shelf must be re-exported as pre-authored Hebrew `BariProductVM` rows; cannot promote fixtures to production. |

### MEDIUM

| Item | Detail |
|------|--------|
| **Snack shelf filters** | Engine uses `SnackEngineFilters` (grades, NOVA, score range) — must become category lenses without NOVA in chip labels if policy requires. |
| **Image hosts** | Yochananof URLs in fixtures — verify `next.config.ts` (already allowed). |
| **Blog vs comparison split** | `snack-editorial-content`, map annotations, flagship article — keep on blog; strip from comparison route. |
| **Redirect strategy** | `snack-bars` → `snacks` slug per `canonical_route_strategy_v1.md`. |
| **Hashvaot index** | Snacks not featured; add card when live. |

### LOW

| Item | Detail |
|------|--------|
| **Dev preview** | Maadanim-only; extend after registry. |
| **Categories marketing page** | `/categories/snacks` separate from comparison — link only. |

### Snacks estimated critical path

1. Audit pipeline → v2 JSON corpus → 2. Validate (forbidden terms critical for snacks) → 3. `snacks-page-data` + `snacks-shelf-filters` → 4. Registry + `/hashvaot/snacks` → 5. QA → 6. Redirects → 7. Quarantine `SnackComparisonEngine`.

---

## 5. Shared platform gaps (affect both bread and snacks)

| Item | Priority | Notes |
|------|----------|-------|
| Corpus validation in CI | HIGH | See `comparison_corpus_validation_plan_v1.md` |
| Registry ids `bread`, `snacks` | HIGH | See `comparison_registry_expansion_plan_v1.md` |
| Canonical routes + redirects | HIGH | See `canonical_route_strategy_v1.md` |
| Generalized dev API `/api/dev/comparison/[id]` | MEDIUM | Speeds QA |
| `/hashvaot` index lists live categories | MEDIUM | Discovery |
| `BariCategoryPageVM` adoption | LOW | Defer; registry shape sufficient for v1 |
| Milk on separate architecture | INFO | Out of scope — document to prevent confusion |

---

## 6. מעadנים — reference hardening (non-blocking for bread/snacks but recommended)

| Item | Priority |
|------|----------|
| Deduplicate route metadata vs `maadanimComparisonMetadata` | MEDIUM |
| Add maadanim to public category listing on `/hashvaot` | LOW |
| QA scripts target `/hashvaot/maadanim` not only `/dev/preview` | MEDIUM |
| Commit frozen reference assets to tracked release | LOW |

מעadנים is **launch-ready** today as the template; items above reduce drift risk during parallel category work.

---

## 7. Risk summary matrix

| Risk | Bread | Snacks |
|------|-------|--------|
| Architecture drift if dashboard/engine left routable | HIGH | HIGH |
| Malformed corpus reaches production | HIGH | HIGH |
| User-facing algorithm terms | MEDIUM | HIGH |
| SEO split across `/compare` and `/hashvaot` | HIGH | HIGH |
| Blog regressions during data module split | MEDIUM | LOW |
| Visual regression vs frozen מעadנים | MEDIUM | MEDIUM |

---

## 8. Recommended rollout order

1. **Platform:** Corpus validator CI + registry expansion types (no new public routes).
2. **Bread:** Corpus → `/hashvaot/bread` → redirects → retire dashboard.
3. **Snacks:** Corpus → `/hashvaot/snacks` → redirects → quarantine engine.
4. **Discovery:** Update `/hashvaot` index; audit external links.
5. **Later:** Milk migration (separate program).

Do **not** run bread and snacks public cutovers in parallel without separate QA owners — shared component changes affect מעadנים.

---

## 9. Definition of “ready to launch”

A category is **ready** when all are true:

- [ ] `{id}_frontend_v2.json` passes validation plan with zero ERRORs
- [ ] Registered in `comparisonCategoryRegistry`
- [ ] `/hashvaot/{id}` renders only `ComparisonShelfPage` stack
- [ ] Legacy routes redirect to canonical URL
- [ ] No forbidden vocabulary in corpus strings
- [ ] Product order matches signed-off shelf order (no client sort)
- [ ] Production QA checklist signed on canonical URL
- [ ] `/hashvaot/maadanim` regression check passed in same release

---

## 10. Related documents

| Document | Scope |
|----------|--------|
| `bread_migration_plan_v1.md` | Bread-specific architecture migration |
| `comparison_registry_expansion_plan_v1.md` | Registry types and ownership |
| `canonical_route_strategy_v1.md` | URLs and redirects |
| `comparison_corpus_validation_plan_v1.md` | CI validation rules |
| `comparison_ui_reference_v1.md` | Frozen UI/IA (מעadנים) |
| `comparison_architecture_audit_v1.md` | Technical audit snapshot |
| `duplicate_systems_audit_v1.md` | Legacy duplicate inventory |

---

## 11. Classification summary table

### Bread

| HIGH | MEDIUM | LOW |
|------|--------|-----|
| v2 corpus + expansion authoring | Shelf filter redesign | Optional page wrapper |
| Replace dashboard with shelf stack | Loader/blog split | Retire synthetic JSON |
| Canonical route + registry | Redirects + metadata copy | Fiber display policy |
| Editorial section relocation | Validation CI | |
| Image strategy | Unscored row policy | |

### Snacks

| HIGH | MEDIUM | LOW |
|------|--------|-----|
| v2 corpus (replace fixtures) | Shelf filters without engine | Dev preview generalization |
| Retire SnackComparisonEngine path | Image host verification | Marketing category page links |
| Remove algorithm exposure | Blog/comparison split | |
| v2 expansion authoring | Redirects + index | |
| Enable canonical route + registry | Validation CI | |

### Shared platform

| HIGH | MEDIUM | LOW |
|------|--------|-----|
| Corpus validation CI | Dev API generalization | `BariCategoryPageVM` merge |
| Registry bread + snacks entries | Hashvaot index discovery | |
| Canonical route strategy execution | מעadנים metadata dedup | |
