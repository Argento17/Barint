# Comparison Corpus Validation Plan v1

**Status:** Planning only — no implementation.  
**Date:** 2026-05-29  
**Applies to:** `src/data/comparisons/{category}_frontend_v2.json` → `BariProductVM[]` via `loadComparisonCorpus`

---

## 1. Purpose

Prevent malformed category datasets from reaching production. Validation runs **at build time or CI** before merge — not in the browser. The UI (`ProductTable`, `ExpansionSection`) assumes well-formed VMs and has minimal runtime guards.

---

## 2. Validation pipeline (target)

```text
{category}_frontend_v2.json
  → JSON schema / TypeScript structural validate
  → business rules (ids, order, copy policy)
  → image URL policy check
  → strip _calibration (loadComparisonCorpus)
  → BariProductVM[]
```

**Suggested location:** `scripts/validate-comparison-corpus.mjs` or `src/lib/comparisons/validate-corpus.ts` invoked from `npm run validate:corpus` and CI.

**Gate:** `npm run build` fails if any registered category corpus fails validation.

---

## 3. File-level requirements

### 3.1 Top-level shape

| Rule | Severity |
|------|----------|
| Root object has `_meta` and `products` | ERROR |
| `products` is non-empty array | ERROR |
| `_meta.product_count === products.length` | ERROR |
| `_meta.category` matches registry category id | ERROR |
| `_meta.generated` is ISO-8601 parseable | WARN if invalid |
| `_meta.version` present for production corpora | WARN |
| No unknown top-level keys that affect UI | INFO |

### 3.2 Internal fields

| Rule | Severity |
|------|----------|
| `_calibration` allowed on products but must strip before UI | INFO (loader handles) |
| No other `_`-prefixed keys on products exposed to UI | WARN |

---

## 4. Product identity

### 4.1 Unique product ids

| Rule | Severity |
|------|----------|
| Every `product.id` is non-empty string | ERROR |
| All `id` values unique within corpus | ERROR |
| `id` stable (no whitespace-only) | ERROR |
| Recommended pattern: `{source}_{category}_{barcode}` or documented prefix | WARN if inconsistent |

### 4.2 Ordering

| Rule | Severity |
|------|----------|
| Corpus defines final shelf order | ERROR (documented) |
| Scored products (`score !== null`) appear before unscored | ERROR |
| Among scored, `score` is non-increasing (desc) | WARN (flag inversions) |
| Client must not re-sort — validate corpus not app | INFO |

---

## 5. Required VM fields (`BariProductVM`)

Per `src/lib/view-models/index.ts`:

| Field | Validation |
|-------|------------|
| `id` | string, non-empty |
| `name` | string, non-empty |
| `imageUrl` | `string \| null` |
| `score` | `number \| null`; if number, integer 0–100 |
| `grade` | `A\|B\|C\|D\|E \| null`; if scored, grade should be present |
| `insightLine` | string (empty allowed — hides slot) |
| `confidence` | `verified \| partial \| insufficient` |
| `expansion` | object, always present |

### 5.1 Score / grade consistency

| Rule | Severity |
|------|----------|
| `score === null` ⇒ `grade === null` (unscored) | ERROR |
| `score !== null` ⇒ `grade !== null` | ERROR |
| Grade aligns with score bands (document band table) | WARN |

---

## 6. Expansion fields (`BariExpansionVM`)

### 6.1 Required substructure

| Field | Validation |
|-------|------------|
| `confidenceLabel` | non-empty string |
| `servingNote` | non-empty string |
| `nutrition` | object or null |
| `ingredients` | string or null |

### 6.2 Interpretive v2 (reference UI)

Rendered when non-empty; order fixed in `ExpansionSection`.

| Field | Validation |
|-------|------------|
| `positiveSignals` | optional array of non-empty strings |
| `limitingFactors` | optional array of non-empty strings |
| `bottomLine` | optional non-empty string |
| `comparisonContext` | optional non-empty string |

| Rule | Severity |
|------|----------|
| At least one interpretive field populated for scored products | WARN |
| No empty strings inside signal arrays | ERROR |
| No duplicate lines within same product section | WARN |

### 6.3 Nutrition grid

When `nutrition` present:

| Field | Type |
|-------|------|
| `energyKcal`, `protein`, `sugar`, `fat`, `fiber`, `sodium` | number or null |

| Rule | Severity |
|------|----------|
| `0` is valid; do not coerce null to 0 | INFO |
| Values are per 100g/100ml (corpus responsibility) | INFO |

