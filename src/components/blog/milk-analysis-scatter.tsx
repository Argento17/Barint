"use client";

import { useMemo, useState } from "react";

import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import {
  PRODUCT_TYPE_COLORS,
  SCATTER_EDITORIAL_NOTES,
  buildScatterPoints,
  type ScatterPoint,
} from "@/lib/blog/milk-analysis-chart-data";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";
import { formatGram, formatIngredientCount, formatScore } from "@/lib/format/numbers";
import type { ProductType } from "@/lib/comparisons/milk-types";

const PLOT_W = 760;
const PLOT_H = 500;
const PAD_X = 34;
const PAD_Y = 28;
const INNER_W = PLOT_W - PAD_X * 2;
const INNER_H = PLOT_H - PAD_Y * 2;

const LEGEND_ORDER: ProductType[] = [
  "dairy",
  "soy",
  "oat",
  "almond",
  "rice",
  "coconut",
  "other_plant",
];

type PlacedPoint = ScatterPoint & { cx: number; cy: number; r: number };

function scale(value: number, min: number, max: number): number {
  if (max === min) return 0.5;
  return (value - min) / (max - min);
}

function dotRadius(ingredientCount: number): number {
  return Math.min(14, Math.max(6.5, 4.5 + ingredientCount * 0.7));
}

function separateOverlapping(points: PlacedPoint[]): PlacedPoint[] {
  const out = points.map((p) => ({ ...p }));
  const minGap = 14;

  for (let pass = 0; pass < 5; pass++) {
    for (let i = 0; i < out.length; i++) {
      for (let j = i + 1; j < out.length; j++) {
        const a = out[i]!;
        const b = out[j]!;
        const dx = b.cx - a.cx;
        const dy = b.cy - a.cy;
        const dist = Math.hypot(dx, dy) || 0.01;
        const need = minGap + a.r + b.r - dist;
        if (need <= 0) continue;

        const ux = dx / dist;
        const uy = dy / dist;
        const push = need / 2;

        a.cx = Math.max(PAD_X + a.r, Math.min(PLOT_W - PAD_X - a.r, a.cx - ux * push));
        a.cy = Math.max(PAD_Y + a.r, Math.min(PLOT_H - PAD_Y - a.r, a.cy - uy * push));
        b.cx = Math.max(PAD_X + b.r, Math.min(PLOT_W - PAD_X - b.r, b.cx + ux * push));
        b.cy = Math.max(PAD_Y + b.r, Math.min(PLOT_H - PAD_Y - b.r, b.cy + uy * push));
      }
    }
  }

  return out;
}

function getProcessingBand(value: number): string {
  if (value < 33) return "עיבוד נמוך";
  if (value < 66) return "עיבוד בינוני";
  return "עיבוד גבוה";
}

function getProteinBand(value: number, max: number): string {
  if (value >= max * 0.7) return "חלבון גבוה";
  if (value >= max * 0.4) return "חלבון בינוני";
  return "חלבון נמוך";
}

