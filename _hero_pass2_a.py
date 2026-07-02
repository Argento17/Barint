# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(r"c:\Bari\bari-web\src")

# --- hero-still-life-products.ts ---
(ROOT / "lib/home/hero-still-life-products.ts").write_text(r'''/** Grocery still-life packs for homepage hero (scrape URLs, decorative only). */
const CL =
  "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/";

export interface StillLifeProduct {
  id: string;
  name: string;
  imageUrl: string;
  imageAlt: string;
  /** Absolute layout within the hero stage (percent-based). */
  layout: {
    top: string;
    left: string;
    width: string;
    rotate: string;
    zIndex: number;
  };
}

/** Brief mix: cereal, granola, yogurt, plant milk, olive oil, protein bar. */
export const HERO_STILL_LIFE_PRODUCTS: StillLifeProduct[] = [
  {
    id: "granola",
    name: "\u05d2\u05e8\u05e0\u05d5\u05dc\u05d4",
    imageUrl: CL + "ARO54_Z_P_7290017962047_1.png",
    imageAlt: "\u05d2\u05e8\u05e0\u05d5\u05dc\u05d4",
    layout: { top: "6%", left: "38%", width: "30%", rotate: "-7deg", zIndex: 1 },
  },
  {
    id: "vitabix",
    name: "\u05d5\u05d9\u05d8\u05d1\u05d9\u05e7\u05e1",
    imageUrl: CL + "KAG24_Z_P_5010029000061_1.png",
    imageAlt: "\u05d5\u05d9\u05d8\u05d1\u05d9\u05e7\u05e1 \u05d3\u05d2\u05e0\u05d9 \u05d1\u05d5\u05e7\u05e8",
    layout: { top: "26%", left: "44%", width: "34%", rotate: "5deg", zIndex: 3 },
  },
  {
    id: "yogurt",
    name: "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8",
    imageUrl: CL + "UVF46_Z_P_7290102393190_1.png",
    imageAlt: "\u05d9\u05d5\u05d2\u05d5\u05e8\u05d8",
    layout: { top: "54%", left: "14%", width: "24%", rotate: "-9deg", zIndex: 2 },
  },
  {
    id: "oat-milk",
    name: "\u05de\u05e9\u05e7\u05d4 \u05e9\u05d9\u05d1\u05d5\u05dc\u05ea \u05e9\u05d5\u05e2\u05dc",
    imageUrl: CL + "BAC42_Z_P_5411188135005_1.png",
    imageAlt: "\u05de\u05e9\u05e7\u05d4 \u05e9\u05d9\u05d1\u05d5\u05dc\u05ea \u05e9\u05d5\u05e2\u05dc",
    layout: { top: "12%", left: "6%", width: "22%", rotate: "6deg", zIndex: 2 },
  },
  {
    id: "olive-oil",
    name: "\u05e9\u05de\u05df \u05d6\u05d9\u05ea",
    imageUrl: CL + "III56_Z_P_7290017334479_1.png",
    imageAlt: "\u05e9\u05de\u05df \u05d6\u05d9\u05ea",
    layout: { top: "4%", left: "66%", width: "20%", rotate: "-5deg", zIndex: 2 },
  },
  {
    id: "protein-bar",
    name: "\u05d7\u05d8\u05d9\u05e3 \u05d7\u05dc\u05d1\u05d5\u05df",
    imageUrl: CL + "RED52_Z_P_7290121161886_1.png",
    imageAlt: "\u05d7\u05d8\u05d9\u05e3 \u05d7\u05dc\u05d1\u05d5\u05df",
    layout: { top: "58%", left: "58%", width: "28%", rotate: "8deg", zIndex: 4 },
  },
];
''', encoding="utf-8")

# --- hero-decorative-score-ring.tsx ---
(ROOT / "components/home/hero-decorative-score-ring.tsx").write_text(r'''"use client";

/** Illustrative circular score for hero still-life (real Vitabix score 75 B). */
export function HeroDecorativeScoreRing({
  score,
  grade,
  className = "",
}: {
  score: number;
  grade: string;
  className?: string;
}) {
  const size = 72;
  const r = 28;
  const c = 2 * Math.PI * r;
  const offset = c * (1 - score / 100);

  return (
    <div
      className={`relative flex items-center justify-center rounded-full bg-white/95 shadow-[0_12px_32px_-12px_rgba(17,19,24,0.22)] ring-1 ring-black/[0.06] backdrop-blur-sm ${className}`}
      style={{ width: size, height: size }}
      aria-hidden
    >
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="absolute inset-0 -rotate-90"
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="#E8ECE9"
          strokeWidth={5}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="#1F8F6A"
          strokeWidth={5}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="relative flex flex-col items-center leading-none">
        <span className="text-lg font-extrabold tabular-nums text-[#167A58]">{score}</span>
        <span className="mt-0.5 text-[10px] font-bold text-[#4E5663]">{grade}</span>
      </div>
    </div>
  );
}
''', encoding="utf-8")

# --- hero-decorative-radar.tsx ---
(ROOT / "components/home/hero-decorative-radar.tsx").write_text(r'''"use client";

/** Small decorative radar card for hero — illustrative only, not live scoring. */
const AXES = [
  { label: "\u05e8\u05db\u05d9\u05d1\u05d9\u05dd", value: 0.78 },
  { label: "\u05e2\u05d9\u05d1\u05d5\u05d3", value: 0.62 },
  { label: "\u05e1\u05d5\u05db\u05e8", value: 0.35 },
  { label: "\u05e0\u05ea\u05e8\u05df", value: 0.55 },
  { label: "\u05e1\u05d9\u05d1\u05d9\u05dd", value: 0.7 },
];

function polar(cx: number, cy: number, radius: number, index: number, total: number) {
  const angle = (Math.PI * 2 * index) / total - Math.PI / 2;
  return {
    x: cx + radius * Math.cos(angle),
    y: cy + radius * Math.sin(angle),
  };
}

export function HeroDecorativeRadar({ className = "" }: { className?: string }) {
  const cx = 60;
  const cy = 60;
  const total = AXES.length;
  const productPoints = AXES.map((axis, i) =>
    polar(cx, cy, 38 * axis.value, i, total)
  );
  const polygon = productPoints.map((p) => `${p.x},${p.y}`).join(" ");

  return (
    <div
      className={`rounded-2xl border border-black/[0.06] bg-white/92 p-3 shadow-[0_16px_40px_-18px_rgba(17,19,24,0.2)] backdrop-blur-md ${className}`}
      aria-hidden
    >
      <p className="mb-2 text-[10px] font-bold text-[#167A58]">\u05e0\u05d9\u05ea\u05d5\u05d7 \u05de\u05d5\u05e6\u05e8</p>
      <svg viewBox="0 0 120 120" className="h-[88px] w-[88px]" role="img">
        <g className="text-[#111318]/10">
          {[0.33, 0.66, 1].map((level) => (
            <polygon
              key={level}
              points={AXES.map((_, i) => {
                const p = polar(cx, cy, 38 * level, i, total);
                return `${p.x},${p.y}`;
              }).join(" ")}
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
            />
          ))}
          {AXES.map((_, i) => {
            const end = polar(cx, cy, 38, i, total);
            return (
              <line
                key={i}
                x1={cx}
                y1={cy}
                x2={end.x}
                y2={end.y}
                stroke="currentColor"
                strokeWidth="1"
              />
            );
          })}
        </g>
        <polygon
          points={polygon}
          fill="rgba(31,143,106,0.12)"
          stroke="#1F8F6A"
          strokeWidth="2"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}
''', encoding="utf-8")

print("wrote lib + decorative components")
