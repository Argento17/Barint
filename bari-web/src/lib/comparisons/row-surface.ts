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
 * Surface the already-present protein value as a first-class row metric. Protein is read
 * straight from expansion.nutrition; null is passed through untouched (the metric column
 * renders "—" for null) — never fabricated. The collapsed row's text comes from the
 * authored insightLine sentence (TASK-167); the +/− positive/limiting signals remain in the
 * expansion and are shown when the row is opened.
 */
export function enrichRowSurface(products: BariProductVM[]): BariProductVM[] {
  return products.map((product) => ({
    ...product,
    metrics: { protein_g: product.expansion.nutrition?.protein ?? null },
    // The collapsed row shows the authored 2-line interpretive verdict (written into
    // insightLine, TASK-168). Routing it through rowVerdict renders it in the multi-line
    // verdict slot instead of the single-line truncated insightLine.
    rowVerdict: product.insightLine,
  }));
}

/**
 * Categories with no metric bar (e.g. snacks, where all nutrition is null — a bar would be
 * fabricated) need no row-surface enrichment: the collapsed row renders insightLine natively
 * (TASK-167). Kept as a passthrough so callers don't have to change.
 */
export function enrichRowReasonOnly(products: BariProductVM[]): BariProductVM[] {
  // No metric bar (e.g. snacks, all nutrition null), but route the authored verdict to the
  // multi-line rowVerdict slot (TASK-168) so the collapsed row shows it in full.
  return products.map((product) => ({
    ...product,
    rowVerdict: product.insightLine,
  }));
}
