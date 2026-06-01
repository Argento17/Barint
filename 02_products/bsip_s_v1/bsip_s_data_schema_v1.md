# BSIP-S Data Schema v1
# Bari Supplement Intelligence Protocol — Observable Data Contract
**Date:** 2026-05-30
**Status:** Design Document v1
**Scope:** What data BSIP-S can observe, require, and flag as missing

---

## Section 1 — Schema Philosophy

BSIP-S only scores what is observable from the product label and any publicly verifiable third-party source (certification databases, manufacturer published CoA, retailer product pages).

**What BSIP-S never assumes:**
- Bioavailability values not documented in the literature for the specific form
- Dose effects not established in peer-reviewed trials
- Purity beyond what is certified or disclosed
- Individual need or response

**Observable sources (in priority order):**
1. Supplement Facts Panel (mandatory in Israel per Ministry of Health food supplement regulation)
2. Other Ingredients list (excipients, fillers, coatings)
3. Front-of-pack claims (health claims, usage claims, certifications claimed)
4. Third-party certification databases (NSF, USP, Informed Sport, ConsumerLab, IFOS)
5. Manufacturer-published Certificate of Analysis (where available)
6. Retailer product page (description, images)

---

## Section 2 — Core Schema (TypeScript reference)

```typescript
interface BSIPSProduct {
  // ── Identity ──────────────────────────────────────────────────
  id: string;                           // "supp-mag-001"
  category: SupplementCategory;         // "magnesium" | "vitamin_d" | ...
  name: string;                         // Full product name as on label (Hebrew/English)
  brand: string;
  retailer?: string;                    // Where observed
  imageUrl?: string;

  // ── Serving ──────────────────────────────────────────────────
  servingSize: string;                  // "2 capsules" | "1 scoop (30g)"
  servingSizeG?: number;                // Gram equivalent if powder
  servingsPerContainer: number | null;  // null if not printed

  // ── Active Ingredients ───────────────────────────────────────
  activeIngredients: BSIPSIngredient[];

  // ── Other Ingredients ────────────────────────────────────────
  otherIngredients: string[];           // Excipients, fillers, flow agents, coatings
  otherIngredients_raw?: string;        // Verbatim from label for audit

  // ── Format ───────────────────────────────────────────────────
  format: ProductFormat;
  // "capsule" | "softgel" | "tablet" | "powder" | "gummy" | "liquid" | "lozenge"

  // ── Certifications ───────────────────────────────────────────
  certifications: Certification[];
  certifications_claimed: string[];     // As printed on label (may differ from verified)

  // ── Label Claims ─────────────────────────────────────────────
  labelClaims: LabelClaim[];

  // ── Price ────────────────────────────────────────────────────
  priceILS?: number;                    // Total product price
  pricePerServing?: number;             // Derived: price / servings

  // ── Data Quality ─────────────────────────────────────────────
  dataConfidence: DataConfidence;       // "verified" | "partial" | "insufficient"
  dataSource: string;                   // "label_photo_2026-05-30" | "retailer_api" | ...
  hasProprietaryBlend: boolean;
  proprietaryBlendTotal_mg?: number;    // If blend total is disclosed

  // ── Score Output (populated after scoring) ───────────────────
  score?: number;                       // 0–100
  grade?: string;                       // "A" | "B" | "C" | "D" | "E"
  insightLine?: string;                 // Single Hebrew insight line for consumer display
  expansion?: BSIPSExpansion;
}

interface BSIPSIngredient {
  name: string;                         // As printed on label
  name_canonical: string;              // Normalized: "magnesium_glycinate"
  compound?: string;                   // "magnesium glycinate" — the full compound
  active?: string;                     // "magnesium" — the active moiety
  amount_mg?: number;                  // Per serving, in mg (convert IU/mcg/CFU as needed)
  amount_unit: "mg" | "mcg" | "IU" | "CFU" | "g" | "billion_cfu";
  amount_raw: string;                  // Verbatim: "400 IU" | "1.2mg" | "10 Billion CFU"
  elemental_mg?: number;               // For minerals: elemental amount (not compound)
  elemental_pct?: number;              // Elemental fraction by weight
  form: string;                        // "glycinate" | "oxide" | "D3_cholecalciferol" | ...
  form_quality?: IngredientFormQuality; // "optimal" | "acceptable" | "low" | "unknown"
  is_primary: boolean;                 // Is this the primary active ingredient for the category
  evidence_notes?: string;             // Internal only — not consumer-facing
}

interface Certification {
  body: string;         // "NSF" | "USP" | "Informed_Sport" | "IFOS" | "ConsumerLab"
  type: string;         // "certified_for_sport" | "verified" | "five_star"
  verified: boolean;    // Cross-checked against certification database
  verification_date?: string;
}

interface LabelClaim {
  claim_text: string;   // Verbatim from label
  claim_type: ClaimType;
  // "structure_function" | "nutrient_content" | "health_claim" | "efficacy_implied" | "general_wellness"
  supported: ClaimSupport;
  // "supported" | "partially_supported" | "unsupported" | "underdosed" | "prohibited_review"
}

type DataConfidence = "verified" | "partial" | "insufficient";

type IngredientFormQuality = "optimal" | "acceptable" | "low" | "unknown";

interface BSIPSExpansion {
  positiveSignals: string[];   // 1–3 observable, specific
  limitingFactors: string[];   // 0–3 specific concerns
  bottomLine: string;          // "[score]/[grade]: one honest sentence"
  comparisonContext?: string;  // Position within category corpus
  doseNote?: string;           // Dose adequacy in plain language
  formNote?: string;           // Form quality in plain language
  safetyNote?: string;         // If safety concern, mandatory disclosure
  certificationNote?: string;  // If third-party verified
  confidenceLabel: string;     // "מידע מלא" | "מידע חלקי" | "מידע לא מספיק"
}
```

