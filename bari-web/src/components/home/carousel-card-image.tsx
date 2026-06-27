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
}

/**
 * Product pack image with skeleton pulse loader and branded SVG fallback.
 * Keyed by productId — never by array index.
 * Uses object-contain so pack shapes are never distorted.
 */
export function CarouselCardImage({
  productId,
  imageUrl,
  imageAlt,
  sizes = "80px",
  className,
}: CarouselCardImageProps) {
  const [loaded, setLoaded] = useState(false);
  const [errored, setErrored] = useState(false);

  const src = !imageUrl || errored ? CAROUSEL_PRODUCT_FALLBACK : imageUrl;

  return (
    <div key={productId} className={cn("relative", className)}>
      {/* Skeleton pulse — visible until image loaded */}
      {!loaded && (
        <div
          className="absolute inset-0 animate-pulse rounded-md bg-black/[0.06]"
          aria-hidden
        />
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
  );
}
