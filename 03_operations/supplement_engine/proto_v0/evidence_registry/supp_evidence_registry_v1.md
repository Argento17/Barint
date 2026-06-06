# SIE Evidence Registry — `SUPP-EV-###` (v1)

**Classification:** Internal — Supplement Scoring Intelligence (sibling to BSIP2 `EV-###`; the two registries never cross)
**Scope:** Phase 1 (TASK-171B) — the 5 MVP actives. Promotes methodology §8 seeds 001–005 to reflect the **built + co-signed** dossiers.
**Owner:** Nutrition Agent · **Co-sign:** Nutrition (D6 tiers + D7 authority) + Product (D7) — see status per entry.
**Firewall (EDPG):** every entry leans on an external source for *calibration/justification* only; the engine reads the in-house dossier, never a live external value. `should_affect_score_now: false` on **all** entries — Phase 1 builds reference data, Phase 2 calibrates, nothing ships.

> **What this co-sign covers.** D6 = the evidence-tier assignment per `(active → claim)`. D7 = the scoring-rule/authority choices (governing UL among discrepant authorities, contested-deferral). It does **NOT** confirm any primary UL/safety number flagged `NEEDS-ENV-VERIFY` — those stay candidate re-sync items; the co-sign is on the tier/authority *choice*, not the raw datum.

---

## Status legend

| Field | Meaning |
|---|---|
| `evidence_tier` | finalized Nutrition D6 tier (Strong / Moderate / Weak / Insufficient / contested-deferred) |
| `should_affect_score_now` | `false` for all Phase-1 entries (firewall) |
| `d7_status` | **D6/D7 CO-SIGNED (candidate)** = Nutrition co-signed tiers+authority this task; Product D7 co-sign of the methodology already stands (v1.1); per-rule Product co-sign rides the methodology co-sign for Phase-1 reference build, formal per-number Product co-sign is a Phase-2 calibration gate |
| `verify_flag` | `NEEDS-ENV-VERIFY` items the co-sign does **not** confirm |

---

## SUPP-EV-001 — Creatine: effective dose & no-UL; claim-specific tiers

| Field | Value |
|---|---|
| concept | Creatine monohydrate ≈ 3–5 g/day maintenance; no established UL. Claim-specific: **strength/lean-mass (with resistance training) = Strong**; **fat loss = Insufficient** (untethered claim, §2.1 default). |
| dimension | Evidence (§2.1), Dose Adequacy (§2.2), Safety Ceiling (§2.5 PASS-control, no-UL) |
| evidence_tier | strength/lean-mass: **Strong** (RATIFIED); fat-loss: **Insufficient** (RATIFIED) |
| citations | PMID:39519498, 37432300, 39074168, 34836013, 24576864 (strength); fat-loss: none (no matching endpoint) |
| source | `literature` (PubMed MAs); ISSN position stand (form authority); `dsld` (market dose 1.5–5 g sanity-check); `pubchem` CID 80116/586 (identity) |
| should_affect_score_now | false |
| risk_of_misuse | treating no-UL as license for mega-dose → fall back to `upper_studied` 5 g/day (§2.5); letting the strength Strong tier bleed onto the fat-loss claim |
| verify_flag | NEEDS-ENV-VERIFY: NIH ODS no-UL statement; exact ISSN form-authority PMID |
| d7_status | **D6/D7 CO-SIGNED (candidate, not score-affecting)** — Nutrition 2026-06-03 |

```yaml
study_objects:
  - claim: "Creatine monohydrate supplementation (3–5 g/day) increases lean mass and strength with resistance training"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: A
    source_doi: "10.1186/s12970-017-0173-z"
    notes: "ISSN position stand 2017 — systematic review of RCTs; population healthy adults performing resistance training. Dose 3–5 g/day matches typical label serving. No conflict of interest declared."
  - claim: "Creatine supplementation shows no meaningful effect on fat loss as a standalone outcome"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: D
    source_doi: "PMID:24576864"
    notes: "Cited as representative of the null fat-loss evidence base. Fat loss is not a studied primary endpoint in quality creatine RCTs; D tier reflects absence of evidence, not evidence of absence."
```

## SUPP-EV-002 — Magnesium: oxide low bioavailability vs glycinate/citrate; claim tiers; governing UL

| Field | Value |
|---|---|
| concept | Mg oxide low fractional absorption (high *elemental* per compound mass = the trap) vs glycinate/citrate better absorbed. Claim tiers: **blood pressure = Moderate**; **sleep = Weak** (held, borderline Weak/Insufficient). Elemental-vs-compound mass is the Dose axis (§2.2). |
| dimension | Form & Bioavailability (§2.3, lead), Dose elemental basis (§2.2), Evidence (§2.1, claim tiers), Safety (§2.5 UL) |
| evidence_tier | form ladder (oxide < glycinate/citrate): **Moderate** (bioavailability studies, some heterogeneity); BP claim: **Moderate** (RATIFIED); sleep claim: **Weak** (RATIFIED, flagged borderline) |
| citations | PMID:39770988, 30761462, 7815675 (form/bioavailability); BP: 27402922, 41000008, 39519450, 22318649, 12160191; sleep: 33865376, 35184264, 40918053 |
| source | `literature` + `pubchem` (CID 14792/6099959/84645 → elemental fractions); `dsld` (125–400 mg market range) |
| should_affect_score_now | false |
| risk_of_misuse | conflating elemental content with absorbed dose; double-charging oxide (Form + Honesty must coordinate, §3); over-reading the thin sleep signal |
| **governing UL (D7) — REVISED (FLAG-2, standing meta-rule)** | **Hard veto = NIH/IOM 350 mg supplemental (toxicity-relevant); EFSA 250 mg (reversible GI/osmotic tolerance) → graded Safety NOTE band, NOT a veto.** Supersedes the prior "EFSA 250 governs the veto" pick: a reversible self-limiting GI threshold doesn't meet the harm bar a hard floor enforces, and the prior rule auto-vetoed an *adequately-dosed* Mg (`min_effective` ~300 > 250). Standing meta-rule (methodology §2.5): veto reserved for toxicity ceilings; reversible-tolerance thresholds → notes. Validated: 300 mg → A/Safety-note, 423 mg → E/veto. |
| verify_flag | NEEDS-ENV-VERIFY: EFSA 250 + NIH/IOM 350 primary values |
| d7_status | **D6/D7 CO-SIGNED (candidate, not score-affecting)** — Nutrition 2026-06-03; **FLAG-2 graded-UL revision CO-SIGNED Nutrition D6/D8 + Product D7 2026-06-03** |

```yaml
study_objects:
  - claim: "Magnesium supplementation (300–450 mg elemental/day) produces modest blood pressure reduction in hypertensive adults"
    dose_realistic: true
    population_direct: false
    rob_grade: moderate
    evidence_tier: B
    source_doi: "10.1111/jch.12775"
    notes: "PMID:27402922 — meta-analysis of 22 RCTs; population skewed toward hypertensive and pre-hypertensive adults, not healthy general population (population_direct: false). Effect size modest: ~2 mmHg SBP. Dose range 300–450 mg elemental matches real products at mid-to-high end."
  - claim: "Magnesium glycinate/citrate has meaningfully higher fractional absorption than magnesium oxide"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: B
    source_doi: "PMID:7815675"
    notes: "Comparative bioavailability study — magnesium oxide fractional absorption ~4% vs organic salts ~30%. Moderate tier because n is modest and cross-over period short. This is the foundational citation for the Form ladder in the SIE."
  - claim: "Magnesium supplementation reduces sleep-onset latency or improves subjective sleep quality"
    dose_realistic: true
    population_direct: false
    rob_grade: high
    evidence_tier: C
    source_doi: "PMID:33865376"
    notes: "PMID:33865376 — SR/MA 2021; 3 RCTs included, mostly elderly populations (population_direct: false). High heterogeneity, short duration. Tier C reflects genuine Weak evidence; borderline toward D. The borderline status is explicitly flagged in the SUPP-EV-002 entry."
```

## SUPP-EV-003 — Vitamin D3 (cholecalciferol) > D2; claim-specific tiers; adult UL

