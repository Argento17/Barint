"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { DAIRY_PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterCheeseProducts,
  CHEESE_SHELF_LENS_OPTIONS,
  type CheeseShelfFilterId,
} from "@/lib/comparisons/cheese-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface CheeseComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** The 2 Sec 6.4 disclosures + labaneh n=1 condition, shown once in the header. */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const cheeseShelfFilters = {
  lensOptions: CHEESE_SHELF_LENS_OPTIONS,
  filterProducts: filterCheeseProducts,
} as const;

// Protein is the cheese row metric (TASK-161A). Uses the dairy-tuned scale
// (DAIRY_PROTEIN_METRIC, scaleMax 8) rather than hummus's 0–20: white-cheese / cottage
// protein tops ~11.5g, so the hummus scale would flatten every bar (Nutrition note 161A #1).
const CHEESE_METRIC_SPECS = [DAIRY_PROTEIN_METRIC] as const;

export function CheeseComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CheeseComparisonPageProps) {
  return (
    <ComparisonPage<CheeseShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={cheeseShelfFilters}
      metricSpecs={CHEESE_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
