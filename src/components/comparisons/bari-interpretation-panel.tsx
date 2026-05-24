"use client";

import type { BariInterpretationPillar } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

const STRENGTH_STYLES: Record<string, { bar: string; text: string }> = {
  חזק: { bar: "bg-[#1F8F6A]", text: "text-[#1F8F6A]" },
  בינוני: { bar: "bg-[#5A9E7E]", text: "text-[#4E5663]" },
  חלש: { bar: "bg-[#C4A574]", text: "text-[#7A817C]" },
  נמוך: { bar: "bg-[#C97B6B]", text: "text-[#7A817C]" },
};

function PillarRow({ pillar }: { pillar: BariInterpretationPillar }) {
  const styles = STRENGTH_STYLES[pillar.strength] ?? STRENGTH_STYLES.בינוני;
  const width = Math.max(8, Math.min(100, pillar.score));

  return (
    <div className="space-y-2 border-b border-black/[0.05] py-4 last:border-0 last:pb-0">
      <div className="flex items-baseline justify-between gap-3">
        <p className="text-sm font-bold text-[#111318]">{pillar.label}</p>
        <span className={cn("text-xs font-semibold", styles.text)}>{pillar.strength}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-[#F7F7F2]">
        <div
          className={cn("h-full rounded-full", styles.bar)}
          style={{ width: `${width}%` }}
        />
      </div>
      <p className="text-sm leading-relaxed text-[#4E5663]">{pillar.interpretation}</p>
    </div>
  );
}

export function BariInterpretationPanel({ pillars }: { pillars: BariInterpretationPillar[] }) {
  return (
    <div className="rounded-xl bg-[#F7F7F2]/60 px-4 py-1">
      {pillars.map((pillar) => (
        <PillarRow key={pillar.key} pillar={pillar} />
      ))}
    </div>
  );
}
