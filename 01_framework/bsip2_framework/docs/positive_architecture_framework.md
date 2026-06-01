# Positive Architecture Framework

**Purpose:** Define how Bari may eventually recognise positive food structure — not merely the absence of penalties. This is a conceptual document. No scoring formulas are proposed here. The goal is to articulate the problem clearly enough that a future version of BSIP2 can solve it without introducing new ideological commitments.

---

## The asymmetry problem

The current BSIP2 architecture is designed to detect and penalize structural concerns. Its guardrail layer is entirely composed of caps and penalties. Its confidence layer is a ceiling. Its whole-food floors are the only positive structural signals — and even those are framed as protective minimums ("a product cannot score below X") rather than positive recognitions of structural quality ("a product with these properties scores higher because of what it contributes").

The result is a system that evaluates food primarily by what it fails to do. A product scores well not because the system recognizes that it is nutritionally excellent but because nothing fires against it.

**The oats case:** Plain rolled oats score well in BSIP2. Why?
- The processing quality dimension scores NOVA 1 well
- The calorie density dimension scores ~380 kcal/100g well in the `cereal` category
- The fiber content contributes positively to the satiety support dimension
- No sugar rules fire; no additive rules fire; no sodium rules fire

This is correct. But it is produced by the *absence of firing* rather than by a positive recognition that: oats have an intact grain matrix; their fiber is structurally complex (beta-glucan); their protein is nutritionally complete for a grain; their calorie-to-fiber ratio is excellent by any reasonable standard. BSIP2 does not "know" any of this — it only knows that oats don't fail.

---

## Why absence of negatives is insufficient

**The low-calorie engineered product problem:**

A diet jelly dessert at 15 kcal/100g with artificial sweeteners, stabilisers, and modified starch may avoid many penalties — it has negligible calories, negligible sugar, negligible fat. If the NOVA proxy inference misses its processing level, it faces only the sweetener cap (70 ceiling). The score could be 65–68.

Plain rolled oats score 75–85.

The gap is correct but the reasoning is not: oats score 10–20 points higher not because the system recognizes oat's food matrix quality but because more rules fire against the diet jelly. If an engineered product is well-designed to avoid rules, it closes the gap not by becoming nutritionally better but by engineering around penalty triggers.

**The concern:**

A scoring architecture that cannot distinguish "this product delivers genuine nutritional value in a structurally intact form" from "this product has managed to avoid triggering our detection rules" is not robust. It will be increasingly gamed as the rule set becomes known.

**The deeper concern:**

This architecture encodes a philosophy of surveillance rather than recognition. Food quality is detected by finding problems, not by finding value. This produces a system that is better at flagging bad food than identifying good food — and good food identification is ultimately more useful to a consumer.

---

## Concepts for a positive architecture

The following concepts describe what a positive evaluation layer might measure. None of these are implemented; they are design-space exploration.

---

### Food matrix integrity

**What it means:** The degree to which a product's nutritional components remain in their original structural relationship to one another — embedded in the food matrix as they occur in nature rather than separated, purified, and recombined.

**Examples:**
- Oats: grain matrix intact; starch, protein, and fiber physically co-located
- Oat flour: matrix partially disrupted; fiber still present but starch surface area dramatically increased
- Oat protein isolate: matrix destroyed; protein extracted and concentrated; fiber absent
- Extruded puffed oats: matrix restructured through heat and pressure; cell walls disrupted; glycemic behaviour altered

Food matrix integrity is not the same as NOVA classification — it is a more granular property. A product can be lightly processed (NOVA 2) with high matrix integrity (minimally ground) or lightly processed with low matrix integrity (puffed, extruded, expanded). The relationship between processing and matrix integrity is imperfect.

**Why it matters:** The food matrix determines how nutrients are metabolically available, how quickly they enter the bloodstream, and how they interact with the digestive system. Two products with identical macronutrient declarations can have very different metabolic effects because their matrix integrity differs.

**What it is not:** A synonym for "unprocessed." Fermented foods have substantially altered matrices — yogurt has no intact milk matrix — but fermentation produces structural properties (microbial activity, altered proteins, beneficial acids) that are nutritionally positive.

---

### Structural satiety

**What it means:** The degree to which a product's structure — not merely its macronutrient content — supports satiety. Structural satiety accounts for: fiber type and density; protein source and bioavailability in context; fat quality and physical form; and water content.

**Examples:**
- An apple at ~50 kcal/100g produces significantly more satiety than apple juice at ~45 kcal/100ml — identical calorie content, different structural satiety due to intact fiber and chewing requirement
- Whole almonds produce more satiety than almond oil at lower calorie equivalence — structural fat behaves differently from purified fat
- Yogurt with intact protein produces more satiety than a whey isolate shake at the same protein content — protein context and matrix matter

**The distinction from the current satiety dimension:** BSIP2's satiety support dimension scores protein and fiber quantity. It does not distinguish between protein in a whole-food context and protein in an isolate, or between intact dietary fiber and added soluble fiber. Structural satiety is a richer concept.

