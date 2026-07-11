/**
 * PD → consumer-VM verdict adapter (TASK-620 / PD-3.1).
 *
 * THE CRUX of the human-readable Overview: the one-line "verdict" text lives
 * only in the published comparison view model (`BariProductVM.rowVerdict`),
 * never in the compiled Product Dossier. Per owner decision (Option A, thin
 * adapter): resolve the dossier's served barcode against the SAME resolver
 * `src/app/p/[barcode]/page.tsx` already uses (`getProductByBarcode`), and
 * render the real `<ComparisonRow>` against the real `BariProductVM` it
 * returns. This file does exactly that resolution — nothing else.
 *
 * SERVER-ONLY (imports the fs-reading inventory loader, same convention as
 * `./data.ts`). Never recomputes a score, never invents a verdict. If no
 * live-shelf match exists, callers must show an honest "no published verdict"
 * state — never a fabricated one.
 */
import { getProductByBarcode } from "@/lib/inventory/loader";
import type { BariProductVM } from "@/lib/view-models";
import type { ProductDossier } from "./types";

export type VerdictResolution =
  | {
      status: "matched";
      product: BariProductVM;
      categorySlug: string;
      categoryNameHe: string;
      comparisonHref: string;
      barcode: string;
    }
  | {
      status: "unmatched";
      reason: string;
    };

/**
 * Resolves a compiled dossier to the live BariProductVM it corresponds to, if
 * any. Barcode resolution order per the memo: prefer the served (unadjudicated)
 * barcode; fall back to the recovered GTIN. Neither present, or no match in the
 * live registry corpus (e.g. the product is on a legacy/quarantined shelf never
 * registered, or was dropped from the live corpus) → "unmatched".
 */
export function resolveVerdict(dossier: ProductDossier): VerdictResolution {
  const barcode =
    dossier.layer_1.barcode_state.served_barcode_unadjudicated ??
    dossier.layer_1.recovered_gtin;

  if (!barcode) {
    return {
      status: "unmatched",
      reason: "No served barcode or recovered GTIN on this dossier — nothing to resolve against the live catalog.",
    };
  }

  const entry = getProductByBarcode(barcode);
  if (!entry) {
    return {
      status: "unmatched",
      reason: `Barcode ${barcode} does not match any product in the live comparison catalog (not on a registered shelf, or dropped from the current corpus).`,
    };
  }

  return {
    status: "matched",
    product: entry.detail,
    categorySlug: entry.row.categoryId,
    categoryNameHe: entry.row.categoryNameHe,
    comparisonHref: entry.row.comparisonHref,
    barcode,
  };
}
