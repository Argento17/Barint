# Magnesium Absorbed-Mg Scoring — Final Delivery Table v1
**SUPP-EV-030 v3.1 | SIE Algorithm v0.3.2 | 2026-06-21 (doc reconciliation — multi-form-blend parser fix)**
**Owner co-sign: APPROVED | Nutrition Agent D6/D7: APPROVED**
**v3.1 change: Solgar E→D (33.4→45.2) per 2026-06-21 parser fix; combo-product value-flag exemption documented (owner ruling 2026-06-20); Magnox B6 provenance flagged. Max 550 D/49 + TRIOMAG E/28.8 confirmed unchanged.**

---

## Methodology Summary

Scores are on the ABSORBED-mg dose basis (elemental mg × population-average absorption fraction), gated on the `absorption_by_form` sentinel key in the magnesium dossier. No other dossier carries this key; the scope guard is verified (5/5 non-Mg dossiers: `absorption_by_form` truthy check = False).

**Absorption fractions (PMID:7815675, PMID:30761462, PMID:39770988):**
- citrate: 0.27 | bisglycinate/glycinate: 0.22 | taurate: 0.15
- malate: 0.17 | carbonate: 0.12 | hydroxide: 0.07 | oxide: 0.04

**Recalibrated absorbed-mg ceiling (SUPP-EV-030 v3) — replaces v2 anchors:**

Three changes from v2 to v3:

**Change 1 — `fairy_floor_absorbed`: 37.5 → 0.**
In v2 all Israeli shelf products (best = ~18mg absorbed) fell into `fairy_dust` (dose sub-score = 20 fixed). The ceiling differentiated grades, but Malate 90 at ~18mg blended to only ~47.7 (D) because the fixed dose=20 pulled the blend down. Setting fairy_floor=0 moves all products to `sub_therapeutic`, giving a dose sub-score that scales continuously: `50 + (absorbed_mg / 75) × 34`. At 18mg: dose_sub = 58.2. Blend now exceeds ceiling for all real shelf products → ceiling always governs.

**Change 2 — Ceiling anchors recalibrated.**
Piecewise-linear monotonic ceiling: `(0→20), (1→30), (6→35), (13→44), (19→60), (24→70), (75→100)`.
Monotonicity verified: 20 < 30 < 35 < 44 < 60 < 70 < 100 — strictly increasing.
Malate 18mg: ceiling ~57.3 → C ✓. Oxide 13mg: ceiling 44 → mid-D ✓. Oxide 11mg: ceiling ~41.2 → mid-D ✓. 13mg strictly above 11mg ✓.

**Change 3 — Form weight: 0.05 → 0.**
Absorbed-mg already encodes bioavailability. With ceiling always governing (blend > ceiling for all real products), form is inert in practice. Setting form=0 eliminates even theoretical inversions. Absorbed mg is the unambiguous driver.

**Calibration anchors (dossier `absorbed_ceiling_curve`):**
| Absorbed mg | Grade ceiling | Grade band |
|---|---|---|
| 0 mg | 20 | E-floor |
| 1 mg | 30 | E (< 35) |
| 6 mg | 35 | D-floor (enters D) |
| 13 mg | 44 | mid-D |
| 19 mg | 60 | C (≥ 50) |
| 24 mg | 70 | C headroom |
| ≥ 75 mg | none | no absorbed ceiling |

**Weight overrides for magnesium (dossier `absorbed_weight_overrides`):**
evidence 0.30 | dose 0.40 | form 0.00 | honesty 0.15 | safety 0.10

**Grade bands (unchanged from global):** S≥90, A≥80, B≥65, C≥50, D≥35, E<35

**Honesty guardrail:** absorbed_mg values are population-average estimates, NOT per-product lab measurements.
Display format: `נספג: ~כ-X מ"ג` | Tooltip: `הערכה ממוצעת — לא מדידה מעבדתית`

---

## NT L.C. Hydroxide Correction (RT-10 / BUG-FIX-2026-06-20)

SP-7290010207640 (NT L.C.) was scored as oxide in v2. The panel cache (`7290010207640.json`) correctly records `form="hydroxide"` and ingredient `"מגנזיום (magnesium hydroxide, Dead Sea source)"`, but `normalize_form()` in `il_supplement_panels.py` was iterating `_FORM_MAP` in insertion order and matching `"oxide"` as a substring of `"hydroxide"` (since `"oxide" in "hydroxide"` = True). This caused a normalization error: `form="oxide"` was written into the parsed panel.

