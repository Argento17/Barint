"use client";

import { cn } from "@/lib/utils";
import type { BariConfidence } from "@/lib/view-models";

import { ConfidenceDot } from "@/components/shared/confidence-marker";

// TASK-226 — superseded model removed. The previous version of this component implemented
// `comparison_ui_reference_v2`'s collapsed-row confidence (hued #1F8F6A/#B5882F dots +
// `נתונים מלאים`/`נתונים חלקיים`/`נתונים חסרים` text labels, plus a bordered desktop pill).
// That model is overridden by score_confidence_indicators_spec_v1.md (D12, 2026-06-10):
//   - verified → renders NOTHING on the row.
//   - partial / insufficient → IDENTICAL achromatic marker (no hue, no text label).
// The canonical marker now lives in `confidence-marker.tsx` and the live row imports it
// directly. This file is retained only as a thin, spec-conformant alias so no caller can
// resurrect the hued/text-label pattern. No grade hue, no Hebrew row label here.

/**
 * @deprecated Use `ConfidenceDot` / `ConfidenceRing` from `confidence-marker.tsx`.
 * Kept as an achromatic, label-free alias. `variant` is ignored — desktop and mobile get
 * the same marker (DESIGN-LOCK: no bordered desktop pill, no text).
 */
export function ConfidenceIndicator({
  confidence,
  className,
}: {
  confidence: BariConfidence;
  variant?: "dot" | "pill";
  className?: string;
}) {
  return <ConfidenceDot confidence={confidence} className={cn(className)} />;
}
