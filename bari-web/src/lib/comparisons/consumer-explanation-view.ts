import { getProductInsight } from "@/lib/comparisons/milk-product-insights";
import type { BariInterpretationPillar, MilkComparisonProduct, ProductType } from "@/lib/comparisons/milk-types";

/** Consumer-facing copy — multidimensional, category-aware; scoring unchanged. */

const PLANT_TYPES: Set<ProductType> = new Set(["oat", "soy", "almond", "rice", "coconut", "other_plant"]);

type ReplacementRule = { pattern: RegExp; replacement: string; gentleProcessingOnly?: boolean };

const REPLACEMENTS: ReplacementRule[] = [
  { pattern: /ערך תזונתי נמוך יחסית/g, replacement: "פרופיל תזונתי דל יחסית בקטגוריה" },
  { pattern: /ערך תזונתי ביחס למוצר נמוך/g, replacement: "חלבון וסיבים לא בולטים מול דומים" },
  { pattern: /ערך תזונתי נמוך/g, replacement: "תרומה תזונתית צנועה" },
  { pattern: /עיבוד בינוני-גבוה/g, replacement: "רמת עיבוד מורגשת" },
  { pattern: /מעובד מאוד — הרבה רכיבים תפקודיים/g, replacement: "מורכבות רכיבים גבוהה יותר (רבים תפקודיים) בהשוואה לגרסאות פשוטות יותר", gentleProcessingOnly: true },
  { pattern: /מעובד מאוד/g, replacement: "עם רמת מורכבות/עיבוד גבוהה יותר", gentleProcessingOnly: true },
  { pattern: /מעובד בינוני — תהליך תעשייתי ברור/g, replacement: "רמת עיבוד נראית לעין — בהתאם למה שמקובל בהרבה מוצרים דומים", gentleProcessingOnly: true },
  { pattern: /עיבוד נמוך-בינוני — שינוי מתון מהמקור/g, replacement: "שינוי מתון מהמקור — רמת עיבוד בינונית-נמוכה", gentleProcessingOnly: true },
  { pattern: /תוספים: מווסתי חומציות, מייצב/g, replacement: "כולל רכיבים לוויסות חומציות ולשיפור מרקם ויציבות" },
  { pattern: /תוספים: מווסת חומציות, פוספט/g, replacement: "כולל רכיבים לוויסות חומציות ופוספטים (לרוב ליציבות)" },
  { pattern: /תוספים: לציטין סויה, מייצבים/g, replacement: "כולל לציטין סויה ומייצבים — טיפוסי למרקם במשקאות צמחיים" },
  { pattern: /תוספים: מווסת חומציות, אינולין/g, replacement: "כולל מווסת חומציות ואינולין בין הרכיבים" },
  { pattern: /תוספים: מווסת חומציות, מייצב/g, replacement: "כולל רכיבים לוויסות חומציות ומייצבים" },
  { pattern: /תוספים: מייצבים, לציטין/g, replacement: "כולל מייצבים ולציטין — טיפוסי לשיפור מרקם" },
  { pattern: /דל יחסית בחלבון וסיבים — יותר כמו משקה מאשר כמקור תזונה מלא/g, replacement: "חלבון וסיבים נמוכים יחסית — מתאים יותר כמשקה מאשר כמקור חלבון/סיבים מרכזי" },
  { pattern: /רשימה ארוכה יותר — יותר מייצבים, העשרה וטעמים/g, replacement: "רשימת רכיבים ארוכה יותר, עם מייצבים, העשרה וטעמים — נפוץ במשקאות מועשרים ומתוקתקים" },
  { pattern: /רמת עיבוד יחסית מתונה — בסיס ברור ברשימת הרכיבים/g, replacement: "מבנה רכיבים בהיר יחסית — בסיס מזוהה ברשימה" },
  {
    pattern: /חלבון בינוני \(1\.6 ג׳\) — לא מקור חלבון עיקרי/g,
    replacement:
      "חלבון בינוני (1.6 ג׳) — סביר למשקה, אך לא מדורג כמקור חלבון עיקרי לעומת חלופות עשירות חלבון",
  },
  {
    pattern: /חלבון נמוך \(([^)]+)\) — מתאים לטעם\/קלוריות, לא לשובע/g,
    replacement: "חלבון נמוך ($1) — מתאים לפרופיל קלוריות/טעם; שובע וחלבון לא מהמובילים כאן",
  },
];

