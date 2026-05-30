"use client";

import { useState } from "react";

import type { SnackProduct } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

const SEGMENT_ACCENT: Record<string, string> = {
  "חטיפי תמרים": "from-[#8B5E3C] to-[#C49A6C]",
  "חטיפי גרנולה ושיבולת שועל": "from-[#B8860B] to-[#D4A84B]",
  "חטיפי דגנים מצופי שוקולד": "from-[#3D2914] to-[#6B4423]",
  "חטיפי פרוטאין": "from-[#2D6A4F] to-[#4F9072]",
  "חטיפי \"סלים\" / רב-דגן": "from-[#5A6170] to-[#8A9199]",
  "חטיפי אגוזים": "from-[#7A5C3E] to-[#A67C52]",
};

type ImageVariant = "card" | "comparison" | "detail" | "hero";

const VARIANT_STYLES: Record<
  ImageVariant,
  { frame: string; image: string; minH: string }
> = {
  card: {
    frame: "w-full rounded-[1rem]",
    image: "p-3",
    minH: "min-h-[120px] md:min-h-[120px]",
  },
  comparison: {
    frame: "w-full max-w-[280px] rounded-[1.1rem]",
    image: "p-4",
    minH: "min-h-[140px] md:min-h-[180px]",
  },
  detail: {
    frame: "w-full max-w-[320px] rounded-[1.2rem]",
    image: "p-5",
    minH: "min-h-[200px] md:min-h-[240px]",
  },
  hero: {
    frame: "w-full max-w-[300px] rounded-[1.15rem]",
    image: "p-4",
    minH: "min-h-[160px] md:min-h-[200px]",
  },
};

function segmentAccent(segment: string) {
  return SEGMENT_ACCENT[segment] ?? "from-[#5A6170] to-[#8A9199]";
}

export function SnackShelfProductImage({
  product,
  variant = "card",
  className,
}: {
  product: Pick<SnackProduct, "name_he" | "image_url" | "segment">;
  variant?: ImageVariant;
  className?: string;
}) {
  const [failed, setFailed] = useState(!product.image_url);
  const styles = VARIANT_STYLES[variant];
  const accent = segmentAccent(product.segment);

  return (
    <div
      className={cn(
        "relative overflow-hidden border border-black/[0.08] bg-[linear-gradient(180deg,#FFFFFF_0%,#F7F7F2_100%)] shadow-[0_16px_40px_-28px_rgba(17,19,24,0.28)]",
        styles.frame,
        styles.minH,
        className
      )}
    >
      <div className="pointer-events-none absolute inset-x-0 bottom-4 h-[2px] bg-black/[0.06]" aria-hidden />
      <div
        className="pointer-events-none absolute inset-x-3 bottom-0 h-6 rounded-t-full bg-[#D7D2C7]/25 blur-md"
        aria-hidden
      />

      {!failed && product.image_url ? (
        <img
          src={product.image_url}
          alt={product.name_he}
          className={cn("h-full w-full object-contain object-bottom", styles.image, styles.minH)}
          loading="lazy"
          decoding="async"
          onError={() => setFailed(true)}
        />
      ) : (
        <div className={cn("flex h-full flex-col items-center justify-center px-4", styles.minH)}>
          <div
            className={cn(
              "h-16 w-28 rounded-[0.65rem] border border-black/[0.08] bg-gradient-to-b shadow-inner md:h-20 md:w-32",
              accent
            )}
          />
          <p className="mt-3 text-center text-[0.65rem] font-semibold uppercase tracking-[0.14em] text-[#7A817C]">
            {product.segment.split("/")[0]?.trim()}
          </p>
        </div>
      )}
    </div>
  );
}
