"use client";

import { X } from "lucide-react";

import { BarCompositionBreakdown } from "@/components/snack/bar-composition-breakdown";
import { SnackConfidencePill } from "@/components/snack/snack-confidence-pill";
import { SnackShelfProductImage } from "@/components/snack/snack-shelf-product-image";
import { SnackScoreChip } from "@/components/snack/snack-score-chip";
import { WhyThisLandedHere } from "@/components/snack/why-this-landed-here";
import {
  buildSnackComposition,
  buildSnackScoreDrivers,
  buildSnackWhyLanded,
} from "@/lib/comparisons/snack-product-detail";
import type { SnackProduct } from "@/lib/comparisons/snack-types";

export function SnackProductDetailPanel({
  product,
  onClose,
}: {
  product: SnackProduct;
  onClose: () => void;
}) {
  const why = buildSnackWhyLanded(product);
  const composition = buildSnackComposition(product);
  const drivers = buildSnackScoreDrivers(product);

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/30">
      <div className="h-full w-full max-w-lg overflow-y-auto bg-[#FFFFFF] shadow-xl">
        <div className="sticky top-0 flex items-center justify-between border-b border-black/[0.06] bg-[#FFFFFF] px-4 py-3">
          <p className="text-sm font-bold text-[#111318]">פרטי מוצר</p>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full p-2 text-[#4E5663] hover:bg-[#F7F7F2]"
            aria-label="סגור"
          >
            <X className="size-5" />
          </button>
        </div>

        <div className="space-y-6 p-5">
          <SnackShelfProductImage product={product} variant="detail" className="mx-auto" />
          <div className="flex flex-wrap items-center gap-3">
            <SnackScoreChip
              score={product.score}
              grade={product.grade}
              displayable={product.displayable}
              variant="hero"
            />
            <SnackConfidencePill level={product.confidence_level} label={product.confidence_label_he} />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-[#111318]">{product.name_he}</h2>
            <p className="mt-1 text-sm text-[#4E5663]">{product.segment}</p>
            {product.nova ? (
              <p className="mt-2 text-xs font-semibold uppercase tracking-[0.12em] text-[#7A817C]">
                NOVA{product.nova}
              </p>
            ) : null}
          </div>

          <hr className="border-black/[0.06]" />

          <WhyThisLandedHere sections={why} />

          <BarCompositionBreakdown rows={composition} />

          <div className="space-y-2">
            <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
              גורמי ציון
            </p>
            <ul className="space-y-2">
              {drivers.map((row) => (
                <li
                  key={`${row.driver}-${row.impact_he}`}
                  className="flex justify-between gap-3 text-sm leading-6 text-[#313834]"
                >
                  <span>{row.driver}</span>
                  <span className="shrink-0 font-semibold text-[#4E5663]">{row.impact_he}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
