# BSIP-S Scoring Architecture v1
# Bari Supplement Intelligence Protocol — Score Engine Design
**Date:** 2026-05-30
**Status:** Design Document v1
**Scope:** All 6 scoring frameworks + composite computation + grade thresholds

---

## Section 1 — Score Architecture Overview

```
BSIP-S Score = Composite(DA, FQ, TR, LI) × Evidence_Ceiling × Safety_Modifier
```

Four scored dimensions:
- **DA** — Dose Adequacy (40% weight)
- **FQ** — Form Quality (30% weight)
- **TR** — Transparency (20% weight)
- **LI** — Label Integrity (10% weight)

Two overrides that modify the composite:
- **Evidence Tier Ceiling** — category-level cap on what the composite can reach
- **Safety Override** — hard caps for products approaching or exceeding ULs

The formula is intentionally non-additive at the override level. An excellent formulation in a weak-evidence category is still capped. A safe dose cannot compensate for an unsafe dose.

---

## Section 2 — Evidence Quality Framework

Evidence Tier is assigned at the **category level**, not the product level. It represents the state of the scientific literature for the primary intended use of the supplement type.

### Tier Definitions

**Tier 1 — Strong Evidence**
Multiple independent RCTs with consistent outcomes. Effect sizes replicated across populations. At least one systematic review or meta-analysis. Consensus among major health authorities (NIH ODS, EFSA, WHO).

**Tier 2 — Mixed/Plausible Evidence**
RCTs exist but with inconsistent results, small populations, or narrow conditions. Plausible biological mechanism established. Effect may be real but context-dependent (strain, population, dosing protocol).

**Tier 3 — Preliminary Evidence**
Mechanistic studies, animal data, or small observational studies. No replication in adequately powered RCTs. Biological plausibility exists but unconfirmed in humans at supplement doses.

**Tier 4 — Insufficient Evidence**
Marketing-driven category. No credible mechanism. No RCT. Presence of active ingredient does not predict any measurable outcome. These categories are not scored — they are flagged.

### Evidence Tier × Score Ceiling

| Evidence Tier | Composite Score Ceiling |
|---|---|
| Tier 1 | 100 (no ceiling) |
| Tier 2 | 80 |
| Tier 3 | 60 |
| Tier 4 | Not scored — flag displayed instead |

### Category Assignments (v1)

| Category | Evidence Tier | Primary Evidence Base | Notes |
|---|---|---|---|
| Creatine | Tier 1 | 500+ RCTs; ISSN consensus | Most researched performance supplement |
| Vitamin D | Tier 1 | NIH ODS, EFSA, multiple meta-analyses | For deficiency correction and bone health |
| Magnesium | Tier 1 | NIH ODS; deficiency correction RCTs | Sleep/muscle benefits Tier 1; anxiety Tier 2 |
| Fish Oil (EPA/DHA) | Tier 1 | Triglyceride reduction: REDUCE-IT, STRENGTH | Cardiovascular event prevention: mixed post-2018 |
| Protein Powder | Tier 1 | ISSN; protein adequacy evidence robust | Scores protein quality, not "enhancement" |
| Probiotics | Tier 2 | Strain-condition pairs vary from T1–T3 | Category is Tier 2; specific strains may be T1 |
| Multivitamins | Tier 2 | No RCT benefit in replete populations; deficiency prevention plausible | Evidence for deficiency prevention; none for enhancement |
| Sleep Supplements | Tier 2 | Melatonin = Tier 1; other ingredients vary | Category average Tier 2 due to heterogeneity |

**Probiotic exception:** When a product uses a strain with a specific Tier 1 condition match (e.g., L. rhamnosus GG for AAD), note this in the expansion panel. The category ceiling remains Tier 2 unless the product is explicitly positioned for the specific evidence-matched condition.

---

## Section 3 — Dose Adequacy Framework (DA) — 40% Weight

Dose Adequacy scores how close the product's per-serving dose is to the dose range used in clinical trials showing an effect.

### Reference Dose Concept

Each category has a **clinical reference dose range**: the dose range across RCTs that demonstrated the primary intended effect. This is not the minimum effective dose (MEDs are often unknown) — it is the range where evidence exists.

**Scoring table:**

