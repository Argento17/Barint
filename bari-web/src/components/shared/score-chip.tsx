"use client";

import {
  BARI_COMPARISON_TOKENS,
  gradeDotOffset,
} from "@/lib/design/bari-comparison-tokens";
import type { BariGrade } from "@/lib/view-models";

export function ScoreChip({
  score,
  grade,
}: {
  score: number | null;
  grade: BariGrade | null;
}) {
  if (score == null || grade == null) {
    return (
      <div
        aria-label="ללא ציון"
        className="inline-flex shrink-0 flex-col items-center justify-center rounded-lg text-center"
        style={{
          minWidth: "2.75rem",
          padding: "5px 8px",
          backgroundColor: "#EEEEEA",
          border: "1px solid rgba(17,19,24,0.07)",
          borderInlineStart: "3px solid #9A9FA6",
        }}
      >
        <span className="text-[11px] font-semibold text-[#9A9FA6]">—</span>
      </div>
    );
  }

  const palette =
    BARI_COMPARISON_TOKENS.gradePalette[grade] ??
    BARI_COMPARISON_TOKENS.gradePalette.C;
  const scoreSize = BARI_COMPARISON_TOKENS.layout.scoreChipSize;

  return (
    <div
      aria-label={`ציון ${Math.round(score)}, דרגה ${grade}`}
      className="relative inline-flex shrink-0 flex-col items-center justify-center rounded-lg text-center"
      style={{
        minWidth: "2.75rem",
        padding: "5px 8px",
        backgroundColor: palette.bg,
        border: `1px solid ${palette.border}`,
        borderInlineStart: `4px solid ${palette.accent}`,
      }}
    >
      <span
        aria-hidden
        className="pointer-events-none absolute inset-inline-start-0 block rounded-full bg-white"
        style={{
          width: "3px",
          height: "3px",
          insetInlineStart: "0.5px",
          top: gradeDotOffset(palette.dot),
          transform: "translateY(-50%)",
        }}
      />
      <span
        className="font-extrabold tabular-nums leading-none"
        style={{ fontSize: scoreSize, color: palette.accent }}
        aria-hidden
      >
        {Math.round(score)}
      </span>
      <span
        className="font-bold leading-none mt-[3px]"
        style={{ fontSize: "10px" }}
        aria-hidden
      >
        <span style={{ color: palette.accent }}>{grade}</span>
      </span>
    </div>
  );
}