**Fix (provenance: scrape mis-parsed; label states hydroxide; red-team verified 2026-06-20):**
`"hydroxide"` added to `_FORM_MAP` BEFORE `"oxide"` so the more-specific entry is checked first. The `oxide_misleading_true` check in `run_full.py` also fixed (word-split guard prevents `"oxide"` from matching inside `"hydroxide"`).

**Corrected calculation:**
450mg compound × 0.417 (Mg(OH)₂ elemental fraction, PubChem CID 14791) = 187.65mg elemental × 0.07 (hydroxide absorption) = 13.14mg absorbed.
Ceiling(13.14) = 35 + (13.14-6)/7 × 9 = 44.4 → D/44.4.

---

## Monotonicity Verification (Shelf Sort by Absorbed mg — Absorbed-Path Products)

All products below sorted strictly by absorbed_mg. Ceiling is a strict function of absorbed_mg → ceiling is monotone. Since blend > ceiling for all real shelf products, the ceiling always governs → final scores are strictly monotone in absorbed_mg.

Products with N/A absorbed_mg (cap_1 evidence-insufficient, proprietary blend, or blend_dominant_limit hidden-composition path) are listed separately as they are NOT in the absorbed ordering and are deliberate exceptions.

| Absorbed mg | Product | Score | Grade | Ceiling Applied |
|---|---|---|---|---|
| ~1.01 mg | Nutricare Taurate | 30.0 | **E** | 30.0 (ceiling=30 at 1mg) |
| ~3.58 mg | Tink Malate 60 | 32.6 | **E** | 32.6 (ceiling at 3.58mg: 30+(3.58-1)/5×5=32.6) |
| ~5.53 mg | Amorphicure carbonate | 34.5 | **E** | 34.5 (ceiling at 5.53mg: 30+(5.53-1)/5×5=34.5; <35 → E) |
| ~7.75 mg | Altman Bisglycinate | 37.2 | **D** | 37.2 (ceiling at 7.75mg: 35+(7.75-6)/7×9=37.2) |
| ~8.75 mg | Altman Citrate 120 | 38.5 | **D** | 38.5 (ceiling at 8.75mg: 35+(8.75-6)/7×9=38.5) |
| ~10.42 mg | Magnox B6 oxide | 40.7 | **D** | 40.7 (ceiling at 10.42mg: 35+(10.42-6)/7×9=40.7) |
| ~10.85 mg | MagUp / Balance (oxide) | 41.2 | **D** | 41.2 (ceiling at 10.85mg: 35+(10.85-6)/7×9=41.2) |
| ~10.94 mg | SupHerb Citrate+B6 | 41.4 | **D** | 41.4 (ceiling at 10.94mg: 35+(10.94-6)/7×9=41.4) |
| ~12.54 mg | Nutricare/Tink/Altman 520 oxide | 43.4 | **D** | 43.4 (ceiling at 12.54mg: 35+(12.54-6)/7×9=43.4) |
| ~13.14 mg | NT L.C. hydroxide | 44.4 | **D** | 44.4 (ceiling at 13.14mg: 35+(13.14-6)/7×9=44.4) |
| ~18.45 mg | Nutricare Malate 90 | 58.5 | **C** | 57.3 → ceiling binds; blend~63 > ceiling → ceiling governs |

**Grades are strictly increasing with absorbed_mg. Monotonicity confirmed.**

Note on 13mg NT L.C. vs 12.54mg 520 oxides: NT L.C. (13.14mg) ceiling=44.4 > 520-oxide (12.54mg) ceiling=43.4 → strict order preserved ✓.
Note on form: Citrate+B6 at 10.94mg scores 41.4 vs oxide at 10.85mg scoring 41.2 — the slight difference is absorbed_mg driving the ceiling (10.94 > 10.85), not form. Form weight = 0; ceiling is the sole driver ✓.

**Exception products (not in absorbed ordering — deliberate):**
| Product | Score | Grade | Reason for exception |
|---|---|---|---|
| Solgar Ca+Mg+D | 45.2 | D | blend_dominant_limit: oxide+citrate blend → form=None → hidden-composition honesty path (2026-06-21 parser fix); cap_3_honesty_core ceiling 49 also fired; blend 45.2 governs |
| Nutricare Nano | 34.0 | E | cap_1: Evidence=Insufficient (liposomal claim, unsupported) |
| Nutricare WELL | 34.0 | E | cap_1: Evidence=Insufficient (proprietary form, unsupported) |
| SupHerb TRIOMAG | 28.8 | E | blend_dominant: Evidence=Insufficient + honesty hidden blend; blend < cap_1 |
| SupHerb Max 550 | 49.0 | D | cap_3_honesty_core: proprietary blend — dose hidden; no absorbed figure; ranked D by honesty cap, not absorbed |
| Hadas Full-Mag 600 | unscoreable | — | Safety UNSCOREABLE: form=None, worst-case elemental 600×0.603=362mg > UL 350mg |

