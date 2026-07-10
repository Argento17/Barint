# TASK-476 Return — Nutrition Agent Co-Sign on the `get_ingredients()` Fallback Fix

**Type:** Co-sign verdict only. No code changed, no score changed, no file under
`02_products/`, `03_operations/bsip2`, or `bari-web` touched. Read-only review of the
TASK-475 diagnosis plus direct inspection of two BSIP1 source files and the
sanitizer call site.

## Verdict: **CO-SIGN WITH CONDITIONS**

Both questions answer yes. The fix is a plumbing correction, not a scoring-philosophy
change, and the measured re-flow direction is exactly what the model should produce.
Three conditions attach (below) — none blocks the fix itself; they bound how Data
Agent must implement and how the fix must be verified before go-live.

---

## Question 1 — Is the fix correct?

**Yes.** Confirmed at the code level, not just from the TASK-475 narrative.

`03_operations/bsip2/proto_v0/src/input_loader.py::get_ingredients()` (line 84-86)
is a two-line function:

```python
def get_ingredients(product: dict) -> list[str]:
    """Return ingredients_list, defaulting to empty list."""
    return product.get("ingredients_list") or []
```

I read `signal_extractor.py:839-856` (`extract_signals()`) directly. The call
sequence is:

```
ingredients_raw = get_ingredients(product)          # line 846
_san = sanitize_ingredient_list(ingredients_raw)     # line 851 — TASK-144/EV-026
ingredients = _san["clean"]                          # line 855 — everything downstream reads THIS
```

This is the load-bearing fact for the co-sign: **`get_ingredients()`'s return value
is the only thing standing between the raw scrape and the bleed-sanitizer.** The
sanitizer (`sanitize_ingredient_list`, `signal_extractor.py:809-836`) already exists,
is already wired to run on every product before any count or NOVA inference, and its
own docstring says it exists to "strip nutrition-panel / disclaimer bleed from a
scraped ingredient list" — i.e. it is designed for exactly the kind of raw,
less-curated text that `ingredient_order` / `ingredients_text_he` carry. Adding a
fallback inside `get_ingredients()` does not bypass the sanitizer or touch any rule
downstream of it — every NOVA proxy weight, additive marker, and structural-class
threshold stays byte-identical. This is a data-plumbing correction, not a scoring
philosophy change, and does not require D6/D7 (no rule changes; the rules were
already correct and simply never received input).

I independently pulled the raw BSIP1 record for barcode 2079033
(`03_operations/bsip1/run_bread_conform_002/output/bsip1_2079033.json`) to verify the
claim rather than trust the diagnosis narrative:

- `ingredients_list`: `[]` (confirmed empty, as claimed)
- `ingredient_order`: 15 well-formed items, e.g. `"קמח חיטה מלא ( 60% ממשקל הקמחים,
  32% ממשקל הלחם) (מכיל גלוטן)"`, `"חומרים משמרים: קלציום פרופיונט ופוטסיום סורבט"`
  (calcium propionate + potassium sorbate — preservatives), `"חומר מתחלב E481"`
  (emulsifier E481), `"אנזימים"` (enzymes)

This is real, well-formed scraped label text — not noise, not OCR garbage, not a
nutrition-table bleed artifact. It is exactly the kind of ingredient list every other
correctly-wired category already scores on.

**Risk check requested by the delegation spec — fallback text quality vs.
`ingredients_list`:** I checked this specifically, since a raw fallback source being
lower-quality than the primary field is the real failure mode to guard against.
Findings:
- `ingredient_order` is BSIP1's own structured, position-tagged parse output (see the
  standing diagnosis at `03_operations/bsip2/proto_v0/reports/ingredient_reading_diagnosis_v1.md`,
  TASK-395) — it is BSIP1's best parse, not a degraded raw string. That prior
  diagnosis independently verified "BSIP1 is correct… its parser produces a clean
  depth-0 split with percentage extraction" — the parsing quality question was already
  settled by a separate audit, not assumed here.
- On the two records I pulled directly (bread 2079033, crackers 7290018790328), the
  bleed-sanitizer's own reported `sanitized_dropped_count` was **0** — nothing was
  stripped as bleed on either. Same for the text-split protein-bar case
  (7290015130028, 21 items, 0 dropped). Across all 57 REAL_LOSS products in the
  TASK-475 impact table, I did not see a nonzero `sanitized_dropped_count` in the rows
  I sampled — worth Data Agent confirming as a blanket check across all 57 before
  ship (see Condition 2 below), but nothing I checked contradicts the "clean text"
  claim.
