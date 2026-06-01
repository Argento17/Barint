"use client";

import type { BreadConfidenceLevel, BreadProduct } from "@/lib/comparisons/bread-types";
import { confidenceTone } from "@/lib/comparisons/bread-page-data";
import { cn } from "@/lib/utils";

export function BreadConfidencePill({
  label,
  level,
  className,
}: {
  label: BreadProduct["confidence_label_he"];
  level: BreadConfidenceLevel;
  className?: string;
}) {
  const tone = confidenceTone(level);

  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border px-2.5 py-1 text-[0.68rem] font-semibold",
        tone.pill,
        className
      )}
    >
      <span className={cn("size-1.5 rounded-full", tone.dot)} aria-hidden />
      {label}
    </span>
  );
}
