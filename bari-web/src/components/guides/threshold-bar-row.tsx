// ThresholdBarRow — per-bar threshold infographic (TASK-504C v1, TASK-504 gauge-unify v2).
//
// Build contract:
//   03_operations/reports/design/magnesium_guide_threshold_infographic_spec_v1.md (anatomy v1)
//   03_operations/reports/design/magnesium_guide_gauge_unify_disclosure_spec_v2.md (supersedes
//     v1 §2/§3 marker geometry + retires the ladder's bordered-cell-table skin — v2 §1/§2)
// (Design Agent, D12 visual-spec approval). Guide-surface-only component (GuideProductVM,
// no score/grade) — per spec v1 §7.6, this must NEVER migrate onto the canonical /hashvaot
// A–E comparison rows, which stay frozen per the golden-page reference.
//
// ONE unified visual anatomy for all four discriminating bars (v2 §1): a horizontal
// zoned track, either value-proportional (dose/safety — real mg domain) or fixed-equal-
// thirds (form/labelTransparency — an ordinal tier, no numeric domain to be
// proportional to). Both share the same track/zone/divider/marker/tick-label rendering
// (`ThresholdTrack` below) — they differ only in how their zones/marker-position/ticks
// are computed (`buildGaugeRender` vs `buildCategoricalRender`).
//
// Every state renders, including an honest CANNOT_VERIFY fallback with NO fabricated
// marker/tier position (v1 spec §2/§3 — the owner's explicit "keep it honest" ask):
//   no marker; a hollow, mid-track placeholder ring instead, UNCHANGED by the v2 marker
//   upgrade (v2 §2.3 — a bigger "we don't know" glyph would work against its own point).
//
// WCAG: every zone boundary/tier divider is a real 1px line, independent of color
// (1.4.1); the marker always pairs with a shape difference (filled circle vs hollow
// ring) — never color alone. Marker upgraded to a 3-layer construction (v2 §2.2) so its
// edge clears WCAG 1.4.11 (~3:1 non-text contrast) against EVERY zone tint it can land
// on, not just the lightest one.

import { BAR_STATE_LABELS_HE, GUIDE_BAR_TONE } from "@/components/shared/bar-state-badge";
import { BarStateBadge } from "@/components/shared/bar-state-badge";
import type {
  GuideBarKey,
  GuideBarResult,
  GuideBarState,
  GuideGaugeGeometry,
  GuideLadderGeometry,
  GuideThresholdGeometry,
  GuideThresholdPlacement,
} from "@/lib/view-models";
import { GUIDE_BAR_LABELS_HE } from "@/lib/view-models";
import { cn } from "@/lib/utils";

/**
 * Mechanical state→tier-index mapping for the two categorical bars. The rubric defines
 * a categorical bar's state AS its tier (formAbsorption PASS ≡ the HIGH tier, FLAG ≡
 * MODERATE, FAIL ≡ LOW; labelTransparency PASS ≡ "גלוי במלואו", etc.) — this is not a
 * new fact, it is the rubric's own state definition read as a 0-based worst→best
 * index. cannot_verify → null (no tier is knowable). Exported so guide data files can
 * derive `tierIndex` from an already-computed bar state instead of hand-duplicating it.
 *
 * TASK-575 gate-2 HIGH-1 ruling (nutrition spec §11) — `evidence_limited` ALSO maps to
 * null (off-ladder), same as `cannot_verify`, but for a different reason: not because
 * the tier is unknowable, but because asserting ANY of the three tiers (including
 * "MODERATE"/flag) would itself be the over-confident ranking claim the ruling exists
 * to remove. The renderer distinguishes the two null-tier states visually/textually
 * downstream (ThresholdMarkerFallback variant) — this function only decides
 * ladder-position (both are off-ladder), never the fallback's appearance.
 */
export function tierIndexFromState(state: GuideBarState): number | null {
  switch (state) {
    case "fail":
      return 0;
    case "flag":
      return 1;
    case "pass":
      return 2;
    case "cannot_verify":
    case "evidence_limited":
    default:
      return null;
  }
}

