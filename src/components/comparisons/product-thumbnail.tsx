"use client";

import { useState } from "react";
import Image from "next/image";

import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

const FALLBACK_ACCENTS: Record<MilkComparisonProduct["productType"], string> = {
  dairy: "from-[#111318] to-[#2D3138]",
  soy: "from-[#1F8F6A] to-[#49B08A]",
  oat: "from-[#B8860B] to-[#D7A835]",
  almond: "from-[#6B7B8C] to-[#95A1B0]",
  rice: "from-[#8B7355] to-[#B49977]",
  coconut: "from-[#5A9E7E] to-[#81C0A4]",
  protein_drink: "from-[#2D6A4F] to-[#4F9072]",
  other_plant: "from-[#7A817C] to-[#A4AAA6]",
};

function compactTitle(product: MilkComparisonProduct): string {
  const source = product.displayTitle ?? product.shortName;
  const trimmed = source.replace(/\s+/g, " ").trim();
  const parts = trimmed.split(" ").slice(0, 4);
  return parts.join(" ");
}

function compactBrand(product: MilkComparisonProduct): string {
  return (product.brandLine ?? product.brand).replace(/^חלב\s+/, "").trim();
}

export function ProductThumbnail({
  product,
  size = "md",
  wrapperClassName,
  imageClassName,
  imageSizes,
}: {
  product: MilkComparisonProduct;
  size?: "sm" | "md" | "lg";
  wrapperClassName?: string;
  imageClassName?: string;
  imageSizes?: string;
}) {
  const [failed, setFailed] = useState(false);
  const dim =
    size === "sm" ? "size-12" : size === "lg" ? "size-28 sm:size-32" : "size-16";
  const accent = FALLBACK_ACCENTS[product.productType];
  const brand = compactBrand(product);
  const title = compactTitle(product);
  const compact = size === "sm";
  const labelText = compact ? product.productTypeLabel : brand;

  if (product.image_url && !failed) {
    return (
      <div
        className={cn(
          `relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm`,
          wrapperClassName
        )}
      >
        <Image
          src={product.image_url}
          alt={product.name_he}
          fill
          className={cn("object-contain p-2", imageClassName)}
          sizes={imageSizes ?? (size === "sm" ? "48px" : size === "lg" ? "128px" : "64px")}
          loading="lazy"
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  return (
    <div
      className={cn(
        `relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm`,
        wrapperClassName
      )}
      aria-hidden
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_10%,rgba(255,255,255,0.92),transparent_40%)]" />
      <div className="absolute inset-x-[18%] bottom-[10%] top-[10%] overflow-hidden rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF]/98 shadow-[0_14px_30px_-24px_rgba(17,19,24,0.35)]">
        <div className={cn("h-[16%] w-full bg-gradient-to-b", accent)} />
        <div className="flex h-[84%] flex-col items-center justify-center p-2 text-center">
          <div
            className={cn("mb-2 h-10 w-10 rounded-full bg-gradient-to-b opacity-[0.16]", accent)}
          />
          <p className="text-[0.5rem] font-bold tracking-[0.04em] text-[#1F8F6A]">
            {product.productTypeLabel}
          </p>
          {!compact ? (
            <>
              <p className="mt-1 text-[0.52rem] font-extrabold leading-tight text-[#111318]">
                {brand}
              </p>
              <p className="mt-1 line-clamp-2 text-[0.43rem] leading-tight text-[#7A817C]">
                {title}
              </p>
            </>
          ) : (
            <p className="mt-1 text-[0.4rem] font-semibold text-[#7A817C]">{labelText}</p>
          )}
        </div>
      </div>
    </div>
  );
}
