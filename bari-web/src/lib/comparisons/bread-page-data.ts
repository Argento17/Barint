import rawData from "@/data/bread-retail-curated.json";

import type {
  BreadCategory,
  BreadClusterId,
  BreadComparisonPair,
  BreadConfidenceLabel,
  BreadConfidenceLevel,
  BreadDataset,
  BreadFilterId,
  BreadGrade,
  BreadInsightBlock,
  BreadProduct,
} from "./bread-types";

const dataset = rawData as BreadDataset;

function normalizeConfidenceLevel(label: BreadConfidenceLabel): BreadConfidenceLevel {
  switch (label) {
    case "נתונים מלאים יחסית":
      return "full";
    case "נתונים חלקיים":
      return "partial";
    case "חסרים נתונים מהותיים":
      return "missing";
    default:
      return "insufficient";
  }
}

function normalizeCategory(category?: string): BreadCategory {
  if (category === "bread" || category === "cracker" || category === "whole_food_fat") {
    return category;
  }

  if (category === "default") return "default";
  return "unknown";
}

function normalizeProduct(product: BreadDataset["all_products"][number]): BreadProduct {
  return {
    ...product,
    id: product.product_id,
    category: normalizeCategory(product._category_internal),
    category_label_he: product.category_display_he,
    displayable: product.display_score_boolean,
    confidence_level: normalizeConfidenceLevel(product.confidence_label_he),
  };
}

export const breadDataset = dataset;
export const breadMeta = dataset.meta;

export const BREAD_REPORT_STATS = {
  scanned: 256,
  sufficient: 81,
  featured: 31,
  transparencyGapPercent: 46,
} as const;

export const BREAD_CLUSTER_FILTERS: Array<{ id: BreadFilterId; label: string }> = [
  { id: "all", label: "הכל" },
  { id: "everyday", label: "יומיומי" },
  { id: "fermentation", label: "מחמצת" },
  { id: "strong", label: "מלא ודגנים" },
  { id: "wellness_ambig", label: "לחמי בריאות" },
  { id: "crackers", label: "קרקרים" },
];

export const breadProducts = dataset.all_products.map(normalizeProduct);

const productMap = new Map(breadProducts.map((product) => [product.id, product] as const));

function requireBreadProduct(id: string) {
  const product = productMap.get(id);
  if (!product) {
    throw new Error(`Bread product not found: ${id}`);
  }
  return product;
}

export function getBreadProductById(id: string) {
  return productMap.get(id);
}

export const breadProductsByCluster = dataset.clusters.reduce<Record<BreadClusterId, BreadProduct[]>>(
  (acc, cluster) => {
    acc[cluster.cluster_id] = cluster.products.map(normalizeProduct);
    return acc;
  },
  {
    everyday: [],
    strong: [],
    fermentation: [],
    wellness_ambig: [],
    crackers: [],
    transparency: [],
  }
);

export const breadScoredProducts = breadProducts.filter((product) => product.displayable);
export const breadTransparencyProducts = breadProductsByCluster.transparency;

export const breadHeroProducts = [
  "shufersal_497044",
  "shufersal_3268429",
  "shufersal_481203",
  "shufersal_7290016245325",
  "shufersal_96086000966",
]
  .map((id) => getBreadProductById(id))
  .filter((product): product is BreadProduct => Boolean(product));

export const flagshipBreadProducts = [
  "shufersal_497044",
  "shufersal_2079996",
  "shufersal_3268429",
  "shufersal_481203",
  "shufersal_7290016245325",
  "shufersal_96086000966",
]
  .map((id) => getBreadProductById(id))
  .filter((product): product is BreadProduct => Boolean(product));

