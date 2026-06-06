**Task:** TASK-179Z

# Bari Glass Box — D3 De-Moralization Spec (v1)

**Status:** SPEC — methodology document only. No engine code, no score movement, no published
score change. Section 3 (consumer-surface framing) requires **Product co-sign before this spec
is filed as CLOSED**. All numeric proposals in §5 (W4 build checklist) are pending that co-sign
and the EV-042 registration before Data builds.

**Author:** Nutrition Agent · **Date:** 2026-06-04 · **Wave:** TASK-179, Wave 4 pre-work
**Reads-first (binding):**
- `01_framework/glass_box/six_dimension_contract_v1.md` — the governing contract; §1.2 defines
  D3 de-moralization and §§D3 + 1.3 D-SCO-3 define D3's scope and the additive-quality rollup.
- `01_framework/glass_box/d5_d6_rule_spec_v1.md` — D6 gate design; D3 uncertainty feeds D6.
- `03_operations/bsip2/proto_v0/src/score_engine.py` — current D3 implementation.
- `03_operations/bsip2/proto_v0/src/constants.py` — `NOVA_PROCESSING_SCORES`, `NOVA_WFI_SCORES`,
  `NOVA_HP_WEIGHTS`, `PROCESSING_CAPS`, `DIMENSION_WEIGHTS`.

---

## 0. What this spec is and is not

**Is:** A methodology document that reframes D3 from a deterministic NOVA-class-to-penalty mapping
to a probabilistic population-level signal with explicit stated uncertainty. Defines the W4 signal
shape, confidence-scaling rule, consumer framing, score-impact boundary, and build-readiness
checklist.

**Is not:** An engine code change. Does not rescore any product. Does not open W4 tasks (CC opens
W4 tasks after the TASK-179X engagement gate verdict). Does not touch frozen invariants.

---

## 1. Current D3 Model: What It Claims vs What It Actually Knows

### 1.1 What the engine currently does

D3 is implemented across three locations in the current engine. Together they encode NOVA class as
a deterministic quality signal:

**Location 1 — `score_processing_quality` (the D3 dimension score).**

`score_engine.py:697–699`:
```python
def score_processing_quality(nova_level: int) -> tuple[float, str]:
    score = NOVA_PROCESSING_SCORES.get(nova_level, 50)
    return score, f"NOVA {nova_level} → processing_quality={score} (NOVA_PROCESSING_SCORES table)"
```

`constants.py:50`:
```python
NOVA_PROCESSING_SCORES = {1: 95, 2: 85, 3: 65, 4: 35}
```

This function takes a NOVA class (1–4) and returns a fixed score with no regard for what the
product actually does, whether the ingredient data is sufficient to assign the class reliably, or
whether the class correlates with the nutritional outcomes NOVA was designed to predict. NOVA 4
always returns 35. NOVA 1 always returns 95. There is no confidence term.

**Location 2 — PROCESSING_LOAD guardrail caps.**

`score_engine.py:1247–1251` (inside `evaluate_guardrails`):
```python
check_cap("NOVA_PROXY_4_ULTRA_PROCESSED", nova_level == 4, 68, proc_caps_fired)
check_cap("ADDITIVE_MARKERS_5_PLUS",      additive_ct >= 5, 60, proc_caps_fired)
check_cap("ADDITIVE_MARKERS_3_PLUS",      3 <= additive_ct < 5, 72, proc_caps_fired)
_nova3_cap = next(c for rule, _, c in PROCESSING_CAPS if rule == "NOVA_PROXY_3_PROCESSED")
check_cap("NOVA_PROXY_3_PROCESSED",       nova_level == 3, _nova3_cap, proc_caps_fired)
```

`constants.py:103–108`:
```python
PROCESSING_CAPS = [
    ("NOVA_PROXY_4_ULTRA_PROCESSED", "nova==4",  68),
    ("ADDITIVE_MARKERS_5_PLUS",      "additives>=5", 60),
    ("ADDITIVE_MARKERS_3_PLUS",      "additives>=3", 72),
    ("NOVA_PROXY_3_PROCESSED",       "nova==3",  87),
]
```

NOVA 4 applies a hard overall-score ceiling of 68, regardless of the product's actual nutritional
profile. A NOVA 4 product with a clean, high-protein, low-sugar nutrition panel is capped at 68
by class assignment alone.

**Location 3 — HP (hyper-palatability) weighting by NOVA class.**

`score_engine.py:1320–1350` (via `NOVA_HP_WEIGHTS`); `constants.py:52`:
```python
NOVA_HP_WEIGHTS = {1: 0.0, 2: 0.0, 3: 0.5, 4: 1.0}  # SRC-06
```

