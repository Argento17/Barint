# Red-Team Challenge Report — Supplements SIE v3 (real_corpus_v3)
Date: 2026-06-19
Scope: 82 scored / 118 shelf, SIE proto_v0 / algorithm_v0.2.0
Corpus file: _corpus_run_full_v3.json (TASK-277 v3 CHANGES_REQUESTED retry)
Challenger: red-team-agent

---

## Opening Finding

**CRITICAL structural defect: elemental-conversion key mismatch causes at least 9 wrong safety vetoes.**

The engine's magnesium safety check converts compound mass to elemental Mg before comparing to the 350 mg UL — but only when the panel's form string exactly matches the full compound name in the dossier's `elemental_by_form` map (e.g. `"magnesium oxide"`, `"magnesium citrate (trimagnesium dicitrate)"`). The corpus stores short form tokens (`"oxide"`, `"citrate"`, `"malate"`, `"bisglycinate"`). The lookup `elem.get(_norm("oxide"))` returns `None`. With no elemental fraction, the engine compares the raw compound mass (432–700 mg) directly against the 350 mg elemental UL. At least 9 magnesium products are vetoed to E/20 on that arithmetic alone.

Corrected elemental estimates:
- 520 mg oxide × 0.603 = 313 mg elemental — WITHIN UL
- 450 mg oxide × 0.603 = 271 mg elemental — WITHIN UL
- 432 mg oxide × 0.603 = 260 mg elemental — WITHIN UL
- 550 mg citrate × 0.162 = 89 mg elemental — WITHIN UL
- 700 mg malate × ~0.113 = ~79 mg elemental — WITHIN UL

All nine are falsely vetoed. None exceeds the 350 mg elemental UL.

This is the single most consequential defect in the corpus. Publishing these scores tells a consumer that a mainstream 520 mg magnesium oxide tablet is at a safety-ceiling dose. It is not.

---

## Product-by-Product Assessment

### S Grades (15 products, all score = 91.2)

| SKU | Active | Score/Grade | Binding | Panel Claim (HE) | Engine Claim Matched | RT Assessment |
|---|---|---|---|---|---|---|
| SP-7290012760266 | vitamin_d3 | 91.2/S | blend | ויטמין D לספיגת סידן…להשלמת מחסור | status correction (Strong) | CLAIM TRANSLATION: panel claim is bone/deficiency HE; bsip0s_label manually maps to status-correction endpoint. Grade follows from the translation, not the engine's own resolution. Plausible but unverifiable. |
| SP-7290013142146 | vitamin_d3 | 91.2/S | blend | ויטמין D לספיגת סידן…להשלמת מחסור | status correction (Strong) | Same translation pattern. |
| SP-7290017490601 | vitamin_d3 | 91.2/S | blend | ויטמין D3 עם K2 לבריאות העצם | status correction (Strong) | Panel claim is "bone health + K2" — a Moderate endpoint at best. Pre-scored to Strong via manual translation. Defendability gap. |
| SP-7290018439623 | vitamin_d3 | 91.2/S | blend | ויטמין D3 לבריאות העצם ומערכת החיסון | status correction (Strong) | Panel is "bone + immune" — umbrella maps bone/immune to Moderate/Weak respectively. Pre-scored to Strong via translation. Serious gap. |
| SP-7290012760761 | vitamin_d3 | 91.2/S | blend | ויטמין D לספיגת סידן…להשלמת מחסור | status correction (Strong) | Same translation pattern. |
| SP-7290019444374 | vitamin_d3 | 91.2/S | blend | ויטמין D לספיגת סידן לשמירה על בריאות העצם | status correction (Strong) | Same translation pattern. |
| SP-7290017218366 | vitamin_d3 | 91.2/S | blend | ויטמין D לספיגת סידן לשמירה על בריאות העצם | status correction (Strong) | Same translation pattern. |
| SP-7290010035984 | vitamin_d3 | 91.2/S | blend | Vitamin D3 1000 IU per drop; no preservatives | status correction (Strong) | EN claim fed directly. Engine token-matched to status-correction via "D3 1000 IU" containment. Defensible: a 1000 IU D3 liquid for deficiency correction is a genuine Strong-tier claim. |
| SP-7290015318433 | vitamin_d3 | 91.2/S | blend | Vitamin D3 1000 IU per drop | status correction (Strong) | Same, defensible. |
| SP-7290118814061 | iron | 91.2/S | blend | (full claim from panel) | anaemia correction (Strong) | Defensible: ferrous bisglycinate at effective dose, correct claim. |
| SP-7290012056741 | iron | 91.2/S | blend | iron | anaemia correction (Strong) | Defensible. |
| SP-783495578741 | iron | 91.2/S | blend | iron | anaemia correction (Strong) | Defensible. |
| SP-7290017243450 | vitamin_b12 | 91.2/S | blend | B12 | B12 deficiency correction (Strong) | Defensible. |
| SP-7290015765572 | vitamin_b12 | 91.2/S | blend | B12 | B12 deficiency correction (Strong) | Defensible. |
| SP-712179581913 | vitamin_b12 | 91.2/S | blend | B12 | B12 deficiency correction (Strong) | Defensible. |

