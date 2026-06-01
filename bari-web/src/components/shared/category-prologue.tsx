"use client";

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function CategoryPrologue({
  sentences,
  wide = false,
}: {
  sentences: string[];
  wide?: boolean;
}) {
  return (
    <section
      className={cn(
        "px-4 pb-3",
        wide && cn(comparisonWebSectionPaddingClass(), "lg:pb-2 lg:pt-0")
      )}
    >
      <div className="space-y-2">
        {sentences.map((sentence, index) => (
          <p
            key={`${index}-${sentence.slice(0, 16)}`}
            className="text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]"
          >
            {sentence}
          </p>
        ))}
      </div>
    </section>
  );
}
