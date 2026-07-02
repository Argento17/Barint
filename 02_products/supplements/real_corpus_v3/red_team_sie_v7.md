# Red-Team Challenge Report — Supplements SIE v7 (real_corpus_v3)
Date: 2026-06-19
Scope: 78 scored / 118 shelf, SIE proto_v0 / algorithm_v0.2.0
Corpus file: _corpus_run_full_v7.json (TASK-350 fourth pass)
Prior reports: red_team_sie_v3.md (3 CRITICAL), red_team_sie_v6.md (2 CRITICAL)
Challenger: red-team-agent

---

## Opening Finding

**RT6-C1 is structurally closed. RT6-C2 is structurally closed. No new CRITICAL introduced by the v7 fixes.**

The v7 fixes are mechanically correct: `label_basis=elemental` gates conversion correctly for iron; the `claim_translation_provenance` block makes the D3 pre-translation step inspectable. Both prior CRITICALs are addressed at the root cause, not papered over.

However, two new findings are elevated to HIGH severity, and one latent gap in the iron overdose-veto machinery is elevated to HIGH because it creates a future-corpus safety blind spot that is not testable against the current corpus:

1. **Zinc chelate label-basis unresolved (HIGH):** The iron fix confirmed that Israeli MOH supplement regulations require ELEMENTAL iron declaration. The zinc dossier does not state a `label_basis`, defaulting to compound conversion. The Israeli label pattern for zinc picolinate (`אבץ (zinc picolinate) 22 מ"ג`) is identical in structure to the iron pattern that was misidentified as compound. If zinc products state elemental zinc (industry-standard for chelated minerals), two B-grade products would correctly score S/91.2 — a three-grade error in the same direction as the RT6-C1 iron error.

2. **Iron overdose veto blind spot with form=None + label_basis=elemental (HIGH, latent):** When an iron product has `form=None` and `label_basis=elemental`, the worst-case guard computes `quantity * max_compound_fraction` — which REDUCES an already-elemental value. A name-derived product stating 65mg elemental iron with no form token would compute worst-case = 65 * 0.368 = 23.9mg (phantom elemental) < 45mg UL, returning safety-neutral. The correct comparison is 65mg elemental > 45mg UL → VETO. No such product exists in v7 corpus. This is a latent architecture gap, not a current consumer harm, but it is unambiguously wrong and the current corpus cannot test it.

---

## Part A — RT6-C1 and RT6-C2 Closure Verification

### RT6-C1: Iron elemental/compound label convention — PASS (CLOSED)

**Evidence checked:**

- `iron.yaml` `active.label_basis: "elemental"` and `effective_dose.label_basis: "elemental"` — confirmed present (lines 33 and 86 of the dossier).
- `dossier_loader.py` exposes `label_basis` in the normalized dict. `score_engine._effective_label_quantity()` gates on `label_basis != "elemental"`: when `elemental`, conversion is skipped and a `elemental_basis_no_conversion` note is logged (code lines 321, 328–335).
- **SP-7290118814061** (SupHerb Iron 9-months, 30mg bisglycinate): `engine_output.score = 91.2`, `grade = S`, `sub_scores.dose = {value: 92, reason: "in_range"}`, `sub_scores.safety = {value: "neutral", reason: "within_ul"}`. Restored from D/49 as v6 reported. The 30mg is treated directly as elemental iron; no conversion fires.
- **SP-783495578741** (liposomal bisglycinate, 27mg): `score = 91.2`, `grade = S`, `dose = in_range`, `safety = within_ul`. Restored from D/49.
- **SP-7290012056741** (Tink Iron 36mg bisglycinate): `score = 91.2`, `grade = S`, `dose = in_range`. Restored from A/81.5. 36mg elemental > 18mg min_effective → in_range → dose=92 → S. Correct.

**Overdose veto test (genuinely vetos at >45mg elemental, form known):**

No product in the v7 corpus exceeds 45mg iron. However, the code path for form-known, label_basis=elemental products is: `should_convert=False` → qty stays at label value → `score_safety` compares qty directly to UL 45mg → if qty > 45 → VETO. This path is correct. For a hypothetical 50mg bisglycinate product (form="bisglycinate", label_basis=elemental): form is known → worst-case guard does NOT fire → qty=50 → 50 > 45 → VETO. Correct.

**Verdict on RT6-C1: CLOSED.** Three iron products restored to correct grades. Veto mechanism intact for form-known overdoses. One latent gap (form=None + label_basis=elemental) is separately classified as HIGH below (RT7-H1).

---

### RT6-C2: D3 claim traceability — PASS (CLOSED)

**Evidence checked:**

The three pre-translated D3 S-grades (SP-7290012760266, SP-7290013142146, SP-7290012760761) all have:

