"use client";

import { Info } from "lucide-react";

import { cn } from "@/lib/utils";
import { DEGRADATION_LABELS } from "@/lib/comparisons/milk-page-data";
import type { MatrixIntegrity } from "@/lib/comparisons/milk-types";

export function MatrixIntegrityBadge({
  matrix,
  compact = false,
}: {
  matrix: MatrixIntegrity;
  compact?: boolean;
}) {
  const levelHe =
    DEGRADATION_LABELS[matrix.structural_degradation_level] ??
    matrix.structural_degradation_level;

  return (
    <span className="group relative inline-flex">
      <span
        className={cn(
          "inline-flex items-center gap-1.5 rounded-lg border border-black/[0.08] bg-[#F7F7F2]/90 font-semibold text-[#4E5663]",
          compact ? "px-2 py-1 text-[0.65rem]" : "px-2.5 py-1.5 text-xs"
        )}
      >
        <span className="font-extrabold tabular-nums text-[#111318]">
          {Math.round(matrix.matrix_integrity_score)}
        </span>
        <span className="text-[#7A817C]">שלמות מטריצה</span>
        {!compact ? <span className="text-[#1F8F6A]">· {levelHe}</span> : null}
        <Info className="size-3 text-[#7A817C]" aria-hidden />
      </span>
      <span
        role="tooltip"
        className="pointer-events-none absolute bottom-full left-1/2 z-30 mb-2 w-56 -translate-x-1/2 rounded-xl border border-black/[0.08] bg-[#FFFFFF] px-3 py-2 text-center text-[0.7rem] leading-relaxed text-[#4E5663] opacity-0 shadow-lg transition-opacity group-hover:opacity-100 group:focus-within:opacity-100"
      >
        {matrix.integrity_summary}
        {matrix.dominant_matrix_signals.length > 0 ? (
          <>
            <br />
            <span className="mt-1 block text-[#111318]">
              {matrix.dominant_matrix_signals.join(" · ")}
            </span>
          </>
        ) : null}
      </span>
    </span>
  );
}
