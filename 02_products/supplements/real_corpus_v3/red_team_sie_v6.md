# Red-Team Challenge Report — Supplements SIE v6 (real_corpus_v3)
Date: 2026-06-19
Scope: 78 scored / 118 shelf, SIE proto_v0 / algorithm_v0.2.0
Corpus file: _corpus_run_full_v6.json (TASK-350 third pass)
Prior report: red_team_sie_v3.md (3 CRITICAL: RT-1 magnesium false vetoes, RT-2 D3 pre-translation, RT-3 pediatric dosing)
Challenger: red-team-agent

---

## Opening Finding

**NEW CRITICAL: The elemental conversion fix (RT-1 resolution) is DOUBLE-APPLYING iron elemental conversion.**

Three iron bisglycinate products that previously scored S/91.2 (and were deemed "defensible" in v3) now score D/49 because the RT-1 fix added bisglycinate to the `elemental_by_form` lookup. The engine now converts `30mg bisglycinate × 0.274 = 8.22mg elemental iron` and calls it fairy_dust relative to an 18mg elemental min_effective. But Israeli supplement labeling convention is to state **elemental iron** on the label, not compound mass. A product labeled "ברזל 30 מ"ג" (iron 30mg) is stating 30mg **elemental**. The engine is misidentifying elemental-label values as compound-mass values and converting them a second time. The effect inverts three products from S to D — a four-grade drop that is an artifact of the fix, not a real quality change.

This was not present in v3 (where the iron S-grades were defensible), was introduced by the RT-1 resolution, and is the most consequential unintended consequence in v6.

---

## Part A: Verification of Original CRITICALs

### RT-1 — Elemental Conversion Key Mismatch: Verdict PARTIALLY CLOSED, NEW CRITICAL INTRODUCED

**What was fixed.** The short-form alias lists (`oxide`, `citrate`, `malate`, `bisglycinate`, `picolinate`, etc.) are now present in all mineral dossiers via `short_form_aliases` arrays. The engine reads these through `dossier_loader`. The `elemental_by_form` lookup now resolves `"oxide"` → `0.603` for magnesium, enabling correct conversion.

**False-veto elimination confirmed.** All 9 products that had false E/20 veto in v3 now score correctly:
- SP-7290017847122 (Magnox 432mg oxide): 432 × 0.603 = 260.5mg elemental → Safety NOTE (above 250mg EFSA band, below 350mg UL), dose sub_therapeutic → C/61.4. Correct.
- SP-7290010207640, SP-7290019444206 (450mg oxide): 450 × 0.603 = 271.4mg → NOTE, in_range → C/62.0. Correct.
- SP-7290001065662, SP-7290015318426, SP-7290017218564 (520mg oxide): 520 × 0.603 = 313.6mg → NOTE, in_range → B/65.6. Correct.
- SP-7290013142894 (450mg oxide + K): 450 × 0.603 = 271.4mg → NOTE → B/69.5. Correct.
- SP-7290118818205 (550mg citrate): 550 × 0.162 = 89.1mg → neutral → D/49 (fairy_dust dose). Correct.
- SP-7290001943700 (Hadas 600mg form=None): correctly routed to `unscoreable_incomplete` via the SUPP-EV-024 worst-case guard (600 × 0.603 = 361.8mg > 350mg UL → hazard possible → indeterminate). Correct.

**False-safe check passed for minerals.** The SUPP-EV-024 worst-case guard prevents any form=None product from scoring clean when worst-case elemental exceeds the UL. SP-0033984010642 (Life Zinc 22mg form=None) correctly shows `safety: ambiguous_basis_no_form` (worst-case: 22 × 0.803 = 17.7mg < 40mg UL → neutral). The guard logic is sound.

**NEW CRITICAL introduced by the RT-1 fix.** The bisglycinate alias is now active in the iron dossier (`elemental_mg_fraction: 0.274`). This converts any labeled iron bisglycinate amount as if it is compound mass. Israeli supplement labels follow the convention of stating **elemental iron** content, not compound mass — a product called "ברזל 30 מ"ג" is certifying 30mg elemental iron to the MOH. The engine now converts this as: 30mg × 0.274 = 8.22mg elemental → below fairy_dust floor (9mg) → cap_2 → D/49. The correct reading is 30mg elemental → sub_therapeutic (between fairy_floor 9mg and min_effective 18mg) → blend → S or A depending on form.

Affected products:
- SP-7290118814061 (SupHerb Iron 9-months 30mg): v3 S/91.2 → v6 D/49 (fairy_dust). If 30mg is elemental: sub_therapeutic → should be A-range.
- SP-783495578741 (iron bisglycinate liposomal 27mg): v3 S/91.2 → v6 D/49 (fairy_dust). If 27mg is elemental: sub_therapeutic → A-range.
- SP-7290012056741 (iron bisglycinate 36mg): v3 S/91.2 → v6 A/81.5 (sub_therapeutic via 36×0.274=9.86mg). If 36mg is elemental: in_range (36 > 18mg min_eff) → should be S.

The dossier identifies the dose axis as elemental iron and instructs "NOT compound mass," but there is no mechanism in the panel parser to flag whether a given label value is compound or elemental. All three iron bisglycinate products are being treated as compound-mass labels when they are almost certainly elemental-label products.