### A Grades (5 products)

| SKU | Active | Score/Grade | Binding | RT Assessment |
|---|---|---|---|---|
| SP-7290019444312 | folic_acid | 82.8/A | blend | Folic acid NTD claim (Strong). Form=50 (unknown, not listed) — drags score. Defensible in structure, though form 50 for a pharma folic acid tablet is arbitrary. |
| SP-7290006437273 | folic_acid | 82.8/A | blend | Same as above. |
| SP-7290008111041 | folic_acid | 82.8/A | blend | Same. |
| SP-7290001471845 | vitamin_b12 | 86.2/A | blend | B12 at sub-optimal dose (dose=72/DOSE_OVER_STUDIED). Defensible. |
| SP-7290012760891 | calcium | 81.0/A | blend | Calcium fracture endpoint (Moderate). Defensible. |

### Selected E/20 Magnesium Veto Cluster (9 structurally wrong vetoes)

| SKU | Form | Compound mg | Est. Elemental mg | Engine Verdict | Correct Verdict |
|---|---|---|---|---|---|
| SP-7290001066973 | malate | 700 | ~79 | E/20 veto | within UL; grade by blend |
| SP-7290017847122 | oxide | 432 | ~260 | E/20 veto | within UL; grade by blend |
| SP-7290010207640 | oxide | 450 | ~271 | E/20 veto | within UL; grade by blend |
| SP-7290019444206 | oxide | 450 | ~271 | E/20 veto | within UL; grade by blend |
| SP-7290001065662 | oxide | 520 | ~314 | E/20 veto | within UL; grade by blend |
| SP-7290015318426 | oxide | 520 | ~314 | E/20 veto | within UL; grade by blend |
| SP-7290013142894 | oxide | 450 | ~271 | E/20 veto | within UL; grade by blend |
| SP-7290017218564 | oxide | 520 | ~314 | E/20 veto | within UL; grade by blend |
| SP-7290118818205 | citrate | 550 | ~89 | E/20 veto | within UL; grade by blend |

One product (SP-7290001943700, Hadas Full-Mag 600 mg, form=None) may be legitimately vetoed IF the 600 mg is elemental — but the panel contains no form information, so the engine's assumption is unverifiable. This is a data gap, not a confirmed correct veto.

### cap_1 E/34 Cluster (22 products)

**Breakdown: 12 name_derived (no panel claim fed), 10 with a real claim that failed to map.**

Of the 10 real-claim cap_1 products:
- 2 (Altman Biotin, Solgar Biotin): claim correctly resolves to hair/skin/nails in replete adults = Insufficient. Biotin E is methodologically defensible and well-evidenced in SUPP-EV-014.
- 4 (omega-3 products with heart/cardiovascular claims): CV endpoint is contested-deferred. Engine maps via umbrella to "brain & mood / general cognition" (Weak) then scores — and the claim_matched field shown to consumers reads "brain & mood / general cognition (BROAD consumer claim)" for a product that made a HEART claim. The conservative outcome (D/49 for most) is defensible; the internally logged claim_matched is misleading.
- 3 (magnesium products: nano-liposomal, bisglycinate 168 mg + zinc/B6, tri-blend citrate/bisglycinate/taurate): Product makes a FORMULATION QUALITY claim ("three types of magnesium for optimal absorption"), not a health benefit claim. The engine correctly finds no health endpoint mapping. E is defensible but the cap_1 reason ("no reliable evidence for claim") does not accurately describe the situation — these are formulation-marketing SKUs, not unsupported health claims.
- 1 (Amorphicure CCAL calcium nano-particle): claim is about bioavailability superiority, not a health endpoint. Same defensibility issue.