---

## Section 3 — Elemental Amount Handling

Minerals are sold as compounds. The label may list compound weight or elemental weight. BSIP-S requires elemental weight for dose adequacy scoring.

**Elemental fractions (by weight):**

| Compound | Elemental Fraction | Notes |
|---|---|---|
| Magnesium glycinate | 14.1% | e.g., 400mg compound → 56mg elemental Mg |
| Magnesium malate | 19.9% | |
| Magnesium citrate | 16.2% | |
| Magnesium oxide | 60.3% | High elemental %, but ~4% absorption rate |
| Magnesium L-Threonate | 7.2% | Low elemental %, but crosses blood-brain barrier |
| Zinc picolinate | 20.6% | |
| Zinc bisglycinate | 24.4% | |
| Zinc oxide | 80.3% | Low bioavailability |
| Iron bisglycinate | 20.0% | |
| Iron fumarate | 33.0% | |
| Calcium carbonate | 40.0% | Low absorption, requires stomach acid |
| Calcium citrate | 21.1% | Better absorption, especially without food |

**When elemental amount is not specified on label:**
- Mark `elemental_mg: null`
- Mark `dataConfidence: "partial"` (at minimum)
- Apply dose adequacy penalty for unverifiable elemental content

---

## Section 4 — IU Conversion Reference

For fat-soluble vitamins where IU is used on labels:

| Vitamin | 1 IU = |
|---|---|
| Vitamin D (D3) | 0.025 mcg cholecalciferol |
| Vitamin D (D2) | 0.025 mcg ergocalciferol |
| Vitamin A (retinol) | 0.3 mcg retinol |
| Vitamin A (beta-carotene) | 0.6 mcg beta-carotene |
| Vitamin E (natural d-alpha-tocopherol) | 0.67 mg |
| Vitamin E (synthetic dl-alpha-tocopherol) | 0.45 mg |

**Example:** "2000 IU Vitamin D3" = 50 mcg cholecalciferol

---

## Section 5 — CFU Handling (Probiotics)

Probiotic CFU counts require special treatment:

```typescript
interface ProbioticIngredient extends BSIPSIngredient {
  strain_name: string;            // Full strain: "Lactobacillus rhamnosus GG"
  strain_code?: string;           // "ATCC 53103" | "LGG" — identifies research strain
  cfu_at_manufacture?: string;    // "50 Billion CFU at manufacture"
  cfu_at_expiry?: string;         // "10 Billion CFU at expiry" (lower, more honest)
  cfu_guarantee: "at_manufacture" | "at_expiry" | "unspecified";
  survivability_claim: boolean;   // Enteric coating / acid-resistant claim
  refrigeration_required: boolean;
  evidence_strain_match: boolean; // Does the strain match a researched strain?
}
```

**CFU at manufacture vs. at expiry:** Products guaranteeing CFU at expiry are significantly more transparent. A "50 Billion CFU at manufacture" product may deliver 5 Billion at time of use if stored improperly.

---

## Section 6 — Proprietary Blend Handling

```typescript
interface ProprietaryBlend {
  blend_name: string;           // "Sleep Support Complex"
  total_mg: number | null;      // Disclosed blend total, if listed
  ingredients: string[];        // Names only, amounts unknown
  primary_ingredient?: string;  // Can be inferred from label order (listed highest→lowest)
}
```

**Scoring impact of proprietary blends:**
- Dose adequacy: forced to "insufficient" assessment → 20 points maximum on DA dimension
- Transparency dimension: maximum 20 points
- Data confidence: "insufficient" for blend ingredients

**Exception:** If a proprietary blend is accompanied by a Certificate of Analysis disclosing individual amounts, treat as full disclosure.

---

## Section 7 — Required vs Optional Fields

| Field | Required for Scoring | Required for Display |
|---|---|---|
| `activeIngredients[].amount_raw` | Yes | Yes |
| `activeIngredients[].form` | Yes | Yes |
| `activeIngredients[].elemental_mg` (minerals) | Yes | No |
| `servingSize` | Yes | Yes |
| `servingsPerContainer` | Recommended | No |
| `certifications` | No | If present |
| `labelClaims` | Recommended | No |
| `pricePerServing` | No | No |
| `otherIngredients` | Recommended | No |
| `hasProprietaryBlend` | Yes | Yes (flag) |

**Minimum viable dataset for scoring:**
Active ingredients with amounts (raw), forms, serving size. Everything else improves score precision but is not blocking.

---

## Section 8 — Data Collection Priorities by Format

| Format | Primary Risk | Collection Focus |
|---|---|---|
| Capsule / tablet | Elemental vs. compound confusion | Verify elemental fraction; confirm form |
| Softgel | Oxidation state not visible | Request IFOS or similar for fish oil |
| Powder | Scoop size inconsistency | Verify g/scoop; check proprietary blend |
| Gummy | Sugar/sweetener content | Check other ingredients for added sugar |
| Liquid | Concentration per ml vs. per serving | Verify serving size against ml |
| Enteric-coated tablet | Bioavailability claim | Confirm coating is pharmaceutical-grade |
