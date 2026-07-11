# Seed Oils Explainer — Nutrition Co-Sign + Scoring Examples (TASK-492A)

**Status:** Nutrition Agent co-sign gate. Scientific framing approved with corrections below.
No score changed. This is the second of two required sign-offs before Content drafts copy — the
Hebrew explainer itself still needs the Content + Adversarial-QA two-gate before it reaches the
owner.

**Reviewed input:** `03_operations/reports/research/seed_oils_evidence_verification_v1.md`
(Research Agent, 2026-07-03).

---

## 1. Co-sign on the calibrated-middle framing

**Approved, with the anchor-hierarchy correction below.**

The proposed position — "seed oils are not uniquely toxic/inflammatory, AND ultra-processed or
deep-fried food still scores poorly for reasons that have nothing to do with the botanical origin
of the oil" — is scientifically defensible. Confirm the following framing constraints before
Content drafts:

**a. Anchor the piece on MSK + Johns Hopkins, cite Nagra et al. 2026 as corroboration only.**
This matches Research's own verification tiering exactly. Reasons, stacked:
- Nagra et al. (DOI 10.1080/10408398.2026.2657527) is a **scoping narrative review**, not a
  systematic review or meta-analysis — a real evidence-tier distinction, not a technicality.
- Lead author Mark Messina's affiliation with the Soy Nutrition Institute Global is a genuine,
  nameable conflict of interest (co-author David Goldman's industry-adjacent nutrition
  communication work is a secondary, softer flag). This doesn't make the review's conclusions
  wrong — the conclusions independently match MSK and Johns Hopkins — but it does mean the review
  cannot be the *spine* citation in consumer-facing copy without disclosure, and should not be
  quoted as if it were disinterested Cochrane-tier evidence.
- MSK (verified via direct fetch, on-the-record clinical dietitians) and Johns Hopkins (verified
  via convergent independent secondary sourcing, named researcher Dr. Matti Marklund) are
  institutional positions with no comparable COI. They are the load-bearing citations. AICR is
  weaker (snippet-only, primary page 403'd) — usable as a third directional data point, not a
  cited authority, unless someone gets a working fetch path before publication.
- Practical instruction for Content: lead with "hospitals and public-health schools that have
  reviewed the evidence say X," and place the 2026 review as "a review published this year reached
  the same conclusion" — never the reverse order.

**b. Preserve the hedge the sources themselves use.** PubMed's own abstract language for Nagra et
al. says LA/seed oils show benefit "possibly" extending beyond CVD to other chronic disease
endpoints — the authors distinguish a firmer CVD conclusion from a softer, exploratory one. MSK and
JHU both explicitly separate **natural liquid seed oils** from **hydrogenated seed oils in
ultra-processed foods**, and both name the confound directly: UPF-heavy diets are blamed on seed
oils when the actual variable may be the UPF matrix itself. Content should preserve this — a flat
"seed oils are totally fine, full stop" line overclaims relative to what even the friendliest
sources say.

**c. The engine's own scoring history is a legitimate example to cite** (see §2) — not as
marketing color, but because it demonstrates the exact point evidentially, on Bari's own past
decision. Bari itself once penalized seed-oil presence more heavily (`seed_pen=10`), reduced it in
2026-06-15 specifically because Nutrition reviewed LA/inflammation meta-analytic evidence
(Judd et al. 1998 PMID 9771853; Ramsden 2012 PMID 22889633) and concluded the "seed oils are
inflammatory" framing was not supported. That is a real, dated, evidence-triggered self-correction
— it is a stronger credibility signal than "trust us," and it is honest because it happened.

**Verdict: framing is correct as proposed, condition (a) is the one substantive fix — anchor on
MSK/JHU, review is corroboration.**

---

## 2. Real Bari scoring examples (pulled from live corpus, verified by direct trace read)

**Method:** grepped `bari-web/src/data/comparisons/*.json` for products whose `expansion.ingredients`
Hebrew text contains a seed/vegetable oil term (שמן קנולה / שמן חמניות / שמן סויה / קנולה / חמניות
etc.), then read each matching product's `_scoring_trace` (penalties_applied, caps_applied,
nova_proxy) directly from the committed JSON — not inferred, not summarized by another agent.
181 matching product records found across 12 live categories. Full extraction script output
retained in this session for audit; can be re-run against `bari-web/src/data/comparisons/` at any
time by grepping the same ingredient-term list.

**Confirmed at the code level** (`03_operations/bsip2/proto_v0/src/score_engine.py:3014`):
```python
check_penalty("SEED_OIL_PRESENT", has_seed_oil, 3, fat_pens_fired)
```
A flat **−3 point** penalty, applied once, regardless of quantity or position in the ingredient
list. This is the entire scoring exposure seed-oil presence has in this pathway. (A second, related
mechanism — `seed_pen`, lines 1713/1728 — is the one EV-096 reduced from 10→5 in 2026-06-15,
gated behind `hc_endemic_relief`→0 for endemic dairy-fat products per EV-104; it is a different
signal path serving whole_food_fat/dairy_protein categories, not the biscuit pathway below, but the
same evidence-driven direction: the engine has already been correcting *toward* less seed-oil
penalty as the LA/inflammation literature came in, not accumulating penalty against it.)

