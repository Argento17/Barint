# Cookies & Coffee — Additive Depth Ruling v1
## מחמאה, PHVO Detection, and Named-Additive Severity Tiers

**Task:** TASK-275  
**Date:** 2026-06-14  
**Author:** Nutrition Agent  
**Status:** RETURNED — proposed for orchestrator review and co-sign

---

## Executive Summary

The current engine does not punish מחמאה (imitation/compound butter, typically
`שומנים מוקשים מן הצומח`) and cannot detect it. This is a double failure: the PHVO
detector (`has_phvo`) misses the ingredient because it uses singular-form markers
(`שומן/שמן צמחי מוקשה`) that do not match the plural form (`שומנים מוקשים`) used on
Israeli labels, and `מחמאה` itself is not a recognized term at all. The result is that
a product declaring hardened vegetable fat receives `fat_quality: 87` — scoring its fat
as high quality. This is a signal inversion. This ruling documents what מחמאה is, why
it warrants severe penalization, what the engine currently does (or fails to do), and
the exact changes recommended. Any score-moving change is tripwire-1 and requires full
regression before publish.

---

## Part 1 — מחמאה, Researched

### What it is in Israeli food labeling

מחמאה (pronounced _makh-mah_) is the Israeli commercial term for **imitation butter**
or **compound fat shortening**. On labels it appears as one of:

- `מחמאה (שומנים מוקשים מן הצומח)` — the explicit declaration: "imitation butter
  (hardened vegetable fats from plant sources)"
- `שומנים מוקשים מן הצומח` alone — the fat description without the trade name
- `מרגרינה` — margarine (the generic term, though מחמאה is specifically the
  butter-substitute formulation common in Israeli baking)

These are not the same substance as חמאה (butter). חמאה is dairy fat: cream separated
from milk, with naturally-occurring saturated fatty acids, CLA, vitamins A/D/K2, and
dairy-specific fat structures. מחמאה is an **industrially restructured fat product**
made from vegetable oils (typically palm or soybean or cottonseed oil) that have been
subjected to one of two industrial hardening processes:

**1. Partial hydrogenation** — the older method: molecular hydrogen is added to unsaturated
fatty acid chains under catalyst pressure, converting cis double bonds to trans
configuration. This produces trans fatty acids (primarily elaidic acid, C18:1 Δ9t).
Israeli regulations now restrict total trans fat to <2% of total fat in finished foods
(MoH Order 2014), but partially-hydrogenated products may still exist in older
formulations, and the label declaration `שומן/שמן צמחי מוקשה` (singular) or
`שומנים מוקשים` (plural) covers both partial and full hydrogenation.

**2. Interesterification** — the modern replacement: fatty acid chains are rearranged
among triglyceride molecules using chemical (sodium methoxide) or enzymatic catalysts.
This changes the positional distribution of fatty acids at the sn-1, sn-2, and sn-3
positions of the glycerol backbone without necessarily producing trans fatty acids.
Interesterified vegetable fats are increasingly common as the trans fat replacement in
Israeli biscuit and pastry manufacturing.

**Label legibility on Israeli biscuits:** Many Israeli biscuit labels declare
`שומנים מוקשים מן הצומח` without specifying whether the process is partial
hydrogenation or interesterification. The plural `שומנים מוקשים` (hardened fats,
plural) is the dominant form seen on Shufersal-sourced biscuit labels; the singular
forms the engine currently detects are less common.

---

### Nutritional profile vs. חמאה

| Attribute | חמאה (butter) | מחמאה (hardened vegetable fat) |
|---|---|---|
| Fat type | Natural dairy fat, ~80g/100g | Restructured plant fat, ~75-82g/100g |
| Saturated fat | ~50-55g/100g (dairy-origin: lauric, myristic, palmitic, stearic in natural proportions) | ~40-55g/100g (palm-dominant: palmitic acid enriched, especially sn-2 position in interesterified forms) |
| Trans fat | Natural dairy trans (CLA, vaccenic acid) — distinct metabolic profile from industrial trans (see EV-050) | May contain industrial trans fat if partially hydrogenated; interesterified forms have near-zero trans but altered sn-2 palmitate structure |
| Micronutrients | Vitamins A, D, K2; CLA | None (stripped in processing); may add synthetic vitamins/color |
| Processing class | NOVA 1 (single-ingredient animal fat) | NOVA 4 / heavily processed (multi-step industrial fat restructuring + additives) |
| Functional additives | None | Typically includes emulsifiers (lecithin, mono/diglycerides), color (beta-carotene or synthetic), flavor, sometimes water and milk powder |