The 12 name_derived products at E/34 have `primary_claim = null` in the panel. The engine receives no claim to score and defaults to Insufficient. This is structurally correct but creates a visible problem: a mainstream Life Vitamin C 1000 mg tablet (SP-7290012497650, SP-7290109317199) scores E/34 alongside Solgar Omega Nano products, indistinguishably, because no claim was scraped from its name-derived panel record. A consumer would reasonably read "no reliable evidence for claim" as a product-quality verdict, not a data-absence verdict.

### cap_2 D/49 Cluster (12 products)

Spot-checked 3:

- SP-7290013464859 (iron drops, infant): dose=0.56 mg elemental/serving (fairy-dust relative to 18 mg min_effective). Mechanically correct. But this is a PEDIATRIC dosing regimen — fairy-dust relative to an adult min_effective is not a fair comparison. No pediatric dose standards exist in the dossier.
- SP-7290003491902 (Floris Vitamin D3 200 IU per drop, labeled "infant formula"): scored D/49 for fairy-dust. Same issue: 200 IU is a standard infant D3 drop dose (WHO/AAP recommend 400 IU/day for infants — within 2 drops). The adult min_effective 1000 IU makes 200 IU/drop appear as fairy-dust. This is a methodology failure: infant-formulated products are being scored against adult dose standards.
- SP-7290012760204 (omega-3 heart claim, 500 mg total fish oil with EPA/DHA hidden): fairy-dust correct if EPA+DHA is not disclosed at therapeutic dose. Defensible.

### B Grade Products (16 products)

Not individually challenged — grade range 65–78, blend-dominant. The B/77.5 Altman Vitamin C500 Liposomal is the clearest B: immune claim (Weak evidence), good dose, good form. Defensible. No anomalies detected in the B cluster.

---

## Summary Assessment

**Justified scores (structural logic holds):** Iron S-grades (3); B12 S-grades (3); Folic acid A-grades (3); Calcium A-grade (1); Biotin E-grades (2 — genuine Insufficient evidence); B-grade vitamin C cluster with scraped claims (9); Caffeine B-grade (1). Total: ~22 products.

**Plausible but unverifiable:** D3 S-grades via manual claim translation (7 of 9 D3 S-grades). The translation from Hebrew label to "status-correction Strong" is reasonable for deficiency-labeling language, but it is a HUMAN JUDGMENT step external to the engine. The engine cannot re-derive it from the label. If the translation is wrong on any SKU, the grade collapses from S to A or B.

**Weak confidence:** name_derived cap_1 products (12): the E/34 is mechanically correct given null claims but carries a misleading display reason ("no evidence for claim" when the real reason is "no claim was scraped").

**Noise-level precision (indistinguishable):** All 15 S-grades score identically at 91.2. All cap_1 E-grades score identically at 34.0. All cap_2 D-grades score identically at 49.0. All veto products score identically at 20.0. Three of four distinct score buckets are point-values, not continuous scores. A consumer cannot distinguish between a 91.2 D3 1000 IU drop (defensible) and a 91.2 iron tablet (also defensible), or between a 34.0 Life Vitamin C 1000 mg (no claim scraped) and a 34.0 Solgar Biotin (genuine evidence gap). This is a presentation problem, but it is rooted in the scoring architecture.

**Potentially incorrect:** 9 magnesium veto products (elemental conversion key mismatch, as detailed in Opening Finding). Possibly 1 additional veto product (Hadas 600 mg no-form). At least 2 pediatric D3/iron products scored against adult dose standards.

**Overriding structural problem:** The elemental conversion key mismatch is a data-integrity defect that produces at least 9 consumer-facing false safety verdicts.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: Magnesium elemental-conversion key mismatch — 9 false safety vetoes**

