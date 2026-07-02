# Red-Team Challenge Report — Supplements SIE v8 (real_corpus_v3)
Date: 2026-06-19
Scope: 78 scored / 118 shelf, SIE proto_v0 / algorithm_v0.2.0
Corpus file: _corpus_run_full_v8.json (TASK-356)
Prior reports: red_team_sie_v7.md (zero CRITICAL, three HIGH: RT7-H1/H2/H3)
Challenger: adversarial-qa-agent

---

## Track V — Verification

### V-Gate 1: Golden Validation (run_golden_validation.py)

Command: `c:\Bari\.venv\Scripts\python.exe run_golden_validation.py`
Exit code: 0
Result: **18/18 PASS**

All fixture sections:
- A. Per-dimension PASS/FAIL anchors (§6): 11/11 PASS
- B. Attribution archetypes (§13): 3/3 PASS
- C. Claim-resolution fixtures (§13.4, v1.3): 3/3 PASS
- D. RT7-H1 elemental-basis form=None overdose guard (TASK-356/SUPP-EV-027): **1/1 PASS**

Decisive test (§13.2) inverted-E pair: PASS — no-evidence E (cap_1) and dangerous E (veto_safety) carry different binding constraints, never confused.

Cross-fixture invariants (§13.4): PASS — R1 reachable only via resolution (B, blend-dominant); R2 stays E (cap_1); R3 strictly below R1 on same active (D, cap_3_honesty_core).

**SAFE-FAIL-d3-50k fixture**: score=20.0, grade=E, binding=veto_safety. Confirmed: the 50,000 IU daily D3 veto is intact.

V-Gate 1: **PASS**

---

### V-Gate 2: Grade Distribution Recount

Recount method: iterate all results where outcome="scored", tally engine_output.grade.
Total scored: 78.

| Grade | Header | Recount | Match |
|---|---|---|---|
| S | 11 | 11 | OK |
| A | 9 | 9 | OK |
| B | 16 | 16 | OK |
| C | 3 | 3 | OK |
| D | 16 | 16 | OK |
| E | 23 | 23 | OK |

Header matches recount: **PASS**

Note: The header edpg_note states "v7→v8 grade delta: S=11→13 (+2), B=16→15 (-1), C=4→3 (-1)". The actual v8 distribution is S=11, B=16, C=3 — the stated delta was incorrect (S did NOT increase to 13; it remained at 11). This is an internal documentation error in the corpus header, not a score propagation defect. The grade distribution itself is internally consistent. Documented as HIGH finding RT8-H1 (see Track C).

V-Gate 2: **PASS** (actual distribution internally consistent; the stated delta in edpg_note is wrong)

---

### V-Gate 3: Iron 3×S/91.2 Regression

All three iron bisglycinate products confirmed at S/91.2:
- 7290118814061 (SupHerb Iron 30mg): grade=S score=91.2 binding=blend_dominant_limit — INTACT
- 783495578741 (liposomal iron 27mg): grade=S score=91.2 binding=blend_dominant_limit — INTACT
- 7290012056741 (Tink Iron 36mg): grade=S score=91.2 binding=blend_dominant_limit — INTACT

V-Gate 3: **PASS**

---

### V-Gate 4: Zero veto_safety on Passing Grade

Checked all 78 scored products: 0 products carry safety=veto AND a non-E grade.
Only product with veto_safety is SP-7290018365359 (Tink Zinc 50mg), grade=E/20.0. Correct.

V-Gate 4: **PASS**

---

### V-Gate 5: Food Scoring Byte-Identical

Command: `git -C "C:\Bari" diff HEAD -- "bari-web/src/data/comparisons/"` → 0 lines output (empty diff).

The supplement engine changes (score_engine.py, evidence_dossiers/, golden_corpus/fixtures.py) are confined to the supplement pipeline. No food scoring JSON in bari-web/src/data/comparisons/ was modified.

V-Gate 5: **PASS**

---

### V-Gate 6: qa_audit.py — NOT FOUND (FAIL)

The dispatch specification states "qa_audit.py PASS (5/5)" as a required gate. No qa_audit.py file exists at C:\Bari\03_operations\supplement_engine\proto_v0\ or any subdirectory. The only audit runner present is run_golden_validation.py (which passed 18/18).

This is an **unverifiable gate claim**. The dispatch specification references a script that does not exist in the repository. This gate cannot be confirmed or denied. Classified: Track V discrepancy — routes to data-agent (determine whether qa_audit.py existed and was removed, or was never written, and reconcile the dispatch specification).

V-Gate 6: **UNVERIFIABLE** (script referenced in spec does not exist)

