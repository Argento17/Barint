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
    default:
      return null;
  }
}

function pct(value: number, domainMax: number): number {
  const clamped = Math.max(0, Math.min(value, domainMax));
  return (clamped / domainMax) * 100;
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
  const zones: TrackZone[] = geometry.zones.map((zone, i) => ({
    startPct: i === 0 ? 0 : pct(geometry.zones[i - 1].upTo, geometry.domainMax),
    endPct: pct(zone.upTo, geometry.domainMax),
    tone: zone.tone,
  }));
  const boundaries: TrackBoundary[] = geometry.zones
    .slice(0, -1)
    .map((zone) => ({ pct: pct(zone.upTo, geometry.domainMax), style: zone.dividerStyle }));
  const ticks: TrackTick[] = [
    // TASK-575 — `hideZeroTick` drops this generic "0" anchor for a gauge whose
    // domain does not meaningfully start at zero (e.g. a corpus-range gauge where the
    // reviewed minimum is the honest left anchor, not zero). Every other gauge
    // (including the unchanged safety gauge) keeps this tick exactly as before.
    ...(geometry.hideZeroTick ? [] : [{ pct: 0, label: "0", anchor: "start" as const }]),
    ...geometry.zones
      .slice(0, -1)
      .filter((z) => z.tickLabel)
      .map((z) => ({ pct: pct(z.upTo, geometry.domainMax), label: z.tickLabel as string, anchor: "center" as const })),
    // TASK-575 — a short domain-max label (e.g. "520"), symmetric with the zone
    // tickLabels above but for the edge that has no natural zone boundary to attach
    // to (the last zone's upper edge IS the domain max). anchor "end" (not "center")
    // — a pct:100 center-anchored tick renders half outside the clipping ancestor.
    ...(geometry.maxTickLabel ? [{ pct: 100, label: geometry.maxTickLabel, anchor: "end" as const }] : []),
  ];
  const contextBand: TrackContextBand | undefined = geometry.contextBand
    ? {
        startPct: pct(geometry.contextBand.from, geometry.domainMax),
        endPct: pct(geometry.contextBand.to, geometry.domainMax),
        label: geometry.contextBand.label,
        qualifierLabel: geometry.contextBand.qualifierLabel,
      }
    : undefined;
  // TASK-575 — reference lines (e.g. corpus median) render as a thin dashed vertical
  // line ON the track, with their full label as a separate below-track caption (never
  // inline in the numeric tick row — that caused a real overlap with the "76" boundary
  // tick, caught in this task's own visual verification pass).
  const referenceLines: TrackReferenceLine[] = (geometry.referenceTicks ?? []).map((rt) => ({
    pct: pct(rt.at, geometry.domainMax),
    caption: `${rt.at} מ"ג — ${rt.label}`,
  }));
  return {
    zones,
    boundaries,
    ticks,
    // Clamp to the track so an over-max value pins the marker at the right edge
    // (fully visible, with the "+" overflow glyph) instead of computing >100% and
    // flying off the edge where an ancestor clips it (owner-caught glitch 2026-07-05).
    markerPct: value != null ? Math.min(pct(value, geometry.domainMax), 100) : null,
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
  //    in from the right so there is room, INSIDE the track's own box, for both
  //    the full halo and the trailing "+" glyph (same 13px gap as before, just the
  //    anchor point shifted left).
  //  - otherwise: a light clamp(11px, pct%, 100%-11px) keeps the halo alone
  //    on-box for the rare legitimate value that lands exactly on 0%/100% without
  //    being flagged over-max. Invisible for every normal mid-track value -- it only
  //    engages within ~11px of either edge, which does not move a real tick/zone
  //    reading in practice.
  const leftExpr = clamped ? "calc(100% - 24px)" : `clamp(11px, ${markerPct}%, calc(100% - 11px))`;
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
            left: leftExpr,
            marginInlineStart: "13px",
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
function ThresholdMarkerFallback() {
  return (
    <div
      aria-hidden
      className="absolute top-1/2 rounded-full"
      style={{
        // Same footprint as the solid ThresholdMarker (~18px visible) so the two
        // read as the SAME SIZE on the track — the honest "we don't know" signal is
        // carried by the dashed/hollow shape, not by being smaller (owner 2026-07-05).
        left: "50%",
        width: "18px",
        height: "18px",
        transform: "translate(-50%, -50%)",
        border: "1.5px dashed #4E5663",
        background: "transparent",
      }}
    />
  );
}

function ThresholdTrack({ render, state }: { render: TrackRender; state: GuideBarState }) {
  return (
    <div className="w-full md:w-[260px] md:shrink-0" dir="ltr">
      {/* Container bumped 18px -> 24px (v2 §2.2) for the larger marker's vertical
          clearance; track itself stays 6px, vertically centered. */}
      <div className="relative" style={{ height: "24px" }}>
        <div
          className="absolute inset-x-0 top-1/2 overflow-hidden rounded-full"
          style={{ height: "6px", transform: "translateY(-50%)", background: "#EDEFEC" }}
        >
          {render.zones.map((zone, i) => (
            <div
              key={i}
              className="absolute top-0 h-full"
              style={{
                left: `${zone.startPct}%`,
                width: `${zone.endPct - zone.startPct}%`,
                background: GUIDE_BAR_TONE[zone.tone].bg,
              }}
            />
          ))}
        </div>

        {/* Mandatory zone-boundary divider lines — never color-only (spec v1 §2/§7.1). */}
        {render.boundaries.map((b, i) => (
          <div
            key={i}
            aria-hidden
            className="absolute top-1/2"
            style={{
              left: `${b.pct}%`,
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
          <ThresholdMarkerFallback />
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
              left: `${rl.pct}%`,
              height: "16px",
              width: 0,
              transform: "translate(-50%, -50%)",
              borderInlineStart: "1.5px dashed #6B7070",
            }}
          />
        ))}

        {/* TASK-575 — context-band bracket (e.g. the RDA all-sources range). Deliberately
            NOT a zone tint (spec §3: never reuse the pass/fail tone system for this) —
            a plain dashed outline, drawn under the track, distinct from both the colored
            zone fill above and the solid/dashed zone-boundary dividers. */}
        {render.contextBand ? (
          <div
            aria-hidden
            className="absolute"
            style={{
              top: "17px",
              left: `${render.contextBand.startPct}%`,
              width: `${render.contextBand.endPct - render.contextBand.startPct}%`,
              height: "6px",
              borderTop: "1.5px dashed #8A8F86",
              borderInlineStart: "1.5px dashed #8A8F86",
              borderInlineEnd: "1.5px dashed #8A8F86",
            }}
          />
        ) : null}
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
            t.anchor === "start" ? (
              <span key={i} className="absolute whitespace-nowrap" style={{ left: 0 }}>
                {t.label}
              </span>
            ) : t.anchor === "end" ? (
              <span key={i} className="absolute whitespace-nowrap" style={{ right: 0 }}>
                {t.label}
              </span>
            ) : (
              <span
                key={i}
                className="absolute whitespace-nowrap text-center leading-tight"
                style={{ left: `${t.pct}%`, transform: "translateX(-50%)" }}
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