---

## Per-SKU Final Score Table (sorted by absorbed mg ascending)

**Shelf statistics (14 absorbed-path scoreable products — Solgar moved to exception/blend_dominant_limit path as of 2026-06-21 parser fix):**
- Shelf median absorbed: ~10.85 mg (8th of 14, unchanged; Solgar was not in absorbed ordering even in v3)
- Price Q3 threshold (top 25%, n=14 absorbed-path products): 157.9 ILS (unchanged)
- claimShortfallFlag Y: ALL 14 absorbed-path products (none delivers ≥75 mg absorbed)
- Value flag "תמורה גרועה למחיר" Y: 3 products (price ≥157.9 ILS AND absorbed < shelf median 10.85 mg; Solgar removed — see combo-product exemption below)

| SKU ID | Name (Hebrew) | Label compound mg | Form | Elemental mg | Absorbed ~mg | Score | Grade | Binding Constraint | claimShortfallFlag | תמורה גרועה למחיר | Price (ILS) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SP-7290018439579 | נוטריקר מגנזיום טאוראט | 76 | taurate | 6.8 | ~כ-1 | 30.0 | E | cap_2_fairy_dust_hidden_dose | Y | **Y** | 161.9 |
| SP-7290015318532 | טינק מגנזיום מאלאט 60 | 136 | malate | 21.1 | ~כ-4 | 32.6 | E | cap_2_fairy_dust_hidden_dose | Y | N | 129.9 |
| SP-0033984005181 | סולגר סידן ומגנזיום +D | 100 | None (oxide+citrate blend) | — | N/A | 45.2 | D | blend_dominant_limit (cap_3_honesty_core ceiling 49 also fired) | Y | N (combo-product exemption — see below) | 157.9 |
| SP-7290015429245 | אמורפיקיור PH מגנזיום | 160 | carbonate | 46.1 | ~כ-6 | 34.5 | E | cap_2_fairy_dust_hidden_dose | Y | **Y** | 181.9 |
| SP-7290019444480 | אלטמן מגנזיום ביסגליצינט | 250 | bisglycinate | 35.3 | ~כ-8 | 37.2 | D | cap_2_fairy_dust_hidden_dose | Y | N | 134.9 |
| SP-7290011899967 | אלטמן מגנזיום ציטראט 120 | 200 | citrate | 32.4 | ~כ-9 | 38.5 | D | cap_2_fairy_dust_hidden_dose | Y | **Y** | 166.9 |
| SP-7290017847122 | מגנוקס B6 כמוסות מגנזיום | 432 | oxide | 260.5 | ~כ-10 | 40.7 | D | cap_2_fairy_dust_hidden_dose | Y | N | 109.9 |
| SP-7290013142894 | מגנזיום UP אלטמן | 450 | oxide | 271.4 | ~כ-11 | 41.2 | D | cap_2_fairy_dust_hidden_dose | Y | N | 83.9 |
| SP-7290019444206 | אלטמן מגנזיום באלאנס | 450 | oxide | 271.4 | ~כ-11 | 41.2 | D | cap_2_fairy_dust_hidden_dose | Y | N | 110.9 |
| SP-7290013464248 | סופהרב מגנזיום ציטראט+B6 | 250 | citrate | 40.5 | ~כ-11 | 41.4 | D | cap_2_fairy_dust_hidden_dose | Y | N | 75.9 |
| SP-7290001065662 | נוטריקר מגנזיום 520 | 520 | oxide | 313.6 | ~כ-13 | 43.4 | D | cap_2_fairy_dust_hidden_dose | Y | N | 99.9 |
| SP-7290015318426 | טינק מגנזיום אוקסיד 520 | 520 | oxide | 313.6 | ~כ-13 | 43.4 | D | cap_2_fairy_dust_hidden_dose | Y | N | 100.9 |
| SP-7290017218564 | אלטמן מגנזיום 520 | 520 | oxide | 313.6 | ~כ-13 | 43.4 | D | cap_2_fairy_dust_hidden_dose | Y | N | 83.9 |
| SP-7290010207640 | NT L.C. כמוסות מגנזיום | 450 | **hydroxide** | 187.7 | ~כ-13 | 44.4 | D | cap_2_fairy_dust_hidden_dose | Y | N | 74.9 |
| SP-7290001066973 | נוטריקר מגנזיום מלאט 90 | 700 | malate | 108.5 | ~כ-18 | 58.5 | **C** | cap_2_fairy_dust_hidden_dose | Y | N | 149.9 |
| SP-7290001065594 | נוטריקר נאנו מגנזיום ליפוזומלי | 88 | bisglycinate | — | — | 34.0 | E | cap_1_insufficient_evidence | Y | N | 129.9 |
| SP-7290018439043 | נוטריקר מגנזיום WELL | 168 | bisglycinate | — | — | 34.0 | E | cap_1_insufficient_evidence | Y | N | 139.9 |
| SP-7290118816065 | סופהרב TRIOMAG מגנזיום | 200 | citrate blend | — | — | 28.8 | E | blend_dominant_limit | Y | N | 139.9 |
| SP-7290118818205 | סופהרב מגנזיום מקס 550 | 550 | citrate+oxide blend | — | — | 49.0 | D | cap_3_honesty_core | Y | N | 84.9 |
| SP-7290001943700 | הדס פול-מאג 600 מגנזיום | — | — | — | — | unscoreable | — | safety_unscoreable | — | — | 100.9 |

