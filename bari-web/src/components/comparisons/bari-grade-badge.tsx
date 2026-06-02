"use client";

import { cn } from "@/lib/utils";
import type { BariGrade } from "@/lib/comparisons/milk-types";
import {
  BARI_COMPARISON_TOKENS,
  gradeDotOffset,
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
        "relative",
        rowTokens.container,
        size === "sm" && rowTokens.size.sm,
        size === "md" && rowTokens.size.md,
        size === "lg" && rowTokens.size.lg
      )}
      style={{
        backgroundColor: colors.bg,
        borderColor: colors.border,
        borderInlineStart: `4px solid ${colors.accent}`,
      }}
    >
      <span
        aria-hidden
        className="pointer-events-none absolute block rounded-full bg-white"
        style={{
          width: "3px",
          height: "3px",
          insetInlineStart: "0.5px",
          top: gradeDotOffset(colors.dot),
          transform: "translateY(-50%)",
        }}
      />
      <span
        className={cn(
          rowTokens.scoreClass,
          size === "sm" && rowTokens.scoreSize.sm,
          size === "md" && rowTokens.scoreSize.md,
          size === "lg" && rowTokens.scoreSize.lg
        )}
        style={{ color: colors.accent }}
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
        <span style={{ color: colors.accent }}>{grade}</span>
        <span> · {gradeLabel}</span>
      </span>
    </div>
  );
}
