"use client";

import { useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { Layer3, Metric } from "@/lib/dossier/types";

type NamespaceId = "assessment" | "data_quality";

const NAMESPACE_LABEL: Record<NamespaceId, string> = {
  assessment: "הערכת מוצר (assessment)",
  data_quality: "איכות רשומה (data_quality)",
};

const NAMESPACE_COLOR: Record<NamespaceId, string> = {
  assessment: "#167A58",
  data_quality: "#546E14",
};

const DIMENSION_LABEL_HE: Record<string, string> = {
  additive_quality: "תוספי מזון",
  calorie_density: "צפיפות קלורית",
  fat_quality: "איכות שומן",
  glycemic_quality: "איכות גליקמית",
  nutrient_density: "צפיפות תזונתית",
  processing_quality: "רמת עיבוד",
  protein_quality: "איכות חלבון",
  regulatory_quality: "רגולציה",
  satiety_support: "תחושת שובע",
  whole_food_integrity: "שלמות המזון",
};

const DATA_QUALITY_LABEL_HE: Record<string, string> = {
  evidence_completeness: "שלמות ראיות",
  evidence_flag_rate: "שיעור דגלים",
  identity_confidence: "ודאות זהות",
  image_confidence: "ודאות תמונה",
};

/**
 * Plain labeled bars (NOT a radar/polygon — per memo §5 MVP fallback:
 * "if the radar costs more than ~a day, ship plain labeled bars instead").
 *
 * Renders `assessment` and `data_quality` as two SEPARATE, user-toggleable
 * bar charts (memo R-C: never blended into one shape or one number). Only
 * one namespace is visible at a time; switching the toggle swaps the whole
 * chart (axes, scale, and color all change) so there is no way to read them
 * as parts of a single composite score.
 */
export function NamespaceBars({ layer3 }: { layer3: Layer3 }) {
  const [active, setActive] = useState<NamespaceId>("assessment");

  const dimensionScores = (layer3.assessment.dimension_scores?.value ?? null) as Record<string, number> | null;

  const assessmentData =
    dimensionScores && Object.keys(dimensionScores).length > 0
      ? Object.entries(dimensionScores).map(([key, value]) => ({
          key,
          label: DIMENSION_LABEL_HE[key] ?? key,
          value,
          max: 100,
        }))
      : [];

  const dataQualityData = Object.entries(layer3.data_quality)
    .filter(([key]) => key !== "image_confidence" || layer3.data_quality[key]?.value !== null)
    .map(([key, metric]) => ({
      key,
      label: DATA_QUALITY_LABEL_HE[key] ?? key,
      value: metric.value === null ? null : Math.round((metric.value as number) * 100),
      max: 100,
    }));

  const activeData = active === "assessment" ? assessmentData : dataQualityData;
  const headerMetrics: [string, Metric][] =
    active === "assessment"
      ? [
          ["final_score_estimate", layer3.assessment.final_score_estimate],
          ["grade_estimate", layer3.assessment.grade_estimate],
          ["confidence_score", layer3.assessment.confidence_score],
          ["category", layer3.assessment.category],
        ]
      : [];

  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold">שכבה 3 — נתוני הערכה (bars, לא ראדר)</h2>
        <div className="flex gap-1 rounded-md border border-neutral-200 p-0.5">
          {(["assessment", "data_quality"] as NamespaceId[]).map((ns) => (
            <button
              key={ns}
              onClick={() => setActive(ns)}
              className={`rounded px-2.5 py-1 text-xs font-medium transition ${
                active === ns ? "text-white" : "text-neutral-500 hover:bg-neutral-50"
              }`}
              style={active === ns ? { backgroundColor: NAMESPACE_COLOR[ns] } : undefined}
            >
              {NAMESPACE_LABEL[ns]}
            </button>
          ))}
        </div>
      </div>

      <p className="mb-3 text-xs text-neutral-400">
        שתי שכבות נפרדות לחלוטין — לעולם לא ממוצעות לציון אחד. הצג שכבה אחת בכל פעם.
      </p>

      {headerMetrics.length > 0 && (
        <div className="mb-3 flex flex-wrap gap-4 text-xs text-neutral-500">
          {headerMetrics.map(([key, metric]) => (
            <span key={key}>
              <span className="text-neutral-400">{key}:</span>{" "}
              <span className="font-medium text-neutral-800">{String(metric?.value ?? "—")}</span>
            </span>
          ))}
        </div>
      )}

      {activeData.length === 0 ? (
        <p className="py-8 text-center text-sm text-neutral-400">
          {active === "assessment" ? "אין נתוני dimension_scores עבור מוצר זה (ייתכן שאין trace)." : "אין מדדי data_quality זמינים."}
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={Math.max(180, activeData.length * 34)}>
          <BarChart data={activeData} layout="vertical" margin={{ top: 4, right: 24, bottom: 4, left: 8 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} />
            <YAxis type="category" dataKey="label" width={110} tick={{ fontSize: 11 }} orientation="right" />
            <Tooltip formatter={(value) => [value === null || value === undefined ? "—" : `${value}`, "value"]} />
            <Bar dataKey="value" radius={[4, 4, 4, 4]}>
              {activeData.map((d) => (
                <Cell key={d.key} fill={NAMESPACE_COLOR[active]} fillOpacity={d.value === null ? 0.15 : 0.85} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
