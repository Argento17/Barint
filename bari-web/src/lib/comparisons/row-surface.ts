import type { BariProductVM } from "@/lib/view-models";

// Shared row-surface enrichment (comparison_ui_reference_v2 §2.2 / §3.3). Factored out of
// hummus-comparison-page-data.ts so every category derives the row reason identically and
// cannot drift. Display-only — never a score input, never alters corpus content. The hummus
// page keeps its own local copy (frozen reference); this module mirrors that behavior
// verbatim for the remaining categories.

/**
 * Shorten a pre-authored signal line to a row-sized reason (§3.3). Deterministic: take the
 * clause before the first em-dash / colon, trimmed. The full string stays in the expansion.
 */
export function shortenReason(line: string | undefined): string | null {
  if (!line) return null;
  const head = line.split(/\s+[—–-]\s+|:\s+/)[0]?.trim();
  return head && head.length > 0 ? head : line.trim();
}

/**
 * Surface the already-present protein value as a first-class row metric and derive the row
 * reason from positiveSignals[0] / limitingFactors[0]. Identical to hummus's
 * enrichHummusRowSurface. Protein is read straight from expansion.nutrition; null is passed
 * through untouched (the metric column renders "—" for null) — never fabricated.
 */
export function enrichRowSurface(products: BariProductVM[]): BariProductVM[] {
  return products.map((product) => ({
    ...product,
    metrics: { protein_g: product.expansion.nutrition?.protein ?? null },
    rowReason: {
      positive: shortenReason(product.expansion.positiveSignals?.[0]),
      limiting: shortenReason(product.expansion.limitingFactors?.[0]),
    },
  }));
}

/**
 * rowReason-only enrichment for categories that must NOT show a metric bar (e.g. snacks,
 * where all nutrition is null — a bar would be fabricated). Derives the row reason exactly
 * like enrichRowSurface but leaves `metrics` untouched.
 */
export function enrichRowReasonOnly(products: BariProductVM[]): BariProductVM[] {
  return products.map((product) => ({
    ...product,
    rowReason: {
      positive: shortenReason(product.expansion.positiveSignals?.[0]),
      limiting: shortenReason(product.expansion.limitingFactors?.[0]),
    },
  }));
}
