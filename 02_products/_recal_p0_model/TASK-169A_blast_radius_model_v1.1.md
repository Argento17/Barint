# TASK-169A — P0 Recalibration Blast-Radius MODEL (v1.1)

**Status:** MODEL ONLY. No score shipped, no frontend JSON, no published run dir touched.
**Engine:** BSIP2 proto_v0 (HEAD), all P0 changes gated behind `BARI_RECAL_P0` (default OFF).
**Author:** Data Agent. Implements `recalibration_p0_design_v1.md` **§ v1.1 REVISION** (R7 + R4 changes); R1/R2/R3/R5/R6 unchanged.
**Supersedes:** `TASK-169A_blast_radius_model_v1.md` (kept for comparison). v1 numbers cited inline as the before-reference.
**Date:** 2026-06-02.

---

## 0. ACCEPTANCE CHECKS (lead) — all PASS

| # | Acceptance check | Result | v1.1 value (was v1) |
|---|---|---|---|
| A1 | **Flag OFF = byte-identical** to flag-OFF baseline on run_cheese_003 (59/59, 0 mismatch on score/grade/every dimension) | **PASS** | 59/59, 0 mismatch |
| A2 | **cottage 1% ≈ 90/A** (NOT S), no R7 +8 | **PASS** | **89.8/A**, ferm=None (was 97.8/S) |
| A3 | **white+garlic inversion resolved** (cottage ≥ white) | **PASS** | cottage 89.8 ≥ white+garlic 84.3 |
| A4 | **Both fluid-milk +8 leaks gone**; no milk A-crossing from R7; no residual R1-curve milk A-crossing | **PASS** | 0 fluid-milk +8; 0 milk A-crossings |
| A5 | **napoleon 16% שום שמיר stays NOVA 3 and does NOT reach A** | **PASS** | **74.5/B, NOVA 3** (was 81.5/A) |
| A6 | **yogurt keeps its (legitimately gated) bonus** | **PASS** | 35 yogurts get +8; **11 A / 3 S** (was 15 A / 3 S) |
| A7 | **Golden + router regressions:** clean OFF, intended-only ON | **PASS** | golden 0 FAIL/1 WARN (flag-insensitive); router all PASS OFF+ON |

> **Headline magnitude correction:** v1.1 produces **ZERO cheese S grades** (v1 had 4). The
> dairy mass-S overshoot is corrected purely by gating R7 to genuinely-cultured products —
> cottage 1% lands exactly at the owner's 90/A target (89.8) from R1+R2+R4 alone, with no +8.

### A1 detail — flag-OFF safety contract
`verify_recal_off_identical.py` and a direct re-score against the flag-OFF baseline both
confirm: with `BARI_RECAL_P0=off`, every R-path (R1–R7, including the new v1.1 R7/R4 logic)
is inert. 59/59 cheese products reproduce score, grade and every dimension. The v1.1 edits
introduced **zero** OFF-path change vs the v1 flag-OFF baseline (0 score/grade/dimension drift).

> Pre-existing HEAD note (unchanged from v1): product `…217492` shows `calorie_density`
> 40→65 between the *published* run_cheese_003 trace and current HEAD — **pre-existing HEAD
> drift in the calorie-density/confidence path, NOT a P0 effect** (P0 touches no
> calorie-density code; score+grade unchanged at 60/C). Flagged for QA, out of P0 scope.

---

## 1. What changed in v1.1 (and what did NOT)

| ID | v1 (old) | v1.1 (this model) | File |
|---|---|---|---|
| **R7** | `product_type_dairy + plain ⇒ +8` (the leak: fired on fluid milk and inflated all fresh cheese) | **Two-path gate.** Path A `has_fermentation` (unchanged). Path B inherently-cultured TYPE: **yogurt subtypes** OR **aged/specialty cultured-cheese name markers**. Hard-excludes fluid milk + plant drinks. Excludes cottage + white-cheese fresh subtypes (cottage ruling). | `score_engine.py` |
| **R4** | `is_plain` = additive-marker-only | **+ `has_flavor_variant` clause:** a declared flavoring (even whole-food garlic/dill/herbs) forfeits the NOVA-3→2 retention → stays NOVA 3. Only ever blocks a demotion. | `nova_proxy.py` |
| new const | — | `CULTURED_YOGURT_SUBTYPES`, `CULTURED_CHEESE_NAME_MARKERS_HE`, `FLUID_MILK_NAME_MARKERS_HE`, `DAIRY_SOLID_IDENTITY_MARKERS_HE`, `FLAVORED_VARIANT_MARKERS_HE` | `constants.py` |
| R1,R2,R3,R5,R6 | — | **UNCHANGED** (model already well-behaved). Re-run only to capture the new combined distribution. | — |

