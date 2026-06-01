# Hummus Dataset Reconciliation Report

**Task:** TASK-080
**Owner:** Frontend Agent
**Date:** 2026-05-31
**Product ruling applied:** nutrition panel **visible**; `fat_g` + `saturated_fat_g` **suppressed**; do **not** null the whole panel.
**Outcome:** one authoritative frontend dataset, deployed and build-verified.

---

## 1. The three artifacts compared

| # | Artifact | Location | Schema | Nutrition | Fat | Run |
|---|---|---|---|---|---|---|
| 1 | TASK-061 canonical | `02_products/hummus/frontend/hummus_frontend_v1.json` | package + VM products | present (snake_case) | dropped | run_002 |
| 2 | Live website dataset | `…\bari\src\data\comparisons\hummus_frontend_v1.json` | BariProductVM | **entirely null** | n/a | run_002 |
| 3 | Legacy build output | `02_products/hummus/hummus_frontend_v1.json` | internal (dimension) | none | flagged unreliable | run_002 |

### Schema differences
- **#2 (live)** and **#1 (canonical)** both use **BariProductVM** products (`id, name, score, grade, insightLine, confidence, expansion`). #1 adds a category package wrapper (`filters`, `known_limitations`, `qa_notes`).
- **#3 (legacy)** uses a different internal schema (`product_id, dimension_scores, caps, penalties…`) that the website never consumes.
- **Critical nutrition-shape gap:** the website renders `expansion.nutrition` as **`BariNutritionVM`** — camelCase `{energyKcal, protein, sugar, fat, fiber, sodium}`. #1 carried bsip1 **snake_case** (`energy_kcal, protein_g…`), which the grid would not read. Neither #1 nor #2 was directly deployable under the ruling: #2 had null nutrition; #1 had the wrong key shape.

### Content differences
- **Scores/grades are identical** across #1 and #2 (both run_hummus_002): A:8 · B:28 · C:27 · D:4 + 2 unscored, scores 43–86. (#3 predates the routing/decision freeze and is not score-comparable.)
- **#2 suppressed the entire nutrition panel** (all 69 null) — the specific thing the Product ruling reverses.
- **#3 self-documents** `"TASK-060 file not found — TASK-045 rules applied"` → it **predates the HUM-001 decision** and never implemented Option B.

### Transform differences
- The website consumes the dataset through `lib/comparisons/hummus-comparison-page-data.ts`:
  - `loadComparisonCorpus()` reads `_meta` + `products` (extra `_meta` keys are ignored).
  - `stripHummusInternalFields()` drops 6 NOVA-1 chickpea products (69→63 displayed), strips `_product_type`, and **preserves `expansion`** (so nutrition flows through).
  - Filters come from `hummus-shelf-filters.ts`, **not** the JSON — so the JSON `filters` array is inert.
  - Hero/prologue/methodology copy is **hardcoded in the TS** (already states *"ערכי השומן אינם מוצגים…"*), not in the JSON.
- The nutrition grid (`expansion-section.tsx → NutritionGrid`) renders only the labels `energyKcal, protein, sugar, fat, sodium` and **hides any null cell**. So suppressing fat = `fat: null`; keeping the panel = other fields non-null.

---

## 2. Authoritative source chosen

**Source:** the TASK-061 canonical build, **rebuilt to the BariNutritionVM shape** and emitted as a single website-consumable artifact.

- Path (canonical): `02_products/hummus/frontend/hummus_frontend_v1.json`
- Build script (reproducible): `build_hummus_frontend_v1.py`
- Shape: `{ _meta (+ provenance, nutrition_policy, known_limitations, qa_notes), products: BariProductVM[] }`
- Nutrition per product: `{ energyKcal, protein, sugar:null, fat:null, fiber, sodium }`
  - **fat = null** → grid hides the cell (HUM-001 / Option B / ruling).
  - **sugar = null** → no coverage (HUM-002).
  - rendered cells: **energyKcal, protein, sodium** → panel is visible.
- Provenance: `run_hummus_002` only; the build **asserts** `source_run_id == run_hummus_002` and **never opens** `run_hummus_001`.

