import type { Metadata } from "next";

import type { BariProductVM } from "@/lib/view-models";

import type { ComparisonCorpusMeta } from "../corpus";

export type ComparisonCategoryId = "bread" | "snacks" | "hummus" | "cheese" | "breakfast-cereals" | "granola" | "crackers";

export interface ComparisonShelfLensOption<TFilterId extends string = string> {
  id: TFilterId;
  label: string;
}

export interface ComparisonShelfFilters<TFilterId extends string = string> {
  lensOptions: ComparisonShelfLensOption<TFilterId>[];
  filterProducts: (
    products: BariProductVM[],
    activeFilters: TFilterId[]
  ) => BariProductVM[];
}

export interface ComparisonPageCopy {
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
}

export interface ComparisonCategoryPageData<TFilterId extends string = string>
  extends ComparisonPageCopy {
  products: BariProductVM[];
  metadataLine: string;
  corpusMeta: ComparisonCorpusMeta;
  shelfFilters: ComparisonShelfFilters<TFilterId>;
}

export interface ComparisonCategoryDefinition<TFilterId extends string = string> {
  id: ComparisonCategoryId;
  routePath: `/hashvaot/${string}`;
  /** Short Hebrew display name for the category. Required — TypeScript blocks any new
   *  category registration that omits it, so it can never be silently forgotten.
   *  Author a clean consumer-facing short name (e.g. "גבינות"), not a hero headline. */
  nameHe: string;
  metadata: Metadata;
  getPageData: () => ComparisonCategoryPageData<TFilterId>;
  getCorpusPayload: () => {
    _meta: ComparisonCorpusMeta;
    products: BariProductVM[];
  };
}
