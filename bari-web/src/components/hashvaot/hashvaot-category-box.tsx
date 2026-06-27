import Link from "next/link";
import { ChevronLeft, Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

/** Converts a hex colour like #BC6A33 to an "r g b" triplet string for use in rgba(). */
function hexToRgbTriplet(hex: string): string {
  const clean = hex.replace("#", "");
  const r = parseInt(clean.slice(0, 2), 16);
  const g = parseInt(clean.slice(2, 4), 16);
  const b = parseInt(clean.slice(4, 6), 16);
  return `${r} ${g} ${b}`;
}

function BuildingCard({ category }: { category: HashvaotCategory }) {
  const rgb = hexToRgbTriplet(category.accent);

  const inner = (
    <div
      role="status"
      aria-label={`קטגוריית ${category.title} — בבנייה, עדיין לא זמינה`}
      style={{
        borderColor: `rgba(${rgb} / 0.35)`,
        background: `rgba(${rgb} / 0.04)`,
      }}
      className="relative flex min-h-[9rem] flex-col gap-3 overflow-hidden rounded-2xl border border-dashed px-6 py-5 opacity-70"
    >
      {/* Glow blob */}
      <div
        aria-hidden
        style={{ background: `rgba(${rgb} / 0.10)` }}
        className="pointer-events-none absolute -end-8 -top-8 size-28 rounded-full blur-2xl"
      />

      {/* Header row */}
      <div className="flex items-center gap-3">
        <Clock
          className="size-4 shrink-0"
          style={{ color: `rgba(${rgb} / 0.75)` }}
          aria-hidden
        />
        <h2 className="text-base font-semibold text-[#4E5663]">{category.title}</h2>
        <span
          style={{
            borderColor: `rgba(${rgb} / 0.4)`,
            color: `rgba(${rgb} / 0.85)`,
          }}
          className="rounded-full border px-3 py-0.5 text-[0.68rem] font-semibold"
        >
          בקרוב
        </span>
      </div>

      {/* Subtext */}
      {category.comingSoonSubtext ? (
        <p className="text-sm leading-relaxed text-[#7A817C]">
          {category.comingSoonSubtext}
        </p>
      ) : null}
    </div>
  );

  // Linkable if href is provided
  if (category.href) {
    return (
      <Link href={category.href} className="block transition-opacity hover:opacity-80">
        {inner}
      </Link>
    );
  }
  return inner;
}

function LiveCard({ category }: { category: HashvaotCategory }) {
  const rgb = hexToRgbTriplet(category.accent);

  return (
    <Link
      href={category.href!}
      className={cn(
        "group relative flex min-h-[9rem] flex-col gap-3 overflow-hidden rounded-2xl border bg-white px-6 py-5",
        "transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
      )}
      style={{
        borderColor: `rgba(${rgb} / 0.25)`,
        borderInlineStartWidth: "4px",
        borderInlineStartColor: category.accent,
        // Hover shadow tinted to accent (applied via inline var trick)
      }}
    >
      {/* Gradient wash */}
      <div
        aria-hidden
        style={{
          background: `linear-gradient(135deg, rgba(${rgb} / 0.07) 0%, transparent 60%)`,
        }}
        className="pointer-events-none absolute inset-0 rounded-2xl"
      />

      {/* Corner glow blob */}
      <div
        aria-hidden
        style={{ background: `rgba(${rgb} / 0.12)` }}
        className="pointer-events-none absolute -end-10 -top-10 size-32 rounded-full blur-3xl"
      />

      {/* Header */}
      <div className="relative flex items-center justify-between gap-2">
        <h2 className="text-base font-bold text-[#111318]">{category.title}</h2>
        <span
          style={{
            background: `rgba(${rgb} / 0.12)`,
            color: category.accent,
            borderColor: `rgba(${rgb} / 0.25)`,
          }}
          className="shrink-0 rounded-full border px-2.5 py-0.5 text-[0.65rem] font-semibold tracking-wide"
        >
          זמין
        </span>
      </div>

      {/* Hero stat */}
      {category.heroStat ? (
        <div className="relative flex items-baseline gap-1.5">
          <span
            style={{ color: category.accent }}
            className="text-3xl font-black leading-none tabular-nums"
          >
            {category.heroStat.value}
          </span>
          <span className="text-xs text-[#7A817C]">{category.heroStat.label}</span>
        </div>
      ) : null}

      {/* Description */}
      {category.description ? (
        <p className="relative text-sm leading-relaxed text-[#4E5663]">
          {category.description}
        </p>
      ) : null}

      {/* Always-visible CTA */}
      <div
        className="relative mt-auto flex items-center gap-1 text-xs font-semibold"
        style={{ color: category.accent }}
      >
        <ChevronLeft className="size-3.5" aria-hidden />
        <span>לכל ההשוואות</span>
      </div>
    </Link>
  );
}

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  if (category.status === "building") {
    return <BuildingCard category={category} />;
  }
  return <LiveCard category={category} />;
}
