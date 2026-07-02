# Protein Bar Sub-Lens — D6 Implementation Spec
# Task: TASK-365 | Status: APPROVED BY OWNER | Authored: Nutrition Agent 2026-06-21

---

## 0. Overview and Scope

This spec covers the `protein_bar` sub-lens — a dedicated scoring lens within the
`snack_bar_granola` category that applies to engineered protein bars, protein cookies, and
protein bites (owner-combined shelf). It is a **design spec only**. Data Agent implements
here, scores the corpus, and shows the owner the re-rank before any go-live.

**What changes:**
- `constants.py` — new token tables (polyol tiers, sweeteners, glycerol, protein sources)
  and `PROTEIN_BAR_WEIGHTS` re-weighting dict
- `router_v2.py` — subtype `protein_bar` routing broadened to cover bars + cookies + bites;
  the existing R1/R2 REQ-362 rules already emit `protein_bar`; the new anchors add direct
  detection for cookie/bite name tokens
- `score_engine.py` — one new `is_protein_bar` branch in the active_weights selector;
  new axis signals fire inside `evaluate_guardrails` / per-dimension scoring on that branch

**What does NOT change:**
- The base BSIP2 dimension scoring functions
- Existing caps for non-protein-bar products
- Any live category (all changes are gated to `category == "snack_bar_granola"` AND
  `category_subtype == "protein_bar"`)
- Any published score (this spec is pre-implementation)

---

## 1. Router Wiring (router_v2.py)

### 1.1 New Hard Anchors

Insert the following in `HARD_ANCHORS` **before** the generic `("גרנולה", "snack_bar_granola", "granola", 0.90)` entry (longer/more-specific first):

```python
# ── Protein bars / cookies / bites (TASK-365) ──────────────────────────────
# These anchor on explicit protein identity in the product NAME only —
# ingredient text is NOT consulted (avoids false positives on granola bars
# that happen to contain whey as a minor ingredient).
("חטיף חלבון",      "snack_bar_granola", "protein_bar",    0.93),
("בר חלבון",        "snack_bar_granola", "protein_bar",    0.93),
("עוגיות חלבון",    "snack_bar_granola", "protein_bar",    0.92),
("עוגיית חלבון",    "snack_bar_granola", "protein_bar",    0.92),
("ביס חלבון",       "snack_bar_granola", "protein_bar",    0.91),
("כדורי חלבון",     "snack_bar_granola", "protein_bar",    0.91),
("פרוטאין בר",      "snack_bar_granola", "protein_bar",    0.93),
("protein bar",     "snack_bar_granola", "protein_bar",    0.92),
```

### 1.2 Anchor Exclusions

Add to `ANCHOR_EXCLUSIONS`:
```python
"חטיף חלבון":   [],     # no exclusions; specificity is the guard
"בר חלבון":     [],
"עוגיות חלבון": [],
"עוגיית חלבון": [],
"ביס חלבון":    [],
"כדורי חלבון":  [],
"פרוטאין בר":   [],
"protein bar":   [],
```

### 1.3 Existing REQ-362 Rules (Unchanged)

**Rule 1** (cracker → snack_bar_granola via `חלבון`/`פרוטאין`/`protein` in name):
Sets `category_subtype = "protein_bar"` — already correct. No change.

**Rule 2** (whole_food_fat → snack_bar_granola via protein_g ≥ 20 AND ingredients ≥ 15):
Sets `category_subtype = "protein_bar"` — already correct. No change.

### 1.4 Subtype Vocabulary

The router emits `category_subtype = "protein_bar"` for all products caught by anchors 1.1,
REQ-362 R1, and REQ-362 R2. The scoring lens activates on this subtype.

---

## 2. Token Detection Tables (constants.py)

All tables below are used by signal_extractor.py / score_engine.py to detect ingredients.
Detection is always against the P2-normalized Hebrew ingredient text (lowercased, Hebrew
final-letter normalized). For each category, **any** match in the list fires the signal.

---

### 2.1 Polyols by Tier

Penalty logic: the **worst tier present** in a product's ingredient list applies (not stacked
per polyol). A product with both מלטיטול (Tier 1) and אריתריטול (Tier 3) scores at Tier 1.

```python
# TASK-365 / EV-PBAR-001 — Polyol tier detection vocabulary.
# Tier 1 = worst penalty (highest glycemic impact / gut fermentation burden)
# Tier 3 = lightest penalty (minimal glycemic impact, well-tolerated at label doses)
# Source: Livesey 2003 (glycemic impact polyols); EV-PBAR-001 summary.

POLYOL_TIER_1_TOKENS = (
    # Maltitol — GI ~35 vs sucrose 65; causes near-identical glucose response to table
    # sugar at typical bar doses (20–30 g serving); the primary deceptive sugar-free claim.
    # Evidence tier: STRONG (Livesey systematic review, glycemic-response studies).
    "מלטיטול",
    "מלטיטול סירופ",
    "סירופ מלטיטול",
    "maltitol",
    "maltitol syrup",
    "E965",
    "e965",
)

POLYOL_TIER_2_TOKENS = (
    # Sorbitol — GI ~9; causes osmotic diarrhoea at >10 g; common in older sugar-free bars.
    # Isomalt — GI ~2–9; osmotic diarrhoea risk at >20 g/d; better than maltitol but
    # still industrial sugar-alcohol substitution.
    # Evidence tier: STRONG for GI effect; MODERATE for GI magnitude vs maltitol.
    "סורביטול",
    "sorbitol",
    "E420",
    "e420",
    "איזומלט",
    "isomalt",
    "E953",
    "e953",
    # Lactitol — GI ~2; osmotic effects; rarer in Israeli bar market.
    "לקטיטול",
    "lactitol",
    "E966",
    "e966",
    # Mannitol — GI ~0 but highest osmotic-laxative risk per gram; used as anti-caking.
    "מניטול",
    "mannitol",
    "E421",
    "e421",
)

POLYOL_TIER_3_TOKENS = (
    # Erythritol — GI ~0; not fermented in colon (excreted unchanged); best-tolerated
    # polyol in systematic evidence; physiologically the least concerning.
    # Evidence tier: STRONG.
    "אריתריטול",
    "erythritol",
    "E968",
    "e968",
    # Xylitol — GI ~7; well-tolerated at label doses (~5–15 g/serving in bars); dental
    # caries benefit. Concerning only at doses >40–50 g/d (EFSA Opinion 2007).
    # Evidence tier: STRONG for dental; MODERATE for GI tolerance at bar doses.
    "קסיליטול",
    "xylitol",
    "E967",
    "e967",
)
```

