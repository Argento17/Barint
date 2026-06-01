# TASK-133 B/C/D — Implementation & Validation Report

**Owner:** Nutrition Agent · **Date:** 2026-06-01
**Scope:** Structural build of F2 (133B), F1 (133C), F4 (133D) on BSIP2 `proto_v0`.
**Gate:** [DEC-004](../decisions/decisions.json) (PENDING) gates the numeric *magnitudes*
and final closure; it explicitly does **not** block the structural build (DEC-004 notes).
**Roadmap:** [TASK-133_implementation_roadmap.md](TASK-133_implementation_roadmap.md).

> All magnitudes shipped here are **DEC-004-gated placeholders**. The structure is
> owner-approved; the numbers are set in a dedicated calibration run against real
> corpora and ratified at Phase E before any frontend rescore.

---

## What shipped (code)

| File | Change |
|------|--------|
| `signal_extractor.py` | Imports `ingredient_taxonomy` (133A). Emits new L3 identity signals: `tax_emulsifier_concern`, `tax_emulsifier_benign`, `tax_native_starch`, `tax_modified_starch`, `tax_bha_present`, `tax_bht_present`, `tax_named_concern_additives`, `has_collagen`, `protein_matrix_form`, `primary_fragmentation`. New `RECONSTRUCTED_PROTEIN_MARKERS_HE` + `COLLAGEN_MARKERS_HE`. |
| `constants.py` | `PROTEIN_QUALITY_MATRIX_DISCOUNT`, `PROTEIN_MATRIX_DISCOUNT_BAR_CATEGORIES` (F2); `ADDITIVE_IDENTITY_DELTAS` (F1, default neutral); `BHA_NAMED_PENALTY` (F4). All placeholder, DEC-004-gated. |
| `score_engine.py` | `score_protein_quality(nn, l3, category)` applies the F2 matrix discount (quality-only). New `_identity_additive_deltas()` applies F1 (neutral) + F4 (BHA −5) on the additive-quality dimension. |

---

## F2 (133B) — protein-quality matrix discount + collagen

- **Design call (DEC-004 G2):** discounts the protein-**quality** dimension only. Protein
  **mass** still feeds `satiety_support` + `nutrient_density` untouched.
- **Trigger (Req 3 / Req 5 — gaming-resistant):** the protein fraction must sit in the
  **primary ingredient positions** (top 3). A trace garnish cannot drive the discount.
  - `collagen` → strongest discount (×0.55 placeholder; incomplete AA profile, lowest matrix DIAAS).
  - `reconstructed` (whey/soy/pea/egg/casein protein, explicit isolate) → ×0.80 placeholder
    (mid-band of the empirical 47–81% DIAAS), **bar-format categories only**.
  - Milk powder (`אבקת חלב`) is explicitly **excluded** (reconstructed dairy, not a fraction).
- **Coordination (top risk):** this is the **sole owner** of the reconstructed-protein
  penalty in the live score path. `matrix_integrity.py`'s degradation pull is **not**
  composited into the live score, so there is no double-count today; documented as a
  PROCESSING_LOAD-family note for any future compositing.

### Behavior (synthetic, cap-free isolate bar)
`חלבון מי גבינה מבודד` primary, 30 g protein → protein-quality **80.8 → 64.6**.
Collagen bar → **×0.55**. Whole-food bar → unchanged. **Whey-in-yogurt (non-bar) → unchanged**
(in-context isolate protected by the bar-format gate).

## F1 (133C) — emulsifier identity tiering + native-starch exclusion

- The **directions are already live** via the EV-003 `sprint1` count correction
  (carrageenan/CMC → +2 count = stronger penalty; lecithin-only → −1 = relief) and the
  additive regexes already differentiate native `עמילן` (not an additive) from modified
  `עמילן מוקשה/משונה` (thickener). 133A's taxonomy now supplies **exact identity**.
- `ADDITIVE_IDENTITY_DELTAS` default to **neutral (no-op)** so they do **not double-count**
  `sprint1`. The calibration run (DEC-004) sets the precise per-identity weights **and**
  reconciles/retires the coarse `sprint1` nudges. **No new caps** (Tension-5 budget).
- Food-grade carrageenan (E407) is the modelled form; degraded poligeenan is not a food additive (rule rationale note).

## F4 (133D) — BHA named penalty (BHT excluded)

- **Gate PASSED** (WebSearch 2026-06-01): FDA launched a **post-market reassessment of BHA
  (E320) on 2026-02-10** (RFI closed 2026-04-13; **no final GRAS rule has landed** as of
  2026-06). NTP lists BHA as "reasonably anticipated to be a human carcinogen."
  **BHT (E321) is not yet under reassessment** (FDA reassesses it only after BHA).
- Small **named** BHA penalty (−5 placeholder) on the additive-quality dimension, distinct
  from the generic `antioxidant`-category count (which BHA/BHT/benign tocopherol share).
  **BHT explicitly excluded.** No regulatory-tracking subsystem (a static penalty is correct
  while no rule has landed).

---

## Validation