| Dose vs. Reference | DA Score | Label |
|---|---|---|
| 90–150% of reference range | 100 | Adequate |
| 70–89% or 151–250% | 80 | Near-adequate |
| 50–69% or 251–500% | 55 | Partial |
| 30–49% | 30 | Low |
| <30% | 10 | Insufficient |
| >500% of reference | See safety override | May exceed UL |
| Proprietary blend (unverifiable) | 20 | Opaque |

**Why ">500% of reference" triggers safety override:** At very high multiples of evidence-based doses, products may approach or exceed ULs (e.g., vitamin D at 10,000+ IU/day for extended periods; zinc at 50+ mg/day; iron at high doses without clinical indication).

### Reference Dose Sources
All reference doses documented in `bsip_s_category_framework_v1.md`. Sources: NIH ODS Fact Sheets, EFSA Dietary Reference Values, ISSN Position Stands, Examine.com synthesis (used for effect size alignment, not as primary reference).

### Elemental vs. Compound Dose
For minerals, DA is calculated on **elemental dose**, not compound weight. A product listing "500mg Magnesium Oxide" provides ~300mg elemental magnesium, but with ~4% absorption, effective delivery is ~12mg. BSIP-S uses elemental dose for DA scoring but notes form-adjusted delivery separately in the expansion panel.

### Multi-Ingredient Products (Multivitamins, Sleep Blends)
Score each primary active ingredient individually against its reference dose. Composite DA = average of primary ingredients weighted by evidence tier for each ingredient. Ingredients at <10% of reference are treated as decorative and excluded from composite DA (counted against LI instead).

---

## Section 4 — Ingredient Form Framework (FQ) — 30% Weight

Form Quality evaluates whether the specific ingredient form used has the bioavailability and pharmacokinetic profile consistent with the evidence base.

### Form Quality Tiers

**Optimal (100 points):** The form used in the majority of clinical trials, or a form with superior bioavailability demonstrated in head-to-head comparative studies. This is the form that delivers what the evidence promises.

**Acceptable (70 points):** A form with adequate bioavailability for the stated use, used in some RCTs, but not the gold standard. The product likely delivers meaningful amounts but with less certainty than optimal.

**Low (30 points):** A form with substantially lower bioavailability, or a form where the clinical evidence was generated with a different compound. The product may contain the nutrient but delivers less of it than labeling implies.

**Unknown (20 points):** Form is not specified on the label. Cannot assess bioavailability.

### Form Hierarchies by Category

**Magnesium:**
| Form | Quality | Bioavailability | Notes |
|---|---|---|---|
| Glycinate (bisglycinate) | Optimal | ~80% | Best tolerated; recommended for sleep/muscle |
| Malate | Optimal | ~65% | Good; used in fibromyalgia RCTs |
| L-Threonate | Optimal | ~7% elemental but crosses BBB | Specific for cognitive applications |
| Citrate | Acceptable | ~35% | Common, decent; laxative risk at high dose |
| Lactate | Acceptable | ~40% | |
| Chloride | Acceptable | ~30% | |
| Oxide | Low | ~4% | Most sold; worst absorbed; "400mg" misleading |
| Aspartate | Low | ~40% | Form; excitotoxicity concern at high dose |
| Sulfate (oral) | Low | ~25% | Primarily IV use |

**Vitamin D:**
| Form | Quality | Notes |
|---|---|---|
| D3 (cholecalciferol) | Optimal | Raises 25(OH)D ~70% more effectively than D2 |
| D2 (ergocalciferol) | Low | Less effective at raising serum levels; shorter half-life |
| Calcifediol (25-OH-D) | Optimal | Pre-converted; faster response; premium product |

**Fish Oil (EPA/DHA):**
| Form | Quality | Notes |
|---|---|---|
| Natural triglyceride (rTG re-esterified) | Optimal | Best absorption; ~50% better than EE |
| Natural triglyceride (wild-caught TG) | Optimal | Also excellent; standard in high-quality products |
| Ethyl ester (EE) | Acceptable | Most common commercial form; requires dietary fat for absorption |
| Phospholipid (krill) | Optimal | Excellent bioavailability; also provides choline |
| Free fatty acid | Optimal | Fast-absorbing; uncommon commercially |