**Penalty magnitudes** (see Section 3 for how these feed the scoring axis):
```python
POLYOL_TIER_1_PENALTY = 18   # maltitol / sorbitol / isomalt (EV-PBAR-001)
POLYOL_TIER_2_PENALTY = 12   # sorbitol, isomalt, mannitol, lactitol
POLYOL_TIER_3_PENALTY =  5   # erythritol, xylitol
```

Evidence rationale: maltitol tier-1 penalty magnitude (18 pts) is calibrated to ensure
a maltitol bar scores materially below an erythritol bar with identical other signals,
and below a real-sugar bar at comparable total-sweetness load. A bar at 35 g/100g maltitol
should score similarly to a bar at ~25 g/100g sucrose in glycemic impact, hence the penalty
spans the same weight zone as the existing `SNACK_BAR_RED_SUGAR_LABEL` cap (55 floor).
Tier-3 erythritol penalty (5 pts) acknowledges that the substitution is genuine but still
represents industrial texture engineering over whole-food matrix. Evidence tier for penalty
magnitudes: MODERATE (no RCT specifically calibrated to bar-format glycemic response — the
calibration is derived from GI literature applied to typical Israeli bar nutritional panels).

---

### 2.2 Artificial Sweeteners

```python
# TASK-365 / EV-PBAR-002 — Artificial sweetener detection for protein_bar lens.
# Existing SWEETENER_CAP_C (=70) and SWEETENER_PENALTY_C (=15) already fire on these
# tokens via the existing signal_extractor sweetener path. These tokens are NOT duplicated
# for scoring — the table below is provided for copy/trace transparency only and to document
# the complete set the Data Agent should verify is covered by signal_extractor.py.
# NO new code is needed; the existing sweetener detection handles this.

ARTIFICIAL_SWEETENER_TOKENS_REFERENCE = (
    # Sucralose
    "סוכרלוז", "sucralose", "E955", "e955",
    # Acesulfame-K
    "אצסולפאם", "אצסולפם", "acesulfame", "אצסולפאם k", "אצסולפאם K", "E950", "e950",
    # Saccharin
    "סכרין", "saccharin", "E954", "e954",
    # Aspartame
    "אספרטם", "aspartame", "E951", "e951",
    # Neotame
    "נאוטם", "neotame", "E961", "e961",
    # Cyclamate
    "ציקלמט", "cyclamate", "E952", "e952",
    # Steviol glycosides — already Tier A in existing sweetener path (SWEETENER_CAP_A=75)
    # Stevia is not an artificial sweetener in the pharmacological sense; it sits correctly
    # at Tier A (lighter penalty) in the existing sweetener taxonomy.
    # "סטיביה", "stevia", "סטיביול גליקוזידים", "E960" → handled as Tier A, NOT re-penalized here.
    # Monk fruit — not yet seen on Israeli protein bar labels; no token needed.
)
```

**Cap/penalty for protein_bar lens:**
Existing `SWEETENER_CAP_C = 70` and `SWEETENER_PENALTY_C = 15` apply. No change to
magnitude. The cap is an OVERRIDE CAP (final score ≤ 70) on ANY product where a Tier-C
sweetener is detected, regardless of other signals. This is correct behavior for the
protein_bar lens and should not be relaxed or modified. The rationale: a bar achieving a
score above 70/B by combining an excellent sugar profile with a Tier-C sweetener would be
giving the product credit for low sugar it only achieves by substituting the worst class of
artificial sweetener — a judgment BEV-014 rule prohibits.

---

### 2.3 Glycerol / Humectant (New Signal)

```python
# TASK-365 / EV-PBAR-003 — Glycerol detection as engineering-depth signal.
# Glycerol (glycerin / E422) is used in protein bars as a humectant to create
# "soft" or "moist" texture without water — it is a hallmark of industrial matrix
# reconstruction. At typical bar doses (5–15 g/serving) it provides ~4.32 kcal/g
# (Calorie Control Council) but is often NOT declared in the nutrition panel as a sugar
# or as fiber, creating a labeling opacity. Israeli labels declare it as "גליצרול",
# "גליצרין", or E422. Detection in ingredient text (not name-only) is appropriate
# since glycerol is never part of a product identity claim.
# Evidence tier: STRONG for detection as engineering marker; MODERATE for magnitude.

GLYCEROL_TOKENS = (
    "גליצרול",
    "גליצרין",
    "glycerol",
    "glycerin",
    "E422",
    "e422",
)

# Penalty magnitude — see Axis 2 (Engineering Depth) in Section 3.
GLYCEROL_ENGINEERING_PENALTY = 8   # EV-PBAR-003
```

---

### 2.4 Protein Source Classification

```python
# TASK-365 / EV-PBAR-004 — Protein source tokens for the protein_bar lens.
# Axis 3: whole-food protein source (credit) vs isolate/concentrate (matrix integrity
# penalty). This is NOT a DIAAS/protein-quality judgment — DIAAS is not
# label-derivable (KB-004). This axis measures MATRIX INTEGRITY: whether the protein
# is structurally embedded in the food matrix (whole-food) or reconstructed
# (extracted/processed). Mirrors the reasoning in PROTEIN_QUALITY_MATRIX_DISCOUNT
# (TASK-222B) but applied at the axis weight level, not as a discount coefficient.

# --- Isolate / Concentrate tokens (engineering markers, NOVA-driving) ---
# These tokens identify extracted protein sources. Their presence increases engineering
# depth. Any ONE of these in the ingredient list identifies the product as
# isolate-dominant (for Axis 3 scoring).

PROTEIN_ISOLATE_TOKENS = (
    # Whey variants
    "חלבון מי גבינה מבודד",     # WPI — most common on Israeli bars
    "חלבון מי גבינה מרוכז",     # WPC
    "חלבון מי גבינה",           # generic whey (covers both)
    "מי גבינה",                 # whey general
    "וויי",                     # transliteration "whey"
    "WPI", "wpi",
    "WPC", "wpc",
    "whey protein isolate",
    "whey protein concentrate",
    "whey protein",
    # Casein
    "קזאין",
    "casein",
    "micellar casein",          # rare but appears in imported products
    # Soy protein isolate / concentrate
    "חלבון סויה מבודד",
    "חלבון סויה מרוכז",
    "חלבון סויה",
    "soy protein isolate",
    "soy protein concentrate",
    # Pea protein isolate / concentrate
    "חלבון אפונה",
    "pea protein",
    # Rice protein
    "חלבון אורז",
    "rice protein",
    # Collagen / gelatin (the structurally lowest-quality protein source)
    "קולגן",
    "collagen",
    "ג'לטין", "ג׳לטין",
    "gelatin",
    # Wheat protein / gluten isolate
    "חלבון חיטה",
    "גלוטן חיטה",
    "wheat protein",
    "wheat gluten",
    "vital wheat gluten",
)

# --- Whole-food protein source tokens (structural credit) ---
# These tokens identify protein embedded in an intact whole-food matrix.
# The PROTEIN IS A CONSEQUENCE of whole-food inclusion, not the designed-in goal.
# Presence of any ONE whole-food source AND absence of isolate-stacking (3+ distinct
# isolate sources) earns the whole-food protein credit.

PROTEIN_WHOLEFOOD_TOKENS = (
    # Nuts and nut butters
    "אגוזי לוז", "לוז",
    "שקדים", "שקד",
    "בוטנים", "בוטן",
    "אגוזי מקדמיה",
    "קשיו",
    "פיסטוקים",
    "אגוזי מלך", "אגוזים",
    "חמאת בוטנים",
    "חמאת שקדים",
    "חמאת קשיו",
    "חמאת אגוזים",
    # Seeds
    "גרעיני דלעת",
    "גרעיני חמנייה",
    "זרעי צ'יה", "צ'יה",
    "זרעי פשתן", "פשתן",
    "שומשום",
    # Legumes
    "עדשים",
    "חומוס",         # chickpea (whole)
    "פולי סויה",     # whole soy beans (distinct from soy protein isolate)
    # Dates and whole dried fruit (protein is incidental but matrix intact)
    "תמרים", "תמר",
    # Tahini (whole sesame paste, full matrix)
    "טחינה",
)
```