**What it is not:** A simple proxy for calorie density or fiber content.

---

### Whole-food coherence

**What it means:** The degree to which a product's ingredient composition represents a recognisable food structure rather than a reconstruction of food components. A product is coherent if its ingredient list reads as "ingredients" rather than "components used to build the appearance of food."

**Examples of high coherence:**
- Tahini: sesame seeds (possibly roasted), optional salt — the product is sesame seeds in paste form; all nutritional properties are present in their natural relationship
- Greek yogurt: milk, live cultures — the product is fermented milk; the structural relationship is intact

**Examples of low coherence:**
- A protein bar: whey protein isolate, chicory root fiber, palm kernel oil, cocoa powder, erythritol, glycerol, sunflower lecithin, flavourings — each component is an extracted fraction of a food, recombined to approximate the macronutrient profile of a nutritionally acceptable product; no original food matrix is present
- An ultra-processed cereal: refined wheat flour, sugar, maltodextrin, modified maize starch, iron sulphate, niacinamide, thiamine mononitrate — grain rebuilt from its processed components, with remediation additives added

**What it is not:** A rule against complexity. A stew is complex but coherent — it combines recognisable whole foods. An engineered protein product may have fewer ingredients but exhibit low coherence if each ingredient is a processed fraction.

---

### Fermentation as structural value

**What it means:** Fermentation transforms a food matrix in ways that BSIP2 should eventually credit, not merely tolerate. Current BSIP2 architecture is neutral-to-negative on processing; fermentation is processing of a specific type that has distinct structural properties.

**Fermentation properties relevant to food quality evaluation:**
- Microbial metabolite production (short-chain fatty acids, organic acids, B vitamins in some ferments)
- Protein structural changes that improve digestibility
- Anti-nutrient reduction (phytate reduction in fermented grains)
- Probiotic microbial presence (live cultures in yogurt, kefir)
- Preservation without synthetic additives

**The NOVA problem with fermentation:**
Traditional fermented foods (kefir, yogurt, miso, tempeh, kimchi, sauerkraut) are NOVA 1–2 at most. The NOVA framework handles fermentation reasonably at the classification level. But the current BSIP2 processing quality dimension scores NOVA 1–2 well because nothing fires against them — not because fermentation is recognized as positive. A future positive architecture should explicitly credit fermentation as a structural value, not merely fail to penalize it.

---

### Meaningful protein density

**What it means:** Protein quantity that is functionally significant in the context of the product's calorie delivery and typical serving size. Not all protein is equivalent:
- A product with 15g protein/100g at 100 kcal/100g delivers excellent protein density
- A product with 15g protein/100g at 550 kcal/100g delivers protein at the cost of significant calorie load
- A product with 6g protein/100g from a whole-food matrix (legumes, whole grains) delivers protein in a context with complementary fiber and micronutrients
- A product with 6g protein/100g from whey isolate delivers the same protein amount in an engineered context with no complementary structure

**What the current system captures:** Total protein quantity in the nutrient density and protein quality dimensions; the protein isolate penalty in the protein quality dimension. It does not capture protein-to-calorie efficiency as a standalone positive signal.

---

### Meaningful fiber density

**What it means:** Fiber content that is structural rather than supplemental — fiber that comes embedded in the food's natural matrix rather than added as an extracted soluble fiber to improve a product's nutritional appearance.

**Examples:**
- Oat beta-glucan: naturally occurring in the grain; structurally embedded; metabolically specific
- Added chicory root inulin: extracted soluble fiber added to a product; a legitimate fiber source but a different structural signal from intact grain fiber
- Pectin from apple: may be naturally occurring in apple-based products or added from extracted apple pomace

**Why it matters:** "12g fiber" on a label is an observed fact (L1). What type of fiber, in what structural context, is a classification question (L3) that the current architecture does not resolve. A positive architecture would distinguish structural fiber from supplemental fiber.

---

## The nourishment-present vs. concern-absent distinction

The most important conceptual shift a positive architecture represents:

**Current frame:** A good score means few concerns were detected.

**Future frame:** A good score means positive structural properties were detected AND few concerns were detected.

This is not a marginal distinction. The two frames produce very different results for:
- Low-calorie engineered products that avoid penalties without delivering value
- Novel food products (plant-based meats, novel protein sources) where structural quality cannot be inferred from absence of traditional negative signals
- Whole-food products where the positive properties are the point, not the absence of problems

The current architecture is appropriate for the current phase — it is based on well-evidenced concern signals with clear analytical justifications. Positive signals are harder to define rigorously and carry more risk of embedding normative positions. The right sequencing is: stabilize the concern layer first; design the positive layer with full understanding of what's already embedded.

---

## What this document does NOT do

- Propose new scoring dimensions
- Propose new positive bonus rules
- Define thresholds for any positive signal
- Create a "nourishment score" or parallel positive index

All of those are future decisions. This document establishes the vocabulary and conceptual frame for making those decisions well.