### Router-reconciliation note (important — flagged per v1.1 spec call #4)
The spec's literal R7 keys `category == "milk_dairy"` and `category == "yogurt"` **do not
exist in the live router**. Verified against `router_v2.py` + the model outputs:
- **No `milk_dairy` category is emitted.** Fluid milk routes to **`dairy_protein`** (subtype
  `None`) or `beverage` — the *same* `dairy_protein` category as cheese AND yogurt.
- **No top-level `yogurt` category.** Yogurt routes as `dairy_protein` with subtypes
  `yogurt / greek_yogurt / protein_yogurt / bio_yogurt / froop_yogurt / yogurt_mixin`.
- **cottage 1% routes with `subtype = None`** (not `cottage`), so subtype alone cannot
  identify the fresh-cheese exclusion.

I therefore implemented the spec's **intent** against the **real router vocabulary**:
- **yogurt qualifies** via the real yogurt SUBTYPES (Path B.1);
- **fluid milk is hard-excluded** by a fluid-milk NAME token (`חלב`/`משקה`/…) that lacks a
  dairy-solid identity marker — because fluid milk shares `dairy_protein` with cheese;
- **aged/specialty cheese qualifies** by NAME marker (`קממבר`/`גאודה`/`פרמזן`/…); cottage and
  white-cheese (`גבינה לבנה`/`לבנה`) are deliberately NOT in the marker set;
- **substring trap fixed:** `חלב` (milk) is a substring of `חלבון` (protein). Naive matching
  wrongly flagged `דנונה פרו 20 גרם חלבון` as fluid milk. v1.1 matches fluid-milk markers
  **token-aware** (whole whitespace-delimited tokens) and treats a confirmed yogurt subtype
  as a definitive cultured-type signal that bypasses the fluid-milk name heuristic.

**Cheese subtypes the spec named but the router does NOT emit** (flagged for the Nutrition
Agent / P1): `labaneh`, `quark`, `sour-cream-style`, and all aged-cheese subtypes — the
router emits only `cottage`, `cream_cheese`, and `None` in the cheese family. Aged/specialty
cheese is therefore caught by NAME marker, not subtype, in this corpus. If the router later
emits dedicated aged-cheese subtypes, fold them into `CULTURED_CHEESE_NAME_MARKERS_HE` or a
subtype allowlist.

---

## 2. Headline cases — cheese (run_cheese_003, n=59)

| product | OFF | v1 ON | **v1.1 ON** | NOVA(v1.1) | ferm | note |
|---|---|---|---|---|---|---|
| **cottage 1%** | 74.9/B | 97.8/S | **89.8/A** | 2 | none | R1+R2+R4 only; **no +8 → 90/A target hit** |
| **cottage 3%** | 71.2/B | — | **88.8/A** | 2 | none | no +8 |
| **cottage 5%** | 69.4/B | — | **87.0/A** | 2 | none | no +8 |
| **cottage 9%** | 52.0/C | 89.1/A | **81.1/A** | 2 | none | no +8 (was +8 in v1) |
| **cottage 12%** | 52.0/C | 84.4/A | **76.4/B** | 2 | none | no +8 → stays B |
| **white+garlic** (`גבינה לבנה 5%+שמיר ושום`) | 76.9/B | 88.3/A | **84.3/A** | 3 | **+8 (Path A)** | declared culture marker; R4 keeps NOVA 3 |
| **napoleon 16% שום שמיר** | 68.3/B | 81.5/A | **74.5/B** | **3** | +8 (Path A) | **A leak CLOSED** — R4 v1.1 keeps NOVA 3 |
| `גבינת נפוליאון שום שמיר` | 52.0/C | — | **55.5/C** | 3 | +8 | stays C |

