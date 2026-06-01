"use client";

import { useComparisonLayout } from "@/lib/comparisons/comparison-layout-context";
import {
  BARI_COMPARISON_TOKENS,
  comparisonWebTableGridClass,
} from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

const WEB = BARI_COMPARISON_TOKENS.webTable;

/** Desktop-only column guide for Comparison Web Template v1. */
export function ProductTableHeader({ productCount }: { productCount: number }) {
  const layout = useComparisonLayout();

  if (layout !== "web") return null;

  return (
    <div
      className={cn(
        "hidden lg:grid lg:items-center lg:border-b lg:border-[rgba(17,19,24,0.06)] lg:py-2.5",
        comparisonWebTableGridClass(),
        WEB.tableInsetClass,
        WEB.headerBgClass
      )}
      aria-hidden
    >
      <span className="text-center text-[10px] font-bold tracking-[0.06em] text-[#9A9FA6]">
        #
      </span>
      <span className="text-[10px] font-bold tracking-[0.06em] text-[#9A9FA6]">תמונה</span>
      <span className="text-[10px] font-bold tracking-[0.06em] text-[#9A9FA6]">
        מוצר ותובנה
      </span>
      <span className="text-center text-[10px] font-bold tracking-[0.06em] text-[#9A9FA6]">
        ציון · {productCount}
      </span>
    </div>
  );
}
