"use client";

import type { BariProductMetricsVM } from "@/lib/view-models";

// Column-aligned, category-scoped metric block (comparison-v2-spec §4, README §5).
// Fixed-width metrics so they align column-to-column down the list — that alignment
// IS the differentiator. Display-only, never a score input. Null → "—", never 0 (§2.3).
// The numeric value is the source of truth; bars/pips are decorative + aria-hidden,
// the group carries the aria-label. Limits are information, not alarms — no red (§4.3).

const TONE = {
  good: "#1F8F6A",
  poor: "#B5882F",
  neutral: "#B5BBB6",
  neutralPip: "#9AA09B",
  track: "#ECECE7",
  emptyPip: "#E6E6E0",
} as const;

type MetricNumberKey =
  | "protein_g"
  | "fiber_g"
  | "additive_count"
  | "base_pct"
  | "sugar_g"
  | "sodium_mg";

export interface MetricSpec {
  key: MetricNumberKey;
  /** short Hebrew label, e.g. "חלבון". */
  label: string;
  /** unit suffix on the value, e.g. "ג׳" or "%". Omit for counts. */
  unit?: string;
  /** per-serving basis shown in the column HEADER, e.g. "ל-100 ג׳" / "ל-100 מ״ל".
   *  Makes the metric's basis explicit above the column (the value cell stays terse). */
  perLabel?: string;
  render: "bar" | "pips";
  /** display scale max (bar fill / pip count). */
  scaleMax: number;
  /** value ≥ good → green; value past poor → amber; otherwise neutral. */
  good?: number;
  poor?: number;
  /** when true, a LOWER value is better (sugar, additives): good = ≤good, poor = ≥poor. */
  lowerIsBetter?: boolean;
  /** spoken units for the aria-label, e.g. "גרם" / "תוספי מזון". */
  ariaUnit: string;
}

// ── Category presets (MILK_RECOMMENDATION §1: the set is category-scoped) ──────────
// Only metrics with real source data should be listed. additive_count / base_pct are
// NOT yet exposed by BSIP (Data Agent dependency) — left out until populated, rather
// than fabricated. Hummus features protein by editorial decision (its prologue headline).
export const PROTEIN_METRIC: MetricSpec = {
  key: "protein_g",
  label: "חלבון",
  unit: "ג׳",
  perLabel: "ל-100 ג׳",
  render: "bar",
  scaleMax: 20,
  good: 10,
  poor: 5,
  ariaUnit: "גרם חלבון ל-100 גרם",
};

// Dairy/milk variant of the protein metric (MILK_RECOMMENDATION §1 risk note): values
// are per-100ml and the category range is narrower/lower than hummus (cow ~3.3, soy up to
// ~6.5, almond/rice <1), so the 0–20g hummus scale would flatten every bar. Dairy-tuned
// max + thresholds keep the bars meaningful and the aria unit honest (מ״ל, not גרם).
export const DAIRY_PROTEIN_METRIC: MetricSpec = {
  key: "protein_g",
  label: "חלבון",
  unit: "ג׳",
  perLabel: "ל-100 מ״ל",
  render: "bar",
  scaleMax: 8,
  good: 5,
  poor: 2,
  ariaUnit: "גרם חלבון ל-100 מ״ל",
};

// Vegetable-spread variant (TASK-165): matbucha/eggplant/pepper spreads draw from the hummus
// corpus but are protein-poor — the real shelf range is 0.7–6.3g per 100g (most cluster 0.7–2.5g),
// so the 0–20g hummus PROTEIN_METRIC scale flattens every bar to a sliver. A 0–7g max lets the top
// value (6.3g) read near-full while the low cluster still discriminates. These are SOLIDS, so the
// aria unit stays "ל-100 גרם" (not the dairy per-100ml). Thresholds scaled to the range: ≥3g good, <1g poor.
export const VEG_PROTEIN_METRIC: MetricSpec = {
  key: "protein_g",
  label: "חלבון",
  unit: "ג׳",
  perLabel: "ל-100 ג׳",
  render: "bar",
  scaleMax: 7,
  good: 3,
  poor: 1,
  ariaUnit: "גרם חלבון ל-100 גרם",
};

// Bread variant (TASK-162): fiber is bread's truer headline number than protein. Values are
// per-100g and the real shelf range is ~3–18.5g, so a 0–20 max keeps the top end (≈18.5g)
// from clipping while still giving the low end (3g) a visible bar. Higher fiber is better, so
// lowerIsBetter stays off: ≥7g (whole-grain territory) reads as good, <4g (refined flour) as poor.
export const FIBER_METRIC: MetricSpec = {
  key: "fiber_g",
  label: "סיבים",
  unit: "ג׳",
  perLabel: "ל-100 ג׳",
  render: "bar",
  scaleMax: 20,
  good: 7,
  poor: 4,
  ariaUnit: "גרם סיבים ל-100 גרם",
};

