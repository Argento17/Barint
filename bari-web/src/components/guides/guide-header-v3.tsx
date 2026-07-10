// GuideHeaderV3 — TASK-577 (magnesium guide v3 STRUCTURAL rebuild).
//
// H1 + ONE intro sentence (dispatch item 1) — replaces v2's `GuideBuyingRule` header,
// which additionally rendered the 4-card "buying rule" explanation grid before the
// products. The owner's dictated v3 intro sentence names only 3 things (dose, form,
// label clarity) and is explicitly the ONE sentence under the H1 — the 4-card grid is
// a "methodology-first" element the owner ruled out, so it is not ported here (see
// this task's return for the explicit structural-decision note). `buyingRule`/
// `buyingRuleIntro` stay present but unread on the VM (rollback path), never rendered
// by this component.
//
// Keeps the hero mascot + `updatedLabel` (the latter was defined on the VM since
// TASK-504C but never actually rendered by any v2 component — wired here for the
// first time) — neither is "methodology prose", so neither is in scope for the
// dispatch's cut list.

import Image from "next/image";

import {
  comparisonWebSectionPaddingClass,
  BARI_COMPARISON_TOKENS,
  GUIDE_SECTION_EYEBROW_CLASS,
} from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function GuideHeaderV3({
  h1,
  subtitle,
  heroImage,
  introSentenceHe,
  updatedLabel,
  wide = false,
}: {
  h1: string;
  subtitle?: string | null;
  heroImage?: { src: string; alt: string; width: number; height: number } | null;
  introSentenceHe?: string | null;
  updatedLabel?: string | null;
  wide?: boolean;
}) {
  return (
    <header
      className={cn("px-4 pt-5 pb-4", wide && cn(comparisonWebSectionPaddingClass(), "lg:pt-7"))}
      style={heroImage ? { backgroundColor: "#FEFEFE" } : undefined}
      dir="rtl"
      data-testid="guide-header-v3"
    >
      <div
        className={cn(
          heroImage &&
            "flex flex-col-reverse items-center gap-4 md:flex-row md:items-end md:justify-between md:gap-8"
        )}
      >
        <div className={cn(heroImage && "min-w-0 flex-1")}>
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

      {introSentenceHe ? (
        <p className="mt-3 max-w-2xl text-[13px] leading-[1.6] text-[#3E444A]">{introSentenceHe}</p>
      ) : null}

      {updatedLabel ? (
        <p className="mt-2 text-[11px] font-semibold text-[#8A8F86]" data-testid="guide-updated-label">
          {updatedLabel}
        </p>
      ) : null}
    </header>
  );
}
