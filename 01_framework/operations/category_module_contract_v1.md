# Category Module Contract — v1

**Task:** TASK-130-A (Operating-Model Hardening)
**Owner:** data-qa-agent (data-agent workstream)
**Date:** 2026-06-01
**Status:** DRAFT — gate for Wave 2 (blocks TASK-132)
**Authority:** Self-contained. This is the single contract a category module must satisfy before frontend handoff. Per-category readiness rules (e.g. `hummus_web_readiness_rules.md`) refine, never override, this contract.
**Enforced by:** `validate-corpus` (spec in §7). A category that does not pass `validate-corpus` is not eligible for handoff regardless of any human sign-off.

---

## 0. Purpose & scope

Defines the **minimum, machine-checkable** contract a category must meet before it can move to frontend handoff. It exists because field-completeness drifted silently between categories (bread shipped with `limitingFactors` empty on 24/24 products; `unknowns` is empty on 6 of 7 live datasets) and there was no gate to catch it.

A "category module" is the full vertical slice for one comparison category:
- a registry definition (`src/lib/comparisons/registry/categories/<id>.ts`),
- a page-data assembler (`src/lib/comparisons/<id>-comparison-page-data.ts`),
- a frontend dataset (`src/data/comparisons/<id>_frontend_v<N>.json`),
- a route (`/hashvaot/<id>`).

"Handoff" = the data/QA side declares the dataset done and the Frontend Agent may wire/ship it. This contract governs the **data → frontend boundary**, not UI implementation.

---

## 1. Required files, fields & naming conventions

### 1.1 Required files (all four mandatory)

| File | Path | Purpose |
|---|---|---|
| Registry definition | `src/lib/comparisons/registry/categories/<id>.ts` | exports `<idCamel>CategoryDefinition: ComparisonCategoryDefinition` |
| Page-data assembler | `src/lib/comparisons/<id>-comparison-page-data.ts` | loads JSON, strips internal fields, exports `get<Id>PageData` + `get<Id>CorpusPayload` + `<id>ComparisonMetadata` |
| Frontend dataset | `src/data/comparisons/<id>_frontend_v<N>.json` | `{ _meta, products[] }`, `products` already ordered |
| Registry wiring | entry in `src/lib/comparisons/registry/index.ts` | id present in `comparisonCategoryRegistry` **and** in the `ComparisonCategoryId` union in `types.ts` |

### 1.2 Naming conventions (hard)

- **`id`** — kebab-case, matches across all four files and the route segment: `id` ∈ `ComparisonCategoryId` union, file stem, `_meta.category`, and `routePath` final segment are the **same string**. (`vegetable-spreads` is the live precedent.)
- **Dataset file** — `<id>_frontend_v<N>.json`, snake_case stem, integer version. Only one version per category may be imported by live page-data; older versions are deprecated (§4).
- **`routePath`** — typed literal `/hashvaot/<id>`.
- **Export symbols** — `<idCamel>CategoryDefinition`, `get<Id>PageData`, `get<Id>CorpusPayload`.

### 1.3 `_meta` fields (dataset)

Required: `generated` (ISO 8601), `category` (= `id`), `product_count` (= `products.length`), `schema` (= `"BariProductVM[]"`), `version`.
Required when any product is unscored: `scored_count` (= count of `score !== null`).
Recommended: `source_run_id`, `production_pass`, `scope_note`, `expansion`.

### 1.4 Product fields (`BariProductVM` — the canonical frontend contract)

Source of truth: `src/lib/view-models/index.ts`. Every product object must conform:

- **Top level (all required):** `id`, `name`, `imageUrl` (`string|null`), `score` (`0–100 int | null`), `grade` (`A–E | null`), `insightLine` (`string`, `""` allowed only to mean "no slot"), `confidence` (`verified|partial|insufficient`), `expansion` (object, always present).
- **`expansion` (always present):** `nutrition` (`BariNutritionVM|null`), `ingredients` (`string|null`), `confidenceLabel` (string), `servingNote` (string).
- **`expansion` interpretive fields:** `positiveSignals[]`, `limitingFactors[]`, `unknowns[]`, `caveats[]`, `bottomLine`, `comparisonContext`.

> **No internal fields in shipped products.** `_calibration`, `_website_cluster`, and any other `_`-prefixed key must be stripped by the page-data loader before reaching the UI (`stripInternalProductFields` / per-category strip). `validate-corpus` flags `_`-prefixed keys that survive into a payload but allows them in the raw dataset.