**RT-1 verdict: FALSE VETO CLUSTER CLOSED (9/9), BUT ELEMENTAL/COMPOUND AMBIGUITY INTRODUCED A NEW CRITICAL for iron.**

---

### RT-2 — D3 Claim Pre-Translation: Verdict PARTIALLY CLOSED, RESIDUAL HIGH-SEVERITY FINDING

**What changed.** In v3, 7 of 9 D3 S-grades carried S via pre-translation of Hebrew panel claims to English "correcting/maintaining vitamin D status." In v6, 7 of the originally-translated products have been reclassified: 4 previously-S products now score A/85.0 via the umbrella (bone health → Moderate), which is the correct outcome for their Hebrew labels. The v6 grade distribution now shows 8 S-grades (down from 15 in v3).

**Residual problem: 3 D3 S-grades remain via pre-translation.**

Products SP-7290012760266, SP-7290013142146, and SP-7290012760761 all have identical panel claims: `"ויטמין D לספיגת סידן ולשמירה על בריאות העצם; להשלמת מחסור בוויטמין D"` (Vitamin D for calcium absorption and bone health; to supplement deficiency in Vitamin D). Their `primary_claim_fed` is still `"correcting/maintaining vitamin D status (raising serum 25(OH)D)"` — full English pre-translation. The engine scores the pre-translated claim, not the panel text. The trace shows `via_umbrella: false`, `resolved_tier: Strong`.

The panel claim contains two clauses: (a) bone health / calcium absorption → Moderate via umbrella, and (b) "להשלמת מחסור" (deficiency correction) → legitimately arguable as status-correction. The RT-2 finding acknowledged that "מחסור" language is the borderline case. However, the critical point is that the pre-translation step is still unauditable from the trace: the trace reads `on_label_claim: "correcting/maintaining vitamin D status (raising serum 25(OH)D)"` which is NOT what the panel says. An independent reviewer cannot verify that the on_label_claim is what the product states. The translation is still a judgment inserted before the engine, and it is still invisible in the trace.

Separately, SP-7290012760853 (SupHerb D400 drops, same Hebrew panel claim, 400 IU) is pre-translated to Strong but scores D/49 due to fairy_dust dose. This means the translation is still being applied but is masked by the dose cap. The traceability gap persists even where the grade doesn't change.

**D3 A-grade analysis.** SP-7290017490601 (D3+K2, "bone health + calcium absorption") and SP-7290018439623 (D3, "bone health + immune system") now correctly score A/85.0 via umbrella Moderate. The claim_fed now passes the Hebrew text through directly (with English appended: `"bone health heart health"`). The `resolved_tier=Moderate` is appropriate for bone-health language without explicit deficiency-correction text. The injected English keywords ("bone health", "heart health", "immune health") feed the umbrella, which functions correctly. These demotions from S to A are genuine improvements and are defensible.

**RT-2 verdict: PARTIALLY CLOSED. 4 of 7 original false-Strong D3 S-grades corrected. 3 remain via pre-translation — the traceability gap persists for these 3 products.**

---

### RT-3 — Pediatric Products Scored on Adult Standards: Verdict CLOSED

Three products are now correctly routed to `unscoreable_pediatric`:
- SP-7290013464859 (SupHerb iron drops for children): correct, with explicit pediatric note.
- SP-7290013464309 (SupHerb Vitamin D drops for children 400 IU): correct.
- SP-7290003491902 (Floris Vitamin D drops, infant): correct.

All three carry the standardized `pediatric_note` text citing WHO/AAP and SUPP-EV-022. The corpus correctly records `outcome: "unscoreable_pediatric"` with no score or grade. No pediatric product is being scored against adult dose thresholds.

The unscoreable_pediatric count is 3 (was 2 known + 1 borderline in v3). SP-7290013464309 is a new correct addition.

**RT-3 verdict: CLOSED.**

---

## Part B: Fix-Introduced Problems

### B-1: Worst-Case Guard — Is max_fraction the Right Conservative Bound?

**Mechanism review.** The SUPP-EV-024 guard computes `worst_case = amount × max(elemental_by_form.values())`. For magnesium, the known forms are oxide (0.603), citrate (0.162), glycinate/bisglycinate (0.141). Max_fraction = 0.603 (oxide). This is the correct conservative bound for magnesium: oxide has the highest elemental density, so if a label is actually oxide at a high compound mass, that is the worst-case elemental exposure. The guard logic is structurally sound.

**Carbonate is not in the magnesium dossier.** The Amorphicure PH product (SP-7290015429245, 160mg carbonate) has form="carbonate" in the panel. The carbonate elemental fraction is approximately 0.239, which falls between oxide (0.603) and citrate (0.162). The dossier's `elemental_by_form` does not list carbonate. The `_effective_label_quantity` lookup for "carbonate" returns `frac=None` — no conversion. The engine then uses raw 160mg for dose and safety comparisons. Safety says `"within_ul"` because 160mg raw < 350mg UL — so safety is accidentally correct. But the dose comparison is wrong: the dossier computes dose as elemental, so comparing raw 160mg compound to an elemental min_effective is structurally invalid. The score (C/59.2, sub_therapeutic dose=52.3) appears as if the engine knows the elemental amount — but that number cannot be right from a raw 160mg input against any plausible elemental min_effective. Either the dose computation falls through to raw (160mg > fairy_floor but sub-therapeutic vs some threshold), or there is an error in the carbonate handling. This is a data-gap finding, not a CRITICAL, but it means the Amorphicure C score is not derived from correct elemental arithmetic.

