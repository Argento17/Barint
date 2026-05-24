"use client";

import { useState } from "react";
import Image from "next/image";
import { Package } from "lucide-react";

import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

export function ProductThumbnail({
  product,
  size = "md",
}: {
  product: MilkComparisonProduct;
  size?: "sm" | "md" | "lg";
}) {
  const [failed, setFailed] = useState(false);
  const dim =
    size === "sm" ? "size-12" : size === "lg" ? "size-28 sm:size-32" : "size-16";
  const iconSize = size === "lg" ? "size-10" : "size-6";

  if (product.image_url && !failed) {
    return (
      <div
        className={`relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm`}
      >
        <Image
          src={product.image_url}
          alt={product.name_he}
          fill
          className="object-contain p-2"
          sizes={size === "sm" ? "48px" : size === "lg" ? "128px" : "64px"}
          loading="lazy"
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  return (
    <div
      className={`flex ${dim} shrink-0 items-center justify-center rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm`}
      aria-hidden
    >
      <Package className={`${iconSize} text-[#7A817C]/70`} />
    </div>
  );
}
