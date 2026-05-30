"use client";

import { cn } from "@/lib/utils";
import type { BariGrade } from "@/lib/comparisons/milk-types";
import {
  BARI_COMPARISON_TOKENS,
  warnComparisonImplementationDeviation,
} from "@/lib/design/bari-comparison-tokens";

export function BariGradeBadge({
  score,
  grade,
  gradeLabel,
  size = "md",
  context = "row",
}: {
  score: number;
  grade: BariGrade;
  gradeLabel: string;
  size?: "sm" | "md" | "lg";
  context?: "row" | "hero";
}) {
  const colors =
    BARI_COMPARISON_TOKENS.gradePalette[grade] ??
    BARI_COMPARISON_TOKENS.gradePalette.C;

  if (context === "hero") {
    const heroTokens = BARI_COMPARISON_TOKENS.score.hero;
    return (
      <div className={heroTokens.container}>
        <p
          className={cn(
            heroTokens.scoreClass,
            size === "sm" && heroTokens.scoreSize.sm,
            size === "md" && heroTokens.scoreSize.md,
            size === "lg" && heroTokens.scoreSize.lg
          )}
          style={{ color: colors.text }}
        >
          {Math.round(score)}
        </p>
        <p
          className={cn(
            heroTokens.labelClass,
            size === "sm" && heroTokens.labelSize.sm,
            size === "md" && heroTokens.labelSize.md,
            size === "lg" && heroTokens.labelSize.lg
          )}
          style={{ color: colors.text }}
        >
          {grade} · {gradeLabel}
        </p>
      </div>
    );
  }

  const rowTokens = BARI_COMPARISON_TOKENS.score.rowChip;
  if (context !== "row") {
    warnComparisonImplementationDeviation(
      "BariGradeBadge",
      `unexpected score context "${context}"`
    );
  }

  return (
    <div
      className={cn(
        rowTokens.container,
        size === "sm" && rowTokens.size.sm,
        size === "md" && rowTokens.size.md,
        size === "lg" && rowTokens.size.lg
      )}
      style={{
        backgroundColor: rowTokens.backgroundColor,
        color: "#313834",
        borderColor: rowTokens.borderColor,
      }}
    >
      <span
        className={cn(
          rowTokens.scoreClass,
          size === "sm" && rowTokens.scoreSize.sm,
          size === "md" && rowTokens.scoreSize.md,
          size === "lg" && rowTokens.scoreSize.lg
        )}
      >
        {Math.round(score)}
      </span>
      <span
        className={cn(
          rowTokens.labelClass,
          size === "sm" && rowTokens.labelSize.sm,
          size === "md" && rowTokens.labelSize.md,
          size === "lg" && rowTokens.labelSize.lg
        )}
      >
        {grade} · {gradeLabel}
      </span>
    </div>
  );
}