---

## 2. Corpus validation requirements

A dataset is **corpus-valid** when all hold:

1. **Schema conformance** — every product matches `BariProductVM` shape; no missing required keys, no type violations, `grade` ∈ `A–E|null`, `confidence` ∈ enum, `score` is integer `0–100` or `null`.
2. **Count integrity** — `_meta.product_count === products.length`; `_meta.scored_count === count(score !== null)` when present; no duplicate `id`.
3. **Scored/grade coherence** — `score !== null ⇔ grade !== null`. `confidence === "insufficient" ⇒ score === null && grade === null` (no-score state). A scored product may not have `grade === null`.
4. **Explanation completeness (the bread gap):** every **scored** product has `insightLine !== ""` **and** at least one of `positiveSignals[]` / `limitingFactors[]` non-empty. Field-completeness v2 additionally requires both `positiveSignals[]` and `limitingFactors[]` non-empty on scored products unless the category's readiness rules grant a documented exemption (hummus exempts `limitingFactors` for clean single-additive spreads — exemptions must be declared, not implicit).
5. **Unknowns when data missing** — if any `nutrition` field is `null` on a scored product, `unknowns[]` must be non-empty for that product (the suppressed-metric must be disclosed, not silently dropped). This is the rule that the 6/7 empty-`unknowns` datasets currently fail.
6. **No-score products explicit** — `confidence === "insufficient"` products carry a `caveats[]` / `unknowns[]` entry; never blank, `—`, or `N/A` semantics encoded as empty strings.
7. **Ordering** — `products` pre-ordered: scored descending by `score`, `insufficient` appended last. The UI never sorts; the dataset owns order.
8. **Prohibited-vocabulary scan** — no framework/health/recommendation tokens in any rendered string field (`insightLine`, `positiveSignals`, `limitingFactors`, `unknowns`, `caveats`, `bottomLine`, `comparisonContext`): NOVA, BSIP, cap/floor, dimension, weight, score-mechanics; health words (בריא/נקי/מסוכן); recommendations (מומלץ/כדאי/עדיף). (Heuristic gate; per-category readiness rules own the exhaustive list.)
9. **Image references resolve** — `imageUrl`, when non-null, points to an asset that exists under `public/`.

---

## 3. Frontend dataset handoff requirements

A category is **handoff-ready** when, in addition to §2:

1. **Wired** — the live page-data imports exactly one dataset version; the registry entry and `ComparisonCategoryId` union include the id; `getComparisonCategory(id)` resolves.
2. **Shared-corpus declared** — if the module renders from another category's dataset (live precedent: `vegetable-spreads` reads `hummus_frontend_v3.json` and filters), the page-data must (a) apply a deterministic filter and (b) record the source in `_meta.scope_note` or a code comment. A module that silently piggybacks on another category's corpus without a declared filter fails handoff.
3. **Internal fields stripped** — payload from `getCorpusPayload()` contains no `_`-prefixed keys.
4. **Copy present** — `ComparisonPageCopy` is complete: `hero.eyebrow`, `hero.title`, ≥2 `prologueSentences`, ≥1 `methodologyLines`. Hebrew, no framework vocabulary.
5. **Metadata line derivable** — `metadataLine` / `metadata` (`Metadata`) populated; `product_count` in copy is derived from rendered products, not hand-typed.
6. **Build-clean** — `next build` and `eslint` pass with the module wired; no type errors from the new dataset against `BariProductVM`.
7. **Committed baseline** — dataset + module committed; no uncommitted local edits in the handoff diff (TASK-130 "clean committed baseline").

---

## 4. Route / status / deprecation rules

### 4.1 Route

- One canonical route per category: `/hashvaot/<id>`. The final segment equals `id`. No two categories share a route.
- A route renders from exactly one **live** dataset version.

### 4.2 Module status (mirrors registry lifecycle)

| Status | Meaning | Frontend-visible? |
|---|---|---|
| `DRAFT` | dataset exists, fails ≥1 §2/§3 check | No |
| `READY` | passes `validate-corpus`, wired, build-clean | Yes (eligible to ship) |
| `LIVE` | route shipped, dataset is the imported version | Yes |
| `DEPRECATED` | superseded dataset version, not imported by any live page-data | No |

Status is derived, not asserted: `validate-corpus` reports `READY`/`DRAFT`; "LIVE" = imported by a route; "DEPRECATED" = present in `src/data/comparisons/` but imported by nothing.

