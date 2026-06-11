"use client";

import { useState } from "react";

import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

export function BariProductThumbnail({
  product,
  size = "md",
  className,
  eager = false,
}: {
  product: BariProductVM;
  /** "fill" → the thumbnail fills its parent box (parent controls the size, e.g. a
   *  container-query-sized table cell). The presets are fixed pixel boxes. */
  size?: "sm" | "md" | "lg" | "fill";
  className?: string;
  /** TASK-233E — above-the-fold rows load eagerly so the image is requested on first
   *  paint instead of being deferred by `loading="lazy"` until a scroll/interaction
   *  nudges layout (the reported "image missing until I re-trigger it" behavior). */
  eager?: boolean;
}) {
  const [failed, setFailed] = useState(false);
  const dim =
    size === "fill"
      ? "h-full w-full"
      : size === "sm"
        ? "size-12"
        : size === "lg"
          ? "size-28 sm:size-32"
          : "size-16";

  if (product.imageUrl && !failed) {
    return (
      <div
        className={cn(
          `relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#FFFFFF] to-[#F7F7F2] shadow-sm`,
          className
        )}
      >
        <img
          src={product.imageUrl}
          alt=""
          className="h-full w-full object-contain p-2"
          sizes={
            size === "sm"
              ? "48px"
              : size === "lg"
                ? "128px"
                : size === "fill"
                  ? "96px"
                  : "64px"
          }
          loading={eager ? "eager" : "lazy"}
          fetchPriority={eager ? "high" : "auto"}
          decoding="async"
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  return (
    <div
      className={cn(
        `relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-gradient-to-b from-[#111318] to-[#2D3138] shadow-sm`,
        className
      )}
      aria-hidden
    >
      <div className="flex h-full flex-col items-center justify-center px-1 text-center">
        <p className="text-[0.55rem] font-bold uppercase tracking-[0.08em] text-white/70">
          Bari
        </p>
        <p className="mt-0.5 line-clamp-2 text-[0.6rem] font-semibold leading-tight text-white">
          {product.name.split(" ").slice(0, 3).join(" ")}
        </p>
      </div>
    </div>
  );
}