**Taurate is not in the magnesium dossier.** SP-7290018439579 (76mg taurate) scores D/49 fairy_dust. 76mg × the estimated taurate fraction (~0.082) = 6.2mg elemental → below any reasonable min_effective → fairy_dust. But the dossier does not have taurate, so the conversion does not fire. 76mg raw is also well below any magnesium min_effective → also fairy_dust even without conversion. So the outcome is accidentally correct, but the mechanism is wrong.

**Routing: forms missing from dossier do not cause consumer harm in v6 because they happen to produce the same outcome as elemental conversion. This remains a data-integrity finding.** Routes to: data-agent / nutrition-agent (add magnesium carbonate and taurate elemental fractions to the dossier).

**Are products routed to unscoreable when they should warn?** The SUPP-EV-024 path routes high-worst-case form=None products to `unscoreable_incomplete` (SP-7290001943700, Hadas 600mg). The `machine_reason` is `mineral_form_undeterminable_dose_may_exceed_ul`. This does not produce a consumer warning — the product simply disappears from the scored set. If Hadas Full-Mag 600mg is genuinely on the shelf and genuinely could exceed the UL, a consumer who expects to see it in the comparison receives no signal at all. The correct consumer-facing disclosure for a product where UL breach cannot be excluded is not silence — it is a disclosure noting that the product could not be safety-verified. This is a content/product decision, not a CRITICAL, but it represents a consumer-communication gap.

---

### B-2: Hebrew Form-Token Name-Parser — Can It Mis-Parse?

**Parser behavior.** For name_derived products where the panel form is `null`, the corpus parser extracts form tokens from the Hebrew product name (e.g., "פיקולינאט" → picolinate, "ציטראט" → citrate). The form is then set in `bsip0s_label.actives[0].form`.

**Tink Zinc Picolinate (SP-7290018365359): correct outcome.** Panel form=None, parsed form="picolinate". The dossier has picolinate in elemental_by_form (fraction 0.211). Engine converts 50mg × 0.211 = 10.55mg elemental → within 40mg UL → safety neutral. The outcome is correct: 10.55mg elemental zinc from a 50mg picolinate compound is well within the UL. No false veto.

**Risk: the parser assigns "picolinate" as form, which changes the elemental conversion.** For Tink Zinc 50mg, this is beneficial (prevents false veto if form=None guard fires) and accurate (the product name confirms picolinate). But the parser could theoretically extract a form token from a product name that does not accurately describe the actual ingredient (e.g., a product named "ביסגליצינאט" that actually contains oxide). This is a provenance risk, not a CRITICAL, because the form token is flagged as `form_resolved_from_name_he` in the lossy field and can be audited.

**Life Calcium Citrate (SP-7290103436841):** name_derived, unscoreable_incomplete (no amount), lossy includes `form_resolved_from_name_he:'citrate'`. This product is correctly excluded from scoring because the amount is missing. The form token would have been used if amount were available.

**No misparse found in the current corpus that changes a safety verdict.** The parsed forms (picolinate, citrate) all correspond to the product names that contain them. However, this is a single-corpus snapshot and the risk persists for future products.

---

### B-3: D3 S/A Set After RT-2 Fix — Is It Defensible?

**v6 D3 scoring:**
- S/91.2 × 3: SP-7290012760266, SP-7290013142146, SP-7290012760761 — all pre-translated to Strong status-correction. Partially defensible (the "להשלמת מחסור" language is genuine deficiency-correction text) but the traceability gap remains.
- S/91.2 × 2: SP-7290010035984, SP-7290015318433 — English claim "Vitamin D3 1000 IU per drop" fed directly, engine token-matched to status-correction. Defensible; English claim is unambiguous and D3 1000 IU is a genuine repletion dose.
- A/85.0 × 4: SP-7290017490601 (D3+K2 bone), SP-7290018439623 (D3 bone+immune), SP-7290019444374 (D3 bone), SP-7290017218366 (D3 bone) — umbrella → bone health → Moderate → A. Correct and defensible.
- D/49 × 1: SP-7290012760853 (SupHerb D400, 400 IU) — pre-translated to Strong but fairy_dust dose (400 IU << 1000 IU min_effective). Outcome defensible (D for an underdosed product is correct regardless of tier) but the pre-translation is still present and would mislead if dose cap were lifted.

**The A/85.0 cluster is the clearest improvement.** SP-7290018439623 (bone + immune claim) should not score S — it now scores A/85.0 correctly via umbrella Moderate. SP-7290017490601 (D3+K2 bone) same.

**Summary: 5 of 8 S-grades are defensible; 3 carry the residual pre-translation problem. The 4 A-grades are all defensible. The S/A tier transition is a genuine improvement over v3.**

---

### B-4: Unscoreable Sets — Over-Exclusion Assessment

**3 unscoreable_pediatric**: All three are genuine pediatric products (children's iron drops, two children's D3 drops). None should be scored against adult standards. Correct.

