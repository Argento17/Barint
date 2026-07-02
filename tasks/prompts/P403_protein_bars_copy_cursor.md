# P403 / Protein-bars v2 copy authoring — 32 verdicts (route: C1-CURSOR)

You are a C1 builder (Cursor) acting as Content author. Write the Hebrew consumer copy for the rebuilt protein-bars comparison page. This is DRAFT under the two-gate rule (an Adversarial-QA gate follows). Edit ONLY the one candidate JSON. Do NOT deploy, do NOT git commit, do NOT touch any file under bari-web/.

## FILE (edit only this — a staging candidate, absolute path)
C:\Bari\02_products\snack_bars\staging\run_pb_standard_20260625_062614\protein_bars_frontend_v2_candidate.json
32 products, ranked 1..32 by score. Every product already has correct score/grade/rank/nutrition_per_100g — DO NOT CHANGE ANY OF THOSE. Copy fields are "PENDING_COPY": insightLine, rowVerdict, expansion.comparisonContext, expansion.positiveSignals, expansion.limitingFactors, and categoryNote.body_he.

## VOICE (Tom's Voice — non-negotiable)
Insight-first, restrained but fearless, natural Israeli Hebrew (NOT translationese, no reciting grams like a label). Each verdict leads with the human takeaway, then the why. At most ONE pivotal number per verdict (the metric bars/nutrition row already show the numbers — don't recite them). No marketing fluff.

## PER-PRODUCT COPY (all 32)
For each product, read its grade + nutrition_per_100g (protein, sugar, sat fat, fiber, kcal, sodium) and ingredients context, then write:
- **insightLine**: one sharp line — the single thing that defines this bar's standing.
- **rowVerdict**: 1–2 sentence human verdict — standing → why → the catch.
- **expansion.comparisonContext / positiveSignals / limitingFactors**: grounded in THIS product's real data.
Grades are B(1)/C(26)/D(5). Most are C — differentiate them by what actually distinguishes each (protein quality, fiber, sugar, additives), don't make them sound identical.

## HARD CONDITIONS (Nutrition co-sign — required)
1. **The two "Nayture" bars MUST name their sugar.** Barcodes 8410076610379 (נייטשר פרוטאין שוקולד) and 8410076610386 (נייטשר פרוטאין קרמל מלוח) both score 55/C but carry **17.2g / 16.1g sugar per 100g** — high. Their copy must NOT bury this: state the sugar plainly as the catch (they earn C on protein+fiber DESPITE high sugar). A shopper must not read 55/C and think they're low-sugar.
2. **categoryNote.body_he** — the "הערת קטגוריה" — must disclose TWO things in clear Hebrew:
   (a) the protein-lens trade-off: on this shelf scores reward protein + fiber architecture, so a high-protein/high-fiber bar can rank above a lower-sugar bar when the sugar is below the red-label threshold — sugar is not the only axis here;
   (b) the data gap: ingredient lists were not available for these products, so processing/NOVA is an estimate and confidence is partial across the shelf.

## GUARDS
- 0 changes to score/grade/rank/nutrition/barcode/imageUrl. Copy fields + categoryNote only.
- No banned phrases: "חלבון נמוך", "נתרן גבוה" as a bare label, "מרכיבים רבים", NOVA/BSIP/pillar words. Sodium = stated as fact, never causal ("...כי הנתרן..."). Referencing "הציון" / the score is allowed.
- OFF ban — ground every claim in the product's own nutrition/data; invent nothing (no ingredient lists exist, so do NOT assert specific ingredients you can't see — speak to the nutrition profile).
- Honest grades: don't inflate. Most are C — say so with substance, no false superlatives.

## VERIFY BEFORE RETURNING
JSON parses; 0 remaining "PENDING_COPY" in any of the 32 products + categoryNote; 0 score/grade/nutrition changed; the two Nayture verdicts contain their sugar figure; categoryNote covers both (a) and (b). Report a 3-line sample + the Nayture verdicts. End with the machine-readable return contract JSON. Do NOT close.
