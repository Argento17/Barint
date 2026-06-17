"use client";

import { useMemo } from "react";
import {
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

import type { BariProductVM } from "@/lib/view-models";

// ─── Brand palette (hollow-point data-journalism aesthetic) ───────────────────
// HARD RULE: grade is NEVER color-encoded. Every dot is the same brand ink.
const BRAND = "#1F8F6A"; // Bari teal — uniform across all dots (not a grade signal)
const BRAND_LIGHT = "rgba(31,143,106,0.14)";
const MEDIAN_ACCENT = "#1F8F6A";
const AXIS = "#9AA0A6";
const GRID = "#EEF0F1";
const CAPTION = "#5E6672";
const EYEBROW = "#8A908B";
const INK = "#1B1F24";

const MEDIAN = 1000;

const sodiumOf = (p: BariProductVM) => p.expansion?.nutrition?.sodium ?? null;
const proteinOf = (p: BariProductVM) => p.expansion?.nutrition?.protein ?? null;
const fatOf = (p: BariProductVM) => p.expansion?.nutrition?.fat ?? null;
const kcalOf = (p: BariProductVM) => p.expansion?.nutrition?.energyKcal ?? null;

// Hollow circle — transparent-ish fill, brand ring.
function HollowDot(props: { cx?: number; cy?: number }) {
  const { cx, cy } = props;
  if (cx == null || cy == null) return null;
  return <circle cx={cx} cy={cy} r={6} fill={BRAND_LIGHT} stroke={BRAND} strokeWidth={2.25} />;
}

function TipBox({ lines }: { lines: string[] }) {
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
        maxWidth: 240,
        boxShadow: "0 8px 24px rgba(0,0,0,0.18)",
      }}
    >
      {lines.map((l, i) => (
        <div key={i} style={{ fontWeight: i === 0 ? 600 : 400, opacity: i === 0 ? 1 : 0.85 }}>
          {l}
        </div>
      ))}
    </div>
  );
}

function Frame({
  eyebrow,
  title,
  caption,
  children,
}: {
  eyebrow: string;
  title: string;
  caption: string;
  children: React.ReactNode;
}) {
  return (
    <section className="w-full">
      <p className="text-[11px] font-semibold uppercase tracking-[0.09em]" style={{ color: EYEBROW }}>
        {eyebrow}
      </p>
      <h3 className="mt-1.5 text-[1.15rem] font-bold leading-tight tracking-[-0.01em]" style={{ color: INK }}>
        {title}
      </h3>
      <p className="mt-1.5 mb-3 text-[12.5px] leading-[1.55]" style={{ color: CAPTION }}>
        {caption}
      </p>
      {children}
    </section>
  );
}

// ─── Chart A — Sodium × grade (the signature insight) ─────────────────────────
const GRADE_LANES = ["A", "B", "C", "D"] as const;
type Grade = (typeof GRADE_LANES)[number];

