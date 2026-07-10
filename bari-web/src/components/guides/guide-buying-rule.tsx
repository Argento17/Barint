// Guide layer 1 — the buying rule (TASK-504, plan §3 item 1).
// "What actually matters, in one read" — the six bars in plain Hebrew, above the fold,
// before any product is shown. Mirrors CategoryHero/CategoryPrologue typography tokens
// so the guide template stays visually conformant with the comparison-page system
// (no novel type scale invented for this new page family).

import Image from "next/image";

import {
  comparisonWebSectionPaddingClass,
  BARI_COMPARISON_TOKENS,
  GUIDE_SECTION_EYEBROW_CLASS,
} from "@/lib/design/bari-comparison-tokens";
import { GUIDE_BAR_LABELS_HE, type GuideBuyingRuleBar } from "@/lib/view-models";
import { cn } from "@/lib/utils";

export function GuideBuyingRule({
  h1,
  subtitle,
  heroImage,
  buyingRuleIntro,
  bars,
  wide = false,
}: {
  h1: string;
  subtitle?: string | null;
  /** TASK-504C add-on — optional hero mascot, see GuidePageVM.heroImage. */
  heroImage?: { src: string; alt: string; width: number; height: number } | null;
  buyingRuleIntro?: string | null;
  bars: GuideBuyingRuleBar[];
  wide?: boolean;
}) {
  return (
    // TASK-504C H1 fix (Design vision-critic HIGH): the hero mascot webp has no alpha
    // channel — it's a flat #FEFEFE rectangle, not a cutout. Per the coordinator's
    // explicit instruction, this is fixed by matching the CONTAINER'S background to
    // the asset's own baked-in background (never by attempting an auto-matte/
    // transparent-key on the source PNG, which would destroy the white pills/bottle/
    // powder actually depicted in it). Setting the whole hero band to #FEFEFE — not
    // just a tight box around the image — means the image's edge dissolves into a
    // continuous field rather than trading one visible rectangle for a smaller one.
    // Scoped to heroImage-bearing guides only; a guide with no image keeps the
    // default (transparent, inherits the template's #FCFCF9).
    <header
      className={cn("px-4 pt-5 pb-4", wide && cn(comparisonWebSectionPaddingClass(), "lg:pt-7"))}
      style={heroImage ? { backgroundColor: "#FEFEFE" } : undefined}
      dir="rtl"
      data-testid="guide-buying-rule"
    >
      <div
        className={cn(
          heroImage && "flex flex-col-reverse items-center gap-4 md:flex-row md:items-end md:justify-between md:gap-8"
        )}
      >
        <div className={cn(heroImage && "min-w-0 flex-1")}>
          {/* TASK-504B: local AA-contrast override of typography.sectionEyebrow — see
              GUIDE_SECTION_EYEBROW_CLASS in bari-comparison-tokens.ts for why. */}
          <p className={GUIDE_SECTION_EYEBROW_CLASS}>מדריכים · בארי</p>
          <h1 className={BARI_COMPARISON_TOKENS.typography.sectionTitle}>{h1}</h1>
          {subtitle ? <p className={BARI_COMPARISON_TOKENS.typography.sectionMeta}>{subtitle}</p> : null}
        </div>
        {heroImage ? (
          <div className="shrink-0 overflow-visible py-1" data-testid="guide-hero-image">
            <Image
              src={heroImage.src}
              alt={heroImage.alt}
              width={heroImage.width}
              height={heroImage.height}
              priority
              className="pointer-events-none h-auto w-40 select-none sm:w-52 md:w-60 lg:w-72"
            />
          </div>
        ) : null}
      </div>
      {buyingRuleIntro ? (
        <p className="mt-3 max-w-2xl text-[13px] leading-[1.6] text-[#3E444A]">{buyingRuleIntro}</p>
      ) : null}

      <ul className="mt-5 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
        {bars.map((entry) => (
          <li
            key={entry.bar}
            className="rounded-xl border border-black/[0.08] bg-white p-3"
          >
            <p className="text-[13px] font-bold text-[#111318]">{GUIDE_BAR_LABELS_HE[entry.bar]}</p>
            <p className="mt-1 text-[12px] leading-[1.5] text-[#4E5663]">{entry.explanation}</p>
          </li>
        ))}
      </ul>
    </header>
  );
}