**Isolate-stacking definition:**
A product has "isolate-stacking" when it contains 3 or more DISTINCT tokens from
`PROTEIN_ISOLATE_TOKENS` matched to 3 different source families (whey family, casein,
soy, pea, rice, collagen, wheat each count as one family). This signal is the most extreme
form of matrix reconstruction.

```python
# TASK-365 / EV-PBAR-004b — Protein family grouping for isolate-stacking detection.
# A product with isolates from 3+ FAMILIES = isolate_stacking = True.
PROTEIN_ISOLATE_FAMILIES = {
    "whey":     ("חלבון מי גבינה מבודד", "חלבון מי גבינה מרוכז", "חלבון מי גבינה",
                 "מי גבינה", "וויי", "WPI", "wpi", "WPC", "wpc",
                 "whey protein isolate", "whey protein concentrate", "whey protein"),
    "casein":   ("קזאין", "casein", "micellar casein"),
    "soy":      ("חלבון סויה מבודד", "חלבון סויה מרוכז", "חלבון סויה",
                 "soy protein isolate", "soy protein concentrate"),
    "pea":      ("חלבון אפונה", "pea protein"),
    "rice":     ("חלבון אורז", "rice protein"),
    "collagen": ("קולגן", "collagen", "ג'לטין", "ג׳לטין", "gelatin"),
    "wheat":    ("חלבון חיטה", "גלוטן חיטה", "wheat protein", "wheat gluten",
                 "vital wheat gluten"),
}
ISOLATE_STACKING_FAMILY_THRESHOLD = 3   # 3+ distinct families = stacking signal
```

---

## 3. Axis Architecture and Dimension Weights

### 3.1 Axis Map

The protein_bar lens operates on the same 10 BSIP2 dimensions but re-weights them to
reflect what matters for this category. Four axes map onto the dimension weights:

| Axis | What it measures | Primary dimension(s) |
|------|-----------------|----------------------|
| Protein quantity gate | Is there a credible protein source at all? | `protein_quality` (weight stays very low) |
| Axis 1: Sugar-reduction mechanism | Real-food displacement vs polyol vs artificial | `glycemic_quality`, `regulatory_quality` |
| Axis 2: Engineering depth | Glycerol, isolate-stacking, ingredient count | `processing_quality`, `whole_food_integrity` |
| Axis 3: Protein source matrix | Whole-food vs isolate | `protein_quality` (modestly elevated) |

### 3.2 Protein_Bar Weight Profile (PROTEIN_BAR_WEIGHTS)

```python
# TASK-365 / EV-PBAR-005 — protein_bar sub-lens dimension weights.
# Rationale for deltas vs base DIMENSION_WEIGHTS:
#   - glycemic_quality UP (0.12 → 0.17): the key differentiation axis for this shelf
#     is the sugar-reduction mechanism; this is where maltitol vs erythritol vs
#     real-food displacement lives.
#   - processing_quality DOWN (0.15 → 0.12): all protein bars are NOVA 4 (highly
#     processed by construction); the dimension gives no differentiation. Reducing
#     weight prevents a structural-equivalence floor from dominating the score.
#   - protein_quality UP (0.10 → 0.13): source integrity matters more here than
#     on a generic snack bar (where protein is not the category promise).
#   - whole_food_integrity UP (0.04 → 0.07): engineering-depth signals (glycerol,
#     isolate-stacking) land here; needs enough weight to move the score.
#   - calorie_density DOWN (0.15 → 0.11): protein bars are structurally calorie-dense
#     (350–450 kcal/100g is normal for the format); penalizing calorie density on this
#     shelf is compositionally misleading — the calorie-per-protein ratio is what
#     matters, and that is captured in nutrient_density.
#   - nutrient_density UNCHANGED (0.15): retains the protein + fiber density signal.
#   - additive_quality UNCHANGED (0.10): preserves the existing additive burden signal.
#   - satiety_support UNCHANGED (0.06): fiber + protein satiety already scores here.
#   - fat_quality UNCHANGED (0.08): sat fat, fat technology signals unchanged.
#   - regulatory_quality UP (0.05 → 0.07): red labels for sugar/sat_fat fire here;
#     given the category promise of "better", regulatory breach matters more.
# Sum check: 0.12+0.15+0.11+0.17+0.13+0.10+0.06+0.08+0.07+0.07 = 1.06 ← ERROR
# Corrected: reduce nutrient_density to 0.13 to sum to 1.00.
#   Corrected sum: 0.12+0.13+0.11+0.17+0.13+0.10+0.06+0.08+0.07+0.07 = 1.04 ← still off
# Final calibration (verified sum = 1.00):

PROTEIN_BAR_WEIGHTS = {
    "processing_quality":   0.12,   # DOWN from 0.15 — NOVA-4 structural floor; low differentiation
    "nutrient_density":     0.14,   # DOWN from 0.15 — marginal reduction; captures protein+fiber
    "calorie_density":      0.10,   # DOWN from 0.15 — format is structurally calorie-dense
    "glycemic_quality":     0.17,   # UP from 0.12 — primary axis: sugar-reduction mechanism
    "protein_quality":      0.13,   # UP from 0.10 — source integrity matters on this shelf
    "additive_quality":     0.10,   # UNCHANGED
    "satiety_support":      0.06,   # UNCHANGED
    "fat_quality":          0.08,   # UNCHANGED
    "regulatory_quality":   0.07,   # UP from 0.05 — red labels cut deeper on this shelf
    "whole_food_integrity": 0.03,   # DOWN from 0.04 — engineering-depth signals move here via AXIS 2
}
# Sum verification: 0.12+0.14+0.10+0.17+0.13+0.10+0.06+0.08+0.07+0.03 = 1.00 CONFIRMED
```