### 4.3 Deprecation policy

- **Superseded dataset versions** (live cases: `hummus_frontend_v1.json`, `hummus_frontend_v2.json` — imported by nothing) are `DEPRECATED`. They must either be deleted or moved out of `src/data/comparisons/` once their successor is `LIVE` for one green build. Orphaned versions left in the live data dir are a `validate-corpus` **warning**, escalating to **error** at handoff time for the affected category.
- **Never delete the live version.** Deprecation acts only on versions no live page-data imports.
- **Route removal** requires registry de-listing (`index.ts` + `ComparisonCategoryId` union) in the same change; a route may not 404 with a dangling registry entry.

---

## 5. Launch QA gate

A category may not be declared launch-ready until every dimension passes. Dimensions 1–3 are **automatable** (owned by `validate-corpus`); 4–6 are **observed** (owned by QA Agent against a built page).

| # | Dimension | Pass criteria | Enforced by |
|---|---|---|---|
| 1 | **Data** | §2.1–§2.3, §2.7 (schema, counts, scored/grade coherence, ordering); no duplicate ids; `_meta` integrity | `validate-corpus` (blocking) |
| 2 | **Scoring** | every scored product has `score` 0–100 + matching `grade`; `score⇔grade` coherence; `insufficient⇒null/null`; distribution sane (no all-A, no all-null) | `validate-corpus` (blocking) |
| 3 | **Explanations** | §2.4–§2.6, §2.8 (insightLine present; ≥1 signal; unknowns when data missing; no prohibited vocab); reader can reconstruct "why this score" from expansion | `validate-corpus` (blocking) + QA spot-read |
| 4 | **UI** | page renders all products in dataset order; filters work; no orphaned counts; no blank/`—`/`N/A` cells; expansion sections render | QA Agent (built page) |
| 5 | **Mobile** | 360–414px viewport: no overflow, tap targets reachable, expansion usable, header/filters not clipped | QA Agent (Playwright + visual) |
| 6 | **Desktop** | ≥1024px: shelf layout, hover/expansion, image loading, methodology footer render | QA Agent (Playwright + visual) |

> Dimensions 4–6 reuse existing capture/QA scripts (`scripts/qa-maadanim-production.mjs`, `capture-*.mjs`, Playwright already a devDependency). `validate-corpus` does not assess rendered UI; it asserts the data is shaped such that the UI *can* be correct.

---

## 6. Recommended enforcement — how `validate-corpus` should enforce this