**Creatine:**
| Form | Quality | Notes |
|---|---|---|
| Monohydrate | Optimal | Gold standard; 99%+ of RCTs; cost-effective |
| Creatine HCl | Acceptable | No evidence of superiority over monohydrate; smaller dose needed |
| Buffered (Kre-Alkalyn) | Acceptable | Not demonstrated superior in head-to-head |
| Ethyl ester | Low | Converts to creatinine; inferior in direct comparison |
| Proprietary forms (Magna Power, etc.) | Unknown | Insufficient comparative evidence |

**Protein:**
| Form | Quality | Notes |
|---|---|---|
| Whey isolate | Optimal | Complete AA profile; high DIAAS; fast-absorbing |
| Whey concentrate | Acceptable | Complete AA profile; some lactose; slightly lower protein% |
| Whey hydrolysate | Optimal | Pre-digested; faster absorption; used in post-surgical |
| Casein (micellar) | Optimal | Slow-release; appropriate for sustained AA delivery |
| Egg white | Optimal | Complete profile; high DIAAS |
| Pea isolate | Acceptable | Incomplete AA profile unless fortified with leucine/methionine |
| Soy isolate | Acceptable | Complete profile; phytoestrogen concern debated |
| Rice + Pea blend | Acceptable | Complementary AAs; approaches complete profile |
| Collagen/gelatin | Low | Not a complete protein; lacks tryptophan; marketed misleadingly |
| Single plant incomplete | Low | Missing essential AAs unless blend-corrected |

**Vitamin B12:**
| Form | Quality | Notes |
|---|---|---|
| Methylcobalamin | Optimal | Active form; direct use; better retention |
| Adenosylcobalamin | Optimal | Mitochondrial active form |
| Cyanocobalamin | Acceptable | Synthetic; must convert; widely used in RCTs |
| Hydroxocobalamin | Acceptable | Longer half-life; used in deficiency treatment |

**Folate (Vitamin B9):**
| Form | Quality | Notes |
|---|---|---|
| Methylfolate (5-MTHF) | Optimal | Active form; no MTHFR conversion required |
| Folinic acid | Optimal | Active; alternative to methylfolate |
| Folic acid | Acceptable | Synthetic; majority of RCT evidence; MTHFR may limit conversion |

**Zinc:**
| Form | Quality | Notes |
|---|---|---|
| Bisglycinate | Optimal | Best absorbed; gentlest on GI |
| Picolinate | Optimal | Well-absorbed |
| Acetate | Optimal | Used in lozenge RCTs |
| Citrate | Acceptable | Adequate |
| Sulfate | Acceptable | Common; GI irritation at high dose |
| Oxide | Low | Poor bioavailability (~10%) |

---

## Section 5 — Transparency Framework (TR) — 20% Weight

Transparency evaluates whether the consumer (and BSIP-S) can verify what is in the product.

### Transparency Tiers

| Scenario | TR Score | Description |
|---|---|---|
| Full disclosure + third-party certified | 100 | All ingredient amounts listed AND verified by NSF/USP/Informed Sport/IFOS/ConsumerLab |
| Full disclosure + manufacturer CoA published | 90 | All amounts listed; CoA available but not third-party |
| Full disclosure, no verification | 75 | All amounts listed; no third-party confirmation |
| Partial disclosure (blend total listed) | 40 | "Proprietary Blend 800mg" — total known, individuals unknown |
| No amounts for active ingredients | 20 | Active ingredients listed without amounts |
| Opaque proprietary blend, no total | 10 | Cannot assess any dose |

### Third-Party Certification Values

| Certification Body | What It Verifies | Trust Level |
|---|---|---|
| NSF Certified for Sport | Label accuracy + banned substance testing | Highest — mandatory for professional athletes |
| USP Verified | Label accuracy + dissolution + contaminants | Highest — pharmaceutical standard |
| Informed Sport | Label accuracy + banned substance | Highest — UK/international athletes |
| ConsumerLab | Label accuracy + purity | High — independent |
| IFOS (fish oil specific) | Purity, oxidation, EPA/DHA content | Highest for fish oil |
| Informed Choice | Label accuracy + banned substance | High |
| Self-certification / QR code to internal CoA | Internal only | Low — not independent |
| "GMP Certified" claim | Manufacturing process only | Not a content verification |