**NT L.C. form note:** hydroxide corrected from erroneously-parsed oxide (RT-10 / BUG-FIX-2026-06-20; provenance: scrape mis-parsed normalization layer; label states "magnesium hydroxide, Dead Sea source"; red-team verified 2026-06-20). Elemental fraction 0.417 (PubChem CID 14791, Mg(OH)₂, MW 58.32). Absorbed: 450 × 0.417 × 0.07 = 13.14mg. Score 44.4/D — correctly ranked above 520-oxide products (12.54mg, 43.4) and below Malate 90 (18.45mg, 58.5).

**Magnox B6 provenance flag (data follow-up, 2026-06-21):** SP-7290017847122 (מגנוקס B6) was scraped from amazon.com (source URL: amazon.com/Magnox-B6-Magnesium-Supplement). Amazon is a geographically questionable source for an Israeli-market product — the listing may reflect a US variant with different formulation details (notably: B6 amount is null in the acquired panel). Flag for Israeli-source re-verification (e.g. Super-Pharm, Yochananof, or direct brand site) before any consumer-facing deployment. Score and absorbed calculation are based on the magnesium oxide compound amount (432mg label; elemental 260.5mg; absorbed ~10.42mg) which is unlikely to differ, but the B6 null is a known data gap.

---

## Grade Changes from v2 (SUPP-EV-030 v2) to v3 (SUPP-EV-030 v3)

| Change | Count | Products |
|---|---|---|
| D → C | 1 | Nutricare Malate 90 (47.7→58.5: fairy_floor=0 → sub_therapeutic; blend now 63 > ceiling 57.3) |
| D → E | 1 | Amorphicure carbonate (35.0→34.5: ceiling recalibration at 5.53mg absorbed; 34.5 < D-floor 35) |
| D → D | 8 | Scores shifted within D; grade unchanged; all strictly monotone |
| E → E | 4 | Taurate, Malate 60, Nano, WELL unchanged in grade |
| D → D | 1 | NT L.C.: form oxide→hydroxide (correction, not calibration change); absorbed 10.85→13.14mg; score 40.9→44.4; grade D unchanged but now correctly placed above 520-oxides |
| special | 1 | TRIOMAG: 30.0→28.8 (blend_dominant; no absorbed path, unchanged pathway) |
| special | 1 | Max 550: 49.0/D unchanged (cap_3_honesty_core) |
| unscoreable | 1 | Hadas unchanged |

**Total grade changes v2→v3: 2/19 (Malate 90 D→C; Amorphicure D→E)**

---

## Grade Changes from v3 to v3.1 (2026-06-21 multi-form-blend parser fix)

**Trigger:** Multi-form-blend parser fix (2026-06-21) — Solgar Ca+Mg+D3 label states "magnesium oxide+citrate"; the parser previously misread form as single-form citrate (16.2mg elemental, 4.37mg absorbed) and scored via the absorbed ceiling path (score 33.4/E, binding cap_2_fairy_dust_hidden_dose). The fix correctly identifies the compound as an undisclosed oxide+citrate blend, sets form=None, and routes Solgar to the hidden-composition honesty path (blend_dominant_limit, cap_3_honesty_core ceiling 49 fired; blend 45.2 governs → score 45.2/D).