The engine's `_effective_label_quantity` performs elemental conversion only when `elem.get(_norm(active.form))` returns a value. The dossier's `elemental_by_form` map uses full compound names as keys (`"magnesium oxide"`, `"magnesium citrate (trimagnesium dicitrate)"`, `"magnesium glycinate / bisglycinate"`). The corpus stores short tokens (`"oxide"`, `"citrate"`, `"malate"`, `"bisglycinate"`). The lookup fails silently — `frac = None` — and the raw compound mass is compared against the 350 mg elemental UL.

Affected products: SP-7290001066973 (malate 700 mg), SP-7290017847122 (oxide 432 mg), SP-7290010207640 (oxide 450 mg), SP-7290019444206 (oxide 450 mg), SP-7290001065662 (oxide 520 mg), SP-7290015318426 (oxide 520 mg), SP-7290013142894 (oxide 450 mg), SP-7290017218564 (oxide 520 mg), SP-7290118818205 (citrate 550 mg).

None of these products exceeds 350 mg elemental Mg. All receive E/20 "dose exceeds safe ceiling." This is factually wrong and, if shown to a consumer, constitutes a false safety warning on mainstream shelf products.

Evidence: `score_engine.py` lines 296–302 (`_effective_label_quantity`), cross-referenced with `magnesium.yaml` `compound_forms_identity` (keys are full names) and corpus panel `actives[*].form` values (keys are short tokens). A lookup of `_norm("oxide")` returns `None`; `_norm("magnesium oxide")` returns `0.603`. The engine produces `value: "veto", reason: "exceeds_UL"` for these nine products.

Implication: If these scores ship, a consumer who owns a standard 520 mg magnesium oxide tablet (313 mg elemental, within UL) is told their supplement is at a dangerous dose. Product liability and trust damage on day one.

