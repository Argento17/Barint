# Bari Scoring Recalibration v1
**Date:** 2026-05-30
**Status:** Implementation-ready
**Decision authority:** Product Owner
**Scope:** BSIP2 engine (proto_v0), all scored categories

---

## Problem Statement

The current scoring system is architecturally correct but calibrated too conservatively. The result:
- Strong products (whole grain, fermented, clean label) cluster in the B range (65–79)
- Grade A is effectively unreachable for most real Israeli supermarket products (NOVA3 cap = 82 leaves only a 2-point A window: 80–82)
- Fermentation — a genuine quality signal — contributes ≤0.2 pts to total score (buried in a 0.04-weight dimension)
- Good sourdough bread scores the same as a mediocre factory loaf
- Relative ranking is broadly correct; absolute positions feel unfair

**Direction from Product Owner:**
- Strong products move up 10–20%
- Relative ranking broadly stable
- Weak products do not become falsely good

---

## Recalibration Changes

### R-01 — NOVA3 Processing Cap: 82 → 87

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\constants.py`

**Current behavior:**  
Any product with NOVA proxy level 3 is capped at score 82. Since most real Israeli supermarket products (bread, dairy, bars) are NOVA3, this limits the effective top score to 82. Grade A requires ≥80, leaving only a 2-point window.

**Proposed behavior:**  
Cap raises to 87. Genuinely high-quality NOVA3 products (whole grain, minimal additives, good nutrition) can now score up to 87 and comfortably reach grade A.

**Expected score impact:**  
- NOVA3 products currently constrained at ~82: gain 0–5 pts
- NOVA3 products scoring below 80: no change (cap doesn't bind)
- NOVA4 cap (68) unchanged

**Categories affected:** Bread, dairy, snack bars

**Implementation:**
```python
# constants.py — PROCESSING_CAPS
# Change:
("NOVA_PROXY_3_PROCESSED", "nova==3", 82),
# To:
("NOVA_PROXY_3_PROCESSED", "nova==3", 87),
```

---

### R-02 — Fermentation Direct Score Bonus: +6 pts

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`

**Current behavior:**  
Fermentation signal (`has_fermentation=True`) adds only +5 to the WFI dimension raw score. At WFI weight = 0.04, this contributes 0.2 pts to the final score. Statistically invisible. A real sourdough bread scores the same as a factory loaf claiming "sourdough" on the label.

