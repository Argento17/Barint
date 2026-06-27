/**
 * Visual band components keyed by visualMode.
 * product_duel / product_single  -> h-36, CarouselCardImage with accent pedestal
 * grade_histogram / grade_skew / grade_stacked / ingredient_mask -> h-40, no photos
 * supplement_molecule -> h-36, abstract SVG
 */

import type { CarouselCard, GradeLetter } from "@/lib/home/homepage-carousel-schema";
import { CarouselCardImage } from "./carousel-card-image";
import { cn } from "@/lib/utils";

// -- Grade palette ---------------------------------------------------------------

const GRADE_COLORS: Record<GradeLetter, string> = {
  A: "#1F8F6A",
  B: "#4A9B7A",
  C: "#C4A035",
  D: "#BC6A33",
  E: "#B84A4A",
};

const GRADES = ["A", "B", "C", "D", "E"] as const;

// -- Shared visual band wrapper --------------------------------------------------

function VisualBand({
  accent,
  children,
  className,
  heightClass = "h-36",
}: {
  accent: string;
  children: React.ReactNode;
  className?: string;
  heightClass?: string;
}) {
  return (
    <div
      className={cn(
        "relative flex w-full items-center justify-center overflow-hidden",
        heightClass,
        className
      )}
      style={{ backgroundColor: accent + "18" }}
    >
      {children}
    </div>
  );
}

// -- product_duel ---------------------------------------------------------------

export function ProductDuelVisual({ card }: { card: CarouselCard }) {
  const left = card.leftProduct;
  const right = card.rightProduct;
  if (!left || !right) return null;

  return (
    <VisualBand accent={card.accent}>
      <div className="flex flex-col items-center gap-1">
        <CarouselCardImage
          productId={left.productId}
          imageUrl={left.imageUrl}
          imageAlt={left.imageAlt}
          sizes="64px"
          className="h-24 w-16"
          accent={card.accent}
        />
        <span className="line-clamp-1 max-w-[5rem] text-center text-[0.55rem] font-semibold text-[#4E5663]">
          {left.brand}
        </span>
      </div>
      <div className="mx-3 flex flex-col items-center gap-0.5">
        <div className="h-8 w-px bg-black/10" />
        <span className="text-[0.6rem] font-extrabold text-[#5E6560]">VS</span>
        <div className="h-8 w-px bg-black/10" />
      </div>
      <div className="flex flex-col items-center gap-1">
        <CarouselCardImage
          productId={right.productId}
          imageUrl={right.imageUrl}
          imageAlt={right.imageAlt}
          sizes="64px"
          className="h-24 w-16 -mt-4"
          accent={card.accent}
        />
        <span className="line-clamp-1 max-w-[5rem] text-center text-[0.55rem] font-semibold text-[#4E5663]">
          {right.brand}
        </span>
      </div>
      <div
        className="pointer-events-none absolute inset-0"
        style={{ background: "linear-gradient(135deg, " + card.accent + "22 0%, transparent 60%)" }}
      />
    </VisualBand>
  );
}

// -- product_single -------------------------------------------------------------

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
        accent={card.accent}
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{ background: "linear-gradient(135deg, " + card.accent + "22 0%, transparent 60%)" }}
      />
    </VisualBand>
  );
}

// -- grade_histogram ------------------------------------------------------------

export function GradeHistogramVisual({ card }: { card: CarouselCard }) {
  const dist = card.gradeDistribution;
  if (!dist) return null;

  const counts = GRADES.map((g) => dist.grades[g] ?? 0);
  const maxCount = Math.max(...counts, 1);
  const MAX_BAR_H = 72;

  return (
    <VisualBand accent={card.accent} heightClass="h-40">
      <div className="flex w-full flex-col items-center gap-1 px-3">
        <div className="flex w-full items-end justify-center gap-1.5">
          {GRADES.map((g, i) => {
            const count = counts[i];
            const isMax = count > 0 && count === maxCount;
            const barH = Math.max(
              Math.round((count / maxCount) * MAX_BAR_H),
              count > 0 ? 4 : 0
            );
            return (
              <div key={g} className="flex flex-col items-center gap-0.5">
                <span
                  className="text-[0.5rem] font-bold tabular-nums"
                  style={{ color: GRADE_COLORS[g], opacity: count > 0 ? 1 : 0 }}
                >
                  {count}
                </span>
                <div
                  className="w-7 rounded-t transition-all"
                  style={{
                    height: barH,
                    backgroundColor: GRADE_COLORS[g],
                    opacity: isMax ? 1 : count > 0 ? 0.45 : 0.1,
                    outline: isMax ? "2px solid " + GRADE_COLORS[g] : undefined,
                    outlineOffset: isMax ? "1px" : undefined,
                  }}
                />
                <span className="text-[0.55rem] font-semibold" style={{ color: GRADE_COLORS[g] }}>
                  {g}
                </span>
              </div>
            );
          })}
        </div>
        <p className="mt-1 text-center text-[0.55rem] font-semibold text-[#5E6560]">
          {dist.count} {dist.label}{" · "}{"הפרש"} {dist.spread}
        </p>
      </div>
    </VisualBand>
  );
}

