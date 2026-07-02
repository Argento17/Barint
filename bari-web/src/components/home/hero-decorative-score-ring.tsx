"use client";

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
