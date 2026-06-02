"use client";

import { cn } from "@/lib/utils";
import type { BariConfidence } from "@/lib/view-models";

// comparison_ui_reference_v2 §5 — confidence promoted onto the collapsed row,
// out of the 10px expansion footnote, beside the grade/score chip group.
// Calm tones, not alarm. The expansion no longer repeats it (de-dup, §6/§7).

const CONFIDENCE_LABELS: Record<BariConfidence, string> = {
  verified: "נתונים מלאים",
  partial: "נתונים חלקיים",
  insufficient: "נתונים חסרים",
};

// graphite → muted, never red (calm editorial tokens, §1.7)
const CONFIDENCE_DOT: Record<BariConfidence, string> = {
  verified: "#1F8F6A",
  partial: "#B5882F",
  insufficient: "#B5BBB6",
};

/**
 * Row-level confidence indicator. `variant="dot"` is a compact dot + short label
 * for the tight mobile row; `variant="pill"` is a bordered chip for the desktop row.
 */
export function ConfidenceIndicator({
  confidence,
  variant = "dot",
  className,
}: {
  confidence: BariConfidence;
  variant?: "dot" | "pill";
  className?: string;
}) {
  const label = CONFIDENCE_LABELS[confidence];
  const dot = CONFIDENCE_DOT[confidence];

  if (variant === "pill") {
    return (
      <span
        className={cn(
          "inline-flex items-center gap-1.5 rounded-full border border-black/[0.07] bg-white px-2 py-0.5",
          className
        )}
        aria-label={label}
      >
        <span
          className="size-1.5 shrink-0 rounded-full"
          style={{ backgroundColor: dot }}
          aria-hidden
        />
        <span className="text-[11px] font-medium leading-none text-[#6E756F]" aria-hidden>
          {label}
        </span>
      </span>
    );
  }

  return (
    <span
      className={cn("inline-flex items-center gap-1", className)}
      aria-label={label}
    >
      <span
        className="size-1.5 shrink-0 rounded-full"
        style={{ backgroundColor: dot }}
        aria-hidden
      />
      <span className="text-[10px] font-medium leading-none text-[#9A9FA6]" aria-hidden>
        {label}
      </span>
    </span>
  );
}
