import {
  getCorpusBySlug,
  listPublicCorpusSlugs,
} from "@/lib/seo/public-corpus-registry";
import { absoluteUrl } from "@/lib/site-url";

export type ProductIndexEntry = {
  id: string;
  name: string;
  categorySlug: string;
  categoryPath: string;
  score: number | null;
  grade: string | null;
  brand: string | null;
  url: string;
  dataUrl: string;
};

function readString(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function readNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function productPageUrl(categoryPath: string, productId: string): string {
  const qs = new URLSearchParams({ product: productId }).toString();
  return absoluteUrl(`${categoryPath}?${qs}`);
}

export function buildProductsIndex(): ProductIndexEntry[] {
  const entries: ProductIndexEntry[] = [];

  for (const categorySlug of listPublicCorpusSlugs()) {
    const corpus = getCorpusBySlug(categorySlug);
    if (!corpus) continue;

    const products = corpus.products;
    if (!Array.isArray(products)) continue;

    const categoryPath = `/hashvaot/${categorySlug}`;

    for (const raw of products) {
      if (!raw || typeof raw !== "object") continue;
      const product = raw as Record<string, unknown>;
      const id = readString(product.id);
      const name = readString(product.name);
      if (!id || !name) continue;

      entries.push({
        id,
        name,
        categorySlug,
        categoryPath,
        score: readNumber(product.score),
        grade: readString(product.grade),
        brand: readString(product.brand),
        url: productPageUrl(categoryPath, id),
        dataUrl: absoluteUrl(`/data/comparisons/${categorySlug}/products/${id}`),
      });
    }
  }

  return entries;
}
