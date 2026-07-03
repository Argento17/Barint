"use client";

import { Bar, BarChart, CartesianGrid, Cell, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { seedOilsArticle } from "@/lib/blog/seed-oils-article-content";

/**
 * SeedOilsCookiesChart — the article's proof visual: rank-1 cookie (~60/C,
 * contains canola oil) vs. the bottom two cookies (~10/E, also contain seed
 * oil). Same seed-oil presence, ~50-point gap — the point is that presence
 * alone doesn't drive the grade.
 *
 * Data: seedOilsArticle.sections[bari-proof].chart (src/data/blog/seed-oils.json),
 * sourced from cookies_coffee_frontend_v2.json (117-product corpus). Numbers are
 * intentionally rounded (60 / 10) to match the surrounding prose and stay
 * re-flow-durable — no decimals, no internal-rule numbers.
 *
 * recharts, not raw SVG (Bari convention — see brined-cheeses-prologue-visualizations.tsx).
 * Grade is never color-encoded elsewhere in Bari; here the two colors intentionally
 * encode the article's OWN two-group comparison (top vs. bottom), not a grade scale.
 */

const TOP_COLOR = "#1F8F6A"; // Bari teal — rank 1
const BOTTOM_COLOR = "#B7BDC4"; // neutral gray — bottom two (same seed-oil presence, low score)

type ChartBar = {
  id: string;
  label: string;
  name: string;
  score: number;
  grade: string;
  tag: string;
};

function TipBox({ bar }: { bar: ChartBar }) {
  return (
    <div
      dir="rtl"
      style={{
        background: "#111318",
        color: "#fff",
        borderRadius: 10,
        padding: "8px 11px",
        fontSize: 12,
        lineHeight: 1.4,
        maxWidth: 220,
        boxShadow: "0 8px 24px rgba(0,0,0,0.18)",
      }}
    >
      <div style={{ fontWeight: 600 }}>{bar.name}</div>
      <div style={{ opacity: 0.85, marginTop: 2 }}>
        {bar.label} · ציון {bar.score} · דירוג {bar.grade}
      </div>
      <div style={{ opacity: 0.85, marginTop: 2 }}>{bar.tag}</div>
    </div>
  );
}

export function SeedOilsCookiesChart() {
  const chart = (seedOilsArticle.sections as unknown as { id: string; chart?: { eyebrow: string; title: string; caption: string; bars: ChartBar[]; footnote: string } }[]).find(
    (s) => s.id === "bari-proof",
  )?.chart;

  if (!chart) return null;

  return (
    <section className="rounded-[1.35rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-6 md:px-8 md:py-8" dir="rtl">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          {chart.eyebrow}
        </p>
        <h3 className="mt-1.5 text-lg font-extrabold leading-tight tracking-[-0.01em] text-[#111318] md:text-xl">
          {chart.title}
        </h3>
        <p className="mt-1.5 text-[13px] leading-[1.55] text-[#5E6672]">{chart.caption}</p>
      </header>

      <div className="mt-5" style={{ direction: "ltr" }}>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={chart.bars} margin={{ top: 24, right: 12, left: 12, bottom: 8 }} barCategoryGap="28%">
            <CartesianGrid vertical={false} stroke="#EEF0F1" />
            <XAxis
              dataKey="label"
              reversed
              tick={{ fontSize: 12, fontWeight: 700, fill: "#444C47" }}
              tickLine={false}
              axisLine={{ stroke: "#EEF0F1" }}
            />
            <YAxis
              domain={[0, 70]}
              ticks={[0, 20, 40, 60]}
              tick={{ fontSize: 11, fill: "#9AA0A6" }}
              tickLine={false}
              axisLine={false}
              width={28}
              orientation="right"
            />
            <Tooltip
              cursor={{ fill: "rgba(17,19,24,0.04)" }}
              content={({ active, payload }) =>
                active && payload?.[0] ? <TipBox bar={payload[0].payload as ChartBar} /> : null
              }
            />
            <Bar dataKey="score" radius={[6, 6, 0, 0]} maxBarSize={72}>
              {chart.bars.map((bar) => (
                <Cell key={bar.id} fill={bar.id === "rank1" ? TOP_COLOR : BOTTOM_COLOR} />
              ))}
              <LabelList
                dataKey="score"
                position="top"
                formatter={(value: string | number | boolean | null | undefined) => `${value ?? ""}`}
                style={{ fontSize: 13, fontWeight: 800, fill: "#111318" }}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Tag legend — both groups labeled "contains seed oil" so the point (presence
          doesn't drive the grade) is glanceable without hovering. */}
      <div className="mt-4 flex flex-wrap items-center justify-end gap-x-5 gap-y-2 text-right">
        {chart.bars.map((bar) => (
          <div key={bar.id} className="flex items-center gap-2">
            <span
              className="inline-block size-2.5 rounded-full"
              style={{ background: bar.id === "rank1" ? TOP_COLOR : BOTTOM_COLOR }}
            />
            <span className="text-xs text-[#4E5663]">
              {bar.label} · {bar.tag}
            </span>
          </div>
        ))}
      </div>

      <p className="mt-4 text-[11px] leading-relaxed text-[#7A817C]">{chart.footnote}</p>
    </section>
  );
}