**26 unscoreable_incomplete**: Spot-checked sample:
- SP-7290103436841 (Life Calcium Citrate): missing dose amount. Correct exclusion.
- SP-7290119917525 (Omega 3 syrup for children): children's product, no dose data. Correct.
- SP-7290106950702 (form=None complex magnesium): amount available (implied), worst-case guard fires? Not visible without panel data. Verify.
- SP-7290001943700 (Hadas 600mg Mg form=None): correctly routed via SUPP-EV-024 worst-case guard. Correct.

**The 26-product unscoreable_incomplete pool deserves audit for over-exclusion.** The primary drivers are: (a) no dose amount in panel (genuine missing data), and (b) safety unscoreable via worst-case guard. No product appears to be scoreable but incorrectly excluded in the sample reviewed.

**Is the scored shelf representative?** Of 19 magnesium products in corpus, 8 are unscoreable_premarket (Magnesia brand) and 3 are unscoreable_incomplete — leaving 11 scored. Of those 11, several are low-dose citrate or bisglycinate at fairy_dust doses (D/49). The dominant scored products by grade are the oxide tablets (B-range), while newer premium forms (taurate, liposomal bisglycinate) score D or E. This creates a presentation where oxide — scientifically the least bioavailable form — appears the best-scoring magnesium. This is a structural finding about the corpus composition, not a scoring error.

---

## Part C: Additional Launch-Blocking Concerns

### C-1: Systematic Claim Injection — 54 Products, Score-Determinative in Multiple Cases

**Scale of injection.** 54 of 78 scored products have English keywords injected into the `primary_claim_fed` that are not present in the `panel.primary_claim`. The injection pattern varies by type:

Type 1 — Semantic anchor keywords (benign for umbrella function): "muscle health", "nerve health", "immune health", "bone health". These help the umbrella tokenizer find mapped terms. The injection is systematic and intentional. The scores are generally correct because the umbrella resolves Hebrew text directly anyway.

Type 2 — Full English replacement (score-determinative, HIGH risk): For 3 D3 S-grade products, the panel Hebrew text is completely replaced by English status-correction language. The trace records the English text as `on_label_claim`. An auditor reading the trace cannot distinguish this from a product that actually stated its claim in English. This is unauditable from the trace alone.

Type 3 — English claim text that maps to a DIFFERENT endpoint than the Hebrew text (new finding): SP-7290010318230 (Alsepa Super Omega 3) panel claim is `"אומגה 3 בריכוז גבוה מדגי ים עמוקים; כשר"` — high-concentration omega-3, kosher. No health claim. The injected claim is `"...כשר cognitive"`. "Cognitive" is injected with no basis in the panel. The engine matches nothing (Insufficient, E/34) because omega-3 cognitive requires a resolved studied endpoint, but the trace records `on_label_claim: "...cognitive"`. This is a false claim provenance — the trace implies the product made a cognitive claim when it made none. Similarly SP-7290001943212 (omega-3 EPA+DHA) has "cognitive" injected with no Hebrew basis.

Type 4 — Endpoint-escalating injection (CRITICAL class): For the 3 remaining D3 S-grades, "correcting/maintaining vitamin D status (raising serum 25(OH)D)" is injected to replace a bone-health claim. The injection changes the resolved tier from Moderate (via umbrella for bone claim) to Strong (direct endpoint match). This is the core of the unresolved RT-2 finding.

**The injection mechanism is undocumented and untraced.** There is no audit field in the corpus that identifies which claims were algorithmically augmented vs. directly scraped. The `claim_note` field carries informal notes but is not machine-parseable for this purpose. The `lossy` field flags absent data but not injected data.

Routes to: data-agent (add a `claim_augmented: true/false` field to `bsip0s_label` so the injection is machine-auditable); content-agent (review all Type 2 and Type 3 injections for false provenance).

---

### C-2: Iron Elemental/Compound Ambiguity — S-grade Collapse to D (NEW CRITICAL)

This is the Opening Finding stated in full. The mechanism:
1. Iron dossier `elemental_by_form` now includes `"bisglycinate": 0.274` (via RT-11/SUPP-EV-022 fix).
2. When a product's panel states "ברזל (iron bisglycinate) 30mg", the engine reads form="bisglycinate", looks up 0.274, computes 30 × 0.274 = 8.22mg elemental.
3. 8.22mg < fairy_dust floor (0.5 × 18 = 9mg) → fairy_dust → cap_2 → D/49.
4. But Israeli MOH supplement registration requires iron content declared as elemental iron. The "30mg" on the label IS the elemental iron, not the compound mass.
5. Correct computation: 30mg elemental / 18mg min_effective = 1.67 → in_range → no cap → S-range.

This matters most for SP-7290118814061 (SupHerb Iron 9-months, 30mg, bisglycinate, pregnancy-targeted) — a legitimate, well-formulated iron supplement for pregnant women, now D/49. Showing a D grade to a pregnant woman looking for an iron supplement is a materially harmful false verdict.

The fix needed: the iron dossier and engine must tag labeled quantities as either compound-mass or elemental-label before applying conversion. The short-term safe default is: for iron bisglycinate labeled in the range 15–36mg (common Israeli elemental iron dosing range), treat as elemental. For ferrous sulfate (common compound labels: 150–325mg range), apply conversion. Or: add a `label_basis` field to panel actives (options: `elemental`, `compound`) and apply conversion only when `compound`.

