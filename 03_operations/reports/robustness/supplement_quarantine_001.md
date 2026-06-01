# Supplement Quarantine — Protein Supplement Detection v1

Generated: 2026-05-25

## Background

BSIP2 currently has no `protein_supplement` category. When protein powders
or meal replacements enter the corpus, their whey ('מי גבינה') and casein
('קזאין') signals route them into `dairy_protein`. This is a category leakage
failure — they are not dairy products, and the dairy scoring model does not
apply to them.

The quarantine approach: detect supplement candidates as an **additive field**
(`supplement_quarantine` in the routing result) without changing the routing
category. Instead, suppress confidence and force UNCERTAINTY degradation.
This surfaces the problem to the analyst without corrupting the scoring pipeline.

---

## Detection Logic

### Name signals (exact substring match):
- `אבקת חלבון` (protein powder)
- `שייק חלבון` (protein shake)
- `תחליף ארוחה` (meal replacement)
- `חלבון ספורט` (sport protein)
- `אבקת מי גבינה` (whey powder)

### Ingredient composition signals:
- Whey terms: `מי גבינה`, `חלבון מי גבינה`, `קזאין`
- Combined with: maltodextrin (`מלתודקסטרין`) or sport name terms
  (`ספורט`, `שייק`, `אבקת`, `פרוטאין`)

### Confidence penalty:
- `supplement_candidate` → **-22** in `interpretation_confidence`

### Degradation rule:
- If supplement detected AND band is very_high or high → **UNCERTAINTY**
- If supplement detected AND band is moderate or low → **INSUFFICIENT**

---

## Quarantine Results — All Detected Cases

| ID | Name | Quarantine Signal | Routed As | Band | Degradation | Score |
|:---|:-----|:-----------------|:----------|:-----|:------------|:------|
| G3 | אבקת חלבון ספורט וניל | name:'אבקת חלבון' | dairy_protein | low | Insufficient | 65.0 |
| G4 | שייק חלבון תחליף ארוחה | name:'שייק חלבון' | dairy_protein | insufficient_context | Insufficient | 40.0 |
| H4 | אבקת שייק חלבון שוקולד | name:'שייק חלבון' | snack_bar_granola | moderate | Insufficient | 70.0 |

---

## Detailed Case Studies

### G3 — אבקת חלבון ספורט וניל

**Noise scenarios:** consistency:kcal_outside_plausible_range
**Test purpose:** 1800 kcal/100g is outside plausible solid food range (700 ceiling). kcal_plausible check should fire

**Quarantine detection:** {'signal': "name:'אבקת חלבון'", 'category': 'protein_supplement_candidate'}

**Routing:**
- Assigned category: `dairy_protein` (conf=0.92)
- Secondary: `whole_food_fat` (sec_conf=0.10)
- Anchor override: False
- Is supplement candidate (interp_conf): True

**Confidence:**
- Base: 75.0 (medium)
- Interpretation: 43.0 (low)

**Degradation:** INSUFFICIENT
**Score:** 65.0 → presented=None

**Deductions from supplement detection:**
- `kcal_implausible_extra: kcal=1800 vs macros_implied=513`: -10
- `supplement_candidate: protein_supplement_candidate outside current food ontology`: -22

**Interpretation narrative:**
> הציון הוא הערכה זהירה בלבד. ערך הקלוריות אינו עולה בקנה אחד עם המאקרונוטריאנטים — ייתכן שגיאת נתונים; המוצר עשוי להיות תוסף חלבון / תחליף ארוחה — מחוץ לאונטולוגיה הנוכחית, ציון אינדיקטיבי בלבד. מומלץ לאמת את הנתונים לפני הסקת מסקנות.

---

### G4 — שייק חלבון תחליף ארוחה

**Noise scenarios:** consistency:multiple_failures
**Test purpose:** Multiple simultaneous consistency failures. System should reach INSUFFICIENT or very low confidence

**Quarantine detection:** {'signal': "name:'שייק חלבון'", 'category': 'protein_supplement_candidate'}

**Routing:**
- Assigned category: `dairy_protein` (conf=0.92)
- Secondary: `whole_food_fat` (sec_conf=0.10)
- Anchor override: False
- Is supplement candidate (interp_conf): True

**Confidence:**
- Base: 35.0 (insufficient)
- Interpretation: 3.0 (insufficient_context)

**Degradation:** INSUFFICIENT
**Score:** 40.0 → presented=None

**Deductions from supplement detection:**
- `kcal_implausible_extra: kcal=600 vs macros_implied=245`: -10
- `supplement_candidate: protein_supplement_candidate outside current food ontology`: -22

**Interpretation narrative:**
> אין מספיק נתונים לניתוח מהימן. שגיאת עקביות: סוכר רשום גבוה מפחמימות — ייתכן שגיאת נתונים. לא מוצג ציון — נדרשים נתוני תזונה ורכיבים מלאים.

---

### H4 — אבקת שייק חלבון שוקולד

**Noise scenarios:** hybrid:protein_powder_category_gap
**Test purpose:** Protein powder — no specific category for this product type. Routes to snack_bar_granola by default; tests ONTOLOGY_GAP exposure

**Quarantine detection:** {'signal': "name:'שייק חלבון'", 'category': 'protein_supplement_candidate'}

**Routing:**
- Assigned category: `snack_bar_granola` (conf=0.66)
- Secondary: `dairy_protein` (sec_conf=0.29)
- Anchor override: False
- Is supplement candidate (interp_conf): True

**Confidence:**
- Base: 87.0 (high)
- Interpretation: 65.0 (moderate)

**Degradation:** INSUFFICIENT
**Score:** 70.0 → presented=None

**Deductions from supplement detection:**
- `supplement_candidate: protein_supplement_candidate outside current food ontology`: -22

**Interpretation narrative:**
> הניתוח שמיש אך כולל אי-ודאות. המוצר עשוי להיות תוסף חלבון / תחליף ארוחה — מחוץ לאונטולוגיה הנוכחית, ציון אינדיקטיבי בלבד.

---

## Known Limitations

1. **Detection is keyword-based** — novel supplement product names not in the signal list
   will pass through undetected.
2. **No dedicated scoring model** — detected supplements are still scored by whichever
   category the router assigned (usually dairy_protein). The score is marked as
   UNCERTAINTY-level and should not be used directly.
3. **Gap remains open** — a proper fix requires a `protein_supplement` category with
   its own scoring dimensions (protein_concentration, amino_acid_profile, etc.).
   This quarantine is a temporary safety net, not a solution.

---

*Report generated by run_calibration_patch.py — BSIP2 Calibration Patch v1*