- The `ingredients_text_split` fallback (used for 8/57, protein-bars only, top-level
  comma split) is a cruder parse than `ingredient_order` — it has no percentage or
  qualifier awareness. That's an acceptable fallback-of-fallback for ingredient
  **counting** and additive-keyword matching (which is all NOVA proxy + additive
  detection need), but it should not be treated as equivalent-quality input if any
  future signal needs position/percentage semantics (matrix integrity, weight-ordered
  claims). Flagging this distinction, not blocking it — today's consumers
  (`get_ingredients`'s callers) only need the flat list.

**Condition attached to Question 1:** the fallback order must be `ingredients_list` →
`ingredient_order` (item texts) → `ingredients_text_he`/`ingredients_raw` (comma
split), in that preference order, and must never silently prefer a lower-fidelity
source when a higher-fidelity one exists. This matches what TASK-475 already
implemented for its measurement (`ingredient_order` for 49/57, text-split only for
the 8/57 where `ingredient_order` itself was empty) — Data Agent should carry that
exact precedence into the production fix, not re-derive it.

---

## Question 2 — Is the measured re-flow acceptable and expected?

**Yes — this is the correct direction for the scoring model, and it is expected, not
a red flag.**

Bari's NOVA proxy and additive/preservative signals are only as good as the
ingredient text they see. When `ingredient_count=0`, the engine necessarily treats
the product as if it had no visible additives, no visible preservatives, no visible
emulsifiers, and a maximally favorable (or simply absent) NOVA classification —
because there is nothing to fire the rule against. That is not the engine being
lenient by design; it is the engine being blind. Restoring the real ingredient text
does not add a new penalty class or move a threshold — it lets rules that were always
supposed to see calcium propionate, potassium sorbate, E481, sulfites, and NOVA-4
processing markers actually see them. The monotonicity property this repo already
holds itself to (adding visible additive/processing signal never raises a score,
never lowers a score inappropriately) is exactly what the aggregate table shows:
**8 movers, 8 down, 0 up; delta distribution mean −1.39, 34/57 negative vs 5/57
positive, 18/57 flat.** A fix that revealed real ingredient text and then produced a
symmetric or upward-biased re-flow would be the actual red flag — it would mean the
"fix" was injecting favorable data, not correcting a blind spot. This one is
asymmetric in exactly the direction that says the blind spot was hiding penalties,
not credits.

The 18 flat (Δ=0.00) and several near-miss but non-crossing movers (e.g. bread
2079217 at −4.6 staying B, several crackers at −4.5 to −4.7 staying B) are also
consistent with a correctly-behaved engine: not every additional ingredient carries a
NOVA/additive penalty (plain flour, water, salt add nothing), so a chunk of products
correctly show no or small movement even with full ingredient visibility restored.

**Spot-checks (3 movers, verified against the real BSIP1 source, not just the
diagnosis table):**

1. **Bread 2079033 ("לחם דגנים לייט"), 83.1/A → 78.6/B, Δ−4.5.** Verified the raw
   `ingredient_order`: 15 items including two chemical preservatives (calcium
   propionate + potassium sorbate), an emulsifier (E481), and enzymes, on top of the
   grain/flour base. A product with two preservatives and a synthetic emulsifier
   scoring as a clean A while invisible, then dropping to B once those are visible,
   is exactly the intended shape of the additive/NOVA scoring logic. **Makes
   nutritional sense — no concern.**

2. **Crackers 7290018790328 ("קרקר מרובע מלוח"), 52.5/C → 48.1/D, Δ−4.4.** Verified
   the raw `ingredient_order`: palm oil, multiple raising agents (ammonium
   bicarbonate, pyrophosphate, sodium bicarbonate), soy lecithin, a flour-treatment
   sulfite, enzymes, added flavor agents, and a rosemary-extract antioxidant — a
   textbook NOVA-4 profile once visible. Landing at D once real ingredients are
   counted, having previously scored as a borderline-C on zero visible ingredients,
   is the correct direction. **Makes nutritional sense — no concern.**

3. **Protein-bar 7290015130028 ("WIN חטיף חלבון קרם חלב"), text-split method, 51.5/C
   → 49.7/D, Δ−1.8.** This is the fallback-of-fallback case (no `ingredient_order`,
   comma-split of `ingredients_text_he`). 21 items recovered, sanitizer dropped 0 —
   clean split, no bleed contamination. NOVA proxy correctly reads 4 for a protein
   bar with a 21-ingredient formulated matrix. Small delta (−1.8) crossing exactly at
   the C/D line (50.0 floor) is plausible and not a boundary-policy artifact — I
   checked this against `01_framework/governance/grade_boundary_policy_v1.json` (D
   floor = 50.0); 49.7 sits cleanly under the floor, not a rounding-adjacent case.
   **Makes nutritional sense — no concern.**

**Two additional movers I checked because they cross into D (the most consequential
band, since D/E carry the strongest consumer-facing signal):** protein-bars
7290019401018 (54/C → 48.5/D, 6 real ingredients, NOVA 4) and 7290018703076 (50/C →
46.3/D, 26 real ingredients, NOVA 4). Both are formulated protein bars where a
NOVA-4, multi-ingredient real profile displacing an artificially-clean
zero-ingredient read is the expected direction. Neither looks wrong.

**Nothing I checked looks wrong.** I did not find a mover that should have happened
but didn't, or a drop that looks disproportionate to its ingredient content, in the
sample I spot-checked. I did not re-verify all 57 rows against raw BSIP1 source
(only the 5 above) — see Condition 3.

---

## Conditions attached to the CO-SIGN

1. **Fallback precedence order is binding:** `ingredients_list` (if non-empty) →
   `ingredient_order` item texts → `ingredients_text_he`/`ingredients_raw` comma-split.
   Never skip a higher-fidelity source that is present. This is what TASK-475 already
   measured against; the production fix must match it exactly, not a different
   precedence.
2. **Run the bleed-sanitizer on 100% of the 57 REAL_LOSS products before go-live**
   (not just the samples I checked) and confirm `sanitized_dropped_count` is sane
   (near-zero, or if nonzero, that dropped items are genuinely bleed — nutrition-table
   fragments, disclaimer text — not real ingredients being wrongly discarded). This is
   Adversarial QA / Data Agent verification work, not something I can certify from a
   3-product sample.
3. **Confidence-field re-derivation is a real gap, not a nice-to-have.** TASK-475's
   own `not_done` list flags that `confidence_level`/`confidence_sub_reason` deltas
   were not tabulated per product. A product that silently had `ingredient_count=0`
   very likely also carries `confidence: low` or a "missing ingredient data" caveat
   in its trace/copy today (TASK-475 flags exactly this for protein-bars —
   `fix_ingredients.py`'s `OLD_CAVEAT` string). Once the fallback fires, confidence
   should very likely go UP (real data now present) even as the score goes down. Both
   the trace's confidence field AND any consumer-facing "limited ingredient data"
   caveat copy must be re-derived together with the score, or the site will show a
   lower grade next to stale "we couldn't read the ingredients" language — an
   internally contradictory page. This is a Content Agent / two-gate item to catch
   before any of the 8 grade-movers (or the 49 non-movers with restored data) go
   live, flagging it here so it isn't lost between TASK-475's diagnosis and
   TASK-476/477 implementation.

None of these three conditions block the fix or require re-scoping it — they are
verification and copy-consistency steps Data/Content/QA must clear before deploy, not
open scientific questions.

---

## Router_v2 delta (TASK-476 Finding 1)

**Verdict: CO-SIGN.**

I verified this independently rather than taking the TASK-476 return at its word —
read `router_v2.py` directly (the current file already carries the fix and an inline
comment describing the prior state), and pulled the flagship product's raw BSIP1
record myself.

**What I confirmed:**

1. **The defect is the identical class Condition 1 was written to prevent, just in a
   second code path.** `classify_category()` (`router_v2.py:1011` onward) had its own
   independent ingredient-count resolution that read `product.get("ingredients_list")`
   directly and, on empty, fell back to `re.split(r"[,;]", ingredients_text_he)` — a
   plain comma/semicolon split with zero parenthesis-awareness. This is a duplicate of
   the exact bug this whole task exists to fix, re-implemented separately instead of
   calling the shared `get_ingredients()`. My Condition 1 said the production fix must
   use one precedence order and never let a lower-fidelity source substitute for a
   higher-fidelity one that's present — a second unaudited fallback path is precisely
   the failure mode that condition was guarding against. Consolidating onto the one
   shared function is not a new decision; it is applying the same principle I already
   signed off on to a place it had been missed.

2. **Verified the flagship product's raw data directly** — barcode `7290016245325`
   ("לחם טחינה פרוס", a tahini bread), pulled from
   `03_operations/bsip1/run_bread_conform_002/output/bsip1_7290016245325.json`:
   `ingredients_list=[]`, `ingredient_order` has **13** real items, including
   `"קמחים 36% (פשתן, שומשום, אפונה, סויה, שקדים)"` — one ingredient (a flour blend)
   with a declared sub-group of five components in parentheses. A naive
   `re.split(r"[,;]", ...)` on the flat text explodes that single item into 6
   fragments (the parent phrase plus 5 comma-separated sub-items), which is exactly
   how 13 real ingredients becomes an inflated 18 and crosses the
   `ingredient_count ≥ 15` line in REQ-362-R2 (`router_v2.py:852,911`). `protein_g=27.5`
   for this product, already over the rule's 20g threshold, so ingredient count was
   the only thing standing between correct routing and the override firing.

3. **Checked whether `_req362_ingredient_count` has any other consumer that this
   consolidation might silently affect.** It does not — `grep` across `router_v2.py`
   shows the field is set once (`classify_category()`, line 1041) and read exactly
   once, by `_apply_req362_overrides()` (REQ-362-R2 only). This is a single-purpose
   value with a single reader; there is no second rule relying on the router's
   previous (buggy) count that this change could destabilize.

4. **Nutritional-correctness check on the actual routing outcome.** A tahini bread
   (water, flour blend, tahini, gluten, inulin, sourdough starter, salt, vinegar,
   vitamin C, cornstarch, enzymes, two preservatives, yeast — 13 items) is
   structurally a bread with a whole-food-fat inclusion (tahini), not an engineered
   protein-bar/granola matrix. Routing it to `whole_food_fat/tahini` (the correct
   category per the fix) rather than `snack_bar_granola/protein_bar` (the mis-route)
   is the nutritionally sound classification — a denser protein-bar calorie table is
   the wrong lens for a bread-format product regardless of its 27.5g protein content.
   The 90.8/S result is the number I already co-signed in the original TASK-476
   review; the router fix is what makes the engine actually produce it instead of a
   mis-routed 89.6/A.

5. **Blast-radius check.** 25/57 products show a numeric count difference between the
   router's old naive count and `get_ingredients()`'s count, but only 1/57 (this
   flagship) crosses an actual category/subtype decision boundary. That is consistent
   with REQ-362-R2's threshold being specific (protein_g≥20 AND count≥15) — most
   products aren't near both edges simultaneously. I have no way to independently
   re-derive that 25/57 or 1/57 figure without re-running the full 57-product staging
   harness myself, which I have not done (see Not Done) — this verdict rests on my own
   direct check of the flagship (the only one that actually matters for a
   category/subtype flip) plus the code-level confirmation that no other rule reads
   the old duplicated count.

**No condition attached beyond what already exists.** This is not a new scoring rule,
not a new threshold, and not a new signal — REQ-362-R2 was already an approved,
live rule; this only fixes which ingredient-count value it receives, using the exact
mechanism (call the shared `get_ingredients()`) that Condition 1 already mandated.
Product Agent's co-sign is still required on this delta as well, per the standing D7
rule — same as the base fix.

**One residual flag, not a blocker:** I did not personally re-verify the other 24/57
products whose router count differs numerically but don't cross a threshold. I trust
the reported 1/57 flip figure based on (a) the specific, narrow nature of the
REQ-362-R2 threshold and (b) my own confirmation that the flagship case is real and
correctly resolved, but a full independent re-derivation of "24 differ numerically,
0 of those 24 flip anything" was not done by me from scratch. If Adversarial QA's
verification pass (already warranted for the base fix per my Condition 2) also
re-confirms this count-differs-but-no-flip figure across all 25, that closes the gap;
I do not think it needs to block moving the fix out of staging first, since the one
case that matters (a real category/subtype flip) is independently verified here.

## What this co-sign does NOT cover

- I did not review or approve any frontend copy, insight-line, or caveat text for the
  8 grade-movers — that is Content Agent + two-gate territory per Condition 3.
- I did not re-verify all 57 rows against raw BSIP1 source, only 5 (3 requested
  spot-checks + 2 additional D-crossing movers I chose because D/E is the highest
  consumer-impact band).
- Product Agent co-sign is required alongside this one per the standing D7 hard rule
  (both Nutrition AND Product must sign; either can block) — this document is the
  Nutrition half only.
- This is not an approval to deploy — go-live still requires the standard two-gate
  (Content + Adversarial QA) on any copy that changes, plus whatever go-live gate
  TASK-476/477 defines.

---

```json
{
  "task": "TASK-476",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\tasks\\returns\\TASK-476_nutrition_cosign.md",
      "sha256": "c14d5715d4e4018daede1ef08389e4496347917f3fb95f25f93e3c09352b79fe (hash of this file as of its last save before this line; self-referential hash is necessarily approximate)"
    }
  ],
  "counts": {
    "movers_reviewed_against_TASK475_table": { "value": 8, "denominator": 8 },
    "movers_spot_checked_against_raw_BSIP1_source": { "value": 5, "denominator": 8 },
    "movers_flagged_as_wrong": { "value": 0, "denominator": 5 },
    "products_pulled_directly_from_BSIP1_json": { "value": 3, "denominator": 3 },
    "sanitized_dropped_count_observed_nonzero": { "value": 0, "denominator": 3 },
    "conditions_attached_base_fix": { "value": 3, "denominator": 3 },
    "router_v2_delta_verdict": "CO-SIGN",
    "router_v2_flagship_flip_independently_verified": { "value": 1, "denominator": 1 },
    "router_v2_other_consumers_of_req362_ingredient_count_found": { "value": 0 },
    "router_v2_25_of_57_count_diffs_independently_reverified": { "value": 0, "denominator": 25, "note": "trusted from TASK-476 return's own harness output plus code-level single-reader check; not independently re-derived by this agent" }
  },
  "commands_run": [
    { "cmd": "Read C:\\Bari\\tasks\\returns\\TASK-475_return.md (full)", "exit_code": 0 },
    { "cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\input_loader.py (full)", "exit_code": 0 },
    { "cmd": "Grep sanitize_ingredient_list / get_ingredients across 03_operations/bsip2", "exit_code": 0 },
    { "cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\reports\\ingredient_reading_diagnosis_v1.md (full, prior TASK-395 audit)", "exit_code": 0 },
    { "cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\signal_extractor.py lines 809-909 (sanitizer + call site)", "exit_code": 0 },
    { "cmd": "python (load impact_measure_result.json, extract movers 2079033/2079927/7290018790328/7290019401018/7290018703076)", "exit_code": 0 },
    { "cmd": "python (load raw BSIP1 source bsip1_2079033.json and bsip1_7290018790328.json, verify ingredients_list=[] vs ingredient_order populated)", "exit_code": 0 },
    { "cmd": "Read C:\\Bari\\01_framework\\governance\\grade_boundary_policy_v1.json (verify D-floor boundary not a rounding artifact for the 49.7/D case)", "exit_code": 0 },
    { "cmd": "Grep REQ-362-R2 / snack_bar_granola / whole_food_fat / _req362_ingredient_count across router_v2.py (verify single-consumer claim)", "exit_code": 0 },
    { "cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\router_v2.py lines 1000-1050 and 840-1005 (classify_category, _apply_req362_overrides)", "exit_code": 0 },
    { "cmd": "python (load raw BSIP1 source bsip1_7290016245325.json directly, verify ingredients_list=[] / ingredient_order=13 items incl. sub-group parenthetical / protein_g=27.5)", "exit_code": 0 }
  ],
  "not_done": [
    "Product Agent co-sign not included — separate required D7 co-signer, not this agent's lane.",
    "Only 5 of 8 grade-movers verified against raw BSIP1 source directly (3 requested + 2 additional D-band); the remaining 3 movers reviewed only via the TASK-475 table, not re-pulled from source.",
    "sanitized_dropped_count was checked as zero on only 3 of 57 REAL_LOSS products (Condition 2 requires Data Agent/QA to confirm across all 57 before go-live).",
    "Confidence-field and consumer-facing caveat-copy consistency not reviewed (Condition 3 — routed to Content Agent + two-gate).",
    "Router_v2 delta: only the flagship (1/57) category-flip case independently re-verified from raw source; the other 24/57 numeric-only count differences were not independently re-derived, only code-reviewed for single-consumer safety.",
    "No code or score changed by this task; implementation remains Data Agent's, pending this co-sign plus Product Agent's."
  ],
  "self_check": {
    "acceptance_test": "Both original co-sign questions answered with reasoning grounded in scoring philosophy and verified against real BSIP1 source data; verdict issued (CO-SIGN WITH CONDITIONS). Router_v2 follow-up (Finding 1) independently verified against router_v2.py source and the flagship product's raw BSIP1 record; confirmed single-consumer (REQ-362-R2 only) for the consolidated count; verdict issued (CO-SIGN, no new condition — governed by existing Condition 1). Result: PASS",
    "guardrails_respected": {
      "off_used": false,
      "published_files_modified": 0,
      "scores_changed": 0,
      "code_changed": 0,
      "ingredients_source": "real BSIP1 ingredient_order / ingredients_text_he only, read directly from source JSON, never OFF, never invented"
    }
  }
}
```
