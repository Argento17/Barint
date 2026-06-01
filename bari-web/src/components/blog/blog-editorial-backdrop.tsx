"use client";

import { useId } from "react";

/** Subtle editorial grid + wave texture for blog hub */
export function BlogEditorialBackdrop() {
  const uid = useId().replace(/:/g, "");

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden>
      <svg
        className="absolute inset-0 h-full w-full text-[#1F8F6A]"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <pattern id={`blog-grid-${uid}`} width={40} height={40} patternUnits="userSpaceOnUse">
            <path
              d="M 40 0 L 0 0 0 40"
              fill="none"
              stroke="currentColor"
              strokeOpacity={0.045}
              strokeWidth={0.5}
            />
          </pattern>
          <pattern id={`blog-grid-fine-${uid}`} width={10} height={10} patternUnits="userSpaceOnUse">
            <path
              d="M 10 0 L 0 0 0 10"
              fill="none"
              stroke="#9AA699"
              strokeOpacity={0.028}
              strokeWidth={0.35}
            />
          </pattern>
          <linearGradient id={`blog-fade-${uid}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#F7F7F2" stopOpacity={0} />
            <stop offset="55%" stopColor="#F7F7F2" stopOpacity={0.65} />
            <stop offset="100%" stopColor="#F7F7F2" stopOpacity={1} />
          </linearGradient>
          <radialGradient id={`blog-glow-${uid}`} cx="72%" cy="8%" r="45%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.9} />
            <stop offset="100%" stopColor="#F7F7F2" stopOpacity={0} />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill={`url(#blog-grid-${uid})`} />
        <rect width="100%" height="100%" fill={`url(#blog-grid-fine-${uid})`} />
        <rect width="100%" height="100%" fill={`url(#blog-glow-${uid})`} />
        <path
          d="M -40 120 Q 200 200 480 140 T 920 100"
          fill="none"
          stroke="currentColor"
          strokeOpacity={0.08}
          strokeWidth={1.2}
        />
        <path
          d="M 0 280 C 180 340 360 260 560 300 S 880 360 1000 320"
          fill="none"
          stroke="#B5CFC3"
          strokeOpacity={0.35}
          strokeWidth={48}
        />
        <rect width="100%" height="100%" fill={`url(#blog-fade-${uid})`} />
      </svg>
      <div className="absolute inset-x-0 top-[42%] h-px bg-gradient-to-l from-transparent via-black/[0.07] to-transparent" />
    </div>
  );
}