function SodiumGradeChart({ products }: { products: BariProductVM[] }) {
  const { data, aAbove, aTotal } = useMemo(() => {
    const d: { sodium: number; grade: Grade; name: string; score: number | null }[] = [];
    let above = 0;
    let total = 0;
    for (const p of products) {
      const s = sodiumOf(p);
      const g = p.grade as Grade | undefined;
      if (s == null || !g || !GRADE_LANES.includes(g)) continue;
      d.push({ sodium: s, grade: g, name: p.name, score: p.score });
      if (g === "A") {
        total += 1;
        if (s >= 900) above += 1;
      }
    }
    return { data: d, aAbove: above, aTotal: total };
  }, [products]);

  return (
    <Frame
      eyebrow="ספקטרום המלח"
      title="A הוא לא דל-נתרן"
      caption={`${aAbove} מתוך ${aTotal} גבינות ה-A יושבות מעל 900 מ"ג. הדירוג נקבע על מבנה הרכיבים — לא על המלח.`}
    >
      <ResponsiveContainer width="100%" height={250}>
        <ScatterChart margin={{ top: 16, right: 16, left: 4, bottom: 18 }}>
          <XAxis
            type="number"
            dataKey="sodium"
            name="נתרן"
            domain={[540, 1700]}
            ticks={[600, 800, 1000, 1200, 1400, 1600]}
            tick={{ fontSize: 11, fill: AXIS }}
            tickLine={false}
            axisLine={{ stroke: GRID }}
            tickFormatter={(v) => `‎${v.toLocaleString()}‎`}
            label={{ value: 'נתרן (מ"ג ל-100 גרם)', position: "bottom", offset: 2, fontSize: 11, fill: AXIS }}
          />
          <YAxis
            type="category"
            dataKey="grade"
            domain={GRADE_LANES as unknown as string[]}
            allowDuplicatedCategory={false}
            tick={{ fontSize: 14, fontWeight: 700, fill: "#444C47" }}
            tickLine={false}
            axisLine={false}
            width={24}
            reversed
          />
          <ZAxis range={[60, 60]} />
          <ReferenceLine
            x={MEDIAN}
            stroke={MEDIAN_ACCENT}
            strokeDasharray="4 3"
            strokeWidth={1.5}
            label={{ value: "חציון 1,000", position: "top", fill: MEDIAN_ACCENT, fontSize: 10, fontWeight: 600 }}
          />
          <Tooltip
            cursor={{ stroke: "rgba(17,19,24,0.1)" }}
            content={({ active, payload }) =>
              active && payload?.[0] ? (
                <TipBox
                  lines={[
                    (payload[0].payload as { name: string }).name,
                    `${(payload[0].payload as { sodium: number }).sodium} מ"ג · ציון ${(payload[0].payload as { score: number }).score}`,
                  ]}
                />
              ) : null
            }
          />
          <Scatter data={data} shape={<HollowDot />} />
        </ScatterChart>
      </ResponsiveContainer>
    </Frame>
  );
}

// ─── Chart B — Protein × fat ──────────────────────────────────────────────────
function ProteinFatChart({ products }: { products: BariProductVM[] }) {
  const data = useMemo(
    () =>
      products
        .map((p) => {
          const protein = proteinOf(p);
          const fat = fatOf(p);
          if (protein == null || fat == null) return null;
          return { fat, protein, name: p.name, score: p.score };
        })
        .filter(Boolean) as { fat: number; protein: number; name: string; score: number | null }[],
    [products]
  );

  return (
    <Frame
      eyebrow="צפיפות תזונתית"
      title="חלבון מול שומן"
      caption='השומן במדף נע בין 5% ל-31%. יותר שומן לא קונה יותר חלבון — צפיפות החלבון היא עניין נפרד.'
    >
      <ResponsiveContainer width="100%" height={260}>
        <ScatterChart margin={{ top: 16, right: 16, left: 0, bottom: 18 }}>
          <XAxis
            type="number"
            dataKey="fat"
            domain={[0, 33]}
            ticks={[0, 5, 10, 15, 20, 25, 30]}
            tick={{ fontSize: 11, fill: AXIS }}
            tickLine={false}
            axisLine={{ stroke: GRID }}
            label={{ value: "שומן (גרם ל-100 גרם)", position: "bottom", offset: 2, fontSize: 11, fill: AXIS }}
          />
          <YAxis
            type="number"
            dataKey="protein"
            domain={[0, 27]}
            ticks={[0, 5, 10, 15, 20, 25]}
            tick={{ fontSize: 11, fill: AXIS }}
            tickLine={false}
            axisLine={false}
            width={30}
            label={{ value: "חלבון", angle: -90, position: "insideLeft", fontSize: 11, fill: AXIS, dy: 20 }}
          />
          <ZAxis range={[60, 60]} />
          <Tooltip
            cursor={{ strokeDasharray: "3 3", stroke: "rgba(17,19,24,0.12)" }}
            content={({ active, payload }) =>
              active && payload?.[0] ? (
                <TipBox
                  lines={[
                    (payload[0].payload as { name: string }).name,
                    `חלבון ${(payload[0].payload as { protein: number }).protein} ג' · שומן ${(payload[0].payload as { fat: number }).fat}% · ציון ${(payload[0].payload as { score: number }).score}`,
                  ]}
                />
              ) : null
            }
          />
          <Scatter data={data} shape={<HollowDot />} />
        </ScatterChart>
      </ResponsiveContainer>
    </Frame>
  );
}

