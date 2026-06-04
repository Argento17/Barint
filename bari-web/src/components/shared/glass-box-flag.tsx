"use client";

import { cn } from "@/lib/utils";
import {
  GLASS_BOX_PARTIAL_LABEL,
  GLASS_BOX_PARTIAL_TOOLTIP,
} from "@/lib/view-models";

// TASK-179I Wave 1 — Glass Box D5/D6 consumer presentation (DEC-006).
//
// The `ניתוח חלקי` (partial analysis) indicator shown beside the grade chip on a DEMOTED
// row. Register is calm and factual, NEVER alarmist and NEVER an accusation (Q2): opacity
// is a disclosure/confidence condition, not a claim that the maker is hiding something.
// Tone mirrors the existing ConfidenceIndicator (muted gold #B5882F on a soft tint),
// deliberately quieter than any error/warning red.
//
// This is a small inline pill — not a banner, not a modal. Mobile-first.

// Label + tooltip come from the Content-owned copy map (single source of truth).
const PARTIAL_LABEL = GLASS_BOX_PARTIAL_LABEL;

/**
 * Inline `ניתוח חלקי` pill for a demoted product. Calm muted-gold tone, no icon noise.
 * The tooltip (GLASS_BOX_PARTIAL_TOOLTIP) explains the pill in one plain line on hover/tap.
 */
export function GlassBoxPartialFlag({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-1.5 py-0.5",
        className
      )}
      style={{
        backgroundColor: "#FBF8EE",
        borderColor: "#ECE3C8",
      }}
      aria-label={PARTIAL_LABEL}
      title={GLASS_BOX_PARTIAL_TOOLTIP}
    >
      <span
        className="size-1.5 shrink-0 rounded-full"
        style={{ backgroundColor: "#B5882F" }}
        aria-hidden
      />
      <span
        className="text-[10px] font-semibold leading-none text-[#8A7430]"
        aria-hidden
      >
        {PARTIAL_LABEL}
      </span>
    </span>
  );
}