HP penalties are scaled by NOVA class — a NOVA 4 product receives the full HP penalty; a NOVA 3
product receives 50%. NOVA 1 and 2 receive no HP scaling at all. This encoding treats NOVA class
as a reliable individual-product marker of hyper-palatability potential, not a population-level
correlate.

**Additionally:** `score_whole_food_integrity` uses `NOVA_WFI_SCORES = {1:100, 2:85, 3:60, 4:30}`
(`score_engine.py:1085–1091`; `constants.py:51`) to map NOVA class to a whole-food-integrity
dimension score. This is a separate NOVA lookup with the same determinism problem.

**D3's dimension weight is 0.15** (`constants.py:11`), making it the joint-largest contributor to
the composite (tied with `nutrient_density` and `calorie_density`). The PROCESSING_LOAD cap
further amplifies its ceiling effect beyond the dimension weight.

### 1.2 What the evidence actually claims

NOVA is an epidemiological food classification system. Its evidence claim, stated precisely, is:

> **Populations whose diets contain a higher proportion of NOVA class 4 foods show, at the
> population level, associations with worse health outcomes including obesity, type 2 diabetes,
> cardiovascular disease, and all-cause mortality (Monteiro et al. 2019; IARC 2020; Srour et al.
> 2020).**

This is a population-level correlation over dietary patterns, not a statement about individual
products. Specifically, the evidence does NOT claim:

1. That any single NOVA 4 product, consumed in context, causes harm. The effect is observed at
   the dietary-pattern level.
2. That NOVA class reliably predicts the nutritional quality of an individual product. A NOVA 4
   high-protein dairy snack and a NOVA 4 sugar-sweetened beverage are assigned the same class but
   have radically different nutritional profiles.
3. That NOVA class is assignable with high confidence from an Israeli retail label. Many products
   cannot be definitively assigned without proportions, named additives, and manufacturing process
   disclosure — exactly the information the Israeli label frequently omits (D5's finding: generic
   additive terms, unnamed stabilisers, missing proportions). Low-confidence NOVA assignments are
   common on the real shelf.
4. That "ultra-processed" is a morally relevant category distinct from "processed." The
   engineering is a neutral fact; the NOVA epidemiology describes dietary-pattern correlations, not
   individual product quality verdicts.

Evidence strength: **Moderate** (the population-level epidemiological association is robust across
multiple cohorts and geographies; the extrapolation to individual product quality verdicts is not
supported by the evidence and is the source of the governance problem).

### 1.3 Where the current model overstates certainty

The current model makes three overstatements:

**O1 — Class-to-score determinism.** `NOVA_PROCESSING_SCORES` maps each NOVA class to a single
fixed score with no confidence term. NOVA 4 = 35, unconditionally. This treats a population-level
probabilistic correlate as if it were a product-level quality measurement. There is no such
measurement; the number is invented certainty.

**O2 — Hard ceiling regardless of nutritional profile.** The `NOVA_PROXY_4_ULTRA_PROCESSED`
guardrail cap of 68 applies to every NOVA 4 product without considering whether the product
actually exhibits the nutritional patterns that make NOVA 4 associated with poor outcomes at
population scale. A clean-formula high-protein NOVA 4 product is capped at 68 on the basis of
class alone, not on any nutritional observation.

**O3 — NOVA-class as HP weight.** Applying `NOVA_HP_WEIGHTS` uses NOVA class as a proxy for the
*probability* that a product is hyper-palatable — but the HP detection signals (fat-sugar combo,
fat-sodium combo, crunch-sweet combo) are already present in the engine as direct observational
signals (`HP_FAT_SUGAR_COMBO`, `HP_FAT_SODIUM_COMBO`, `HP_CRUNCH_SWEET_COMBO`). Scaling those
signals by NOVA class compounds the NOVA assumption on top of the direct observation. If the HP
signals fire, they fire — their magnitude should not further depend on a population-level class.

**What the engine should do instead:** D3 should report, with stated confidence, that this product
belongs to a formulation pattern population-level-associated with certain outcomes — and scale that
signal by how confident the NOVA assignment actually is, given the ingredient evidence available.
Low confidence NOVA assignment → smaller modifier, clearly flagged. High confidence NOVA
assignment (e.g. a clean NOVA 1 product: single ingredient, no additives) → modifier of current
magnitude.

---

## 2. Reframed D3 Model

### 2.1 Core reframe

D3 becomes a **probabilistic signal**: a score modifier within a defined range, scaled by
confidence in the NOVA assignment. It does not apply a fixed penalty by NOVA class. It reports
how confident the engine is in the NOVA assignment and scales the modifier accordingly.

The philosophical shift, stated precisely: D3 no longer claims "this product has processing
quality 35." It claims: "this product's formulation pattern is, at population scale, associated
with [direction] with [confidence]. The modifier is [value], scaled to that confidence."