**GMP certification does not verify label accuracy.** It verifies that the manufacturing process was followed. A GMP facility can still produce a product with inaccurate label claims. This distinction must be reflected in TR scoring.

---

## Section 6 — Label Integrity Framework (LI) — 10% Weight

Label Integrity evaluates the honesty of the claims made on the label relative to the actual formulation and evidence.

### Claim Classification

**Structure/Function Claims (e.g., "supports immune health")**
Allowed without clinical proof under Israeli supplement regulations. However, BSIP-S assesses whether the formulation and dose are consistent with the implied mechanism.

**Nutrient Content Claims (e.g., "high in vitamin D")**
Verifiable from label. Score reflects whether the stated amount is accurate and the threshold claim is legitimate.

**Efficacy Claims (e.g., "clinically proven to improve sleep")**
These require specific evidence backing. BSIP-S evaluates whether the cited or implied evidence matches the actual product.

**Comparison Claims (e.g., "3× more bioavailable")**
Must be backed by head-to-head data. BSIP-S flags unsupported comparison claims.

### LI Scoring Table

| Claim Assessment | LI Score | Action |
|---|---|---|
| All claims consistent with dose and evidence | 100 | |
| Minor unsupported wellness language | 80 | Flag in expansion |
| Structure/function claim with underdosed ingredient | 55 | Note in expansion: "label claim not matched by dose" |
| Efficacy claim without supporting evidence | 40 | Flag as "unsupported" in expansion |
| Misleading comparison claim | 30 | Flag as "unsupported comparison" |
| Prohibited efficacy/disease claim | 10 | Mandatory disclosure; do not suppress |

### Claim Integrity × Dose Adequacy Interaction

A claim integrity failure triggered by underdosing is captured in both LI and DA. The two scores are independent — underdosing penalizes DA directly (low score) AND LI (claim not matched by formula). This double-signal is intentional: underdosed claims are the most prevalent form of supplement deception.

---

## Section 7 — Safety Framework

Safety is not a dimension in the composite score. It is an **override layer** that applies after composite calculation.

### Upper Tolerable Intake Levels (ULs)

ULs are set by EFSA and NIH ODS. Supplemental ULs apply on top of dietary intake. BSIP-S evaluates supplemental dose only, acknowledging that dietary intake is unobservable.

| Nutrient | UL (Supplemental) | Source |
|---|---|---|
| Magnesium (elemental) | 350 mg/day | NIH ODS |
| Vitamin D | 4,000 IU/day (100 mcg) | NIH ODS; EFSA 100 mcg |
| Zinc (elemental) | 40 mg/day | NIH ODS |
| Vitamin A (preformed) | 3,000 mcg RAE/day | NIH ODS |
| Iron | 45 mg/day | NIH ODS |
| Calcium | 2,500 mg/day | NIH ODS |
| Vitamin B6 | 100 mg/day | NIH ODS |
| Folate (synthetic) | 1,000 mcg/day | NIH ODS |
| Selenium | 400 mcg/day | NIH ODS |
| Iodine | 1,100 mcg/day | NIH ODS |
| Fish Oil (EPA+DHA) | 3,000 mg/day (supplemental); FDA GRAS at 3g/day | FDA/NIH |
| Creatine | No established UL; 3–5g/day maintenance supported | ISSN |
| Melatonin | No formal UL; 10mg/day commonly cited upper bound | Not established; guidance-based |

**Note on Vitamin D:** The 4,000 IU/day UL is conservative. Many practitioners and studies use 10,000 IU/day safely. BSIP-S applies the NIH ODS UL but notes in the safety flag that supervised higher doses are used clinically.

### Safety Override Rules

| Scenario | Override |
|---|---|
| Dose 80–99% of UL | Score capped at 70; note: "קרוב למגבלה הבטוחה — ייעוץ מקצועי מומלץ" |
| Dose at or above UL | Score hard-capped at 50; mandatory safety disclosure |
| Dose >200% of UL | Score hard-capped at 30; mandatory safety disclosure |
| Known serious drug interaction risk at stated dose | Score hard-capped at 50; mandatory disclosure |
| Ingredient with banned substance risk (professional sport) | Mandatory disclosure if no third-party sport certification |

### Known Interaction Flags (Mandatory Disclosure Triggers)

