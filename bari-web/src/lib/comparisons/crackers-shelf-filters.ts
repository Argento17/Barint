import type { BariProductVM } from "@/lib/view-models";

// TASK-433: crackers reads _website_cluster from the product record itself
// (a structural/data field added in crackers_frontend_v1.json — whole_grain-flour-%
// derived, no copy authored). Mirrors the bread shelf-filter pattern (TASK-322).

export type CrackersShelfFilterId = "whole_grain" | "mixed_grain" | "refined_white";

export const CRACKERS_SHELF_LENS_OPTIONS: Array<{ id: CrackersShelfFilterId; label: string }> = [
  { id: "whole_grain", label: "דגן מלא" },
  { id: "mixed_grain", label: "דגן מעורב" },
  { id: "refined_white", label: "קמח לבן" },
];

export function filterCrackersProducts(
  products: BariProductVM[],
  activeFilters: CrackersShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    // _website_cluster is an extension field carried through by loadComparisonCorpus.
    const cluster = (product as BariProductVM & { _website_cluster?: string })._website_cluster;
    return (
      cluster != null &&
      cluster !== "PENDING_COPY" &&
      activeFilters.includes(cluster as CrackersShelfFilterId)
    );
  });
}
