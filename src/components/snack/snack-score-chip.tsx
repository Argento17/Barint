"use client";

import type { SnackGrade } from "@/lib/comparisons/snack-types";
import {
  BARI_COMPARISON_TOKENS,
  warnComparisonImplementationDeviation,
} from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function SnackScoreChip({
  score,
  grade,
  displayable = true,
  variant = "card",
  className,
}: {
  score: number | null;
  grade: SnackGrade | null;
  displayable?: boolean;
  variant?: "card" | "comparison" | "hero";
  className?: string;
}) {
  if (className) {
    warnComparisonImplementationDeviation(
      "SnackScoreChip",
      "custom className override detected"
    );
  }

  if (!displayable || score == null || !grade) {
    return (
      <span
        className={cn(
          "inline-flex rounded-full border border-[#8A8F98]/20 bg-[#EEF0F2] px-3 py-1.5 text-sm font-semibold text-[#4E5663]",
          className
        )}
      >
        לא נוקד
      </span>
    );
  }

  const colors =
    BARI_COMPARISON_TOKENS.gradePalette[grade] ??
    BARI_COMPARISON_TOKENS.gradePalette.C;
  const rowTokens = BARI_COMPARISON_TOKENS.score.rowChip;
  const heroTokens = BARI_COMPARISON_TOKENS.score.hero;

  if (variant === "card") {
    return (
      <div
        className={cn(
          rowTokens.container,
          rowTokens.size.md,
          className
        )}
        style={{
          backgroundColor: rowTokens.backgroundColor,
          borderColor: rowTokens.borderColor,
          color: "#313834",
        }}
      >
        <span className={cn(rowTokens.scoreClass, rowTokens.scoreSize.md)}>{Math.round(score)}</span>
        <span className={cn(rowTokens.labelClass, rowTokens.labelSize.md)}>{grade}</span>
      </div>
    );
  }

  if (variant === "hero") {
    return (
      <div className={cn(heroTokens.container, className)}>
        <span className={cn(heroTokens.scoreClass, heroTokens.scoreSize.sm)} style={{ color: colors.text }}>
          {Math.round(score)}
        </span>
        <span className={cn(heroTokens.labelClass, heroTokens.labelSize.sm)} style={{ color: colors.text }}>
          {grade}
        </span>
      </div>
    );
  }

  if (variant !== "comparison") {
    warnComparisonImplementationDeviation(
      "SnackScoreChip",
      `unsupported variant "${variant}"`
    );
  }

  return (
    <div
      className={cn(
        BARI_COMPARISON_TOKENS.score.comparisonChip.container,
        BARI_COMPARISON_TOKENS.score.comparisonChip.size,
        className
      )}
      style={{
        backgroundColor: colors.bg,
        color: colors.text,
        borderColor: colors.border,
      }}
    >
      <span
        className={BARI_COMPARISON_TOKENS.score.comparisonChip.gradeClass}
      >
        {grade}
      </span>
      <span className={BARI_COMPARISON_TOKENS.score.comparisonChip.scoreClass}>
        {Math.round(score)}
      </span>
    </div>
  );
}