// TASK-587: `domainMin` defaults to 0 at every call site below via `geometry.domainMin
// ?? 0`, so every existing gauge (which has no domainMin set) is byte-for-byte
// unaffected — this is a single-root-cause fix, same discipline as TASK-580: one
// helper change propagates correctly to every positioned element because they all
// already route through pct().
function pct(value: number, domainMin: number, domainMax: number): number {
  const clamped = Math.max(domainMin, Math.min(value, domainMax));
  return ((clamped - domainMin) / (domainMax - domainMin)) * 100;
}

// Bidi fix (TASK-504 design vision-critic, MEDIUM): a `valueLabel` that leads with a
// currency token — "~$0.27 ל-3 גרם", "₪0.52 ל-3 גרם" — mixes an LTR numeric run into
// the surrounding RTL caption. A leading "~" has no strong bidi direction, so the
// browser's bidi algorithm can attach it to either side of the adjacent LTR run and
// paint it after the price ("$0.27~") instead of before it. Isolating the currency
// token in a `<bdi dir="ltr">` fences it off from the surrounding RTL context so its
// own logical order (tilde, symbol, digits) is always what paints — for every
// currency (₪ and $ both matched), not just the one that happens to use "~" today.
const CURRENCY_TOKEN_RE = /^~?[$₪][\d.,–-]+/;

function splitCurrencyToken(label: string): { token: string; rest: string } | null {
  const match = label.match(CURRENCY_TOKEN_RE);
  if (!match) return null;
  return { token: match[0], rest: label.slice(match[0].length) };
}

// ─── Shared render-descriptor shape consumed by <ThresholdTrack> ───────────────────
interface TrackZone {
  startPct: number;
  endPct: number;
  tone: GuideBarState;
}
interface TrackBoundary {
  pct: number;
  style: "solid" | "dashed";
}
interface TrackTick {
  pct: number;
  label: string;
  /** TASK-575 — "end" anchors flush to the track's right edge (mirrors "start"'s
   *  flush-left), fixing a real clipping bug where a pct:100 "center" tick (e.g. the
   *  domain-max label) rendered half outside the row's clipping ancestor — the exact
   *  same trap the marker already solves via its own clamp/anchor logic, caught here
   *  in this task's own screenshot verification pass. */
  anchor: "start" | "center" | "end";
}
interface TrackContextBand {
  startPct: number;
  endPct: number;
  label: string;
  qualifierLabel: string;
}
interface TrackReferenceLine {
  pct: number;
  /** e.g. "190 מ״ג — חציון בין 15 מוצרים עם מינון ברור" — rendered on its OWN line
   *  below the track, never inline in the short numeric tick row (see geometry
   *  header comment: a real collision was caught in this task's visual QA pass). */
  caption: string;
}

interface TrackRender {
  zones: TrackZone[];
  boundaries: TrackBoundary[];
  ticks: TrackTick[];
  markerPct: number | null;
  clamped: boolean;
  /** Categorical tick labels (tier names) can be longer than numeric ticks and need
   *  room to wrap within their own zone column rather than overlapping a neighbor
   *  (v2 spec §5.2 flagged risk) — numeric gauge ticks stay single-line as before. */
  multilineTicks: boolean;
  /** TASK-575 — an un-toned overlay band (e.g. the RDA all-sources context range),
   *  distinct from the zone-tone system. Absent for every gauge except a geometry
   *  that explicitly supplies `contextBand`. */
  contextBand?: TrackContextBand;
  /** TASK-575 — thin dashed reference lines (e.g. corpus median), each with its own
   *  below-track caption (see TrackReferenceLine). */
  referenceLines: TrackReferenceLine[];
}