function gentleProcessingLanguage(score: number): boolean {
  return score >= 48;
}

function applyReplacements(text: string, score: number): string {
  let out = text;
  const gentle = gentleProcessingLanguage(score);
  for (const { pattern, replacement, gentleProcessingOnly } of REPLACEMENTS) {
    if (gentleProcessingOnly && !gentle) continue;
    out = out.replace(pattern, replacement);
  }
  return out;
}

/** Opening nuance by score band — proportionate tone (§7). */
export function scoreBandNuance(score: number): string {
  if (score >= 85) return "הרכב פשוט יחסית עם מעט סימני עיבוד.";
  if (score >= 70) return "הרכב סביר יחסית לקטגוריה, עם כמה סימני עיבוד.";
  if (score >= 55) return "מוצר עם איזון בין תרומה תזונתית לבין מורכבות רכיבים מסוימת.";
  if (score >= 40) return "כולל יותר סימני עיבוד ותוספים ביחס למוצרים פשוטים יותר בקטגוריה.";
  return "ביחס למוצרים פשוטים יותר באותה קטגוריה, כאן יש יותר רכיבי תוסף ומורכבות רכיבים ניכרת.";
}

function plantCategorySentence(product: MilkComparisonProduct): string | null {
  if (!PLANT_TYPES.has(product.productType)) return null;
  return "במשקאות צמחיים מייצוב, תוספי מרקם והעשרה נפוצים — זה חלק מהציפיות בקטגוריה, לא בהכרח חריגה.";
}

function categoryPeerLabel(type: ProductType): string {
  switch (type) {
    case "dairy":
      return "חלב הפרה";
    case "soy":
      return "משקאות הסויה";
    case "oat":
      return "משקאות השיבולת";
    case "almond":
      return "משקאות השקדים";
    case "rice":
      return "משקאות האורז";
    case "coconut":
      return "משקאות הקוקוס";
    case "protein_drink":
      return "משקאות חלבון";
    default:
      return "מוצרים דומים ברשימה";
  }
}

function median(nums: number[]): number | null {
  if (nums.length === 0) return null;
  const a = [...nums].sort((x, y) => x - y);
  const m = Math.floor(a.length / 2);
  return a.length % 2 ? a[m]! : (a[m - 1]! + a[m]!) / 2;
}

/**
 * Relative comparison vs similar products (same type in list, fallback: full list).
 */
export function buildPeerComparisonSentence(
  product: MilkComparisonProduct,
  allProducts: MilkComparisonProduct[]
): string {
  const cohort =
    allProducts.filter((p) => p.productType === product.productType).length >= 2
      ? allProducts.filter((p) => p.productType === product.productType)
      : allProducts;

  const proteins = cohort
    .map((p) => p.proteinPer100ml)
    .filter((n): n is number => n != null && Number.isFinite(n));
  const sugars = cohort
    .map((p) => p.sugarPer100ml)
    .filter((n): n is number => n != null && Number.isFinite(n));

  const medP = median(proteins);
  const medS = median(sugars);
  const label = categoryPeerLabel(product.productType);
  const parts: string[] = [];

  if (product.proteinPer100ml != null && medP != null) {
    const d = product.proteinPer100ml - medP;
    if (Math.abs(d) < 0.2) {
      parts.push(`ביחס ל${label} בהשוואה הזו, רמת החלבון דומה לחציון.`);
    } else if (d > 0) {
      parts.push(`ביחס ל${label} ברשימה, יש כאן חלבון גבוה יותר מהרוב.`);
    } else {
      parts.push(`ביחס ל${label} ברשימה, יש כאן חלבון נמוך יותר מהרוב.`);
    }
  }

  if (product.sugarPer100ml != null && medS != null) {
    const d = product.sugarPer100ml - medS;
    if (Math.abs(d) < 0.35) {
      parts.push(`רמת הסוכר דומה לרוב המדגם באותה משפחה.`);
    } else if (d > 0) {
      parts.push(`רמת הסוכר גבוהה יותר ממרבית המדגם באותה משפחה.`);
    } else {
      parts.push(`רמת הסוכר נמוכה יותר ממרבית המדגם באותה משפחה.`);
    }
  }

  if (parts.length === 0) {
    return "ההשוואה כאן היא יחסית למוצרים מאותה משפחה ברשימה — לא מול כל סוגי המזונות.";
  }

  if (parts.length === 1) {
    return parts[0]!;
  }
  return parts.join(" ");
}

