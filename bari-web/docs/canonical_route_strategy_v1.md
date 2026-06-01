# Canonical Comparison Route Strategy v1

**Status:** Planning only — no implementation.  
**Date:** 2026-05-29  
**Frozen reference route:** `/hashvaot/maadanim`

---

## 1. Problem statement

Bari currently operates **multiple route families** for comparisons:

| Family | Example paths | Stack |
|--------|---------------|--------|
| **Hashvaot shelf (reference)** | `/hashvaot/maadanim` | `ComparisonShelfPage` + `BariProductVM` |
| **Hashvaot legacy redirect** | `/hashvaot/bread-comparison` | → `/compare/bread-comparison` |
| **Compare legacy** | `/compare/bread-comparison`, `/compare/bread-shufersal`, `/compare/snack-bars` | Bread dashboard or `notFound` |
| **Hashvaot disabled** | `/hashvaot/snack-bars` | `notFound()` |
| **Hashvaot editorial (milk)** | `/hashvaot/milk-comparison` | `MilkComparisonPage` (separate architecture) |
| **Dev** | `/dev/preview` | Client fetch maadanim corpus |

This splits SEO, analytics, and engineering mental models. Category scaling requires **one routing model** for shelf comparisons.

---

## 2. Recommendation: canonical route family

### 2.1 Production comparisons (shelf template)

**Canonical base:** `/hashvaot/{categorySlug}`

| Category | Canonical path | Status |
|----------|----------------|--------|
| מעדנים | `/hashvaot/maadanim` | **Live — frozen reference** |
| לחם | `/hashvaot/bread` | Planned |
| חטיפים | `/hashvaot/snacks` | Planned |

**Properties:**

- Static Next.js app routes (build-time corpus import).
- Registered in `comparisonCategoryRegistry`.
- Render `ComparisonShelfPage` (directly or via thin category wrapper).
- Listed on `/hashvaot` index when `status: live`.

### 2.2 What is NOT canonical for shelf comparisons

| Path pattern | Disposition |
|--------------|-------------|
| `/compare/*` | Legacy — redirect to `/hashvaot/{slug}` |
| `/hashvaot/bread-comparison` | Legacy — redirect to `/hashvaot/bread` |
| `/hashvaot/snack-bars` | Legacy — redirect to `/hashvaot/snacks` |
| `/categories/snacks` | Marketing/category hub — **not** the comparison engine |

### 2.3 Milk and blog (explicitly separate)

| Path | Role |
|------|------|
| `/hashvaot/milk-comparison` | Legacy editorial comparison — **out of shelf rollout v1** |
| `/blog/*` | Long-form analysis; may link to canonical comparisons |

Do not force milk into `/hashvaot/{slug}` shelf template until a dedicated milk migration is approved.

### 2.4 Dev routes

| Path | Role |
|------|------|
| `/dev/preview?category=` | Multi-category smoke (post-registry expansion) |
| `/api/dev/comparison/[categoryId]` | Corpus JSON for dev preview |

Dev routes are **never** canonical for users or SEO.

---

## 3. Redirect strategy

### 3.1 Principles

- **301/308 permanent redirects** from legacy paths to canonical (Next `redirect()` in route files).
- **Never** chain more than one hop (audit all redirect sources).
- Update **in-repo** links before external comms (`BREAD_COMPARISON_HREF`, hashvaot cards, blog CTAs).

### 3.2 Redirect matrix (target state)

| Legacy path | Redirect target | When |
|-------------|-----------------|------|
| `/compare/bread-comparison` | `/hashvaot/bread` | Bread Phase 4 |
| `/compare/bread-shufersal` | `/hashvaot/bread` | Same |
| `/hashvaot/bread-comparison` | `/hashvaot/bread` | Same (replace current redirect to `/compare`) |
| `/compare/snack-bars` | `/hashvaot/snacks` | Snacks cutover |
| `/hashvaot/snack-bars` | `/hashvaot/snacks` | Same |
| `/api/dev/maadanim` | `/api/dev/comparison/maadanim` | Optional alias after API generalization |

**מעadנים:** No redirect changes — already canonical.

### 3.3 Link constant migration

| Constant / component | Current | Target |
|---------------------|---------|--------|
| `BREAD_COMPARISON_HREF` | `/compare/bread-comparison` | `/hashvaot/bread` |
| Hashvaot bread card | uses `BREAD_COMPARISON_HREF` | `/hashvaot/bread` |
| Snack flagship links | blog-defined | `/hashvaot/snacks` |

### 3.4 External links

**Not verified in audit:** inbound links, newsletters, social, Search Console.

**Action before cutover:** run link crawl (GSC, analytics, `rg` on repo) for `/compare/` paths.

---

## 4. Legacy route handling

### 4.1 Tier classification