- **R7 inversion RESOLVED:** cottage 1% (89.8) ranks above white+garlic (84.3). ✓
- **cottage 9% R5 collapse RESOLVED:** 52/C → 81.1/A, above napoleon (74.5). ✓
- **napoleon flavored-A leak CLOSED:** R4 v1.1 keeps it NOVA 3 → 74.5/B (was 81.5/A). ✓
- **cheese A=13, S=0** (v1: 4 S). Dairy no longer mass-produces S.

**Observation (flag for Nutrition, not a leak):** `גבינה לבנה 5%+שמיר ושום` reaches **84.3/A**
via the **Path A declared-culture +8** (its panel declares a culture marker) on a lean 5%
white cheese. This is unchanged HEAD Path-A behavior (not the v1 leak path), and R4 correctly
keeps it NOVA 3. It is a *flavored* white cheese reaching A through a legitimate declared
culture, distinct from the napoleon test. If Nutrition wants flavored variants excluded from
**Path A** too (not just Path B / R4 NOVA), that is a separate design decision — currently a
declared culture marker overrides flavoring for the +8. Surfaced for the owner's eye.

## Hummus (run_hummus_002 lineage = canonical_bsip1, n=69) — R1/R6, unchanged from v1 intent
- Chickpea/tahini hummus: ON spreads with better differentiation; **median 67.8**, **max 88.0
  (no S overshoot)** — cleaner than v1 (which had one 94.2/S), because v1.1 R7 no longer
  touches hummus (it was never dairy; the v1 S came from the broader stack).
- **R6 veg-spreads (17 detected): unchanged, the cleanest result.** matbucha 50–60/C → 61–71/B;
  eggplant spreads → 60–69. **None cross the 80 anti-immunity ceiling.** Guard intact. No
  router changes.

---

## 3. FROZEN-CEILING collision report (feeds the deliverable-2 sign-off table)

All frozen corpora re-scored OFF vs ON (v1.1). **Every frozen move is a P2 owner decision.**

| corpus | n | score moves | grade moves | crosses A (≥80) | reaches S (≥90) | vs v1 |
|---|---|---|---|---|---|---|
| **snack_bars** | 53 | 14 | **0** | 0 | 0 | unchanged — snk-001 = 70/B HELD ✔ |
| **milk** (frozen top = 85/A) | 20 | 9 | **2** | **0** | 0 | **leak CLOSED** (v1 had 1 A-crossing) |
| **yogurt** | 86 | 82 | 37 | **14** | **3** | tighter (v1: 15 A / 3 S) |
| bread retail_003 | — | not modelled — bespoke loader (see §6) | | | | unchanged |

### snack_bars — CEILING HELD ✔ (unchanged)
0 grade changes; max new score 70. R1 keeps the supplement curve for `snack_bar_granola`, so
**snk-001 = 70/B is untouched**. Only tiny R5 sat-fat nudges, no flips. **Invariant safe.**

### milk — LEAK CLOSED ✔ (the headline v1.1 fix)
| product | OFF | v1 ON | **v1.1 ON** | why |
|---|---|---|---|---|
| `חלב נטול לקטוז מועשר בחלבון 2%` | 74.1/B | **87.3/A (BREACH)** | **79.3/B** | R7 +8 removed; lift now from R1 curve + R2/R3 only → **does NOT cross 85/A** |
| `חלב בבקבוק 1% מהדרין` | 56.6/C | 69.8/B (erroneous +8) | **61.8/C** | R7 +8 removed |
| `חלב טבעי 4%` / `חלב עיזים` / `חלב מלא בטעם של פעם` | 85/A | 85/A | **85/A (unchanged)** | the frozen `run_004_recalibrated` top; OFF==ON, no move |
| plant drinks (rice/soy) | D/E | C/D | C/D | R3 leanness only (the only 2 milk grade flips) |