export type ConsumerExplanationView = {
  /** Short contextual summary */
  whatToKnow: string;
  /** Positive contributors */
  raisesScore: string[];
  /** Tradeoffs / complexity — not "warnings" */
  lowersScore: string[];
  /** Relative to similar SKUs */
  relativeToPeers: string;
  /** Optional tradeoff / closure from legacy context */
  tradeoffNote: string | null;
  /** One-line strip under the title */
  takeawayLine: string;
};

function uniqueLines(lines: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const line of lines) {
    const t = line.trim();
    if (!t || seen.has(t)) continue;
    seen.add(t);
    out.push(t);
  }
  return out;
}

export function buildConsumerExplanationView(
  product: MilkComparisonProduct,
  allProducts: MilkComparisonProduct[]
): ConsumerExplanationView {
  const curated = getProductInsight(product.barcode);
  if (curated) {
    return {
      whatToKnow: curated.whatMatters,
      raisesScore: curated.positives,
      lowersScore: curated.cautions,
      relativeToPeers: curated.comparisonContext,
      tradeoffNote: null,
      takeawayLine: curated.takeaway,
    };
  }

  const exp = product.consumerExplanation;
  const score = product.score;
  const plant = plantCategorySentence(product);
  const softenedWhy = applyReplacements(exp.whyRated, score);
  const nuance = scoreBandNuance(score);
  /** One contextual block: category note + nuance (dairy / general) + engine summary — avoid piling three intros. */
  const whatToKnow = plant
    ? `${plant} ${softenedWhy}`.trim()
    : `${nuance} ${softenedWhy}`.trim();

  const raisesScore = uniqueLines(exp.good.map((line) => applyReplacements(line, score)));

  const lowersScore = uniqueLines(exp.watchOut.map((line) => applyReplacements(line, score)));

  const tradeoffNote = exp.context.trim()
    ? applyReplacements(exp.context, score)
    : null;

  const relativeToPeers = buildPeerComparisonSentence(product, allProducts);

  const takeawayLine = applyReplacements(
    product.consumerTakeaway || exp.takeaway || "",
    score
  );

  return {
    whatToKnow,
    raisesScore,
    lowersScore,
    relativeToPeers,
    tradeoffNote,
    takeawayLine,
  };
}

/** Soften pillar blurbs for display — keeps scores/labels; wording only. */
export function mapPillarsForDisplay(
  pillars: BariInterpretationPillar[] | undefined,
  score: number
): BariInterpretationPillar[] | undefined {
  if (!pillars?.length) return pillars;

  return pillars.map((p) => ({
    ...p,
    interpretation: applyReplacements(p.interpretation, score),
    label: PILLAR_LABELS[p.key] ?? p.label,
  }));
}

const PILLAR_LABELS: Record<string, string> = {
  ingredients: "רשימת רכיבים ופשטות",
  processing: "מבנה ועיבוד (הקשרי)",
  density: "תרומה תזונתית בפרופיל",
  additives: "תוספים ומייצבים",
  sugar: "סוכר (כפי שמופיע)",
  protein: "חלבון ביחס למדף",
};