### 6.4 Forbidden vocabulary (user-facing strings)

Scan all string fields in product + expansion (including arrays) for forbidden tokens:

**ERROR if present (case-insensitive, Hebrew + English):**

- `BSIP`, `NOVA`, `cap`, `caps`, `dimension`, `GSS`, `ferm_q`, `fiber_q`, `routing`, `audit trace`, `scoring engine`
- Internal cluster ids exposed as copy (e.g. `wellness_ambig`)

Maintain allowlist file for false positives.

---

## 7. Metadata integrity

### 7.1 `_meta` required fields

| Field | Validation |
|-------|------------|
| `generated` | ISO date |
| `category` | matches filename / registry id |
| `product_count` | matches array length |

### 7.2 Optional fields

| Field | Use |
|-------|-----|
| `scored_count` | Should equal count of `score !== null` |
| `version` | e.g. `v2-production` |
| `schema` | e.g. `BariProductVM[]` |
| `production_pass` | audit notes — not shown in UI |

| Rule | Severity |
|------|----------|
| `scored_count` matches actual if present | ERROR |

### 7.3 Metadata line derivation

`formatComparisonMetadataLine(product_count, generated)`:

| Rule | Severity |
|------|----------|
| `product_count > 0` | ERROR |
| Invalid `generated` → fallback copy (acceptable) | WARN |

---

## 8. Image integrity

### 8.1 URL format

| Rule | Severity |
|------|----------|
| `imageUrl` null or absolute `https://` URL | ERROR |
| No `http://` in production corpora | WARN |
| No local paths (`/images/...`) unless supported | ERROR |

### 8.2 Next.js image config

Cross-check hosts against `next.config.ts` `images.remotePatterns`:

| Current allowed | Host |
|-----------------|------|
| Yes | `api.yochananof.co.il` |
| Yes | `res.cloudinary.com` (shufersal path) |

| Rule | Severity |
|------|----------|
| Every non-null `imageUrl` host allowed in config | ERROR at CI |
| Document new host → config change in same PR | PROCESS |

### 8.3 Broken image policy

| Rule | Severity |
|------|----------|
| Track % null `imageUrl` per category | WARN if > threshold (e.g. 50% bread) |
| Optional HEAD request smoke in nightly CI | INFO |

---

## 9. Category-specific extensions (optional meta)

Bread/snacks corpora may include extra `_meta` fields (retailer, scope). Validators should **ignore** unknown meta keys unless listed in category schema.

Category-specific product extensions must not appear in JSON — all data must map into `BariProductVM` before commit.

---

## 10. Registry integration

| Rule | Severity |
|------|----------|
| Every `ComparisonCategoryId` with `status: live` has passing corpus | ERROR in CI |
| Corpus filename convention: `{id}_frontend_v2.json` | ERROR |
| `getCorpusPayload()` matches validated file | INFO (unit test) |

---

## 11. Validation outputs

### 11.1 Reporter format

```text
[corpus:maadanim] OK — 90 products
[corpus:bread] FAILED — 3 errors, 2 warnings
  ERROR  products[12].id duplicate "shufersal_123"
  WARN   products[4].imageUrl host not in next.config
```

Exit code non-zero on ERROR; WARN configurable per environment.

### 11.2 PR checklist

- [ ] `npm run validate:corpus` passes
- [ ] `npm run build` passes
- [ ] Image hosts updated in `next.config.ts` if needed
- [ ] Manual spot-check 3 products in `/hashvaot/{category}`

---

## 12. Implementation phases (when approved)

| Phase | Deliverable |
|-------|-------------|
| P1 | Validator for maadanim only — baseline |
| P2 | Forbidden vocabulary scanner |
| P3 | Image host cross-check |
| P4 | Wire into CI + prebuild |
| P5 | Extend to bread/snacks as corpora land |

---

## 13. Non-goals

- Validating blog article JSON or `bread-retail-curated.json` legacy shape.
- Validating scoring algorithm correctness (audit pipeline separate).
- Runtime validation in React components (keep UI thin).

---

## 14. Reference: maadanim baseline metrics (audit snapshot)

Use as regression baseline when P1 validator ships:

| Metric | Value |
|--------|-------|
| Product count | 90 |
| Version | v2-production |
| Products with `_calibration` in raw JSON | 1 (stripped) |
| `positiveSignals` populated | ~58/90 (WARN-only if interpretive empty on scored) |

Re-run counts after validator implementation to lock expected ranges.
