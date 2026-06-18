import type { BariProductVM } from "@/lib/view-models";

// TASK-322: Updated to read _website_cluster from the product record itself
// (set by generate_page via copy_stage from the baseline corpus) instead of
// the legacy bread-retail-curated.json. Decouples the filter from the old
// bespoke data file.

export type BreadShelfFilterId =
  | "everyday"
  | "fermentation"
  | "strong"
  | "wellness_ambig"
  | "crackers";

export const BREAD_SHELF_LENS_OPTIONS: Array<{ id: BreadShelfFilterId; label: string }> = [
  { id: "everyday", label: "יומיומי" },
  { id: "fermentation", label: "מחמצת" },
  { id: "strong", label: "מלא ודגנים" },
  { id: "wellness_ambig", label: "לחמי בריאות" },
  { id: "crackers", label: "קרקרים" },
];

export function filterBreadProducts(
  products: BariProductVM[],
  activeFilters: BreadShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    // _website_cluster is an extension field emitted by generate_page.
    // It is populated from the corpus baseline by copy_stage for carried products;
    // PENDING_COPY products will not match any filter (filtered out), which is
    // correct interim behavior until the content author fills it in.
    const cluster = (product as BariProductVM & { _website_cluster?: string })._website_cluster;
    return cluster != null && cluster !== "PENDING_COPY" && activeFilters.includes(cluster as BreadShelfFilterId);
  });
}