// Salty-snacks variant (TASK-227): sodium is the category's second headline number after
// fiber — it's what separates a baked-legume snack from a salt-loaded extruded puff. Real
// per-100g label value; shelf range is ~10–920mg, so a 0–1000 max keeps the bars meaningful.
// Lower is better: ≤300mg (genuinely low for a salty snack) reads good, ≥600mg reads as a
// limit worth seeing. Information, not alarm — amber, never red (§4.3).
export const SODIUM_METRIC: MetricSpec = {
  key: "sodium_mg",
  label: "נתרן",
  unit: 'מ״ג',
  perLabel: "ל-100 ג׳",
  render: "bar",
  scaleMax: 1000,
  good: 300,
  poor: 600,
  lowerIsBetter: true,
  ariaUnit: 'מ״ג נתרן ל-100 גרם',
};

export const ADDITIVES_METRIC: MetricSpec = {
  key: "additive_count",
  label: "תוספים",
  render: "pips",
  scaleMax: 5,
  good: 1,
  poor: 4,
  lowerIsBetter: true,
  ariaUnit: "תוספי מזון",
};

export const BASE_METRIC: MetricSpec = {
  key: "base_pct",
  label: "% גרגר",
  unit: "%",
  render: "bar",
  scaleMax: 100,
  good: 80,
  poor: 55,
  ariaUnit: "אחוז רכיב עיקרי",
};

export const SUGAR_METRIC: MetricSpec = {
  key: "sugar_g",
  label: "סוכר",
  unit: "ג׳",
  render: "bar",
  scaleMax: 15,
  good: 5,
  poor: 10,
  lowerIsBetter: true,
  ariaUnit: "גרם סוכר ל-100 מ״ל",
};

// Display rounding: raw per-100g values can carry full float precision (e.g. fiber
// 7.66666666666667 from a back-computed panel). Round to at most 1 decimal and drop a
// trailing ".0" so the value fits the 62px cell and never overflows into the next metric.
function formatMetricValue(value: number): string {
  const rounded = Math.round(value * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

function toneFor(spec: MetricSpec, value: number): keyof typeof TONE {
  const { good, poor, lowerIsBetter } = spec;
  if (good == null || poor == null) return "neutral";
  if (lowerIsBetter) {
    if (value <= good) return "good";
    if (value >= poor) return "poor";
    return "neutral";
  }
  if (value >= good) return "good";
  if (value < poor) return "poor";
  return "neutral";
}

function Metric({ spec, value }: { spec: MetricSpec; value: number | null }) {
  const hasValue = typeof value === "number";
  const ariaLabel = hasValue
    ? `${spec.label} ${formatMetricValue(value)} ${spec.ariaUnit}`
    : `${spec.label} — נתון לא זמין`;
  const tone = hasValue ? toneFor(spec, value) : "neutral";

  return (
    <div className="w-[62px] shrink-0" role="group" aria-label={ariaLabel}>
      <div className="flex items-baseline justify-between gap-1">
        <span className="text-[0.6rem] font-medium leading-none text-[#9AA09B]" aria-hidden>
          {spec.label}
        </span>
        <span
          className="text-[0.74rem] font-bold leading-none tabular-nums"
          style={{ color: hasValue ? "#4A524E" : "#9AA09B" }}
          aria-hidden
        >
          {hasValue ? (
            <>
              {formatMetricValue(value)}
              {spec.unit ? (
                <i className="text-[0.56rem] font-medium not-italic text-[#9AA09B]">
                  {spec.unit === "%" ? "%" : ` ${spec.unit}`}
                </i>
              ) : null}
            </>
          ) : (
            "—"
          )}
        </span>
      </div>

      {spec.render === "bar" ? (
        <div
          className="mt-1 h-[3px] w-full overflow-hidden rounded-full bg-[#ECECE7]"
          aria-hidden
        >
          {hasValue ? (
            <span
              className="block h-full rounded-full"
              style={{
                width: `${Math.max(0, Math.min(100, (value / spec.scaleMax) * 100))}%`,
                background: TONE[tone],
              }}
            />
          ) : null}
        </div>
      ) : (
        <div className="mt-[5px] flex gap-[3px]" aria-hidden>
          {Array.from({ length: spec.scaleMax }).map((_, i) => (
            <span
              key={i}
              className="h-[5px] w-full rounded-[2px]"
              style={{
                background:
                  hasValue && i < value
                    ? tone === "neutral"
                      ? TONE.neutralPip
                      : TONE[tone]
                    : TONE.emptyPip,
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}

/**
 * Category-scoped aligned metric block. `specs` is the per-category metric set; the
 * component reads each spec's key off `metrics`. Empty `specs` → renders nothing
 * (categories without a metric surface just omit it).
 */
export function MetricColumn({
  specs,
  metrics,
}: {
  specs: readonly MetricSpec[];
  metrics?: BariProductMetricsVM;
}) {
  if (specs.length === 0) return null;

  return (
    <div className="flex items-center gap-[14px]" role="group" aria-label="מדדי מוצר">
      {specs.map((spec) => (
        <Metric key={spec.key} spec={spec} value={metrics?.[spec.key] ?? null} />
      ))}
    </div>
  );
}
