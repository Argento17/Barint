import rawCorpus from "@/data/comparisons/cereals_frontend_v2.json";
import type { BariGrade } from "@/lib/view-models";

const VITABIX_ID = "bsip1_cereal_5010029000061";
const LYON_ID = "bsip1_cereal_5900020036407";

export interface CerealDuelProduct {
  id: string;
  name: string;
  brand: string;
  score: number;
  grade: BariGrade;
  sugarPer100g: number;
  fiberPer100g: number;
  imageUrl: string | null;
  imageAlt: string;
}

export interface FeaturedCerealDuel {
  title: string;
  eyebrow: string;
  matchupLine: string;
  verdict: string;
  insightStrip: string;
  bullets: string[];
  href: string;
  vitabix: CerealDuelProduct;
  lyon: CerealDuelProduct;
}

function findProduct(id: string): CerealDuelProduct | null {
  const products = (rawCorpus as { products: Record<string, unknown>[] }).products;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const p = products.find((x: any) => x.id === id) as any;
  if (!p) return null;
  return {
    id: p.id,
    name: p.name,
    brand: p.brand ?? "",
    score: Math.round(p.score),
    grade: (p.grade as BariGrade) ?? "C",
    sugarPer100g: p.expansion?.nutrition?.sugar ?? 0,
    fiberPer100g: p.expansion?.nutrition?.fiber ?? 0,
    imageUrl: p.imageUrl ?? null,
    imageAlt: p.name,
  };
}

export function getFeaturedCerealDuel(): FeaturedCerealDuel | null {
  const vitabix = findProduct(VITABIX_ID);
  const lyon = findProduct(LYON_ID);
  if (!vitabix || !lyon) return null;

  // Sugar teaspoons: ~4g per teaspoon. vitabix 4.2g -> ~1 tsp, lyon 24.7g -> ~6 tsp.
  const vitabixTsp = Math.round(vitabix.sugarPer100g / 4);
  const lyonTsp = Math.round(lyon.sugarPer100g / 4);

  const hasFiber = vitabix.fiberPer100g > 0 && lyon.fiberPer100g > 0;

  return {
    title: "אתם יודעים מה נמצא בדגני הבוקר שלכם?",
    eyebrow: "דגני בוקר",
    matchupLine:
      vitabix.brand +
      " מול " +
      lyon.brand +
      " — אותו מדף, תמונה אחרת לגמרי",
    verdict:
      vitabix.brand +
      " מקבל ציון " +
      vitabix.score +
      " — סוכר נמוך וסיבים גבוהים. " +
      lyon.brand +
      " עוצרת ב-" +
      lyon.score +
      " — בעיקר בגלל עומס הסוכר.",
    insightStrip:
      "כ-" +
      vitabixTsp +
      " כפית סוכר מול כ-" +
      lyonTsp +
      " כפיות ל-100 גרם",
    bullets: [
      vitabix.brand +
        ": " +
        vitabix.sugarPer100g.toFixed(1) +
        " גרם סוכר ל-100 גרם",
      lyon.brand +
        ": " +
        lyon.sugarPer100g.toFixed(1) +
        " גרם סוכר ל-100 גרם",
      hasFiber
        ? "סיבים תזונתיים: " +
          vitabix.fiberPer100g +
          " גרם מול " +
          lyon.fiberPer100g +
          " גרם ל-100 גרם"
        : "הפרש סוכר: " +
          (lyon.sugarPer100g - vitabix.sugarPer100g).toFixed(1) +
          " גרם ל-100 גרם",
    ],
    href: "/hashvaot/breakfast-cereals",
    vitabix,
    lyon,
  };
}
