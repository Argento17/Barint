/** Hero stage products -- Bari scanning a supermarket shelf. */
const CL =
  "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/";

export type ProductRole = "hero" | "support";

export interface StageProduct {
  id: string;
  name: string;
  imageUrl: string;
  imageAlt: string;
  role: ProductRole;
  /** Left-to-right slot index on the platform (0-based). */
  slot: number;
  /** Percent-based position within the canvas. */
  layout: {
    top: string;
    left: string;
    width: string;
    zIndex: number;
  };
}

export const HERO_STAGE_SCORE = { score: 75, grade: "B" as const };

/**
 * 5 products L to R on a soft oval platform:
 * granola | yogurt | [vitabix hero] | oat-milk | olive-oil
 * All rotate at the same -4deg: a real shelf scan, not a random collage.
 */
export const HERO_STAGE_PRODUCTS: StageProduct[] = [
  {
    id: "granola",
    name: "גרנולה",
    imageUrl: CL + "ARO54_Z_P_7290017962047_1.png",
    imageAlt: "גרנולה",
    role: "support",
    slot: 0,
    layout: { top: "36%", left: "3%", width: "22%", zIndex: 1 },
  },
  {
    id: "yogurt",
    name: "יוגורט",
    imageUrl: CL + "UVF46_Z_P_7290102393190_1.png",
    imageAlt: "יוגורט",
    role: "support",
    slot: 1,
    layout: { top: "40%", left: "22%", width: "22%", zIndex: 2 },
  },
  {
    id: "vitabix",
    name: "ויטביקס",
    imageUrl: CL + "KAG24_Z_P_5010029000061_1.png",
    imageAlt: "ויטביקס דגני בוקר",
    role: "hero",
    slot: 2,
    layout: { top: "10%", left: "35%", width: "30%", zIndex: 4 },
  },
  {
    id: "oat-milk",
    name: "משקה שיבולת שועל",
    imageUrl: CL + "BAC42_Z_P_5411188135005_1.png",
    imageAlt: "משקה שיבולת שועל",
    role: "support",
    slot: 3,
    layout: { top: "26%", left: "64%", width: "22%", zIndex: 2 },
  },
  {
    id: "olive-oil",
    name: "שמן זית",
    imageUrl: CL + "III56_Z_P_7290017334479_1.png",
    imageAlt: "שמן זית",
    role: "support",
    slot: 4,
    layout: { top: "30%", left: "78%", width: "20%", zIndex: 1 },
  },
];

/** @deprecated Use HERO_STAGE_PRODUCTS instead. */
export const HERO_STILL_LIFE_PRODUCTS = HERO_STAGE_PRODUCTS;