**NOTE ON WHOLE_FOOD_INTEGRITY WEIGHT (0.03):**
This weight appears to decrease the engineering-depth signal's impact, but the axis-2
signals (glycerol, isolate-stacking) are implemented as PENALTY DEDUCTIONS directly on
the `whole_food_integrity` raw dimension score, not as weight adjustments. At a weight of
0.03, a 20-point drop in `whole_food_integrity` (e.g. from 60 to 40) moves the composite
by 0.6 points — insufficient. Therefore, engineering-depth penalties are implemented as
**guardrail-family penalties** (not dimension weight penalties), specifically as new
members of the `PROCESSING_LOAD` family applied when `category_subtype == "protein_bar"`.
This is the same approach as `LONG_INGREDIENT_LIST` in `PROCESSING_CAPS`. See Section 4.

---

### 3.3 Protein Quantity Gate (Near-Zero Weight)

```python
# TASK-365 / EV-PBAR-006 — Credible protein source gate.
# The protein grams value is NOT a scoring axis for protein bars — it is a GATE only.
# A product on the protein_bar shelf with < PROTEIN_BAR_GATE_MIN_G protein per 100g
# is almost certainly a misrouted product (a candy bar, not a protein bar).
# The gate does NOT change the score; it sets a confidence flag used in the trace.
# Definition: "credible protein source" = protein_g >= 12 per 100g.
# Rationale: the Israeli market's bottom-of-shelf protein bars (e.g. cheaper impulse
# products) typically deliver 12–15g/100g; legitimate protein products start here.
# Anything below 12g/100g on this shelf is routing-suspicious.
# The gate does NOT cap the score; it emits a trace warning:
#   protein_bar_gate_result: "PASS" | "WARN_LOW_PROTEIN" | "FAIL_NOT_PROTEIN"

PROTEIN_BAR_GATE_MIN_G      = 12.0   # g/100g — below = "WARN_LOW_PROTEIN"
PROTEIN_BAR_GATE_REJECT_G   =  8.0   # g/100g — below = "FAIL_NOT_PROTEIN" (routing suspect)
```

The gate result is TRACE-ONLY. It does not modify the score. A `FAIL_NOT_PROTEIN` result
should prompt the Data Agent / QA Agent to verify whether the product was correctly routed.
The score engine does not auto-reject or cap based on the gate.

**Protein quantity weight in the lens:**
The weight on `protein_quality` is 0.13 (see above). The `protein_quality` dimension
score itself is computed by the existing `lookup_protein_scale()` function using the
`snack_bar_granola` curve (which already has a reasonable curve for bars). This provides
modest differentiation for protein density but does NOT make protein grams the primary
axis. A 20g-protein bar will outscore a 15g-protein bar only ~5 raw dimension points on
this curve, producing <0.65 composite point difference from this source alone — correctly
subordinate to the sugar-mechanism axis (weight 0.17 × potentially 20+ raw points = 3.4+
composite points).

---

## 4. Guardrail Caps and Penalties (New Protein Bar Family)

### 4.1 Axis 1 — Sugar-Reduction Mechanism Penalties

These slot into the **SUGAR_LOAD family** when `category_subtype == "protein_bar"`.
They are applied INSTEAD OF (not in addition to) the standard `SNACK_BAR_RED_SUGAR_LABEL`
cap for products where the sugar is low due to polyol substitution.

```python
# TASK-365 / EV-PBAR-001 — Polyol penalty guardrails for protein_bar sub-lens.
# Applied to SUGAR_LOAD family budget when category_subtype=="protein_bar".
# These fire when the product's sweetness reduction mechanism is identified as
# polyol substitution (the engineering-sweetness problem, not a genuine sugar reduction).

PROTEIN_BAR_POLYOL_CAPS = [
    # Tier 1 (maltitol): cap score at 62 — equivalent to a "slightly better than mediocre"
    # finding. Rationale: maltitol delivers ~GI 35 vs sucrose ~GI 65; the reduction is
    # real but the claim "sugar-free" is deeply misleading at the dose found in bars.
    # A product where maltitol is the primary sweetener should NOT reach grade B (70).
    # 62 = cap below grade B, above grade C floor (50).
    ("PROTEIN_BAR_MALTITOL_TIER1",    "protein_bar AND polyol_tier_1", 62),
    # Tier 2 (sorbitol/isomalt/mannitol/lactitol): cap at 66.
    # Better than maltitol but still industrial substitution with osmotic risk.
    ("PROTEIN_BAR_POLYOL_TIER2",      "protein_bar AND polyol_tier_2", 66),
    # Tier 3 (erythritol/xylitol): no score cap. These polyols are genuinely
    # low-concern at label doses. A penalty applies (see PENALTIES below)
    # but no hard ceiling — a well-formulated erythritol bar can reach grade A.
    # No cap entry for Tier 3.
]

PROTEIN_BAR_POLYOL_PENALTIES = [
    # Tier 3 penalty — confirms engineering substitution even for well-tolerated polyols.
    ("PROTEIN_BAR_POLYOL_TIER3",      "protein_bar AND polyol_tier_3", 5),
]
```

**Real-food displacement credit:**
When a protein bar achieves low sugar WITHOUT any polyol or artificial sweetener — i.e., the
low sugar is a consequence of whole-food ingredient selection (nuts, seeds, dates as the
sweetener), grant a `GLYCEMIC_QUALITY` bonus:

```python
PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS = 5   # EV-PBAR-007
# Condition: protein_bar AND sugar_g <= 10 AND no polyol_any AND no artificial_sweetener
# Applied as a positive adjustment to the glycemic_quality raw dimension score (pre-weighting).
# Cap: cannot push glycemic_quality raw score above 95.
```

Evidence for bonus: strong (whole-food matrix inherently does not raise glycemic load
beyond what the ingredient FRAP + fiber already capture; the bonus rewards genuine
formulation restraint, not a substitution trick).

