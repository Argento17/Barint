export type BreadCategory = "bread" | "cracker" | "crispbread";

export type BreadArchetype =
  | "sourdough_traditional"
  | "nordic_whole_grain"
  | "seeds_multigrain"
  | "sourdough_theater"
  | "fiber_inflation"
  | "engineered_functional"
  | "simple_white"
  | "treat_salty";

export type FermentationQuality = "traditional" | "mixed" | "flavor_only" | "none";

export type FiberSourceQuality = "structural" | "hybrid" | "isolated";

export type BreadGrade = "A" | "B" | "C" | "D" | "E";

export type BreadNutrition = {
  energy_kcal: number;
  protein_g: number;
  fiber_g: number;
  fat_g: number;
  carbs_g: number;
  sugar_g: number;
};

export type BreadProduct = {
  id: string;
  name_he: string;
  brand: string;
  category: BreadCategory;
  archetype: BreadArchetype;
  score: number;
  grade: BreadGrade;
  grade_label: string;
  base_score: number;
  delta: number;
  nova_proxy: number;
  gss: number;
  ferm_q: FermentationQuality;
  fiber_q: FiberSourceQuality;
  image_url: string | null;
  nutrition: BreadNutrition;
  ingredients_display: string;
  red_labels: string[];
  insight: string;
  finding: string | null;
};

export type BreadComparisonPage = {
  generated_at: string;
  schema_version: string;
  comparison_title: string;
  story_headline: string;
  products: BreadProduct[];
};

export type BreadFilterId =
  | "all"
  | "sourdough_traditional"
  | "nordic_whole_grain"
  | "seeds_multigrain"
  | "sourdough_theater"
  | "fiber_inflation"
  | "engineered_functional"
  | "simple_white"
  | "treat_salty"
  | "grade_a"
  | "grade_b_plus"
  | "has_fermentation"
  | "isolated_fiber";
