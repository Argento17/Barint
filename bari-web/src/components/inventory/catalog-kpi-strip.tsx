"use client";

/**
 * KPI header strip + grade distribution bar for the public /catalog dashboard.
 * All numbers derived from computeCatalogDashboardMetrics(rows) at render time.
 */

import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade } from "@/lib/view-models";
import {
  GRADED_KEYS,
  type CatalogDashboardMetrics,
  type CatalogGradeDistribution,
} from "./catalog-dashboard-metrics";

const CARD_SHELL =
  "rounded-lg border bg-white px-4 py-3 shadow-[0_1px_3px_rgba(17,19,24,0.06)]";
const HAIRLINE = "rgba(17,19,24,0.08)";

interface KpiCardProps {
  label: string;
  value: string;
  sub?: string;
}

function KpiCard({ label, value, sub }: KpiCardProps) {
  return (
    <div className={CARD_SHELL} style={{ borderColor: HAIRLINE }}>
      <p
        className="text-[11px] font-semibold leading-tight"
        style={{ color: "var(--fg3, #5E6560)" }}
      >
        {label}
      </p>
      <p
        className="mt-1 font-extrabold tabular-nums leading-none tracking-tight"
        style={{
          fontSize: "clamp(22px, 3vw, 28px)",
          color: "var(--fg1, #111318)",
          fontVariantNumeric: "tabular-nums",
          letterSpacing: "-0.03em",
        }}
      >
        {value}
      </p>
      {sub ? (
        <p className="mt-1 text-[11px]" style={{ color: "var(--fg4, #888C88)" }}>
          {sub}
        </p>
      ) : null}
    </div>
  );
}

const GRADE_BAR_COLORS: Record<BariGrade | "unscored", string> = {
  A: BARI_COMPARISON_TOKENS.gradePalette.A.accent,
  B: BARI_COMPARISON_TOKENS.gradePalette.B.accent,
  C: BARI_COMPARISON_TOKENS.gradePalette.C.accent,
  D: BARI_COMPARISON_TOKENS.gradePalette.D.accent,
  E: BARI_COMPARISON_TOKENS.gradePalette.E.accent,
  unscored: "#D6D8D1",
};

interface GradeDistributionBarProps {
  distribution: CatalogGradeDistribution;
  total: number;
}

function GradeDistributionBar({ distribution, total }: GradeDistributionBarProps) {
  const segments: Array<{ key: BariGrade | "unscored"; count: number; label: string }> = [
    ...GRADED_KEYS.map((g) => ({ key: g, count: distribution[g], label: g })),
    ...(distribution.unscored > 0
      ? [{ key: "unscored" as const, count: distribution.unscored, label: "ללא" }]
      : []),
  ].filter((s) => s.count > 0);

  if (total === 0 || segments.length === 0) {
    return (
      <div
        className="flex h-2.5 w-full rounded-sm"
        style={{ background: "var(--surface-neutral, #F2F2ED)" }}
        aria-hidden
      />
    );
  }

  return (
    <div className="space-y-2">
      <div
        className="flex h-2.5 w-full overflow-hidden rounded-sm"
        role="img"
        aria-label={`פילוח דרגות: ${segments.map((s) => `${s.label} ${s.count}`).join(", ")}`}
      >
        {segments.map((seg) => {
          const pct = (seg.count / total) * 100;
          return (
            <div
              key={seg.key}
              style={{
                width: `${pct}%`,
                background: GRADE_BAR_COLORS[seg.key],
                minWidth: seg.count > 0 ? 2 : 0,
              }}
              title={`${seg.label}: ${seg.count.toLocaleString("he-IL")}`}
            />
          );
        })}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {segments.map((seg) => (
          <span
            key={seg.key}
            className="inline-flex items-center gap-1.5 text-[11px] font-medium"
            style={{ color: "var(--fg2, #4E5663)" }}
          >
            <span
              className="inline-block h-2 w-2 shrink-0 rounded-[2px]"
              style={{ background: GRADE_BAR_COLORS[seg.key] }}
              aria-hidden
            />
            <span>{seg.label}</span>
            <span
              className="font-semibold tabular-nums"
              style={{
                fontFamily: "var(--font-mono, ui-monospace, monospace)",
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {seg.count.toLocaleString("he-IL")}
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}

interface CatalogKpiStripProps {
  metrics: CatalogDashboardMetrics;
}

export function CatalogKpiStrip({ metrics }: CatalogKpiStripProps) {
  const { totalProducts, categoryCount, gradeDistribution, fullDataPercent, verifiedCount } =
    metrics;
  const gradedTotal = GRADED_KEYS.reduce((s, g) => s + gradeDistribution[g], 0);

  // When every product is scored, the "מוצרים עם ציון" card would just repeat the
  // total — show it only when there is an unscored remainder worth surfacing.
  const showGradedCard = gradeDistribution.unscored > 0;

  return (
    <section aria-label="מדדי קטלוג" className="space-y-3">
      <div className={`grid grid-cols-2 gap-3 ${showGradedCard ? "lg:grid-cols-4" : "lg:grid-cols-3"}`}>
        <KpiCard
          label="סה״כ מוצרים"
          value={totalProducts.toLocaleString("he-IL")}
        />
        <KpiCard
          label="קטגוריות"
          value={categoryCount.toLocaleString("he-IL")}
        />
        {showGradedCard && (
          <KpiCard
            label="מוצרים עם ציון"
            value={gradedTotal.toLocaleString("he-IL")}
            sub={`${gradeDistribution.unscored.toLocaleString("he-IL")} ללא ציון`}
          />
        )}
        <KpiCard
          label="נתונים מלאים"
          value={`${fullDataPercent.toLocaleString("he-IL")}%`}
          sub={`${verifiedCount.toLocaleString("he-IL")} מוצרים`}
        />
      </div>

      <div
        className={`${CARD_SHELL} py-3.5`}
        style={{ borderColor: HAIRLINE }}
      >
        <p
          className="mb-2.5 text-[11px] font-semibold"
          style={{ color: "var(--fg3, #5E6560)" }}
        >
          פילוח לפי דרגה
        </p>
        <GradeDistributionBar distribution={gradeDistribution} total={totalProducts} />
      </div>
    </section>
  );
}