---

### 4.2 Axis 2 — Engineering Depth Penalties

These slot into the **PROCESSING_LOAD family** when `category_subtype == "protein_bar"`.

```python
# TASK-365 / EV-PBAR-003/004b — Engineering depth penalty guardrails.
# Glycerol and isolate-stacking are markers of matrix reconstruction depth.
# They belong to PROCESSING_LOAD family (same family as LONG_INGREDIENT_LIST).

PROTEIN_BAR_ENGINEERING_PENALTIES = [
    # Glycerol presence: the single most reliable marker of industrial bar matrix
    # engineering on the Israeli shelf. Per EV-PBAR-003.
    ("PROTEIN_BAR_GLYCEROL",          "protein_bar AND glycerol_detected",     8),
    # Isolate stacking: 3+ distinct isolate families amplifies the engineering signal.
    # An additional penalty on top of glycerol (stacking is the worst form of reconstruction).
    ("PROTEIN_BAR_ISOLATE_STACKING",  "protein_bar AND isolate_stacking",      6),
    # Ingredient count penalty (existing LONG_INGREDIENT_LIST already fires at >12;
    # for protein bars, add an additional tier for very long lists).
    ("PROTEIN_BAR_VERY_LONG_LIST",    "protein_bar AND ingredients>20",        4),
]

# PROCESSING_LOAD family budget for protein_bar:
# Base PROCESSING_FAMILY_BUDGET = 12. The new protein-bar penalties can stack with the
# existing LONG_INGREDIENT_LIST (4 pts) and NOVA_PROXY_4_ULTRA_PROCESSED cap.
# To prevent over-stacking, apply the engineering penalties within the existing
# PROCESSING_FAMILY_BUDGET = 12 (shared budget — these count toward the 12-point cap).
# In practice: glycerol(8) + isolate_stacking(6) + very_long_list(4) = 18 gross,
# capped at 12. A product with all three still lands at the PROCESSING_FAMILY_BUDGET cap.
```

---

### 4.3 Axis 3 — Protein Source (Dimension Weight Signal)

Axis 3 does NOT use guardrail caps. It operates through the `protein_quality` dimension
score adjustment, applied as a pre-weighting modifier:

```python
# TASK-365 / EV-PBAR-004 — Protein source modifier for protein_bar lens.
# Applied to protein_quality RAW DIMENSION SCORE before weighting.

PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS = 8   # whole-food protein source detected
PROTEIN_BAR_COLLAGEN_PENALTY       = 12  # collagen/gelatin = structural protein-quality fraud
                                          # (already partially handled by PROTEIN_QUALITY_MATRIX_DISCOUNT
                                          # at 0.55 coefficient; this adds a separate signal)

# Condition for WHOLEFOOD_SOURCE_BONUS:
# protein_bar AND any(PROTEIN_WHOLEFOOD_TOKENS in ingredients) AND NOT isolate_stacking
#
# Condition for COLLAGEN_PENALTY:
# protein_bar AND "קולגן" OR "collagen" OR "ג'לטין" OR "gelatin" in ingredients
# NOTE: collagen penalty should NOT stack with PROTEIN_QUALITY_MATRIX_DISCOUNT collagen=0.55.
# The existing discount and this penalty must be coordinated — use ONE, not both.
# COORDINATION RULE: if BARI_RECAL_P0 is ON (PROTEIN_QUALITY_MATRIX_DISCOUNT active),
# do NOT apply PROTEIN_BAR_COLLAGEN_PENALTY separately (it is subsumed by the discount).
# If BARI_RECAL_P0 is OFF, apply PROTEIN_BAR_COLLAGEN_PENALTY as a flat deduction.
```

---

### 4.4 Existing Artificial Sweetener Cap (Unchanged)

`SWEETENER_CAP_C = 70` — the existing cap applies unchanged to protein bars. No protein
bar with a Tier-C synthetic sweetener can score above 70. This is the correct behavior.
Do NOT add a separate protein-bar sweetener cap.

The existing `SWEETENER_PENALTY_C = 15` also applies. On the protein_bar lens, both the
penalty and the cap fire. This produces the expected hierarchy:
artificial sweetener bar (≤70) < maltitol bar (≤62) — WAIT, this is an ordering problem.

**ORDERING CORRECTION:** The artificial sweetener cap (70) is HIGHER than the maltitol
cap (62). This means a maltitol bar scores worse than an artificial-sweetener bar on the
cap alone, which is correct: maltitol's deceptive "sugar-free" claim (with GI ~35) is a
worse nutritional outcome than sucralose's genuine calorie/glycemic absence, despite
sucralose's other concerns. The cap hierarchy correctly encodes: erythritol/xylitol
(no cap) > artificial sweetener (cap 70) > isomalt/sorbitol (cap 66) > maltitol (cap 62).

This ordering is INTENTIONAL. Sucralose at cap 70 remains grade C; maltitol at cap 62 is
also grade C. The ordering reflects the MECHANISM ranking, not a general endorsement of
artificial sweeteners.

---

### 4.5 Calorie Density Table for Protein Bars

Add a `protein_bar` entry to `CALORIE_DENSITY_TABLES`. Protein bars are structurally
calorie-dense (350–480 kcal/100g is format-normal; they are not analogous to granola bars
at the low end):

```python
# TASK-365 / EV-PBAR-008 — Calorie density table for protein_bar sub-lens.
# Calibration reference: Israeli protein bar corpus typical range 350–450 kcal/100g.
# A bar at 350 kcal/100g should not be penalized relative to its category peers.
# Existing snack_bar_granola table penalizes 350 kcal at score=55 — too harsh for
# a protein-dense bar (protein is calorie-dense at 4 kcal/g; 30g protein/100g adds
# ~120 kcal that does not indicate poor formulation).

"protein_bar": [(250,90),(320,80),(380,72),(430,62),(480,50),(540,38),(1e9,20)],
```

The `cd_table_key` selector in score_engine.py (around line 3364) already handles
`category_subtype == "yogurt"` → `cd_table_key = "yogurt"`. Add the parallel:
```python
if cat_result.get("category_subtype") == "protein_bar":
    cd_table_key = "protein_bar"
```

---

## 5. Per-Bar Protein Framing Rule

This is a display spec, not a scoring spec. Passed to the frontend JSON as a flag.

