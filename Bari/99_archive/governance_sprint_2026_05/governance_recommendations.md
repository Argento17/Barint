# Governance Recommendations

**Status:** Planning document — recommendations only, no files moved.  
**Date:** 2026-05-17  
**Scope:** `C:\Bari\` repository structure, naming, and operational practices

---

## Executive summary

The Bari repository has grown organically across three pipeline stages (BSIP0, BSIP1, BSIP2) without a unifying structure. The result is functional but disorganized: framework documents and operational artifacts are co-mingled; freezes are buried inside operational directories; naming is inconsistent; and two directories (`BISP0`, `bsip2_concept`) are either empty or superseded without clear labeling.

The proposed target architecture (`01_framework / 02_products / 03_operations / 99_archive`) addresses each of these issues. This document provides recommendations for how to execute the migration and maintain the structure going forward.

---

## Recommendation 1: Execute migration in two phases

**Phase 1 — Freeze and archive (low risk, reversible):**
1. Create a complete freeze of `bisp2_concept_v1` before touching anything (see `freeze_inventory.md`)
2. Move `BISP0\` to `99_archive\bisp0_placeholder\` with a `README.md` explaining it was an empty placeholder
3. Move `bisp2_concept\` to `99_archive\bisp2_concept_prototype\`
4. Delete `bisp2_concept\__pycache__\` before archiving
5. Delete `bsip0_scrape\docs\CHANGELOG_BSIP0_v0_2.md` (duplicate; canonical copy is in `bsip_freezes\`)
6. Delete `bsip0_scrape\schemas\` (empty; schemas were never written)

**Phase 2 — Move active directories (medium risk, plan import paths first):**
1. Extract `bsip0_scrape\bsip_freezes\bsip0_v0_2\` to `01_framework\freezes\bsip0_v0_2\`
2. Move `bisp2_concept_v1\` to `01_framework\bsip2_framework\`
3. Move `bsip0_pipeline\` to `03_operations\bsip0\pipeline\`
4. Move `bsip0_scrape\` (remainder after freeze extraction) to `03_operations\bsip0\scrape\`
5. Move `bsip1_concept\batch_test_001\` to `03_operations\bsip1\run_001\`
6. Move `bsip2_proto_v0\` to `03_operations\bsip2\proto_v0\`

**Why two phases:** Phase 1 is purely additive or moves clearly inactive content. It can be done immediately with minimal risk. Phase 2 moves active operational directories and requires verifying that hardcoded paths in scripts are updated or that the run environment is reconfigured.

---

## Recommendation 2: Resolve the two path encoding problems before Phase 2

### Problem A — Hardcoded absolute paths in scripts

Several scripts in `bsip2_proto_v0\src\` are likely to reference paths like `C:\Bari\bsip2_proto_v0\outputs\`. When the directory moves to `C:\Bari\03_operations\bsip2\proto_v0\`, any hardcoded path breaks.

**Action before Phase 2:**
- Grep all Python files in `bsip2_proto_v0\src\` for `C:\Bari` path literals
- Replace hardcoded absolute paths with paths computed relative to the script location (`__file__`) or driven by a config file
- Verify the batch runner (`batch.py`) and any path-referencing scripts resolve paths dynamically

### Problem B — `bsip1_concept` import paths

`batch_test_001.py` in `bsip1_concept\` likely imports from a relative location or has a hardcoded path to BSIP0 outputs or BSIP2 code. Verify before moving.

---

## Recommendation 3: Create `02_products` structure from existing scrape outputs

The `02_products\` layer does not yet exist. Products are currently scattered inside retailer-specific subdirectories under `bsip0_scrape\`. The target structure is category-first:

```
02_products\snack_bars\carrefour\
02_products\snack_bars\yohananof\
02_products\chocolates\carrefour\
...
```

**Action:** After Phase 2, audit the `bsip0_scrape\carrefour\outputs\` and `bsip0_scrape\yohananof\outputs\` directories to determine product categories and organize accordingly under `02_products\`.

**Note:** Do not create `02_products` as a copy of scraper outputs — scraper outputs remain in `03_operations\bsip0\scrape\`. `02_products` is the curated, cross-retailer, category-organized product data store. This distinction matters for BSIP1's consolidation role.

---

## Recommendation 4: Complete the incomplete `bisp2_concept_v1` freeze

The current freeze at `freezes\bsip2_concept_v1\` captures only `docs\scoring\` and is missing most of the documentation. Before migrating the live `bisp2_concept_v1\` directory, create a complete snapshot.

**Immediate action:**
1. Create `01_framework\freezes\bsip2_concept_v1_complete\` (or as a staging step, create it at `freezes\bsip2_concept_v1_complete\`)
2. Copy all contents of current `bisp2_concept_v1\` to this freeze directory
3. Add a `freeze_metadata.md` with the date and state (see template in `freeze_inventory.md`)
4. Rename the old partial freeze to `bsip2_concept_v1_partial_early\` to flag its incomplete state

---

## Recommendation 5: Establish a `governance\README.md` and directory conventions file

The `governance\` directory itself should have a `README.md` that:
- Explains this is planning-only documentation
- Lists the five documents and their purposes
- States the current migration status (phase 1 complete / phase 2 complete / etc.)
- Is updated as migration progresses

Additionally, create a top-level `ARCHITECTURE.md` in `C:\Bari\` that provides a one-page orientation:
- What each top-level directory contains
- How the three pipeline stages relate to the directories
- Who maintains what

---

## Recommendation 6: Long-term — adopt a product ID convention at BSIP0 level

Currently, product IDs (`product_001` through `product_010` in `bsip0_pipeline`, various names in `bsip0_scrape`) are inconsistent. The BSIP2 outputs use product IDs derived from BSIP1 (which are hashes or file-based names).

**Recommendation:** Define a stable product ID convention at BSIP0 level:

```
{retailer_code}_{category_code}_{sequence}
# Example:
CAR_SB_001    ← Carrefour, snack bar, product 001
YOH_SB_001    ← Yohananof, snack bar, product 001
```

This ID should persist through BSIP1 (consolidation) and BSIP2 (scoring), and be the filename base for all per-product JSON outputs.

This is a design decision with downstream implications — it should be planned before adding more products to the dataset.

---

## Risk register

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Hardcoded paths break after Phase 2 move | High | High | Audit and fix before moving; run batch after move to verify |
| Partial freeze misleads about framework state | Medium | Medium | Rename partial freeze; create complete freeze first |
| Moving `bsip1_concept` breaks BSIP2 input assumptions | Medium | Medium | Check `batch.py` and `score_engine.py` for BSIP1 output path references |
| Category-first reorganization of products requires re-wiring scraper outputs | Low | Medium | `02_products` is a new layer; scraper outputs remain in `03_operations`; no existing scripts break |
| Archive of `bisp2_concept` removes tests that later prove useful | Low | Low | Archive is read-only, not deleted; tests remain accessible |
| Freeze of `bsip2_proto_v0` captures a state with known issues (before positive structure) | Low | Low | Freeze metadata should note this is pre-positive-structure state |

---

## Immediate actions (before any migration)

In order of priority:

1. **Create complete `bisp2_concept_v1` freeze** — captures all positive structure documents written in this session; freeze is lost if directory is moved without it
2. **Audit hardcoded paths in `bsip2_proto_v0\src\`** — prerequisite for Phase 2
3. **Execute Phase 1** (archive empty/superseded, delete duplicates) — safe, reversible, clears clutter immediately
4. **Create `governance\README.md`** — tracks migration progress going forward
5. **Plan Phase 2 timing** — Phase 2 can wait until a natural development pause; Phase 1 can happen now

---

## What is NOT recommended

**Do not reorganize products before BSIP1 is running cross-category.** The category-first product structure is the right end state, but building it now with only 64 scraped products across two retailers is premature. Create the `02_products` skeleton when adding the third retailer or the second category type.

**Do not delete `bisp2_concept` without extracting any tests worth keeping.** The `tests\` directory in the pre-v1 prototype may contain test logic (golden products, concern coordinator tests) that has conceptual value even if the code is superseded. Review before archiving.

**Do not merge `bsip0_pipeline` and `bsip0_scrape` into a single `bsip0` directory** unless their code is actually integrated. They are currently independent tools (OCR extraction vs. web scraping). Merging them structurally implies an integration that hasn't been built.

**Do not create a `bsip0_framework` documentation directory** until BSIP0 design is stable. The BSIP0 implementation is still evolving (scraping conventions, schema format, product ID conventions not decided). Creating framework docs prematurely will require constant updates.
