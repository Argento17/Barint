"use client";

/**
 * Donut chart primitives for the inventory dashboard.
 *
 * Generic engine: DonutChart accepts segments [{ id, label, count, color }] and
 * renders the SVG arc + legend. Single-segment = full ring (no gap seam). 27px centre total.
 *
 * GradeDonut: consumes gradeDistribution from InventorySummaryVM → segments in
 * fixed order A/B/C/D/E (+ unscored if >0). Colors from BARI_COMPARISON_TOKENS.gradePalette.
 * Card title should be "פילוח לפי ציון".
 *
 * RetailerDonut: legacy export kept for API compat — re-wraps DonutChart with retailer data.
 *
 * SVG spec (from Bari Dashboard.dc.html):
 *   viewBox 160×160, cx=cy=80, r=60, strokeWidth=20, rotate(-90).
 *   Track ring: #EEEEE9.
 *   Centre total: 27px extrabold, --fg1.
 *   Centre sub-label "מוצרים": 11px, --fg3.
 *   Gap between segments: 2°, except single-segment = full ring.
 *
 * NO imports from scoring/bsip/registry/comparisons modules.
 */

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade, BariRetailerRefVM, InventorySummaryVM } from "@/lib/view-models";

const CIRCUMFERENCE = 2 * Math.PI * 60; // 376.991...

// ── Generic segment type ───────────────────────────────────────────────────────

export interface DonutSegmentDef {
  id: string;
  label: string;
  count: number;
  color: string;
}

// ── Grade palette for donut ────────────────────────────────────────────────────

const GRADE_DONUT_COLORS: Record<BariGrade | "unscored", string> = {
  A: BARI_COMPARISON_TOKENS.gradePalette.A.accent,  // #1E7A4F
  B: BARI_COMPARISON_TOKENS.gradePalette.B.accent,  // #546E14
  C: BARI_COMPARISON_TOKENS.gradePalette.C.accent,  // #8A6300
  D: BARI_COMPARISON_TOKENS.gradePalette.D.accent,  // #B04510
  E: BARI_COMPARISON_TOKENS.gradePalette.E.accent,  // #A52121
  unscored: "#D6D8D1",
};

const GRADE_ORDER: Array<BariGrade | "unscored"> = ["A", "B", "C", "D", "E", "unscored"];

// ── SVG arc computation ────────────────────────────────────────────────────────

interface ComputedSegment extends DonutSegmentDef {
  dashArray: string;
  dashOffset: number;
}

function computeSegments(defs: DonutSegmentDef[], total: number): ComputedSegment[] {
  const isSingle = defs.length === 1;
  const gapDeg = isSingle ? 0 : 2;
  const gapFrac = gapDeg / 360;

  const out: ComputedSegment[] = [];
  let offsetAccum = 0;

  for (const def of defs) {
    const ratio = total > 0 ? def.count / total : 0;
    const segLen = isSingle ? CIRCUMFERENCE : Math.max(0, (ratio - gapFrac) * CIRCUMFERENCE);
    out.push({
      ...def,
      dashArray: `${segLen} ${CIRCUMFERENCE}`,
      dashOffset: -offsetAccum,
    });
    offsetAccum += ratio * CIRCUMFERENCE;
  }
  return out;
}

// ── Generic DonutChart ────────────────────────────────────────────────────────

interface DonutChartProps {
  segments: DonutSegmentDef[];
  /** Total shown in the donut centre. If not provided, sums segments. */
  centerTotal?: number;
  centerSublabel?: string;
  ariaLabel?: string;
}

