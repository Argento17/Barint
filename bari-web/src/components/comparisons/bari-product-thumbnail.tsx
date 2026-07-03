"use client";

import { useState } from "react";
import Image from "next/image";

import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

export function BariProductThumbnail({
  product,
  size = "md",
  className,
  eager = false,
  blendWhite = false,
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
  /** When true, swap the tile's cream fill (#F7F7F2) for pure white so the photo's
   *  baked-in white background dissolves into the tile — no mismatched "white box
   *  inside a cream tile" look. Border + shadow are retained so the card edge stays
   *  defined (pharmacy/e-commerce style). Used for retail supplement shots.
   *  Default false → every other category renders byte-identical. */
  blendWhite?: boolean;
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
          `relative ${dim} shrink-0 overflow-hidden rounded-2xl`,
          blendWhite
            ? "border border-black/[0.06] bg-white shadow-sm"
            : "border border-black/[0.06] bg-[#F7F7F2] shadow-sm",
          className
        )}
      >
        {/* next/image (not a raw <img>) so the photo is proxied through Next's optimizer
            and served SAME-ORIGIN from /_next/image — it never hotlinks the retailer host
            from the visitor's browser, so ad blockers / VPNs / private-DNS filters that block
            third-party image domains can no longer blank the thumbnail. `fill` sizes the image
            to the parent box (which carries the fixed dimensions). onError still trips the
            no-photo ✦ fallback below. */}
        <Image
          src={product.imageUrl}
          alt={product.name}
          fill
          className="object-contain p-2"
          sizes={
            size === "sm"
              ? "48px"
              : size === "lg"
                ? "128px"
                : size === "fill"
                  ? "96px"
                  : "64px"
          }
          priority={eager}
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  // No-photo fallback. Matches the framed-tile surface (border + fill + shadow) of the
  // photo tiles so a product without an image reads as a calm, consistent tile rather
  // than a dark block among the photo tiles. When blendWhite is active (supplements) the
  // fallback uses white to match the white photo tiles; otherwise cream (#F7F7F2).
  // The product name is already shown in the row's name cell, so the tile carries only a
  // faint neutral mark; aria-label keeps the name available to assistive tech.
  return (
    <div
      className={cn(
        `relative ${dim} shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] shadow-sm`,
        blendWhite ? "bg-white" : "bg-[#F7F7F2]",
        className
      )}
      aria-label={product.name}
    >
      <div className="flex h-full items-center justify-center">
        <span
          aria-hidden
          className="select-none text-[1.25rem] leading-none"
          style={{ color: "rgba(17,19,24,0.18)" }}
        >
          ✦
        </span>
      </div>
    </div>
  );
}