- `trace.on_label_claim` = verbatim Hebrew panel text: `"ויטמין D לספיגת סידן ולשמירה על בריאות העצם; להשלמת מחסור בוויטמין D"`. This is the raw auditable label.
- `trace.on_label_claim_fed` = `"correcting/maintaining vitamin D status (raising serum 25(OH)D)"`. This is what the engine scored.
- `bsip0s_label.claim_translation_provenance` = dict containing `claim_source: "studied_endpoint_translation"`, `triggered_rule: "_STUDIED_HINT['vitamin_d3']"`, `triggered_token: "מחסור"`, `translated_studied_claim`, and `supp_ev: "SUPP-EV-026"`.

The translation step is now inspectable. An independent reviewer can: (1) read the Hebrew panel text, (2) find the trigger token "מחסור" (deficiency), (3) see the translation rule that fired, (4) verify the resulting studied endpoint.

**Grade defensibility of the three pre-translated S-grades:**

These three products all state: bone health + calcium absorption + deficiency correction ("להשלמת מחסור בוויטמין D"). The "מחסור" (deficiency) clause is genuine deficiency-correction language. The SUPP-EV-026 entry documents the adjudication: Nutrition D6 co-sign holds these at Strong status-correction. An independent Nutrition reviewer can challenge this adjudication but can now fully reconstruct the decision from the trace. The traceability gap is closed; the adjudication question remains open as a documented, acknowledged judgment call.

**Two English-label D3 S-grades (SP-7290010035984, SP-7290015318433):**

`on_label_claim` = `"Vitamin D3 1000 IU per drop"`. No translation fired. The engine matched to status-correction directly (1000 IU D3 as a per-drop repletion dose maps to deficiency-correction). `claim_translation_provenance` is absent. These are the cleanest S-grades in the corpus.

**Verdict on RT6-C2: CLOSED.** The translation audit trail is machine-readable in both `bsip0s_label` and `trace`. A reviewer can reconstruct the full decision chain. Grade defensibility of the "מחסור" translation is a judgment-call, documented and owned by Nutrition D6.

---

## Part B — V7 Fix Weak Spots: Where a New CRITICAL Could Hide

### B-1: Magnesium and Zinc label_basis — Is the Compound Assumption Correct?

**The iron fix confirmed a fundamental principle:** Israeli MOH supplement regulations require elemental mineral declaration for iron. The v7 dossier cites: "Regulations for Dietary Supplement Products 2003, amendment 2009." The question is whether this principle extends to zinc.

**Zinc label evidence in this corpus:**

- SP-0033984037250 (Solgar Zinc Picolinate 22mg): panel label reads `"אבץ (zinc picolinate) 22 מ"ג"`. The ingredient name is `"אבץ (zinc picolinate)"` — where `אבץ` means zinc (the element). The numeric amount 22mg modifies the elemental name "zinc," not the compound name "zinc picolinate."
- SP-7290006437563 (Altman Zinc Picolinate 25mg): label reads `"zinc (zinc picolinate) 25mg"`. Same pattern.

This is structurally identical to the iron bisglycinate label pattern that triggered RT6-C1: `"ברזל (iron bisglycinate) 30 מ"ג"` stated elemental iron, not compound mass.

**Zinc dossier `dose_axis` states:** "ELEMENTAL zinc — NOT compound mass (§2.2 trap). Convert label compound mass x elemental_mg_fraction." This instruction presupposes that labels state COMPOUND mass. But if Israeli zinc labels (like iron) state ELEMENTAL zinc — which the DSLD market range [8–50 mg elemental] and standard chelated-mineral convention would support — then the conversion is wrong.

**Scoring impact if elemental assumption is correct:**

| SKU | Amount | Current (compound assumed) | If elemental |
|---|---|---|---|
| SP-0033984037250 | 22mg picolinate | 22×0.211=4.64mg → sub_therapeutic → B/68.4 | 22mg elemental → in_range → S/91.2 |
| SP-7290006437563 | 25mg picolinate | 25×0.211=5.28mg → sub_therapeutic → B/69.7 | 25mg elemental → in_range → S/91.2 |

A three-grade error (B→S, ~22 points) for two products, in the same direction as RT6-C1, with the same structural cause.

**Mitigation:** Unlike the iron case (where RT6-C1 collapsed S→D, a direct consumer harm), both affected zinc products currently score B — a defensible mid-tier grade. Under the elemental interpretation they would score S, so the current error is a potential under-rating rather than a damaging false verdict. The consumer harm is lower: a B-grade for a well-formulated chelated zinc supplement is not a false safety warning.

**Classification: HIGH.** This is the same assumption-vs-reality gap that caused RT6-C1. It has not been adjudicated for zinc. It must be resolved before launch, but the current error direction (B vs potential S) is less harmful than RT6-C1 was (D vs correct S). Routes to: nutrition-agent (adjudicate whether Israeli MOH zinc regulations match the iron elemental-declaration requirement; set `label_basis` in zinc.yaml accordingly).

---

### B-2: Magnesium Carbonate — Score Arithmetic Incorrect (carries forward from RT6-H4)

**Finding:**