// -- grade_skew ----------------------------------------------------------------

export function GradeSkewVisual({ card }: { card: CarouselCard }) {
  const dist = card.gradeDistribution;
  if (!dist) return null;

  const total = GRADES.reduce((sum, g) => sum + (dist.grades[g] ?? 0), 0) || 1;

  return (
    <VisualBand accent={card.accent} heightClass="h-40">
      <div className="flex w-full flex-col items-center gap-3 px-4">
        <div className="flex h-7 w-full overflow-hidden rounded-full">
          {GRADES.map((g) => {
            const count = dist.grades[g] ?? 0;
            if (count === 0) return null;
            const pct = (count / total) * 100;
            return (
              <div
                key={g}
                style={{ width: pct + "%", backgroundColor: GRADE_COLORS[g] }}
              />
            );
          })}
        </div>
        <div className="flex flex-wrap justify-center gap-1.5">
          {GRADES.filter((g) => (dist.grades[g] ?? 0) > 0).map((g) => (
            <span
              key={g}
              className="flex items-center gap-1 rounded-full px-2 py-0.5 text-[0.55rem] font-bold text-white"
              style={{ backgroundColor: GRADE_COLORS[g] }}
            >
              {g}{" · "}{dist.grades[g]}
            </span>
          ))}
        </div>
        <p className="text-center text-[0.55rem] font-semibold text-[#5E6560]">
          {dist.count} {dist.label}
        </p>
      </div>
    </VisualBand>
  );
}

// -- grade_stacked -------------------------------------------------------------

export function GradeStackedVisual({ card }: { card: CarouselCard }) {
  const dist = card.gradeDistribution;
  if (!dist) return null;

  const total = GRADES.reduce((sum, g) => sum + (dist.grades[g] ?? 0), 0) || 1;
  const activeGrades = GRADES.filter((g) => (dist.grades[g] ?? 0) > 0);

  return (
    <VisualBand accent={card.accent} heightClass="h-40">
      <div className="flex w-full flex-col items-center gap-1.5 px-4">
        <div className="flex h-10 w-full gap-0.5">
          {activeGrades.map((g, i) => {
            const count = dist.grades[g] ?? 0;
            const pct = (count / total) * 100;
            return (
              <div
                key={g}
                className={cn(
                  "flex items-center justify-center overflow-hidden text-[0.6rem] font-extrabold text-white",
                  i === 0 && "rounded-l-full",
                  i === activeGrades.length - 1 && "rounded-r-full"
                )}
                style={{ width: pct + "%", backgroundColor: GRADE_COLORS[g] }}
              >
                {pct > 8 ? g : ""}
              </div>
            );
          })}
        </div>
        <div className="flex w-full">
          {activeGrades.map((g) => {
            const count = dist.grades[g] ?? 0;
            const pct = (count / total) * 100;
            return (
              <div
                key={g}
                className="text-center text-[0.5rem] font-semibold"
                style={{ width: pct + "%", color: GRADE_COLORS[g] }}
              >
                {count}
              </div>
            );
          })}
        </div>
        <p className="text-center text-[0.55rem] font-semibold text-[#5E6560]">
          {dist.count} {dist.label}
        </p>
      </div>
    </VisualBand>
  );
}

// -- ingredient_mask -----------------------------------------------------------

function TokenPill({ token, accent }: { token: string; accent: string }) {
  return (
    <span
      className="whitespace-nowrap rounded-full border px-2 py-0.5 text-[0.55rem] font-bold"
      style={{
        borderColor: accent + "55",
        backgroundColor: accent + "14",
        color: accent,
      }}
    >
      {token}
    </span>
  );
}

