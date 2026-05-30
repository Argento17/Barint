# Current Architecture Tensions

**Purpose:** Identify and articulate the unresolved conceptual tensions in the BSIP2 architecture. Each tension is real — not a bug to be fixed immediately, but a design choice with inherent tradeoffs that the system must eventually resolve or explicitly accept.

This document does not propose solutions. It makes tensions legible so they can be managed consciously rather than accumulated silently.

---

## Tension 1 — NOVA vs. Engineering Intensity

**The tension:**
BSIP2 uses NOVA as its primary processing signal, but NOVA is a classification system designed for epidemiological research, not for per-product analytical scoring. NOVA 4 is a broad category that includes: ultra-processed snacks, heavily engineered protein supplements, artisan fermented cured meats, certain breakfast cereals, commercial bread, and many other structurally diverse products. Within NOVA 4, a product with six synthetic additives and a product with two preservatives and one stabiliser are indistinguishable.

BSIP2 adds additive burden markers to provide granularity within NOVA levels — this partially addresses the problem. But the relationship between NOVA classification and the additive marker system is not fully resolved: a product can be NOVA 4 with few additive markers (novel processing without additive indicators) or NOVA 3 with many additive markers (inconsistency in the inference approach).

**Why it matters:**
If NOVA proxy classification and additive burden markers disagree, the system applies both penalties through the PROCESSING_LOAD concern family coordination — the strictest cap survives. This is architecturally correct but may produce outcomes where the additive marker signal dominates the NOVA signal for reasons that are not analytically transparent.

