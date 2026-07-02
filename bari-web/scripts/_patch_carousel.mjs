import { writeFileSync, readFileSync } from "fs";

const stats = `/**
 * Grade distributions derived from live comparison JSON.
 */
import cerealsData from "@/data/comparisons/cereals_frontend_v2.json";
import snacksData from "@/data/comparisons/snacks_frontend_v5.json";
import granolaData from "@/data/comparisons/granola_frontend_v2.json";
import type { GradeDistribution, GradeLetter } from "./homepage-carousel-schema";

const GRADE_ORDER = ["A", "B", "C", "D", "E"];

function deriveGradeDistribution(products, label) {
  const grades = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  const scores = [];
  for (const p of products) {
    if (p.grade && grades[p.grade] !== undefined) grades[p.grade]++;
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

export const CEREALS_GRADE_DIST = deriveGradeDistribution(cerealsData.products, "\u05d3\u05d2\u05e0\u05d9 \u05d1\u05d5\u05e7\u05e8");
export const SNACKS_GRADE_DIST = deriveGradeDistribution(snacksData.products, "\u05d7\u05d8\u05d9\u05e4\u05d9\u05dd");
export const GRANOLA_GRADE_DIST = deriveGradeDistribution(granolaData.products, "\u05d2\u05e8\u05e0\u05d5\u05dc\u05d5\u05ea");

const hfcsRe = /\u05d2\u05dc\u05d5\u05e7\u05d5.?\u05e4\u05e8\u05d5\u05e7\u05d8\u05d5\u05d6|\u05e4\u05e8\u05d5\u05e7\u05d8\u05d5\u05d6.?\u05d2\u05dc\u05d5\u05e7\u05d5/;
const sugarTerms = ["\u05e1\u05d5\u05db\u05e8", "\u05d3\u05d1\u05e9", "\u05d2\u05dc\u05d5\u05e7\u05d5\u05d6", "\u05e4\u05e8\u05d5\u05e7\u05d8\u05d5\u05d6", "\u05de\u05d5\u05dc\u05e1\u05d4", "\u05d3\u05e7\u05e1\u05d8\u05e8\u05d5\u05d6"];

export const CEREALS_SUGAR_MASK_STATS = {
  surveyed: cerealsData.products.length,
  withHfcs: cerealsData.products.filter((p) => hfcsRe.test(p.expansion?.ingredients ?? "")).length,
  withHoneyLabel: cerealsData.products.filter((p) => (p.expansion?.ingredients ?? "").includes("\u05d3\u05d1\u05e9")).length,
  withMultipleSugarSources: cerealsData.products.filter((p) => {
    const ing = p.expansion?.ingredients ?? "";
    return sugarTerms.filter((t) => ing.includes(t)).length >= 2;
  }).length,
  spotlightProductId: "bsip1_cereal_7296073705567",
};
`;

writeFileSync("src/lib/home/homepage-carousel-category-stats.ts", stats);
console.log("wrote stats");