function buildGaugeRender(
  geometry: GuideGaugeGeometry,
  placement: GuideThresholdPlacement | undefined
): TrackRender {
  const value = placement?.value ?? null;
  const domainMin = geometry.domainMin ?? 0;
  const zones: TrackZone[] = geometry.zones.map((zone, i) => ({
    startPct: i === 0 ? 0 : pct(geometry.zones[i - 1].upTo, domainMin, geometry.domainMax),
    endPct: pct(zone.upTo, domainMin, geometry.domainMax),
    tone: zone.tone,
  }));
  const boundaries: TrackBoundary[] = geometry.zones
    .slice(0, -1)
    .map((zone) => ({ pct: pct(zone.upTo, domainMin, geometry.domainMax), style: zone.dividerStyle }));
  const ticks: TrackTick[] = [
    // TASK-587 — the domain-minimum tick. Always rendered now (the old
    // `hideZeroTick` suppression flag is retired): once `domainMin` genuinely moves
    // the domain floor, pct(domainMin, domainMin, domainMax) === 0 by construction, so
    // this tick always sits flush at the track's start edge — for the unchanged safety
    // gauge (domainMin defaults to 0) this renders the exact same "0" tick as before.
    { pct: 0, label: geometry.minTickLabel ?? String(domainMin), anchor: "start" as const },
    ...geometry.zones
      .slice(0, -1)
      .filter((z) => z.tickLabel)
      .map((z) => ({ pct: pct(z.upTo, domainMin, geometry.domainMax), label: z.tickLabel as string, anchor: "center" as const })),
    // TASK-575 — a short domain-max label (e.g. "520"), symmetric with the zone
    // tickLabels above but for the edge that has no natural zone boundary to attach
    // to (the last zone's upper edge IS the domain max). anchor "end" (not "center")
    // — a pct:100 center-anchored tick renders half outside the clipping ancestor.
    ...(geometry.maxTickLabel ? [{ pct: 100, label: geometry.maxTickLabel, anchor: "end" as const }] : []),
  ];
  const contextBand: TrackContextBand | undefined = geometry.contextBand
    ? {
        startPct: pct(geometry.contextBand.from, domainMin, geometry.domainMax),
        endPct: pct(geometry.contextBand.to, domainMin, geometry.domainMax),
        label: geometry.contextBand.label,
        qualifierLabel: geometry.contextBand.qualifierLabel,
      }
    : undefined;
  // TASK-575 — reference lines (e.g. corpus median) render as a thin dashed vertical
  // line ON the track, with their full label as a separate below-track caption (never
  // inline in the numeric tick row — that caused a real overlap with the "76" boundary
  // tick, caught in this task's own visual verification pass).
  const referenceLines: TrackReferenceLine[] = (geometry.referenceTicks ?? []).map((rt) => ({
    pct: pct(rt.at, domainMin, geometry.domainMax),
    caption: `${rt.at} מ"ג — ${rt.label}`,
  }));
  return {
    zones,
    boundaries,
    ticks,
    // Clamp to the track so an over-max value pins the marker at the right edge
    // (fully visible, with the "+" overflow glyph) instead of computing >100% and
    // flying off the edge where an ancestor clips it (owner-caught glitch 2026-07-05).
    markerPct: value != null ? Math.min(pct(value, domainMin, geometry.domainMax), 100) : null,
    clamped: !!placement?.clamped,
    multilineTicks: false,
    contextBand,
    referenceLines,
  };
}

function buildCategoricalRender(
  geometry: GuideLadderGeometry,
  placement: GuideThresholdPlacement | undefined
): TrackRender {
  const n = geometry.tiers.length;
  const zoneWidth = 100 / n;
  const zones: TrackZone[] = geometry.tiers.map((tier, i) => ({
    startPct: i * zoneWidth,
    endPct: (i + 1) * zoneWidth,
    tone: tier.tone,
  }));
  // Categorical tier boundaries are all equally hard (a product is never "half in the
  // moderate tier") — every boundary is solid, unlike the gauge's dashed-EFSA case
  // (v2 spec §1.2).
  const boundaries: TrackBoundary[] = geometry.tiers
    .slice(0, -1)
    .map((_, i) => ({ pct: (i + 1) * zoneWidth, style: "solid" as const }));
  const ticks: TrackTick[] = geometry.tiers.map((tier, i) => ({
    pct: (i + 0.5) * zoneWidth,
    label: tier.label,
    anchor: "center" as const,
  }));
  const tierIndex = placement?.tierIndex ?? null;
  return {
    zones,
    boundaries,
    ticks,
    markerPct: tierIndex != null ? (tierIndex + 0.5) * zoneWidth : null,
    clamped: false,
    multilineTicks: true,
    referenceLines: [],
  };
}

