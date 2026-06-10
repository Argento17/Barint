# TASK-233 Confirmation Sweep — BSIP0→Website Structural Audit

**Status:** Complete · **Date:** 2026-06-10 · **Mode:** READ-ONLY (nothing fixed)
**Executors:** Data Agent (A/C/D-grade/E1) ‖ QA Agent (B/D-defects/E2) — dispatched in parallel.
**Reviewers (pending):** Content Agent, Frontend Agent.
**Verdict: PASS WITH FIXES.** All three root causes confirmed systemic. Targeted hold
recommended for frozen_vegetables; one editorial finding routed to Content/Design for a policy
ruling before it is treated as a blocker.

> **Scope correction captured mid-sweep (load-bearing):** `salty_snacks_frontend_v4.json` was
> **regenerated on disk during the sweep** (TASK-231 remediation; meta `generated 2026-06-10T14:14:48Z`,
> 47→41 products). The earlier file's `NOVA 4` + `עדיף לבחור` + grade-literal leaks are **gone** from
> the shipped file. Salty v2/v3 are dead (not imported). `olive_oil_frontend_v1` and `crackers_staged_v1`
> are staged/dead (imported by no page-data). All leak findings below are scoped to the **13 shipped JSONs**.
> The current working branch is `salty-snacks-v4`; **frozen_vegetables lives on its own preview branch,
> not master** — so its issues are pre-merge, which is the right time to catch them.

---

## 1. Root-cause confirmation

| Root cause | Verdict | Evidence (categories) |
|---|---|---|
| **#1 No shared frontend-packaging core** | **CONFIRMED SYSTEMIC** | 10+ bespoke generators each hand-roll score/grade/confidence/cluster/copy/image. Only shared layer is `corpus.ts` (TS, runtime, downstream). `BariProductVM` is compile-time only — no runtime schema validation of any JSON. (DA-001, DA-003) |
| **#2 Validation is late and manual** | **CONFIRMED SYSTEMIC** | The `is_clean` leak gate, dup-barcode hard fail, and internal-key allowlist all exist conceptually but **none run as a build/pre-ship gate**. salty v4 is clean only because its generator ran `is_clean` manually; the other 12 categories never did. (DA-004, QA-E2) |
| **#3 Editorial copy escapes the editorial system** | **CONFIRMED SYSTEMIC** | Per-product consumer copy is emitted by `build_*()` template functions in the generators, not authored/filtered by Content. 4 shipped categories render score-mechanic grade literals (`NN/A-E`) in consumer copy; cereals also leaks internal rescore-history narration. (DA-005/007, QA-001..004) |

---

## 2. Merged findings table

Finding IDs preserve each executor's numbering (DA-* Data Agent, QA-* QA Agent) for traceability.