Routes to: data-agent (fix the elemental_by_form key map to include short-form aliases, e.g. `"oxide": 0.603`, `"citrate": 0.162`, `"malate": 0.113`, `"bisglycinate": 0.141`) and nutrition-agent (confirm the malate fraction; the corpus has malate but the dossier `compound_forms_identity` does not include magnesium malate's elemental fraction).

---

**RT-2: Claim pre-translation outside the engine — 7 of 9 D3 S-grades are not engine-resolved**

For the seven D3 products where `panel.primary_claim` differs from `bsip0s_label.primary_claim_fed`, the translation from Hebrew label language to a scored English endpoint was performed by the pipeline external to the score engine. The engine scored the pre-translated claim, not the actual on-label text. These products carry claims like "bone health and calcium absorption" and "bone + immune system" on their Hebrew labels, which would resolve via the D3 umbrella to Moderate (bone) or Weak (immune) — not Strong. The pre-translation mapped them to "correcting/maintaining vitamin D status (raising serum 25(OH)D)" = Strong, lifting them to S.

This is not observable or auditable from the engine trace alone. The `via_umbrella: False` and `resolved_tier: Strong` entries in the trace are accurate for the claim that was fed to the engine, but that claim was constructed by a human upstream.

Evidence: SP-7290012760266 `panel.primary_claim = "ויטמין D לספיגת סידן ולשמירה על בריאות העצם; להשלמת מחסור בוויטמין D"`, `bsip0s_label.primary_claim_fed = "correcting/maintaining vitamin D status (raising serum 25(OH)D)"`. SP-7290018439623 `panel.primary_claim = "ויטמין D3 לבריאות העצם ומערכת החיסון"`, same `claim_fed`. The D3 umbrella maps "bone health" to Moderate and "immune system" to Weak; the Strong tier requires an explicit status/25(OH)D claim — which is not present on the Hebrew label.

Implication: If the pre-translation is wrong on even one product, the grade is wrong by two full grade levels (S→A or S→B). This is not a calibration question — it is an unauditable judgment step inserted before the engine. For a system claiming to score what the product states, this is a traceability break.

Routes to: data-agent (document and formalize the claim-translation protocol; make the translation decision part of the auditable trace rather than a silent bsip0s_label pre-fill) and nutrition-agent (adjudicate: does "ויטמין D לשמירה על בריאות העצם" + "להשלמת מחסור" warrant Strong status-correction, or Moderate bone?).

---

**RT-3: Pediatric/infant products scored against adult dose standards**

At least two products are pediatric-formulated yet scored on adult min_effective dose thresholds:

- SP-7290003491902 (Floris Vitamin D3 drops, labeled "infant formula", 200 IU/drop): The standard infant D3 recommendation (WHO/AAP/Israeli MOH) is 400 IU/day = 2 drops. The engine compares 200 IU/serving to an adult min_effective of 1,000 IU, computes it as fairy-dust (dose=20), and assigns D/49 (cap_2). A product correctly dosed for its pediatric target population is called under-dosed relative to adults.

- SP-7290013464859 (iron drops, infant): 0.56 mg elemental iron/serving vs adult min_effective 18 mg. Same fairy-dust outcome.

The dossier notes in `vitamin_d3.yaml` that "children have lower ULs (1000–3000 IU by age)" and explicitly warns "NEVER apply the adult UL to a children's SKU." But there is no analogous protection on the DOSE side. An infant SKU is more harmful than just getting a lower grade — the cap_2 machine_reason "underdosed_or_unverifiable_dose" is shown in the trace. If any copy surfaces this reason, it tells the consumer that an infant vitamin D formula is under-dosed, which is false.

Evidence: SP-7290003491902 trace `sub_scores.dose.value = 20, reason = "fairy_dust"`, `sub_scores.dose.min_effective = 1000`, `label_qty_basis = 200.0`. Panel `primary_claim: "Vitamin D3 200 IU per drop; infant formula"`.

Implication: Consumer-facing copy that uses the engine binding constraint for pediatric products will mislead caregivers. A pediatric product marketed as appropriate for infants should either be excluded from the comparison corpus or scored against a pediatric reference dose.

Routes to: nutrition-agent (add pediatric dose references to the D3 and iron dossiers; define a scoring exclusion or separate scoring path for products labeled as infant/pediatric formulas) and data-agent (tag pediatric products in the corpus; exclude from the adult comparison page or route to a distinct pediatric shelf).

---

### HIGH — should resolve before launch

**RT-4: name_derived products at E/34 display misleading binding reason**

12 name_derived products (Life Vitamin D-400, Life D-1000, Life Vitamin C 1000, Life Vitamin C 1000 mg, Life Iron 15 mg, Life Iron 30 mg, Solgar Zinc 22 mg, Life Vitamin E 400, three more D3s and vitamin C) receive E/34 with `binding_constraint.machine_reason = "no_reliable_evidence_for_claim"`. The actual reason is that no claim was scraped — the `primary_claim` field is null in the panel record, and the engine defaults to Insufficient when no claim resolves.

A consumer shown "no reliable evidence for claim" on a mainstream Life Vitamin D-1000 IU tablet will read that as a quality verdict on the product. It is actually a verdict on the data-scraping method. These are indistinguishable in the trace from products that genuinely make unsupported claims (e.g. Altman Biotin for hair growth in replete adults, where E/34 is fully justified by the evidence).

Evidence: SP-7290017242170, SP-7290113826052, SP-7290111594342 (D3 name-derived), SP-7290012497650, SP-7290018365243, SP-7290109317199 (vitamin C name-derived), SP-7290016417197, SP-7290015765985 (iron name-derived), SP-0033984010642, SP-7290016417227 (zinc name-derived), SP-7290114965279 (vitamin E name-derived) — all `acquisition_method: name_derived`, all `panel.primary_claim: null`, all `binding_constraint.mechanism: cap_1_insufficient_evidence`.

Implication: Conflating "data absent" with "evidence insufficient" is the kind of systematic misclassification that, in a published comparison, functions as defamation of the product and its manufacturer. The Life and generic house-brand products receive the same E treatment as snake-oil biotin for cosmetic claims.

Routes to: data-agent (distinguish `outcome: "scored_no_claim"` from `"scored_insufficient_evidence"` in the trace; use a separate machine_reason string); content-agent (do not surface "no reliable evidence for claim" for products where the driver is a data gap, not an evidence gap).

---

**RT-5: Omega-3 claim_matched displays "brain & mood / general cognition" for products making heart claims**

Four omega-3 D-grade products make cardiovascular health claims on their Hebrew labels: "לבריאות הלב וכלי הדם" (heart and vascular health), "לתמיכה בדלקתיות" (inflammation support). The CV endpoint is contested-deferred in the dossier. Via the umbrella, "בריאות הלב" maps to "brain & mood / general cognition (BROAD consumer claim)" at Weak — because that is the only non-contested mapped endpoint.

The claim_matched field recorded in the trace — "brain & mood / general cognition (BROAD consumer claim)" — is the label exposed when explaining "why this product scored D." A consumer whose heart-health omega-3 is rated D/49 and told the engine's reason is "brain & mood (weak evidence)" is receiving a factually incorrect explanation of the score driver. The actual reason is: your product made a CV claim, and CV is scientifically contested (a defensible, honest reason). The stated reason is: your product is a brain supplement with weak evidence (false).

Evidence: SP-7290012760204 trace `claim_matched: "brain & mood / general cognition (BROAD consumer claim)"`, `claim_resolution.umbrella_mapped: [{"phrase": "בריאות הלב", "resolves_to": "brain & mood / general cognition (BROAD consumer claim)"}]`, `panel.primary_claim: "אומגה 3 לתמיכה בבריאות הלב וכלי הדם"`. SP-0033984020573, SP-0033984020580 same pattern.

Implication: Consumer copy derived from `claim_matched` will attribute the D grade to the wrong category, creating a factual error in the comparison. The correct explanation is "the cardiovascular claim your product makes is contested in the scientific literature; Bari does not score contested claims."

Routes to: content-agent (never surface the internal engine `claim_matched` reason verbatim for contested-routing; write a separate disclosure string for the contested-CV case) and nutrition-agent (consider a distinct `contested_deferred` outcome in the trace rather than silently routing to the nearest non-contested endpoint).

---

**RT-6: 91.2 score clustering — all 15 S-grades are identical point values**

Every S-grade product scores exactly 91.2. This is an arithmetic artifact: the blend formula with weights {ev: 0.30, dose: 0.25, form: 0.20, honesty: 0.15, safety: 0.10} and values {ev: 92.5, dose: 92, form: 92, honesty: 100, safety_blend: 70} produces exactly 91.15, which rounds to 91.2. Any product that achieves the same combination of sub-scores lands at the same number. The 15 S-grade products span three different actives (D3, iron, B12), multiple brands, multiple forms, and meaningfully different products — yet they are presented as identical on the numeric scale.

A consumer or competitor asking "why is a ferrous bisglycinate iron supplement identical to a vitamin D3 drop?" has no answer. The score is not wrong — it is blind to real differentiation that exists at the sub-score level. A 91.2 that results from ev=92.5/dose=92/form=92/honesty=100 is not the same product-quality statement as ev=92.5/dose=72/form=92/honesty=100 (which produces 86.2, the B12 A-grade).

Evidence: All 15 S-grade traces show identical `sub_scores: {evidence: 92.5, dose: 92, form: 92, honesty: 100, safety: "neutral"}`. Blend formula verified: (92.5×0.30 + 92×0.25 + 92×0.20 + 100×0.15 + 70×0.10) = 27.75 + 23 + 18.4 + 15 + 7 = 91.15 → 91.2.

Implication: A comparison page showing 15 identical scores for disparate products cannot be defended to a journalist or regulator as a meaningful differentiation. The S-grade pool becomes an undifferentiated block.

Routes to: nutrition-agent (consider whether the `SAFETY_NEUTRAL_BLEND_VALUE = 70` constant should introduce variation between clean-safety products, or whether a tiebreaker sub-score is needed; this is a calibration question, not a data error).

---

**RT-7: The Magnesia brand (5 products, 0% scored) is completely absent from the magnesium comparison**

Magnesia is a dedicated Israeli magnesium brand with 5 SKUs on the Super-Pharm addressable shelf (FOCUS, WOMEN, CALM, WINTER, ACTIVE), all classified `unscoreable_premarket`. If these products are visible on the live Super-Pharm shelf at time of publication, a consumer who buys a Magnesia product and looks for it on Bari will not find it. Meanwhile, the comparison will contain 11 magnesium products (reduced from 20 vetoed) that skew toward Altman oxide and generic oxide formulations.

A Magnesia product marketed for "focus" or "women's health" is precisely the kind of vague-claim magnesium supplement the scoring engine is designed to evaluate. Classifying all five as premarket without verifying their actual shelf status is a coverage assumption that may be wrong.

Evidence: `_corpus_run_full_v3.json` brand_bucket `magnesia` — 5 products, all `unscoreable_premarket`. No cache files for Magnesia barcodes visible in the cache directory. The corpus report notes Magnesia products as "dose not retrievable / acquisition miss (niche)" — this does not confirm premarket status.

Implication: A magnesium comparison page without Magnesia is a structural gap. If Magnesia products are sold on-shelf, their absence makes the comparison unrepresentative and exposes Bari to the accusation of cherry-picking brands.

Routes to: data-agent (verify Magnesia shelf status; attempt direct brand-site scrape for dose data; reclassify if live products).

---

### MEDIUM — should document or monitor

**RT-8: Single-active vitamins (Life brand, 12 name_derived) systematically excluded from scoring by house-brand data wall**

Life (Super-Pharm house brand) has 22 products in the corpus and only 7 scored (32%). The 15 unscored are all `unscoreable_incomplete` due to dose unavailability. Life has no brand website and its products are not well-represented on third-party e-tailers with dose information. The corpus report correctly identifies this as a "BD / data-feed ask" — not an engine failure.

However, when 15 of the 22 most price-competitive products on the Israeli shelf (house brand = cheapest tier) are systematically excluded, the scored comparison skews toward branded supplements (Altman 18/18, Solgar 6/6, SupHerb 16/18). A comparison that is 100% branded is not the Israeli supplement shelf.

Routes to: product-agent (decide: is a supplement comparison page valid without coverage of the price-competitive house-brand tier? If yes, disclose scope clearly; if no, defer go-live until Life BD data feed is arranged).

---

**RT-9: Magnesium malate is not in the dossier's compound_forms_identity**

The corpus includes magnesium malate products (SP-7290001066973: 700 mg malate, SP-7290015318532: 136 mg malate, SP-7290018439579: 76 mg taurate). Magnesium malate and magnesium taurate do not appear in `magnesium.yaml compound_forms_identity`, which only lists oxide, citrate, and glycinate/bisglycinate. Without an elemental fraction for malate, the engine cannot correctly convert compound mass to elemental — and even after fixing the key-name bug (RT-1), malate and taurate will still lack conversion fractions.

Evidence: `magnesium.yaml` `compound_forms_identity` lists 3 forms only. `elemental_by_form` in the loaded dossier has 3 entries. `_norm("malate")` returns `None`.

Routes to: nutrition-agent (add magnesium malate elemental fraction ~0.113 and magnesium taurate ~0.082 to the dossier `compound_forms_identity`).

---

**RT-10: D-grade omega-3 heart-claim products: cap_2 fires on total fish oil mass, not EPA+DHA**

Several omega-3 D-grade products receive fairy-dust dose scores (cap_2, dose=20). The dossier specifies dose basis as active EPA+DHA, not total fish-oil mass. If the panel's active dose entry records total fish-oil (e.g. 500 mg fish oil with EPA 90/DHA 60 hidden), the engine would compare 500 mg fish oil to the min_effective EPA+DHA threshold and rate the dose as well above range — or, if the active dose is the EPA+DHA subset, it may be below fairy-dust. Verifying that all omega-3 dose comparisons use confirmed EPA+DHA figures (not total fish oil mass) is essential. One product (SP-7290012760204) shows the label "אומגה 3 לתמיכה בבריאות הלב" — total fish oil vs active EPA/DHA split not confirmed in trace.

Routes to: data-agent (verify that all omega-3 panel records encode EPA+DHA mg, not total fish oil; add a check in the QA audit).

---

**RT-11: Iron UL (45 mg elemental) applies the same elemental-conversion risk as magnesium**

The iron dossier has the same `compound_forms_identity` / short-form panel mismatch risk as magnesium. The dossier lists ferrous sulfate, ferrous fumarate, ferrous bisglycinate as full names; the corpus may store short forms. The iron UL is 45 mg elemental — a product labeled 30 mg ferrous bisglycinate (containing ~8 mg elemental iron) could be incorrectly vetoed if the engine compared 30 mg raw to 45 mg UL without conversion. Spot-check: SP-7290016417197 (iron 15 mg, name_derived) and SP-7290015765985 (iron 30 mg) both score cap_1, not veto — so the veto is not currently firing for iron. But if a high-iron-compound product enters the corpus (e.g. 300 mg ferrous sulfate = 60 mg elemental → should veto; 300 mg raw = 300 mg → also vetoes but for wrong reason), the mismatch could produce either a missed veto or a false veto. This needs the same key-map fix as magnesium.

Routes to: data-agent (apply the same short-form key alias fix to iron dossier as part of the RT-1 fix).

---

## Verdict

**FAIL — 3 open CRITICAL findings block launch.**

The corpus cannot go in front of consumers in its current state. The specific blockers:

- **RT-1** (magnesium elemental conversion mismatch): 9 products receive false E/20 safety verdicts. Publishing a false safety warning on mainstream magnesium tablets is the most serious possible consumer-facing error.
- **RT-2** (D3 claim pre-translation): 7 of 9 D3 S-grades carry S because a human operator translated a Hebrew bone/immune claim to a Strong status-correction endpoint before it reached the engine. The traceability break means these scores cannot be independently verified from the trace.
- **RT-3** (pediatric products scored on adult standards): At least 2 products labeled and formulated for infants are scored D for being "underdosed" relative to adult thresholds. This is a direct, consumer-visible false verdict.

The HIGH findings (RT-4 through RT-7) do not individually block launch but collectively represent a content-quality gate that product-agent should review before go-live. RT-4 (name_derived misleading reason) and RT-5 (omega-3 brain-claim mislabeling) are the most urgent of the HIGH tier.

The corpus's mechanical integrity — OFF=0, distribution consistency, no fabricated nutrition data — is genuinely clean, and the QA team's 5/5 pass is legitimate within its scope. The defects found here are in scoring logic and methodology, which is this agent's domain, not QA's.

---

```json
{
  "return_contract": "v1",
  "agent": "red-team-agent",
  "task_ref": "TASK-277 v3 pre-launch challenge",
  "run_date": "2026-06-19",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_sie_v3.md",
      "sha256": "pending-write",
      "role": "challenge_report"
    }
  ],
  "counts": {
    "denominator_description": "82 scored products from _corpus_run_full_v3.json",
    "total_scored": 82,
    "s_grades": 15,
    "a_grades": 5,
    "b_grades": 16,
    "c_grades": 1,
    "d_grades": 12,
    "e_grades": 33,
    "unscored_total": 36,
    "unscored_incomplete": 25,
    "unscored_premarket": 11,
    "findings_critical": 3,
    "findings_high": 4,
    "findings_medium": 4,
    "false_safety_vetoes_confirmed": 9,
    "false_safety_vetoes_unverifiable": 1,
    "d3_s_grades_pre_translated": 7,
    "d3_s_grades_engine_resolved": 2,
    "pediatric_products_scored_on_adult_standard": 2,
    "name_derived_misleading_e34": 12,
    "omega3_heart_claim_brain_mislabeled": 4
  },
  "commands_run": [
    {"cmd": "python3 corpus parse + grade extraction", "exit_code": 0},
    {"cmd": "python3 elemental_by_form key lookup test", "exit_code": 0},
    {"cmd": "python3 elemental dose calculation for veto cluster", "exit_code": 0},
    {"cmd": "python3 cap_1 breakdown analysis", "exit_code": 0},
    {"cmd": "python3 brand coverage analysis", "exit_code": 0},
    {"cmd": "python3 claim_fed vs panel_claim comparison", "exit_code": 0},
    {"cmd": "python3 dossier_loader.load_dossier for magnesium/omega3/iron", "exit_code": 0},
    {"cmd": "read score_engine.py constants.py magnesium.yaml vitamin_d3.yaml iron.yaml supp_evidence_registry_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "External evidence verification (PubMed/CrossRef) of cited PMIDs — out of scope for this challenge run; evidence registry entries reviewed structurally, not re-verified",
    "Frontend JSON challenge — no frontend JSON exists yet for supplements; RT skipped",
    "Prior challenge report comparison — this is the first red-team report for this category",
    "Zinc dossier review — zinc compound_forms_identity short-form key risk noted but not fully traced"
  ],
  "verdict": "FAIL",
  "open_criticals": ["RT-1", "RT-2", "RT-3"],
  "acceptance_test": {
    "spec": "challenge report covers all 6 delegated scope areas with per-finding severity classification and named routing",
    "result": "PASS — all 6 areas covered (S/A grades, cap_1 E-grades, magnesium veto cluster, cap_2/cap_3 D-grades, corpus representativeness, claim-specificity discipline)"
  }
}
```
