"use client";

import { SnackShelfProductImage } from "@/components/snack/snack-shelf-product-image";
import { SnackScoreChip } from "@/components/snack/snack-score-chip";
import type { SnackProduct } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

export type ProductCardGridProps = {
  products: SnackProduct[];
  selectedIds?: string[];
  onToggleCompare?: (id: string) => void;
  onOpenProduct?: (product: SnackProduct) => void;
  compareMode?: boolean;
};

export function ProductCardGrid({
  products,
  selectedIds = [],
  onToggleCompare,
  onOpenProduct,
  compareMode = false,
}: ProductCardGridProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {products.map((product) => {
        const selected = selectedIds.includes(product.id);
        return (
          <article
            key={product.id}
            className={cn(
              "flex min-w-[10rem] flex-col rounded-[1rem] border border-black/[0.08] bg-[#FFFFFF] p-4 transition-opacity hover:opacity-85 md:min-w-[12.5rem]",
              selected && "ring-2 ring-[#1F8F6A]/40"
            )}
          >
            <button
              type="button"
              onClick={() => onOpenProduct?.(product)}
              className="text-right"
            >
              <SnackShelfProductImage product={product} variant="card" />
              <h3 className="mt-3 line-clamp-2 text-sm font-bold leading-snug text-[#111318]">
                {product.name_he}
              </h3>
              <div className="mt-2 flex items-center justify-between gap-2">
                <SnackScoreChip
                  score={product.score}
                  grade={product.grade}
                  displayable={product.displayable}
                  variant="card"
                />
                {product.nova ? (
                  <span className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-[#7A817C]">
                    NOVA{product.nova}
                  </span>
                ) : null}
              </div>
              <p className="mt-2 text-xs text-[#4E5663]">{product.segment}</p>
            </button>

            {compareMode && onToggleCompare ? (
              <button
                type="button"
                onClick={() => onToggleCompare(product.id)}
                className={cn(
                  "mt-3 w-full rounded-full border px-3 py-2 text-xs font-bold",
                  selected
                    ? "border-[#1F8F6A] bg-[#E8F5EF] text-[#176F53]"
                    : "border-black/[0.08] text-[#4E5663]"
                )}
              >
                {selected ? "בהשוואה" : "השווה"}
              </button>
            ) : null}
          </article>
        );
      })}
    </div>
  );
}
