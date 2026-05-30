"use client";

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function CategoryHero({
  eyebrow,
  title,
  metadata,
  wide = false,
}: {
  eyebrow: string;
  title: string;
  metadata: string;
  wide?: boolean;
}) {
  return (
    <header
      className={cn(
        "px-4 pt-4 pb-2",
        wide && cn(comparisonWebSectionPaddingClass(), "lg:pt-5 lg:pb-1.5")
      )}
    >
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
      <p className={cn("mt-1 text-[12px] leading-snug text-[#6A716E]", wide && "lg:text-[13px]")}>
        {metadata}
      </p>
    </header>
  );
}
