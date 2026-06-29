import breadCorpus from "@/data/comparisons/bread_frontend_v3.json";
import breakfastCerealsCorpus from "@/data/comparisons/cereals_frontend_v2.json";
import brinedCheesesCorpus from "@/data/comparisons/brined_cheeses_frontend_v2.json";
import cakesCorpus from "@/data/comparisons/cakes_hard_cookies_frontend_v1.json";
import cheeseCorpus from "@/data/comparisons/cheese_frontend_v4.json";
import chocolateBarsCorpus from "@/data/comparisons/chocolate_bars_frontend_v1.json";
import chocolateTabletsCorpus from "@/data/comparisons/chocolate_tablets_frontend_v1.json";
import cookiesCoffeeCorpus from "@/data/comparisons/cookies_coffee_frontend_v2.json";
import granolaCorpus from "@/data/comparisons/granola_frontend_v1.json";
import hardCheesesCorpus from "@/data/comparisons/hard_cheeses_frontend_v2.json";
import hummusCorpus from "@/data/comparisons/hummus_frontend_v5.json";
import juicesCorpus from "@/data/comparisons/juices_frontend_v3.json";
import milkCorpus from "@/data/comparisons/milk_frontend_v1.json";
import proteinBarsCorpus from "@/data/comparisons/protein_combined_frontend_v2.json";
import snacksCorpus from "@/data/comparisons/snacks_frontend_v5.json";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";

const CORPUS_BY_SLUG: Record<string, Record<string, unknown>> = {
  bread: breadCorpus as Record<string, unknown>,
  "breakfast-cereals": breakfastCerealsCorpus as Record<string, unknown>,
  "brined-cheeses": brinedCheesesCorpus as Record<string, unknown>,
  cakes: cakesCorpus as Record<string, unknown>,
  cheese: cheeseCorpus as Record<string, unknown>,
  "chocolate-bars": chocolateBarsCorpus as Record<string, unknown>,
  "chocolate-tablets": chocolateTabletsCorpus as Record<string, unknown>,
  "cookies-coffee": cookiesCoffeeCorpus as Record<string, unknown>,
  granola: granolaCorpus as Record<string, unknown>,
  "hard-cheeses": hardCheesesCorpus as Record<string, unknown>,
  hummus: hummusCorpus as Record<string, unknown>,
  juices: juicesCorpus as Record<string, unknown>,
  magnesium: {
    _meta: {
      category: "magnesium",
      generated: "2026-06-23T00:00:00Z",
      product_count: magnesiumProducts.length,
    },
    products: magnesiumProducts,
  },
  "milk-comparison": milkCorpus as Record<string, unknown>,
  "protein-bars": proteinBarsCorpus as Record<string, unknown>,
  snacks: snacksCorpus as Record<string, unknown>,
};

export function getCorpusBySlug(slug: string): Record<string, unknown> | null {
  return CORPUS_BY_SLUG[slug] ?? null;
}

export function listPublicCorpusSlugs(): string[] {
  return Object.keys(CORPUS_BY_SLUG).sort();
}