// ─── Marker (v2 §2.2 — 3-layer construction: 12px core + 3px white halo + 1.5px
// #4E5663 definition ring ≈ 21px total footprint, guarantees a real edge against
// every zone tint the marker can land on). ──────────────────────────────────────────
function ThresholdMarker({
  pct: markerPct,
  state,
  clamped,
}: {
  pct: number;
  state: GuideBarState;
  clamped?: boolean;
}) {
  const tone = GUIDE_BAR_TONE[state];
  // Anchor position (v2 gauge-unify fix #2, 2026-07-05 owner-caught glitch): the
  // ancestor that clips collapsed/expanded row content (`.bari-cmp-expclip`) is
  // sized to exactly the track's own box, so anything the marker paints past that
  // box's left/right edge -- the 3-layer halo (visual radius ~10.5px from center)
  // and the "+" overflow glyph that trails a clamped marker -- gets hard-clipped by
  // the ancestor, not just visually tight (confirmed via vision-in: clipChain rect
  // == trackRect exactly). The earlier `markerPct` clamp-to-100 fix was necessary
  // (stopped the marker computing past 100% and flying off-screen) but not
  // sufficient -- AT 100% the halo + "+" still straddle the box edge and get cut.
  // Two cases:
  //  - clamped (always pct === 100 -- an over-max value): anchor the marker 24px
  //    in from the LEFT edge (TASK-580 RTL-axis fix: max is now the track's left
  //    end, mirroring the pre-fix "24px in from the right") so there is room,
  //    INSIDE the track's own box, for both the full halo and the trailing "+"
  //    glyph (same 13px gap as before, now trailing further LEFT of the marker --
  //    "further past the max" is a leftward direction now, not rightward).
  //  - otherwise: a light clamp(11px, mirroredPct%, 100%-11px) keeps the halo alone
  //    on-box for the rare legitimate value that lands exactly on 0%/100% without
  //    being flagged over-max. Invisible for every normal mid-track value -- it only
  //    engages within ~11px of either edge, which does not move a real tick/zone
  //    reading in practice.
  //
  // TASK-580 RTL-axis fix: `left: L, transform: translate(-50%, -50%)` renders its
  // CENTER at physical L regardless of dir (verified by hand: the -50% pullback is
  // always half of the marker's OWN 12px width, independent of which edge L is
  // measured from) -- so the fix mirrors the VALUE passed as `left`, not the CSS
  // property or the transform. `markerPct` itself (the domain-relative percent,
  // computed upstream in buildGaugeRender/buildCategoricalRender) is untouched;
  // only the render-time expression flips it to "distance from the track's own
  // left edge" via `100 - markerPct`.
  const CLAMPED_MARKER_INSET_PX = 24;
  const CLAMPED_GLYPH_GAP_PX = 13;
  const leftExpr = clamped
    ? `${CLAMPED_MARKER_INSET_PX}px`
    : `clamp(11px, calc(100% - ${markerPct}%), calc(100% - 11px))`;
  return (
    <>
      <div
        aria-hidden
        className="absolute top-1/2 rounded-full"
        style={{
          left: leftExpr,
          width: "12px",
          height: "12px",
          transform: "translate(-50%, -50%)",
          background: tone.text,
          boxShadow: "0 0 0 3px #FFFFFF, 0 0 0 4.5px #4E5663",
        }}
      />
      {clamped ? (
        <span
          aria-hidden
          className="absolute top-1/2 text-[10px] font-bold"
          style={{
            // The "+" has no centering transform (it flows naturally from its own
            // anchor), so mirroring its `left` value the same way as the marker
            // would make it grow RIGHTWARD from a point near the marker -- wrong
            // direction now that "further past the max" is leftward. Anchoring via
            // `right` instead lets it grow LEFTWARD from that same point: its right
            // edge sits at (marker inset - gap) px from the track's own left edge,
            // i.e. 13px further left than the marker's 24px inset.
            right: `calc(100% - ${CLAMPED_MARKER_INSET_PX - CLAMPED_GLYPH_GAP_PX}px)`,
            transform: "translateY(-50%)",
            color: tone.text,
          }}
        >
          +
        </span>
      ) : null}
    </>
  );
}