| finding_id | category | file | evidence (fn / line / product ID + string) | severity | systemic/specific | owner | recommended fix |
|---|---|---|---|---|---|---|---|
| **DA-005** | frozen_vegetables | generate_frozen_vegetables_frontend.py:158-173 | `build_confidence()` maps **high AND medium → verified** → label "מבוסס על נתונים מלאים" | CRITICAL | driver of systemic C | Data + Nutrition | medium→partial; only full panel+ingredients→verified (7-state spec) |
| **DA-006** | frozen_vegetables | frozen_vegetables_frontend_v1.json (53/53) | All 53 = `verified`+"full data" **yet all 53 carry data-gap `unknowns`** (missing fiber/sat-fat). File **absent from `run_confidence_annotation_pass.py` LIVE_FILES:27-33** so never corrected | CRITICAL | category-specific | Data | Add frozen_veg to LIVE_FILES + re-derive; most drop to partial |
| **DA-001** | all | 10+ generators | No generator imports a shared core; logic re-implemented each time | HIGH | **systemic (≥10)** | Data | Extract shared Python packaging core |
| **DA-003** | all | view-models/index.ts; corpus.ts | `BariProductVM` compile-time only; no runtime JSON-schema validation | HIGH | systemic | Data + QA | Runtime VM-conformance gate before bari-web import |
| **DA-004** | all | run_schema_validation_gate.py:39-43 | Schema gate covers only 4 of 17 files; not wired to build/pre-commit | HIGH | systemic | QA | Extend to all live files; wire as blocking gate |
| **DA-007** | salty v4, cheese, yogurts, cereals, maadanim | 03_build_frontend_v4.py:180; build_yogurt_cheese:70; build_cereals:75; cheese_003:58 | "sufficient"/"has_ing"→verified; none require BOTH ingredients+full panel | HIGH | **systemic (≥5)** | Data + Nutrition | Route all through `confidence_annotation.derive_from_trace`; delete inline fns |
| **DA-009** | granola, hummus, maadanim, salty | granola 7290013433244 (65→C stored/B runtime); maadanim …5431968 (35→E/D); hummus …931330 (65→C/B) | **Grade computed twice**: generator writes `grade`, `corpus.ts normalizeGrade()` re-derives & overrides → disagree on ≥9 boundary products | HIGH | **systemic (≥4)** | Data | Generators write score-derived grade so disk==runtime; or stop writing grade in JSON |
| **DA-002** | hard_cheeses, juices, butter | build_hard_cheeses:215; build_juices_v3:284; butter build:348 | `grade` written from engine `grade_estimate` (6-grade incl. S) not `grade_from_score` | MEDIUM | systemic (3) | Data | Always derive 5-grade from score |
| **DA-008** | salty_snacks_v2 | salty_snacks_frontend_v2.json | v2 still on disk, 39/54 `verified` via loose `has_ing`, no 7-state fields | HIGH | category-specific | Data | Confirm v2 dead (QA: it is) / delete |
| **DA-010** | hard_cheeses | build_hard_cheeses:28 (`OUT_WEB=hard_cheeses.json`) | Generator writes a filename the frontend does NOT import; live file is copy/patched → re-run won't update page | MEDIUM | category-specific | Data | Point `OUT_WEB` at `hard_cheeses_frontend_v2.json` |
| **DA-011** | cheese | build_yogurt_cheese:239 (`_a_gate_capped`) vs corpus.ts:59 (`_aCappedToB`) | A-ceiling cap field name mismatch → regeneration would emit caps runtime ignores | MEDIUM | category-specific | Data | Align generator to `_aCappedToB` |
| **DA-013** | all | confidence_annotation.py:235 `annotate_fallback` | On trace-join miss, pass **trusts existing (possibly inflated) confidence** instead of re-deriving | MEDIUM | systemic | Data | Fallback must not preserve `verified` without trace evidence |
| **QA-001** | frozen_vegetables | frozen_vegetables_frontend_v1.json (53/53) | `insightLine` grade literal, e.g. `"קטניה קפואה טבעית — 90/A …"`; `is_clean=False` | CRITICAL* | systemic (4) | **Content (Design confirm)** | *Policy call — see §4. Strip `NN/X` token if confirmed banned |
| **QA-002** | snacks | snacks_frontend_v2.json (18/18) | `bottomLine` `"70/B: …"`; `comparisonContext` `"…56/C: …"`; `is_clean=False` | CRITICAL* | systemic | Content | Same policy call |
| **QA-003** | cereals | cereals_frontend_v2.json | `rowVerdict` 5290…061: `"…78/B בגרסה הקודמת עקב תקלת נתונים; הציון המתוקן 55/C…"` — grade literals **+ internal rescore narration** | CRITICAL | systemic | Content | Remove rescore-history narration outright (this part is unambiguous) |
| **QA-004** | bread | bread_frontend_v2.json | shufersal_7290018500316 `comparisonContext` `"…ציון 82/A על בסיס מחמצת."` | HIGH* | systemic | Content | Policy call |
| **QA-005** | yogurts | yogurts_frontend_v3.json | dup barcode `7290107936309`: yog-007 (78/B) + bsip1_yogurt_… (75/B, untranslated "Greek yogurt") — same product scored twice | HIGH | category-specific | Data | De-dupe; one barcode=one product/score |
| **QA-006** | snacks | snacks_frontend_v2.json | dup barcode `7290011498894`: snk-015 (63/C) + snk-003 (55/C), two distinct products | MEDIUM | category-specific | Data | Fix shared/wrong barcode |
| **QA-007** | butter | butter_frontend_v2.json | bsip1_butter_369709 `score: 45.2` (float; VM requires rounded int) | MEDIUM | category-specific | Data | Round at packaging |
| **QA-008** | yogurts | yogurts_frontend_v3.json | bsip1_yogurt_7290102394081 `imageUrl` null (1/19) | LOW | category-specific | Data/Frontend | Supply image / confirm placeholder |
| **DA-012 / QA-003-key** | all (≥10) | shipped JSONs | `source_traceability_status` ships as a product key in **10/13** categories; also `_cluster/_subpool/_internal_cluster/novaGroup/_calibration`. None in `BariProductVM`; not rendered but ships internal vocabulary | LOW (per item) / HIGH (as a pattern) | **systemic** | Data + Frontend | Strip all non-VM keys in the packaging core / corpus loader |