1. **Single command, exit-coded.** `validate-corpus [<id> | --all]` returns non-zero on any blocking failure. Wire as `npm run validate-corpus`. CI/handoff runs `--all`; per-category dev runs `validate-corpus <id>`.
2. **Errors vs warnings.** Errors (§2.1–§2.8, §3.1, §3.3, §3.6, §5 dims 1–3) block. Warnings (orphaned dataset versions §4.3, missing recommended `_meta` keys, image-resolution misses on `imageUrl`) report but don't block in dev — orphan/handoff warnings **escalate to errors under `--handoff`**.
3. **Per-product diagnostics.** Failure output names `id`, the failing rule number, and the offending value — not just a count. (The current "24/24 missing limitingFactors" must be reportable per product so it's fixable.)
4. **Baseline snapshots.** Persist a per-category JSON baseline (counts, scored_count, grade distribution, field-completeness %) under `scripts/baselines/<id>.json`. `validate-corpus` diffs against baseline and flags regressions (e.g. completeness dropping, product_count shrinking unexpectedly) so a category that was green can't silently rot. Baseline updates are explicit (`--update-baseline`).
5. **Reuse the real types.** Validate against `BariProductVM` from `src/lib/view-models` (import the types; don't re-describe the shape) so the gate and the UI contract can never disagree.
6. **Shared-corpus aware.** When a module reads another category's dataset, validate the **post-filter** product set the route actually renders, not the raw shared file.
7. **Handoff mode.** `validate-corpus <id> --handoff` runs all §2/§3 checks, asserts build-clean precondition, asserts clean git status for the module's files, and emits a `READY`/`DRAFT` verdict line suitable for pasting into a registry return.

---

## Deliverable summary

### Category module contract v1
Sections 1–4 above. Four required files, kebab-case `id` consistent across all of them, `BariProductVM` as the field contract, corpus-validity rules, handoff rules, and route/status/deprecation policy.

### Validation checklist
Per category, all must pass (blocking unless noted):

- [ ] Four required files present; `id` consistent across files, `_meta.category`, and route (§1.1–1.2)
- [ ] `_meta` complete; `product_count === products.length`; `scored_count` present when any unscored (§1.3)
- [ ] Every product conforms to `BariProductVM`; no surviving `_`-prefixed keys in payload (§1.4, §3.3)
- [ ] No duplicate `id`; schema/types valid (§2.1–2.2)
- [ ] `score ⇔ grade` coherence; `insufficient ⇒ null/null` (§2.3)
- [ ] Every scored product: `insightLine` present **and** ≥1 of `positiveSignals`/`limitingFactors` (§2.4) — **bread currently fails**
- [ ] `unknowns[]` non-empty when any `nutrition` field null (§2.5) — **6/7 datasets currently fail**
- [ ] No-score products explicit, never blank/`—`/`N/A` (§2.6)
- [ ] Products pre-ordered scored-desc, insufficient last (§2.7)
- [ ] No prohibited framework/health/recommendation vocabulary (§2.8)
- [ ] Module wired (registry + union + single live dataset import); build + eslint clean (§3.1, §3.6)
- [ ] Shared-corpus filter declared if reusing another category's dataset (§3.2) — applies to **vegetable-spreads**
- [ ] Copy complete (hero/prologue/methodology), Hebrew, derived counts (§3.4–3.5)
- [ ] Committed clean baseline (§3.7)
- [ ] Launch QA: data ✓ scoring ✓ explanations ✓ (automated) + UI ✓ mobile ✓ desktop ✓ (observed) (§5)
- [ ] No orphaned dataset versions in live data dir (§4.3) — **`hummus_frontend_v1/v2.json` currently orphaned**

### Required automation changes
1. Add `scripts/validate-corpus.ts` + `npm run validate-corpus` (`[<id>|--all|--handoff]`, exit-coded, per-product diagnostics) — §6.
2. Import and validate against `BariProductVM`; do not re-declare the shape — §6.5.
3. Add `scripts/baselines/<id>.json` snapshots + regression diff (`--update-baseline`) — §6.4.
4. Close the **bread `limitingFactors`** gap (24/24) and the cross-dataset **`unknowns`** gap before bread/others can pass `--handoff`.
5. Resolve orphaned `hummus_frontend_v1.json` / `hummus_frontend_v2.json` (delete or relocate) — §4.3.
6. Wire `validate-corpus --all` into the handoff/CI step that gates Wave 2 (TASK-132).

### Open risks
- **R1 — Existing datasets fail the new gate.** Turning on §2.5 (`unknowns`) errors fails 6/7 live datasets, including shipped pages. Mitigation: land `validate-corpus` in **warn** mode for already-LIVE categories, **error** mode for new handoffs, until backfill completes. Decision needed from Central Controller.
- **R2 — Exemption sprawl.** §2.4 lets readiness rules exempt `limitingFactors` (hummus does). Without a registry of declared exemptions, the gate weakens silently. Mitigation: exemptions must be a machine-readable field in the per-category readiness doc, read by `validate-corpus`.
- **R3 — Shared-corpus coupling.** `vegetable-spreads` depends on `hummus_frontend_v3.json`; a hummus dataset bump can break vegetable-spreads without an obvious signal. Mitigation: `validate-corpus` must validate the post-filter set for *both* routes whenever the shared file changes; baseline diff (§6.4) catches the count shift.
- **R4 — Prohibited-vocab scan is heuristic.** Hebrew token matching will miss paraphrases and false-positive on legitimate uses. It is a backstop, not the authority; per-category readiness rules + QA read remain the real gate.
- **R5 — UI/mobile/desktop stay human.** Dims 4–6 are not automated by this contract; they depend on QA Agent discipline. A category can pass `validate-corpus` and still ship a broken mobile layout. Acceptable for v1; candidate for a future visual-regression workstream.
- **R6 — Owner mismatch.** Brief names `data-qa-agent`; registry `TASK-130` records `owner: data-agent`. Cosmetic, but the registry is authoritative — reconcile on acceptance.

---

*Category Module Contract v1 — TASK-130-A — data-qa-agent — 2026-06-01*
*Field contract: `src/lib/view-models/index.ts` (`BariProductVM`). Enforced by: `validate-corpus` (§6–§7). Gates Wave 2 / TASK-132.*