```python
# TASK-365 — Per-bar protein display rule.
# Primary display: per-100g (all scoring is per-100g; this is non-negotiable for
# score comparability across bar sizes).
# Secondary display: per-bar (package weight ÷ 100 × nutrient per-100g).
# Condition for showing per-bar: product.package_weight_g is not None AND
#   product.package_weight_g is between 30 and 120 g (single-serve bar range).
# Outside that range, per-bar is misleading (mini-bites at 10g each, or twin-packs
# declared at total weight 120g).

PROTEIN_BAR_DISPLAY_PER_BAR_MIN_G  = 30    # g — minimum package weight for per-bar display
PROTEIN_BAR_DISPLAY_PER_BAR_MAX_G  = 120   # g — maximum package weight for per-bar display
```

Implementation: the frontend JSON generator (build_*_frontend.py) should compute and emit:
- `protein_per_100g` (always)
- `protein_per_bar` = round(protein_g * package_weight_g / 100, 1) when in-range
- `bar_weight_g` = package_weight_g (for display context)
- `show_per_bar` = True when in-range

These fields are emitted in the BSIP0/BSIP1 enrichment pass, not in the score engine.

---

## 6. Score_Engine Wiring (score_engine.py)

### 6.1 Active Weights Selector

In score_engine.py, add `PROTEIN_BAR_WEIGHTS` to the imports from constants.py and add
this branch in the `active_weights` selector block (around line 3461–3470):

```python
# Imports (add to the constants import block at top of score_engine.py):
from constants import (
    ...
    PROTEIN_BAR_WEIGHTS,          # TASK-365
    PROTEIN_BAR_GATE_MIN_G,       # TASK-365
    PROTEIN_BAR_GATE_REJECT_G,    # TASK-365
    POLYOL_TIER_1_TOKENS, POLYOL_TIER_2_TOKENS, POLYOL_TIER_3_TOKENS,
    POLYOL_TIER_1_PENALTY, POLYOL_TIER_2_PENALTY, POLYOL_TIER_3_PENALTY,
    GLYCEROL_TOKENS, GLYCEROL_ENGINEERING_PENALTY,
    PROTEIN_ISOLATE_FAMILIES, ISOLATE_STACKING_FAMILY_THRESHOLD,
    PROTEIN_WHOLEFOOD_TOKENS,
    PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS, PROTEIN_BAR_COLLAGEN_PENALTY,
    PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS,
    PROTEIN_BAR_POLYOL_CAPS, PROTEIN_BAR_POLYOL_PENALTIES,
    PROTEIN_BAR_ENGINEERING_PENALTIES,
    ...
)
```

Active weights selector (add BEFORE the `is_veg_spread` / `is_dairy_protein_reweight` block):
```python
is_protein_bar = (
    category == "snack_bar_granola"
    and cat_result.get("category_subtype") == "protein_bar"
)
if is_protein_bar:
    active_weights = PROTEIN_BAR_WEIGHTS
elif is_dairy_protein_reweight:
    active_weights = DAIRY_PROTEIN_WEIGHTS
elif is_veg_spread:
    active_weights = VEG_SPREAD_WEIGHTS
else:
    active_weights = DIMENSION_WEIGHTS
```

### 6.2 Protein Bar Signal Detection (New Helper Function)

Add a helper function `_detect_protein_bar_signals(l3, nn)` that returns a dict of
signals to be used by the guardrail and dimension adjusters:

```python
def _detect_protein_bar_signals(l3: dict, nn: dict) -> dict:
    """Detect protein_bar-specific signals from the Level-3 extract and nutrition.
    Returns a signals dict consumed by the protein_bar scoring path.
    """
    ing_text = " ".join(l3.get("ingredient_list") or []).lower()
    protein_g = (nn.get("protein_g") or 0)

    # Polyol tier detection (worst tier wins)
    polyol_tier = None
    for tok in POLYOL_TIER_1_TOKENS:
        if tok.lower() in ing_text:
            polyol_tier = 1
            break
    if polyol_tier is None:
        for tok in POLYOL_TIER_2_TOKENS:
            if tok.lower() in ing_text:
                polyol_tier = 2
                break
    if polyol_tier is None:
        for tok in POLYOL_TIER_3_TOKENS:
            if tok.lower() in ing_text:
                polyol_tier = 3
                break

    # Glycerol detection
    glycerol_detected = any(tok.lower() in ing_text for tok in GLYCEROL_TOKENS)

    # Isolate stacking detection
    families_detected = set()
    for family, tokens in PROTEIN_ISOLATE_FAMILIES.items():
        if any(tok.lower() in ing_text for tok in tokens):
            families_detected.add(family)
    isolate_stacking = len(families_detected) >= ISOLATE_STACKING_FAMILY_THRESHOLD
    isolate_families_count = len(families_detected)

    # Whole-food protein source
    wholefood_protein_detected = any(
        tok.lower() in ing_text for tok in PROTEIN_WHOLEFOOD_TOKENS
    )
    # Collagen detected (for penalty coordination)
    collagen_detected = any(
        tok.lower() in ing_text for tok in ("קולגן", "collagen", "ג'לטין", "ג׳לטין", "gelatin")
    )

    # Protein gate
    if protein_g >= PROTEIN_BAR_GATE_MIN_G:
        protein_gate = "PASS"
    elif protein_g >= PROTEIN_BAR_GATE_REJECT_G:
        protein_gate = "WARN_LOW_PROTEIN"
    else:
        protein_gate = "FAIL_NOT_PROTEIN"

    # Artificial sweetener (already detected upstream in l3; read from there)
    has_artificial_sweetener = l3.get("sweetener_tier") in ("C",)  # existing taxonomy

    # Real-food sugar bonus condition
    sugar_g = nn.get("sugars_g") or nn.get("sugar_g") or 0
    real_food_sugar_bonus_eligible = (
        sugar_g <= 10.0
        and polyol_tier is None
        and not has_artificial_sweetener
    )

    return {
        "polyol_tier": polyol_tier,                   # 1/2/3/None
        "glycerol_detected": glycerol_detected,
        "isolate_stacking": isolate_stacking,
        "isolate_families_count": isolate_families_count,
        "families_detected": sorted(families_detected),
        "wholefood_protein_detected": wholefood_protein_detected,
        "collagen_detected": collagen_detected,
        "protein_gate": protein_gate,
        "protein_g": protein_g,
        "real_food_sugar_bonus_eligible": real_food_sugar_bonus_eligible,
        "has_artificial_sweetener": has_artificial_sweetener,
    }
```

### 6.3 Dimension Adjustments (Applied Pre-Weighting)

After the dimension score computations and before the weighted sum, when `is_protein_bar`:

