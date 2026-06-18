# Brined / Salty Soft Cheese (גבינות מלוחות) — Scoring Interpretation v1

**Task:** brined-cheese-methodology
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** DRAFT — proposed RETURNED; awaiting orchestrator review
**Dependency for:** Factory move #6 (first real-shelf run for this category)
**Predecessor document:** `01_framework/governance/cheese_spreads_stress_test_001.md` (TASK-141),
which explicitly excludes "בולגרית, פטה, צפתית" and defers them to "a separate stress test."
This document is that separate stress test — methodology core only.

---

## 1. Category Scope and Boundaries

### 1.1 Defining characteristic

Brined / salty soft cheese is defined by a single structural property: **the cheese is preserved in,
or was produced via, a saturated brine**, resulting in a sodium load that is substantially higher than
fresh (non-brined) dairy and is an intrinsic consequence of the production method — not a reformulation
choice or an additive decision. Sodium in this category is preservation architecture, not excess.

This is the analogue of the `brined_food` context_flag that already exists in the engine for pickled
vegetables and olives. The mechanism is identical; only the food matrix and the scoring implications
differ (see Section 3).

### 1.2 In scope

| Type | Hebrew | Notes |
|---|---|---|
| Bulgarian cheese | בולגרית (מעודנת / מסורתית) | Fat tiers 5% / 16% / 24%; cow's milk standard; cubes/blocks |
| Feta-style cow | פטה עיזים / פטה כבשים / פטה פרה | Includes imported and Israeli production; sheep/goat/cow/mixed |
| Tzfatit | צפתית | Israeli semi-soft brined cheese; milder, distinct culture profile |
| Halloumi | חלומי | Brined semi-firm; notable for cooking stability |
| Seasoning variants | בולגרית עם שום / עשבי תיבול | Treated as variants within the same type, not separate pools |
| Brand-specific names that map to the above | גבינה מלוחה חמד | Evaluate on structure: if it is brined semi-soft, it is in scope |

### 1.3 Out of scope — and the in/out rule

**The in/out rule:** A product is in scope if and only if (a) it is soft or semi-firm, (b) it is
preserved in brine as the primary production/preservation method, and (c) it is a table cheese
(consumed as-purchased or with minimal preparation, not as a cooking ingredient).

Products excluded:

| Type | Reason |
|---|---|
| Hard/aged yellow cheeses (גאודה, קשקבל, עמק, צ'דר) | Different matrix, aging rather than brining, separate category |
| Fresh cottage / white cheese / cream cheese | Covered by cheese-spreads (TASK-141/142); not brined |
| Labaneh | Covered by cheese-spreads; fermentation-set, not brined |
| Processed melting slices/triangles (משולשים) | NOVA-4 processed cheese; own category |
| Infant / toddler dairy | Out of scope per `evaluation_scope.py` OUT_OF_SCOPE_SIGNALS_HE |
| גבינת מריחה בולגרית (Bulgarian spreadable) | **Boundary call — rule:** if the label says "ממרח" / "מריחה" and the texture is whipped/spreadable rather than block-form, it belongs in the cheese-spreads cream-cheese pool, not here. Brined-block בולגרית at any fat tier belongs here. |

**Ricotta ruling:** Ricotta (ריקוטה) is OUT of this category. The cheese-spreads stress test already
excluded it as a "cooking ingredient, not a table cheese." That ruling stands. Ricotta is not brined
(it is a heat-coagulated whey cheese), does not share the sodium architecture of brined cheese, and is
consumed primarily as a baking/cooking ingredient in the Israeli retail context. ריקוטה לאפייה is the
dominant shelf form. Ricotta belongs to neither cheese-spreads nor brined-cheeses; it is a cooking
ingredient sub-category that is out of scope for comparison scoring in v1. If ricotta appears in a
scrape, filter it at the corpus stage.

---

## 2. Sub-Pool Structure

### 2.1 Recommendation: a single pool with type disclosed in the display layer

The brined-cheese shelf does NOT warrant sub-pools. Here is the reasoning.

The cheese-spreads category required four pools because the structural divergence between cottage,
white-cheese, labaneh, and cream-cheese was real and deep: different set methods, different protein
tiers, different fermentation architectures, different consumer occasions. The Sec 2.9 dairy divergence
axis confirmed this.

Brined cheeses share a **unified structural identity**: all are brined, all carry the same preservation
sodium architecture, all are consumed as table/mezze cheese, and the scoring-relevant variation
(fat %, milk source, additives) runs continuously across the shelf rather than clustering into
architecturally distinct pools. Specifically:

- Fat % (5 / 16 / 20 / 24%) is a **variant dimension**, not a pool split. Within each type
  (בולגרית, פטה, צפתית) the fat tier is a product variant exactly as 3/5/9% is a variant within
  white cheese (Constitution Sec 2.9 / Article II 2.5).
- Milk source (cow / goat / sheep) is meaningful for consumer taste preference but is **not a scoring
  architecture split**. Goat-milk and sheep-milk feta are not structurally different from each other in
  a way the engine meaningfully scores — fat content, protein, sodium, and NOVA behave similarly.
  They should be disclosed in the display layer (insight lines), not separated into pools.
- Halloumi has one unusual property (it can be grilled), but its nutritional architecture and sodium
  profile are within the same scoring-relevant range as the rest of the shelf. It belongs in the single
  pool with a type label on its display card.

**The single-pool recommendation does not mean the shelf collapses to one grade** — see Section 5.
The variation within the category is real and the engine will produce genuine spread. Pools add
governance complexity without adding scoring signal here.

**Display layer instruction (for the Frontend/Content handoff):** the category display should show
the cheese type (type badge: בולגרית / פטה / צפתית / חלומי) as a visual context label on the product
card, so the consumer knows they are looking at a type-disclosed single-shelf comparison. This is a
display instruction, not a scoring split.

---

## 3. Sodium — The Central Question

### 3.1 What the engine currently does (exact code behavior)

**`evaluation_scope.py`** defines the `brined_food` context-limited signal as:

```python
"brined_food": {
    "name_keywords": [
        "זיתים", "זיתים כבושים", "חמוצים", "כרוב כבוש",
        "ירקות כבושים", "קיפר",
    ],
    "nutrition_validator": lambda nn: (nn.get("sodium_mg") or 0) > 500,
},
```

The keyword list covers **pickled vegetables and olives only**. None of the brined-cheese names
(בולגרית, פטה, צפתית, חלומי) are in this list. The function checks only the product's
`canonical_name_he` field (not ingredient text). Therefore:

**Every brined cheese currently evaluates as `evaluation_status: "standard"` with
`context_flag: None`.**

**`score_engine.py` line 1905:**

```python
sodium_weight = 0.7 if context_flag == "brined_food" else 1.0
```

Since `context_flag` is `None` for all brined cheeses, `sodium_weight` is always `1.0`.
The 0.7 relief mechanism exists in the engine but is completely unwired for this category.
The `HIGH_SODIUM_700MG_PLUS` cap (score capped at 60 when sodium >= 700mg) fires at full weight.

The `context_note` for `brined_food` ("Sodium reflects preservation brine. Not all sodium in the
per-100g figure is consumed; brine is typically not eaten.") also never renders for these products.

### 3.2 Is sodium a real differentiator on this shelf, or a near-constant trait?

Sodium in brined cheese is substantially higher than fresh cheese but **is not a constant across the
shelf**. The differentiation is real but compressed:

- Low-sodium brined cheese (e.g., בולגרית מעודנת 5%): ~300–500mg sodium/100g. These are lower-brine
  or shorter-brine products positioned as "refined."
- Standard brined cheese (בולגרית מסורתית 16%, standard פטה): ~500–800mg sodium/100g.
- High-sodium variants (full-fat traditional פטה, חלומי): 800–1100mg sodium/100g is commonly
  observed on the Israeli retail shelf.

This range — roughly 300mg to 1100mg — crosses the `HIGH_SODIUM_700MG_PLUS` cap threshold for a
meaningful portion of the shelf (the upper third). Under current unmodified scoring, products at
900mg sodium/100g would receive a hard cap of 60/C. This is technically correct behavior in isolation
but fails the context test: the consumer of brined cheese does not consume 100g of brine-soaked
product in a single sitting, and the standard portion (30–50g) plus the typical practice of rinsing
the cheese before eating materially reduces the consumed sodium.

However — and this is critical — **the brine-context argument is not infinitely elastic**. The
difference between a 350mg and a 900mg product is real and reflects genuine production choices
(brine concentration, production duration, drainage quality). The engine should **reduce** the sodium
penalty weight relative to standard foods, but it should **not zero it out**. Sodium remains a
legitimate differentiator within this category; the attenuation should reflect portion-and-rinsing
reality, not eliminate the signal.

### 3.3 Is the existing 0.7 weight the right number?

The 0.7 weight was designed for olives and pickled vegetables — foods where the consumer **definitely
does not consume the brine** (it stays in the jar). The corresponding context note ("Not all sodium
in the per-100g figure is consumed; brine is typically not eaten") is apt for olives.

For brined cheese, the reality is more nuanced:
- The brine is not consumed directly, but the cheese is soaked and retains brine sodium in the matrix.
- Rinsing removes a fraction of the surface sodium but not all embedded sodium.
- A 30–50g portion of 800mg/100g cheese delivers ~240–400mg sodium — a non-trivial dietary load.

**Recommendation:** Retain 0.7 as the sodium weight for brined cheese. It is not perfectly calibrated
for cheese versus olives, but it is directionally correct and within the range that is defensible given
real portion behavior. The alternative — designing a separate weight specifically for brined cheese —
would require evidence-registry support (EV-### + D7 co-sign) and is not warranted at this stage.
The 0.7 weight applied to brined cheese is an **application of an existing governed parameter**, not
a new scoring rule. It does not require a new D7 cycle.

What does require action is wiring the flag so it actually fires.

### 3.4 The wiring gap — how to set the `brined_food` flag for these SKUs

**Current state:** The flag is never set for any brined cheese because none of their canonical names
match the existing keyword list.

**Required change:** Add the brined-cheese name signals to the `brined_food` keyword list in
`evaluation_scope.py`. The recommended additions:

```
"בולגרית", "פטה", "צפתית", "חלומי", "גבינה מלוחה"
```

The nutrition validator (sodium > 500mg) already correctly filters out products that happen to have
these words in the name but are not high-sodium (unlikely, but the guard is appropriate to keep).

**Scope of this change:** This is a routing/flag assignment change, exactly analogous to the
cream-cheese router anchors added in TASK-145. It changes which `context_flag` a product receives —
and therefore whether the 0.7 sodium weight applies — but it does not change any scoring weight,
threshold, penalty, or cap. The 0.7 weight already exists and was already D7-approved for brined
foods.

**Governance classification:** This change does NOT require a new D7 cycle. It is an application of
an already-approved context classification to a new food type that the flag was designed for. It
requires:
- An Evidence Registry entry documenting the extension (EV-###, to be assigned)
- Nutrition Agent sign-off (this document constitutes that sign-off, conditional on orchestrator
  acceptance)
- A regression test covering בולגרית / פטה / צפתית / חלומי name signals

**Flag:** I am flagging this as a decision the orchestrator should confirm before the Data Agent wires
it. If the orchestrator or Product Agent believes this constitutes a scoring rule change (because it
moves sodium weight from 1.0 to 0.7 for a whole new food class), it should go through the full D7
path. My reading is that it does not — the weight was already approved for this exact use — but I
will not unilaterally wire it without acknowledgment.

---

## 4. What Actually Differentiates Quality on This Shelf

Once the sodium signal is appropriately attenuated (0.7 weight), the following signals carry genuine
differentiation information for this category. I list them in order of scoring relevance.

### 4.1 Fat % — real variation, real scoring signal (FIRES CORRECTLY, no modification needed)

Fat ranges from 5% to 24% across the shelf. This is genuine architectural variation:
- 5% בולגרית מעודנת is lower in calories, lower in saturated fat, structurally lighter
- 16%/24% is richer, higher sat-fat, higher caloric density

The **sat-fat cap** (`ISRAELI_RED_LABEL_1_SAT_FAT`, cap at 55) will fire for high-fat variants
(24% fat cheese will typically show sat-fat in the red-label range). This is correct behavior.

**No modification needed.** The fat scoring drivers behave correctly for this shelf.

### 4.2 NOVA / additives — the real differentiator (FIRES CORRECTLY, no modification needed)

This is the strongest differentiator within the category. The shelf has a genuine two-tier structure:

**NOVA-1 / clean matrix products** (typically: בולגרית מסורתית, clean פטה, צפתית):
- Ingredients: milk (or goat/sheep milk), salt, bacterial cultures, rennet. Sometimes calcium chloride.
- NOVA 1. No additive penalty. No `LONG_INGREDIENT_LIST`. These are among the least-processed items
  in the entire dairy case.

**NOVA-3/4 / extended matrix products** (typically: some branded פטה variants, flavored בולגרית with
preservatives, halloumi with emulsifiers or stabilizers, "Bulgarian spread" edge cases):
- May contain: locust bean gum, carrageenan, modified starch, potassium sorbate, E-numbered
  stabilizers, flavor enhancers.
- NOVA 3–4. Additive penalty fires. `LONG_INGREDIENT_LIST` may fire for complex variants.

This NOVA split is the honest finding on this shelf and the primary quality differentiator beyond
fat. The engine handles it correctly with no modification.

**Seasoning variants (שום / עשבי תיבול):** Garlic and herb variants of בולגרית are on the shelf.
The correct treatment is to check whether the seasoning is a clean ingredient (dried garlic, dried
herbs → still NOVA 1, no penalty) or whether it is accompanied by flavor enhancers, preservatives,
or stabilizers. The ingredient parse at BSIP1 handles this correctly via the existing NOVA inference.
No special rule needed.

### 4.3 Milk source — display context, not a scoring signal (SUPPRESS as a scoring driver)

Goat-milk, sheep-milk, and cow-milk variants exist on the shelf. Milk source is NOT a scoring signal
in the current engine and should not become one for this category. The nutritional differences between
sheep-milk and cow-milk feta are real but small, and the evidence for meaningful health differentiation
is weak (evidence tier: Weak). Milk source matters to the consumer's taste and cultural preference
and should appear in the insight line / display card, not in the score.

**Instruction:** Do not add a milk-source signal to the engine for this category.

### 4.4 Protein density — fires correctly for most products, no modification

Brined cheeses generally have moderate protein (8–16g/100g depending on fat tier and milk source).
The existing protein signal handles this correctly. No specific modification needed; protein will be
a minor contributor in the score, which is appropriate for a category where fat, NOVA, and sodium
are the primary dimensions.

### 4.5 Fermentation credit — apply existing EV-015 logic, enforce flavor-vs-marker guard

Brined cheeses are almost universally produced with bacterial cultures. The culture credit (EV-015)
should apply when the ingredient list confirms live or active cultures in the standard BSIP1
enrichment vocabulary (established in TASK-139B). The flavor-vs-marker guard applies: "culture
flavor" (תרבית לטעם) does not qualify; only confirmed live-culture markers do.

In practice, the fermentation signal in this category is likely to be less differentiated than in
yogurt or labaneh — most clean brined cheeses will list cultures, while highly processed variants
may not. The signal is valid; the BSIP1 enrichment team should apply the existing detection logic
without modification.

### 4.6 Signals to suppress

| Signal | Reason to suppress |
|---|---|
| `HP_FAT_SUGAR_COMBO` (hyper-palatability fat+sugar) | Brined cheese has near-zero sugar; the fat in this category is structural dairy fat, not an engineered palatability stack. The HP signal should not fire because the sugar leg of the combo (which requires sugar >= threshold) will not be met. No active suppression needed — it self-gates. |
| `HP_FAT_SODIUM_COMBO` (hyper-palatability fat+sodium) | This one needs attention. A 24% fat brined cheese at 900mg sodium would satisfy both the fat% threshold and the sodium threshold for HP_FAT_SODIUM. This is a false positive: the fat is structural dairy fat, not engineered palatability fat, and the sodium is brine preservation, not added-flavor engineering. **Recommendation:** Apply the same `context_limited` context reasoning to suppress the HP fat+sodium penalty for products that receive the `brined_food` context_flag. The flag already communicates "sodium here is brine, not engineered." The HP family should respect the flag. This is a flag-check addition in the HP evaluation block — it is an extension of the existing brined_food context logic, not a new rule. This needs D7 co-sign before the Data Agent wires it. |

---

## 5. Anti-Collapse Check

### 5.1 What a naive full-weight run would produce

Without the `brined_food` flag wired:
- Every product on this shelf has sodium >= 300mg.
- Products at or above 700mg sodium (expected: roughly the upper half of the shelf, particularly
  traditional-format 16%+ fat products) receive the `HIGH_SODIUM_700MG_PLUS` cap: score capped at 60.
- Products at the high end of both fat and sodium simultaneously (24% fat, 900mg+ sodium) would hit
  both the sat-fat cap (55) and the sodium cap (60). Effective cap: 55.
- Result: **the entire upper-fat, traditional-format segment collapses into 55–60 range (C).** The
  clean NOVA-1 traditional בולגרית מסורתית at 24% and the additive-laden "light" reformulated variant
  both land at 55–60 because sodium and sat-fat caps overwhelm the NOVA differentiation. This is a
  genuine collapse, not an honest finding.

### 5.2 What the recommended treatment produces

With the `brined_food` flag correctly wired (sodium_weight = 0.7):
- The `HIGH_SODIUM_700MG_PLUS` cap effective value rises: `max(60, int(60 + (100-60) * (1-0.7)))` =
  `max(60, int(60 + 40 * 0.3))` = `max(60, int(72))` = 72. A 900mg sodium product is now capped at
  72, not 60.
- The sat-fat cap (55 for red-label sat-fat) continues to fire correctly for 24% fat products.
  This remains a real signal.
- The NOVA differential now gets room to express: a clean NOVA-1 traditional 24% בולגרית with
  sat-fat-cap firing lands around 55–65; a NOVA-1/no-additives 16% product without sat-fat red label
  lands in the 65–75 range; a 5% clean NOVA-1 product lands 70–80. A 16% additive-laden reformulated
  variant with NOVA 3–4 lands notably lower than the same-fat-tier clean product.
- This produces genuine spread: expected range approximately 50–80 across the shelf, with grades B
  (70–80 range, clean NOVA-1 at moderate fat) to C (55–70 range, high-fat or sodium-heavy or
  processed) and potentially D for heavily additive-laden variants.

### 5.3 Is this manufactured spread?

No. The spread is honest:
- Clean NOVA-1 brined cheese (milk + salt + cultures) genuinely has a better nutritional architecture
  than an additive-laden "cheese product" with emulsifiers and stabilizers. The NOVA signal is real.
- Lower-fat variants (5%) genuinely have less sat-fat. The fat signal is real.
- The sodium attenuation (0.7 weight) does not eliminate sodium differentiation — a 350mg product
  still scores better than a 900mg product on the sodium dimension, just less harshly.
- We are not adding signals to manufacture spread; we are removing an overcorrection (the 1.0 sodium
  weight treating brine-sodium identically to reformulation-sodium) that was artificially suppressing
  what would otherwise be a legitimate quality signal from NOVA and fat.

### 5.4 Honest-clustering acknowledgment

If, after the real scrape, the Israeli brined-cheese shelf turns out to be predominantly NOVA-1 with
sodium in the 500–700mg range (possible for a retailer that stocks primarily traditional products),
genuine clustering may result in a narrow grade band (e.g., B-/C+). That outcome should be reported
honestly, not engineered away. The butter memory rule applies here: genuine clustering is a valid
finding.

---

## 6. Outstanding Items and Flags for Orchestrator

1. **Engine wiring — evaluation_scope.py:** Adding `"בולגרית", "פטה", "צפתית", "חלומי", "גבינה מלוחה"`
   to the `brined_food` name_keywords list. I have classified this as an application of an existing
   approved parameter. The orchestrator should confirm or escalate to D7 before Data Agent wires it.

2. **HP fat+sodium suppression for brined_food context:** I have recommended suppressing `HP_FAT_SODIUM_COMBO`
   when context_flag == "brined_food". This is a scoring behavior change in the HP family and
   **does require a D7 co-sign** (Nutrition + Product Agent). It is a new conditional, not an
   application of an existing parameter. I am proposing it here; it needs an Evidence Registry entry
   and D7 before implementation.

3. **No stress test governance document produced here.** This is a methodology brief, not a full
   governance stress test document of the kind produced for cheese-spreads (TASK-141) or cereals.
   Whether a full stress test is required before the factory run is a Product Agent / orchestrator
   decision. My read: the category is simpler than cheese-spreads (no sub-pool splits, one new flag
   application, one new HP suppression rule), and the governance frameworks from TASK-141 (Sec 2.9,
   Sec 5.2.1, Sec 6.4 with DISTORTION-010 sodium disclosure) already apply and need only be activated
   rather than amended.

4. **DISTORTION-010 (sodium endemic):** The sodium-and-saturated-fat disclosure text approved in
   cheese-spreads (TASK-141 / Resolution 3 category-wide note) applies directly to this category as
   well. It should be activated at the frontend packaging stage, not re-written. The same BSIP3
   priority note applies: DISTORTION-010 is the biggest honest limitation of the current score on
   this shelf.

5. **A-ceiling (EV-021 / RULING-DAIRY-A-01):** The dairy A-ceiling applies. A clean brined cheese
   (NOVA-1, no added sugar, no engineered additives, live cultures confirmed) is potentially
   A-eligible at the macro level if it scores >= 80. The C1–C6 ceiling applies: C2 (engineered
   additives — none in clean brined cheese), C3 (live culture — must be confirmed in ingredient list,
   not just implied by category). The ceiling functions correctly and needs no modification.

---

## 7. Summary Table

| Question | Answer |
|---|---|
| Scope | Brined/brine-preserved semi-soft table cheeses: בולגרית, פטה, צפתית, חלומי, גבינה מלוחה |
| Ricotta | OUT. Not brined, cooking ingredient, out of scope for both cheese-spreads and brined-cheeses. |
| גבינת מריחה בולגרית | OUT. "ממרח" / spreadable form → cheese-spreads cream-cheese pool. |
| Sub-pools | Single pool. Fat tier and milk source are variant dimensions, not pool splits. |
| Sodium differentiator? | Yes, but compressed range; brine context means 0.7 weight is correct. |
| 0.7 weight correct? | Yes. Retain as-is. Not too harsh, not too soft. |
| Wiring gap | brined_food flag never fires for any cheese — name_keywords list missing all cheese signals. Add "בולגרית", "פטה", "צפתית", "חלומי", "גבינה מלוחה". |
| Primary quality differentiator | NOVA / additives. Clean milk+salt+cultures vs. stabilizer-laden variants. |
| HP fat+sodium combo | Needs suppression for brined_food context — D7 required. |
| Anti-collapse result | With 0.7 weight: ~50–80 spread, honest NOVA differentiation. Without: shelf collapses into 55–60. |
| Honest clustering | If shelf is predominantly clean NOVA-1, clustering at B/C is a valid finding. |