SP-7290015429245 (Amorphicure magnesium carbonate, 160mg) scores C/59.2. The magnesium dossier does NOT contain carbonate in `compound_forms_identity`, and `magnesium.yaml` confirms this — the word "carbonate" does not appear in the dossier. `dossier_loader` indexes only forms present in `compound_forms_identity`; carbonate is absent.

**Consequence:** No elemental conversion fires for `form="carbonate"`. The engine uses raw 160mg compound mass and compares it to a dose axis defined in ELEMENTAL mg (min_effective = 300mg).

- Raw 160mg vs fairy_floor (0.5 × 300 = 150mg): 160 > 150 → not fairy_dust.
- Raw 160mg vs min_effective 300mg: 160 < 300 → sub_therapeutic.
- `frac = (160 - 150) / (300 - 150) = 0.0667`.
- `sub_t = 50 + 0.0667 × 34 = 52.3`. This is the exact trace value.

**Correct computation with conversion:**

- Magnesium carbonate elemental fraction ≈ 0.239 (MgCO₃ MW 84.3, Mg 24.3 → fraction 0.288; mixed forms approx. 0.239 per RT-9 estimate).
- 160 × 0.239 = 38.2mg elemental < fairy_floor (150mg) → FAIRY_DUST → cap_2 → D/49.

The product should score D/49, not C/59.2. It is overstated by one full grade. Safety is accidentally correct (160mg raw < 350mg elemental UL, so no veto fires regardless of conversion).

