// Bar-state UI primitive (TASK-504, verdict-color spec v1 — final polish).
//
// Renders one of 5 explicit states for a supplement-guide bar: PASS / FLAG / FAIL /
// CANNOT_VERIFY / EVIDENCE_LIMITED (the 5th added TASK-575, gate-2 HIGH-1 ruling,
// nutrition spec §11 — see GuideBarState in view-models/guide.ts for the full
// rationale). This is NOT the A–E ScoreChip grade system — no letter grade, no numeric
// score, ever. Guides retire ordinal scoring entirely (plan §1).
//
// Color source note (owner-directed semantic-color pass,
// 03_operations/reports/design/magnesium_guide_verdict_color_spec_v1.md §3): this
// palette WAS a deliberately non-semantic teal/indigo/berry/gray set (see the
// superseded TASK-504B reasoning this comment used to carry — a green/amber/red ramp
// risked pattern-matching onto the frozen A–E `gradePalette` ramp). The owner's
// directive for the GUIDES surface specifically overrides that caution: guides carry
// NO numeric score and NO A–E letter anywhere (`GuideProductVM` has no score/grade
// field), and a guide page never renders beside a `/hashvaot` comparison row, so there
// is no page where a reader sees both systems at once to conflate. No hex below is
// byte-identical to any `gradePalette` entry (spec §3 hue-delta table) — this is a
// distinct, non-lookalike green→amber→red ramp, exercised ONLY on the guide surface.
//
// The chip's VISIBLE text is now the bar's NAME (`barLabel`, e.g. "מינון"), not the
// state word — the state word moved to `aria-label` + `title` (spec §1.1/§1.3). Color
// + a redundant lucide icon still carry the state; color is never the only signal.
//
// Labels below are structural placeholders (state names), not final Content-authored
// microcopy — Content Agent + two-gate sign-off owns the shipped wording per the
// content sign-off hard rule.

import { Check, TriangleAlert, X, HelpCircle, Info } from "lucide-react";

import type { GuideBarState } from "@/lib/view-models";

export const BAR_STATE_LABELS_HE: Record<GuideBarState, string> = {
  pass: "עומד בסף",
  flag: "עם דגל",
  fail: "לא עומד",
  cannot_verify: "לא ניתן לאמת",
  // TASK-575 gate-2 HIGH-1 ruling (nutrition spec §11) — copy package Slot 11.1,
  // wired verbatim. Matches the length class of "גבוהה"/"בינונית"/"נמוכה" by design
  // (Content's own note) but must never sit ON that ladder — see tierIndexFromState.
  evidence_limited: "ראיות מוגבלות לדירוג",
};

// Shared semantic verdict palette (verdict-color spec v1 §3) — ONE object reused by
// the badge chip (this file), the tier-header pill (guide-product-table.tsx), and the
// gauge zone tints / marker fill (threshold-bar-row.tsx), so "amber = flag" reads
// identically everywhere on the page. pass/cannot_verify hex are unchanged from the
// prior (non-semantic) palette; flag/fail are NEW — amber/red, replacing indigo/berry
// — per the owner's explicit, guide-scoped exception to the "no A–E lookalike" rule
// (spec §3 "Delta from gradePalette" table: no hex here is byte-identical to any
// gradePalette entry). Measured contrast (text on own bg): pass 6.73:1, flag 5.56:1,
// fail 6.29:1, cannot_verify 6.71:1 — all clear the 4.5:1 AA floor (spec §1.2 table).
// TASK-575 gate-2 HIGH-1 ruling — `evidence_limited` reuses the EXACT SAME neutral
// bg/border/text as `cannot_verify` (nutrition spec §11: "the same non-ordinal
// treatment cannot_verify already receives" — same neutral treatment FAMILY, never a
// new color axis, per the guide's frozen "color is never the only signal" rule below).
// Icon is the ONE deliberate visual difference (Info, not HelpCircle) — colorblind-safe
// redundant shape signal distinguishing "known but unranked" from "unknown" without
// adding a color.
export const GUIDE_BAR_TONE: Record<
  GuideBarState,
  { bg: string; border: string; text: string; icon: typeof Check }
> = {
  pass: { bg: "#E2F2EF", border: "#0F6E6333", text: "#0B5D52", icon: Check },
  flag: { bg: "#FCEFD6", border: "#A8650033", text: "#8A5300", icon: TriangleAlert },
  fail: { bg: "#FBE4E1", border: "#B3261E33", text: "#A02318", icon: X },
  cannot_verify: { bg: "#F3F4F2", border: "#D8DDD9", text: "#4E5663", icon: HelpCircle },
  evidence_limited: { bg: "#F3F4F2", border: "#D8DDD9", text: "#4E5663", icon: Info },
};

export function BarStateBadge({
  state,
  barLabel,
  note,
}: {
  state: GuideBarState;
  /** The bar's name (e.g. "מינון") — now the chip's PRIMARY VISIBLE content (spec
   *  §1.1). Required: this is no longer an accessibility-only enhancement, it's what
   *  the chip shows. */
  barLabel: string;
  /** Short reason line (e.g. why a bar FLAGged, or what is missing for CANNOT_VERIFY).
   *  Folded into the accessible name and the native tooltip. */
  note?: string | null;
}) {
  const tone = GUIDE_BAR_TONE[state];
  const stateWord = BAR_STATE_LABELS_HE[state];
  const Icon = tone.icon;
  // Accessible name still leads with the bar name and states the real verdict word —
  // unchanged in spirit from before, just re-pointed now that the visible text isn't
  // the state word anymore (spec §1.3.2).
  const ariaLabel = `${barLabel}: ${stateWord}${note ? ` — ${note}` : ""}`;
  // Native tooltip now ALWAYS carries at least the plain state word (previously only
  // set when a `note` existed) — spec §1.3.3.
  const title = `${stateWord}${note ? ` — ${note}` : ""}`;

  return (
    <span
      role="img"
      aria-label={ariaLabel}
      title={title}
      data-testid="bar-state-badge"
      data-bar-state={state}
      dir="rtl"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "5px",
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 600,
        lineHeight: 1.4,
        backgroundColor: tone.bg,
        border: `1px solid ${tone.border}`,
        color: tone.text,
        whiteSpace: "nowrap",
      }}
    >
      {/* Icon = colorblind-safe redundant shape signal (spec §1.2/§1.3.1) — distinct
          per state (Check/TriangleAlert/X/HelpCircle), aria-hidden since the
          accessible name above already carries the real word. */}
      <Icon aria-hidden size={12} strokeWidth={2.25} style={{ flexShrink: 0 }} />
      {barLabel}
    </span>
  );
}
