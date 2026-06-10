import type { Metadata } from "next";

import type { BariProductVM } from "@/lib/view-models";

import type { ComparisonCorpusMeta } from "../corpus";

export type ComparisonCategoryId = "maadanim" | "bread" | "snacks" | "salty-snacks" | "yogurts" | "hummus" | "vegetable-spreads" | "cheese" | "breakfast-cereals" | "granola" | "butter" | "frozen-vegetables";

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
  metadata: Metadata;
  getPageData: () => ComparisonCategoryPageData<TFilterId>;
  getCorpusPayload: () => {
    _meta: ComparisonCorpusMeta;
    products: BariProductVM[];
  };
}
