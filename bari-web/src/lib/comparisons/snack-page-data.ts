import type {
  SnackClusterId,
  SnackFilterId,
  SnackProduct,
} from "@/lib/comparisons/snack-types";

export const SNACK_REPORT_STATS = {
  scraped: 53,
  scored: 48,
  insufficient: 5,
  displayed: 18,
  scoreRange: "13–70",
  gradeBCount: 1,
  retailer: "יוחננוף",
  snapshotDate: "מאי 2026",
} as const;

function makeProduct(
  data: Omit<SnackProduct, "confidence_level" | "confidence_label_he"> & {
    confidence: SnackProduct["confidence_level"];
  }
): SnackProduct {
  const confidenceLabel =
    data.confidence === "full"
      ? "נתונים מלאים יחסית"
      : data.confidence === "partial"
        ? "נתונים חלקיים"
        : "לא מספיק לניתוח ודאי";

  return {
    ...data,
    confidence_level: data.confidence,
    confidence_label_he: confidenceLabel,
  };
}

export const snackProducts: SnackProduct[] = [
  makeProduct({
    id: "snk-001",
    name_he: "חטיף תמרים במילוי חמאת שקדים",
    brand: "Free",
    segment: "חטיפי תמרים",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498870_s1_0004-09-2026_10-52-18.jpg",
    ingredient_count: 4,
    score: 70,
    grade: "B",
    displayable: true,
    confidence: "full",
    nova: 2,
    structural_base: "בסיס שלם",
    sweetener_pattern: "מקור יחיד",
    additive_load: "0–2",
    positioning: "טבעי/תמרים",
    key_observation_he: "4 רכיבים בלבד, תמרים כרכיב ראשון וללא סוכר מוסף.",
    explainability_tags: ["בסיס שלם", "עיבוד מינימלי", "תמרים ראשונים"],
    caps_applied: [],
    cluster_id: "date-simple",
    x: 16,
    y: 18,
  }),
  makeProduct({
    id: "snk-002",
    name_he: "חטיף תמרים בציפוי שוקולד 100% קקאו",
    brand: "Free",
    segment: "חטיפי תמרים",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498948_s1_1505-10-2020_23-00-27.jpg",
    score: 57,
    grade: "C",
    displayable: true,
    confidence: "full",
    nova: 2,
    structural_base: "בסיס שלם",
    sweetener_pattern: "מקור יחיד",
    additive_load: "0–2",
    positioning: "טבעי/תמרים",
    key_observation_he: "בסיס תמרים פשוט עם ציפוי קקאו, ללא ריבוי ממתיקים.",
    explainability_tags: ["בסיס שלם", "ציפוי שוקולד", "ללא ריבוי ממתיקים"],
    caps_applied: [],
    cluster_id: "date-simple",
    x: 20,
    y: 24,
  }),
  makeProduct({
    id: "snk-003",
    name_he: "קראנצ'י שיבולת שועל עם דבש",
    brand: "Nature Valley",
    segment: "חטיפי גרנולה ושיבולת שועל",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/0/1/016000548404_s1_1512-29-2024_06-37-26.jpg",
    score: 53,
    grade: "C",
    displayable: true,
    confidence: "full",
    nova: 3,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "2 מקורות",
    additive_load: "3–4",
    positioning: "ללא מיצוב",
    key_observation_he: "שיבולת שועל בולטת אך עיבוד בינוני ותוספות מתונות מורידים ציון.",
    explainability_tags: ["עיבוד בינוני", "שיבולת שועל", "3–4 תוספות"],
    caps_applied: [],
    cluster_id: "granola-oat",
    x: 42,
    y: 41,
  }),
  makeProduct({
    id: "snk-004",
    name_he: "מרבה סלים דליס שוקולד מריר",
    brand: "Slim Delice",
    segment: "חטיפי \"סלים\" / רב-דגן",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8423207206495_h105-15-2023_13-17-20.jpg",
    score: 59,
    grade: "C",
    displayable: true,
    confidence: "partial",
    nova: 3,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "2 מקורות",
    additive_load: "3–4",
    positioning: "פיטנס",
    key_observation_he: "בסיס רב-דגן עם עיבוד בינוני; טוב יותר ממרבית המדף אך לא פשוט.",
    explainability_tags: ["עיבוד בינוני", "בסיס מעובד", "מיצוב פיטנס"],
    caps_applied: [],
    cluster_id: "granola-oat",
    x: 46,
    y: 43,
  }),
  makeProduct({
    id: "snk-005",
    name_he: "חטיפי דגנים פיטנס קלאסי",
    brand: "Fitness",
    segment: "חטיפי \"סלים\" / רב-דגן",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12505889_5900020039590.jpg",
    score: 46,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פיטנס",
    key_observation_he: "קמח + סירופ כבסיס, עיבוד מרבי וריבוי תוספות למרות מיצוב פיטנס.",
    explainability_tags: ["עיבוד מרבי", "ריבוי ממתיקים", "5+ תוספות"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55", "5+ תוספות — cap 60"],
    cluster_id: "fitness",
    x: 78,
    y: 72,
  }),
  makeProduct({
    id: "snk-006",
    name_he: "פיטנס בר גרנולה שוקולד מריר",
    brand: "Fitness",
    segment: "חטיפי דגנים מצופי שוקולד",
    ingredient_count: 14,
    score: 17,
    grade: "E",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פיטנס",
    key_observation_he: "אותו מדף גרנולה, אבל בסיס מהונדס מאוד עם עומס תוספות גבוה.",
    explainability_tags: ["עיבוד מרבי", "בסיס מהונדס", "5+ תוספות"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "coated-cereal",
    x: 88,
    y: 88,
  }),
  makeProduct({
    id: "snk-007",
    name_he: "חטיפי דגנים פיטנס שוקולד מריר",
    brand: "Fitness",
    segment: "חטיפי דגנים מצופי שוקולד",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12506828_5900020015174.jpg",
    score: 28,
    grade: "E",
    displayable: true,
    confidence: "partial",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פיטנס",
    key_observation_he: "ציפוי שוקולד מעל בסיס מהונדס עם ריבוי ממתיקים.",
    explainability_tags: ["עיבוד מרבי", "ריבוי ממתיקים", "ציפוי שוקולד"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "coated-cereal",
    x: 84,
    y: 84,
  }),
  makeProduct({
    id: "snk-008",
    name_he: "חטיפי דגנים פיטנס שוקולד בננה",
    brand: "Fitness",
    segment: "חטיפי דגנים מצופי שוקולד",
    score: 22,
    grade: "E",
    displayable: false,
    confidence: "partial",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פיטנס",
    key_observation_he: "מיצוב פיטנס עם ריבוי תוספות וסוכרים במערכת ציפוי.",
    explainability_tags: ["עיבוד מרבי", "5+ תוספות", "מיצוב פיטנס"],
    caps_applied: ["עיבוד מרבי — cap 68"],
    cluster_id: "coated-cereal",
    x: 86,
    y: 86,
  }),
  makeProduct({
    id: "snk-009",
    name_he: "נייצ'ר וואלי פרוטאין בוטנים ושוקולד",
    brand: "Nature Valley",
    segment: "חטיפי פרוטאין",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610379_s1_15_gs102-19-2024_08-41-10.jpg",
    ingredient_count: 15,
    score: 47,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פרוטאין",
    key_observation_he: "מיצוב פרוטאין עם מערכת רכיבים מהונדסת ועומק עיבוד גבוה.",
    explainability_tags: ["עיבוד מרבי", "ריכוז חלבון", "5+ תוספות"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "protein",
    x: 80,
    y: 68,
  }),
  makeProduct({
    id: "snk-010",
    name_he: "נייצ'ר וואלי פרוטאין בוטנים קרמל מלוח",
    brand: "Nature Valley",
    segment: "חטיפי פרוטאין",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610386_s1_15_gs102-19-2024_08-21-37.jpg",
    score: 46,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פרוטאין",
    key_observation_he: "אותו דפוס פרוטאין ממותג: עיבוד מרבי ועומס תוספות.",
    explainability_tags: ["עיבוד מרבי", "ריכוז חלבון", "ריבוי ממתיקים"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "protein",
    x: 79,
    y: 70,
  }),
  makeProduct({
    id: "snk-011",
    name_he: "פרי מארז תמרים ואגוזי לוז",
    brand: "פרי מארז",
    segment: "חטיפי תמרים",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290111936784_s104-01-2025_21-19-00.jpg",
    score: 44,
    grade: "D",
    displayable: true,
    confidence: "partial",
    nova: 4,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "3+ מקורות",
    additive_load: "3–4",
    positioning: "טבעי/תמרים",
    key_observation_he: "תמרים בשם אך עומק עיבוד גבוה וסוכרים מוספים ברשימה.",
    explainability_tags: ["טבעי מול הרכב", "עיבוד מרבי", "ריבוי ממתיקים"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "natural-gap",
    x: 66,
    y: 60,
  }),
  makeProduct({
    id: "snk-012",
    name_he: "פרי מארז תמרים ושברי קקאו",
    brand: "פרי מארז",
    segment: "חטיפי תמרים",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290111937262_s104-01-2025_21-21-11.jpg",
    score: 42,
    grade: "D",
    displayable: true,
    confidence: "partial",
    nova: 4,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "3+ מקורות",
    additive_load: "3–4",
    positioning: "טבעי/תמרים",
    key_observation_he: "מיצוב טבעי עם קקאו, אבל עיבוד מרבי ועומס סוכרים מאחורי הקלעים.",
    explainability_tags: ["עיבוד מרבי", "סוכר גבוה", "טבעי מול הרכב"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "natural-gap",
    x: 68,
    y: 62,
  }),
  makeProduct({
    id: "snk-013",
    name_he: "שחור ולבן קורני שוקולד",
    brand: "Corny",
    segment: "חטיפי דגנים מצופי שוקולד",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/4/0/4011800633516.jpg",
    score: 17,
    grade: "E",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "אנרג'י",
    key_observation_he: "עיבוד מרבי, ריבוי ממתיקים ותוספות.",
    explainability_tags: ["עיבוד מרבי", "ריבוי ממתיקים", "5+ תוספות"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55", "5+ תוספות — cap 60"],
    cluster_id: "coated-cereal",
    x: 92,
    y: 92,
  }),
  makeProduct({
    id: "snk-015",
    name_he: "חטיף תמרים במילוי חמאת בוטנים",
    brand: "Free",
    segment: "חטיפי תמרים",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290011498894_s1_0004-09-2026_11-01-01.jpg",
    score: 63,
    grade: "C",
    displayable: true,
    confidence: "full",
    nova: 2,
    structural_base: "בסיס שלם",
    sweetener_pattern: "מקור יחיד",
    additive_load: "0–2",
    positioning: "טבעי/תמרים",
    key_observation_he: "4 מרכיבים, בסיס תמרים-בוטנים נקי — 7 נקודות מתחת לגרסת השקדים; סוכר גבוה ממקור שלם.",
    explainability_tags: ["בסיס שלם", "עיבוד מינימלי", "תמרים ראשונים"],
    caps_applied: ["סוכר מפרי — cap 63 (מקור שלם)"],
    cluster_id: "date-simple",
    x: 22,
    y: 26,
  }),
  makeProduct({
    id: "snk-016",
    name_he: "מרבה סלים טופינג אגוזי לוז",
    brand: "Slim",
    segment: "חטיפי \"סלים\" / רב-דגן",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8423207210928_h105-15-2023_13-25-08.jpg",
    score: 51,
    grade: "C",
    displayable: true,
    confidence: "partial",
    nova: 3,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "2 מקורות",
    additive_load: "3–4",
    positioning: "פיטנס",
    key_observation_he: "גרסת הטופינג של מרבה סלים: אגוזי לוז על גבי בסיס דגן.",
    explainability_tags: ["עיבוד בינוני", "מיצוב פיטנס", "אגוזים אמיתיים"],
    caps_applied: [],
    cluster_id: "granola-oat",
    x: 48,
    y: 45,
  }),
  makeProduct({
    id: "snk-017",
    name_he: "נייצ'ר וואלי צ'ואי שוקולד מריר",
    brand: "Nature Valley",
    segment: "חטיפי פרוטאין",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076610508_s1_1503-02-2023_08-23-21.jpg",
    score: 39,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מהונדס",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פרוטאין",
    key_observation_he: "קו ה-Chewy של נייצ'ר וואלי — אותו מותג, 8 נקודות פחות מה-Protein.",
    explainability_tags: ["עיבוד מרבי", "סירופ ממתיק", "ריבוי מרכיבים"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "protein",
    x: 82,
    y: 75,
  }),
  makeProduct({
    id: "snk-018",
    name_he: "קראנצ'י שיבולת שועל עם חתיכות שוקולד",
    brand: "Nature Valley",
    segment: "חטיפי גרנולה ושיבולת שועל",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/8/4/8410076602251_s1_1512-29-2024_06-26-36.jpg",
    score: 44,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 3,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "2 מקורות",
    additive_load: "3–4",
    positioning: "ללא מיצוב",
    key_observation_he: "גרסת השוקולד של קראנצ'י — שיבולת שועל ראשון, אבל חתיכות שוקולד מורידות 7 נקודות.",
    explainability_tags: ["שיבולת שועל ראשון", "סוכר מוסף", "עיבוד בינוני"],
    caps_applied: [],
    cluster_id: "granola-oat",
    x: 52,
    y: 57,
  }),
  makeProduct({
    id: "snk-019",
    name_he: "חטיפי פיטנס שיבולת שועל דבש",
    brand: "Fitness",
    segment: "חטיפי \"סלים\" / רב-דגן",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/1/2/12615334_7290118247896.jpg",
    score: 40,
    grade: "D",
    displayable: true,
    confidence: "full",
    nova: 4,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "3+ מקורות",
    additive_load: "5+",
    positioning: "פיטנס",
    key_observation_he: "שיבולת שועל ודבש בשם — עיבוד מרבי וסירופ גלוקוז-פרוקטוז בהרכב.",
    explainability_tags: ["עיבוד מרבי", "סירופ ממתיק", "מיצוב פיטנס"],
    caps_applied: ["עיבוד מרבי — cap 68", "סוכר גבוה — cap 55"],
    cluster_id: "fitness",
    x: 76,
    y: 70,
  }),
  makeProduct({
    id: "snk-020",
    name_he: "מרבה סלים דליס קריספי אוכמניות",
    brand: "Slim",
    segment: "חטיפי \"סלים\" / רב-דגן",
    image_url:
      "https://api.yochananof.co.il/media/catalog/product/cache/7d40ab1d2c85da43a7701c1338d70a16/7/2/7290014525306_s105-31-2020_13-54-07.jpg",
    score: 33,
    grade: "E",
    displayable: true,
    confidence: "partial",
    nova: 3,
    structural_base: "בסיס מעובד",
    sweetener_pattern: "3+ מקורות",
    additive_load: "3–4",
    positioning: "פיטנס",
    key_observation_he: "גם מרבה סלים מגיע ל-E: קריספי עם סוכר גבוה ומרכיבים מפתיעים.",
    explainability_tags: ["עיבוד בינוני", "סוכר גבוה", "פער מיצוב"],
    caps_applied: ["סוכר גבוה — cap 55"],
    cluster_id: "granola-oat",
    x: 64,
    y: 63,
  }),
];

export function getSnackProduct(id: string) {
  return snackProducts.find((product) => product.id === id);
}

export const snackDisplayableProducts = snackProducts.filter((product) => product.displayable);
export const snackInsufficientProducts = snackProducts.filter((product) => !product.displayable);

export const SNACK_FILTERS: Array<{ id: SnackFilterId; label: string }> = [
  { id: "all", label: "הכל" },
  { id: "date-based", label: "תמרים/טבעי" },
  { id: "oat-cereal", label: "שיבולת שועל ודגנים" },
  { id: "wellness", label: "מיצוב בריאות" },
  { id: "grade-e", label: "ציון E" },
  { id: "insufficient", label: "לא נוקד" },
];

export function snackMatchesFilter(product: SnackProduct, filterId: SnackFilterId) {
  switch (filterId) {
    case "all":
      return product.displayable;
    case "date-based":
      return product.positioning === "טבעי/תמרים" && product.displayable;
    case "oat-cereal":
      return (product.cluster_id === "granola-oat" || product.cluster_id === "fitness") && product.displayable;
    case "wellness":
      return (product.positioning === "פרוטאין" || product.positioning === "פיטנס") && product.displayable;
    case "grade-e":
      return product.grade === "E" && product.displayable;
    case "insufficient":
      return !product.displayable;
    default:
      return true;
  }
}

export function snackConfidenceTone(level: SnackProduct["confidence_level"]) {
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
    default:
      return {
        pill: "border-[#8A8F98]/16 bg-[#EEF0F2] text-[#4E5663]",
        dot: "bg-[#8A8F98]",
      };
  }
}

export function formatSnackScore(product: Pick<SnackProduct, "score" | "grade" | "displayable">) {
  if (!product.displayable || product.score == null || !product.grade) {
    return "לא נוקד";
  }

  return `${Math.round(product.score)} / ${product.grade}`;
}

export const SNACK_CLUSTER_ORDER: SnackClusterId[] = [
  "date-simple",
  "granola-oat",
  "coated-cereal",
  "protein",
  "fitness",
  "natural-gap",
  "insufficient",
];

export const SNACK_CLUSTER_LABELS: Record<SnackClusterId, string> = {
  "date-simple": "חטיפי תמרים פשוטים",
  "granola-oat": "שיבולת שועל / גרנולה בינוניים",
  "coated-cereal": "מצופי שוקולד ודגנים",
  protein: "פרוטאין ממותג",
  fitness: "פיטנס / אנרג'י ממותגים",
  "natural-gap": "תמרים / טבעי עם פער הרכב",
  insufficient: "נתונים לא מספיקים",
};

export function snackClusterProducts(clusterId: SnackClusterId) {
  return snackProducts.filter((product) => product.cluster_id === clusterId);
}

export const snackExplainabilityLegend: Array<{
  key: string;
  direction: "strength" | "weakening" | "uncertainty";
}> = [
  { key: "בסיס שלם", direction: "strength" },
  { key: "עיבוד מינימלי", direction: "strength" },
  { key: "תמרים ראשונים", direction: "strength" },
  { key: "עיבוד מרבי", direction: "weakening" },
  { key: "עיבוד בינוני", direction: "weakening" },
  { key: "ריבוי ממתיקים", direction: "weakening" },
  { key: "5+ תוספות", direction: "weakening" },
  { key: "סוכר גבוה", direction: "weakening" },
  { key: "לא נוקד", direction: "uncertainty" },
];

export const flagshipComparisonIds = ["snk-001", "snk-009", "snk-006", "snk-011"] as const;

export const snackHeroLine =
  "חטיפי תמרים, גרנולה, פיטנס ופרוטאין על אותו מדף — עם פערים של עשרות נקודות באותה קטגוריה.";

export const snackMethodologyText =
  "ניתחנו 53 חטיפי דגנים, גרנולה, תמרים ופרוטאין ממדף יוחננוף (מאי 2026). 48 מוצרים קיבלו ציון ו-5 מוצרים סומנו כלא נוקד עקב נתונים חלקיים. 18 מוצרים נבחרו לתצוגה עריכתית על בסיס מגוון קטגוריות, פערי ציון משמעותיים ועניין צרכני. ההשוואה נשענת על עומק עיבוד, בסיס מבני, ארכיטקטורת סוכר, ועומס תוספות. ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.";

export const snackGlossary = [
  ["עיבוד מרבי", "מוצר עם מערכת תוספות ותהליכי שחזור תעשייתיים — בדרך כלל מעל 10 מרכיבים."],
  ["בסיס שלם", "כשהרכיב הראשון הוא מזון שלם כמו תמרים, אגוזים או שיבולת שועל שלמה."],
  ["ארכיטקטורת סוכר", "האם המתיקות נשענת על מקור אחד או על שכבות של סירופים וסוכרים מוספים."],
  ["עומס תוספות", "מספר תוספות פונקציונליות כמו מייצבים, מתחלבים ומשפרי טעם."],
  ["cap", "תקרת פרשנות שמופעלת כשנמצא דפוס סיכון עקבי כמו עיבוד מרבי או סוכר גבוה."],
  ["פער מיצוב", "פער בין השפה על האריזה לבין מה שמופיע בפועל ברשימת הרכיבים."],
  ["לא נוקד", "מוצר ללא נתוני רכיבים מספקים לחישוב עקבי."],
] as const;

export { SNACK_COMPARISON_HREF, snackComparisonMeta } from "@/lib/blog/snack-analysis-content";

