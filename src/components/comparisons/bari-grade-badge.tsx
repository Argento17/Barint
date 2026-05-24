"use client";

import { cn } from "@/lib/utils";
import { GRADE_COLORS } from "@/lib/comparisons/milk-page-data";
import type { BariGrade } from "@/lib/comparisons/milk-types";

export function BariGradeBadge({
  score,
  grade,
  gradeLabel,
  size = "md",
}: {
  score: number;
  grade: BariGrade;
  gradeLabel: string;
  size?: "sm" | "md" | "lg";
}) {
  const colors = GRADE_COLORS[grade] ?? GRADE_COLORS.C;

  return (
    <div
      className={cn(
        "inline-flex flex-col items-center justify-center rounded-xl border text-center shadow-sm",
        size === "sm" && "min-w-[3.25rem] px-2 py-1.5",
        size === "md" && "min-w-[4rem] px-2.5 py-2",
        size === "lg" && "min-w-[4.5rem] px-3 py-2.5"
      )}
      style={{
        backgroundColor: colors.bg,
        color: colors.text,
        borderColor: colors.border,
      }}
    >
      <span
        className={cn(
          "font-extrabold tabular-nums leading-none",
          size === "sm" && "text-lg",
          size === "md" && "text-xl",
          size === "lg" && "text-2xl"
        )}
      >
        {Math.round(score)}
      </span>
      <span
        className={cn(
          "mt-0.5 font-bold opacity-90",
          size === "sm" && "text-[0.6rem]",
          size === "md" && "text-[0.65rem]",
          size === "lg" && "text-xs"
        )}
      >
        {grade} · {gradeLabel}
      </span>
    </div>
  );
}
