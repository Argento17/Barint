export type BariGrade = "A" | "B" | "C" | "D" | "E";

export type ProductNutrition = {
  energy_kcal: number | null;
  protein_g: number | null;
  sugar_g: number | null;
  fat_g: number | null;
  fiber_g: number | null;
  sodium_mg: number | null;
};

export type ComparisonProduct = {
  id: string;
  name_he: string;
  image_url: string | null;
  score: number | null;
  grade: BariGrade | null;
  insight_line: string;
  ingredients_he: string;
  nutrition: ProductNutrition;
  confidence_level: "full" | "partial" | "insufficient";
};
