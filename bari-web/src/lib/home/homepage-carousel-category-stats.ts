/**
 * Grade distributions derived from live comparison JSON.
 */
import cerealsData from "@/data/comparisons/cereals_frontend_v2.json";
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

export const CEREALS_GRADE_DIST = deriveGradeDistribution(cerealsData.products, "\u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8");
export const GRANOLA_GRADE_DIST = deriveGradeDistribution(granolaData.products, "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D5\u05EA");

const hfcsRe = /\u05D2\u05DC\u05D5\u05E7\u05D5.?\u05E4\u05E8\u05D5\u05E7\u05D8\u05D5\u05D6|\u05E4\u05E8\u05D5\u05E7\u05D8\u05D5\u05D6.?\u05D2\u05DC\u05D5\u05E7\u05D5/;
const sugarTerms = ["\u05E1\u05D5\u05DB\u05E8", "\u05D3\u05D1\u05E9", "\u05D2\u05DC\u05D5\u05E7\u05D5\u05D6", "\u05E4\u05E8\u05D5\u05E7\u05D8\u05D5\u05D6", "\u05DE\u05D5\u05DC\u05E1\u05D4", "\u05D3\u05E7\u05E1\u05D8\u05E8\u05D5\u05D6"];

export const CEREALS_SUGAR_MASK_STATS = {
  surveyed: cerealsData.products.length,
  withHfcs: cerealsData.products.filter((p) => hfcsRe.test(p.expansion?.ingredients ?? "")).length,
  withHoneyLabel: cerealsData.products.filter((p) => (p.expansion?.ingredients ?? "").includes("\u05D3\u05D1\u05E9")).length,
  withMultipleSugarSources: cerealsData.products.filter((p) => {
    const ing = p.expansion?.ingredients ?? "";
    return sugarTerms.filter((t) => ing.includes(t)).length >= 2;
  }).length,
  spotlightProductId: "bsip1_cereal_7296073705567",
};