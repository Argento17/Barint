"use client";

import { useReducedMotion } from "framer-motion";
import { ChevronLeft } from "lucide-react";

import {
  ComparisonAnalysisParticles,
  ComparisonIntelligenceBackdrop,
} from "@/components/comparisons/comparison-intelligence-backdrop";
import { cn } from "@/lib/utils";

export type ComparisonHeroStat = {
  value: string | number;
  label: string;
};

export type ComparisonHeroTheme = {
  /** muted product hue, used ONLY for the faint tint wash + (optional) future accents */
  accent: string;
  /** image URL — a /public path (preferred) or remote URL.
   *  Optional: when omitted, the hero renders the accent tint wash + backdrop only
   *  (no product photo). Used while a category-true photo is being commissioned. */
  photo?: string;
};

export type ComparisonIntelligenceHeroProps = {
  badge: string;
  categoryTags: string;
  title: string;
  description: string;
  /** @deprecated Removed 2026-07-01 — "תובנות מרכזיות" callout deleted per owner review #6. Prop accepted but ignored so callers need not be updated atomically. */
  insightLines?: readonly string[];
  /** @deprecated Removed 2026-07-01 — insights section deleted. Accepted but ignored. */
  showInsights?: boolean;
  stats: readonly ComparisonHeroStat[];
  updatedLabel?: string;
  ctaLabel?: string;
  /** Scroll target on comparison pages (e.g. `#comparison-grid`). */
  ctaTargetId?: string;
  /** When true, CTA renders as span for use inside a parent Link. */
  asLinkChild?: boolean;
  className?: string;
  theme?: ComparisonHeroTheme;
};

export function ComparisonIntelligenceHero({
  badge,
  categoryTags,
  title,
  description,
  // insightLines and showInsights accepted but ignored — callout removed 2026-07-01
  stats,
  updatedLabel,
  ctaLabel = "פתיחת דוח ההשוואה",
  ctaTargetId = "#comparison-grid",
  asLinkChild = false,
  className,
  theme,
}: ComparisonIntelligenceHeroProps) {
  const reduceMotion = useReducedMotion();

  const ctaClassName = cn(
    "relative isolate inline-flex items-center gap-2 overflow-hidden rounded-2xl border border-[#1F8F6A]/38",
    "bg-[#167A58] px-6 py-3.5 text-sm font-bold text-[#FAFAFA]",
    "shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_14px_40px_-16px_rgba(31,143,106,0.58)]",
    "transition-[transform,box-shadow] duration-500",
    !asLinkChild &&
      "hover:-translate-x-px hover:shadow-[inset_0_1px_0_rgba(255,255,255,0.24),0_18px_48px_-12px_rgba(31,143,106,0.48)]"
  );

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl",
        "min-h-[22rem]",
        "border border-[rgba(17,19,24,0.09)] bg-white shadow-[0_1px_2px_rgba(17,19,24,0.05)]",
        className
      )}
    >
      {/* accent top-bar — reference hub card language (owner-approved 2026-07-09) */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 z-[2] h-[0.4rem]"
        style={{ background: theme?.accent ?? "#1F8F6A" }}
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,#FDFDF8_0%,#F4F6F3_42%,#EEF5F1_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom_left,rgba(31,143,106,0.045),transparent_48%,transparent_72%,rgba(31,143,106,0.028))]"
        aria-hidden
      />

      {/* ── per-product theme: photo + veil + tint (decorative) ── */}
      {theme ? (
        <>
          {/* product photo — bled in from the bottom-left, faded into the card.
              Optional: omitted while a category-true photo is being commissioned. */}
          {theme.photo ? (
            <>
              <div
                aria-hidden
                className="pointer-events-none absolute inset-y-0 left-0 z-0 h-full w-[60%]"
                style={{
                  backgroundImage: `url(${theme.photo})`,
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                  opacity: 0.62,
                  filter: "grayscale(0.08) contrast(1.02) saturate(1.02)",
                  WebkitMaskImage:
                    "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
                  maskImage:
                    "radial-gradient(135% 145% at 0% 100%, #000 30%, rgba(0,0,0,0.5) 56%, transparent 80%)",
                }}
              />
              {/* white veil so foreground text stays crisp over the photo */}
              <div
                aria-hidden
                className="pointer-events-none absolute inset-0 z-0"
                style={{
                  background:
                    "linear-gradient(105deg, transparent 0%, rgba(253,253,248,0.10) 38%, rgba(253,253,248,0.62) 64%, rgba(253,253,248,0.86) 100%)",
                }}
              />
            </>
          ) : null}
          {/* faint product-hue tint wash in the corner */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 z-0 mix-blend-multiply"
            style={{
              background: `radial-gradient(60% 80% at 14% 96%, color-mix(in oklab, ${theme.accent} 13%, transparent), transparent 70%)`,
            }}
          />
        </>
      ) : null}

      <ComparisonIntelligenceBackdrop />
      <ComparisonAnalysisParticles reduceMotion={reduceMotion} />

      <div className="relative z-[1] px-6 pb-10 pt-8 sm:px-8 lg:px-11 lg:py-11">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          <span className="rounded-md border border-[#1F8F6A]/14 bg-[#1F8F6A]/[0.06] px-2 py-0.5 text-[0.58rem] font-extrabold tracking-wide text-[#167A58]">
            {badge}
          </span>
          <span className="text-[0.62rem] font-bold uppercase tracking-[0.22em] text-[#8A928A]">
            Bari Intel
          </span>
          <span className="h-px w-5 bg-[#1F8F6A]/15" aria-hidden />
          <span className="text-[0.65rem] font-semibold tracking-wide text-[#4E5663]">
            {categoryTags}
          </span>
        </div>

        <h1
          className="mt-5 text-balance text-2xl font-extrabold leading-[1.12] tracking-[-0.045em] text-[#12151A] sm:text-[1.75rem] lg:text-[2rem] lg:tracking-[-0.05em]"
          style={{ fontFamily: "var(--font-heading, var(--font-sans))" }}
        >
          {title}
        </h1>

        <p className="mt-3 max-w-2xl text-pretty text-sm leading-[1.7] text-[#4E5663] sm:text-[0.95rem] lg:mt-4">
          {description}
        </p>

        <div className="mt-5 flex flex-wrap gap-x-3 gap-y-1.5 border-t border-black/[0.05] pt-5 text-[0.62rem] font-medium tabular-nums leading-relaxed text-[#8A918B]">
          {stats.map((stat, index) => (
            <span key={`${stat.label}-${index}`} className="inline-flex items-center gap-x-3">
              {index > 0 ? (
                <span className="text-[#D5DAD6]" aria-hidden>
                  ·
                </span>
              ) : null}
              <span>
                <strong className="font-bold text-[#5C645E]">{stat.value}</strong> {stat.label}
              </span>
            </span>
          ))}
          {updatedLabel ? (
            <>
              <span className="text-[#D5DAD6]" aria-hidden>
                ·
              </span>
              <span>{updatedLabel}</span>
            </>
          ) : null}
        </div>

        <div className="mt-7">
          {asLinkChild ? (
            <span className={ctaClassName}>
              <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-[#FFFFFF]/25" aria-hidden />
              <span className="relative">{ctaLabel}</span>
              <ChevronLeft className="relative size-[1.125rem]" />
            </span>
          ) : (
            <a href={ctaTargetId} className={ctaClassName}>
              <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-[#FFFFFF]/25" aria-hidden />
              <span className="relative">{ctaLabel}</span>
              <ChevronLeft className="relative size-[1.125rem]" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
