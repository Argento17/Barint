# Superlatives Allowed — Policy v1

**Owner:** Nutrition Agent (scoring philosophy / category interpretation), co-signed by Data Agent
(owns the `superlatives_allowed` fact-sheet field mechanics in `build_copy_inputs.py`).
**Trigger:** TASK-550 — content_agent_v1 cereals pilot minted unauthorized sodium superlatives
("highest/lowest sodium among 20 tested") for two products whose fact sheets carried
`superlatives_allowed: []`. Both claims were corpus-true; the breach was **authorization**, not
accuracy.

## The rule

A superlative token ("highest_X" / "lowest_X") may be granted to a product in a category's fact
sheet **only if all of the following hold**:

1. **Uniqueness.** The product's value equals the corpus extreme and no other product in the
   displayed corpus ties it. A tie grants nothing — "the X-est" is false when two products share
   the extreme. *(Already enforced by `is_unique_extreme()`.)*

2. **Minimum corpus size.** The category run must have at least **12 non-null observations** for
   that metric. Below this, "highest/lowest among N tested" reads as spurious precision on a small
   sample. Cereals (n=20 for sodium/protein/kcal/fat, n=19 for sugar/fiber) clears this bar.

3. **Minimum margin over 2nd place.** The gap between the extreme and the next-closest value must
   be **≥ 10% of the corpus range** (max − min) for that metric, or the token is withheld even if
   technically unique. This is the guard against a 0.1g gap minting a superlative. (Not yet coded
   as a numeric gate in `build_copy_inputs.py` — today uniqueness is the only gate. Recommended as
   a follow-up enhancement; flagged, not blocking, since neither Shugi's 435mg nor Cranch's 16mg
   sodium was close to 2nd place — the margin issue did not cause this incident.)

4. **Null-awareness (RT-6).** If the metric has any nulls in the corpus (n < product_count), the
   granted token carries a `superlatives_context` entry — `n_measured` and
   `phrase_as_among_measured: true` — and the author **must** render "among N measured," never
   "among all [product_count] tested." Implemented in `build_copy_inputs.py`
   (`superlatives_context_for()`, this task).

5. **Driver relevance — the line that failed.** Two tiers:
   - **Core consumer-priority metrics** (`protein`, `energyKcal`, `sugar`) are **always** eligible
     per rules 1–4, regardless of whether that exact metric is the product's named scoring driver.
     Bari has already decided these three map to universally-understood shopping priorities
     (how much protein, how many calories, how much sugar) and are headline-safe on their own
     terms.
   - **Every other metric — sodium, fat, fiber, anything else** — additionally requires that the
     metric appear in the product's **actual fired driver chain**: a named `cap_rules` entry, a
     `penalties_applied` entry, or the `lowest_dimension` in that product's trace. If the metric is
     not part of why the product scored what it scored, a rank claim about it may appear only as a
     **supporting fact** (plain sentence, no superlative/"-est" phrasing) in `positiveSignals` /
     `limitingFactors` / `watchOut` — **never** in `insightLine` or the opening clause of
     `rowVerdict`, and it is never "granted" as a token.

## Ruling: sodium in cereals (this incident)

**Sodium extremes are NOT sanctioned as superlative tokens for the cereals category**, under rule
5's second tier. Reasoning:

- Neither breach product had sodium as its scoring driver. Shugi's (7290107647854) driver is
  `low_satiety` (satiety_support = 21.0, the lowest dimension). Cranch's (3387390525960) driver is
  `cap_plus_penalty` on `ISRAELI_RED_LABEL_1_SUGAR` + `multiple_added_sugar_sources` +
  `long_ingredient_list` + `seed_oil_present`, with `whole_food_integrity` (4.0) as the lowest
  dimension. Sodium appears in neither product's `cap_rules`, `penalties_applied`, nor
  `lowest_dimension`.
- No product in this 20-SKU cereals run trips a sodium-specific cap or red-label rule at all — the
  engine's own trace output never treats sodium as scoring-relevant in this category run. A
  superlative built from raw per-100g arithmetic, disconnected from anything the engine actually
  fired on, is decorative — and per the standing verdict-copy standard (verdicts name the real
  fired driver), decorative facts do not earn headline placement.
- This is a category-and-run-scoped ruling, not a permanent ban on sodium language: Bari's standing
  calorie/sodium verdict-copy standard already permits naming sodium as a **driver-based** claim
  when it IS the fired reason. If a future cereals cap rule fires on sodium for some SKU, that
  SKU's sodium extreme (if unique) would qualify under this same rule 5, tier 2.
- **Practical effect:** `superlatives_for()` in `build_copy_inputs.py` does not compute sodium at
  all (was already true pre-incident — confirmed, not a builder bug). The breach was the LLM
  author computing its own corpus extreme from the raw `nutrition` block and `corpus_stats` it was
  given for other purposes, then minting `-est` phrasing never granted. The fix belongs in the
  content-authoring engine's operating instructions, not in this builder: **an author may use
  superlative/"-est" phrasing for a product ONLY when the exact token is present in that product's
  `superlatives_allowed` list. Computing a rank claim independently from `nutrition` /
  `corpus_stats`, even when factually true, is out of bounds.** (Routed to Content Agent as a
  required instruction-set fix; not implemented here — authoring engine instructions are Content
  Agent's lane.)

## Non-driver supporting mentions remain fine

Cranch's copy citing "the lowest sodium among all measured" as a **secondary positive bullet**
(not headline) would have been an acceptable plain fact under rule 5's supporting-fact allowance —
the actual defect is (a) it was phrased as a granted superlative ("Xn ביותר") rather than a plain
sentence, (b) for Shugi it was promoted to the **insightLine itself**, which is the single
highest-scrutiny field and must state the real fired driver (low satiety), not an incidental
corpus-rank fact.

## Implementation record (this task)

- `superlatives_for()` — no change; already sodium-free. Doc comment added citing this ruling.
- `superlatives_context_for()` — new function, `03_operations/page_generator/copy/build_copy_inputs.py`,
  attaches `n_measured` / `phrase_as_among_measured` to every granted token (RT-6 fix).
- `_meta.s_products` — filtered to the run's actual barcodes (RT-11 fix). Root cause: the
  module-level `S_VERBATIM` dict (hardcoded yogurt S-grade barcodes/text, see file top) was listed
  in full via `list(S_VERBATIM.keys())` for every category's `_meta`, regardless of whether those
  barcodes existed in the current run. Per-product attachment (`if bc in S_VERBATIM`) was already
  correctly scoped; only the summary field was not. Fixed by intersecting with `{s["barcode"] for
  s in sheets}`. Deeper smell not fixed here: a shared, cross-category script hardcoding one
  category's verbatim copy as a global constant — flagged to Data Agent as a candidate for the
  uniform-baseline cleanup (move `S_VERBATIM` to a per-category external file, loaded only when
  `category` matches).
- Rule 3 (margin threshold) is written down here but **not yet coded** — flagged as a follow-up,
  not blocking, since it did not cause this incident.