**Golden corpus** (`run_regression_check.py`): **11 PASS / 1 WARN / 0 FAIL** — identical to
baseline (same scores 85, 50.7, 67.0, 41.4, 45.3, 49.4). The single WARN (soy drink B-vs-C)
is **pre-existing** and unaffected. No golden score changed.

**Cross-corpora before/after** (F2+F4 on vs. neutralized), 464 products, 7 corpora:

| Corpus | Products | Changed | Grade-flips |
|--------|---------:|--------:|------------:|
| snack_bars | 53 | 2 | 0 |
| maadanim (LIVE) | 200 | 1 | 0 |
| yogurt | 45 | 0 | 0 |
| milk | 20 | 0 | 0 |
| cereals | 45 | 1 | 0 |
| bread_light | 32 | 0 | 0 |
| hummus | 69 | 0 | 0 |
| **total** | **464** | **4** | **0** |

All 4 changed products are genuine reconstructed-protein bars routed to `snack_bar_granola`
(`חלבון סויה` primary), moving **down** ~0.8–1.6 pts (correct direction). **Zero grade flips.**
Frozen invariants (milk), in-context whey (yogurt), and hummus are fully preserved.

### Precision iterations during validation
1. Initial broad `isolate_matches` trigger flagged 25/53 bars (milk-powder false positives) →
   narrowed to genuine protein fractions (`RECONSTRUCTED_PROTEIN_MARKERS_HE`, milk powder excluded).
2. A 0.6% soy-crisp / 1.5% collagen trace garnish still triggered on the maadanim corpus
   (one C→D flip) → **primary-position gating (top 3)** added; trace garnishes no longer
   trigger; the maadanim flip is eliminated.

---

## Status & remaining work (gated by DEC-004 + Phase E)

**Structural build of B/C/D: COMPLETE and validated.** Remaining (blocked on DEC-004 PENDING):

1. **Calibration magnitudes** — F2 discount curve (47–81% band), F1 per-identity deltas
   (+ reconcile/retire `sprint1` nudges), F4 penalty size — set in a dedicated calibration run.
2. **Phase E closure** — integrated regression across all real corpora; version bump
   `0.3.1 → 0.4.0`; spec sync (`signal_system.md`, `processing_analysis.md`, `methodology.md`,
   mark `matrix_integrity_framework.md` Req 1 implemented); `ui_language.md` entries; then
   controlled frontend rescore (the maadanim soy-protein bar is the only live-corpus product
   F2 currently touches — its final magnitude must be ratified before rescore).

---

## Phase E — executed 2026-06-01 (owner authorized)

**DEC-004: DECIDED.** Magnitudes ratified: F2 reconstructed ×0.80 / collagen ×0.55; F1 deltas
**neutral/0** (the live EV-003 `sprint1` tiering already realizes F1's directions in proto_v0 —
carrageenan/CMC penalized, lecithin-only carries no penalty, native/modified starch already
split; no additional delta warranted); F4 BHA −5, BHT excluded.

- **Version:** `0.3.1 → 0.4.0` (`methodology.md`, `.claude/scoring.md`, `trace_writer.algorithm_version`).
- **Spec sync:** `signal_system.md` (identity/fragmentation signals), `processing_analysis.md`
  (emulsifier identity tiering — replaces the former flat `Emulsifiers: −6`),
  `methodology.md` (Protein/Additive now matrix-aware; **weight table re-synced to the engine**,
  DEC-004 G3 — was 18/16/12/11/9/7/6/6/4/1, now 15/15/15/12/10/10/8/6/5/4 = 100%),
  `matrix_integrity_framework.md` Req 1 marked **✅ IMPLEMENTED**, `ui_language.md` (4 new lines).

### Controlled frontend rescore — RESULT: no rescore performed (zero displayed-product impact)

Rescore safety check rescored every displayed product on the live pages and isolated TASK-133's
effect (engine with F2/F4 neutralized vs. active):

- **maadanim** (90 displayed): TASK-133 changes **0 / 90**. The one affected maadanim *corpus*
  product (`8410076610379`, a soy-protein bar) is **not displayed** on the curated page.
- The 3 TASK-133-affected products corpus-wide appear in **no** live frontend JSON
  (maadanim / hummus / bread / snacks / yogurt).

→ **TASK-133 changes zero published scores. No frontend rescore is needed or warranted.**

### ⚠️ Separate finding (NOT TASK-133): pre-existing maadanim engine drift

While verifying the rescore, the displayed maadanim scores were found to **no longer match the
current engine**, independent of TASK-133 (all affected products are `protein_matrix_form = None`):
**85 / 90 displayed products differ** from `maadanim_frontend_v2.json` (most by rounding/≤0.5, but
several by 3–4 pts, and at least **one latent grade flip**: `bsip1_maadanim_7290110323585`
52 (C) → 47.9 (D)). The live page was built by an older engine state and has drifted.

**This is out of scope for TASK-133** and must **not** be folded into a TASK-133 rescore (doing so
would conflate unrelated drift with this revision). **Recommend QA/Product open a separate task** to
triage the maadanim engine drift and decide on a clean, governed rebuild. Flagged to the owner.