export const breadInsightBlocks: BreadInsightBlock[] = [
  {
    id: "genuine-fermentation",
    title: "13 מוצרים כוללים \"מחמצת\" בשם — שמרים מופיעים לפני המחמצת",
    body:
      "מחמצת מצוינת בשם, אבל ברשימת הרכיבים שמרים תעשייתיים מופיעים קודם. לכן ההבדל המשמעותי הוא בין מה שכתוב על האריזה למה שמופיע בפועל ברשימה.",
    supporting: ["לחם ברמן אקטיב", "לחם מחמצת קמח מלא", "לחם מחמצת מכוסמין"],
  },
  {
    id: "everyday-surprises",
    title: "מוצרים יומיומיים פשוטים יצרו פערים ברורים על אותו מדף",
    body:
      "המדף לא מתחלק ליומיומי מול פרימיום. גם מוצרים שנראים פשוטים וגם מוצרים עם שם גדול נבדלו בעיקר לפי מה שמופיע ראשון ברשימת הרכיבים.",
    supporting: ["לחם אחיד פרוס קל", "לחם ברמן אקטיב", "לחם מחמצת אגוזים צימוקים"],
  },
  {
    id: "spelt-gap",
    title: "\"כוסמין\" ו-\"כוסמין מלא\" — לא אותו דבר",
    body:
      "כשהמילה \"מלא\" לא מופיעה לצד שם הדגן ברשימת הרכיבים, אי אפשר לאמת כוסמין מלא. שם המוצר לבדו לא פותר את הפער הזה.",
    supporting: ["לחם כוסמין לבן", "לחם מחמצת מכוסמין", "לחם שיפון מלא מסטמכר"],
  },
  {
    id: "data-gap",
    title: "46% מהמוצרים לא קיבלו מספיק נתונים",
    body:
      "רשימת רכיבים לא הייתה זמינה לציבור עבור חלק גדול מהמוצרים במדף, ולכן הם לא קיבלו ציון.",
    supporting: ["מארז פיתות אסליות", "לחם מחמצת אגוזים פרוס", "לחם אחיד"],
  },
];

export const breadComparisonPairs: BreadComparisonPair[] = [
  {
    id: "berman-vs-spelt-sourdough",
    title: "מיינסטרים מול תווית מחמצת",
    kicker: "ברמן אקטיב מול מחמצת כוסמין",
    caption:
      "לחם ברמן אקטיב מציג מחמצת ברכיבים ומבנה יציב יותר. מולו, לחם מחמצת מכוסמין נשען על שם שמבטיח מחמצת, אבל ברכיבים מופיעים שמרים תעשייתיים.",
    left: requireBreadProduct("shufersal_497044"),
    right: requireBreadProduct("shufersal_6451507"),
  },
  {
    id: "plain-vs-premium-nuts",
    title: "לחם פשוט מול לחם פרימיום",
    kicker: "אחיד פרוס קל מול אגוזים וצימוקים",
    caption:
      "לחם אחיד פרוס קל קיבל ציון גבוה יותר ועם יותר סיבים. זה מראה ששם פרימיום לא מחליף את מה שמופיע בפועל ברשימת הרכיבים.",
    left: requireBreadProduct("shufersal_2079996"),
    right: requireBreadProduct("shufersal_6451484"),
  },
  {
    id: "spelt-vs-white-spelt",
    title: "כוסמין מול כוסמין לבן",
    kicker: "אותו דגן, ציפייה אחרת",
    caption:
      "כוסמין לבן לא אומר כוסמין מלא, ושם שמזכיר כוסמין לא בהכרח מגובה באותו בסיס ברשימת הרכיבים.",
    left: requireBreadProduct("shufersal_6451507"),
    right: requireBreadProduct("shufersal_7290018500316"),
  },
];

export const breadStandoutProducts = [
  "shufersal_3268429",
  "shufersal_481203",
  "shufersal_3054183",
  "shufersal_2079927",
  "shufersal_3268252",
  "shufersal_481197",
  "shufersal_574370",
]
  .map((id) => getBreadProductById(id))
  .filter((product): product is BreadProduct => Boolean(product));

export function formatBreadScoreLine(
  product: Pick<BreadProduct, "score" | "grade" | "displayable">
): string | null {
  if (product.score == null || !product.displayable || !product.grade) {
    return null;
  }

  return `${Math.round(product.score)} / ${product.grade}`;
}

function sanitizeBreadBlurb(blurb: string) {
  const cleaned = blurb
    .replace(/ציון\s+[^.—–]+/gi, "")
    .replace(/\b(חזק|חלש|בינוני|טוב|מצוין|נמוך)(\-[א-ת]+)?\b/gi, "")
    .replace(/\s{2,}/g, " ")
    .trim();

  return cleaned.split(/[.—–]/)[0]?.trim() ?? "";
}

