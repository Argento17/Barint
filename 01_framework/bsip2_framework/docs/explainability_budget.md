# Explainability Budget

**Purpose:** Define the conceptual constraints on scoring complexity that must be respected to keep BSIP2 scores explainable to a human. A score that cannot be explained clearly — without requiring the user to understand 40 interacting rules — has failed as a communication tool regardless of its analytical precision.

---

## The explainability problem

BSIP2's current architecture contains:
- 11 weighted dimensions
- 20+ individual guardrail rules (caps and penalties)
- 6 concern families with coordination logic
- Family budget clamping for 10 penalty families
- 4 hyper-palatability patterns
- Category-specific scoring tables (8 categories)
- Confidence calculation with 10+ reduction factors
- Whole-food floors
- Context-aware routing (ISRAELI_RED_LABEL_1)

For most products, only a subset of these rules are active. For a simple product — plain oats — the effective rule set is small: calorie density table (cereal category), NOVA 1 processing quality, fiber contribution to satiety dimension. The rest are inactive.

For a complex product — a sweetened, NOVA 4 protein bar with multiple additives and red labels — many rules fire simultaneously. The final score is produced by their interaction through concern coordination, budget clamping, and confidence ceiling. At this complexity level, the score is not explainable without a reference document.

**The core tension:** The architecture needs enough rules to evaluate diverse products correctly. But more rules = less explainability. There is no resolution that doesn't require trade-offs. The explainability budget is how those trade-offs are governed.

---

## The explainability contract

**Principle:** For any product scored by BSIP2, it must be possible to produce a complete and honest explanation of why the score is what it is using at most three primary drivers and a short supporting context statement.

A primary driver is a signal that was singularly responsible for a significant portion of the final score — either a fired cap that is binding, a dimension with a score more than 15 points below average, or the confidence ceiling if active.

**Example of a valid explanation:**
> "Score: 52 (Grade D). Primary drivers: (1) Cap applied — sugar concentration of 28g/100g exceeds structural threshold; score ceiling is 60. (2) Processing quality dimension low — product shows ultra-processed characteristics. (3) Calorie density high for category — evaluated against snack bar thresholds. Supporting context: protein content is moderate; no red labels applied."

This explanation is complete, honest, and requires no knowledge of the scoring architecture to understand. It names the primary signals, identifies them as concerns rather than facts, and acknowledges a compensating positive.

**Example of an invalid explanation (complexity failure):**
> "Score: 52 reflects coordination of SUGAR_LOAD concern family (HIGH_SUGAR_25G_PLUS cap at 60, MULTIPLE_ADDED_SUGAR_MARKERS penalty −2 after coordination, HIGH_CAL_HIGH_SUGAR_SOFT penalty scaled at 40%), PROCESSING_LOAD (NOVA_PROXY_4_ULTRA_PROCESSED cap at 60 coordinated against ADDITIVE_MARKERS_3_PLUS cap at 65), family budget clamping applied to sugar family (budget 10, actual 7), calorie density dimension 28/100 in snack_bar_granola category, confidence ceiling not triggered (confidence 72, medium band)."

This is technically accurate. It is analytically complete. It is not explainable to a human without a reference document.

---

## Maximum complexity tolerances

These are proposed soft limits. They are not hard technical constraints — they are design governance principles.

**Cap rule limit per concern family:** ≤ 4 cap rules per concern family. Any family with more than 4 cap rules is a candidate for consolidation — either by removing a rule that duplicates an adjacent one, or by converting the stacked rules into a gradient.

**Active rules per product:** For any product scored, the number of guardrail rules (caps or penalties) that actually fire should ideally be ≤ 5. A product with 10+ rules firing is analytically correct but practically unexplainable. When a product hits this complexity level, the UI must surface the two or three dominant signals only, with a "see full analysis" option for users who want depth.

**Dimension contribution threshold for UI:** Only dimensions with a score more than 15 points from their neutral value (50) should be surfaced as primary signals in the default view. Dimensions close to 50 are neither a significant strength nor a significant concern — displaying them alongside high-signal dimensions obscures the important signals.

**Score delta attribution:** When comparing two products, the score gap should be attributable to ≤ 3 signal differences in the default comparison view. If the gap requires more signals to explain, the UI should aggregate them ("processing quality and additive burden account for 8 of the 12 point difference") rather than listing each rule.

---

## Dominant-driver explanation

**Concept:** Every score has a dominant driver — the single signal that contributes most to the score differing from a neutral baseline. The dominant driver should be identifiable from the score output without requiring full rule trace.

**How to identify the dominant driver:**

1. If a confidence ceiling is active, that is the dominant driver (it overrides everything else).
2. Otherwise, if a binding cap is active, the binding cap is the dominant driver.
3. If no cap is binding, the dimension with the highest deviation from its neutral value is the dominant driver.
4. If all dimensions are within 15 points of neutral, the score is primarily positive ("no significant concerns detected").