**RT6-H4 flagged this in v6 and it is unchanged in v7.** This is a documented persistent error. Classification: HIGH (one grade error). Routes to: nutrition-agent (add magnesium carbonate to `compound_forms_identity` in magnesium.yaml, per the dossier's existing malate/taurate precedent; SUPP-EV-022 already covers the alias mechanism).

---

### B-3: Name-Derived Minerals — label_basis Applies Correctly for Iron, Gap for Others

For name-derived iron products (form=None, label parsed from product name), the `label_basis=elemental` declaration still applies at the dossier level: no conversion fires regardless of form token. This is correct for iron (all Israeli iron labels are elemental). The two name-derived iron products (SP-7290016417197, SP-7290015765985) both score E/34 for lack of claim — form basis is irrelevant because the dose sub-score is `N/A` (Insufficient evidence short-circuit).

For name-derived magnesium and zinc products where amount is present, the compound assumption is applied (label_basis=None → convert if form known). This is consistent with the confirmed compound convention for magnesium. For zinc, the same uncertainty from B-1 applies.

No name-derived mineral scoring error is confirmed for the current corpus. The B-1 zinc uncertainty is the only unresolved assumption gap.

---

### B-4: Iron Overdose Veto — Latent Gap with form=None + label_basis=elemental

**Architecture gap (no current consumer harm, future-corpus risk):**

When `active.form = None` and the dossier has `elemental_by_form` entries, `score_safety()` triggers the worst-case guard: `worst_case = amount × max(elemental_by_form.values())`. For iron, `max_fraction = 0.368` (ferrous sulfate, anhydrous).

When `label_basis = "elemental"`, the `amount` value is already elemental iron. Multiplying by 0.368 REDUCES it: a name-derived product labeled 65mg elemental iron (form=None) computes `worst_case = 65 × 0.368 = 23.9mg < 45mg UL` → safety neutral. The correct comparison is `65mg elemental > 45mg UL → VETO`.

The current corpus has no form=None iron product above 45mg (all name-derived iron products are 15mg and 30mg). The gap is latent. However, the scoring engine does not protect against it structurally, and any future high-dose iron product acquired without a form token would be false-safe on safety.

**Classification: HIGH (latent, zero current impact).** Routes to: data-agent / nutrition-agent (in `score_safety()`, when `label_basis = "elemental"` AND `form is None`, bypass the worst-case guard and compare `quantity` directly to the UL as elemental — the label IS the elemental content; the worst-case guard is a compound-mass guard and should not fire for elemental labels).

---

## Part C — Residual Launch Concerns

### C-1: S-Grade Clustering at 91.2 — Structural, Unchanged

All 11 S-grade products score exactly 91.2. The distribution is: 5 D3 (3 pre-translated, 2 English-label), 3 iron bisglycinate, 3 B12. These span three actives, multiple brands, and meaningfully different products, yet they are presented as identical.

A journalist or regulator asking "why does a pregnancy iron supplement score the same as an English-label D3 drop?" has no answer from the score output. The sub-score level shows the arithmetic uniformity: evidence=92.5, dose=92, form=92, honesty=100, safety_blend=70 → blend = 91.15 → 91.2. Any product achieving this combination scores identically.

The v6 finding (RT6-M2) reduced the cluster from 8 to a new count of 11 (since 3 iron products were restored). The clustering is now larger in absolute terms than in v6.

**Classification: MEDIUM.** Routes to: nutrition-agent (calibration question — introduce sub-tier differentiation within the S pool, e.g., a tiebreaker sub-score or a fractional precision boost for dose proximity within in_range).

### C-2: Omega-3 Heart-Claim Mislabeling — RT-5/RT6-H2, Unchanged

SP-7290012760204, SP-0033984020573, SP-0033984020580 all make cardiovascular claims in Hebrew ("לתמיכה בבריאות הלב וכלי הדם"). They score D/49 via the contested-CV deferred path. The `claim_matched` field in their traces reads `"brain & mood / general cognition (BROAD consumer claim)"` — because the CV endpoint routes to the nearest non-contested umbrella entry.

SP-7290013464897 (omega-3 DHA + D3, pregnancy) also shows `claim_matched: "brain & mood / general cognition (BROAD consumer claim)"` for a DHA-pregnancy claim. This is a different kind of mislabeling: DHA for brain development in-utero is a legitimate and cited endpoint; the mislabeling is attributing it to the broad consumer cognition bucket rather than the developmental DHA endpoint.

Any consumer-facing copy generated from `claim_matched` will attribute D grades to the wrong reason for these four products. The correct explanation for the CV products is: "This product makes a cardiovascular claim that is scientifically contested (REDUCE-IT vs STRENGTH); Bari does not score contested claims." The current trace claim_matched says nothing of the sort.

**Classification: MEDIUM (consumer-facing copy hazard; not a grade error).** Routes to: content-agent (do not surface `claim_matched` verbatim for contested-CV products); nutrition-agent (consider a `contested_deferred` outcome flag in the trace that routes copy to a dedicated disclosure string).

### C-3: Coverage Bias — S-Pool Dominated by Pre-Translation Judgment Calls

11 S-grades in v7. Five are D3 — of which three remain via the `מחסור` pre-translation adjudication. Three are iron bisglycinate, now correctly restored. Three are B12.

Of the 11 S-grades, 3 (27%) rest on a Nutrition D6 adjudication that the "מחסור" clause in a bone-health + deficiency-correction D3 label legitimately maps to Strong status-correction. This adjudication is now traceable (RT6-C2 closed) but remains an expert judgment, not a self-evident derivation from the label text. If a product manager, regulatory reviewer, or journalist independently adjudicates "מחסור" language as Moderate (bone health + general deficiency awareness, not deficiency-correction), those three S-grades become A/85.0.

**Classification: MEDIUM.** The adjudication is documented, traceable, and owned by Nutrition D6. It is not undefendable — "להשלמת מחסור בוויטמין D" (to supplement/correct a deficiency in Vitamin D) is reasonable deficiency-correction language. But it requires expert agreement at launch, not just traceability.

### C-4: Life Brand Systematic Exclusion — Unchanged

Life (Super-Pharm house brand): 7 of 22 products scored (32%). 15 remain unscoreable_incomplete due to dose unavailability. The scored comparison skews toward Altman, Solgar, SupHerb, and Tink. The price-competitive tier is largely invisible.

**Classification: MEDIUM.** Routes to: product-agent (decide whether the comparison launches without disclosing the Life coverage gap; disclosure should appear in the category caveat).

---

## Product-by-Product Assessment (Key Products)

| SKU | Active | Score v7 | Grade | v6 Score | v3 Score | RT Assessment |
|---|---|---|---|---|---|---|
| SP-7290118814061 | iron bisglycinate | 91.2 | S | 49.0/D | 91.2/S | CLOSED RT6-C1 — label_basis=elemental fixes double-conversion. JUSTIFIED. |
| SP-783495578741 | iron bisglycinate | 91.2 | S | 49.0/D | 91.2/S | CLOSED RT6-C1. JUSTIFIED. |
| SP-7290012056741 | iron bisglycinate | 91.2 | S | 81.5/A | 91.2/S | CLOSED RT6-C1 — 36mg elemental in_range. JUSTIFIED. |
| SP-7290012760266 | vitamin_d3 | 91.2 | S | 91.2/S | 91.2/S | CLOSED RT6-C2 — מחסור translation now traceable via SUPP-EV-026. PLAUSIBLE (adjudication documented). |
| SP-7290013142146 | vitamin_d3 | 91.2 | S | 91.2/S | 91.2/S | Same pattern. PLAUSIBLE. |
| SP-7290012760761 | vitamin_d3 | 91.2 | S | 91.2/S | 91.2/S | Same pattern. PLAUSIBLE. |
| SP-7290010035984 | vitamin_d3 | 91.2 | S | 91.2/S | 91.2/S | English label, 1000 IU. JUSTIFIED. |
| SP-7290015318433 | vitamin_d3 | 91.2 | S | 91.2/S | 91.2/S | English label, 1000 IU. JUSTIFIED. |
| SP-7290017243450 | vitamin_b12 | 91.2 | S | 91.2/S | 91.2/S | JUSTIFIED — blood/fatigue claim maps Strong. |
| SP-7290015765572 | vitamin_b12 | 91.2 | S | 91.2/S | 91.2/S | JUSTIFIED. |
| SP-712179581913 | vitamin_b12 | 91.2 | S | 91.2/S | 91.2/S | PLAUSIBLE — liposomal B12 three-form panel pre-translated; traceable via SUPP-EV-026. |
| SP-0033984037250 | zinc picolinate | 68.4 | B | 68.4/B | — | POTENTIALLY INCORRECT — compound assumption not adjudicated for zinc (see B-1). If elemental: S/91.2. |
| SP-7290006437563 | zinc picolinate | 69.7 | B | 69.7/B | — | POTENTIALLY INCORRECT — same. |
| SP-7290015429245 | magnesium carbonate | 59.2 | C | 59.2/C | — | INCORRECT — carbonate not in dossier; raw 160mg used; correct grade is D/49 (38mg elemental < fairy_floor). |
| SP-7290017847122 | magnesium oxide | 61.4 | C | 61.4/C | 20.0/E | FIXED (v6) — RT-1 resolved. |
| SP-7290001065662 | magnesium oxide | 65.6 | B | 65.6/B | 20.0/E | FIXED (v6) — RT-1 resolved. |
| SP-7290013464859 | iron (infant) | unscoreable_pediatric | — | unscoreable_ped | D/49 | FIXED (v5) — RT-3 resolved. |
| SP-7290001943700 | magnesium form=None | unscoreable_incomplete | — | unscoreable | B/71.6 (v5 false-safe) | FIXED (v6) — SUPP-EV-024 worst-case guard. |

---

## Summary Assessment

**Justified scores (structural logic holds):** Iron S-grades (3, restored and confirmed elemental); D3 S-grades via English label (2); D3 A-grades via bone-health umbrella (4); B12 S-grades (3); folic acid A-grades (3); calcium A-grade (1); magnesium oxide B-grades (4, RT-1 fix verified); biotin E-grades (2, genuine Insufficient). Total: approximately 25 products.

**Plausible but unverifiable:** D3 S-grades via "מחסור" pre-translation (3) — now traceable, adjudication documented; B12 liposomal S-grade via form-claim pre-translation (1) — traceable via SUPP-EV-026.

**Potentially incorrect:** Zinc picolinate B-grades (2) — compound-basis assumption unverified; magnesium carbonate C-grade (1, should be D/49).

**Noise-level precision (indistinguishable):** All 11 S-grades score 91.2. All cap_2 D-grades score 49.0. All cap_1 E-grades score 34.0.

**Overriding structural problem:** None as of v7. The RT6-C1 and RT6-C2 structural defects are closed. The residual problems are calibration gaps and one dossier omission.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**None.** No CRITICAL findings in v7.

---

### HIGH — should resolve before launch

**RT7-H1: Iron worst-case guard fires incorrectly for label_basis=elemental + form=None (latent veto gap)**

When `active.form = None` and `dossier.label_basis = "elemental"`, `score_safety()` applies the mineral worst-case guard: `worst_case = amount × max(elemental_by_form.values())`. For iron, max_fraction = 0.368. This REDUCES an already-elemental label value: a 65mg elemental iron product (form=None) computes worst_case = 65 × 0.368 = 23.9mg < 45mg UL → returns safety neutral.

The correct behavior: when `label_basis = "elemental"`, the `amount` is already elemental iron. The worst-case guard must be bypassed, and `amount` compared directly to the UL.

No current corpus product triggers this. The two name-derived iron products with form=None (SP-7290016417197 at 15mg, SP-7290015765985 at 30mg) are both below 45mg elemental, so safety-neutral is accidentally correct. But the mechanism is wrong.

Evidence: `score_engine.py` `score_safety()` — the worst-case guard block does not check `dossier.get("label_basis")` before computing `worst_case = amount_mg * max_frac`. When `label_basis = "elemental"`, `_effective_label_quantity` returns `qty` unchanged (correct for dose), but `score_safety` independently applies the worst-case multiplication regardless of label_basis.

Implication: Any future name-derived iron product above 45mg elemental but below 45/0.368 = 122mg in label value would be false-safe on safety.

Routes to: data-agent (in `score_safety()`, add `label_basis = dossier.get("label_basis")` and bypass the worst-case guard when `label_basis = "elemental"`, comparing `amount` directly to the UL).

---

**RT7-H2: Zinc picolinate label_basis unresolved — two B-grade products potentially mis-scored**

The iron fix established that Israeli MOH supplement regulations require elemental mineral declaration for iron. The same logic applies to chelated zinc: `אבץ (zinc picolinate) 22 מ"ג` states elemental zinc (zinc is the active declared; picolinate is the form identified in parentheses). This is the standard industry convention for chelated minerals: the numeric amount refers to the active mineral, not the whole chelate compound.

The zinc dossier lacks a `label_basis` field (defaults to None → treated as compound). Engine converts 22mg picolinate × 0.211 = 4.64mg elemental → sub_therapeutic → B/68.4. If elemental: 22mg > 8mg min_effective → in_range → S/91.2.

Evidence: Cache file for SP-0033984037250 (barcode 0033984037250): `"ingredient": "אבץ (zinc picolinate)", "amount": 22, "form": "picolinate"`. Cache file for SP-7290006437563: `"ingredient": "zinc (zinc picolinate)", "amount": 25, "form": "picolinate"`. Both follow the `[mineral] ([compound form]) [amount]` pattern identical to iron bisglycinate.

Zinc dossier `dose_axis` states "ELEMENTAL zinc — NOT compound mass" — but the engine behavior defaults to compound conversion because `label_basis` is unset.

If elemental: SP-0033984037250 would be S/91.2 (+22.8 points from B/68.4); SP-7290006437563 would be S/91.2 (+21.5 points from B/69.7).

Implication: Two products are potentially under-rated by three grades. The current error direction (B rather than potential S) is less harmful to consumers than RT6-C1 (which produced a false D), but the mechanism is identical and the resolution requires the same adjudication.

Routes to: nutrition-agent (confirm whether Israeli MOH zinc labeling requirements match iron — check if zinc products must declare elemental zinc; adjudicate `label_basis` for zinc and set in zinc.yaml; SUPP-EV-025 provides the iron-precedent logic that can be extended).

---

**RT7-H3: Magnesium carbonate not in dossier — C/59.2 score arithmetic incorrect (should be D/49)**

SP-7290015429245 (Amorphicure 160mg magnesium carbonate) scores C/59.2. Magnesium carbonate is absent from `magnesium.yaml compound_forms_identity`, so no elemental conversion fires. The engine compares raw 160mg compound mass to a dose axis defined in elemental mg (min_effective = 300mg). Result: sub_therapeutic = 52.3, blend → C/59.2.

Correct computation: 160mg carbonate × ~0.239 elemental fraction (MgCO₃ MW 84.3, Mg 24.3 → actual fraction 0.288; RT-9 estimate 0.239) = 38–46mg elemental < fairy_floor (150mg) → fairy_dust → D/49.

The product is overstated by one grade (C vs D). Safety is accidentally correct (160mg raw < 350mg UL regardless of conversion).

This was RT6-H4 in v6. It is unchanged in v7. The malate and taurate forms were added to the dossier in v6 (evidenced in magnesium.yaml); carbonate was not.

Evidence: `magnesium.yaml` does not contain the string "carbonate" (verified). `dossier_loader.py` builds `elemental_by_form` only from `compound_forms_identity` entries. `score_engine._effective_label_quantity()` calls `elem.get(_norm("carbonate"))` → None → no conversion → qty = 160mg raw.

Routes to: nutrition-agent (add magnesium carbonate to `compound_forms_identity` in magnesium.yaml; elemental fraction ~0.288 per MgCO₃ molecular weights, NEEDS-ENV-VERIFY; includes short_form_alias ["carbonate", "magnesium carbonate"] per SUPP-EV-022 pattern; update change_log with SUPP-EV-022 reference).

---

### MEDIUM — should document or monitor

**RT7-M1: S-grade clustering at 91.2 — now 11 products (worse than v6's 8)**

All 11 S-grade products score exactly 91.2. The restoration of 3 iron bisglycinate products increased the cluster from 8 (v6) to 11. A consumer or journalist comparing a pregnancy iron supplement to a vitamin D3 drop sees no numeric differentiation. The underlying arithmetic is correct but the presentation conflates products that are meaningfully different.

Routes to: nutrition-agent (calibration question — sub-tier differentiation within the S pool via either dose-proximity bonus within in_range, or a fractional evidence-tier precision beyond the mid-band point).

---

**RT7-M2: Omega-3 heart-claim mislabeling persists (RT-5 / RT6-H2)**

Four scored omega-3 products make cardiovascular or DHA-developmental claims. Their traces record `claim_matched: "brain & mood / general cognition (BROAD consumer claim)"` — the nearest non-contested umbrella routing. Consumer-facing copy derived from this field would attribute D grades to brain/cognition evidence, not cardiovascular contestation. Unchanged from v3 and v6.

Routes to: content-agent; nutrition-agent (see RT6-H2 routing).

---

**RT7-M3: Three D3 S-grades carry expert adjudication risk at launch**

The "מחסור" pre-translation is now traceable (RT6-C2 closed). But the grade of three products depends on a Nutrition D6 judgment that "להשלמת מחסור" maps to Strong status-correction rather than bone-health Moderate. If this adjudication is challenged at launch — by a journalist, a competitor, or a regulatory body — the response requires the Nutrition D6 documented justification. The justification exists and is auditable. This is a documentation risk, not a scoring error.

Routes to: product-agent (ensure the D6 adjudication document is accessible if challenged; consider adding a brief consumer-facing disclosure that the deficiency-correction claim is the basis for the S-grade on these three products).

---

**RT7-M4: Magnesia brand absence — unverified shelf status**

8 Magnesia products remain `unscoreable_premarket`. If any are currently sold on-shelf at Super-Pharm or online, their absence from the comparison is undisclosed. Unchanged from v6 (RT6-M1 elevated Magnesia count from 5 in v3 to 8). Routes to: data-agent (re-verify Magnesia shelf status before launch).

---

## Verdict

**CONDITIONAL PASS — zero open CRITICAL findings; three HIGH findings require resolution or explicit acknowledgment before go-live.**

RT6-C1 (iron elemental/compound label_basis): **CLOSED.** Three iron products correctly at S/91.2. Veto at >45mg intact for form-known products.

RT6-C2 (D3 claim traceability): **CLOSED.** `on_label_claim_raw_he` + `claim_translation_provenance` make the translation decision machine-auditable in both `bsip0s_label` and `trace`.

RT3 (pediatric dosing): **CLOSED** (v6); confirmed unchanged in v7.

**Open HIGH findings:**

- **RT7-H1** (iron worst-case guard + label_basis=elemental + form=None): Latent safety veto gap. No current consumer harm; any name-derived iron product above 45mg would receive a false-safe verdict. Requires a one-line engine fix in `score_safety()`. Must be fixed before corpus expansion includes higher-dose iron products.
- **RT7-H2** (zinc picolinate label_basis): Two B-grade products potentially mis-scored at B (should be S if elemental convention confirmed). Requires Nutrition D6 adjudication and `label_basis` setting in zinc.yaml. Grade impact: B→S for 2 products.
- **RT7-H3** (magnesium carbonate): One C-grade product scores C when correct arithmetic yields D/49. Requires adding carbonate to `magnesium.yaml compound_forms_identity`. Grade impact: C→D for 1 product.

**One-line go/no-go:** V7 is launch-defensible at zero open CRITICAL, provided the three HIGH findings are resolved (RT7-H1: safety architecture fix before corpus expansion; RT7-H2: zinc adjudication; RT7-H3: dossier addition) or are explicitly acknowledged by Product as acceptable pre-launch exceptions with documented rationale. RT7-H1 is the highest-urgency because it touches the safety veto — the most consequential scoring dimension.

---

```json
{
  "return_contract": "v1",
  "agent": "red-team-agent",
  "task_ref": "TASK-350 v7 re-challenge (fourth pass, decider pass)",
  "run_date": "2026-06-19",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_sie_v7.md",
      "sha256": "pending-write",
      "role": "challenge_report"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v7.json",
      "sha256": "read-only-source",
      "role": "corpus_scored"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\iron.yaml",
      "sha256": "read-only-source",
      "role": "iron_dossier_label_basis_elemental"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\magnesium.yaml",
      "sha256": "read-only-source",
      "role": "magnesium_dossier_no_carbonate"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\zinc.yaml",
      "sha256": "read-only-source",
      "role": "zinc_dossier_no_label_basis"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\src\\score_engine.py",
      "sha256": "read-only-source",
      "role": "score_engine_v7"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_registry\\supp_evidence_registry_v1.md",
      "sha256": "read-only-source",
      "role": "evidence_registry_SUPP-EV-025-026"
    }
  ],
  "counts": {
    "denominator_description": "118 shelf products; 78 scored in v7",
    "total_shelf": 118,
    "total_scored": 78,
    "unscoreable_incomplete": 26,
    "unscoreable_pediatric": 3,
    "unscoreable_premarket": 11,
    "grade_S": 11,
    "grade_A": 9,
    "grade_B": 16,
    "grade_C": 4,
    "grade_D": 15,
    "grade_E": 23,
    "rt6_c1_status": "CLOSED",
    "rt6_c2_status": "CLOSED",
    "rt3_status": "CLOSED (v6)",
    "iron_products_restored_to_S": 3,
    "d3_s_grades_total": 5,
    "d3_s_grades_via_english_label_justified": 2,
    "d3_s_grades_via_machsur_translation_plausible": 3,
    "open_criticals_v7": 0,
    "open_highs_v7": 3,
    "open_mediums_v7": 4,
    "zinc_picolinate_products_potentially_mis_scored": 2,
    "magnesium_carbonate_products_grade_error": 1,
    "iron_latent_veto_gap_products_affected_current_corpus": 0,
    "s_grade_cluster_size": 11,
    "claim_translations_fired_supp_ev_026": 14,
    "omega3_heart_claim_mislabeled_in_trace": 4
  },
  "commands_run": [
    {"cmd": "Read red_team_sie_v6.md (prior CRITICAL findings)", "exit_code": 0},
    {"cmd": "Read red_team_sie_v3.md (original CRITICAL findings)", "exit_code": 0},
    {"cmd": "Read _corpus_run_full_v7.json (full parse, all 78 scored products)", "exit_code": 0},
    {"cmd": "Read iron.yaml (label_basis=elemental, compound_forms_identity, UL)", "exit_code": 0},
    {"cmd": "Read magnesium.yaml (compound_forms_identity, no carbonate)", "exit_code": 0},
    {"cmd": "Read zinc.yaml (no label_basis, compound_forms_identity)", "exit_code": 0},
    {"cmd": "Read score_engine.py (label_basis gate in _effective_label_quantity, worst-case guard in score_safety)", "exit_code": 0},
    {"cmd": "Read dossier_loader.py (elemental_by_form construction, label_basis exposure)", "exit_code": 0},
    {"cmd": "Grep SUPP-EV-025 / SUPP-EV-026 in evidence registry", "exit_code": 0},
    {"cmd": "python3: extract iron product traces (score, dose_trace, safety_trace) for barcodes 7290118814061/783495578741/7290012056741", "exit_code": 0},
    {"cmd": "python3: extract D3 S-grade claim traceability (on_label_claim, on_label_claim_fed, claim_translation_provenance)", "exit_code": 0},
    {"cmd": "python3: dossier_loader.load_dossier('magnesium') -> elemental_by_form keys (carbonate not indexed)", "exit_code": 0},
    {"cmd": "python3: dossier_loader.load_dossier('iron') -> label_basis=elemental confirmed", "exit_code": 0},
    {"cmd": "python3: dossier_loader.load_dossier('zinc') -> label_basis=None confirmed", "exit_code": 0},
    {"cmd": "python3: carbonate dose arithmetic verification (160mg raw, fairy_floor 150, sub_t=52.3 vs correct fairy_dust)", "exit_code": 0},
    {"cmd": "python3: zinc picolinate label basis impact analysis (compound: B/68.4 vs elemental: S/91.2)", "exit_code": 0},
    {"cmd": "python3: iron worst-case guard analysis for label_basis=elemental + form=None (latent veto gap)", "exit_code": 0},
    {"cmd": "python3: all scored iron products, amounts, form, safety traces", "exit_code": 0},
    {"cmd": "python3: omega-3 claim_matched field check (heart->brain mislabeling)", "exit_code": 0},
    {"cmd": "python3: grade distribution trace vs header cross-check (PASS: both S=11 A=9 B=16 C=4 D=15 E=23)", "exit_code": 0},
    {"cmd": "Read cache/0033984037250.json (Solgar Zinc Picolinate label format)", "exit_code": 0},
    {"cmd": "Read cache/7290006437563.json (Altman Zinc Picolinate label format)", "exit_code": 0}
  ],
  "not_done": [
    "External PubMed verification of SUPP-EV-025/026 citations (structural audit only, not evidence re-review)",
    "Full audit of all 26 unscoreable_incomplete products (spot-checked; no anomalies in sample)",
    "Frontend JSON challenge (no supplements frontend JSON exists)",
    "Magnesia brand shelf-status verification (data-agent scope)",
    "Israeli MOH Zinc labeling regulation primary source check (nutrition-agent scope for RT7-H2 adjudication)"
  ],
  "verdict": "CONDITIONAL PASS",
  "open_criticals": [],
  "open_highs": [
    "RT7-H1 (iron worst-case guard + label_basis=elemental + form=None — latent safety veto gap; routes to data-agent)",
    "RT7-H2 (zinc picolinate label_basis unresolved — B/68.4 and B/69.7 potentially should be S/91.2; routes to nutrition-agent)",
    "RT7-H3 (magnesium carbonate not in dossier — C/59.2 should be D/49; routes to nutrition-agent)"
  ],
  "prior_criticals_status": {
    "RT-1_magnesium_false_vetoes": "CLOSED (v6, confirmed unchanged v7 — 9/9 false vetoes eliminated)",
    "RT-2_d3_pre_translation_traceability": "CLOSED (v7 — SUPP-EV-026 adds on_label_claim_raw_he + claim_translation_provenance)",
    "RT-3_pediatric_dosing": "CLOSED (v5/v6, confirmed unchanged v7 — 3 products at unscoreable_pediatric)",
    "RT6-C1_iron_elemental_compound_ambiguity": "CLOSED (v7 — label_basis=elemental in iron.yaml; 3 iron products restored to S/91.2)",
    "RT6-C2_d3_pre_translation_residual": "CLOSED (v7 — SUPP-EV-026 traceability; adjudication documented in Nutrition D6)"
  },
  "acceptance_test": {
    "spec": "Confirm RT6-C1 and RT6-C2 are truly closed with trace evidence; attack the v7 fix weak spots (magnesium/zinc compound basis assumptions; name-derived minerals; iron overdose protection); assess residual Part C concerns; classify all findings CRITICAL/HIGH/MEDIUM; explicit PASS/FAIL on RT6-C1 and RT6-C2; explicit go/no-go on whether v7 is defensible for consumers with zero open CRITICAL",
    "result": "PASS — all delegated scope areas covered: RT6-C1 PASS (closed), RT6-C2 PASS (closed), Part B weak spots fully attacked (4 sub-items), Part C residual concerns assessed (4 items). Verdict: CONDITIONAL PASS."
  }
}
```
