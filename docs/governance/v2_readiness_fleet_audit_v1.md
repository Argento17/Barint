# TASK-128-A — v2 Readiness Audit: Comparison Fleet

**Owner:** frontend-agent
**Date:** 2026-06-01
**Reference standard:** `handoff/comparison-v2-spec.md` (accepted direction, TASK-098) — the binding `comparison_ui_reference_v2.md` is **not yet authored** (hard gate; see Blockers).
**Fleet audited:** hummus · maadanim · snacks · yogurts · bread · milk

---

## 0. Method & key finding

Each category was checked against the v2 spec's 9 presentation/IA changes (#1–#9), the v2 **data contract** (`metrics{}` + `rowReason{}` on `BariProductVM`), and the v1 invariants it must preserve. Source of truth: `src/app/hashvaot/*`, `src/components/comparisons/*`, `src/lib/comparisons/*`, `src/lib/view-models/index.ts`, corpus `_meta` in `src/data/comparisons/*`.

**Single most important finding:** the v2 surface is gated by **shared-platform work, not per-category work.** Five of six categories (hummus, maadanim, snacks, yogurts, bread) already run on the *same* shared stack — mobile `ComparisonShelfPage` + desktop `BariComparisonDesktopPage`, both consuming `BariProductVM[]`. None of the v2-defining features (#1–#5, #7) exist anywhere yet, because the platform pieces they depend on are absent fleet-wide:

- `BariProductVM` has **no `metrics{}` block** (`protein_g`, `additive_count`, `base_pct`, …) → blocks the metric block (#2), the band rail data (#3 derives from score, OK) and the row reason (#5).
- `BariProductVM` has **no `rowReason{}`** → blocks strongest +/− on the collapsed row (#5).
- Confidence is still rendered in the 10px expansion footnote (`bari-product-shelf-row.tsx:192`), **not promoted to the row** (#6).
- The expansion still carries the **second "advanced" toggle** (`setAdvanced`, `bari-product-shelf-row.tsx:170`) that #7 explicitly removes.

So per-category readiness is really a question of **corpus/content maturity and category-specific debt**, layered on top of one shared Phase-1 platform build. milk is the exception — it is off-contract legacy and is not a shelf citizen at all.

---

## 1. Fleet readiness table

| Category | Route | Stack | Corpus | N (scored) | v2 data ready? | Classification |
|---|---|---|---|---|---|---|
| **maadanim** | `/hashvaot/maadanim` | shared shelf + desktop | `maadanim_frontend_v2.json` `v2-production` | 90 (90) | metrics derivable, no debt | **READY** (v2 pilot) |
| **hummus** | `/hashvaot/hummus` | shared shelf + desktop | `hummus_frontend_v3.json` `v3-explanation-layer` | 66 (64; 2 insufficient) | rich, but fat/sugar suppressed + confidence re-audit open | **NEEDS MINOR FIXES** |
| **bread** | `/hashvaot/bread` | shared shelf + desktop | `bread_frontend_v2.json` `v2-production` | 24 (24) | derivable; legacy duplicate routes live | **NEEDS MINOR FIXES** |
| **snacks** | `/hashvaot/snacks` | shared shelf + desktop | `snacks_frontend_v2.json` `v2-production` | 18 (18) | derivable, but documented data-lineage history | **NEEDS MINOR FIXES** |
| **yogurts** | `/hashvaot/yogurts` | shared shelf + desktop | `yogurts_frontend_v1.json` `v1-mvp-**manual**` | 13 (13) | corpus is manual MVP, not production | **NEEDS MAJOR WORK** |
| **milk** | `/hashvaot/milk-comparison` | **bespoke legacy** (`MilkComparisonProduct`, not in registry) | `milk-page-data.ts` (TS, not corpus JSON) | ~bespoke | not on `BariProductVM` at all | **LEGACY** |

*"READY" here = ready to be the v2 **pilot** once the shared platform + reference doc land; it does not mean v2 is already shipped (it is not, anywhere).*

---

## 2. Fleet-wide gaps (shared platform — apply to all 5 shelf categories at once)

These are built **once** in the shared stack, not per category:

| Spec | Gap | Where | Status |
|---|---|---|---|
| #1 | Dense row + compact/comfortable density toggle | `bari-product-shelf-row.tsx` / `product-row.tsx` | Not built (only `shelf`/`web` layout mode exists) |
| #2 | Column-aligned metric block (protein · additives · base%) | needs `metrics{}` on VM + row UI | Not built (data + UI) |
| #3 | Score-band jump rail (80+/70s/60s/50s/<50) | new chrome | Not built |
| #4 | Inline band dividers | product table | Not built |
| #5 | Strongest +/− on collapsed row | needs `rowReason{}` on VM | Not built (data + UI) |
| #6 | Confidence promoted to row (accuracy-gated) | `bari-product-shelf-row.tsx:192` | Not done — still 10px footnote (v1-safe / Phase 0) |
| #7 | Expansion restructure; **drop 2nd "advanced" toggle**; magnitude on limits | `bari-product-shelf-row.tsx:170` | Not done — `setAdvanced` toggle still present |
| #8 | Category disclosures once (header/methodology), not per-row | per-row `unknowns` | Partial — hummus fat-note lives in insight/methodology; per-row `unknowns` still carry category-wide gaps |
| #9 | Responsive dense table from `lg`, single-col mobile | shelf vs desktop split | Partial — a responsive split exists, but desktop is a hero+zebra reflow, **not** the dense aligned-metric table v2 specifies |
| Data | `metrics{}` + `rowReason{}` on `BariProductVM` | `src/lib/view-models/index.ts` | **Absent fleet-wide** — backbone of #2/#3/#5 |
| Process | `comparison_ui_reference_v2.md` authored + signed | — | **Not authored** — hard gate on all Phase 1 |

---

## 3. Gap list per category

### maadanim — READY (v2 pilot)
- **Frontend/data/content:** none category-specific. Frozen v1 reference; 90/90 scored; richest expansion corpus (`interpretive_expansion_system_v2`, full production pass).
- **Only outstanding:** the fleet-wide platform gaps (§2). `protein_g`/`additive_count` are derivable from existing nutrition + ingredient data; `base_pct` deferred fleet-wide (Phase 3).
- **Route/UI/mobile/desktop/filter/sort/methodology/empty-state:** all conform to v1 reference; this *is* the reference. No isolated gaps.

### hummus — NEEDS MINOR FIXES
- **Data:** fat + saturated-fat suppressed (HUM-001, 67 fat values dropped) and sugar 0% coverage (HUM-002) → metric bars limited to protein + additives (consistent with the 2-of-3 launch decision; **base% n/a**).
- **Content:** confidence **re-audit not yet run** (gates #6 promotion per `confidence_label_audit_v1`); go-live still gated on DEC-002 (Product).
- **Methodology/disclosure (#8):** category fat-disclosure exists but is split between insight lines and methodology — consolidate to one header/methodology slot.
- **Empty-state:** strong — 2 `insufficient` products already exercise the null-score "—" state (good v2 regression fixture).
- **Desktop/route/filter/sort:** conform (live v2 source-of-truth `bari.digital/hashvaot/hummus`).

### bread — NEEDS MINOR FIXES
- **Route debt:** legacy duplicates still live — `/hashvaot/bread-comparison` and `/compare/bread-comparison` (+ `bread-comparison-dashboard.tsx`, ~19KB; `bread-editorial-content.ts`). Canonicalize to `/hashvaot/bread` and retire the duplicates (per `docs/canonical_route_strategy_v1.md`) before bread v2.
- **Data/content:** `v2-production`, 24/24 scored; metrics derivable. No corpus debt.
- **UI/mobile/desktop/filter/sort/methodology/empty-state:** conform to shared stack.

### snacks — NEEDS MINOR FIXES
- **Data lineage:** documented history (`snacks_data_lineage_audit_v1`, `snack_nutrition_recovery_plan_v1`, `image_integrity_audit_snacks_v1`) — validate `protein_g`/`additive_count` extraction against these before exposing them as metric bars.
- **Scope:** single-retailer (Yochananof), editorial subset (18 of 48 scored) — fine, but the metric block and band rail will look sparse at N=18; verify band distribution.
- **Content:** `v2-production`, CE-approved, NOVA terminology purged. Conforms.
- **UI/route/filter/sort/methodology/empty-state:** conform.

### yogurts — NEEDS MAJOR WORK
- **Corpus:** `v1-mvp-**manual**` — scores manually calibrated, **not a production extraction run**. The v2 metric block (#2) and band rail (#3) require *trustworthy* per-product nutrition/additive data; a manual MVP corpus cannot back them credibly.
- **Scale:** N=13 across 5 score bands → band rail and dividers will be very sparse; histogram (#header) near-meaningless at this N.
- **Action:** uplift corpus to a `v2-production` extraction pass before adopting v2 metric/rail features. Expansion content exists but should be re-derived from real signals, not manual calibration.
- **Route/UI/desktop/filter/sort:** structurally on the shared stack (no route/UI debt) — the gap is **data**, not frontend.

### milk — LEGACY
- **Off-contract:** uses `MilkComparisonProduct` (not `BariProductVM`), bespoke `MilkComparisonPage` (~18KB) with cinematic hero + `milk-editorial/*` components, its own dimension/pillar model (`consumer-explanation-view`, `PRIMARY_DIMENSION_KEYS`). `milk-data.ts` is `@deprecated`.
- **Not in registry:** absent from `comparisonCategoryRegistry`; route is `/hashvaot/milk-comparison`, not `/hashvaot/milk`.
- **Every v2 axis is a gap** because it isn't a shelf citizen: no shared route/UI/filter/sort/methodology/empty-state parity, no `BariProductVM`, no corpus JSON.
- **Action:** this is a **migration**, not a v2 upgrade — port to `BariProductVM` + corpus JSON + registry + shared shelf/desktop first; only then does v2 apply. Largest single-category lift in the fleet.

---

## 4. Recommended P1 implementation sequence

**Phase 0 (v1-safe, no reference change) — do first, unblocks everyone:**
1. #6 confidence promotion + accuracy gate, #8 category-disclosure de-dup, relativity tag — shared stack. Requires the hummus confidence re-audit (Blocker #4).

**Gate — must clear before any Phase-1 category work:**
2. **Author + sign `comparison_ui_reference_v2.md`** (Blocker #1).
3. Extend `BariProductVM` with `metrics{}` + `rowReason{}` and build the shared v2 components (dense row + density toggle, aligned metric block [protein+additives only], band rail, inline dividers, expansion restructure) (Blocker #2; #3 base% deferred).
4. QA re-baseline at mobile + `lg` (Blocker #5).

**Phase 1 category rollout (after gate) — in this order:**
5. **maadanim** — pilot. Reference category, richest production corpus, zero category debt; prove v2 here.
6. **hummus** — second. Live v2 source-of-truth; gate on the confidence re-audit clearing (#6) and consolidate the fat disclosure (#8).
7. **bread** — retire the legacy `bread-comparison` route + dashboard first, then apply v2.
8. **snacks** — after validating `protein_g`/`additive_count` extraction against the data-lineage audits; sanity-check band sparsity at N=18.
9. **yogurts** — only after corpus uplift from `v1-mvp-manual` to a production pass (otherwise the metric block/rail are not data-credible).

**Separate track (not Phase 1):**
10. **milk** — legacy migration to registry + `BariProductVM` + shared shelf/desktop. v2 cannot be considered until this lands.

---

## 5. Blockers

| # | Blocker | Impact | Owner |
|---|---|---|---|
| 1 | **`comparison_ui_reference_v2.md` not authored** | Hard gate — v2 code "does not ship on frozen v1 without" it. Blocks all of Phase 1+. | Frontend + design/product |
| 2 | **`BariProductVM` lacks `metrics{}` + `rowReason{}`** | Blocks metric block (#2), rail data, strongest +/− (#5) fleet-wide. | Frontend + Data |
| 3 | **`base_pct` main-ingredient extraction not built** (TASK-111) | Blocks the 3rd metric bar → mitigated by shipping 2-of-3, defer to Phase 3. | Data |
| 4 | **Hummus confidence re-audit not run** | Gates Phase 0 #6 confidence promotion and hummus v2. | Data / QA |
| 5 | **QA re-baseline (mobile + `lg`) not captured** | v1's 375px-only snapshots invalid for v2; gates Phase 1 ship. | QA |
| 6 | **yogurts corpus is `v1-mvp-manual`** | Not production-grade; blocks credible v2 metric/rail for yogurts. | Data |
| 7 | **milk is off-contract legacy** | Not a shelf citizen; blocks v2 entirely until migrated to registry/`BariProductVM`. | Frontend |
| 8 | **bread legacy duplicate routes live** (`/hashvaot/bread-comparison`, `/compare/bread-comparison`, dashboard) | Should be canonicalized/retired before bread v2. | Frontend |
| 9 | **Process/naming gaps** — TASK-106 not locatable; TASK-119/TASK-111 naming gap (from sign-off package) | Soft blockers on final Phase-1 sign-off. | Central Controller |

---

*Audit only — no production `src/**` code modified. Classifications are relative v2 readiness; no category is v2-shipped today because the shared platform and binding reference are not yet built.*
