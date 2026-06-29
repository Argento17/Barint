import milkAnalysisArticleData from "@/data/blog/milk-analysis.json";

import { milkProducts } from "@/lib/comparisons/milk-page-data";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

export const MILK_COMPARISON_HREF = "/hashvaot/milk-comparison";

const PREVIEW_BARCODES = [
  "7290000051352",
  "7290116936116",
  "7394376619939",
  "5411188112709",
  "7290110324926",
  "8000215204219",
] as const;

export const milkAnalysisArticle = milkAnalysisArticleData;

export function getPreviewProducts(): MilkComparisonProduct[] {
  const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
  return PREVIEW_BARCODES.map((b) => byBarcode.get(b)).filter(
    (p): p is MilkComparisonProduct => p != null
  );
}

export function getPreviewTags(product: MilkComparisonProduct): string[] {
  const tags: string[] = [];

  if (product.additivesLabel.includes("ללא")) {
    tags.push("רכיבים פשוטים");
  } else {
    tags.push("יותר מייצבים");
  }

  const protein = product.proteinPer100ml ?? 0;
  if (protein >= 2.5) tags.push("חלבון גבוה");
  else if (protein < 1) tags.push("חלבון נמוך");

  if (product.sugarPer100ml != null && product.sugarPer100ml < 2) {
    tags.push("פחות סוכר");
  }

  const processing = product.dimensions.processing_quality?.score;
  if (processing != null && processing >= 85) {
    tags.push("רמת עיבוד נמוכה");
  }

  return [...new Set(tags)].slice(0, 3);
}

/** Products for simplicity ladder — spread from simple to complex */
export function getSimplicityLadderProducts(): MilkComparisonProduct[] {
  const barcodes = [
    "7290000051352",
    "7394376619939",
    "7290116936116",
    "5411188112709",
    "8000215204219",
  ];
  const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
  return barcodes
    .map((b) => byBarcode.get(b))
    .filter((p): p is MilkComparisonProduct => p != null);
}