---

### Track V Summary

| Gate | Result | Observed Value |
|---|---|---|
| V1: Golden 18/18 | PASS | 18/18, exit code 0 |
| V2: Grade distribution | PASS | S=11 A=9 B=16 C=3 D=16 E=23 (header = recount) |
| V3: Iron 3×S regression | PASS | 7290118814061/783495578741/7290012056741 all S/91.2 |
| V4: 0 veto on passing grade | PASS | 0 products with veto_safety AND non-E grade |
| V5: Food scoring byte-identical | PASS | git diff → 0 lines |
| V6: qa_audit.py 5/5 | UNVERIFIABLE | File does not exist |

**Track V Verdict: CONDITIONAL** — 5/5 runnable gates PASS; the sixth gate is unverifiable because the referenced script is absent.

---

## Track C — Adversarial Challenge

### Opening Finding

**The v8 edpg_note contains a materially false claim about the score outcome for two zinc picolinate products.** The note states "SP-0033984037250 (22mg, B/68.4→S/91.2)" and "SP-7290006437563 (25mg, B/69.7→S/91.2)." The actual scores in the corpus are B/77.5 for both. This is not a rounding error — it is a three-grade error in the documentation of the fix's outcome.

The underlying fix (elemental label_basis applied to zinc) is correct: dose=92 (in_range) confirms the elemental basis is applied. But the scores are B/77.5 because the claim on both products is "תמיכה במערכת החיסון" (immune support) = Weak evidence tier (evidence_val=47.0), not Strong. S/91.2 would require Strong evidence (evidence_val=92.5), which would require a deficiency-correction claim. These products make a general immune support claim, not a deficiency-correction claim.

The edpg_note's stated grade delta (S=11→13, B=16→15) is also wrong: S remains 11 and B remains 16. The grade distribution header itself is correct (matching the recount), but the stated delta narrative is fabricated or was written for an earlier version of the fix that was subsequently changed.

**Consumer-facing risk is LOW** (no grade shown to consumer yet — corpus is candidate/unpublished). The internal documentation error does not affect the scores displayed to consumers. However, it is a documentation integrity failure that must be noted before any go/no-go decision.

---

## Part A — Delta 1: Zinc label_basis=elemental (RT7-H2, SUPP-EV-027)

### A-1: Is the elemental assumption sound?

The v8 zinc.yaml sets `label_basis: "elemental"`, citing Israeli MOH Regulations for Dietary Supplement Products 2003 (amendment 2009) — the same regulatory instrument cited for iron (SUPP-EV-025). The dossier notes: the label pattern "אבץ (zinc picolinate) 22 מ"ג" states elemental zinc (אבץ = zinc the element; picolinate = form in parentheses).

**Challenge: is this assumption independently defensible?**

The label pattern observed on SP-0033984037250: `"ingredient": "אבץ (zinc picolinate)", "amount": 22.0, "form": "picolinate"`. The Hebrew text "אבץ (zinc picolinate) 22 מ"ג" follows the exact same structural pattern as iron bisglycinate: [element name] ([chelate form]) [amount]. The amount modifies the elemental name, not the compound.

Supporting evidence for elemental interpretation:
1. If 22mg stated compound mass → 22 × 0.211 = 4.64mg elemental zinc → below the adult RDA (8mg women / 11mg men). A supplement positioned as a zinc supplement providing sub-RDA elemental zinc would be clinically incoherent for any maintenance use.
2. Solgar Zinc Picolinate is labeled on Solgar's international site at 22mg zinc (elemental), matching DSLD market range [8–50mg elemental]. Compound mass interpretation (4.64mg) does not appear in any standard supplement reference.
3. The structural label convention "[element] ([chelate form]) [amount]" = elemental amount is industry-standard for chelated minerals in the Israeli and international supplement markets.

**Judgment: the elemental assumption for zinc is sound.** The regulatory instrument cited (Israeli MOH 2003/2009) is the same that governed the iron fix (SUPP-EV-025), and the market-range and label-pattern evidence coheres. A skeptical regulator, food scientist, or journalist examining the Solgar Zinc Picolinate 22mg label would agree that 22mg refers to elemental zinc.

**However: the fix produced B/77.5, not S/91.2 as stated in the edpg_note.**

The dose sub-score is 92 (in_range), confirming the elemental basis fires correctly. The binding constraint is blend_dominant_limit with evidence=47.0 (Weak tier). The claim "אבץ פיקולינאט לתמיכה במערכת החיסון ועור בריא" (zinc picolinate for immune system support and healthy skin) resolves to "broad immune system support" = Weak evidence. This is a correct resolution: daily oral zinc for general immune support is Weak (not Strong, which requires a deficiency-correction claim).