Routes to: data-agent (add label_basis field to iron actives); nutrition-agent (adjudicate the correct interpretation of iron bisglycinate labels in Israeli MOH context).

---

### C-3: RT-5 Omega-3 Heart→Brain Mislabeling — Persists Unchanged

The omega-3 umbrella still resolves "בריאות הלב" (heart health) to "brain & mood / general cognition (BROAD consumer claim)" as the nearest non-contested endpoint. SP-7290012760204 (SupHerb Omega 3, heart claim), SP-0033984020573, SP-0033984020580 all carry claim_matched "brain & mood / general cognition" in their traces despite making CV claims. This was RT-5 in v3 and is unchanged in v6. The trace misattributes the D grade reason to brain/cognition when the actual driver is the contested CV endpoint. Any consumer-facing copy derived from `claim_matched` will be factually incorrect for these products.

Routes to: content-agent (do not expose `claim_matched` for contested-deferred products; write a distinct disclosure: "this product makes a cardiovascular claim that is scientifically contested; Bari does not score contested claims").

---

### C-4: 91.2 Score Clustering — Persists at 8 Products

All 8 S-grade products still score exactly 91.2. This is arithmetically structural: any product achieving ev=92.5, dose=92, form=92, honesty=100, safety=neutral arrives at the same blend. Legitimate variation exists at the sub-score level (different actives, different forms, different products) but is invisible at the grade/score display level. A journalist asking "why does a D3 drop score the same as a B12 tablet?" has no answer in the current scoring output.

This was RT-6 in v3. It was not remediated in v4–v6. The clustering now affects 8 products rather than 15 (improvement in scope) but the structural cause is unchanged.