---

### What does the evidence actually say about interesterified fat?

Evidence quality must be stated honestly, per Hard Rule #6.

**On partially hydrogenated fat (industrial trans fat) — Evidence: Strong**

The evidence that partially-hydrogenated vegetable oil (PHVO) causes cardiovascular harm
is among the strongest in nutritional epidemiology. The mechanism is well-characterized:
industrial trans fat (elaidic acid) suppresses HDL-C while raising LDL-C, promotes
endothelial inflammation, and impairs membrane fluidity. The dose-response is linear
with no safe threshold per WHO (2018) and EFSA (2019) — both call for elimination from
the food supply. The AHA Presidential Advisory (Sacks et al., Circulation 2017) treats
industrial trans fat as straightforwardly harmful. Israel's trans fat restriction (MoH
2014) reflects this consensus.

**On interesterified fat as PHVO replacement — Evidence: Moderate/Mixed**

The picture is more complicated, and intellectual honesty requires stating this.

An early crossover RCT (Sundram et al. 2007, published as a comment to Am J Clin Nutr)
compared palm olein, partially-hydrogenated soybean oil, and interesterified fat in
30 volunteers over 4-week periods. Both the trans-rich fat AND the interesterified fat
significantly elevated the LDL/HDL ratio and fasting blood glucose relative to palm
olein, suggesting that replacing trans fat with interesterified fat was not a clean
solution.

A 2020 review (Destaillats et al., PMC5497165) noted that interesterification changes
the positional distribution of palmitic acid — moving it into the sn-2 position of
triglycerides. Sn-2 palmitate is absorbed differently: it is not saponified by pancreatic
lipase in the same way as sn-1,3 palmitate, and animal studies (notably mouse models)
showed impaired glucose homeostasis and liver fat accumulation with interesterified palm
oil diets.

A 2024 systematic review (van Rooij et al., PMC7146500) examined the evidence on
palmitic vs stearic acid interesterification and cardiometabolic risk markers. Their
conclusion: interesterification of palmitic acid-rich fats does not appear to significantly
affect fasting serum lipids, but evidence is limited by small sample sizes and short
duration.

A 2025 RCT (published PMC12799373) in 51 healthy adults — the largest and most recent
controlled trial — compared 6-week diets with palmitic acid-rich vs stearic acid-rich
interesterified fats at 10% energy intake. Primary outcome: total:HDL cholesterol ratio.
The finding: no significant difference in cardiometabolic markers between the two arms,
and neither arm showed alarming signals versus baseline. This is the most rigorous recent
evidence, and it tempers the earlier Sundram concern.

**Honest evidence-tier summary for interesterified fat specifically:**

| Claim | Evidence Tier | Notes |
|---|---|---|
| Partially-hydrogenated fat (industrial trans) is harmful | Strong | Mechanistically clear, multiple large cohorts, regulatory consensus worldwide |
| Interesterified fat raises LDL/HDL ratio | Weak-to-Moderate | Early RCT (Sundram 2007) positive finding; more recent larger RCT (2025) did not replicate; conflicting |
| Interesterified fat impairs glucose homeostasis | Insufficient (human) | Animal models positive; human RCT evidence negative or mixed; cannot extrapolate |
| Interesterified fat is nutritionally equivalent to butter | Insufficient | Absence of harm evidence ≠ equivalence; no micronutrients, no CLA; palm-dominant FA profile; processing class NOVA 4 |
| מחמאה is nutritionally worse than חמאה at the structural level | Moderate | NOVA class, processing indicators, additive burden, and absence of dairy micronutrients establish inferior food architecture even absent confirmed cardiovascular outcome data |

---

### The correct framing for Bari

