/**
 * Visual band components keyed by visualMode.
 * All variants share a fixed h-36 height.
 * Rules:
 *  - product_duel / product_single: CarouselCardImage only (no theme photos)
 *  - score_spread: mini bar chart, NO photos
 *  - ingredient_tokens: pill chips, NO photos
 *  - supplement_molecule: abstract SVG grid, NO external URLs
 */

import type { CarouselCard } from "@/lib/home/homepage-carousel-schema";
import { CarouselCardImage } from "./carousel-card-image";
import { cn } from "@/lib/utils";

// ── Shared visual band wrapper ────────────────────────────────────────────────

function VisualBand({
  accent,
  children,
  className,
}: {
  accent: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "relative flex h-36 w-full items-center justify-center overflow-hidden",
        className
      )}
      style={{ backgroundColor: accent + "18" }}
    >
      {children}
    </div>
  );
}

// ── product_duel ─────────────────────────────────────────────────────────────

export function ProductDuelVisual({ card }: { card: CarouselCard }) {
  const left = card.leftProduct;
  const right = card.rightProduct;
  if (!left || !right) return null;

  return (
    <VisualBand accent={card.accent}>
      {/* Left product */}
      <div className="flex flex-col items-center gap-1">
        <CarouselCardImage
          productId={left.productId}
          imageUrl={left.imageUrl}
          imageAlt={left.imageAlt}
          sizes="64px"
          className="h-24 w-16"
        />
        <span className="line-clamp-1 max-w-[5rem] text-center text-[0.55rem] font-semibold text-[#4E5663]">
          {left.brand}
        </span>
      </div>

      {/* VS divider */}
      <div className="mx-3 flex flex-col items-center gap-0.5">
        <div className="h-8 w-px bg-black/10" />
        <span className="text-[0.6rem] font-extrabold text-[#5E6560]">VS</span>
        <div className="h-8 w-px bg-black/10" />
      </div>

      {/* Right product */}
      <div className="flex flex-col items-center gap-1">
        <CarouselCardImage
          productId={right.productId}
          imageUrl={right.imageUrl}
          imageAlt={right.imageAlt}
          sizes="64px"
          className="h-24 w-16 -mt-4"
        />
        <span className="line-clamp-1 max-w-[5rem] text-center text-[0.55rem] font-semibold text-[#4E5663]">
          {right.brand}
        </span>
      </div>

      {/* Accent gradient overlay */}
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background: `linear-gradient(135deg, ${card.accent}22 0%, transparent 60%)`,
        }}
      />
    </VisualBand>
  );
}

// ── product_single ───────────────────────────────────────────────────────────

export function ProductSingleVisual({ card }: { card: CarouselCard }) {
  const product = card.spotlightProduct;
  if (!product) return null;

  return (
    <VisualBand accent={card.accent}>
      <CarouselCardImage
        productId={product.productId}
        imageUrl={product.imageUrl}
        imageAlt={product.imageAlt}
        sizes="88px"
        className="h-28 w-20"
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background: `linear-gradient(135deg, ${card.accent}22 0%, transparent 60%)`,
        }}
      />
    </VisualBand>
  );
}

// ── score_spread ─────────────────────────────────────────────────────────────

export function ScoreSpreadVisual({ card }: { card: CarouselCard }) {
  const spread = card.scoreSpread;
  if (!spread) return null;

  const range = spread.high - spread.low;
  const midpoint = Math.round(spread.low + range * 0.42);

  // Three bars: low, mid, high — heights proportional
  const bars = [
    { value: spread.low, height: 28, label: String(spread.low) },
    { value: midpoint, height: 50, label: "~" + String(midpoint) },
    { value: spread.high, height: 72, label: String(spread.high) },
  ];

  return (
    <VisualBand accent={card.accent}>
      <div className="flex flex-col items-center gap-1 px-4 w-full">
        <div className="flex items-end justify-center gap-2 w-full">
          {bars.map((bar) => (
            <div key={bar.value} className="flex flex-col items-center gap-1">
              <span
                className="text-[0.6rem] font-bold tabular-nums"
                style={{ color: card.accent }}
              >
                {bar.label}
              </span>
              <div
                className="w-8 rounded-t-md transition-all"
                style={{
                  height: bar.height,
                  backgroundColor: card.accent,
                  opacity: bar.value === spread.high ? 1 : bar.value === spread.low ? 0.3 : 0.6,
                }}
              />
            </div>
          ))}
        </div>
        <p className="text-[0.6rem] font-semibold text-[#5E6560]">
          {spread.count} {spread.label}
        </p>
      </div>
    </VisualBand>
  );
}

