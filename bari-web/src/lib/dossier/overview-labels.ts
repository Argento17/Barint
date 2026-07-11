/**
 * English label maps for the Product Dossier Overview/Evidence tabs (TASK-620 /
 * PD-3.1). Pure data — no framework vocabulary (NOVA, BSIP, cap, structural_class,
 * matrix_integrity, pillar, dimension) ever appears as a rendered value; internal
 * field keys are translated to plain English here instead of being printed verbatim
 * (that verbatim behavior stays confined to the Technical-audit tab, which moves the
 * existing Hebrew diagnostic components as-is, per spec).
 *
 * `dimension_scores` keys are rendered under their real field names (labeled in
 * English) rather than force-fit to an invented 5-axis scheme — see the Overview
 * profile-bars component comment for why.
 *
 * NOTE: `assessment.nova_proxy` is intentionally NOT given a label here and must
 * never be rendered in the Overview or Evidence tabs — its very field name is the
 * banned framework term (Hard Rule 3).
 */

export const LAYER4_CHECK_LABEL: Record<string, string> = {
  barcode: "Barcode identity",
  source_traceability: "Source traceability",
  calculation: "Score reproducibility",
  publishability: "Publishability (diagnostic only)",
};

export const DIMENSION_LABEL: Record<string, string> = {
  additive_quality: "Additives",
  calorie_density: "Calorie density",
  fat_quality: "Fat quality",
  glycemic_quality: "Glycemic quality",
  nutrient_density: "Nutrient density",
  processing_quality: "Processing",
  protein_quality: "Protein quality",
  regulatory_quality: "Regulatory / labeling",
  satiety_support: "Satiety",
  whole_food_integrity: "Whole-food integrity",
};

export const DATA_QUALITY_LABEL: Record<string, string> = {
  evidence_completeness: "Evidence completeness",
  evidence_flag_rate: "Evidence flag rate",
  identity_confidence: "Identity confidence",
  image_confidence: "Image confidence",
};

export const PUBLICATION_RECORD_LABEL: Record<string, string> = {
  score: "Published score",
  grade: "Published grade",
  run_id: "Run ID",
  trace_hash: "Trace hash",
};

export const ASSESSMENT_HEADLINE_LABEL: Record<string, string> = {
  final_score_estimate: "Reproduced score estimate",
  grade_estimate: "Reproduced grade estimate",
  confidence_score: "Assessment confidence",
  category: "Category",
};

export const IDENTITY_FACT_LABEL: Record<string, string> = {
  name: "Name",
  brand: "Brand",
  manufacturer: "Manufacturer",
  package_size: "Package size",
  retailer: "Retailer",
  source_urls: "Source URLs",
  last_scrape: "Last scraped",
};

/** field name → { label, unit }. Units are fixed per field (never invented per-row). */
export const LAYER2_FIELD_META: Record<string, { label: string; unit: string }> = {
  energy: { label: "Energy", unit: "kcal" },
  protein: { label: "Protein", unit: "g" },
  fat: { label: "Fat", unit: "g" },
  saturated_fat: { label: "Saturated fat", unit: "g" },
  trans_fat: { label: "Trans fat", unit: "g" },
  carbs: { label: "Carbohydrates", unit: "g" },
  sugar: { label: "Sugar", unit: "g" },
  fiber: { label: "Fiber", unit: "g" },
  sodium: { label: "Sodium", unit: "mg" },
  cholesterol: { label: "Cholesterol", unit: "mg" },
};

export const BARCODE_STATUS_LABEL_EN: Record<string, string> = {
  verified: "Verified",
  malformed: "Malformed",
  pending_manual_review: "Pending manual review",
  found_but_conflicting: "Conflicting match",
  not_found: "Not found",
  unknown: "Unknown",
};
