# Maadanim Headline Metric — Nutrition Ruling (TASK-137F)

**Reviewer:** Nutrition Agent · **Date:** 2026-06-01 · Grounded in the current (post-TASK-136, engine 0.4.0) displayed set.

## Headline metric = PROTEIN (g/100g)

Same discipline as hummus. Three reasons:

1. **It separates two products sold under one name.** "מעדן" spans an *indulgent dessert* and a
   *functional protein snack*. Protein is the axis that tells you which you're holding — on this
   shelf it runs from **0 g** (pudding / jelly products that aren't even dairy-based) to **~10 g**
   (protein-enriched: יופלה GO, דנונה פרו, מעדן חלבון).
2. **It is the most trustworthy number we can show.** Protein is present on **87/87** products.
   Sugar — the other candidate — is present on only **29/87**, and the values (2.5–5.4 g) are
   implausibly low for sweet desserts → a source-data gap, not a usable metric. So protein is both
   meaningful *and* reliable; sugar is neither here (parallels suppressed fat in hummus).
3. **It is consumer-legible.** The per-100g protein figure instantly flags treat vs. functional.

## Guardrail (encoded in the prologue + verdicts)
Protein is the **headline, not the verdict**. The score also weighs stabilizer/additive load and
processing. High protein does **not** make a dessert "healthy" (most 8–10 g products are still
stabilizer-heavy and sit in C/D); a low-protein traditional מעדן is **not** "worse" — it serves a
different use. This matches the existing methodology line about the two use-cases.

## Category shape (current data)
87 displayed · grades **1 B / 19 C / 55 D / 12 E** · range **27–70**. Top = יופלה GO מועשר בחלבון
70/B (only B). מילקי paradox preserved (iconic, but stabilizer-built → D). This is a low-ceiling
category — the prologue/verdicts must hold the "best ≠ excellent" framing.

*Ruling: protein is the headline metric for maadanim. No score changes (TASK-136 owns scores).*
