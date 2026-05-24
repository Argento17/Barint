"use client";

import { useMemo, useState } from "react";

import {
  PRODUCT_TYPE_COLORS,
  buildScatterPoints,
  type ScatterPoint,
} from "@/lib/blog/milk-analysis-chart-data";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";
import type { ProductType } from "@/lib/comparisons/milk-types";

const PLOT_W = 560;
const PLOT_H = 320;

/** Milk & plant drinks on the shelf map (no protein-drink category) */
const LEGEND_ORDER: ProductType[] = [
  "dairy",
  "soy",
  "oat",
  "almond",
  "rice",
  "coconut",
  "other_plant",
];

function scale(value: number, min: number, max: number): number {
  if (max === min) return 0.5;
  return (value - min) / (max - min);
}

function dotRadius(ingredientCount: number): number {
  return Math.min(14, Math.max(7, 5 + ingredientCount * 0.85));
}

type PlacedPoint = ScatterPoint & { cx: number; cy: number; r: number };

export function MilkAnalysisScatter() {
  const { scatter } = milkAnalysisArticle;
  const points = useMemo(() => buildScatterPoints(), []);
  const [hovered, setHovered] = useState<string | null>(null);

  const legendTypes = useMemo(() => {
    const present = new Set(points.map((p) => p.product.productType));
    return LEGEND_ORDER.filter((t) => present.has(t));
  }, [points]);

  const placed = useMemo((): PlacedPoint[] => {
    const xs = points.map((p) => p.ingredientComplexity);
    const ys = points.map((p) => p.lessProcessing);
    const minX = Math.min(...xs) - 4;
    const maxX = Math.max(...xs) + 4;
    const minY = Math.min(...ys) - 4;
    const maxY = Math.max(...ys) + 4;
    const pad = 28;

    return points.map((p) => {
      const tX = scale(p.ingredientComplexity, minX, maxX);
      const tY = scale(p.lessProcessing, minY, maxY);
      const cx = pad + (PLOT_W - pad * 2) * (1 - tX);
      const cy = pad + (PLOT_H - pad * 2) * (1 - tY);
      return { ...p, cx, cy, r: dotRadius(p.ingredientCount) };
    });
  }, [points]);

  const active = placed.find((p) => p.product.barcode === hovered);
  const midX = PLOT_W / 2;
  const midY = PLOT_H / 2;

  return (
    <section id="shelf-map" className="scroll-mt-24">
      <header className="mb-6 md:mb-8">
        <p className="text-sm font-bold text-[#1F8F6A]">תובנה מרכזית</p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {scatter.title}
        </h2>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
          {scatter.subtitle}
        </p>
      </header>

      <div className="border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7">
        <div className="mb-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-[#4E5663]">
          {legendTypes.map((type) => {
            const sample = points.find((p) => p.product.productType === type);
            const label = sample?.product.productTypeLabel ?? type;
            return (
              <span key={type} className="inline-flex items-center gap-1.5">
                <span
                  className="size-3 shrink-0 rounded-full"
                  style={{ backgroundColor: PRODUCT_TYPE_COLORS[type] }}
                />
                {label}
              </span>
            );
          })}
          <span className="text-[#7A817C]">· {scatter.sizeLegend}</span>
        </div>

        {/*
          LTR grid for the plot so axes stay spatially correct:
          plot left · Y labels right (top = less processing, bottom = more)
        */}
        <div className="mx-auto w-full max-w-3xl" dir="ltr">
          <div className="grid grid-cols-[minmax(0,1fr)_7.5rem] grid-rows-[auto_minmax(0,1fr)_auto] items-stretch gap-x-3 sm:grid-cols-[minmax(0,1fr)_9rem] sm:gap-x-4">
            <div className="col-start-1 row-start-1" aria-hidden />

            <div className="col-start-2 row-start-1 self-start pb-2 text-right text-xs leading-snug">
              <p className="font-bold text-[#111318]">{scatter.yHigh}</p>
              <p className="mt-0.5 text-[#7A817C]">{scatter.yHighHint}</p>
            </div>

            <div className="col-start-1 row-start-2 min-w-0 self-center">
              <svg
                viewBox={`0 0 ${PLOT_W} ${PLOT_H}`}
                width="100%"
                height="auto"
                className="block w-full"
                preserveAspectRatio="xMidYMid meet"
                role="img"
                aria-label={`מפת ${points.length} מוצרים לפי מורכבות רכיבים ורמת עיבוד`}
              >
                <rect
                  x={0}
                  y={0}
                  width={PLOT_W}
                  height={PLOT_H}
                  fill="#F7F7F2"
                  stroke="rgba(0,0,0,0.08)"
                  strokeWidth={1}
                  rx={2}
                />
                <line
                  x1={midX}
                  y1={0}
                  x2={midX}
                  y2={PLOT_H}
                  stroke="rgba(0,0,0,0.06)"
                  strokeWidth={1}
                  strokeDasharray="4 4"
                />
                <line
                  x1={0}
                  y1={midY}
                  x2={PLOT_W}
                  y2={midY}
                  stroke="rgba(0,0,0,0.06)"
                  strokeWidth={1}
                  strokeDasharray="4 4"
                />
                {placed.map((p) => {
                  const isActive = hovered === p.product.barcode;
                  const color = PRODUCT_TYPE_COLORS[p.product.productType];
                  return (
                    <g
                      key={p.product.barcode}
                      onMouseEnter={() => setHovered(p.product.barcode)}
                      onMouseLeave={() => setHovered(null)}
                      onFocus={() => setHovered(p.product.barcode)}
                      onBlur={() => setHovered(null)}
                      style={{ cursor: "pointer" }}
                    >
                      {isActive ? (
                        <circle
                          cx={p.cx}
                          cy={p.cy}
                          r={p.r + 5}
                          fill={color}
                          opacity={0.18}
                        />
                      ) : null}
                      <circle
                        cx={p.cx}
                        cy={p.cy}
                        r={p.r}
                        fill={color}
                        stroke={isActive ? "#111318" : "#FFFFFF"}
                        strokeWidth={isActive ? 2 : 1.5}
                        opacity={hovered && !isActive ? 0.45 : 1}
                      />
                    </g>
                  );
                })}
              </svg>
            </div>

            <div className="col-start-2 row-start-2 flex items-center justify-center px-1">
              <p
                className="text-center text-[10px] font-bold uppercase leading-tight tracking-wide text-[#1F8F6A] sm:text-[11px]"
                style={{ writingMode: "vertical-rl" }}
              >
                {scatter.yAxisTitle}
              </p>
            </div>

            <div className="col-start-1 row-start-3" aria-hidden />

            <div className="col-start-2 row-start-3 self-end pt-2 text-right text-xs leading-snug">
              <p className="font-bold text-[#111318]">{scatter.yLow}</p>
              <p className="mt-0.5 text-[#7A817C]">{scatter.yLowHint}</p>
            </div>
          </div>

          <div className="mt-5 border-t border-black/[0.06] pt-4">
            <p className="text-center text-[10px] font-bold uppercase tracking-wide text-[#1F8F6A] sm:text-xs">
              {scatter.xAxisTitle}
            </p>
            <div className="mt-3 flex justify-between gap-6 text-xs leading-snug">
              <div className="max-w-[46%] text-left">
                <p className="font-bold text-[#111318]">{scatter.xComplex}</p>
                <p className="mt-0.5 text-[#7A817C]">{scatter.xComplexHint}</p>
              </div>
              <div className="max-w-[46%] text-right">
                <p className="font-bold text-[#111318]">{scatter.xSimple}</p>
                <p className="mt-0.5 text-[#7A817C]">{scatter.xSimpleHint}</p>
              </div>
            </div>
          </div>
        </div>

        {active ? (
          <div className="mt-4 rounded-lg border border-black/[0.06] bg-[#F7F7F2]/60 px-4 py-3">
            <p className="text-sm font-bold text-[#111318]">{active.label}</p>
            <p className="mt-1 text-sm leading-relaxed text-[#4E5663]">
              {active.placementInsight}
            </p>
            <p className="mt-2 text-xs text-[#7A817C]">
              ציון Bari {active.product.score} · {active.product.productTypeLabel} ·{" "}
              {active.ingredientCount} רכיבים ברשימה
            </p>
          </div>
        ) : (
          <p className="mt-4 text-xs text-[#7A817C]">
            העבירו את העכבר על נקודה לשם המוצר והסבר קצר למיקום
          </p>
        )}

        <ul className="mt-6 grid gap-3 border-t border-black/[0.06] pt-5 md:grid-cols-3">
          {scatter.editorialNotes.map((note) => (
            <li
              key={note}
              className="border-r-2 border-[#1F8F6A]/40 pr-3 text-sm leading-snug text-[#4E5663]"
            >
              {note}
            </li>
          ))}
        </ul>

        <p className="mt-5 text-sm leading-relaxed text-[#7A817C]">{scatter.footnote}</p>
      </div>
    </section>
  );
}