- **0 fluid-milk +8 bonuses** (v1 had 5). **0 milk A-crossings.** The frozen 85/A ceiling is
  fully preserved — the three 85/A dairy milks did not move, and no milk crosses A.
- **No residual R1-curve milk A-crossing in this corpus.** `חלב נטול לקטוז 2%` (the v1 breach)
  lands at 79.3/B — below A — so the R1 `milk_dairy` curve alone does not create a new A here.
  (If a higher-protein milk did cross from the R1 curve alone, that would be a clean P2 item,
  not a leak. None occurs in this corpus.)
- The 2 milk grade changes are both **plant drinks** (`משקה אורז` D→C, `אלפרו שוקו סויה` E→D)
  from R3 leanness — not dairy, not the frozen invariant.

### yogurt — bonus retained, 14 A / 3 S (legitimate, owner-reviewable)
Yogurt IS cultured → Path B keeps the +8 legitimately (35 yogurts credited). High-protein GO
yogurts reach S (98.8, 97.0, 93.2); bio/Greek/goat plain yogurts reach low-A (80–87). Per the
owner ruling (no hard cap), this is a genuine distribution for P2 sign-off, **not leakage** —
trimmable via the `yogurt` R1 protein-apex anchors if the owner wants fewer S. (v1.1 is one A
tighter than v1 because the yogurt-subtype gate is now precise and flavored/mixin yogurts are
screened by the flavored-variant clause.)

---

## 4. Frozen-ceiling sign-off table (DELIVERABLE 2 — owner approves in P2)

Every frozen product that **changes grade**, old→new, root cause, and whether it crosses a
prior frozen invariant. **No frozen invariant is breached by v1.1.**

| corpus | product | old → new | root cause | crosses frozen invariant? |
|---|---|---|---|---|
| **milk** | `משקה אורז אורגני` | 49.4/D → 52.3/C | R3 leanness (plant drink) | No — not dairy; below 85/A |
| **milk** | `אלפרו שוקו משקה סויה` | 34.5/E → 37.0/D | R3 leanness (plant drink) | No — not dairy |
| **milk** | *(frozen dairy top: `חלב טבעי 4%`, `חלב עיזים`, `חלב מלא`)* | 85/A → **85/A (no move)** | — | **No — milk 85/A ceiling HELD ✔** |
| **snack_bars** | *(none — 0 grade changes)* | — | R5 sat-fat nudges only (<grade) | **No — snk-001 70/B ceiling HELD ✔** |
| **yogurt** | `יוגורט גו נטול לקטוז` | 78.2/B → 98.8/S | R1 protein + Path B +8 | **New S** — yogurt has no prior frozen ceiling; **P2 owner call** |
| **yogurt** | `יוגורט GO חלבון 25 גרם` | 71.8/B → 97.0/S | R1 protein + Path B +8 | New S — P2 owner call |
| **yogurt** | `יופלה GO מועשר בחלבון` | 70.3/B → 93.2/S | R1 protein + Path B +8 | New S — P2 owner call |
| **yogurt** | `דנונה פרו 20/21 חלבון`, `יוגורט פרו שוקולד`, `מולר אקטיב`, `יוגורט ביו 1.5%/3%`, `יוגורט עזים 3%`, `דנונה ביו 1.7%`, `נטול לקטוז 3%` (11 products) | B/C → A (80–87) | R1 protein + R2 fiber-N/A + Path B +8 | New A — yogurt has no prior frozen ceiling; **P2 owner call** |
| **yogurt** | ~22 further B/C/D moves (e.g. Greek 6.5–10%, flavored GO, מולר מיקס) | C↑B, D↑C, etc. | R1 + R2 (+8 where cultured) | No invariant — ordinary recal lift; P2 review |

**Prior frozen invariants and their v1.1 status:**
- **Milk top = 85/A (`run_004_recalibrated`, whole/4%/goat):** **HELD.** OFF==ON, no move; no
  milk crosses A. ✔
- **snk-001 = 70/B (snack-bar ceiling):** **HELD.** 0 snack-bar grade changes. ✔
- **Bread provenance `real_bread_retail_003`:** not re-modelled (bespoke loader, §6); expected
  radius small (R3+R5 only; bread is not dairy). No bread invariant touched by R4/R7.
