"use client";

import { useState } from "react";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

// TASK-384 FIX: collapseMobile — on mobile (< md), shows the first sentence with a
// "קרא עוד" toggle; remaining sentences expand inline. Content stays in DOM for SEO.
// Desktop (md+) always shows all sentences. Default false — existing callers unchanged.
const PROLOGUE_MOBILE_VISIBLE = 1;

export function CategoryPrologue({
  sentences,
  wide = false,
  collapseMobile = false,
}: {
  sentences: string[];
  wide?: boolean;
  collapseMobile?: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const hasMore = collapseMobile && sentences.length > PROLOGUE_MOBILE_VISIBLE;

  return (
    <section
      className={cn(
        // TASK-384: when collapseMobile active, use pb-2 on mobile to recover 4px of
        // vertical space, pushing the product table up so ≥3 rows clear the fold.
        collapseMobile ? "px-4 pb-2 md:pb-3" : "px-4 pb-3",
        wide && cn(comparisonWebSectionPaddingClass(), "lg:pb-2 lg:pt-0")
      )}
    >
      <div className="space-y-2">
        {sentences.map((sentence, index) => {
          const hiddenOnMobile = hasMore && index >= PROLOGUE_MOBILE_VISIBLE && !expanded;
          return (
            <p
              key={`${index}-${sentence.slice(0, 16)}`}
              className={cn(
                "text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]",
                hiddenOnMobile ? "hidden md:block" : undefined
              )}
            >
              {sentence}
            </p>
          );
        })}
      </div>

      {/* Expand/collapse toggle — mobile only, only when collapseMobile is active */}
      {hasMore && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className={cn(
            "mt-1 text-[11px] font-semibold text-[#1F8F6A] hover:underline focus:outline-none",
            "md:hidden"
          )}
          aria-expanded={expanded}
        >
          {expanded ? "הצג פחות ▲" : "קרא עוד ▼"}
        </button>
      )}
    </section>
  );
}
