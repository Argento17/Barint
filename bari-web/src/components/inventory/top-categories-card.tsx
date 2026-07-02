"use client";

/**
 * TopCategoriesCard — sorted descending by count, rank-numbered, clickable.
 *
 * Changes from v1:
 *  • Sorted: categories come in from the loader but we re-sort desc by count
 *    here so the component is self-contained (biggest category = rank 1).
 *  • Rank tile: replaces the first-Hebrew-letter with a bold rank number (1,2,3…).
 *    Keeps the dominantGrade tint background so quality reads at a glance.
 *  • Clickable: each row calls onCategorySelect(categoryId). The currently-active
 *    row has a tint + ring. Clicking the active row a second time clears the filter.
 *    Keyboard-accessible: <button>, aria-pressed, Enter/Space.
 *
 * Props:
 *  categories       — from InventorySummaryVM.topCategories (unsorted or sorted — we re-sort)
 *  onCategorySelect — called with categoryId or "" (clear)
 *  activeCategoryId — the currently-selected categoryId, or "" for none
 *
 * NO imports from scoring/bsip/registry/comparisons modules.
 */

import { ChevronLeft } from "lucide-react";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade } from "@/lib/view-models";

interface TopCategoryRow {
  categoryId: string;
  nameHe: string;
  count: number;
  dominantGrade: BariGrade | null;
}

interface TopCategoriesCardProps {
  categories: TopCategoryRow[];
  activeCategoryId?: string;
  onCategorySelect?: (categoryId: string) => void;
}

function RankTile({
  rank,
  grade,
}: {
  rank: number;
  grade: BariGrade | null;
}) {
  const style: React.CSSProperties = {
    width: 30,
    height: 30,
    borderRadius: 9,
    fontSize: 13,
    fontWeight: 800,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    fontVariantNumeric: "tabular-nums",
    fontFamily: "var(--font-mono, ui-monospace, monospace)",
  };

  if (grade === null) {
    return (
      <span
        style={{
          ...style,
          background: "var(--surface-neutral, #F2F2ED)",
          color: "var(--fg3, #5E6560)",
        }}
        aria-hidden="true"
      >
        {rank}
      </span>
    );
  }

  const p = BARI_COMPARISON_TOKENS.gradePalette[grade];
  return (
    <span
      style={{ ...style, background: p.bg, color: p.text }}
      aria-hidden="true"
    >
      {rank}
    </span>
  );
}

export function TopCategoriesCard({
  categories,
  activeCategoryId = "",
  onCategorySelect,
}: TopCategoriesCardProps) {
  if (categories.length === 0) {
    return (
      <p className="text-sm" style={{ color: "var(--fg3, #5E6560)" }}>
        אין קטגוריות.
      </p>
    );
  }

  // Sort descending by count — biggest first = rank 1
  const sorted = [...categories].sort((a, b) => b.count - a.count);

  // role=group (not list): the rows are toggle BUTTONS (filter select/clear), so they
  // must keep the native button role — role="listitem" would override it and does not
  // support aria-pressed (jsx-a11y/role-supports-aria-props, QA gate-2 F-V3).
  return (
    <div className="flex flex-col" role="group" aria-label="קטגוריות מובילות">
      {sorted.map((cat, idx) => {
        const rank = idx + 1;
        const isActive = cat.categoryId === activeCategoryId;

        return (
          <button
            key={cat.categoryId}
            type="button"
            aria-pressed={isActive}
            onClick={() => onCategorySelect?.(isActive ? "" : cat.categoryId)}
            className="flex w-full items-center gap-3 rounded-[10px] px-1.5 py-2 text-start transition-colors"
            style={{
              background: isActive ? "var(--grade-a-bg, #E7F4EC)" : "transparent",
              outline: isActive ? "1.5px solid rgba(30,122,79,0.30)" : "none",
              outlineOffset: -1,
              cursor: "pointer",
              border: "none",
            }}
            onMouseEnter={(e) => {
              if (!isActive) (e.currentTarget as HTMLButtonElement).style.background = "#F7F7F2";
            }}
            onMouseLeave={(e) => {
              if (!isActive) (e.currentTarget as HTMLButtonElement).style.background = "transparent";
            }}
          >
            <RankTile rank={rank} grade={cat.dominantGrade} />

            <span
              className="flex-1 min-w-0 truncate text-start"
              style={{
                fontSize: 14,
                fontWeight: isActive ? 600 : 500,
                color: "var(--fg1, #111318)",
              }}
            >
              {cat.nameHe}
            </span>

            <span
              className="shrink-0 tabular-nums"
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: "var(--fg2, #4E5663)",
                fontFamily: "var(--font-mono, ui-monospace, monospace)",
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {cat.count.toLocaleString("he-IL")}
            </span>

            <ChevronLeft
              className="shrink-0"
              style={{
                width: 16,
                height: 16,
                color: isActive ? "var(--bari-green, #1F8F6A)" : "#C7C9C3",
              }}
              aria-hidden
            />
          </button>
        );
      })}
    </div>
  );
}