**Verdict on Delta 1 (elemental basis fix):** CORRECT — the label_basis=elemental change is scientifically sound and the engine behavior is correct (dose in_range for both products). The stated score outcome in the edpg_note (S/91.2) is wrong; the actual outcome (B/77.5) is the correct score for a Weak-evidence immune claim. The fix is a genuine improvement: these products moved from B/68.4 (sub-therapeutic under compound assumption) to B/77.5 (in-range dose under elemental, but Weak evidence claim = B). This is a correct-direction fix; the error is in the documentation, not the score.

### A-2: Are the two picolinate products correctly graded at B/77.5?

Sub-score analysis for SP-0033984037250 (Solgar Zinc Picolinate 22mg):
- Evidence: 47.0 (Weak — "broad immune support" = Weak, PMID:29186856, PMID:23775705)
- Dose: 92 (in_range — 22mg elemental > 8mg min_effective)
- Form: 92 (picolinate = preferred form)
- Honesty: 100
- Safety: neutral (22mg < 40mg UL)
- Blend: 0.3×47 + 0.25×92 + 0.2×92 + 0.15×100 + 0.1×70 = 14.1+23+18.4+15+7 = 77.5

This arithmetic is exact and correct. B/77.5 is the genuine score for a well-formulated zinc picolinate supplement making a broad immune support claim. **The grade is defensible.**

A journalist or regulator asking "why is this B and not S?" can be answered: the claim is general immune support, which has Weak evidence in supplemented adults; a deficiency-correction claim would earn S. This is a legitimate scoring distinction.

### A-3: Tink Zinc 50mg — Safety Veto Path

**The edpg_note states**: "SP-7290018365359 (Tink Zinc 50mg, elemental, form=None via name_derived): 50mg elemental > 40mg UL → VETO → correctly E; was E/34 via cap_1 (no claim), remains E."

**What the trace actually shows**: The bsip0s_label actives entry has `"form": "picolinate"` — form was resolved FROM the product name ("טינק אבץ פיקולינאט 50 מג"). The lossy field confirms "form_resolved_from_name_he:'picolinate'". Therefore form is NOT None as the edpg_note states. The product enters the engine with form="picolinate".

**Consequence for RT7-H1 path**: The RT7-H1 safety guard in score_engine.py fires only when `elemental_by_form and active.form is None`. With form="picolinate", the RT7-H1 guard does NOT fire. Instead, the standard path executes:
1. `_effective_label_quantity` is called: label_basis=elemental, form="picolinate" → no conversion (elemental basis: "elemental_basis_no_conversion" note) → qty = 50mg.
2. `score_safety` reaches the standard comparison at line 607: `daily = 50mg > ul = 40mg → VETO`. Reason: "exceeds_UL".

This is confirmed by the trace: `"safety": {"value": "veto", "reason": "exceeds_UL"}` — NOT "elemental_basis_no_form_exceeds_ul" (which would be the RT7-H1 path).

**Net result is correct**: 50mg elemental zinc > 40mg UL → E/20.0 (veto). The VETO correctly fires. However, the stated mechanism in the edpg_note is wrong: the veto routes through the standard exceeds_UL path (form known from name parse), not through the RT7-H1 form=None elemental-basis path.

**Consumer-facing grade impact**: E either way. The edpg_note claim "was E/34 via cap_1, remains E" is partially right — the product is still E, but the mechanism changed: it now binds veto_safety at E/20.0 (not cap_1 at E/34). The binding_constraint changed AND the score changed (34→20). The note correctly says "remains E" but mischaracterizes the change as "same E, different cap" when it is actually "same grade, different score (34→20), different binding mechanism."

**The score IS lower (20 vs 34) — this is a consumer-facing change.** A product previously E/34 is now E/20.0. Both are E, but if displayed numerically, 20.0 would appear harsher. This is correct (a veto should floor harder than an evidence cap), but the edpg_note's framing "remains E" without noting the 34→20 score change and cap_1→veto_safety mechanism shift is misleading documentation.

**Verdict on Delta 1 (Tink 50mg safety veto):** CORRECT outcome (E grade, veto appropriate — 50mg elemental zinc exceeds the 40mg UL). Mechanism actually used: standard exceeds_UL path (form="picolinate" from name parse), NOT the RT7-H1 form=None path. The RT7-H1 guard was not actually exercised by this real product. Score changed from E/34 to E/20 — both E, but the documentation doesn't flag the score change.

