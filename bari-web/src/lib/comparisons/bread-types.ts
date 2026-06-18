export type BreadCategory =
  | "bread"
  | "cracker"
  | "whole_food_fat"
  | "default"
  | "unknown";

export type BreadClusterId =
  | "everyday"
  | "strong"
  | "fermentation"
  | "wellness_ambig"
  | "crackers"
  | "transparency";

export type BreadVisibleClusterId = Exclude<BreadClusterId, "transparency">;

export type BreadFilterId =
  | "all"
  | "everyday"
  | "fermentation"
  | "strong"
  | "wellness_ambig"
  | "crackers";

export type BreadGrade = "A" | "B" | "C" | "D" | "E";

export type BreadConfidenceLabel =
  | "נתונים מלאים יחסית"
  | "נתונים חלקיים"
  | "חסרים נתונים מהותיים"
  | "לא מספיק לניתוח ודאי";

export type BreadConfidenceLevel = "full" | "partial" | "missing" | "insufficient";

export type BreadFermentationStatus =
  | "מחמצת אמיתית (מזוהה ברכיבים)"
  | "מחמצת אמיתית (עם שמרים עזר)"
  | "מחמצת בשם, שמרים ברכיבים"
  | "שמרים תעשייתיים בלבד"
  | "לא ידוע — חסרים נתוני רכיבים"
  | "לא זוהה תוהל";

export type BreadRawProduct = {
  product_id: string;
  name_he: string;
  brand: string;
  category_display_he: string;
  website_cluster: BreadClusterId;
  website_cluster_label_he: string;
  score: number | null;
  grade: BreadGrade | null;
  confidence_label_he: BreadConfidenceLabel;
  display_score_boolean: boolean;
  safe_for_ranking_boolean: boolean;
  safe_for_blog_boolean: boolean;
  fiber_g: number | null;
  protein_g: number | null;
  sodium_mg: number | null;
  fermentation_status_he: BreadFermentationStatus;
  fiber_source_status_he: string;
  seed_halo_status_he: string;
  structural_summary_he: string;
  why_featured_he: string;
  suggested_card_blurb_he: string;
  image_url: string;
  source_url: string;
  degradation_level: string;
  acquisition_tier: string;
  _category_internal?: string;
};

export type BreadProduct = BreadRawProduct & {
  id: string;
  category: BreadCategory;
  category_label_he: string;
  displayable: boolean;
  confidence_level: BreadConfidenceLevel;
};

export type BreadCluster = {
  cluster_id: BreadClusterId;
  label_he: string;
  products: BreadRawProduct[];
};

export type BreadDatasetMeta = {
  run_id: string;
  generated: string;
  total_curated: number;
  source: string;
  scope_note: string;
  cluster_labels: Record<BreadClusterId, string>;
  cluster_counts: Record<BreadClusterId, number>;
  signal_notes: {
    fermentation: string;
    fiber_source: string;
    seed_halo: string;
  };
};

export type BreadDataset = {
  meta: BreadDatasetMeta;
  clusters: BreadCluster[];
  all_products: BreadRawProduct[];
};

export type BreadComparisonPair = {
  id: string;
  title: string;
  kicker: string;
  caption: string;
  left: BreadProduct;
  right: BreadProduct;
};

export type BreadInsightBlock = {
  id: string;
  title: string;
  body: string;
  supporting: string[];
};

export type BreadArticleHeroStat = {
  value: string;
  label: string;
  note?: string;
};

export type BreadArticleProductMention = {
  productId: string;
  kicker?: string;
  note: string;
};

export type BreadArticleStatRow = {
  productId: string;
  score: string;
  whatWeChecked: string;
  whatWeLearned: string;
};

export type BreadArticleBlockTone = "neutral" | "positive" | "warning";

export type BreadArticleNarrativeBlock = {
  type: "narrative";
  title?: string;
  paragraphs: string[];
  sideNote?: {
    label: string;
    text: string;
  };
};

export type BreadArticleInsightBlockContent = {
  type: "insight";
  eyebrow: string;
  title: string;
  body: string;
  bullets?: string[];
  tone?: BreadArticleBlockTone;
};

export type BreadArticleEvidenceItem = BreadArticleProductMention & {
  evidence?: string;
  tone?: BreadArticleBlockTone;
};

export type BreadArticleEvidenceStripBlock = {
  type: "evidenceStrip";
  title: string;
  intro?: string;
  columns?: 2 | 3;
  items: BreadArticleEvidenceItem[];
};

export type BreadArticleComparisonSide = {
  productId: string;
  label: string;
  evidence?: string;
  points: string[];
};

export type BreadArticleComparisonBlock = {
  type: "comparison";
  eyebrow?: string;
  title: string;
  intro?: string;
  left: BreadArticleComparisonSide;
  right: BreadArticleComparisonSide;
  takeaway: string;
};

export type BreadArticleMicroShelfBlock = {
  type: "microShelf";
  title: string;
  intro?: string;
  items: BreadArticleProductMention[];
};

export type BreadArticleTableBlock = {
  type: "table";
  title: string;
  note: string;
  rows: BreadArticleStatRow[];
};

export type BreadArticleQuoteBlock = {
  type: "quote";
  text: string;
};

export type BreadArticleBlock =
  | BreadArticleNarrativeBlock
  | BreadArticleInsightBlockContent
  | BreadArticleEvidenceStripBlock
  | BreadArticleComparisonBlock
  | BreadArticleMicroShelfBlock
  | BreadArticleTableBlock
  | BreadArticleQuoteBlock;

export type BreadArticleContent = {
  slug: string;
  href: string;
  title: string;
  shortTitle: string;
  description: string;
  metaTitle: string;
  metaDescription: string;
  readTime: string;
  metaLine: string;
  categoryLabel: string;
  eyebrow: string;
  deck: string;
  scopeNote?: string;
  contextStats: BreadArticleHeroStat[];
  intro: string[];
  leadMentions?: BreadArticleProductMention[];
  blocks: BreadArticleBlock[];
  ctaLabel: string;
  ctaHref: string;
};
