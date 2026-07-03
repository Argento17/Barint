"use client";

import type { ReactNode } from "react";

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function CategoryHero({
  eyebrow,
  title,
  metadata,
  wide = false,
  mascot,
}: {
  eyebrow: string;
  title: string;
  metadata: string;
  wide?: boolean;
  /**
   * Optional decorative mascot rendered at the hero's left (RTL end). When absent,
   * the header renders byte-identically to the frozen golden template — so this is a
   * no-op for every category except the one that opts in. Decorative only.
   */
  mascot?: ReactNode;
}) {
  const content = (
    <>
      <p className="font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80">
        {eyebrow}
      </p>
      <h1
        className={cn(
          "mt-1 text-[1.35rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318]",
          wide && "lg:text-[1.75rem]"
        )}
      >
        {title}
      </h1>
      <p className={cn("mt-1 text-[12px] leading-snug text-[#4E5663]", wide && "lg:text-[13px]")}>
        {metadata}
      </p>
    </>
  );

  return (
    <header
      className={cn(
        "px-4 pt-4 pb-2",
        wide && cn(comparisonWebSectionPaddingClass(), "lg:pt-5 lg:pb-1.5")
      )}
    >
      {mascot ? (
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">{content}</div>
          {mascot}
        </div>
      ) : (
        content
      )}
    </header>
  );
}