| Field | Value |
|---|---|
| concept | D3 raises/maintains serum 25(OH)D more effectively than D2. Claim tiers (claim-specific, no upward inheritance): **status-correction (raise 25(OH)D) = Strong**; **bone/fracture = Moderate** (conditional — clearer with calcium + in deficient/institutionalized groups, limited in replete community-dwelling adults); **all-cause mortality / broad prevention = Weak**. |
| dimension | Form (§2.3, D3>D2), Evidence (§2.1, 3 claim tiers), Safety Ceiling (§2.5, UL veto) |
| evidence_tier | status: **Strong**; bone/fracture: **Moderate** (conditional framing confirmed); mortality/broad: **Weak** — all RATIFIED |
| citations | status: 24414552, 39385006; bone: 29279934, 24119980, 26510847; mortality/broad: 24414552, 34815552; safety: 17209171, 24456284 |
| source | NIH ODS Vitamin D fact sheet (UL); `literature` (D2-vs-D3 RCTs, fracture MAs); `pubchem` CID 5280795/5280793 (D3/D2 identity) |
| should_affect_score_now | false |
| risk_of_misuse | applying adult UL to a children's SKU (children 1000–3000 IU age-banded); treating a clinician-directed weekly-repletion SKU as a daily-use veto; letting the Strong status-correction tier inherit onto bone/mortality claims |
| **governing UL (D7)** | **4,000 IU/100 mcg adult — CONFIRMED.** NIH ODS and EFSA concordant → no conservative-veto pick needed; concordant value governs. Child ULs tracked separately. |
| verify_flag | NEEDS-ENV-VERIFY: NIH ODS 4,000 IU adult UL primary value |
| d7_status | **D6/D7 CO-SIGNED (candidate, not score-affecting)** — Nutrition 2026-06-03 |

```yaml
study_objects:
  - claim: "Vitamin D3 raises serum 25(OH)D more effectively than D2 at equivalent IU doses"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: A
    source_doi: "10.3945/ajcn.111.031070"
    notes: "PMID:24414552 — systematic review and meta-analysis of head-to-head D3 vs D2 RCTs. Consistent superiority of D3 for 25(OH)D maintenance across studies. Dose ranges span 600–4000 IU/day, fully within real product range. No conflict reported."
  - claim: "Vitamin D3 supplementation (with or without calcium) reduces fracture risk in older or deficient adults"
    dose_realistic: true
    population_direct: false
    rob_grade: moderate
    evidence_tier: B
    source_doi: "10.1001/jamainternmed.2015.7148"
    notes: "PMID:26510847 — large meta-analysis. Conditional Moderate: clearest benefit in institutionalized elderly and vitamin-D-deficient populations. In replete, community-dwelling adults the effect is smaller and less consistent (population_direct: false for the general consumer claim). This conditionality is the foundation for the 'conditional Moderate' tier framing."
  - claim: "Vitamin D3 supplementation reduces all-cause mortality or broadly prevents chronic disease"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: C
    source_doi: "10.1001/jamanetworkopen.2021.31640"
    notes: "PMID:34815552 — large VITAL sub-analysis; null for most broad-prevention claims including cancer incidence and cardiovascular events. Tier C because the biological rationale is plausible but RCT evidence has consistently failed to confirm population-level mortality benefit."
```

## SUPP-EV-004 — Caffeine: ergogenic dose, claim tiers, proprietary-blend hiding; UL

| Field | Value |
|---|---|
| concept | Caffeine ergogenic ≈ 3–6 mg/kg (~200 mg adult). Claim tiers: **ergogenic/performance = Strong**; **acute alertness/vigilance (with broad-cognition halo) = Moderate**. Honesty lead: per-serving caffeine commonly hidden inside a proprietary "energy blend" → dose unknowable → Honesty cap (§2.4/§3 cap 3). The signal is HIDDEN DOSE, not the word "blend." |
| dimension | Formulation Honesty (§2.4, lead), Evidence (§2.1, claim tiers), Dose (§2.2), Safety (§2.5 total-caffeine) |
| evidence_tier | ergogenic: **Strong** (RATIFIED); alertness/cognition: **Moderate** (RATIFIED — alertness robust, broad cognitive halo weaker); blend-hiding = label-practice observation |
| citations | ergogenic: 29876876, 30926628, 29527137, 36615805; alertness: 20464765, 33800853 |
| source | `literature`; `dsld` (200 mg dominant disclosed dose — calibrates the disclosed-panel baseline so the Honesty cap threshold is grounded) |
| should_affect_score_now | false |
| risk_of_misuse | scoring "blend" by name vs hidden-dose by disclosure (penalize disclosure failure, not nomenclature); ignoring the pregnancy sub-limit |
| **governing UL (D7)** | **400 mg/day adult / 200 mg single dose / 200 mg pregnancy — CONFIRMED.** EFSA & FDA concordant (not an IOM-style UL; safe-intake guidance) → concordant value governs; pregnancy 200 mg is a distinct population sub-limit. |
| verify_flag | NEEDS-ENV-VERIFY: EFSA 2015 caffeine opinion (400/200/200) |
| d7_status | **D6/D7 CO-SIGNED (candidate, not score-affecting)** — Nutrition 2026-06-03 |

```yaml
study_objects:
  - claim: "Caffeine at 3–6 mg/kg body weight improves endurance and high-intensity exercise performance"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: A
    source_doi: "10.1007/s40279-018-0949-1"
    notes: "PMID:29876876 — International Society of Sports Nutrition position stand on caffeine. Synthesizes large body of RCT evidence. Dose 3–6 mg/kg (~200–400 mg for 70 kg adult) matches typical disclosed pre-workout label dose. Population: healthy trained adults."
  - claim: "Caffeine (75–200 mg) improves acute alertness and sustained attention"
    dose_realistic: true
    population_direct: true
    rob_grade: low
    evidence_tier: B
    source_doi: "10.1177/0269881110376190"
    notes: "PMID:20464765 — systematic review of double-blind RCTs on cognitive performance. Alertness and sustained attention effects are robust; broader 'cognitive enhancement' (memory, executive function) evidence is weaker. Moderate overall tier reflects that the alertness claim is strong but the full cognitive halo is overstated by most product labels."
```

## SUPP-EV-005 — Omega-3 (EPA/DHA): claim-specific tiers + conflation firewall; dose basis; form ladder; mass-honesty trap; governing UL

> **Note:** SUPP-EV-005 was re-assigned from ashwagandha to omega-3 per methodology v1.1 (Evidence-probe swap). Ashwagandha is a **deferred Phase-2 note** (below), not a live entry.