| Tier | Definition | Action |
|------|------------|--------|
| **T0 Canonical** | `/hashvaot/maadanim`, future bread/snacks | Maintain; registry-owned |
| **T1 Legacy redirect** | `/compare/*`, old hashvaot slugs | Permanent redirect |
| **T2 Quarantine** | `BreadComparisonDashboard`, `SnackComparisonEngine` | Remove from routes; keep in repo until blog dependencies cleared |
| **T3 Parallel legacy** | Milk comparison | Document; no redirect until milk program |
| **T4 Dev-only** | `/dev/preview`, dev APIs | Document; robots/noindex if needed |

### 4.2 `notFound()` routes today

- `/hashvaot/snack-bars`, `/compare/snack-bars` return 404.

**Plan:** Replace `notFound()` with redirect to `/hashvaot/snacks` **only when** snacks shelf is production-ready. Until then, keep 404 or a minimal "בקרוב" holding page — **product decision** (404 avoids false launch; holding page preserves URL equity).

### 4.3 Compare namespace retirement

Long-term: **no new routes under `/compare/`**.

Existing `/compare/*` files become redirect-only stubs (minimal bundle). Remove duplicate page components from compare routes.

---

## 5. Rollout sequence

### Wave 0 — Foundation (complete / in progress)

- [x] `ComparisonShelfPage` + registry for maadanim
- [x] `docs/comparison_ui_reference_v1.md` frozen
- [ ] Corpus validation CI (planned — see validation plan)

### Wave 1 — מעadנים hardening (no URL change)

- Deduplicate metadata sources for maadanim route.
- QA production route (`/hashvaot/maadanim`) as mandatory gate.
- Add maadanim to `listComparisonCategories()` for index when ready to surface.

### Wave 2 — Bread

1. Publish `/hashvaot/bread` (preview/staging).
2. QA sign-off on frozen template.
3. Flip redirects from `/compare/bread-comparison`.
4. Update hashvaot index card.
5. Retire bread dashboard route component from production.

### Wave 3 — Snacks

1. Publish `/hashvaot/snacks`.
2. QA sign-off.
3. Enable redirects from snack legacy paths.
4. Retire `SnackComparisonEngine` from any production route.
5. Update blog CTAs.

### Wave 4 — Platform cleanup

- Generalize dev API + preview.
- Parameterize QA scripts.
- Document route map in README or `docs/comparison_routes.md`.
- Evaluate milk migration separately.

### Wave 5 — Index and discovery

- `/hashvaot` lists all `live` registry categories with consistent cards (מעadנים, bread, snacks).
- Deprioritize or relabel milk/bread dashboard CTAs that imply non-canonical UX.

---

## 6. Routing model diagram

```text
                    ┌─────────────────────────────┐
                    │      /hashvaot (index)      │
                    └──────────────┬──────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
 /hashvaot/maadanim          /hashvaot/bread           /hashvaot/snacks
 (FROZEN)                   (planned)                 (planned)
         │                         │                         │
         └─────────────────────────┴─────────────────────────┘
                                   │
                    ComparisonShelfPage + BariProductVM corpus
```

```text
Legacy (redirect only):
  /compare/bread-comparison  ──► /hashvaot/bread
  /hashvaot/bread-comparison ──► /hashvaot/bread
  /compare/snack-bars        ──► /hashvaot/snacks
  /hashvaot/snack-bars       ──► /hashvaot/snacks
```

---

## 7. SEO and metadata rules

- One canonical URL per category — use `metadata.alternates.canonical` if duplicate paths exist during transition.
- Titles/descriptions owned by `{category}-page-data.ts` / registry `metadata`.
- No indexing of `/dev/*` or `/api/dev/*`.

---

## 8. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Redirect loops bread-comparison ↔ compare | HIGH | Single target `/hashvaot/bread`; delete intermediate redirect to `/compare` |
| Split traffic during Wave 2 | MEDIUM | Short transition window; monitor analytics |
| Snacks 404 → live flip breaks bookmarks | MEDIUM | Communicate; use redirect not 404 when launching |
| Milk remains on different UX | LOW | Document as intentional; index copy clarifies |
| `/hashvaot/maadanim` altered accidentally | HIGH | Code review rule: maadanim route frozen without explicit approval |

---

## 9. Decision log (recommended defaults)

| Question | Decision |
|----------|----------|
| Canonical prefix | `/hashvaot/` only for shelf comparisons |
| Bread slug | `bread` (not `bread-comparison`) |
| Snacks slug | `snacks` (not `snack-bars`) |
| Compare namespace | Redirect-only, no new features |
| Dynamic `[category]` route | Defer until 3 categories stable |
| Milk | Remain on `/hashvaot/milk-comparison` until separate plan |

---

## 10. Acceptance criteria

- [ ] Documented redirect matrix implemented for bread and snacks at cutover.
- [ ] All in-repo CTAs point to `/hashvaot/{slug}`.
- [ ] Registry `routePath` matches filesystem routes exactly.
- [ ] No production comparison uses `/compare/` as primary entry.
- [ ] `/hashvaot/maadanim` unchanged in behavior and URL.