export function DonutChart({
  segments,
  centerTotal,
  centerSublabel = "מוצרים",
  ariaLabel,
}: DonutChartProps) {
  const total = centerTotal ?? segments.reduce((s, x) => s + x.count, 0);

  if (total === 0 || segments.length === 0) {
    return (
      <div
        className="flex h-48 items-center justify-center text-sm"
        style={{ color: "var(--fg3, #5E6560)" }}
      >
        אין נתונים
      </div>
    );
  }

  // Use segment sum for arc math (may differ from centerTotal if centerTotal is filtered)
  const arcTotal = segments.reduce((s, x) => s + x.count, 0);
  const computed = computeSegments(segments, arcTotal);
  const totalStr = total.toLocaleString("he-IL");

  return (
    <div
      className="flex flex-col items-center gap-5 sm:flex-row sm:items-center"
      role="img"
      aria-label={ariaLabel ?? `פילוח: ${segments.map((s) => `${s.label} ${s.count}`).join(", ")}`}
    >
      {/* SVG donut */}
      <div className="relative shrink-0" style={{ width: 150, height: 150 }}>
        <svg viewBox="0 0 160 160" width="150" height="150" aria-hidden="true" role="presentation">
          {/* Track ring */}
          <circle cx="80" cy="80" r="60" fill="none" stroke="#EEEEE9" strokeWidth="20" />
          {/* Segments */}
          <g transform="rotate(-90 80 80)" fill="none" strokeWidth="20" strokeLinecap="butt">
            {computed.map((seg) => (
              <circle
                key={seg.id}
                cx="80"
                cy="80"
                r="60"
                stroke={seg.color}
                strokeDasharray={seg.dashArray}
                strokeDashoffset={seg.dashOffset}
                aria-label={`${seg.label}: ${seg.count.toLocaleString("he-IL")}`}
              />
            ))}
          </g>
        </svg>

        {/* Centre text */}
        <div
          className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center"
          aria-hidden="true"
        >
          <span
            className="font-extrabold tabular-nums leading-none tracking-tight"
            style={{
              fontSize: "27px",
              color: "var(--fg1, #111318)",
              fontVariantNumeric: "tabular-nums",
              letterSpacing: "-0.04em",
            }}
          >
            {totalStr}
          </span>
          <span
            className="mt-1 font-medium"
            style={{ fontSize: "11px", color: "var(--fg3, #5E6560)" }}
          >
            {centerSublabel}
          </span>
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-1 flex-col gap-2.5">
        {computed.map((seg) => (
          <div key={seg.id} className="flex items-center gap-2">
            <span
              className="inline-block shrink-0 rounded-[2px]"
              style={{ width: 9, height: 9, background: seg.color }}
              aria-hidden="true"
            />
            <span
              className="flex-1 text-sm"
              style={{ color: "var(--fg2, #4E5663)", fontWeight: 500 }}
            >
              {seg.label}
            </span>
            <span
              className="font-semibold tabular-nums"
              style={{
                fontSize: "13.5px",
                color: "var(--fg1, #111318)",
                fontVariantNumeric: "tabular-nums",
                fontFamily: "var(--font-mono, ui-monospace, monospace)",
              }}
            >
              {seg.count.toLocaleString("he-IL")}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── GradeDonut ────────────────────────────────────────────────────────────────

interface GradeDonutProps {
  gradeDistribution: InventorySummaryVM["gradeDistribution"];
}

export function GradeDonut({ gradeDistribution }: GradeDonutProps) {
  const segments: DonutSegmentDef[] = GRADE_ORDER
    .filter((g) => {
      const count = g === "unscored" ? gradeDistribution.unscored : gradeDistribution[g];
      // Suppress "unscored" when count is 0; always show graded grades if present
      return count > 0;
    })
    .map((g) => ({
      id: g,
      label: g === "unscored" ? "ללא ציון" : `ציון ${g}`,
      count: g === "unscored" ? gradeDistribution.unscored : gradeDistribution[g],
      color: GRADE_DONUT_COLORS[g],
    }));

  const gradedTotal = (["A", "B", "C", "D", "E"] as BariGrade[]).reduce(
    (sum, g) => sum + (gradeDistribution[g] ?? 0),
    0,
  );

  return (
    <DonutChart
      segments={segments}
      centerTotal={gradedTotal + (gradeDistribution.unscored ?? 0)}
      centerSublabel="מוצרים"
      ariaLabel={`פילוח לפי ציון: ${segments.map((s) => `${s.label} ${s.count}`).join(", ")}`}
    />
  );
}

// ── RetailerDonut — legacy shim (API compat) ──────────────────────────────────

const RETAILER_PALETTE: Record<string, string> = {
  shufersal: "#1F8F6A",
  yochananof: "#2FAE82",
  victory: "#86B6A6",
  "rami-levy": "#2FAE82",
  other: "#D6D8D1",
};
const FALLBACK_COLORS = ["#86B6A6", "#A8CEC4", "#C4DDD8"];

interface RetailerDonutProps {
  breakdown: Array<BariRetailerRefVM & { count: number }>;
  total: number;
}

export function RetailerDonut({ breakdown, total }: RetailerDonutProps) {
  const segments: DonutSegmentDef[] = breakdown.map((r, i) => ({
    id: r.id,
    label: r.nameHe,
    count: r.count,
    color: RETAILER_PALETTE[r.id] ?? FALLBACK_COLORS[i % FALLBACK_COLORS.length],
  }));

  return (
    <DonutChart
      segments={segments}
      centerTotal={total}
      centerSublabel="מוצרים"
      ariaLabel={`פילוח לפי רשת: ${breakdown.map((r) => `${r.nameHe} ${r.count} מוצרים`).join(", ")}`}
    />
  );
}
