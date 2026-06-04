"use client";

// TASK-181I — Glass Box W4 D3 processing-signal surface.
//
// Renders the engine-emitted `note_he` (the calm "how processed is this food" line) as a
// quiet drilldown footnote inside the expansion — NOT a headline, NOT a banner, NOT a chip.
// Matches the D5 "מה לא צוין בתווית" register (small label + muted line). Disclosure surface
// only: no score, no number, no engine term (NOVA / cap / modifier never reach JSX).
//
// HARD: the Hebrew is rendered VERBATIM from the engine. This component does NOT author,
// rewrite, or interpolate any consumer copy — it only chooses which engine string to show
// (full vs mobile-compressed) and presents low-confidence honestly as provisional.
//
// Confidence honesty (spec §3.3, EV-042):
//   - high / medium → the line reads as a factual population-level association (Candidate A/B).
//   - low           → the line is the provisional Candidate C wording; we additionally render
//                      it in the quieter "uncertain" tone (same muted gold the D5/D6 calm-
//                      uncertainty pattern uses) so it never reads as a hard verdict.
//
// Mobile-compressed variant (Candidate C): note_he_mobile is shown on small screens, the full
// note_he on desktop/professional. Implemented with CSS breakpoints (SSR-safe, zero layout
// shift, no JS media-query hook) at the 375px primary viewport. When the engine sends no
// mobile variant (Candidates A/B), the full note renders on all widths.

import { GLASS_BOX_PROCESSING_HEADING } from "@/lib/view-models";
import type { BariProcessingSignalVM } from "@/lib/view-models";

const HEADING = GLASS_BOX_PROCESSING_HEADING;

// Calm-uncertainty tone for low confidence mirrors the D5/D6 `ניתוח חלקי` muted gold
// (#8A7430 text), deliberately quieter than any warning red. high/medium use the neutral
// drilldown grey shared with the other expansion footnotes.
const LOW_CONFIDENCE_COLOR = "#8A7430";
const NEUTRAL_COLOR = "#6E756F";

function SectionLabel({ children }: { children: string }) {
  return (
    <p className="text-[11px] font-bold leading-snug tracking-[0.01em] text-[#4A524E]">
      {children}
    </p>
  );
}

/**
 * D3 processing-signal drilldown line. Flag-gated upstream — this component is only
 * mounted when NEXT_PUBLIC_GLASSBOX_W4 is ON and the product carries a d3_processing
 * signal with a non-empty note. Renders nothing if there is no note to show.
 */
export function ProcessingSignalNote({ signal }: { signal: BariProcessingSignalVM }) {
  const full = signal.note_he?.trim();
  const mobile = signal.note_he_mobile?.trim();

  // No engine-emitted note → no surface (e.g. NOVA-2 non-low → note_he = null).
  if (!full && !mobile) return null;

  const isLow = signal.confidence === "low";
  const color = isLow ? LOW_CONFIDENCE_COLOR : NEUTRAL_COLOR;
  const confidenceNote = signal.confidence_note?.trim();

  // When a mobile-compressed variant exists, swap the two strings purely with CSS so the
  // mobile form shows ≤ sm and the full form shows ≥ sm. No JS, no hydration mismatch.
  const hasMobileVariant = Boolean(mobile && full && mobile !== full);

  return (
    <div className="pt-2.5" dir="rtl">
      <SectionLabel>{HEADING}</SectionLabel>
      {hasMobileVariant ? (
        <>
          {/* Mobile (< sm, 375px primary viewport): compressed Candidate C variant. */}
          <p
            className="mt-1.5 text-[12px] leading-relaxed sm:hidden"
            style={{ color }}
          >
            {mobile}
          </p>
          {/* Desktop / professional (≥ sm): full form. */}
          <p
            className="mt-1.5 hidden text-[12px] leading-relaxed sm:block"
            style={{ color }}
          >
            {full}
          </p>
        </>
      ) : (
        <p className="mt-1.5 text-[12px] leading-relaxed" style={{ color }}>
          {full ?? mobile}
        </p>
      )}
      {confidenceNote ? (
        <p className="mt-1 text-[11px] leading-relaxed text-[#9A9FA6]">
          {confidenceNote}
        </p>
      ) : null}
    </div>
  );
}
