/**
 * Grade distributions derived from live comparison JSON.
 */
import cerealsData from "@/data/comparisons/cereals_frontend_v2.json";
import snacksData from "@/data/comparisons/snacks_frontend_v5.json";
import granolaData from "@/data/comparisons/granola_frontend_v2.json";
import type { GradeDistribution, GradeLetter } from "./homepage-carousel-schema";

const GRADE_ORDER: GradeLetter[] = ["A", "B", "C", "D", "E"];

function deriveGradeDistribution(
  products: Array<{ grade?: string; score?: number }>,
  label: string
): GradeDistribution {
  const grades: Record<GradeLetter, number> = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  const scores: number[] = [];
  for (const p of products) {
    if (p.grade && Object.prototype.hasOwnProperty.call(grades, p.grade)) grades[p.grade as GradeLetter]++;
    if (typeof p.score === "number") scores.push(p.score);
  }
  const low = scores.length ? Math.min(...scores) : 0;
  const high = scores.length ? Math.max(...scores) : 0;
  return {
    count: products.length,
    label,
    low: Math.round(low * 10) / 10,
    high: Math.round(high * 10) / 10,
    spread: Math.round((high - low) * 10) / 10,
    grades,
    gradeOrder: GRADE_ORDER,
  };
}

export const CEREALS_GRADE_DIST = deriveGradeDistribution(cerealsData.products, "דגני בוקר");
export const SNACKS_GRADE_DIST = deriveGradeDistribution(snacksData.products, "חטיפים");
export const GRANOLA_GRADE_DIST = deriveGradeDistribution(granolaData.products, "גרנולות");

const hfcsRe = /גלוקו.?פרוקטוז|פרוקטוז.?גלוקו/;
const sugarTerms = ["סוכר", "דבש", "גלוקוז", "פרוקטוז", "מולסה", "דקסטרוז"];

export const CEREALS_SUGAR_MASK_STATS = {
  surveyed: cerealsData.products.length,
  withHfcs: cerealsData.products.filter((p) => hfcsRe.test(p.expansion?.ingredients ?? "")).length,
  withHoneyLabel: cerealsData.products.filter((p) => (p.expansion?.ingredients ?? "").includes("דבש")).length,
  withMultipleSugarSources: cerealsData.products.filter((p) => {
    const ing = p.expansion?.ingredients ?? "";
    return sugarTerms.filter((t) => ing.includes(t)).length >= 2;
  }).length,
  spotlightProductId: "bsip1_cereal_7296073705567",
};