- **Yogurt (run_yogurt_003):** has **no frozen numeric ceiling** in the CNO invariants. The
  14 A / 3 S distribution is a new, legitimate (R7 gated) distribution for explicit P2
  per-product owner sign-off — no hard cap per owner ruling 2.

---

## 5. Evidence-registry note (governance — author before P1 merge)
- **EV-024/026 lineage — REVISED (R4 + R7), under `BARI_RECAL_P0`:**
  - *R4 v1.1:* benign culinary/culturing/fortification additions keep NOVA 2 — **but a
    declared flavoring (even whole-food) makes it a flavored variant and forfeits the
    retention.** Label observability: name + ingredient substring. Tier **Moderate**.
  - *R7 v1.1:* the +8 fires only on **(A) a declared culture marker, OR (B) an
    inherently-cultured TYPE (yogurt subtype; aged/specialty cultured-cheese name)** — and is
    **hard-excluded for fluid milk + plant drinks**. The v1 "plain-dairy ⇒ cultured"
    assumption is **retracted**. Tier **Moderate**; Path A fully label-observable, Path B is
    router-subtype / name-derived (reconciled against live routing — see §1).
- **No new rule, no shadow rule.** R7 v1.1 *narrows* an existing bonus path; R4 v1.1 *adds one
  disqualifier clause*. Net rule count unchanged; blast radius strictly *smaller* than v1.
  `CULTURED_YOGURT_SUBTYPES` / `CULTURED_CHEESE_NAME_MARKERS_HE` / `FLUID_MILK_NAME_MARKERS_HE`
  / `DAIRY_SOLID_IDENTITY_MARKERS_HE` are routing allowlists; `FLAVORED_VARIANT_MARKERS_HE`
  feeds an existing test.
- **Rollback unchanged:** single `BARI_RECAL_P0` flag (default OFF → 0.4.1 byte-identical).
- EV-029 (R1), EV-030 (R3), EV-031 (R5), EV-032 (R6) and the EV-027 (R2) extension are
  unchanged from v1 and still require their registry entries before P1 merges.

## 6. Coverage gaps / what was NOT modelled
- **bread retail_003 — STILL NOT WIRED.** It uses a bespoke inline BSIP0→BSIP1 normalizer, not
  a `load_batch` dir (the only bread BSIP1 dir is `run_bread_light_001`, a synthetic light
  run, not the frozen retail_003 corpus). **Estimated radius: small.** Bread is not dairy →
  **no R4/R7 effect at all.** Only R3 (leanness, fires for fat ≤ 3g — most breads) and R5
  (graded sat-fat, fires only for sat > 5g — rare in bread) apply, plus the conservative R1
  `bread` protein curve (deliberately tuned so bread is not rewarded as a protein food).
  Expectation: minor positive nudges on lean breads, no grade flips, no invariant risk. **Do
  not block on it** — a dedicated bread re-model in P1 (once the loader is wired) should
  precede any bread frozen sign-off.
- Headline nutrition values are driven by the live BSIP1 inputs (the published traces null
  `normalized_nutrition_per_100g`), so all numbers above are from a real re-score.

## 7. Artifacts
- Engine (flag-gated, v1.1): `03_operations/bsip2/proto_v0/src/constants.py`,
  `score_engine.py` (R7 v1.1 block ~L1145–1196), `nova_proxy.py` (R4 v1.1 `is_plain`).
- Harness (unchanged, extended fields captured): `…/src/run_recal_p0_blast_radius.py`,
  `…/src/verify_recal_off_identical.py`.
- Model data (v1.1): `02_products/_recal_p0_model/{cheese,hummus,milk,yogurt,snack_bars}_{off,on}_v1.1.json`,
  `blast_radius_summary_v1.1.json`. (Base-name `*.json` = latest v1.1 run; v1 numbers live in
  the v1 report.)
- This report: `02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.1.md`.
- v1 report (comparison reference): `TASK-169A_blast_radius_model_v1.md`.