### Example A — seed oil present, best score in its entire category
**עוגיות גרידת לימון ללת"ס** (Danny & Galit lemon-zest cookies), `cookies_coffee_frontend_v2.json`
- **Score: 59.8 / C — rank 1 of 117** products in the biscuit/cookie shelf. The single
  highest-scoring product in the category contains canola oil (שמן קנולה).
- Ingredients open with almonds and whole rice flour, agave as sweetener; canola oil sits mid-list.
- Trace: `SEED_OIL_PRESENT` fires, **−3 points**. The binding constraint on the score is
  `NOVA_PROXY_3_PROCESSED` (cap 94.8, far above the actual 59.8) — i.e. the oil penalty is a minor
  residual on a score that a structural processing signal, not the oil, actually shapes.
- The product's own live `rowVerdict` already names this correctly in Hebrew: *"שמן הקנולה ברשימה
  הוא הסייג הקטן"* ("the canola oil in the list is the minor caveat") — the copy engine is already
  editorially calibrated to treat the oil as a footnote, not the headline. This is a useful existing
  proof point, not something to newly invent.

### Example B — seed oil present, worst scores in the same category
**פתי בר ללא גלוטן קלאסי / שוקו** (gluten-free Petit Beurre), same file, **rank 116–117 of 117**
(scores 10.0–10.7, grade E). Also contains seed oil (`SEED_OIL_PRESENT` fires, same −3). What
actually drives these to the bottom of the shelf: `ISRAELI_RED_LABEL_1_SUGAR`,
`NOVA_PROXY_4_ULTRA_PROCESSED` (cap 68), `ADDITIVE_MARKERS_5_PLUS` (cap 60),
`HIGH_CAL_HIGH_SUGAR_SOFT`, `HIGH_CAL_LOW_SATIETY_SOFT`. Five to six independent structural
penalties/caps stack; the −3 seed-oil residual is a rounding error next to them.

**A and B together are the demonstration:** identical −3 flat penalty fires on both the #1 and the
#116/117 product in a 117-product shelf. If seed oil were the thing driving grade, presence alone
could not coexist with a 50-point score spread. It doesn't drive grade. Processing depth (NOVA
proxy), added-sugar structure, and additive load do.

### Example C — seed oil present, zero scoring exposure at all
**Oat/rice milk-alternative drinks**, `milk_frontend_v1.json` — e.g. משקה שיבולת שועל ללא סוכר
(50.5/C, rank 9/18) down through משקה אורז אורגני (46.3/D, rank 16/18). These plant-based drinks
contain sunflower/canola oil (verified in TASK-284A's corpus check: "8 real plant-based oat/rice
drinks... correctly in milk_and_alternatives... benign, no correction") but **no
`SEED_OIL_PRESENT` penalty fires in this pathway at all** — the D/C-range scores here come from
this category's own structural comparison to dairy milk (protein density, fortification), not from
the oil. This is the cleanest "near-neutral" case: multiple products, seed oil present, zero
seed-oil-specific scoring exposure.

### What the honest finding is
Seed-oil presence alone is **near-neutral in the engine** — a flat, small (−3, or in the other
pathway a de-escalating 5/0-point) residual that never determines a grade on its own in any example
pulled. What actually moves scores in this corpus, repeatedly and by a wide margin: NOVA-proxy
processing depth caps (60–95 point range), Israeli red-label sugar/sat-fat crossings (cap 45–55),
additive-marker density caps (60–72), and compound signals like `HIGH_CAL_HIGH_SUGAR_SOFT` /
`HP_FAT_SUGAR_COMBO`. This is consistent with the engine's own stated architecture
(`fat_technology_scoring_state`, `redlabel_deanchor_directive`): fat-source severity is meant to be
expressed through processing/technology signals (hydrogenation, trans-fat status), not through a
seed-vs-non-seed binary.

**Recommended framing sentence for Content** (Nutrition-approved wording, may be edited for voice
by Content within the two-gate, but the factual claim must survive intact):
*"ברי לא מעניש שמן קנולה או חמניות בגלל המקור הצמחי שלהם — מה שבאמת מזיז ציון הוא רמת העיבוד,
כמות הסוכר והתוספים. עוגייה עם שמן קנולה יכולה לקבל את הציון הכי גבוה במדף שלה; עוגייה אחרת עם אותו
שמן יכולה לקבל את הציון הכי נמוך — ההבדל הוא לא השמן."*
(Translation for internal review: "Bari does not penalize canola or sunflower oil for their plant
origin — what actually moves the score is processing depth, sugar load, and additives. A cookie
with canola oil can score the highest in its shelf; another cookie with the same oil can score the
lowest — the difference isn't the oil.")

---

## 3. The honest boundary — what NOT to overclaim

Content must not turn "not uniquely toxic" into "fry all you want" or "seed oils are strictly
better than alternatives in every context." Specifically:

1. **Repeated high-heat frying / oil reuse is a real, separate, peer-reviewed concern** —
   documented formation of aldehydic lipid-oxidation byproducts in heavily reused, high-temperature
   fried PUFA oils (Research's tier: Moderate evidence for the oxidation-product-formation
   mechanism). This is a claim about oil **degradation under specific handling conditions**
   (commercial deep-frying, repeated reuse), categorically different from "linoleic acid causes
   inflammation in the body at normal dietary intake" (which is the claim MSK/JHU/the review are
   rebutting). Do not let the piece imply the frying-oxidation concern is debunked by the same
   evidence that debunks the inflammation claim — it isn't; it's a different question with its own,
   weaker evidentiary support for human health outcomes (Research's tier: Insufficient for
   extrapolating to population-level disease outcomes from ordinary home cooking).
2. **Hydrogenated seed oil in ultra-processed foods is not the same exposure as home-cooking with
   fresh liquid oil.** MSK and JHU both draw this line explicitly — it should survive into the
   piece. Bari's own engine draws a version of this same line structurally (PHVO/trans-fat
   detection is a separate, harder-hitting signal path from the flat seed-oil-presence penalty;
   see `fat_technology_scoring_state`).