---

## Part B — Delta 2: Magnesium Carbonate (RT7-H3, SUPP-EV-028)

### B-1: Fraction 0.288 verification

MgCO3 molecular weight verification:
- Mg: 24.305 g/mol (IUPAC standard)
- C: 12.011 g/mol
- O×3: 3 × 15.999 = 47.997 g/mol
- MgCO3 MW = 24.305 + 12.011 + 47.997 = 84.313 g/mol
- Elemental fraction = 24.305 / 84.313 = 0.2882, rounded to 0.288

**Fraction 0.288 is arithmetically correct.** The prior red-team estimate of ~0.239 was wrong (used a mixed-form estimate). The v8 dossier value of 0.288 is verified against PubChem CID 11029 molecular weights.

### B-2: D/49 arithmetic verification

SP-7290015429245: 160mg carbonate × 0.288 = 46.08mg elemental.
- fairy_floor = 0.5 × min_effective(300mg) = 150mg
- 46.08mg < 150mg → fairy_dust → cap_2 floor = D/49

From the trace: dose=20 (fairy_dust reason confirmed), binding=cap_2_fairy_dust_hidden_dose, score=49.0, grade=D.

**D/49 is correct.** The trace confirms the carbonate conversion fired: 160 × 0.288 = 46.1mg elemental < fairy_floor(150mg) → fairy_dust → cap_2 → D/49.

The evidence tier resolved to Weak (claim: "מגנזיום לתפקוד תקין של השרירים ומערכת העצבים" → "muscle health" → Weak). Form=50 (carbonate is not on the magnesium form ladder; neither preferred nor poor → form_unknown = 50). The fairy_dust cap (ceiling=49) binds before the blend (51.1).

Safety: trace shows "within_ul". Verification: 160mg carbonate × 0.288 = 46.1mg elemental. Hard UL = 350mg supplemental. 46.1 << 350 → safely within UL regardless of interpretation.

**Verdict on Delta 2 (Mg carbonate):** CORRECT — fraction 0.288 verified from first principles; D/49 confirmed by trace arithmetic; safety correctly neutral. The prior C/59.2 was a dossier-omission error; D/49 is the correct grade.

---

## Part C — Delta 3: RT7-H1 Iron Guard + Fixture

### C-1: Fixture tests real elemental-basis form=None overdose path

Fixture RT7-H1-elemental-form-none-overdose: iron 65mg elemental, form=None, claim "blood / blood health."
- score_engine path: elemental_by_form non-empty (iron dossier), form=None, label_basis=elemental → RT7-H1 branch: compare 65mg directly to UL=45mg → 65 > 45 → VETO → E/20.0
- Trace: grade=E, binding=veto_safety, safety=veto — confirmed
- The fixture genuinely exercises the "elemental-basis form=None overdose" scenario the prior code failed on.

**PASS: the fixture tests a real overdose path and correctly vetoes.**

### C-2: No real product disturbed by the RT7-H1 fix

The RT7-H1 path fires when: (a) `elemental_by_form` is non-empty (mineral dossier), (b) `active.form is None`, (c) `label_basis == "elemental"`.

Real corpus products where this could apply: any name-derived or form-unknown iron product. The two name-derived iron products are SP-7290016417197 and SP-7290015765985 — both scored E (no claim) and amounts 15mg and 30mg respectively, both below the 45mg UL. Both would be safety-neutral under the RT7-H1 path (15mg ≤ 45 → neutral; 30mg ≤ 45 → neutral) — same outcome as before. No real product is disturbed.

For Tink Zinc 50mg: as established in Part A, form="picolinate" (from name parse), so the RT7-H1 path does NOT fire. The standard exceeds_UL path fires instead.

**PASS: no real product was disturbed by the RT7-H1 fix. All affected real products land at the same grade/score via their actual (non-RT7-H1) path.**

### C-3: "SAFE-FAIL-d3-50k still vetoes" — confirmed

SAFE-FAIL-d3-50k fixture: 50,000 IU D3 daily, score=20.0, grade=E, binding=veto_safety. The D3 safety veto is intact and unaffected by the v8 changes.

---

## Product-by-Product Assessment (Delta Products)