More broadly: NOVA is a population-level tool. Applying it as a product-level quality proxy embeds its limitations into BSIP2. The limitations are known (NOVA doesn't account for food matrix; NOVA 4 is heterogeneous; NOVA inference from ingredients is proxy-dependent) but are not currently surfaced in scoring output.

**Proposed future direction:**
Develop an Engineering Intensity metric that is derived directly from ingredient markers rather than mapped from NOVA. Engineering Intensity would measure the degree to which a product's composition requires industrial processes that cannot be replicated in a home kitchen — regardless of NOVA category. NOVA would remain an input signal, not the primary processing dimension. This separates "degree of processing" (NOVA) from "quality of processing" (Engineering Intensity) — a distinction BSIP2 currently conflates.

---

## Tension 2 — Hyper-palatability vs. Satiety

**The tension:**
Hyper-palatability (HP) and satiety are both attempting to measure a product's relationship with the consumer's regulatory mechanisms — but from opposite directions. HP patterns identify combinations that override normal appetite regulation (engineered reward). Satiety signals identify the presence or absence of structural properties (protein, fiber) that support appetite regulation.

The two mechanisms are analytically distinct in BSIP2: HP runs through the guardrail layer (penalty rules, family budget clamp); satiety runs through both the satiety support dimension (6% weight) and the low-satiety guardrail rules (high-calorie-low-protein-fiber penalties). But they can fire on the same product for overlapping reasons: a high-fat, high-sugar, low-fiber snack bar may trigger HP_FAT_SUGAR_COMBO (high reward) AND HIGH_CAL_LOW_SATIETY_SOFT (low satiety signals). These are different mechanisms but may describe the same structural problem — that the product is designed to drive consumption without providing satiation.

The concern coordination system assigns HP patterns to the `hyper_palatability` family and low satiety to `CALORIE_LOAD`. They are treated as independent concerns. But the underlying reality may be that they are two analytical views of the same single concern: this product will make you eat more and leave you unsatisfied.

**Why it matters:**
If HP and satiety penalties accumulate independently on the same product, the concern coordination system is not preventing a form of double-counting — just not within the same concern family. The two mechanisms can each individually be justified, but their interaction may produce an overly punitive combined result.

Additionally: HP patterns are calibrated for engineered products. A whole-food product with naturally high fat and naturally low fiber (e.g. macadamia nuts) triggers no HP penalty despite matching the compositional pattern. The matrix distinction is currently embedded in the threshold values — but this implicit assumption is not architecturally explicit.

**Proposed future direction:**
Consider whether HP and low-satiety signals should be evaluated as a combined consumption-pattern dimension rather than two separate penalty mechanisms. This would require defining the structural question more precisely: "Does this product's composition support or subvert normal consumption regulation?" — and answering it with a single analytical signal rather than two overlapping penalty chains.

---

## Tension 3 — Hard caps vs. Continuous scoring

**The tension:**
BSIP2 uses two scoring mechanisms that operate on fundamentally different principles: dimension scoring is continuous (a dimension score can be any value 0–100, producing smooth gradients); guardrail caps are binary (they fire at a threshold and impose a hard ceiling, producing score cliffs).

The two mechanisms serve different purposes: dimension scoring evaluates nutritional quality along a spectrum; caps enforce structural floors below which a product cannot be graded regardless of other signals. Both are philosophically defensible. But they exist in the same score, and a consumer or analyst reading the final score cannot distinguish between "this product scored 62 because its continuous dimension scores average to 62" and "this product scored 62 because a hard cap forced it there despite its dimensions averaging higher."

The cliff-threshold problem (FM-04) is a direct consequence of binary caps: a product at 499 kcal is analytically indistinguishable from one at 501 kcal in dimensional terms, but a guardrail fires on one and not the other.

**Why it matters:**
Binary caps introduce discontinuities that undermine the precision claim of the scoring system. If the score is supposed to carry meaningful information across its range (a 58 and a 62 are analytically different), then a threshold that forces many products to exactly 60 or exactly 55 is eroding that information.

More practically: caps make the score gameable in a specific direction. A manufacturer reformulating to 499 kcal has made no nutritional change of consequence but escaped a binding cap. If caps are binding and visible in the market, they create reformulation targets that do not correspond to genuine quality improvements.

**Proposed future direction:**
Consider whether the guardrail layer should shift toward steep-gradient continuous penalties near threshold values rather than binary fire/no-fire caps. This would preserve the "structural floor" concept while reducing cliff behaviour. For example, instead of "score ≤ 60 if kcal ≥ 500 AND sugar ≥ 25g," a continuous penalty that begins at 470/20g and deepens sharply through 500/25g would produce a smoother but still-decisive quality signal. This is a significant architectural change — it would require redesigning the guardrail layer and is not appropriate for the current specification phase.

---

## Tension 4 — Punishment-heavy vs. Nourishment-aware scoring

**The tension:**
The current BSIP2 architecture is primarily structured around negative signals: caps, penalties, concern coordination, family budgets, confidence ceilings. The positive contribution of nutritional signals is encoded in dimension scores (which are bounded at 100 and weighted at their assigned fraction) — but the guardrail layer adds only downward pressure. There are no guardrail bonuses, no structural positive caps that lift a score above what dimension scoring would produce.

This architecture encodes a particular analytical philosophy: food quality is assessed by ruling out concerns, not by accumulating virtues. The score is, in effect, "100 minus the aggregate of what is wrong." This is not stated explicitly in the specification.

**Why it matters:**
A scoring system designed primarily to identify failure modes will systematically produce lower scores for products with unusual profiles that don't fit the failure patterns — even when those products are genuinely excellent. The system is calibrated to detect problems; it has limited machinery to express strength.

More subtly: a product that simply has no detectable problems — plain oats, plain almonds — will score well not because the system recognises their nutritional excellence, but because nothing bad fires. The positive signal (whole grain, whole food, high fiber) is expressed through dimension scores, but there is no architectural mechanism that reads "this is an unusually excellent food structure" as a distinct positive signal.

The result is that the score ceiling for genuinely excellent products is determined by how well they avoid penalties — not by how much they deliver. This may be the right architecture for a comparative tool, but it should be a conscious choice, not an accidental one.

**Proposed future direction:**
Define whether BSIP2 should remain primarily a penalty-avoidance scoring system or whether a future version should introduce positive structural signals — "nourishment markers" — that can lift dimension scores for products with specifically valuable structural properties (complete protein from whole food, prebiotic fiber from whole grain, diverse micronutrient profile from varied whole ingredients). This would shift BSIP2 from "what is wrong with this food" toward "what does this food do for you and what concerns does it carry" — a more complete analytical framing.

---

## Tension 5 — Rule complexity vs. Explainability

**The tension:**
BSIP2 currently contains: 11 dimensions with individual scoring formulas; 6+ concern families with coordinator logic; 20+ individual guardrail rules across caps and penalties; supporting evidence factors; family budget clamps; floor rules; confidence ceilings; NOVA proxy classification with marker inference; 4 hyper-palatability patterns; category-specific calorie threshold tables across 8 categories; and context-sensitive routing for ISRAELI_RED_LABEL_1.

Each element was added for a defensible reason. The result is a system that can produce a score for almost any product with available data. But the score is produced by a rule stack that no individual can fully hold in working memory — including the people who designed it.

**Why it matters:**
A scoring system that cannot be explained clearly and simply to a user has limited value as a transparency tool. If a user asks "why did this product score 54?" and the answer requires tracing through concern coordination, family budget clamping, and the interaction between NOVA proxy classification and additive marker overlap, the explanation has failed its purpose.

More structurally: rule complexity accumulates in one direction. Rules are added; they are rarely removed. Each new edge case generates a new rule. Over time, the system becomes a layer cake of corrections and exceptions rather than a coherent analytical framework. The concern was explicitly identified in the strategic guidance: Bari should not become "NOVA with more math."

The current freeze is an appropriate moment to assess whether the current rule set has crossed the complexity threshold at which it can no longer be explained without a reference document open.

**Proposed future direction:**
Establish an explicit rule budget: a maximum number of guardrail rules per concern family, enforced at the architecture level. When a new rule is proposed, an existing rule must either be retired or the threshold for the existing rule must be adjusted. This prevents rule explosion and forces the system to remain interpretable.

Additionally: develop a one-page explainability contract — a document that defines what level of explanation BSIP2 must be able to produce for any given score, in plain language, without reference to internal rule identifiers. If the system cannot produce that explanation, the rule that prevents it is a candidate for removal or simplification.
