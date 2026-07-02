/**
 * InventoryGradeChip — shared between /admin/inventory and /catalog.
 *
 * Grade chip: A/B green, C amber, D terracotta, E red — from BARI_COMPARISON_TOKENS.gradePalette.
 * Unscored (grade === null) → calm "—" chip, never an error look.
 *
 * Dimensions (H3): height 26px, min-width 30px, padding 0 8px, border-radius 8px, font 800 14px.
 * Matches reference line 174.
 *
 * Token map:
 *   Unscored background: --surface-neutral (nearest sanctioned surface, #F2F2ED canonical fallback)
 *   Unscored text: --fg3 (#5E6560) — legible muted caption text, ≥4.5:1 on white
 *   Grade colors: from BARI_COMPARISON_TOKENS.gradePalette (token-sourced)
 */

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade } from "@/lib/view-models";

interface InventoryGradeChipProps {
  grade: BariGrade | null;
}

export function InventoryGradeChip({ grade }: InventoryGradeChipProps) {
  if (grade === null) {
    return (
      <span
        role="img"
        aria-label="לא נוקד"
        className="inline-flex items-center justify-center rounded-lg font-bold"
        style={{
          height: 26,
          minWidth: 30,
          padding: "0 8px",
          background: "var(--surface-neutral, #F2F2ED)",
          color: "var(--fg3, #5E6560)",
          border: "1px solid rgba(17,19,24,0.08)",
          fontSize: 14,
          fontWeight: 800,
        }}
      >
        —
      </span>
    );
  }

  const palette = BARI_COMPARISON_TOKENS.gradePalette[grade];

  return (
    <span
      role="img"
      aria-label={`דרגה ${grade}`}
      className="inline-flex items-center justify-center rounded-lg font-extrabold"
      style={{
        height: 26,
        minWidth: 30,
        padding: "0 8px",
        borderRadius: 8,
        background: palette.bg,
        color: palette.text,
        border: `1px solid ${palette.border}`,
        fontSize: 14,
        fontWeight: 800,
      }}
    >
      {grade}
    </span>
  );
}