| Field | Value |
|---|---|
| concept | SAME EPA/DHA molecule, tiered **per claim**: **triglyceride lowering = Strong** (dose-dependent, ~2–4 g/day EPA+DHA); **broad "brain & mood / cognition" (consumer) = Weak**; **cardiovascular-events = contested → deferred, NOT tiered** (REDUCE-IT vs STRENGTH). Dose axis = **active EPA+DHA mg**, never total fish-oil mass (§2.2 trap, symmetric to the minerals' elemental trap). Form ladder: TG/rTG (preferred) > ethyl ester (acceptable). Honesty trap: "1,000 mg fish oil" front label hides ~120–300 mg active. |
| dimension | Evidence Strength (§2.1, **lead**), Dose Adequacy (§2.2, active-fraction basis), Form (§2.3, TG/rTG vs EE), Formulation Honesty (§2.4, misleading-mass), Safety (§2.5 UL) |
| evidence_tier | TG-lowering: **Strong** (RATIFIED); broad brain/mood: **Weak** (RATIFIED, broad-consumer scope ONLY); CV-events: **contested — NOT TIERED (deferred)**, RATIFIED under Hard Rule 7 |
| **conflation firewall (D6)** | The broad brain/mood **Weak** tier is FENCED from the narrower "adjunct in diagnosed major depression" evidence (PMID:31383846, 26978738), which is **stronger but a different claim** (different population/endpoint/indication). The clinical-MDD claim is **not a tiered entry** — recorded only as a `does_not_inherit_from` pointer + `clinical_depression_note`, so the §2.1 claim-matcher can resolve a consumer SKU only to the broad Weak tier; there is no higher tier for it to inherit. A genuine diagnosed-MDD adjunct claim is **out of MVP scope** (clinical/diagnostic; SIE Invariant 1), not scored higher here. |
| citations | TG: 38922552, 30102092, 35717726, 41156531; broad brain/mood: 38468309, 29540267, 38281596; clinical-MDD (fenced, untiered): 31383846, 26978738; CV-contested: 32114706, 30019766, 39758310, 35739003; form: 25218856 |
| source | `literature` (per-claim RCTs/MAs; REDUCE-IT/STRENGTH for the contested CV claim); `pubchem` CID 5282847/445580 (EPA/DHA + ester-form identity); `dsld` (EPA/DHA-vs-total-mass prevalence) |
| should_affect_score_now | false |
| risk_of_misuse | tiering the contested CV claim instead of deferring; comparing total fish-oil mass instead of active EPA+DHA; treating EE as equivalent to TG/rTG; **leaking the clinical-depression evidence into the broad consumer brain/mood claim** |
| **governing UL (D7)** | **EFSA 5 g/day no-concern GOVERNS the veto; FDA ~3 g/day = a Safety NOTE band, not a veto.** Principled divergence from the magnesium pick: only EFSA's is a *tolerance threshold*; FDA's is GRAS/labeling guidance. Meta-rule across all discrepant sets: **the veto sits at the most-credible TOLERANCE/HAZARD threshold** (Mg: both are GI-tolerance ULs → lower governs; omega-3: only EFSA is a tolerance ceiling → it governs, FDA becomes a note). |
| verify_flag | NEEDS-ENV-VERIFY: EFSA 5 g no-concern opinion; FDA 3 g guidance; the 2–4 g/day TG effective dose; TG/rTG-vs-EE bioavailability magnitude |
| d7_status | **D6/D7 CO-SIGNED (candidate, not score-affecting)** — Nutrition 2026-06-03; highest-drift active (semi-annual sweep) |

```yaml
study_objects:
  - claim: "EPA+DHA supplementation at 2–4 g/day reduces fasting triglycerides by approximately 15–30%"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: A
    source_doi: "10.1161/CIRCULATIONAHA.118.033015"
    notes: "PMID:30102092 — systematic review of 17 RCTs. Dose-dependent effect well established. Population skewed toward hypertriglyceridemic adults (population_direct: false for general consumers; in normo-TG adults the effect is present but smaller). Dose 2–4 g active EPA+DHA matches prescription omega-3 products and upper end of OTC labeling."
  - claim: "Omega-3 (EPA+DHA) supplementation improves broad consumer outcomes related to brain health, mood, or cognition"
    dose_realistic: true
    population_direct: true
    rob_grade: moderate
    evidence_tier: C
    source_doi: "10.1001/jamanetworkopen.2024.3806"
    notes: "PMID:38468309 — large meta-analysis of RCTs on depression/mood in non-clinical populations. Small and inconsistent effects across endpoints. This study supports the Weak tier for the broad consumer brain/mood claim. The fenced clinical-MDD evidence (PMID:31383846) is deliberately NOT used here — different population, different claim."
  - claim: "EPA-enriched omega-3 at high dose reduces major cardiovascular events in statin-treated patients"
    dose_realistic: false
    population_direct: false
    rob_grade: moderate
    evidence_tier: B
    source_doi: "10.1056/NEJMoa1812792"
    notes: "REDUCE-IT trial (Bhatt et al. 2018) — 4 g/day icosapentaenoic acid ethyl ester in statin-treated hypertriglyceridemic patients. dose_realistic: false (4 g/day is at or beyond real consumer OTC serving). population_direct: false (statin-treated, hypertriglyceridemic). The contested finding: STRENGTH trial (PMID:32114706) at same dose found no benefit, raising concerns about REDUCE-IT mineral oil placebo arm artifact. This study is recorded to document the contested signal — it does NOT contribute to the consumer tier. Contested CV claim is deferred per Hard Rule 7."
```

## SUPP-EV-006 — Claim-resolution rule (v1.3) + magnesium structure/function umbrella

> **Note:** SUPP-EV-006 is a **rule** entry (the claim-resolution mechanism) plus the **magnesium umbrella mappings** that exercise it. It is the first SIE entry that **moves a real grade** (magnesium PoC E/34 → expected B/A), so it carries the heaviest governance: **Product D7 co-sign is REQUIRED before it can ship** (not yet granted).

| Field | Value |
|---|---|
| concept | **Claim-resolution rule (methodology v1.3, §2.1):** a vague structure/function claim resolves to the active's studied endpoint(s) via the pre-authored, cited `structure_function_umbrella` (§5); Evidence scores the **best plausibly-mapped tier**; the cap-1 Insufficient ceiling fires **only when no endpoint plausibly maps.** "Plausibly maps" = **moderate posture**: a recognized physiological correlate of the claim term, pre-authored + cited (narrower than any-loosely-related, wider than exact-endpoint-verbatim). Over-specific over-promise ("clinically proven", "cures", named disease) → §2.4 Honesty claim-gap + resolves to the *real* (often Weak) tier (resolution is not a loophole). **Magnesium umbrella authored this task:** heart→blood-pressure=**Moderate** (maps, best — reuses SUPP-EV-002 BP tier); bone→BMD=**Weak** (observational SR/MA, no RCT/fracture benefit); muscle→sarcopenia/strength=**Weak** (observational SR; interventional cramp evidence NULL per Cochrane); nerve→**does NOT map** (deficiency/disease-state findings only; no recognized cited correlate for a generic supplementation benefit in replete adults). |
| dimension | Evidence Strength (§2.1, claim-resolution mechanism); interacts with Formulation Honesty (§2.4, over-promise catch) and §3 cap-1 (Insufficient ceiling now conditional on "nothing maps") |
| evidence_tier | rule = N/A (mechanism). Magnesium mappings: heart/BP **Moderate** (RATIFIED, SUPP-EV-002); bone/BMD **Weak** (NEW, this task); muscle/sarcopenia **Weak** (NEW, this task); nerve **does-not-map** (NEW non-mapping decision, this task) |
| citations | bone (Weak): PMID:34666201, 26556742, 19488681 (SR/MA on BMD — observational; surrogate-only RCT). muscle (Weak): PMID:37355247, 28711425, 32956536 (sarcopenia SRs observational; Cochrane cramp-null). nerve (non-mapping basis): PMID:33166742, 11008927, 2157640, 34444861 (deficiency/disease only — cited to *justify the refusal to map*). heart/BP reuses SUPP-EV-002: PMID:27402922, 41000008, 39519450 |
| source | `literature` (PubMed SR/MA pull, this task — Nutrition tiered, client never tiers); reuses `pubchem`/`dsld` already in SUPP-EV-002. Engine reads the in-house dossier umbrella, never a live literature call (firewall). |
| should_affect_score_now | **false** — moves a grade, so it ships ONLY after Product D7 co-sign + Data engine implementation + golden-corpus validation |
| risk_of_misuse | (1) **loophole risk** — resolution must NOT let a snake-oil active inherit a tier; guarded by the moderate-posture "recognized + cited" boundary + the §13.4 R2 fixture (all-null umbrella → still E). (2) **over-read risk** — mapping "bone"/"muscle" to Moderate would over-tier an observational-only signal; held at **Weak** deliberately. (3) **non-mapping must be explicit** — "nerve" is recorded with `resolves_to: null` + a cited justification, not silently dropped. (4) free-association / live inference forbidden — engine does an exact umbrella key-lookup only. |
| verify_flag | NEEDS-ENV-VERIFY: the new bone/muscle endpoint citations were captured via the `literature` client this task; primary full-text screen + GRADE confirmation pending (consistent with the registry's tier-vs-datum split). The Weak tiers are the **authoring judgement**; the underlying primary numbers are candidate. |
| d7_status | **D6-AUTHORED (Nutrition, 2026-06-03); Product D7 co-sign PENDING.** Moderate posture owner-approved; approach ruled by Product (TASK-171E). This is the gating co-sign — until Product co-signs, the rule does NOT ship and the magnesium PoC stays E/34. |

---

# Phase-1 widen (TASK-171H) — SUPP-EV-007…016 — 10 coverage actives

> **Scope of these entries.** The 10 widen actives (vitamin C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vitamin E, CoQ10) are **reference data** built to widen shelf coverage from ~15–25% to ~40–55% (per `market_coverage_analysis_v1`). **Governance:** these are a **Nutrition D6 self-sign** reference build; **Product D7 rides the methodology co-sign** for the reference build (registry convention) — a **per-number Product gate applies only if/when a specific value moves a published score** (none ship now). **All `should_affect_score_now: false`.** Every tier/UL/form leans on `literature`/`pubchem`/NIH-ODS/EFSA with a citation; `NEEDS-ENV-VERIFY` retained on primary UL/safety numbers (co-sign is on the tier/authority *choice*, not the raw datum). **All citations were verified topically against the live `literature` (PubMed) client this task** — a first-pass authoring set contained mismatched PMIDs which were detected by `pubmed_fetch` title-check and corrected; the shipped citations resolve to the intended papers.

## SUPP-EV-007 — Vitamin C: claim-specific tiers; reversible-GI UL (note); immune-support umbrella
| Field | Value |
|---|---|
| concept | Vitamin C claim tiers: **scurvy/repletion = Strong**; **common-cold DURATION (regular supplementation) = Moderate** (Cochrane: no *prevention* in general population, small duration effect); **broad 'immune support' = Weak**. UL 2,000 mg = **reversible GI tolerance (osmotic diarrhea)** → **Safety NOTE, NOT a veto** (§2.5 veto-vs-note, like Mg's EFSA 250). Form largely non-discriminating (liposomal-superiority thin). |
| dimension | Evidence (§2.1), Safety (§2.5 note), Form (§2.3 flat) |
| evidence_tier | scurvy **Strong**; cold-duration **Moderate**; broad immune **Weak** (all RATIFIED D6) |
| citations | scurvy: 37795755, 29099763; cold-duration: 23440782 (Cochrane), 36415746; immune role: 29099763 |
| structure_function_umbrella | immune support→cold-duration **Moderate (best)**; antioxidant→Weak; skin→Weak (collagen-cofactor route); energy→**null** (no recognized correlate) |
| should_affect_score_now | false |
| governing UL (D6) | 2,000 mg = reversible-GI **NOTE** band (no toxicity veto in healthy adults). NEEDS-ENV-VERIFY. |
| risk_of_misuse | letting 'prevents colds/boosts immunity' inherit Moderate (it's a §2.4 over-promise → Honesty debit); vetoing a reversible GI threshold |
| d7_status | **D6 self-sign (candidate, not score-affecting)** — Nutrition 2026-06-03; Product per-number gate if a value moves a score |

## SUPP-EV-008 — Zinc: form ladder (oxide paradox) + elemental trap; claim tiers; TOXICITY UL (discrepant)
| Field | Value |
|---|---|
| concept | Zinc mirrors magnesium: oxide **high elemental (0.803) / low absorbed** (oxide paradox) vs picolinate/citrate/gluconate. Claim tiers: **repletion = Strong**; **acute-cold-duration (lozenge, <24h) = Moderate**; **broad daily-immune = Weak**. UL is a **genuine TOXICITY ceiling (copper antagonism) → HARD VETO** (unlike vitamin C/Mg reversible-GI). |
| dimension | Form (§2.3 lead-style), Dose elemental (§2.2), Evidence (§2.1), Safety (§2.5 veto) |
| evidence_tier | repletion **Strong**; acute-cold **Moderate**; broad immune **Weak** (RATIFIED D6) |
| citations | repletion: 38367035, 29186856; acute-cold: 23775705 (Cochrane), 28515951; bioavailability: 16372518; immune: 29186856 |
| structure_function_umbrella | immune support→acute-cold **Moderate (best)**; skin→Weak; antioxidant→**null** (SOD mechanism-only) |
| should_affect_score_now | false |
| governing UL (D6) | **DISCREPANT** NIH/IOM 40 vs EFSA 25 (both copper-antagonism toxicity). Proposed: **hard veto at 40** + **Safety NOTE band 25–40** (graded, like Mg). MOVES behavior → Product co-sign if it scores. NEEDS-ENV-VERIFY both. |
| risk_of_misuse | conflating elemental with absorbed; double-charging oxide (Form+Honesty coordinate, §3); mapping daily-capsule 'immunity' to the lozenge Moderate without Honesty policing |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03; Product per-number gate (discrepant UL) |

## SUPP-EV-009 — Iron: NECESSITY-context-only (Invariant 1); TOXICITY veto; elemental trap
| Field | Value |
|---|---|
| concept | Iron is the **necessity/contraindication-nuance** active. **CRITICAL: necessity (who needs iron) is reader CONTEXT ONLY, NEVER scored (SIE Invariant 1).** Claim tiers (population-conditional, conditionality = context not score): **anaemia-correction = Strong**; **fatigue in iron-deficient (incl. non-anaemic) = Moderate**. UL 45 mg = **genuine TOXICITY veto** (overload + **acute pediatric poisoning**, leading cause of fatal childhood supplement poisoning). Elemental-vs-compound trap + **hydrate-state** caveat on ferrous sulfate. |
| dimension | Evidence (§2.1), Safety (§2.5 veto), Dose elemental (§2.2), Form (§2.3 ferrous>ferric, bisglycinate tolerability) |
| evidence_tier | anaemia-correction **Strong**; fatigue **Moderate** (RATIFIED D6) |
| citations | anaemia: 23252877, 26314490; fatigue (non-anaemic ID women): 12763985 (Verdon BMJ), 41736325 |
| structure_function_umbrella | blood→anaemia-correction **Strong (best)**; energy→fatigue **Moderate** (iron 'energy' genuinely maps — unlike hand-wave actives); immune→**null** (deficiency-only) |
| should_affect_score_now | false |
| governing UL (D6) | 45 mg elemental = **TOXICITY veto** (not reversible-GI). NEEDS-ENV-VERIFY; verify ferrous-sulfate hydrate state for elemental fraction. |
| risk_of_misuse | **scoring necessity** (forbidden, Invariant 1); comparing compound mass not elemental; missing hydrate-state |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-010 — Calcium: conditional bone tier (with vit D); total-intake UL; citrate>carbonate-in-low-acid
| Field | Value |
|---|---|
| concept | Calcium claim tiers: **mineralization/repletion = Strong**; **fracture reduction = Moderate** (conditional — **with vitamin D, in older/deficient**, limited in replete community adults; debated CV signal). Structurally mirrors vitamin D3 bone-Moderate. UL 2,500 mg is on **TOTAL intake** (engine sees supplement only → veto rare, NOTE >1,500 mg supplemental). Form: citrate (acid-independent) > carbonate (needs food/acid) — carbonate **acceptable not poor**. |
| dimension | Evidence (§2.1), Safety (§2.5 note/total-intake caveat), Dose elemental (§2.2), Form (§2.3) |
| evidence_tier | mineralization **Strong**; fracture **Moderate** conditional (RATIFIED D6) |
| citations | fracture: 29279934, 26510847; BMD/intake: 26420598; bioavailability citrate-vs-carbonate: 11329115 |
| structure_function_umbrella | bone health→fracture **Moderate (maps)**; teeth→mineralization **Strong (best)**; muscle→**null** (contraction mechanism-only) |
| should_affect_score_now | false |
| governing UL (D6) | 2,500 mg **total**-intake toxicity ceiling; engine sees supplement → veto rare, NOTE >1,500 mg supplemental (like Mg supplement-only caveat). Age-banded (2,000 for 51+). NEEDS-ENV-VERIFY. |
| risk_of_misuse | vetoing on total intake the engine cannot see; over-tiering bone to Strong (it's conditional Moderate) |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-011 — Folic acid: Strong narrow NTD claim; B12-masking UL (graded + clinical carve-out); vitamer form
| Field | Value |
|---|---|
| concept | Folic acid claim tiers: **periconceptional NTD prevention = Strong** (MRC RCT + Cochrane — among the strongest in supplementation); **folate-status correction = Strong**; **broad CV/cognitive (homocysteine halo) = Weak** (surrogate moves, outcomes don't). UL 1,000 mcg synthetic = **B12-masking** (graded NOTE→veto at multiples; **clinical_use carve-out** for high-risk-pregnancy 4–5 mg). Form: folic acid (NTD-evidence form) / 5-MTHF (MTHFR-variant, dose-adjusted DFE). |
| dimension | Evidence (§2.1), Safety (§2.5 B12-masking), Form (§2.3 vitamer) |
| evidence_tier | NTD **Strong**; status **Strong**; broad CV/cognitive **Weak** (RATIFIED D6) |
| citations | NTD: 26662928 (Cochrane), 1677062 (MRC trial); homocysteine/CV: 22695899; stroke-subgroup: 28404799 |
| structure_function_umbrella | pregnancy→NTD **Strong (best)**; blood→megaloblastic **Strong**; heart→homocysteine **Weak**; energy→**null** |
| should_affect_score_now | false |
| governing UL (D6) | 1,000 mcg synthetic = B12-masking graded NOTE; **clinical_use carve-out** (4–5 mg high-risk pregnancy, like D3 weekly). Food folate uncapped. NEEDS-ENV-VERIFY. |
| risk_of_misuse | letting status-Strong inherit onto CV/cognitive; missing the B12-masking pairing context (never scored, surfaced) |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-012 — B12: NO UL (clean Safety); 'nerve' MAPS Strong (per-active boundary vs Mg-nerve=null)
| Field | Value |
|---|---|
| concept | B12 claim tiers: **repletion = Strong**; **broad 'energy/reduces tiredness' = Weak** (EFSA recognizes the role, deficiency-anchored — so 'energy' genuinely maps, unlike hand-wave actives, but consumer benefit in replete adults is thin); **broad cognitive/CV = Weak** (homocysteine halo). **NO established UL** → Safety neutral (clean no-UL active like creatine). **Key per-active boundary: 'nerve' MAPS Strong for B12** (recognized studied neuro endpoint — neuropathy/SCD correction) **where it did NOT map for magnesium** (deficiency/disease-only) — proves the umbrella boundary is per-active, as designed. |
| dimension | Evidence (§2.1), Safety (§2.5 no-UL), Form (§2.3 cyano/methyl) |
| evidence_tier | repletion **Strong**; energy **Weak**; cognitive/CV **Weak** (RATIFIED D6) |
| citations | repletion/review: 28925645, 38231320; cognition/homocysteine: 23765945, 34432056 |
| structure_function_umbrella | blood→repletion **Strong (best)**; **nerve→repletion Strong (MAPS — contrast Mg nerve=null)**; energy→Weak; mood→Weak |
| should_affect_score_now | false |
| governing UL (D6) | **no UL** — Safety neutral; high mcg labels are normal (low passive absorption), NOT over-dosing. NEEDS-ENV-VERIFY no-UL statement. |
| risk_of_misuse | flagging normal high-mcg labels as over-dose; methylcobalamin-superiority premium claim without evidence (Honesty watch) |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-013 — Melatonin: OVER-DOSE-AS-NORM probe ('more is worse'); regulatory-status flag
| Field | Value |
|---|---|
| concept | Melatonin is the **over-dose-as-norm** probe: effective **0.5–1 mg**, market norm **5–10 mg** = NOT more effective + more next-day grogginess. Claim tiers: **sleep-onset latency = Moderate**; **jet lag = Moderate** (Cochrane). **No toxicity UL** → a dose >5 mg earns **no Dose bonus + a Safety NOTE** (grogginess, precautionary long-term/pediatric), NOT a veto (§2.2 'more is not better' + §2.5 no-UL). **Coverage caveat: ~0 IL open-shelf SKUs** (pharmacist-counter/Rx-adjacent) — high-value engine probe, low IL shelf coverage. |
| dimension | Dose (§2.2 over-dose-no-bonus), Evidence (§2.1), Safety (§2.5 note + regulatory-status flag) |
| evidence_tier | sleep-onset **Moderate**; jet lag **Moderate** (RATIFIED D6) |
| citations | sleep-onset: 23691095, 33417003; jet lag: 12076414 (Cochrane) |
| structure_function_umbrella | sleep→onset-latency **Moderate (best)**; relaxation→onset **Moderate**; immune→**null** (mechanism/experimental only) |
| should_affect_score_now | false |
| governing UL (D6) | no toxicity UL; **NOTE >5 mg** (no benefit + grogginess). Regulatory-status varies (IL pharmacist-counter; Rx in EU/UK) — legitimacy/context flag, not scored. NEEDS-ENV-VERIFY. |
| risk_of_misuse | reading 10 mg as 'high potency' virtue; treating grogginess as toxicity veto |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-014 — Biotin: the DEFICIENCY-ONLY REFUSAL — proves resolution is a FLOOR, not a loophole
| Field | Value |
|---|---|
| concept | Biotin is the **loophole-proof** case: claim tiers **deficiency-correction = Strong** (rare); **hair/skin/nails in REPLETE adults = Insufficient** (benefit is deficiency-CONFINED per SR 28879195 — yet it is the dominant market claim). **Every cosmetic umbrella phrase resolves to NULL** → §3 cap-1 Insufficient FIRES + §2.2 Dose short-circuits to N/A → a cosmetic biotin scores **E**. Real safety vector: high-dose biotin causes **lab-assay interference** (false troponin/thyroid — FDA communication) → Safety NOTE. |
| dimension | Evidence (§2.1 + cap-1), Dose (§2.2 short-circuit), Safety (§2.5 assay-interference NOTE) |
| evidence_tier | deficiency-correction **Strong**; cosmetic-in-replete **Insufficient** (RATIFIED D6) |
| citations | deficiency/role: 28701385, 22116691; hair/nails SR (benefit deficiency-confined): 28879195 |
| structure_function_umbrella | **hair→null, skin→null, nails→null, energy→null — NOTHING MAPS** (cap-1 Insufficient correctly fires). Citations on the refusals justify the deficiency-confinement. |
| should_affect_score_now | false |
| governing UL (D6) | no toxicity UL; **lab-assay-interference Safety NOTE** at high dose (FDA). NEEDS-ENV-VERIFY FDA communication. |
| risk_of_misuse | **the central loophole risk** — must NOT let the cosmetic claim inherit the Strong deficiency tier; the all-null umbrella is the guardrail (with the snake-oil fixture, the proof resolution is fair not loophole) |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-015 — Vitamin E: antioxidant halo that FAILED in RCTs — Evidence AND Safety both bite
| Field | Value |
|---|---|
| concept | Vitamin E is the **'antioxidant supplement can HARM'** case: claim tiers **deficiency-correction = Strong**; **broad antioxidant/CV-prevention = Weak** (HOPE-TOO null + Miller high-dose all-cause-mortality signal); **cancer prevention = Insufficient** (SELECT showed **increased prostate cancer**). UL 1,000 mg = **HAEMORRHAGE toxicity veto**; separately **>=400 IU (268 mg) = all-cause-mortality Safety NOTE below the UL**. Form: natural d- (RRR) > synthetic dl- (all-rac, ~half bioavailability + IU/mg + natural/synthetic traps). |
| dimension | Evidence (§2.1), Safety (§2.5 veto + sub-UL NOTE), Form (§2.3 natural>synthetic), Dose (§2.2 'more is worse') |
| evidence_tier | deficiency **Strong**; antioxidant/CV **Weak**; cancer-prevention **Insufficient** (RATIFIED D6) |
| citations | deficiency: 35929460; CV-null/mortality: 15769967 (HOPE-TOO), 15537682 (Miller MA); cancer harm: 21990298 (SELECT), 36615673 |
| structure_function_umbrella | antioxidant→Weak **(best, role recognized / benefit failed)**; heart→Weak; skin→**null** (oral≠topical); immune→**null** |
| should_affect_score_now | false |
| governing UL (D6) | **1,000 mg = haemorrhage toxicity VETO**; **>=400 IU/268 mg = mortality/cancer Safety NOTE** below the UL. NEEDS-ENV-VERIFY both. |
| risk_of_misuse | letting deficiency-Strong inherit onto the failed antioxidant claim; missing that high-dose is a *harm*, not a virtue |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03 |

## SUPP-EV-016 — CoQ10: clinical-vs-consumer CONFLATION FIREWALL (mirrors omega-3 clinical-MDD)
| Field | Value |
|---|---|
| concept | CoQ10 claim tiers: **heart-failure adjunct = Moderate but CLINICAL** (Q-SYMBIO + Cochrane — diagnosed disease, **FENCED out of consumer scope** like omega-3 clinical-MDD); **statin-myopathy = Weak (borderline-contested — watch for re-classify)**; **broad consumer energy/heart = Weak**. **A consumer 'heart' CoQ10 resolves to the broad Weak tier, NOT the clinical HF Moderate** (conflation firewall: the clinical endpoint carries `claim_scope: clinical` and is an unreachable umbrella target). NO UL (clean Safety). Form: ubiquinone (studied) / ubiquinol (contested-superiority) / solubilization matters. |
| dimension | Evidence (§2.1 + clinical-scope fence), Form (§2.3), Dose (§2.2 sub-therapeutic low-dose multis), Safety (§2.5 no-UL) |
| evidence_tier | HF-adjunct **Moderate (clinical, fenced)**; statin-myopathy **Weak (borderline-contested)**; broad consumer **Weak** (RATIFIED D6) |
| citations | HF: 25282031 (Q-SYMBIO), 35608922 (Cochrane); statin-myopathy: 30371340, 25440725 (conflicting MAs) |
| structure_function_umbrella | heart health→**broad-consumer Weak (FENCED from clinical Moderate)**; energy→Weak; anti-aging→**null** |
| should_affect_score_now | false |
| conflation firewall (D6) | the clinical HF Moderate is recorded but **unreachable from a consumer claim** — only the consumer Weak tier is umbrella-mappable (mirrors omega-3 SUPP-EV-005 clinical-MDD fence exactly). |
| governing UL (D6) | **no UL** — Safety clean. Warfarin-interaction context (not scored). NEEDS-ENV-VERIFY. |
| risk_of_misuse | leaking the clinical HF Moderate into a consumer 'heart' claim; tiering statin-myopathy harder than Weak before the conflict resolves |
| d7_status | **D6 self-sign (candidate)** — Nutrition 2026-06-03; statin-myopathy = **semi-annual sweep** (borderline-contested) |

---

## Deferred-to-hard-gate notes (TASK-171H) — NOT dossiers

These are the two **highest-coverage** next actives (`market_coverage_analysis_v1` rank 1–2) — **deliberately NOT built**, because each breaks the `(active, dose, form, evidence)` scoring unit the engine assumes. Recorded as deferred, not authored.

- **Multivitamin / multi-ingredient blends (rank 1, ~4.6% named + 10–20% blend-adjusted; demand 74.5).** DEFERRED — needs **per-active dose attribution** across 20+ actives sharing one serving; the engine cannot answer "is the dose adequate" for a blend it cannot itemize. This is the §7 out-of-scope "blend-level dose attribution" machinery. Building 20 single-active umbrellas does **not** produce a multivitamin score.
- **Probiotics (rank 2, ~4.6%; demand 74.7).** DEFERRED — needs **CFU viability at end-of-shelf-life + strain-specificity** (a live-organism count over time, not a `(dose, form)` tuple); neither is on the label nor in any client, and evidence is strain-by-strain not "probiotics." §7 out-of-scope "CFU/probiotic viability" machinery.

**Borderline picks flagged (built, with the nuance recorded):** **iron** = necessity/contraindication nuance — built; necessity is **reader-context only, never scored** (SIE Invariant 1, SUPP-EV-009). **B-complex** = a mini-blend (multi-active dose attribution) — **NOT built as a dossier** for the same reason as multivitamin; the single B-vitamins (B12, folic acid) are built individually instead. **CoQ10** carries a borderline-contested statin claim — built at Weak with a re-classify watch (SUPP-EV-016).

---

## Deferred Phase-2 note — ashwagandha / standardized botanicals (NOT a live `SUPP-EV`)

Preserved so the KSM-66 insight is not lost (it vacated SUPP-EV-005 in the v1.1 probe swap): *stress/anxiety evidence is on **standardized extracts** (e.g. KSM-66 ~300–600 mg) and does **NOT** transfer to unstandardized raw root or unstudied doses; over-tiering a small/heterogeneous trial base is a real risk.* This belongs to the **Phase-2 botanical/standardization subsystem** because its central difficulty (contested botanical evidence + extract standardization) is exactly the **contested-evidence machinery the MVP defers** (§7). It gets its own `SUPP-EV-###` only when the Phase-2 botanical subsystem is authorized. **Status: deferred note, not a live entry, not co-signed for scoring.**

---

# Hebrew + EFSA Art.13 claim-vocab expansion (TASK-171K) — addendum to SUPP-EV-001…016

> **Why.** The real Israeli corpus run (TASK-171J, `_corpus_report_v2.md`) found the `structure_function_umbrella` claim maps were authored against English/expected phrasing and **missed the actual Hebrew structure/function claims on Israeli labels** — so honest products scored E unfairly (canonical case: a magnesium scored E because its label said **"עייפות/fatigue"**, which did not map, even though **magnesium → "reduction of tiredness and fatigue" is an EFSA Article 13 AUTHORIZED claim**). This addendum records the Hebrew + EFSA-anchored vocab expansion. **Authoring only — no engine/methodology edit, no new tiers; every new key is a CITED POINTER to an endpoint already tiered in its dossier.** All `verification_status: candidate` / `should_affect_score_now: false`.

**Anchoring authority.** New mappings are anchored on the **EFSA Article 13 authorized health-claims register (Reg (EU) 432/2012)** — the authoritative permitted structure/function vocabulary EU/IL labels may use — and/or a `literature` PMID already in the dossier. An uncited mapping hard-fails the loader (`DossierError`), so every MAPPING key carries citations; every NON-MAPPING key is a documented `resolves_to: null` refusal.

**What changed, per active (all candidate):**

| Active | New Hebrew/EFSA MAPPING keys | New cited NON-MAPPING (null) | EFSA Art.13 anchor |
|---|---|---|---|
| **magnesium** | עייפות/fatigue/תשישות→BP **Moderate** (THE corpus fix); שרירים/תפקוד שרירים→sarcopenia Weak; בריאות העצם/עצמות→BMD Weak; לב→BP Moderate | מערכת העצבים→null (mirrors English nerve-null) | Q-2010-00807 (tiredness/fatigue), Q-2010-00790 (muscle/bones/nervous-system) |
| **vitamin C** | חיזוק חיסוני/מערכת החיסון→cold-duration Moderate; נוגד חמצון→Weak; עור→Weak; **ספיגת ברזל→Weak** (iron-absorption is a HEALTH claim, maps); **עייפות→Weak** (EFSA fatigue maps; vague 'energy' stays null) | — | Q-2009-00226 (immune), Q-2009-00230 (oxidative-stress/collagen-skin), Q-2008-1325 (iron absorption), Q-2009-00231 (fatigue) |
| **zinc** | חיזוק חיסוני/מערכת החיסון→acute-cold Moderate; עור→Weak; **שיער→Weak** (EFSA hair — maps, CONTRAST biotin) | — | Q-2008-1322 (immune/skin/hair/nails) |
| **iron** | עייפות/תשישות→fatigue Moderate; דם→anaemia Strong | — | Q-2008-1215 (red-cell/haemoglobin, tiredness/fatigue) |
| **calcium** | בריאות העצם/עצמות→fracture Moderate; שיניים→mineralization Strong | — | Q-2008-1180 (normal bones/teeth) |
| **folic acid** | הריון→NTD Strong; דם→megaloblastic Strong; **עייפות→Weak** (EFSA fatigue maps; vague 'energy' null) | — | Q-2008-1213 (maternal tissue growth, blood formation, tiredness/fatigue) |
| **B12** | עייפות/אנרגיה→energy Weak; **מערכת העצבים→repletion Strong** (CONTRAST Mg nerve=null, per-active boundary); דם→repletion Strong | — | Q-2008-1304 (red-cell, nervous-system, energy metabolism, tiredness/fatigue) |
| **melatonin** | שינה/הירדמות→sleep-onset Moderate; ג'ט לג→sleep-onset Moderate | — | Q-2011-00531 (time to fall asleep), Q-2011-00829 (jet lag) |
| **biotin** | — | **שיער/עור/ציפורניים→null (ALL, BY DESIGN)** — preserves the loophole-proof cap-1 FLOOR (cosmetic biotin → E) | EFSA biotin skin/hair claim EXISTS but dossier D6 holds replete-adult cosmetic benefit Insufficient — **not re-adjudicated** (flagged) |
| **vitamin E** | נוגד חמצון→Weak (role recognized, benefit failed) | עור→null (oral≠topical) | Q-2008-1136 (oxidative-stress) |
| **CoQ10** | בריאות הלב/לב→broad-consumer Weak (FENCED from clinical HF Moderate); אנרגיה→Weak | — | **none — CoQ10 has NO authorized EFSA claim**; aliases on the dossier's own cited base (35608922) |
| **vitamin D3** | (umbrella **AUTHORED** — none existed) immune/חיזוק חיסוני/מערכת החיסון→broad-prevention Weak; bone/בריאות העצם/עצמות/שיניים/שרירים→fracture Moderate | mood→null | Q-2008-1192 (immune, bones, teeth, muscle) |
| **creatine** | (umbrella **AUTHORED**) מסת שריר/כוח/בניית שריר→resistance-training **Strong** (the genuine studied endpoint) | שריפת שומן→null (the Insufficient fat-loss FAIL anchor — must not inherit); אנרגיה→null | none (EFSA rejected creatine claims); the dossier's own Strong literature |
| **omega-3** | (umbrella **AUTHORED**) בריאות הלב/לב→broad-consumer Weak (**anti-loophole: NOT TG=Strong**); מוח/זיכרון/מצב רוח→broad cognition Weak (FENCED from clinical-MDD) | — | Q-2008-1252 (normal heart function, 250 mg), Q-2008-1207 (DHA brain function) |
| **caffeine** | (umbrella **DELIBERATELY NOT authored**) — axis is Honesty; NO EFSA caffeine claim; vague 'energy/focus'→tier would be a loophole | — (no umbrella; studied claims via §2.1 explicit-claim matcher) | none (EFSA did not adopt the 2011 caffeine opinions) |

**Verification (this task):**
- `dossier_loader.load_all()` → **clean, all 16 dossiers load** (every MAPPING key is cited; uncited would `DossierError`).
- `run_golden_validation.py` → **17/17 PASS, no regression** (existing English fixtures, R1/R2/R3 claim-resolution fixtures, inverted-E pair all unchanged).
- **Magnesium fatigue fix verified end-to-end:** `resolve_claim_tier(magnesium, "עייפות")` → **Moderate** (resolved via the EFSA fatigue key to the BP endpoint), `"עייפות ותשישות"` → Moderate, English `"fatigue"` → Moderate.

> **⚠️ BLOCKER surfaced (engine, NOT dossier — out of this task's "no-code" scope).** The dossier keys are necessary but **NOT sufficient** to make Hebrew labels resolve in the live engine. `score_engine._PUNCT = re.compile(r"[^a-z0-9]+")` strips **every non-ASCII character**, so a Hebrew label claim tokenizes to **∅** before the umbrella lookup — `resolve_claim_tier(magnesium, "עייפות")` on the **unmodified** engine returns **Insufficient** (the magnesium still scores E). The Hebrew keys go live only with a **one-line tokenizer fix** to preserve the Hebrew Unicode block (e.g. `r"[^a-z0-9֐-׿]+"`), verified in-memory this task (with it, `עייפות`→Moderate). This is a **Data engine change** (its own D7/governance), recorded here as the gating dependency for the Hebrew vocab to take effect. EFSA-anchored **English** keys (fatigue, immune support, antioxidant…) already resolve on the current engine.

> **EFSA-divergence items flagged for a future sweep (NOT re-adjudicated here — Hebrew-vocab task only):** magnesium 'nerve/מערכת העצבים', zinc 'antioxidant', calcium 'muscle', and (most consequentially) **biotin 'hair/skin/nails'** — each has an EFSA Art.13 structure/function relationship but a prior ratified D6 `null`/Insufficient decision. TASK-171K keeps the existing decision (mirrors the English key) to avoid silently moving a score; any change needs full D6/D7.

---

# Phase-2 Banked Amendments (TASK-195, 2026-06-06) — SUPP-EV-017…019

> **Scope.** These three entries are banked amendments to the SIE methodology while TASK-171 is closed. The SIE is a proven asset; these entries update the methodology for revival, not for any current scoring run. All `should_affect_score_now: false`. No engine code was touched; no corpus was touched; no score was changed. Source: "Clinical and Pharmacological Assessment of Dietary Supplementation" (New Batch, 2026-06-06). These entries are Nutrition self-signed (no per-number Product D7 required for pre-launch banked methodology within the lane, per TASK-195 governance — `roadmap_impact: false`). Product per-number gate applies on any value that moves a published score on revival.

## SUPP-EV-017 — Speciation tier: graded Form scoring for Mg, folate, B12 (Amendment A)

| Field | Value |
|---|---|
| concept | **Mineral and vitamin speciation produces ≥2× absorption differentials that are label-observable and must be scored on a graded (not binary) scale within the Form dimension (§2.3).** Three actives covered: (1) **Magnesium:** oxide ~4% fractional absorption (insoluble); citrate ~25–30% (post-load urinary Mg excretion 0.22 vs 0.006 mg/mg creatinine for oxide at 4h, p<0.05); glycinate/bisglycinate ~31% (active amino-acid transport, low osmotic-laxation). Magnesium L-threonate crosses the BBB — preferred-specialized for cognitive/anxiety applications. (2) **Folate:** folic acid (85–100% bioavailability) BUT requires rate-limiting hepatic DHFR conversion — DHFR saturates at ≥200–400 mcg/day causing circulating unmetabolized folic acid (UMFA); MTHFR polymorphisms (C677T/A1298C, ~10–15% population) severely impair conversion. 5-MTHF (L-methylfolate/levomefolate) bypasses DHFR and MTHFR entirely; no UMFA; does not mask B12 deficiency. Both forms are label-observable by ingredient name. (3) **B12:** cyanocobalamin (acceptable — standard crystalline form, requires renal conversion); methylcobalamin (preferred — active coenzyme, no conversion required, label-observable); adenosylcobalamin (preferred-specialized — mitochondrial coenzyme). |
| dimension | Form & Bioavailability (§2.3), graded within-tier scoring |
| evidence_tier | Mg form differential: **Moderate** (bioavailability studies; post-load urinary excretion RCT); folate speciation: **Strong/regulatory** (FNB DFE conversion factors established; DHFR bottleneck well-characterized biochemically; MTHFR clinical literature); B12 form tiers: **Moderate** (methylcobalamin superiority contested at equivalent doses — watch item; cyanocobalamin effectiveness at 1,000 mcg/day well-established for repletion) |
| citations | All from "Clinical and Pharmacological Assessment of Dietary Supplementation" (New Batch, 2026-06-06): Mg citrate vs oxide RCT (urinary-excretion data); DHFR rate-limiting characterization + MTHFR polymorphism clinical significance + DFE conversion (FNB); geriatric cobalamin repletion. `NEEDS-PRIMARY-PMID-VERIFY` — primary PMIDs pending full-text verification against research doc's cited literature |
| source | Research doc (2026-06-06); existing SUPP-EV-002 (Mg), SUPP-EV-011 (folate), SUPP-EV-012 (B12) |
| should_affect_score_now | **false** — banked amendment; activates on TASK-171 revival |
| risk_of_misuse | (1) Conflating elemental Mg content with absorbed Mg (oxide paradox — dose comparison must use elemental fraction via pubchem §2.2); (2) asserting methylcobalamin superiority as uncontested (at equivalent doses the literature is mixed — record as watch item); (3) applying 5-MTHF preference as a blanket rule without noting folic acid is the clinical NTD-prevention form in large RCTs (form-vs-indication coupling persists) |
| d7_status | **Nutrition self-sign (banked, pre-launch, roadmap_impact: false per TASK-195).** Product per-number gate applies if any value from this entry moves a published score on revival. |

## SUPP-EV-018 — EFSA Tolerable Upper Limit as named primary Safety ceiling (Amendment B)

| Field | Value |
|---|---|
| concept | **EFSA Tolerable Upper Intake Levels (TULs) are formalized as the primary named Safety ceiling reference for the SIE (§2.5).** Previously the Safety dimension referenced "tolerable upper limit" without citing the authoritative table. Amendment B names EFSA TULs — established under Directive 2002/46/EC and assessed by EFSA's Panel on Nutrition, Novel Foods and Food Allergens (NDA) — as the governing reference. Israel has no standalone equivalent TUL table. The tiered penalty structure: (1) Dose > EFSA TUL → **Safety VETO** (hard floor, grade cap E; existing behavior, now explicitly cited); (2) Dose 80–100% EFSA TUL → **Safety FLAG** (annotate only; `safety_flag: approaching_tul`; no grade cap); (3) Dose < 80% EFSA TUL → no Safety action on dose grounds. Engine constant `TUL_FLAG_FRACTION = 0.80`. Representative EFSA TULs confirmed by the research doc: Vitamin B6 12.5 mg/day (reduced from 30 by EFSA NDA due to sensory peripheral neuropathy risk); Folate/folic acid 1,000 mcg/day; Selenium 255 mcg/day; Elemental iron 40 mg/day; Manganese 8 mg/day. |
| dimension | Safety Ceiling (§2.5), all actives where EFSA TUL is established |
| evidence_tier | **Regulatory** — EFSA TUL values are mandatory systematic toxicological evaluations under EU food supplement law (Directive 2002/46/EC; Regulation EU 2015/2283). No evidence-tier uncertainty on the existence of the reference table; individual values remain `NEEDS-ENV-VERIFY` for primary EFSA opinion numbers per active. |
| citations | Research doc (2026-06-06) — EFSA regulatory framework (Directive 2002/46/EC; NDA Panel process; B6 UL reduction 30→12.5 mg/day); EFSA NDA Panel opinions primary (per active — `NEEDS-PRIMARY-PMID-VERIFY`) |
| source | Research doc (2026-06-06); existing SUPP-EV-002 through SUPP-EV-016 (per-active UL choices already recorded); EFSA Nutrient UL Tolerable Upper Intake Levels report |
| should_affect_score_now | **false** — banked amendment; activates on revival. The VETO behavior already exists; the 80% FLAG band is new behavior (pre-launch, non-score-moving while banked). |
| risk_of_misuse | (1) Treating EFSA TUL as the only ceiling without checking per-active dossier for cases where NIH/IOM governs (e.g. Mg — SUPP-EV-002 FLAG-2 ruling; omega-3 — SUPP-EV-005); per-dossier governing-UL choice supersedes this general rule. (2) Applying the 80% FLAG to reversible-tolerance thresholds already resolved to NOTE bands (FLAG is for genuine TUL proximity; reversible-vs-toxicity classification in §2.5 is upstream). (3) Confusing EFSA TUL (supplement safety ceiling) with EFSA ADI for food additives — different regulatory instruments. |
| d7_status | **Nutrition self-sign (banked, pre-launch, roadmap_impact: false per TASK-195).** The VETO behavior was already present. FLAG behavior (80–100% band) is new but non-score-moving while banked. Product per-number gate applies if FLAG is activated on a live-scored product. |

## SUPP-EV-019 — Probiotics: strain-resolved Evidence Dossiers (Amendment C — Phase 3+ scope)

| Field | Value |
|---|---|
| concept | **Probiotic efficacy is strain-specific and disease-specific; pooling strains or genera produces inaccurate clinical conclusions. The SIE must score probiotics at the individual named-strain level.** Evidence: (1) Systematic review of 228 probiotic clinical trials showed highly variable gastric-acid survival, mucosal adherence, and immunomodulatory properties among strains within the same species. (2) In screening of >127 *Lactobacillus* strains, only 3% met probiotic criteria (bile + acid resistance). (3) Clinical efficacy established only for specific named strains in targeted indications: *Saccharomyces boulardii* CNCM I-745 and the *L. acidophilus* CL1285 / *L. casei* LBC80R / *L. rhamnosus* CLR2 mixture for antibiotic-associated diarrhea prevention; *L. rhamnosus* GG and *S. boulardii* CNCM I-745 for acute pediatric gastroenteritis and recurrent *C. difficile* prevention. Other *Lactobacillus* strains showed no benefit for these same indications. **Scoring rules (Phase 3+ only):** each named strain requires its own Evidence Dossier; un-named strains or CFU-only labels → Evidence tier = Insufficient (cap-1 fires); CFU dose adequacy is unresolvable without end-of-shelf-life viability data. **Does NOT affect MVP or Phase 2 scope.** |
| dimension | Evidence Strength (§2.1, per-strain tier), Dose Adequacy (§2.2, unresolvable until viability gate), Form (§2.3, not applicable — viability is the primary form-equivalent for probiotics) |
| evidence_tier | Strain-specificity principle: **Strong** (228 clinical trials; mechanistic consensus; 3% screening pass rate). Individual strain tiers: per-dossier, Phase 3+, not authored here. |
| citations | Research doc (2026-06-06): systematic review 228 probiotic trials; >127 *Lactobacillus* strain screening (3% pass); *S. boulardii* CNCM I-745 and *L. rhamnosus* GG AAD evidence; meta-analysis 63 depression / 49 anxiety RCTs (SMD −0.53 / −0.44 — high heterogeneity, consistent with strain-pooling masking differential effects). `NEEDS-PRIMARY-PMID-VERIFY` on primary strain-specific trial PMIDs. |
| source | Research doc (2026-06-06); existing §7 deferred-to-hard-gate note (pre-v1.4) |
| should_affect_score_now | **false** — Phase 3+ scope; banked; does not affect MVP or Phase 2 |
| risk_of_misuse | (1) Reading meta-analytic SMD improvements for depression/anxiety as justification for genus-level scoring (the heterogeneity is the problem; within-study strain identity is the required discriminator). (2) Treating CFU count as a dose proxy without viability data. (3) Assuming this entry authorizes any probiotic scoring under TASK-171 or current tasks. |
| d7_status | **Nutrition self-sign (banked, pre-launch, roadmap_impact: false per TASK-195).** Phase 3+ only; no score activation possible until revival gate + separate Phase 3 authorization. |

---

## Registry status

- Entries 001–005 promoted from §8 seeds to reflect the **built + Nutrition-co-signed** dossiers (TASK-171B).
- **Entries 007–016 added (TASK-171H widen):** 10 coverage actives (vitamin C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vitamin E, CoQ10). **Nutrition D6 self-sign** reference build; Product D7 rides the methodology co-sign; per-number Product gate only if a value moves a score. **All citations verified topically against the live `literature` (PubMed) client this task.** Multivitamin + probiotics **deferred-to-hard-gate** (not dossiers). B-complex deferred (mini-blend); single B-vitamins built instead.
- **All `should_affect_score_now: false`** — Phase 1 reference data; Phase 2 calibrates; no score ships.
- **D6/D7 co-sign (Nutrition, 2026-06-03)** covers: finalized claim tiers, the 3 scrutiny rulings (omega-3 broad-brain Weak + conflation firewall; magnesium sleep Weak; vitamin D3 bone Moderate-conditional), and the governing-UL authority picks (Mg→EFSA 250; omega-3→EFSA 5 g veto / FDA 3 g note; caffeine 400/200 & vitamin D 4,000 IU confirmed concordant). `NEEDS-ENV-VERIFY` flags on primary numbers are **retained** — the co-sign is on the tier/authority *choice*, not the raw datum.
- Product D7 co-sign of the SIE methodology (v1.1) stands; per-number Product co-sign is a **Phase-2 calibration gate** before any value can move a published score.
- **Entries 017–019 added (TASK-195, 2026-06-06 — banked amendments):** speciation tier (Mg/folate/B12 form grading, §2.3), EFSA TUL named primary Safety ceiling (§2.5), probiotics strain-resolved dossier rules (§7, Phase 3+). Nutrition self-sign; `roadmap_impact: false`; `should_affect_score_now: false` on all. No engine code, no corpus, no score touched.
- **TASK-171K (2026-06-03):** Hebrew + EFSA Art.13 claim-vocab expansion across SUPP-EV-001…016 (addendum above). Dossier-authoring only (no engine/methodology edit); cited pointers to existing tiers; all `should_affect_score_now: false`. `load_all` clean + golden 17/17. Magnesium 'עייפות'→Moderate verified. **Gating dependency surfaced:** Hebrew keys are inert until `score_engine._PUNCT` is made Hebrew-aware (one-line Data change, its own governance). Three dossiers got a *first* umbrella (vitamin D3, creatine, omega-3 — score-path-creating like SUPP-EV-006 → Product D7 + golden re-validation before ship); caffeine deliberately left without one.
