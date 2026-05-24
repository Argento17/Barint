"use client";

import Image from "next/image";
import { useMemo } from "react";
import { motion, useReducedMotion } from "framer-motion";

import { milkProducts } from "@/lib/comparisons/milk-page-data";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

/** 2 left · 2 center · 2 right — symmetrical analysis shelf */
const SHELF_BARCODES = [
  "7290110324926",
  "7290000051352",
  "7290116936116",
  "7394376619939",
  "5411188124689",
  "8000215204554",
] as const;

type ShelfSlot = {
  /** 0 = left end, 1 = right end along semicircle */
  t: number;
  widthRem: number;
  rotate: number;
  depth: number;
};

const SHELF_SLOTS: ShelfSlot[] = [
  { t: 0.1, widthRem: 2.65, rotate: -7, depth: 1 },
  { t: 0.24, widthRem: 2.85, rotate: -3, depth: 2 },
  { t: 0.4, widthRem: 3.35, rotate: 0, depth: 4 },
  { t: 0.6, widthRem: 3.2, rotate: 0, depth: 3 },
  { t: 0.76, widthRem: 2.85, rotate: 3, depth: 2 },
  { t: 0.9, widthRem: 2.65, rotate: 7, depth: 1 },
];

/** Elliptical semicircle shelf — SVG coords */
const SHELF_GEOMETRY = {
  viewW: 560,
  viewH: 200,
  cx: 280,
  cy: 168,
  rx: 228,
  ry: 72,
};

function pointOnShelfArc(t: number) {
  const angle = Math.PI * (1 - t);
  const { cx, cy, rx, ry } = SHELF_GEOMETRY;
  return {
    x: cx + rx * Math.cos(angle),
    y: cy - ry * Math.sin(angle),
    angle,
  };
}

function ShelfPack({
  product,
  slot,
  reduceMotion,
  index,
}: {
  product: MilkComparisonProduct;
  slot: ShelfSlot;
  reduceMotion: boolean | null;
  index: number;
}) {
  const pt = pointOnShelfArc(slot.t);
  const leftPct = (pt.x / SHELF_GEOMETRY.viewW) * 100;
  const topPct = (pt.y / SHELF_GEOMETRY.viewH) * 100;

  return (
    <motion.div
      className="pointer-events-none absolute"
      style={{
        left: `${leftPct}%`,
        top: `${topPct}%`,
        zIndex: slot.depth,
        width: `${slot.widthRem}rem`,
      }}
      initial={reduceMotion ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.04 + index * 0.05, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
    >
      <div
        className="relative"
        style={{
          transform: `translate(-50%, calc(-100% + ${slot.depth === 4 ? 0 : slot.depth === 3 ? 1 : 2}px)) rotate(${slot.rotate}deg)`,
        }}
      >
        {product.image_url ? (
          <div className="relative aspect-[3/4] w-full">
            <Image
              src={product.image_url}
              alt=""
              fill
              className="object-contain object-bottom drop-shadow-[0_4px_12px_rgba(17,19,24,0.12)]"
              sizes="72px"
              priority={index >= 2 && index <= 3}
            />
          </div>
        ) : null}
      </div>
    </motion.div>
  );
}

type MilkOrbitVisualProps = {
  className?: string;
  /** @deprecated use className height on parent */
  minHeight?: string;
  showArc?: boolean;
  caption?: string;
};

export function MilkOrbitVisual({
  className,
  minHeight,
  showArc = true,
  caption,
}: MilkOrbitVisualProps) {
  const reduceMotion = useReducedMotion();
  const products = useMemo(() => {
    const byBarcode = new Map(milkProducts.map((p) => [p.barcode, p]));
    return SHELF_BARCODES.map((b, i) => {
      const p = byBarcode.get(b);
      return p?.image_url ? { product: p, slot: SHELF_SLOTS[i]! } : null;
    }).filter((x): x is { product: MilkComparisonProduct; slot: ShelfSlot } => x != null);
  }, []);

  const { cx, cy, rx, ry, viewW, viewH } = SHELF_GEOMETRY;
  const arcPath = `M ${cx - rx} ${cy} A ${rx} ${ry} 0 0 1 ${cx + rx} ${cy}`;

  return (
    <div
      className={cn(
        "relative mx-auto w-full max-w-xl",
        minHeight ?? "h-[clamp(9.5rem,22vh,12.5rem)]",
        className
      )}
      aria-hidden
    >
      {caption ? (
        <p className="mb-1 text-center text-xs font-bold text-[#1F8F6A]">{caption}</p>
      ) : null}

      <div className="relative h-full w-full">
        {showArc ? (
          <svg
            className="absolute inset-0 h-full w-full"
            viewBox={`0 0 ${viewW} ${viewH}`}
            preserveAspectRatio="xMidYMax meet"
            aria-hidden
          >
            <defs>
              <linearGradient id="shelf-surface" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#E8EBE6" />
                <stop offset="100%" stopColor="#F7F7F2" />
              </linearGradient>
            </defs>

            <path
              d={`${arcPath} L ${cx + rx} ${viewH} L ${cx - rx} ${viewH} Z`}
              fill="url(#shelf-surface)"
              opacity={0.55}
            />

            <path
              d={arcPath}
              fill="none"
              stroke="#1F8F6A"
              strokeOpacity={0.22}
              strokeWidth={1.5}
              strokeDasharray="5 9"
            />

            <line
              x1={cx - rx}
              y1={cy + 2}
              x2={cx + rx}
              y2={cy + 2}
              stroke="#D8DDD4"
              strokeWidth={3}
              strokeLinecap="round"
            />
          </svg>
        ) : null}

        {products.map(({ product, slot }, i) => (
          <ShelfPack
            key={product.barcode}
            product={product}
            slot={slot}
            reduceMotion={reduceMotion}
            index={i}
          />
        ))}
      </div>
    </div>
  );
}
