/**
 * Homepage carousel -- 7 cards using the strict CarouselCard schema.
 */

import type { CarouselCard } from "./homepage-carousel-schema";
import { CAROUSEL_PRODUCT_FALLBACK } from "./homepage-carousel-schema";
import {
  CEREALS_GRADE_DIST,
  GRANOLA_GRADE_DIST,
} from "./homepage-carousel-category-stats";

const CL =
  "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/";

export { CAROUSEL_PRODUCT_FALLBACK };

export const HOMEPAGE_CAROUSEL_CARDS: CarouselCard[] = [
  // -- Comparison 1: Bread -------------------------------------------------------
  {
    id: "comparison-bread-sourdough-vs-cracker",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "\u05D4\u05E9\u05D5\u05D5\u05D0\u05D4",
    category: "\u05DC\u05D7\u05DD \u05D5\u05DE\u05D0\u05E4\u05D9\u05DD",
    title: "\u05DE\u05D7\u05DE\u05E6\u05EA \u05E7\u05DE\u05D7 \u05DE\u05DC\u05D0 \u05DE\u05D5\u05DC \u05E7\u05E8\u05E7\u05E8 \u05E9\u05D5\u05DE\u05E9\u05D5\u05DD",
    evidence: "\u05D1\u05E7\u05E8\u05E7\u05E8: \u05E7\u05DE\u05D7 \u05DE\u05D6\u05D5\u05E7\u05E7 \u05DC\u05E4\u05E0\u05D9 \u05D4\u05E9\u05D5\u05DE\u05E9\u05D5\u05DD; \u05D1\u05DE\u05D7\u05DE\u05E6\u05EA: \u05E7\u05DE\u05D7 \u05DE\u05DC\u05D0 \u05D5\u05EA\u05E1\u05D9\u05E1\u05D4 \u05DE\u05DE\u05E9\u05D9\u05EA. \u05E4\u05E2\u05E8 \u05E9\u05DC \u05DB-29 \u05E0\u05E7\u05D5\u05D3\u05D5\u05EA, \u05D1\u05E2\u05D9\u05E7\u05E8 \u05D1\u05D6\u05DB\u05D5\u05EA \u05D4\u05E8\u05DB\u05D9\u05D1 \u05D4\u05E8\u05D0\u05E9\u05D5\u05DF.",
    metric: "89 \u05DE\u05D5\u05DC 60",
    href: "/hashvaot/bread",
    accent: "#6B7B5E",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "bsip1_bread_481203",
      barcode: "481203",
      name: "\u05DC\u05D7\u05DD \u05DE\u05D7\u05DE\u05E6\u05EA \u05E7\u05DE\u05D7 \u05DE\u05DC\u05D0",
      brand: "\u05D0\u05E8\u05E0\u05D4",
      score: 89,
      imageUrl: CL + "IUU18_Z_P_481203_1.png",
      imageAlt: "\u05DC\u05D7\u05DD \u05DE\u05D7\u05DE\u05E6\u05EA \u05E7\u05DE\u05D7 \u05DE\u05DC\u05D0 \u05D0\u05E8\u05E0\u05D4",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "bsip1_bread_74252",
      barcode: "74252",
      name: "\u05E7\u05E8\u05E7\u05E8 \u05E9\u05D5\u05DE\u05E9\u05D5\u05DD",
      brand: "\u05D0\u05E1\u05DD",
      score: 60,
      imageUrl: CL + "EUV20_Z_P_74252_1.png",
      imageAlt: "\u05E7\u05E8\u05E7\u05E8 \u05E9\u05D5\u05DE\u05E9\u05D5\u05DD \u05D0\u05E1\u05DD",
      imageStatus: "verified",
    },
  },

  // -- Comparison 2: Hummus duel (replaces milk) ---------------------------------
  {
    id: "comparison-hummus-tahini-rich-vs-lean",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "\u05D4\u05E9\u05D5\u05D5\u05D0\u05D4",
    category: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05D5\u05DE\u05DE\u05E8\u05D7\u05D9\u05DD",
    title: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05DE\u05E1\u05E2\u05D3\u05D5\u05EA \u05DE\u05D5\u05DC \u05DE\u05E1\u05D1\u05D7\u05D4",
    evidence: "31% \u05D8\u05D7\u05D9\u05E0\u05D4 \u05DE\u05D5\u05DC 10% \u2014 \u05D0\u05D5\u05EA\u05D5 \u05DE\u05D3\u05E3, \u05D4\u05E4\u05E8\u05E9 20 \u05E0\u05E7\u05D5\u05D3\u05D5\u05EA \u05E9\u05E0\u05E7\u05D1\u05E2 \u05D1\u05D9\u05D7\u05E1 \u05D4\u05D8\u05D7\u05D9\u05E0\u05D4 \u05DC\u05D7\u05D5\u05DE\u05D5\u05E1.",
    metric: "71 \u05DE\u05D5\u05DC 51",
    href: "/hashvaot/hummus",
    accent: "#8B7355",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "bsip1_7296073725404",
      barcode: "7296073725404",
      name: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05DE\u05E1\u05E2\u05D3\u05D5\u05EA",
      brand: "\u05D0\u05E1\u05DD",
      score: 71,
      imageUrl: CL + "IMV56_Z_P_7296073725404_1.png",
      imageAlt: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05DE\u05E1\u05E2\u05D3\u05D5\u05EA",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "bsip1_7296073725398",
      barcode: "7296073725398",
      name: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05DE\u05E1\u05D1\u05D7\u05D4",
      brand: "\u05D0\u05E1\u05DD",
      score: 51,
      imageUrl: CL + "IMP68_Z_P_7296073725398_1.png",
      imageAlt: "\u05D7\u05D5\u05DE\u05D5\u05E1 \u05DE\u05E1\u05D1\u05D7\u05D4",
      imageStatus: "verified",
    },
  },

  // -- Comparison 3: Granola -----------------------------------------------------
  {
    id: "comparison-granola-premium-vs-bottom",
    type: "comparison",
    visualMode: "product_duel",
    eyebrow: "\u05D4\u05E9\u05D5\u05D5\u05D0\u05D4",
    category: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4",
    title: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05D3\u05E0\u05D9 \u05D5\u05D2\u05DC\u05D9\u05EA \u05DE\u05D5\u05DC \u05E9\u05D5\u05E7 \u05E7\u05D5\u05DC\u05D9\u05E0\u05E8\u05D9",
    evidence: "\u05D1'\u05E9\u05D5\u05E7 \u05E7\u05D5\u05DC\u05D9\u05E0\u05E8\u05D9' \u05D4\u05E1\u05D5\u05DB\u05E8 \u05DE\u05E7\u05D3\u05D9\u05DD \u05D0\u05EA \u05E9\u05D9\u05D1\u05D5\u05DC\u05EA \u05D4\u05E9\u05D5\u05E2\u05DC. \u05D0\u05E6\u05DC \u05D3\u05E0\u05D9 \u05D5\u05D2\u05DC\u05D9\u05EA \u2014 \u05DC\u05D4\u05E4\u05DA. \u05E1\u05D3\u05E8 \u05D4\u05E8\u05DB\u05D9\u05D1\u05D9\u05DD \u05DE\u05E1\u05D1\u05D9\u05E8 \u05D7\u05DC\u05E7 \u05D2\u05D3\u05D5\u05DC \u05DE\u05E4\u05E2\u05E8 39 \u05D4\u05E0\u05E7\u05D5\u05D3\u05D5\u05EA.",
    metric: "70 \u05DE\u05D5\u05DC 31",
    href: "/hashvaot/granola",
    accent: "#8B7355",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    leftProduct: {
      productId: "bsip1_cereal_7290017962047",
      barcode: "7290017962047",
      name: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05D7\u05DE\u05D5\u05E6\u05D9\u05D5\u05EA \u05D5\u05E9\u05E7\u05D3\u05D9\u05DD",
      brand: "\u05D3\u05E0\u05D9 \u05D5\u05D2\u05DC\u05D9\u05EA",
      score: 70,
      imageUrl: CL + "ARO54_Z_P_7290017962047_1.png",
      imageAlt: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05D7\u05DE\u05D5\u05E6\u05D9\u05D5\u05EA \u05D5\u05E9\u05E7\u05D3\u05D9\u05DD \u05D3\u05E0\u05D9 \u05D5\u05D2\u05DC\u05D9\u05EA",
      imageStatus: "verified",
    },
    rightProduct: {
      productId: "bsip1_cereal_1343845",
      barcode: "1343845",
      name: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05E2\u05DD \u05E4\u05D9\u05E8\u05D5\u05EA",
      brand: "\u05E9\u05D5\u05E7 \u05E7\u05D5\u05DC\u05D9\u05E0\u05E8\u05D9",
      score: 31,
      imageUrl: CL + "KXI28_Z_P_1343845_1.png",
      imageAlt: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05E2\u05DD \u05E4\u05D9\u05E8\u05D5\u05EA \u05E9\u05D5\u05E7 \u05E7\u05D5\u05DC\u05D9\u05E0\u05E8\u05D9",
      imageStatus: "verified",
    },
  },

  // -- Product spotlight: Tahini bread -------------------------------------------
  {
    id: "spotlight-tahini-bread",
    type: "product_spotlight",
    visualMode: "product_single",
    eyebrow: "\u05DE\u05D5\u05E6\u05E8 \u05DE\u05D5\u05D1\u05D9\u05DC",
    category: "\u05DC\u05D7\u05DD \u05D5\u05DE\u05D0\u05E4\u05D9\u05DD",
    title: "\u05DC\u05D7\u05DD \u05D8\u05D7\u05D9\u05E0\u05D4 \u2014 \u05E6\u05D9\u05D5\u05DF 94",
    evidence: "\u05E6\u05D9\u05D5\u05DF 94 \u05DE\u05D1\u05D9\u05DF 29 \u05DC\u05D7\u05DE\u05D9\u05DD: \u05D8\u05D7\u05D9\u05E0\u05D4 \u05D1\u05D1\u05E1\u05D9\u05E1, \u05E7\u05DE\u05D7\u05D9 \u05D6\u05E8\u05E2\u05D9\u05DD, \u05DC\u05DC\u05D0 \u05E1\u05D5\u05DB\u05E8 \u05DE\u05D5\u05E1\u05E3 \u2014 \u05D4\u05E9\u05D9\u05DC\u05D5\u05D1 \u05D4\u05D9\u05D7\u05D9\u05D3\u05D9 \u05D1\u05DE\u05D3\u05E3.",
    metric: "94 / S",
    href: "/hashvaot/bread",
    accent: "#6B7B5E",
    fallbackVisual: CAROUSEL_PRODUCT_FALLBACK,
    spotlightProduct: {
      productId: "bsip1_bread_7290016245325",
      barcode: "7290016245325",
      name: "\u05DC\u05D7\u05DD \u05D8\u05D7\u05D9\u05E0\u05D4 \u05E4\u05E8\u05D5\u05E1",
      brand: "\u05DC\u05D7\u05DD \u05D0\u05E8\u05E5",
      score: 94,
      imageUrl: CL + "JDU46_Z_P_7290016245325_1.png",
      imageAlt: "\u05DC\u05D7\u05DD \u05D8\u05D7\u05D9\u05E0\u05D4 \u05E4\u05E8\u05D5\u05E1 \u05DC\u05D7\u05DD \u05D0\u05E8\u05E5",
      imageStatus: "verified",
    },
  },

  // -- Category report: Cereals (grade_histogram) --------------------------------
  {
    id: "category-report-cereals",
    type: "category_report",
    visualMode: "grade_histogram",
    eyebrow: "\u05D3\u05D5\u05D7 \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4",
    category: "\u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8",
    title: "\u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8: \u05D0\u05E4\u05E1 \u05E6\u05D9\u05D5\u05E0\u05D9 A",
    evidence: "20 \u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8, \u05D0\u05E4\u05E1 \u05E6\u05D9\u05D5\u05E0\u05D9 A \u2014 \u05D2\u05DD \u05D4\u05DE\u05D5\u05D1\u05D9\u05DC \u05E2\u05D5\u05E6\u05E8 \u05E2\u05DC B+. \u05D4\u05E1\u05D5\u05DB\u05E8 \u05D1\u05E8\u05DB\u05D9\u05D1 \u05D4\u05E9\u05E0\u05D9 \u05D0\u05D5 \u05D4\u05E9\u05DC\u05D9\u05E9\u05D9 \u05D1\u05E8\u05D5\u05D1 \u05D4\u05DE\u05D3\u05E3.",
    metric: "\u05D4\u05E4\u05E8\u05E9 " + CEREALS_GRADE_DIST.spread + " \u05E0\u05E7\u05D5\u05D3\u05D5\u05EA \u00B7 " + CEREALS_GRADE_DIST.grades.A + " \u05E6\u05D9\u05D5\u05E0\u05D9 A",
    href: "/hashvaot/breakfast-cereals",
    accent: "#7A8C5E",
    gradeDistribution: CEREALS_GRADE_DIST,
  },

  // -- Category report: Granola (grade_stacked) ----------------------------------
  {
    id: "category-report-granola",
    type: "category_report",
    visualMode: "grade_stacked",
    eyebrow: "\u05D3\u05D5\u05D7 \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4",
    category: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4",
    title: "\u05D2\u05E8\u05E0\u05D5\u05DC\u05D4 \u05D0\u05D5 \u05DE\u05DE\u05EA\u05E7?",
    evidence: "\u05DE\u05EA\u05D5\u05DA 22 \u05D2\u05E8\u05E0\u05D5\u05DC\u05D5\u05EA \u05E9\u05E0\u05E1\u05E8\u05E7\u05D5 \u2014 \u05D4\u05D4\u05E4\u05E8\u05E9 31\u201370 \u05E0\u05E7\u05D1\u05E2 \u05DB\u05E9\u05E1\u05D5\u05DB\u05E8, \u05E9\u05DE\u05DF \u05D5\u05E1\u05D9\u05E8\u05D5\u05E4 \u05D3\u05D5\u05D7\u05E4\u05D9\u05DD \u05D0\u05EA \u05D4\u05E9\u05D9\u05D1\u05D5\u05DC\u05EA \u05D4\u05E6\u05D9\u05D3\u05D4.",
    metric: "\u05E6\u05D9\u05D5\u05DF " + GRANOLA_GRADE_DIST.low + "\u2013" + GRANOLA_GRADE_DIST.high,
    href: "/hashvaot/granola",
    accent: "#8B7355",
    gradeDistribution: GRANOLA_GRADE_DIST,
  },

  // -- Category insight: Cereals whole-grain claim (claim_split) -----------------
  {
    id: "category-insight-cereals-whole-grain-claim",
    type: "category_report",
    visualMode: "claim_split",
    eyebrow: "\u05DE\u05DE\u05E6\u05D0 \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4",
    category: "\u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8",
    title: "\u05DB\u05D9\u05EA\u05D5\u05D1 '\u05D3\u05D2\u05DF \u05DE\u05DC\u05D0' \u2014 \u05E8\u05DB\u05D9\u05D1 \u05E8\u05D0\u05E9\u05D5\u05DF: \u05E7\u05DE\u05D7 \u05DE\u05D6\u05D5\u05E7\u05E7",
    evidence: "\u05D7\u05DC\u05E7 \u05DE\u05D3\u05D2\u05E0\u05D9 \u05D4\u05D1\u05D5\u05E7\u05E8 \u05DE\u05E6\u05D9\u05D2\u05D9\u05DD '\u05D3\u05D2\u05E0\u05D9\u05DD \u05DE\u05DC\u05D0\u05D9\u05DD' \u05D1\u05D7\u05D6\u05D9\u05EA \u2014 \u05D5\u05E8\u05E9\u05D9\u05DE\u05EA \u05D4\u05E8\u05DB\u05D9\u05D1\u05D9\u05DD \u05DE\u05D2\u05DC\u05D4 \u05E7\u05DE\u05D7 \u05DE\u05D6\u05D5\u05E7\u05E7 \u05D1\u05DE\u05E7\u05D5\u05DD \u05D4\u05E8\u05D0\u05E9\u05D5\u05DF. \u05D4\u05DB\u05D9\u05EA\u05D5\u05D1 \u05D4\u05E7\u05D3\u05DE\u05D9 \u05DC\u05D0 \u05DE\u05D7\u05D9\u05D9\u05D1 \u05E9\u05D4\u05D3\u05D2\u05DF \u05D4\u05DE\u05DC\u05D0 \u05D4\u05D5\u05D0 \u05D4\u05D3\u05D5\u05DE\u05D9\u05E0\u05E0\u05D8\u05D9.",
    metric: "0 \u05E6\u05D9\u05D5\u05E0\u05D9 A \u05DE\u05EA\u05D5\u05DA 20 \u05D3\u05D2\u05E0\u05D9 \u05D1\u05D5\u05E7\u05E8",
    href: "/hashvaot/breakfast-cereals",
    accent: "#7A8C5E",
    claimSplit: {
      packClaim: "\u05D3\u05D2\u05E0\u05D9\u05DD \u05DE\u05DC\u05D0\u05D9\u05DD",
      firstIngredient: "\u05E7\u05DE\u05D7 \u05EA\u05D9\u05E8\u05E1 / \u05E7\u05DE\u05D7 \u05DE\u05D6\u05D5\u05E7\u05E7",
    },
  },
];