// Honest CANNOT_VERIFY fallback — UNCHANGED by the v2 marker upgrade (v2 §2.3: a
// bigger "we don't know" glyph would work against its own purpose of reading as
// visually quieter than a real data point). Hollow, dashed, fixed mid-track.
//
// TASK-575 gate-2 HIGH-1 ruling (nutrition spec §11) adds a SECOND, visually distinct
// off-ladder fallback for `evidence_limited`: a SOLID neutral-gray disc (not hollow,
// not dashed) at the same mid-track position and footprint. The shape distinction is
// deliberate and carries real meaning, same "shape, not just color" discipline as the
// rest of this component (WCAG 1.4.1): hollow/dashed = "we don't know this fact at
// all" (cannot_verify); solid/filled = "we know this fact, we are just not confident
// enough in the literature to rank it" (evidence_limited) — the fact is not missing,
// so the marker must not LOOK like it is missing (spec §11: "must not read as missing
// data"). Neither variant sits at a ladder tier position — both are fixed mid-track.
function ThresholdMarkerFallback({ variant = "unknown" }: { variant?: "unknown" | "evidence_limited" }) {
  // TASK-580 RTL-axis fix: deliberately UNCHANGED. `left: L, transform: translate(-50%,
  // -50%)` renders its center at physical L (see ThresholdMarker's comment); mirroring
  // this component's convention would give `left: 100 - 50 = 50`, i.e. the identical
  // value -- so there is nothing to edit here. Confirmed explicitly (not inferred from
  // the tick fix, per the spec's own warning that this is the one state where a
  // regression is easy to miss) via the acceptance checklist's assertion #10 and the
  // TRIOMAG / evidence_limited-form screenshots.
  const shared = {
    left: "50%",
    // Same footprint as the solid ThresholdMarker (~18px visible) so all three marker
    // states read as the SAME SIZE on the track — the honest signal is carried by
    // shape (dashed/hollow vs. solid vs. filled-circle), not by being smaller/bigger.
    width: "18px",
    height: "18px",
    transform: "translate(-50%, -50%)",
  } as const;

  if (variant === "evidence_limited") {
    return (
      <div
        aria-hidden
        className="absolute top-1/2 rounded-full"
        style={{
          ...shared,
          border: "1.5px solid #4E5663",
          background: "#C7CBC7",
        }}
      />
    );
  }

  return (
    <div
      aria-hidden
      className="absolute top-1/2 rounded-full"
      style={{
        ...shared,
        border: "1.5px dashed #4E5663",
        background: "transparent",
      }}
    />
  );
}

