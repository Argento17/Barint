# Bari Intelligence — Milk & Alternatives
## Executive Summary (run_003)

**Run date:** 2026-05-18  
**Category:** Milk & Dairy Alternatives  
**Corpus:** 20 products — Yohananof real retailer scrape  
**Architecture version:** BSIP2 proto_v0 + Fix 1 (beverage gate) + Fix 2 (SE threshold)  

---

## Key Findings

### The hierarchy that emerged

Bari's scoring engine independently reproduced a hierarchy that aligns with
nutritional science consensus, without being hand-tuned to match it:

| Tier | Products | Score Range |
|------|----------|-------------|
| **B — Whole dairy** | Full-fat, natural, and goat milks | 73–75 |
| **C — Enriched dairy / plain soy** | Protein-enriched milks; plain soy drink | 56–66 |
| **D — Plant milk alternatives** | Oat, almond, rice, barista variants | 43–51 |
| **E — Engineered protein/chocolate** | Go Milk protein shake, chocolate soy | 36–40 |

No product in this category earns an A. The ceiling is structural: milks and
alternatives are dilute liquids — NOVA class, calorie density, and protein
concentration all converge to limit scores below the A threshold.

---

### Strongest products

- **חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן** (7290000051352) — 75 [B] 
- **חלב טבעי 4% 1 ליטר** (7290019790259) — 75 [B] 
- **חלב עיזים בקרטון 1 ליטר** (7290102392094) — 75 [B] 
- **חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר** (7290114313865) — 73.2 [B] 
- **משקה סויה ללא סוכרים 1 ליטר** (7290116936116) — 66.1 [C] 

The three whole milks (full-fat, natural, goat) share the B-tier floor at 75.
This is the NOVA 1 single-ingredient floor — not a ceiling. It reflects their
structural identity as minimally processed whole foods.

---

### Weakest products

- **אלפרו שקדים ללא סוכר** (5411188112709) — 43.4 [D]
- **משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ"ל** (7290110324773) — 39.5 [E]
- **אלפרו שוקו משקה סויה** (5411188300328) — 36.2 [E]

The E-tier is dominated by:
- **Go Milk** (engineered protein shake, NOVA 4, heavily fortified — Bari penalizes formulation complexity)
- **Alpro Soy Chocolate** (added sugar, NOVA 4, flavored)
- **Alpro Almond unsweetened** (very dilute, NOVA 4, ultra-low kcal relative to processing level)

---

### Architectural findings

**Finding 1: NOVA is the dominant driver in this category.**
Every NOVA 1 dairy product lands at B. Every NOVA 4 engineered product lands at D–E.
NOVA 2–3 products cluster in C–D depending on protein and enrichment level.

**Finding 2: Plant milk calorie density is structurally mismatched with the scoring model.**
Almond milk at 15 kcal/100g correctly looks 'excellent' on calorie density,
but it contributes almost no protein or fiber. Satiety support near zero.
The score reflects this tension: moderate calorie density score, very low nutrient density.

**Finding 3: The soy premium is real and architecturally earned.**
Plain soy drink (NOVA 2, 3.4g protein) scores C (66), well above oat (D, 50).
The gap is protein — soy is the only plant milk that meaningfully contributes protein.

---

### What surprised Bari

- **Alpro Soy Barista** (500ml) scores lower than plain soy drink (1L same brand)
  despite being marketed as premium. Reason: NOVA 4 due to acidity regulator — a
  single additive drops the processing classification entirely.

- **The two Oatly barista variants** score identically (48.8). Bari correctly refuses
  to distinguish marketing variants from identical formulas.

- **Go Milk protein shake** (39.5 E) scores *lower* than plain almond milk (43.4 D)
  despite having 27g protein per serving. On a per-100g basis, the engineering
  complexity, NOVA 4 cap, and sweet flavor system all fire — the protein signal
  cannot overcome the architecture penalties.

---

### What consumers misunderstand about this category

1. **'Plant milk is healthier than dairy.'** Not according to Bari. Whole cow's milk
   (NOVA 1, 3.4g protein, real fat) scores B. Oat milk (NOVA 3, 1.5g protein, seed
   oil added) scores D. The 'health halo' around plant milks is not supported by
   structural food quality analysis.

2. **'Unsweetened means clean.'** Alpro Almond Unsweetened still contains stabilizers,
   emulsifiers, and synthetic flavoring — earning NOVA 4 despite having no added sugar.
   The 'unsweetened' claim is accurate but incomplete.

3. **'More protein = better.'** Go Milk's 27g protein score comes with heavy fortification,
   sweeteners, and complex flavoring. Bari evaluates the whole matrix — not just one signal.

4. **'Organic means less processed.'** The two Vitariz organic rice/coconut drinks
   score 48.5 and 47.2 (D). Organic certification does not address NOVA processing level
   or additive complexity.
