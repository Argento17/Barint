"use client";

import { useState } from "react";

import type { BreadProduct } from "@/lib/comparisons/bread-types";
import { breadCategoryLabel } from "@/lib/comparisons/bread-page-data";
import { cn } from "@/lib/utils";

const SIZE_STYLES = {
  sm: {
    frame: "h-20 w-14 rounded-[1rem]",
    image: "p-1.5",
    label: "text-[0.46rem]",
  },
  md: {
    frame: "h-28 w-20 rounded-[1.2rem]",
    image: "p-2",
    label: "text-[0.5rem]",
  },
  lg: {
    frame: "h-36 w-24 rounded-[1.35rem]",
    image: "p-2.5",
    label: "text-[0.52rem]",
  },
} as const;

export function BreadShelfProductImage({
  product,
  size = "md",
  className,
}: {
  product: Pick<BreadProduct, "name_he" | "image_url" | "category" | "category_label_he">;
  size?: keyof typeof SIZE_STYLES;
  className?: string;
}) {
  const [failed, setFailed] = useState(false);
  const styles = SIZE_STYLES[size];

  return (
    <div
      className={cn(
        "relative overflow-hidden border border-black/[0.06] bg-[linear-gradient(180deg,#FFFFFF_0%,#F7F7F2_100%)] shadow-[0_12px_32px_-24px_rgba(17,19,24,0.34)]",
        styles.frame,
        className
      )}
    >
      <div className="pointer-events-none absolute inset-x-0 bottom-3 h-[2px] bg-black/[0.07]" aria-hidden />
      <div className="pointer-events-none absolute inset-x-2 bottom-0 h-5 rounded-t-full bg-[#D7D2C7]/30 blur-md" aria-hidden />
      <div className="pointer-events-none absolute inset-x-0 top-0 h-8 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.96),transparent_70%)]" aria-hidden />

      {!failed ? (
        <img
          src={product.image_url}
          alt={product.name_he}
          className={cn("h-full w-full object-contain object-bottom", styles.image)}
          sizes={size === "lg" ? "96px" : size === "md" ? "80px" : "56px"}
          loading="lazy"
          decoding="async"
          onError={() => setFailed(true)}
        />
      ) : (
        <div className="flex h-full flex-col items-center justify-center px-3 text-center">
          <div className="h-9 w-8 rounded-[0.85rem] border border-black/[0.07] bg-[#FFFFFF]" />
          <p className={cn("mt-2 font-semibold tracking-[0.12em] text-[#7A817C]", styles.label)}>
            {breadCategoryLabel(product)}
          </p>
        </div>
      )}
    </div>
  );
}
