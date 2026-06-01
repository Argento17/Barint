import type { BariProductVM } from "@/lib/view-models";

/** Shared corpus metadata shape for v2 frontend JSON exports. */
export interface ComparisonCorpusMeta {
  generated: string;
  category: string;
  product_count: number;
  scored_count?: number;
  schema?: string;
  version?: string;
  expansion?: string;
  v2_changes?: Record<string, unknown>;
  production_pass?: string;
}

export type ComparisonCorpusProduct = BariProductVM & {
  _calibration?: unknown;
};

export interface ComparisonCorpusRaw<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  _meta: TMeta;
  products: ComparisonCorpusProduct[];
}

export interface LoadedComparisonCorpus<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  meta: TMeta;
  products: BariProductVM[];
}

export function stripInternalProductFields(
  products: ComparisonCorpusProduct[]
): BariProductVM[] {
  return products.map((product) => {
    const { _calibration, ...rest } = product;
    void _calibration;
    return rest;
  });
}

export function loadComparisonCorpus<TMeta extends ComparisonCorpusMeta>(
  raw: ComparisonCorpusRaw<TMeta>
): LoadedComparisonCorpus<TMeta> {
  return {
    meta: raw._meta,
    products: stripInternalProductFields(raw.products),
  };
}

export function formatComparisonMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  const date = new Date(generatedIso);
  const monthYear = Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
  const updated = monthYear ? `עודכן ב${monthYear}` : "עודכן לאחרונה";
  return `${productCount} מוצרים • ${updated}`;
}
