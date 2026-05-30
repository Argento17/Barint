"use client";

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade } from "@/lib/view-models";

const GRADE_ACCENT_COLORS: Record<BariGrade, string> = {
  A: "#3E6B57",
  B: "#2F6E69",
  C: "#9A6D25",
  D: "#9A5A24",
  E: "#8A4338",
};

const GRADE_TINT_BACKGROUNDS: Record<BariGrade, string> = {
  A: "#F3F7F5",
  B: "#F1F7F6",
  C: "#F8F4EB",
  D: "#F8F1EA",
  E: "#F7EFED",
};

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
          borderLeft: "3px solid #9A9FA6",
        }}
      >
        <span className="text-[11px] font-semibold text-[#9A9FA6]">—</span>
      </div>
    );
  }

  const { borderColor } = BARI_COMPARISON_TOKENS.score.rowChip;
  const scoreSize = BARI_COMPARISON_TOKENS.layout.scoreChipSize;
  const accentColor = GRADE_ACCENT_COLORS[grade];
  const tintBackground = GRADE_TINT_BACKGROUNDS[grade];

  return (
    <div
      aria-label={`ציון ${Math.round(score)}, דרגה ${grade}`}
      className="inline-flex shrink-0 flex-col items-center justify-center rounded-lg text-center"
      style={{
        minWidth: "2.75rem",
        padding: "5px 8px",
        backgroundColor: tintBackground,
        border: `1px solid ${borderColor}`,
        borderLeft: `4px solid ${accentColor}`,
      }}
    >
      <span
        className="font-extrabold tabular-nums leading-none"
        style={{ fontSize: scoreSize, color: accentColor }}
        aria-hidden
      >
        {Math.round(score)}
      </span>
      <span
        className="font-bold leading-none mt-[3px]"
        style={{ fontSize: "10px" }}
        aria-hidden
      >
        <span style={{ color: accentColor }}>{grade}</span>
      </span>
    </div>
  );
}