3. **Do not claim Bari "proves" seed oils are safe.** Bari's scoring behavior is evidence of how
   the *engine* weights a signal, not a clinical claim about human health outcomes. The correct
   claim is narrower and more defensible: "the presence of seed oil doesn't drive Bari's grade one
   way or the other because the science doesn't support treating it as a standalone risk marker
   — the things that do drive grade are named and shown."
4. **Do not cite the two MSK-referenced studies' specific numbers** (16% lower mortality; 17% lower
   cancer-mortality from a butter→seed-oil swap) unless someone independently re-verifies them on
   PubMed first — Research flagged these as reported secondhand via MSK's page, not independently
   checked. If Content wants those numbers in the piece, that's a follow-up verification task, not
   something to carry through on MSK's citation alone.
5. **NOVA / BSIP / cap / floor / structural_class stay out of consumer copy** per standing hard
   rule — describe the drivers ("how processed it is," "how much sugar," "how many additives
   stack up") in plain Hebrew, never the internal signal names.

---

## Bottom line

Co-sign granted for the calibrated-middle framing with the anchor-order correction (MSK/JHU
load-bearing, Nagra et al. corroborating and COI-disclosed if quoted). Three real corpus examples
with fully verified scoring traces are ready to hand to Content: the #1-ranked cookie in a
117-product shelf contains canola oil (Example A), the #116–117-ranked cookies in the same shelf
also contain seed oil (Example B) — same flat penalty, 50-point spread, proving presence doesn't
drive grade — and the milk-alternative category shows seed oil present with zero scoring exposure
at all (Example C). The frying/oxidation nuance and the hydrogenated-oil/UPF distinction are named
explicitly as guardrails against overclaiming. No score changed; no scoring philosophy changed;
this is a citation and editorial-direction review only.

---

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\01_framework\\nutrition\\seed_oils_blog_cosign_v1.md",
      "sha256": "9a2c05e204a2741c1fde5ff24c1f53ac66e44f4f778c520c1bb21e9b472b616e"
    }
  ],
  "counts": {
    "comparison_json_files_scanned": 17,
    "products_matching_seed_oil_ingredient_term": 181,
    "categories_with_seed_oil_matches": 12,
    "products_cited_as_examples": 3,
    "example_A_rank": "1 of 117 (cookies_coffee_frontend_v2.json)",
    "example_B_rank": "116-117 of 117 (cookies_coffee_frontend_v2.json)",
    "example_C_products_zero_penalty": 8,
    "engine_penalty_verified_at_line": "03_operations/bsip2/proto_v0/src/score_engine.py:3014",
    "scores_changed": 0,
    "scoring_philosophy_changed": 0
  },
  "commands_run": [
    {"cmd": "python3 scan of bari-web/src/data/comparisons/*.json for seed-oil ingredient terms + _scoring_trace extraction", "exit_code": 0},
    {"cmd": "grep -n SEED_OIL_PRESENT|seed_pen|has_seed_oil 03_operations/bsip2/proto_v0/src/score_engine.py", "exit_code": 0},
    {"cmd": "grep -n EV-096|EV-097|EV-104 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "AICR position remains snippet-level only (Research's gap, not closed by this task)",
    "MSK's two cited studies (2025 Nutrients, 2025 JAMA IM) not independently re-verified on PubMed — flagged as a pre-publication follow-up if their specific numbers are used",
    "Content has not yet drafted the Hebrew explainer; Adversarial QA sign-off has not occurred"
  ],
  "acceptance_test": "Co-sign delivered with named correction (anchor order); >=2 real, trace-verified corpus examples handed to Content with file:line/rank citations; honest boundary (frying/oxidation, hydrogenated-UPF distinction, no-overclaim) stated explicitly. PASS.",
  "status_proposed": "RETURNED"
}
```
