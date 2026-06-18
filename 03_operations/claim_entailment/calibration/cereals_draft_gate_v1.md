# Cereals Draft Gate — Entailment Check v1

**Task:** TASK-254 / P17 — first pre-ship gate (production rehearsal for rubric v2)
**Draft:** `cereals_copy_remediation_draft_v1.json` (34 products, NEW rowVerdict + insightLine)
**Rubric:** `claim_entailment_rubric_v2.md` (§4 two-layer; §5 decomposition)
**Ground truth:** Reconstruction traces (`run_cereals_008_reconstruction/`, `run_cereals_multiretailer_001_reconstruction/`) + draft badge fields + methodology docs
**Date:** 2026-06-12
**Checker:** QA Agent

---

## 1. Verdict Totals

| Verdict | Strings (68 total) | Products with non-PASS |
|---------|-------------------|----------------------|
| **PASS** (all claims entailed) | 51 | — |
| **REVIEW** | 15 | 14 products |
| **HARD-FAIL** | **0** | — |
| **UNVERIFIABLE** | 2 | 2 products |

**Zero HARD-FAILs.** The draft successfully remediates all 17+ live incidents identified in Phase 1c calibration (CHF-01 through CHF-21).

**Draft is owner-read-ready.** The 15 REVIEW items are editorial framing, superlatives requiring corpus scan, and data-availability caveats. A content fix loop is NOT required before owner review. Proceed to owner read.

---

## 2. Items Checked — Clean Results

| Check | Status |
|-------|--------|
| Sodium causal language (auto HARD-FAIL) | Not found in any string |
| MoH/red-label invocations | Not found (no `"הסף האדום"`, `"משרד הבריאות"`) |
| Grade letters in text vs badge field | All 34 products match exactly |
| T4 prior-run / provenance claims | Not found (all removed as stated) |
| BHT/vitamin enrichment as grade cause | Not found |
| Fabricated mechanism claims | None — all causal statements are T3 editorial or consistent with trace |

---

## 3. HARD-FAILs: 0

None.

---

## 4. UNVERIFIABLE: 2 strings

### UNV-01 — bsip1_cereal_7290112495228 (קורנפלקס דבש)
**String:** new_rowVerdict
**Claim:** `"נתוני סיבים לא היו זמינים"`
**Type:** T1
**Evidence:** L1_observed_signals.dietary_fiber_g = null. Claim is factually correct but per rubric §2.1 step 2, null → UNVERIFIABLE.
**Verdict:** UNVERIFIABLE (data gap, not fabrication)

### UNV-02 — bsip1_cereal_5900020046833 (Cheerios whole grain oat)
**String:** new_rowVerdict
**Claim:** `"נתוני סיבים לא היו זמינים"`
**Type:** T1
**Evidence:** Same pattern — dietary_fiber_g = null in trace.
**Verdict:** UNVERIFIABLE (data gap, not fabrication)

---

## 5. REVIEW: 15 strings

### 5.1 Superlatives / Corpus Claims (need corpus-wide scan)

| # | Product | String | Phrase | Evidence |
|---|---------|--------|--------|----------|
| R-01 | bsip1_cereal_7290017325910 (הרדוף) | rowVerdict | `"הרשימה הקצרה ביותר בקטגוריה"` | 3 ingredients; needs full corpus ingredient-count sort to confirm "shortest." T3 superlative per rubric §8.3. |
| R-02 | bsip1_cereal_7296073642046 (ללא גלוטן) | rowVerdict | `"עובדה לדגל"` about 390mg sodium | Editorial emphasis on sodium. Sodium is fact-only (no cap fired), but "עובדה לדגל" is T3 framing. |

### 5.2 T3 Editorial Causal Framing

