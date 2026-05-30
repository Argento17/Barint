"use client";

import { snackConfidenceTone } from "@/lib/comparisons/snack-page-data";
import type { SnackProduct } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

export function SnackConfidencePill({
  label,
  level,
  className,
}: {
  label: SnackProduct["confidence_label_he"];
  level: SnackProduct["confidence_level"];
  className?: string;
}) {
  const tone = snackConfidenceTone(level);

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