// ── ingredient_tokens ─────────────────────────────────────────────────────────

export function IngredientTokensVisual({ card }: { card: CarouselCard }) {
  const tokens = card.ingredientTokens ?? [];

  return (
    <VisualBand accent={card.accent}>
      <div className="flex flex-wrap justify-center gap-2 px-4" dir="rtl">
        {tokens.map((token) => (
          <span
            key={token}
            className="rounded-full border px-3 py-1.5 text-[0.7rem] font-bold"
            style={{
              borderColor: card.accent + "55",
              backgroundColor: card.accent + "14",
              color: card.accent,
            }}
          >
            {token}
          </span>
        ))}
      </div>
    </VisualBand>
  );
}

// ── supplement_molecule ──────────────────────────────────────────────────────

export function SupplementMoleculeVisual({ card }: { card: CarouselCard }) {
  const stat = card.supplementStat;

  return (
    <VisualBand accent={card.accent}>
      {/* Abstract molecule grid — CSS/SVG only, no external URLs */}
      <svg
        viewBox="0 0 140 100"
        className="absolute inset-0 h-full w-full opacity-20"
        aria-hidden
      >
        {/* Bonds */}
        <line x1="30" y1="50" x2="55" y2="30" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="30" x2="85" y2="30" stroke={card.accent} strokeWidth="1.5" />
        <line x1="85" y1="30" x2="110" y2="50" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="30" x2="55" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="85" y1="30" x2="85" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="60" x2="85" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="30" y1="50" x2="55" y2="60" stroke={card.accent} strokeWidth="1" />
        <line x1="110" y1="50" x2="85" y2="60" stroke={card.accent} strokeWidth="1" />
        {/* Nodes */}
        <circle cx="30" cy="50" r="5" fill={card.accent} />
        <circle cx="55" cy="30" r="5" fill={card.accent} />
        <circle cx="85" cy="30" r="5" fill={card.accent} />
        <circle cx="110" cy="50" r="5" fill={card.accent} />
        <circle cx="55" cy="60" r="4" fill={card.accent} />
        <circle cx="85" cy="60" r="4" fill={card.accent} />
        <circle cx="70" cy="45" r="6" fill={card.accent} />
      </svg>

      {/* Stat overlay */}
      {stat && (
        <div className="relative z-10 flex flex-col items-center gap-0.5">
          <span
            className="text-4xl font-extrabold tabular-nums tracking-tight"
            style={{ color: card.accent }}
          >
            {stat.value}
          </span>
          <span className="text-xs font-semibold text-[#5E6560]">{stat.label}</span>
        </div>
      )}
    </VisualBand>
  );
}

// ── Router ────────────────────────────────────────────────────────────────────

export function CardVisualBand({ card }: { card: CarouselCard }) {
  switch (card.visualMode) {
    case "product_duel":
      return <ProductDuelVisual card={card} />;
    case "product_single":
      return <ProductSingleVisual card={card} />;
    case "score_spread":
      return <ScoreSpreadVisual card={card} />;
    case "ingredient_tokens":
      return <IngredientTokensVisual card={card} />;
    case "supplement_molecule":
      return <SupplementMoleculeVisual card={card} />;
    default:
      return null;
  }
}
