# Hummus Frontend v1 — Build Report

**Task:** TASK-061
**Owner:** Data Agent
**Date:** 2026-05-31
**Source run:** `run_hummus_002` (AUTHORITATIVE) — `run_hummus_001` never read
**Decision applied:** TASK-060 / HUM-001 — Option B (suppress fat display)
**Output:** `C:\Bari\02_products\hummus\frontend\hummus_frontend_v1.json`
**Build script:** `build_hummus_frontend_v1.py` (reproducible)

---

## Result

| Metric | Value |
|---|---|
| Products | 69 |
| Scored | 67 (2 `insufficient` → null score/grade) |
| Grade distribution | A:8 · B:28 · C:27 · D:4 · (2 unscored) |
| Score range | 43–86 |
| Confidence | verified 61 · partial 6 · insufficient 2 |
| Nutrition panels (fat-free) | 67 |
| **fat values dropped** | **67** |
| Filters | 6 (all + 5 product types) |
| insightLine | "" for all 69 (placeholders) |
| Size | 76.9 KB |

Package sections delivered: category metadata, product records, scores, grades,
filters, insight placeholders, known limitations, QA notes. All present and validated.

---

## Provenance — run_hummus_002 only

- Authoritative score / grade / confidence / product-type were taken from the
  QA-reviewed `run_hummus_002` build; the build script **asserts**
  `_meta.source_run_id == "run_hummus_002"` and aborts otherwise.
- `run_hummus_001` is **never opened** by the build. It is recorded in
  `_meta.invalid_run_never_used` and `known_limitations[HUM-003]` for provenance only.
- Nutrition and ingredient text were joined from BSIP1 canonical records
  (`canonical_product_id`), 69/69 matched.

---

## HUM-001 implementation (Option B)

Fat is suppressed structurally, not blanked:

1. The nutrition panel is built from an explicit allow-list —
   `energy_kcal, protein_g, carbohydrates_g, sodium_mg, dietary_fiber_g`.
   `fat_g` and `saturated_fat_g` are **never copied in**.
2. A post-build **assertion** scans every product and fails the build if any
   nutrition key contains "fat". Build passed (0 leaks).
3. `_meta.suppressed_fields` records the suppression: fields, scope (all 69),
   reason (TASK-039 defect → TASK-060 Option B), `fat_present_in_source_dropped: 67`,
   and the v2 remediation plan.

Validation: the strings `fat_g` / `saturated_fat` appear in the file **only** inside
the `suppressed_fields` documentation manifest — **0 products** carry a fat value.

### Omitted fields

| Field | Why omitted | Where recorded |
|---|---|---|
| `fat_g` | HUM-001 / TASK-060 Option B (corrupt source) | `_meta.suppressed_fields`, `known_limitations[HUM-001]` |
| `saturated_fat_g` | Same; also absent from BSIP1 entirely | `_meta.suppressed_fields` |
| `sugars_g` | 0% coverage in BSIP1 (HUM-002) | `known_limitations[HUM-002]` |
| dimension scores / caps / penalties | Internal scoring detail — not consumer data | n/a (excluded by design) |

---

## Remaining data-quality issues

| ID | Severity | Issue | Disposition |
|---|---|---|---|
| HUM-001 | High | `fat_g` corrupt for ~58/69 (TASK-039) | Suppressed; fix scraper → run_hummus_003 → restore in v2 (Q3 2026) |
| HUM-002 | Medium | `sugars_g` 0% coverage | Accepted at category level; no sugar surfaced |
| HUM-003 | Low | run_001 misrouting | run_002 authoritative; run_001 unused |
| HUM-004 | High | 2 products have no nutrition → null score | `displayable=false` semantics: render "score unavailable" |

---

## Deployment assumptions

1. This file is the **Data Agent canonical** dataset. It is written under
   `C:\Bari` and is **not** auto-copied to the website. Deployment to
   `C:\bari\bari-web\src\data\comparisons\` is the Frontend Agent's action,
   after reconciliation (below).
2. `insightLine` is intentionally empty. Per-product editorial copy is owned by
   the Content Agent (TASK-067 content spec / TASK-073) and is injected downstream.
3. Filter display labels are factual category names; the Content Agent should
   ratify them against the label registry before launch.
4. The 2 `insufficient` products must render a "score unavailable" state, not a grade.
5. Go-live remains gated: QA verdict is **WARN** (TASK-072, warning W-1) and
   **DEC-002** (Product go-live approval) is pending on TASK-073.

---

## ⚠ Discrepancy surfaced — three divergent artifacts exist

This task asked to "create" the dataset, but related artifacts already exist and
**diverge**. I did not overwrite either of them. Flagging for Product / Frontend
reconciliation before deployment:

| Artifact | Path | Schema | Nutrition | Status |
|---|---|---|---|---|
| **This build (TASK-061)** | `02_products/hummus/frontend/hummus_frontend_v1.json` | package + BariProductVM | present, **fat-free** | new canonical |
| Deployed website file | `…\bari\src\data\comparisons\hummus_frontend_v1.json` | BariProductVM | **entirely null** | live, QA-reviewed (TASK-072) |
| Prior rich canonical | `02_products/hummus/hummus_frontend_v1.json` | internal (dimensions) | none | **stale — predates TASK-060** |

Key points:

1. **The deployed file suppresses the *entire* nutrition panel (all 69 null).**
   TASK-061 asks to suppress *fat only*. This build follows TASK-061 literally
   (nutrition kept, fat removed). **Product Agent must decide** which is intended:
   - (a) deploy nutrition-minus-fat per TASK-061/TASK-060, or
   - (b) keep the deployed "no nutrition panel" approach.
   I did not change the live file.

2. **The prior `build_frontend.py` predates TASK-060.** It self-documents
   *"TASK-060 file not found — TASK-045 rules applied"* and emits an internal
   dimension schema, not Option B. It should be **archived**; this build supersedes it.

3. **Ingredients:** the deployed file leaves `expansion.ingredients` empty (likely
   populated by the website transform layer, `hummus-comparison-page-data.ts`,
   per TASK-069). This build **does** include `ingredients_text_he` from BSIP1. If
   the transform layer also injects ingredients, the Frontend Agent should pick one
   source to avoid double-population.

**Recommendation:** Product Agent rules on the nutrition-panel question (1);
Frontend Agent then reconciles the deployed file to this canonical dataset (or
documents an explicit, intentional divergence). Archive the stale rich file (2).

---

## Reproduce

```powershell
cd C:\Bari\02_products\hummus\frontend
C:\Bari\.venv\Scripts\python.exe build_hummus_frontend_v1.py
```

The build is deterministic and re-asserts run_002 provenance and zero fat leakage
on every run.
