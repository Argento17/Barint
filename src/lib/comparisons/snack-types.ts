export type SnackGrade = "B" | "C" | "D" | "E";

export type SnackConfidenceLevel = "full" | "partial" | "insufficient";

export type SnackClusterId =
  | "date-simple"
  | "granola-oat"
  | "coated-cereal"
  | "protein"
  | "fitness"
  | "natural-gap"
  | "insufficient";

export type SnackNOVA = 2 | 3 | 4;

export type SnackStructuralBase = "בסיס שלם" | "בסיס מעובד" | "בסיס מהונדס";

export type SnackSweetenerPattern = "מקור יחיד" | "2 מקורות" | "3+ מקורות";

export type SnackAdditiveLoad = "0–2" | "3–4" | "5+";

export type SnackPositioningLens =
  | "פרוטאין"
  | "פיטנס"
  | "אנרג'י"
  | "טבעי/תמרים"
  | "ללא מיצוב";

export type SnackCompositionRow = {
  dimension: string;
  value: string;
  effect_he: string;
};

export type SnackScoreDriverRow = {
  driver: string;
  impact_he: string;
};

export type SnackWhyLanded = {
  highlight_he: string;
  limit_he?: string;
  uncertainty_he?: string;
};

export type SnackProduct = {
  id: string;
  name_he: string;
  brand: string;
  segment: string;
  image_url?: string | null;
  ingredient_count?: number | null;
  score: number | null;
  grade: SnackGrade | null;
  displayable: boolean;
  confidence_level: SnackConfidenceLevel;
  confidence_label_he: string;
  nova: SnackNOVA | null;
  structural_base: SnackStructuralBase;
  sweetener_pattern: SnackSweetenerPattern;
  additive_load: SnackAdditiveLoad;
  positioning: SnackPositioningLens;
  key_observation_he: string;
  explainability_tags: string[];
  caps_applied: string[];
  cluster_id: SnackClusterId;
  x: number;
  y: number;
};

export type SnackEngineFilters = {
  grades: SnackGrade[];
  nova: SnackNOVA[];
  segment: string | null;
  scoreMin: number;
  scoreMax: number;
};

export const SNACK_SEGMENTS = [
  "חטיפי תמרים",
  "חטיפי גרנולה ושיבולת שועל",
  "חטיפי דגנים מצופי שוקולד",
  "חטיפי פרוטאין",
  "חטיפי \"סלים\" / רב-דגן",
  "חטיפי אגוזים",
] as const;

export type SnackFilterId =
  | "all"
  | "date-based"
  | "oat-cereal"
  | "wellness"
  | "grade-e"
  | "insufficient";