| Change | Products | Old score/grade | New score/grade | Binding (old → new) |
|---|---|---|---|---|
| E → D | Solgar Ca+Mg+D (SP-0033984005181) | 33.4/E | 45.2/D | cap_2_fairy_dust_hidden_dose → blend_dominant_limit |

**Confirmed unchanged by 2026-06-21 fix:**
- Max 550 (SP-7290118818205): 49.0/D, cap_3_honesty_core — UNCHANGED
- TRIOMAG (SP-7290118816065): 28.8/E, blend_dominant_limit — UNCHANGED

**Total grade changes v3→v3.1: 1/20 (Solgar E→D)**

---

## Grade Changes from Pre-SUPP-EV-030 Baseline (original → v0.3.2)

| Change | Count | Products |
|---|---|---|
| B → D | 1 | מגנזיום UP (oxide; was incorrectly high due to elemental-mg bias) |
| C → D/E | 5 | Nutricare 520, Tink 520, Altman 520, Magnox B6, Altman Balance (oxide absorption reality) |
| D → C | 1 | Nutricare Malate 90 (best absorber on shelf; now correctly graded C) |
| D → E | 3 | Taurate, Tink Malate 60, Amorphicure (near-zero absorbed → E correctly) |
| D → D | 8 | Continuous score differentiation within D |
| E → E | 3 | Unchanged (insufficient evidence) |

**Total grade changes from original baseline: 13/19 scored**

---

## Value Flag Details ("תמורה גרועה למחיר")

**Combo-product / multivitamin exemption (owner ruling, 2026-06-20):** Combination products (e.g. Ca+Mg+D3, multivitamins) are EXEMPT from the "תמורה גרועה למחיר" value flag. The price of a combination product covers multiple actives; applying a magnesium-only value judgement misrepresents what the consumer is paying for. The value flag applies to single-active premium products with poor magnesium delivery only. Solgar Ca+Mg+D3 (SP-0033984005181) is exempt under this ruling.

**Value flag set = single-active premium + poor magnesium delivery products only.**

These 3 products are in the top price quartile (≥157.9 ILS) AND deliver absorbed magnesium below the shelf median (~10.85 mg):

1. **SP-7290018439579** — נוטריקר מגנזיום טאוראט — 161.9 ILS, ~1 mg absorbed → **grade E** (worst value: most expensive, lowest absorbed)
2. **SP-7290015429245** — אמורפיקיור PH מגנזיום — 181.9 ILS, ~6 mg absorbed → **grade E** (most expensive product on shelf, grades E)
3. **SP-7290011899967** — אלטמן מגנזיום ציטראט 120 — 166.9 ILS, ~9 mg absorbed → **grade D**

---

## Implementation Artifacts

| Artifact | Path | Role |
|---|---|---|
| Engine source | `03_operations/supplement_engine/proto_v0/src/score_engine.py` | `_absorbed_ceiling()` + `combine()` (new `elif sub_therapeutic` clause for cap_2) |
| Constants | `03_operations/supplement_engine/proto_v0/src/constants.py` | Version 0.3.2 |
| Magnesium dossier | `03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml` | `fairy_floor_absorbed=0`, new `absorbed_ceiling_curve.anchors`, `form=0` in overrides |
| Form map fix | `integrations/clients/il_supplement_panels.py` | `_FORM_MAP`: hydroxide added before oxide (RT-10 BUG-FIX-2026-06-20) |
| Corpus runner | `02_products/supplements/real_corpus_v3/run_full.py` | oxide_misleading word-split fix; output to `_corpus_run_full_v10.json` |
| Golden fixtures | `03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py` | Comment update for FORM-FAIL-mg-oxide (logic unchanged; expectation binding=cap_2 still holds) |
| SKU JSONs (19) | `02_products/supplements/real_corpus_v3/skus_full/SP-*.json` | `engine_output` updated with new scores; NT L.C. form=hydroxide |
| This document | `03_operations/supplement_engine/proto_v0/benchmark/magnesium_absorbed_scoring_FINAL_v1.md` | Final delivery record (v3 update) |

---

## Validation Results

**Golden corpus: 18/18 PASS** (SIE v0.3.2)
**Scope guard: 5/5 non-Mg dossiers confirm `absorption_by_form` truthy check = False** — absorbed path never fires outside magnesium
**Monotonicity: PASS** — all 14 absorbed-path products strictly ordered by absorbed_mg; ceiling always governs (blend > ceiling for all); no inversions (Solgar moved to exception/blend_dominant_limit path as of v3.1)

Evidence type: CALIBRATION-PENDING (prototype; no published score, no frontend, no category launch)