```python
if is_protein_bar:
    pb_signals = _detect_protein_bar_signals(l3, nn)

    # Axis 1 — Real-food sugar bonus on glycemic_quality
    if pb_signals["real_food_sugar_bonus_eligible"]:
        _old_gq = dim_scores["glycemic_quality"]
        dim_scores["glycemic_quality"] = min(95, dim_scores["glycemic_quality"]
                                             + PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS)
        dim_notes["glycemic_quality"] += (
            f" [PBAR_REAL_FOOD_SUGAR_BONUS: +{PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS},"
            f" {_old_gq:.1f}→{dim_scores['glycemic_quality']:.1f}]"
        )

    # Axis 3 — Protein source modifier on protein_quality
    # TASK-365 NUTRITION RULING FIX (2026-06-21): collagen wins unconditionally.
    # The old `elif` was WRONG — it let a product with collagen + a wholefood token
    # skip the collagen penalty and receive the wholefood bonus instead.
    # CORRECT logic: collagen penalty fires FIRST (unconditionally when collagen detected);
    # wholefood bonus fires ONLY when collagen is NOT detected AND not isolate_stacking.
    if pb_signals["collagen_detected"]:
        # Collagen wins — check COND-2 branch
        if not RECAL_P0_ON:
            # Apply collagen penalty when PROTEIN_QUALITY_MATRIX_DISCOUNT is NOT active
            _old_prq = dim_scores["protein_quality"]
            dim_scores["protein_quality"] = max(0, dim_scores["protein_quality"]
                                                - PROTEIN_BAR_COLLAGEN_PENALTY)
            dim_notes["protein_quality"] += (
                f" [PBAR_COLLAGEN_PENALTY: -{PROTEIN_BAR_COLLAGEN_PENALTY},"
                f" {_old_prq:.1f}→{dim_scores['protein_quality']:.1f};"
                f" WHOLEFOOD_BONUS suppressed — collagen wins]"
            )
        else:
            # COND-2: discount is active — skip penalty to avoid double-count
            dim_notes["protein_quality"] += (
                " [PBAR_COLLAGEN_PENALTY: SKIPPED — RECAL_P0_ON=True;"
                " WHOLEFOOD_BONUS suppressed — collagen wins]"
            )
    elif pb_signals["wholefood_protein_detected"] and not pb_signals["isolate_stacking"]:
        # Wholefood bonus fires ONLY when collagen NOT detected
        _old_prq = dim_scores["protein_quality"]
        dim_scores["protein_quality"] = min(100, dim_scores["protein_quality"]
                                            + PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS)
        dim_notes["protein_quality"] += (
            f" [PBAR_WHOLEFOOD_SOURCE: +{PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS},"
            f" {_old_prq:.1f}→{dim_scores['protein_quality']:.1f}]"
        )

    # Emit protein bar signals to trace
    score_result["protein_bar_signals"] = pb_signals
```

### 6.4 Guardrail Application (evaluate_guardrails)

The polyol caps and engineering penalties are applied INSIDE `evaluate_guardrails()` when
`category_subtype == "protein_bar"`. Pass `pb_signals` into `evaluate_guardrails` as an
additional parameter (or compute them inside if preferred — both approaches are valid; Data
Agent to choose). The penalty conditions:

```
PROTEIN_BAR_MALTITOL_TIER1:   fires when pb_signals["polyol_tier"] == 1
PROTEIN_BAR_POLYOL_TIER2:     fires when pb_signals["polyol_tier"] == 2
PROTEIN_BAR_POLYOL_TIER3:     fires when pb_signals["polyol_tier"] == 3  (penalty only, no cap)
PROTEIN_BAR_GLYCEROL:         fires when pb_signals["glycerol_detected"] == True
PROTEIN_BAR_ISOLATE_STACKING: fires when pb_signals["isolate_stacking"] == True
PROTEIN_BAR_VERY_LONG_LIST:   fires when ingredient_count > 20
```

All engineering penalties (glycerol + isolate_stacking + very_long_list) count toward
the existing `PROCESSING_FAMILY_BUDGET = 12`. No new family budget needed.

Polyol caps are evaluated AFTER the artificial sweetener cap in the cap-application order.
If both fire (a product with both sucralose AND maltitol — pathological but possible),
the **lower** cap wins (more conservative = maltitol cap 62 beats sucralose cap 70).

---

## 7. Calorie Density Table Entry Placement

In `CALORIE_DENSITY_TABLES` in constants.py, add after the `snack_bar_granola` entry:

```python
"protein_bar": [(250,90),(320,80),(380,72),(430,62),(480,50),(540,38),(1e9,20)],
```

The lookup key selection in score_engine.py line ~3364:
```python
cd_table_key = category
if cat_result.get("category_subtype") == "protein_bar":
    cd_table_key = "protein_bar"
elif cat_result.get("category_subtype") == "yogurt":
    cd_table_key = "yogurt"
```

---

## 8. Environmental Gate

This entire lens is activated by a new env flag:

```python
# BARI_PROTEIN_BAR_V1 — protein_bar sub-lens activation (default OFF).
# Flag OFF → category_subtype=="protein_bar" products score on the standard
# snack_bar_granola weights and tables — byte-identical to HEAD.
# Flag ON → PROTEIN_BAR_WEIGHTS + protein-bar axes + polyol caps + engineering
# penalties + protein_bar calorie table + per-bar display fields active.
PROTEIN_BAR_LENS_ON = os.environ.get("BARI_PROTEIN_BAR_V1", "off").lower() == "on"
```

All `is_protein_bar` branches in score_engine.py are gated by `PROTEIN_BAR_LENS_ON`.
The router subtype detection (Section 1) is NOT gated — routing always happens; scoring
gate controls whether the sub-lens activates.

---

## 9. Acceptance Checks (Adversarial QA Gate)

The QA gate must verify the following invariants on the scored protein-bar corpus:

### 9.1 Ordering Invariants (Monotonicity Checks)

| Test pair | Required ordering |
|-----------|------------------|
| Bar A (maltitol, identical otherwise) vs Bar B (erythritol) | score(A) < score(B); ΔS ≥ 8 pts |
| Bar A (sucralose, identical otherwise) vs Bar B (no sweetener) | score(A) < score(B) |
| Bar A (glycerol present) vs Bar B (no glycerol, otherwise identical) | score(A) < score(B); ΔS ≥ 5 pts |
| Bar A (whole-food protein source) vs Bar B (isolate-only, equal sugar) | score(A) ≥ score(B) |
| Bar A (isolate-stacking 3+ families) vs Bar B (single isolate source) | score(A) < score(B) |
| Adding maltitol to a bar must not raise the score | score_with_maltitol ≤ score_without |
| Adding glycerol to a bar must not raise the score | score_with_glycerol ≤ score_without |

