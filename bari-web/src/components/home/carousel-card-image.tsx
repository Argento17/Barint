"use client";

import { useState } from "react";
import { CAROUSEL_PRODUCT_FALLBACK } from "@/lib/home/homepage-carousel-schema";
import { cn } from "@/lib/utils";

interface CarouselCardImageProps {
  productId: string;
  imageUrl?: string;
  imageAlt: string;
  sizes?: string;
  className?: string;
  accent?: string;
}

/**
 * Product pack image with accent-tinted tile background and branded SVG fallback.
 * Uses native <img> to avoid next/image domain restrictions (yochananof returns 403).
 * mix-blend-multiply removes white backgrounds on pack shots.
 */
export function CarouselCardImage({
  productId,
  imageUrl,
  imageAlt,
  className,
  accent,
}: CarouselCardImageProps) {
  const [loaded, setLoaded] = useState(false);
  const [errored, setErrored] = useState(false);

  const src = !imageUrl || errored ? CAROUSEL_PRODUCT_FALLBACK : imageUrl;
  const tileColor = accent ? accent + "1A" : "#00000010";

  return (
    <div
      key={productId}
      className="rounded-xl overflow-hidden flex items-center justify-center"
      style={{ backgroundColor: tileColor }}
    >
      <div className={cn("relative", className)}>
        {!loaded && (
          <div className="absolute inset-0 animate-pulse rounded-md bg-black/[0.06]" aria-hidden />
        )}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={src}
          alt={imageAlt}
          className={cn(
            "absolute inset-0 h-full w-full object-contain transition-opacity duration-300",
            loaded ? "opacity-100" : "opacity-0",
            !errored && "mix-blend-multiply"
          )}
          onLoad={() => setLoaded(true)}
          onError={() => {
            setErrored(true);
            setLoaded(true);
          }}
        />
      </div>
    </div>
  );
}