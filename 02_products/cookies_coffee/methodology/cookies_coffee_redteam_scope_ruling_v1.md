# Cookies-near-coffee — Red-Team Scope Ruling v1

**Task:** TASK-275 (factory run #7, cookies-near-coffee)
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** RETURNED — awaiting orchestrator verification
**Gates:** Data re-score (run_cookies_004) and Content fixes
**Scores grounded in:** run_cookies_003
**Methodology basis:** `cookies_coffee_scoring_interpretation_v1.md` §1.3 + `cookies_coffee_routing_ruling_v1.md` §3.1

---

## Corpus starting point

run_cookies_003: 61 products. Distribution: C9 / D22 / E30 (confirmed by red-team hard-fail table).

---

## Finding-by-Finding Rulings

---

### RT-2 — ck-80083764 (עוגיות דגנים עם ש.שועל — גנדולה): grain oat cookie

**Ruling: RE-ROUTE to biscuit, NOT OUT.**

**Reason:**

The product fails the §1.3 in-scope test for this page only if it is not "plausibly consumed as a coffee accompaniment" OR if it fails the structural test (not dry/crisp, not sweet, has filling/coating). It fails neither: a crisp oat-grain biscuit is a recognized coffee-accompaniment form on the Israeli shelf. The §1.4 ruling is explicit: "Whole-grain variants (digestive with whole wheat, oat digestive) — IN." A Gandola oat-grain cookie is structurally equivalent to an oat digestive — same form factor, same consumer occasion.

The problem is not scope: the product belongs on this page. The problem is that the run_cookies_003 trace routed it to `snack_bar_granola` (classification_basis: `snack_bar_granola:דגנים(name×2)`, `snack_bar_granola:nutrition_hint(0.30)`), causing two snack-bar-specific caps to fire that have no business applying to a plain oat biscuit:
- `SNACK_BAR_HIGH_CAL_SUGAR` (cap 60) — fired because category = snack_bar_granola
- `SNACK_BAR_HIGH_CAL` (cap 70) — fired because category = snack_bar_granola
- Binding cap = 60; penalty `HIGH_CAL_HIGH_SUGAR_SOFT` −5 → final score 55

Under the biscuit lens (which EV-058 / `cookies_coffee_routing_ruling_v1.md` §2.3 specifies), neither of these caps fires. The product's actual composition (sugar=17.0g < 17.5g threshold; satFat=2.3g < 5g threshold; zero red labels confirmed in trace `red_labels: []`, `red_label_count: 0`) crosses no Israeli red-label threshold. The correct biscuit-lens score, pending a re-run, is approximately 56–63 (weighted dimension score without snack-bar caps = 61.01 per trace `weighted_dimension_score`; the binding cap under biscuit routing would be from the sugar family or calorie density, not the SNACK_BAR-specific rules).

**The verdict for this product in run_cookies_003 is therefore factually wrong on two counts:**
1. The score (55) is depressed by snack-bar caps that should never have fired.
2. The published verdict attributes the score to sugar ("הסוכר הוא מה שמשאיר את הציון בגבול") when no sugar cap fires for this product — the only fired cap is the snack-bar calorie-sugar combination cap, which is a category-inappropriate rule.

**Action:** Data Agent re-routes `bsip1_cookies_80083764` to `biscuit` category (anchor: "עוגיות" already fires as `hard_anchor:עוגיות` in run_cookies_003 for the `biscuit` category in run_003, but the snack_bar_granola routing won via name signal `דגנים×2`; the anchor exclusion for "עוגיות" when paired with "דגנים" needs to be handled per EV-058 §2.3 — this product is a carry-forward from before the EV-058 anchor was properly ordered). Re-score in run_cookies_004. Regenerate verdict.

**Product stays IN corpus. Moves to OUT_OF_SCOPE = false.**

---

### RT-4 — ck-7290106656727 (עוגיות חיוכים שוקולד — עלית): children's character cookie

**Ruling: OUT.**

**Reason:**

The methodology §1.3 is unambiguous: "Children's character cookies (עוגיות ספרים, בחשנים, Leibniz Zoo, animal-shaped) — PRIMARY consumer occasion is children's snacking, not coffee. OUT — children's biscuits category."

"חיוכים" (smileys) is Elite's character-based children's cookie line. The consumer occasion test fails on both name and packaging: the product is a chocolate-coated, character-shaped small cookie sold in Elite's children's confection packaging. It is not positioned as a coffee-accompaniment biscuit by Elite or by Israeli retail context.

The red-team trace confirms the product is NOVA 4 (nova_proxy=4, nova_confidence=0.55, medium confidence — the highest-confidence NOVA assignment in the products I examined), with four additive categories detected, three multiple-sugar sources, and artificial flavoring ("חומרי טעם וריח"). Its score 15.4/E is real and defensible — but that is irrelevant to the scope question. The corpus filter failed to catch this product at the shelf-mapping stage.

**This is not a close call.** The character-cookie exclusion exists precisely because Elite's children's character line is the paradigm example of the exclusion type. Including it on a coffee-biscuit shelf exposes Bari to a correct methodological challenge: "you say children's character cookies are out, but Elite Smileys is on the page."

The product's low rank (59/61) and E grade do not mitigate the exclusion. Scope integrity is a threshold criterion, not a balance-of-harms decision.

**Action:** Mark `ck-7290106656727` as `OUT_OF_SCOPE` in the corpus. Do not delete the trace or data. Do not re-score. The product is excluded from the displayed corpus and the frontend JSON.

**Corpus after RT-4 drop: 61 → 60 products.**

---

### RT-5 — ck-7290119043149 (עוגיות בטעם חמאה — לה פזואלוס): 1-ingredient parse, NOVA=2 artifact

**Ruling: TRANSPARENCY_NULL / discard.**

**Reason:**

The trace is definitive: `ingredient_count: 1`, `ingredient_list: ["קמח חיטה לבן ("]`. Only one ingredient was parsed (a truncated extraction of "קמח חיטה לבן"). The engine assigned NOVA=2 (`nova_proxy: 2`, `nova_confidence: 0.25`) on this single-ingredient basis, and the whole-food integrity dimension scored 85 (NOVA-2 base, complexity_pen=0 because no other ingredients parsed).

The red-team report identifies the real ingredient list from the displayed frontend JSON ingredients field: "קמח חיטה לבן, סוכר לבן, מים, שמנים ושומנים מהצומח (חלקם מוקשים), גלוקוזה, חומרי תפיחה (E450, E500), מלח, חומרי טעם וריח." This contains:
- Partially hydrogenated vegetable fats ("שמנים ושומנים מהצומח (חלקם מוקשים)") — a NOVA-4 marker and a potential trans-fat concern
- Artificial flavoring ("חומרי טעם וריח") — a `has_flavor_enhancer=true` trigger in nova_proxy.py that adds 3 to nova4_score, sufficient on its own to push NOVA to 4
- E450 (diphosphate leavener) + E500 (sodium carbonate leavener) — additive categories

If the full ingredient list had been correctly parsed, the engine would have assigned at minimum NOVA 3 (artificial flavorings = NOVA-4 trigger; more likely NOVA 4) and the `whole_food_integrity` score would not have been 85. The `processing_quality` score would not have rested on NOVA-2. The positive signal "עיבוד מינימלי יחסית לקטגוריה" that appears in the frontend is built on a corrupted NOVA inference.

**This is a genuine one-shot data miss per the missing_data_discard_rule.** The ingredient extraction failed at the scrape stage — only one of ~8 ingredients was captured. The correct behavior under the owner's rule (MEMORY: `missing_data_discard_rule`, 2026-06-13) is: discard. We do not re-source, re-scrape, or manually patch.

**A secondary concern stands independent of the discard ruling:** even if we hypothetically accepted the partial parse, the NOVA=2 assignment for a product with displayed ingredients that include partially hydrogenated fat and artificial flavoring is an active content-integrity failure. The page would display a "minimal processing" positive signal for a product whose visible ingredient text contradicts that signal. This cannot ship regardless of how the discard question resolves.

**Action:** Mark `ck-7290119043149` as `OUT_OF_SCOPE` with discard reason = `EXTRACTION_FAILURE_ONE_SHOT_MISS` (per missing_data_discard_rule). Do not delete the trace or data. Remove from the frontend JSON and displayed corpus.

**Corpus after RT-5 drop: 60 → 59 products.**

---

### RT-7 — Grade ceiling after drops and re-routes

**Ruling: B is the honest achievable ceiling post-reroute. C is NOT the final ceiling.**

**Reason:**

The red-team correctly identifies the tension: the page prologue states "C is the ceiling of this category" (run_cookies_003 empirical max = 63.1), but the routing ruling §3.1 explicitly predicts "B achievable for 5–8 products" after correct routing, and `cookies_coffee_scoring_interpretation_v1.md` §2.3 states "the honest ceiling is B (70–79)."

The run_cookies_003 ceiling of 63.1 (grade C) reflects two compounding distortions:
1. The grain product (ck-80083764) is scored 55 instead of its correct ~61 under biscuit routing — but this alone does not get to B.
2. More importantly: run_cookies_003 is the corpus BEFORE the full EV-058 biscuit routing was applied to all relevant products. Several products that should score in the 65–75 range under biscuit routing may currently be scored under snack_bar_granola or cracker lenses, with snack-bar-specific caps depressing their scores.

The methodology §2.3 is mechanistically grounded: a clean digestive with whole-grain flour, sat-fat < 5g (no ISRAELI_RED_LABEL_1_SAT_FAT cap), sugar < 17.5g (no sugar cap), no synthetic additives (no NOVA-4 cap), and minimal calorie density cap exposure can reach 68–75 (grade B). The committed engine supports this. The run_cookies_003 max of 63.1 is the pre-EV-058-reroute ceiling, not the methodology ceiling.

**After run_cookies_004 (which implements correct biscuit routing for all 59 remaining products):**
- The ceiling is expected to be B (approximately 68–76 for the 3–8 best-in-class digestive/whole-grain/minimal-processing products)
- C remains the modal grade for the majority of the shelf
- E/D products may shift modestly as routing distortions are corrected

**The statement "C is the ceiling" must not appear in any copy until after run_cookies_004 is complete and the empirical max is verified.** If run_cookies_004 confirms a max of 63.x (grade C), the statement becomes accurate and can ship. If the max reaches B territory, the statement is false and must be revised.

**Interim ruling for content:** "C is the ceiling" is FROZEN as a consumer-facing claim until run_cookies_004 empirical max is confirmed. Content Agent must not ship this claim without the post-run_004 verification signal from the orchestrator.

---

### RT-8 — Peanut butter cookies (protein ~15g): IN with disclosure requirement

**Ruling: KEEP IN corpus. Disclose peanut-protein source in copy. No implication of health.**

**Reason:**

Both products — `ck-7290013453631` (עוגיות חמאת בוטנים כשל"פ — דני וגלית, protein=15.5g, score=32.0/E) and `ck-7290123330488` (עוגיות בוטנים כשל"פ — לה פזואלוס, protein=15.4g, score=23.3/E) — were included via the §1.3 "natural-not-fortified" exception, confirmed by the routing ruling.

The inclusion is justified:

1. **The exception is correctly scoped.** §1.3 excludes "Protein / functional biscuits (>10g protein/100g, engineered fiber)" because their "macro architecture diverges from the coffee-biscuit shelf." Peanut butter as the primary fat/protein source is not engineered fortification — it is a natural ingredient that incidentally raises protein. The protein architecture of a peanut butter cookie is fundamentally different from a protein-bar-shaped-as-a-cookie. The routing ruling correctly distinguishes these.

2. **The trace confirms natural-protein source.** `ck-7290013453631` trace shows: `protein_source: "whole_food"`, `has_fortification: false`. The protein comes from peanut butter in the ingredient mix, not from isolate or powder addition.

3. **The scores are honest.** Both products score E (32.0 and 23.3) because their composition genuinely warrants it: `ck-7290013453631` has sugar=24.8g (crosses 17.5g threshold), satFat=6.4g (crosses 5g threshold) — `ISRAELI_RED_LABELS_2_PLUS` fires. The high protein does not rescue the score. Inclusion does not create a misleading "high protein = good" signal because both products are at the bottom of the page.

4. **The copy must disclose the inclusion rationale.** The red-team correctly identifies (RT-8) that the verdicts currently do not explain why these products are in scope despite their high protein. A methodology-curious consumer or competitor who reads §1.3 and sees these products would correctly ask: "why are these in?" The answer needs to be surfaced — not in the methodology text, but as a brief honest line in the verdict: something along the lines of "high protein here is from peanut butter, not from engineered fortification — peanut cookies are a recognized coffee biscuit type on the Israeli shelf." The copy must also not imply that the protein makes the product healthy; both products score E precisely because the fat and sugar architecture overrides any protein benefit.

**Copy requirement (for Content Agent):** The verdict for both peanut cookie products must:
- State explicitly that the protein derives from peanut butter (natural source)
- Not frame the protein as a positive nutritional feature
- Explain that the products remain E because sugar and fat architecture dominate
- A single clarifying note in the methodology section (not product-level) is acceptable as an alternative, but a product-level disclosure is preferred for direct consumer readability

**Both products remain IN corpus. No corpus change.**

---

## Final Corpus Count

| Action | Products |
|---|---|
| run_cookies_003 starting count | 61 |
| RT-4 drop: ck-7290106656727 (OUT — children's character cookie) | −1 |
| RT-5 drop: ck-7290119043149 (OUT — extraction failure, 1-ingredient parse) | −1 |
| RT-2: ck-80083764 stays IN, re-routes to biscuit (no count change) | 0 |
| RT-8: 2 peanut cookies stay IN (no count change) | 0 |
| **FINAL CORPUS** | **59** |

---

## Expected Ceiling After run_cookies_004

**B (70–79) is the honest achievable ceiling.** Approximately 3–8 products are expected to reach B after correct biscuit routing. C remains the modal grade. A is not achievable (methodology §2.3, grounded in NOVA-3 cap + sat-fat/sugar cap mechanics). The "C is the ceiling" prologue claim must be held until run_cookies_004 confirms empirically.

---

## Downstream Gates

| Gate | Status |
|---|---|
| Data Agent re-score (run_cookies_004) | UNBLOCKED — this ruling provides the corpus (59 products), OUT dispositions for 2 drops, and re-route directive for ck-80083764 |
| Content Agent copy fixes | BLOCKED on run_cookies_004 (ceiling claim cannot ship until run_004 empirical max is confirmed); RT-1 prologue fix (false threshold claim) and RT-3 (17g → 17.5g threshold correction) can proceed before run_004 |
| RT-7 ceiling claim | FROZEN until run_cookies_004 max is verified |
| RT-8 peanut cookie copy disclosure | Unblocked — Content Agent can draft the disclosure language now |
| Red-team re-gate (Stage 9, re-run) | Blocked on run_004 completion and frontend regeneration |

---

## Guards Confirmation

| Guard | Status |
|---|---|
| No engine edits in this ruling | CONFIRMED — no cap changes, no signal changes, no scoring rule modifications |
| OFF ban absolute | CONFIRMED — no OFF data referenced or used |
| No fabricated data | CONFIRMED — all scores, cap conditions, and ingredient data cited from verified run_cookies_003 traces |
| Frozen invariants untouched | CONFIRMED — milk scores (run_005_headpin), snk-001=70/B ceiling, bread provenance all untouched |
| OUT = data preserved (not deleted) | CONFIRMED — both OUT products retain their traces and BSIP data; only excluded from displayed corpus |
| Drops marked OUT_OF_SCOPE, not DISCARD (data) | CONFIRMED |

---

```json
{
  "task": "P88",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/cookies_coffee_redteam_scope_ruling_v1.md",
      "sha256": "PENDING — orchestrator to verify via sha256sum on file write"
    }
  ],
  "counts": {
    "findings_ruled": 5,
    "findings_denominator": "RT-2, RT-4, RT-5, RT-7, RT-8 (all 5 required by P88 spec)",
    "corpus_start": 61,
    "drops": 2,
    "corpus_final": 59,
    "reroutest_no_count_change": 1,
    "products_confirmed_in": {"ck-80083764": "IN-reroute", "ck-7290013453631": "IN-keep", "ck-7290123330488": "IN-keep"},
    "products_out": {"ck-7290106656727": "OUT-children-character-cookie", "ck-7290119043149": "OUT-extraction-failure"},
    "expected_ceiling_post_run004": "B (70-79)",
    "ceiling_claim_status": "FROZEN until run_cookies_004 empirical max confirmed",
    "run_referenced": "run_cookies_003"
  },
  "per_finding_rulings": {
    "RT-2": "RE-ROUTE to biscuit (not OUT). ck-80083764 is a valid oat-grain coffee biscuit per §1.4 whole-grain IN rule. Score 55 is artifact of snack_bar_granola routing (SNACK_BAR_HIGH_CAL_SUGAR + SNACK_BAR_HIGH_CAL caps fired; no red-label cap fires for this product). Verdict attributing score to sugar is factually wrong. Action: re-route in run_cookies_004.",
    "RT-4": "OUT. עוגיות חיוכים שוקולד — עלית matches §1.3 children's-character-cookie exclusion verbatim. Consumer occasion is children's snacking, not coffee. Corpus filter failure. Product marked OUT_OF_SCOPE, data retained.",
    "RT-5": "TRANSPARENCY_NULL / discard. ck-7290119043149 had 1-ingredient extraction (קמח חיטה לבן only). NOVA=2 is an artifact of failed extraction. Real ingredient list includes partially hydrogenated fats + artificial flavoring — these are NOVA-4 triggers. Showing 'minimal processing' positive signal on a partial parse is a content-integrity failure. Genuine one-shot miss per missing_data_discard_rule. Product marked OUT_OF_SCOPE, data retained.",
    "RT-7": "B is the honest achievable ceiling post-reroute (routing_ruling_v1 §3.1 + scoring_interpretation_v1 §2.3). run_cookies_003 max 63.1/C is pre-EV-058 distortion. The 'C is the ceiling' prologue claim is FROZEN until run_cookies_004 empirical max is confirmed. C remains modal grade.",
    "RT-8": "KEEP IN with disclosure requirement. Peanut protein is natural-source (whole_food per trace), not engineered fortification. §1.3 natural-not-fortified exception applies. Both products score E (composition warrants it). Copy must disclose peanut-protein source, must not frame protein as a positive feature. No corpus change."
  },
  "commands_run": [],
  "not_done": [
    "Data Agent: re-route ck-80083764 to biscuit category in run_cookies_004",
    "Data Agent: remove ck-7290106656727 and ck-7290119043149 from corpus (mark OUT_OF_SCOPE, retain data)",
    "Data Agent: run_cookies_004 re-score on 59-product corpus",
    "Data Agent: regenerate frontend JSON from run_cookies_004",
    "Content Agent: fix RT-1 prologue (false claim all products cross a red-label threshold)",
    "Content Agent: fix RT-3 threshold display (17g → 17.5g in page-data.ts)",
    "Content Agent: add peanut-protein disclosure to verdicts for ck-7290013453631 and ck-7290123330488",
    "Content Agent: hold RT-7 ceiling claim (C vs B) until run_cookies_004 max confirmed by orchestrator",
    "Data Agent: fix RT-6 additives pipeline for 4 products with E-numbers but empty d4_additives dropdown",
    "Stage-9 red-team re-gate: blocked on run_004 completion and frontend regeneration"
  ],
  "self_check": {
    "off_ban_respected": true,
    "no_fabricated_numbers": true,
    "all_rulings_grounded_in_methodology_section": true,
    "methodology_citations": ["§1.3 children's-character exclusion (RT-4)", "§1.4 whole-grain IN rule (RT-2)", "§2.3 B ceiling mechanics (RT-7)", "§1.3 protein>10g exception + routing_ruling natural-not-fortified (RT-8)"],
    "trace_citations": {
      "RT-2": "bsip1_cookies_80083764/bsip2_trace.json: caps_applied=[SNACK_BAR_HIGH_CAL_SUGAR,SNACK_BAR_HIGH_CAL], red_label_count=0, weighted_dimension_score=61.01",
      "RT-5": "bsip1_cookies_7290119043149/bsip2_trace.json: ingredient_count=1, nova_proxy=2, NOVA inference unreliable",
      "RT-8": "bsip1_cookies_7290013453631/bsip2_trace.json: protein_source=whole_food, has_fortification=false"
    },
    "frozen_invariants_untouched": true,
    "no_engine_edits_in_this_ruling": true,
    "drops_data_retained": true,
    "ceiling_claim_frozen": true,
    "proposed_status_not_closed": true,
    "acceptance_test": "orchestrator verifies: (1) 5/5 findings ruled, (2) corpus_final=59, (3) RT-4 and RT-5 marked OUT_OF_SCOPE in corpus, (4) RT-2 re-route directive clear, (5) RT-7 ceiling claim frozen, (6) RT-8 disclosure requirement stated"
  }
}
```