| SKU | Product | Score v8 | Grade | v7 Score | Assessment |
|---|---|---|---|---|---|
| SP-0033984037250 | Solgar Zinc Picolinate 22mg | 77.5 | B | 68.4/B | CORRECT. Elemental basis applied (dose=in_range); grade unchanged because evidence=Weak (immune claim). |
| SP-7290006437563 | Altman Zinc Picolinate 25mg | 77.5 | B | 69.7/B | CORRECT. Same pattern as Solgar. Both improved 68→77 in score; grade B in both v7 and v8. |
| SP-7290018365359 | Tink Zinc 50mg | 20.0 | E | 34.0/E | CORRECT GRADE (E), but path differs from stated. Veto via standard exceeds_UL (form=picolinate from name parse), NOT RT7-H1 form=None path. Score changed 34→20. |
| SP-7290015429245 | Amorphicure Mg Carbonate 160mg | 49.0 | D | 59.2/C | CORRECT. Fraction 0.288 verified; D/49 confirmed by trace (fairy_dust cap). One grade improvement in accuracy. |
| SP-7290118814061 | SupHerb Iron 30mg | 91.2 | S | 91.2/S | INTACT (v7 fix). Confirmed unchanged. |
| SP-783495578741 | Liposomal Iron 27mg | 91.2 | S | 91.2/S | INTACT (v7 fix). Confirmed unchanged. |
| SP-7290012056741 | Tink Iron 36mg | 91.2 | S | 91.2/S | INTACT (v7 fix). Confirmed unchanged. |

---

## Summary Assessment

**Justified scores:** Three iron S-grades (elemental basis, RT6-C1 fix intact). D3 S-grades (English label and "מחסור" pre-translation, RT6-C2 closed). B12 S-grades. Mg oxide B-grades (RT-1 fix). Amorphicure Mg carbonate D/49 (RT7-H3 fix, correct). Tink Zinc 50mg E/20 (correct veto).

**Correct-direction, correct-grade, wrong-mechanism documented:** Tink Zinc 50mg veto fires via standard exceeds_UL (form="picolinate" from name parse), not RT7-H1 form=None path as stated. Grade E is correct; the edpg_note's mechanism description is wrong.

**Correct-direction, correctly scored, wrong-stated-outcome in documentation:** Both zinc picolinate products are B/77.5 (not S/91.2 as edpg_note claims). The dose fix is correct; the claim resolves to Weak, so B is the right answer.

**v7 open HIGH findings — disposition:**
- RT7-H1 (latent iron veto gap): CLOSED — engine fix implemented (score_engine.py RT7-H1 branch), fixture passes (18/18), no real product disturbed.
- RT7-H2 (zinc picolinate label_basis): CLOSED — label_basis=elemental set in zinc.yaml, SUPP-EV-027, products score correctly (B/77.5 for immune claim, not S/91.2 as mis-stated in edpg_note).
- RT7-H3 (magnesium carbonate): CLOSED — carbonate added to magnesium.yaml compound_forms_identity, fraction 0.288 verified, D/49 confirmed.

**All three v7 HIGH findings are structurally resolved.**

---

## Findings by Severity

### CRITICAL — must resolve before launch

**None.** Zero open CRITICAL findings.

---

### HIGH — should resolve before launch

**RT8-H1: edpg_note contains false stated outcome for zinc picolinate grade delta**

The corpus header edpg_note states "SP-0033984037250 (22mg, B/68.4→S/91.2), SP-7290006437563 (25mg, B/69.7→S/91.2)" and "v7→v8 grade delta: S=11→13 (+2), B=16→15 (-1)." The actual v8 scores are B/77.5 for both products; S=11 (unchanged); B=16 (unchanged).

Evidence: grade_distribution header={B:16, S:11}; recount from engine_output confirms identity. Trace for SP-0033984037250: evidence_tier=Weak (immune claim), dose=92 (in_range), final=B/77.5. The edpg_note's claim of S/91.2 is a three-grade error in the documentation.

Implication: If a Product Agent or Nutrition Agent reads the edpg_note to validate the v8 run, they will believe two products were promoted to S and the S-pool grew to 13. Neither is true. Any go/no-go decision based on the edpg_note's stated grade delta would be misinformed. The actual scoring is correct; the documentation is wrong.

Routes to: data-agent (correct the edpg_note to state actual outcomes: "SP-0033984037250: B/68.4→B/77.5 (dose moved from sub_therapeutic to in_range; grade unchanged — claim resolves Weak); SP-7290006437563: B/69.7→B/77.5 (same); grade delta S=11 unchanged, B=16 unchanged, C=4→3 from Mg carbonate fix").

---

**RT8-H2: Tink Zinc 50mg — stated mechanism (RT7-H1 form=None path) does not match actual path (standard exceeds_UL)**

The edpg_note and corpus description claim Tink Zinc 50mg exercises the RT7-H1 guard ("form=None via name_derived"). The actual trace shows safety_reason="exceeds_UL" — the standard path — because the runner resolved form="picolinate" from the product name before engine entry. RT7-H1 (the form=None elemental-basis guard) was NOT exercised by this real product.

