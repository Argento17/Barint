export type BariGrade = "A" | "B" | "C" | "D" | "E";

export type ProductType =
  | "dairy"
  | "oat"
  | "soy"
  | "almond"
  | "rice"
  | "coconut"
  | "protein_drink"
  | "other_plant";

export type ComparisonFilterId =
  | "type:dairy"
  | "type:oat"
  | "type:soy"
  | "type:almond"
  | "type:rice"
  | "no_additives"
  | "high_protein"
  | "low_sugar"
  | "coffee"
  | "high_score";

export type BariInterpretationPillar = {
  key: string;
  label: string;
  score: number;
  strength: string;
  interpretation: string;
};

export type ConsumerExplanation = {
  whyRated: string;
  good: string[];
  watchOut: string[];
  context: string;
  takeaway: string;
};

export type MatrixIntegrity = {
  matrix_integrity_score: number;
  reconstruction_depth: number;
  structural_degradation_level: string;
  engineering_intensity: number;
  dominant_matrix_signals: string[];
  integrity_summary: string;
};

export type MilkComparisonProduct = {
  barcode: string;
  shortName: string;
  displayTitle?: string;
  brandLine?: string | null;
  name_he: string;
  brand: string;
  productType: ProductType;
  productTypeLabel: string;
  image_url: string | null;
  score: number;
  grade: BariGrade;
  grade_label: string;
  proteinPer100ml: number | null;
  sugarPer100ml: number | null;
  additivesLabel: string;
  mainIngredient: string;
  bestUseCases: string[];
  consumerTakeaway: string;
  consumerExplanation: ConsumerExplanation;
  bariInterpretation?: BariInterpretationPillar[];
  filterTags: string[];
  /** Advanced / debug only */
  nova_proxy: number;
  red_labels: string[];
  ingredients_display: string;
  energy_kcal: number | null;
  dimensions: Record<string, { score: number; display_name: string }>;
  matrix_integrity: MatrixIntegrity;
  explanation_drivers: string[];
};

export type MilkComparisonPageData = {
  generated_at: string;
  data_source: string;
  comparison_title: string;
  story_headline: string;
  story_teaser: string;
  philosophy_note: string;
  products: MilkComparisonProduct[];
};
