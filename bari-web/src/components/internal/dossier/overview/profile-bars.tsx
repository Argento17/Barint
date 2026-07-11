"use client";

import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { DIMENSION_LABEL } from "@/lib/dossier/overview-labels";
import type { Layer3 } from "@/lib/dossier/types";

// Overview §D — compact 2D product-profile visual (TASK-620 / PD-3.1). Bars,
// not a radar/polygon (spec: "2D only, no 3D") — reuses the same plain-bars
// approach as the Technical-audit NamespaceBars component, restyled with
// English labels and restricted to PRODUCT metrics only: this reads
// `layer_3.assessment.dimension_scores` exclusively and never renders
// data_quality or publication_record fields (spec hard rule — this profile is
// about the product, not the record).
//
// NOTE on scope: the spec named 5 illustrative axes ("Nutrition, Ingredients,
// Processing, Additives, Category position"). The compiler's actual
// dimension_scores keys are a different, real 10-axis set (see
// DIMENSION_LABEL) — there is no field in the data matching the spec's 5 names
// literally. Rather than force an invented mapping not backed by any real
// field, this renders the REAL dimension_scores keys under honest English
// labels (a deterministic projection of an existing field, per the Overview's
// own "no invented claims" rule). Flagged in the TASK-620 return.
export function ProductProfileBars({ assessment }: { assessment: Layer3["assessment"] }) {
  const raw = assessment.dimension_scores?.value as Record<string, number> | null | undefined;

  const data = raw
    ? Object.entries(raw)
        .filter(([, v]) => typeof v === "number")
        .map(([key, value]) => ({ key, label: DIMENSION_LABEL[key] ?? key, value }))
        .sort((a, b) => b.value - a.value)
    : [];

  if (data.length === 0) {
    return (
      <div className="rounded-md border border-neutral-200 p-4">
        <h3 className="mb-1 text-sm font-semibold text-neutral-800">Product profile</h3>
        <p className="py-6 text-center text-sm text-neutral-400">No per-axis assessment data available for this product.</p>
      </div>
    );
  }

  return (
    <div className="rounded-md border border-neutral-200 p-4">
      <h3 className="mb-2 text-sm font-semibold text-neutral-800">Product profile</h3>
      <p className="mb-3 text-[11px] text-neutral-400">
        Per-axis assessment scores (0–100), highest first. Product signal only — never blended with data quality or publication fields.
      </p>
      <ResponsiveContainer width="100%" height={Math.max(180, data.length * 30)}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, bottom: 4, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} />
          <YAxis type="category" dataKey="label" width={120} tick={{ fontSize: 11 }} />
          <Tooltip formatter={(value) => [value == null ? "—" : `${value}`, "score"]} />
          <Bar dataKey="value" radius={[4, 4, 4, 4]}>
            {data.map((d) => (
              <Cell key={d.key} fill="#167A58" fillOpacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
