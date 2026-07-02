import type { BariProductVM } from "@/lib/view-models";

// TASK-322: Updated to read _website_cluster from the product record itself
// (set by generate_page via copy_stage from the baseline corpus) instead of
// the legacy bread-retail-curated.json. Decouples the filter from the old
// bespoke data file.

// TASK-433: "crackers" lens removed — the 6 crackers products were split out of the
// bread corpus into their own /hashvaot/crackers category (bread_frontend_v4.json no
// longer contains any _website_cluster: "crackers" product, by design).
//
// TASK-435: the filter ids below previously referenced a stale cluster taxonomy
// (everyday/fermentation/strong/wellness_ambig) that matched ZERO products against
// bread_frontend_v4.json's actual _website_cluster values. Realigned 1:1 to the real
// clusters shipped in the JSON (verified by direct count against bread_frontend_v4.json,
// 23/23 products covered): high_protein(1) / wholegrain(7) / sourdough(4) / everyday(5) /
// wellness_ambig(1) / pita(2) / specialty(3). Hebrew labels kept human/consumer-facing
// (Frontend judgment call within lane — not Content-authored copy).
export type BreadShelfFilterId =
  | "high_protein"
  | "wholegrain"
  | "sourdough"
  | "everyday"
  | "wellness_ambig"
  | "pita"
  | "specialty";

export const BREAD_SHELF_LENS_OPTIONS: Array<{ id: BreadShelfFilterId; label: string }> = [
  { id: "everyday", label: "יומיומי" },
  { id: "wholegrain", label: "דגן מלא" },
  { id: "sourdough", label: "מחמצת" },
  { id: "high_protein", label: "עתיר חלבון" },
  { id: "pita", label: "פיתות" },
  { id: "specialty", label: "מיוחד" },
  { id: "wellness_ambig", label: "לחמי בריאות" },
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