export function IngredientMaskVisual({ card }: { card: CarouselCard }) {
  const tokens = card.ingredientTokens ?? [];
  const centerLabel = "סוכר";

  return (
    <VisualBand accent={card.accent} heightClass="h-40">
      <div className="relative h-full w-full">
        <svg className="absolute inset-0 h-full w-full" aria-hidden>
          <line x1="50%" y1="50%" x2="50%" y2="16%"
            stroke={card.accent} strokeWidth="1" strokeOpacity="0.35" strokeDasharray="3 2" />
          <line x1="50%" y1="50%" x2="15%" y2="84%"
            stroke={card.accent} strokeWidth="1" strokeOpacity="0.35" strokeDasharray="3 2" />
          <line x1="50%" y1="50%" x2="85%" y2="84%"
            stroke={card.accent} strokeWidth="1" strokeOpacity="0.35" strokeDasharray="3 2" />
        </svg>
        <div
          className="absolute left-1/2 top-1/2 z-10 flex h-14 w-14 -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full text-white shadow-md"
          style={{ backgroundColor: card.accent }}
        >
          <span className="text-[0.7rem] font-extrabold leading-none">{centerLabel}</span>
          {card.ingredientMaskCount != null && (
            <span
              className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-white text-[0.5rem] font-black"
              style={{ color: card.accent }}
            >
              {card.ingredientMaskCount}
            </span>
          )}
        </div>
        {tokens[0] && (
          <div className="absolute left-1/2 top-2 z-10 -translate-x-1/2">
            <TokenPill token={tokens[0]} accent={card.accent} />
          </div>
        )}
        {tokens[1] && (
          <div className="absolute bottom-2 left-2 z-10">
            <TokenPill token={tokens[1]} accent={card.accent} />
          </div>
        )}
        {tokens[2] && (
          <div className="absolute bottom-2 right-2 z-10">
            <TokenPill token={tokens[2]} accent={card.accent} />
          </div>
        )}
      </div>
    </VisualBand>
  );
}

// -- supplement_molecule -------------------------------------------------------

export function SupplementMoleculeVisual({ card }: { card: CarouselCard }) {
  const stat = card.supplementStat;

  return (
    <VisualBand accent={card.accent}>
      <svg viewBox="0 0 140 100" className="absolute inset-0 h-full w-full opacity-20" aria-hidden>
        <line x1="30" y1="50" x2="55" y2="30" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="30" x2="85" y2="30" stroke={card.accent} strokeWidth="1.5" />
        <line x1="85" y1="30" x2="110" y2="50" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="30" x2="55" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="85" y1="30" x2="85" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="55" y1="60" x2="85" y2="60" stroke={card.accent} strokeWidth="1.5" />
        <line x1="30" y1="50" x2="55" y2="60" stroke={card.accent} strokeWidth="1" />
        <line x1="110" y1="50" x2="85" y2="60" stroke={card.accent} strokeWidth="1" />
        <circle cx="30" cy="50" r="5" fill={card.accent} />
        <circle cx="55" cy="30" r="5" fill={card.accent} />
        <circle cx="85" cy="30" r="5" fill={card.accent} />
        <circle cx="110" cy="50" r="5" fill={card.accent} />
        <circle cx="55" cy="60" r="4" fill={card.accent} />
        <circle cx="85" cy="60" r="4" fill={card.accent} />
        <circle cx="70" cy="45" r="6" fill={card.accent} />
      </svg>
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

// -- Router --------------------------------------------------------------------

export function CardVisualBand({ card }: { card: CarouselCard }) {
  switch (card.visualMode) {
    case "product_duel":
      return <ProductDuelVisual card={card} />;
    case "product_single":
      return <ProductSingleVisual card={card} />;
    case "grade_histogram":
      return <GradeHistogramVisual card={card} />;
    case "grade_skew":
      return <GradeSkewVisual card={card} />;
    case "grade_stacked":
      return <GradeStackedVisual card={card} />;
    case "ingredient_mask":
      return <IngredientMaskVisual card={card} />;
    case "supplement_molecule":
      return <SupplementMoleculeVisual card={card} />;
    default:
      return null;
  }
}
