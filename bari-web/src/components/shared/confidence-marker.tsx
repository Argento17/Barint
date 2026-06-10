"use client";

import { cn } from "@/lib/utils";
import type { BariConfidence } from "@/lib/view-models";

// Score Confidence / Data-Completeness Indicators — collapsed-row marker (spec v1).
//
// This is the NON-HUE confidence channel that rides ALONGSIDE the grade chip. It never
// uses grade hue, never adds fill, never adds a second color scale (Hard Rule 1). It
// encodes confidence purely as texture/shape (TASK-226 DESIGN-LOCK, authority
// score_confidence_indicators_spec_v1.md §2–§4):
//   - verified     → nothing (solid chip, no marker)
//   - partial AND insufficient (non-suppressed rows) → IDENTICAL achromatic marker;
//                    the gap type is NOT branched on the row (it is differentiated only
//                    inside the expansion). 1px dotted achromatic ring on the chip's
//                    footprint (0 extra width) + a 6px grey dot in the chip's inline-start
//                    gutter. No text, no hue.
//   - insufficient rows whose chip is suppressed upstream show the null-state pill (§5)
//     in the chip's footprint instead (see NullScorePill below) — the pill carries the
//     signal, so no dot/ring there.
//
// Token values are the spec's named tokens, inlined here because the project has no CSS
// custom properties for them: --hairline = rgba(17,19,24,0.08), --fg3 = #5E6560
// (TASK-226 amendment — darker grey from the contrast-token decision, supersedes #7A817C),
// null-pill surface = #EEEEEA, null-pill border = rgba(17,19,24,0.07).

const HAIRLINE = "rgba(17,19,24,0.08)";
const FG3 = "#5E6560";
const NULL_PILL_BG = "#EEEEEA";
const NULL_PILL_BORDER = "rgba(17,19,24,0.07)";

/** Not-yet-scored copy. Verbatim per spec §5 — no digits, no grade letter. */
const NULL_PILL_LABEL = "טרם נוקד";

/**
 * The 6px grey dot in the chip's inline-start gutter (RTL: to the right of the chip,
 * before the name). Rendered for `partial` AND `insufficient` (identical marker — the
 * row does not branch by gap type; that distinction lives in the expansion). Decorative —
 * the confidence label is spelled out in the expansion; on the row the dot is a calm
 * "there is a note here" affordance. aria-hidden so it adds no screen-reader noise (the
 * row already exposes the full confidence sentence inside the expansion).
 */
export function ConfidenceDot({
  confidence,
  className,
}: {
  confidence: BariConfidence;
  className?: string;
}) {
  if (confidence === "verified") return null;
  return (
    <span
      aria-hidden
      className={cn("inline-block shrink-0 rounded-full", className)}
      style={{ width: "6px", height: "6px", backgroundColor: FG3 }}
    />
  );
}

/**
 * The dotted achromatic ring drawn on the chip's existing footprint. Rendered as an
 * absolutely-positioned overlay with `outline` (not border, not an extra box) so it adds
 * ZERO layout width and causes no CLS (spec §7, open-question §8.3). The parent must be
 * `position: relative`. Rendered for `partial` AND `insufficient` (identical marker).
 */
export function ConfidenceRing({
  confidence,
}: {
  confidence: BariConfidence;
}) {
  if (confidence === "verified") return null;
  return (
    <span
      aria-hidden
      className="pointer-events-none absolute inset-0 rounded-xl"
      style={{
        // 1px dotted achromatic ring, drawn just outside the chip's border box via a
        // small positive outline-offset — no layout box, no width change.
        outline: `1px dotted ${HAIRLINE}`,
        outlineOffset: "1px",
      }}
    />
  );
}

/**
 * State 7 null-state pill (spec §5). Replaces the grade chip in its footprint when the
 * product is `insufficient`: same width band / radius / row height as the chip so a shelf
 * mixing scored and not-yet-scored rows has no layout shift. SOLID hairline border (not
 * dotted — there is no score to caveat), `#EEEEEA` surface, the words `טרם נוקד` centered.
 * No digits, no grade letter, no grade hue.
 */
export function NullScorePill({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "inline-flex w-[4.25rem] flex-col items-center justify-center rounded-xl px-2 py-1.5 text-center",
        className
      )}
      style={{
        backgroundColor: NULL_PILL_BG,
        border: `1px solid ${NULL_PILL_BORDER}`,
      }}
      aria-label={NULL_PILL_LABEL}
    >
      <span
        className="whitespace-nowrap text-[0.7rem] font-bold leading-none"
        style={{ color: FG3 }}
        aria-hidden
      >
        {NULL_PILL_LABEL}
      </span>
    </div>
  );
}