// ─── Chart C — Calories × score ───────────────────────────────────────────────
function CalorieScoreChart({ products }: { products: BariProductVM[] }) {
  const data = useMemo(
    () =>
      products
        .map((p) => {
          const kcal = kcalOf(p);
          if (kcal == null || p.score == null) return null;
          return { kcal, score: p.score, name: p.name };
        })
        .filter(Boolean) as { kcal: number; score: number; name: string }[],
    [products]
  );

  return (
    <Frame
      eyebrow="המחיר הקלורי של האיכות"
      title="קלוריות מול ציון"
      caption='הגבינות בראש הדירוג נוטות להיות דלות-קלוריות (כ-117 קק"ל), בעוד שבתחתית הקלוריות מטפסות מעבר ל-300.'
    >
      <ResponsiveContainer width="100%" height={260}>
        <ScatterChart margin={{ top: 16, right: 16, left: 0, bottom: 18 }}>
          <XAxis
            type="number"
            dataKey="kcal"
            domain={[60, 380]}
            ticks={[100, 150, 200, 250, 300, 350]}
            tick={{ fontSize: 11, fill: AXIS }}
            tickLine={false}
            axisLine={{ stroke: GRID }}
            tickFormatter={(v) => `‎${v}‎`}
            label={{ value: "אנרגיה (קק\"ל ל-100 גרם)", position: "bottom", offset: 2, fontSize: 11, fill: AXIS }}
          />
          <YAxis
            type="number"
            dataKey="score"
            domain={[40, 90]}
            ticks={[40, 50, 60, 70, 80, 90]}
            tick={{ fontSize: 11, fill: AXIS }}
            tickLine={false}
            axisLine={false}
            width={30}
            label={{ value: "ציון", angle: -90, position: "insideLeft", fontSize: 11, fill: AXIS, dy: 12 }}
          />
          <ZAxis range={[60, 60]} />
          <Tooltip
            cursor={{ strokeDasharray: "3 3", stroke: "rgba(17,19,24,0.12)" }}
            content={({ active, payload }) =>
              active && payload?.[0] ? (
                <TipBox
                  lines={[
                    (payload[0].payload as { name: string }).name,
                    `${(payload[0].payload as { kcal: number }).kcal} קק"ל · ציון ${(payload[0].payload as { score: number }).score}`,
                  ]}
                />
              ) : null
            }
          />
          <Scatter data={data} shape={<HollowDot />} />
        </ScatterChart>
      </ResponsiveContainer>
    </Frame>
  );
}

// ─── Container ───────────────────────────────────────────────────────────────
/**
 * Brined-cheeses golden-template charts — recharts, hollow-point data-journalism
 * aesthetic (derived from the NotebookLM exploration; data verified against
 * brined_cheeses_frontend_v2.json). HARD RULE: grade is NEVER color-encoded —
 * every dot is the uniform brand ink; grade appears only as a text lane label.
 * Drift amendment (owner-sanctioned): charts precede the first product row.
 */
export function BrinedCheesesPrologueVisualizations({ products }: { products: BariProductVM[] }) {
  return (
    <div data-testid="brined-viz" className="space-y-9 px-4 py-5 lg:px-8 xl:px-10 2xl:px-12">
      <SodiumGradeChart products={products} />
      <hr className="border-t" style={{ borderColor: "rgba(17,19,24,0.07)" }} />
      <ProteinFatChart products={products} />
      <hr className="border-t" style={{ borderColor: "rgba(17,19,24,0.07)" }} />
      <CalorieScoreChart products={products} />
    </div>
  );
}