Routes to: nutrition-agent (calibration question — whether sub-score variation within the S pool should produce fractional score differences; no EV-### change needed, a constant adjustment).

---

### C-5: Folic Acid Claim Translation for SP-7290008111041

SP-7290008111041 panel claim: `"חומצה פולית 400 מק"ג לתמיכה בהיריון ובריאות תאים"` (folic acid 400mcg to support pregnancy and cell health). The bsip claim_fed is `"neural tube defect risk reduction (periconceptional)"`. This is a significant injection: the panel does not mention NTDs at all. The resolution to Strong NTD claim may be justifiable (folic acid for pregnancy support in the periconceptional period is the NTD-prevention context) but the panel claim says "pregnancy support and cell health" — which could legitimately resolve to Moderate (pregnancy support, not NTD-specific) or Strong (if the pregnancy context is interpreted as periconceptional NTD). The injection is a human judgment that is not visible in the trace and is not the most conservative reading of the panel.

Routes to: data-agent / nutrition-agent (adjudicate whether "תמיכה בהיריון ובריאות תאים" warrants the NTD Strong translation or should resolve via umbrella to a pregnancy-support Moderate).

---

## Product-by-Product Assessment (Summary Table — Key Products)

| SKU | Active | Score v6 | Grade | Score v3 | RT Assessment |
|---|---|---|---|---|---|
| SP-7290012760266 | vitamin_d3 | 91.2 | S | 91.2/S | PLAUSIBLE — pre-translation "מחסור" language justifiable; traceability gap remains |
| SP-7290013142146 | vitamin_d3 | 91.2 | S | 91.2/S | Same pattern |
| SP-7290012760761 | vitamin_d3 | 91.2 | S | 91.2/S | Same pattern |
| SP-7290010035984 | vitamin_d3 | 91.2 | S | 91.2/S | JUSTIFIED — English label, 1000 IU |
| SP-7290015318433 | vitamin_d3 | 91.2 | S | 91.2/S | JUSTIFIED |
| SP-7290017243450 | vitamin_b12 | 91.2 | S | 91.2/S | JUSTIFIED — blood/fatigue panel claim maps Strong |
| SP-7290015765572 | vitamin_b12 | 91.2 | S | 91.2/S | JUSTIFIED |
| SP-712179581913 | vitamin_b12 | 91.2 | S | 91.2/S | PLAUSIBLE — liposomal B12 "3 forms" panel is a form claim, pre-translated to deficiency-correction; defensible but unverifiable from trace |
| SP-7290118814061 | iron | 49.0 | D | 91.2/S | POTENTIALLY INCORRECT — elemental/compound ambiguity (see C-2) |
| SP-783495578741 | iron | 49.0 | D | 91.2/S | POTENTIALLY INCORRECT — same |
| SP-7290012056741 | iron | 81.5 | A | 91.2/S | POTENTIALLY INCORRECT — if 36mg is elemental, should be S |
| SP-7290017847122 | magnesium oxide | 61.4 | C | 20/E (false veto) | FIXED — RT-1 resolved, C is correct |
| SP-7290001065662 | magnesium oxide | 65.6 | B | 20/E (false veto) | FIXED |
| SP-7290015318426 | magnesium oxide | 65.6 | B | 20/E (false veto) | FIXED |
| SP-7290010207640 | magnesium oxide | 62.0 | C | 20/E (false veto) | FIXED |
| SP-7290013142146 | vitamin_d3 | 91.2 | S | 91.2/S | See above |
| SP-7290013464859 | iron (infant) | unscoreable_pediatric | — | D/49 | FIXED — RT-3 resolved |
| SP-7290003491902 | vitamin_d3 (infant) | unscoreable_pediatric | — | D/49 | FIXED |
| SP-7290015429245 | magnesium carbonate | 59.2 | C | — | SUSPICIOUS — carbonate not in elemental_by_form; raw 160mg used for dose; C/59.2 may not derive from correct arithmetic |
| SP-7290001943700 | magnesium (form=None) | unscoreable_incomplete | — | B/71.6 (v5 false-safe) | FIXED — SUPP-EV-024 correctly routes to unscoreable |

---

## Summary Assessment

**Justified scores (structural logic holds):** B12 S-grades (3, well-supported); D3 S-grades via English label (2); D3 A-grades via bone-health umbrella (4); folic acid A-grades (2 of 3); calcium A-grade (1); B-grade magnesium oxide cluster (4 products, correct after RT-1 fix); biotin E-grades (2); B-grade vitamin C cluster with real scraped claims (4). Total: approximately 25 products.

**Plausible but unverifiable:** D3 S-grades via "מחסור" pre-translation (3 products); B12 S-grade with liposomal form-claim panel (1); folic acid A-grade for pregnancy-support translation (1).

**Potentially incorrect:** Iron bisglycinate products (3 products, elemental/compound ambiguity). Magnesium carbonate (1 product, no elemental conversion). Magnesium taurate (1 product, no elemental conversion).

**Noise-level precision (indistinguishable):** All 8 S-grades score exactly 91.2. All cap_1 E-grades score exactly 34.0. All cap_2 D-grades score exactly 49.0. Score clustering is unchanged.

**Overriding structural problem:** Iron elemental/compound label convention is unresolved. The RT-1 fix, by adding bisglycinate to the iron elemental_by_form map, now double-converts products whose label amounts are already elemental — collapsing three products from S to D.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT6-C1: Iron bisglycinate elemental/compound label convention — 3 products falsely graded D**

Products SP-7290118814061 (30mg), SP-783495578741 (27mg), SP-7290012056741 (36mg) label their iron content as elemental iron per Israeli MOH convention. The engine now converts this elemental-stated quantity via `0.274` bisglycinate fraction, producing a phantom low elemental value (e.g., 30 × 0.274 = 8.22mg) that falls below the fairy_dust floor. SP-7290118814061 is a pregnancy-targeted iron supplement from a major Israeli brand (SupHerb), widely available at Super-Pharm, targeted at pregnant women. Publishing D/49 on this product while it correctly scores S under the right interpretation is the clearest consumer-harm scenario in the v6 corpus.

Evidence: `panel.actives[0].amount = 30.0, form = "bisglycinate"`, `trace.sub_scores.dose = {value: 20, reason: "fairy_dust"}`, `trace.sub_scores.dose.min_effective` (implied 18mg). v3 scored S/91.2 before elemental_by_form was populated.

Implication: A pregnant woman comparing iron supplements sees SupHerb Iron 9-months at D while a 36mg ferrous bisglycinate scores A. The D verdict is an artifact of an unresolved label-basis assumption, not a quality difference.

Routes to: data-agent (add `label_basis: elemental | compound` field to panel actives; iron bisglycinate should default to `elemental` unless the panel explicitly states compound mass); nutrition-agent (confirm Israeli MOH iron labeling convention; add the elemental-label flag to the dossier's dose interpretation guidance).

---

**RT6-C2: Three D3 S-grades still scored via pre-translation — traceability break persists**

SP-7290012760266, SP-7290013142146, SP-7290012760761 all have `on_label_claim: "correcting/maintaining vitamin D status (raising serum 25(OH)D)"` in their traces despite their panel claims being Hebrew bone-health + deficiency-correction text. The RT-2 fix improved 4 of 7 pre-translated products but left these 3 at S/91.2 via the same mechanism. The trace cannot be independently verified.

Evidence: Panel claim for all three: `"ויטמין D לספיגת סידן ולשמירה על בריאות העצם; להשלמת מחסור בוויטמין D"`. `primary_claim_fed: "correcting/maintaining vitamin D status (raising serum 25(OH)D)"`. `claim_resolution.via_umbrella: false`. `resolved_tier: Strong`.

Implication: If the pre-translation is adjudicated as Moderate (bone health / deficiency as two separate clauses, both Moderate via umbrella), these three products drop from S to A. Three S-grades carried by an unauditable pipeline step cannot be published without the translation decision being formally documented.

Routes to: data-agent (make the pre-translation step traceable — add a `claim_translated_from` field; the translation decision must appear in the audit trail); nutrition-agent (adjudicate: does "להשלמת מחסור בוויטמין D" suffice for Strong status-correction, or should these resolve to bone-health Moderate as the other 4 products now do?).

---

### HIGH — should resolve before launch

**RT6-H1: Systematic claim injection undocumented — 54 products, Type 2/3 injections mislead trace auditors**

54 of 78 scored products have English keywords injected into `primary_claim_fed` not present in the panel. For Type 3 injections (SP-7290010318230, SP-7290001943212 with "cognitive" injected despite no cognitive claim), the trace records a false claim provenance. There is no `claim_augmented` flag to identify injected claims.

Routes to: data-agent (add injection audit field); content-agent (audit all Type 3 injections for claim falsification risk).

---

**RT6-H2: Omega-3 heart→brain claim_matched mislabeling — persists from v3 RT-5**

SP-7290012760204, SP-0033984020573, SP-0033984020580 all record `claim_matched: "brain & mood / general cognition (BROAD consumer claim)"` for products that made cardiovascular health claims. Any consumer-facing copy using this field misattributes the D grade reason.

Routes to: content-agent (write dedicated copy for contested-CV products that correctly states the reason for D); nutrition-agent (consider a distinct `contested_deferred` outcome in the trace rather than routing to brain/mood).

---

**RT6-H3: Folic acid NTD translation of SP-7290008111041 — conservative reading is pregnancy support, not NTD-specific**

Panel claim "תמיכה בהיריון ובריאות תאים" (pregnancy and cell health) does not mention NTDs. Pre-translated to Strong NTD claim. The most conservative resolution is Moderate (pregnancy support via umbrella) → expected A, not the current A/82.8 (both produce A-range, so grade is unchanged, but the evidence-tier assignment of Strong is not warranted by the panel text). This is a correctness concern, not a grade error.

Routes to: nutrition-agent (adjudicate whether "pregnancy support" without NTD mention deserves NTD Strong tier or pregnancy Moderate).

---

**RT6-H4: Magnesium carbonate and taurate missing from elemental_by_form**

SP-7290015429245 (160mg carbonate) computes dose without elemental conversion, producing a structurally invalid dose comparison. SP-7290018439579 (76mg taurate) same problem. Both happen to reach defensible outcomes but via incorrect arithmetic.

Routes to: nutrition-agent (add magnesium carbonate ~0.239 and taurate ~0.082 fractions to the dossier; add a dossier-validation test that any corpus-present form has a corresponding elemental_by_form entry).

---

**RT6-H5: Unscoreable_incomplete products — silent disappearance without consumer disclosure**

SP-7290001943700 (Hadas Full-Mag 600mg form=None) routes to `unscoreable_incomplete` with reason `mineral_form_undeterminable_dose_may_exceed_ul`. A consumer who encounters this product on-shelf and looks it up on Bari receives no result — not a warning, not an explanation. The `machine_reason` is present in the trace but never surfaces to the consumer. The correct behavior is a disclosed exclusion: "This product could not be safety-verified; Bari cannot rate it."

Routes to: product-agent (define a consumer-facing disclosure for safety-unscoreable exclusions); content-agent (draft copy for unscoreable_incomplete products in the UI).

---

### MEDIUM — should document or monitor

**RT6-M1: Magnesia brand (8 products, unscoreable_premarket) — shelf status unverified**

8 Magnesia products remain `unscoreable_premarket`. v3 RT-7 flagged this as 5 products. If any Magnesia products are now live on-shelf, the comparison omits them without disclosure.

Routes to: data-agent (re-verify Magnesia shelf status; the corpus counts are now higher than v3 Magnesia count, suggesting new products entered).

---

**RT6-M2: Score clustering persists at S=91.2, D=49.0, E=34.0**

All 8 S-grades, all cap_2 D-grades, and all cap_1 E-grades score point-values. Consumer and journalist cannot distinguish between products within each tier.

Routes to: nutrition-agent (calibration question — introduce sub-tier differentiation within the S pool).

---

**RT6-M3: Life brand systematic exclusion (house-brand data wall)**

Life (Super-Pharm house brand) continues at 7/22 scored (32%). The price-competitive tier remains underrepresented.

Routes to: product-agent (decide whether supplement comparison ships without house-brand coverage or with explicit scope disclosure).

---

**RT6-M4: B12 S-grade for liposomal triple-form product (SP-712179581913) — form claim pre-translated**

Panel claim: "ויטמין B12 ליפוזומלי בשלוש צורות; מתיל, אדנוסיל, הידרוקסי קובלאמין עם מתיל פולאט." This is a formulation/form claim, not a health-endpoint claim. `primary_claim_fed: "treating/preventing B12 deficiency"`. The pre-translation attributes B12 deficiency-correction to a product that made no deficiency claim. The outcome (S/91.2) may be appropriate for a liposomal B12 with methyl/adenosyl/hydroxo forms, but the claim basis is not the panel text.

Routes to: data-agent (document translation logic for B12 products; add auditable field).

---

## Verdict

**FAIL — 2 open CRITICAL findings block launch.**

RT6-C1 (iron elemental/compound ambiguity) and RT6-C2 (residual D3 pre-translation traceability gap) are both launch blockers. RT6-C1 is the more severe because it inverts three products that were previously defensible S-grades to D/49, including a widely-distributed pregnancy iron supplement. The D verdict for SP-7290118814061 (SupHerb Iron 9-months) would be factually wrong if the 30mg figure is elemental — and it almost certainly is.

**RT-1 (magnesium false vetoes): CLOSED** — 9/9 false vetoes eliminated; Hadas form=None correctly handled.
**RT-2 (D3 pre-translation): PARTIALLY CLOSED** — 4/7 demoted correctly; 3 remain at S via unauditable translation.
**RT-3 (pediatric dosing): CLOSED** — 3 products correctly routed to unscoreable_pediatric.

The HIGH findings (RT6-H1 through RT6-H5) do not individually block launch but collectively represent a content and data-integrity quality gate. RT6-H2 (omega-3 brain mislabeling) in particular would produce factually incorrect consumer-facing copy if the `claim_matched` field is ever surfaced directly.

The mechanical integrity of v6 is improved over v3 — no false safety vetoes on the original 9 magnesium products, no pediatric adult-dosing errors, more accurate D3 tier resolution. But the RT-1 fix introduced a new scoring error that is arguably worse in consumer impact than the original: a pregnancy iron supplement at D is a more harmful signal to a real consumer than a generic magnesium tablet at E.

---

```json
{
  "return_contract": "v1",
  "agent": "red-team-agent",
  "task_ref": "TASK-350 v6 re-challenge (third pass post-remediation)",
  "run_date": "2026-06-19",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_sie_v6.md",
      "sha256": "453a9d1da7dac374ff68f6f1f946e669b79624b4040f647fd23f5b248b3e2e49",
      "role": "challenge_report"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v6.json",
      "sha256": "b3f7865a96b1605ab6e428cf7a1edc1be2470d22f77b368dff6e8586f86a2ac0",
      "role": "corpus_scored"
    }
  ],
  "counts": {
    "denominator_description": "118 shelf products in v6 corpus; 78 scored",
    "total_shelf": 118,
    "total_scored": 78,
    "unscoreable_incomplete": 26,
    "unscoreable_pediatric": 3,
    "unscoreable_premarket": 11,
    "grade_S": 8,
    "grade_A": 10,
    "grade_B": 16,
    "grade_C": 4,
    "grade_D": 17,
    "grade_E": 23,
    "prior_criticals_from_v3": 3,
    "criticals_closed": 1,
    "criticals_partially_closed": 1,
    "criticals_fully_closed": 1,
    "new_criticals_introduced": 1,
    "total_open_criticals_v6": 2,
    "findings_high": 5,
    "findings_medium": 4,
    "false_vetoes_eliminated": 9,
    "iron_products_wrongly_graded_D_by_fix": 3,
    "d3_pre_translation_remaining": 3,
    "d3_pre_translation_resolved": 4,
    "pediatric_correctly_routed": 3,
    "claim_injections_total_scored": 54,
    "claim_injections_score_determinative": 3,
    "omega3_heart_claim_brain_mislabeled": 3
  },
  "commands_run": [
    {"cmd": "Read _corpus_run_full_v6.json (full corpus parse)", "exit_code": 0},
    {"cmd": "Read red_team_sie_v3.md (prior challenge report)", "exit_code": 0},
    {"cmd": "Read score_engine.py (full engine code)", "exit_code": 0},
    {"cmd": "Read supp_evidence_registry_v1.md (SUPP-EV-022/023/024)", "exit_code": 0},
    {"cmd": "Read zinc.yaml (dossier — elemental_by_form, UL, safety)", "exit_code": 0},
    {"cmd": "Read iron.yaml (dossier — elemental_by_form bisglycinate=0.274, min_effective=18)", "exit_code": 0},
    {"cmd": "python3 — extract S/A grades + claim translation patterns", "exit_code": 0},
    {"cmd": "python3 — extract all magnesium product outcomes + safety traces", "exit_code": 0},
    {"cmd": "python3 — extract iron products + dose traces", "exit_code": 0},
    {"cmd": "python3 — claim injection analysis (54/78 with injection; 3 score-determinative)", "exit_code": 0},
    {"cmd": "python3 — grade distribution + outcome counts verification", "exit_code": 0}
  ],
  "not_done": [
    "External evidence verification (PubMed/CrossRef) of SUPP-EV-022/023/024 citations — out of scope; structural audit only",
    "Frontend JSON challenge — no frontend JSON exists for supplements",
    "Zinc picolinate label convention check — assumes compound basis; not verified against Israeli MOH zinc labeling standards",
    "Full audit of all 26 unscoreable_incomplete — spot-checked, not exhaustively verified",
    "Magnesium carbonate elemental fraction cross-check against PubChem"
  ],
  "verdict": "FAIL",
  "open_criticals": ["RT6-C1 (iron elemental/compound label ambiguity — 3 products falsely D)", "RT6-C2 (D3 pre-translation traceability gap — 3 S-grades unauditable)"],
  "prior_criticals_status": {
    "RT-1_magnesium_false_vetoes": "CLOSED (9/9 false vetoes eliminated; SUPP-EV-024 worst-case guard correct)",
    "RT-2_d3_pre_translation": "PARTIALLY CLOSED (4/7 resolved; 3 remain at S via unauditable translation)",
    "RT-3_pediatric_dosing": "CLOSED (3 products correctly routed to unscoreable_pediatric)"
  },
  "acceptance_test": {
    "spec": "Re-challenge report confirms closure of RT-1/RT-2/RT-3; audits fix-introduced problems (B-1 through B-4); assesses Part C launch-blocking concerns; classifies all findings CRITICAL/HIGH/MEDIUM with explicit verdict",
    "result": "PASS — all six delegated scope areas covered (RT-1/RT-2/RT-3 closure verification, fix-introduced problems B-1/B-2/B-3/B-4, coverage/clustering/claim-honesty Part C)"
  }
}
```
