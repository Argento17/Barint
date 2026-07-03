"use client";

/**
 * ProductExpansionClient — thin client boundary for <ExpansionSection/> on the
 * standalone /p/[barcode] page.
 *
 * Why this file exists: <ExpansionSection/> is itself a "use client" component
 * that takes an onCollapse callback. Functions cannot be passed as props from a
 * Server Component straight into a Client Component (they are not serializable
 * across the RSC boundary), so the page (a Server Component) cannot inline
 * `onCollapse={() => {}}` directly. This wrapper owns that no-op locally —
 * there is nothing to collapse on a standalone product page (no accordion), so
 * the close button becomes a no-op rather than being hidden (ExpansionSection
 * always renders its footer close affordance; hiding it would be a layout
 * change beyond this task's scope).
 *
 * Pure passthrough — no additional state, no data transformation.
 */

import { ExpansionSection } from "@/components/shared/expansion-section";
import type { BariProductVM } from "@/lib/view-models";
import type { ComparisonCategoryId } from "@/lib/comparisons/registry/types";

export function ProductExpansionClient({
  detail,
  categoryId,
}: {
  detail: BariProductVM;
  categoryId: ComparisonCategoryId;
}) {
  return (
    <ExpansionSection
      expansion={detail.expansion}
      confidence={detail.confidence}
      confidenceLabelHe={detail.confidence_label_he}
      confidenceTooltipHe={detail.confidence_tooltip_he}
      onCollapse={() => {}}
      category={categoryId}
      rowVerdict={detail.rowVerdict}
      consumerExplanation={detail.expansion.consumerExplanation}
      bestUseCases={detail.bestUseCases}
      consumerTakeaway={detail.consumerTakeaway}
      bariInterpretation={detail.bariInterpretation}
      rank={detail.rank}
      categoryTotal={detail.categoryTotal}
      glassBox={detail.glassBox}
      d4Additives={detail.d4_additives}
      d3Processing={detail.d3_processing}
      productId={detail.id}
      magnesiumBadges={detail.magnesiumBadges}
      wide
    />
  );
}