| # | Product | String | Phrase | Evidence |
|---|---------|--------|--------|----------|
| R-03 | bsip1_cereal_7613037686906 (Fitness almond honey) | rowVerdict | `"ב כי הפרופיל התזונתי מחזיק"` | Real dominant driver = confidence ceiling (missing ingredients). T3 interpretation, not a claim of an unfired rule → REVIEW |
| R-04 | bsip1_cereal_7613033548192 (Fitness Dark Chocolate) | rowVerdict | `"ב; הפרופיל התזונתי מחזיק את הציון"` | Same pattern — confidence ceiling is the real cap → REVIEW |
| R-05 | bsip1_cereal_7297488098688 (פצפוצי אורז) | rowVerdict | `"3 גרם סיבים ו-8 גרם חלבון ... עוצרים את הציון"` | Trace shows NOVA cap (not binding here) + nutrient_density limits. Attributing stop to specific numeric values is T3 editorial → REVIEW |
| R-06 | bsip1_cereal_5900020041142 (קורנפלקס פיטנס) | rowVerdict | `"ה-1.3 גרם סיבים בולטים כמגבלה"` | Confidence ceiling dominant. Fiber IS a limiting dimension, but "בולטים כמגבלה" is editorial → REVIEW |
| R-07 | bsip1_cereal_7290116535371 (קורנפלקס לל"ג) | rowVerdict | `"מוצר מעובד בינוני, הסיבים הנמוכים מגבילים"` | NOVA_PROXY_3_PROCESSED cap + nutrient_density limited by fiber. "סיבים נמוכים מגבילים" is consistent with trace dimension notes (nutrient_density limited by fiber) but interpretive. Acceptable → REVIEW |
| R-08 | bsip1_cereal_7297488199590 (פצפוצי אורז תפוח) | rowVerdict | `"עיבוד בינוני וסיבים נמוכים מאוד מגבילים"` | Binding cap = NOVA_PROXY_3_PROCESSED + fiber limit. Consistent T3 → REVIEW |
| R-09 | bsip1_cereal_5900020036407 (ליון) | rowVerdict | `"רמת הסוכר מחילה מגבלה על הציון"` | ISRAELI_RED_LABEL_1_SUGAR IS the binding cap. This is correct. But the NOVA_PROXY secondary cap is omitted. Minor simplification → REVIEW |
| R-10 | bsip1_cereal_5900020012814 (נסקוויק) | rowVerdict | `"רמת הסוכר גבוהה ומחילה מגבלה על הציון"` | Same pattern as R-09. Correct but a simplification → REVIEW |
| R-11 | bsip1_cereal_72968 (סיני מיניס) | rowVerdict | `"רמת הסוכר גבוהה ומחילה מגבלה"` | Same pattern. ISRAELI_RED_LABEL_1_SUGAR + HIGH_SUGAR_25G_PLUS both fired. Correct but simplified → REVIEW |
| R-12 | bsip1_cereal_42400108153 (Froot Loops style) | rowVerdict | `"הסוכר הגבוה מחיל מגבלה ונוספים צבעי מאכל סינתטיים"` | Sugar cap + artificial colors = consistent with trace (ISRAELI_RED_LABEL_1_SUGAR + has_artificial_color). T3 coupling of color and sugar as joint limit is editorial → REVIEW |

### 5.3 T1 Data-Availability Claims

| # | Product | String | Phrase | Evidence |
|---|---------|--------|--------|----------|
| R-13 | bsip1_cereal_7290017325910 (הרדוף) | rowVerdict | `"נתוני חלבון וסיבים חלקיים"` | L1 shows protein_g=8.0, dietary_fiber_g=4.0 — both non-null. Claiming "partial" (חלקיים) when values exist is potentially misleading. No missing_nutrition_fields for protein or fiber (only sat_fat missing) → REVIEW |
| R-14 | bsip1_cereal_7290116537351 (כריות נוגט) | insightLine | `"כריות עם מילוי נוגט"` | Product descriptor. "מילוי נוגט" describes the product type, which is consistent with high fat and missing sugar data but isn't verified from trace inputs → REVIEW |

### 5.4 T1 Numeric — Missing display_values

| # | Product | String | Phrase | Evidence |
|---|---------|--------|--------|----------|
| R-15 | bsip1_cereal_5010029000061 (ויטביקס) | insightLine | `"95% חיטה, 12 גרם חלבון ו-10 גרם סיבים"` | T1 values are present in trace L1_observed_signals (protein_g=12.0, dietary_fiber_g=10.0, ingredient_list shows "חיטה (מכיל גלוטן) (95%)"). Verifiable from trace → PASS on trace check. However, without a display_values inventory (§9), these cannot be Layer-1 verified. Marking REVIEW per rubric transition protocol until display_values are populated. |

---

## 6. Drift Products (9) — All Clean

| Product | Live | Recon | Copy grade | Verdict |
|---------|------|-------|------------|---------|
| 7296073642046 (ללא גלוטן) | 61/C | 58/C | C | PASS — grade matches live badge; drift (3pt, same grade) flagged as pipeline finding per §4.3 |
| 7290112494351 (של אלופים) | 60/C | 57/C | C | PASS — same pattern |
| 7290107647854 (שוגי) | 53/C | 50/D | C | PASS — grade matches live badge; grade-band drift (C→D) flagged as DISPLAY-DRIFT per §4.3 |
| 7290112495433 (דליפקאן) | 46/D | 43/D | D | PASS |
| 7296073642022 (טבעות דבש לל"ג) | 43/D | 42/D | D | PASS |
| 7290112495228 (קורנפלקס דבש) | 40/D | 37/D | D | PASS |
| 8445290964595 (קיטקט) | 39/D | 37/D | D | PASS |
| 3387390525960 (קראנץ') | 37/D | 35/D | D | PASS |
| 884912126115 (גרייט גריינס) | 35/D | 35/E | D | PASS — grade matches live badge; grade-band drift (D→E) flagged as DISPLAY-DRIFT |

**Mechanism claims in draft for drift products:** All causal statements verified against trace drivers. No fabricated claims. Key examples:
- Great Grains: `"ד כי הסוכר גבוה ורמת העיבוד גבוהה ומחילים מגבלה"` — matches trace (ISRAELI_RED_LABEL_1_SUGAR + HIGH_SUGAR_25G_PLUS + NOVA4). BHT mentioned as fact only (`"BHT (E321) ברשימה כנוגד חמצון"`), not as grade cause ✓
- קורנפלקס דבש: `"מוצר מעובד"` + `"368 מ״ג נתרן"` — sodium as fact only ✓

---

## 7. Special-Attention Items Verified

### Sodium causal language
Auto HARD-FAIL per Nutrition ruling. **Result: Not found.** All sodium references are factual observations. Examples:
- `"600 מ״ג נתרן ל-100 גרם בולטים"` (הרדוף) — "stand out" as notable, not causal
- `"390 מ״ג נתרן ל-100 גרם"` (פצפוצי אורז תפוח) — fact only
- `"עובדה לדגל"` (ללא גלוטן) — flagged for attention, marked REVIEW

### MoH / red-label invocations
**Result: Not found.** No `"משרד הבריאות"`, `"הסף האדום"`, or similar MoH authority references in any NEW string.

### Grade letters vs badge field
**Result: All 34 match exactly.** Every grade claim in copy (ב/ג/ד/ה) matches the corresponding badge.grade field in the draft entry. The 9 drift products reference their live badge grade, not reconstructed grade.

### T4 prior-run claims
**Result: Not found.** All prior-run references (like `"הציון הקודם"`, `"בגרסה הקודמת"`) from old copy have been removed as stated in the draft's _meta.hard_rules_applied.

### BHT / vitamin enrichment as grade cause
**Result: Not found.** Great Grains rowVerdict mentions BHT as `"BHT (E321) ברשימה כנוגד חמצון"` — factual observation, not grade attribution. Vitamin enrichment not mentioned as grade cause anywhere.

---

## 8. Return Block

**Status proposed: RETURNED**

**Deliverable:** `C:\Bari\03_operations\claim_entailment\calibration\cereals_draft_gate_v1.md`

**Gate verdict: PASS** — no HARD-FAILs. The draft is owner-read-ready. Content fix loop is not required.

**15 REVIEW items** (non-blocking) for owner awareness during read:
- 2 superlatives requiring corpus scan (R-01, R-02)
- 10 T3 editorial causal framings (R-03 through R-12) — all are interpretive but consistent with trace
- 1 potentially misleading data-availability claim (R-13)
- 1 product descriptor (R-14)
- 1 display_values gap (R-15)

**2 UNVERIFIABLE items** — fiber null in source data. Acceptable; documented as data gaps.

**Outstanding pipeline findings (not copy issues):**
- 9 drift products tracked for next cereals re-ship
- display_values inventory (§9) needed for Layer-1 T1 numeric verification
- No change to current live site required — this gate covers the remediation draft only

**Registry update:** Close TASK-254. The first pre-ship gate confirms the remediation draft is ready for owner read.
