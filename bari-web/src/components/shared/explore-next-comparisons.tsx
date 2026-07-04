"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import {
  getExploreNextCategories,
  type ExploreNextCategory,
} from "@/lib/hashvaot/explore-next-categories";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

/**
 * TASK-507 — "עוד השוואות" (More comparisons) module.
 *
 * Rendered at the bottom of every leaf comparison page (below the existing white
 * card, in the page background) to give single-page landers an onward path into
 * other live categories. Additive only — never rendered inside the scored product
 * table/verdict area, so it cannot touch product-row copy (frozen per the active
 * product-descriptions freeze).
 *
 * Data-driven from `EXPLORE_NEXT_CATEGORIES` (src/lib/hashvaot/explore-next-categories.ts):
 * adding a category there makes it eligible to appear here automatically, and the
 * current page's own category is always filtered out. Candidates are additionally
 * scoped to the current category's own shelf (Product D1 — e.g. magnesium/supplements
 * never mixes with the supermarket shelf) and capped at one card per `family` tag
 * (Product D2 — e.g. cheese / brined-cheeses / hard-cheeses never all appear together).
 * `currentCategoryId` is intentionally its OWN prop, decoupled from the `category` prop
 * ComparisonPage/ComparisonTable use for expansion nutrition-scale lookups (TASK-507
 * HIGH-1) — never source this value from that prop.
 *
 * Visual language is deliberately NOT novel: geometry (radius, border, shadow, hover
 * lift, focus ring) is copied from the existing `HashvaotCategoryBox` LiveCard pattern
 * (src/components/hashvaot/hashvaot-category-box.tsx) — the closest already-approved
 * "compact category card" in the system — with a self-hosted stock category image
 * added on top, the same asset already used by the Featured*IntelligenceCard family.
 *
 * NOTE: this is a new canonical component built without a fresh Design Agent visual
 * spec (none existed for this task). It reuses only existing tokens/classes; flagged
 * in the TASK-507 return for a Design Agent conformance pass before go-live.
 */

const SECTION_HEADING = "עוד השוואות"; // DRAFT — pending Content + Adversarial QA sign-off

export interface ExploreNextComparisonsProps {
  /** The current page's category id (route segment under /hashvaot/). Excluded from
   *  the card list so a category never links to itself. */
  currentCategoryId?: string | null;
  /** Number of cards to show. Defaults to 4 per the TASK-507 spec (3–4 cards). */
  count?: number;
  /** Matches the outer page's max-width so the section aligns under the card above
   *  it. Pass the same value the page uses for its bounded white card. */
  wide?: boolean;
  className?: string;
}

export function ExploreNextComparisons({
  currentCategoryId,
  count = 4,
  wide = false,
  className,
}: ExploreNextComparisonsProps) {
  const cards = getExploreNextCategories(currentCategoryId, count);
  if (cards.length === 0) return null;

  return (
    <section
      dir="rtl"
      aria-labelledby="explore-next-heading"
      className={cn(
        "mx-auto mt-8 w-full max-w-[640px] px-4 pb-2",
        wide && "lg:max-w-[1180px]",
        wide && comparisonWebSectionPaddingClass(),
        className
      )}
    >
      {/*
       * Heading color: #4E5663, not the #7A817C used by the (visually similar)
       * HashvaotCategoryGroupHeader — that header sits on bg-[#F7F7F2] (near-white);
       * this section sits directly on the comparison page's bg-[#EFEFEB], where
       * #7A817C measures 3.46:1 (fails WCAG 1.4.3). #4E5663 is the same slate
       * already used for prologue/body copy across the comparison pages and
       * clears 4.5:1 against this background. Confirmed via `npm run test:a11y`.
       */}
      <h2
        id="explore-next-heading"
        className="text-sm font-bold uppercase tracking-[0.18em] text-[#4E5663]"
      >
        {SECTION_HEADING}
      </h2>

      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((category) => (
          <ExploreNextCard key={category.id} category={category} />
        ))}
      </div>
    </section>
  );
}

function ExploreNextCard({ category }: { category: ExploreNextCategory }) {
  const [imageFailed, setImageFailed] = useState(false);

  return (
    <Link
      href={`/hashvaot/${category.id}`}
      className={cn(
        "group flex flex-col overflow-hidden rounded-[0.875rem] border border-black/8 bg-white",
        "shadow-[0_1px_3px_rgba(17,19,24,0.06),0_1px_2px_rgba(17,19,24,0.04)]",
        "transition-[transform,box-shadow] duration-200",
        "hover:-translate-y-0.5 hover:shadow-[0_18px_48px_-24px_rgba(17,19,24,0.22)]",
        "active:translate-y-0 active:shadow-[0_1px_3px_rgba(17,19,24,0.06)]",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <div className="relative aspect-[16/10] w-full shrink-0 overflow-hidden bg-[#F7F7F2]">
        {imageFailed ? (
          // Design Finding B: broken/missing stock image degrades to a plain
          // accent-tinted panel instead of a next/image broken-icon placeholder.
          <div
            aria-hidden
            className="absolute inset-0"
            style={{ backgroundColor: `${category.accent}22` }}
          />
        ) : (
          <Image
            src={category.image}
            alt=""
            fill
            aria-hidden
            sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
            className="object-cover"
            onError={() => setImageFailed(true)}
          />
        )}
        {/* Decorative category accent — non-text, so per-category color does
            not carry a WCAG 1.4.3 text-contrast obligation (unlike the CTA
            label below, which stays on the fixed brand link color). */}
        <span
          aria-hidden
          className="absolute inset-x-0 bottom-0 h-[3px]"
          style={{ backgroundColor: category.accent }}
        />
      </div>
      <div className="flex flex-1 flex-col gap-3 px-4 py-3.5">
        <h3 className="text-[0.95rem] font-extrabold tracking-[-0.01em] text-[#111318]">
          {category.label}
        </h3>
        {/*
         * CTA text uses the fixed brand link color (#167A58), not the
         * per-category accent: several accents (e.g. juices #E8A020, milk
         * #5C7FB0) fail WCAG 1.4.3 (~2.2:1 / ~4.1:1) as bold 12px text on
         * white — confirmed by `npm run test:a11y` against this component.
         * #167A58 is the same color already used for link text elsewhere
         * in this codebase (e.g. comparison-page.tsx blogLink, bread
         * dashboard CTAs) at the same or smaller sizes.
         *
         * Copy: "להשוואה" (Content gate-1 approved, TASK-507 fix #2) — the
         * original "לכל ההשוואות" implied linking to ALL comparisons, but each
         * card links to exactly one category.
         */}
        <span className="mt-auto inline-flex w-fit items-center gap-1.5 text-xs font-bold text-[#167A58]">
          להשוואה
          <ChevronLeft className="size-3.5 stroke-[2.5]" aria-hidden />
        </span>
      </div>
    </Link>
  );
}
