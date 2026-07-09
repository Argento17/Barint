import type { CSSProperties, ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

const LEAF_SRC = "/bari-icon-optimized.webp";

/**
 * Gradient-tile glyphs (owner-approved "Variant B", 2026-07-09). Bespoke
 * inline SVGs — not lucide-react — because the tile is a gradient surface
 * with a white glyph, not a flat tinted background with a colored stroke.
 */
function SupermarketGlyph() {
  return (
    <svg className="hashvaot-icon-svg" viewBox="0 0 24 24" aria-hidden="true">
      <path
        className="hashvaot-icon-g-stroke"
        d="M2.5 3.5h2.1l.9 3m0 0 1.7 8.1a1.6 1.6 0 0 0 1.56 1.27h7.2a1.6 1.6 0 0 0 1.55-1.19L20.5 6.5H5.5z"
      />
      <circle className="hashvaot-icon-g-solid" cx="9.6" cy="19.4" r="1.4" />
      <circle className="hashvaot-icon-g-solid" cx="16.8" cy="19.4" r="1.4" />
      <path
        className="hashvaot-icon-g-fill"
        d="M6.1 8.2h12.2l-1 3.9a1 1 0 0 1-.97.75H8.1a1 1 0 0 1-.98-.8z"
      />
    </svg>
  );
}

function SupplementsGlyph() {
  return (
    <svg className="hashvaot-icon-svg" viewBox="0 0 48 48" aria-hidden="true">
      <ellipse className="hashvaot-icon-orbit" cx="24" cy="24" rx="20" ry="7.5" />
      <ellipse className="hashvaot-icon-orbit" cx="24" cy="24" rx="20" ry="7.5" transform="rotate(60 24 24)" />
      <ellipse className="hashvaot-icon-orbit" cx="24" cy="24" rx="20" ry="7.5" transform="rotate(120 24 24)" />
      <circle className="hashvaot-icon-nucleus" cx="24" cy="24" r="3.4" />
      <g className="hashvaot-icon-e-grp e1">
        <circle className="hashvaot-icon-electron" cx="44" cy="24" r="2.1" />
      </g>
      <g className="hashvaot-icon-e-grp e2" transform="rotate(60 24 24)">
        <circle className="hashvaot-icon-electron" cx="44" cy="24" r="2.1" />
      </g>
      <g className="hashvaot-icon-e-grp e3" transform="rotate(120 24 24)">
        <circle className="hashvaot-icon-electron" cx="44" cy="24" r="2.1" />
      </g>
    </svg>
  );
}

function PersonalCareGlyph() {
  return (
    <svg className="hashvaot-icon-svg" viewBox="0 0 24 24" aria-hidden="true">
      <path
        className="hashvaot-icon-g-stroke"
        d="M12 3.2c3.4 3.6 5.4 6.4 5.4 9.4a5.4 5.4 0 0 1-10.8 0c0-3 2-5.8 5.4-9.4z"
      />
      <path
        className="hashvaot-icon-g-fill"
        d="M12 8.6c1.9 2.1 3 3.7 3 5.3a3 3 0 0 1-6 0c0-1.6 1.1-3.2 3-5.3z"
      />
    </svg>
  );
}

function RawFoodsGlyph() {
  return (
    <svg className="hashvaot-icon-svg" viewBox="0 0 24 24" aria-hidden="true">
      <path className="hashvaot-icon-g-stroke" d="M12 21v-8" />
      <path className="hashvaot-icon-g-fill" d="M12 13c0-3.2-2.3-5.4-6-5.7.2 3.6 2.4 5.7 6 5.7z" />
      <path className="hashvaot-icon-g-stroke" d="M12 13c0-3.2-2.3-5.4-6-5.7.2 3.6 2.4 5.7 6 5.7z" />
      <path className="hashvaot-icon-g-fill" d="M12 11.4c.3-2.8 2.3-4.7 5.6-4.9-.3 3-2.3 4.9-5.6 4.9z" />
      <path className="hashvaot-icon-g-stroke" d="M12 11.4c.3-2.8 2.3-4.7 5.6-4.9-.3 3-2.3 4.9-5.6 4.9z" />
    </svg>
  );
}

type CategoryGlyph = () => ReactNode;

/**
 * One glyph per category, keyed by category.id. Kept out of the data file —
 * hashvaot-categories.ts stays framework/UI-free per the View Model boundary.
 */
const CATEGORY_ICONS: Record<string, CategoryGlyph> = {
  supermarket: SupermarketGlyph,
  supplements: SupplementsGlyph,
  "personal-care": PersonalCareGlyph,
  "raw-foods": RawFoodsGlyph,
};
const DEFAULT_CATEGORY_ICON: CategoryGlyph = SupermarketGlyph;

/**
 * Splits an existing countLabel string (e.g. "16 השוואות") into a leading
 * number and its trailing Hebrew label, so the number can be accent-colored.
 * Never fabricates a value — returns null if the string doesn't start with
 * digits, in which case the raw countLabel is rendered as-is by the caller.
 */
function splitCountLabel(countLabel?: string): { value: string; label: string } | null {
  if (!countLabel) return null;
  const match = countLabel.match(/^(\d+)\s+(.+)$/);
  if (!match) return null;
  const [, value, label] = match;
  return { value, label };
}

function CardShell({
  category,
  status,
  href,
  ariaLabel,
  children,
}: {
  category: HashvaotCategory;
  status: "live" | "building";
  href?: string;
  ariaLabel: string;
  children: ReactNode;
}) {
  const accentBarBackground =
    status === "live"
      ? category.accent
      : `color-mix(in srgb, ${category.accent} 45%, #E3E3DD)`;

  const shellClassName = cn(
    "hashvaot-card-link group relative flex min-h-[12.5rem] flex-col overflow-hidden",
    "rounded-2xl border border-[rgba(17,19,24,0.09)] bg-white",
    "shadow-[0_1px_2px_rgba(17,19,24,0.05)]",
    status === "live" && [
      "transition-[transform,box-shadow] duration-200",
      "hover:-translate-y-[3px] hover:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]",
      "motion-reduce:transition-none motion-reduce:hover:translate-y-0",
    ]
  );

  const style = { "--tex-accent": category.accent } as CSSProperties;

  const content = (
    <>
      <div className="h-[0.4rem] w-full shrink-0" style={{ background: accentBarBackground }} aria-hidden />
      {children}
    </>
  );

  if (href) {
    return (
      <Link href={href} className={shellClassName} style={style} aria-label={ariaLabel}>
        {content}
      </Link>
    );
  }

  return (
    <div className={shellClassName} style={style} role="status" aria-label={ariaLabel}>
      {content}
    </div>
  );
}

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  const isLive = category.status === "live";
  const insightText = isLive ? category.description : category.comingSoonSubtext;
  const stat = isLive ? splitCountLabel(category.countLabel) : null;
  const CategoryGlyph = CATEGORY_ICONS[category.id] ?? DEFAULT_CATEGORY_ICON;

  return (
    <CardShell
      category={category}
      status={category.status}
      href={category.href}
      ariaLabel={
        isLive
          ? `קטגוריית ${category.title}`
          : `קטגוריית ${category.title} — בבנייה, עדיין לא זמינה`
      }
    >
      <div className="relative z-[1] flex flex-1 flex-col gap-[0.7rem] px-[1.4rem] pb-[1.25rem] pt-[1.15rem]">
        <div className="flex items-start justify-between gap-3">
          <div className="flex min-w-0 flex-1 items-center justify-start gap-2.5">
            <span
              className={cn(
                "shrink-0 rounded-full px-2.5 py-0.5 text-[0.65rem] font-bold",
                !isLive && "bg-black/5 text-[#7A817C]"
              )}
              style={
                isLive
                  ? {
                      backgroundColor: `color-mix(in srgb, ${category.accent} 12%, #fff)`,
                      color: category.accent,
                      boxShadow: `inset 0 0 0 1px color-mix(in srgb, ${category.accent} 35%, transparent)`,
                    }
                  : undefined
              }
            >
              {isLive ? "זמין" : "בקרוב"}
            </span>
            <h2
              className={cn(
                "text-right text-[1.2rem] font-extrabold tracking-[-0.02em]",
                isLive ? "text-[#111318]" : "text-[#4E5663]"
              )}
              style={{ fontFamily: "var(--font-heading, var(--font-sans))" }}
            >
              {category.title}
            </h2>
          </div>

          <div className={cn("flex shrink-0 flex-col items-center gap-2", !isLive && "opacity-55")}>
            <Image
              src={LEAF_SRC}
              alt=""
              width={28}
              height={28}
              aria-hidden
              className="h-7 w-7 shrink-0 object-contain"
            />
            <div
              className="hashvaot-icon-tile size-11 shrink-0"
              style={{ "--tile-accent": category.accent } as CSSProperties}
              aria-hidden
            >
              <CategoryGlyph />
            </div>
          </div>
        </div>

        {insightText ? (
          <p
            className={cn(
              "text-[1.05rem] font-medium leading-relaxed",
              isLive ? "text-[#3B424D]" : "text-[#6B7167]"
            )}
          >
            {insightText}
          </p>
        ) : null}

        {isLive && category.countLabel ? (
          <div className="mt-1 flex items-baseline gap-1.5 border-t border-black/5 pt-2 text-[0.8rem]">
            {stat ? (
              <>
                <span className="font-bold" style={{ color: category.accent }}>
                  {stat.value}
                </span>
                <span className="text-[#7A817C]">{stat.label}</span>
              </>
            ) : (
              <span className="font-semibold text-[#7A817C]">{category.countLabel}</span>
            )}
          </div>
        ) : null}

        <div className="mt-auto pt-1">
          {isLive ? (
            <span
              className="inline-flex items-center gap-1.5 text-[0.85rem] font-bold"
              style={{ color: category.accent }}
            >
              {category.ctaLabel ?? "לכל ההשוואות"}
              <ChevronLeft
                className="size-4 stroke-[2.5] transition-transform duration-200 group-hover:-translate-x-1 motion-reduce:transition-none motion-reduce:group-hover:translate-x-0"
                aria-hidden
              />
            </span>
          ) : (
            <span className="inline-flex w-fit items-center rounded-full bg-black/5 px-2.5 py-0.5 text-[0.65rem] font-bold text-[#7A817C]">
              בקרוב
            </span>
          )}
        </div>
      </div>
    </CardShell>
  );
}