Bari scores nutritional architecture, not health outcomes (Hard Rule #5). The correct
framing is not "interesterified fat causes heart disease." The correct framing is:

1. מחמאה is a highly processed industrial fat product (NOVA 4 indicator) substituting
   for a whole-food fat ingredient.
2. Its use signals cost reduction over ingredient quality — a formulation choice, not
   an outcome claim.
3. The fatty acid profile is palm-dominant, high in saturated fat, with no dairy
   micronutrients or beneficial lipid fractions (CLA, vitamins).
4. Products that use מחמאה instead of חמאה in a category named "butter cookies"
   (`עוגיות חמאה`, `בטעם חמאה`) are presenting a cheaper processed-fat product under
   a quality-ingredient label.
5. This is **worse than using palm oil alone**, because palm oil at least declares itself
   honestly. מחמאה is a compound product that typically carries additional emulsifiers,
   color, and flavor to mimic butter — it is a formulation built for cost, not nutrition.

---

## Part 2 — Does the Engine Currently Punish It?

**Verdict: No. The engine is essentially blind to מחמאה.**

### What fires on a מחמאה product today

On a product like ביסקוטי — החוש השישי (barcode 7290017898506, score 47.7/D):

- `has_phvo: false` — PHVO detector missed entirely (see below)
- `fat_quality: 87` — rated as HIGH quality fat (engine scored the sat-fat ratio as good
  because sat_fat = 4g/fat = 22g → ratio = 0.18, which is low and scores as "good")
- `additive_quality: 100` — perfect additive score (ingredient truncation meant zero
  additives detected at all)
- The score of 47.7/D is driven by sugar red label + HP penalty, NOT by any hardened-fat
  signal. The fat dimension actually HELPS this product.

This is a signal inversion: a product using industrial hardened fat receives near-perfect
fat quality and perfect additive scores.

### Root cause 1: Ingredient truncation (16/58 products)

Sixteen of 58 products in run_cookies_004 show `ingredient_count == 1`, meaning the
ingredient parser captured only the first token (e.g., `קמח חיטה (`) before the opening
parenthesis and stopped. The entire ingredient list — including any מחמאה,
`שומנים מוקשים`, emulsifiers, colors, and flavors — is invisible to L3 signal detection.
This is a separate data/parser bug from the scoring logic gap. Products affected include
ביסקוטי (7290017898506), עוגיות בטעם חמאה (311128), פתי בר קלאסי (74184), and 13 others.

**This is the first gap and it is upstream of scoring.** Even a perfect PHVO detector
cannot fire if the ingredient text is truncated to `קמח חיטה (`.

### Root cause 2: PHVO marker gap (signal_extractor.py:1122)

The `_PHVO_MARKERS` list at line 1122 contains four entries:

```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",    # hydrogenated vegetable fat (SINGULAR)
    "שמן צמחי מוקשה",     # hydrogenated vegetable oil (SINGULAR)
    "מוקשה חלקית",        # partially hydrogenated
    "partially hydrogenated",
]
```

Israeli biscuit labels commonly declare `שומנים מוקשים מן הצומח` (PLURAL — hardened
fats from plant sources) or simply `מחמאה`. Neither of these matches any entry in
`_PHVO_MARKERS`. The substring search `any(m in full_text for m in _PHVO_MARKERS)` will
always return `False` on these labels.

**Confirmed**: on the 42/58 products where ingredient text was not truncated, `has_phvo`
was `False` on every single product. Zero PHVO flags fired in the entire run_cookies_004
corpus of 58 products.

### What does fire correctly

The engine does detect some ingredient-level signals correctly when text is not truncated:

- `sweetener_detected: true` fires correctly on E965 (maltitol) — barcode 311463 — and
  caps to a sweetener tier C, limiting score to 70. This is correct behavior.
- `tax_named_concern_additives: ['cmc']` fires correctly on the gluten-free פתי בר
  products (7290109354972, 7290109354996) via CMC/carboxymethylcellulose detection.
- `soy_lecithin` named detection fires correctly on multiple products including standard
  פתי בר lines.

The additive taxonomy (EV-041/043 glass box framework) functions correctly for the
additives it knows about, on products where ingredient text is available. The failure is
specifically: (a) truncation upstream, and (b) absence of מחמאה and the plural hardened-
fat terms from the PHVO vocabulary.

---

## Part 3 — Additive Knowledge, Not Additive Counting

The owner's directive is precise: the engine should reason like "this product uses
מחמאה AND strange additives, unusual for biscuits — that combination is the reason for
the penalty." This is a fundamentally different posture from the current model.

### Current model: count-based

`additive_quality` today is `100 - (additive_count × 18)`. Five categories → score 10.
Three categories → score 46. Zero categories → score 100. The score is indifferent to
WHICH additives are present. Soy lecithin (a phospholipid with a benign safety profile)
and CMC (a synthetic polymer with EFSA dose-dependent concern) each count as 1. מחמאה
doesn't count at all because it isn't in the additive vocabulary.

The D4 glass box framework (EV-041/043) already assigns qualitative tiers to 36 additives,
but this is annotate-only and does not move the headline score (by explicit policy
decision — TASK-179X engagement gate, demand-gated).

### Proposed named-additive severity tiers for fat quality

The right place to encode מחמאה is not in `additive_quality` but in `fat_quality` and
the PHVO detection chain, because מחמאה is fundamentally a fat-identity signal, not an
additive signal. The additive dimension handles E-numbers and functional molecules. מחמאה
is the fat SOURCE declaration.

However, the owner's broader ask — additive *knowledge* not just *counting* — does point
to a named-severity tier structure that should eventually exist across both dimensions.
Here is the proposed three-tier structure for the biscuit/cookie shelf specifically:

**Tier 1 — Structural Fat Fraud (severe; PHVO-class)**
- `מחמאה`, `שומנים מוקשים מן הצומח`, `שומן צמחי מוקשה`, `שמן צמחי מוקשה`, `מוקשה חלקית`
- These are not additives — they are the fat source itself, declared as industrial
  hardened vegetable fat.
- Why severe: NOVA 4 indicator; worst-in-class fat sourcing; misrepresents the product
  category (a "butter cookie" with no butter); established regulatory concern (trans fat
  regulation); even in interesterified form, represents the deliberate substitution of a
  whole-food fat with a refinery product.
- Score impact: PHVO cap / fat_quality floor (see Part 4).

**Tier 2 — Structural Processing Markers (moderate)**
- CMC (E466), DATEM (E472e), SSL (E481), modified starches (E14xx) in primary position
- These are functional additives that indicate industrial-scale structure engineering.
  Their presence in a biscuit is not automatically harmful, but it signals NOVA 4
  territory.
- Score impact: existing `additive_quality` count mechanism already handles some; the
  glass box D4 tiers (EV-043) classify these correctly as `dose-dependent` or `contested`.

**Tier 3 — Standard Baking Agents (benign)**
- Soy lecithin (E322), leavening agents (sodium bicarbonate E500, ammonium carbonate
  E503), vanilla extract, natural colors (beta-carotene E160a)
- These are functionally expected in biscuit manufacturing. Their presence alone should
  not penalize quality. Lecithin in biscuits is a standard emulsifier with an established
  safety profile at food doses.
- Score impact: minimal; current count-based mechanism somewhat over-penalizes these.

**The verdict logic the owner wants:**
"This product declares מחמאה — hardened vegetable fat — as a primary fat source. This
is atypical for quality biscuits. Combined with [specific additives], this product's fat
architecture is industrial, not natural. Penalty applies."

This requires the engine to know: (a) what מחמאה is, (b) what it signals about the
product's fat source, and (c) how to compose the score penalty from ingredient identity
rather than a raw count.

---

## Part 4 — Concrete Recommendation

### (a) Widen PHVO markers — exact change

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\signal_extractor.py`, line 1122

Replace:
```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",    # hydrogenated vegetable fat
    "שמן צמחי מוקשה",     # hydrogenated vegetable oil
    "מוקשה חלקית",        # partially hydrogenated
    "partially hydrogenated",
]
```

With:
```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",       # hydrogenated vegetable fat (singular)
    "שמן צמחי מוקשה",        # hydrogenated vegetable oil (singular)
    "שומנים מוקשים",          # hardened vegetable fats (plural — dominant Israeli label form)
    "שומן מוקשה",             # hardened fat (generic singular, no "צמחי" qualifier)
    "מחמאה",                  # imitation/compound butter — Israeli trade term for hardened VF
    "מוקשה חלקית",            # partially hydrogenated
    "partially hydrogenated",
]
```

**False-positive gate required:** The bare `מוקשה` warning from the original comment
(risk of firing on `עמילן מוקשה` / modified starch) does NOT apply to `שומנים מוקשים`
(the plural fat form) or `מחמאה`. However, `שומן מוקשה` without the `צמחי` qualifier
does carry modest false-positive risk if a product mentions `שומן מוקשה` in a
non-fat-source context (unlikely on standard Israeli labels, but should be validated
against the full registered corpus before shipping).

**Validation required before shipping:** Run each new marker against all 7 live
category corpora + the full cookies corpus. Report any hits. Expected: the new markers
fire on the 2+ biscotti products known to declare מחמאה; zero fires on non-fat-source
contexts.

### (b) מחמאה/PHVO severity rule — recommended cap and justification

**Recommended: add a `PHVO_IDENTIFIED` cap at 45.**

Justification:
- The `ISRAELI_RED_LABELS_2_PLUS` cap (sugar >17.5g AND sat_fat >5g) is already 45.
  This is Bari's current "worst combination we can observe from the label" floor for
  biscuits.
- מחמאה is categorically worse than two red labels together because it is a fat-source
  identity signal, not a nutrient-quantity threshold signal. A product can be red-labeled
  on sugar and sat-fat by using quality ingredients in rich formulations. A product that
  uses מחמאה has made a cost-over-quality choice at the fat-architecture level.
- However, the evidence for setting מחמאה worse than, say, a NOVA 4 ultra-processed
  product (cap 87.2, which effectively limits scores to ~mid-range when combined with
  other penalties) is not strong enough to justify a more aggressive cap than 45. The
  owner's "severely punish" directive is met at 45, which maps to D — the same grade
  as the existing worst-case biscuit composition.
- The cap should fire when `has_phvo == True` (after the marker widening above), regardless
  of whether the product also has red labels.
- **Do not set this cap below 45.** A cap lower than 45 (e.g., 35) would mean מחמאה
  alone produces an E grade before any other signal fires. That is possible to justify
  if the owner wants it, but it would affect grade distribution significantly and requires
  an explicit owner ruling. The 45 cap + existing penalty stack (HP penalty, sugar cap,
  etc.) will typically drive affected products to D or E through the combined effect —
  the cap does not need to be the sole driver.

**Naming convention:** Register this as `PHVO_IDENTIFIED` in the caps table in
`score_engine.py`, tied to `has_phvo == True` in `evaluate_guardrails`.

**Implementation note:** The cap applies in `evaluate_guardrails`, the same block where
`ISRAELI_RED_LABELS_2_PLUS` fires. It is additive with red-label caps (the binding cap
is always the lowest applicable cap).

### (c) Fat quality floor for מחמאה

In addition to the cap, `fat_quality` should receive a named floor (i.e., ceiling for
the fat dimension — no higher than a defined maximum) when `has_phvo == True`. Current
behavior: the ביסקוטי product received `fat_quality: 87` because sat-fat fraction (0.18)
is low and no PHVO fired. With the widened markers, `has_phvo` would fire and `fat_quality`
should be capped at 40 (below the sat-fat neutral of 50) to reflect that the fat is
structurally industrial regardless of the sat-fat ratio. The sat-fat ratio is not a
reliable indicator of fat quality when the fat source is industrial hardened vegetable oil.

**Recommended fat_quality rule when has_phvo == True:**
- `fat_quality = min(fat_quality_computed, 40)` — PHVO products cannot score above 40
  on fat quality.
- This mirrors the logic of EV-050: fat source identity overrides the nutrient-ratio
  calculation. For dairy fat (butter), the EV-050 exemption gates the trans-fat veto;
  for hardened vegetable fat, the PHVO flag should gate the fat-quality ceiling.

### (d) Ingredient truncation — separate fix, equally urgent

The PHVO detection improvement is irrelevant for the 16/58 products with truncated
ingredient lists (ingredient_count == 1). These products run through the engine with
no ingredient signal at all, producing systematically incorrect additive quality (100)
and PHVO status (False). Fix required upstream in the ingredient parser.

This is a data pipeline issue (BSIP0/scrape layer), not a scoring logic issue. It
predates this ruling and is not governed here — but it must be flagged as a dependency.
If ingredient text is not fixed for these 16 products, the PHVO detection improvement
will not reach them even after the marker widening is implemented.

### (e) Tripwire confirmation

Any implementation of (a), (b), or (c) above is **tripwire-1** (touches scoring logic
that would move published or in-flight scores). Required before any publish:

1. `engine_invariants.py` 342-case suite — must pass with zero new failures.
2. Golden-corpus byte-identity check on all 7 live categories (milk, yogurts, breads,
   salty snacks, cereals, snack bars, brined cheeses). None of these products should
   contain מחמאה or `שומנים מוקשים` — confirm zero hits before running to be sure.
3. Full re-score of the cookies corpus with the new markers active — publish grade
   distribution delta showing which products moved and why.
4. Bleed simulation: run each new marker string against the full registered corpus of
   all live categories. Expected zero fires. Document the result.
5. EV-059 registration in `bsip2_evidence_registry_v1.md` citing this ruling as the
   scientific basis + D7 co-sign from both Nutrition Agent (this document) and Product
   Agent before any code ships.

**This document is the Nutrition Agent side of the D7 co-sign. Product Agent D7 must
co-sign before implementation begins.**

---

## Part 5 — Verdict on Engine Maturity

The owner's aspiration — "from all the products I've seen in biscuits, this one uses
very strange additives and מחמאה, and that's why I'm going to punish it" — describes
a two-part engine capability:

1. **Named ingredient recognition** — the engine must know what מחמאה is, not just
   count it.
2. **Contextual abnormality detection** — the engine must know that מחמאה is unusual
   for biscuits, so its presence is signal-amplifying (it's not just a default biscuit
   ingredient, it's a quality-revealing choice).

This ruling solves (1) completely: widening the PHVO markers + naming the מחמאה term
gives the engine the vocabulary to recognize and penalize it.

(2) is a more sophisticated capability — contextual baseline for what "normal" ingredients
look like in the biscuit category, so that unusual ingredients stand out. This is
architecturally possible (it is essentially what D4's "disclosure gap" tier tries to do
for individual additives), but implementing it for the fat source layer is a future
milestone, not part of this ruling. It does not block the marker widening.

The current implementation path is: (a) fix ingredient truncation → (b) widen PHVO
markers → (c) add cap 45 + fat_quality ceiling 40 when has_phvo fires → (d) register
EV-059 + co-sign. This delivers the verdict the owner wants: a product with מחמאה
gets punished, and the trace shows exactly why.

---

## Return Contract

```json
{
  "task": "TASK-275",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/cookies_coffee_additive_depth_ruling_v1.md",
      "sha256": "aa3386d04b5668889e59aff87065475091fd6f05cb0dcdede1f0de8e3c305509"
    }
  ],
  "counts": {
    "products_total_run_cookies_004": 58,
    "products_truncated_ingredient_count_1": 16,
    "products_with_phvo_fired": 0,
    "products_with_additive_taxonomy_hits": 29,
    "phvo_markers_current": 4,
    "phvo_markers_proposed": 7,
    "new_markers_added": ["שומנים מוקשים", "שומן מוקשה", "מחמאה"],
    "proposed_phvo_cap": 45,
    "proposed_fat_quality_ceiling_when_phvo": 40,
    "evidence_tiers_assigned": {
      "partially_hydrogenated_PHVO_harm": "Strong",
      "interesterified_fat_LDL_HDL": "Weak-to-Moderate",
      "interesterified_fat_glucose_homeostasis_human": "Insufficient",
      "machma_architecturally_inferior_to_butter": "Moderate"
    },
    "parts_in_ruling": 5,
    "tripwires_confirmed": 1,
    "live_categories_in_regression_scope": 7,
    "d7_co_signs_required": 2,
    "d7_co_signs_complete": 1
  },
  "commands_run": [],
  "not_done": [
    "Product Agent D7 co-sign — required before any implementation",
    "EV-059 registration in bsip2_evidence_registry_v1.md",
    "engine_invariants.py 342-case suite re-run (tripwire-1)",
    "PHVO marker widening implementation (signal_extractor.py:1122) — blocked on D7 co-sign",
    "PHVO_IDENTIFIED cap implementation in score_engine.py evaluate_guardrails — blocked on D7 co-sign",
    "fat_quality ceiling implementation when has_phvo==True — blocked on D7 co-sign",
    "Ingredient truncation fix (16/58 products, upstream parser/BSIP0 layer) — separate task, not scored here",
    "Bleed simulation: new markers against all 7 live category corpora",
    "Full re-score of cookies corpus with new rules active + grade distribution delta",
    "Consumer-facing copy for מחמאה verdict lines — blocked on score changes + Content Agent"
  ],
  "self_check": {
    "conclusion_stated_first": true,
    "evidence_tiers_named_for_all_claims": true,
    "no_health_claims_made": true,
    "no_score_changes_without_d7": true,
    "no_bsip_nova_terminology_in_consumer_copy": true,
    "off_ban_respected": true,
    "frozen_invariants_untouched": true,
    "tripwire_1_confirmed": true,
    "single_recommendation_no_menu": true,
    "product_agent_d7_required_confirmed": true,
    "ingredient_truncation_flagged": true,
    "proposed_status_returned_not_closed": true
  }
}
```