| Supplement | Interaction Risk |
|---|---|
| Fish Oil at >3g EPA+DHA | Anticoagulant potentiation (warfarin, aspirin) |
| Vitamin K2 (MK-4/MK-7) | Warfarin antagonism |
| St. John's Wort (in sleep blends) | CYP3A4 inducer — broad drug interaction |
| 5-HTP (in sleep blends) | Serotonin syndrome risk with SSRIs/MAOIs |
| Iron at high doses | Potentially harmful without confirmed deficiency |
| Vitamin A (preformed high dose) | Teratogenic at >3,000 mcg/day; pregnancy warning |
| Melatonin | CNS depressant interaction; immunosuppressant interaction |
| High-dose zinc | Copper depletion with chronic use |

---

## Section 8 — Composite Score Calculation

```python
def compute_bsip_s_score(product):
    # Step 1: Calculate dimension scores
    da = score_dose_adequacy(product)     # 0–100
    fq = score_form_quality(product)      # 0–100
    tr = score_transparency(product)      # 0–100
    li = score_label_integrity(product)   # 0–100

    # Step 2: Weighted composite
    composite = (
        da * 0.40 +
        fq * 0.30 +
        tr * 0.20 +
        li * 0.10
    )

    # Step 3: Evidence tier ceiling
    ceiling = EVIDENCE_TIER_CEILINGS[product.category_evidence_tier]
    composite = min(composite, ceiling)

    # Step 4: Safety override
    composite = apply_safety_override(composite, product)

    # Step 5: Confidence floor
    if product.dataConfidence == "insufficient":
        composite = min(composite, 40)

    # Step 6: Round and grade
    score = round(composite)
    grade = score_to_grade(score)

    return score, grade


EVIDENCE_TIER_CEILINGS = {1: 100, 2: 80, 3: 60}


def score_to_grade(score):
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"
```

---

## Section 9 — Grade Interpretation

| Grade | Score Range | Consumer Meaning |
|---|---|---|
| A | ≥80 | Optimal formulation. Evidence-backed category. Adequate dose. Full or near-full transparency. |
| B | 65–79 | Good formulation. Minor gaps: slightly underdosed, acceptable (not optimal) form, or limited third-party verification. |
| C | 50–64 | Adequate but compromised. May be in a mixed-evidence category, use a lower-bioavailability form, or disclose partially. |
| D | 35–49 | Significant formulation concerns. Likely underdosed, low-bioavailability form, or opaque blend. Limited utility at stated dose. |
| E | <35 | Formulation unlikely to deliver meaningful dose of active ingredient at the right form. Proprietary blend typical. |

**Grade notes for consumer-facing display:**
- Never display BSIP-S dimension names
- Never display evidence tier
- Never display safety override trigger
- Expansion panel surfaces the signal, not the mechanism

---

## Section 10 — Multi-Ingredient Product Scoring (Multivitamins and Sleep Blends)

### Step 1: Identify primary ingredients
Classify each ingredient by evidence tier for its primary function in this product context.

### Step 2: Score each primary ingredient individually
- DA, FQ per ingredient
- TR, LI are product-level (not per-ingredient)

### Step 3: Composite DA
```
DA_composite = Σ(DA_i × evidence_weight_i) / Σ(evidence_weight_i)
evidence_weight = {Tier 1: 1.0, Tier 2: 0.6, Tier 3: 0.3}
```

### Step 4: Composite FQ
```
FQ_composite = Σ(FQ_i × evidence_weight_i) / Σ(evidence_weight_i)
```
Same evidence weighting applied to FQ.

### Step 5: Decorative ingredient flag
Any ingredient dosed at <10% of its reference dose is flagged as "decorative." It does not contribute to DA composite positively, and each decorative ingredient deducts 5 points from LI (claim inflation).

### Step 6: Category ceiling
- Multivitamins: Tier 2 ceiling (80)
- Sleep supplements: Tier 2 ceiling (80), unless product is melatonin-only → Tier 1 ceiling (100)

---

## Section 11 — Score Confidence Interaction

| Confidence | Maximum Score |
|---|---|
| Verified | 100 (limited only by evidence tier ceiling and safety) |
| Partial | 85 (some uncertainty in dose/form assessment) |
| Insufficient | 40 (can only partially assess product quality) |

These are additional caps, applied after evidence tier ceiling and safety override.
