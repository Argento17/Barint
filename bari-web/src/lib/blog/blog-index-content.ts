import blogIndexData from "@/data/blog/blog-index.json";

export type BlogCategoryId =
  | "all"
  | "comparisons"
  | "ingredients"
  | "processing"
  | "israeli-shelf"
  | "bari-labs";

export type BlogArticleCard = {
  slug: string;
  href: string;
  title: string;
  description: string;
  cta: string;
  category: BlogCategoryId;
  categoryLabel: string;
  readTime: string;
  published?: string;
  metaLine?: string;
  featured?: boolean;
  comingSoon?: boolean;
  stat?: { value: string; unit: string };
};

export const blogCategories: { id: BlogCategoryId; label: string }[] = [
  { id: "all", label: "הכל" },
  { id: "comparisons", label: "השוואות" },
  { id: "ingredients", label: "רכיבים" },
  { id: "processing", label: "עיבוד" },
  { id: "israeli-shelf", label: "מדף ישראלי" },
  { id: "bari-labs", label: "Bari Labs" },
];

export const blogIndex = blogIndexData.blogIndex;

export const featuredArticle: BlogArticleCard = blogIndexData.featuredArticle as BlogArticleCard;

export const secondaryArticles: BlogArticleCard[] = blogIndexData.secondaryArticles as BlogArticleCard[];

export function articleMatchesCategory(
  article: BlogArticleCard,
  category: BlogCategoryId
): boolean {
  if (category === "all") return true;
  return article.category === category;
}