**Proposed behavior:**  
After the weighted dimension sum and before guardrail cap application, add +6 directly to the score for products where `has_fermentation=True` and `nova_level ≤ 3`. NOVA4 products are excluded (fermentation in a heavily processed product doesn't redeem it).

**Expected score impact:**  
- Sourdough bread (NOVA3, currently 72–78): → 78–84, grade B → A
- Fermented dairy/yogurt (NOVA1–2): → +6 pts, well into A range
- NOVA4 products: no bonus
- Non-fermented products: no change

**Categories affected:** Bread (sourdough products), dairy (yogurt, kefir, fermented milk)

**Implementation:**
```python
# score_engine.py — in score_product(), after weighted dimension sum,
# before _apply_guardrail_caps()
# Add:
has_fermentation = l3.get("has_fermentation", False)
nova_level = l3.get("nova_level", 4)
if has_fermentation and nova_level <= 3:
    pre_guardrail_score = min(100, pre_guardrail_score + 6)
    score_trace.append("fermentation_bonus: +6 (direct, pre-cap)")
```

---

### R-03 — Fiber Nutrient Density Ceiling: 85 → 95

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`

**Current behavior:**  
Fiber scoring function maxes at 85 at ≥12g/100g. A bread with 14g fiber scores the same as a bread with 12g fiber.

**Proposed behavior:**  
Raise the ceiling to 95 at 12g, keeping the same breakpoint. Products at 12g+ fiber see a meaningful improvement.

**Expected score impact:**  
- Breads with 12g+ fiber: ND dimension raw score +6 → final score +0.9 pts (ND weight 0.15)
- Breads with 8g fiber: ND raw score +4 → final +0.6 pts
- Products with low fiber (<5g): minimal change
- Net: modest but real uplift for genuinely high-fiber whole grain products

**Categories affected:** Bread, crispbreads, cereals

**Implementation:**
```python
# score_engine.py — in score_nutrient_density()
# Change:
fs = min(85, max(0, (fiber / 12) * 85))
# To:
fs = min(95, max(0, (fiber / 12) * 95))
```

---

### R-04 — Natural Dairy Sugar Relief (NOVA1–2 plain dairy)

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py`

**Current behavior:**  
Lactose in plain dairy (milk, plain yogurt) triggers the same sugar caps as added sucrose. A plain yogurt with 4g lactose/100ml can hit the ISRAELI_RED_LABEL_1_SUGAR guardrail and be penalized as if it were sweetened.

**Proposed behavior:**  
Apply the existing SC-2 relief logic (already implemented for whole-fruit snacks) to plain dairy products: NOVA1–2 products where the detected sugar source is lactose only (no added sugar markers in ingredients) receive the same cap relaxation as SC-2.

**Trigger conditions:**
- `nova_level in [1, 2]`  
- `product_type == "dairy"` (detected from ingredient text: "חלב", "יוגורט", "גבינה")
- No added sugar markers in ingredients (`added_sugar_sources == 0`)

**Expected score impact:**  
- Plain cow's milk (NOVA1, lactose only): remove spurious red-label sugar penalty → +5–8 pts
- Flavored/sweetened dairy: no change (has added sugar markers)
- Non-dairy alternatives with added sugar: no change

**Categories affected:** Milk, yogurt, fermented dairy

**Implementation:**
```python
# score_engine.py — in evaluate_guardrails(), in the SUGAR_LOAD guardrail family
# Existing SC-2 check pattern (from RC-01): 
# if sc2_relief:
#     apply relaxed caps instead of standard caps
# Extend the SC-2 condition to also include plain dairy:
is_plain_dairy = (
    nova_level in [1, 2] and
    l3.get("product_type_dairy", False) and
    l3.get("added_sugar_sources", 0) == 0
)
sc2_or_plain_dairy = sc2_relief or is_plain_dairy
# Use sc2_or_plain_dairy in place of sc2_relief in cap selection
```

New signal needed in `signal_extractor.py`:
```python
DAIRY_BASE_MARKERS_HE = ["חלב", "יוגורט", "גבינת", "מי גבינה", "קזאין"]
product_type_dairy = any(m in first_three_ingredients for m in DAIRY_BASE_MARKERS_HE)
# Add to L3:
"product_type_dairy": product_type_dairy,
```

---

### R-05 — Yogurt Calorie Density Table (new archetype)

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\constants.py`

**Current behavior:**  
No "yogurt" entry in `CALORIE_DENSITY_TABLES`. Yogurt products would fall back to "default" table.

**Proposed behavior:**  
Add yogurt-specific calorie density breakpoints. Yogurt naturally ranges 50–120 kcal/100g for plain varieties; flavored/full-fat ranges 100–200.

**Implementation:**
```python
# constants.py — CALORIE_DENSITY_TABLES
# Add:
"yogurt": [(60,95),(100,88),(140,78),(180,65),(250,50),(1e9,30)],
```

**Category routing:**  
When BSIP2 detects `category_archetype == "yogurt"`, use this table. Plain yogurt at 60 kcal → 95; Greek yogurt at 100 kcal → 88.

---

## Combined Impact by Category

### Bread (24 products, scores 59–82)

| Product type | Current range | Expected post-calibration |
|---|---|---|
| Sourdough whole grain (e.g., "לחם מחמצת קמח מלא") | 72–78/B | 80–86/A |
| Whole grain non-fermented (e.g., "לחם ירוק מקמח מלא") | 75–80/B–A | 77–83/B–A |
| Crackers/crispbreads (e.g., "קרקר כוסמין מלא") | 78–82/B–A | 79–84/A |
| Standard/white bread | 59–67/C–B | 60–69/C–B |

### Snacks (18 products, scores 17–70)

| Product type | Current range | Expected post-calibration |
|---|---|---|
| Date bar (NOVA2, snk-001) | 70/B | 70–72/B (minimal change) |
| Clean date+nut bars (NOVA1–2) | 57–63/C | 58–65/B–C |
| Protein bars (NOVA3–4) | 43–59/C–D | 44–62/C–D |
| Grade E products | 17–33/E | 17–35/E–D (no meaningful change) |

### Milk (18 products, hand-curated, not re-run)
- R-04 would apply if scores were re-derived from BSIP2
- Hand-curated values: no change needed for MVP; note in methodology

### Yogurt (future category)
- All changes apply when BSIP2 run is performed
- R-04 + R-05 provide correct treatment for plain dairy

---

## SHOULD-HAVE After MVP

**R-06: Whole-grain primary ingredient bonus (+5)**  
When the first ingredient is whole grain flour (קמח מלא, קמח שיפון מלא, etc.), apply +5 directly to final score. Requires new `whole_grain_primary` signal in `signal_extractor.py`. This would lift non-fermented whole grain breads by 5 pts — most go from solid B to A. Defer to Sprint 2 to avoid BSIP2 re-run before MVP.

**R-07: Grade threshold for A: 80 → 77**  
Lower the A threshold slightly to reflect that Israeli supermarket products cannot realistically reach 90+. A score of 77 on a real, honest product in this market IS outstanding. Keep this as a discussion item — only implement if post-calibration grade distribution still feels too harsh.

---

## Implementation Order

1. `constants.py`: R-01 (NOVA3 cap), R-05 (yogurt calorie table)
2. `score_engine.py`: R-02 (fermentation bonus), R-03 (fiber ceiling)
3. `signal_extractor.py` + `score_engine.py`: R-04 (dairy sugar relief)
4. Re-run BSIP2 on all scored categories
5. Update frontend JSON files with new scores
6. Update grade fields where they changed
7. QA: verify no grade regressions for products that should not improve

---

## What Must NOT Change

- NOVA4 cap (68) — ultra-processed products do not benefit from recalibration
- Sugar caps for products with added sugar — remains fully punitive
- Additive penalties — unchanged
- Trans fat veto — unchanged
- Confidence ceiling — unchanged
- Relative ranking within each category — preserve as much as possible
