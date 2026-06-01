"use client";

import { useId } from "react";
import { motion } from "framer-motion";

export function ComparisonIntelligenceBackdrop() {
  const uid = useId().replace(/:/g, "");

  return (
    <svg
      className="pointer-events-none absolute inset-0 h-full w-full text-[#1F8F6A]"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
    >
      <defs>
        <linearGradient id={`cmp-wave-a-${uid}`} x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="currentColor" stopOpacity="0" />
          <stop offset="38%" stopColor="currentColor" stopOpacity="0.09" />
          <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
        <linearGradient id={`cmp-wave-b-${uid}`} x1="50%" x2="50%" y1="0%" y2="100%">
          <stop offset="0%" stopColor="#FAFAF6" />
          <stop offset="50%" stopColor="#F7F7F2" stopOpacity={0} />
          <stop offset="100%" stopColor="#E4EEE7" stopOpacity={0.32} />
        </linearGradient>
        <radialGradient id={`cmp-spot-${uid}`} cx="28%" cy="20%" r="58%">
          <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.95} />
          <stop offset="42%" stopColor="#F7F7F2" stopOpacity={0.3} />
          <stop offset="100%" stopColor="#F7F7F2" stopOpacity={0} />
        </radialGradient>
        <pattern id={`cmp-grid-${uid}`} width={32} height={32} patternUnits="userSpaceOnUse">
          <path
            d="M 32 0 L 0 0 0 32"
            fill="none"
            stroke="currentColor"
            strokeOpacity="0.065"
            strokeWidth="0.45"
          />
        </pattern>
        <pattern id={`cmp-grid-fine-${uid}`} width={8} height={8} patternUnits="userSpaceOnUse">
          <path
            d="M 8 0 L 0 0 0 8"
            fill="none"
            stroke="#9AA699"
            strokeOpacity="0.035"
            strokeWidth="0.35"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill={`url(#cmp-grid-${uid})`} />
      <rect width="100%" height="100%" fill={`url(#cmp-grid-fine-${uid})`} opacity={0.7} />
      <rect width="100%" height="100%" fill={`url(#cmp-spot-${uid})`} />
      <g opacity={0.5} stroke="#8A968F" strokeOpacity={0.14} strokeWidth="0.6">
        <line x1="4%" y1="22%" x2="96%" y2="22%" strokeDasharray="4 14" />
        <line x1="8%" y1="52%" x2="94%" y2="50%" strokeDasharray="3 12" />
        <line x1="12%" y1="78%" x2="88%" y2="76%" strokeDasharray="5 16" />
      </g>
      <path
        d="M -8 42 C 85 88 160 14 276 52 S 442 118 514 74 S 688 -12 792 62"
        fill="none"
        stroke="currentColor"
        strokeOpacity={0.14}
        strokeWidth={1.45}
      />
      <path
        d="M -4 118 C 120 154 212 92 348 134 S 512 218 596 174 S 760 126 836 148"
        fill="none"
        stroke="#B5CFC3"
        strokeOpacity={0.48}
        strokeWidth={15}
      />
      <ellipse cx="86%" cy="78%" rx="38%" ry="22%" fill={`url(#cmp-wave-b-${uid})`} opacity={0.28} />
      <path
        d="M -20 268 Q 420 348 940 236"
        fill="none"
        stroke={`url(#cmp-wave-a-${uid})`}
        strokeWidth={102}
        opacity={0.55}
      />
    </svg>
  );
}

export function ComparisonAnalysisParticles({
  reduceMotion,
}: {
  reduceMotion: boolean | null;
}) {
  const seeds = [12, 28, 44, 58, 72, 88, 22, 66, 38, 91];
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden>
      {seeds.map((left, i) => (
        <motion.span
          key={i}
          className="absolute size-[2.5px] rounded-full bg-[#1F8F6A]"
          style={{ left: `${left}%`, top: `${22 + (i % 4) * 14}%` }}
          animate={
            reduceMotion ? { opacity: 0.12 } : { opacity: [0.08, 0.22, 0.1, 0.18, 0.08] }
          }
          transition={
            reduceMotion
              ? undefined
              : { duration: 8 + i * 0.55, repeat: Infinity, ease: "easeInOut" }
          }
        />
      ))}
    </div>
  );
}
