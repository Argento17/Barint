"use client";

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function MethodologyFooter({ lines, wide = false }: { lines: string[]; wide?: boolean }) {
  return (
    <footer
      className={cn("px-4 pt-4 pb-6", wide && cn(comparisonWebSectionPaddingClass(), "lg:pb-8 lg:pt-3"))}
    >
      <div className="space-y-1.5">
        {lines.map((line, index) => (
          <p key={`${index}-${line.slice(0, 14)}`} className="text-[11px] leading-relaxed text-[#8A908B]">
            {line}
          </p>
        ))}
      </div>
    </footer>
  );
}