This is consistent with the contract's §1.2 ("D3 reports 'this formulation pattern is, at the
population level, associated with [outcome direction], with [confidence]' — never 'this is
ultra-processed therefore bad'") and the four structural truths (truth #2: engineered ≠ bad;
truth #4: engine must not pretend certainty).

### 2.2 Signal shape

The D3 signal output struct, emitted per product in the trace (internal/professional surface):

```
d3_processing_signal: {
    nova_class: int,            # 1–4; NOVA proxy assignment from the existing NOVA classifier
    confidence: str,            # "low" | "medium" | "high" — see §2.3 for thresholds
    population_correlation: float,  # 0.0–1.0; see §2.4 for class-to-correlation mapping
    modifier: float,            # the actual score modifier applied (signed; negative = penalty)
    modifier_note: str,         # trace string explaining the modifier computation
    note_he: str                # honest Hebrew consumer framing (see Section 3)
}
```

**Field semantics:**

- `nova_class`: the NOVA proxy class from the existing classifier. Unchanged — D3 reframe does
  not change NOVA assignment logic, only what is done with the class.
- `confidence`: the engine's confidence in the NOVA assignment for THIS product, derived from
  observable signals (§2.3). This is the new term the current model lacks.
- `population_correlation`: a fixed, class-level reference value encoding the strength of the
  population-level epidemiological association for this NOVA class (§2.4). It is NOT a per-product
  measurement; it is the best available estimate of the signal's magnitude at population scale.
  Range 0.0–1.0 where 1.0 = strong association. This is a calibration anchor, not a score.
- `modifier`: the actual signed score modifier applied to the D3 dimension score, computed as:
  `modifier = base_modifier(nova_class) × confidence_scale(confidence)` (§2.5).
- `note_he`: the consumer-facing framing string for this product (Section 3).

### 2.3 Confidence thresholds

Confidence in the NOVA assignment is **high**, **medium**, or **low** based on observable signals
from the BSIP0 panel, not on the NOVA class itself. The following criteria determine the band:

**`high` confidence** — all three conditions met:
1. An ingredient list is present (not missing or corrupted).
2. The NOVA class is unambiguous from the ingredient signals: either (a) single-ingredient, no
   additives detected (NOVA 1); or (b) additives are named with E-codes or specific names (not
   generic bare terms per D5's G4 detector), and the processing pattern is clear.
3. No D5 `severe` disclosure band (a severe-opaque panel cannot support a confident NOVA
   assignment — the class is inferred from a structurally incomplete picture).

**`medium` confidence** — default when neither `high` nor `low` applies:
- An ingredient list is present; some or most additives are named; the NOVA class is plausible
  but not fully verifiable from the panel alone. Typical for multi-ingredient NOVA 2–3 products
  with partial ingredient disclosure.

**`low` confidence** — any of these conditions:
1. No ingredient list present (missing or empty panel).
2. D5 disclosure band is `partial` or `severe` (closable gaps that could materially affect NOVA
   assignment — unnamed stabilisers, unnamed preservatives, unnamed emulsifiers).
3. NOVA class inferred primarily from product name / category heuristics with no corroborating
   ingredient evidence (the classifier is working from a name signal alone, not from panel
   content).

**NOTE:** these confidence criteria reference D5 output (`d5_band`) as an input. The D3 reframe
therefore depends on `BARI_GLASSBOX_D5D6` being active to get the full `d5_band` signal. When
`BARI_GLASSBOX_D5D6` is OFF (current behavior), D3 confidence falls back to a simplified
two-signal rule (ingredient list present/absent + NOVA assignment certainty from the classifier's
own confidence band). The W4 flag (`BARI_GLASSBOX_W4`) subsumes the D5 integration — see §4.

**(Conceptual — needs EV-042 + D7 to bind these exact criteria before Data builds.)**

### 2.4 Population-correlation reference values

These are fixed, class-level calibration anchors derived from the epidemiological literature
(Monteiro et al. 2019; Srour et al. 2020; IARC 2020). They are NOT per-product measurements.
They encode how strong the NOVA-4 vs NOVA-1 population signal is and provide a proportional
anchor for the modifier calculation.

| NOVA class | `population_correlation` (reference) | Rationale |
|---|---|---|
| 1 | 0.05 | Near-zero association; unprocessed whole foods are the reference group in NOVA epidemiology |
| 2 | 0.15 | Culinary-processed foods (oils, flours, fermented staples); small positive signal vs NOVA 1 |
| 3 | 0.40 | Processed foods; moderate association; heterogeneous group (artisan bread to industrial preserves) |
| 4 | 0.75 | Ultra-processed foods; the strong association that drives the NOVA epidemiology; still a population correlate, not a per-product verdict |

**(Conceptual — these reference values require EV-042 + D7 co-sign to bind before they enter
the engine. The literature basis is the NOVA epidemiological cohort studies listed in §3 of
`research/glass_box/engine_enrichment_frameworks_scoping_v1.md`.)**

### 2.5 Score modifier formula

The D3 dimension score modifier replaces the fixed `NOVA_PROCESSING_SCORES` lookup with a
confidence-scaled version:

```
base_modifier(nova_class) = current NOVA_PROCESSING_SCORES[nova_class]
    # i.e. 95 / 85 / 65 / 35 — these anchor values are retained

confidence_scale(confidence):
    "high"   → 1.0   (current-magnitude modifier; high confidence = no scaling down)
    "medium" → 0.70  (moderate scale-down; uncertainty is real but assignment is plausible)
    "low"    → 0.40  (substantial scale-down; low-confidence NOVA assignment should contribute little)

modifier = base_modifier × confidence_scale
```

This means:
- A NOVA 4 product with HIGH confidence yields: `35 × 1.0 = 35` — same as today.
- A NOVA 4 product with MEDIUM confidence yields: `35 × 0.70 = 24.5` — a larger effective score
  (the base is 35; scaling down the penalty moves the product toward neutral 50, not lower).
- A NOVA 4 product with LOW confidence yields: `35 × 0.40 = 14.0` — close to neutral.

Wait — the modifier is the **dimension score** (0–100 where higher = better), not a penalty.
The base values in `NOVA_PROCESSING_SCORES` are already expressed as quality scores (95 = good,
35 = poor). Scaling them by confidence for low-confidence cases means the score moves toward a
neutral 50, not toward a worse score. This is the correct behavior: uncertain NOVA assignment →
D3 contributes less extreme signal toward either end.

**Corrected formula:**
```
base_score(nova_class) = NOVA_PROCESSING_SCORES[nova_class]  # 95 / 85 / 65 / 35
neutral = 50.0

confidence_scale(confidence):
    "high"   → 1.0
    "medium" → 0.70
    "low"    → 0.40

modifier_score = neutral + (base_score - neutral) × confidence_scale
# NOVA 4, high:   50 + (35 - 50) × 1.0  = 35.0  (same as today)
# NOVA 4, medium: 50 + (35 - 50) × 0.70 = 39.5
# NOVA 4, low:    50 + (35 - 50) × 0.40 = 44.0
# NOVA 1, high:   50 + (95 - 50) × 1.0  = 95.0  (same as today)
# NOVA 1, medium: 50 + (95 - 50) × 0.70 = 81.5
# NOVA 1, low:    50 + (95 - 50) × 0.40 = 68.0
```

**Implication for PROCESSING_LOAD caps:** The current `NOVA_PROXY_4_ULTRA_PROCESSED` cap (68) and
`NOVA_PROXY_3_PROCESSED` cap (87) apply uniformly. Under the reframe, the caps should likewise be
confidence-scaled — a low-confidence NOVA 4 assignment should not trigger the same hard ceiling as
a high-confidence one. The precise cap-scaling formula is a W4 implementation detail that Data
must derive from this spec; the governing principle is the same as the score-scaling rule above.

**(Conceptual — confidence_scale values 0.70 and 0.40 require EV-042 + D7 co-sign to bind.)**

### 2.6 Insufficient ingredient data: D3 defers to D6

When ingredient data is insufficient for NOVA classification — no ingredient list, heavily
corrupted panel, or a confidence band of `low` from the classifier itself with no corroborating
signals — **D3 does NOT invent a NOVA class.**

In this case:
- `nova_class` in the signal struct is set to the classifier's best-estimate value but flagged as
  low-confidence.
- `confidence` = `"low"`.
- The D3 modifier score is pushed toward neutral (50) via the confidence-scaling formula.
- The `note_he` field carries a hedged framing (Section 3, Candidate C).
- D3 passes a `low_confidence_nova` signal to D6, which may lower the grade ceiling further
  via the existing confidence-accumulator mechanism.

**D3 does not produce a fabricated NOVA class or a fabricated quality score. The uncertainty is
surfaced explicitly through the confidence field and through D6.** This is the same philosophy as
the D5 detector's G3 protein-blend handling: disclose the gap, route to D6, do not invent a value.

---

## 3. Consumer-Surface Framing

> **REQUIRES PRODUCT CO-SIGN BEFORE SPEC IS FILED AS CLOSED.**
>
> This section is Nutrition's draft. Product must review and co-sign the framing before Data
> builds the `note_he` copy into the W4 engine. The co-sign must be recorded inline in this
> document or as a return annotation to this task.
>
> **[PRODUCT CO-SIGN PLACEHOLDER — awaiting review and sign-off]**

### 3.1 Governing constraints (binding on all candidates)

From the contract §1.2 and Nutrition Hard Rules:

- **Forbidden framing:** Any variant of "מזון מעובד = גרוע" (ultra-processed = bad). This is
  moralizing a probabilistic signal. The engine does not make that claim; the consumer surface must
  not either.
- **Forbidden terms:** NOVA, BSIP, structural_class, cap, floor, ultra-processed (as a verdict).
  (Hard Rule 4; governance_v1 §7 framework-invisibility.)
- **Required framing:** probabilistic, explicitly hedged. The distinction is "מתאם ב-, לא גורם ל-"
  (associated with, not causes). The phrasing must reflect a population-level signal, not an
  individual-product verdict.
- **Tone:** calm, precise, non-alarmist. Bari scores nutritional architecture; it does not advise
  on diet or health outcomes. (Hard Rule 5.)
- **Length:** `note_he` is a single phrase (1–2 sentences maximum). It lives in a trace field and
  may appear on the professional surface or as a drilldown footnote — it is not a headline.

### 3.2 Candidate `note_he` phrases

**Candidate A — NOVA 1 (high confidence, positive signal):**

> "מוצר בעיבוד מינימלי — דפוס ההרכב שלו מתאם, ברמה אוכלוסייתית, עם תוצאות תזונתיות חיוביות."

*"Minimally processed product — its formulation pattern is, at the population level, associated
with positive nutritional outcomes."*

Rationale: Positive framing for the high end is symmetric with the negative framing at the low
end, and is truthful. NOVA 1 is the reference group in the epidemiology — the positive association
is the same evidence as the negative association at NOVA 4. Avoids "clean" or "healthy" (health
claim) in favor of "associated with positive outcomes at population scale."

---

**Candidate B — NOVA 3–4 (medium/high confidence, negative signal):**

> "דפוס הרכב זה מתאם, ברמה אוכלוסייתית, עם צריכה תזונתית גבוהה יותר של סוכר, שומן ונתרן — לא אמירה על מוצר זה בפני עצמו."

*"This formulation pattern is, at the population level, associated with higher dietary intake of
sugar, fat, and sodium — not a verdict on this individual product."*

Rationale: The explicit hedge ("not a verdict on this individual product") is the critical
de-moralizing move. It names what NOVA actually measures (population-level dietary pattern
correlations) and explicitly disclaims the individual-product extrapolation that the current model
wrongly implies. The phrase "ברמה אוכלוסייתית" (at the population level) is the key epistemic
marker — consumers reading this know they are seeing a statistical observation, not a personal
recommendation.

---

**Candidate C — Low confidence NOVA assignment (any class, ingredient data insufficient):**

> "הרכב המוצר לא פורט במלואו — לא ניתן להעריך את דפוס העיבוד בביטחון. האומדן הנוכחי הוא זמני."

*"The product's composition is not fully disclosed — the processing pattern cannot be assessed
with confidence. The current estimate is provisional."*

Rationale: When the engine cannot assign NOVA class with confidence, the honest framing is
disclosure of the uncertainty — not a hedged quality claim. This phrase routes the consumer to
the D5 finding (incomplete panel) rather than to a processing verdict. It is aligned with D5's
"לא צוין" / "לא ניתן לאמת" language standard (governance_v1 §8; d5_d6_rule_spec_v1.md §Q2).

---

### 3.3 Product co-sign notes

Product should review:

1. Whether Candidate B's explicit disavowal ("not a verdict on this individual product") is
   appropriate on the consumer surface (professional surface vs consumer drilldown distinction,
   contract §3 and §2.7).
2. Whether the phrases need shorter variants for mobile (the drilldown context may allow longer
   text than the score card).
3. Whether Candidate A (positive framing for NOVA 1) should be surfaced at all, or only the
   negative/uncertain candidates.
4. Whether "ברמה אוכלוסייתית" is legible to the target consumer without explanation, or whether
   a softer formulation is needed (e.g. "במחקרים גדולים על אוכלוסיות רבות").

**Product co-sign — decisions recorded 2026-06-04:**

**Q1 — Candidate B's disavowal on consumer surface: approved on all surfaces.**
"לא אמירה על מוצר זה בפני עצמו" is appropriate on both the professional surface and the consumer
drilldown. Removing it in consumer context would leave the phrase doing exactly what §1.3/O1
identifies as the governance problem: a population-level signal read as an individual-product
verdict. The hedge is not confusing — it is the honest framing that prevents the moralizing
extrapolation. It stays verbatim in both contexts.

**Q2 — Mobile variants: Candidate C only.**
Candidates A and B are each one sentence and render acceptably on mobile without separate variants.
Candidate C runs two sentences and is the one case long enough to warrant a mobile-compressed form.
Approved mobile-only variant for C:

> "הרכב המוצר לא פורט במלואו — האומדן לדפוס העיבוד הוא זמני."

*"The product's composition is not fully disclosed — the processing pattern estimate is provisional."*

This preserves the two core facts (incomplete panel, provisional estimate) within a single sentence.
The full two-sentence form is retained for desktop/professional contexts.

**Q3 — Candidate A (positive NOVA 1 framing): approved and required.**
Surface it. Suppressing the positive signal is a distortion — it implies the engine only has
negative findings on processing, which is false and asymmetric with the evidence. NOVA 1 at high
confidence is the reference-group finding; its positive association is drawn from the same
epidemiological evidence base as the NOVA 4 negative association. Surfacing both directions signals
to the consumer that this is a factual formulation-pattern observation, not a health warning system.
Candidate A ships alongside B and C.

**Q4 — "ברמה אוכלוסייתית" legibility: replace in both A and B.**
The target consumer is mobile and health-curious, not epidemiologically literate. "ברמה
אוכלוסייתית" reads as jargon for most of that audience and will not communicate the epistemic
intent. The alternative "במחקרים גדולים על אוכלוסיות רבות" is plain and carries the same
meaning: the finding comes from large population studies, not from this individual product's
profile. Apply the substitution to Candidates A and B.

**Approved `note_he` phrases (final wording):**

Candidate A (NOVA 1, high confidence, positive signal) — APPROVED WITH WORDING CHANGE:
> "מוצר בעיבוד מינימלי — דפוס ההרכב שלו מתאם, במחקרים גדולים על אוכלוסיות רבות, עם תוצאות תזונתיות חיוביות."

Candidate B (NOVA 3–4, medium/high confidence, negative signal) — APPROVED WITH WORDING CHANGE:
> "דפוס הרכב זה מתאם, במחקרים גדולים על אוכלוסיות רבות, עם צריכה תזונתית גבוהה יותר של סוכר, שומן ונתרן — לא אמירה על מוצר זה בפני עצמו."

Candidate C full form (low confidence, any class) — APPROVED AS DRAFTED:
> "הרכב המוצר לא פורט במלואו — לא ניתן להעריך את דפוס העיבוד בביטחון. האומדן הנוכחי הוא זמני."

Candidate C mobile variant — APPROVED (NEW):
> "הרכב המוצר לא פורט במלואו — האומדן לדפוס העיבוד הוא זמני."

All three candidates ship. No candidate is rejected. Wording changes affect A and B only
("ברמה אוכלוסייתית" → "במחקרים גדולים על אוכלוסיות רבות"); Candidate C is unchanged.
The full-form / mobile-compressed distinction for C is a rendering decision for Data — both
strings must be in the W4 implementation.

**Product D7 co-sign — 2026-06-04**

---

## 4. Score Impact Boundary

### 4.1 What changes under the D3 reframe

When `BARI_GLASSBOX_W4` is ON, the D3 reframe produces the following and only the following
score-affecting changes:

1. **`processing_quality` dimension score** moves from the fixed `NOVA_PROCESSING_SCORES` lookup
   to the confidence-scaled `modifier_score` formula (§2.5). For high-confidence products the
   score is identical to today. For medium/low-confidence products the score moves toward neutral.

2. **`NOVA_PROXY_4_ULTRA_PROCESSED` and `NOVA_PROXY_3_PROCESSED` guardrail caps** are scaled by
   the same confidence signal. A low-confidence NOVA 4 assignment does not trigger the full 68
   ceiling. (Exact cap-scaling formula deferred to Data as a W4 implementation detail from this
   spec's governing principle.)

3. **`NOVA_HP_WEIGHTS`-scaled HP penalties** are no longer scaled by NOVA class. HP detection
   signals (`HP_FAT_SUGAR_COMBO`, `HP_FAT_SODIUM_COMBO`, `HP_CRUNCH_SWEET_COMBO`) fire on their
   direct observational criteria; their magnitude is not modified by NOVA class. The direct HP
   signals already embed the relevant nutritional information. (This is a simplification, not an
   attenuation — the HP system becomes more honest by relying on its own observations rather than
   using NOVA as an amplifier.)

4. **`d3_processing_signal` struct** is added to the product trace (professional surface, internal
   only).

### 4.2 What does NOT change

- The NOVA classification / proxy assignment logic itself. This spec does not touch the NOVA
  classifier.
- `score_whole_food_integrity` and `NOVA_WFI_SCORES`. The whole-food-integrity dimension also uses
  NOVA, but it scores a different concept (ingredient count + fermentation + NOVA as a matrix
  signal). Its de-moralization, if any, is a separate spec.
- All other dimensions (D1/D2/D4/D5/D6).
- `DIMENSION_WEIGHTS` — processing_quality remains at 0.15.
- Published scores, grades, or any live category output.

### 4.3 Frozen invariants — explicitly preserved

This spec does not affect the frozen invariants. They are stated here as a guard:

- **Milk = `run_005_headpin`** (top = 85/A; engine tag `engine-baseline-2026-06-04`). Milk is
  predominantly NOVA 1–2 with high-confidence assignments. The D3 reframe at high confidence
  produces the same modifier as today — no milk score moves.
- **Snack bar ceiling = 70/B** (`snk-001 = 70/B`). D6 can only demote or withhold, never promote.
  D3 confidence-scaling for medium/low confidence moves D3 toward neutral (50), which raises the
  D3 sub-score contribution but is bounded — and cannot by itself breach the snack-bar ceiling
  logic, which is grounded in sugar/calorie guardrails independent of D3.
- **Bread provenance = `real_bread_retail_003_v1`** (Shufersal, 25–26 May 2026; 256 scanned, 81
  scored, 31 curated). Bread NOVA assignments are a known uncertainty source; the D3 reframe
  explicitly handles this by scaling toward neutral for low-confidence assignments, which is a more
  honest representation of what the engine actually knows.

Any score movement that would affect these invariants requires an explicit, separately authorized
rescore — this spec does not authorize one.

### 4.4 Flag and rollback

The D3 reframe ships behind `BARI_GLASSBOX_W4`, consistent with the existing Glass Box flag
convention:

```python
# score_engine.py (to be added at module load, same pattern as existing flags):
BARI_GLASSBOX_W4 = os.environ.get("BARI_GLASSBOX_W4", "off").lower() == "on"
```

Flag naming is consistent with:
- `BARI_GLASSBOX_D5D6` (Wave 1, D5/D6)
- `BARI_GLASSBOX_W15` (Wave 1.5, DIAAS)
- `BARI_GLASSBOX_W2` (Wave 2, D4 additive detection)

**OFF = byte-identical to the `BARI_GLASSBOX_W2` baseline.** No D3 signal struct is emitted;
`score_processing_quality` runs the current `NOVA_PROCESSING_SCORES` lookup verbatim;
`NOVA_HP_WEIGHTS` scaling is unchanged. All golden/frozen runs must verify 0-diff with the flag
OFF before any W4 commit.

Rollback = unset `BARI_GLASSBOX_W4`. No code revert required.

---

## 5. W4 Build Readiness Checklist

This checklist enumerates what Data Agent needs from this spec to begin W4 engine implementation.
All items are grounded here or in the referenced sources. Items marked PENDING require Product
co-sign (Section 3) before they are final.

### Item 1 — Signal shape
**Source:** §2.2 of this spec.
**Status:** DEFINED.
The `d3_processing_signal` struct (fields: `nova_class`, `confidence`, `population_correlation`,
`modifier`, `modifier_note`, `note_he`) is fully specified above. Data should add this struct to
the per-product trace output alongside the existing `processing_quality` dimension scores,
gated by `BARI_GLASSBOX_W4`.

### Item 2 — Confidence thresholds
**Source:** §2.3 of this spec.
**Status:** CONCEPTUAL — requires EV-042 + Product D7 co-sign to bind the exact criteria.
Three criteria determine `high` / `medium` / `low` confidence:
(a) ingredient list present/absent;
(b) additive naming completeness (named vs bare generic terms, using D5's G4 output when
    `BARI_GLASSBOX_D5D6` is ON);
(c) D5 disclosure band (`severe` band → not high confidence).
Simplified two-signal fallback (ingredient list + classifier confidence band) applies when
`BARI_GLASSBOX_D5D6` is OFF.

### Item 3 — Flag name
**Source:** §4.4 of this spec.
**Status:** CONFIRMED.
Flag: `BARI_GLASSBOX_W4`. Env var: `os.environ.get("BARI_GLASSBOX_W4", "off").lower() == "on"`.
Default OFF. Consistent with the existing Glass Box flag naming sequence.

### Item 4 — Score formula delta
**Source:** §2.5 of this spec.
**Status:** FORMULA DEFINED, confidence_scale VALUES CONCEPTUAL — require EV-042 + D7 co-sign.
Formula:
```
modifier_score = 50.0 + (base_score - 50.0) × confidence_scale(confidence)
    where base_score = NOVA_PROCESSING_SCORES[nova_class]
    and confidence_scale: high=1.0, medium=0.70, low=0.40
```
PROCESSING_LOAD cap scaling follows the same principle (confidence-scaled) — Data to derive the
exact cap formula from the governing principle in §4.1 Item 2.
NOVA_HP_WEIGHTS scaling to be removed — HP penalties revert to their direct-observation magnitude
without NOVA amplification.

### Item 5 — Consumer copy templates (note_he)
**Source:** §3.2 of this spec.
**Status:** DRAFTED — PENDING Product co-sign on Section 3.
Three candidate `note_he` phrases:
- Candidate A: NOVA 1 positive framing (minimally processed, population-level positive
  association).
- Candidate B: NOVA 3–4 negative framing (population-level association, explicit individual-
  product hedge).
- Candidate C: Low-confidence framing (incomplete panel, provisional estimate).
Product co-sign on Section 3 finalizes which candidates ship, their exact wording, and any
mobile/drilldown variants.

### Item 6 — Evidence registry entry
**Status:** DRAFT — requires Product D7 co-sign to append to registry.
Draft EV number: **EV-042** (next in sequence after EV-041, which covers D4 additive-tier
detector; `bsip2_evidence_registry_v1.md`). Data must not build W4 D3 scoring rules without an
EV-042 entry co-signed by both Nutrition and Product.

### Summary — what blocks W4 engine start

| Blocker | Status | Resolution path |
|---|---|---|
| Section 3 consumer framing | PENDING Product co-sign | Product reviews §3 and signs inline or via return block |
| confidence_scale values (0.70, 0.40) | CONCEPTUAL | EV-042 + Product D7 co-sign |
| Confidence criteria (§2.3) | CONCEPTUAL | EV-042 + Product D7 co-sign |
| population_correlation reference values (§2.4) | CONCEPTUAL | EV-042 + Product D7 co-sign |
| W4 tasks opened | BLOCKED | CC opens W4 tasks only after TASK-179X engagement gate verdict |

**Nothing in this spec authorizes Data to begin engine implementation. This is W4 pre-work.**
Data can begin only after: (a) Product co-signs Section 3; (b) EV-042 is registered with D7
co-sign; (c) TASK-179X passes the engagement gate and CC opens W4 tasks.

---

## 6. DRAFT Evidence-Registry Entry (EV-042)

**Status:** DRAFT — pending Product D7 co-sign. Not to be appended to
`bsip2_evidence_registry_v1.md` until co-signed.

| Field | Value |
|---|---|
| **finding_id** | EV-042 (Glass Box Wave 4, D3 de-moralization; TASK-179Z spec) |
| **task** | TASK-179Z (methodology spec); W4 implementation task (to be opened by CC after TASK-179X) |
| **recorded** | 2026-06-04 |
| **dimension** | D3 — processing / formulation signal |
| **signal** | D3 is a population-level probabilistic correlate of nutritional risk, confidence-scaled by the quality of the NOVA assignment. Emits `d3_processing_signal: {nova_class, confidence, population_correlation, modifier, modifier_note, note_he}`. Score modifier = `50 + (base_score − 50) × confidence_scale`, where confidence_scale is 1.0 / 0.70 / 0.40 for high / medium / low. NOVA_HP_WEIGHTS NOVA-class amplification removed; HP penalties revert to direct-observation magnitude. |
| **evidence_claim** | Population-level epidemiological association (Monteiro et al. 2019; Srour et al. 2020; IARC 2020): NOVA 4 dietary patterns are associated with worse health outcomes at population scale. This is a dietary-pattern correlate, not an individual-product verdict. Evidence strength: **Moderate** (robust epidemiology; individual-product extrapolation not supported by evidence). |
| **source** | `01_framework/glass_box/d3_demoralization_spec_v1.md`; `six_dimension_contract_v1.md §1.2, §D3`; `score_engine.py` (`score_processing_quality` L697–699, `NOVA_PROXY_4_ULTRA_PROCESSED` cap L1247, `NOVA_HP_WEIGHTS` scaling L1321–1350); `constants.py` (NOVA_PROCESSING_SCORES L50, NOVA_WFI_SCORES L51, NOVA_HP_WEIGHTS L52, PROCESSING_CAPS L103–108). |
| **co_sign** | Nutrition D7 — co-signed (TASK-179Z, 2026-06-04). Product D7 — **PENDING**. |
| **status** | DRAFT — not adopted. Adoption requires Product D7 co-sign + W4 task open by CC after TASK-179X. |
| **rollback_flag** | `BARI_GLASSBOX_W4` (default OFF) — unset → D3 runs current NOVA_PROCESSING_SCORES verbatim; byte-identical to BARI_GLASSBOX_W2 baseline. |

---

*End of D3 De-Moralization Spec v1. Doc-only — no engine, frontend, scoring, or governance file
was modified. Section 3 consumer framing is drafted by Nutrition; Product co-sign is required
before CC closes TASK-179Z.*
