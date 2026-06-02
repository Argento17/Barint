# TASK-144 — Implementation & Delta Report (engine 0.4.0 → 0.4.1)

**Owner:** nutrition-agent · **Date:** 2026-06-01 · **Proposed disposition:** RETURNED
**Approved outcome (PO):** GO lands ~77/B; B ceiling stands; **no A** (RULING-DAIRY-A-01 holds).
**Scope:** maadanim run only (gated `BARI_TASK144_FIXES`, default OFF). **No frontend JSON touched.**

---

## A. GO — new score + dimension breakdown (confirms ~77/B)

**יופלה GO מועשר בחלבון** (`bsip1_maadanim_7290110321031`): **69.6/B → 77.7/B** (rounds to **78/B**).
Engine 0.4.1, NOVA 3→2, confidence 90/high, category dairy_protein.

| Dimension | 0.4.0 | 0.4.1 | Driver |
|---|---|---|---|
| processing_quality | 65 | **85** | sanitizer: ingredient_count 8→3 → NOVA 3→2 (EV-026) |
| nutrient_density | 32.5 | **50.0** | fiber not-applicable (dairy) → protein-only (EV-027) |
| calorie_density | 85 | 90 | (router gives dairy_protein table; pre-existing, not TASK-144) |
| glycemic_quality | 90 | 90 | — |
| protein_quality | 42.5 | **50.0** | source mixed→dairy, drop ×0.85 haircut (EV-028) |
| additive_quality | 100 | 100 | — |
| satiety_support | 100 | 100 | — |
| fat_quality | 50 | 50 | sat-fat absent → neutral |
| regulatory_quality | 95 | 95 | — |
| whole_food_integrity | 60 | **85** | NOVA 3→2 (EV-026) |

Ingredient sanitization: `8 → 3` (`חלב`, `חלבוני חלב (7.4%)`, `אבקת חלב`); dropped 4 nutrition-panel/disclaimer items, truncated `אבקת חלב.n20 גרם…` → `אבקת חלב`.

**A is NOT reached.** GO has no live culture (`has_fermentation:false`) and is a protein-enriched/reconstituted matrix → fails RULING-DAIRY-A-01 C3/C4. 77.7/B is the truthful, ruling-consistent score.

---

## B. Every maadanim product whose score/grade changed (clean TASK-144 attribution)

Method: same patched engine + same router, fixes **OFF vs ON** (`BARI_TASK144_FIXES`), so deltas are attributable to TASK-144 alone (NOT the pre-existing router/engine drift). Source data: `task144_delta_data.json`.

- **Corpus:** 200 · **score changed:** 119 · **grade changed:** 21.
- All grade changes are dairy products previously penalized for absent fiber / OCR-inflated NOVA. Mostly D→C and E→D lifts; none is a dessert reaching A.

### 21 grade changes (old → new)
| Old | New | NOVA | Product |
|---|---|---|---|
| 42.7/D | 57.5/C | 4→3 | יופלה טיוב תות בננה |
| 46.7/D | 60.7/C | 4→3 | גמדים לשתיה תות בננה |
| 48.6/D | 54.9/C | 4→4 | משקה יוגורט פרו וניל ללס |
| 49.1/D | 54.8/C | 3→3 | מעדן הגולן שוקולד מריר |
| 45.0/D | 50.6/C | 4→4 | מעדן גבינה מוקצף וניל |
| 48.4/D | 53.9/C | 3→3 | מעדן הגולן וניל |
| 45.5/D | 50.6/C | 4→4 | דנונה תות 3% שומן |
| 34.2/E | 39.2/D | 4→4 | משקה יוגורט תות-מלון |
| 34.3/E | 39.2/D | 4→4 | משקה יופלה בננה תות1.6% |
| 33.0/E | 37.3/D | 4→4 | ריבת פירות יער |
| 48.7/D | 53.0/C | 4→4 | גמדים סקוויז לדרך תות |
| 46.5/D | 50.8/C | 4→4 | גמדים ארוחת בוקר תות |
| 33.2/E | 37.4/D | 4→4 | ריבת תות |
| **79.4/B** | **82.4/A** | 3→3 | **גבינה צפתית מעודנת 5%** ⚠️ (see §D) |
| 48.7/D | 51.7/C | 4→4 | יופלה GO דובדבן 0.7% |
| 62.8/C | 65.5/B | 4→4 | יוגורט GO קרמי אפרסק |
| 48.5/D | 50.1/C | 4→4 | דניאלה תות בננה |
| 48.5/D | 50.1/C | 4→4 | דניאלה תות מוקצף5% שומן |
| 33.6/E | 35.0/D | 4→4 | עוגת גבינה פירורים |
| 34.6/E | 35.9/D | 4→4 | מילקי בלונדי |
| 49.5/D | 50.3/C | 3→3 | פודינג אינסטנט שוקולד |

### Patched grade tally (200-product run, 0.4.1)
A:1 (mis-binned cheese, §D) · B:4 · C:53 · D:84 · E:26 · insufficient:32.

