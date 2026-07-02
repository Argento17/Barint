"use client";

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
      <p className="mb-2 text-[10px] font-bold text-[#167A58]">ניתוח מוצר</p>
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
