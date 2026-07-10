"use client";

// GuideProductGroupsV3 — TASK-577 (magnesium guide v3, wiring phase).
//
// Renders `products` grouped by the SIGNED `groupV3` key (GUIDE_V3_GROUP_ORDER, per
// mag_guide_v3_structure_spec.md §A.3, D6+D7 co-signed), immediately after the intro
// + "what we found" box — no methodology section before them, no prose product
// summaries before the cards (dispatch item 3). Section headers are a flat, neutral,
// un-toned treatment — same idiom as v2's `GroupSectionHeader`
// (guide-product-table.tsx), reused rather than re-invented, since these are still
// descriptive sections, not a ranking.
//
// The guide-level market-information-gaps box (dispatch item 7 — "ONE occurrence of
// each explanation, not two") renders once, after the groups, using the SIGNED
// compact copy (mag_guide_v3_copy_package.md §4) — never the v2 4-sentence
// `suppressedBarsDisclosureHe`, which stays reserved for v2 rollback only.

import type {
  GuideBarKey,
  GuideProductVM,
  GuideThresholdGeometry,
  GuideV3Group,
} from "@/lib/view-models";
import { GUIDE_V3_GROUP_ORDER } from "@/lib/view-models";
import { GuideProductRowV3 } from "@/components/guides/guide-product-row-v3";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

function groupByV3(products: GuideProductVM[]): Record<GuideV3Group, GuideProductVM[]> {
  const groups: Record<GuideV3Group, GuideProductVM[]> = { g1: [], g2: [], g3: [], g4: [] };
  for (const product of products) {
    if (product.groupV3) groups[product.groupV3].push(product);
  }
  return groups;
}

function GroupSectionHeaderV3({ label, count }: { label: string; count: number }) {
  return (
    <div className="mb-3 flex items-center gap-2 rounded-xl">
      <h2
        className="inline-flex items-center whitespace-nowrap rounded-full font-extrabold"
        style={{
          padding: "5px 12px",
          fontSize: "13px",
          backgroundColor: "#F3F4F2",
          border: "1px solid rgba(17,19,24,0.08)",
          color: "#3E444A",
        }}
        data-testid="guide-group-v3-header"
      >
        {label}
      </h2>
      <span className="text-[11px] font-semibold text-[#4E5663]">({count})</span>
      <span className="h-px flex-1 bg-black/[0.06]" aria-hidden />
    </div>
  );
}

export function GuideProductGroupsV3({
  products,
  groupLabelsHe,
  suppressedBars,
  thresholdGeometry,
  marketGapsHe,
  expanderLabels,
  wide = false,
}: {
  products: GuideProductVM[];
  groupLabelsHe?: Partial<Record<GuideV3Group, string>>;
  suppressedBars?: GuideBarKey[];
  thresholdGeometry?: Partial<Record<GuideBarKey, GuideThresholdGeometry>>;
  /** Signed compact market-gaps copy (GuidePageVM.marketGapsCompactHe, copy package
   *  §4) — rendered in exactly one place, after the groups. */
  marketGapsHe?: string | null;
  /** Signed per-card disclosure toggle labels (GuidePageVM.expanderLabelsV3, copy
   *  package §5), threaded to every GuideProductRowV3. */
  expanderLabels?: { collapsed: string; expanded: string } | null;
  wide?: boolean;
}) {
  const groups = groupByV3(products);

  return (
    <section
      id="guide-products-v3"
      className={cn("px-4 py-4", wide && cn(comparisonWebSectionPaddingClass(), "lg:py-6"))}
      dir="rtl"
      data-testid="guide-product-groups-v3"
    >
      <div className="space-y-8">
        {GUIDE_V3_GROUP_ORDER.map((group) => {
          const groupProducts = groups[group];
          if (groupProducts.length === 0) return null;
          const label = groupLabelsHe?.[group] ?? group;

          return (
            <div key={group} data-testid={`guide-group-v3-${group}`}>
              <GroupSectionHeaderV3 label={label} count={groupProducts.length} />
              <div className="space-y-3">
                {groupProducts.map((product, i) => (
                  <GuideProductRowV3
                    key={product.id}
                    product={product}
                    rank={i + 1}
                    suppressedBars={suppressedBars}
                    thresholdGeometry={thresholdGeometry}
                    expanderLabels={expanderLabels}
                  />
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Market-information-gaps box — ONE occurrence (dispatch item 7), signed
          compact copy. */}
      {suppressedBars && suppressedBars.length > 0 && marketGapsHe ? (
        <div
          className="mt-8 rounded-2xl border p-4"
          style={{ borderColor: "#E2E5E2", background: "#F7F8F6" }}
          dir="rtl"
          data-testid="guide-market-gaps-box-v3"
        >
          <p className="text-[12px] leading-[1.6]" style={{ color: "#4E5663" }}>
            {marketGapsHe}
          </p>
        </div>
      ) : null}
    </section>
  );
}