### Live 87-curated vs new authoritative (full reconcile list)
62 of 87 live products changed (this set mixes TASK-144 effect with pre-existing router/engine drift baked into the live JSON). The complete old→new list is in this report's companion data and was provided to CC inline. Notable boundary crossings on live products: GO 70/B→78/B; מעדן סויה ביו 57/C→70/B (soy, sanitizer-driven, not dairy-A); several C→B / D→C lifts; two minor regressions (אינסטנט פודינג 41/D→insufficient on macro guard; באדי 50/C→50/D rounding). CC to reconcile against the 87 hand-authored `rowVerdict` strings.

---

## C. Cross-category blast radius (Fix 1/2/3 reach) — `task144_blast_radius.json`

Method: each frozen corpus run fixes OFF vs ON on the patched engine.

| Category | Corpus | Score Δ | Grade Δ | Assessment |
|---|---|---|---|---|
| snack_bars | 53 | 14 | 1 (E→D crispbread) | sanitizer; benign |
| cereals | 45 | 0 | 0 | **gate tight — inert** |
| milk | 20 | 4 | 1 (D→C oat beverage) | sanitizer; benign, far from A |
| cheese | 57 | 50 | 6 (C→B/D→C/E→D) | Fix 2 dairy effect; none reaches A |
| hummus | 69 | 2 | 0 | A's preserved (after truncation fix) |
| yogurt | 86 | 65 | 8 (incl. **3 B→A**) | Fix 2/3 dairy effect |
| bread_light | 32 | 0 | 0 | **gate tight — inert** |

**Decision:** because maadanim and frozen yogurt/cheese share the `dairy_protein` routing category, a category gate cannot separate them. The three fixes are therefore **scoped to the maadanim run only** (default `BARI_TASK144_FIXES=off`; only `batch_run_maadanim_001.py` opts in). **Verification of frozen isolation:** at production default, golden corpus PASS (whole milk 85/A, go-milk 41.4/E, plain yogurt B) and **yogurt_003 = 0 diff vs committed frozen traces**. Router regression all pass. Frozen invariants intact.

The yogurt/cheese B→A's are architecturally *correct* (clean intact fermented dairy can earn A per the milk 85/A precedent) but are **out of TASK-144 scope** and on FROZEN categories → **cross-category adoption requires Product Agent sign-off** (escalation per Nutrition Agent rules). Logged as an opportunity, not deployed.

---

## D. Two maadanim-corpus anomalies for CC (NOT on the live 87 shelf)

1. **`יוגורט גו נטול לקטוז` (id 7290116932620)** — BSIP1 source has `protein_g=190.0/100g` (physically impossible; OCR `19.0`→`190` parse error). Pre-guard it produced a spurious 88.7/A. The new **macro-plausibility guard** now flags it `insufficient_data` (correct). Source data needs correction.
2. **`גבינה צפתית מעודנת 5%` (id 554532)** — the only A in the patched corpus (82.4/A). It is a **צפתית cheese mis-binned into the maadanim shelf**, not a dessert. Its A is partly a fiber-not-applicable lift; its C1 "added sugar" signal is a **false positive** from un-sanitized nutrition-panel text in `ingredients_text_he` (`6 גרם סוכרים`). It is **not on the live 87 shelf.** Recommend CC exclude it from the maadanim corpus (wrong category). It is NOT a dessert A and not a counterexample to the dairy A-ceiling.

Neither product is in the 87 curated live entries — **the live maadanim shelf has no A.**

---

## E. Governance record

- **Engine bump:** 0.4.0 → **0.4.1** (`trace_writer.py`). Numbers-versioning, no architecture change.
- **Evidence registry:** EV-026 (sanitize), EV-027 (fiber-not-applicable, tight allowlist), EV-028 (dairy source typing) + macro-plausibility companion — `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.
- **Activation scope:** maadanim run only via `BARI_TASK144_FIXES` (default OFF). Tight category allowlist on Fix 2.
- **F2/TASK-133B collision:** none (verified — mutually exclusive gates; GO `protein_matrix_form=None`).
- **Rollback:** unset `BARI_TASK144_FIXES` → frozen 0.4.0 behavior returns deterministically; or revert the four source files. Notify: Central Controller + Product Agent.
- **Regression:** `run_regression_check.py` PASS (1 pre-existing soy WARN), `run_router_regression.py` all PASS.
- **Files changed:** `signal_extractor.py`, `score_engine.py`, `nova_proxy.py`, `constants.py`, `trace_writer.py`, `batch_run_maadanim_001.py`. New harnesses: `run_maadanim_144_delta.py`, `run_task144_blast_radius.py`.
- **NOT touched:** `bari-web/src/data/comparisons/maadanim_frontend_v2.json` (87 hand-authored `rowVerdict` strings preserved for CC surgical reconcile).

**Only the Central Controller records the baseline re-freeze and CLOSED.**
