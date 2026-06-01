"use client";

import { motion, useReducedMotion } from "framer-motion";

import { GRADE_COLORS } from "@/lib/comparisons/milk-page-data";
import type { BariGrade } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

export function AnimatedScoreRing({
  score,
  grade,
  size = 88,
  className,
}: {
  score: number;
  grade: BariGrade;
  size?: number;
  className?: string;
}) {
  const reduceMotion = useReducedMotion();
  const colors = GRADE_COLORS[grade] ?? GRADE_COLORS.C;
  const r = (size - 10) / 2;
  const circumference = 2 * Math.PI * r;
  const targetOffset = circumference - (score / 100) * circumference;

  return (
    <div
      className={cn("relative inline-flex items-center justify-center", className)}
      style={{ width: size, height: size }}
    >
      <div
        className="absolute inset-0 rounded-full opacity-40 blur-md"
        style={{ backgroundColor: colors.bg }}
        aria-hidden
      />
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="rgba(255,255,255,0.12)"
          strokeWidth={5}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={colors.bg}
          strokeWidth={5}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={reduceMotion ? { strokeDashoffset: targetOffset } : { strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: targetOffset }}
          transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
        />
      </svg>
      <span
        className="relative text-xl font-extrabold tabular-nums text-[#F7F7F2]"
        aria-label={`ציון ${Math.round(score)}`}
      >
        {Math.round(score)}
      </span>
    </div>
  );
}