**The 80% rule:** In most cases, the dominant driver and one secondary signal together account for at least 80% of why the score is what it is, rather than the neutral value. If this is not true — if the score requires 6 signals of roughly equal weight to explain — the scoring architecture is too distributed to be explainable. This is a design failure, not a communication failure.

---

## Collapsing secondary rules in UI

**Principle:** Rules that fire as supporting evidence in the concern coordination system should not be surfaced individually in the UI. Only the primary signal (the winner in concern coordination) is surfaced for a given concern.

**Current behavior:** Concern coordination already selects a primary signal per concern family. The supporting signals are scaled down and their individual contribution is minor. The UI should follow the same logic: surface the primary concern, not the full list of rules that fired within it.

**Practical implementation concept:**
The scoring output record should include:
- `dominant_driver`: the primary signal (cap rule ID, dimension name, or confidence ceiling)
- `supporting_signals`: a list of ≤ 3 additional signals that are notable (not all that fired)
- `full_rule_trace`: the complete list of all rules that fired, stored but not shown by default

The UI reads `dominant_driver` and `supporting_signals`. The `full_rule_trace` is available for audit, developer inspection, and advanced users — not for the default product card.

---

## UI explainability constraints

**The product card (default view):**
- Score + grade
- Dominant driver (one sentence)
- ≤ 2 supporting signals (one phrase each)
- Category label
- Confidence level if below high

**The expanded view:**
- All dimension scores with labels
- Primary signals by concern family
- Confidence breakdown if relevant
- Category classification with confidence

**The full analysis view (developer/audit mode):**
- Complete rule trace
- All fired caps and penalties before coordination
- Coordination outcomes
- Family budget clamping outputs
- Full confidence calculation

The default product card should never require the user to know what a "concern family" is. The expanded view can introduce the concept. The full analysis view assumes technical knowledge.

---

## Human comprehensibility limits

**Research context:** Cognitive load research suggests that humans can hold approximately 7 ± 2 items in working memory simultaneously. For a complex decision (understanding why a product scored the way it did), the effective limit is lower — approximately 3–5 active considerations before attention degrades and confidence in understanding drops.

**Practical implications:**
- A product explanation with 8 negative signals is less effective than one with 3 clearly ranked signals plus a summary
- A score range (score: 52–58, depending on category refinement) may communicate uncertainty more honestly than a point estimate
- The primary vs. supporting signal structure in concern coordination maps well to the human limit: one primary concern, one or two supporting ones, grouped by root cause

**What this means for rule design:**
When adding a new rule, ask: "If this rule fires on a product that already has two other firing rules, can I still explain all three clearly in one sentence each?" If not, the new rule may need to be absorbed into an existing concern rather than added as a standalone.

---

## Rule explosion risk

**What rule explosion is:** The accumulation of rules over time in response to edge cases, until the rule set is large enough that no single person fully understands it. This is a known failure mode in expert systems and regulatory scoring frameworks.

**How it happens in scoring systems:**
1. A product scores unexpectedly well because a specific edge case wasn't anticipated
2. A new rule is added to handle the edge case
3. The new rule creates a new edge case that wasn't anticipated
4. Another new rule is added
5. After many iterations, the rule set is internally consistent but no one can explain why any given rule exists without reviewing the original edge case that prompted it

**The BSIP2 risk:** The current architecture has 20+ guardrail rules. This is not yet at the explosion point — most rules have clear rationales. But the trajectory is toward explosion if rules continue to be added in response to specific products without removing or consolidating existing rules.

**The governance mechanism:**
Before any new rule is added:
1. Confirm it cannot be handled by adjusting an existing threshold
2. Confirm it does not overlap with an existing rule in the same concern family
3. Identify which existing rule it replaces or whether it adds net complexity
4. Document the specific product type that prompted the addition
5. Add it to the cap taxonomy (see `cap_taxonomy.md`) with its classification

**The simplification pressure:**
Every three months (or at every version increment), review the full rule list and identify:
- Rules that have never fired in the product database
- Rules that fire on every product in a concern family (suggesting the threshold is set too low)
- Rules that fire on fewer than 1% of products (either very good — targeting a rare severe concern — or unnecessary)
- Rules that could be merged into a gradient without losing analytical power

This review is not optional — it is how rule explosion is prevented over time.

---

## A score should remain explainable without 40 interacting rules

This is the explainability budget's central principle. It is not a technical constraint; it is a design commitment. The architecture is explicitly designed to prevent a situation where a score requires 40 interacting rules to explain, even if all 40 rules are individually justified.

The mechanisms that enforce this commitment are:
1. The concern coordination system (groups rules by root concern; only the primary signal is fully expressed)
2. The family budget clamp (aggregates penalty impact per family; individual penalty values are internal)
3. The dominant-driver identification (surfaces one primary explanation per score)
4. The rule proliferation limit (prevents the underlying rule count from growing unchecked)
5. This document (establishes the commitment explicitly, making future violation recognisable)

If a future BSIP2 version can no longer produce a three-signal explanation for any product in the golden products suite, the explainability budget has been exceeded. The response is to simplify the architecture, not to improve the UI.