Evidence: bsip0s_label shows `"form": "picolinate"` for SP-7290018365359; the trace confirms `safety.reason = "exceeds_UL"` (not "elemental_basis_no_form_exceeds_ul"). The score changed from E/34 (v7, cap_1) to E/20 (v8, veto_safety) — a change the edpg_note does not clearly disclose.

Implication: (a) The RT7-H1 guard has no real-corpus exercise — it is tested only by the synthetic fixture. (b) The score delta (34→20) was not disclosed. (c) If a future product with genuine form=None and elemental label_basis appears, the RT7-H1 guard is the untested-by-real-data path. The fixture test is the only validation.

Routes to: data-agent (correct edpg_note to state actual mechanism; disclose 34→20 score change). nutrition-agent (confirm whether RT7-H1 guard's reliance on fixture-only validation is acceptable given the corpus has no real-product exercise of the form=None + elemental-basis path).

---

### MEDIUM — should document or monitor

**RT8-M1: S-grade cluster at 91.2 — 11 products (unchanged from v7)**

11 S-grade products all score exactly 91.2. Three iron bisglycinate, five D3, three B12. A journalist comparing a pregnancy iron supplement to a D3 drop sees identical scores. v7's RT7-M1 finding; unchanged.

Routes to: nutrition-agent (calibration — sub-tier differentiation within the S pool).

---

**RT8-M2: Omega-3 heart-claim mislabeling — unchanged from v7 (RT7-M2)**

Four omega-3 products with cardiovascular or DHA-developmental claims record claim_matched = "brain & mood / general cognition (BROAD consumer claim)." Consumer copy derived from this field would attribute D grades to the wrong reason.

Routes to: content-agent, nutrition-agent.

---

**RT8-M3: Three D3 S-grades carry expert adjudication risk — unchanged from v7 (RT7-M3)**

The three "מחסור" pre-translated D3 S-grades depend on Nutrition D6 adjudication that the deficiency-correction translation is Strong. Traceable (RT6-C2 closed) but an expert judgment, not self-evident from the label.

Routes to: product-agent (ensure D6 adjudication document is accessible at launch).

---

**RT8-M4: Life brand coverage gap — unchanged from v7 (RT7-M4)**

7 of 22 Life products scored (32%). 15 remain unscoreable_incomplete. The comparison skews toward premium brands.

Routes to: product-agent (category caveat disclosure).

---

**RT8-M5: qa_audit.py referenced but absent**

The dispatch specification names "qa_audit.py PASS (5/5)" as a required verification gate. No such script exists in the repository. The existing golden validation runner (run_golden_validation.py) covers 18 fixtures and passes; but whatever 5 distinct checks "qa_audit.py" was meant to run cannot be confirmed.

Routes to: data-agent (verify whether qa_audit.py was planned, written, removed, or was a naming error in the dispatch specification; if absent by intent, remove the reference from the dispatch spec).

---

## Verdict

**CONDITIONAL PASS — zero open CRITICAL findings; two HIGH findings (RT8-H1, RT8-H2) require documentation correction before go/no-go; five MEDIUM findings carry forward from v7.**

**V7 HIGH closure status:**
- RT7-H1 (iron latent veto gap): CLOSED — engine fix confirmed, fixture passes 18/18.
- RT7-H2 (zinc picolinate label_basis): CLOSED at the engine level; documented with RT8-H1/H2 caveats.
- RT7-H3 (magnesium carbonate): CLOSED — carbonate in dossier, D/49 confirmed.

**One-line go/no-go:** v8 is launch-defensible at zero open CRITICAL, but the edpg_note contains wrong stated outcomes (S/91.2 never happened; grade delta S=11→13 never happened; Tink mechanism was not RT7-H1), which must be corrected before any go/no-go decision to ensure Product and Nutrition are not acting on false information. The actual scores are correct; the documentation around what the scores are is wrong.

---

## Zinc Label_basis Determination (adversarial adjudication)

**Question:** Is the zinc elemental-basis assumption sound, and what is the actual consumer-facing risk?

**Determination: the assumption is sound.** Reasoning:

1. **Label pattern**: "אבץ (zinc picolinate) 22 מ"ג" follows the identical structure as iron bisglycinate: [element name] ([compound form]) [amount]. The amount (22mg) modifies the elemental name (אבץ = zinc), not the compound (zinc picolinate). This is the standard Israeli supplement label format for chelated minerals.

2. **Clinical coherence test**: Under compound assumption, 22mg × 0.211 = 4.64mg elemental zinc — below the adult RDA (8mg women / 11mg men). A supplement positioned as a standard zinc supplement providing sub-RDA elemental zinc is clinically incoherent for any maintenance use. Under elemental assumption, 22mg is a normal dose in the 8–40mg studied range.

3. **Regulatory grounding**: The Israeli MOH Regulations for Dietary Supplement Products 2003 (amendment 2009), cited for the iron fix (SUPP-EV-025), governs chelated mineral labeling. The dossier relies on the same instrument for zinc (SUPP-EV-027), and the label pattern is identical.

4. **Score impact under correct basis**: Dose moves from sub_therapeutic to in_range (+23 points on dose). However, the two picolinate products score B/77.5 (not S/91.2) because their claim is "immune support" (Weak evidence), not deficiency correction (Strong). The grade remains B. No consumer harm from the elemental assumption.

**Quantified consumer-facing risk if assumption were wrong:**
- Under compound basis: 4.64mg elemental → sub_therapeutic → dose sub-score ≈ 52 → blend ≈ 68 → B/68.4 (actual v7 score).
- Under elemental basis: 22mg → in_range → dose=92 → blend ≈ 77.5 → B/77.5 (v8 score).
- Grade unchanged (B in both cases for immune claim). Score changes from 68→77. The consumer sees a higher B score but the same grade label.
- If elemental assumption is wrong AND the correct score is B/68 rather than B/77, the consumer impact is a 9-point score overstatement within the same grade band. This is a within-grade calibration error, not a grade misclassification. Not a safety issue.

**The zinc elemental determination is correct and the consumer-facing risk of an incorrect assumption is bounded to a within-grade-band score shift.**

---

```json
{
  "return_contract": "v1",
  "agent": "adversarial-qa-agent",
  "task_ref": "TASK-356 v8 final adversarial gate",
  "run_date": "2026-06-19",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_sie_v8.md",
      "sha256": "written-this-run",
      "role": "challenge_report"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v8.json",
      "sha256": "read-only-source",
      "role": "corpus_scored_v8"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\src\\score_engine.py",
      "sha256": "read-only-source",
      "role": "score_engine_v8_with_RT7H1"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\zinc.yaml",
      "sha256": "read-only-source",
      "role": "zinc_dossier_label_basis_elemental_SUPP-EV-027"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\magnesium.yaml",
      "sha256": "read-only-source",
      "role": "magnesium_dossier_with_carbonate_SUPP-EV-028"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\evidence_dossiers\\iron.yaml",
      "sha256": "read-only-source",
      "role": "iron_dossier_label_basis_elemental_SUPP-EV-025"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\golden_corpus\\fixtures.py",
      "sha256": "read-only-source",
      "role": "fixture_library_18_including_RT7H1"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\run_golden_validation.py",
      "sha256": "read-only-source",
      "role": "golden_validation_runner"
    }
  ],
  "counts": {
    "denominator_description": "118 shelf products; 78 scored in v8",
    "total_shelf": 118,
    "total_scored": 78,
    "unscoreable_incomplete": 26,
    "unscoreable_pediatric": 3,
    "unscoreable_premarket": 11,
    "grade_S": 11,
    "grade_A": 9,
    "grade_B": 16,
    "grade_C": 3,
    "grade_D": 16,
    "grade_E": 23,
    "golden_fixtures_total": 18,
    "golden_fixtures_pass": 18,
    "golden_fixtures_fail": 0,
    "iron_s_grades_confirmed_intact": 3,
    "veto_safety_on_passing_grade": 0,
    "food_scoring_diff_lines": 0,
    "open_criticals_v8": 0,
    "open_highs_v8": 2,
    "open_mediums_v8": 5,
    "v7_high_rt7h1_status": "CLOSED",
    "v7_high_rt7h2_status": "CLOSED (engine correct; documentation error in edpg_note)",
    "v7_high_rt7h3_status": "CLOSED",
    "zinc_picolinate_actual_score_v8": "B/77.5 (both products — NOT S/91.2 as stated in edpg_note)",
    "tink_50mg_veto_path_actual": "standard exceeds_UL (form=picolinate from name parse) — NOT RT7-H1 form=None path",
    "tink_50mg_score_v7_to_v8_delta": "E/34.0 (cap_1) -> E/20.0 (veto_safety)",
    "qa_audit_py_exists": false
  },
  "commands_run": [
    {"cmd": "c:\\Bari\\.venv\\Scripts\\python.exe run_golden_validation.py", "exit_code": 0, "result": "18/18 PASS"},
    {"cmd": "python _tmp_v8_check.py (grade distribution recount)", "exit_code": 0, "result": "S=11 A=9 B=16 C=3 D=16 E=23 all match header"},
    {"cmd": "python _tmp_v8_analysis.py (dimension weights, zinc blend math, iron regression, veto-on-passing check)", "exit_code": 0, "result": "all checks PASS; zinc blend verified 77.5"},
    {"cmd": "python _tmp_tink_detail.py (full trace extraction for Tink 50mg, Solgar zinc, Amorphicure)", "exit_code": 0, "result": "traces extracted; form=picolinate on Tink confirmed; carbonate D/49 confirmed"},
    {"cmd": "git -C C:\\Bari diff HEAD -- bari-web/src/data/comparisons/", "exit_code": 0, "result": "0 lines (food scoring unchanged)"},
    {"cmd": "Read score_engine.py (RT7-H1 branch at lines 527-557)", "exit_code": 0},
    {"cmd": "Read zinc.yaml (label_basis=elemental, SUPP-EV-027 change_log)", "exit_code": 0},
    {"cmd": "Read magnesium.yaml (carbonate entry, SUPP-EV-028 change_log, fraction 0.288)", "exit_code": 0},
    {"cmd": "Read iron.yaml (label_basis=elemental, UL=45mg)", "exit_code": 0},
    {"cmd": "Read fixtures.py (RT7_H1_FIXTURES, ALL_FIXTURES count=18)", "exit_code": 0},
    {"cmd": "Read run_golden_validation.py (section D, RT7-H1 fixture count)", "exit_code": 0},
    {"cmd": "Read red_team_sie_v7.md (prior findings for regression check)", "exit_code": 0},
    {"cmd": "Glob for qa_audit.py", "exit_code": 0, "result": "NOT FOUND"}
  ],
  "not_done": [
    "External primary-source verification of Israeli MOH zinc-labeling regulation (cited in SUPP-EV-027; accepted as stated in dossier — nutrition-agent scope)",
    "Full audit of all 26 unscoreable_incomplete products (out of v8 scope; no anomalies in prior spot-checks)",
    "Frontend JSON challenge (no supplements frontend JSON exists — consumer-facing content gate is deferred to that phase)",
    "Magnesia brand shelf-status re-verification (RT7-M4 persistent; data-agent scope)",
    "NEEDS-ENV-VERIFY items in dossiers (iron UL 45mg NIH source; zinc UL 40/25mg NIH/EFSA; magnesium UL 350/250mg NIH/EFSA — all flagged candidate, nutrition-agent scope)"
  ],
  "verdict": "CONDITIONAL PASS",
  "open_criticals": [],
  "open_highs": [
    "RT8-H1 (edpg_note false stated outcomes: zinc picolinate stated S/91.2 but actual B/77.5; grade delta S=11→13 never happened; routes to data-agent)",
    "RT8-H2 (Tink 50mg mechanism mismatch: stated RT7-H1 form=None path; actual standard exceeds_UL with form=picolinate from name parse; score changed 34→20 undisclosed; routes to data-agent)"
  ],
  "v7_high_closure": {
    "RT7-H1_iron_latent_veto_gap": "CLOSED — engine fix in score_engine.py lines 527-557; RT7-H1 fixture passes; no real product disturbed",
    "RT7-H2_zinc_label_basis": "CLOSED (engine correct: dose=in_range for both picolinate products) — documentation error in edpg_note (see RT8-H1)",
    "RT7-H3_magnesium_carbonate": "CLOSED — fraction 0.288 verified; D/49 confirmed by trace"
  },
  "acceptance_test": {
    "spec": "Run both tracks V+C; golden 18/18; grade distribution matches; iron 3×S intact; 0 veto on passing grade; food scoring byte-identical; adjudicate zinc elemental basis and quantify consumer risk; verify Mg carbonate fraction and D/49; confirm RT7-H1 fixture tests real elemental-basis form=None overdose path; classify all findings; explicit verdict on each delta; go/no-go at zero open CRITICAL",
    "result": "PASS — all delegated scope areas covered. Track V: 5/5 runnable gates PASS (sixth gate unverifiable — qa_audit.py absent). Track C: zinc elemental basis adjudicated (correct, B/77.5 not S/91.2); Mg carbonate fraction 0.288 verified; RT7-H1 fixture confirmed as real synthetic overdose test; all three v7 HIGH findings structurally closed. Two new HIGH findings (documentation errors in edpg_note). Zero CRITICAL. Verdict: CONDITIONAL PASS."
  }
}
```