### 9.2 Cap Checks

| Product type | Required cap |
|-------------|-------------|
| Any product with maltitol (Tier 1 polyol) | final score ≤ 62 |
| Any product with sorbitol/isomalt (Tier 2 polyol) | final score ≤ 66 |
| Any product with sucralose/acesulfame/aspartame | final score ≤ 70 |
| Product with both maltitol AND sucralose | final score ≤ 62 (worst cap wins) |

### 9.3 Protein Quantity Non-Movement Check

```
For any two protein_bar products identical except protein_g (20g vs 15g vs 10g):
- Score difference attributable to protein_quantity alone ≤ 5 composite points
- Verified by: run the product at 3 protein levels, diff the traces
```

### 9.4 Routing Check

All products on the protein bar shelf that have "חלבון" or "פרוטאין" in the name must
route to `category = snack_bar_granola`, `category_subtype = protein_bar`.

### 9.5 BEV-014 Double-Count Check

A "Max Brenner protein bar" or similar confectionery-with-protein product that already
scores correctly via the existing sugar/sat_fat/NOVA signals must NOT receive an additional
penalty from the protein_bar lens that pushes it below the absolute floor (10 pts).
The lens adds signals; it does not create new vetoes.

### 9.6 Calorie Density Non-Cliff Check

A bar at 379 kcal/100g and 381 kcal/100g should differ by ≤ 2 raw dimension points on
the calorie_density dimension (no cliff at the table boundaries). Verify the interpolation
function handles the protein_bar table correctly.

---

## 10. Files to Change (Summary)

| File | Change |
|------|--------|
| `constants.py` | Add: `PROTEIN_BAR_WEIGHTS`, `PROTEIN_BAR_GATE_*`, `POLYOL_TIER_*_TOKENS`, `POLYOL_TIER_*_PENALTY`, `GLYCEROL_TOKENS`, `GLYCEROL_ENGINEERING_PENALTY`, `PROTEIN_ISOLATE_FAMILIES`, `ISOLATE_STACKING_FAMILY_THRESHOLD`, `PROTEIN_WHOLEFOOD_TOKENS`, `PROTEIN_BAR_WHOLEFOOD_SOURCE_BONUS`, `PROTEIN_BAR_COLLAGEN_PENALTY`, `PROTEIN_BAR_REAL_FOOD_SUGAR_BONUS`, `PROTEIN_BAR_POLYOL_CAPS`, `PROTEIN_BAR_POLYOL_PENALTIES`, `PROTEIN_BAR_ENGINEERING_PENALTIES`, `PROTEIN_BAR_DISPLAY_PER_BAR_*`, `PROTEIN_BAR_LENS_ON`; add `"protein_bar"` row to `CALORIE_DENSITY_TABLES` |
| `router_v2.py` | Add new protein-bar hard anchors (Section 1.1) and their exclusion entries. Update `ROUTER_VERSION`. |
| `score_engine.py` | Add new constants to import block; add `is_protein_bar` active-weights branch; add `cd_table_key` branch for `protein_bar`; add `_detect_protein_bar_signals()` helper; add pre-weighting dimension adjusters block; pass `pb_signals` to guardrail path; add `protein_bar_signals` to trace output. |
| `evaluate_guardrails()` | Add polyol cap entries and engineering penalty entries for `protein_bar` subtype. |

No changes to `signal_extractor.py`, `ingredient_taxonomy.py`, `matrix_integrity.py`, or
any frontend files. The existing GLASSBOX / BSIP0 / BSIP1 pipelines are untouched.

---

## 11. Evidence Registry Entries Required (Before D7 Co-Sign)

| ID | Signal | Evidence tier | Status |
|----|--------|--------------|--------|
| EV-PBAR-001 | Polyol tier penalties (maltitol GI ~35; erythritol GI ~0) | STRONG | Pre-registered |
| EV-PBAR-002 | Artificial sweetener cap (existing SWEETENER_CAP_C, unchanged) | MODERATE | Already registered |
| EV-PBAR-003 | Glycerol as engineering marker | MODERATE | Pre-registered |
| EV-PBAR-004 | Protein source taxonomy (isolate vs whole-food; DIAAS excluded per KB-004) | MODERATE | Pre-registered |
| EV-PBAR-004b | Isolate-stacking family threshold (3+) | WEAK-MODERATE | Pre-registered |
| EV-PBAR-005 | Weight re-distribution rationale | — (design decision) | N/A |
| EV-PBAR-006 | Protein gate threshold (12g/100g) | MODERATE | Pre-registered |
| EV-PBAR-007 | Real-food sugar bonus magnitude (+5) | MODERATE | Pre-registered |
| EV-PBAR-008 | Calorie density table calibration | MODERATE | Pre-registered |

Evidence tier guidance: STRONG = systematic reviews or multiple RCTs; MODERATE = single
robust study or consistent mechanistic evidence; WEAK = mechanistic only or single small
study. All EV-PBAR entries require formal registration in `bsip2_evidence_registry_v1.md`
before the Data Agent activates the flag.

---

## 12. D7 Co-Sign Requirement

Per governance: this spec requires **both** Nutrition Agent (self) AND Product Agent
co-sign before Data Agent activates `BARI_PROTEIN_BAR_V1=on`. The spec is submitted to
Product Agent for co-sign as the next step after this document is filed.

Disputed areas (if any) surface during Product Agent review. No rule deploys in disputed
state.

---

## 13. What Is NOT in This Spec (Explicitly Out of Scope)

1. **DIAAS per-SKU scoring** — not label-derivable (KB-004). The Axis 3 source integrity
   judgment is MATRIX INTEGRITY (whole-food vs reconstructed), not DIAAS. These are
   different constructs; this spec does not conflate them.

2. **Protein-quantity ranking** — protein grams are a gate, not an axis. A 30g-protein
   bar does NOT automatically outscore a 20g-protein bar. This is by design.

3. **Hebrew copy / insight lines / row verdicts** — authoring is a separate deliverable
   (Content Agent + sign-off). This spec produces scores; copy comes later.

4. **Price-value ranking** — part of the supplement worldwide benchmark program
   (TASK-361), not this lens.

5. **Max-Brenner / candy-with-protein edge case** — handled by EXISTING signals
   (sugar/fat/NOVA/red-label). No new axis added. Copy will handle the framing.

---

*Authored: Nutrition Agent, 2026-06-21. TASK-365 design spec.*
*Next step: file EV-PBAR-001 through EV-PBAR-008 in evidence registry, then route to
Product Agent for D7 co-sign.*