export function MilkAnalysisScatter() {
  const { scatter } = milkAnalysisArticle;
  const points = useMemo(() => buildScatterPoints(), []);
  const [hovered, setHovered] = useState<string | null>(null);
  const [pinned, setPinned] = useState<string | null>(null);

  const legendTypes = useMemo(() => {
    const present = new Set(points.map((p) => p.product.productType));
    return LEGEND_ORDER.filter((t) => present.has(t));
  }, [points]);

  const proteinMax = useMemo(
    () => Math.max(...points.map((p) => p.proteinLevel), 0) + 0.35,
    [points]
  );

  const placed = useMemo((): PlacedPoint[] => {
    const xs = points.map((p) => p.processingIntensity);
    const ys = points.map((p) => p.proteinLevel);
    const minX = Math.max(0, Math.min(...xs) - 5);
    const maxX = Math.min(100, Math.max(...xs) + 5);
    const minY = 0;
    const maxY = Math.max(...ys, 0) + 0.35;

    const raw = points.map((p) => {
      const tX = scale(p.processingIntensity, minX, maxX);
      const tY = scale(p.proteinLevel, minY, maxY);
      const cx = PAD_X + INNER_W * tX;
      const cy = PAD_Y + INNER_H * (1 - tY);
      return { ...p, cx, cy, r: dotRadius(p.ingredientCount) };
    });

    return separateOverlapping(raw);
  }, [points]);

  const activeBarcode = pinned ?? hovered;
  const active = placed.find((p) => p.product.barcode === activeBarcode);
  const midX = PLOT_W / 2;
  const midY = PLOT_H / 2;

  return (
    <section id="shelf-map" className="scroll-mt-24">
      <header className="mb-6 md:mb-8">
        <p className="text-sm font-bold text-[#1F8F6A]">תובנה מרכזית</p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {scatter.title}
        </h2>
        <p className="mt-3 max-w-3xl text-base leading-relaxed text-[#4E5663]">
          {scatter.subtitle}
        </p>
      </header>

      <div className="rounded-[1.2rem] border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7">
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

        <div className="mb-4 flex flex-wrap items-center justify-between gap-3 text-[0.7rem] font-semibold text-[#7A817C]">
          <span>{scatter.yAxisTitle}</span>
          <span>{scatter.xAxisTitle}</span>
        </div>

        <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_18rem] lg:items-start">
          <div className="min-w-0">
            <div className="mx-auto w-full max-w-[54rem]" dir="ltr">
              <div className="relative pl-9">
                <div className="pointer-events-none absolute inset-y-2 left-0 flex flex-col justify-between text-[11px] font-bold text-[#4E5663]">
                  <span>{scatter.yHigh}</span>
                  <span>{scatter.yLow}</span>
                </div>

                <div className="pointer-events-none absolute left-12 top-3 z-10 rounded-full border border-[#1F8F6A]/14 bg-[#1F8F6A]/8 px-2.5 py-1 text-[11px] font-bold text-[#1F8F6A]">
                  יותר חלבון · פחות עיבוד
                </div>
                <div className="pointer-events-none absolute bottom-3 right-3 z-10 rounded-full border border-black/[0.08] bg-[#111318]/[0.05] px-2.5 py-1 text-[11px] font-semibold text-[#4E5663]">
                  פחות חלבון · יותר עיבוד
                </div>

                <svg
                  viewBox={`0 0 ${PLOT_W} ${PLOT_H}`}
                  width="100%"
                  height="auto"
                  className="block w-full rounded-[1rem] border border-black/[0.06]"
                  preserveAspectRatio="xMidYMid meet"
                  role="img"
                  aria-label={`מפת ${points.length} מוצרים לפי עיבוד וחלבון`}
                >
                  <rect x={0} y={0} width={PLOT_W} height={PLOT_H} fill="#F7F7F2" rx={12} />

                  <rect
                    x={PAD_X}
                    y={PAD_Y}
                    width={INNER_W / 2}
                    height={INNER_H / 2}
                    fill="#1F8F6A"
                    opacity={0.07}
                    rx={8}
                  />
                  <rect
                    x={midX}
                    y={midY}
                    width={INNER_W / 2}
                    height={INNER_H / 2}
                    fill="#111318"
                    opacity={0.045}
                    rx={8}
                  />

                  <line
                    x1={midX}
                    y1={PAD_Y}
                    x2={midX}
                    y2={PLOT_H - PAD_Y}
                    stroke="rgba(0,0,0,0.09)"
                    strokeWidth={1}
                    strokeDasharray="4 4"
                  />
                  <line
                    x1={PAD_X}
                    y1={midY}
                    x2={PLOT_W - PAD_X}
                    y2={midY}
                    stroke="rgba(0,0,0,0.09)"
                    strokeWidth={1}
                    strokeDasharray="4 4"
                  />

                  {placed.map((p) => {
                    const isActive = activeBarcode === p.product.barcode;
                    const color = PRODUCT_TYPE_COLORS[p.product.productType];
                    return (
                      <g
                        key={p.product.barcode}
                        tabIndex={0}
                        role="button"
                        aria-label={`${p.label}, ${p.product.productTypeLabel}`}
                        onMouseEnter={() => setHovered(p.product.barcode)}
                        onMouseLeave={() => setHovered(null)}
                        onFocus={() => setHovered(p.product.barcode)}
                        onBlur={() => setHovered(null)}
                        onClick={() =>
                          setPinned((prev) => (prev === p.product.barcode ? null : p.product.barcode))
                        }
                        onKeyDown={(event) => {
                          if (event.key === "Enter" || event.key === " ") {
                            event.preventDefault();
                            setPinned((prev) =>
                              prev === p.product.barcode ? null : p.product.barcode
                            );
                          }
                        }}
                        style={{ cursor: "pointer" }}
                      >
                        {pinned === p.product.barcode ? (
                          <circle
                            cx={p.cx}
                            cy={p.cy}
                            r={p.r + 9}
                            fill="none"
                            stroke={color}
                            strokeWidth={1.5}
                            opacity={0.35}
                            strokeDasharray="4 4"
                          />
                        ) : null}
                        {isActive ? (
                          <circle cx={p.cx} cy={p.cy} r={p.r + 6} fill={color} opacity={0.18} />
                        ) : null}
                        <circle
                          cx={p.cx}
                          cy={p.cy}
                          r={p.r}
                          fill={color}
                          stroke={isActive ? "#111318" : "#FFFFFF"}
                          strokeWidth={isActive ? 2.25 : 1.5}
                          opacity={activeBarcode && !isActive ? 0.42 : 1}
                        />
                      </g>
                    );
                  })}
                </svg>
              </div>

              <div className="mt-3 flex items-center justify-between text-xs font-semibold text-[#4E5663]">
                <span>{scatter.xSimple}</span>
                <span>{scatter.xComplex}</span>
              </div>
              <p className="mt-1 text-center text-[0.65rem] leading-snug text-[#7A817C]">
                {scatter.xSimpleHint} · {scatter.yHighHint}
              </p>
              <p className="mt-1 text-center text-[0.65rem] leading-snug text-[#7A817C]">
                {scatter.xComplexHint} · {scatter.yLowHint}
              </p>
            </div>
          </div>

          <aside className="rounded-[1.1rem] border border-black/[0.06] bg-[#F7F7F2]/70 p-4 md:p-5">
            {active ? (
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <ProductThumbnail
                    product={active.product}
                    size="lg"
                    wrapperClassName="w-20 md:w-24 aspect-[3/5] rounded-[0.9rem]"
                    imageClassName="p-1.5"
                    imageSizes="96px"
                  />

                  <div className="min-w-0 flex-1">
                    <p className="text-[0.65rem] font-bold text-[#1F8F6A]">
                      {active.product.productTypeLabel}
                    </p>
                    <h3 className="mt-1 text-base font-extrabold leading-snug text-[#111318]">
                      {active.label}
                    </h3>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      <span className="rounded-full bg-[#111318] px-2.5 py-0.5 text-[0.65rem] font-extrabold text-[#F7F7F2]">
                        ציון {formatScore(active.product.score)}
                      </span>
                      <span className="rounded-full border border-black/[0.08] bg-[#FFFFFF]/80 px-2.5 py-0.5 text-[0.65rem] font-bold text-[#4E5663]">
                        {getProcessingBand(active.processingIntensity)}
                      </span>
                    </div>
                  </div>
                </div>

                <p className="text-sm leading-relaxed text-[#4E5663]">{active.placementInsight}</p>

                <dl className="grid grid-cols-2 gap-2 text-right text-xs text-[#4E5663]">
                  <div className="rounded-[0.9rem] border border-black/[0.06] bg-[#FFFFFF]/80 px-3 py-2.5">
                    <dt className="font-bold text-[#111318]">חלבון</dt>
                    <dd className="mt-1 font-semibold">
                      {formatGram(active.product.proteinPer100ml, " ג׳ / 100 מ״ל")}
                    </dd>
                  </div>
                  <div className="rounded-[0.9rem] border border-black/[0.06] bg-[#FFFFFF]/80 px-3 py-2.5">
                    <dt className="font-bold text-[#111318]">רכיבים</dt>
                    <dd className="mt-1 font-semibold">
                      {formatIngredientCount(active.ingredientCount)} ברשימה
                    </dd>
                  </div>
                  <div className="rounded-[0.9rem] border border-black/[0.06] bg-[#FFFFFF]/80 px-3 py-2.5">
                    <dt className="font-bold text-[#111318]">מיקום חלבון</dt>
                    <dd className="mt-1 font-semibold">{getProteinBand(active.proteinLevel, proteinMax)}</dd>
                  </div>
                  <div className="rounded-[0.9rem] border border-black/[0.06] bg-[#FFFFFF]/80 px-3 py-2.5">
                    <dt className="font-bold text-[#111318]">נעיצה</dt>
                    <dd className="mt-1 font-semibold">
                      {pinned ? "לחצו שוב לביטול" : "לחצו כדי לקבע"}
                    </dd>
                  </div>
                </dl>
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-sm font-extrabold text-[#111318]">
                  נגעו בנקודות לקבלת פרטים אודות כל מוצר
                </p>
                <p className="text-sm leading-relaxed text-[#4E5663]">
                  רחפו על נקודה כדי לראות את המוצר, התמונה שלו, כמות החלבון והמיקום היחסי על
                  הציר. במובייל אפשר ללחוץ כדי לנעוץ.
                </p>
              </div>
            )}
          </aside>
        </div>

        <ul className="mt-6 grid gap-3 border-t border-black/[0.06] pt-5 md:grid-cols-3">
          {SCATTER_EDITORIAL_NOTES.map((note) => (
            <li
              key={note.title}
              className="rounded-[1rem] border border-black/[0.06] bg-[#F7F7F2]/50 p-4 text-right"
            >
              <p className="text-xs font-bold text-[#1F8F6A]">{note.title}</p>
              <p className="mt-1.5 text-sm leading-snug text-[#4E5663]">{note.text}</p>
            </li>
          ))}
        </ul>

        <p className="mt-5 text-sm leading-relaxed text-[#7A817C]">{scatter.footnote}</p>
      </div>
    </section>
  );
}