**Why this source:** it is the only option that satisfies the ruling exactly — real run_002 scores, a visible nutrition panel, and fat suppressed — in the precise VM shape the UI renders.

### Rejected sources
| Rejected | Reason |
|---|---|
| Live dataset (#2) as-is | Suppressed the **entire** nutrition panel — directly contradicts the ruling. |
| Legacy build output (#3) | Predates TASK-060 (*"TASK-060 file not found"*); wrong schema; not Option-B compliant. |
| TASK-061 canonical *as built* (#1) | Correct content, but nutrition in snake_case → would render an empty grid. Superseded by the VM-shape rebuild. |

---

## 3. Migration actions performed

1. **Rebuilt** the canonical dataset to `BariNutritionVM` shape (fat=null, sugar=null, energy/protein/sodium populated; ingredients carried from BSIP1). 69 products, 67 fat values dropped, 67 visible panels.
2. **Backed up** the pre-existing live file →
   `99_archive/hummus_dataset_reconciliation_TASK080/deployed_hummus_frontend_v1.PRE-TASK080.json`.
3. **Deployed** the canonical dataset verbatim to the website →
   `…\bari\src\data\comparisons\hummus_frontend_v1.json`. Canonical and deployed are **byte-identical (MD5 match)** — a single source of truth.
4. **Archived obsolete artifacts** (moved out of the active tree):
   - legacy `03_operations/bsip2/build_frontend.py` → `…/build_frontend.LEGACY-predates-TASK060.py`
   - stale `02_products/hummus/hummus_frontend_v1.json` → `…/rich_hummus_frontend_v1.STALE-predates-TASK060.json`
5. **Verified** (below).

---

## 4. Verification

| Check | Result |
|---|---|
| `npm run build` (Next.js, TS + SSG) | **PASS** — TypeScript clean; all 30 static pages generated, incl. `/hashvaot/hummus` |
| Nutrition shape == `BariNutritionVM` | PASS — keys exactly `{energyKcal, protein, sugar, fat, fiber, sodium}` |
| `fat == null` for all 69 | PASS — asserted in build (build fails otherwise) |
| Visible panels (energy/protein/sodium non-null) | 67 (the 2 `insufficient` correctly carry `nutrition: null`) |
| Live DOM render | nutrition labels `קק"ל / חלבון / נתרן` present; `סוכרים` absent |
| Canonical == deployed | PASS — MD5 identical |

**Determinism note:** `NutritionGrid` renders only non-null cells from `{energyKcal, protein, sugar, fat, sodium}`. With `fat=null` and `sugar=null` for every product, a fat row is structurally impossible to render while energy/protein/sodium show. The ruling is satisfied by construction, not by chance.

A clean automated screenshot of a single expanded row was not reliably captured (the page ships both mobile and desktop row variants in the DOM, so the off-screen variant is not clickable); recommend a manual visual spot-check at go-live. This does not affect the verified correctness above.

---

## 5. Final state

**One authoritative frontend dataset:**
`…\bari\src\data\comparisons\hummus_frontend_v1.json`
= verbatim copy of `02_products/hummus/frontend/hummus_frontend_v1.json`
(run_hummus_002 · 69 products · BariProductVM · nutrition visible · fat suppressed).

Obsolete artifacts archived under `99_archive/hummus_dataset_reconciliation_TASK080/`.

### Residual notes for go-live (unchanged by this task)
- `insightLine` placeholders remain empty (Content Agent — TASK-067/073); the transform supplies grade-level fallback text in the interim.
- QA verdict is **WARN** (TASK-072, W-1) and **DEC-002** (go-live approval) is still pending on TASK-073.
- Ingredients are now carried in the dataset (were empty before); they render via the existing ingredient list.

### Reproduce
```powershell
cd C:\Bari\02_products\hummus\frontend
C:\Bari\.venv\Scripts\python.exe build_hummus_frontend_v1.py
Copy-Item .\hummus_frontend_v1.json "C:\bari\bari-web\src\data\comparisons\hummus_frontend_v1.json" -Force
cd C:\bari\bari-web ; npm run build
```