function ThresholdTrack({ render, state }: { render: TrackRender; state: GuideBarState }) {
  return (
    // TASK-580 RTL-axis fix (mag_guide_gauge_rtl_spec.md): this wrapper used to force
    // dir="ltr", which — combined with every child using the PHYSICAL `left` property —
    // put the domain minimum/worst tier at the track's physical LEFT and the
    // maximum/best tier at the physical RIGHT, backwards for a reading-right-to-left
    // page (Design ruling: RTL-ascending axis for all 4 bar types, matching the
    // upf-confidence-ladder precedent — no LTR exception for this component family).
    // Dropping the override (inheriting dir="rtl" from ThresholdBarRow below) does
    // NOT by itself fix anything, since every position below is still a physical
    // `left`/`right`/`px` value, never a logical inset-inline-*/margin-inline-*
    // property — see the chosen approach note at the top of ThresholdMarker. Every
    // position value below has been re-derived (not just relabeled) so that `left: L`
    // + the SAME unchanged `transform: translateX(-50%)` centering trick still holds:
    // for that trick, final rendered center == L regardless of dir, so mirroring the
    // VALUE (L → the position matching "L% from the track's RIGHT edge") is both
    // correct and lower-risk than switching the anchor property to `right` (which
    // would require also flipping every centering transform's sign — verified by hand
    // and rejected as more error-prone for an equivalent result).
    <div className="w-full md:w-[260px] md:shrink-0">
      {/* Container bumped 18px -> 24px (v2 §2.2) for the larger marker's vertical
          clearance; track itself stays 6px, vertically centered. data-testid added
          TASK-587 for acceptance-checklist geometry verification only (QA hook, no
          visual/behavioral change) — the track fill below is inset-x-0 within this
          wrapper, so this box's own bounding rect IS the track's x-axis bounding rect. */}
      <div className="relative" style={{ height: "24px" }} data-testid="threshold-track">
        <div
          className="absolute inset-x-0 top-1/2 overflow-hidden rounded-full"
          style={{ height: "6px", transform: "translateY(-50%)", background: "#EDEFEC" }}
        >
          {render.zones.map((zone, i) => (
            <div
              key={i}
              className="absolute top-0 h-full"
              style={{
                // RTL-axis mirror (TASK-580): the span [startPct, endPct] measured from
                // the domain minimum now renders physically starting at (100 - endPct)%
                // from the track's own left edge — i.e. the same span, flush to the
                // track's RIGHT edge at pct 0 instead of its left edge. Width unchanged.
                left: `${100 - zone.endPct}%`,
                width: `${zone.endPct - zone.startPct}%`,
                background: GUIDE_BAR_TONE[zone.tone].bg,
              }}
            />
          ))}
        </div>

        {/* TASK-587 — RDA context-band, redone as an ON-TRACK shaded+bordered zone
            (spec §2), replacing the old floating 3-sided dashed outline that painted
            below the track with no fill and an open bottom edge (the "hovering
            rectangle" glitch the owner flagged). Shares the track's own vertical
            center (top: 50%, translateY(-50%)) and is only marginally taller than it
            (8px vs. the track's 6px) so it visibly "hugs" the pill from both sides
            rather than exactly overlapping it 1:1. Painted here — right after the
            zones' color-fill layer, BEFORE boundaries/marker/referenceLines — so a
            marker landing inside 310–420 still paints visibly on top of the band,
            matching how the marker already paints on top of ordinary zone-tone fills
            everywhere else on the track (spec §2.2 paint-order fix). Token: #6B7070,
            already this file's own zone-boundary/reference-line color (line ~446/474
            below), at two strengths — 16% alpha fill (a quiet tint, never the sole
            WCAG signal) + full-opacity 1.5px dashed border (the element that actually
            carries the ≥3:1 non-text contrast floor, spec §2.3). Dashed, not solid —
            this component's own established vocabulary for "advisory/context, not a
            hard boundary" (spec §2.3). */}
        {render.contextBand ? (
          <div
            aria-hidden
            className="absolute rounded-full"
            data-testid="threshold-context-band"
            style={{
              top: "50%",
              // RTL-axis mirror (TASK-580 convention, unchanged) — same span-mirroring
              // as the zones above: [startPct, endPct] renders flush from
              // (100 - endPct)%, same width.
              left: `${100 - render.contextBand.endPct}%`,
              width: `${render.contextBand.endPct - render.contextBand.startPct}%`,
              height: "8px",
              transform: "translateY(-50%)",
              background: "rgba(107, 112, 112, 0.16)",
              border: "1.5px dashed #6B7070",
            }}
          />
        ) : null}

        {/* Mandatory zone-boundary divider lines — never color-only (spec v1 §2/§7.1). */}
        {render.boundaries.map((b, i) => (
          <div
            key={i}
            aria-hidden
            className="absolute top-1/2"
            style={{
              // RTL-axis mirror (TASK-580): `left: L, transform: translateX(-50%)`
              // always renders its center at physical L regardless of dir (the
              // transform is unchanged on purpose — width:0 here anyway, so its X
              // component is a no-op) — so mirroring the VALUE to (100 - b.pct) is
              // the whole fix. b.pct itself (the domain-relative percent) is untouched.
              left: `${100 - b.pct}%`,
              height: "10px",
              width: 0,
              transform: "translate(-50%, -50%)",
              borderInlineStart: `1px ${b.style} #6B7070`,
            }}
          />
        ))}

        {render.markerPct != null ? (
          <ThresholdMarker pct={render.markerPct} state={state} clamped={render.clamped} />
        ) : (
          <ThresholdMarkerFallback variant={state === "evidence_limited" ? "evidence_limited" : "unknown"} />
        )}

        {/* TASK-575 — reference lines (e.g. corpus median): a thin dashed vertical line
            ON the track, tone-free, distinct from the marker (filled circle) and from
            zone boundaries (which carry a real zone/tone change). Its full label is a
            below-track caption, not rendered here. */}
        {render.referenceLines.map((rl, i) => (
          <div
            key={i}
            aria-hidden
            data-testid="threshold-reference-line"
            className="absolute top-1/2"
            style={{
              // RTL-axis mirror (TASK-580) — same "mirror the value, keep left +
              // transform unchanged" convention as the zone boundaries above.
              left: `${100 - rl.pct}%`,
              height: "16px",
              width: 0,
              transform: "translate(-50%, -50%)",
              borderInlineStart: "1.5px dashed #6B7070",
            }}
          />
        ))}
      </div>

      {/* Tick labels — only meaningful anchors for a gauge (spec v1 §2), every tier
          name for a categorical bar (spec v2 §1.2).
          Bug fix (TASK-504 design vision-critic, HIGH): the categorical/ladder ticks
          are evenly spaced (each owns an equal-width column), so they no longer need
          absolute positioning — a plain flex row lets the container's height grow to
          fit a wrapped 2-line tick label instead of a fixed `min-h` guess. That fixed
          guess previously under-reported the container's real height, so the caption
          `<p>` below (normal-flow sibling on mobile) started painting on top of the
          label's second line whenever a tick label wrapped (e.g. the third-party
          ladder's "מוצהר, טרם אומת מול מאגר" tier). The numeric gauge ticks (dose/
          price/safety) keep absolute positioning unchanged — their anchors are
          arbitrary threshold pct positions, not equal-width columns, and they never
          wrap (single line), so they were never part of this bug. */}
      {render.multilineTicks ? (
        // TASK-580 RTL-axis fix: deliberately UNCHANGED. This row is plain flex flow
        // (source order), not absolute-positioned like the numeric-gauge ticks above —
        // a `flex` row is direction-aware natively, so now that the dir="ltr" override
        // is dropped, this row auto-reverses under the inherited dir="rtl": DOM index 0
        // (worst tier, e.g. "נמוכה") already renders at the main-start edge, which is
        // physically the RIGHT in RTL, matching the mirrored zone coloring below without
        // any code change here. Verified against the zones' new physical span (worst
        // zone now renders in the track's rightmost third) so label and color agree.
        <div className="mt-0.5 flex w-full text-[11px]" style={{ color: "#6B7070" }}>
          {render.ticks.map((t, i) => (
            <span
              key={i}
              className="text-center leading-tight"
              style={{ width: `${100 / render.ticks.length}%` }}
            >
              {t.label}
            </span>
          ))}
        </div>
      ) : (
        <div className="relative mt-0.5 h-3 text-[11px]" style={{ color: "#6B7070" }}>
          {render.ticks.map((t, i) =>
            // RTL-axis mirror (TASK-580): the two flush anchors swap which physical
            // edge they hug — "start" (domain minimum, e.g. "76"/"0") now flushes to
            // the track's RIGHT edge (reading-start); "end" (domain maximum, e.g.
            // "520") now flushes LEFT. This is the exact inverse of the TASK-575 fix
            // that flush-anchored the max label to stop it clipping the row's
            // clipping ancestor — same guarantee, opposite side.
            t.anchor === "start" ? (
              <span key={i} className="absolute whitespace-nowrap" style={{ right: 0 }}>
                {t.label}
              </span>
            ) : t.anchor === "end" ? (
              <span key={i} className="absolute whitespace-nowrap" style={{ left: 0 }}>
                {t.label}
              </span>
            ) : (
              <span
                key={i}
                className="absolute whitespace-nowrap text-center leading-tight"
                // Center-anchored: same "mirror the value, keep left + transform
                // unchanged" convention as the zone boundaries — translateX(-50%) is
                // untouched on purpose (see ThresholdTrack's own comment above).
                style={{ left: `${100 - t.pct}%`, transform: "translateX(-50%)" }}
              >
                {t.label}
              </span>
            )
          )}
        </div>
      )}

      {/* TASK-575 — reference-line captions (e.g. corpus median), each its own line —
          deliberately NOT inline in the numeric tick row above (a real overlap with
          the "76" boundary tick was caught in this task's own screenshot verification
          pass; see the geometry header comment). */}
      {render.referenceLines.length > 0 ? (
        <div className="mt-1 space-y-0.5" dir="rtl" data-testid="threshold-reference-line-caption">
          {render.referenceLines.map((rl, i) => (
            <p key={i} className="text-[11px] leading-[1.4]" style={{ color: "#6B7070" }}>
              {rl.caption}
            </p>
          ))}
        </div>
      ) : null}

      {/* TASK-575 — context-band label + mandatory qualifier (spec §3: the qualifier
          must render wherever the band renders, never as a bare number). Rendered as
          its own line so it never overlaps a positioned tick label. */}
      {render.contextBand ? (
        <p
          className="mt-1 text-[11px] leading-[1.4]"
          dir="rtl"
          style={{ color: "#6B7070" }}
          data-testid="threshold-context-band-label"
        >
          {render.contextBand.label} · {render.contextBand.qualifierLabel}
        </p>
      ) : null}
    </div>
  );
}

