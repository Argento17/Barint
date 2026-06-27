"use client";

import { useState } from "react";
import Image from "next/image";
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
 * Product pack image with rounded pedestal, skeleton pulse, and branded SVG fallback.
 * Keyed by productId. object-contain preserves pack shapes.
 * accent tints the pedestal background for brand colour coherence.
 */
export function CarouselCardImage({
  productId,
  imageUrl,
  imageAlt,
  sizes = "80px",
  className,
  accent,
}: CarouselCardImageProps) {
  const [loaded, setLoaded] = useState(false);
  const [errored, setErrored] = useState(false);

  const src = !imageUrl || errored ? CAROUSEL_PRODUCT_FALLBACK : imageUrl;

  return (
    <div
      key={productId}
      className="rounded-2xl bg-gradient-to-b from-white/50 to-black/[0.04] p-1.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)]"
      style={accent ? { backgroundColor: accent + "0a" } : undefined}
    >
      <div className={cn("relative", className)}>
        {!loaded && (
          <div className="absolute inset-0 animate-pulse rounded-md bg-black/[0.06]" aria-hidden />
        )}
        <Image
          src={src}
          alt={imageAlt}
          fill
          className={cn(
            "object-contain transition-opacity duration-300",
            loaded ? "opacity-100" : "opacity-0"
          )}
          sizes={sizes}
          onLoad={() => setLoaded(true)}
          onError={() => {
            setErrored(true);
            setLoaded(true);
          }}
          priority={false}
        />
      </div>
    </div>
  );
}