\* QA-001/002/004 severity is **provisional** — see §4 (grade-literals-in-copy is a Content/Design policy question, not yet adjudicated).

---

## 3. Validation placement (E1 + E2 merged)

| Boundary | Checks that exist | Manual-only → should be a gate |
|---|---|---|
| BSIP0 | `bsip0_qa_validator.py` (panel/scope) | dup-barcode + conflicting-table + range checks (none today) |
| scope-clean | per-run scope-class filters | scope-coverage report (none) |
| BSIP1 | per-run normalization; `ingredient_quality_gate` (maadanim only) | cross-category coverage floor |
| BSIP2 | trace gen; `grade_governance.apply_a_grade_floor`; per-cat caps | rank-order / plausibility check |
| Packaging | `validate_frontend_schema.py` (structural, all files); `run_schema_validation_gate.py` (4 files); `run_copy_golden_diff.py`; `run_confidence_annotation_pass.py` | **`is_clean` leak gate**, **dup-barcode on final JSON**, **internal-key allowlist**, **score int/range**, **grade==score consistency** — all exist conceptually, none block the build |

**The single missing check that would have caught the most:** there is **no grade-vs-score consistency check at any boundary** (lets DA-009 drift through), and the `is_clean` leak gate is **not wired into the build** (lets QA-001..004 reach live JSON).

---

## 4. The one finding that needs Content/Design adjudication (not yet a confirmed blocker)

QA-001/002/004 flag grade literals (`90/A`, `70/B:`) inside consumer copy as a CRITICAL leak,
on the strength of the offline `hebrew_readability.is_clean` gate. **Orchestrator caution:** this
is a **pre-existing editorial style on the oldest categories** (snacks, bread, cereals all use
`NN/X:` prefixes by design), not a regression. Whether putting the literal score in the prose —
when the chip already shows it — is *banned* or merely *redundant* is a Content/Design policy
call, and it collides with the `comparison_row_verdict_model` (verdict ends on grade). It should
be **ruled on by Content + Design before being actioned as a launch blocker.** What is *not* a
policy call and **is** a clear defect: **QA-003's internal rescore-history narration** in cereals
("78/B in the previous version due to a data error; corrected to 55/C") — that exposes pipeline
internals to the consumer regardless of the grade-literal ruling.

---

## 5. Recommendation

### PASS WITH FIXES. Open three implementation subtasks under TASK-233, in this order:

1. **TASK-233A — Validation gate harness (root cause #2).** Highest leverage, cheapest, catches
   the rest going forward. Wire as build/pre-commit gates: `is_clean` over every consumer string
   of every shipped JSON; `BariProductVM` runtime conformance + internal-key allowlist;
   dup-barcode uniqueness on final JSON; score int/range; **grade==score consistency.** Owner: QA + Data.
2. **TASK-233B — Shared packaging core (root causes #1 + confidence).** One module all generators
   call: single `grade_from_score` (matching `corpus.ts` so disk==runtime), single confidence
   deriver (`confidence_annotation.derive_from_trace`, medium≠verified), single field-strip, single
   VM emitter. Subsumes DA-001/003/005/007/009/013. Owner: Data (+ Nutrition co-sign on confidence).
3. **TASK-233C — Editorial copy routing + policy (root cause #3).** (a) Content/Design **ruling**
   on grade-literals-in-copy (§4); (b) remove cereals rescore narration (unambiguous); (c) route
   per-product copy through Content's banned-term filter at write time. Owner: Content (+ Design ruling).

Plus a small **TASK-233D — targeted data fixes** (not root-cause): add frozen_veg to the
annotation-pass; de-dupe yogurts/snacks barcodes; round butter float; fix hard_cheeses orphan
filename + cheese cap-field name. Owner: Data.

### Launch hold

- **Hold frozen_vegetables go-live** until DA-005/DA-006 are fixed. A product that says "based on
  full data" while listing missing data is an indefensible, unambiguous consumer-facing
  contradiction — and frozen veg is still on a preview branch, so this is caught pre-merge (the
  right time). This is the one clear hold.
- **Do NOT emergency-pause** the already-live snacks/cereals/bread over grade-literals — that's a
  pre-existing style pending the §4 policy ruling. **Do** fast-track the cereals rescore-narration
  removal (QA-003) since it leaks pipeline internals regardless of the ruling.
- salty_snacks v4 is clean on the leak axis post-regen; no hold.

## 6. Owner observations (2026-06-10, added post-sweep)

1. **Duplicated/inflated confidence tooltip.** Owner saw *"all nutrition and ingredient data was
   available from the official food source"* in **both** salty-snacks and frozen vegetables.
   Verified: the exact line `כל נתוני התזונה והרכיבים היו זמינים ממקור המזון הרשמי` ships **53×,
   only in frozen_vegetables**; salty-snacks no longer has it (v4 regen removed it). It is a
   **non-canonical variant** — every other verified category uses the milder
   `הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים` (74×). It overclaims ("official food source"
   vs the actual Shufersal retailer scrape per `_meta.provenance`) and rides on all 53 products as
   "full data" while they list `unknowns`. → folded into **TASK-233B** (canonical tooltip + accuracy
   flag to Nutrition/Content); interim re-derive in **TASK-233D**.
2. **Product images don't load on first paint.** Recurring across categories; owner must re-trigger
   each time. → **TASK-233E** (Frontend Agent diagnosis: synthesized URL vs `next/image` config vs
   load-timing). Tied to the image-handling weakness flagged in the original audit (W1.3).

## 7. Subtasks opened
TASK-233A (validation gate harness · QA+Data) · 233B (shared packaging core + confidence · Data+Nutrition) ·
233C (editorial copy routing + grade-literal policy ruling · Content+Design) · 233D (targeted data fixes · Data) ·
233E (image first-paint bug · Frontend). All IN_PROGRESS, depends_on TASK-233.

## 8. Reviewer pass (Content + Frontend, 2026-06-10)

**Content ruling** → `01_framework/editorial/grade_literal_in_copy_ruling_v1.md`: (1) `NN/X` grade
literals in prose **banned everywhere** (grade *letter* in a causal clause stays); QA-001 blocks
frozen_veg at merge, QA-002/004 normal-track HIGH. (2) cereals rescore narration **removed
unconditionally**. (3) canonical verified tooltip = `הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים`;
**retire** `ממקור המזון הרשמי` (overclaim).

**Frontend pass — image bug split into two causes:**
- **Load-timing bug (the recurring "first paint" symptom) — FIXED.** Thumbnails used `loading="lazy"`
  with no priority; eager + `fetchPriority="high"` now applied to the top-6 above-the-fold rows
  (`bari-product-thumbnail.tsx`, `comparison-row.tsx`, `comparison-table.tsx`). tsc/build clean,
  verified on cheese + hummus. **This is a working-tree code change on branch `salty-snacks-v4`.**
- **NEW finding — frozen_veg images are 404 (wrong synthesized URL).** Generator guesses prefix
  `MNH68_`; real scraped prefixes (cheese `TZE58_`, hummus `UFL56_`) return 200. → TASK-233D (Data).
- **Render surfaces for the grade-literal filter:** `expansion-section.tsx:184` bottomLine,
  **:191 AND :242** comparisonContext (two sites — filter must cover both), :204/:211 signals;
  row `comparison-row.tsx:182` rowVerdict, :188 insightLine.
- **VM-gate feasibility (233A):** one edit at `corpus.ts loadComparisonCorpus` (today strips only
  `_calibration`) — switch to a `BariProductVM` allowlist + conformance check; **must allowlist the
  intentional snake_case copy fields** `confidence_label_he` / `confidence_tooltip_he` /
  `confidence_sub_reason`. Lets the per-category hand-strips (e.g. frozen-veg page-data) be deleted.

## What this changes about the original Glassier audit
Confirmed and *strengthened*: the original audit inferred "every category hand-rolls" from
frozen-veg + cheese; the sweep proves it across 10+ generators with file:line evidence, and adds
two findings the original missed — **grade computed twice → real drift on ≥9 products (DA-009)**
and **generator/runtime field-name mismatches (DA-010/011)** that would silently break on the
next regeneration.