export function ThresholdBarRow({
  barKey,
  result,
  geometry,
  placement,
  isFirst,
}: {
  barKey: GuideBarKey;
  result: GuideBarResult;
  /** Static, shared-across-products geometry for this bar. Absent → plain badge row
   *  (no infographic anatomy defined for this bar yet — spec v1 §1). */
  geometry?: GuideThresholdGeometry;
  placement?: GuideThresholdPlacement;
  isFirst?: boolean;
}) {
  const barLabel = GUIDE_BAR_LABELS_HE[barKey];

  // Caption: "המוצר: {value}" + the bar's own existing `note`, if any — the note is
  // Content's field, rendered verbatim, never invented here (spec v1 §2 caption rule).
  const valueLabel = placement?.valueLabel ?? BAR_STATE_LABELS_HE[result.state];
  const currencySplit = splitCurrencyToken(valueLabel);
  const captionNode = (
    <>
      {"המוצר: "}
      {currencySplit ? (
        <>
          <bdi dir="ltr">{currencySplit.token}</bdi>
          {currencySplit.rest}
        </>
      ) : (
        valueLabel
      )}
      {result.note ? ` · ${result.note}` : null}
    </>
  );
  const showCaption = !!placement;

  const render =
    geometry?.anatomy === "gauge"
      ? buildGaugeRender(geometry, placement)
      : geometry?.anatomy === "ladder"
        ? buildCategoricalRender(geometry, placement)
        : null;

  return (
    <div
      className={cn("pt-2.5", !isFirst && "mt-2.5 border-t border-black/[0.05]")}
      dir="rtl"
      data-testid="threshold-bar-row"
      data-bar-key={barKey}
    >
      {/* Verdict-color spec v1 §1.1: the chip itself now shows the bar name in color
          (BarStateBadge), so the separate plain-text name span is redundant and
          removed — one flex child, anchored to the line's start (RTL: visually the
          right edge), not `justify-between` (spec §5 risk #2). */}
      <div className="flex items-center justify-start">
        <BarStateBadge state={result.state} barLabel={barLabel} note={result.note} />
      </div>

      {render ? (
        // Spec v2 §4/desktop cap carried over from spec v1's H2 fix — now applies
        // identically to all 4 bars since form/labelTransparency share the same
        // unified anatomy as dose/safety (was gauge-only before this unification).
        <div className="mt-1.5 md:flex md:items-center md:gap-3">
          <ThresholdTrack render={render} state={result.state} />
          {showCaption ? (
            <p className="mt-1 text-[11px] leading-[1.4] md:mt-0 md:flex-1" style={{ color: "#4E5663" }}>
              {captionNode}
            </p>
          ) : null}
        </div>
      ) : showCaption ? (
        <p className="mt-1 text-[11px] leading-[1.4]" style={{ color: "#4E5663" }}>
          {captionNode}
        </p>
      ) : null}
    </div>
  );
}