export function breadScoreObservation(
  product: Pick<
    BreadProduct,
    | "fermentation_status_he"
    | "fiber_source_status_he"
    | "structural_summary_he"
    | "suggested_card_blurb_he"
  >
) {
  if (product.fermentation_status_he.startsWith("מחמצת אמיתית")) {
    return "מחמצת מופיעה ברכיבים";
  }

  if (product.fermentation_status_he === "מחמצת בשם, שמרים ברכיבים") {
    return "מחמצת בשם · שמרים ברכיבים";
  }

  if (product.fermentation_status_he === "שמרים תעשייתיים בלבד") {
    return "שמרים תעשייתיים ברכיבים";
  }

  const fiberSource = product.fiber_source_status_he?.trim();
  if (fiberSource && fiberSource !== "מקור הסיבים לא ברור") {
    return fiberSource;
  }

  const summaryParts = product.structural_summary_he
    .split("|")
    .map((part) => part.trim())
    .filter(Boolean);

  const informative = summaryParts.find(
    (part) =>
      !part.startsWith("בסיס קמח מזוקק") &&
      !part.startsWith("בסיס קמח לבן") &&
      !part.includes("אפקט הילה") &&
      !part.startsWith("שמרים תעשייתיים")
  );

  if (informative) {
    return informative
      .replace(/^תסיסת /, "")
      .replace(/^עשיר בסיבים/, "סיבים גבוהים ברשימה");
  }

  const blurb = sanitizeBreadBlurb(product.suggested_card_blurb_he);
  if (blurb) return blurb;

  return summaryParts[0] ?? "נתונים חלקיים";
}

export function breadCategoryLabel(product: Pick<BreadProduct, "category" | "category_label_he">) {
  if (product.category_label_he) return product.category_label_he;
  if (product.category === "bread") return "לחם";
  if (product.category === "cracker") return "קרקר";
  if (product.category === "whole_food_fat") return "לחם / מוצר שמן";
  return "מוצר מדף";
}

export function gradeTone(grade: BreadGrade | null) {
  switch (grade) {
    case "A":
      return "border-[#1F8F6A]/15 bg-[#E8F5EF] text-[#176F53]";
    case "B":
      return "border-[#2D5BFF]/12 bg-[#EEF3FF] text-[#2442B5]";
    case "C":
      return "border-[#C98A00]/14 bg-[#FBF4DE] text-[#8F6600]";
    case "D":
    case "E":
      return "border-[#D1583D]/14 bg-[#FDECE8] text-[#A63F2A]";
    default:
      return "border-black/[0.08] bg-[#F3F4F5] text-[#5E6672]";
  }
}

export function confidenceTone(level: BreadConfidenceLevel) {
  switch (level) {
    case "full":
      return {
        pill: "border-[#1F8F6A]/18 bg-[#E8F5EF] text-[#176F53]",
        dot: "bg-[#1F8F6A]",
      };
    case "partial":
      return {
        pill: "border-[#C98A00]/16 bg-[#FBF4DE] text-[#8F6600]",
        dot: "bg-[#C98A00]",
      };
    case "missing":
      return {
        pill: "border-[#D8743C]/16 bg-[#FDECE8] text-[#A54A22]",
        dot: "bg-[#D8743C]",
      };
    default:
      return {
        pill: "border-[#8A8F98]/16 bg-[#EEF0F2] text-[#4E5663]",
        dot: "bg-[#8A8F98]",
      };
  }
}

export function getConfidenceLabel(
  product: Pick<BreadProduct, "confidence_label_he">
) {
  return product.confidence_label_he;
}

export function formatBreadNumber(value: number | null, suffix = "") {
  if (value == null) return "אין נתון";
  const formatted = Number.isInteger(value) ? `${value}` : `${value.toFixed(1)}`;
  return `${formatted}${suffix}`;
}

export function fermentationSignal(status: BreadProduct["fermentation_status_he"]) {
  switch (status) {
    case "מחמצת אמיתית (מזוהה ברכיבים)":
      return { icon: "✅", label: "מחמצת ברכיבים" };
    case "מחמצת אמיתית (עם שמרים עזר)":
      return { icon: "✅", label: "מחמצת + שמרים עזר" };
    case "מחמצת בשם, שמרים ברכיבים":
      return {
        icon: "⚠️",
        label: "שמרים ברכיבים",
        tooltip:
          "שם המוצר מכיל 'מחמצת', אך רשימת הרכיבים מציגה שמרים תעשייתיים — לא מחמצת ברכיבים.",
      };
    case "שמרים תעשייתיים בלבד":
      return { icon: "○", label: "שמרים תעשייתיים" };
    case "לא ידוע — חסרים נתוני רכיבים":
      return { icon: "—", label: "לא ידוע" };
    default:
      return { icon: "—", label: "לא רלוונטי" };
  }
}

export function breadProductMatchesFilter(product: BreadProduct, filter: BreadFilterId) {
  if (filter === "all") return product.website_cluster !== "transparency";
  return product.website_cluster === filter;
}

export function clusterProducts(filter: BreadFilterId) {
  return breadScoredProducts.filter((product) => breadProductMatchesFilter(product, filter));
}
